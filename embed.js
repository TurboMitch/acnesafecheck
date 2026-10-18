/* AcneSafeCheck embeddable ingredient checker — https://acnesafecheck.com/embed.html
   Usage: <div id="acnesafecheck"></div><script src="https://acnesafecheck.com/embed.js" async></script>
   Runs against the public API (/api/check). No cookies, no tracking of visitors on your site. */
(function () {
  var API = 'https://acnesafecheck.com/api/check';
  var HOME = 'https://acnesafecheck.com/';
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function pill(r) {
    var bg = r >= 3 ? '#fde4df' : (r >= 1 ? '#fbf1d6' : '#e3f4e9');
    var fg = r >= 3 ? '#c44d38' : (r >= 1 ? '#8a6400' : '#1f7a48');
    var t = r >= 3 ? 'Clogging risk · ' + r + '/5' : (r >= 1 ? 'Low risk · ' + r + '/5' : 'Acne safe · 0/5');
    return '<span style="display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:700;background:' + bg + ';color:' + fg + ';white-space:nowrap">' + t + '</span>';
  }
  function mount(el) {
    el.innerHTML =
      '<div style="font:14px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;color:#241f1c;border:1px solid #eadfd8;border-radius:12px;padding:16px;background:#fff;max-width:640px">' +
      '<label style="font-weight:700;display:block;margin-bottom:6px">Check ingredients for pore-clogging risk</label>' +
      '<textarea data-acs="ta" rows="4" placeholder="Paste the ingredient (INCI) list…" style="width:100%;box-sizing:border-box;border:1px solid #d9cfc8;border-radius:8px;padding:8px;font:inherit"></textarea>' +
      '<div style="display:flex;gap:8px;align-items:center;margin-top:8px;flex-wrap:wrap">' +
      '<button data-acs="btn" style="background:#e0654f;color:#fff;border:0;border-radius:8px;padding:9px 14px;font:inherit;font-weight:700;cursor:pointer">Check ingredients</button>' +
      '<span data-acs="st" style="font-size:12px;color:#6f655e"></span></div>' +
      '<div data-acs="out" style="margin-top:12px"></div>' +
      '<p style="margin:12px 0 0;font-size:12px;color:#6f655e">Powered by <a href="' + HOME + '?utm_source=embed&utm_medium=widget" target="_blank" rel="noopener" style="color:#c44d38;font-weight:700">AcneSafeCheck</a> · 559 ingredients rated 0–5 · informational only, not medical advice.</p>' +
      '</div>';
    var ta = el.querySelector('[data-acs=ta]'), btn = el.querySelector('[data-acs=btn]'),
        st = el.querySelector('[data-acs=st]'), out = el.querySelector('[data-acs=out]');
    btn.addEventListener('click', function () {
      var raw = ta.value.trim(); if (!raw) return;
      st.textContent = 'Checking…'; out.innerHTML = '';
      fetch(API + '?ingredients=' + encodeURIComponent(raw.slice(0, 20000)))
        .then(function (r) { return r.json(); })
        .then(function (d) {
          st.textContent = '';
          if (!d || !d.results) { out.innerHTML = '<p>Could not check right now — try again or open <a href="' + HOME + '" target="_blank" rel="noopener">acnesafecheck.com</a>.</p>'; return; }
          var bad = d.summary.poreClogging, fa = d.summary.fungalAcneTriggers;
          var head = bad ? '<strong style="color:#c44d38">' + bad + ' pore-clogging ingredient' + (bad > 1 ? 's' : '') + ' found</strong>' : '<strong style="color:#1f7a48">No high-risk pore-clogging ingredients found</strong>';
          if (fa) head += ' <span style="color:#6f655e">· ' + fa + ' fungal-acne trigger' + (fa > 1 ? 's' : '') + '</span>';
          var rows = d.results.filter(function (x) { return x.result; })
            .sort(function (a, b) { return b.result.rating - a.result.rating; })
            .map(function (x) {
              var r = x.result;
              return '<div style="display:flex;justify-content:space-between;gap:10px;align-items:center;padding:7px 0;border-top:1px solid #f1e9e4">' +
                '<a href="' + esc(r.url) + '?utm_source=embed" target="_blank" rel="noopener" style="color:inherit;text-decoration:none">' + esc(r.name) + (r.fungalAcneTrigger ? ' 🍄' : '') + '</a>' + pill(r.rating) + '</div>';
            }).join('');
          var unknown = d.results.filter(function (x) { return !x.result; }).map(function (x) { return esc(x.input); });
          out.innerHTML = '<p style="margin:0 0 6px">' + head + '</p>' + rows +
            (unknown.length ? '<p style="margin:8px 0 0;font-size:12px;color:#6f655e">Not in database: ' + unknown.join(', ') + '</p>' : '');
        })
        .catch(function () { st.textContent = ''; out.innerHTML = '<p>Could not reach the checker — please try again.</p>'; });
    });
  }
  function init() {
    var nodes = document.querySelectorAll('#acnesafecheck, [data-acnesafecheck]');
    for (var i = 0; i < nodes.length; i++) if (!nodes[i].getAttribute('data-acs-mounted')) { nodes[i].setAttribute('data-acs-mounted', '1'); mount(nodes[i]); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
