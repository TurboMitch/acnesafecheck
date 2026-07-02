// AcneSafeCheck newsletter/waitlist signup — adds a contact to a Resend Audience.
// Requires env vars (set in Vercel → Project → Settings → Environment Variables):
//   RESEND_API_KEY        — your Resend API key (server-side only, never exposed to the browser)
//   RESEND_AUDIENCE_ID    — the Audience to add contacts to (create one in the Resend dashboard)
// Optional: RESEND_PREMIUM_AUDIENCE_ID for the premium waitlist.
//
// NOTE: for real list-bombing protection also enable double opt-in on the Resend
// Audience — the in-memory limiter below is per-instance (Vercel may run several).

const MAX_BODY_BYTES = 4096;

// Per-IP rate limit: max 5 signups per 10 minutes per warm instance.
const RATE_MAX = 5, RATE_WINDOW_MS = 10 * 60 * 1000;
const hits = new Map();
function rateLimited(ip) {
  const now = Date.now();
  if (hits.size > 5000) { // bound memory
    for (const [k, v] of hits) { if (now - v.t > RATE_WINDOW_MS) hits.delete(k); }
  }
  const h = hits.get(ip);
  if (!h || now - h.t > RATE_WINDOW_MS) { hits.set(ip, { t: now, n: 1 }); return false; }
  h.n += 1;
  return h.n > RATE_MAX;
}

function readRaw(req) {
  return new Promise((resolve) => {
    let d = '', done = false, size = 0;
    const settle = (v) => { if (!done) { done = true; resolve(v); } };
    req.on('data', c => {
      size += c.length;
      if (size > MAX_BODY_BYTES) { settle(''); try { req.destroy(); } catch (_) {} return; }
      d += c;
    });
    req.on('end', () => settle(d));
    req.on('error', () => settle(''));
    req.on('close', () => settle(''));
    setTimeout(() => settle(''), 5000); // never hang on a stalled/consumed stream
  });
}

module.exports = async (req, res) => {
  // Signup forms only live on the site itself — no cross-origin use case.
  res.setHeader('Access-Control-Allow-Origin', 'https://acnesafecheck.com');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }
  if (req.method !== 'POST') { res.statusCode = 405; return res.end(JSON.stringify({ error: 'POST only' })); }

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (rateLimited(ip)) {
    res.statusCode = 429;
    return res.end(JSON.stringify({ ok: false, error: 'Too many requests — try again later.' }));
  }

  let body = req.body;
  if (!body || typeof body !== 'object') { try { body = JSON.parse(await readRaw(req)); } catch (e) { body = {}; } }
  const email = String((body && body.email) || '').trim().slice(0, 254);
  const list = String((body && body.list) || 'newsletter');
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    res.statusCode = 400; return res.end(JSON.stringify({ ok: false, error: 'Invalid email' }));
  }

  const KEY = process.env.RESEND_API_KEY;
  const AUD = list === 'premium-waitlist'
    ? (process.env.RESEND_PREMIUM_AUDIENCE_ID || process.env.RESEND_AUDIENCE_ID)
    : process.env.RESEND_AUDIENCE_ID;
  if (!KEY || !AUD) {
    // Log so signups attempted before configuration are at least recoverable from logs.
    console.warn('subscribe: provider not configured; dropping signup for list=' + list);
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
    // Log provider detail server-side; never echo it to the client.
    console.error('subscribe: provider error', r.status, (await r.text()).slice(0, 500));
    res.statusCode = 502; return res.end(JSON.stringify({ ok: false, error: 'provider_error' }));
  } catch (e) {
    console.error('subscribe: request failed', e);
    res.statusCode = 502; return res.end(JSON.stringify({ ok: false, error: 'provider_error' }));
  }
};
