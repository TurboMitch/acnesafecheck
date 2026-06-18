/* AcneSafeCheck — comedogenicity engine + database.
   rating: 0 (non-comedogenic) .. 5 (very pore-clogging).
   Ratings are general guidance compiled from widely-cited comedogenicity references. */
const DB = [
  // ---- Oils & butters ----
  {n:"Coconut Oil", r:4, c:"Oil", a:["coconut oil","cocos nucifera oil","cocos nucifera (coconut) oil"]},
  {n:"Coconut Butter", r:4, c:"Butter", a:["coconut butter"]},
  {n:"Coconut Alkanes", r:3, c:"Oil", a:["coconut alkanes"]},
  {n:"Cocoa Butter", r:4, c:"Butter", a:["cocoa butter","theobroma cacao seed butter","theobroma cacao"]},
  {n:"Wheat Germ Oil", r:5, c:"Oil", a:["wheat germ oil","triticum vulgare germ oil"]},
  {n:"Wheat Germ Glyceride", r:3, c:"Oil", a:["wheat germ glyceride"]},
  {n:"Cotton Seed Oil", r:3, c:"Oil", a:["cottonseed oil","cotton seed oil","gossypium oil"]},
  {n:"Soybean Oil", r:3, c:"Oil", a:["soybean oil","glycine soja oil"]},
  {n:"Linseed / Flaxseed Oil", r:4, c:"Oil", a:["linseed oil","flaxseed oil","linum usitatissimum seed oil"]},
  {n:"Corn Oil", r:3, c:"Oil", a:["corn oil","zea mays oil"]},
  {n:"Sesame Oil", r:3, c:"Oil", a:["sesame oil","sesamum indicum seed oil"]},
  {n:"Avocado Oil", r:3, c:"Oil", a:["avocado oil","persea gratissima oil"]},
  {n:"Olive Oil", r:2, c:"Oil", a:["olive oil","olea europaea fruit oil"]},
  {n:"Sweet Almond Oil", r:2, c:"Oil", a:["almond oil","prunus amygdalus dulcis oil","sweet almond oil"]},
  {n:"Peanut Oil", r:2, c:"Oil", a:["peanut oil","arachis hypogaea oil"]},
  {n:"Apricot Kernel Oil", r:2, c:"Oil", a:["apricot kernel oil","prunus armeniaca kernel oil"]},
  {n:"Grapeseed Oil", r:1, c:"Oil", a:["grapeseed oil","grape seed oil","vitis vinifera seed oil"]},
  {n:"Jojoba Oil", r:2, c:"Oil", a:["jojoba oil","simmondsia chinensis seed oil"]},
  {n:"Argan Oil", r:0, c:"Oil", a:["argan oil","argania spinosa kernel oil"]},
  {n:"Hemp Seed Oil", r:0, c:"Oil", a:["hemp seed oil","cannabis sativa seed oil"]},
  {n:"Rosehip Oil", r:1, c:"Oil", a:["rosehip oil","rosa canina fruit oil","rosehip seed oil"]},
  {n:"Sunflower Oil", r:0, c:"Oil", a:["sunflower oil","helianthus annuus seed oil"]},
  {n:"Safflower Oil", r:0, c:"Oil", a:["safflower oil","carthamus tinctorius seed oil"]},
  {n:"Castor Oil", r:1, c:"Oil", a:["castor oil","ricinus communis seed oil"]},
  {n:"Marula Oil", r:1, c:"Oil", a:["marula oil","sclerocarya birrea seed oil"]},
  {n:"Squalane", r:1, c:"Oil", a:["squalane"]},
  {n:"Squalene", r:1, c:"Oil", a:["squalene"]},
  {n:"Shark Liver Oil", r:3, c:"Oil", a:["shark liver oil"]},
  {n:"Mink Oil", r:3, c:"Oil", a:["mink oil"]},
  {n:"Mineral Oil", r:1, c:"Oil", a:["mineral oil","paraffinum liquidum"]},
  {n:"Petrolatum", r:0, c:"Occlusive", a:["petrolatum","petroleum jelly"]},
  {n:"Shea Butter", r:0, c:"Butter", a:["shea butter","butyrospermum parkii butter"]},
  {n:"Mango Butter", r:0, c:"Butter", a:["mango butter","mangifera indica seed butter"]},
  {n:"Tamanu Oil", r:2, c:"Oil", a:["tamanu oil","calophyllum inophyllum seed oil"]},
  {n:"Evening Primrose Oil", r:2, c:"Oil", a:["evening primrose oil","oenothera biennis oil"]},
  {n:"Borage Oil", r:2, c:"Oil", a:["borage oil","borago officinalis seed oil"]},
  {n:"Camellia / Tsubaki Oil", r:1, c:"Oil", a:["camellia oil","camellia japonica seed oil","tsubaki oil"]},
  {n:"Meadowfoam Seed Oil", r:1, c:"Oil", a:["meadowfoam seed oil","limnanthes alba seed oil"]},

  // ---- Esters (common pore-cloggers) ----
  {n:"Isopropyl Myristate", r:5, c:"Ester", a:["isopropyl myristate"]},
  {n:"Isopropyl Palmitate", r:4, c:"Ester", a:["isopropyl palmitate"]},
  {n:"Isopropyl Isostearate", r:5, c:"Ester", a:["isopropyl isostearate"]},
  {n:"Isopropyl Linoleate", r:5, c:"Ester", a:["isopropyl linoleate"]},
  {n:"Myristyl Myristate", r:5, c:"Ester", a:["myristyl myristate"]},
  {n:"Myristyl Lactate", r:4, c:"Ester", a:["myristyl lactate"]},
  {n:"Octyl Palmitate", r:4, c:"Ester", a:["octyl palmitate","ethylhexyl palmitate"]},
  {n:"Octyl Stearate", r:5, c:"Ester", a:["octyl stearate"]},
  {n:"Isocetyl Stearate", r:5, c:"Ester", a:["isocetyl stearate"]},
  {n:"Isostearyl Isostearate", r:4, c:"Ester", a:["isostearyl isostearate"]},
  {n:"Isostearyl Neopentanoate", r:4, c:"Ester", a:["isostearyl neopentanoate"]},
  {n:"Butyl Stearate", r:3, c:"Ester", a:["butyl stearate"]},
  {n:"Decyl Oleate", r:3, c:"Ester", a:["decyl oleate"]},
  {n:"Cetyl Acetate", r:3, c:"Ester", a:["cetyl acetate"]},
  {n:"Glyceryl Stearate SE", r:3, c:"Ester", a:["glyceryl stearate se"]},
  {n:"Glyceryl Stearate", r:1, c:"Ester", a:["glyceryl stearate"]},
  {n:"PPG-2 Myristyl Ether Propionate", r:3, c:"Ester", a:["ppg-2 myristyl ether propionate"]},
  {n:"Caprylic/Capric Triglyceride", r:1, c:"Ester", a:["caprylic/capric triglyceride","caprylic capric triglyceride"]},

  // ---- Fatty acids & alcohols ----
  {n:"Lauric Acid", r:4, c:"Fatty acid", a:["lauric acid"]},
  {n:"Myristic Acid", r:3, c:"Fatty acid", a:["myristic acid"]},
  {n:"Palmitic Acid", r:2, c:"Fatty acid", a:["palmitic acid"]},
  {n:"Stearic Acid", r:2, c:"Fatty acid", a:["stearic acid"]},
  {n:"Oleic Acid", r:2, c:"Fatty acid", a:["oleic acid"]},
  {n:"Hexadecyl Alcohol", r:5, c:"Fatty alcohol", a:["hexadecyl alcohol"]},
  {n:"Cetyl Alcohol", r:2, c:"Fatty alcohol", a:["cetyl alcohol"]},
  {n:"Cetearyl Alcohol", r:2, c:"Fatty alcohol", a:["cetearyl alcohol"]},
  {n:"Stearyl Alcohol", r:2, c:"Fatty alcohol", a:["stearyl alcohol"]},

  // ---- Emulsifiers / surfactants ----
  {n:"Laureth-4", r:5, c:"Emulsifier", a:["laureth-4","laureth 4"]},
  {n:"Laureth-23", r:3, c:"Emulsifier", a:["laureth-23"]},
  {n:"Sodium Lauryl Sulfate", r:5, c:"Surfactant", a:["sodium lauryl sulfate","sls"]},
  {n:"Sodium Laureth Sulfate", r:3, c:"Surfactant", a:["sodium laureth sulfate","sles"]},
  {n:"PEG-16 Lanolin", r:4, c:"Emulsifier", a:["peg-16 lanolin","peg 16 lanolin"]},
  {n:"PEG-8 Stearate", r:3, c:"Emulsifier", a:["peg-8 stearate","peg 8 stearate"]},
  {n:"PEG-100 Stearate", r:1, c:"Emulsifier", a:["peg-100 stearate"]},
  {n:"Steareth-10", r:4, c:"Emulsifier", a:["steareth-10"]},
  {n:"Steareth-20", r:2, c:"Emulsifier", a:["steareth-20"]},
  {n:"Sorbitan Oleate", r:3, c:"Emulsifier", a:["sorbitan oleate"]},
  {n:"Sorbitan Sesquioleate", r:3, c:"Emulsifier", a:["sorbitan sesquioleate"]},
  {n:"Polyglyceryl-3 Diisostearate", r:4, c:"Emulsifier", a:["polyglyceryl-3 diisostearate"]},
  {n:"Lecithin", r:4, c:"Emulsifier", a:["lecithin"]},
  {n:"Polysorbate 80", r:1, c:"Emulsifier", a:["polysorbate 80"]},
  {n:"Polysorbate 20", r:0, c:"Emulsifier", a:["polysorbate 20"]},

  // ---- Algae / thickeners ----
  {n:"Algae Extract", r:5, c:"Marine", a:["algae extract","algae"]},
  {n:"Red Algae", r:5, c:"Marine", a:["red algae"]},
  {n:"Carrageenan", r:5, c:"Thickener", a:["carrageenan","chondrus crispus"]},
  {n:"Algin", r:4, c:"Thickener", a:["algin"]},
  {n:"Laminaria Digitata Extract", r:4, c:"Marine", a:["laminaria digitata extract"]},
  {n:"Xanthan Gum", r:0, c:"Thickener", a:["xanthan gum"]},
  {n:"Carbomer", r:0, c:"Thickener", a:["carbomer"]},

  // ---- Dyes (D&C reds) ----
  {n:"D&C Red 6", r:3, c:"Colorant", a:["d&c red 6","red 6","ci 15850"]},
  {n:"D&C Red 7", r:3, c:"Colorant", a:["d&c red 7","red 7"]},
  {n:"D&C Red 9", r:3, c:"Colorant", a:["d&c red 9","red 9"]},
  {n:"D&C Red 17", r:3, c:"Colorant", a:["d&c red 17","red 17"]},
  {n:"D&C Red 21", r:3, c:"Colorant", a:["d&c red 21","red 21"]},
  {n:"D&C Red 27", r:2, c:"Colorant", a:["d&c red 27","red 27"]},
  {n:"D&C Red 30", r:3, c:"Colorant", a:["d&c red 30","red 30"]},
  {n:"D&C Red 33", r:2, c:"Colorant", a:["d&c red 33","red 33"]},
  {n:"D&C Red 36", r:3, c:"Colorant", a:["d&c red 36","red 36"]},

  // ---- Silicones ----
  {n:"Dimethicone", r:1, c:"Silicone", a:["dimethicone"]},
  {n:"Cyclopentasiloxane", r:0, c:"Silicone", a:["cyclopentasiloxane"]},
  {n:"Cyclomethicone", r:0, c:"Silicone", a:["cyclomethicone"]},

  // ---- Humectants / hydrators ----
  {n:"Glycerin", r:0, c:"Humectant", a:["glycerin","glycerine","glycerol"]},
  {n:"Hyaluronic Acid", r:0, c:"Humectant", a:["hyaluronic acid","sodium hyaluronate"]},
  {n:"Propylene Glycol", r:0, c:"Humectant", a:["propylene glycol"]},
  {n:"Butylene Glycol", r:0, c:"Humectant", a:["butylene glycol"]},
  {n:"Panthenol", r:0, c:"Soothing", a:["panthenol","provitamin b5"]},
  {n:"Allantoin", r:0, c:"Soothing", a:["allantoin"]},
  {n:"Sodium PCA", r:0, c:"Humectant", a:["sodium pca"]},
  {n:"Urea", r:0, c:"Humectant", a:["urea"]},

  // ---- Actives ----
  {n:"Niacinamide", r:0, c:"Active", a:["niacinamide","vitamin b3","nicotinamide"]},
  {n:"Salicylic Acid", r:0, c:"Active", a:["salicylic acid","bha"]},
  {n:"Glycolic Acid", r:0, c:"Active", a:["glycolic acid"]},
  {n:"Lactic Acid", r:0, c:"Active", a:["lactic acid"]},
  {n:"Azelaic Acid", r:0, c:"Active", a:["azelaic acid"]},
  {n:"Retinol", r:1, c:"Active", a:["retinol"]},
  {n:"Ascorbic Acid", r:0, c:"Active", a:["ascorbic acid","vitamin c"]},
  {n:"Tocopherol", r:2, c:"Active", a:["tocopherol","tocopheryl acetate","vitamin e"]},
  {n:"Benzoyl Peroxide", r:0, c:"Active", a:["benzoyl peroxide"]},
  {n:"Zinc Oxide", r:1, c:"Sunscreen", a:["zinc oxide"]},
  {n:"Titanium Dioxide", r:1, c:"Sunscreen", a:["titanium dioxide"]},
  {n:"Avobenzone", r:0, c:"Sunscreen", a:["avobenzone"]},

  // ---- Botanicals & misc ----
  {n:"Aloe Vera", r:0, c:"Botanical", a:["aloe vera","aloe barbadensis leaf juice"]},
  {n:"Green Tea Extract", r:0, c:"Botanical", a:["green tea extract","camellia sinensis leaf extract"]},
  {n:"Centella Asiatica", r:0, c:"Botanical", a:["centella asiatica extract","cica"]},
  {n:"Spearmint Oil", r:3, c:"Essential oil", a:["spearmint oil","mentha viridis leaf oil"]},
  {n:"Peppermint Oil", r:2, c:"Essential oil", a:["peppermint oil","mentha piperita oil"]},
  {n:"Beeswax", r:2, c:"Wax", a:["beeswax","cera alba"]},
  {n:"Lanolin", r:2, c:"Occlusive", a:["lanolin"]},
  {n:"Acetylated Lanolin", r:4, c:"Occlusive", a:["acetylated lanolin"]},
  {n:"Acetylated Lanolin Alcohol", r:4, c:"Occlusive", a:["acetylated lanolin alcohol"]},
  {n:"Sodium Chloride", r:0, c:"Misc", a:["sodium chloride","sea salt"]},
  {n:"Water", r:0, c:"Solvent", a:["water","aqua","eau"]},
  {n:"Talc", r:1, c:"Mineral", a:["talc"]},
  {n:"Kaolin", r:0, c:"Clay", a:["kaolin"]},
  {n:"Bentonite", r:0, c:"Clay", a:["bentonite"]},
  {n:"Colloidal Oatmeal", r:0, c:"Soothing", a:["colloidal oatmeal","avena sativa"]}
];

const lookup = {};
DB.forEach(item => item.a.forEach(al => lookup[al] = item));

function normalize(s){
  return s.toLowerCase()
    .replace(/\([^)]*\)/g,' ')
    .replace(/[^a-z0-9&/\-\s]/g,' ')
    .replace(/\s+/g,' ').trim();
}
function parseList(raw){
  return raw.split(/[,;\n•·]+/).map(x=>x.trim()).filter(Boolean);
}
function match(token){
  const norm = normalize(token);
  if(lookup[norm]) return lookup[norm];
  for(const al in lookup){ if(norm === al) return lookup[al]; }
  for(const al in lookup){ if(al.length>4 && norm.includes(al)) return lookup[al]; }
  return null;
}
function pill(r){
  if(r>=3) return '<span class="pill bad">Clogging risk · '+r+'/5</span>';
  if(r>=1) return '<span class="pill low">Low risk · '+r+'/5</span>';
  return '<span class="pill safe">Acne safe · 0/5</span>';
}
function riskText(r){
  if(r>=4) return 'High likelihood of clogging pores — a common breakout trigger for acne-prone skin.';
  if(r===3) return 'Moderate pore-clogging potential; many acne-prone people avoid this.';
  if(r===2) return 'Mild — usually fine, but sensitive skin may want to patch test.';
  if(r===1) return 'Very low risk of clogging pores.';
  return 'Considered non-comedogenic.';
}
function escapeHtml(s){return s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

function checkIngredients(){
  const ta = document.getElementById('ingredients');
  const res = document.getElementById('results');
  if(!ta || !res) return;
  const raw = ta.value;
  if(!raw.trim()){ res.classList.add('hidden'); return; }
  const tokens = parseList(raw);
  const bad=[], low=[], safe=[], unknown=[];
  const seen = new Set();
  tokens.forEach(t=>{
    const m = match(t);
    if(m){ if(seen.has(m.n)) return; seen.add(m.n);
      if(m.r>=3) bad.push(m); else if(m.r>=1) low.push(m); else safe.push(m);
    } else { const key=normalize(t); if(key && !seen.has(key)){ seen.add(key); unknown.push(t.trim()); } }
  });
  let cls='ok', headline='Looks acne safe', sub='No high-risk pore-clogging ingredients found.';
  if(bad.length){ cls='bad'; headline=bad.length+' pore-clogging ingredient'+(bad.length>1?'s':'')+' found'; sub='These have a comedogenicity rating of 3 or higher.'; }
  else if(low.length){ cls='warn'; headline='Mostly fine — '+low.length+' low-risk ingredient'+(low.length>1?'s':''); sub='Nothing high-risk, but a few mild ones to watch.'; }
  let html = '<div class="score '+cls+'"><div class="big">'+(bad.length||low.length||'✓')+'</div><div><div class="lbl"><strong>'+headline+'</strong></div><div class="muted" style="font-size:13px">'+sub+'</div></div></div>';
  const section = (title, arr) => {
    if(!arr.length) return '';
    let s = '<h3 style="margin:18px 0 4px;font-size:15px">'+title+'</h3>';
    arr.sort((a,b)=>b.r-a.r).forEach(m=>{ s += '<div class="flag"><div><div class="name">'+m.n+'</div><div class="why">'+riskText(m.r)+'</div></div>'+pill(m.r)+'</div>'; });
    return s;
  };
  html += section('🔴 Pore-clogging risk', bad);
  html += section('🟡 Low risk', low);
  html += section('🟢 Acne safe', safe);
  if(unknown.length){
    html += '<h3 style="margin:18px 0 4px;font-size:15px">⚪ Not in database ('+unknown.length+')</h3>';
    html += '<p class="muted" style="font-size:13px">Not on common pore-clogging lists — not necessarily safe or unsafe: '+unknown.map(u=>escapeHtml(u)).join(', ')+'</p>';
  }
  res.innerHTML = html; res.classList.remove('hidden');
  res.scrollIntoView({behavior:'smooth', block:'start'});
}
function clearAll(){const ta=document.getElementById('ingredients');if(ta)ta.value='';const r=document.getElementById('results');if(r)r.classList.add('hidden');}
function loadSample(){
  const ta=document.getElementById('ingredients'); if(!ta) return;
  ta.value="Water, Glycerin, Coconut Oil, Niacinamide, Isopropyl Myristate, Cocoa Butter, Hyaluronic Acid, Squalane, Cetyl Alcohol, Tocopherol, Algae Extract, Fragrance";
  checkIngredients();
}
// Encyclopedia table renderer (used on the ingredient list page)
function renderTable(){
  const tb = document.getElementById('dbtable'); if(!tb) return;
  const rows = DB.slice().sort((a,b)=> b.r-a.r || a.n.localeCompare(b.n));
  tb.innerHTML = rows.map(m=>'<tr data-name="'+m.n.toLowerCase()+'"><td>'+m.n+'</td><td>'+m.c+'</td><td>'+pill(m.r)+'</td></tr>').join('');
  document.getElementById('count').textContent = DB.length;
}
function filterTable(){
  const q = document.getElementById('dbsearch').value.toLowerCase();
  document.querySelectorAll('#dbtable tr').forEach(tr=>{
    tr.style.display = tr.getAttribute('data-name').includes(q) ? '' : 'none';
  });
}
