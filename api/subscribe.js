// AcneSafeCheck newsletter/waitlist signup — adds a contact to a Resend Audience.
// Requires env vars (set in Vercel → Project → Settings → Environment Variables):
//   RESEND_API_KEY        — your Resend API key (server-side only, never exposed to the browser)
//   RESEND_AUDIENCE_ID    — the Audience to add contacts to (create one in the Resend dashboard)
// Optional: RESEND_PREMIUM_AUDIENCE_ID for the premium waitlist.

function readRaw(req) {
  return new Promise((resolve) => {
    let d = ''; req.on('data', c => (d += c));
    req.on('end', () => resolve(d)); req.on('error', () => resolve(''));
  });
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }
  if (req.method !== 'POST') { res.statusCode = 405; return res.end(JSON.stringify({ error: 'POST only' })); }

  let body = req.body;
  if (!body || typeof body !== 'object') { try { body = JSON.parse(await readRaw(req)); } catch (e) { body = {}; } }
  const email = String((body && body.email) || '').trim();
  const list = String((body && body.list) || 'newsletter');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    res.statusCode = 400; return res.end(JSON.stringify({ ok: false, error: 'Invalid email' }));
  }

  const KEY = process.env.RESEND_API_KEY;
  const AUD = list === 'premium-waitlist'
    ? (process.env.RESEND_PREMIUM_AUDIENCE_ID || process.env.RESEND_AUDIENCE_ID)
    : process.env.RESEND_AUDIENCE_ID;
  if (!KEY || !AUD) {
    res.statusCode = 200;
    return res.end(JSON.stringify({ ok: false, configured: false, message: 'Email provider not configured yet.' }));
  }

  try {
    const r = await fetch(`https://api.resend.com/audiences/${AUD}/contacts`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, unsubscribed: false })
    });
    if (r.ok || r.status === 409) { res.statusCode = 200; return res.end(JSON.stringify({ ok: true })); }
    const detail = (await r.text()).slice(0, 200);
    res.statusCode = 502; return res.end(JSON.stringify({ ok: false, error: 'provider_error', detail }));
  } catch (e) {
    res.statusCode = 502; return res.end(JSON.stringify({ ok: false, error: String(e).slice(0, 200) }));
  }
};
