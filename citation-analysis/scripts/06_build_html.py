"""Step 6: build a self-contained interactive HTML visualisation of the
internal citation graph (D3 force-directed, no server / network needed).

Output: reports/internal_citation_graph.html
"""
import os
import json
import common as C

CATEGORIES = ["robust_marl", "robust_rl", "marl", "rl", "game_theory", "other"]
CAT_COLOR = {
    "robust_marl": "#e6194B",
    "robust_rl":   "#f58231",
    "marl":        "#4363d8",
    "rl":          "#3cb44b",
    "game_theory": "#911eb4",
    "other":       "#9aa0a6",
}
CAT_LABEL = {
    "robust_marl": "Robust MARL",
    "robust_rl":   "Robust RL",
    "marl":        "MARL",
    "rl":          "RL / Deep RL",
    "game_theory": "Game theory",
    "other":       "Other",
}


def build_data():
    stats = C.load_json("internal_stats.json")["per_paper"]
    papers = {int(k): v for k, v in C.load_json("papers.json").items()}
    edges = C.load_json("internal_edges.json")
    nodes = []
    for pid in sorted(papers):
        d = stats[str(pid)]
        title = papers[pid]["canonical_title"]
        nodes.append({
            "id": pid,
            "title": title,
            "cat": C.classify(title),
            "in": d["in"],
            "out": d["out"],
            "cited_by": d["cited_by"],
            "cites": d["cites"],
        })
    links = [{"source": e["src"], "target": e["dst"], "how": e["how"]}
             for e in edges]
    return nodes, links


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Robust MARL — Internal Citation Graph</title>
<script>__D3__</script>
<style>
  :root { --bg:#0f1115; --panel:#171a21; --line:#262b36; --txt:#e8eaed;
          --muted:#9aa0a6; }
  * { box-sizing: border-box; }
  html,body { margin:0; height:100%; background:var(--bg); color:var(--txt);
              font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }
  #app { display:flex; height:100vh; }
  #graph { flex:1; position:relative; }
  svg { width:100%; height:100%; display:block; cursor:grab; }
  svg:active { cursor:grabbing; }
  #side { width:340px; background:var(--panel); border-left:1px solid var(--line);
          padding:16px; overflow-y:auto; }
  h1 { font-size:15px; margin:0 0 4px; }
  .sub { color:var(--muted); font-size:12px; margin-bottom:14px; line-height:1.5; }
  .ctl { margin-bottom:14px; }
  .ctl label { font-size:12px; color:var(--muted); display:block; margin-bottom:5px; }
  input[type=search]{ width:100%; padding:7px 9px; border-radius:7px;
    border:1px solid var(--line); background:#0f1115; color:var(--txt); font-size:13px; }
  .legend-item, .filter-item { display:flex; align-items:center; gap:8px;
    font-size:12.5px; padding:3px 0; cursor:pointer; user-select:none; }
  .legend-item.off { opacity:.35; }
  .dot { width:12px; height:12px; border-radius:50%; flex:none; }
  .row { display:flex; gap:8px; align-items:center; }
  .slider-val { font-size:12px; color:var(--muted); }
  input[type=range]{ width:100%; }
  button { background:#222732; color:var(--txt); border:1px solid var(--line);
    border-radius:7px; padding:6px 10px; font-size:12px; cursor:pointer; }
  button:hover { background:#2b313d; }
  #info { margin-top:6px; font-size:12.5px; line-height:1.55; }
  #info .it { color:var(--muted); }
  #info .pill { display:inline-block; padding:1px 7px; border-radius:10px;
    font-size:11px; color:#fff; margin-left:4px; }
  #info a { color:#8ab4f8; cursor:pointer; text-decoration:none; }
  #info a:hover { text-decoration:underline; }
  .tt { position:absolute; pointer-events:none; background:#000d; color:#fff;
    padding:6px 9px; border-radius:6px; font-size:12px; max-width:280px;
    line-height:1.4; opacity:0; transition:opacity .1s; z-index:5; }
  node, .lnk { }
  .hint { font-size:11px; color:var(--muted); margin-top:10px; line-height:1.5; }
  hr { border:none; border-top:1px solid var(--line); margin:14px 0; }
</style>
</head>
<body>
<div id="app">
  <div id="graph"><div class="tt" id="tt"></div></div>
  <div id="side">
    <h1>Internal Citation Graph</h1>
    <div class="sub" id="meta"></div>

    <div class="ctl">
      <label>Search paper (id or title)</label>
      <input type="search" id="search" placeholder="e.g. 43, state uncertainty"/>
    </div>

    <div class="ctl">
      <label>Filter by category (click to toggle)</label>
      <div id="filters"></div>
    </div>

    <div class="ctl">
      <label>Min in-degree: <span class="slider-val" id="degval">0</span></label>
      <input type="range" id="deg" min="0" max="32" value="0"/>
    </div>

    <div class="ctl row">
      <label style="margin:0;flex:1"><input type="checkbox" id="hideiso"/>
        Hide isolated nodes</label>
      <button id="reset">Reset view</button>
    </div>

    <hr/>
    <div id="info"><div class="it">Click a node to inspect its citations.</div></div>
    <div class="hint">Node size = times cited within the set. Color = topic.
      Drag nodes; scroll to zoom. Click a node to highlight its citation
      neighbourhood; click empty space to clear.</div>
  </div>
</div>
<script>
const NODES = __NODES__;
const LINKS = __LINKS__;
const CATCOLOR = __CATCOLOR__;
const CATLABEL = __CATLABEL__;
const CATS = __CATS__;

const byId = new Map(NODES.map(n => [n.id, n]));
const maxIn = d3.max(NODES, d => d.in) || 1;
const rScale = d3.scaleSqrt().domain([0, maxIn]).range([4, 26]);

const active = new Set(CATS);
let minDeg = 0, hideIso = false, selected = null;

document.getElementById("meta").innerHTML =
  `${NODES.length} papers · ${LINKS.length} directed citations ` +
  `(A → B means A cites B).`;

// ---- legend / filters
const fbox = d3.select("#filters");
CATS.forEach(c => {
  const it = fbox.append("div").attr("class","filter-item")
    .on("click", () => {
      active.has(c) ? active.delete(c) : active.add(c);
      it.classed("off", !active.has(c)); applyFilter();
    });
  it.append("span").attr("class","dot").style("background", CATCOLOR[c]);
  const n = NODES.filter(d => d.cat===c).length;
  it.append("span").text(`${CATLABEL[c]} (${n})`);
});

// ---- svg
const graphEl = document.getElementById("graph");
const svg = d3.select("#graph").append("svg");
const W = () => graphEl.clientWidth, H = () => graphEl.clientHeight;
svg.append("defs").append("marker")
  .attr("id","arrow").attr("viewBox","0 -5 10 10").attr("refX",10)
  .attr("refY",0).attr("markerWidth",6).attr("markerHeight",6)
  .attr("orient","auto").append("path").attr("d","M0,-5L10,0L0,5")
  .attr("fill","#3a4150");
const root = svg.append("g");
const zoom = d3.zoom().scaleExtent([0.15, 6])
  .on("zoom", e => root.attr("transform", e.transform));
svg.call(zoom).on("dblclick.zoom", null);

let linkSel = root.append("g").attr("stroke-opacity",0.55)
  .selectAll("line");
let nodeSel = root.append("g").selectAll("circle");
let labelSel = root.append("g").selectAll("text");

const sim = d3.forceSimulation(NODES)
  .force("link", d3.forceLink(LINKS).id(d=>d.id).distance(70).strength(0.35))
  .force("charge", d3.forceManyBody().strength(-180))
  .force("center", d3.forceCenter())
  .force("collide", d3.forceCollide().radius(d=>rScale(d.in)+3))
  .on("tick", ticked);

function neighborsOf(n){
  const s = new Set([n.id]);
  n.cites.forEach(i=>s.add(i)); n.cited_by.forEach(i=>s.add(i));
  return s;
}

function render(){
  linkSel = linkSel.data(LINKS, d=>d.source.id+"-"+d.target.id)
    .join("line").attr("class","lnk").attr("stroke","#3a4150")
    .attr("stroke-width", d=>d.how==="fuzzy"?1:1.3)
    .attr("stroke-dasharray", d=>d.how==="fuzzy"?"3,3":null)
    .attr("marker-end","url(#arrow)");
  nodeSel = nodeSel.data(NODES, d=>d.id)
    .join("circle").attr("r", d=>rScale(d.in))
    .attr("fill", d=>CATCOLOR[d.cat]).attr("stroke","#0b0d11")
    .attr("stroke-width",1.2).style("cursor","pointer")
    .on("mouseover", hover).on("mousemove", moveTT)
    .on("mouseout", outTT).on("click", (e,d)=>{ e.stopPropagation(); select(d); })
    .call(d3.drag().on("start",dstart).on("drag",dragged).on("end",dend));
  labelSel = labelSel.data(NODES.filter(d=>d.in>=6), d=>d.id)
    .join("text").text(d=>"#"+d.id).attr("font-size",10)
    .attr("fill","#c8ccd2").attr("text-anchor","middle").attr("dy",-2)
    .style("pointer-events","none");
}
render();
svg.on("click", ()=>select(null));

function ticked(){
  linkSel.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
    .attr("x2",d=>edgeX(d)).attr("y2",d=>edgeY(d));
  nodeSel.attr("cx",d=>d.x).attr("cy",d=>d.y);
  labelSel.attr("x",d=>d.x).attr("y",d=>d.y-rScale(d.in));
}
// shorten link so arrow sits at target circle edge
function edgeX(d){ const a=Math.atan2(d.target.y-d.source.y,d.target.x-d.source.x);
  return d.target.x - Math.cos(a)*(rScale(d.target.in)+3); }
function edgeY(d){ const a=Math.atan2(d.target.y-d.source.y,d.target.x-d.source.x);
  return d.target.y - Math.sin(a)*(rScale(d.target.in)+3); }

// ---- filtering
function visible(n){
  if(!active.has(n.cat)) return false;
  if(n.in < minDeg) return false;
  if(hideIso && n.in===0 && n.out===0) return false;
  return true;
}
function applyFilter(){
  nodeSel.style("display", d=>visible(d)?null:"none");
  labelSel.style("display", d=>visible(d)?null:"none");
  linkSel.style("display", d=>(visible(d.source)&&visible(d.target))?null:"none");
  if(selected) highlight(selected);
}

// ---- selection / highlight
function select(d){
  selected = d;
  if(!d){ clearHi(); info(null); return; }
  highlight(d); info(d);
}
function highlight(d){
  const nb = neighborsOf(d);
  nodeSel.attr("opacity", n=> visible(n)?(nb.has(n.id)?1:0.12):0);
  labelSel.attr("opacity", n=> nb.has(n.id)?1:0.1);
  linkSel.attr("stroke", l=> (l.source.id===d.id)?"#e6194B"
      : (l.target.id===d.id)?"#3cb44b":"#3a4150")
    .attr("stroke-opacity", l=>(l.source.id===d.id||l.target.id===d.id)?0.95:0.05);
}
function clearHi(){
  nodeSel.attr("opacity", n=>visible(n)?1:0);
  labelSel.attr("opacity",1);
  linkSel.attr("stroke","#3a4150").attr("stroke-opacity",0.55);
}
function info(d){
  const box = document.getElementById("info");
  if(!d){ box.innerHTML='<div class="it">Click a node to inspect its citations.</div>';
    return; }
  const pill = `<span class="pill" style="background:${CATCOLOR[d.cat]}">${CATLABEL[d.cat]}</span>`;
  const lk = ids => ids.length ? ids.map(i=>`<a data-id="${i}">#${i}</a>`).join(", ") : "<span class='it'>none</span>";
  box.innerHTML =
    `<div><b>#${d.id}</b> ${pill}</div>`+
    `<div style="margin:6px 0 8px">${d.title}</div>`+
    `<div class="it">Cited by ${d.in} · cites ${d.out} (within set)</div>`+
    `<div style="margin-top:8px"><b>Cited by</b> (${d.cited_by.length}): ${lk(d.cited_by)}</div>`+
    `<div style="margin-top:6px"><b>Cites</b> (${d.cites.length}): ${lk(d.cites)}</div>`;
  box.querySelectorAll("a[data-id]").forEach(a=>a.onclick=()=>{
    const t=byId.get(+a.dataset.id); focusNode(t); select(t); });
}

// ---- tooltip
const tt = document.getElementById("tt");
function hover(e,d){ tt.style.opacity=1;
  tt.innerHTML=`<b>#${d.id}</b> · ${CATLABEL[d.cat]}<br>${d.title}`
    +`<br><span style="opacity:.7">cited by ${d.in} · cites ${d.out}</span>`;
  moveTT(e); }
function moveTT(e){ const r=graphEl.getBoundingClientRect();
  tt.style.left=(e.clientX-r.left+14)+"px"; tt.style.top=(e.clientY-r.top+14)+"px"; }
function outTT(){ tt.style.opacity=0; }

// ---- drag
function dstart(e,d){ if(!e.active) sim.alphaTarget(0.25).restart();
  d.fx=d.x; d.fy=d.y; }
function dragged(e,d){ d.fx=e.x; d.fy=e.y; }
function dend(e,d){ if(!e.active) sim.alphaTarget(0); d.fx=null; d.fy=null; }

// ---- controls
document.getElementById("deg").oninput = e=>{
  minDeg=+e.target.value; document.getElementById("degval").textContent=minDeg;
  applyFilter(); };
document.getElementById("hideiso").onchange = e=>{ hideIso=e.target.checked; applyFilter(); };
document.getElementById("reset").onclick = ()=>{
  svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity); };
document.getElementById("search").oninput = e=>{
  const q=e.target.value.trim().toLowerCase(); if(!q){ select(null); return; }
  let hit = /^\d+$/.test(q) ? byId.get(+q)
    : NODES.find(n=>n.title.toLowerCase().includes(q));
  if(hit){ focusNode(hit); select(hit); }
};
function focusNode(d){
  const k=1.4, t=d3.zoomIdentity.translate(W()/2,H()/2).scale(k)
    .translate(-d.x,-d.y);
  svg.transition().duration(600).call(zoom.transform, t);
}

// center the simulation in the viewport
sim.force("center", d3.forceCenter(0,0));
root.attr("transform", `translate(${W()/2},${H()/2})`);
svg.call(zoom.transform, d3.zoomIdentity.translate(W()/2,H()/2));
window.addEventListener("resize", ()=> sim.alpha(0.1).restart());
</script>
</body>
</html>
"""


def main():
    nodes, links = build_data()
    d3_path = os.path.join(os.path.dirname(__file__), "d3.min.js")
    with open(d3_path, encoding="utf-8") as f:
        d3_src = f.read()
    html = (HTML
            .replace("__D3__", d3_src)
            .replace("__NODES__", json.dumps(nodes))
            .replace("__LINKS__", json.dumps(links))
            .replace("__CATCOLOR__", json.dumps(CAT_COLOR))
            .replace("__CATLABEL__", json.dumps(CAT_LABEL))
            .replace("__CATS__", json.dumps(CATEGORIES)))
    out = os.path.join(C.REPORTS_DIR, "internal_citation_graph.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    iso = sum(1 for n in nodes if n["in"] == 0 and n["out"] == 0)
    print(f"wrote {out}")
    print(f"  {len(nodes)} nodes, {len(links)} links, {iso} isolated")


if __name__ == "__main__":
    main()
