// Minimal first-party funnel-event beacon. No cookies, no PII — just an event
// name counter so "do people use the checker / try to subscribe?" is answerable.
// Events show up in Vercel function logs (filter on "acs_event").
// GET or POST /api/event?e=<name>  → 204
const ALLOWED = new Set([
  'check_run', 'fungal_run', 'scan_run',
  'subscribe_attempt', 'subscribe_ok', 'subscribe_fail',
  'cheatsheet_download', 'api_docs_view'
]);

// Soft per-IP limit so the log can't be flooded (per warm instance).
const RATE_MAX = 60, RATE_WINDOW_MS = 60 * 1000;
const hits = new Map();
function limited(ip) {
  const now = Date.now();
  if (hits.size > 5000) { for (const [k, v] of hits) { if (now - v.t > RATE_WINDOW_MS) hits.delete(k); } }
  const h = hits.get(ip);
  if (!h || now - h.t > RATE_WINDOW_MS) { hits.set(ip, { t: now, n: 1 }); return false; }
  h.n += 1;
  return h.n > RATE_MAX;
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', 'https://acnesafecheck.com');
  res.setHeader('Cache-Control', 'no-store');
  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  const e = String((req.query && req.query.e) || '').slice(0, 40);
  if (ALLOWED.has(e) && !limited(ip)) {
    console.log('acs_event', e); // aggregate counting via log search; no IP/PII logged
  }
  res.statusCode = 204;
  res.end();
};
