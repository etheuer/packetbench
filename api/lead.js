export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.statusCode = 405;
    res.setHeader("Allow", "POST");
    return res.end("Method not allowed");
  }

  let body = "";
  for await (const chunk of req) body += chunk;
  let data;
  try {
    data = JSON.parse(body || "{}");
  } catch {
    res.statusCode = 400;
    return json(res, { ok: false, error: "invalid_json" });
  }

  if (data.company_website) {
    return json(res, { ok: true });
  }

  const required = ["name", "email", "offer_id", "message"];
  for (const key of required) {
    if (!String(data[key] || "").trim()) {
      res.statusCode = 400;
      return json(res, { ok: false, error: `missing_${key}` });
    }
  }

  const email = String(data.email).trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    res.statusCode = 400;
    return json(res, { ok: false, error: "bad_email" });
  }

  const payload = {
    name: String(data.name).slice(0, 200),
    email,
    offer_id: String(data.offer_id).slice(0, 80),
    company: String(data.company || "").slice(0, 200),
    message: String(data.message).slice(0, 4000),
    utm_source: String(data.utm_source || "").slice(0, 120),
    utm_medium: String(data.utm_medium || "").slice(0, 120),
    utm_campaign: String(data.utm_campaign || "").slice(0, 120),
    referrer: String(data.referrer || "").slice(0, 500),
    path: String(data.path || "").slice(0, 200),
    consented: Boolean(data.consented),
    received_at: new Date().toISOString(),
  };

  const webhook = process.env.LEAD_WEBHOOK_URL;
  const tgToken = process.env.TELEGRAM_BOT_TOKEN;
  const tgChat = process.env.TELEGRAM_CHAT_ID;

  if (!webhook && !tgToken) {
    res.statusCode = 503;
    return json(res, { ok: false, error: "INTAKE_NOT_WIRED" });
  }

  try {
    if (webhook) {
      const r = await fetch(webhook, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!r.ok) throw new Error(`webhook_${r.status}`);
    }
    if (tgToken && tgChat) {
      const text = [
        `Packetbench lead: ${payload.offer_id}`,
        `${payload.name} <${payload.email}>`,
        payload.company ? `Company: ${payload.company}` : "",
        payload.message,
      ]
        .filter(Boolean)
        .join("\n");
      const r = await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ chat_id: tgChat, text: text.slice(0, 3500) }),
      });
      if (!r.ok) throw new Error(`telegram_${r.status}`);
    }
  } catch (err) {
    res.statusCode = 502;
    return json(res, { ok: false, error: "forward_failed" });
  }

  return json(res, { ok: true });
}

function json(res, obj) {
  res.setHeader("content-type", "application/json");
  res.end(JSON.stringify(obj));
}
