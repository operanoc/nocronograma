#!/usr/bin/env python3
"""
Agrega:
1. Boton 'Cierre de Turno' en el header con modal de novedades
2. Sistema de notificaciones (campana con badge y panel dropdown)
3. Seccion 'Novedades de Turno' visible para el turno entrante
Los cierres de turno se guardan en localStorage y son visibles para todos.
"""

SRC = "/home/z/my-project/download/bitacora_noc_con_login.html"
OUT = "/home/z/my-project/download/bitacora_noc_con_login.html"

with open(SRC, "r", encoding="utf-8") as f:
    c = f.read()

# ============================================================
# 1. CSS
# ============================================================
css = """
/* ===== CIERRE DE TURNO & NOTIFICACIONES ===== */
.btn-cierre{display:inline-flex;align-items:center;gap:5px;padding:6px 14px;background:var(--amber-600);color:#fff;border-radius:var(--radius);font-size:12px;font-weight:600;cursor:pointer;transition:background .15s;white-space:nowrap}
.btn-cierre:hover{background:var(--amber-800)}
.btn-novedades{display:inline-flex;align-items:center;gap:5px;padding:6px 14px;background:var(--sky-600);color:#fff;border-radius:var(--radius);font-size:12px;font-weight:600;cursor:pointer;transition:background .15s;white-space:nowrap}
.btn-novedades:hover{background:var(--sky-800)}
/* Notification bell */
.notif-wrap{position:relative;display:inline-flex}
.notif-btn{position:relative;cursor:pointer;background:none;border:none;padding:6px;border-radius:6px;color:var(--gray-500);display:flex;align-items:center;transition:background .15s}
.notif-btn:hover{background:var(--gray-100);color:var(--gray-700)}
.notif-badge{position:absolute;top:2px;right:2px;min-width:16px;height:16px;background:var(--red-500);color:#fff;font-size:9px;font-weight:700;border-radius:99px;display:none;align-items:center;justify-content:center;padding:0 4px;line-height:1}
.notif-badge.show{display:flex}
.notif-badge.zero{display:none}
/* Notification dropdown */
.notif-panel{position:absolute;top:100%;right:0;margin-top:4px;width:380px;max-height:420px;background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);box-shadow:var(--shadow-md);z-index:300;display:none;flex-direction:column;overflow:hidden}
.notif-panel.show{display:flex}
.notif-panel-header{padding:10px 14px;border-bottom:1px solid var(--gray-200);display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
.notif-panel-header h4{font-size:13px;font-weight:600;color:var(--gray-800);margin:0}
.notif-panel-header button{font-size:11px;color:var(--sky-600);cursor:pointer;background:none;border:none;font-weight:600}
.notif-list{flex:1;overflow-y:auto}
.notif-list::-webkit-scrollbar{width:5px}
.notif-list::-webkit-scrollbar-thumb{background:var(--gray-300);border-radius:3px}
.notif-item{padding:10px 14px;border-bottom:1px solid var(--gray-50);cursor:pointer;transition:background .1s;display:flex;gap:10px;align-items:flex-start}
.notif-item:hover{background:var(--gray-50)}
.notif-item.unread{background:var(--sky-50)}
html.dark .notif-item.unread{background:#082f49}
.notif-item.unread:hover{background:var(--sky-100)}
.notif-icon-wrap{width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:14px}
.notif-icon-wrap.handover{background:var(--amber-100);color:var(--amber-800)}
.notif-icon-wrap.alert{background:var(--red-100);color:var(--red-800)}
.notif-icon-wrap.info{background:var(--sky-100);color:var(--sky-800)}
.notif-body{flex:1;min-width:0}
.notif-title{font-size:12px;font-weight:600;color:var(--gray-800);margin-bottom:2px}
.notif-desc{font-size:11px;color:var(--gray-500);line-height:1.4;word-break:break-word}
.notif-time{font-size:10px;color:var(--gray-400);margin-top:3px;font-family:'SF Mono',Monaco,Consolas,monospace}
.notif-empty{text-align:center;padding:30px 16px;color:var(--gray-400);font-size:13px}
/* Cierre modal fields */
.cierre-checks{display:flex;flex-direction:column;gap:8px;margin-bottom:12px}
.cierre-check{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--gray-700);cursor:pointer}
.cierre-check input[type="checkbox"]{width:16px;height:16px;accent-color:var(--emerald-600);cursor:pointer}
/* Novedades panel (full section) */
.novedades-section{background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);margin-bottom:12px;overflow:hidden;transition:background .3s}
.novedades-header{padding:10px 16px;border-bottom:1px solid var(--gray-100);display:flex;align-items:center;justify-content:space-between;cursor:pointer;transition:background .1s}
.novedades-header:hover{background:var(--gray-50)}
.novedades-header h3{font-size:13px;font-weight:600;color:var(--gray-600);display:flex;align-items:center;gap:6px;margin:0}
.novedades-header .nv-badge{background:var(--amber-600);color:#fff;font-size:10px;font-weight:700;padding:1px 7px;border-radius:99px}
.novedades-body{max-height:0;overflow:hidden;transition:max-height .3s}
.novedades-body.open{max-height:600px;overflow-y:auto}
.novedades-body::-webkit-scrollbar{width:5px}
.novedades-body::-webkit-scrollbar-thumb{background:var(--gray-300);border-radius:3px}
.nv-card{padding:12px 16px;border-bottom:1px solid var(--gray-50)}
.nv-card:last-child{border-bottom:none}
.nv-card-head{display:flex;align-items:center;gap:8px;margin-bottom:6px;flex-wrap:wrap}
.nv-card-op{font-size:13px;font-weight:700;color:var(--gray-800)}
.nv-card-shift{font-size:10px;padding:1px 7px;border-radius:99px;font-weight:600}
.nv-card-time{font-size:10px;color:var(--gray-400);font-family:'SF Mono',Monaco,Consolas,monospace}
.nv-card-text{font-size:13px;color:var(--gray-700);line-height:1.5;white-space:pre-wrap;word-break:break-word}
.nv-card-checks{margin-top:6px;display:flex;gap:12px;flex-wrap:wrap;font-size:11px;color:var(--gray-500)}
.nv-card-checks span{display:flex;align-items:center;gap:4px}
.nv-card-checks .chk-ok{color:var(--emerald-600)}
.nv-card-checks .chk-fail{color:var(--red-500)}
.nv-empty{text-align:center;padding:20px;color:var(--gray-400);font-size:13px}
@media(max-width:640px){.notif-panel{width:calc(100vw - 32px);right:-60px}.btn-cierre,.btn-novedades{font-size:11px;padding:5px 10px}}
"""

c = c.replace("</style>", css + "\n</style>", 1)

# ============================================================
# 2. HTML: Buttons in header (before dashBtn)
# ============================================================
header_buttons = """
      <button class="btn-cierre" id="cierreBtn" onclick="openCierreModal()" title="Cierre de Turno" style="display:none">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
        Cierre de Turno
      </button>
      <div class="notif-wrap" id="notifWrap" style="display:none">
        <button class="notif-btn" onclick="toggleNotifPanel()" title="Notificaciones">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
          <span class="notif-badge" id="notifBadge">0</span>
        </button>
        <div class="notif-panel" id="notifPanel">
          <div class="notif-panel-header"><h4>Notificaciones</h4><button onclick="markAllRead()">Marcar leidas</button></div>
          <div class="notif-list" id="notifList"></div>
        </div>
      </div>
"""

c = c.replace(
    '      <button class="btn btn-ghost btn-sm" id="dashBtn"',
    header_buttons + '      <button class="btn btn-ghost btn-sm" id="dashBtn"',
    1
)

# ============================================================
# 3. HTML: Novedades section (after timeline-card, before stats)
# ============================================================
novedades_html = """
  <div class="novedades-section" id="novedadesSection" style="display:none">
    <div class="novedades-header" onclick="toggleNovedades()">
      <h3>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>
        Novedades de Turno
        <span class="nv-badge" id="nvBadge" style="display:none">0</span>
      </h3>
      <svg id="nvChevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="transition:transform .2s"><polyline points="6 9 12 15 18 9"/></svg>
    </div>
    <div class="novedades-body" id="novedadesBody"></div>
  </div>

"""

c = c.replace(
    '  <div class="stats">',
    novedades_html + '  <div class="stats">',
    1
)

# ============================================================
# 4. JS: Cierre de Turno + Notificaciones + Novedades
# ============================================================
js = r"""
// ===== CIERRE DE TURNO =====
function openCierreModal(){
  if(!currentUser)return;
  const day=getDay(currentDate);
  const sk=SHIFT_MAP[currentUser.username]||'ADMIN';
  const skLabel=SHIFT_LABELS[sk]||sk;
  const auto=getCurrentOperator()||currentUser.username;
  document.getElementById('modalTitle').textContent='Cierre de Turno - '+skLabel;
  document.getElementById('modalBody').innerHTML=
    '<div class="form-group"><label>Operador</label><select id="cierreOp">'+buildOpOptions(auto)+'</select></div>'+
    '<div class="form-group"><label>Novedades (obligatorio)</label><textarea id="cierreText" rows="4" placeholder="Detalle de novedades del turno, incidencias, tareas pendientes..." style="width:100%;font-size:13px;border:1px solid var(--gray-300);border-radius:6px;padding:8px;resize:vertical;min-height:80px"></textarea></div>'+
    '<div class="cierre-checks">'+
    '<label class="cierre-check"><input type="checkbox" id="cierrePollOk" checked> Pollings completados</label>'+
    '<label class="cierre-check"><input type="checkbox" id="cierreBkpOk" checked> Backups OK</label>'+
    '<label class="cierre-check"><input type="checkbox" id="cierreProcOk" checked> Procesos OK</label>'+
    '</div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="saveCierre()">Confirmar Cierre</button>';
  openModal();
}
function buildOpOptions(selected){
  let names=new Set();
  const sk=SHIFT_MAP[currentUser.username]||'ADMIN';
  if(sk!=='ADMIN'&&SCHEDULE[sk]){
    const sch=SCHEDULE[sk];names.add(sch.weekday);names.add(sch.weekend);
    if(sch.friday)names.add(sch.friday);
    (sch.backups||[]).forEach(b=>names.add(b));
  }
  if(sk==='ADMIN'){Object.values(SCHEDULE).forEach(sch=>{names.add(sch.weekday);names.add(sch.weekend);if(sch.friday)names.add(sch.friday);(sch.backups||[]).forEach(b=>names.add(b));});}
  let h='';[...names].sort().forEach(n=>h+='<option value="'+escHtml(n)+'"'+(n===selected?' selected':'')+'>'+escHtml(n)+'</option>');
  return h;
}
function saveCierre(){
  const text=document.getElementById('cierreText').value.trim();
  if(!text){toast('Escribir novedades (campo obligatorio)');document.getElementById('cierreText').focus();return;}
  const op=document.getElementById('cierreOp').value;
  const sk=SHIFT_MAP[currentUser.username]||'ADMIN';
  const now=new Date();
  const ts=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0')+' '+String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0')+':'+String(now.getSeconds()).padStart(2,'0');
  const day=getDay(currentDate);
  if(!day.handovers)day.handovers=[];
  const entry={
    id:uid(),
    operator:op,
    shift:sk,
    shiftLabel:SHIFT_LABELS[sk]||sk,
    timestamp:ts,
    text:text,
    pollOk:document.getElementById('cierrePollOk').checked,
    bkpOk:document.getElementById('cierreBkpOk').checked,
    procOk:document.getElementById('cierreProcOk').checked,
    readBy:{}
  };
  day.handovers.push(entry);
  // Create notification
  if(!day.notifications)day.notifications=[];
  day.notifications.push({
    id:uid(),
    type:'handover',
    title:'Cierre de Turno - '+entry.shiftLabel,
    desc:op+': '+text.substring(0,80)+(text.length>80?'...':''),
    timestamp:ts,
    shift:sk,
    readBy:{}
  });
  saveStore();closeModal();
  renderNovedades(day);updateNotifBadge(day);renderNotifPanel(day);
  toast('Cierre de turno registrado');
}

// ===== NOVEDADES DE TURNO SECTION =====
function toggleNovedades(){
  const body=document.getElementById('novedadesBody');
  const chev=document.getElementById('nvChevron');
  body.classList.toggle('open');
  chev.style.transform=body.classList.contains('open')?'rotate(180deg)':'';
}
function renderNovedades(day){
  const sec=document.getElementById('novedadesSection');
  const body=document.getElementById('novedadesBody');
  const badge=document.getElementById('nvBadge');
  const hovers=(day.handovers||[]);
  if(!hovers.length){sec.style.display='none';return;}
  sec.style.display='';
  // Count unread
  const mySk=currentUser?SHIFT_MAP[currentUser.username]:'';
  const unread=hovers.filter(h=>h.shift!==mySk&&!(h.readBy&&h.readBy[mySk])).length;
  if(unread>0){badge.style.display='';badge.textContent=unread;}else{badge.style.display='none';}
  let html='';
  const sorted=[...hovers].reverse();
  sorted.forEach(h=>{
    const css=SHIFT_CSS[h.shift]||'admin';
    const chk=(val,label)=>val?'<span class="chk-ok">&#10003; '+label+'</span>':'<span class="chk-fail">&#10007; '+label+'</span>';
    html+='<div class="nv-card">';
    html+='<div class="nv-card-head">';
    html+='<span class="nv-card-op">'+escHtml(h.operator)+'</span>';
    html+='<span class="nv-card-shift '+css+'">'+escHtml(h.shiftLabel||h.shift)+'</span>';
    html+='<span class="nv-card-time">'+escHtml(h.timestamp)+'</span>';
    html+='</div>';
    html+='<div class="nv-card-text">'+escHtml(h.text)+'</div>';
    html+='<div class="nv-card-checks">'+chk(h.pollOk,'Pollings')+chk(h.bkpOk,'Backups')+chk(h.procOk,'Procesos')+'</div>';
    html+='</div>';
  });
  body.innerHTML=html;
}

// ===== NOTIFICATION SYSTEM =====
function toggleNotifPanel(){
  const panel=document.getElementById('notifPanel');
  const isOpen=panel.classList.contains('show');
  if(isOpen){panel.classList.remove('show');}
  else{renderNotifPanel();panel.classList.add('show');}
}
function updateNotifBadge(day){
  const badge=document.getElementById('notifBadge');
  if(!day)day=getDay(currentDate);
  const notifs=day.notifications||[];
  const mySk=currentUser?SHIFT_MAP[currentUser.username]:'';
  const unread=notifs.filter(n=>!(n.readBy&&n.readBy[mySk])&&n.shift!==mySk).length;
  if(unread>0){badge.textContent=unread>9?'9+':unread;badge.classList.add('show');badge.classList.remove('zero');}
  else{badge.classList.add('zero');}
}
function renderNotifPanel(day){
  if(!day)day=getDay(currentDate);
  const list=document.getElementById('notifList');
  const notifs=(day.notifications||[]).reverse();
  const mySk=currentUser?SHIFT_MAP[currentUser.username]:'';
  if(!notifs.length){list.innerHTML='<div class="notif-empty">Sin notificaciones</div>';updateNotifBadge(day);return;}
  let html='';
  notifs.forEach(n=>{
    const isUnread=!(n.readBy&&n.readBy[mySk])&&n.shift!==mySk;
    const iconClass=n.type==='handover'?'handover':n.type==='alert'?'alert':'info';
    const iconSvg=n.type==='handover'?'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>':n.type==='alert'?'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>':'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
    html+='<div class="notif-item'+(isUnread?' unread':'')+'" onclick="readNotif(\''+n.id+'\')">';
    html+='<div class="notif-icon-wrap '+iconClass+'">'+iconSvg+'</div>';
    html+='<div class="notif-body">';
    html+='<div class="notif-title">'+escHtml(n.title)+'</div>';
    html+='<div class="notif-desc">'+escHtml(n.desc)+'</div>';
    html+='<div class="notif-time">'+escHtml(n.timestamp)+'</div>';
    html+='</div></div>';
  });
  list.innerHTML=html;
  updateNotifBadge(day);
}
function readNotif(nid){
  const day=getDay(currentDate);
  const notifs=day.notifications||[];
  const mySk=currentUser?SHIFT_MAP[currentUser.username]:'';
  const n=notifs.find(x=>x.id===nid);
  if(n){if(!n.readBy)n.readBy={};n.readBy[mySk]=true;saveStore();}
  renderNotifPanel(day);renderNovedades(day);
}
function markAllRead(){
  const day=getDay(currentDate);
  const notifs=day.notifications||[];
  const mySk=currentUser?SHIFT_MAP[currentUser.username]:'';
  notifs.forEach(n=>{if(!n.readBy)n.readBy={};n.readBy[mySk]=true;});
  // Also mark handovers
  (day.handovers||[]).forEach(h=>{if(!h.readBy)h.readBy={};h.readBy[mySk]=true;});
  saveStore();renderNotifPanel(day);renderNovedades(day);toast('Notificaciones marcadas como leidas');
}
// Close notif panel on outside click
document.addEventListener('click',e=>{
  const wrap=document.getElementById('notifWrap');
  if(wrap&&!e.target.closest('#notifWrap')){
    document.getElementById('notifPanel').classList.remove('show');
  }
});

// Show/hide cierre+notif buttons on login
function showTurnoButtons(){
  const show=!!currentUser;
  document.getElementById('cierreBtn').style.display=show?'':'none';
  document.getElementById('notifWrap').style.display=show?'':'none';
}
// Patch doLogin and checkSession to show buttons and render novedades
const __origDoLogin=doLogin;
doLogin=function(){
  __origDoLogin();
  showTurnoButtons();
  const day=getDay(currentDate);
  renderNovedades(day);updateNotifBadge(day);
};
const __origCheckSession=checkSession;
checkSession=function(){
  __origCheckSession();
  showTurnoButtons();
  if(currentUser){
    const day=getDay(currentDate);
    renderNovedades(day);updateNotifBadge(day);
  }
};
// Patch render to also render novedades
const __origRender=render;
render=function(){
  __origRender();
  if(currentUser){
    const day=getDay(currentDate);
    renderNovedades(day);updateNotifBadge(day);
  }
};
// Patch doLogout to hide buttons
const __origDoLogout=doLogout;
doLogout=function(){
  __origDoLogout();
  showTurnoButtons();
  document.getElementById('novedadesSection').style.display='none';
  document.getElementById('notifPanel').classList.remove('show');
};
"""

# Replace the old triple-patch block (from previous timeline additions) with the new combined one
# Find and replace the old patch block
old_patch = """const _origDoLogin=doLogin;
doLogin=function(){
  _origDoLogin();
  populateOperatorSelect();
  const day=getDay(currentDate);
  renderTimeline(day);
};
const _origCheckSession=checkSession;
checkSession=function(){
  _origCheckSession();
  populateOperatorSelect();
  if(currentUser){const day=getDay(currentDate);renderTimeline(day);}
};
// Re-populate on date change - patch render
const _origRender=render;
render=function(){
  _origRender();
  const day=getDay(currentDate);
  renderTimeline(day);
  populateOperatorSelect();
};

loadStore();render();"""

new_patch = js + """
const _origDoLogin=doLogin;
doLogin=function(){
  _origDoLogin();
  populateOperatorSelect();
  const day=getDay(currentDate);
  renderTimeline(day);
};
const _origCheckSession=checkSession;
checkSession=function(){
  _origCheckSession();
  populateOperatorSelect();
  if(currentUser){const day=getDay(currentDate);renderTimeline(day);}
};
// Re-populate on date change - patch render
const _origRender=render;
render=function(){
  _origRender();
  const day=getDay(currentDate);
  renderTimeline(day);
  populateOperatorSelect();
};

loadStore();render();"""

c = c.replace(old_patch, new_patch, 1)

# Also patch doLogout to call the new logout wrapper
# The original doLogout doesn't have a wrapper yet, so we need to handle this
# The new js defines __origDoLogout=doLogout and overrides it
# But we also need the original doLogout to be called from the old patches
# Since the js block is inserted BEFORE the old patch block, __origDoLogout captures the original
# Then the old patch block also captures doLogin/checkSession/render again...
# This creates a chain. Let me verify the order is correct.

# Actually, let me re-think. The new `js` block defines wrappers with __orig prefix.
# Then the old patch block defines more wrappers with _orig prefix.
# The old _origDoLogin captures the NEW doLogin (which is the __orig wrapper).
# So the call chain is: old doLogin -> __orig doLogin -> _origDoLogin (actual original from auth JS)
# This should work correctly.

# But wait, the old patch also overrides render and doLogin again!
# The old _origRender captures the NEW render (which calls __origRender + renderNovedades + updateNotifBadge)
# Then the old render calls _origRender (which is the new render with novedades) + renderTimeline + populateOperatorSelect
# So the chain is: final render -> old _origRender -> new __origRender -> original render
# And the final render adds: renderTimeline + populateOperatorSelect
# While __origRender adds: renderNovedades + updateNotifBadge
# This should work!

# Similarly for doLogin:
# final doLogin -> old _origDoLogin -> new __origDoLogin -> original auth doLogin
# old adds: populateOperatorSelect + renderTimeline
# new adds: showTurnoButtons + renderNovedades + updateNotifBadge
# This works!

# For doLogout, the new __origDoLogout captures the original, and overrides it.
# But there's no old patch for doLogout, so it stays as the new override.
# We need to make sure the old code doesn't override it.

with open(OUT, "w", encoding="utf-8") as f:
    f.write(c)

print(f"OK: {OUT}")
print(f"Size: {len(c)} bytes")

checks = [
    "cierreBtn", "openCierreModal", "saveCierre",
    "notifWrap", "notifBadge", "notifPanel", "toggleNotifPanel",
    "markAllRead", "readNotif", "renderNotifPanel",
    "novedadesSection", "novedadesBody", "nvBadge",
    "renderNovedades", "toggleNovedades",
    "showTurnoButtons",
    "Cierre de Turno",
    "Novedades de Turno",
    "handovers",
    "notifications",
    "btn-cierre",
    "notif-panel",
]
import re
for check in checks:
    found = check in c
    print(f"  {'OK' if found else 'FAIL'}: {check}")
opens = len(re.findall(r'<div', c))
closes = len(re.findall(r'</div>', c))
print(f"  DIVs: {opens}/{closes} {'OK' if opens==closes else 'FAIL'}")