// AcneSafeCheck public API — Vercel serverless function.
// GET /api/check?ingredient=coconut%20oil
// GET /api/check?ingredients=water,glycerin,coconut%20oil
const DB = require('../db.json');

const lookup = {};
DB.forEach(it => (it.a || []).forEach(al => { lookup[al] = it; }));

function normalize(s) {
  return String(s).toLowerCase()
    .replace(/\([^)]*\)/g, ' ')
    .replace(/[^a-z0-9&/\-\s]/g, ' ')
    .replace(/\s+/g, ' ').trim();
}
function match(token) {
  const n = normalize(token);
  if (lookup[n]) return lookup[n];
  for (const al in lookup) { if (al.length > 5 && n.includes(al)) return lookup[al]; }
  return null;
}
function fmt(m) {
  if (!m) return null;
  return {
    name: m.n, rating: m.r, category: m.c,
    poreClogging: m.r >= 3, fungalAcneTrigger: !!m.fa,
    slug: m.s, url: `https://acnesafecheck.com/ingredient/${m.s}.html`
  };
}

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 's-maxage=86400, stale-while-revalidate');
  if (req.method === 'OPTIONS') { res.statusCode = 204; return res.end(); }

  const q = req.query || {};
  const send = (obj) => { res.statusCode = 200; res.end(JSON.stringify(obj)); };

  if (q.ingredient) {
    return send({ query: q.ingredient, result: fmt(match(q.ingredient)) });
  }
  if (q.ingredients) {
    const list = String(q.ingredients).split(/[,;\n]/).map(s => s.trim()).filter(Boolean);
    const results = list.map(t => {
      const m = fmt(match(t));
      return m ? { input: t, ...m } : { input: t, result: null };
    });
    const rated = results.filter(r => typeof r.rating === 'number');
    const summary = {
      total: list.length,
      matched: rated.length,
      poreClogging: rated.filter(r => r.rating >= 3).length,
      fungalAcneTriggers: rated.filter(r => r.fungalAcneTrigger).length
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
    license: 'Ratings are general guidance, not medical advice. Attribution to acnesafecheck.com appreciated.',
    docs: 'https://acnesafecheck.com/api.html'
  });
};
