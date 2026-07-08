#!/usr/bin/env python3
"""
Agrega seccion de Notas Timeline con:
- Boton "Agregar nota" con nombre de operador obligatorio
- Auto-deteccion del operador segun turno + dia de semana
- Publicacion con fecha y hora (linea de tiempo)
- Lista de operadores por turno segun schedule proporcionado
"""

SRC = "/home/z/my-project/download/bitacora_noc_con_login.html"
OUT = "/home/z/my-project/download/bitacora_noc_con_login.html"

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# 1. CSS: Timeline notes
# ============================================================
timeline_css = """
/* ===== TIMELINE NOTES ===== */
.timeline-card{background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);margin-bottom:12px;transition:background .3s;overflow:hidden}
.timeline-header{padding:10px 16px;border-bottom:1px solid var(--gray-100);display:flex;align-items:center;justify-content:space-between}
.timeline-header h3{font-size:13px;font-weight:600;color:var(--gray-600);display:flex;align-items:center;gap:6px;margin:0}
.timeline-body{padding:0;max-height:300px;overflow-y:auto}
.timeline-body::-webkit-scrollbar{width:5px}
.timeline-body::-webkit-scrollbar-thumb{background:var(--gray-300);border-radius:3px}
.timeline-add-bar{padding:8px 16px;border-top:1px solid var(--gray-100);display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:var(--gray-50)}
.timeline-add-bar select,.timeline-add-bar input{font-size:12px;padding:6px 10px;border-radius:6px;border:1px solid var(--gray-300);background:var(--white);color:var(--gray-800);outline:none}
.timeline-add-bar select{min-width:160px;max-width:220px}
.timeline-add-bar input[type="text"]{flex:1;min-width:150px}
.timeline-add-bar .btn-tl-add{padding:6px 14px;background:var(--emerald-600);color:#fff;border:none;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;white-space:nowrap;transition:background .15s}
.timeline-add-bar .btn-tl-add:hover{background:var(--emerald-700)}
.timeline-add-bar .btn-tl-add:disabled{background:var(--gray-300);cursor:not-allowed}
.tl-item{padding:10px 16px;border-bottom:1px solid var(--gray-50);display:flex;gap:12px;align-items:flex-start;transition:background .1s;position:relative}
.tl-item:hover{background:var(--gray-50)}
.tl-item:last-child{border-bottom:none}
.tl-dot-col{display:flex;flex-direction:column;align-items:center;padding-top:4px;flex-shrink:0}
.tl-dot{width:10px;height:10px;border-radius:50%;border:2px solid var(--emerald-600);background:var(--white);flex-shrink:0}
.tl-dot.shift-manana{border-color:#1d4ed8;background:#dbeafe}
.tl-dot.shift-tarde{border-color:#d97706;background:#fef3c7}
.tl-dot.shift-noche{border-color:#7c3aed;background:#ede9fe}
.tl-dot.shift-admin{border-color:#059669;background:#d1fae5}
.tl-line{width:2px;flex:1;min-height:20px;background:var(--gray-200);margin-top:4px}
.tl-content{flex:1;min-width:0}
.tl-meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:3px}
.tl-operator{font-size:13px;font-weight:700;color:var(--gray-800)}
.tl-time{font-size:10px;color:var(--gray-400);font-family:'SF Mono',Monaco,Consolas,monospace}
.tl-shift-tag{font-size:9px;padding:1px 6px;border-radius:99px;font-weight:600}
.tl-shift-tag.manana{background:#dbeafe;color:#1d4ed8}
.tl-shift-tag.tarde{background:#fef3c7;color:#92400e}
.tl-shift-tag.noche{background:#ede9fe;color:#5b21b6}
.tl-shift-tag.admin{background:#d1fae5;color:#065f46}
.tl-text{font-size:13px;color:var(--gray-700);line-height:1.5;word-break:break-word}
.tl-del{position:absolute;top:8px;right:8px;opacity:0;transition:opacity .15s}
.tl-item:hover .tl-del{opacity:1}
.tl-empty{text-align:center;padding:24px 16px;color:var(--gray-400);font-size:13px}
@media(max-width:640px){.timeline-add-bar{flex-direction:column;align-items:stretch}.timeline-add-bar select{max-width:none}}
"""

# Insert before </style>
content = content.replace("</style>", timeline_css + "\n</style>", 1)

# ============================================================
# 2. HTML: Timeline section after notes-card </div>
# ============================================================
timeline_html = """
  <div class="timeline-card">
    <div class="timeline-header">
      <h3>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        Notas del Turno
      </h3>
      <span style="font-size:11px;color:var(--gray-400)" id="tlCount"></span>
    </div>
    <div class="timeline-body" id="timelineBody">
      <div class="tl-empty" id="tlEmpty">Sin notas para este dia</div>
    </div>
    <div class="timeline-add-bar">
      <select id="tlOperator" title="Operador (obligatorio)">
        <option value="">-- Operador --</option>
      </select>
      <input type="text" id="tlText" placeholder="Escribir nota..." maxlength="500">
      <button class="btn-tl-add" id="tlAddBtn" onclick="addTimelineNote()">Agregar nota</button>
    </div>
  </div>
"""

# Insert after the notes-card closing div (before <div class="stats">)
content = content.replace(
    '  </div>\n\n  <div class="stats">',
    '  </div>\n' + timeline_html + '\n  <div class="stats">',
    1
)

# ============================================================
# 3. JS: Schedule + Timeline logic
# ============================================================
timeline_js = r"""
// ===== OPERATOR SCHEDULE =====
const SCHEDULE={
  MANANA:{
    weekday:'Sebastian Torrez',
    weekend:'Daniel Di Pino',
    backups:['Omar Baldomir','Anibal Rivero']
  },
  TARDE:{
    weekday:'Fulgencio Godoy',
    weekend:'Humberto Nu\u00f1ez',
    backups:['Anibal Rivero','Sebastian Torrez','Omar Baldomir']
  },
  NOCHE:{
    weekday:'Hugo Magari\u00f1os',
    friday:'Anibal Rivero / Sebastian Torrez',
    weekend:'Gustavo Castellani',
    backups:['Sebastian Torrez','Anibal Rivero']
  }
};
const SHIFT_MAP={OPERAMANANA:'MANANA',OPERATARDE:'TARDE',OPERANOCHE:'NOCHE',OPERAADMIN:'ADMIN'};
const SHIFT_LABELS={MANANA:'Ma\u00f1ana',TARDE:'Tarde',NOCHE:'Noche',ADMIN:'Admin'};
const SHIFT_CSS={MANANA:'manana',TARDE:'tarde',NOCHE:'noche',ADMIN:'admin'};

function getCurrentOperator(){
  if(!currentUser)return null;
  const sk=SHIFT_MAP[currentUser.username];
  if(!sk||sk==='ADMIN')return null;
  const now=new Date();
  const dow=now.getDay(); // 0=Dom
  const isWeekend=(dow===0||dow===6);
  const isFriday=(dow===5);
  const sch=SCHEDULE[sk];
  if(sk==='NOCHE'){
    if(isFriday)return sch.friday;
    if(isWeekend)return sch.weekend;
    return sch.weekday;
  }
  if(isWeekend)return sch.weekend;
  return sch.weekday;
}

function populateOperatorSelect(){
  const sel=document.getElementById('tlOperator');
  if(!sel)return;
  sel.innerHTML='<option value="">-- Operador --</option>';
  if(!currentUser)return;
  const sk=SHIFT_MAP[currentUser.username]||'ADMIN';
  const names=new Set();
  // Add current operator (auto-detected)
  const auto=getCurrentOperator();
  if(auto){
    names.add(auto);
    // Add the schedule entry's operators
  }
  // Add all operators from the user's shift
  if(sk!=='ADMIN'&&SCHEDULE[sk]){
    const sch=SCHEDULE[sk];
    names.add(sch.weekday);
    names.add(sch.weekend);
    if(sch.friday)names.add(sch.friday);
    (sch.backups||[]).forEach(b=>names.add(b));
  }
  // If admin, add all operators from all shifts
  if(sk==='ADMIN'){
    Object.values(SCHEDULE).forEach(sch=>{
      names.add(sch.weekday);
      names.add(sch.weekend);
      if(sch.friday)names.add(sch.friday);
      (sch.backups||[]).forEach(b=>names.add(b));
    });
  }
  // Build options with optgroup
  let html='';
  if(auto)html+='<option value="'+escHtml(auto)+'" selected>'+escHtml(auto)+' *</option>';
  const others=[...names].filter(n=>n!==auto).sort();
  if(others.length){
    html+='<option value="" disabled>──────────</option>';
    others.forEach(n=>html+='<option value="'+escHtml(n)+'">'+escHtml(n)+'</option>');
  }
  sel.innerHTML=html;
}

function escHtml(s){if(!s)return'';return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

// ===== TIMELINE NOTES =====
function addTimelineNote(){
  const opSel=document.getElementById('tlOperator');
  const txtIn=document.getElementById('tlText');
  const op=opSel.value.trim();
  const txt=txtIn.value.trim();
  if(!op){toast('Seleccionar operador (campo obligatorio)');opSel.focus();return;}
  if(!txt){toast('Escribir una nota');txtIn.focus();return;}
  const day=getDay(currentDate);
  if(!day.timeline)day.timeline=[];
  const now=new Date();
  const ts=String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0')+':'+String(now.getSeconds()).padStart(2,'0');
  day.timeline.push({
    id:uid(),
    operator:op,
    text:txt,
    time:ts,
    date:currentDate,
    shift:SHIFT_MAP[currentUser.username]||'ADMIN'
  });
  saveStore();
  txtIn.value='';
  renderTimeline(day);
  toast('Nota agregada');
}
function deleteTimelineNote(id){
  if(!confirm('Eliminar esta nota?'))return;
  const day=getDay(currentDate);
  if(day.timeline)day.timeline=day.timeline.filter(n=>n.id!==id);
  saveStore();renderTimeline(day);toast('Nota eliminada');
}
function renderTimeline(day){
  const body=document.getElementById('timelineBody');
  const countEl=document.getElementById('tlCount');
  const notes=(day.timeline||[]);
  countEl.textContent=notes.length?'('+notes.length+')':'';
  if(!notes.length){
    body.innerHTML='<div class="tl-empty">Sin notas para este dia</div>';
    return;
  }
  // Show newest first
  const sorted=[...notes].reverse();
  let h='';
  sorted.forEach((n,i)=>{
    const isLast=(i===sorted.length-1);
    const sk=n.shift||'ADMIN';
    const css=SHIFT_CSS[sk]||'admin';
    const lbl=SHIFT_LABELS[sk]||sk;
    h+='<div class="tl-item">';
    h+='<div class="tl-dot-col"><div class="tl-dot shift-'+css+'"></div>';
    if(!isLast)h+='<div class="tl-line"></div>';
    h+='</div>';
    h+='<div class="tl-content">';
    h+='<div class="tl-meta">';
    h+='<span class="tl-operator">'+escHtml(n.operator)+'</span>';
    h+='<span class="tl-shift-tag '+css+'">'+lbl+'</span>';
    h+='<span class="tl-time">'+escHtml(n.date)+' '+escHtml(n.time)+'</span>';
    h+='</div>';
    h+='<div class="tl-text">'+escHtml(n.text)+'</div>';
    h+='</div>';
    h+='<button class="btn-icon danger tl-del" title="Eliminar" onclick="deleteTimelineNote(\''+n.id+'\')"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>';
    h+='</div>';
  });
  body.innerHTML=h;
}

// Enter key on note input
document.getElementById('tlText').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();addTimelineNote();}});

// Populate operator select after login
function refreshOperatorSelect(){populateOperatorSelect();}
// Override doLogin to also populate operator select
const _origDoLogin=doLogin;
doLogin=function(){
  _origDoLogin();
  populateOperatorSelect();
};
const _origCheckSession=checkSession;
checkSession=function(){
  _origCheckSession();
  populateOperatorSelect();
};
// Re-populate on date change - patch render
const _origRender=render;
render=function(){
  _origRender();
  const day=getDay(currentDate);
  renderTimeline(day);
  populateOperatorSelect();
};

"""

# Insert before loadStore();render();
content = content.replace(
    "loadStore();render();\n",
    timeline_js + "loadStore();render();\n",
    1
)

# ============================================================
# 4. Write output
# ============================================================
with open(OUT, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK: {OUT}")
print(f"Size: {len(content)} bytes")

# Verify
checks = [
    "timeline-card",
    "tlOperator",
    "tlText",
    "addTimelineNote",
    "deleteTimelineNote",
    "renderTimeline",
    "SCHEDULE",
    "getCurrentOperator",
    "populateOperatorSelect",
    "Sebastian Torrez",
    "Hugo Magari",
    "Fulgencio Godoy",
    "Daniel Di Pino",
    "Humberto Nu",
    "Gustavo Castellani",
    "Omar Baldomir",
    "Anibal Rivero",
    "SHIFT_MAP",
    "SHIFT_LABELS",
]
for c in checks:
    found = c in content
    print(f"  {'OK' if found else 'FAIL'}: {c}")

# Balanced divs
import re
opens = len(re.findall(r'<div', content))
closes = len(re.findall(r'</div>', content))
print(f"  DIVs: open={opens} close={closes} {'OK' if opens==closes else 'MISMATCH'}")