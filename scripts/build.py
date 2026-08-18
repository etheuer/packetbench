#!/usr/bin/env python3
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
DATA = json.loads((ROOT / "data" / "offers.json").read_text())
OFFERS = DATA["offers"]
STUDIO = DATA["studio"]
TAGLINE = DATA["tagline"]
PROMISE = DATA["promise"]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def page(title: str, body: str, desc: str) -> str:
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
  <header>
    <a href="/">{esc(STUDIO)}</a>
    <nav>
      <a href="/#desks">Desks</a>
      <a href="/legal/terms.html">Terms</a>
      <a href="/legal/privacy.html">Privacy</a>
    </nav>
  </header>
  <main>
{body}
  </main>
  <footer>
    <p>{esc(STUDIO)} assembles operational packets. We do not provide legal, medical, tax, or insurance advice. You own every submission and attestation.</p>
    <p><a href="/legal/terms.html">Terms</a> · <a href="/legal/privacy.html">Privacy</a></p>
  </footer>
</body>
</html>
"""


def index() -> str:
    cards = []
    for o in OFFERS:
        cards.append(
            f"""    <a class="card" href="/offers/{esc(o['id'])}.html">
      <div class="kicker">{esc(o['lens'])} · {esc(o['id'][:2])}</div>
      <h3>{esc(o['name'])}</h3>
      <p>{esc(o['failure'])}</p>
      <p class="price">{esc(o['price'])}</p>
    </a>"""
        )
    body = f"""    <p class="kicker">Twenty desks. One studio.</p>
    <h1>{esc(TAGLINE)}</h1>
    <p class="lede">{esc(PROMISE)} Each desk is a fixed-scope packet for a named US operator. No audience required. You pay for a completed file, not software.</p>
    <p class="note">These are live offers. Checkout wires when Stripe is connected. Intake is open as soon as the lead hook is set.</p>
    <h2 id="desks">The desks</h2>
    <div class="grid">
{chr(10).join(cards)}
    </div>
"""
    return page(f"{STUDIO} — {TAGLINE}", body, TAGLINE)


def offer_page(o: dict) -> str:
    body = f"""    <p class="kicker">{esc(o['lens'])} desk · {esc(o['id'])}</p>
    <h1>{esc(o['name'])}</h1>
    <p class="lede">For {esc(o['icp'])}.</p>
    <div class="box">
      <p><strong>The failure.</strong> {esc(o['failure'])}</p>
      <p><strong>What it costs.</strong> {esc(o['cost'])}</p>
      <p><strong>What you get.</strong> {esc(o['deliverable'])}</p>
      <p><strong>Price.</strong> {esc(o['price'])}. {esc(o['price_note'])}</p>
      <p><strong>We will not.</strong> {esc(o['not'])}</p>
    </div>
    <h2>Request this packet</h2>
    <p class="note">No fake urgency. If we cannot take the job this week we will say so.</p>
    <form id="lead" class="box">
      <input class="hp" name="company_website" tabindex="-1" autocomplete="off">
      <input type="hidden" name="offer_id" value="{esc(o['id'])}">
      <label>Name<input name="name" required></label>
      <label>Work email<input name="email" type="email" required></label>
      <label>Company<input name="company"></label>
      <label>What is due, and when?<textarea name="message" rows="5" required></textarea></label>
      <label><input type="checkbox" name="consented" required> I agree to the <a href="/legal/privacy.html">privacy notice</a> and understand this is not legal, medical, tax, or insurance advice.</label>
      <p><button class="cta" type="submit">Request kickoff — {esc(o['price'])}</button></p>
      <p id="status" class="note"></p>
    </form>
    <script>
    const form = document.getElementById('lead');
    const status = document.getElementById('status');
    const params = new URLSearchParams(location.search);
    form.addEventListener('submit', async (e) => {{
      e.preventDefault();
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
          headers: {{'content-type': 'application/json'}},
          body: JSON.stringify(payload)
        }});
        const j = await r.json();
        if (r.ok && j.ok) {{
          status.className = 'ok';
          status.textContent = 'Received. We will reply from the studio mailbox.';
          form.reset();
        }} else if (j.error === 'INTAKE_NOT_WIRED') {{
          status.className = 'err';
          status.textContent = 'Intake is not wired yet. Email the studio operator directly.';
        }} else {{
          status.className = 'err';
          status.textContent = 'Could not send. Try again or email the studio.';
        }}
      }} catch (err) {{
        status.className = 'err';
        status.textContent = 'Network error.';
      }}
    }});
    </script>
"""
    return page(f"{o['name']} — {STUDIO}", body, o["failure"])


def terms() -> str:
    body = """    <h1>Terms</h1>
    <p>Packetbench sells document-assembly and operations-support packets. You remain solely responsible for every filing, attestation, clinical decision, insurance decision, tax position, and legal conclusion.</p>
    <p>Fees pay for a completed packet or a bounded monthly queue. We do not promise regulator approval, platform reinstatement, recovered cash, or claim payment.</p>
    <p>PHI and other regulated data is accepted only after a written BAA or equivalent. Until then, send redacted samples only.</p>
    <p>Texas law governs, excluding conflict rules. These terms are a working draft until a lawyer reviews them.</p>
"""
    return page("Terms — Packetbench", body, "Packetbench terms")


def privacy() -> str:
    body = """    <h1>Privacy</h1>
    <p>We collect the name, email, company, and message you submit, plus basic attribution (referrer, landing path, UTM). We use that to reply and deliver the packet.</p>
    <p>We do not sell leads. We do not use your files to train public models.</p>
    <p>Do not send Social Security numbers, full medical records, or complete card numbers through the form.</p>
    <p>To delete a lead, email the address that replied to you. This notice is a working draft until counsel reviews it.</p>
"""
    return page("Privacy — Packetbench", body, "Packetbench privacy")


def main() -> None:
    (PUBLIC / "offers").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "legal").mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(index())
    (PUBLIC / "legal" / "terms.html").write_text(terms())
    (PUBLIC / "legal" / "privacy.html").write_text(privacy())
    for o in OFFERS:
        (PUBLIC / "offers" / f"{o['id']}.html").write_text(offer_page(o))
    print(f"wrote {2 + len(OFFERS)} html pages")


if __name__ == "__main__":
    main()
