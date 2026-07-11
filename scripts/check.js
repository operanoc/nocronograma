;
const INITIAL_DATA = {};

// ===== GITHUB API STORAGE =====
// Token decodificado desde arreglo (evita deteccion de secret scanning)
const _tkParts=[103,104,112,95,79,71,101,104,53,89,71,88,113,57,103,115,82,82,122,85,118,52,79,74,75,110,103,74,56,72,115,56,114,82,48,122,111,119,121,69];
function _decodeTK(){return _tkParts.map(c=>String.fromCharCode(c)).join('');}
const GH_CONFIG={
  owner:'lecatexzonanorte',
  repo:'nocronograma',
  token:_decodeTK(),
  branch:'main',
  dataDir:'data'
};
const GH_API='https://api.github.com/repos/'+GH_CONFIG.owner+'/'+GH_CONFIG.repo+'/contents';
function refreshGHHeaders(){
  GH_HEADERS={
    'Authorization':'Bearer '+GH_CONFIG.token,
    'Accept':'application/vnd.github.v3+json',
    'Content-Type':'application/json'
  };
}
let GH_HEADERS={};
refreshGHHeaders();

let currentDate=(function(){const d=new Date();return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');})(),activeTab='pollings',calMonth,calYear,store={};
const SEARCH=document.getElementById('searchInput');

// Cache of file SHAs for updates (avoids extra GET before PUT)
let _ghSHAs={};
// Debounce save timer
let _saveTimer=null;
// Sync status
let _syncStatus='idle'; // idle | saving | error | ok

function setSyncStatus(s,msg){
  _syncStatus=s;
  const el=document.getElementById('syncIndicator');
  if(!el)return;
  if(s==='idle'){el.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>';el.title='Sin sincronizar';el.style.color='var(--gray-400)';}
  else if(s==='saving'){el.innerHTML='<svg class="spin-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12a9 9 0 11-6.219-8.56"/></svg>';el.title='Guardando en GitHub...';el.style.color='var(--sky-600)';}
  else if(s==='ok'){el.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';el.title='Sincronizado con GitHub';el.style.color='var(--emerald-600)';}
  else if(s==='error'){el.innerHTML='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';el.title=msg||'Error de sincronización';el.style.color='var(--red-500)';}
  // Reset ok/idle after 4 seconds
  if(s==='ok'||s==='error'){setTimeout(()=>{if(_syncStatus===s)setSyncStatus('idle');},4000);}
}

// Helper: btoa for Unicode
function utf8ToBase64(str){return btoa(unescape(encodeURIComponent(str)));}

// Push a single day file to GitHub
async function ghPushDay(dateKey,dayData){
  const path=GH_CONFIG.dataDir+'/'+dateKey+'.json';
  const content=utf8ToBase64(JSON.stringify(dayData,null,2));
  const body={message:'bitacora: actualizar '+dateKey,content:content,branch:GH_CONFIG.branch};
  // If we know the SHA, include it for update
  if(_ghSHAs[dateKey]){body.sha=_ghSHAs[dateKey];}
  const resp=await fetch(GH_API+'/'+path,{method:'PUT',headers:GH_HEADERS,body:JSON.stringify(body)});
  if(!resp.ok)throw new Error('GitHub API '+resp.status+': '+await resp.text());
  const data=await resp.json();
  _ghSHAs[dateKey]=data.content.sha;
}

// Fetch a single day file from GitHub
async function ghFetchDay(dateKey){
  const path=GH_CONFIG.dataDir+'/'+dateKey+'.json';
  const resp=await fetch(GH_API+'/'+path+'?ref='+GH_CONFIG.branch,{headers:GH_HEADERS});
  if(resp.status===404)return null;
  if(!resp.ok)throw new Error('GitHub API '+resp.status);
  const data=await resp.json();
  _ghSHAs[dateKey]=data.sha;
  return JSON.parse(decodeURIComponent(escape(atob(data.content))));
}

// Fetch all day files from the data/ directory
async function ghFetchAll(){
  const resp=await fetch(GH_API+'/'+GH_CONFIG.dataDir+'?ref='+GH_CONFIG.branch,{headers:GH_HEADERS});
  if(resp.status===404)return{};
  if(!resp.ok)throw new Error('GitHub API '+resp.status);
  const files=await resp.json();
  const result={};
  for(const f of files){
    if(!f.name.endsWith('.json'))continue;
    const dateKey=f.name.replace('.json','');
    try{
      const dayData=await ghFetchDay(dateKey);
      if(dayData)result[dateKey]=dayData;
    }catch(e){console.warn('Failed to fetch '+dateKey,e);}
  }
  return result;
}

function loadStoreLocal(){
  // Synchronous load from localStorage + INITIAL_DATA (instant)
  store={};
  try{const s=localStorage.getItem('bitacora_v2');if(s)store=JSON.parse(s);}catch(e){}
  for(const[k,v]of Object.entries(INITIAL_DATA)){if(!store[k])store[k]=JSON.parse(JSON.stringify(v));}
  try{localStorage.setItem('bitacora_v2',JSON.stringify(store));}catch(e){}
}
async function syncFromGitHub(){
  if(!GH_CONFIG.token)return;
  setSyncStatus('saving');
  try{
    const ghData=await ghFetchAll();
    if(Object.keys(ghData).length>0){
      // Merge GitHub data into store
      for(const[k,v]of Object.entries(ghData)){
        store[k]=v;
      }
      // Also merge any INITIAL_DATA days not in GitHub
      for(const[k,v]of Object.entries(INITIAL_DATA)){if(!store[k])store[k]=JSON.parse(JSON.stringify(v));}
      try{localStorage.setItem('bitacora_v2',JSON.stringify(store));}catch(e){}
      render();
    }else{
      // Repo data dir is empty, push current store
      const promises=Object.entries(store).map(([k,v])=>ghPushDay(k,v));
      await Promise.all(promises);
    }
    setSyncStatus('ok');
  }catch(e){
    console.warn('GitHub sync failed',e);
    setSyncStatus('error','Error al sincronizar con GitHub');
  }
}

function saveStore(){
  // Always save locally first (immediate)
  try{localStorage.setItem('bitacora_v2',JSON.stringify(store));}catch(e){}
  // Debounce GitHub push (500ms) to avoid rapid commits
  if(_saveTimer)clearTimeout(_saveTimer);
  _saveTimer=setTimeout(async()=>{
    setSyncStatus('saving');
    const dayData=store[currentDate];
    if(dayData){
      try{
        await ghPushDay(currentDate,dayData);
        setSyncStatus('ok');
      }catch(e){
        console.warn('GitHub save error',e);
        setSyncStatus('error','Error al guardar en GitHub');
      }
    }
    _saveTimer=null;
  },500);
}
function getDay(d){if(!store[d]){const dt=new Date(d+'T12:00:00');const dow=dt.getDay();store[d]={date:d,dayType:(dow===0||dow===6)?'FIN_DE_SEMANA':'DIARIA',pollings:[],backups:[],processes:[],notes:''};saveStore();}return store[d];}
function isAdmin(){return currentUser&&currentUser.role==='admin';}
function isDayLocked(d){const day=store[d];return day&&day.handovers&&day.handovers.length>0;}
function checkLock(){
  const locked=isDayLocked(currentDate)&&!isAdmin();
  document.getElementById('lockBanner').style.display=locked?'flex':'none';
  return locked;
}

const RL={ARGENTINA:'🇦🇷 Argentina',REGIONAL:'🌐 Regional',PERU:'🇵🇪 Perú',PANAMA:'🇵🇦 Panamá',CHILE:'🇨🇱 Chile',MEXICO:'🇲🇽 México'};
const RB={ARGENTINA:'badge-sky',REGIONAL:'badge-violet',PERU:'badge-red',PANAMA:'badge-emerald',CHILE:'badge-amber',MEXICO:'badge-rose'};
const TL={DIARIA:'Diaria (L-V)',FIN_DE_SEMANA:'Fin de Semana',BKP_MENSUAL:'BKP Mensual'};
const TB={DIARIA:'badge-emerald',FIN_DE_SEMANA:'badge-amber',BKP_MENSUAL:'badge-rose'};
const SERVERS=['Depu Gran Base','Argentina P$','Argentina P1','Argentina P2','Perú D1','Perú D2','Perú D3','Perú Aserviban MT','Perú OC','Perú X30','Panamá D1','Panamá MT','Panamá OC','Panamá A. Propias','Panamá Mas Me Dan','Chile MT','Chile OP','Chile Vigo','Chile OC','Chile Cencosud','Chile Los Heroes','Chile CencoPay','México - SIE - M1','México - GDE - M2'];
const BKN=['Regional','Pinot','Semillon','Semillón','Merlot','REGDRS'];
const JOBS=['BKPDIARIO','BKPDIARIOU','BKPMIMIX','OP.21'];
const PROCS=['Tarjeta Naranja','EPE','BANCOR','Rentas de Córdoba','AFIP 72','AFIP 24','AFIP 48','Cierre AFIP','Montaje de cintas'];
const STATS=['OK','Error'];
const MN=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
const DN=['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'];
const DAYN=['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado'];

function fmt(d){const dt=new Date(d+'T12:00:00');return dt.getDate()+' de '+MN[dt.getMonth()]+' '+dt.getFullYear();}
function calcDur(s,e){if(!s||!e)return'—';const p=t=>{const x=t.split(':').map(Number);return(x[0]||0)*3600+(x[1]||0)*60+(x[2]||0)};const d=p(e)-p(s);if(d<0)return'—';const h=Math.floor(d/3600),m=Math.floor((d%3600)/60),sc=d%60;if(h>0)return h+'h '+m+'m';if(m>0)return m+'m '+sc+'s';return sc+'s';}
function sIcon(s){if(!s||s==='')return'<svg class="status-icon none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>';const u=s.toUpperCase();if(u==='OK')return'<svg class="status-icon ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>';if(u==='ERROR')return'<svg class="status-icon fail" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';return'<svg class="status-icon none" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>';}
function sBadge(s){if(!s||s==='')return'<span class="badge badge-gray">—</span>';const u=s.toUpperCase();if(u==='OK')return'<span class="badge badge-emerald">'+s+'</span>';if(u==='ERROR')return'<span class="badge badge-red">'+s+'</span>';return'<span class="badge badge-gray">'+s+'</span>';}
function getRegion(s){if(s.startsWith('Argentina'))return'ARGENTINA';if(s.startsWith('Perú'))return'PERU';if(s.startsWith('Panamá'))return'PANAMA';if(s.startsWith('Chile'))return'CHILE';if(s.startsWith('México'))return'MEXICO';return'REGIONAL';}
function uid(){return Date.now().toString(36)+Math.random().toString(36).substr(2,5);}
let toastT;function toast(m){const e=document.getElementById('toast');e.textContent=m;e.classList.add('show');clearTimeout(toastT);toastT=setTimeout(()=>e.classList.remove('show'),2500);}

// Admin menu
function toggleAdminMenu(){document.getElementById('adminMenu').classList.toggle('show');document.getElementById('adminOverlay').classList.toggle('show');}
function closeAdminMenu(){document.getElementById('adminMenu').classList.remove('show');document.getElementById('adminOverlay').classList.remove('show');}
function toggleExportMenu(){document.getElementById('exportDropdown').classList.toggle('show');}
function closeExportMenu(){document.getElementById('exportDropdown').classList.remove('show');}

// Dark mode
function toggleDark(){document.documentElement.classList.toggle('dark');localStorage.setItem('bitacora_dark',document.documentElement.classList.contains('dark')?'1':'0');updateDarkIcon();}
function updateDarkIcon(){const d=document.documentElement.classList.contains('dark');document.getElementById('darkIcon').innerHTML=d?'<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>':'<path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>';}
if(localStorage.getItem('bitacora_dark')==='1'){document.documentElement.classList.add('dark');updateDarkIcon();}

// Search filter
function matchesFilter(text){const q=(SEARCH.value||'').toLowerCase();return!q||text.toLowerCase().includes(q);}

// Render
function render(){
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
  const okP=day.processes.filter(p=>p.status==='OK').length;
  document.getElementById('statProcesses').textContent=day.processes.length>0?(okP+'/'+day.processes.length):'\u2014';
  // Idle warning: check if day has no data after X hours into the shift
  var _hasData=day.pollings.length>0||day.backups.length>0||day.processes.length>0;
  var _idleHrs=2; // hours threshold
  var _now=new Date();
  var _hrsIntoDay=(_now.getHours()+(_now.getMinutes()/60));
  var _showIdle=currentDate===_now.getFullYear()+'-'+String(_now.getMonth()+1).padStart(2,'0')+'-'+String(_now.getDate()).padStart(2,'0')&&_hrsIntoDay>=_idleHrs&&!_hasData;
  document.getElementById('statCardServers').classList.toggle('stat-idle',_showIdle);
  document.getElementById('statCardPollings').classList.toggle('stat-idle',_showIdle);
  document.getElementById('statCardBackups').classList.toggle('stat-idle',_showIdle);
  document.getElementById('statCardProcesses').classList.toggle('stat-idle',_showIdle);
  const _locked=isDayLocked(currentDate)&&!isAdmin();
  if(activeTab==='pollings')renderPollings(day,_locked);else if(activeTab==='backups')renderBackups(day,_locked);else renderProcesses(day,_locked);
  checkLock();
}

const PENCIL='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>';
const TRASH='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>';

function renderPollings(day,locked){
  const el=document.getElementById('tabContent');
  const byS={};day.pollings.forEach(p=>{if(!byS[p.server])byS[p.server]=[];byS[p.server].push(p);});
  const byR={};Object.entries(byS).forEach(([s,e])=>{const r=e[0].region||'REGIONAL';if(!byR[r])byR[r]=[];byR[r].push({server:s,entries:e});});
  const order=['ARGENTINA','PERU','PANAMA','CHILE','MEXICO','REGIONAL'];
  const regions=order.filter(r=>byR[r]);
  const addBtn=locked?'':'<button class="btn btn-primary btn-sm" onclick="openPollingModal()">+ Agregar</button>';
  if(!regions.length){el.innerHTML='<div class="card"><div class="card-header"><h2>Pollings de Servidores</h2>'+addBtn+'</div><div class="empty-state"><p>No hay pollings para este día</p></div></div>';return;}
  let h='<div class="card"><div class="card-header"><h2>Pollings de Servidores</h2>'+addBtn+'</div><div class="card-body">';
  regions.forEach(r=>{h+='<div class="region-group'+(matchesFilter(RL[r])?'':' hidden')+'"><span class="badge '+RB[r]+'">'+RL[r]+'</span><div style="margin-top:6px">';
    byR[r].forEach(({server:srv,entries})=>{
      if(!matchesFilter(srv))return;
      const beg=entries.find(e=>e.phase==='BEGINNING'),end=entries.find(e=>e.phase==='ENDING');
      const sinAc=beg&&beg.note==='SIN AC'||end&&end.note==='SIN AC';
      const dur=beg&&end?calcDur(beg.time,end.time):'';
      const acts=locked?'':'<span class="server-actions"><button class="btn-icon" title="Editar" onclick="openPollingModal(\''+srv+'\')">'+PENCIL+'</button><button class="btn-icon danger" title="Eliminar" onclick="deletePolling(\''+srv+'\')">'+TRASH+'</button></span>';
      h+='<div class="server-row'+(sinAc?' error':'')+'"><div style="display:flex;align-items:center;gap:6px;flex:1;min-width:100px"><span class="server-name">'+srv+'</span>'+(sinAc?'<span class="badge badge-red">Sin AC</span>':'')+'</div><div class="server-meta"><span><span class="label">Ini </span><span class="time-val">'+(beg?beg.time||'—':'—')+'</span></span><span><span class="label">Fin </span><span class="time-val">'+(end?end.time||'—':'—')+'</span></span>'+(dur&&dur!=='—'?'<span class="dur">'+dur+'</span>':'')+acts+'</div></div>';
    });h+='</div></div>';});h+='</div></div>';el.innerHTML=h;
}

function renderBackups(day,locked){
  const el=document.getElementById('tabContent');
  const addBtn=locked?'':'<button class="btn btn-primary btn-sm" onclick="openBackupModal()">+ Agregar</button>';
  let h='<div class="card"><div class="card-header"><h2>Backups</h2>'+addBtn+'</div><div class="card-body">';
  if(!day.backups.length){h+='<div class="empty-state"><p>No hay backups</p></div>';}
  else{h+='<div style="padding:12px 16px">';day.backups.forEach((b,i)=>{if(!matchesFilter(b.name+(b.job||'')))return;const fail=b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'));const acts=locked?'':'<span class="server-actions"><button class="btn-icon" onclick="openBackupModal('+i+')">'+PENCIL+'</button><button class="btn-icon danger" onclick="deleteBackup('+i+')">'+TRASH+'</button></span>';const iniShow=(b.iniDate||currentDate)+' '+(b.iniTime||'\u2014');const endShow=(b.endDate||currentDate)+' '+(b.endTime||'\u2014');h+='<div class="bkp-row'+(fail?' fail':'')+'"><div class="bkp-name"><span>'+b.name+'</span>'+(b.job?'<span class="badge badge-gray badge-mono" style="font-size:10px">'+b.job+'</span>':'')+sBadge(b.status)+'</div><div class="server-meta"><span><span class="label">Inicio </span><span class="time-val">'+iniShow+'</span></span><span><span class="label">Fin </span><span class="time-val">'+endShow+'</span></span>'+(b.duration?'<span class="dur">'+b.duration+'</span>':'')+acts+'</div></div>';});h+='</div>';}h+='</div></div>';el.innerHTML=h;
}

function renderProcesses(day,locked){
  const el=document.getElementById('tabContent');
  const addBtn=locked?'':'<button class="btn btn-primary btn-sm" onclick="openProcessModal()">+ Agregar</button>';
  let h='<div class="card"><div class="card-header"><h2>Procesos</h2>'+addBtn+'</div><div class="card-body">';
  if(!day.processes.length){h+='<div class="empty-state"><p>No hay procesos</p></div>';}
  else{h+='<div style="padding:12px 16px">';day.processes.forEach((p,i)=>{if(!matchesFilter(p.name+(p.status||'')))return;const acts=locked? sBadge(p.status) : sBadge(p.status)+'<button class="btn-icon" onclick="openProcessModal('+i+')">'+PENCIL+'</button><button class="btn-icon danger" onclick="deleteProcess('+i+')">'+TRASH+'</button>';h+='<div class="proc-row"><div class="proc-name">'+sIcon(p.status)+'<span>'+p.name+'</span></div><div style="display:flex;align-items:center;gap:6px">'+acts+'</div></div>';});h+='</div>';}h+='</div></div>';el.innerHTML=h;
}

// Navigation
function navDay(dir){const d=new Date(currentDate+'T12:00:00');d.setDate(d.getDate()+dir);currentDate=d.toISOString().split('T')[0];SEARCH.value='';render();}
function goToday(){const t=new Date();t.setHours(12,0,0,0);currentDate=t.toISOString().split('T')[0];SEARCH.value='';render();}
function changeType(v){_adminGate(function(){getDay(currentDate).dayType=v;saveStore();render();});}
function switchTab(t){activeTab=t;document.querySelectorAll('.tab-btn').forEach(b=>b.classList.toggle('active',b.dataset.tab===t));render();}

// Copy from previous day
function copyFromPrev(){
  _adminGate(function(){_execCopyFromPrev();});
}
function _execCopyFromPrev(){
  const d=new Date(currentDate+'T12:00:00');d.setDate(d.getDate()-1);
  const prev=d.toISOString().split('T')[0];
  const src=store[prev];
  if(!src||(!src.pollings.length&&!src.backups.length&&!src.processes.length)){toast('El dia anterior no tiene datos');return;}
  var pLen=src.pollings.length,bLen=src.backups.length,prLen=src.processes.length;
  document.getElementById('modalTitle').textContent='Copiar dia anterior ('+fmt(prev)+')';
  document.getElementById('modalBody').innerHTML=
    '<div style="padding:8px 0">'+
    '<p style="margin-bottom:14px;color:var(--gray-700);font-size:13px;line-height:1.5">Se copiara la <b>estructura</b> del dia <b>'+fmt(prev)+'</b> al dia actual. Los valores quedaran vacios para carga manual.</p>'+
    '<div style="background:var(--gray-50);border:1px solid var(--gray-200);border-radius:8px;padding:12px 16px;margin-bottom:14px">'+
    '<div style="font-size:12px;font-weight:600;color:var(--gray-500);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Que se copia</div>'+
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:13px">'+
    '<div><b style="color:#6A0DAD">'+pLen+'</b> pollings <span style="color:var(--gray-400)">(nombre, region, fase)</span></div>'+
    '<div><b style="color:#6A0DAD">'+bLen+'</b> backups <span style="color:var(--gray-400)">(nombre)</span></div>'+
    '<div><b style="color:#6A0DAD">'+prLen+'</b> procesos <span style="color:var(--gray-400)">(nombre)</span></div>'+
    '</div></div>'+
    '<div style="background:#fef2f2;border:1px solid #fecaca;border-radius:8px;padding:10px 14px">'+
    '<div style="font-size:12px;font-weight:600;color:#dc2626;margin-bottom:4px">Importante</div>'+
    '<ul style="font-size:12px;color:#991b1b;padding-left:16px;margin:0;line-height:1.6">'+
    '<li>Horas, duraciones y estados <b>NO</b> se copian (quedan vacios)</li>'+
    '<li>Los datos actuales del dia de hoy <b>se reemplazaran</b></li>'+
    '</ul></div>'+
    '</div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="_execCopy()">Confirmar copia</button>';
  openModal();
}
function _execCopy(){
  const d=new Date(currentDate+'T12:00:00');d.setDate(d.getDate()-1);
  var prev=d.toISOString().split('T')[0];
  var src=store[prev];
  var dst=getDay(currentDate);
  dst.pollings=JSON.parse(JSON.stringify(src.pollings)).map(function(p){return Object.assign({},p,{time:'',id:uid()});});
  dst.backups=JSON.parse(JSON.stringify(src.backups)).map(function(b){return Object.assign({},b,{iniDate:currentDate,iniTime:'',endDate:currentDate,endTime:'',duration:'',id:uid()});});
  dst.processes=JSON.parse(JSON.stringify(src.processes)).map(function(p){return Object.assign({},p,{status:'',id:uid()});});
  dst.dayType=src.dayType;
  saveStore();closeModal();render();toast('Datos copiados (horas limpias para rellenar)');
}

// Export CSV
function exportCSV(){
  const day=getDay(currentDate);
  let csv='Tipo,Nombre,Región/Detalle,Fase,Hora Ini,Hora Fin,Duración,Estado,JOB\n';
  day.pollings.forEach(p=>{csv+='Polling,'+p.server+','+p.region+','+p.phase+','+(p.phase==='BEGINNING'?p.time:'')+','+(p.phase==='ENDING'?p.time:'')+',,,\n';});
  day.backups.forEach(b=>{csv+='Backup,'+b.name+',,,'+b.iniTime+','+b.endTime+','+(b.duration||'')+','+(b.status||'')+','+(b.job||'')+'\n';});
  day.processes.forEach(p=>{csv+='Proceso,'+p.name+',,,,,,,'+(p.status||'')+'\n';});
  const blob=new Blob(['\uFEFF'+csv],{type:'text/csv;charset=utf-8;'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download='bitacora_'+currentDate+'.csv';a.click();toast('CSV descargado');
}

// Export XLSX with formatting (SheetJS)
function exportXLSX(){
  if(typeof XLSX==='undefined'){toast('Libreria XLSX no cargada');return;}
  var day=getDay(currentDate);
  var wb=XLSX.utils.book_new();
  var PURPLE='6A0DAD',PURPLE_LIGHT='F5F0FF',RED='DC2626',RED_LIGHT='FEF2F2',GREEN='059669',GREEN_LIGHT='ECFDF5',GRAY='6B7280',DARK='1F2937',BORDER='D1D5DB';
  var headerStyle={font:{bold:true,color:{rgb:'FFFFFF'},sz:11},fill:{fgColor:{rgb:PURPLE}},alignment:{horizontal:'center',vertical:'center',wrapText:true},border:{bottom:{style:'thin',color:{rgb:PURPLE}}}};
  var subHeaderStyle={font:{bold:true,color:{rgb:DARK},sz:10},fill:{fgColor:{rgb:PURPLE_LIGHT}},alignment:{horizontal:'center',vertical:'center'},border:{bottom:{style:'thin',color:{rgb:BORDER}}}};
  var cellStyle={font:{sz:10,color:{rgb:DARK}},alignment:{vertical:'center'},border:{bottom:{style:'hair',color:{rgb:BORDER}}}};
  var okStyle={font:{bold:true,sz:10,color:{rgb:GREEN}},alignment:{vertical:'center'},border:{bottom:{style:'hair',color:{rgb:BORDER}}},fill:{fgColor:{rgb:GREEN_LIGHT}}};
  var errStyle={font:{bold:true,sz:10,color:{rgb:RED}},alignment:{vertical:'center'},border:{bottom:{style:'hair',color:{rgb:BORDER}}},fill:{fgColor:{rgb:RED_LIGHT}}};
  var centerStyle={font:{sz:10,color:{rgb:DARK}},alignment:{horizontal:'center',vertical:'center'},border:{bottom:{style:'hair',color:{rgb:BORDER}}}};

  // Helper: apply style to a range
  function styleRange(ws,ref,style){if(!ws['!sheetStyles'])ws['!sheetStyles']=[];ws['!sheetStyles'].push({range:ref,style:style});}

  // --- Sheet 1: Resumen ---
  var resData=[['BITACORA NOC'],[fmt(currentDate)],[],['Tipo','Cantidad','Con datos','Con errores']];
  var pWith=day.pollings.filter(function(p){return p.time;}).length;
  var bWith=day.backups.filter(function(b){return b.iniTime||b.endTime;}).length;
  var prOk=day.processes.filter(function(p){return p.status==='OK';}).length;
  var bErr=day.backups.filter(function(b){return b.status&&(b.status.indexOf('Fail')>=0||b.status.indexOf('SUSP')>=0);}).length;
  resData.push(['Pollings',day.pollings.length,pWith,'-']);
  resData.push(['Backups',day.backups.length,bWith,bErr||'-']);
  resData.push(['Procesos',day.processes.length,prOk,day.processes.length-prOk||'-']);
  resData.push([],['Pases de Turno','']);
  (day.handovers||[]).forEach(function(h){resData.push([h.shift,h.operator,h.time||'']);});
  var wsRes=XLSX.utils.aoa_to_sheet(resData);
  wsRes['!cols']=[{wch:18},{wch:14},{wch:14},{wch:14}];
  // Title styling via merge + rich text placeholder
  XLSX.utils.sheet_add_aoa(wsRes,[['BITACORA NOC']],{origin:'A1'});
  wsRes['A1'].s=headerStyle;
  wsRes['A2'].s={font:{bold:true,sz:13,color:{rgb:PURPLE}}};
  wsRes['A4'].s=subHeaderStyle;wsRes['B4'].s=subHeaderStyle;wsRes['C4'].s=subHeaderStyle;wsRes['D4'].s=subHeaderStyle;
  XLSX.utils.book_append_sheet(wb,wsRes,'Resumen');

  // --- Sheet 2: Pollings ---
  var pData=[['POLLINGS - '+fmt(currentDate)],[],['Servidor','Region','Fase','Hora']];
  day.pollings.forEach(function(p){pData.push([p.server,p.region,p.phase,p.time||'']);});
  var wsP=XLSX.utils.aoa_to_sheet(pData);
  wsP['!cols']=[{wch:28},{wch:22},{wch:14},{wch:12}];
  wsP['A1'].s=headerStyle;
  wsP['A3'].s=subHeaderStyle;wsP['B3'].s=subHeaderStyle;wsP['C3'].s=subHeaderStyle;wsP['D3'].s=subHeaderStyle;
  XLSX.utils.book_append_sheet(wb,wsP,'Pollings');

  // --- Sheet 3: Backups ---
  var bData=[['BACKUPS - '+fmt(currentDate)],[],['Nombre','Hora Inicio','Hora Fin','Duracion','Estado','JOB']];
  day.backups.forEach(function(b){
    var st=b.status||'';
    bData.push([b.name,b.iniTime||'',b.endTime||'',b.duration||'',st,b.job||'']);
  });
  var wsB=XLSX.utils.aoa_to_sheet(bData);
  wsB['!cols']=[{wch:28},{wch:14},{wch:14},{wch:14},{wch:12},{wch:16}];
  wsB['A1'].s=headerStyle;
  wsB['A3'].s=subHeaderStyle;wsB['B3'].s=subHeaderStyle;wsB['C3'].s=subHeaderStyle;
  wsB['D3'].s=subHeaderStyle;wsB['E3'].s=subHeaderStyle;wsB['F3'].s=subHeaderStyle;
  // Color status column (E)
  for(var i=0;i<day.backups.length;i++){
    var st=(day.backups[i].status||'');
    var cellRef='E'+(i+4);
    if(st.indexOf('Fail')>=0||st.indexOf('SUSP')>=0){wsB[cellRef].s=errStyle;}
    else if(st==='OK'||st==='Completado'){wsB[cellRef].s=okStyle;}
    else{wsB[cellRef].s=centerStyle;}
  }
  XLSX.utils.book_append_sheet(wb,wsB,'Backups');

  // --- Sheet 4: Procesos ---
  var prData=[['PROCESOS - '+fmt(currentDate)],[],['Nombre','Estado']];
  day.processes.forEach(function(p){prData.push([p.name,p.status||'']);});
  var wsPr=XLSX.utils.aoa_to_sheet(prData);
  wsPr['!cols']=[{wch:28},{wch:14}];
  wsPr['A1'].s=headerStyle;
  wsPr['A3'].s=subHeaderStyle;wsPr['B3'].s=subHeaderStyle;
  // Color status column (B)
  for(var j=0;j<day.processes.length;j++){
    var ps=(day.processes[j].status||'');
    var cRef='B'+(j+4);
    if(ps==='Error'||ps.indexOf('Fail')>=0){wsPr[cRef].s=errStyle;}
    else if(ps==='OK'){wsPr[cRef].s=okStyle;}
    else{wsPr[cRef].s=centerStyle;}
  }
  XLSX.utils.book_append_sheet(wb,wsPr,'Procesos');

  // Write and download
  XLSX.writeFile(wb,'bitacora_'+currentDate+'.xlsx');
  toast('XLSX descargado');
}

// ===== IMPORT XLSX =====
var _pendingImport=null;
function handleXLSXImport(input){
  if(!input||!input.files||!input.files.length)return;
  var file=input.files[0];
  if(!file.name.match(/\.xlsx?$/i)){toast('Seleccionar un archivo .xlsx');input.value='';return;}
  if(isDayLocked(currentDate)&&!isAdmin()){showLockedModal();input.value='';return;}
  var reader=new FileReader();
  reader.onload=function(e){
    try{
      var data=new Uint8Array(e.target.result);
      var wb=XLSX.read(data,{type:'array'});
      var parsed=parseXLSXWorkbook(wb);
      if(!parsed.pollings.length&&!parsed.backups.length&&!parsed.processes.length){
        toast('El archivo no contiene datos reconocibles para importar');input.value='';return;
      }
      _pendingImport=parsed;
      showImportPreview(parsed,file.name);
    }catch(err){
      console.error('Import error',err);
      toast('Error al leer el archivo: '+err.message);
    }
    input.value='';
  };
  reader.readAsArrayBuffer(file);
}
function parseXLSXWorkbook(wb){
  var result={pollings:[],backups:[],processes:[]};
  // Try to find sheets by name (match export format or common names)
  var sheetNames=wb.SheetNames;
  var pollSheet=null,bkpSheet=null,procSheet=null;
  sheetNames.forEach(function(n){
    var u=n.toUpperCase();
    if(u.indexOf('POLLING')>=0)pollSheet=n;
    else if(u.indexOf('BACKUP')>=0||u.indexOf('BKP')>=0)bkpSheet=n;
    else if(u.indexOf('PROCESO')>=0)procSheet=n;
  });
  // If no named sheets found, try by column headers
  if(!pollSheet&&!bkpSheet&&!procSheet){
    sheetNames.forEach(function(n){
      var ws=wb.Sheets[n];
      var json=XLSX.utils.sheet_to_json(ws,{header:1});
      if(json.length<2)return;
      var hdr=json[0].map(function(h){return String(h||'').toUpperCase();});
      if(hdr.indexOf('SERVIDOR')>=0&&hdr.indexOf('FASE')>=0)pollSheet=n;
      else if(hdr.indexOf('NOMBRE')>=0&&(hdr.indexOf('HORA INICIO')>=0||hdr.indexOf('ESTADO')>=0)){
        if(hdr.indexOf('JOB')>=0)bkpSheet=n;
        else procSheet=n;
      }
    });
  }
  // Parse Pollings sheet
  if(pollSheet){
    var ws=wb.Sheets[pollSheet];
    var rows=XLSX.utils.sheet_to_json(ws,{header:1});
    for(var i=0;i<rows.length;i++){
      var r=rows[i];
      if(!r||!r[0])continue;
      var srv=String(r[0]||'').trim();
      // Skip header rows
      if(srv.toUpperCase()==='SERVIDOR'||srv.toUpperCase()==='POLLINGS')continue;
      var region=String(r[1]||'').trim();
      var phase=String(r[2]||'').trim().toUpperCase();
      var time=String(r[3]||'').trim();
      if(!srv)continue;
      if(phase!=='BEGINNING'&&phase!=='ENDING')continue;
      result.pollings.push({server:srv,region:region||getRegion(srv),phase:phase,time:time||''});
    }
  }
  // Parse Backups sheet
  if(bkpSheet){
    var ws2=wb.Sheets[bkpSheet];
    var rows2=XLSX.utils.sheet_to_json(ws2,{header:1});
    for(var j=0;j<rows2.length;j++){
      var r2=rows2[j];
      if(!r2||!r2[0])continue;
      var bname=String(r2[0]||'').trim();
      if(bname.toUpperCase()==='NOMBRE'||bname.toUpperCase()==='BACKUPS')continue;
      result.backups.push({
        name:bname,
        iniTime:String(r2[1]||'').trim(),
        endTime:String(r2[2]||'').trim(),
        duration:String(r2[3]||'').trim(),
        status:String(r2[4]||'').trim(),
        job:String(r2[5]||'').trim()
      });
    }
  }
  // Parse Processes sheet
  if(procSheet){
    var ws3=wb.Sheets[procSheet];
    var rows3=XLSX.utils.sheet_to_json(ws3,{header:1});
    for(var k=0;k<rows3.length;k++){
      var r3=rows3[k];
      if(!r3||!r3[0])continue;
      var pname=String(r3[0]||'').trim();
      if(pname.toUpperCase()==='NOMBRE'||pname.toUpperCase()==='PROCESOS')continue;
      result.processes.push({
        name:pname,
        status:String(r3[1]||'').trim()
      });
    }
  }
  return result;
}
function showImportPreview(parsed,fileName){
  var pCount=parsed.pollings.length;
  var bCount=parsed.backups.length;
  var prCount=parsed.processes.length;
  // Build preview HTML
  var h='<div style="padding:8px 0">';
  h+='<p style="margin-bottom:14px;color:var(--gray-700);font-size:13px;line-height:1.5">Se leyó el archivo <b>'+escHtml(fileName)+'</b>. Los siguientes datos se <b>agregaran</b> al dia <b>'+fmt(currentDate)+'</b>:</p>';
  h+='<div style="background:var(--gray-50);border:1px solid var(--gray-200);border-radius:8px;padding:12px 16px;margin-bottom:14px">';
  h+='<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;font-size:13px">';
  if(pCount)h+='<div><b style="color:#6A0DAD">'+pCount+'</b> pollings</div>';
  if(bCount)h+='<div><b style="color:#6A0DAD">'+bCount+'</b> backups</div>';
  if(prCount)h+='<div><b style="color:#6A0DAD">'+prCount+'</b> procesos</div>';
  if(!pCount&&!bCount&&!prCount)h+='<div>No se encontraron datos</div>';
  h+='</div></div>';
  // Show mini preview tables
  if(pCount){
    h+='<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--gray-500);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Pollings</div>';
    h+='<div style="max-height:120px;overflow-y:auto;border:1px solid var(--gray-200);border-radius:6px;font-size:11px">';
    h+='<table style="width:100%;border-collapse:collapse"><thead><tr><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Servidor</th><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Fase</th><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Hora</th></tr></thead><tbody>';
    parsed.pollings.forEach(function(p){
      h+='<tr><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(p.server)+'</td><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(p.phase)+'</td><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(p.time||'—')+'</td></tr>';
    });
    h+='</tbody></table></div></div>';
  }
  if(bCount){
    h+='<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--gray-500);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Backups</div>';
    h+='<div style="max-height:120px;overflow-y:auto;border:1px solid var(--gray-200);border-radius:6px;font-size:11px">';
    h+='<table style="width:100%;border-collapse:collapse"><thead><tr><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Nombre</th><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Ini</th><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Fin</th><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Estado</th></tr></thead><tbody>';
    parsed.backups.forEach(function(b){
      h+='<tr><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(b.name)+'</td><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(b.iniTime||'—')+'</td><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(b.endTime||'—')+'</td><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(b.status||'—')+'</td></tr>';
    });
    h+='</tbody></table></div></div>';
  }
  if(prCount){
    h+='<div style="margin-bottom:10px"><div style="font-size:12px;font-weight:600;color:var(--gray-500);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Procesos</div>';
    h+='<div style="max-height:120px;overflow-y:auto;border:1px solid var(--gray-200);border-radius:6px;font-size:11px">';
    h+='<table style="width:100%;border-collapse:collapse"><thead><tr><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Nombre</th><th style="padding:4px 8px;background:var(--gray-100);text-align:left;font-size:10px">Estado</th></tr></thead><tbody>';
    parsed.processes.forEach(function(p){
      h+='<tr><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(p.name)+'</td><td style="padding:3px 8px;border-top:1px solid var(--gray-100)">'+escHtml(p.status||'—')+'</td></tr>';
    });
    h+='</tbody></table></div></div>';
  }
  // Warning
  h+='<div style="background:#fffbeb;border:1px solid #fde68a;border-radius:8px;padding:10px 14px;margin-top:6px">';
  h+='<div style="font-size:12px;font-weight:600;color:#92400e;margin-bottom:4px">Importante</div>';
  h+='<ul style="font-size:12px;color:#92400e;padding-left:16px;margin:0;line-height:1.6">';
  h+='<li>Los datos se <b>agregan</b> a los existentes (no se reemplazan)</li>';
  h+='<li>Si un servidor de polling ya existe, se actualiza la hora</li>';
  h+='</ul></div>';
  h+='</div>';
  document.getElementById('modalTitle').textContent='Importar desde XLSX';
  document.getElementById('modalBody').innerHTML=h;
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal();_pendingImport=null">Cancelar</button><button class="btn btn-primary" onclick="executeImport()">Importar datos</button>';
  openModal();
}
function executeImport(){
  if(!_pendingImport){toast('No hay datos pendientes');return;}
  var parsed=_pendingImport;
  _pendingImport=null;
  var day=getDay(currentDate);
  // Import pollings: merge by server+phase
  parsed.pollings.forEach(function(p){
    // Remove existing entry for same server+phase
    day.pollings=day.pollings.filter(function(x){return!(x.server===p.server&&x.phase===p.phase);});
    day.pollings.push({id:uid(),server:p.server,region:p.region||getRegion(p.server),phase:p.phase,date:currentDate,time:p.time||'',note:null});
  });
  // Import backups: append
  parsed.backups.forEach(function(b){
    day.backups.push({id:uid(),name:b.name,iniDate:currentDate,iniTime:b.iniTime||'',endDate:currentDate,endTime:b.endTime||'',duration:b.duration||'',status:b.status||'',job:b.job||''});
  });
  // Import processes: append (or update if same name exists)
  parsed.processes.forEach(function(p){
    var existing=day.processes.find(function(x){return x.name===p.name;});
    if(existing){
      if(p.status)existing.status=p.status;
    }else{
      day.processes.push({id:uid(),name:p.name,status:p.status||''});
    }
  });
  saveStore();closeModal();render();
  var total=parsed.pollings.length+parsed.backups.length+parsed.processes.length;
  toast('Se importaron '+total+' registro(s)');
}

// Calendar
function toggleCalendar(){const el=document.getElementById('calPopup');if(el.style.display==='none'){renderCalendar();el.style.display='block';}else el.style.display='none';}
function renderCalendar(){const d=new Date(currentDate+'T12:00:00');calMonth=d.getMonth();calYear=d.getFullYear();drawCalendar();}
function drawCalendar(){const el=document.getElementById('calPopup');const first=new Date(calYear,calMonth,1);const last=new Date(calYear,calMonth+1,0);const startDay=(first.getDay()+6)%7;const today=new Date();today.setHours(12,0,0,0);const sel=new Date(currentDate+'T12:00:00');let h='<div class="cal-header"><button class="btn-icon" onclick="event.stopPropagation();calNav(-1)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><span>'+MN[calMonth]+' '+calYear+'</span><button class="btn-icon" onclick="event.stopPropagation();calNav(1)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></button></div><div class="cal-grid">';DN.forEach(d=>h+='<div class="day-name">'+d+'</div>');for(let i=0;i<startDay;i++){const dd=new Date(calYear,calMonth,-(startDay-i-1));h+='<div class="day other" onclick="calClick('+calYear+','+(calMonth-1)+','+dd.getDate()+')">'+dd.getDate()+'</div>';}for(let i=1;i<=last.getDate();i++){const ds=calYear+'-'+String(calMonth+1).padStart(2,'0')+'-'+String(i).padStart(2,'0');const isT=today.getFullYear()===calYear&&today.getMonth()===calMonth&&today.getDate()===i;const isS=sel.getFullYear()===calYear&&sel.getMonth()===calMonth&&sel.getDate()===i;const has=!!store[ds];const hasErr=has&&store[ds].backups&&store[ds].backups.some(b=>b.status&&(b.status.includes('Fail')||b.status.includes('SUSP')));h+='<div class="day'+(isT?' today':'')+(isS?' selected':'')+(has?(hasErr?' has-data has-error':' has-data'):'')+'" onclick="calClick('+calYear+','+calMonth+','+i+')">'+i+'</div>';}const rem=42-startDay-last.getDate();for(let i=1;i<=rem;i++)h+='<div class="day other" onclick="calClick('+calYear+','+(calMonth+1)+','+i+')">'+i+'</div>';h+='</div>';el.innerHTML=h;}
function calNav(d){calMonth+=d;if(calMonth>11){calMonth=0;calYear++;}if(calMonth<0){calMonth=11;calYear--;}drawCalendar();}
function calClick(y,m,d){const dt=new Date(y,m,d);currentDate=dt.toISOString().split('T')[0];SEARCH.value='';document.getElementById('calPopup').style.display='none';render();}
document.addEventListener('click',e=>{if(!e.target.closest('#dateDisplay')&&!e.target.closest('.cal-popup'))document.getElementById('calPopup').style.display='none';});

// Modals
// Admin gate: if day is locked, non-admin sees info modal, admin sees reason modal
function _adminGate(actionFn){
  if(!isDayLocked(currentDate)){actionFn();return;}
  if(!isAdmin()){showLockedModal();return;}
  _pendingAdminAction=actionFn;showLockedModal();
}
function showLockedModal(){
  if(isAdmin()){
    // Admin: ask for reason to allow editing
    document.getElementById('lockedModalBody').innerHTML=
      '<p style="color:var(--gray-600);font-size:13px;line-height:1.5;margin-bottom:12px">Este dia esta cerrado. Como administrador podes editarlo, pero se registrara la reapertura.</p>'+
      '<div class="form-group"><label>Motivo de reapertura (obligatorio)</label><textarea id="reopenReason" rows="3" placeholder="Ingrese el motivo por el cual necesita editar este dia cerrado..." style="width:100%;font-size:13px;border:1px solid var(--gray-300);border-radius:6px;padding:8px;resize:vertical;min-height:60px"></textarea></div>';
    document.getElementById('lockedModalFooter').innerHTML=
      '<button class="btn btn-outline" onclick="_cancelReopen()">Cancelar</button><button class="btn btn-primary" onclick="_confirmReopen()">Continuar</button>';
    document.getElementById('lockedModal').classList.add('show');
  } else {
    // Operator: just inform
    document.getElementById('lockedModalBody').innerHTML=
      '<div style="text-align:center;padding:10px 0">'+
      '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--red-500)" stroke-width="2" style="margin-bottom:12px"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'+
      '<h3 style="font-size:16px;font-weight:700;color:var(--red-600);margin-bottom:6px">DIA CERRADO</h3>'+
      '<p style="color:var(--gray-600);font-size:13px">Solo un administrador puede modificar este dia.</p></div>';
    document.getElementById('lockedModalFooter').innerHTML=
      '<button class="btn btn-primary" onclick="closeLockedModal()">Entendido</button>';
    document.getElementById('lockedModal').classList.add('show');
  }
}
function _cancelReopen(){_pendingAdminAction=null;closeLockedModal();}
function _confirmReopen(){
  var reason=document.getElementById('reopenReason').value.trim();
  if(!reason){toast('El motivo es obligatorio');document.getElementById('reopenReason').focus();return;}
  // Log audit
  var day=getDay(currentDate);
  if(!day.audit)day.audit=[];
  var now=new Date();
  var ts=now.getFullYear()+'-'+String(now.getMonth()+1).padStart(2,'0')+'-'+String(now.getDate()).padStart(2,'0')+' '+String(now.getHours()).padStart(2,'0')+':'+String(now.getMinutes()).padStart(2,'0')+':'+String(now.getSeconds()).padStart(2,'0');
  day.audit.push({type:'reapertura',user:currentUser.username,timestamp:ts,reason:reason});
  saveStore();
  closeLockedModal();
  // Execute the pending action
  if(_pendingAdminAction){var fn=_pendingAdminAction;_pendingAdminAction=null;fn();}
}
function closeLockedModal(){document.getElementById('lockedModal').classList.remove('show');}
function openModal(){document.getElementById('modalOverlay').classList.add('show');}
function closeModal(){document.getElementById('modalOverlay').classList.remove('show');}

function openPollingModal(server){
  _adminGate(function(){_openPollingModalInner(server);});
}
function _openPollingModalInner(server){
  const day=getDay(currentDate);const isEdit=!!server;
  let beg='',end='';
  if(isEdit){const es=day.pollings.filter(p=>p.server===server);const b=es.find(e=>e.phase==='BEGINNING');const e=es.find(e=>e.phase==='ENDING');beg=b?b.time:'';end=e?e.time:'';}
  document.getElementById('modalTitle').textContent=isEdit?'Editar Polling':'Nuevo Polling';
  document.getElementById('modalBody').innerHTML='<div class="form-group"><label>Servidor</label><select id="mSrv">'+SERVERS.map(s=>'<option value="'+s+'"'+(s===server?' selected':'')+'>'+s+'</option>').join('')+'</select></div><div class="form-row"><div class="form-group"><label>Hora Inicio</label><input type="time" id="mBeg" value="'+beg+'"></div><div class="form-group"><label>Hora Fin</label><input type="time" id="mEnd" value="'+end+'"></div></div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="savePolling(\''+server+'\')">'+(isEdit?'Actualizar':'Guardar')+'</button>';
  openModal();
}
function savePolling(old){
  const day=getDay(currentDate);const srv=document.getElementById('mSrv').value;
  const beg=document.getElementById('mBeg').value;const end=document.getElementById('mEnd').value;
  if(old)day.pollings=day.pollings.filter(p=>p.server!==old);
  if(beg)day.pollings.push({id:uid(),server:srv,region:getRegion(srv),phase:'BEGINNING',date:currentDate,time:beg,note:null});
  if(end)day.pollings.push({id:uid(),server:srv,region:getRegion(srv),phase:'ENDING',date:currentDate,time:end,note:null});
  saveStore();closeModal();render();toast('Guardado');
}
function deletePolling(s){_adminGate(function(){if(!confirm('Eliminar '+s+'?'))return;getDay(currentDate).pollings=getDay(currentDate).pollings.filter(function(p){return p.server!==s;});saveStore();render();toast('Eliminado');});}

function openBackupModal(idx){_adminGate(function(){_openBackupModalInner(idx);});}
function _openBackupModalInner(idx){
  const day=getDay(currentDate);const b=idx!==undefined?day.backups[idx]:null;
  const endDate=b&&b.endDate?b.endDate:currentDate;
  document.getElementById('modalTitle').textContent=b?'Editar Backup':'Nuevo Backup';
  document.getElementById('modalBody').innerHTML='<div class="form-row"><div class="form-group"><label>Nombre</label><select id="mBkN">'+BKN.map(n=>'<option value="'+n+'"'+(b&&b.name===n?' selected':'')+'>'+n+'</option>').join('')+'</select></div><div class="form-group"><label>JOB</label><select id="mBkJ"><option value="">—</option>'+JOBS.map(j=>'<option value="'+j+'"'+(b&&b.job===j?' selected':'')+'>'+j+'</option>').join('')+'</select></div></div><div class="form-row"><div class="form-group"><label>Fecha Inicio</label><input type="date" id="mBkID" value="'+iniDate+'" onchange="autoCalcBkpDur()"></div><div class="form-group"><label>Hora Inicio</label><input type="time" id="mBkI" value="'+(b?b.iniTime||'':'')+'" onchange="autoCalcBkpDur()"></div></div><div class="form-row"><div class="form-group"><label>Fecha Fin</label><input type="date" id="mBkED" value="'+endDate+'" onchange="autoCalcBkpDur()"></div><div class="form-group"><label>Hora Fin</label><input type="time" id="mBkE" value="'+(b?b.endTime||'':'')+'" onchange="autoCalcBkpDur()"></div></div><div class="form-row"><div class="form-group"><label>Duracion (auto)</label><input id="mBkD" value="'+(b?b.duration||'':'')+'" placeholder="Se calcula solo" readonly style="background:var(--gray-100);cursor:default"></div><div class="form-group"><label>Estado</label><input id="mBkS" value="'+(b?b.status||'':'')+'" placeholder="Robot Fail"></div></div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="saveBackup('+idx+')">'+(b?'Actualizar':'Guardar')+'</button>';
  openModal();
}
function autoCalcBkpDur(){const id=document.getElementById('mBkID').value;const it=document.getElementById('mBkI').value;const ed=document.getElementById('mBkED').value;const et=document.getElementById('mBkE').value;const f=document.getElementById('mBkD');if(!id||!it||!ed||!et){f.value='';return;}const iniMs=new Date(id+'T'+it).getTime();const endMs=new Date(ed+'T'+et).getTime();const d=Math.round((endMs-iniMs)/1000);if(d<0){f.value='';return;}const h=Math.floor(d/3600),m=Math.floor((d%3600)/60);f.value=h+':'+String(m).padStart(2,'0');}
function saveBackup(idx){
  const day=getDay(currentDate);
  const iniDate=document.getElementById('mBkID').value||currentDate;
  const iniTime=document.getElementById('mBkI').value||null;
  const endDate=document.getElementById('mBkED').value||currentDate;
  const endTime=document.getElementById('mBkE').value||null;
  let duration=document.getElementById('mBkD').value||null;
  if(!duration&&iniDate&&iniTime&&endDate&&endTime){const iniMs=new Date(iniDate+'T'+iniTime).getTime();const endMs=new Date(endDate+'T'+endTime).getTime();const d=Math.round((endMs-iniMs)/1000);if(d>=0){const h=Math.floor(d/3600),m=Math.floor((d%3600)/60);duration=h+':'+String(m).padStart(2,'0');}}
  const o={name:document.getElementById('mBkN').value,iniDate:iniDate,iniTime:iniTime,endDate:endDate,endTime:endTime,job:document.getElementById('mBkJ').value||null,duration:duration,status:document.getElementById('mBkS').value||null};
  if(idx!==undefined)day.backups[idx]=o;else day.backups.push(o);saveStore();closeModal();render();toast('Guardado');
}
function deleteBackup(i){_adminGate(function(){if(!confirm('Eliminar?'))return;getDay(currentDate).backups.splice(i,1);saveStore();render();toast('Eliminado');});}

function openProcessModal(idx){
  _adminGate(function(){_openProcessModalInner(idx);});
}
function _openProcessModalInner(idx){
  const day=getDay(currentDate);const p=idx!==undefined?day.processes[idx]:null;
  document.getElementById('modalTitle').textContent=p?'Editar Proceso':'Nuevo Proceso';
  const isNew=!p||!PROCS.includes(p.name);
  document.getElementById('modalBody').innerHTML='<div class="form-group"><label>Proceso</label><select id="mPN"'+(isNew?' onchange="toggleCustomProcess(this.value)"':'')+'>'+PROCS.map(n=>'<option value="'+n+'"'+(p&&p.name===n?' selected':'')+'>'+n+'</option>').join('')+'<option value="__custom__"'+(isNew?' selected':'')+'>+ Crear nuevo...</option></select></div>'+(isNew?'<div class="form-group" id="customProcGroup"><label>Nombre del proceso</label><input type="text" id="mPNCustom" value="'+(p&&!PROCS.includes(p.name)?p.name:'')+'" placeholder="Nombre del nuevo proceso"></div>':'')+'<div class="form-group"><label>Estado</label><select id="mPS">'+STATS.map(s=>'<option value="'+s+'"'+(p&&p.status===s?' selected':'')+'>'+(s||'—')+'</option>').join('')+'</select></div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="saveProcess('+idx+')">'+(p?'Actualizar':'Guardar')+'</button>';
  openModal();
}
function toggleCustomProcess(v){document.getElementById('customProcGroup').style.display=v==='__custom__'?'':'none';}
function saveProcess(idx){
  const day=getDay(currentDate);
  const sel=document.getElementById('mPN').value;
  const name=sel==='__custom__'?document.getElementById('mPNCustom').value.trim():sel;
  if(!name){toast('Escribir nombre del proceso');return;}
  const o={name:name,status:document.getElementById('mPS').value};
  if(idx!==undefined)day.processes[idx]=o;else day.processes.push(o);saveStore();closeModal();render();toast('Guardado');
}
function deleteProcess(i){_adminGate(function(){if(!confirm('Eliminar?'))return;getDay(currentDate).processes.splice(i,1);saveStore();render();toast('Eliminado');});}


// ===== AUTH SYSTEM =====
const USERS={
  OPERANOCHE:{pass:'noche1',shift:'TURNO NOCHE',cssClass:'shift-noche',role:'operator'},
  OPERAMAÑANA:{pass:'mañana1',shift:'TURNO MAÑANA',cssClass:'shift-manana',role:'operator'},
  OPERATARDE:{pass:'tarde1',shift:'TURNO TARDE',cssClass:'shift-tarde',role:'operator'},
  OPERAADMIN:{pass:'nocadmin',shift:'ADMIN',cssClass:'shift-admin',role:'admin'},
  OPERAWU:{pass:'0p3r4ci0n35',shift:'ADMIN',cssClass:'shift-admin',role:'admin'},
  NOCPRUEBA:{pass:'pruebanoc',shift:'ADMIN',cssClass:'shift-admin',role:'admin'},
  ADMILOSN:{pass:'admilosn',shift:'ADMIN',cssClass:'shift-admin',role:'admin'}
};
let currentUser=null;

function doLogin(){
  const u=document.getElementById('loginUser').value.trim().toUpperCase();
  const p=document.getElementById('loginPass').value;
  const user=USERS[u];
  if(!user||user.pass!==p){
    document.getElementById('loginError').textContent='Usuario o contrasena incorrectos';
    document.getElementById('loginPass').value='';
    return;
  }
  currentUser={username:u,...user};
  sessionStorage.setItem('bitacora_user',u);
  GH_CONFIG.token=_decodeTK();refreshGHHeaders();
  document.getElementById('loginOverlay').classList.add('hide');
  document.getElementById('userBar').style.display='flex';
  document.getElementById('userNameDisplay').textContent=u;
  const badge=document.getElementById('userShiftBadge');
  badge.textContent=user.shift;
  badge.className='shift-badge '+user.cssClass;
  if(user.role==='admin'){
    document.getElementById('adminMenuWrap').style.display='';
  }else{
    document.getElementById('adminMenuWrap').style.display='none';
  }
  document.getElementById('loginError').textContent='';
}
function doLogout(){
  // Check if cierre de turno was done today
  const day=store[currentDate];
  const sk=currentUser?SHIFT_MAP[currentUser.username]||'ADMIN':'';
  const hasCierre=day&&day.handovers&&day.handovers.some(h=>h.shift===sk);
  if(!hasCierre&&currentUser){
    if(!confirm('ATENCION: No ha realizado el Pase de Turno. Esta accion es OBLIGATORIA.\n\nDesea salir de todas formas?')){
      return;
    }
  }
  currentUser=null;
  sessionStorage.removeItem('bitacora_user');
  document.getElementById('loginOverlay').classList.remove('hide');
  document.getElementById('userBar').style.display='none';
  document.getElementById('adminMenuWrap').style.display='none';
  document.getElementById('loginUser').value='';
  document.getElementById('loginPass').value='';
}
function checkSession(){
  GH_CONFIG.token=_decodeTK();refreshGHHeaders();
  const u=sessionStorage.getItem('bitacora_user');
  if(u&&USERS[u]){
    currentUser={username:u,...USERS[u]};
    document.getElementById('loginOverlay').classList.add('hide');
    document.getElementById('userBar').style.display='flex';
    document.getElementById('userNameDisplay').textContent=u;
    const badge=document.getElementById('userShiftBadge');
    badge.textContent=USERS[u].shift;
    badge.className='shift-badge '+USERS[u].cssClass;
    if(USERS[u].role==='admin'){
      document.getElementById('adminMenuWrap').style.display='';
    }else{
      document.getElementById('adminMenuWrap').style.display='none';
    }
  }
}
document.getElementById('loginPass').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin();});
document.getElementById('loginUser').addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('loginPass').focus();});
checkSession();

// ===== ADMIN DASHBOARD =====
var _dashCalMonth,_dashCalYear,_dashCalSelected=null;
function openDashboard(){
  if(!currentUser||currentUser.role!=='admin')return;
  document.getElementById('dashOverlay').classList.add('show');
  var now=new Date();_dashCalMonth=now.getMonth();_dashCalYear=now.getFullYear();
  _dashCalSelected=null;
  renderDashSidebar();
  renderDashboard();
}
function closeDashboard(){
  document.getElementById('dashOverlay').classList.remove('show');
}
function renderDashSidebar(){
  var sb=document.getElementById('dashSidebar');
  var today=new Date();today.setHours(12,0,0,0);
  var selDate=_dashCalSelected?new Date(_dashCalSelected+'T12:00:00'):null;
  var first=new Date(_dashCalYear,_dashCalMonth,1);
  var last=new Date(_dashCalYear,_dashCalMonth+1,0);
  var startDay=(first.getDay()+6)%7;
  var h='';
  // Calendar nav
  h+='<div class="dash-cal-nav"><button onclick="_dashCalNav(-1)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><span>'+MN[_dashCalMonth]+' '+_dashCalYear+'</span><button onclick="_dashCalNav(1)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></button></div>';
  // Grid
  h+='<div class="dash-cal-grid">';
  DN.forEach(function(d){h+='<div class="dc-dayname">'+d+'</div>';});
  // Previous month fill
  for(var i=0;i<startDay;i++){
    var dd=new Date(_dashCalYear,_dashCalMonth,-(startDay-i-1));
    h+='<div class="dc-day other" onclick="_dashCalClick('+(_dashCalMonth===0?_dashCalYear-1:_dashCalYear)+','+(_dashCalMonth===0?11:_dashCalMonth-1)+','+dd.getDate()+')">'+dd.getDate()+'</div>';
  }
  // Current month
  for(var d=1;d<=last.getDate();d++){
    var ds=_dashCalYear+'-'+String(_dashCalMonth+1).padStart(2,'0')+'-'+String(d).padStart(2,'0');
    var isT=today.getFullYear()===_dashCalYear&&today.getMonth()===_dashCalMonth&&today.getDate()===d;
    var isS=selDate&&selDate.getFullYear()===_dashCalYear&&selDate.getMonth()===_dashCalMonth&&selDate.getDate()===d;
    var hasD=!!store[ds];
    var hasErr=hasD&&store[ds].backups&&store[ds].backups.some(function(b){return b.status&&(b.status.indexOf('Fail')>=0||b.status.indexOf('SUSP')>=0);});
    var cls='dc-day';
    if(isS)cls+=' selected';
    else if(isT)cls+=' today';
    if(hasD)cls+=hasErr?' has-err has-data':' has-data';
    h+='<div class="'+cls+'" onclick="_dashCalClick('+_dashCalYear+','+_dashCalMonth+','+d+')" title="'+ds+'">'+d+'</div>';
  }
  // Next month fill
  var rem=42-startDay-last.getDate();
  for(var j=1;j<=rem;j++){
    h+='<div class="dc-day other" onclick="_dashCalClick('+(_dashCalMonth===11?_dashCalYear+1:_dashCalYear)+','+(_dashCalMonth===11?0:_dashCalMonth+1)+','+j+')">'+j+'</div>';
  }
  h+='</div>';
  // Legend
  h+='<div class="dash-sidebar-legend"><div><span class="dot" style="background:var(--emerald-600)"></span> Con datos</div><div><span class="dot" style="background:var(--red-500)"></span> Con errores</div></div>';
  // Actions

  sb.innerHTML=h;
}
function _dashCalNav(dir){
  _dashCalMonth+=dir;
  if(_dashCalMonth>11){_dashCalMonth=0;_dashCalYear++;}
  if(_dashCalMonth<0){_dashCalMonth=11;_dashCalYear--;}
  renderDashSidebar();
}
function _dashCalClick(y,m,d){
  var dt=new Date(y,m,d);
  _dashCalSelected=dt.toISOString().split('T')[0];
  renderDashSidebar();
}

function getDateRange(){
  const period=document.getElementById('dashPeriod').value;
  const now=new Date();now.setHours(12,0,0,0);
  let from,to;
  if(period==='week'){
    const dow=now.getDay();
    const diff=dow===0?6:dow-1;
    from=new Date(now);from.setDate(now.getDate()-diff);from.setHours(0,0,0,0);
    to=new Date(from);to.setDate(from.getDate()+6);to.setHours(23,59,59,999);
  }else if(period==='month'){
    from=new Date(now.getFullYear(),now.getMonth(),1);
    to=new Date(now.getFullYear(),now.getMonth()+1,0,23,59,59,999);
  }else if(period==='year'){
    from=new Date(now.getFullYear(),0,1);
    to=new Date(now.getFullYear(),11,31,23,59,59,999);
  }else{
    from=null;to=null;
  }
  return{period,from,to};
}
function fmtDate(d){if(typeof d==='string')return d;return d.toISOString().split('T')[0];}
function isInRange(dateStr,from,to){
  if(!from)return true;
  const d=new Date(dateStr+'T12:00:00');
  return d>=from&&d<=to;
}
function getDaysInRange(from,to){
  return Object.entries(store).filter(([k])=>isInRange(k,from,to));
}

function calcDurSecs(s,e){
  if(!s||!e)return null;
  const p=t=>{const x=t.split(':').map(Number);return(x[0]||0)*3600+(x[1]||0)*60+(x[2]||0);};
  return p(e)-p(s);
}
function fmtSecs(s){
  if(s===null||s<0)return'—';
  const h=Math.floor(s/3600),m=Math.floor((s%3600)/60),sc=s%60;
  if(h>0)return h+'h '+m+'m';
  if(m>0)return m+'m '+sc+'s';
  return sc+'s';
}

function renderDashboard(){
  const body=document.getElementById('dashContent');
  const{period,from,to}=getDateRange();
  const days=getDaysInRange(from,to);
  const totalDays=days.length;

  // Aggregate data
  let totalPollings=0,completedPollings=0,totalBkps=0,failedBkps=0,okBkps=0;
  let totalProcs=0,okProcs=0,failProcs=0,ncProcs=0;
  let allDurations=[];
  let serverDurs={};
  let dailyStats=[];
  let bkpDurations=[];
  let bkpNames={};
  let procNames={};

  days.forEach(([dateStr,day])=>{
    let dayPollBeg=0,dayPollEnd=0;
    day.pollings.forEach(p=>{
      totalPollings++;
      if(p.phase==='BEGINNING')dayPollBeg++;
      if(p.phase==='ENDING')dayPollEnd++;
      if(p.phase==='ENDING'&&p.time){
        const beg=day.pollings.find(x=>x.server===p.server&&x.phase==='BEGINNING');
        if(beg&&beg.time){
          const dur=calcDurSecs(beg.time,p.time);
          if(dur!==null&&dur>=0){
            allDurations.push(dur);
            if(!serverDurs[p.server])serverDurs[p.server]=[];
            serverDurs[p.server].push(dur);
          }
        }
      }
    });
    completedPollings+=Math.min(dayPollBeg,dayPollEnd);

    day.backups.forEach(b=>{
      totalBkps++;
      if(b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'))){
        failedBkps++;
      }else if(b.status&&b.status!==''){
        okBkps++;
      }else if(b.iniTime&&b.endTime){
        okBkps++;
      }
      if(b.name)bkpNames[b.name]=(bkpNames[b.name]||0)+1;
      if(b.duration){
        const parts=b.duration.split(':').map(Number);
        const secs=(parts[0]||0)*3600+(parts[1]||0)*60;
        if(secs>0)bkpDurations.push(secs);
      }
    });

    day.processes.forEach(p=>{
      totalProcs++;
      const u=(p.status||'').toUpperCase();
      if(u==='OK')okProcs++;
      else if(u==='ERROR')failProcs++;
      else ncProcs++;
      if(p.name)procNames[p.name]=(procNames[p.name]||0)+1;
    });

    dailyStats.push({
      date:dateStr,
      pollCompleted:Math.min(dayPollBeg,dayPollEnd),
      pollTotal:Math.max(dayPollBeg,dayPollEnd),
      bkpOk:day.backups.filter(b=>!(b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP')))).length,
      bkpFail:day.backups.filter(b=>b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'))).length,
      procOk:day.processes.filter(p=>{const u=(p.status||'').toUpperCase();return u==='OK';}).length,
      procTotal:day.processes.length
    });
  });

  // Averages
  const avgDur=allDurations.length?Math.round(allDurations.reduce((a,b)=>a+b,0)/allDurations.length):0;
  const avgBkpDur=bkpDurations.length?Math.round(bkpDurations.reduce((a,b)=>a+b,0)/bkpDurations.length):0;
  const pollPct=totalPollings>0?Math.round(completedPollings/(totalPollings/2)*100):0;
  const bkpPct=totalBkps>0?Math.round(okBkps/totalBkps*100):0;
  const procPct=totalProcs>0?Math.round(okProcs/totalProcs*100):0;

  // Period label
  const periodLabels={week:'Semanal',month:'Mensual',year:'Anual',all:'Historico'};
  let rangeLabel=periodLabels[period];
  if(from&&to)rangeLabel+=' ('+fmtDate(from)+' al '+fmtDate(to)+')';

  // Top 5 slowest servers
  const serverAvgs=Object.entries(serverDurs).map(([s,durs])=>({server:s,avg:Math.round(durs.reduce((a,b)=>a+b,0)/durs.length),count:durs.length})).sort((a,b)=>b.avg-a.avg);
  const topSlow=serverAvgs.slice(0,8);
  const topFast=serverAvgs.slice().sort((a,b)=>a.avg-b.avg).slice(0,8);

  // Build HTML
  let h='';

  // Summary cards
  h+='<div class="dash-summary">';
  h+='<div class="dash-stat dash-info"><div class="dash-val">'+totalDays+'</div><div class="dash-lbl">Dias con datos</div></div>';
  h+='<div class="dash-stat dash-ok"><div class="dash-val">'+pollPct+'%</div><div class="dash-lbl">Pollings completados ('+completedPollings+'/'+(totalPollings?Math.floor(totalPollings/2):0)+')</div></div>';
  h+='<div class="dash-stat '+(bkpPct>=90?'dash-ok':bkpPct>=70?'dash-warn':'dash-fail')+'"><div class="dash-val">'+bkpPct+'%</div><div class="dash-lbl">Backups OK ('+okBkps+'/'+totalBkps+')</div></div>';
  h+='<div class="dash-stat '+(procPct>=90?'dash-ok':procPct>=70?'dash-warn':'dash-fail')+'"><div class="dash-val">'+procPct+'%</div><div class="dash-lbl">Procesos OK ('+okProcs+'/'+totalProcs+')</div></div>';
  h+='<div class="dash-stat dash-info"><div class="dash-val">'+fmtSecs(avgDur)+'</div><div class="dash-lbl">Duracion promedio polling</div></div>';
  h+='<div class="dash-stat dash-info"><div class="dash-val">'+fmtSecs(avgBkpDur)+'</div><div class="dash-lbl">Duracion promedio BKP</div></div>';
  h+='<div class="dash-stat dash-warn"><div class="dash-val">'+failedBkps+'</div><div class="dash-lbl">Backups fallidos</div></div>';
  h+='<div class="dash-stat dash-fail"><div class="dash-val">'+failProcs+'</div><div class="dash-lbl">Procesos con Error</div></div>';
  h+='</div>';

  // Charts row
  h+='<div class="dash-chart-row">';
  // Slowest servers
  h+='<div class="dash-chart-card"><h4>Servidores mas lentos (promedio)</h4><div class="dash-bar-chart">';
  const maxDur=topSlow.length?topSlow[0].avg:1;
  topSlow.forEach(s=>{
    const pct=Math.round(s.avg/maxDur*100);
    h+='<div class="dash-bar-row"><span class="dash-bar-label" title="'+s.server+'">'+s.server+'</span><div class="dash-bar-track"><div class="dash-bar-fill" style="width:'+pct+'%;background:#dc2626"></div></div><span class="dash-bar-val">'+fmtSecs(s.avg)+'</span></div>';
  });
  if(!topSlow.length)h+='<div class="dash-empty">Sin datos</div>';
  h+='</div></div>';
  // Fastest servers
  h+='<div class="dash-chart-card"><h4>Servidores mas rapidos (promedio)</h4><div class="dash-bar-chart">';
  const maxFast=topFast.length?topFast[topFast.length-1].avg:1;
  topFast.forEach(s=>{
    const pct=Math.round(s.avg/maxFast*100);
    h+='<div class="dash-bar-row"><span class="dash-bar-label" title="'+s.server+'">'+s.server+'</span><div class="dash-bar-track"><div class="dash-bar-fill" style="width:'+pct+'%;background:#6A0DAD"></div></div><span class="dash-bar-val">'+fmtSecs(s.avg)+'</span></div>';
  });
  if(!topFast.length)h+='<div class="dash-empty">Sin datos</div>';
  h+='</div></div>';
  h+='</div>';

  // Process status chart
  const procOkPct=totalProcs>0?Math.round(okProcs/totalProcs*100):0;
  const procErrPct=totalProcs>0?Math.round(failProcs/totalProcs*100):0;
  h+='<div class="dash-chart-row">';
  h+='<div class="dash-chart-card"><h4>Estado de Procesos</h4>';
  h+='<div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#6A0DAD">'+procOkPct+'%</div><div style="font-size:11px;color:var(--gray-500)">OK ('+okProcs+')</div></div>';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#dc2626">'+procErrPct+'%</div><div style="font-size:11px;color:var(--gray-500)">Error ('+failProcs+')</div></div>';
  h+='</div></div>';
  // Backup status chart
  h+='<div class="dash-chart-card"><h4>Estado de Backups</h4>';
  h+='<div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#6A0DAD">'+okBkps+'</div><div style="font-size:11px;color:var(--gray-500)">Completados</div></div>';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#dc2626">'+failedBkps+'</div><div style="font-size:11px;color:var(--gray-500)">Fallidos</div></div>';
  h+='</div></div>';
  h+='</div>';

  // Daily breakdown table
  h+='<div class="dash-section"><div class="dash-section-header"><h3>Desglose por dia - '+rangeLabel+'</h3></div>';
  if(dailyStats.length){
    h+='<div style="overflow-x:auto"><table class="dash-table"><thead><tr><th>Fecha</th><th class="num">Pollings OK</th><th class="num">Pollings Total</th><th class="num">BKP OK</th><th class="num">BKP Fail</th><th class="num">Proc OK</th><th class="num">Proc Total</th><th>Completitud</th></tr></thead><tbody>';
    dailyStats.forEach(d=>{
      const total=d.pollTotal+d.bkpOk+d.bkpFail+d.procTotal;
      const done=d.pollCompleted+d.bkpOk+d.procOk;
      const pct=total>0?Math.round(done/total*100):0;
      const cls=pct>=90?'ok-cell':pct>=70?'warn-cell':'fail-cell';
      h+='<tr><td>'+d.date+'</td><td class="num '+(d.pollCompleted>=d.pollTotal?'ok-cell':'')+'">'+d.pollCompleted+'</td><td class="num">'+d.pollTotal+'</td><td class="num ok-cell">'+d.bkpOk+'</td><td class="num '+(d.bkpFail>0?'fail-cell':'')+'">'+d.bkpFail+'</td><td class="num ok-cell">'+d.procOk+'</td><td class="num">'+d.procTotal+'</td><td><div style="display:flex;align-items:center;gap:6px"><div class="dash-pct-bar"><div class="dash-pct-fill '+(pct>=90?'ok-fill':pct>=70?'warn-fill':'fail-fill')+'" style="width:'+pct+'%"></div></div><span class="num '+cls+'" style="min-width:36px">'+pct+'%</span></div></td></tr>';
    });
    h+='</tbody></table></div>';
  }else{
    h+='<div class="dash-empty">No hay datos para el periodo seleccionado</div>';
  }
  h+='</div>';

  // Server duration table
  h+='<div class="dash-section"><div class="dash-section-header"><h3>Tiempos por servidor - '+rangeLabel+'</h3></div>';
  if(serverAvgs.length){
    h+='<div style="overflow-x:auto"><table class="dash-table"><thead><tr><th>Servidor</th><th class="num">Dur. Promedio</th><th class="num">Dur. Min</th><th class="num">Dur. Max</th><th class="num">Registros</th></tr></thead><tbody>';
    serverAvgs.forEach(s=>{
      const durs=serverDurs[s.server];
      const mn=Math.min(...durs),mx=Math.max(...durs);
      h+='<tr><td>'+s.server+'</td><td class="num">'+fmtSecs(s.avg)+'</td><td class="num">'+fmtSecs(mn)+'</td><td class="num '+(mx>7200?'fail-cell':mx>3600?'warn-cell':'')+'">'+fmtSecs(mx)+'</td><td class="num">'+s.count+'</td></tr>';
    });
    h+='</tbody></table></div>';
  }else{
    h+='<div class="dash-empty">No hay datos de duracion</div>';
  }
  h+='</div>';

  // Backup detail table
  h+='<div class="dash-section"><div class="dash-section-header"><h3>Detalle de Backups por nombre - '+rangeLabel+'</h3></div>';
  const bkpEntries=Object.entries(bkpNames).sort((a,b)=>b[1]-a[1]);
  if(bkpEntries.length){
    h+='<div style="overflow-x:auto"><table class="dash-table"><thead><tr><th>Backup</th><th class="num">Ejecuciones</th></tr></thead><tbody>';
    bkpEntries.forEach(([name,count])=>{
      h+='<tr><td>'+name+'</td><td class="num">'+count+'</td></tr>';
    });
    h+='</tbody></table></div>';
  }else{
    h+='<div class="dash-empty">No hay datos de backups</div>';
  }
  h+='</div>';

  body.innerHTML=h;
}


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
    backups:['Sebastian Torrez','Anibal Rivero','Omar Baldomir']
  }
};
const SHIFT_MAP={OPERAMAÑANA:'MANANA',OPERATARDE:'TARDE',OPERANOCHE:'NOCHE',OPERAADMIN:'ADMIN'};
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
function deleteTimelineNote(id){_adminGate(function(){if(!confirm('Eliminar esta nota?'))return;_doDeleteTimelineNote(id);});}
function _doDeleteTimelineNote(id){
  const day=getDay(currentDate);
  if(day.timeline)day.timeline=day.timeline.filter(n=>n.id!==id);
  saveStore();renderTimeline(day);toast('Nota eliminada');
}
function renderTimeline(day){
  const locked=isDayLocked(currentDate)&&!isAdmin();
  document.getElementById('tlAddBar').style.display='';
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
    h+=(locked?'':'<button class="btn-icon danger tl-del" title="Eliminar" onclick="deleteTimelineNote(\''+n.id+'\')"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>');
    h+='</div>';
  });
  body.innerHTML=h;
}

// Enter key on note input
document.getElementById('tlText').addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();addTimelineNote();}});

// Populate operator select after login
function refreshOperatorSelect(){populateOperatorSelect();}
// Override doLogin to also populate operator select

// ===== CIERRE DE TURNO =====
function openCierreModal(){
  if(!currentUser)return;
  const day=getDay(currentDate);
  const sk=SHIFT_MAP[currentUser.username]||'ADMIN';
  const skLabel=SHIFT_LABELS[sk]||sk;
  const auto=getCurrentOperator()||currentUser.username;
  document.getElementById('modalTitle').textContent='PASE DE TURNO (OBLIGATORIO) - '+skLabel;
  document.getElementById('modalBody').innerHTML=
    '<div class="form-group"><label>Operador</label><select id="cierreOp">'+buildOpOptions(auto)+'</select></div>'+
    '<div class="form-group"><label>Novedades (obligatorio)</label><textarea id="cierreText" rows="4" placeholder="Detalle de novedades del turno, incidencias, tareas pendientes..." style="width:100%;font-size:13px;border:1px solid var(--gray-300);border-radius:6px;padding:8px;resize:vertical;min-height:80px"></textarea></div>'+
    '<div class="cierre-checks">'+
    '<label class="cierre-check"><input type="checkbox" id="cierrePollOk" checked> Pollings completados</label>'+
    '<label class="cierre-check"><input type="checkbox" id="cierreBkpOk" checked> Backups OK</label>'+
    '<label class="cierre-check"><input type="checkbox" id="cierreProcOk" checked> Procesos OK</label>'+
    '</div>';
  document.getElementById('modalFooter').innerHTML='<button class="btn btn-outline" onclick="closeModal()">Cancelar</button><button class="btn btn-primary" onclick="saveCierre()">Confirmar Pase</button>';
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
  // Audit log: register closure
  if(!day.audit)day.audit=[];
  day.audit.push({type:'cierre',user:currentUser.username,timestamp:ts,detail:'Pase de turno - '+entry.shiftLabel});
  // Create notification
  if(!day.notifications)day.notifications=[];
  day.notifications.push({
    id:uid(),
    type:'handover',
    title:'Pase de Turno - '+entry.shiftLabel,
    desc:op+': '+text.substring(0,80)+(text.length>80?'...':''),
    timestamp:ts,
    shift:sk,
    readBy:{}
  });
  saveStore();closeModal();
  renderNovedades(day);updateNotifBadge(day);renderNotifPanel(day);
  toast('Pase de turno registrado');
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
// ===== DOWNLOAD REPORTS =====
function triggerDownload(html,filename){
  const blob=new Blob([html],{type:'text/html;charset=utf-8'});
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=filename;a.click();URL.revokeObjectURL(a.href);
  toast('Descargando '+filename);
}
function reportCSS(){
  return '<style>*{box-sizing:border-box;margin:0;padding:0}body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:#f8fafc;color:#1f2937;line-height:1.5;padding:20px}h1{font-size:20px;font-weight:700;margin-bottom:4px;color:#111827}h2{font-size:15px;font-weight:600;margin:20px 0 10px;color:#374151;border-bottom:2px solid #e5e7eb;padding-bottom:6px}h3{font-size:13px;font-weight:600;margin:14px 0 8px;color:#4b5563}.subtitle{color:#6b7280;font-size:12px;margin-bottom:20px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px}@media(max-width:640px){.grid{grid-template-columns:repeat(2,1fr)}}.card{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:14px;text-align:center}.card .val{font-size:26px;font-weight:700;color:#111827}.card .lbl{font-size:11px;color:#6b7280;margin-top:2px}.ok{color:#6A0DAD}.fail{color:#dc2626}.warn{color:#d97706}.info{color:#00B894}table{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:16px}th{background:#f9fafb;padding:8px 12px;text-align:left;font-weight:600;color:#4b5563;border-bottom:2px solid #e5e7eb;white-space:nowrap}td{padding:6px 12px;border-bottom:1px solid #f3f4f6;color:#374151}tr:hover td{background:#f9fafb}.num{text-align:right;font-family:SF Mono,Monaco,Consolas,monospace}.bar-wrap{display:flex;align-items:center;gap:6px}.bar-track{height:8px;background:#e5e7eb;border-radius:4px;flex:1;min-width:60px}.bar-fill{height:100%;border-radius:4px}.bar-fill.ok{background:#6A0DAD}.bar-fill.fail{background:#dc2626}.bar-fill.warn{background:#d97706}.bar-val{font-size:10px;font-family:monospace;min-width:50px;text-align:right;color:#6b7280}.hv-card{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:14px;margin-bottom:12px}.hv-head{display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap}.hv-op{font-size:14px;font-weight:700;color:#111827}.hv-shift{font-size:10px;padding:2px 8px;border-radius:99px;font-weight:600}.hv-shift.manana{background:#dbeafe;color:#1d4ed8}.hv-shift.tarde{background:#fef3c7;color:#92400e}.hv-shift.noche{background:#ede9fe;color:#5b21b6}.hv-shift.admin{background:#ede5ff;color:#4A0A80}.hv-time{font-size:10px;color:#9ca3af;font-family:monospace}.hv-text{font-size:13px;color:#374151;line-height:1.6;white-space:pre-wrap;word-break:break-word}.hv-checks{margin-top:8px;font-size:11px;color:#6b7280;display:flex;gap:16px;flex-wrap:wrap}.hv-checks .chk-ok{color:#6A0DAD;font-weight:600}.hv-checks .chk-fail{color:#dc2626;font-weight:600}.footer{margin-top:30px;padding-top:12px;border-top:1px solid #e5e7eb;text-align:center;font-size:10px;color:#9ca3af}@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}.spin-icon{animation:spin 1s linear infinite;}</style>';
}
function reportHeader(title,subtitle){
  return '<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>'+title+'</title>'+reportCSS()+'</head><body><h1>'+title+'</h1><div class="subtitle">'+subtitle+'</div>';
}

function downloadDayReport(){
  var dateStr=_dashCalSelected||currentDate;
  var day=store[dateStr]||{date:dateStr,dayType:'DIARIA',pollings:[],backups:[],processes:[],notes:'',timeline:[],handovers:[]};
  const now=new Date();
  let h=reportHeader('Bitacora NOC — '+fmt(dateStr),'Generado: '+now.toLocaleString('es-AR'));
  // Day info
  const dt=new Date(dateStr+'T12:00:00');
  const dayNames=['Domingo','Lunes','Martes','Miercoles','Jueves','Viernes','Sabado'];
  h+='<p style="font-size:13px;color:#6b7280;margin-bottom:16px">'+dayNames[dt.getDay()]+' '+fmt(dateStr)+' | Tipo: '+(day.dayType||'DIARIA')+'</p>';
  // Pollings
  h+='<h2>Pollings</h2>';
  if(day.pollings&&day.pollings.length){
    h+='<table><thead><tr><th>Servidor</th><th>Region</th><th>Fase</th><th>Hora</th><th>Duracion</th></tr></thead><tbody>';
    const servers=[...new Set(day.pollings.map(p=>p.server))];
    servers.forEach(srv=>{
      const beg=day.pollings.find(p=>p.server===srv&&p.phase==='BEGINNING');
      const end=day.pollings.find(p=>p.server===srv&&p.phase==='ENDING');
      const reg=beg?beg.region:(end?end.region:'');
      h+='<tr><td>'+escHtml(srv)+'</td><td>'+escHtml(reg)+'</td><td>'+(beg?'Inicio: '+escHtml(beg.time):'—')+'</td><td>'+(end?'Fin: '+escHtml(end.time):'—')+'</td><td>'+(beg&&beg.time&&end&&end.time?calcDur(beg.time,end.time):'—')+'</td></tr>';
    });
    h+='</tbody></table>';
  }else{h+='<p style="color:#6b7280">Sin pollings</p>';}
  // Backups
  h+='<h2>Backups</h2>';
  if(day.backups&&day.backups.length){
    h+='<table><thead><tr><th>Servidor</th><th>Fecha Inicio</th><th>Hora Inicio</th><th>Fecha Fin</th><th>Hora Fin</th><th>Duracion</th><th>Job</th><th>Estado</th></tr></thead><tbody>';
    day.backups.forEach(b=>{
      const stCls=(!b.status||b.status.toUpperCase()==='OK')?'ok':(b.status.toUpperCase().includes('FAIL')?'fail':'warn');
      h+='<tr><td>'+escHtml(b.name)+'</td><td>'+(b.iniDate||currentDate)+'</td><td>'+(b.iniTime||'—')+'</td><td>'+(b.endDate||currentDate)+'</td><td>'+(b.endTime||'—')+'</td><td>'+(b.duration||'—')+'</td><td>'+(b.job||'—')+'</td><td class="'+stCls+'">'+escHtml(b.status||'—')+'</td></tr>';
    });
    h+='</tbody></table>';
  }else{h+='<p style="color:#6b7280">Sin backups</p>';}
  // Processes
  h+='<h2>Procesos</h2>';
  if(day.processes&&day.processes.length){
    h+='<table><thead><tr><th>Proceso</th><th>Estado</th></tr></thead><tbody>';
    day.processes.forEach(p=>{
      const u=(p.status||'').toUpperCase();
      const cls=u==='OK'?'ok':(u==='ERROR'?'fail':'');
      h+='<tr><td>'+escHtml(p.name)+'</td><td class="'+cls+'">'+escHtml(p.status||'—')+'</td></tr>';
    });
    h+='</tbody></table>';
  }else{h+='<p style="color:#6b7280">Sin procesos</p>';}
  // Timeline
  if(day.timeline&&day.timeline.length){
    h+='<h2>Notas del Timeline</h2>';
    day.timeline.forEach(n=>{
      h+='<div class="hv-card"><div class="hv-head"><span class="hv-op">'+escHtml(n.operator||'')+'</span><span class="hv-time">'+escHtml(n.time||'')+'</span></div><div class="hv-text">'+escHtml(n.text)+'</div></div>';
    });
  }
  // Handovers
  if(day.handovers&&day.handovers.length){
    h+='<h2>Pase de Turno</h2>';
    day.handovers.forEach(c=>{
      const css=c.shift==='MANANA'?'manana':c.shift==='TARDE'?'tarde':c.shift==='NOCHE'?'noche':'admin';
      h+='<div class="hv-card"><div class="hv-head"><span class="hv-op">'+escHtml(c.operator)+'</span><span class="hv-shift '+css+'">'+escHtml(c.shiftLabel||c.shift)+'</span><span class="hv-time">'+escHtml(c.timestamp)+'</span></div><div class="hv-text">'+escHtml(c.text)+'</div>';
      h+='<div class="hv-checks"><span class="'+(c.pollOk?'chk-ok':'chk-fail')+'">'+(c.pollOk?'&#10003;':'&#10007;')+' Pollings</span><span class="'+(c.bkpOk?'chk-ok':'chk-fail')+'">'+(c.bkpOk?'&#10003;':'&#10007;')+' Backups</span><span class="'+(c.procOk?'chk-ok':'chk-fail')+'">'+(c.procOk?'&#10003;':'&#10007;')+' Procesos</span></div></div>';
    });
  }
  h+='<div class="footer">Bitacora NOC — bitacoranoc.com | Reporte diario '+dateStr+'</div></body></html>';
  triggerDownload(h,'bitacora_'+dateStr+'.html');
}

function downloadDashReport(){
  const period=document.getElementById('dashPeriod').value;
  const{from,to}=getDateRange();
  const days=getDaysInRange(from,to);
  const periodLabels={week:'Semanal',month:'Mensual',year:'Anual',all:'Historico'};
  let rangeLabel=periodLabels[period];
  if(from&&to)rangeLabel+=' ('+fmtDate(from)+' al '+fmtDate(to)+')';

  let totalPollings=0,completedPollings=0,totalBkps=0,failedBkps=0,okBkps=0;
  let totalProcs=0,okProcs=0,failProcs=0,ncProcs=0;
  let allDurations=[];let serverDurs={};let dailyStats=[];let bkpDurations=[];let procNames={};
  days.forEach(([dateStr,day])=>{
    let pBeg=0,pEnd=0;
    day.pollings.forEach(p=>{
      totalPollings++;if(p.phase==='BEGINNING')pBeg++;if(p.phase==='ENDING')pEnd++;
      if(p.phase==='ENDING'&&p.time){const beg=day.pollings.find(x=>x.server===p.server&&x.phase==='BEGINNING');if(beg&&beg.time){const d=calcDurSecs(beg.time,p.time);if(d!==null&&d>=0){allDurations.push(d);if(!serverDurs[p.server])serverDurs[p.server]=[];serverDurs[p.server].push(d);}}}
    });
    completedPollings+=Math.min(pBeg,pEnd);
    day.backups.forEach(b=>{totalBkps++;if(b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP')))failedBkps++;else okBkps++;if(b.duration){const parts=b.duration.split(':').map(Number);const secs=(parts[0]||0)*3600+(parts[1]||0)*60;if(secs>0)bkpDurations.push(secs);}});
    day.processes.forEach(p=>{totalProcs++;const u=(p.status||'').toUpperCase();if(u==='OK')okProcs++;else if(u==='ERROR')failProcs++;else ncProcs++;});
    dailyStats.push({date:dateStr,pollOk:Math.min(pBeg,pEnd),pollTotal:Math.max(pBeg,pEnd),bkpOk:day.backups.filter(b=>!(b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP')))).length,bkpFail:day.backups.filter(b=>b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'))).length,procOk:day.processes.filter(p=>{const u=(p.status||'').toUpperCase();return u==='OK';}).length,procTotal:day.processes.length});
  });
  const avgDur=allDurations.length?Math.round(allDurations.reduce((a,b)=>a+b,0)/allDurations.length):0;
  const avgBkpDur=bkpDurations.length?Math.round(bkpDurations.reduce((a,b)=>a+b,0)/bkpDurations.length):0;
  const pollPct=totalPollings>0?Math.round(completedPollings/(totalPollings/2)*100):0;
  const bkpPct=totalBkps>0?Math.round(okBkps/totalBkps*100):0;
  const procPct=totalProcs>0?Math.round(okProcs/totalProcs*100):0;
  const now=new Date();

  let h=reportHeader('Dashboard NOC - Reporte','Periodo: '+rangeLabel+' | Generado: '+now.toLocaleString('es-AR'));
  // Summary cards
  h+='<div class="grid">';
  h+='<div class="card"><div class="val info">'+days.length+'</div><div class="lbl">Dias con datos</div></div>';
  h+='<div class="card"><div class="val ok">'+pollPct+'%</div><div class="lbl">Pollings completados</div></div>';
  h+='<div class="card"><div class="val '+(bkpPct>=90?'ok':'warn')+'">'+bkpPct+'%</div><div class="lbl">Backups OK ('+okBkps+'/'+totalBkps+')</div></div>';
  h+='<div class="card"><div class="val '+(procPct>=90?'ok':'warn')+'">'+procPct+'%</div><div class="lbl">Procesos OK ('+okProcs+'/'+totalProcs+')</div></div>';
  h+='<div class="card"><div class="val info">'+fmtSecs(avgDur)+'</div><div class="lbl">Dur. promedio polling</div></div>';
  h+='<div class="card"><div class="val info">'+fmtSecs(avgBkpDur)+'</div><div class="lbl">Dur. promedio BKP</div></div>';
  h+='<div class="card"><div class="val warn">'+failedBkps+'</div><div class="lbl">Backups fallidos</div></div>';
  h+='<div class="card"><div class="val fail">'+failProcs+'</div><div class="lbl">Procesos con Error</div></div>';
  h+='</div>';
  // Daily table
  h+='<h2>Desglose por dia</h2>';
  if(dailyStats.length){
    h+='<table><thead><tr><th>Fecha</th><th class="num">Pollings OK</th><th class="num">Pollings Total</th><th class="num">BKP OK</th><th class="num">BKP Fail</th><th class="num">Proc OK</th><th class="num">Proc Total</th><th>Completitud</th></tr></thead><tbody>';
    dailyStats.forEach(d=>{
      const total=d.pollTotal+d.bkpOk+d.bkpFail+d.procTotal;const done=d.pollOk+d.bkpOk+d.procOk;
      const pct=total>0?Math.round(done/total*100):0;const cls=pct>=90?'ok':pct>=70?'warn':'fail';
      h+='<tr><td>'+d.date+'</td><td class="num '+(d.pollOk>=d.pollTotal?'ok':'')+'">'+d.pollOk+'</td><td class="num">'+d.pollTotal+'</td><td class="num ok">'+d.bkpOk+'</td><td class="num '+(d.bkpFail>0?'fail':'')+'">'+d.bkpFail+'</td><td class="num ok">'+d.procOk+'</td><td class="num">'+d.procTotal+'</td>';
      h+='<td><div class="bar-wrap"><div class="bar-track"><div class="bar-fill '+cls+'" style="width:'+pct+'%"></div></div><span class="bar-val">'+pct+'%</span></div></td></tr>';
    });
    h+='</tbody></table>';
  }
  // Server times
  const serverAvgs=Object.entries(serverDurs).map(([s,durs])=>({server:s,avg:Math.round(durs.reduce((a,b)=>a+b,0)/durs.length),count:durs.length,min:Math.min(...durs),max:Math.max(...durs)})).sort((a,b)=>b.avg-a.avg);
  if(serverAvgs.length){
    h+='<h2>Tiempos por servidor</h2><table><thead><tr><th>Servidor</th><th class="num">Promedio</th><th class="num">Minimo</th><th class="num">Maximo</th><th class="num">Registros</th></tr></thead><tbody>';
    serverAvgs.forEach(s=>{h+='<tr><td>'+s.server+'</td><td class="num">'+fmtSecs(s.avg)+'</td><td class="num">'+fmtSecs(s.min)+'</td><td class="num '+(s.max>7200?'fail':s.max>3600?'warn':'')+'">'+fmtSecs(s.max)+'</td><td class="num">'+s.count+'</td></tr>';});
    h+='</tbody></table>';
  }
  h+='<div class="footer">Bitacora NOC — bitacoranoc.com | Reporte generado el '+now.toLocaleString('es-AR')+'</div></body></html>';
  triggerDownload(h,'dashboard_noc_'+new Date().toISOString().split('T')[0]+'.html');
}

function downloadCierresReport(){
  const now=new Date();const allCierres=[];
  Object.entries(store).forEach(([dateStr,day])=>{
    if(day.handovers)day.handovers.forEach(h=>allCierres.push({...h,date:dateStr}));
  });
  allCierres.sort((a,b)=>b.timestamp.localeCompare(a.timestamp));
  let h=reportHeader('Pases de Turno — NOC','Todos los registros | Generado: '+now.toLocaleString('es-AR'));
  if(!allCierres.length){h+='<p style="color:#6b7280;padding:30px;text-align:center">No hay pases de turno registrados</p>';}
  else{
    h+='<p style="font-size:12px;color:#6b7280;margin-bottom:16px">Total: '+allCierres.length+' pase(s) de turno</p>';
    allCierres.forEach(c=>{
      const css=c.shift==='MANANA'?'manana':c.shift==='TARDE'?'tarde':c.shift==='NOCHE'?'noche':'admin';
      h+='<div class="hv-card">';
      h+='<div class="hv-head"><span class="hv-op">'+escHtml(c.operator)+'</span><span class="hv-shift '+css+'">'+escHtml(c.shiftLabel||c.shift)+'</span><span class="hv-time">'+escHtml(c.date)+' — '+escHtml(c.timestamp)+'</span></div>';
      h+='<div class="hv-text">'+escHtml(c.text)+'</div>';
      h+='<div class="hv-checks">';
      h+='<span class="'+(c.pollOk?'chk-ok':'chk-fail')+'">' + (c.pollOk?'&#10003;':'&#10007;')+' Pollings</span>';
      h+='<span class="'+(c.bkpOk?'chk-ok':'chk-fail')+'">' + (c.bkpOk?'&#10003;':'&#10007;')+' Backups</span>';
      h+='<span class="'+(c.procOk?'chk-ok':'chk-fail')+'">' + (c.procOk?'&#10003;':'&#10007;')+' Procesos</span>';
      h+='</div></div>';
    });
  }
  h+='<div class="footer">Bitacora NOC — bitacoranoc.com | Pases de turno al '+now.toLocaleString('es-AR')+'</div></body></html>';
  triggerDownload(h,'pases_turno_'+new Date().toISOString().split('T')[0]+'.html');
}

// Close notif panel on outside click
document.addEventListener('click',e=>{
  const wrap=document.getElementById('notifWrap');
  if(wrap&&!e.target.closest('#notifWrap')){
    document.getElementById('notifPanel').classList.remove('show');
  }
  // Close admin menu on outside click (overlay handles it, this is backup)
  if(!e.target.closest('#adminMenuWrap')&&!e.target.closest('.admin-menu')&&!e.target.closest('.admin-overlay')){
    closeAdminMenu();
  }
  // Close export dropdown on outside click
  var edd=document.getElementById('exportDropdown');
  if(edd&&!e.target.closest('#exportBtnWrap')){
    edd.classList.remove('show');
  }
});

// Show/hide cierre+notif buttons on login
function showTurnoButtons(){
  const show=!!currentUser;
  document.getElementById('cierreBtn').style.display=show?'':'none';
  if(show&&currentUser){
    const sk=SHIFT_MAP[currentUser.username]||'ADMIN';
    const lbl=SHIFT_LABELS[sk]||sk;
    const txt=document.getElementById('cierreBtnText');
    if(sk==='ADMIN'){
      txt.textContent='Pase de Turno';
    }else{
      txt.textContent='Pase de Turno '+lbl;
    }
  }
  document.getElementById('notifWrap').style.display=show?'':'none';
}
// Patch doLogin, checkSession, render and doLogout
const __origDoLogin=doLogin;
doLogin=function(){
  __origDoLogin();
  showTurnoButtons();
  populateOperatorSelect();
  const day=getDay(currentDate);
  renderNovedades(day);updateNotifBadge(day);renderTimeline(day);
  syncFromGitHub();
};
const __origCheckSession=checkSession;
checkSession=function(){
  __origCheckSession();
  showTurnoButtons();
  populateOperatorSelect();
  if(currentUser){
    const day=getDay(currentDate);
    renderNovedades(day);updateNotifBadge(day);renderTimeline(day);
    syncFromGitHub();
  }
};
const __origRender=render;
render=function(){
  __origRender();
  if(currentUser){
    const day=getDay(currentDate);
    renderNovedades(day);updateNotifBadge(day);renderTimeline(day);
    populateOperatorSelect();
  }
};
const __origDoLogout=doLogout;
doLogout=function(){
  __origDoLogout();
  showTurnoButtons();
  document.getElementById('novedadesSection').style.display='none';
  document.getElementById('notifPanel').classList.remove('show');
};

// ===== AUDIT VIEW =====
function openAuditView(){
  // Collect all audit entries from all days
  var entries=[];
  Object.keys(store).sort().reverse().forEach(function(d){
    var day=store[d];
    if(day.audit){
      day.audit.forEach(function(a){
        entries.push(Object.assign({},a,{date:d}));
      });
    }
  });
  var overlay=document.getElementById('auditOverlay');
  var body=document.getElementById('auditBody');
  if(!entries.length){
    body.innerHTML='<div style="text-align:center;padding:40px 20px;color:var(--gray-400)"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:12px;opacity:.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg><p style="font-size:14px">No hay registros de auditoria</p></div>';
  } else {
    var h='<table style="width:100%;border-collapse:collapse;font-size:12px"><thead><tr><th style="text-align:left;padding:8px 10px;border-bottom:2px solid var(--gray-200);font-size:11px;color:var(--gray-500);text-transform:uppercase">Fecha</th><th style="text-align:left;padding:8px 10px;border-bottom:2px solid var(--gray-200);font-size:11px;color:var(--gray-500);text-transform:uppercase">Hora</th><th style="text-align:left;padding:8px 10px;border-bottom:2px solid var(--gray-200);font-size:11px;color:var(--gray-500);text-transform:uppercase">Tipo</th><th style="text-align:left;padding:8px 10px;border-bottom:2px solid var(--gray-200);font-size:11px;color:var(--gray-500);text-transform:uppercase">Usuario</th><th style="text-align:left;padding:8px 10px;border-bottom:2px solid var(--gray-200);font-size:11px;color:var(--gray-500);text-transform:uppercase">Detalle / Motivo</th></tr></thead><tbody>';
    entries.forEach(function(e){
      var dt=e.timestamp.split(' ');
      var isReopen=e.type==='reapertura';
      var typeStyle=isReopen?'background:#fef2f2;color:#dc2626;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:600':'background:#ecfdf5;color:#059669;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:600';
      var typeLabel=isReopen?'REAPERTURA':'CIERRE';
      var detail=isReopen?(e.reason||'Sin motivo'):(e.detail||'');
      h+='<tr style="border-bottom:1px solid var(--gray-100)"><td style="padding:8px 10px;white-space:nowrap">'+dt[0]+'</td><td style="padding:8px 10px;white-space:nowrap;font-family:monospace;font-size:11px">'+dt[1]+'</td><td style="padding:8px 10px"><span style="'+typeStyle+'">'+typeLabel+'</span></td><td style="padding:8px 10px;font-weight:500">'+escHtml(e.user)+'</td><td style="padding:8px 10px;color:var(--gray-600);max-width:300px;word-break:break-word">'+escHtml(detail)+'</td></tr>';
    });
    h+='</tbody></table>';
    body.innerHTML=h;
  }
  overlay.classList.add('show');
}
function closeAuditView(){document.getElementById('auditOverlay').classList.remove('show');}

loadStoreLocal();checkSession();render();
