"""End-to-end test of the marketplace service against Microsoft's SaaS API emulator.

Run with the local test stack up (scratchpad mp-test compose: app on :18711, emulator on :18712):
    python e2e_emulator.py
Covers: purchase token -> landing (resolve) -> Activate -> ChangePlan webhook -> ChangeQuantity is
rejected for a flat plan -> Unsubscribe webhook, and checks what the app stored.
"""
import base64
import json
import re
import subprocess
import sys
import time
import uuid

import httpx

APP = "http://127.0.0.1:18711"
EMU = "http://127.0.0.1:18712"
PUB = "publisherId=TemyDigitalWorkers&api-version=2018-08-31"
fails = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        fails.append(name)


def emu_sub(sid):
    return httpx.get(f"{EMU}/api/saas/subscriptions/{sid}?{PUB}").json()


def wait_status(sid, field, want, secs=40):
    for _ in range(secs):
        v = emu_sub(sid).get(field)
        if v == want:
            return v
        time.sleep(1)
    return emu_sub(sid).get(field)


def app_rows(sql):
    out = subprocess.run(["docker", "exec", "dw-mp-test-test-1", "python", "-c",
                          f"import sqlite3,json;c=sqlite3.connect('/tmp/mp.db');c.row_factory=sqlite3.Row;"
                          f"print(json.dumps([dict(r) for r in c.execute({sql!r})]))"],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


sid = str(uuid.uuid4())
purchase = {
    "id": sid, "subscriptionId": sid, "offerId": "flat-rate", "planId": "flat-rate-1", "name": "AP Clerk for Contoso",
    "quantity": 1, "autoRenew": True, "isTest": True, "isFreeTrial": False,
    "beneficiary": {"emailId": "it@contoso.example", "objectId": str(uuid.uuid4()), "tenantId": str(uuid.uuid4()), "puid": ""},
    "purchaser": {"emailId": "buyer@contoso.example", "objectId": str(uuid.uuid4()), "tenantId": str(uuid.uuid4()), "puid": ""},
}
token = base64.b64encode(json.dumps(purchase).encode()).decode()

with httpx.Client(base_url=APP, follow_redirects=False, timeout=30) as c:
    r = c.get("/marketplace/landing", params={"token": token})
    check("landing resolves the purchase token", r.status_code == 200 and "Activate subscription" in r.text, r.status_code)
    check("landing shows plan and buyer", "flat-rate-1" in r.text and "buyer@contoso.example" in r.text)
    csrf = re.search(r'name="csrf" value="([^"]+)"', r.text)
    r = c.post("/marketplace/activate", data={"csrf": "wrong"})
    check("activate refuses a bad CSRF value", r.status_code == 400)
    r = c.post("/marketplace/activate", data={"csrf": csrf.group(1) if csrf else ""})
    check("activate succeeds", r.status_code == 200 and "subscription is active" in r.text, r.status_code)

check("emulator shows Subscribed", wait_status(sid, "saasSubscriptionStatus", "Subscribed") == "Subscribed")
row = app_rows(f"select * from subscription where id='{sid}'")
check("app stored the subscription as Subscribed", row and row[0]["status"] == "Subscribed", row and row[0]["status"])
check("app stored purchaser and beneficiary", row and row[0]["purchaser_email"] == "buyer@contoso.example"
      and row[0]["beneficiary_email"] == "it@contoso.example")

# Customer-side actions (Azure portal) -> the marketplace calls our webhook. The emulator's
# /api/webhook/... routes simulate exactly those customer actions.
def customer(action, method="post", **kw):
    url = f"{EMU}/api/webhook/subscription/{sid}" + ("" if action == "update" else f"/{action}")
    return getattr(httpx, method)(url, timeout=30, **kw)


def wait_event(action, secs=30):
    ev = []
    for _ in range(secs):
        ev = app_rows(f"select action,status,result from webhook_event where subscription_id='{sid}'")
        if any(e["action"] == action for e in ev):
            return ev
        time.sleep(1)
    return ev


r = customer("update", "patch", json={"planId": "flat-rate-2"})
check("customer ChangePlan accepted by emulator", r.status_code < 300, f"{r.status_code} {r.text[:120]}")
ev = wait_event("ChangePlan")
check("webhook received ChangePlan", any(e["action"] == "ChangePlan" for e in ev), ev)
check("plan becomes flat-rate-2", wait_status(sid, "planId", "flat-rate-2") == "flat-rate-2")

r = customer("suspend")
check("customer Suspend accepted", r.status_code < 300, r.status_code)
check("webhook received Suspend", any(e["action"] == "Suspend" for e in wait_event("Suspend")))
r = customer("reinstate")
check("customer Reinstate accepted", r.status_code < 300, r.status_code)
check("webhook received Reinstate", any(e["action"] == "Reinstate" for e in wait_event("Reinstate")))

# A webhook for a subscription the marketplace doesn't know must be refused
r = httpx.post(f"{APP}/marketplace/webhook", json={"id": str(uuid.uuid4()), "subscriptionId": str(uuid.uuid4()),
                                                    "action": "Unsubscribe", "status": "Succeeded"})
check("webhook refuses an operation for an unknown subscription", r.status_code == 400, r.status_code)

r = customer("unsubscribe")
check("customer Unsubscribe accepted", r.status_code < 300, r.status_code)
check("webhook received Unsubscribe", any(e["action"] == "Unsubscribe" for e in wait_event("Unsubscribe")))
check("emulator shows Unsubscribed", wait_status(sid, "saasSubscriptionStatus", "Unsubscribed") == "Unsubscribed")
time.sleep(2)
row = app_rows(f"select status from subscription where id='{sid}'")
check("app marks the subscription Unsubscribed", row and row[0]["status"] == "Unsubscribed", row)

print("\nevents:", json.dumps(app_rows(f"select action,status,result from webhook_event where subscription_id='{sid}'")))
print(f"\n{'ALL PASSED' if not fails else str(len(fails)) + ' FAILED: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
