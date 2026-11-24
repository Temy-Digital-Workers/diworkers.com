"""Temy Digital Workers - Microsoft commercial marketplace integration.

Serves, behind nginx on https://diworkers.com:
  GET  /marketplace/landing          landing page (Microsoft redirects buyers here with ?token=)
  GET  /marketplace/auth/callback    Entra ID sign-in callback
  POST /marketplace/activate         activates the resolved subscription (starts billing)
  POST /marketplace/webhook          connection webhook (plan / quantity / suspend / reinstate / unsubscribe)
  GET  /marketplace/healthz          liveness

SaaS Fulfillment API v2:
  https://learn.microsoft.com/partner-center/marketplace-offers/pc-saas-fulfillment-subscription-api
Landing page rules:
  https://learn.microsoft.com/partner-center/marketplace-offers/azure-ad-transactable-saas-landing-page

The app authenticates to the marketplace API with a CERTIFICATE (no client secret exists).
In EMULATOR mode (MARKETPLACE_MODE=emulator) it talks to Microsoft's open-source API emulator
and skips buyer sign-in and webhook JWT checks; that mode is only ever bound to localhost.
"""
from __future__ import annotations

import html
import json
import logging
import os
import secrets
import sqlite3
import time
from contextlib import closing
from pathlib import Path
from urllib.parse import unquote

import httpx
import jwt
import msal
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from itsdangerous import BadSignature, URLSafeSerializer

log = logging.getLogger("marketplace")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

# ---------------------------------------------------------------- config
MODE = os.environ.get("MARKETPLACE_MODE", "live")  # live | emulator
TENANT_ID = os.environ["PUBLISHER_TENANT_ID"]  # our (publisher) Entra tenant
CLIENT_ID = os.environ["CLIENT_ID"]  # the "Temy Digital Workers" multi-tenant app
CERT_KEY = os.environ.get("CERT_KEY_PATH", "/secrets/app.key")
CERT_THUMBPRINT = os.environ.get("CERT_THUMBPRINT", "")
BASE_URL = os.environ.get("BASE_URL", "https://diworkers.com").rstrip("/")
API_BASE = os.environ.get("MARKETPLACE_API_BASE", "https://marketplaceapi.microsoft.com/api").rstrip("/")
API_VERSION = "2018-08-31"
EMULATOR_PUBLISHER_ID = os.environ.get("EMULATOR_PUBLISHER_ID", "TemyDigitalWorkers")
DB_PATH = os.environ.get("DB_PATH", "/data/marketplace.db")
SESSION_SECRET = os.environ["SESSION_SECRET"]
PROVISION_HOOK_URL = os.environ.get("PROVISION_HOOK_URL", "")  # Temy Labs flow trigger (optional)
PROVISION_HOOK_TOKEN = os.environ.get("PROVISION_HOOK_TOKEN", "")
SUPPORT_EMAIL = os.environ.get("SUPPORT_EMAIL", "support@diworkers.com")

MARKETPLACE_RESOURCE = "20e940b3-4c77-4b0b-9a53-9e16a1b010a7"  # Microsoft marketplace API app id
SIGNIN_SCOPES = ["User.Read"]  # openid/profile/email are added by MSAL
REDIRECT_URI = f"{BASE_URL}/marketplace/auth/callback"
COOKIE = "dw_mp"

if MODE not in ("live", "emulator"):
    raise SystemExit(f"bad MARKETPLACE_MODE {MODE!r}")

serializer = URLSafeSerializer(SESSION_SECRET, salt="dw-marketplace")
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


# ---------------------------------------------------------------- storage
SCHEMA = """
CREATE TABLE IF NOT EXISTS subscription (
  id TEXT PRIMARY KEY,
  name TEXT, offer_id TEXT, plan_id TEXT, quantity INTEGER,
  status TEXT,                    -- marketplace saasSubscriptionStatus
  purchaser_email TEXT, purchaser_tenant TEXT,
  beneficiary_email TEXT, beneficiary_tenant TEXT,
  activated_by TEXT,              -- email of the person who pressed Activate
  provisioning TEXT DEFAULT 'none',  -- none | requested | done | failed
  raw TEXT,
  created_at REAL, updated_at REAL
);
CREATE TABLE IF NOT EXISTS webhook_event (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  operation_id TEXT, subscription_id TEXT, action TEXT, status TEXT,
  plan_id TEXT, quantity INTEGER, payload TEXT,
  verified INTEGER, result TEXT, received_at REAL
);
CREATE UNIQUE INDEX IF NOT EXISTS webhook_event_op ON webhook_event(operation_id, action, status);
CREATE TABLE IF NOT EXISTS auth_flow (
  id TEXT PRIMARY KEY, flow TEXT, mp_token TEXT, created_at REAL
);
"""


def db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with closing(db()) as c:
        c.executescript(SCHEMA)
        c.commit()


init_db()


def upsert_subscription(sub: dict, **extra) -> None:
    """Store what the marketplace says about a subscription (resolve / get-subscription shapes)."""
    s = sub.get("subscription", sub)
    sid = sub.get("id") or s.get("id")
    purchaser = s.get("purchaser") or {}
    beneficiary = s.get("beneficiary") or {}
    now = time.time()
    with closing(db()) as c:
        c.execute(
            """INSERT INTO subscription(id,name,offer_id,plan_id,quantity,status,purchaser_email,purchaser_tenant,
                   beneficiary_email,beneficiary_tenant,raw,created_at,updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(id) DO UPDATE SET name=excluded.name, offer_id=excluded.offer_id,
                   plan_id=excluded.plan_id, quantity=excluded.quantity, status=excluded.status,
                   purchaser_email=excluded.purchaser_email, purchaser_tenant=excluded.purchaser_tenant,
                   beneficiary_email=excluded.beneficiary_email, beneficiary_tenant=excluded.beneficiary_tenant,
                   raw=excluded.raw, updated_at=excluded.updated_at""",
            (
                sid,
                sub.get("subscriptionName") or s.get("name"),
                sub.get("offerId") or s.get("offerId"),
                sub.get("planId") or s.get("planId"),
                sub.get("quantity") or s.get("quantity"),
                s.get("saasSubscriptionStatus"),
                purchaser.get("emailId"),
                purchaser.get("tenantId"),
                beneficiary.get("emailId"),
                beneficiary.get("tenantId"),
                json.dumps(sub),
                now,
                now,
            ),
        )
        for k, v in extra.items():
            c.execute(f"UPDATE subscription SET {k}=?, updated_at=? WHERE id=?", (v, now, sid))
        c.commit()


# ---------------------------------------------------------------- marketplace API
_cca: msal.ConfidentialClientApplication | None = None


def cca() -> msal.ConfidentialClientApplication:
    global _cca
    if _cca is None:
        _cca = msal.ConfidentialClientApplication(
            CLIENT_ID,
            authority=f"https://login.microsoftonline.com/{TENANT_ID}",
            client_credential={"private_key": Path(CERT_KEY).read_text(), "thumbprint": CERT_THUMBPRINT},
        )
    return _cca


def signin_app() -> msal.ConfidentialClientApplication:
    """Buyers sign in from ANY work tenant, so the authority is 'organizations'."""
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority="https://login.microsoftonline.com/organizations",
        client_credential={"private_key": Path(CERT_KEY).read_text(), "thumbprint": CERT_THUMBPRINT},
    )


def api_headers() -> dict:
    h = {"Content-Type": "application/json", "x-ms-requestid": secrets.token_hex(16)}
    if MODE == "live":
        res = cca().acquire_token_for_client(scopes=[f"{MARKETPLACE_RESOURCE}/.default"])
        if "access_token" not in res:
            raise RuntimeError(f"marketplace token failed: {res.get('error')}: {res.get('error_description')}")
        h["Authorization"] = f"Bearer {res['access_token']}"
    return h


def api_url(path: str) -> str:
    url = f"{API_BASE}/saas/subscriptions{path}"
    url += ("&" if "?" in url else "?") + f"api-version={API_VERSION}"
    if MODE == "emulator":
        url += f"&publisherId={EMULATOR_PUBLISHER_ID}"
    return url


def api(method: str, path: str, **kw) -> httpx.Response:
    with httpx.Client(timeout=30, follow_redirects=False) as client:
        r = client.request(method, api_url(path), headers={**api_headers(), **kw.pop("headers", {})}, **kw)
    log.info("marketplace %s %s -> %s", method, path.split("?")[0], r.status_code)
    return r


def resolve(mp_token: str) -> dict:
    r = api("POST", "/resolve", headers={"x-ms-marketplace-token": mp_token})
    r.raise_for_status()
    return r.json()


def activate(sub_id: str, plan_id: str, quantity) -> None:
    body = {"planId": plan_id}
    if quantity:
        body["quantity"] = quantity
    r = api("POST", f"/{sub_id}/activate", json=body)
    r.raise_for_status()


def get_subscription(sub_id: str) -> dict:
    r = api("GET", f"/{sub_id}")
    r.raise_for_status()
    return r.json()


def get_operation(sub_id: str, op_id: str) -> dict:
    r = api("GET", f"/{sub_id}/operations/{op_id}")
    r.raise_for_status()
    return r.json()


def patch_operation(sub_id: str, op_id: str, status: str) -> int:
    r = api("PATCH", f"/{sub_id}/operations/{op_id}", json={"status": status})
    return r.status_code


def request_provisioning(sub_id: str, reason: str) -> None:
    """Hand the subscription to Temy Labs. The work itself (create / pause / archive the customer's
    workspace) runs as a flow there, never inside this web process."""
    if not PROVISION_HOOK_URL:
        log.info("provisioning hook not configured; %s for %s recorded only", reason, sub_id)
        return
    with closing(db()) as c:
        row = c.execute("SELECT * FROM subscription WHERE id=?", (sub_id,)).fetchone()
    payload = {"reason": reason, "subscription": dict(row) if row else {"id": sub_id}}
    try:
        with httpx.Client(timeout=15) as client:
            r = client.post(
                PROVISION_HOOK_URL,
                json=payload,
                headers={"Authorization": f"Bearer {PROVISION_HOOK_TOKEN}"} if PROVISION_HOOK_TOKEN else {},
            )
        state = "requested" if r.status_code < 300 else "failed"
        log.info("provisioning hook %s -> %s", reason, r.status_code)
    except httpx.HTTPError as e:
        state = "failed"
        log.warning("provisioning hook error: %s", e)
    with closing(db()) as c:
        c.execute("UPDATE subscription SET provisioning=?, updated_at=? WHERE id=?", (state, time.time(), sub_id))
        c.commit()


# ---------------------------------------------------------------- pages
def page(title: str, body: str, status: int = 200) -> HTMLResponse:
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Temy Digital Workers</title>
<link rel="icon" href="/assets/img/favicon-32.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Hind+Vadodara:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/css/site.css">
<style>
 .mp{{max-width:760px;margin:0 auto;padding:120px 20px 80px}}
 .mp .card{{background:#fff;border:1px solid var(--line,#ebedf3);border-radius:18px;padding:28px;box-shadow:0 10px 30px rgba(52,55,58,.06)}}
 .mp dl{{display:grid;grid-template-columns:180px 1fr;gap:10px 16px;margin:18px 0}}
 .mp dt{{color:var(--grey,#575d72)}} .mp dd{{margin:0;font-weight:600;word-break:break-word}}
 .mp .msbtn{{display:inline-flex;align-items:center;gap:10px;background:#2f2f2f;color:#fff;border:0;border-radius:6px;padding:12px 18px;font:600 15px 'Hind Vadodara',sans-serif;cursor:pointer;text-decoration:none}}
 .mp .ok{{color:#1b7f3b}} .mp .warn{{color:#b45309}} .mp .err{{color:#eb4747}}
 .mp .btn-red{{background:#eb4747;color:#fff;border:0;border-radius:999px;padding:12px 26px;font:700 15px Montserrat,sans-serif;cursor:pointer}}
 @media (max-width:560px){{.mp dl{{grid-template-columns:1fr}}}}
</style></head><body>
<header class="hdr"><div class="wrap"><a class="logo" href="/"><img src="/assets/img/temy-logo.svg" alt="Temy" height="28"></a></div></header>
<main class="mp">{body}</main></body></html>"""
    return HTMLResponse(doc, status_code=status, headers={"Cache-Control": "no-store"})


MS_LOGO = ('<svg width="18" height="18" viewBox="0 0 21 21" aria-hidden="true"><rect width="10" height="10" fill="#f25022"/>'
           '<rect x="11" width="10" height="10" fill="#7fba00"/><rect y="11" width="10" height="10" fill="#00a4ef"/>'
           '<rect x="11" y="11" width="10" height="10" fill="#ffb900"/></svg>')


def session_of(request: Request) -> dict:
    raw = request.cookies.get(COOKIE)
    if not raw:
        return {}
    try:
        return serializer.loads(raw)
    except BadSignature:
        return {}


def with_session(resp, data: dict):
    resp.set_cookie(COOKIE, serializer.dumps(data), httponly=True, secure=BASE_URL.startswith("https"),
                    samesite="lax", max_age=3600, path="/marketplace")
    return resp


def subscription_card(sub: dict, user: dict, csrf: str) -> str:
    s = sub.get("subscription", {})
    e = html.escape
    status = s.get("saasSubscriptionStatus", "")
    rows = [
        ("Subscription", sub.get("subscriptionName") or s.get("name")),
        ("Digital worker (offer)", sub.get("offerId")),
        ("Plan", sub.get("planId")),
        ("Quantity", sub.get("quantity") or s.get("quantity") or "-"),
        ("Purchased by", (s.get("purchaser") or {}).get("emailId")),
        ("For", (s.get("beneficiary") or {}).get("emailId")),
        ("Status", status),
        ("Signed in as", user.get("email") or user.get("name") or "-"),
    ]
    dl = "".join(f"<dt>{e(k)}</dt><dd>{e(str(v or '-'))}</dd>" for k, v in rows)
    if status == "PendingFulfillmentStart":
        action = f"""<form method="post" action="/marketplace/activate">
<input type="hidden" name="csrf" value="{e(csrf)}">
<p>Press <b>Activate</b> to start your subscription. Billing starts at this moment. We then set up your
digital worker and email the next steps to {e((s.get('beneficiary') or {}).get('emailId') or 'you')}.</p>
<button class="btn-red" type="submit">Activate subscription</button></form>"""
    elif status == "Subscribed":
        action = '<p class="ok"><b>This subscription is active.</b> Your digital worker is being set up.</p>'
    else:
        action = f'<p class="warn">This subscription is <b>{e(status)}</b>. Contact {e(SUPPORT_EMAIL)} if this is unexpected.</p>'
    return f'<div class="card"><h1>Welcome to Temy Digital Workers</h1><dl>{dl}</dl>{action}</div>'


@app.get("/marketplace/healthz")
def healthz():
    with closing(db()) as c:
        n = c.execute("SELECT count(*) FROM subscription").fetchone()[0]
    return {"ok": True, "mode": MODE, "subscriptions": n}


@app.get("/marketplace/landing")
@app.get("/marketplace/landing/")
def landing(request: Request, token: str | None = None):
    if not token:
        return page("Get started", f"""<div class="card"><h1>Buy Temy Digital Workers on Microsoft Marketplace</h1>
<p>Temy digital workers are sold through Microsoft Marketplace and billed on your Microsoft invoice.
After you buy one there, Microsoft brings you back to this page to activate it.</p>
<p>Questions: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a> · <a href="/workers">See the digital workers</a></p></div>""")
    mp_token = unquote(token)
    if MODE == "emulator":
        return finish_landing(mp_token, {"email": "emulator@localhost", "name": "Emulator user"})
    # Live: the buyer must sign in with Microsoft Entra ID first (marketplace certification rule).
    flow = signin_app().initiate_auth_code_flow(SIGNIN_SCOPES, redirect_uri=REDIRECT_URI, prompt="select_account")
    fid = secrets.token_urlsafe(24)
    with closing(db()) as c:
        c.execute("DELETE FROM auth_flow WHERE created_at < ?", (time.time() - 3600,))
        c.execute("INSERT INTO auth_flow(id,flow,mp_token,created_at) VALUES(?,?,?,?)",
                  (fid, json.dumps(flow), mp_token, time.time()))
        c.commit()
    return with_session(RedirectResponse(flow["auth_uri"], status_code=302), {"fid": fid})


@app.get("/marketplace/auth/callback")
def auth_callback(request: Request):
    sess = session_of(request)
    fid = sess.get("fid")
    with closing(db()) as c:
        row = c.execute("SELECT * FROM auth_flow WHERE id=?", (fid,)).fetchone() if fid else None
        if row:
            c.execute("DELETE FROM auth_flow WHERE id=?", (fid,))
            c.commit()
    if not row:
        return page("Sign-in expired", '<div class="card"><h1>Your sign-in expired</h1><p>Please open the '
                    'subscription again from Microsoft Marketplace (Configure account now).</p></div>', 400)
    result = signin_app().acquire_token_by_auth_code_flow(json.loads(row["flow"]), dict(request.query_params))
    if "error" in result:
        log.warning("sign-in failed: %s %s", result.get("error"), result.get("error_description"))
        return page("Sign-in failed", f'<div class="card"><h1>Sign-in failed</h1><p class="err">'
                    f'{html.escape(result.get("error_description") or result.get("error"))}</p></div>', 400)
    claims = result.get("id_token_claims", {})
    user = {"email": claims.get("preferred_username") or claims.get("email"), "name": claims.get("name"),
            "tid": claims.get("tid"), "oid": claims.get("oid")}
    return finish_landing(row["mp_token"], user)


def finish_landing(mp_token: str, user: dict):
    try:
        sub = resolve(mp_token)
    except httpx.HTTPStatusError as e:
        log.warning("resolve failed: %s %s", e.response.status_code, e.response.text[:300])
        return page("Purchase not found", '<div class="card"><h1>We could not read this purchase</h1><p>The link may '
                    f'have expired. Open it again from Microsoft Marketplace, or write to {SUPPORT_EMAIL}.</p></div>', 400)
    try:
        full = get_subscription(sub["id"])
        sub["subscription"] = full
    except httpx.HTTPStatusError:
        pass
    upsert_subscription(sub)
    csrf = secrets.token_urlsafe(16)
    resp = page("Activate", subscription_card(sub, user, csrf))
    return with_session(resp, {"sub": sub["id"], "plan": sub.get("planId"), "qty": sub.get("quantity"),
                               "user": user.get("email"), "csrf": csrf})


@app.post("/marketplace/activate")
def do_activate(request: Request, csrf: str = Form(...)):
    sess = session_of(request)
    if not sess.get("sub") or not secrets.compare_digest(sess.get("csrf", ""), csrf):
        return page("Session expired", '<div class="card"><h1>Session expired</h1><p>Open the purchase again from '
                    'Microsoft Marketplace.</p></div>', 400)
    sub_id = sess["sub"]
    try:
        activate(sub_id, sess["plan"], sess.get("qty"))
    except httpx.HTTPStatusError as e:
        log.warning("activate failed: %s %s", e.response.status_code, e.response.text[:300])
        return page("Activation failed", f'<div class="card"><h1>Activation failed</h1><p class="err">Microsoft '
                    f'answered {e.response.status_code}. Please try again or write to {SUPPORT_EMAIL}.</p></div>', 502)
    try:
        upsert_subscription({"id": sub_id, "subscription": get_subscription(sub_id)}, activated_by=sess.get("user"))
    except httpx.HTTPStatusError:
        pass
    request_provisioning(sub_id, "activated")
    return page("Activated", f"""<div class="card"><h1 class="ok">Your subscription is active</h1>
<p>Thank you. We are setting up your digital worker now and will email the next steps within one business day.</p>
<p>Questions: <a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></p></div>""")


# ---------------------------------------------------------------- webhook
_jwks: dict[str, jwt.PyJWKClient] = {}


def verify_webhook_jwt(auth_header: str | None) -> dict:
    """Microsoft calls the webhook with an Entra token: aud = our app id, tid = our tenant,
    issued to the marketplace app. Signature checked against Entra's published keys."""
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise PermissionError("no bearer token")
    token = auth_header.split(" ", 1)[1]
    unverified = jwt.decode(token, options={"verify_signature": False})
    tid = unverified.get("tid")
    if tid != TENANT_ID:
        raise PermissionError(f"wrong tenant {tid}")
    ver = unverified.get("ver", "2.0")
    jwks_url = (f"https://login.microsoftonline.com/{tid}/discovery/v2.0/keys" if ver == "2.0"
                else f"https://login.microsoftonline.com/{tid}/discovery/keys")
    client = _jwks.setdefault(jwks_url, jwt.PyJWKClient(jwks_url))
    key = client.get_signing_key_from_jwt(token)
    issuers = [f"https://login.microsoftonline.com/{tid}/v2.0", f"https://sts.windows.net/{tid}/"]
    claims = jwt.decode(token, key.key, algorithms=["RS256"], audience=[CLIENT_ID, f"api://{CLIENT_ID}"],
                        issuer=issuers)
    caller = claims.get("azp") or claims.get("appid")
    if caller != MARKETPLACE_RESOURCE:
        raise PermissionError(f"token not from the marketplace app ({caller})")
    return claims


def _subscription_exists(sub_id: str) -> bool:
    try:
        get_subscription(sub_id)
        return True
    except httpx.HTTPStatusError:
        return False


@app.post("/marketplace/webhook")
async def webhook(request: Request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return JSONResponse({"error": "bad json"}, status_code=400)
    verified = 0
    if MODE == "live":
        try:
            verify_webhook_jwt(request.headers.get("authorization"))
            verified = 1
        except (PermissionError, jwt.PyJWTError) as e:
            log.warning("webhook rejected: %s", e)
            return JSONResponse({"error": "unauthorized"}, status_code=401)
    op_id, sub_id = body.get("id"), body.get("subscriptionId")
    action, status = body.get("action"), body.get("status")
    log.info("webhook %s %s sub=%s op=%s", action, status, sub_id, op_id)
    # Defence in depth: the payload is only trusted after the operation is confirmed by the API.
    result = "recorded"
    try:
        op = get_operation(sub_id, op_id)
        if op.get("action") != action:
            log.warning("operation mismatch: payload %s vs api %s", action, op.get("action"))
            return JSONResponse({"error": "operation mismatch"}, status_code=400)
    except httpx.HTTPStatusError as e:
        # Microsoft's emulator posts webhook operations it never stores (createOperation in its
        # webhook-api-impl.ts is not persisted), so only the emulator gets a pass, and only when the
        # subscription itself exists there. Live always requires the operation to exist.
        if MODE == "emulator" and e.response.status_code == 404 and _subscription_exists(sub_id):
            result = "recorded (emulator: operation not stored by emulator)"
        else:
            log.warning("operation lookup failed: %s", e.response.status_code)
            return JSONResponse({"error": "unknown operation"}, status_code=400)
    with closing(db()) as c:
        try:
            c.execute("""INSERT INTO webhook_event(operation_id,subscription_id,action,status,plan_id,quantity,payload,
                         verified,result,received_at) VALUES(?,?,?,?,?,?,?,?,?,?)""",
                      (op_id, sub_id, action, status, body.get("planId"), body.get("quantity"), json.dumps(body),
                       verified, result, time.time()))
            c.commit()
        except sqlite3.IntegrityError:
            return {"ok": True, "duplicate": True}  # Microsoft retries; we answer idempotently
    # Plan and quantity changes started in the Azure portal wait for our answer (PATCH the operation).
    if status == "InProgress" and action in ("ChangePlan", "ChangeQuantity", "Reinstate"):
        code = patch_operation(sub_id, op_id, "Success")
        result = f"patched Success ({code})"
    try:
        upsert_subscription({"id": sub_id, "subscription": get_subscription(sub_id)})
    except httpx.HTTPStatusError:
        pass
    reason = {"Unsubscribe": "unsubscribed", "Suspend": "suspended", "Reinstate": "reinstated",
              "ChangePlan": "plan_changed", "ChangeQuantity": "quantity_changed", "Renew": "renewed"}.get(action)
    if reason and status in ("Succeeded", "Success", "InProgress"):
        request_provisioning(sub_id, reason)
    with closing(db()) as c:
        c.execute("UPDATE webhook_event SET result=? WHERE operation_id=? AND action=? AND status=?",
                  (result, op_id, action, status))
        c.commit()
    return {"ok": True}
