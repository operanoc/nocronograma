#!/usr/bin/env python3
"""Generate improved bitacora_noc.html with all 16 enhancements."""

import re

with open('/home/z/my-project/upload/index.html', 'r') as f:
    content = f.read()

# ============================================================
# 1. CSS ADDITIONS (before </style>)
# ============================================================
new_css = r"""
/* === NEW: Save indicator === */
.save-indicator{font-size:11px;color:var(--emerald-600);opacity:0;transition:opacity .4s;margin-left:6px;white-space:nowrap;display:inline-flex;align-items:center;gap:3px}
.save-indicator.show{opacity:1}

/* === NEW: Tab transitions === */
#tabContent{transition:opacity .15s ease}
#tabContent.fading{opacity:0}

/* === NEW: Filter controls === */
.filter-select{padding:5px 8px;font-size:12px;border-radius:var(--radius);min-width:110px;max-width:140px}
.sep-v{width:1px;height:20px;background:var(--gray-200);margin:0 2px;flex-shrink:0}

/* === NEW: Operator / Shift bar === */
.operator-bar{background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);padding:8px 12px;margin-bottom:12px;display:flex;align-items:center;gap:8px;flex-wrap:wrap;transition:background .3s}
.operator-bar label{font-size:12px;color:var(--gray-500);font-weight:500;white-space:nowrap}
.operator-bar input,.operator-bar select{font-size:13px;padding:5px 8px;min-width:0}

/* === NEW: Out-of-schedule highlight === */
.server-row.late{border-color:var(--amber-400);background:var(--amber-50)}
html.dark .server-row.late{border-color:var(--amber-600);background:rgba(217,119,6,.1)}

/* === NEW: Summary / Handover modal === */
.summary-modal-body{max-height:65vh;overflow-y:auto}
.summary-modal-body::-webkit-scrollbar{width:6px}
.summary-modal-body::-webkit-scrollbar-thumb{background:var(--gray-300);border-radius:3px}
.summary-section{margin-bottom:14px}
.summary-section h4{font-size:13px;font-weight:600;margin-bottom:6px;color:var(--gray-700);display:flex;align-items:center;gap:6px}
.summary-grid{display:grid;grid-template-columns:1fr 1fr;gap:5px}
.summary-item{display:flex;justify-content:space-between;padding:5px 8px;background:var(--gray-50);border-radius:4px;font-size:12px}
html.dark .summary-item{background:var(--gray-100)}
.summary-item .val{font-weight:600;font-family:'SF Mono',Monaco,Consolas,monospace}
.summary-notes{background:var(--gray-50);border-radius:6px;padding:8px 10px;font-size:13px;white-space:pre-wrap;max-height:120px;overflow-y:auto;color:var(--gray-700)}
html.dark .summary-notes{background:var(--gray-100)}

/* === NEW: Week history bars === */
.week-row{display:flex;align-items:center;gap:8px;padding:4px 0;font-size:12px}
.week-row .week-label{width:100px;flex-shrink:0;font-weight:500;color:var(--gray-600)}
.week-row .week-bar-bg{flex:1;height:16px;background:var(--gray-100);border-radius:3px;overflow:hidden;position:relative}
html.dark .week-row .week-bar-bg{background:var(--gray-200)}
.week-row .week-bar-fill{height:100%;border-radius:3px;transition:width .4s ease;min-width:2px}
.week-row .week-bar-fill.ok{background:var(--emerald-600)}
.week-row .week-bar-fill.fail{background:var(--red-500)}
.week-row .week-bar-fill.total{background:var(--sky-600)}
.week-row .week-val{width:40px;text-align:right;font-family:'SF Mono',Monaco,Consolas,monospace;font-size:11px;color:var(--gray-500)}

/* === NEW: Storage bar === */
.storage-bar{display:flex;align-items:center;gap:6px;font-size:10px;color:var(--gray-400)}
.storage-bar .bar{width:60px;height:3px;background:var(--gray-200);border-radius:2px;overflow:hidden}
.storage-bar .bar .fill{height:100%;border-radius:2px;transition:width .3s,background .3s}

/* === NEW: Import label === */
.import-label{cursor:pointer}
.import-label input{display:none}

/* === NEW: Better empty states === */
.empty-state .empty-actions{display:flex;gap:8px;justify-content:center;margin-top:12px;flex-wrap:wrap}

/* === NEW: Keyboard shortcut hints === */
.kbd{display:inline-block;padding:1px 5px;font-size:10px;font-family:'SF Mono',Monaco,Consolas,monospace;background:var(--gray-100);border:1px solid var(--gray-300);border-radius:3px;color:var(--gray-500);line-height:1.4}

/* Print updates */
@media print{
  .operator-bar,.storage-bar,.filter-select,.sep-v,.save-indicator,.kbd{display:none!important}
}

/* Mobile updates */
@media(max-width:640px){
  .operator-bar{flex-direction:column;align-items:stretch}
  .operator-bar label{min-width:70px}
  .summary-grid{grid-template-columns:1fr}
  .filter-select{min-width:90px;max-width:120px}
}
"""

content = content.replace('</style>', new_css + '\n</style>')

# ============================================================
# 2. HTML ADDITIONS
# ============================================================

# 2a. Add storage bar and handover/history/import buttons in header-actions
old_header_actions = '''<div class="header-actions">
      <button class="btn btn-ghost btn-sm" onclick="window.print()" title="Imprimir">'''
new_header_actions = '''<div class="header-actions">
      <div class="storage-bar" id="storageBar"><div class="bar"><div class="fill" id="storageFill"></div></div><span id="storageText"></span></div>
      <button class="btn btn-ghost btn-sm" onclick="showHandover()" title="Resumen de turno">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
      </button>
      <button class="btn btn-ghost btn-sm" onclick="showHistory()" title="Historial semanal">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
      </button>
      <label class="btn btn-ghost btn-sm import-label" title="Importar CSV">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
        <input type="file" accept=".csv" onchange="importCSV(event)">
      </label>
      <button class="btn btn-ghost btn-sm" onclick="showExportRange()" title="Exportar rango">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      </button>
      <span class="save-indicator" id="saveIndicator">&#10003; Guardado</span>
      <button class="btn btn-ghost btn-sm" onclick="window.print()" title="Imprimir">'''
content = content.replace(old_header_actions, new_header_actions)

# 2b. Add region/status filters in quick-bar
old_quickbar_end = '''    <div class="search-box">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input type="text" id="searchInput" placeholder="Buscar servidor, proceso..." oninput="render()">
    </div>
  </div>'''
new_quickbar_end = '''    <div class="search-box">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input type="text" id="searchInput" placeholder="Buscar servidor, proceso..." oninput="render()">
    </div>
    <div class="sep-v"></div>
    <select class="filter-select" id="filterRegion" onchange="render()">
      <option value="">Todas las regiones</option>
      <option value="ARGENTINA">Argentina</option>
      <option value="PERU">Peru</option>
      <option value="PANAMA">Panama</option>
      <option value="CHILE">Chile</option>
      <option value="MEXICO">Mexico</option>
    </select>
    <select class="filter-select" id="filterStatus" onchange="render()">
      <option value="">Todos los estados</option>
      <option value="ok">OK / Realizado</option>
      <option value="fail">Con errores</option>
      <option value="empty">Sin completar</option>
      <option value="pending">Pendiente</option>
    </select>
    <div class="sep-v"></div>
    <button class="btn btn-ghost btn-sm" onclick="cleanupOldData()" title="Limpiar datos antiguos (&gt;30 dias)">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
    </button>
  </div>'''
content = content.replace(old_quickbar_end, new_quickbar_end)

# 2c. Add operator/shift bar after notes-card
old_after_notes = '''  <div class="notes-card">
    <h3>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
      Notas del d\u00eda
    </h3>
    <textarea id="dayNotes" placeholder="Observaciones, incidencias, novedades del turno..." oninput="saveNotes()"></textarea>
  </div>'''
new_after_notes = '''  <div class="notes-card">
    <h3>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
      Notas del d\u00eda
    </h3>
    <textarea id="dayNotes" placeholder="Observaciones, incidencias, novedades del turno..." oninput="saveNotes()"></textarea>
  </div>
  <div class="operator-bar">
    <label>Operador:</label>
    <input type="text" id="operatorName" placeholder="Nombre del operador" oninput="saveOperator()" style="flex:1;min-width:120px">
    <label>Turno:</label>
    <select id="shiftSelect" onchange="saveOperator()" style="min-width:130px">
      <option value="Manana (06-14)">Manana (06-14)</option>
      <option value="Tarde (14-22)">Tarde (14-22)</option>
      <option value="Noche (22-06)">Noche (22-06)</option>
    </select>
    <span style="font-size:11px;color:var(--gray-400)"><span class="kbd">&larr;</span> <span class="kbd">&rarr;</span> dias &middot; <span class="kbd">Esc</span> cerrar &middot; <span class="kbd">N</span> nuevo</span>
  </div>'''
content = content.replace(old_after_notes, new_after_notes)

# ============================================================
# 3. JS MODIFICATIONS
# ============================================================

# 3a. Add esc() and utilities after DAYN
old_after_constants = "const DAYN=['Domingo','Lunes','Martes','Mi\u00e9rcoles','Jueves','Viernes','S\u00e1bado'];"
new_after_constants = """const DAYN=['Domingo','Lunes','Martes','Mi\u00e9rcoles','Jueves','Viernes','S\u00e1bado'];

// === XSS sanitization ===
function esc(s){if(!s)return'';const d=document.createElement('div');d.textContent=s;return d.innerHTML;}

// === Storage size control ===
function getStorageSize(){try{return new Blob([localStorage.getItem('bitacora_v2')||'']).size;}catch(e){return 0;}}
function fmtBytes(b){if(b<1024)return b+' B';if(b<1048576)return(b/1024).toFixed(1)+' KB';return(b/1048576).toFixed(1)+' MB';}
const MAX_STORAGE=4*1024*1024;
function updateStorageBar(){const sz=getStorageSize();const pct=Math.min(100,Math.round(sz/MAX_STORAGE*100));const fill=document.getElementById('storageFill');const txt=document.getElementById('storageText');if(fill){fill.style.width=pct+'%';fill.style.background=pct>80?'var(--red-500)':pct>50?'var(--amber-600)':'var(--emerald-600)';}if(txt)txt.textContent=fmtBytes(sz);}

// === Save indicator ===
let saveT;function showSaveInd(){const e=document.getElementById('saveIndicator');if(!e)return;e.classList.add('show');clearTimeout(saveT);saveT=setTimeout(()=>e.classList.remove('show'),2000);}

// === Operator / Shift ===
function loadOperator(){const d=getDay(currentDate);document.getElementById('operatorName').value=d.operator||'';document.getElementById('shiftSelect').value=d.shift||'Manana (06-14)';}
function saveOperator(){const d=getDay(currentDate);d.operator=document.getElementById('operatorName').value;d.shift=document.getElementById('shiftSelect').value;saveStore();}

// === Average times for out-of-schedule detection ===
function getAvgTimes(server){
  let totalBeg=0,totalEnd=0,countBeg=0,countEnd=0;
  Object.values(store).forEach(day=>{if(!day.pollings)return;day.pollings.forEach(p=>{if(p.server===server){if(p.phase==='BEGINNING'&&p.time){const s=p.time.split(':').map(Number);totalBeg+=s[0]*60+s[1];countBeg++;}if(p.phase==='ENDING'&&p.time){const s=p.time.split(':').map(Number);totalEnd+=s[0]*60+s[1];countEnd++;}}});});
  return{avgBeg:countBeg?totalBeg/countBeg:null,avgEnd:countEnd?totalEnd/countEnd:null,countBeg,countEnd};
}
function isLate(server,beg,end){
  const avg=getAvgTimes(server);
  if(!avg.avgBeg||!avg.avgEnd||avg.countBeg<3)return false;
  const THRESHOLD=30;
  if(beg){const s=beg.split(':').map(Number);const mins=s[0]*60+s[1];if(Math.abs(mins-avg.avgBeg)>THRESHOLD)return true;}
  if(end){const s=end.split(':').map(Number);const mins=s[0]*60+s[1];if(Math.abs(mins-avg.avgEnd)>THRESHOLD)return true;}
  return false;
}"""
content = content.replace(old_after_constants, new_after_constants)

# 3b. Modify saveStore
old_saveStore = "function saveStore(){localStorage.setItem('bitacora_v2',JSON.stringify(store));}"
new_saveStore = """function saveStore(){
  try{localStorage.setItem('bitacora_v2',JSON.stringify(store));}catch(e){
    if(e.name==='QuotaExceededError'){toast('Almacenamiento lleno. Usa el boton de limpieza.');return;}
    throw e;
  }
  showSaveInd();updateStorageBar();
}"""
content = content.replace(old_saveStore, new_saveStore)

# 3c. Modify loadStore to call updateStorageBar
old_loadStore = "function loadStore(){const s=localStorage.getItem('bitacora_v2');if(s)try{store=JSON.parse(s)}catch(e){store={};}for(const[k,v]of Object.entries(INITIAL_DATA)){if(!store[k])store[k]=JSON.parse(JSON.stringify(v));}saveStore();}"
new_loadStore = "function loadStore(){const s=localStorage.getItem('bitacora_v2');if(s)try{store=JSON.parse(s)}catch(e){store={};}for(const[k,v]of Object.entries(INITIAL_DATA)){if(!store[k])store[k]=JSON.parse(JSON.stringify(v));}saveStore();updateStorageBar();}"
content = content.replace(old_loadStore, new_loadStore)

# 3d. Modify render() to load operator + tab fade
old_render = """function render(){
  const day=getDay(currentDate);
  document.getElementById('dateDisplay').textContent=fmt(currentDate);
  const d=new Date(currentDate+'T12:00:00');
  document.getElementById('dayLabel').textContent=DAYN[d.getDay()];
  document.getElementById('typeSelect').value=day.dayType;
  const tb=document.getElementById('typeBadge');tb.className='badge '+TB[day.dayType];tb.textContent=TL[day.dayType];
  const servers=[...new Set(day.pollings.map(p=>p.server))].length;
  const endings=day.pollings.filter(p=>p.phase==='ENDING').length;
  const total=day.pollings.length;
  document.getElementById('statServers').textContent=servers;
  document.getElementById('statPollings').textContent=total>0?(endings+'/'+Math.floor(total/2)):'0/0';
  document.getElementById('statBackups').textContent=day.backups.length;
  const okP=day.processes.filter(p=>p.status==='OK'||p.status==='Realizado').length;
  document.getElementById('statProcesses').textContent=day.processes.length>0?(okP+'/'+day.processes.length):'—';
  loadNotes();
  if(activeTab==='pollings')renderPollings(day);else if(activeTab==='backups')renderBackups(day);else renderProcesses(day);
}"""
new_render = """function render(){
  const day=getDay(currentDate);
  document.getElementById('dateDisplay').textContent=fmt(currentDate);
  const d=new Date(currentDate+'T12:00:00');
  document.getElementById('dayLabel').textContent=DAYN[d.getDay()];
  document.getElementById('typeSelect').value=day.dayType;
  const tb=document.getElementById('typeBadge');tb.className='badge '+TB[day.dayType];tb.textContent=TL[day.dayType];
  const servers=[...new Set(day.pollings.map(p=>p.server))].length;
  const endings=day.pollings.filter(p=>p.phase==='ENDING').length;
  const total=day.pollings.length;
  document.getElementById('statServers').textContent=servers;
  document.getElementById('statPollings').textContent=total>0?(endings+'/'+Math.floor(total/2)):'0/0';
  document.getElementById('statBackups').textContent=day.backups.length;
  const okP=day.processes.filter(p=>p.status==='OK'||p.status==='Realizado').length;
  document.getElementById('statProcesses').textContent=day.processes.length>0?(okP+'/'+day.processes.length):'\u2014';
  loadNotes();loadOperator();
  const tc=document.getElementById('tabContent');tc.classList.add('fading');
  setTimeout(()=>{if(activeTab==='pollings')renderPollings(day);else if(activeTab==='backups')renderBackups(day);else renderProcesses(day);tc.classList.remove('fading');},80);
}"""
content = content.replace(old_render, new_render)

# 3e. Modify matchesFilter
old_matchesFilter = "function matchesFilter(text){const q=(SEARCH.value||'').toLowerCase();return!q||text.toLowerCase().includes(q);}"
new_matchesFilter = """function matchesFilter(text,region,status){
  const q=(SEARCH.value||'').toLowerCase();
  if(q&&!text.toLowerCase().includes(q))return false;
  const fR=document.getElementById('filterRegion').value;
  if(fR&&region&&region!==fR)return false;
  const fS=document.getElementById('filterStatus').value;
  if(fS&&status!==undefined){
    const u=(status||'').toUpperCase();
    if(fS==='ok'&&!['OK','REALIZADO'].includes(u))return false;
    if(fS==='fail'&&!u.includes('FAIL')&&!u.includes('SUSP')&&!u.includes('ROBOT')&&u!=='')return false;
    if(fS==='fail'&&u==='')return false;
    if(fS==='empty'&&u!=='')return false;
    if(fS==='pending'&&!u.includes('PEND'))return false;
  }
  return true;
}"""
content = content.replace(old_matchesFilter, new_matchesFilter)

# 3f. Modify renderPollings
old_renderPollings = """function renderPollings(day){
  const el=document.getElementById('tabContent');
  const byS={};day.pollings.forEach(p=>{if(!byS[p.server])byS[p.server]=[];byS[p.server].push(p);});
  const byR={};Object.entries(byS).forEach(([s,e])=>{const r=e[0].region||'REGIONAL';if(!byR[r])byR[r]=[];byR[r].push({server:s,entries:e});});
  const order=['ARGENTINA','PERU','PANAMA','CHILE','MEXICO','REGIONAL'];
  const regions=order.filter(r=>byR[r]);
  if(!regions.length){el.innerHTML='<div class="card"><div class="card-header"><h2>Pollings de Servidores</h2><button class="btn btn-primary btn-sm" onclick="openPollingModal()">+ Agregar</button></div><div class="empty-state"><p>No hay pollings para este dia</p></div></div>';return;}
  let h='<div class="card"><div class="card-header"><h2>Pollings de Servidores</h2><button class="btn btn-primary btn-sm" onclick="openPollingModal()">+ Agregar</button></div><div class="card-body">';
  regions.forEach(r=>{h+='<div class="region-group'+(matchesFilter(RL[r])?'':' hidden')+'"><span class="badge '+RB[r]+'">'+RL[r]+'</span><div style="margin-top:6px">';
    byR[r].forEach(({server:srv,entries})=>{
      if(!matchesFilter(srv))return;
      const beg=entries.find(e=>e.phase==='BEGINNING'),end=entries.find(e=>e.phase==='ENDING');
      const sinAc=beg&&beg.note==='SIN AC'||end&&end.note==='SIN AC';
      const dur=beg&&end?calcDur(beg.time,end.time):'';
      h+='<div class="server-row'+(sinAc?' error':'')+'"><div style="display:flex;align-items:center;gap:6px;flex:1;min-width:100px"><span class="server-name">'+srv+'</span>'+(sinAc?'<span class="badge badge-red">Sin AC</span>':'')+'</div><div class="server-meta"><span><span class="label">Ini </span><span class="time-val">'+(beg?beg.time||'\u2014':'\u2014')+'</span></span><span><span class="label">Fin </span><span class="time-val">'+(end?end.time||'\u2014':'\u2014')+'</span></span>'+(dur&&dur!=='\u2014'?'<span class="dur">'+dur+'</span>':'')+'<span class="server-actions"><button class="btn-icon" title="Editar" onclick="openPollingModal(\\''+srv+'\\')">'+PENCIL+'</button><button class="btn-icon danger" title="Eliminar" onclick="deletePolling(\\''+srv+'\\')">'+TRASH+'</button></span></div></div>';
    });h+='</div></div>';});h+='</div></div>';el.innerHTML=h;
}"""
new_renderPollings = r"""function renderPollings(day){
  const el=document.getElementById('tabContent');
  const byS={};day.pollings.forEach(p=>{if(!byS[p.server])byS[p.server]=[];byS[p.server].push(p);});
  const byR={};Object.entries(byS).forEach(([s,e])=>{const r=e[0].region||'REGIONAL';if(!byR[r])byR[r]=[];byR[r].push({server:s,entries:e});});
  const order=['ARGENTINA','PERU','PANAMA','CHILE','MEXICO','REGIONAL'];
  const regions=order.filter(r=>byR[r]);
  if(!regions.length){el.innerHTML='<div class="card"><div class="card-header"><h2>Pollings de Servidores</h2><button class="btn btn-primary btn-sm" onclick="openPollingModal()">+ Agregar</button></div><div class="empty-state"><p>No hay pollings para este dia</p><div class="empty-actions"><button class="btn btn-outline btn-sm" onclick="copyFromPrev()">Copiar dia anterior</button><button class="btn btn-primary btn-sm" onclick="openPollingModal()">+ Agregar servidor</button></div></div></div>';return;}
  let h='<div class="card"><div class="card-header"><h2>Pollings de Servidores</h2><button class="btn btn-primary btn-sm" onclick="openPollingModal()">+ Agregar</button></div><div class="card-body">';
  regions.forEach(r=>{h+='<div class="region-group'+(matchesFilter(RL[r],r)?'':' hidden')+'"><span class="badge '+RB[r]+'">'+RL[r]+'</span><div style="margin-top:6px">';
    byR[r].forEach(({server:srv,entries})=>{
      const beg=entries.find(e=>e.phase==='BEGINNING'),end=entries.find(e=>e.phase==='ENDING');
      const sinAc=beg&&beg.note==='SIN AC'||end&&end.note==='SIN AC';
      const dur=beg&&end?calcDur(beg.time,end.time):'';
      const late=!sinAc&&beg&&end&&beg.time&&end.time&&isLate(srv,beg.time,end.time);
      const stCat=sinAc?'fail':'';
      if(!matchesFilter(srv,r,stCat))return;
      const srvEsc=esc(srv);
      h+='<div class="server-row'+(sinAc?' error':'')+(late?' late':'')+'"><div style="display:flex;align-items:center;gap:6px;flex:1;min-width:100px"><span class="server-name">'+srvEsc+'</span>'+(sinAc?'<span class="badge badge-red">Sin AC</span>':'')+(late?'<span class="badge badge-amber">Fuera de horario</span>':'')+'</div><div class="server-meta"><span><span class="label">Ini </span><span class="time-val">'+(beg?beg.time||'\u2014':'\u2014')+'</span></span><span><span class="label">Fin </span><span class="time-val">'+(end?end.time||'\u2014':'\u2014')+'</span></span>'+(dur&&dur!=='\u2014'?'<span class="dur">'+dur+'</span>':'')+'<span class="server-actions"><button class="btn-icon" title="Editar" onclick="openPollingModal(\''+srvEsc.replace(/'/g,"\\'")+'\')">'+PENCIL+'</button><button class="btn-icon danger" title="Eliminar" onclick="deletePolling(\''+srvEsc.replace(/'/g,"\\'")+'\')">'+TRASH+'</button></span></div></div>';
    });h+='</div></div>';});h+='</div></div>';el.innerHTML=h;
}"""
content = content.replace(old_renderPollings, new_renderPollings)

# 3g. Modify renderBackups
old_renderBackups = """function renderBackups(day){
  const el=document.getElementById('tabContent');
  let h='<div class="card"><div class="card-header"><h2>Backups</h2><button class="btn btn-primary btn-sm" onclick="openBackupModal()">+ Agregar</button></div><div class="card-body">';
  if(!day.backups.length){h+='<div class="empty-state"><p>No hay backups</p></div>';}
  else{h+='<div style="padding:12px 16px">';day.backups.forEach((b,i)=>{if(!matchesFilter(b.name+(b.job||'')))return;const fail=b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'));h+='<div class="bkp-row'+(fail?' fail':'')+'"><div class="bkp-name"><span>'+b.name+'</span>'+(b.job?'<span class="badge badge-gray badge-mono" style="font-size:10px">'+b.job+'</span>':'')+sBadge(b.status)+'</div><div class="server-meta"><span><span class="label">Ini </span><span class="time-val">'+(b.iniTime||'\u2014')+'</span></span><span><span class="label">Fin </span><span class="time-val">'+(b.endTime||'\u2014')+'</span></span>'+(b.duration?'<span class="dur">'+b.duration+'</span>':'')+'<span class="server-actions"><button class="btn-icon" onclick="openBackupModal('+i+')">'+PENCIL+'</button><button class="btn-icon danger" onclick="deleteBackup('+i+')">'+TRASH+'</button></span></div></div>';});h+='</div>';}h+='</div></div>';el.innerHTML=h;
}"""
new_renderBackups = r"""function renderBackups(day){
  const el=document.getElementById('tabContent');
  let h='<div class="card"><div class="card-header"><h2>Backups</h2><button class="btn btn-primary btn-sm" onclick="openBackupModal()">+ Agregar</button></div><div class="card-body">';
  if(!day.backups.length){h+='<div class="empty-state"><p>No hay backups para este dia</p><div class="empty-actions"><button class="btn btn-outline btn-sm" onclick="copyFromPrev()">Copiar dia anterior</button><button class="btn btn-primary btn-sm" onclick="openBackupModal()">+ Agregar backup</button></div></div>';}
  else{h+='<div style="padding:12px 16px">';day.backups.forEach((b,i)=>{const fail=b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'));const bSt=fail?'fail':(b.status?'ok':'empty');if(!matchesFilter(esc(b.name)+(b.job||''),'',bSt))return;h+='<div class="bkp-row'+(fail?' fail':'')+'"><div class="bkp-name"><span>'+esc(b.name)+'</span>'+(b.job?'<span class="badge badge-gray badge-mono" style="font-size:10px">'+esc(b.job)+'</span>':'')+sBadge(b.status)+'</div><div class="server-meta"><span><span class="label">Ini </span><span class="time-val">'+(b.iniTime||'\u2014')+'</span></span><span><span class="label">Fin </span><span class="time-val">'+(b.endTime||'\u2014')+'</span></span>'+(b.duration?'<span class="dur">'+esc(b.duration)+'</span>':'')+'<span class="server-actions"><button class="btn-icon" onclick="openBackupModal('+i+')">'+PENCIL+'</button><button class="btn-icon danger" onclick="deleteBackup('+i+')">'+TRASH+'</button></span></div></div>';});h+='</div>';}h+='</div></div>';el.innerHTML=h;
}"""
content = content.replace(old_renderBackups, new_renderBackups)

# 3h. Modify renderProcesses
old_renderProcesses = """function renderProcesses(day){
  const el=document.getElementById('tabContent');
  let h='<div class="card"><div class="card-header"><h2>Procesos</h2><button class="btn btn-primary btn-sm" onclick="openProcessModal()">+ Agregar</button></div><div class="card-body">';
  if(!day.processes.length){h+='<div class="empty-state"><p>No hay procesos</p></div>';}
  else{h+='<div style="padding:12px 16px">';day.processes.forEach((p,i)=>{if(!matchesFilter(p.name+(p.status||'')))return;h+='<div class="proc-row"><div class="proc-name">'+sIcon(p.status)+'<span>'+p.name+'</span></div><div style="display:flex;align-items:center;gap:6px">'+sBadge(p.status)+'<button class="btn-icon" onclick="openProcessModal('+i+')">'+PENCIL+'</button><button class="btn-icon danger" onclick="deleteProcess('+i+')">'+TRASH+'</button></div></div>';});h+='</div>';}h+='</div></div>';el.innerHTML=h;
}"""
new_renderProcesses = r"""function renderProcesses(day){
  const el=document.getElementById('tabContent');
  let h='<div class="card"><div class="card-header"><h2>Procesos</h2><button class="btn btn-primary btn-sm" onclick="openProcessModal()">+ Agregar</button></div><div class="card-body">';
  if(!day.processes.length){h+='<div class="empty-state"><p>No hay procesos para este dia</p><div class="empty-actions"><button class="btn btn-outline btn-sm" onclick="copyFromPrev()">Copiar dia anterior</button><button class="btn btn-primary btn-sm" onclick="openProcessModal()">+ Agregar proceso</button></div></div>';}
  else{h+='<div style="padding:12px 16px">';day.processes.forEach((p,i)=>{const u=(p.status||'').toUpperCase();const cat=u==='OK'||u==='REALIZADO'?'ok':(u.includes('PEND')?'pending':(u==='N/A'||u==='N/C'?'na':(!p.status?'empty':'other')));if(!matchesFilter(esc(p.name)+(p.status||''),'',cat))return;h+='<div class="proc-row"><div class="proc-name">'+sIcon(p.status)+'<span>'+esc(p.name)+'</span></div><div style="display:flex;align-items:center;gap:6px">'+sBadge(p.status)+'<button class="btn-icon" onclick="openProcessModal('+i+')">'+PENCIL+'</button><button class="btn-icon danger" onclick="deleteProcess('+i+')">'+TRASH+'</button></div></div>';});h+='</div>';}h+='</div></div>';el.innerHTML=h;
}"""
content = content.replace(old_renderProcesses, new_renderProcesses)

# 3i. Modify openPollingModal to add note field
old_openPollingModal = """function openPollingModal(server){
  const day=getDay(currentDate);const isEdit=!!server;
  let beg='',end='';
  if(isEdit){const es=day.pollings.filter(p=>p.server===server);const b=es.find(e=>e.phase==='BEGINNING');const e=es.find(e=>e.phase==='ENDING');beg=b?b.time:'';end=e?e.time:'';}
  document.getElementById('modalTitle').textContent=isEdit?'Editar Polling':'Nuevo Polling';
  document.getElementById('modalBody').innerHTML='<div class="form-group"><label>Servidor</label><select id="mSrv">'+SERVERS.map(s=>'<option value="'+s+'"'+(s===server?' selected':'')+'>'+s+'</option>').join('')+'</select></div><div class="form-row"><div class="form-group"><label>Hora Inicio</label><input type="time" id="mBeg" value="'+beg+'"></div><div class="form-group"><label>Hora Fin</label><input type="time" id="mEnd" value="'+end+'"></div></div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="savePolling(\\''+server+'\\')">'+(isEdit?'Actualizar':'Guardar')+'</button>';
  openModal();
}"""
new_openPollingModal = r"""function openPollingModal(server){
  const day=getDay(currentDate);const isEdit=!!server;
  let beg='',end='',note='';
  if(isEdit){const es=day.pollings.filter(p=>p.server===server);const b=es.find(e=>e.phase==='BEGINNING');const e=es.find(e=>e.phase==='ENDING');beg=b?b.time:'';end=e?e.time:'';note=(b&&b.note)||(e&&e.note)||'';}
  document.getElementById('modalTitle').textContent=isEdit?'Editar Polling':'Nuevo Polling';
  document.getElementById('modalBody').innerHTML='<div class="form-group"><label>Servidor</label><select id="mSrv">'+SERVERS.map(s=>'<option value="'+esc(s)+'"'+(s===server?' selected':'')+'>'+esc(s)+'</option>').join('')+'</select></div><div class="form-row"><div class="form-group"><label>Hora Inicio</label><input type="time" id="mBeg" value="'+beg+'"></div><div class="form-group"><label>Hora Fin</label><input type="time" id="mEnd" value="'+end+'"></div></div><div class="form-group"><label>Nota</label><input type="text" id="mNote" value="'+esc(note)+'" placeholder="Ej: SIN AC, Sin conexion..."></div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="savePolling(\''+server+'\')">'+(isEdit?'Actualizar':'Guardar')+'</button>';
  openModal();
}"""
content = content.replace(old_openPollingModal, new_openPollingModal)

# 3j. Modify savePolling - validate times + save note
old_savePolling = """function savePolling(old){
  const day=getDay(currentDate);const srv=document.getElementById('mSrv').value;
  const beg=document.getElementById('mBeg').value;const end=document.getElementById('mEnd').value;
  if(old)day.pollings=day.pollings.filter(p=>p.server!==old);
  if(beg)day.pollings.push({id:uid(),server:srv,region:getRegion(srv),phase:'BEGINNING',date:currentDate,time:beg,note:null});
  if(end)day.pollings.push({id:uid(),server:srv,region:getRegion(srv),phase:'ENDING',date:currentDate,time:end,note:null});
  saveStore();closeModal();render();toast('Guardado');
}"""
new_savePolling = r"""function savePolling(old){
  const srv=document.getElementById('mSrv').value;
  const beg=document.getElementById('mBeg').value;const end=document.getElementById('mEnd').value;
  const note=(document.getElementById('mNote').value||'').trim()||null;
  if(beg&&end&&beg>end){toast('La hora de fin es anterior a la de inicio');return;}
  const day=getDay(currentDate);
  if(old)day.pollings=day.pollings.filter(p=>p.server!==old);
  if(beg)day.pollings.push({id:uid(),server:srv,region:getRegion(srv),phase:'BEGINNING',date:currentDate,time:beg,note:note});
  if(end)day.pollings.push({id:uid(),server:srv,region:getRegion(srv),phase:'ENDING',date:currentDate,time:end,note:note});
  saveStore();closeModal();render();toast('Guardado');
}"""
content = content.replace(old_savePolling, new_savePolling)

# 3k. Modify saveBackup - validate times
old_saveBackup = """function saveBackup(idx){
  const day=getDay(currentDate);
  const o={name:document.getElementById('mBkN').value,iniDate:currentDate,iniTime:document.getElementById('mBkI').value||null,endDate:currentDate,endTime:document.getElementById('mBkE').value||null,job:document.getElementById('mBkJ').value||null,duration:document.getElementById('mBkD').value||null,status:document.getElementById('mBkS').value||null};
  if(idx!==undefined)day.backups[idx]=o;else day.backups.push(o);saveStore();closeModal();render();toast('Guardado');
}"""
new_saveBackup = """function saveBackup(idx){
  const iniT=document.getElementById('mBkI').value||null;
  const endT=document.getElementById('mBkE').value||null;
  if(iniT&&endT&&iniT>endT){toast('La hora de fin es anterior a la de inicio');return;}
  const day=getDay(currentDate);
  const o={name:document.getElementById('mBkN').value,iniDate:currentDate,iniTime:iniT,endDate:currentDate,endTime:endT,job:document.getElementById('mBkJ').value||null,duration:document.getElementById('mBkD').value||null,status:document.getElementById('mBkS').value||null};
  if(idx!==undefined)day.backups[idx]=o;else day.backups.push(o);saveStore();closeModal();render();toast('Guardado');
}"""
content = content.replace(old_saveBackup, new_saveBackup)

# 3l. Modify navDay to reset filters
old_navDay = "function navDay(dir){const d=new Date(currentDate+'T12:00:00');d.setDate(d.getDate()+dir);currentDate=d.toISOString().split('T')[0];SEARCH.value='';render();}"
new_navDay = "function navDay(dir){const d=new Date(currentDate+'T12:00:00');d.setDate(d.getDate()+dir);currentDate=d.toISOString().split('T')[0];SEARCH.value='';document.getElementById('filterRegion').value='';document.getElementById('filterStatus').value='';render();}"
content = content.replace(old_navDay, new_navDay)

# 3m. Modify calClick to reset filters
old_calClick = "function calClick(y,m,d){const dt=new Date(y,m,d);currentDate=dt.toISOString().split('T')[0];SEARCH.value='';document.getElementById('calPopup').style.display='none';render();}"
new_calClick = "function calClick(y,m,d){const dt=new Date(y,m,d);currentDate=dt.toISOString().split('T')[0];SEARCH.value='';document.getElementById('filterRegion').value='';document.getElementById('filterStatus').value='';document.getElementById('calPopup').style.display='none';render();}"
content = content.replace(old_calClick, new_calClick)

# 3n. Add all new functions before final loadStore();render();
new_functions = r"""
// === Keyboard shortcuts ===
document.addEventListener('keydown',e=>{
  const tag=e.target.tagName;
  const inInput=tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT';
  if(e.key==='Escape'){closeModal();document.getElementById('calPopup').style.display='none';return;}
  if(inInput)return;
  if(e.key==='ArrowLeft'){e.preventDefault();navDay(-1);}
  if(e.key==='ArrowRight'){e.preventDefault();navDay(1);}
  if(e.key==='n'||e.key==='N'){e.preventDefault();if(activeTab==='pollings')openPollingModal();else if(activeTab==='backups')openBackupModal();else openProcessModal();}
});

// === Handover / Shift summary ===
function showHandover(){
  const day=getDay(currentDate);
  const totalPollings=day.pollings.filter(p=>p.phase==='ENDING').length;
  const expectedPollings=Math.floor(day.pollings.length/2);
  const sinAc=day.pollings.filter(p=>p.note==='SIN AC').length;
  const failBkp=day.backups.filter(b=>b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'))).length;
  const okProc=day.processes.filter(p=>{const u=(p.status||'').toUpperCase();return u==='OK'||u==='REALIZADO';}).length;
  const pendProc=day.processes.filter(p=>{const u=(p.status||'').toUpperCase();return u.includes('PEND');}).length;
  const naProc=day.processes.filter(p=>{const u=(p.status||'').toUpperCase();return u==='N/A'||u==='N/C';}).length;
  const totalLate=day.pollings.filter(p=>{if(p.phase!=='BEGINNING'||!p.time)return false;const avg=getAvgTimes(p.server);if(!avg.avgBeg||avg.countBeg<3)return false;const s=p.time.split(':').map(Number);return Math.abs(s[0]*60+s[1]-avg.avgBeg)>30;}).length;

  let h='<div class="summary-modal-body">';
  h+='<div style="text-align:center;margin-bottom:12px"><strong>'+fmt(currentDate)+'</strong> &mdash; '+DAYN[new Date(currentDate+'T12:00:00').getDay()]+'<br><span class="badge '+TB[day.dayType]+'">'+TL[day.dayType]+'</span>'+(day.operator?'<br>Operador: <strong>'+esc(day.operator)+'</strong>'+(day.shift?' ('+esc(day.shift)+')':''):'')+'</div>';

  h+='<div class="summary-section"><h4><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><circle cx="6" cy="6" r="1"/><circle cx="6" cy="18" r="1"/></svg> Pollings</h4><div class="summary-grid">';
  h+='<div class="summary-item"><span>Completados</span><span class="val" style="color:var(--emerald-600)">'+totalPollings+'/'+expectedPollings+'</span></div>';
  if(sinAc)h+='<div class="summary-item"><span>Sin AC</span><span class="val" style="color:var(--red-500)">'+sinAc+'</span></div>';
  if(totalLate)h+='<div class="summary-item"><span>Fuera de horario</span><span class="val" style="color:var(--amber-600)">'+totalLate+'</span></div>';
  h+='</div></div>';

  h+='<div class="summary-section"><h4><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/></svg> Backups</h4><div class="summary-grid">';
  h+='<div class="summary-item"><span>Total</span><span class="val">'+day.backups.length+'</span></div>';
  h+='<div class="summary-item"><span>Con errores</span><span class="val" style="color:var(--red-500)">'+failBkp+'</span></div>';
  if(failBkp){h+='<div style="margin-top:4px">';day.backups.filter(b=>b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'))).forEach(b=>{h+='<span class="badge badge-red" style="margin:2px">'+esc(b.name)+': '+esc(b.status)+'</span>';});h+='</div>';}
  h+='</div></div>';

  h+='<div class="summary-section"><h4><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/></svg> Procesos</h4><div class="summary-grid">';
  h+='<div class="summary-item"><span>OK / Realizado</span><span class="val" style="color:var(--emerald-600)">'+okProc+'</span></div>';
  if(pendProc)h+='<div class="summary-item"><span>Pendientes</span><span class="val" style="color:var(--amber-600)">'+pendProc+'</span></div>';
  if(naProc)h+='<div class="summary-item"><span>N/A</span><span class="val" style="color:var(--gray-500)">'+naProc+'</span></div>';
  h+='</div></div>';

  if(day.notes){h+='<div class="summary-section"><h4><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg> Notas</h4><div class="summary-notes">'+esc(day.notes)+'</div></div>';}
  h+='</div>';

  document.getElementById('modalTitle').textContent='Resumen de Turno';
  document.getElementById('modalBody').innerHTML=h;
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cerrar</button><button class="btn btn-primary" onclick="closeModal();window.print()"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg> Imprimir</button>';
  openModal();
}

// === Weekly history ===
function showHistory(){
  const today=new Date();today.setHours(12,0,0,0);
  const days=[];
  for(let i=6;i>=0;i--){const d=new Date(today);d.setDate(d.getDate()-i);const ds=d.toISOString().split('T')[0];const day=store[ds]||{pollings:[],backups:[],processes:[]};const totalP=Math.floor((day.pollings||[]).length/2);const endP=(day.pollings||[]).filter(p=>p.phase==='ENDING').length;const failB=(day.backups||[]).filter(b=>b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'))).length;const okPr=(day.processes||[]).filter(p=>{const u=(p.status||'').toUpperCase();return u==='OK'||u==='REALIZADO';}).length;days.push({date:ds,label:DN[d.getDay()]+' '+d.getDate(),totalP,endP,failB,totalB:(day.backups||[]).length,okPr,totalPr:(day.processes||[]).length});}
  const maxP=Math.max(1,...days.map(d=>d.totalP));
  let h='<div class="summary-modal-body">';
  h+='<div class="summary-section"><h4>Pollings completados (ultimos 7 dias)</h4>';
  days.forEach(d=>{const pct=Math.round(d.endP/maxP*100);h+='<div class="week-row" style="cursor:pointer" onclick="currentDate=\''+d.date+'\';closeModal();render();"><span class="week-label">'+d.label+'</span><div class="week-bar-bg"><div class="week-bar-fill '+(d.endP<d.totalP?'fail':'ok')+'" style="width:'+pct+'%"></div></div><span class="week-val">'+d.endP+'/'+d.totalP+'</span></div>';});
  h+='</div>';
  h+='<div class="summary-section"><h4>Backups con error</h4>';
  days.forEach(d=>{const pct=d.totalB?Math.round(d.failB/d.totalB*100):0;h+='<div class="week-row" style="cursor:pointer" onclick="currentDate=\''+d.date+'\';closeModal();render();"><span class="week-label">'+d.label+'</span><div class="week-bar-bg"><div class="week-bar-fill '+(d.failB>0?'fail':'ok')+'" style="width:'+(pct||2)+'%"></div></div><span class="week-val">'+d.failB+'/'+d.totalB+'</span></div>';});
  h+='</div></div>';
  document.getElementById('modalTitle').textContent='Historial Semanal';
  document.getElementById('modalBody').innerHTML=h;
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cerrar</button>';
  openModal();
}

// === Export date range CSV ===
function showExportRange(){
  const today=new Date().toISOString().split('T')[0];
  const weekAgo=new Date();weekAgo.setDate(weekAgo.getDate()-7);const from=weekAgo.toISOString().split('T')[0];
  document.getElementById('modalTitle').textContent='Exportar rango de fechas';
  document.getElementById('modalBody').innerHTML='<div class="form-row"><div class="form-group"><label>Desde</label><input type="date" id="expFrom" value="'+from+'"></div><div class="form-group"><label>Hasta</label><input type="date" id="expTo" value="'+today+'"></div></div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="doExportRange()">Exportar CSV</button>';
  openModal();
}
function doExportRange(){
  const from=document.getElementById('expFrom').value;const to=document.getElementById('expTo').value;
  if(!from||!to||from>to){toast('Rango de fechas invalido');return;}
  let csv='Fecha,Tipo,Nombre,Region/Detalle,Fase,Hora Ini,Hora Fin,Duracion,Estado,JOB,Operador,Turno,Notas\n';
  const d=new Date(from+'T12:00:00');const end=new Date(to+'T12:00:00');
  while(d<=end){const ds=d.toISOString().split('T')[0];const day=store[ds];if(day){(day.pollings||[]).forEach(p=>{csv+=ds+',Polling,'+p.server+','+p.region+','+p.phase+','+(p.phase==='BEGINNING'?p.time:'')+','+(p.phase==='ENDING'?p.time:'')+',,'+(p.note||'')+',,'+(day.operator||'')+','+(day.shift||''),\n';});(day.backups||[]).forEach(b=>{csv+=ds+',Backup,'+b.name+',,,'+(b.iniTime||'')+','+(b.endTime||'')+','+(b.duration||'')+','+(b.status||'')+','+(b.job||'')+','+(day.operator||'')+','+(day.shift||''),\n';});(day.processes||[]).forEach(p=>{csv+=ds+',Proceso,'+p.name+',,,,,,,'+(p.status||'')+','+(day.operator||'')+','+(day.shift||''),\n';});}d.setDate(d.getDate()+1);}
  const blob=new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8;'});const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='bitacora_'+from+'_a_'+to+'.csv';a.click();closeModal();toast('CSV descargado ('+from+' a '+to+')');
}

// === Import CSV ===
function importCSV(event){
  const file=event.target.files[0];if(!file)return;
  const reader=new FileReader();
  reader.onload=function(e){
    try{
      const text=e.target.result;const lines=text.split('\n');let count=0;
      for(let i=1;i<lines.length;i++){const l=lines[i].trim();if(!l)continue;const cols=l.split(',');if(cols.length<3)continue;
        const ds=cols[0].trim();if(!/^\d{4}-\d{2}-\d{2}$/.test(ds))continue;
        const day=getDay(ds);const tipo=cols[1].trim();
        if(tipo==='Polling'&&cols[2]&&cols[5]){day.pollings.push({id:uid(),server:cols[2].trim(),region:getRegion(cols[2].trim()),phase:'BEGINNING',date:ds,time:cols[5].trim(),note:null});}
        if(tipo==='Backup'&&cols[2]){day.backups.push({name:cols[2].trim(),iniDate:ds,iniTime:cols[5]||null,endDate:ds,endTime:cols[6]||null,job:cols[9]||null,duration:cols[7]||null,status:cols[8]||null});}
        if(tipo==='Proceso'&&cols[2]){day.processes.push({name:cols[2].trim(),status:cols[8]||''});}
        count++;
      }
      saveStore();render();toast('Importados '+count+' registros');
    }catch(err){toast('Error al importar: '+err.message);}
  };
  reader.readAsText(file);event.target.value='';
}

// === Cleanup old data ===
function cleanupOldData(){
  const keys=Object.keys(store).filter(k=>/^\d{4}-\d{2}-\d{2}$/.test(k)).sort();
  if(keys.length<=30){toast('No hay suficientes datos para limpiar');return;}
  const cutoff=keys[keys.length-31];
  if(!confirm('Se eliminaran los datos anteriores a '+fmt(cutoff)+' ('+keys.indexOf(cutoff)+' dias). Continuar?'))return;
  keys.forEach(k=>{if(k<cutoff)delete store[k];});
  saveStore();render();toast('Datos antiguos eliminados');
}
"""

old_final = "loadStore();render();\n</script>"
new_final = new_functions + "loadStore();render();\n</script>"
content = content.replace(old_final, new_final)

# Write the result
with open('/home/z/my-project/download/bitacora_noc_mejorada.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("OK - File generated successfully!")
print(f"Size: {len(content)} chars")