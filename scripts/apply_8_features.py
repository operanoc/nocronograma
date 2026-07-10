#!/usr/bin/env python3
"""Apply 8 improvements to bitacora_noc_con_login.html"""

import re

PATH = '/home/z/my-project/download/bitacora_noc_con_login.html'

with open(PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# FEATURE 8: Branding consistente paleta violeta Semantix
# ============================================================
# Header gradient violet
html = html.replace(
    '.header{background:var(--white);border-bottom:1px solid var(--gray-200);',
    '.header{background:linear-gradient(135deg,#6A0DAD 0%,#5A0C9D 100%);border-bottom:2px solid #4A0A80;'
)
# Header text white
html = html.replace(
    '.header h1{font-size:17px;font-weight:700;display:flex;align-items:center;gap:8px}\n.header h1 svg{color:var(--emerald-600)}',
    '.header h1{font-size:17px;font-weight:700;display:flex;align-items:center;gap:8px;color:#fff}\n.header h1 svg{color:#e0d0f0}'
)
# Header actions color
html = html.replace(
    '.header-actions{display:flex;align-items:center;gap:6px}',
    '.header-actions{display:flex;align-items:center;gap:6px;color:#e0d0f0}'
)
# Dark mode header
html = html.replace(
    'html.dark{\n  --bg:#0f172a;',
    'html.dark{\n  --bg:#0f172a;--header-bg:linear-gradient(135deg,#3A0A80 0%,#2d0860 100%);'
)
# Footer
html = html.replace(
    '.footer{margin-top:auto;border-top:1px solid var(--gray-200);background:var(--white);padding:8px;text-align:center;font-size:11px;color:var(--gray-400);transition:background .3s}',
    '.footer{margin-top:auto;border-top:2px solid #4A0A80;background:#6A0DAD;padding:10px;text-align:center;font-size:11px;color:#e0d0f0}'
)
# "Hoy" button violet
html = html.replace(
    """onclick="goToday()" style="color:var(--emerald-600);font-size:12px">Hoy</button>""",
    """onclick="goToday()" style="background:rgba(255,255,255,.2);color:#fff;border:1px solid rgba(255,255,255,.3);font-size:12px;border-radius:var(--radius);padding:4px 10px">Hoy</button>"""
)
# Sync indicator color in header
old_sync_idle = """el.title='Sin sincronizar';el.style.color='var(--gray-400)'"""
new_sync_idle = """el.title='Sin sincronizar';el.style.color='#c4b0e0'"""
html = html.replace(old_sync_idle, new_sync_idle)
# Pase de turno button in header - white text
html = html.replace(
    '.btn-cierre{display:inline-flex;align-items:center;gap:5px;padding:6px 14px;background:var(--amber-600);color:#fff;border-radius:var(--radius);font-size:12px;font-weight:600;cursor:pointer;transition:background .15s;white-space:nowrap}',
    '.btn-cierre{display:inline-flex;align-items:center;gap:5px;padding:6px 14px;background:var(--amber-600);color:#fff;border-radius:var(--radius);font-size:12px;font-weight:600;cursor:pointer;transition:background .15s;white-space:nowrap;box-shadow:0 2px 8px rgba(217,119,6,.3)}'
)
# Lock banner violet tint
html = html.replace(
    '.lock-banner{background:var(--red-50);border:1px solid var(--red-500);border-radius:var(--radius);padding:10px 16px;margin-bottom:12px;display:flex;align-items:center;gap:10px;color:var(--red-800);font-size:13px;animation:fadeIn .3s}',
    '.lock-banner{background:var(--emerald-50);border:1px solid var(--emerald-600);border-radius:var(--radius);padding:10px 16px;margin-bottom:12px;display:flex;align-items:center;gap:10px;color:var(--emerald-800);font-size:13px;animation:fadeIn .3s}'
)
html = html.replace(
    '.lock-banner svg{flex-shrink:0;color:var(--red-500)}\n.lock-banner strong{color:var(--red-600)}',
    '.lock-banner svg{flex-shrink:0;color:var(--emerald-600)}\n.lock-banner strong{color:var(--emerald-700)}'
)
# Print override
html = html.replace(
    '  body{background:#fff;color:#000}\n}',
    '  body{background:#fff;color:#000}\n  .header{background:#6A0DAD!important;color:#fff!important}\n  .header *{color:#fff!important}\n  .footer{background:#6A0DAD!important;color:#fff!important}\n}'
)

# ============================================================
# FEATURE 6: Responsive / mobile <480px
# ============================================================
responsive_css = """
@media(max-width:480px){
  .stats{grid-template-columns:1fr 1fr}
  .server-row,.bkp-row,.proc-row{flex-direction:column;align-items:stretch;gap:4px}
  .server-name,.bkp-name,.proc-name{min-width:0;width:100%}
  .server-meta{width:100%;justify-content:flex-start;gap:8px;padding-left:4px}
  .bkp-name{flex-direction:column;gap:4px}
  .server-actions{align-self:flex-end}
  .date-nav{padding:8px 10px}
  .date-nav-left{gap:4px}
  .date-display{min-width:140px;font-size:12px;padding:6px 8px}
  .quick-bar{gap:4px;padding:6px 8px}
  .quick-bar .btn{font-size:11px;padding:4px 8px}
  .search-box{min-width:100px;max-width:none;order:10;flex-basis:100%}
  .card-header h2{font-size:13px}
  .tabs-bar{gap:0}
  .tab-btn{padding:8px 10px;font-size:12px}
  .timeline-add-bar{flex-direction:column}
  .timeline-add-bar select{max-width:none}
  .header h1{font-size:14px}
  .header h1 svg{width:16px;height:16px}
  .header-inner{gap:4px}
  .btn-cierre{font-size:11px;padding:5px 10px}
  .notif-panel{width:calc(100vw - 16px);right:-80px}
  .user-bar .user-name{font-size:11px}
}
"""
html = html.replace(
    '@media(max-width:640px){.notif-panel{width:calc(100vw - 32px);right:-60px}.btn-cierre,.btn-novedades{font-size:11px;padding:5px 10px}}',
    '@media(max-width:640px){.notif-panel{width:calc(100vw - 32px);right:-60px}.btn-cierre,.btn-novedades{font-size:11px;padding:5px 10px}}\n' + responsive_css
)

# ============================================================
# FEATURE 3: Idle warning CSS
# ============================================================
idle_css = """
.stat-card.idle-warning{border:2px solid var(--amber-600);background:var(--amber-50);animation:idlePulse 2s ease-in-out infinite}
.stat-card.idle-warning .stat-value{color:var(--amber-600)!important}
.stat-card.idle-warning .stat-label{color:var(--amber-800)!important}
html.dark .stat-card.idle-warning{border-color:var(--amber-600);background:rgba(217,119,6,.1)}
@keyframes idlePulse{0%,100%{opacity:1}50%{opacity:.85}}
"""
# Insert before the closing </style>
html = html.replace('</style>', idle_css + '\n</style>')

# ============================================================
# FEATURE 7: Critical notification CSS
# ============================================================
notif_critical_css = """
.notif-item.critical{border-left:4px solid var(--red-500);background:var(--red-50)}
html.dark .notif-item.critical{background:rgba(220,38,38,.08)}
.notif-item.critical .notif-icon-wrap{background:var(--red-100);color:var(--red-600)}
.notif-ack-btn{font-size:10px;color:var(--emerald-600);cursor:pointer;background:none;border:1px solid var(--emerald-600);border-radius:99px;padding:2px 8px;font-weight:600;transition:all .15s;white-space:nowrap}
.notif-ack-btn:hover{background:var(--emerald-600);color:#fff}
"""
html = html.replace('</style>', notif_critical_css + '\n</style>')

# ============================================================
# FEATURE 2: Timeout modal CSS
# ============================================================
timeout_css = """
.timeout-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:9998;display:flex;align-items:center;justify-content:center;padding:16px}
.timeout-overlay.hide{display:none}
.timeout-box{background:var(--white);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.3);width:100%;max-width:400px;padding:32px;text-align:center}
.timeout-box h3{font-size:18px;font-weight:700;color:var(--gray-800);margin-bottom:8px}
.timeout-box p{color:var(--gray-500);font-size:13px;margin-bottom:20px}
.timeout-countdown{font-size:32px;font-weight:700;color:var(--red-600);margin-bottom:16px;font-family:'SF Mono',Monaco,Consolas,monospace}
.timeout-box .btn-keep{width:100%;padding:12px;background:#6A0DAD;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;transition:background .15s}
.timeout-box .btn-keep:hover{background:#5A0C9D}
"""
html = html.replace('</style>', timeout_css + '\n</style>')

# ============================================================
# FEATURE 2: Timeout modal HTML
# ============================================================
timeout_html = """
<div class="timeout-overlay hide" id="timeoutOverlay">
  <div class="timeout-box">
    <h3>Sesion por inactividad</h3>
    <p>No se detecto actividad. La sesion se cerrara automaticamente.</p>
    <div class="timeout-countdown" id="timeoutCountdown">60</div>
    <button class="btn-keep" onclick="keepSession()">Seguir conectado</button>
  </div>
</div>
"""
# Insert before the toast div
html = html.replace(
    '<div class="toast" id="toast"></div>',
    timeout_html + '\n<div class="toast" id="toast"></div>'
)

# ============================================================
# FEATURE 5: SheetJS CDN
# ============================================================
html = html.replace(
    '<script>',
    '<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>\n<script>'
)

# ============================================================
# FEATURE 5: XLSX button in quick-bar
# ============================================================
html = html.replace(
    '''<button class="btn btn-outline btn-sm" onclick="exportCSV()">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      Exportar CSV
    </button>''',
    '''<button class="btn btn-outline btn-sm" onclick="exportCSV()">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      Exportar CSV
    </button>
    <button class="btn btn-outline btn-sm" onclick="exportXLSX()" style="border-color:var(--emerald-600);color:var(--emerald-600)">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      Descargar XLSX
    </button>'''
)

# ============================================================
# JS: FEATURE 2 - Inactivity Timeout
# ============================================================
timeout_js = """
// ===== INACTIVITY TIMEOUT =====
const INACTIVITY_TIMEOUT_MIN=15;
const INACTIVITY_WARNING_MIN=1;
let _inactivityTimer=null;
let _warningTimer=null;
let _sessionStartTime=Date.now();

function resetInactivityTimer(){
  if(_inactivityTimer)clearTimeout(_inactivityTimer);
  if(_warningTimer)clearTimeout(_warningTimer);
  document.getElementById('timeoutOverlay').classList.add('hide');
  _inactivityTimer=setTimeout(showInactivityWarning,(INACTIVITY_TIMEOUT_MIN-INACTIVITY_WARNING_MIN)*60*1000);
}
function showInactivityWarning(){
  if(!currentUser)return;
  document.getElementById('timeoutOverlay').classList.remove('hide');
  let secs=INACTIVITY_WARNING_MIN*60;
  document.getElementById('timeoutCountdown').textContent=secs;
  _warningTimer=setInterval(()=>{
    secs--;
    document.getElementById('timeoutCountdown').textContent=secs;
    if(secs<=0){clearInterval(_warningTimer);forceLogout();}
  },1000);
}
function keepSession(){
  document.getElementById('timeoutOverlay').classList.add('hide');
  if(_warningTimer)clearInterval(_warningTimer);
  resetInactivityTimer();
}
function forceLogout(){
  document.getElementById('timeoutOverlay').classList.add('hide');
  if(_warningTimer)clearInterval(_warningTimer);
  if(_inactivityTimer)clearTimeout(_inactivityTimer);
  currentUser=null;
  sessionStorage.removeItem('bitacora_user');
  document.getElementById('loginOverlay').classList.remove('hide');
  document.getElementById('userBar').style.display='none';
  document.getElementById('dashBtn').style.display='none';
  document.getElementById('loginUser').value='';
  document.getElementById('loginPass').value='';
  showTurnoButtons();
  toast('Sesion cerrada por inactividad');
}
['click','keydown','mousemove','scroll','touchstart'].forEach(ev=>{
  document.addEventListener(ev,()=>{if(currentUser)resetInactivityTimer();},{passive:true});
});
"""

# ============================================================
# JS: FEATURE 3 - Idle warning for zero counters
# ============================================================
idle_js = """
// ===== IDLE COUNTER WARNING =====
const IDLE_WARNING_HOURS=2;
let _hasAnyData=false;
function checkIdleWarning(){
  if(!currentUser)return;
  const day=store[currentDate];
  if(!day)return;
  const hasData=day.pollings.length||day.backups.length||day.processes.length;
  if(hasData)_hasAnyData=true;
  const elapsed=(Date.now()-_sessionStartTime)/(1000*60*60);
  const cards=document.querySelectorAll('.stat-card');
  const showWarning=!_hasAnyData&&elapsed>=IDLE_WARNING_HOURS;
  cards.forEach(c=>{if(showWarning)c.classList.add('idle-warning');else c.classList.remove('idle-warning');});
}
"""

# ============================================================
# JS: FEATURE 1 - Audit Log
# ============================================================
audit_js = """
// ===== AUDIT LOG =====
function addAuditEntry(dayDate,action,details){
  const day=getDay(dayDate);
  if(!day.auditLog)day.auditLog=[];
  const now=new Date();
  const ts=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0')+' '+String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0')+':'+String(now.getSeconds()).padStart(2,'0');
  day.auditLog.push({id:uid(),action:action,user:currentUser?currentUser.username:'SYSTEM',timestamp:ts,details:details||''});
  saveStore();
}
function checkAdminReopen(dayDate){
  if(!isAdmin())return true; // non-admins blocked by lock
  if(!isDayLocked(dayDate))return true;
  // Admin editing a locked day - require reason
  const reason=prompt('Este dia esta cerrado. Ingrese el MOTIVO de reapertura:');
  if(!reason||!reason.trim()){toast('Debe ingresar un motivo para reaperturar el dia');return false;}
  addAuditEntry(dayDate,'REAPERTURA','Motivo: '+reason.trim());
  return true;
}
function openAuditLog(){
  // Gather all audit entries from all days
  const allEntries=[];
  Object.entries(store).forEach(([dateStr,day])=>{
    if(day.auditLog)day.auditLog.forEach(e=>allEntries.push({...e,date:dateStr}));
  });
  allEntries.sort((a,b)=>b.timestamp.localeCompare(a.timestamp));
  let h='<div style="padding:14px 16px">';
  if(!allEntries.length){h+='<p style="color:var(--gray-400);text-align:center;padding:20px">Sin registros de auditoria</p>';}
  else{
    h+='<table style="width:100%;border-collapse:collapse;font-size:12px"><thead><tr><th style="text-align:left;padding:6px 8px;border-bottom:2px solid var(--gray-200)">Fecha/Hora</th><th style="text-align:left;padding:6px 8px;border-bottom:2px solid var(--gray-200)">Dia</th><th style="text-align:left;padding:6px 8px;border-bottom:2px solid var(--gray-200)">Accion</th><th style="text-align:left;padding:6px 8px;border-bottom:2px solid var(--gray-200)">Usuario</th><th style="text-align:left;padding:6px 8px;border-bottom:2px solid var(--gray-200)">Detalle</th></tr></thead><tbody>';
    allEntries.forEach(e=>{
      const isClose=e.action==='CIERRE';
      const isReopen=e.action==='REAPERTURA';
      const rowStyle=isClose?'color:var(--amber-800);background:var(--amber-50)':isReopen?'color:var(--red-600);background:var(--red-50)':'';
      const badge=isClose?'<span class="badge badge-amber">Cierre</span>':isReopen?'<span class="badge badge-red">Reapertura</span>':'<span class="badge badge-gray">'+escHtml(e.action)+'</span>';
      h+='<tr style="'+rowStyle+'"><td style="padding:6px 8px;border-bottom:1px solid var(--gray-100);font-family:monospace;font-size:11px;white-space:nowrap">'+escHtml(e.timestamp)+'</td><td style="padding:6px 8px;border-bottom:1px solid var(--gray-100);white-space:nowrap">'+escHtml(e.date)+'</td><td style="padding:6px 8px;border-bottom:1px solid var(--gray-100)">'+badge+'</td><td style="padding:6px 8px;border-bottom:1px solid var(--gray-100);font-weight:600">'+escHtml(e.user)+'</td><td style="padding:6px 8px;border-bottom:1px solid var(--gray-100);max-width:300px;word-break:break-word">'+escHtml(e.details)+'</td></tr>';
    });
    h+='</tbody></table>';
  }
  h+='</div>';
  document.getElementById('modalTitle').textContent='Historial de Auditoria';
  document.getElementById('modalBody').innerHTML=h;
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cerrar</button>';
  openModal();
}
"""

# ============================================================
# JS: FEATURE 5 - XLSX Export
# ============================================================
xlsx_js = """
// ===== XLSX EXPORT =====
function exportXLSX(){
  if(typeof XLSX==='undefined'){toast('Libreria XLSX no cargada. Verifique la conexion.');return;}
  const day=store[currentDate]||{pollings:[],backups:[],processes:[],handovers:[]};
  const wb=XLSX.utils.book_new();
  // Style helpers
  const hdrStyle={fill:{fgColor:{rgb:'6A0DAD'}},font:{bold:true,color:{rgb:'FFFFFF'}},alignment:{horizontal:'center'}};
  const okStyle={font:{color:{rgb:'059669'}}};
  const errStyle={font:{color:{rgb:'DC2626'},bold:true}};
  function applySheet(ws,cols,rows){
    XLSX.utils.sheet_add_aoa(ws,rows,{origin:'A1'});
    ws['!cols']=cols.map(c=>({wch:c}));
    // Apply header style
    const range=XLSX.utils.decode_range(ws['!ref']||'A1');
    for(let c=range.s.c;c<=range.e.c;c++){
      const cell=ws[XLSX.utils.encode_cell({r:range.s.r,c:c})];
      if(cell)cell.s=hdrStyle;
    }
  }
  // Sheet 1: Pollings
  if(day.pollings&&day.pollings.length){
    const byS={};day.pollings.forEach(p=>{if(!byS[p.server])byS[p.server]=[];byS[p.server].push(p);});
    const rows=[['Servidor','Region','Inicio','Fin','Duracion']];
    Object.entries(byS).forEach(([srv,entries])=>{
      const beg=entries.find(e=>e.phase==='BEGINNING');
      const end=entries.find(e=>e.phase==='ENDING');
      const reg=beg?beg.region:(end?end.region:'');
      rows.push([srv,reg,beg?beg.time:'',end?end.time:'',beg&&end?calcDur(beg.time,end.time):'']);
    });
    const ws=XLSX.utils.aoa_to_sheet(rows);
    applySheet(ws,[30,15,12,12,12],rows);
    XLSX.utils.book_append_sheet(wb,ws,'Pollings');
  }
  // Sheet 2: Backups
  if(day.backups&&day.backups.length){
    const rows=[['Servidor','JOB','Fecha Inicio','Hora Inicio','Fecha Fin','Hora Fin','Duracion','Estado']];
    day.backups.forEach(b=>{
      rows.push([b.name,b.job||'',b.iniDate||'',b.iniTime||'',b.endDate||'',b.endTime||'',b.duration||'',b.status||'']);
      // Color status cell
    });
    const ws=XLSX.utils.aoa_to_sheet(rows);
    applySheet(ws,[20,15,15,12,15,12,12,10],rows);
    XLSX.utils.book_append_sheet(wb,ws,'Backups');
  }
  // Sheet 3: Procesos
  if(day.processes&&day.processes.length){
    const rows=[['Proceso','Estado']];
    day.processes.forEach(p=>{rows.push([p.name,p.status||'']);});
    const ws=XLSX.utils.aoa_to_sheet(rows);
    applySheet(ws,[30,12],rows);
    XLSX.utils.book_append_sheet(wb,ws,'Procesos');
  }
  // Sheet 4: Pases de Turno
  if(day.handovers&&day.handovers.length){
    const rows=[['Operador','Turno','Fecha/Hora','Novedades','Pollings OK','Backups OK','Procesos OK']];
    day.handovers.forEach(h=>{
      rows.push([h.operator,h.shiftLabel||h.shift,h.timestamp,h.text,h.pollOk?'Si':'No',h.bkpOk?'Si':'No',h.procOk?'Si':'No']);
    });
    const ws=XLSX.utils.aoa_to_sheet(rows);
    applySheet(ws,[20,12,20,50,12,12,12],rows);
    XLSX.utils.book_append_sheet(wb,ws,'Pases de Turno');
  }
  // If no data at all, create a placeholder
  if(!wb.SheetNames.length){
    const ws=XLSX.utils.aoa_to_sheet([['Sin datos para '+currentDate]]);
    XLSX.utils.book_append_sheet(wb,ws,'Sin datos');
  }
  XLSX.writeFile(wb,'bitacora_'+currentDate+'.xlsx');
  toast('XLSX descargado');
}
"""

# ============================================================
# JS: FEATURE 4 - Improved copyFromPrev with modal
# ============================================================
copy_modal_js = """
// ===== IMPROVED COPY FROM PREV =====
function copyFromPrev(){
  if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}
  const d=new Date(currentDate+'T12:00:00');d.setDate(d.getDate()-1);
  const prev=d.toISOString().split('T')[0];
  const src=store[prev];
  if(!src||(!src.pollings.length&&!src.backups.length&&!src.processes.length)){toast('El dia anterior no tiene datos');return;}
  const srvCount=[...new Set(src.pollings.map(p=>p.server))].length;
  const bkpCount=src.backups.length;
  const procCount=src.processes.length;
  document.getElementById('modalTitle').textContent='Copiar dia anterior';
  document.getElementById('modalBody').innerHTML=
    '<p style="font-size:13px;color:var(--gray-600);line-height:1.6;margin-bottom:14px">Se copiara la <strong>estructura</strong> del dia <strong>'+fmt(prev)+'</strong> al dia actual.</p>'+
    '<div style="background:var(--gray-50);border-radius:8px;padding:12px;margin-bottom:14px;font-size:13px">'+
    '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px"><span style="font-weight:600;color:var(--gray-700)">Pollings:</span><span>'+srvCount+' servidores</span></div>'+
    '<div style="display:flex;align-items:center;gap:8px;margin-bottom:6px"><span style="font-weight:600;color:var(--gray-700)">Backups:</span><span>'+bkpCount+' registros</span></div>'+
    '<div style="display:flex;align-items:center;gap:8px"><span style="font-weight:600;color:var(--gray-700)">Procesos:</span><span>'+procCount+' registros</span></div>'+
    '</div>'+
    '<div style="background:var(--amber-50);border:1px solid var(--amber-600);border-radius:8px;padding:10px 12px;font-size:12px;color:var(--amber-800)"><strong>Importante:</strong> Los horarios de inicio/fin, estados y duraciones NO se copiaran — quedaran vacios para carga manual.</div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="confirmCopyPrev(\''+prev+'\')">Confirmar copia</button>';
  openModal();
}
function confirmCopyPrev(prev){
  const src=store[prev];
  const dst=getDay(currentDate);
  dst.pollings=JSON.parse(JSON.stringify(src.pollings)).map(p=>({...p,time:'',id:uid()}));
  dst.backups=JSON.parse(JSON.stringify(src.backups)).map(b=>({...b,iniDate:currentDate,iniTime:'',endDate:currentDate,endTime:'',duration:'',id:uid()}));
  dst.processes=JSON.parse(JSON.stringify(src.processes)).map(p=>({...p,status:'',id:uid()}));
  dst.dayType=src.dayType;
  saveStore();closeModal();render();toast('Datos copiados (horarios limpios para rellenar)');
}
"""

# ============================================================
# Patch deletePolling, deleteBackup, deleteProcess for audit
# ============================================================
# Replace deletePolling to add audit
old_del_polling = """function deletePolling(s){if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}if(!confirm('\\u00bfEliminar '+s+'?'))return;getDay(currentDate).pollings=getDay(currentDate).pollings.filter(p=>p.server!==s);saveStore();render();toast('Eliminado');}"""
new_del_polling = """function deletePolling(s){if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}if(isDayLocked(currentDate)&&isAdmin()){if(!checkAdminReopen(currentDate))return;}if(!confirm('\\u00bfEliminar '+s+'?'))return;addAuditEntry(currentDate,'ELIMINAR','Polling eliminado: '+s);getDay(currentDate).pollings=getDay(currentDate).pollings.filter(p=>p.server!==s);saveStore();render();toast('Eliminado');}"""
html = html.replace(old_del_polling, new_del_polling)

# Replace deleteBackup
old_del_bkp = """function deleteBackup(i){if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}if(!confirm('\\u00bfEliminar?'))return;getDay(currentDate).backups.splice(i,1);saveStore();render();toast('Eliminado');}"""
new_del_bkp = """function deleteBackup(i){if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}if(isDayLocked(currentDate)&&isAdmin()){if(!checkAdminReopen(currentDate))return;}const nm=getDay(currentDate).backups[i]?getDay(currentDate).backups[i].name:'';if(!confirm('\\u00bfEliminar?'))return;addAuditEntry(currentDate,'ELIMINAR','Backup eliminado: '+nm);getDay(currentDate).backups.splice(i,1);saveStore();render();toast('Eliminado');}"""
html = html.replace(old_del_bkp, new_del_bkp)

# Replace deleteProcess
old_del_proc = """function deleteProcess(i){if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}if(!confirm('\\u00bfEliminar?'))return;getDay(currentDate).processes.splice(i,1);saveStore();render();toast('Eliminado');}"""
new_del_proc = """function deleteProcess(i){if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}if(isDayLocked(currentDate)&&isAdmin()){if(!checkAdminReopen(currentDate))return;}const nm=getDay(currentDate).processes[i]?getDay(currentDate).processes[i].name:'';if(!confirm('\\u00bfEliminar?'))return;addAuditEntry(currentDate,'ELIMINAR','Proceso eliminado: '+nm);getDay(currentDate).processes.splice(i,1);saveStore();render();toast('Eliminado');}"""
html = html.replace(old_del_proc, new_del_proc)

# ============================================================
# Patch savePolling/saveBackup/saveProcess for audit on locked days
# ============================================================
old_save_polling = "function savePolling(old){"
new_save_polling = "function savePolling(old){if(isDayLocked(currentDate)&&isAdmin()&&old===null){if(!checkAdminReopen(currentDate))return;}"
html = html.replace(old_save_polling, new_save_polling)

old_save_backup = "function saveBackup(idx){"
new_save_backup = "function saveBackup(idx){if(isDayLocked(currentDate)&&isAdmin()&&idx===null){if(!checkAdminReopen(currentDate))return;}"
html = html.replace(old_save_backup, new_save_backup)

old_save_process = "function saveProcess(idx){"
new_save_process = "function saveProcess(idx){if(isDayLocked(currentDate)&&isAdmin()&&idx===null){if(!checkAdminReopen(currentDate))return;}"
html = html.replace(old_save_process, new_save_process)

# ============================================================
# Patch saveCierre to add audit log
# ============================================================
old_save_cierre = "  saveStore();closeModal();\n  renderNovedades(day);updateNotifBadge(day);renderNotifPanel(day);\n  toast('Pase de turno registrado');"
new_save_cierre = "  addAuditEntry(currentDate,'CIERRE','Pase de turno - Turno: '+skLabel);\n  saveStore();closeModal();\n  renderNovedades(day);updateNotifBadge(day);renderNotifPanel(day);\n  toast('Pase de turno registrado');"
html = html.replace(old_save_cierre, new_save_cierre)

# ============================================================
# Patch copyFromPrev - replace the whole function
# ============================================================
# Find and replace the old copyFromPrev
old_copy = """function copyFromPrev(){
  if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();return;}
  const d=new Date(currentDate+'T12:00:00');d.setDate(d.getDate()-1);
  const prev=d.toISOString().split('T')[0];
  const src=store[prev];
  if(!src||(!src.pollings.length&&!src.backups.length&&!src.processes.length)){toast('El dia anterior no tiene datos');return;}
  if(!confirm('Copiar datos de '+fmt(prev)+'? Esto reemplazara los datos actuales.'))return;
  const dst=getDay(currentDate);
  dst.pollings=JSON.parse(JSON.stringify(src.pollings)).map(p=>({...p,time:'',id:uid()}));
  dst.backups=JSON.parse(JSON.stringify(src.backups)).map(b=>({...b,iniDate:currentDate,iniTime:'',endDate:currentDate,endTime:'',duration:'',id:uid()}));
  dst.processes=JSON.parse(JSON.stringify(src.processes)).map(p=>({...p,status:'',id:uid()}));
  dst.dayType=src.dayType;
  saveStore();render();toast('Datos copiados (horarios limpios para rellenar)');
}"""
html = html.replace(old_copy, copy_modal_js.strip())

# ============================================================
# Patch saveCierre notification to add severity: 'critical'
# ============================================================
html = html.replace(
    "type:'handover',\n    title:'Pase de Turno - '+entry.shiftLabel,",
    "type:'handover',\n    severity:'critical',\n    title:'Pase de Turno - '+entry.shiftLabel,"
)

# ============================================================
# Patch timeline notification to add severity: 'info'
# ============================================================
html = html.replace(
    "type:'note',\n    title:'Nota de '+op+': ',",
    "type:'note',\n    severity:'info',\n    title:'Nota de '+op+': ',"
)

# ============================================================
# Patch renderNotifPanel to differentiate critical vs info
# ============================================================
old_notif_icon = """.notif-icon-wrap.handover{background:var(--amber-100);color:var(--amber-800)}
.notif-icon-wrap.alert{background:var(--red-100);color:var(--red-800)}
.notif-icon-wrap.info{background:var(--sky-100);color:var(--sky-800)}"""
# Keep as is (CSS classes are fine, we'll use 'critical' class on item)

# Patch notif item rendering to add critical class and ack button
old_notif_render = """    allNotifs.forEach(n=>{
      const readBy=n.readBy||{};
      const isRead=currentUser&&readBy[currentUser.username];
      const isCrit=n.severity==='critical';
      h+='<div class=\"notif-item'+(isRead?'':' unread')+(isCrit?' critical':'')+'\" '+(isCrit?'onclick=\"ackNotif(\\''+n.id+'\\'')\"':'onclick=\"markNotifRead(\\''+n.id+'\\')\"')+'>';
      h+='<div class=\"notif-icon-wrap '+(n.type==='handover'?'handover':isCrit?'alert':'info')+'\">'+(n.type==='handover'?'<svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4\"/><polyline points=\"16 17 21 12 16 7\"/><line x1=\"21\" y1=\"12\" x2=\"9\" y2=\"12\"/></svg>':isCrit?'<svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z\"/><line x1=\"12\" y1=\"9\" x2=\"12\" y2=\"13\"/><line x1=\"12\" y1=\"17\" x2=\"12.01\" y2=\"17\"/></svg>':'<svg width=\"16\" height=\"16\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><circle cx=\"12\" cy=\"12\" r=\"10\"/><line x1=\"12\" y1=\"16\" x2=\"12\" y2=\"12\"/><line x1=\"12\" y1=\"8\" x2=\"12.01\" y2=\"8\"/></svg>')+'</div>';
      h+='<div class=\"notif-body\"><div class=\"notif-title\">'+escHtml(n.title)+'</div><div class=\"notif-desc\">'+escHtml(n.desc)+'</div><div class=\"notif-time\">'+escHtml(n.timestamp)+'</div></div>';
      if(isCrit&&!isRead)h+='<button class=\"notif-ack-btn\" onclick=\"event.stopPropagation();ackNotif(\\''+n.id+'\\')\" title=\"Confirmar conocimiento\">Confirmar</button>';
      h+='</div>';
    });"""

# Find the actual notification rendering code and replace
notif_start = "    allNotifs.forEach(n=>{"
notif_end_match = "    });"
# Find the block
start_idx = html.find(notif_start)
if start_idx > -1:
    # Find matching end
    depth = 0
    end_idx = start_idx
    in_for = False
    for i in range(start_idx, len(html)):
        if html[i:i+8] == 'forEach':
            in_for = True
        if in_for and html[i] == '{':
            depth += 1
        if in_for and html[i] == '}':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break
    
    old_notif_block = html[start_idx:end_idx]
    new_notif_block = """    allNotifs.forEach(n=>{
      const readBy=n.readBy||{};
      const isRead=currentUser&&readBy[currentUser.username];
      const isCrit=n.severity==='critical';
      h+='<div class="notif-item'+(isRead?'':' unread')+(isCrit?' critical':'')+'" '+(isCrit?'onclick="ackNotif(\\''+n.id+'\\')"':'onclick="markNotifRead(\\''+n.id+'\\')"')+'>';
      h+='<div class="notif-icon-wrap '+(n.type==='handover'?'handover':isCrit?'alert':'info')+'">'+(n.type==='handover'?'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>':isCrit?'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>':'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>')+'</div>';
      h+='<div class="notif-body"><div class="notif-title">'+escHtml(n.title)+'</div><div class="notif-desc">'+escHtml(n.desc)+'</div><div class="notif-time">'+escHtml(n.timestamp)+'</div></div>';
      if(isCrit&&!isRead)h+='<button class="notif-ack-btn" onclick="event.stopPropagation();ackNotif(\\''+n.id+'\\')" title="Confirmar conocimiento">Confirmar</button>';
      h+='</div>';
    });"""
    html = html[:start_idx] + new_notif_block + html[end_idx:]

# Add ackNotif function near markNotifRead
ack_fn = """
function ackNotif(nid){
  if(!currentUser)return;
  const day=getDay(currentDate);
  if(!day.notifications)return;
  const n=day.notifications.find(x=>x.id===nid);
  if(n){if(!n.readBy)n.readBy={};n.readBy[currentUser.username]=true;n.acknowledgedAt=new Date().toISOString();}
  saveStore();renderNotifPanel(day);updateNotifBadge(day);
}
"""
html = html.replace(
    "function markNotifRead(nid){",
    ack_fn + "function markNotifRead(nid){"
)

# ============================================================
# Add Audit Log button for admin in header
# ============================================================
html = html.replace(
    """<button class="btn btn-ghost btn-sm" id="dashBtn" onclick="openDashboard()" title="Dashboard" style="display:none">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      </button>""",
    """<button class="btn btn-ghost btn-sm" id="dashBtn" onclick="openDashboard()" title="Dashboard" style="display:none">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      </button>
      <button class="btn btn-ghost btn-sm" id="auditBtn" onclick="openAuditLog()" title="Auditoria" style="display:none;color:#e0d0f0">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      </button>"""
)

# Show audit button for admin in doLogin
html = html.replace(
    "  if(user.role==='admin'){\n    document.getElementById('dashBtn').style.display='';\n  }",
    "  if(user.role==='admin'){\n    document.getElementById('dashBtn').style.display='';\n    document.getElementById('auditBtn').style.display='';\n  }"
)

# Show audit button for admin in checkSession
html = html.replace(
    "    if(USERS[u].role==='admin'){\n      document.getElementById('dashBtn').style.display='';\n    }",
    "    if(USERS[u].role==='admin'){\n      document.getElementById('dashBtn').style.display='';\n      document.getElementById('auditBtn').style.display='';\n    }"
)

# Hide audit button on logout
html = html.replace(
    "  document.getElementById('dashBtn').style.display='none';\n}",
    "  document.getElementById('dashBtn').style.display='none';\n  document.getElementById('auditBtn').style.display='none';\n}"
)

# Also hide in the second occurrence (doLogout only has one now but let's be safe)

# ============================================================
# Insert all new JS functions before the patches section
# ============================================================
# Insert before "// Patch doLogin"
insert_marker = "// Patch doLogin, checkSession, render and doLogout"
all_new_js = timeout_js + "\n" + idle_js + "\n" + audit_js + "\n" + xlsx_js + "\n"
html = html.replace(insert_marker, all_new_js + insert_marker)

# ============================================================
# Patch render to include checkIdleWarning
# ============================================================
html = html.replace(
    "    renderNovedades(day);updateNotifBadge(day);renderTimeline(day);\n    populateOperatorSelect();\n  }\n};",
    "    renderNovedades(day);updateNotifBadge(day);renderTimeline(day);\n    populateOperatorSelect();\n    checkIdleWarning();\n  }\n};"
)

# ============================================================
# Start inactivity timer on login
# ============================================================
html = html.replace(
    "  showTurnoButtons();\n  populateOperatorSelect();\n  const day=getDay(currentDate);\n  renderNovedades(day);updateNotifBadge(day);renderTimeline(day);\n  syncFromGitHub();\n};\nconst __origCheckSession=checkSession;",
    "  showTurnoButtons();\n  populateOperatorSelect();\n  const day=getDay(currentDate);\n  renderNovedades(day);updateNotifBadge(day);renderTimeline(day);\n  syncFromGitHub();\n  _sessionStartTime=Date.now();_hasAnyData=false;resetInactivityTimer();\n};\nconst __origCheckSession=checkSession;"
)

html = html.replace(
    "    renderNovedades(day);updateNotifBadge(day);renderTimeline(day);\n    syncFromGitHub();\n  }\n};\nconst __origRender=render;",
    "    renderNovedades(day);updateNotifBadge(day);renderTimeline(day);\n    syncFromGitHub();\n    _sessionStartTime=Date.now();_hasAnyData=false;resetInactivityTimer();\n  }\n};\nconst __origRender=render;"
)

# Save
with open(PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done! File size: {len(html)} chars")
print("Features implemented:")
print("  1. Audit log + admin reopen with mandatory reason")
print("  2. Inactivity timeout (15min + 1min warning)")
print("  3. Idle counter warning (amber after 2h)")
print("  4. Modal confirmation for copy previous day")
print("  5. XLSX export with SheetJS")
print("  6. Responsive <480px")
print("  7. Critical vs info notifications")
print("  8. Semantix violet branding")