# Redesign brief: 20 standalone B2B offer pages

## Job

Give `/root/packetbench` a visual personality. Pages convert but look like a blank government form. Keep the generator. Do not invent a second site.

Run `python3 /root/packetbench/scripts/build.py` when CSS/HTML template changes. Do not create 20 hand-edited HTML files.

## Current system

- Template lives in `/root/packetbench/scripts/build.py` (`offer_page`, `nav`, `footer`, `shell`)
- Styles: `/root/packetbench/public/styles.css`
- Copy sources: `data/hormozi.json`, `data/conversion.json`, `LANDING` in build.py
- Live: https://packetbench.vercel.app/offers/01-pecos-revalidation.html
- Offer pages must stay standalone (no Packetbench catalog, no link to the other 19)
- Short brand in nav (PECOS File, FDA Renewal, …)

## Benchmarks to steal from (open these)

1. https://unbounce.com/landing-page-examples/best-b2b-landing-page-examples/
   - One goal per page.
   - Adult B2B (their Blue Forest Farms note): taken seriously, not startup-cute.
2. https://front.com/teams/customer-service-support/
   - Pain in the hero. A concrete visual of the work, not a gradient blob.
3. https://directiveconsulting.com/services/ppc-agency/
   - Professional-services trust: process and expertise, not a SaaS screenshot theater.
4. Pattern from 2026 B2B roundups (Instapage, Flowtrix, Popupsmart):
   - Benefit headline, CTA visible without scroll
   - Short form
   - Proof near the ask
   - Repeat one CTA
   - Mobile-first
   We have no customers, so proof = the actual file contents + turnaround + what we will not do. Never fake logos or quotes.

## Design read (commit to this)

Reading this as: professional-services landing for a US operator with a deadline.
Vibe: print shop + federal file clerk. Not Linear SaaS. Not beige luxury DTC. Not the current stone-plain page.
Dials: VARIANCE 6 / MOTION 3 / DENSITY 4.

World to build:
- Paper that feels printed (cool bone or pale sage, not cream-brass)
- One stamp color (oxide red or filing-cabinet green). One accent only.
- Numbered exhibits, hairline rules, a folder/document object in the hero that looks designed, not a gray box
- Self-hosted Geist is already in `/root/packetbench/public/fonts/`. Keep it or add one more self-hosted face. No Google Fonts. No Inter. No Fraunces.
- Dark mode via prefers-color-scheme is already expected.

## Copy rules

- Keep facts (price, turnaround, no-login, no legal/medical advice).
- You may tighten headlines/subs in hormozi.json if they still sound like slogans.
- Banned: em-dashes, fake testimonials, packaged-dollar stacks, "Buy this if", DFY, sit-beside, Packetbench on offer pages, AI-purple, three identical icon cards as the page structure.

## Sections that must remain (order can tighten)

Hero (headline, who, fee, CTA) → what’s in the file → what this is → who it is for → how work runs → included → fee + limits → missing-item redo → questions → request form.

## Done when

- `python3 /root/packetbench/scripts/build.py` succeeds
- All 20 `/root/packetbench/public/offers/*.html` rebuilt
- Offer 01 has a distinct first viewport (not the current gray column)
- No banned strings above
- You write `/root/packetbench/REDESIGN_NOTES.md` with: world chosen, what you stole from each reference URL, what you refused.

Do not deploy. Do not buy fonts. Do not add node/npm.
