"""Builds the static pages of diworkers.com from the bodies below (one shared header and footer)."""
from pathlib import Path

ROOT = Path(__file__).parent
CONTACT = "support@diworkers.com"
LEGAL = "Team Technologies Development Center LLP"
FOOTER_LEGAL = (
    f"Temy Digital Workers is a trading name of {LEGAL}, a limited liability partnership "
    "registered in England and Wales, registration number OC404423. "
    "Registered office: Ground Floor, 41 Devonshire Street, London W1G 7AJ, United Kingdom."
)


def page(name, title, desc, body):
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Crect width='16' height='16' rx='4' fill='%23d92d20'/%3E%3C/svg%3E">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="/"><span class="dot"></span>Temy Digital Workers</a>
<nav><a href="/#workers">Workers</a><a href="/#how">How it works</a><a href="/support.html">Support</a><a href="/#contact">Contact</a></nav>
</div></header>
{body}
<footer><div class="wrap">
<div class="links"><a href="/privacy.html">Privacy policy</a><a href="/terms.html">Terms of service</a><a href="/support.html">Support</a><a href="mailto:{CONTACT}">{CONTACT}</a></div>
<p>{FOOTER_LEGAL}</p>
<p>&copy; 2026 {LEGAL}. All rights reserved.</p>
</div></footer>
</body>
</html>
"""
    (ROOT / name).write_text(html, encoding="utf-8")


INDEX = f"""<main>
<section class="hero"><div class="wrap">
<div class="eyebrow">Temy Digital Workers</div>
<h1>AI workers that do <em>real back-office work</em> inside the systems you already use.</h1>
<p class="lead">Each digital worker is one job done end to end: it reads the source documents, does the work in your business system, and asks a person to approve before anything is posted or sent. Every step is logged as evidence.</p>
<a class="btn" href="#contact">Talk to us</a><a class="btn ghost" href="#workers">See the workers</a>
</div></section>

<section id="workers"><div class="wrap">
<h2>The workers</h2>
<p class="lead">Built for Microsoft-centred businesses and the IT partners who serve them.</p>
<div class="grid">
<div class="card"><span class="tag">Finance</span><h3>AP Clerk</h3><p>Reads supplier invoices, matches them to vendors and purchase orders, and drafts bills in Microsoft Dynamics 365 Business Central or QuickBooks for approval.</p></div>
<div class="card"><span class="tag">Finance</span><h3>AR and Collections</h3><p>Tracks overdue invoices, drafts polite reminders and records promises to pay, so cash comes in without a person chasing every customer.</p></div>
<div class="card"><span class="tag">Compliance</span><h3>Compliance Evidence Officer</h3><p>Collects evidence for ISO 27001 and SOC 2 controls from Microsoft 365, Entra, Defender and Purview, grades each control and explains every finding.</p></div>
<div class="card"><span class="tag">Security</span><h3>Alert Triage</h3><p>Reviews Microsoft Defender alerts, enriches them with threat intelligence and known-exploited vulnerability data, and proposes the next action for an analyst.</p></div>
<div class="card"><span class="tag">Sales</span><h3>Sales Assistant</h3><p>Enriches and qualifies leads in Dynamics 365 Sales or HubSpot and writes the results back to the CRM record.</p></div>
<div class="card"><span class="tag">Microsoft 365</span><h3>Copilot Readiness</h3><p>Checks a Microsoft 365 tenant for the permissions, labels and sharing settings that should be fixed before rolling out Copilot.</p></div>
</div>
</div></section>

<section id="how"><div class="wrap">
<h2>How it works</h2>
<div class="grid steps">
<div class="card"><h3>Connect</h3><p>The worker connects to your systems with its own scoped account. You choose what it may read and what it may change.</p></div>
<div class="card"><h3>Work and ask</h3><p>It does the job and stops for a person's approval before posting, sending or changing anything that matters.</p></div>
<div class="card"><h3>Prove</h3><p>Every run keeps its inputs, decisions and results, so you can see what was done, by whom and why.</p></div>
</div>
</div></section>

<section><div class="wrap">
<div class="grid">
<div class="card"><h3>Your data stays yours</h3><p>Workers can run in our cloud or inside your own Azure subscription. Customer data is used only to do the job and is never used to train models.</p></div>
<div class="card"><h3>Pay for work done</h3><p>Simple monthly plans, with usage-based options priced per document or per task.</p></div>
<div class="card"><h3>Built by Temy</h3><p>Made by the engineering team behind Temy, building software for businesses in the UK, EU and US.</p></div>
</div>
</div></section>

<section id="contact"><div class="wrap">
<div class="card">
<h2>Contact</h2>
<p>For a demo, a pilot or partnership questions, email <a href="mailto:{CONTACT}">{CONTACT}</a>. We reply within one business day.</p>
<p class="small" style="margin-top:12px">{LEGAL} &middot; Ground Floor, 41 Devonshire Street, London W1G 7AJ, United Kingdom</p>
</div>
</div></section>
</main>"""

PRIVACY = f"""<main class="wrap"><article class="doc">
<h1>Privacy policy</h1>
<p class="small">Last updated: 24 November 2026</p>
<h2>1. Who we are</h2>
<p>Temy Digital Workers is a trading name of {LEGAL} ("we", "us"), a limited liability partnership registered in England and Wales (OC404423), with its registered office at Ground Floor, 41 Devonshire Street, London W1G 7AJ, United Kingdom. We are the controller of the personal data described in this policy. Contact: <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
<h2>2. Data we collect</h2>
<ul>
<li><b>Contact and account data:</b> name, business email, company, job title and phone number that you give us when you contact us, sign up or buy a subscription (including through Microsoft Marketplace or a reseller).</li>
<li><b>Subscription and billing data:</b> plan, usage quantities, subscription identifiers and invoices. Payment card details are handled by the marketplace or payment provider, not by us.</li>
<li><b>Customer content:</b> documents and records that a digital worker processes on your instructions. For customer content we act as a <b>processor</b> on behalf of the customer, under our terms and any data processing agreement.</li>
<li><b>Technical data:</b> logs of sign-ins and worker runs needed to operate, secure and support the service.</li>
</ul>
<h2>3. Why we use it and our legal basis</h2>
<ul>
<li>To provide the service and support (performance of a contract).</li>
<li>To bill and keep accounting records (legal obligation).</li>
<li>To keep the service secure and improve its reliability (legitimate interests).</li>
<li>To reply to enquiries and, where you agree, send product news (legitimate interests or consent; you can opt out at any time).</li>
</ul>
<p>We do not sell personal data and we do not use customer content to train AI models.</p>
<h2>4. Who we share it with</h2>
<p>Hosting and infrastructure providers, AI model providers acting as our processors, Microsoft or the reseller through which you bought the service, and professional advisers, each under appropriate contracts. We disclose data to authorities only where the law requires it.</p>
<h2>5. International transfers</h2>
<p>Where data is transferred outside the UK or EEA, we use adequacy decisions or standard contractual clauses (including the UK International Data Transfer Addendum).</p>
<h2>6. How long we keep it</h2>
<p>Account and billing data for as long as the subscription runs and then as long as tax and accounting law requires (normally six years). Customer content and run logs for the period set in the customer's contract, after which they are deleted.</p>
<h2>7. Your rights</h2>
<p>You may ask for access, correction, deletion, restriction or portability of your personal data, and object to processing based on legitimate interests. Email <a href="mailto:{CONTACT}">{CONTACT}</a>. You can also complain to the UK Information Commissioner's Office (ico.org.uk).</p>
<h2>8. Cookies</h2>
<p>This website uses no tracking or advertising cookies. The service itself uses only cookies needed to keep you signed in.</p>
<h2>9. Changes</h2>
<p>We will post any changes on this page and update the date above.</p>
</article></main>"""

TERMS = f"""<main class="wrap"><article class="doc">
<h1>Terms of service</h1>
<p class="small">Last updated: 24 November 2026</p>
<h2>1. Who you contract with</h2>
<p>These terms are between you (the customer) and {LEGAL}, trading as Temy Digital Workers, registered in England and Wales (OC404423), Ground Floor, 41 Devonshire Street, London W1G 7AJ ("we"). If you buy through Microsoft Marketplace or a reseller, the commercial terms of that channel also apply; if they conflict with these terms on price, billing or payment, the channel's terms win.</p>
<h2>2. The service</h2>
<p>We provide software-based digital workers that perform tasks in systems you connect. You decide which systems a worker may access. Actions that change records or send messages are submitted for approval by your staff unless you configure otherwise.</p>
<h2>3. Your responsibilities</h2>
<ul>
<li>You have the right to connect the systems and data you give the workers access to.</li>
<li>You review and approve the worker's proposed actions; final business decisions remain yours.</li>
<li>You keep your sign-in details secure and do not use the service unlawfully.</li>
</ul>
<h2>4. Fees</h2>
<p>Fees are as shown in your plan or offer. Usage-based charges are measured by the service and reported to the billing channel. Fees are exclusive of taxes unless stated.</p>
<h2>5. Data</h2>
<p>You own your content. We process it only to provide the service, as described in our <a href="/privacy.html">privacy policy</a> and any data processing agreement between us. We do not use your content to train AI models.</p>
<h2>6. Availability and support</h2>
<p>We aim to keep the service available and to respond to support requests within one business day (see <a href="/support.html">Support</a>). Planned maintenance is announced in advance where practical.</p>
<h2>7. Warranties and liability</h2>
<p>The service is provided with reasonable skill and care. AI output can contain errors, which is why approval steps exist. To the extent permitted by law, our total liability in any 12 months is limited to the fees you paid in that period, and we are not liable for indirect or consequential loss. Nothing limits liability that cannot be limited by law.</p>
<h2>8. Term and termination</h2>
<p>Subscriptions renew for the billing term unless cancelled through the channel you bought from. Either party may terminate for material breach not fixed within 30 days of notice. On termination we delete your content after 30 days unless you ask us to return it first.</p>
<h2>9. Law</h2>
<p>These terms are governed by the laws of England and Wales, and the courts of England and Wales have exclusive jurisdiction.</p>
<h2>10. Contact</h2>
<p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
</article></main>"""

SUPPORT = f"""<main class="wrap"><article class="doc">
<h1>Support</h1>
<p>Email <a href="mailto:{CONTACT}">{CONTACT}</a> with your company name, the worker concerned and, if you have it, the run ID shown in the worker's history.</p>
<h2>Response times</h2>
<ul>
<li>First response within one business day (Monday to Friday, 09:00 to 18:00 UK time).</li>
<li>A worker that has stopped working for all users is handled first.</li>
</ul>
<h2>Subscriptions bought through Microsoft Marketplace or a reseller</h2>
<p>For billing and cancellation, use the channel you bought from. For anything about how a worker behaves, contact us directly.</p>
<h2>Security issues</h2>
<p>Report suspected vulnerabilities to <a href="mailto:{CONTACT}">{CONTACT}</a> with "Security" in the subject line.</p>
<p class="small">{LEGAL}, Ground Floor, 41 Devonshire Street, London W1G 7AJ, United Kingdom.</p>
</article></main>"""

page("index.html", "Temy Digital Workers", "AI digital workers for finance, compliance, security and sales, built on Microsoft systems.", INDEX)
page("privacy.html", "Privacy policy | Temy Digital Workers", "Privacy policy of Temy Digital Workers.", PRIVACY)
page("terms.html", "Terms of service | Temy Digital Workers", "Terms of service of Temy Digital Workers.", TERMS)
page("support.html", "Support | Temy Digital Workers", "How to get support for Temy Digital Workers.", SUPPORT)
page("404.html", "Not found | Temy Digital Workers", "Page not found.", '<main class="wrap"><article class="doc"><h1>Page not found</h1><p><a href="/">Back to the home page</a></p></article></main>')


print("built")
