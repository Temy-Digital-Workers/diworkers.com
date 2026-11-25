"""Builds diworkers.com (Temy Digital Workers) into static html. Run: python build.py ; deploy: sh deploy.sh"""
import html as H
import json
from pathlib import Path

ROOT = Path(__file__).parent
HELLO = "hello@diworkers.com"
SUPPORT = "support@diworkers.com"
LEGAL = "Team Technologies Development Center LLP"
OFFICE = "Ground Floor, 41 Devonshire Street, London W1G 7AJ, United Kingdom"
FOOT_LEGAL = (f"Temy Digital Workers is a trading name of {LEGAL}, a limited liability partnership registered in "
              f"England and Wales, registration number OC404423. Registered office: {OFFICE}.")

ICONS = {
    "invoice": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h5"/>',
    "brief": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "check": '<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/>',
    "sales": '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "radar": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><path d="M12 12l6-6"/>',
    "plug": '<path d="M9 7V3M15 7V3M7 7h10v4a5 5 0 0 1-10 0zM12 16v5"/>',
    "hand": '<path d="M7 11V6a2 2 0 0 1 4 0v5M11 10V4a2 2 0 0 1 4 0v6M15 10V6a2 2 0 0 1 4 0v8a7 7 0 0 1-7 7h-1a6 6 0 0 1-5-3l-3-5a2 2 0 0 1 3-2l2 2"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "server": '<rect x="3" y="4" width="18" height="7" rx="2"/><rect x="3" y="13" width="18" height="7" rx="2"/><path d="M7 8h.01M7 17h.01"/>',
    "flow": '<rect x="3" y="3" width="6" height="6" rx="1.5"/><rect x="15" y="15" width="6" height="6" rx="1.5"/><path d="M9 6h5a3 3 0 0 1 3 3v6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0M16 4a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 4 6"/>',
    "coin": '<circle cx="12" cy="12" r="9"/><path d="M15 9a3 3 0 0 0-3-1.5c-1.7 0-3 .9-3 2.2 0 3 6 1.6 6 4.6 0 1.3-1.3 2.2-3 2.2A3 3 0 0 1 9 15M12 6v1.5M12 16.5V18"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}


def icon(name, size=24):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


ARROW = icon("arrow", 16)

NAV = [("/workers.html", "Workers"), ("/how-it-works.html", "How it works"), ("/trust.html", "Security"),
       ("/partners.html", "Partners"), ("/about.html", "About")]


def layout(path, title, desc, body, active=""):
    nav = "".join(f'<a href="{h}"{" class=on" if active == h else ""}>{t}</a>' for h, t in NAV)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{H.escape(title)}</title>
<meta name="description" content="{H.escape(desc)}">
<meta property="og:title" content="{H.escape(title)}">
<meta property="og:description" content="{H.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="https://diworkers.com{path}">
<meta property="og:image" content="https://diworkers.com/assets/video/flow-ap-clerk.jpg">
<link rel="canonical" href="https://diworkers.com{path}">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/img/favicon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hind+Vadodara:wght@400;500;600&family=Montserrat:wght@600;700&display=swap">
<link rel="stylesheet" href="/assets/css/site.css?v=2">
</head>
<body>
<header class="hdr"><div class="wrap"><div class="pill">
<a class="brand" href="/" aria-label="Temy Digital Workers, home"><img src="/assets/img/temy-logo.svg" alt="Temy" width="81" height="24"><span class="sub">Digital<br>Workers</span></a>
<nav class="nav" aria-label="Main">{nav}</nav>
<div style="display:flex;align-items:center;gap:8px"><a class="btn red sm cta-top" href="/contact.html">Book a demo</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button></div>
</div></div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div class="cols">
<div><a class="brand" href="/"><img src="/assets/img/temy-logo.svg" alt="Temy" width="81" height="24"><span class="sub">Digital<br>Workers</span></a>
<p style="margin-top:18px;max-width:340px">AI workers that do back-office jobs end to end, inside the systems you already use, with a person approving every step that matters.</p>
<a href="mailto:{HELLO}" style="margin-top:14px">{HELLO}</a></div>
<div><h4>Workers</h4>{"".join(f'<a href="/workers/{w["slug"]}.html">{w["name"]}</a>' for w in WORKERS)}</div>
<div><h4>Product</h4><a href="/how-it-works.html">How it works</a><a href="/trust.html">Security and data</a><a href="/partners.html">For IT partners</a><a href="/contact.html">Book a demo</a></div>
<div><h4>Company</h4><a href="/about.html">About</a><a href="/support.html">Support</a><a href="/privacy.html">Privacy policy</a><a href="/terms.html">Terms of service</a></div>
</div>
<div class="legal">{FOOT_LEGAL}<br>&copy; 2026 {LEGAL}. All rights reserved. Product names and logos of other companies belong to their owners and are shown only to name the systems our workers connect to.</div>
</div></footer>
<script src="/assets/js/site.js?v=2" defer></script>
</body>
</html>
"""


def write(path, title, desc, body, active=""):
    out = ROOT / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(layout(path, title, desc, body, active), encoding="utf-8")


def logos(names):
    return "".join(f'<img src="/assets/logos/{n}.svg" alt="{LOGO_NAMES[n]}" title="{LOGO_NAMES[n]}" width="26" height="26">' for n in names)


def chips(names):
    return "".join(f'<span class="chip"><img src="/assets/logos/{n}.svg" alt="" width="22" height="22">{LOGO_NAMES[n]}</span>' for n in names)


LOGO_NAMES = {"quickbooks": "QuickBooks Online", "google-chat": "Google Chat", "gmail": "Gmail", "halo": "HaloPSA",
              "hudu": "Hudu", "hubspot": "HubSpot", "apollo": "Apollo.io", "snovio": "Snov.io", "jira": "Jira",
              "github": "GitHub", "digitalocean": "DigitalOcean", "serpapi": "SerpAPI", "google-sheets": "Google Sheets",
              "business-central": "Dynamics 365 Business Central", "outlook": "Outlook", "microsoft-365": "Microsoft 365",
              "dynamics-365": "Dynamics 365 Sales", "entra": "Microsoft Entra ID", "defender": "Microsoft Defender",
              "teams": "Microsoft Teams", "sharepoint": "SharePoint"}

FLOWS = [
    ("flow-ap-clerk", "AP Clerk", "The real AP Clerk flow, in its QuickBooks version: a Google Chat message starts it, the hub records the invoice, the AI agent codes it, QuickBooks receives the bill, and the chat gets a report. It loops for up to 30 rounds and parks for a person if something is off."),
    ("flow-client-briefs", "Client Briefs", "The real Client Briefs flow: on a schedule it collects tickets and contracts from HaloPSA and documentation from Hudu, joins them, has the AI write five briefs and publishes them to the worker's hub."),
    ("flow-threat-hunting", "Threat Hunter", "The real Threat Hunter flow: it collects fresh threat intelligence, an AI agent correlates it with what we already know, a second pass writes hunt queries, and the results go to the security hub and to chat."),
]

# ------------------------------------------------------------------ workers
WORKERS = [
    dict(
        slug="ap-clerk", name="AP Clerk", icon="invoice", family="Finance",
        logos=["outlook", "business-central", "quickbooks"],
        card="Reads supplier invoices from the AP mailbox, codes every line and enters a draft purchase invoice in Business Central or QuickBooks. Asks a person only when it is unsure.",
        h1='Every supplier invoice, from the inbox <em class="r">to the books</em>.',
        lead="The AP Clerk picks up bills wherever they arrive, reads them, matches the supplier, codes each line to the right G/L account and enters the invoice in your accounting system. When it is not sure, it stops and asks a person.",
        facts=[("25", "supplier emails in our Business Central test run"), ("17", "entered as draft purchase invoices with no human touch"), ("5 + 3", "sent to a person, plus 2 duplicates and 1 statement stopped")],
        problem="Someone on the team spends hours a week opening PDFs, retyping supplier names, amounts and VAT, choosing an expense account and chasing duplicates. It is slow, it is boring, and the mistakes show up at month end.",
        steps=[
            ("Finds the invoice", "Reads the AP mailbox in Outlook (or a chat space). A PDF or a photo of a bill is enough.", "script"),
            ("Reads and understands it", "Extracts supplier, invoice number, dates, lines, tax and totals, even from scans.", "ai"),
            ("Checks against your books", "Looks up suppliers, G/L accounts and recent invoices in Business Central, spots duplicates and unknown suppliers.", "script"),
            ("Codes every line", "Chooses the G/L account for each line, separates VAT and scores its own confidence.", "ai"),
            ("Asks when unsure", "Below the confidence threshold, for a new supplier or when the arithmetic does not add up, it waits for a person.", "human"),
            ("Enters the invoice", "Creates a draft purchase invoice in Business Central with the original PDF attached, checks the VAT total and emails a report.", "script"),
        ],
        case_title="Case: 25 supplier emails into Business Central",
        case="We emailed 25 UK supplier documents to an AP mailbox and ran the AP Clerk against a Dynamics 365 Business Central company (the CRONUS UK demo). 17 were entered as draft purchase invoices with the right G/L accounts and the PDF attached, with no human touch. 5 went to a person: a blurry phone photo, a vague \"services as agreed\" line, an invoice whose lines did not add up, and 2 new suppliers. It stopped a byte-identical resend and a reused invoice number, and recognised a statement as not an invoice. On 7 drafts Business Central's VAT total differed from the printed one because those suppliers were set up without UK VAT, and the worker flagged each before posting. The same worker also runs on QuickBooks Online, where a 25-invoice run posted 18 bills with no human touch.",
        media=("img", "/assets/img/bc-ap-drafts.jpg", "The 17 draft purchase invoices the AP Clerk entered in Business Central from 25 supplier emails (CRONUS UK demo company)."),
        video="flow-ap-clerk",
        systems=["outlook", "business-central", "quickbooks", "google-chat", "gmail"],
        next_note="Runs on Dynamics 365 Business Central and QuickBooks Online today. Invoices arrive through Outlook, Google Chat or Gmail.",
        faq=[("Does it post anything without approval?", "Only what you allow. You set the confidence threshold and which suppliers or amounts always need a person. Everything else is posted and reported."),
             ("What if the invoice is a bad scan?", "It reads scans and photos, but if a field cannot be read with confidence it asks rather than guesses."),
             ("Can it handle VAT and multiple currencies?", "It reads tax lines and currency from the document and uses the tax codes set up in your accounting system.")],
    ),
    dict(
        slug="ar-collections", name="AR Collections Clerk", icon="invoice", family="Finance",
        logos=["business-central", "outlook"],
        card="Reads open customer invoices in Business Central, ages them and drafts a polite reminder per overdue customer in Outlook for a person to send.",
        h1='Overdue invoices, <em class="r">chased politely and on time</em>.',
        lead="The AR Collections Clerk reads your open sales invoices, sorts them by how overdue they are, drafts one reminder per customer with the exact invoices and amounts, and sends the finance team a summary with a cash-in forecast. Nothing goes to a customer until a person sends it.",
        facts=[("13", "open invoices read in our Business Central test"), ("4", "reminders drafted, one per overdue customer"), ("0", "emails sent to customers without a person")],
        problem="Chasing late payers is the job everyone postpones. Reminders go out late, with the wrong amounts, or not at all, and cash sits in receivables.",
        steps=[
            ("Reads the ledger", "Takes open sales invoices and customer balances from Business Central.", "script"),
            ("Ages every invoice", "Sorts them into current, 1-30, 31-60, 61-90 and 90+ days overdue.", "script"),
            ("Drafts the reminders", "Writes one reminder per customer in the right tone for how late it is, with a table of that customer's invoices.", "ai"),
            ("Leaves them for a person", "Saves each reminder as an Outlook draft. A person reviews and sends.", "human"),
            ("Reports", "Emails the finance team the ageing table and a weekly cash-in forecast.", "script"),
        ],
        case_title="Case: a Business Central test company",
        case="We ran the AR Collections Clerk on the CRONUS UK test company in Dynamics 365 Business Central. It read 13 open sales invoices across 4 customers, aged them, and found £44,005.48 overdue, all more than 90 days past due. It wrote one reminder per customer, each with a table of that customer's invoices built from Business Central figures, and left all 4 in Outlook Drafts for a person to review and send. Nothing went to customers; it sent one summary with the ageing table and the cash-in forecast to the finance mailbox.",
        media=None, video=None, systems=["business-central", "outlook"],
        next_note="Runs on Dynamics 365 Business Central today.",
        faq=[("Will it email my customers on its own?", "No. Reminders are drafts until a person sends them."),
             ("Can it match our tone?", "Yes. The tone per ageing bucket is set when the worker is configured.")],
    ),
    dict(
        slug="client-briefs", name="Client Briefs", icon="brief", family="IT services",
        logos=["halo", "hudu"],
        card="For IT service providers: reads each client's tickets, contract and devices in HaloPSA plus documentation in Hudu, and writes five briefs before the call.",
        h1='Know every client <em class="r">before the call</em>.',
        lead="Client Briefs joins what your PSA and your documentation platform know about each client and turns it into five short briefs, with every figure linked back to its source. Account managers walk into reviews prepared, in minutes instead of hours.",
        facts=[("5", "briefs per client, every figure linked to its source"), ("2", "systems joined: HaloPSA and Hudu"), ("100", "clients in our test IT-provider dataset")],
        problem="Before a quarterly review an account manager clicks through dozens of tickets, the contract, the device list, licences and backup status, spread over two systems that do not talk to each other. Most of the time the preparation simply does not happen.",
        steps=[
            ("Collects from HaloPSA", "Tickets, contract and devices for each client.", "script"),
            ("Collects from Hudu", "Documentation, licences and backups for the same client.", "script"),
            ("Joins the two", "Matches devices by serial number and people by email, so both systems describe one client.", "script"),
            ("Writes five briefs", "Health, open issues, assets, risks and talking points, each claim linked to the ticket or record behind it.", "ai"),
            ("Publishes to the hub", "Account managers open the client page, read, and jump to the evidence in one click.", "script"),
        ],
        case_title="Case: a 100-client IT provider, end to end",
        case="We built a realistic IT-provider dataset of 100 fictional clients in HaloPSA and Hudu, with problems planted in it (expiring warranties, failed backups, licence gaps). Client Briefs runs on a schedule, refreshes a client when its data changes, and publishes five briefs per client with links straight back to the ticket or the Hudu record. Passwords stored in the documentation platform are read only as names and dates, never as values.",
        media=None, video="flow-client-briefs", systems=["halo", "hudu"], next_note="",
        faq=[("Does it change anything in HaloPSA or Hudu?", "No. It only reads. Briefs are published to the worker's own portal."),
             ("Can we use it with another PSA?", "The flow is built from connectors; another PSA or documentation tool means swapping two steps, not rebuilding the worker.")],
    ),
    dict(
        slug="security-operations", name="Security Operations", icon="shield", family="Security",
        logos=["github", "digitalocean", "google-chat"],
        card="A team of twelve security workers on one board: threat hunting, alert triage, attack surface, identity and cloud posture, detection engineering and more.",
        h1='A security team of digital workers, <em class="r">on one board</em>.',
        lead="Twelve specialised workers share one findings board. Each does one job well (enrichment, hunting, triage, posture checks) and the later ones build on what the earlier ones found. A person approves every containment action.",
        facts=[("12", "security workers on one board"), ("110", "findings on our own infrastructure in the first runs"), ("0", "actions executed without approval")],
        problem="Small security teams drown in alerts and checklists. The important signal, an exposed bucket, an unpatched exploited CVE, a missing DMARC record, sits in a queue nobody has time to work through.",
        steps=[
            ("Indicator enrichment", "Looks up suspicious IPs, domains and hashes in public threat-intelligence feeds.", "script"),
            ("Threat hunting", "Correlates fresh intelligence with what is already known and writes hunt queries.", "ai"),
            ("Alert triage", "Scores alerts against the list of vulnerabilities known to be exploited in the wild.", "ai"),
            ("Posture checks", "Attack surface from certificate logs, email identity (SPF, DKIM, DMARC), public cloud storage, endpoint coverage.", "script"),
            ("Response proposals", "Drafts containment steps as a dry run. Nothing runs until an analyst approves it.", "human"),
            ("Daily briefing", "A SOC copilot summarises the whole board every morning.", "ai"),
        ],
        case_title="Case: pointing the team at our own estate",
        case="We run the security workers against Temy's own infrastructure. In their first runs they raised 110 findings across hunting, triage, attack surface, email identity, cloud posture and endpoint coverage, each with the evidence that produced it. Response actions are proposals only: they are recorded, explained and wait for a person.",
        media=None, video="flow-threat-hunting", systems=["github", "digitalocean", "google-chat"],
        next_note="Microsoft 365 identity posture (Entra, MFA, admin roles, Secure Score) runs today through the Compliance Evidence worker. Defender alert triage is next.",
        faq=[("Will it block anything on its own?", "No. Containment is always a proposal that an analyst approves."),
             ("Which workers are in the team?", "Indicator enrichment, threat hunter, detection engineer (Sigma, Elastic, YARA), alert triage, incident investigator, attack surface, identity posture, cloud posture, endpoint coverage gaps, response proposals, SOC copilot and compliance evidence.")],
    ),
    dict(
        slug="compliance-evidence", name="Compliance Evidence", icon="check", family="Compliance",
        logos=["microsoft-365", "entra", "github"],
        card="Collects evidence for ISO 27001, SOC 2 and Cyber Essentials controls straight from Microsoft 365 and your other systems, grades each control and explains every gap.",
        h1='Audit evidence that <em class="r">collects itself</em>.',
        lead="The Compliance Evidence worker checks your controls against the systems that actually run your business, keeps the evidence with a timestamp and tells you in plain words what is missing.",
        facts=[("19", "controls graded on our own Microsoft 365 tenant"), ("8 / 6 / 5", "passed, failed, not collected"), ("0", "controls marked as passed without evidence")],
        problem="Before an audit, people take screenshots, export lists and paste them into folders. The evidence is out of date by the time the auditor reads it, and nobody can say how it was collected.",
        steps=[
            ("Reads the controls", "Starts from the ISO 27001 and SOC 2 controls you are in scope for.", "script"),
            ("Checks the real systems", "Microsoft 365 and Entra (MFA, admin roles, sign-in policy, Secure Score), email DNS, cloud resources, source code settings and certificates.", "script"),
            ("Grades each control", "Pass, partial or fail, with the exact check that produced the grade.", "ai"),
            ("Explains the gaps", "Writes what is missing and what would close it, in language a manager understands.", "ai"),
            ("Keeps the evidence", "Stores artefacts, provenance and history so the auditor sees how each result was made.", "script"),
        ],
        case_title="Case: our own Microsoft 365 tenant",
        case="We pointed the Compliance Evidence worker at our own Microsoft 365 tenant and it graded 19 controls mapped to ISO 27001:2022, SOC 2 and Cyber Essentials, using Microsoft Graph and public DNS only. 8 passed, including enforced MFA, blocked legacy sign-in, and SPF, DKIM and DMARC on our domain. 6 failed with 11 specific gaps, each with the evidence behind it and the change that would close it. 5 more were marked not collected rather than passed, because the worker did not yet have permission to read those systems. On our engineering estate (DigitalOcean, GitHub, Jira and TLS certificates) the same worker grades 31 controls.",
        media=None, video=None, systems=["microsoft-365", "entra", "digitalocean", "github", "jira"],
        next_note="Intune device compliance, SharePoint sharing, mailbox forwarding and Defender alerts are added as soon as the tenant grants their read permissions.",
        faq=[("Does this replace the auditor?", "No. It replaces the evidence-gathering, so the auditor's time goes on judgement."),
             ("Can we add our own controls?", "Yes. A control is a check plus a rule for grading it.")],
    ),
    dict(
        slug="sales-assistant", name="Sales Assistant", icon="sales", family="Sales",
        logos=["dynamics-365", "hubspot", "apollo"],
        card="Enriches and scores new leads in Dynamics 365 Sales or HubSpot, explains each score on the record and drafts the first email in Outlook.",
        h1='Every new lead, <em class="r">researched before you call</em>.',
        lead="The Sales Assistant takes new leads from your CRM, finds verified company and contact data, and writes it back to the record, so sales starts from facts instead of a bare email address.",
        facts=[("10", "Dynamics 365 leads enriched and scored in our test run"), ("5", "first-touch emails left as Outlook drafts"), ("0", "existing CRM fields overwritten")],
        problem="Leads arrive as a name and an email. Someone has to look up the company, the role and a verified address before anyone can call, and that research is where good leads go cold.",
        steps=[
            ("Picks up new leads", "Takes a small batch of open leads from Dynamics 365 Sales or HubSpot that have not been enriched yet.", "script"),
            ("Researches the person and company", "Looks them up in Apollo.io and Snov.io and compares the answers.", "script"),
            ("Verifies the email", "Keeps only addresses the providers can verify.", "script"),
            ("Checks and scores", "Matches each lead against existing contacts and accounts, then scores it with its reasons.", "ai"),
            ("Writes back safely", "Adds a note to the CRM record and drafts the first email in Outlook. It never overwrites what your team typed or sends anything itself.", "script"),
        ],
        case_title="Case: Dynamics 365 Sales, and our own HubSpot",
        case="We ran the Sales Assistant on a Dynamics 365 Sales trial with 10 open leads. It enriched all 10 with Apollo.io and Snov.io and checked each against existing contacts and accounts (1 was already a contact, 5 worked at known accounts). It scored and explained every lead (5 worth a short email, 5 not worth outreach now), added the reasoning as a note on each lead without changing any field, and left 5 first-touch emails as Outlook drafts for a salesperson to send. On Temy's own HubSpot portal it runs every hour in small batches and writes its results to separate fields.",
        media=None, video=None, systems=["dynamics-365", "hubspot", "outlook", "apollo", "snovio"],
        next_note="Runs on Dynamics 365 Sales and HubSpot today.",
        faq=[("Will it email leads on its own?", "No. It researches and records. Outreach stays with your team."),
             ("Can it work with our data provider?", "Yes, providers are connectors. Apollo.io and Snov.io are the ones in use today.")],
    ),
    dict(
        slug="research-monitor", name="Research and Monitoring", icon="radar", family="Research",
        logos=["serpapi", "google-sheets", "google-chat"],
        card="Reads the sources you care about every day, keeps what matters, rewrites it clearly and publishes a ranked digest. No repeats.",
        h1='The news that matters, <em class="r">read for you every morning</em>.',
        lead="Research workers watch websites, feeds and search results, decide what is worth your time, rewrite it in plain language and publish it as a digest or a portal, every day, without repeating themselves.",
        facts=[("793", "AI news stories ranked by one worker"), ("Daily", "runs, with no repeats"), ("4", "research workers live")],
        problem="Keeping up with regulation, a market or an industry means reading the same sources every day and throwing most of it away. It is necessary work that nobody wants.",
        steps=[
            ("Reads the sources", "RSS feeds, official websites and search results, on a schedule.", "script"),
            ("Drops what it has seen", "Every item is remembered, so nothing is published twice.", "script"),
            ("Ranks by impact", "An AI judge scores each item for relevance and explains why it matters.", "ai"),
            ("Rewrites clearly", "Short, plain summaries with a link to the original.", "ai"),
            ("Publishes", "To a public or private portal, a chat space or a spreadsheet.", "script"),
        ],
        case_title="Case: four research workers we run every day",
        case="AI Impact ranks AI news by its impact on the industry and has scored 793 stories. A legislative digest reads the Ukrainian parliament's news feed daily and publishes only the most valuable items. A business-events worker finds conferences and extracts dates, venues and ticket prices. A places worker rates restaurants against a written rubric. All four publish to their own portals.",
        media=None, video=None, systems=["serpapi", "google-sheets", "google-chat"], next_note="",
        faq=[("Can it watch our competitors or regulators?", "Yes. Give it the sources and what counts as important; the rest is configuration."),
             ("Where does the digest go?", "A web portal, a chat space, email or a spreadsheet.")],
    ),
]

CONSOLE = [
    dict(short="AP Clerk", name="AP Clerk", role="Finance worker", av="AP", steps=[
        ["New email in the AP mailbox", "cr-05-wwi.pdf from Wide World Importers"],
        ["Read and understood", "2 lines, net £1,655.00, VAT £331.00, total £1,986.00"],
        ["Checked in Business Central", "Known supplier, no duplicate found"],
        ["Coded every line", "Freight fees for goods, Customs and forwarding, confidence 99%"],
        ["Checked the VAT", "Business Central total differs by £284.00: flagged", "CHECK"],
        ["Draft purchase invoice entered", "PDF attached, report emailed to the AP team"]]),
    dict(short="Client Briefs", name="Client Briefs", role="IT services worker", av="CB", steps=[
        ["Collected from HaloPSA", "41 tickets, contract, 23 devices"],
        ["Collected from Hudu", "Licences, backups, documentation"],
        ["Joined the two", "Devices by serial, people by email"],
        ["Wrote five briefs", "2 risks found: backup failing, warranty expiring"],
        ["Published to the hub", "Every figure linked to its source"]]),
    dict(short="Security", name="Threat Hunter", role="Security worker", av="TH", steps=[
        ["Collected fresh intelligence", "New indicators from public feeds"],
        ["Correlated with the board", "3 indicators match earlier findings"],
        ["Wrote hunt queries", "Queries ready for the analyst"],
        ["Proposed containment", "Dry run only, nothing executed", "ANALYST APPROVES"],
        ["Posted to the security board", "And notified the team in chat"]]),
]


# ------------------------------------------------------------------ pages
def band():
    return f"""<section class="tight"><div class="wrap"><div class="band rv">
<div><h2>See a digital worker do your job.</h2><p>30 minutes, on your own process. We show a worker running end to end and agree what a first pilot would prove.</p></div>
<div class="acts"><a class="btn white" href="/contact.html">Book a demo {ARROW}</a><a class="btn line" href="/workers.html">Browse workers</a></div>
</div></div></section>"""


def flows_block(dark=True, heading=True):
    tabs = "".join(f'<button type="button" class="{"on" if i == 0 else ""}" data-src="/assets/video/{f}.mp4" data-poster="/assets/video/{f}.jpg" data-title="{t}" data-cap="{H.escape(c)}">{t}</button>' for i, (f, t, c) in enumerate(FLOWS))
    f0 = FLOWS[0]
    head = """<div class="sec-head"><div class="stack"><span class="eyebrow">Real flows, recorded</span>
<h2>Watch a worker run, step by step.</h2>
<p class="lead">These are the actual flows behind our workers, recorded in the Temy Labs flow editor. The highlighted step is the one running; the dashed line is where it goes next.</p></div></div>""" if heading else ""
    return f"""<section class="{'dark' if dark else 'bg-soft'}"><div class="wrap" data-flows>
{head}
<div class="flow-tabs" role="tablist">{tabs}</div>
<div class="frame rv"><div class="chrome"><i></i><i></i><i></i><span data-title>{f0[1]}</span></div>
<video src="/assets/video/{f0[0]}.mp4" poster="/assets/video/{f0[0]}.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Recording of a digital worker flow running"></video></div>
<p class="muted" style="margin-top:16px" data-cap>{H.escape(f0[2])}</p>
<div class="legend"><span><i style="background:#e9f7ef;border:1px solid #9bd8b5"></i>Connector step (Google Chat, QuickBooks, HaloPSA)</span><span><i style="background:#fbe9e5;border:1px solid #f0b5a6"></i>AI agent step</span><span><i style="background:#fdecec;border:1px solid #f3a9a9"></i>Worker hub step</span></div>
</div></section>"""


def home():
    cards = "".join(f"""<a class="card worker-card rv d{i % 3}" href="/workers/{w['slug']}.html"><div class="ico">{icon(w['icon'])}</div>
<span class="tag">{w['family']}</span><h3>{w['name']}</h3><p>{w['card']}</p><div class="logos">{logos(w['logos'])}</div>
<span class="more">See how it works {ARROW}</span></a>""" for i, w in enumerate(WORKERS))
    allchips = chips(list(LOGO_NAMES)) * 2
    body = f"""
<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">Temy Digital Workers</span>
<h1>AI workers that do <em class="r">real back-office work</em>.</h1>
<p class="lead">A digital worker is one job done end to end: it reads the documents, works in the systems you already use, and asks a person before anything important is posted or sent. Every step is recorded.</p>
<div class="cta"><a class="btn red" href="/contact.html">Book a demo {ARROW}</a><a class="btn ghost" href="#watch">Watch one work</a></div>
<div class="trust-line"><span>Human approval built in</span><span>Runs in our cloud or yours</span><span>Full audit trail</span></div></div>
<div class="rv"><div class="console" data-console='{H.escape(json.dumps(CONSOLE))}'>
<div class="top"><div class="who"><div class="av">AP</div><div><div class="name">AP Clerk</div><div class="role">Finance worker</div></div></div><span class="live">LIVE RUN</span></div>
<ul class="steps-live"></ul><div class="bar"><i></i></div><div class="tabs"></div></div>
<p class="muted small" style="margin-top:12px;text-align:center">An illustration of three of our workers' real steps. Sample data.</p></div>
</div></section>

<section class="tight bg-soft"><div class="wrap">
<div class="nums">
<div class="num rv"><b data-count="6">6</b><span>workers running today, for finance, IT services, security, compliance, sales and research</span></div>
<div class="num rv d1"><b data-count="12">12</b><span>specialised security workers sharing one findings board</span></div>
<div class="num rv d2"><b><i style="font-style:normal" data-count="25">25</i><em>/25</em></b><span>test invoices handled: posted, sent for approval or stopped as duplicates</span></div>
<div class="num rv d3"><b data-count="100">100</b><span>clients in the IT-provider dataset Client Briefs is tested on</span></div>
</div></div></section>

<section><div class="wrap">
<div class="sec-head"><div class="stack"><span class="eyebrow">What is a digital worker</span>
<h2>Not a chatbot. <em class="r">A colleague with one job.</em></h2></div>
<p class="lead" style="max-width:460px">A chatbot answers questions. A digital worker finishes work: it takes the input, does every step in your systems and hands you the result, with the evidence.</p></div>
<div class="grid g3">
<div class="card rv"><div class="ico">{icon('plug')}</div><h3>Works in your systems</h3><p>It signs in to Microsoft 365, Business Central, Dynamics 365, QuickBooks, HaloPSA, HubSpot or your cloud with its own limited account, and works there like a careful new hire would.</p></div>
<div class="card rv d1"><div class="ico">{icon('hand')}</div><h3>Asks before it acts</h3><p>Approval gates sit wherever you want them. Low confidence, a new supplier or a risky change goes to a person in chat first.</p></div>
<div class="card rv d2"><div class="ico">{icon('eye')}</div><h3>Shows its work</h3><p>Every run keeps its inputs, its decisions and its results. You can always see what was done, why, and who approved it.</p></div>
</div></div></section>

<span id="watch"></span>
{flows_block()}

<section><div class="wrap">
<div class="sec-head"><div class="stack"><span class="eyebrow">The workers</span><h2>Seven workers, each with a real case behind it.</h2></div>
<a class="btn ghost" href="/workers.html">All workers {ARROW}</a></div>
<div class="grid g3">{cards}</div></div></section>

<section class="bg-soft"><div class="wrap split">
<div class="stack"><span class="eyebrow">Inside a worker</span><h2>Its own portal, <em class="r">its own records</em>.</h2>
<p class="lead">Every worker has a portal where your team sees what it received, what it did, what is waiting for approval and how sure it was. This is the AP Clerk's, on our accounting test company.</p>
<ul class="checks"><li>Confidence score on every document</li><li>"Needs you" queue for approvals</li><li>Duplicates stopped before they reach the books</li><li>Link from each bill to its source file</li></ul>
<a class="btn red" href="/workers/ap-clerk.html" style="margin-top:12px">Meet the AP Clerk {ARROW}</a></div>
<div class="frame rv"><div class="chrome"><i></i><i></i><i></i><span>AP Clerk · Invoices</span></div><img src="/assets/img/ap-invoices.jpg" alt="The AP Clerk portal listing 25 invoices with confidence scores and statuses" loading="lazy" width="3200" height="1800"></div>
</div></section>

<section class="tight"><div class="wrap center">
<span class="eyebrow">Connects to</span><h2 style="margin:14px 0 28px">The systems your team already uses</h2>
<div class="marquee"><div class="track">{allchips}</div></div>
<p class="muted small" style="margin-top:18px">Runs on Microsoft 365, Dynamics 365 Business Central and Dynamics 365 Sales, signing in with a certificate and no passwords. Plus any system with an API.</p>
</div></section>

<section class="bg-soft"><div class="wrap">
<div class="sec-head"><div class="stack"><span class="eyebrow">How we start</span><h2>From first call to a worker in production.</h2></div></div>
<div class="grid g4 how">
<div class="card rv"><h3>Pick one job</h3><p>A repetitive process with clear inputs and a clear result. We map it with you in one session.</p></div>
<div class="card rv d1"><h3>Connect</h3><p>The worker gets its own limited access to the systems involved. Nothing more.</p></div>
<div class="card rv d2"><h3>Shadow run</h3><p>It works alongside your team on real cases and records what it would do, without posting anything.</p></div>
<div class="card rv d3"><h3>Go live</h3><p>You switch on the steps you trust, keep approvals where you want them, and pay for the work done.</p></div>
</div></div></section>
{band()}"""
    write("/index.html", "Temy Digital Workers: AI workers for real back-office work",
          "Digital workers that do back-office jobs end to end in Microsoft 365, Business Central, Dynamics 365, QuickBooks, HaloPSA and HubSpot, with human approval and a full audit trail.", body)


def workers_index():
    rows = "".join(f"""<a class="card worker-card rv d{i % 3}" href="/workers/{w['slug']}.html"><div class="ico">{icon(w['icon'])}</div>
<span class="tag">{w['family']}</span><h3>{w['name']}</h3><p>{w['card']}</p>
<div class="facts" style="grid-template-columns:1fr;margin-top:18px"><div class="fact"><b>{w['facts'][0][0]}</b><span>{w['facts'][0][1]}</span></div></div>
<div class="logos">{logos(w['logos'])}</div><span class="more">Open {ARROW}</span></a>""" for i, w in enumerate(WORKERS))
    body = f"""<section class="hero" style="padding-bottom:40px"><div class="wrap"><span class="eyebrow">Workers</span>
<h1 style="max-width:900px">Pick the job. <em class="r">We bring the worker.</em></h1>
<p class="lead">Each worker below runs today, on real systems, with a case we can show you. If your job is not here, we build it from the same parts.</p></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="grid g3">{rows}</div></div></section>
<section class="bg-soft tight"><div class="wrap split">
<div class="stack"><span class="eyebrow">Something else?</span><h2>Most back-office jobs fit the same shape.</h2>
<p class="lead">Read something, check it against a system, decide, ask a person when needed, write the result back. If your process looks like that, it can be a digital worker.</p></div>
<div class="grid g2">
<div class="card"><div class="ico">{icon('coin')}</div><h3>Finance</h3><p>Collections reminders, expense checks, bank reconciliation.</p></div>
<div class="card"><div class="ico">{icon('users')}</div><h3>Operations</h3><p>Onboarding checklists, licence reviews, contract renewals.</p></div>
</div></div></section>
{band()}"""
    write("/workers.html", "Workers | Temy Digital Workers", "The digital workers we run today: AP Clerk, Client Briefs, Security Operations, Compliance Evidence, Sales Assistant and Research.", body, "/workers.html")


def worker_page(w):
    steps = "".join(f"""<div class="row rv{' gate' if who == 'human' else ''}"><div class="n">{i + 1}</div><div><h3>{t}</h3><p>{d}</p>
<span class="who {who}">{ {'ai': 'AI agent', 'script': 'Automated step', 'human': 'Person decides'}[who] }</span></div></div>""" for i, (t, d, who) in enumerate(w["steps"]))
    facts = "".join(f'<div class="fact"><b>{a}</b><span>{b}</span></div>' for a, b in w["facts"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in w["faq"])
    media = ""
    if w["media"]:
        _, src, cap = w["media"]
        media = f"""<div class="frame rv" style="margin-top:28px"><div class="chrome"><i></i><i></i><i></i><span>{w['name']} portal</span></div><img src="{src}" alt="{H.escape(cap)}" loading="lazy"></div><p class="muted small" style="margin-top:10px">{cap}</p>"""
    video = ""
    if w["video"]:
        f = next(x for x in FLOWS if x[0] == w["video"])
        video = f"""<section class="dark"><div class="wrap"><span class="eyebrow">The real flow</span><h2 style="margin:14px 0 10px">Watch the {w['name']} run.</h2>
<p class="lead">{H.escape(f[2])}</p>
<div class="frame rv" style="margin-top:28px"><div class="chrome"><i></i><i></i><i></i><span>{w['name']} flow</span></div>
<video src="/assets/video/{f[0]}.mp4" poster="/assets/video/{f[0]}.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Recording of the {w['name']} flow running"></video></div></div></section>"""
    others = "".join(f'<a class="card rv" href="/workers/{o["slug"]}.html"><span class="tag">{o["family"]}</span><h3>{o["name"]}</h3><p>{o["card"]}</p></a>' for o in WORKERS if o is not w)[:99999]
    note = f'<p class="muted small" style="margin-top:14px">{w["next_note"]}</p>' if w["next_note"] else ""
    body = f"""<section class="hero w-hero"><div class="wrap hero-grid">
<div><div class="crumbs"><a href="/workers.html">Workers</a> / {w['family']}</div>
<h1>{w['h1']}</h1><p class="lead" style="margin-top:20px">{w['lead']}</p>
<div class="cta" style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn red" href="/contact.html?worker={w['slug']}">Book a demo {ARROW}</a><a class="btn ghost" href="#how">How it works</a></div>
<div class="facts">{facts}</div></div>
<div class="rv"><div class="card" style="padding:32px"><div class="ico">{icon(w['icon'])}</div><span class="tag">The problem it solves</span>
<p style="font-size:18px;color:var(--ink)">{w['problem']}</p>
<div class="sys">{chips(w['systems'])}</div>{note}</div></div>
</div></section>
<section id="how" class="bg-soft"><div class="wrap split" style="align-items:start">
<div class="stack" style="position:sticky;top:110px"><span class="eyebrow">Step by step</span><h2>What the {w['name']} does.</h2>
<p class="lead">Each step is either an automated action, an AI agent's judgement or a person's decision. You choose where the people are.</p>{media}</div>
<div class="timeline">{steps}</div></div></section>
{video}
<section><div class="wrap"><div class="case-box rv"><span class="eyebrow">Real case</span><h2 style="margin:14px 0 16px">{w['case_title']}</h2><p class="lead" style="max-width:none;color:var(--ink)">{w['case']}</p></div></div></section>
<section class="tight"><div class="wrap split" style="align-items:start"><div class="stack"><span class="eyebrow">Questions</span><h2>What people ask.</h2></div><div class="faq">{faq}</div></div></section>
<section class="bg-soft"><div class="wrap"><div class="sec-head"><div class="stack"><span class="eyebrow">More workers</span><h2>Other jobs we take off your plate.</h2></div></div><div class="grid g3">{others}</div></div></section>
{band()}"""
    write(f"/workers/{w['slug']}.html", f"{w['name']} | Temy Digital Workers", w["card"], body, "/workers.html")


def how():
    body = f"""<section class="hero" style="padding-bottom:48px"><div class="wrap"><span class="eyebrow">How it works</span>
<h1 style="max-width:960px">A worker is a flow: <em class="r">steps you can see, test and trust</em>.</h1>
<p class="lead">Every digital worker runs on Temy Labs, our platform for durable AI work. A worker is a flow of steps. Each step is a script, an AI agent or a person, and the platform makes sure every step finishes, is recorded and can be replayed.</p></div></section>
{flows_block(dark=True, heading=False)}
<section><div class="wrap"><div class="grid g3">
<div class="card rv"><div class="ico">{icon('flow')}</div><h3>Flows, not black boxes</h3><p>Each worker is a graph of named steps. You can read it, change it and see exactly which step a run is in.</p></div>
<div class="card rv d1"><div class="ico">{icon('clock')}</div><h3>Durable by design</h3><p>Runs survive restarts and outages. A failed step retries or parks for a person; it never silently disappears.</p></div>
<div class="card rv d2"><div class="ico">{icon('hand')}</div><h3>Approval gates</h3><p>Any step can wait for a person in chat. The run pauses, keeps its place and continues on approval.</p></div>
<div class="card rv"><div class="ico">{icon('lock')}</div><h3>Its own identity</h3><p>Each worker uses its own credentials, injected for one run only and encrypted at rest.</p></div>
<div class="card rv d1"><div class="ico">{icon('eye')}</div><h3>Everything recorded</h3><p>Logs, reports, artefacts and cost for every run, kept with the run and visible in the worker's portal.</p></div>
<div class="card rv d2"><div class="ico">{icon('server')}</div><h3>Runs where you need it</h3><p>In our cloud, in your own cloud subscription or on your own server, with Claude or a private open-source model.</p></div>
</div></div></section>
<section class="bg-soft"><div class="wrap"><div class="sec-head"><div class="stack"><span class="eyebrow">Architecture</span><h2>How data flows through a worker.</h2>
<p class="lead">A trigger starts a run. The control plane freezes the flow, its prompts and its identity into the run; an execution worker carries out every step and reports each result back.</p></div></div>
<div class="frame rv"><img src="/assets/img/architecture.jpg" alt="Architecture: triggers, control plane, execution sandbox, models, connectors and results" loading="lazy"></div></div></section>
<section><div class="wrap split"><div class="stack"><span class="eyebrow">Pricing</span><h2>Pay for work done.</h2>
<p class="lead">Each worker has a simple monthly plan. Where the volume varies, such as invoices or briefs, there is a usage-based plan priced per document or per task, with a monthly cap so the bill never surprises you.</p>
<a class="btn red" href="/contact.html" style="margin-top:8px">Ask for pricing {ARROW}</a></div>
<div class="grid g2"><div class="card"><span class="tag">Fixed</span><h3>Monthly plan</h3><p>A set price for a set volume. Easiest to budget.</p></div>
<div class="card"><span class="tag">Usage</span><h3>Base plus usage</h3><p>A small base fee plus a price per document or task, capped each month.</p></div></div></div></section>
{band()}"""
    write("/how-it-works.html", "How it works | Temy Digital Workers", "Digital workers are durable flows of scripts, AI agents and human approvals, recorded step by step on the Temy Labs platform.", body, "/how-it-works.html")


def trust():
    body = f"""<section class="hero" style="padding-bottom:40px"><div class="wrap"><span class="eyebrow">Security and data</span>
<h1 style="max-width:900px">Built to be <em class="r">trusted with real systems</em>.</h1>
<p class="lead">A digital worker touches your books, your clients and your infrastructure. These are the rules every one of them follows.</p></div></section>
<section style="padding-top:24px"><div class="wrap"><div class="grid g2">
<div class="card rv"><div class="ico">{icon('hand')}</div><h3>People decide what matters</h3><p>Posting, sending and changing things can always require approval. Security response actions are proposals only, every time.</p></div>
<div class="card rv d1"><div class="ico">{icon('lock')}</div><h3>Least privilege</h3><p>Each worker has its own account in each system, with only the permissions its job needs. Read-only wherever the job allows it.</p></div>
<div class="card rv"><div class="ico">{icon('eye')}</div><h3>A full audit trail</h3><p>Every run records its inputs, the steps it took, the decisions it made, who approved them and what changed.</p></div>
<div class="card rv d1"><div class="ico">{icon('shield')}</div><h3>Your data is not training data</h3><p>Customer content is used only to do the job. It is never used to train AI models.</p></div>
<div class="card rv"><div class="ico">{icon('server')}</div><h3>Choose where it runs</h3><p>Our cloud, your own cloud subscription or your own server. For sensitive data, workers can use a private open-source model on your hardware.</p></div>
<div class="card rv d1"><div class="ico">{icon('check')}</div><h3>We use our own workers on ourselves</h3><p>Our Compliance Evidence and security workers run on Temy's own infrastructure, so we find our own gaps first.</p></div>
</div></div></section>
<section class="bg-soft tight"><div class="wrap center"><h2>Have a security questionnaire?</h2><p class="lead" style="margin:14px auto 24px">Send it over. We answer them for every pilot.</p><a class="btn red" href="mailto:{HELLO}?subject=Security%20questionnaire">{HELLO}</a></div></section>
{band()}"""
    write("/trust.html", "Security and data | Temy Digital Workers", "Approval gates, least privilege, full audit trail, no training on customer data, and the option to run in your own cloud.", body, "/trust.html")


def partners():
    body = f"""<section class="hero"><div class="wrap hero-grid">
<div><span class="eyebrow">For IT partners</span><h1>Add digital workers <em class="r">to what you sell</em>.</h1>
<p class="lead" style="margin-top:20px">Managed service providers and Microsoft partners already own the client relationship and the systems. Digital workers turn that position into a new monthly line on the invoice, without hiring.</p>
<div class="cta"><a class="btn red" href="/contact.html?topic=partner">Become a partner {ARROW}</a></div></div>
<div class="rv"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span>Client Briefs flow</span></div><video src="/assets/video/flow-client-briefs.mp4" poster="/assets/video/flow-client-briefs.jpg" autoplay muted loop playsinline preload="metadata" aria-label="Client Briefs flow running"></video></div>
<p class="muted small" style="margin-top:10px">Client Briefs, built for IT providers on HaloPSA and Hudu.</p></div></div></section>
<section class="bg-soft"><div class="wrap"><div class="grid g3">
<div class="card rv"><div class="ico">{icon('coin')}</div><h3>Recurring revenue</h3><p>Monthly plans per worker, billed through your usual channel, with a partner margin.</p></div>
<div class="card rv d1"><div class="ico">{icon('users')}</div><h3>You keep the client</h3><p>You sell and own the relationship. We build, run and support the workers behind you.</p></div>
<div class="card rv d2"><div class="ico">{icon('brief')}</div><h3>Useful to you first</h3><p>Client Briefs and the security workers help your own team before you sell a single seat.</p></div>
</div></div></section>
<section><div class="wrap split"><div class="stack"><span class="eyebrow">How a partnership starts</span><h2>A 90-day pilot with one client.</h2>
<ul class="checks"><li>Choose one worker and one client together</li><li>Two weeks in shadow mode on real cases</li><li>Go live with approval gates you agree</li><li>Review the numbers, then roll out to more clients</li></ul></div>
<div class="quote rv"><h3>"Which workers sell best through an IT provider?"</h3><p class="muted" style="margin-top:12px">The AP Clerk for clients on QuickBooks or Business Central, Compliance Evidence for clients preparing for ISO 27001 or SOC 2, and the security team for clients without a SOC.</p></div></div></section>
{band()}"""
    write("/partners.html", "For IT partners | Temy Digital Workers", "For MSPs and Microsoft partners: sell digital workers to your clients with recurring revenue and a partner margin.", body, "/partners.html")


def about():
    body = f"""<section class="hero"><div class="wrap split">
<div><span class="eyebrow">About</span><h1>Made by engineers who <em class="r">automate their own work first</em>.</h1>
<p class="lead" style="margin-top:20px">Temy Digital Workers is built by Temy, a software engineering company that builds products for businesses in the UK, Europe and the US. We built Temy Labs to run our own engineering with AI agents, then turned the same platform on back-office work.</p></div>
<div class="card rv" style="padding:36px"><span class="tag">Company details</span>
<p style="color:var(--ink);margin-top:6px"><b>{LEGAL}</b><br>Trading as Temy Digital Workers<br>Registered in England and Wales, OC404423<br>D-U-N-S 221578021<br>{OFFICE}</p>
<p style="margin-top:16px"><a href="https://find-and-update.company-information.service.gov.uk/company/OC404423" rel="noopener">View on Companies House</a></p></div></div></section>
<section class="bg-soft"><div class="wrap"><div class="grid g3">
<div class="card rv"><h3>We run what we sell</h3><p>Our own invoices, evidence, security checks and leads go through our own workers first.</p></div>
<div class="card rv d1"><h3>Honest about limits</h3><p>Workers ask when they are unsure. So do we: if a job is not a good fit for automation, we say so.</p></div>
<div class="card rv d2"><h3>Small team, senior people</h3><p>You talk to the engineers who build the workers, not to a ticket queue.</p></div>
</div></div></section>
{band()}"""
    write("/about.html", "About | Temy Digital Workers", f"Temy Digital Workers is a trading name of {LEGAL}, registered in England and Wales (OC404423).", body, "/about.html")


def contact():
    opts = "".join(f"<option>{w['name']}</option>" for w in WORKERS) + "<option>Partnership</option><option>Something else</option>"
    body = f"""<section class="hero"><div class="wrap split" style="align-items:start">
<div class="stack"><span class="eyebrow">Book a demo</span><h1>Tell us about <em class="r">the job</em>.</h1>
<p class="lead">Describe the process you want a worker for. We reply within one business day with a time for a 30-minute demo on your own case.</p>
<ul class="checks"><li>A live worker running end to end</li><li>What a pilot on your process would prove</li><li>Pricing for your volume</li></ul>
<p class="muted" style="margin-top:20px">Prefer email? <a href="mailto:{HELLO}">{HELLO}</a></p></div>
<form class="card form rv" data-mailto="{HELLO}" style="padding:32px">
<div><label for="n">Your name</label><input id="n" name="name" required autocomplete="name"></div>
<div><label for="c">Company</label><input id="c" name="company" autocomplete="organization"></div>
<div><label for="t">Interested in</label><select id="t" name="topic">{opts}</select></div>
<div><label for="m">The job you want done</label><textarea id="m" name="message" rows="5" placeholder="For example: we receive 300 supplier invoices a month by email and enter them into Business Central by hand."></textarea></div>
<button class="btn red" type="submit">Write the email {ARROW}</button>
<p class="muted small">This opens your own email app with the message filled in. Nothing is sent from this page.</p>
</form></div></section>"""
    write("/contact.html", "Book a demo | Temy Digital Workers", "Book a 30-minute demo of a digital worker on your own process.", body)


def doc(path, title, inner, desc):
    write(path, f"{title} | Temy Digital Workers", desc, f'<div class="wrap"><article class="doc">{inner}</article></div>')


PRIVACY = f"""<h1>Privacy policy</h1><p class="muted">Last updated: 24 November 2026</p>
<h2>1. Who we are</h2><p>Temy Digital Workers is a trading name of {LEGAL} ("we", "us"), a limited liability partnership registered in England and Wales (OC404423), registered office {OFFICE}. We are the controller of the personal data described in this policy. Contact: <a href="mailto:{HELLO}">{HELLO}</a>.</p>
<h2>2. Data we collect</h2><ul>
<li><b>Contact and account data:</b> name, business email, company, job title and phone number that you give us when you contact us, sign up or buy a subscription (including through Microsoft Marketplace or a reseller).</li>
<li><b>Subscription and billing data:</b> plan, usage quantities, subscription identifiers and invoices. Payment card details are handled by the marketplace or payment provider, not by us.</li>
<li><b>Customer content:</b> documents and records a digital worker processes on your instructions. For customer content we act as a <b>processor</b> for the customer, under our terms and any data processing agreement.</li>
<li><b>Technical data:</b> logs of sign-ins and worker runs needed to operate, secure and support the service.</li></ul>
<h2>3. Why we use it and our legal basis</h2><ul><li>To provide the service and support (performance of a contract).</li><li>To bill and keep accounting records (legal obligation).</li><li>To keep the service secure and reliable (legitimate interests).</li><li>To reply to enquiries and, where you agree, send product news (legitimate interests or consent; you can opt out at any time).</li></ul>
<p>We do not sell personal data and we do not use customer content to train AI models.</p>
<h2>4. Who we share it with</h2><p>Hosting and infrastructure providers, AI model providers acting as our processors, Microsoft or the reseller through which you bought the service, and professional advisers, each under appropriate contracts. We disclose data to authorities only where the law requires it.</p>
<h2>5. International transfers</h2><p>Where data is transferred outside the UK or EEA, we use adequacy decisions or standard contractual clauses, including the UK International Data Transfer Addendum.</p>
<h2>6. How long we keep it</h2><p>Account and billing data for as long as the subscription runs and then as long as tax and accounting law requires (normally six years). Customer content and run logs for the period set in the customer's contract, after which they are deleted.</p>
<h2>7. Your rights</h2><p>You may ask for access, correction, deletion, restriction or portability of your personal data, and object to processing based on legitimate interests. Email <a href="mailto:{HELLO}">{HELLO}</a>. You can also complain to the UK Information Commissioner's Office (ico.org.uk).</p>
<h2>8. Cookies</h2><p>This website sets no cookies and uses no tracking or advertising scripts. Fonts are loaded from Google Fonts. The service itself uses only the cookies needed to keep you signed in.</p>
<h2>9. Changes</h2><p>We will post any changes on this page and update the date above.</p>"""

TERMS = f"""<h1>Terms of service</h1><p class="muted">Last updated: 24 November 2026</p>
<h2>1. Who you contract with</h2><p>These terms are between you (the customer) and {LEGAL}, trading as Temy Digital Workers, registered in England and Wales (OC404423), {OFFICE} ("we"). If you buy through Microsoft Marketplace or a reseller, the commercial terms of that channel also apply; if they conflict with these terms on price, billing or payment, the channel's terms win.</p>
<h2>2. The service</h2><p>We provide software-based digital workers that perform tasks in systems you connect. You decide which systems a worker may access. Actions that change records or send messages are submitted for approval by your staff unless you configure otherwise.</p>
<h2>3. Your responsibilities</h2><ul><li>You have the right to connect the systems and data you give the workers access to.</li><li>You review and approve the worker's proposed actions; final business decisions remain yours.</li><li>You keep your sign-in details secure and do not use the service unlawfully.</li></ul>
<h2>4. Fees</h2><p>Fees are as shown in your plan or offer. Usage-based charges are measured by the service and reported to the billing channel. Fees exclude taxes unless stated.</p>
<h2>5. Data</h2><p>You own your content. We process it only to provide the service, as described in our <a href="/privacy.html">privacy policy</a> and any data processing agreement between us. We do not use your content to train AI models.</p>
<h2>6. Availability and support</h2><p>We aim to keep the service available and to respond to support requests within one business day (see <a href="/support.html">Support</a>). Planned maintenance is announced in advance where practical.</p>
<h2>7. Warranties and liability</h2><p>The service is provided with reasonable skill and care. AI output can contain errors, which is why approval steps exist. To the extent permitted by law, our total liability in any 12 months is limited to the fees you paid in that period, and we are not liable for indirect or consequential loss. Nothing limits liability that cannot be limited by law.</p>
<h2>8. Term and termination</h2><p>Subscriptions renew for the billing term unless cancelled through the channel you bought from. Either party may terminate for material breach not fixed within 30 days of notice. On termination we delete your content after 30 days unless you ask us to return it first.</p>
<h2>9. Law</h2><p>These terms are governed by the laws of England and Wales, and the courts of England and Wales have exclusive jurisdiction.</p>
<h2>10. Contact</h2><p><a href="mailto:{HELLO}">{HELLO}</a></p>"""

SUPPORT = f"""<h1>Support</h1><p>Email <a href="mailto:{SUPPORT}">{SUPPORT}</a> with your company name, the worker concerned and, if you have it, the run ID shown in the worker's portal.</p>
<h2>Response times</h2><ul><li>First response within one business day (Monday to Friday, 09:00 to 18:00 UK time).</li><li>A worker that has stopped for all users is handled first.</li></ul>
<h2>Bought through Microsoft Marketplace or a reseller?</h2><p>For billing and cancellation, use the channel you bought from. For anything about how a worker behaves, contact us directly.</p>
<h2>Security issues</h2><p>Report suspected vulnerabilities to <a href="mailto:{SUPPORT}">{SUPPORT}</a> with "Security" in the subject line.</p>
<p class="muted">{LEGAL}, {OFFICE}.</p>"""

if __name__ == "__main__":
    home(); workers_index()
    for w in WORKERS:
        worker_page(w)
    how(); trust(); partners(); about(); contact()
    doc("/privacy.html", "Privacy policy", PRIVACY, "Privacy policy of Temy Digital Workers.")
    doc("/terms.html", "Terms of service", TERMS, "Terms of service of Temy Digital Workers.")
    doc("/support.html", "Support", SUPPORT, "How to get support for Temy Digital Workers.")
    doc("/404.html", "Page not found", '<h1>Page not found</h1><p><a href="/">Back to the home page</a></p>', "Page not found.")
    print("built", len(list(ROOT.rglob("*.html"))), "pages")
