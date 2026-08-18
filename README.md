# Packetbench

Twenty US-first concierge desks on one storefront.

A stranger should be able to read an offer, request a kickoff, and pay.
Delivery is manual. Software comes after paid demand.

## Local

```bash
python3 scripts/build.py
python3 -m http.server 8765 --directory public
```

Lead API: `api/lead.js` on Vercel. Set one of:

- `LEAD_WEBHOOK_URL`
- `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`

Optional later: Stripe payment links per offer.

## Do not

- Fake testimonials or metrics
- Promise regulator approval, recovered cash, or clinical/legal conclusions
- Commit secrets
