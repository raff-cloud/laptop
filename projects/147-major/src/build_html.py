import json, re, sys
T = open('/root/.claude/projects/-home-user-laptop/8f9fd665-bf8b-5e11-bfc8-a02fabbfa285/tool-results/artifact-5ee546f1-1792361059-dd97.html').read().split('\n')
head = '\n'.join(T[:115]); js = '\n'.join(T[116:])
M = json.load(open('model.json'))
Q = json.load(open('questions.json'))
# ---------------- header / html
head = head.replace('<title>149 Gledhill Clash Model</title>', '<title>147 Major Clash Model</title>')
head = re.sub(r'<div class="eyebrow">.*?</div>', '<div class="eyebrow">147 Major St · BIM coordination · Rev. Oct 22, 2026</div>', head, count=1)
head = re.sub(r'<h1>.*?</h1>', '<h1>147 Major — HVAC vs. Build</h1>', head, count=1)
head = re.sub(r'<div class="sub">.*?</div>', '<div class="sub">Two systems: F-1 (basement) feeds the basement and main floor from below; F-2 (2nd-floor mech room) feeds the 2nd and 3rd floors from the 3rd-floor joist space. Walls from the stamped permit vectors (A6–A9, 13.5 pt/ft), windows from A10–A12, ceilings from section A-A, ducts from HVAC Designs LO# 113963 at real size, finishes from the Oct 12 material list.</div>', head, count=1)
head = head.replace('<button id="lv-x" data-l="X" aria-pressed="false">Exterior</button><button id="lv-b" data-l="B" aria-pressed="false">Basement</button><button id="lv-g" data-l="G" aria-pressed="true">Main</button><button id="lv-s" data-l="S" aria-pressed="false">Second</button><button id="lv-a" data-l="A" aria-pressed="false">All</button>',
  '<button id="lv-x" data-l="X" aria-pressed="false">Exterior</button><button id="lv-b" data-l="B" aria-pressed="false">Basement</button><button id="lv-g" data-l="G" aria-pressed="false">Main</button><button id="lv-s" data-l="S" aria-pressed="true">Second</button><button id="lv-t" data-l="T" aria-pressed="false">Third</button><button id="lv-a" data-l="A" aria-pressed="false">All</button>')
head = head.replace('aria-label="3D coordination model of 149 Gledhill"', 'aria-label="3D coordination model of 147 Major Street"')
head = head.replace('<div class="k">PROJECT</div><div>149 Gledhill Ave, Toronto</div><div class="k">SOURCES</div><div>Permit A5–A9 · GTA M1–M5 · Cab Oct 7</div>',
  '<div class="k">PROJECT</div><div>147 Major St, Toronto · Ashish &amp; Shivani</div><div class="k">PERMITS</div><div>26 167838 BLD 00 · HVA 00</div><div class="k">SOURCES</div><div>Permit A6–A12 · HVAC LO# 113963 · Mat. list Oct 12</div>')
head = re.sub(r'<div class="note" id="note">.*?</div>', '<div class="note" id="note">Accuracy: walls ±½" (vector, 13.5 pt/ft, checked against 16\'-8", 28\'-11", 60\'-3½"). HVAC sheets registered to the permit plans by translation, same scale. Joists at drawn spacing; in-bay branches can shift and are not flagged. Cabinets follow permit A7 until the 9/8 cabinet set geometry is loaded.</div>', head, count=1)
head = head.replace('.tag.b{background:#6b4ea0;color:#fff}', '.tag.b{background:#6b4ea0;color:#fff}\n.dl{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.dl span{font:500 11px var(--f-mono);border:1px solid var(--rule);padding:2px 6px;color:var(--muted)}')
head = head.replace('<div class="tally">', '<div class="tally">', 1)
# ---------------- JS patches
start = js.index('const DUCTFIX = {'); end = js.index('const CL=groupClashes();')
blocks = 'const DUCTFIX = ' + json.dumps(Q['fix'], ensure_ascii=False) + ';\n'
blocks += 'const ALIAS=' + json.dumps(Q['alias']) + ';\n'
blocks += js[js.index('function groupClashes(){'):js.index('const OPEN=[')]
blocks += 'const QS=' + json.dumps(Q['questions'], ensure_ascii=False) + ';\n'
blocks += "const OPEN=QS.filter(q=>q.status==='open').map(q=>[q.owner,q.title,q.detail]);\nconst SITE=QS.filter(q=>q.status==='site').map(q=>[q.date,q.title,q.answer]);\nconst RESOLVED=QS.filter(q=>q.status==='resolved').map(q=>[q.date,q.title,q.answer]);\n"
js = js[:start] + blocks + js[end:]
js = js.replace("const L = M.levels;", "const L = M.levels; L.CEIL1=L.CEIL1; ")
# materials
js = js.replace(" whitedove:{map:'shaker',c:'#EFECE3',r:.55},", " whitedove:{map:'shaker',c:'#EFECE3',r:.55}, walnut:{map:'walnut',r:.5}, whitegloss:{map:'fluted',c:'#FBFBF8',r:.12},")
js = js.replace(" drywall:[cnv(128,128,", """ walnut:[cnv(512,512,(g,w,h)=>{g.fillStyle='#6B4A33';g.fillRect(0,0,w,h);g.globalAlpha=.22;for(let k=0;k<60;k++){g.strokeStyle=k%3?'#3E2817':'#9C7253';g.lineWidth=1+Math.random()*2;g.beginPath();let y=Math.random()*h;g.moveTo(0,y);for(let x=0;x<=w;x+=32){y+=(Math.random()-.5)*6;g.lineTo(x,y)}g.stroke()}g.globalAlpha=1;g.fillStyle='rgba(0,0,0,.25)';g.fillRect(0,h/2-1,w,2)}),2.5,2.5],
 fluted:[cnv(256,256,(g,w,h)=>{g.fillStyle='#fff';g.fillRect(0,0,w,h);for(let i=0;i<16;i++){const gr=g.createLinearGradient(i*16,0,i*16+16,0);gr.addColorStop(0,'rgba(0,0,0,.10)');gr.addColorStop(.5,'rgba(255,255,255,0)');gr.addColorStop(1,'rgba(0,0,0,.06)');g.fillStyle=gr;g.fillRect(i*16,0,16,h)}}),1,1],
 drywall:[cnv(128,128,""")
js = js.replace("whitedove:[2.4,2.5],", "whitedove:[2.4,2.5],walnut:[2.5,2.5],whitegloss:[1,1],")
# levels / cut planes
js = js.replace("const CUT={X:999,A:L.CEIL1+0.05,B:L.J0T+0.02,G:L.J1T+0.02,S:L.CEIL1+0.05};", "const CUT={X:999,A:L.TOP+0.05,B:L.J0T+0.02,G:L.J1T+0.02,S:L.J2T+0.02,T:L.TOP+0.05};")
js = js.replace("const LVLOK={X:null,A:['B','G','S','X'],B:['B','X'],G:['B','G','X'],S:['B','G','S','X']};", "")
js = js.replace("let level='G';", "let level='S';")
js = js.replace("function levelOf(ids){let best='B';ids.forEach(id=>{const e=byId[id];if(!e)return;if(e.lvl==='S')best='S';else if(e.lvl==='G'&&best!=='S')best='G'});return best}",
  "const RANK={B:0,G:1,S:2,T:3};function levelOf(ids){let best='B';ids.forEach(id=>{const e=byId[id];if(!e)return;if((RANK[e.lvl]??0)>RANK[best])best=e.lvl});return best}")
js = js.replace("const lv=levelOf([c.a]); if(level==='X'||(lv==='S'&&level!=='S'&&level!=='A')||(lv==='G'&&level==='B')){level=lv;applyLevel()}",
  "const lv=levelOf([c.a]); if(level==='X'||(level!=='A'&&RANK[lv]!==RANK[level])){level=lv;applyLevel()}")
# trace (generic, no gap special-cases)
s = js.index('function selectTrace(r){'); e = js.index('function selectBulk(){')
js = js[:s] + """function selectTrace(r){sel={type:'t',r};ghostAll(true);clearTags();const box=new THREE.Box3();
  r.path.forEach(id=>{const m=hi(id,r.sys==='supply'?0xd8412f:0x2f67cf);if(m)box.expandByObject(m)});
  const t=hi(r.id,r.ok?0x2fbf6a:0xff1a1a);if(t){box.expandByObject(t);tag(r.id,r.ok?'connected':'NOT CONNECTED')}
  const lv=levelOf([r.id].concat(r.path)); if(level==='X'||(level!=='A'&&RANK[lv]!==RANK[level])){level=lv;applyLevel()}
  if(!box.isEmpty())flyBox(box,1.7);
  const src=r.path[0]&&r.path[0].startsWith('D2')||r.path[0]==='R2-XD'?'F-2':'F-1';
  focusTxt(r.ok?`${r.name}: connected`:`${r.name}: not connected`, r.ok?`<div>${r.path.length} segments from ${src} to this outlet.</div>`:`<div>${r.why||'Gap in the drawn route.'}</div>`)}
""" + js[e:]
# bulkheads
s = js.index('function selectBulk(){'); e = js.index('function reselect(){')
js = js[:s] + """function selectBulk(){sel={type:'b'};ghostAll(false);clearTags();level='S';applyLevel();Object.values(meshes).forEach(m=>{const c=m.userData.e.cat;if(c==='joist'||c==='beam'||(c==='duct'&&m.userData.e.lvl==='S'))m.visible=false});const box=new THREE.Box3();
  M.elements.filter(e=>e.cat==='bulkhead').forEach(e=>{const m=meshes[e.id];m.visible=true;m.userData.orig=m.material;m.material=BULKMAT;box.expandByObject(m);
    const w=Math.round(Math.min(e.x1-e.x0,e.y1-e.y0)*12),Ln=Math.max(e.x1-e.x0,e.y1-e.y0),cl=e.clear;if(Ln>3)tag(e.id,`${e.name.replace('Proposed bulkhead - ','')}: ${w}" · ${Ln.toFixed(1)} ft · ${Math.floor(cl)}'-${Math.round((cl%1)*12)}" clear`)});
  fly={t0:performance.now(),p0:C.position.clone(),c0:CTL.target.clone(),p1:new THREE.Vector3(8.3,92,30.6),c1:new THREE.Vector3(8.3,20,30)};
  focusTxt('2nd-floor ceiling bulkheads if F-2 is built as drawn','<div>Trunks A, B, C and returns Y, Z run front-to-back across side-to-side 3rd-floor joists (and B sits on the LVL1 cantilever beam). Boxed below the joists they leave about 8\\'-1" to 8\\'-3" clear under a 9\\'-0" ceiling. Shown in orange.</div>')}
""" + js[e:]
# list text
js = js.replace("sm.innerHTML=`<b>Review status, Oct 18</b><div>${RESOLVED.length} resolved · ${SITE.length} to verify on site · ${OPEN.length} open with owners. Detailed clash cards below.</div>`",
  "sm.innerHTML=`<b>Review status, Oct 22</b><div>${RESOLVED.length} resolved · ${SITE.length} to verify on site · ${OPEN.length} open with owners. Questions go one at a time in chat; answers land here.</div><div class=\"dl\"><span>147-Major-clash-markup.pdf</span><span>147-Major-model.ifc</span><span>sent in chat</span></div>`")
js = js.replace("list.appendChild(card('info','Basement bulkhead (decision Oct 16): show me','4 sections · 25–43\" wide · 8\\'-2\" clear','One bulkhead along the west wall; short cross-bulkhead in the games room.',sel&&sel.type==='b',()=>{selectBulk();renderList()}));",
  "list.appendChild(card('info','2nd-floor ceiling bulkheads as drawn: show me',`${M.elements.filter(e=>e.cat==='bulkhead').length} runs · 12–22\" wide · ~8\\'-1\" to 8\\'-3\" clear`,'Trunks A, B, C and returns Y, Z cross the 3rd-floor joists.',sel&&sel.type==='b',()=>{selectBulk();renderList()}));")
js = js.replace("h.textContent=`Risers sticking out past 4\" furring (${p.length})`", "h.textContent=`Stacks too deep for their 2x4 wall (${p.length})`")
js = js.replace("p.forEach(x=>list.appendChild(card('info',`${byId[x.id].name.split(' - ')[0]} sticks out ${x.inches}\"`,'exterior wall furring',`Use a 3-1/4×10 wall stack, fur 2x6 locally, or box it out.`",
  "p.forEach(x=>list.appendChild(card('info',`${byId[x.id].name.split(' (')[0]} sticks out ${x.inches}\"`,`${x.wall}\" wall`,`Round stack is deeper than the stud cavity. Use a 3-1/4×10 / 3-1/4×14 wall stack, build the wall 2x6, or box it out.`")
js = js.replace("rz.textContent=`Resolved with Raff (${RESOLVED.length})`", "rz.textContent=`Resolved with Raff (${RESOLVED.length})`")
js = js.replace("bh.textContent=`Runs hanging below the joists (${M.bulkheads.length})`", "bh.textContent=`Runs crossing joists (${M.bulkheads.length})`")
js = js.replace("`${x.len_ft} ft · underside ${x.under_ft} ft above ${x.lvl==='B'?'slab':'main floor'}`", "`${x.len_ft} ft · ${x.lvl==='B'?'under basement joists, '+x.under_ft+' ft above slab (unfinished)':x.note}`")
js = js.replace("h.textContent=`${s} outlets · ${rs.filter(r=>r.ok).length}/${rs.length} traced to AHU-1`", "h.textContent=`${s} · ${rs.filter(r=>r.ok).length}/${rs.length} traced to F-1 / F-2`")
js = js.replace("['supply','return'].forEach(s=>", "['supply','return','exhaust'].forEach(s=>")
js = js.replace("r.ok?`${r.path.length} segments to AHU-1`:'no path back to AHU-1'", "r.ok?`${r.path.length} segments to ${(r.path[0]||'').startsWith('D2')||r.path[0]==='R2-XD'?'F-2':'F-1'}`:'not connected'")
js = js.replace("n.textContent='Permit = clear wall length measured from the stamped A6/A7 vectors. Cab. set = overall run on the Oct 7 cabinet plan. Boxes = sum of cabinet boxes on the elevations. Red = cabinets longer than the wall, or aisle under 42\". Confirm with Thomas site measure before the order.';list.appendChild(n)}",
  """n.textContent='Permit = measured from the stamped A7/A9 vectors. Cab./spec = 9/8 cabinet set text or the Oct 12 material list model. Red = longer than the opening, or aisle under the minimum. Site measure before the cabinet order.';list.appendChild(n);
   const r=document.createElement('div');r.style.overflowX='auto';r.innerHTML=`<div class="grp">Room sizes: printed vs model</div><table class="dim"><thead><tr><th>Room</th><th>Printed</th><th>Model</th><th>Δ</th></tr></thead><tbody>${M.rooms.map(x=>{const ok=Math.abs(x.d1)<=1&&Math.abs(x.d2)<=1;return `<tr><td>${x.room}</td><td>${x.printed}</td><td>${x.model}</td><td class="${ok?'good':'bad'}">${ok?'ok':(x.d1>0?'+':'')+x.d1+'" / '+(x.d2>0?'+':'')+x.d2+'"'}</td></tr>`}).join('')}</tbody></table>
   <div class="grp">Ceiling heights (section A-A, geodetic levels)</div><table class="dim"><tbody>${M.ceil.map(x=>`<tr><td>${x.level}</td><td>${x.ft}</td></tr>`).join('')}</tbody></table>
   <div class="grp">Windows & glazed doors (elevations A10–A12)</div><table class="dim"><thead><tr><th>Unit</th><th>Width</th><th>Sill</th><th>Head</th></tr></thead><tbody>${M.windows.map(x=>`<tr><td>${x.name}<div class="m">${x.lvl==='B'?'basement':x.lvl==='G'?'main':x.lvl==='S'?'second':'third'}</div></td><td>${x.w}</td><td>${x.sill}</td><td>${x.head}</td></tr>`).join('')}</tbody></table>`;list.appendChild(r)}""")
s = js.index("if(tab==='e'){[["); e = js.index("}\ndocument.querySelectorAll('[data-t]')")
js = js[:s] + "if(tab==='e'){" + json.dumps(Q['equipment'], ensure_ascii=False) + ".forEach(([a,b,k])=>{const d=document.createElement('div');d.className='eq';d.innerHTML=`<span class=\"pill\" style=\"background:var(--${k==='ok'?'ok':k==='soft'?'soft':'hard'})\">${k==='ok'?'OK':k==='soft'?'CHECK':'FIX'}</span><b>${a}</b><div>${b}</div>`;list.appendChild(d)})}\n" + js[e:]
js = js.replace("function viewFor(l){const V={X:[[8,12,30],[-34,26,-26]],A:[[8,12,30],[-38,48,6]],B:[[8,2,30],[-8,52,58]],G:[[8,10,38],[-6,56,60]],S:[[8,20,30],[-8,64,52]]}[l];",
  "function viewFor(l){const V={X:[[8,16,28],[-36,34,-24]],A:[[8,18,28],[-40,58,4]],B:[[8,2,28],[-10,50,62]],G:[[8,10,34],[-8,58,66]],S:[[8,20,30],[-10,70,60]],T:[[8,30,32],[-10,82,62]]}[l];")
js = js.replace("document.getElementById('v-top').onclick=()=>{go(new THREE.Vector3(8.25,0,29),new THREE.Vector3(8.26,95,29.6))};", "document.getElementById('v-top').onclick=()=>{go(new THREE.Vector3(8.3,0,28),new THREE.Vector3(8.31,110,28.6))};")
js = js.replace("C.position.set(-6,56,60); CTL.target.set(8,10,38);", "C.position.set(-10,70,60); CTL.target.set(8,20,30);")
js = js.replace("if(location.hash==='#bulkhead')", "if(location.hash==='#bulkheads')")
js = js.replace("const LAYER={wall:'Walls',", "const LAYER={wall:'Walls',")
# gap / T-18 special removal safety
assert 'T-18' not in js.split('function selectTrace')[1].split('function selectBulk')[0]
M_js = 'const M = ' + json.dumps(M, separators=(',', ':')) + ';'
out = head + '\n' + M_js + '\n' + js
open('147-major-clash-model.html', 'w').write(out)
print(len(out))
