#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DATA = json.loads((ROOT / "data" / "offers.json").read_text())
OFFERS = {o["id"]: o for o in DATA["offers"]}

# Per-desk landing copy. No em-dashes. Headlines stay short.
LANDING = {
    "01-pecos-revalidation": {
        "headline": "Your PECOS window is already running.",
        "sub": "We assemble the revalidation packet. Your official attests and submits.",
        "buyer": "Practice administrator or authorized official",
        "packet": [
            "Due-date extract from the CMS revalidation list",
            "Document inventory mapped to PECOS screens",
            "Draft answers for your official to review",
            "Submit-day click path, written for one sitting",
        ],
        "steps": [
            ("Send the CMS line", "NPI, due month, and who can attest. Redacted samples only."),
            ("We build the file", "Checklist, missing-doc list, and draft responses in five business days."),
            ("You attest", "You log into PECOS. We do not hold your password or click Submit."),
        ],
        "turnaround": "5 business days for one enrollment record",
    },
    "02-fda-ffr-renewal": {
        "headline": "The 2026 FDA renewal window is open.",
        "sub": "We prepare the FURLS worksheet. The owner submits before December 31.",
        "buyer": "Shared-kitchen or copacker owner",
        "packet": [
            "Facility facts worksheet ready to type into FURLS",
            "UFI and DUNS check before you sit down",
            "Click path for the Oct 1 to Dec 31 window",
            "A calendar reminder for December 15",
        ],
        "steps": [
            ("Send facility facts", "Legal name, address, food categories, and who owns the FDA account."),
            ("We fill the worksheet", "You get a sit-beside pack, not a login request."),
            ("Owner submits", "You stay the registrant. We never act as US Agent."),
        ],
        "turnaround": "3 business days per facility",
    },
    "03-osha-ita-hygiene": {
        "headline": "The ITA file is still sitting open.",
        "sub": "We clean last year's submission and set a weekly log so next March is quiet.",
        "buyer": "Safety lead or controller at a covered establishment",
        "packet": [
            "Prior-year 300A file checked against ITA rules",
            "Late-file packet if March 2 already passed",
            "Weekly capture sheet for 2026 cases",
            "A one-page owner note on what you still decide",
        ],
        "steps": [
            ("Export the logs", "300, 300A, and 301 as you already keep them."),
            ("We tidy the file", "Formatting, totals, and a list of questions only you can answer."),
            ("You post and submit", "Recordability stays with you. We do not speak to OSHA."),
        ],
        "turnaround": "Setup in one week, then a monthly hygiene pass",
    },
    "04-fsis-origin-label": {
        "headline": "The origin claim needs a paper trail.",
        "sub": "We map your Product of USA file. Your QA lead keeps the attestations.",
        "buyer": "QA or plant manager at a small FSIS establishment",
        "packet": [
            "Claim inventory from current labels",
            "Document map for born, raised, slaughtered, processed",
            "Gaps called out in plain language",
            "A folder layout your inspector can follow",
        ],
        "steps": [
            ("Send current claims", "Photos or PDFs of labels that say Product of USA or Made in USA."),
            ("We assemble the map", "What you have, what is missing, what QA should sign."),
            ("QA owns the file", "We do not file LSAS or certify origin."),
        ],
        "turnaround": "10 business days for one establishment",
    },
    "05-solar-interconnect": {
        "headline": "One missing model number resets the queue.",
        "sub": "We completeness-check the interconnection packet before the utility sees it.",
        "buyer": "Ops manager at a residential solar installer",
        "packet": [
            "Utility-specific completeness checklist",
            "Equipment list matched to the site plan",
            "A punch list of what still needs the engineer",
            "A resubmit pack if the first file bounced",
        ],
        "steps": [
            ("Drop the draft app", "Site plan, equipment cut sheets, and the utility form."),
            ("We mark every hole", "You get a first-pass file or a punch list, not a redesign."),
            ("Your PE stamps", "We do not engineer or submit as contractor of record."),
        ],
        "turnaround": "2 business days per application",
    },
    "06-gmc-pid-recovery": {
        "headline": "Shopping went dark on a price mismatch.",
        "sub": "We build the SKU ledger and the exact landing-page and feed fixes.",
        "buyer": "Ecommerce lead at a US Shopify brand",
        "packet": [
            "SKU-level price and availability mismatch ledger",
            "Landing-page and schema fixes, written per URL",
            "Feed field corrections ready to upload",
            "A review request note for Merchant Center",
        ],
        "steps": [
            ("Export Diagnostics", "Needs-attention CSV plus three sample product URLs."),
            ("We write the ledger", "Each SKU gets a cause and a fix you can publish."),
            ("You publish and request review", "We do not log into GMC or run ads."),
        ],
        "turnaround": "5 business days for up to 200 flagged SKUs",
    },
    "07-amz-vendor-chargebacks": {
        "headline": "The defect list is eating the margin.",
        "sub": "We build evidence packets from your Vendor Central defect list. You submit.",
        "buyer": "Vendor operations or finance lead",
        "packet": [
            "Reason-coded evidence folder per dispute",
            "Weekly identified versus submitted ledger",
            "A skip list for disputes that are not worth filing",
            "Due-date calendar for the current window",
        ],
        "steps": [
            ("Export the defect list", "IDs, reason codes, and any backup you already have."),
            ("We assemble packets", "You get files named for the dispute, ready to upload."),
            ("You click submit", "We do not promise Amazon reverses the charge."),
        ],
        "turnaround": "Setup in one week, then a weekly packet batch",
    },
    "08-gbp-trade-reinstatement": {
        "headline": "The Maps listing is gone. The phones stopped.",
        "sub": "One appeal packet, matched to your license and address. You submit once.",
        "buyer": "Owner of a licensed home-service trade",
        "packet": [
            "Name, address, and phone match sheet",
            "License and insurance pages ready to upload",
            "Appeal text written for the official form",
            "A do-not-resubmit note so you do not stack appeals",
        ],
        "steps": [
            ("Send the suspension note", "Plus license, utility bill, and the listed address."),
            ("We build one packet", "Identity match first. Then the appeal language."),
            ("You submit once", "We do not guarantee Google brings the listing back."),
        ],
        "turnaround": "3 business days",
    },
    "09-ncci-emod-audit": {
        "headline": "The new mod landed. Nobody checked the worksheet.",
        "sub": "We line up the worksheet against your claim file. Your broker files mismatches.",
        "buyer": "Controller or safety lead at an experience-rated contractor",
        "packet": [
            "Line-by-line worksheet versus claim extract",
            "Class-code and closed-date mismatches called out",
            "A broker-ready exception list",
            "A one-page note on what we did not decide",
        ],
        "steps": [
            ("Send the worksheet", "NCCI or state copy, plus the claim listing you already have."),
            ("We mark mismatches", "You get a file your broker can act on."),
            ("Broker files", "We do not sell insurance or change the mod."),
        ],
        "turnaround": "7 business days for one rating year",
    },
    "10-coi-chase-desk": {
        "headline": "The award is public. You still cannot get on site.",
        "sub": "We chase and match certificates to the exhibit. Your broker issues the certs.",
        "buyer": "Project manager at a specialty subcontractor",
        "packet": [
            "Requirement matrix from the exhibit",
            "Chase log with last-touch dates",
            "Matched COI packet for the GC",
            "A list of gaps only the broker can close",
        ],
        "steps": [
            ("Send the award and exhibit", "Plus current certs and broker contact."),
            ("We chase and match", "You see a living log, not a pile of PDFs."),
            ("Broker issues", "We do not decide if coverage is adequate."),
        ],
        "turnaround": "Setup in 3 days, then a twice-weekly chase",
    },
    "11-prior-auth-chase": {
        "headline": "Auths are sitting in missing-info.",
        "sub": "We run the status queue from your exports. Clinicians still decide necessity.",
        "buyer": "Office manager at an independent specialty clinic",
        "packet": [
            "Daily open-auth status board",
            "Missing-info list with the exact payer ask",
            "Aging over 7 and 14 days",
            "A BAA-first onboarding note",
        ],
        "steps": [
            ("Sign a BAA, then export", "No PHI until the agreement is in place."),
            ("We chase status", "Portal work from your logins, or from files you send."),
            ("Clinicians decide", "We never write medical necessity."),
        ],
        "turnaround": "Daily queue once onboarded",
    },
    "12-resto-cash-tax-pack": {
        "headline": "Monday should not start in five POS exports.",
        "sub": "We send a cash and sales-tax exception pack. Your CPA files.",
        "buyer": "Operator or bookkeeper at a multi-unit independent restaurant",
        "packet": [
            "Cash over and short by drawer",
            "Sales-tax exception list",
            "Files named the way your CPA asked",
            "A one-page note on what we did not interpret",
        ],
        "steps": [
            ("Share the POS export", "Toast, Square, or whatever you already run."),
            ("We pack Monday", "Exceptions only. Not a full close."),
            ("CPA files", "We do not give tax advice or file returns."),
        ],
        "turnaround": "Every Monday for the prior week",
    },
    "13-hvac-rebate-filing": {
        "headline": "The job is done. The rebate form is still in the truck.",
        "sub": "We complete utility rebate packets from your job file. You or the homeowner submit.",
        "buyer": "Owner or office manager at a licensed HVAC shop",
        "packet": [
            "Completed utility form from the job packet",
            "Invoice, model, and photo checklist",
            "A not-ready list when a job cannot be filed",
            "A submitted-versus-paid ledger you own",
        ],
        "steps": [
            ("Send closed jobs", "Invoice, equipment photos, and the utility program name."),
            ("We fill the packet", "Only programs with a live mail-in window."),
            ("You submit", "We do not promise the utility pays."),
        ],
        "turnaround": "4 business days per packet",
    },
    "14-pharmacy-pbm-recon": {
        "headline": "The remit does not match your claim file.",
        "sub": "We build a monthly identified-versus-disputed ledger. You decide what to file.",
        "buyer": "Owner or PIC at an independent pharmacy",
        "packet": [
            "835 versus claim exception list",
            "Identified, disputed, and collected columns",
            "A skip list for noise",
            "A one-page note: identified is not cash",
        ],
        "steps": [
            ("Send remits and claims", "One PBM first. Redact where you can."),
            ("We reconcile", "You get a ledger, not a lawsuit memo."),
            ("You file disputes", "We do not give legal advice or guarantee recoveries."),
        ],
        "turnaround": "Monthly, ten business days after you send remits",
    },
    "15-warranty-labor-rescue": {
        "headline": "You already did the work. The labor claim bounced.",
        "sub": "We rebuild the rejected warranty-labor pack with the evidence the OEM asked for.",
        "buyer": "Owner of an independent appliance or HVAC shop",
        "packet": [
            "Rejection reason mapped to missing evidence",
            "Photo and model checklist",
            "Resubmit pack named for the claim number",
            "A do-not-resubmit list when the claim is dead",
        ],
        "steps": [
            ("Send the rejection", "Plus the original claim and job photos."),
            ("We rebuild the pack", "Only what that OEM asked for."),
            ("You resubmit", "We do not promise the manufacturer pays."),
        ],
        "turnaround": "2 business days per claim",
    },
    "16-hotel-ota-shortpay": {
        "headline": "The virtual card posted short again.",
        "sub": "We pull nightly folio exceptions and build dispute packets. You send them.",
        "buyer": "GM or night-audit lead at an independent hotel",
        "packet": [
            "Nightly short-pay and no-show exception list",
            "Dispute packet per reservation",
            "Identified versus submitted ledger",
            "A skip list for noise under your threshold",
        ],
        "steps": [
            ("Export the folio", "PMS plus the OTA remittance you already get."),
            ("We mark exceptions", "Short pays and no-shows, not a full audit."),
            ("You dispute", "We do not promise the OTA pays."),
        ],
        "turnaround": "Nightly file, next morning pack",
    },
    "17-sam-first-award": {
        "headline": "The award hit. The onboarding pile did not.",
        "sub": "A 30-day packet for UEI hygiene, reporting dates, and documents. You stay the registrant.",
        "buyer": "Owner of a first-time federal awardee",
        "packet": [
            "Identifier hygiene checklist (UEI, CAGE, legal name)",
            "30-day reporting calendar",
            "Document list for invoicing and reporting",
            "A note on what APEX or counsel should still do",
        ],
        "steps": [
            ("Send the award line", "PIID, agency, and whether this is your first federal award."),
            ("We build the 30-day pack", "Calendar plus the files you still need to collect."),
            ("You remain the registrant", "We do not bid, certify size, or take your SAM login."),
        ],
        "turnaround": "7 business days",
    },
    "18-new-contractor-pack": {
        "headline": "The license email arrived. The site still will not let you on.",
        "sub": "A first-90-day pack for COI, postings, and workers-comp setup. Your broker finishes.",
        "buyer": "Newly licensed contractor in CA or FL",
        "packet": [
            "State-specific first-90 checklist",
            "COI request draft for your broker",
            "Posting and notice list",
            "A calendar of dates that actually matter",
        ],
        "steps": [
            ("Send the new license", "State, class, and whether you have a broker yet."),
            ("We build the 90-day pack", "Forms and a chase list, not an insurance quote."),
            ("Broker and accountant finish", "We do not sell insurance."),
        ],
        "turnaround": "5 business days",
    },
    "19-fda-warning-cleanup": {
        "headline": "The warning letter is public. The files are not in one place.",
        "sub": "We index registration, labels, and recall-readiness for your counsel. Counsel writes the response.",
        "buyer": "QA lead at a US food facility named on a new letter",
        "packet": [
            "Letter excerpt and date index",
            "Current registration and label inventory",
            "Recall-readiness file list",
            "A handoff memo for counsel, not a legal draft",
        ],
        "steps": [
            ("Counsel is already in", "We will not start without a lawyer on the thread."),
            ("We index the files", "What exists, what is missing, where it lives."),
            ("Counsel writes", "We do not practice law or promise close-out."),
        ],
        "turnaround": "10 business days for the index",
    },
    "20-new-medicare-dme": {
        "headline": "Enrollment is active. The first claims will bounce.",
        "sub": "A first-billing documentation kit. Your biller submits. We do not bill Medicare.",
        "buyer": "Owner or biller at a newly enrolled DME supplier",
        "packet": [
            "First-claim document checklist",
            "Sample packet layout with no beneficiary data",
            "A bounce-reason crib from common rejects",
            "BAA-first onboarding note",
        ],
        "steps": [
            ("Sign a BAA if we will see PHI", "Until then, process only. No beneficiary files."),
            ("We build the kit", "What must sit in the chart before claim one."),
            ("Your biller submits", "We do not determine coverage or send claims."),
        ],
        "turnaround": "7 business days",
    },
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def shell(title: str, desc: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <!--
  THESIS: Each desk is a standalone product page that sells one packet, not a studio catalog.
  OWN-WORLD: Cool paper, ink, one cobalt accent, sharp corners, self-hosted Geist.
  STORY: Visitor sees the failure, the file they get, the price, and can request kickoff.
  FIRST VIEWPORT: Split hero. Headline left, packet contents right, primary CTA under the subtext.
  FORM: Trust-first B2B service landing. Seed: unattended-rebuild-2026-08-18.
  FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
  -->
  {body}
</body>
</html>
"""


def nav(current: str | None = None) -> str:
    mid = f'<span>{esc(OFFERS[current]["name"])}</span>' if current else '<a href="/#desks">Desks</a>'
    return f"""<div class="wrap">
  <nav class="nav">
    <a class="brand" href="/">Packetbench</a>
    <div class="nav-links">
      {mid}
      <a href="/legal/terms.html">Terms</a>
    </div>
  </nav>
</div>"""


def footer() -> str:
    return """<footer>
  <div class="wrap">
    <p>Packetbench assembles operational packets. We do not provide legal, medical, tax, or insurance advice. You own every submission and attestation.</p>
    <p><a href="/legal/terms.html">Terms</a> · <a href="/legal/privacy.html">Privacy</a></p>
  </div>
</footer>"""


def offer_page(oid: str) -> str:
    o = OFFERS[oid]
    L = LANDING[oid]
    items = "\n".join(f"          <li>{esc(x)}</li>" for x in L["packet"])
    steps = "\n".join(
        f'      <div class="step"><h3>{esc(t)}</h3><p>{esc(b)}</p></div>'
        for t, b in L["steps"]
    )
    body = f"""{nav(oid)}
  <div class="wrap">
    <section class="hero">
      <div>
        <h1>{esc(L["headline"])}</h1>
        <p class="sub">{esc(L["sub"])}</p>
        <div class="actions">
          <a class="btn" href="#request">Request this packet</a>
          <a class="btn ghost" href="#includes">See what is in it</a>
        </div>
      </div>
      <aside class="packet">
        <h2>What is in the packet</h2>
        <ol>
{items}
        </ol>
      </aside>
    </section>
  </div>
  <div class="wrap">
    <section class="section" id="includes">
      <h2>How the work runs</h2>
      <p class="lead">Built for the {esc(L["buyer"])}. {esc(L["turnaround"])}.</p>
      <div class="steps">
{steps}
      </div>
    </section>
    <section class="section">
      <h2>Price and limits</h2>
      <div class="price-row">
        <div class="price">{esc(o["price"])}</div>
        <div class="price-note">{esc(o["price_note"])}</div>
      </div>
      <div class="split">
        <div class="block">
          <strong>What you get</strong>
          <p>{esc(o["deliverable"])}</p>
        </div>
        <div class="block">
          <strong>What we will not do</strong>
          <p class="wont">{esc(o["not"])}</p>
        </div>
      </div>
    </section>
    <section class="section" id="request">
      <h2>Request this packet</h2>
      <p class="lead">Tell us what is due and when. If we cannot take the job this week we will say so.</p>
      <form id="lead" class="intake">
        <input class="hp" name="company_website" tabindex="-1" autocomplete="off">
        <input type="hidden" name="offer_id" value="{esc(oid)}">
        <label for="name">Name</label>
        <input id="name" name="name" required>
        <label for="email">Work email</label>
        <input id="email" name="email" type="email" required>
        <label for="company">Company</label>
        <input id="company" name="company">
        <label for="message">What is due, and when?</label>
        <textarea id="message" name="message" rows="5" required></textarea>
        <label class="check"><input type="checkbox" name="consented" required> I agree to the <a href="/legal/privacy.html">privacy notice</a> and understand this is not legal, medical, tax, or insurance advice.</label>
        <button class="btn" type="submit">Request this packet</button>
        <p id="status" class="status"></p>
      </form>
    </section>
  </div>
{footer()}
<script>
const form = document.getElementById('lead');
const status = document.getElementById('status');
const params = new URLSearchParams(location.search);
form.addEventListener('submit', async (e) => {{
  e.preventDefault();
  status.className = 'status';
  status.textContent = 'Sending…';
  const fd = new FormData(form);
  const payload = Object.fromEntries(fd.entries());
  payload.consented = fd.get('consented') === 'on';
  payload.utm_source = params.get('utm_source') || '';
  payload.utm_medium = params.get('utm_medium') || '';
  payload.utm_campaign = params.get('utm_campaign') || '';
  payload.referrer = document.referrer || '';
  payload.path = location.pathname;
  try {{
    const r = await fetch('/api/lead', {{
      method: 'POST',
      headers: {{'content-type':'application/json'}},
      body: JSON.stringify(payload)
    }});
    const j = await r.json();
    if (r.ok && j.ok) {{
      status.className = 'status ok';
      status.textContent = 'Received. We will reply from the studio mailbox.';
      form.reset();
    }} else if (j.error === 'INTAKE_NOT_WIRED') {{
      status.className = 'status err';
      status.textContent = 'Intake is not connected yet. Email the person who sent you this page.';
    }} else {{
      status.className = 'status err';
      status.textContent = 'Could not send. Try again.';
    }}
  }} catch (err) {{
    status.className = 'status err';
    status.textContent = 'Network error.';
  }}
}});
</script>
"""
    return shell(f"{o['name']} | Packetbench", L["headline"], body)


def index() -> str:
    groups = {}
    for o in DATA["offers"]:
        groups.setdefault(o["lens"], []).append(o)
    chunks = []
    for lens, items in groups.items():
        rows = "\n".join(
            f'        <li><a href="/offers/{esc(o["id"])}.html"><span><span class="dn">{esc(o["name"])}</span><div class="dp">{esc(LANDING[o["id"]]["headline"])}</div></span><span class="dp">{esc(o["price"])}</span></a></li>'
            for o in items
        )
        chunks.append(f'      <div><h2>{esc(lens)}</h2><ul class="desk-list">\n{rows}\n      </ul></div>')
    body = f"""{nav()}
  <div class="wrap dir">
    <h1>Operational packets for a named deadline.</h1>
    <p class="sub">Each desk is its own offer. You pay for a completed file, not software.</p>
    <div class="groups" id="desks">
{chr(10).join(chunks)}
    </div>
  </div>
{footer()}
"""
    return shell("Packetbench", "Operational packets for US operators.", body)


def legal(title: str, paras: list[str]) -> str:
    inner = "\n".join(f"    <p>{esc(p)}</p>" for p in paras)
    body = f"""{nav()}
  <div class="wrap dir">
    <h1>{esc(title)}</h1>
{inner}
  </div>
{footer()}
"""
    return shell(f"{title} | Packetbench", title, body)


def main() -> None:
    missing = set(OFFERS) - set(LANDING)
    extra = set(LANDING) - set(OFFERS)
    if missing or extra:
        raise SystemExit(f"landing map mismatch missing={missing} extra={extra}")
    (PUBLIC / "offers").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "legal").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(index())
    (PUBLIC / "legal" / "terms.html").write_text(
        legal(
            "Terms",
            [
                "Packetbench sells document-assembly and operations-support packets. You remain solely responsible for every filing, attestation, clinical decision, insurance decision, tax position, and legal conclusion.",
                "Fees pay for a completed packet or a bounded monthly queue. We do not promise regulator approval, platform reinstatement, recovered cash, or claim payment.",
                "PHI and other regulated data is accepted only after a written BAA or equivalent. Until then, send redacted samples only.",
                "Texas law governs, excluding conflict rules. These terms are a working draft until a lawyer reviews them.",
            ],
        )
    )
    (PUBLIC / "legal" / "privacy.html").write_text(
        legal(
            "Privacy",
            [
                "We collect the name, email, company, and message you submit, plus basic attribution (referrer, landing path, UTM). We use that to reply and deliver the packet.",
                "We do not sell leads. We do not use your files to train public models.",
                "Do not send Social Security numbers, full medical records, or complete card numbers through the form.",
                "To delete a lead, email the address that replied to you. This notice is a working draft until counsel reviews it.",
            ],
        )
    )
    for oid in OFFERS:
        (PUBLIC / "offers" / f"{oid}.html").write_text(offer_page(oid))
    # Ban check
    bad = []
    for p in PUBLIC.rglob("*.html"):
        t = p.read_text()
        if "—" in t or "–" in t:
            bad.append(str(p))
    if bad:
        raise SystemExit(f"em/en dash in {bad}")
    print(f"wrote {2 + len(OFFERS)} html pages")


if __name__ == "__main__":
    main()
