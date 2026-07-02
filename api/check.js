// AcneSafeCheck public API — Vercel serverless function.
// GET /api/check?ingredient=coconut%20oil
// GET /api/check?ingredients=water,glycerin,coconut%20oil
const DB = require('../db.json');

// Null-prototype map: user input like "constructor" must not hit Object.prototype.
const lookup = Object.create(null);
DB.forEach(it => (it.a || []).forEach(al => { lookup[al] = it; }));

const MAX_INPUT_CHARS = 20000; // ~ a very long INCI list; reject beyond
const MAX_TOKENS = 200;
const MAX_TOKEN_CHARS = 200;

function normalize(s) {
  return String(s).toLowerCase()
    .replace(/\([^)]*\)/g, ' ')
    .replace(/[^a-z0-9&/\-\s]/g, ' ')
    .replace(/\s+/g, ' ').trim();
}
// Exact alias match, else the alias as a whole-word SUFFIX of the token (INCI names put the
// chemical head-noun last: "cocos nucifera coconut oil" -> "coconut oil"). The old substring
// match returned confidently-wrong results ("sucrose stearate" -> Sucrose 0/5).
function match(token) {
  const n = normalize(String(token).slice(0, MAX_TOKEN_CHARS));
  if (lookup[n]) return { item: lookup[n], matchType: 'exact' };
  for (const al in lookup) {
    if (al.length > 5 && n.length > al.length && n.endsWith(' ' + al)) {
      return { item: lookup[al], matchType: 'partial' };
    }
  }
  return null;
}
function fmt(m) {
  if (!m) return null;
  const it = m.item;
  return {
    name: it.n, rating: it.r, category: it.c,
    poreClogging: it.r >= 3, fungalAcneTrigger: !!it.fa,
    match: m.matchType,
    slug: it.s, url: `https://acnesafecheck.com/ingredient/${it.s}.html`
  };
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 's-maxage=86400, stale-while-revalidate');
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }

  const q = req.query || {};
  const send = (obj, status) => { res.statusCode = status || 200; res.end(JSON.stringify(obj)); };

  if (q.ingredient) {
    const input = String(q.ingredient);
    if (input.length > MAX_TOKEN_CHARS) return send({ error: `ingredient too long (max ${MAX_TOKEN_CHARS} chars)` }, 400);
    return send({ query: input, result: fmt(match(input)) });
  }
  if (q.ingredients) {
    const raw = String(q.ingredients);
    if (raw.length > MAX_INPUT_CHARS) return send({ error: `input too long (max ${MAX_INPUT_CHARS} chars)` }, 400);
    // Same tokenizer as the website checker (includes bullet separators).
    const list = raw.split(/[,;\n•·]+/).map(s => s.trim()).filter(Boolean);
    if (list.length > MAX_TOKENS) return send({ error: `too many ingredients (max ${MAX_TOKENS})` }, 400);
    // Consistent shape: every element is { input, result: object|null }.
    const results = list.map(t => ({ input: t, result: fmt(match(t)) }));
    const rated = results.filter(r => r.result);
    const summary = {
      total: list.length,
      matched: rated.length,
      poreClogging: rated.filter(r => r.result.rating >= 3).length,
      fungalAcneTriggers: rated.filter(r => r.result.fungalAcneTrigger).length
    };
    return send({ summary, results });
  }

  return send({
    name: 'AcneSafeCheck API',
    description: 'Comedogenicity (0–5) and fungal-acne data for cosmetic ingredients.',
    database_size: DB.length,
    usage: [
      'GET /api/check?ingredient=coconut oil',
      'GET /api/check?ingredients=water,glycerin,coconut oil,niacinamide'
    ],
    limits: { maxIngredients: MAX_TOKENS, maxInputChars: MAX_INPUT_CHARS },
    license: 'Ratings are general guidance, not medical advice. Attribution to acnesafecheck.com appreciated.',
    docs: 'https://acnesafecheck.com/api.html'
  });
};
