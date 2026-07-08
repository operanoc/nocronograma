#!/usr/bin/env python3
"""
Genera la bitácora NOC con sistema de login (4 usuarios) y dashboard admin.
Usa marcadores HTML confiables (</style>, </head>, <body>, </main>, </script>)
en lugar de reemplazo de cadenas de código.
"""

import html as html_mod

ORIG = "/home/z/my-project/upload/index.html"
OUT  = "/home/z/my-project/download/bitacora_noc_con_login.html"

with open(ORIG, "r", encoding="utf-8") as f:
    content = f.read()

# ============================================================
# 1. CSS: Login screen + Dashboard styles
# ============================================================
login_css = """
/* ===== LOGIN SCREEN ===== */
.login-overlay{position:fixed;inset:0;background:linear-gradient(135deg,#0f172a 0%,#1e293b 50%,#0f172a 100%);z-index:9999;display:flex;align-items:center;justify-content:center;transition:opacity .4s}
.login-overlay.hide{opacity:0;pointer-events:none}
.login-box{background:var(--white,#fff);border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.3);width:100%;max-width:400px;padding:40px 32px;text-align:center}
.login-box .login-logo{display:flex;align-items:center;justify-content:center;gap:10px;margin-bottom:24px}
.login-box .login-logo svg{color:#059669;width:28px;height:28px}
.login-box .login-logo h2{font-size:20px;font-weight:700;color:#1f2937}
.login-box p.sub{color:#6b7280;font-size:13px;margin-bottom:24px}
.login-box .form-group{text-align:left;margin-bottom:14px}
.login-box .form-group label{display:block;font-size:12px;font-weight:600;color:#374151;margin-bottom:4px}
.login-box .form-group input{width:100%;padding:10px 14px;border:1px solid #d1d5db;border-radius:8px;font-size:14px;outline:none;transition:border .15s,box-shadow .15s}
.login-box .form-group input:focus{border-color:#0284c7;box-shadow:0 0 0 3px rgba(2,132,199,.15)}
.login-box .btn-login{width:100%;padding:12px;background:#059669;color:#fff;border:none;border-radius:8px;font-size:15px;font-weight:600;cursor:pointer;transition:background .15s}
.login-box .btn-login:hover{background:#047857}
.login-box .login-error{color:#dc2626;font-size:12px;margin-top:10px;min-height:18px}
.login-box .login-hint{color:#9ca3af;font-size:11px;margin-top:16px}
.login-shift-badge{display:inline-block;padding:3px 10px;border-radius:99px;font-size:11px;font-weight:600;margin-top:4px}

/* ===== USER BAR IN HEADER ===== */
.user-bar{display:flex;align-items:center;gap:8px}
.user-bar .user-name{font-size:12px;font-weight:600;color:var(--gray-700)}
.user-bar .shift-badge{font-size:10px;padding:2px 8px;border-radius:99px;font-weight:600}
.shift-manana{background:#dbeafe;color:#1d4ed8}
.shift-tarde{background:#fef3c7;color:#92400e}
.shift-noche{background:#ede9fe;color:#5b21b6}
.shift-admin{background:#d1fae5;color:#065f46}
.btn-logout{font-size:11px;color:var(--gray-500);padding:4px 8px;border-radius:6px}
.btn-logout:hover{background:var(--red-50);color:var(--red-600)}

/* ===== ADMIN DASHBOARD ===== */
.dashboard-overlay{position:fixed;inset:0;background:var(--bg);z-index:500;display:none;flex-direction:column;overflow:hidden}
.dashboard-overlay.show{display:flex}
.dash-header{background:var(--white);border-bottom:1px solid var(--gray-200);padding:10px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;flex-shrink:0}
.dash-header h2{font-size:17px;font-weight:700;display:flex;align-items:center;gap:8px;color:var(--gray-800)}
.dash-controls{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.dash-controls select,.dash-controls button{font-size:12px;padding:6px 12px;border-radius:var(--radius);border:1px solid var(--gray-300);background:var(--white);color:var(--gray-700);cursor:pointer}
.dash-controls select:focus{border-color:var(--sky-600)}
.dash-controls .btn-dash-active{background:var(--emerald-600);color:#fff;border-color:var(--emerald-600)}
.dash-body{flex:1;overflow-y:auto;padding:20px;max-width:1400px;margin:0 auto;width:100%}
.dash-summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:20px}
.dash-stat{background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);padding:16px;text-align:center;transition:background .3s}
.dash-stat .dash-val{font-size:28px;font-weight:700;color:var(--gray-900)}
.dash-stat .dash-lbl{font-size:11px;color:var(--gray-500);margin-top:4px}
.dash-stat.dash-ok .dash-val{color:#059669}
.dash-stat.dash-fail .dash-val{color:#dc2626}
.dash-stat.dash-warn .dash-val{color:#d97706}
.dash-stat.dash-info .dash-val{color:#0284c7}
.dash-section{background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);margin-bottom:16px;overflow:hidden;transition:background .3s}
.dash-section-header{padding:12px 16px;border-bottom:1px solid var(--gray-200);display:flex;align-items:center;justify-content:space-between}
.dash-section-header h3{font-size:14px;font-weight:600;color:var(--gray-800)}
.dash-table{width:100%;border-collapse:collapse;font-size:12px}
.dash-table th{background:var(--gray-50);padding:8px 12px;text-align:left;font-weight:600;color:var(--gray-600);border-bottom:2px solid var(--gray-200);white-space:nowrap}
.dash-table td{padding:6px 12px;border-bottom:1px solid var(--gray-100);color:var(--gray-700);white-space:nowrap}
.dash-table tr:hover td{background:var(--gray-50)}
.dash-table .num{text-align:right;font-family:'SF Mono',Monaco,Consolas,monospace}
.dash-table .ok-cell{color:#059669;font-weight:600}
.dash-table .fail-cell{color:#dc2626;font-weight:600}
.dash-table .warn-cell{color:#d97706;font-weight:600}
.dash-empty{text-align:center;padding:30px;color:var(--gray-400);font-size:13px}
.dash-pct-bar{height:6px;background:var(--gray-200);border-radius:3px;overflow:hidden;min-width:80px}
.dash-pct-fill{height:100%;border-radius:3px;transition:width .3s}
.dash-pct-fill.ok-fill{background:#059669}
.dash-pct-fill.fail-fill{background:#dc2626}
.dash-pct-fill.warn-fill{background:#d97706}
.dash-chart-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-bottom:16px}
.dash-chart-card{background:var(--white);border:1px solid var(--gray-200);border-radius:var(--radius);padding:16px;transition:background .3s}
.dash-chart-card h4{font-size:13px;font-weight:600;color:var(--gray-700);margin-bottom:12px}
.dash-bar-chart{display:flex;flex-direction:column;gap:6px}
.dash-bar-row{display:flex;align-items:center;gap:8px}
.dash-bar-label{font-size:11px;color:var(--gray-600);min-width:120px;max-width:150px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.dash-bar-track{flex:1;height:16px;background:var(--gray-100);border-radius:3px;overflow:hidden;position:relative}
.dash-bar-fill{height:100%;border-radius:3px;transition:width .3s;min-width:2px}
.dash-bar-val{font-size:10px;font-family:'SF Mono',Monaco,Consolas,monospace;color:var(--gray-500);min-width:50px;text-align:right}
@media(max-width:640px){.dash-body{padding:12px}.dash-summary{grid-template-columns:repeat(2,1fr)}.dash-chart-row{grid-template-columns:1fr}.dash-bar-label{min-width:80px}}
"""

# Insert login+dashboard CSS before </style>
content = content.replace("</style>", login_css + "\n</style>", 1)

# ============================================================
# 2. HTML: Login overlay (after <body>)
# ============================================================
login_html = """
<!-- LOGIN SCREEN -->
<div class="login-overlay" id="loginOverlay">
  <div class="login-box">
    <div class="login-logo">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>
      <h2>Bitacora NOC</h2>
    </div>
    <p class="sub">Ingresar usuario y contrasena para continuar</p>
    <div class="form-group">
      <label>Usuario</label>
      <input type="text" id="loginUser" autocomplete="off" spellcheck="false">
    </div>
    <div class="form-group">
      <label>Contrasena</label>
      <input type="password" id="loginPass" autocomplete="off">
    </div>
    <button class="btn-login" onclick="doLogin()">Ingresar</button>
    <div class="login-error" id="loginError"></div>
    <div class="login-hint">NOC Operations Center</div>
  </div>
</div>

<!-- ADMIN DASHBOARD -->
<div class="dashboard-overlay" id="dashOverlay">
  <div class="dash-header">
    <h2>
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      Dashboard Admin
    </h2>
    <div class="dash-controls">
      <select id="dashPeriod" onchange="renderDashboard()">
        <option value="week">Semanal</option>
        <option value="month" selected>Mensual</option>
        <option value="year">Anual</option>
        <option value="all">Historico</option>
      </select>
      <button class="btn-dash-active" onclick="renderDashboard()">Actualizar</button>
      <button onclick="closeDashboard()" style="background:var(--gray-200);font-weight:600">Cerrar Dashboard</button>
    </div>
  </div>
  <div class="dash-body" id="dashBody"></div>
</div>
"""

content = content.replace("<body>\n", "<body>\n" + login_html, 1)

# ============================================================
# 3. HTML: Add user bar + dashboard button to header
# ============================================================
old_header_actions = '''    <div class="header-actions">
      <button class="btn btn-ghost btn-sm" onclick="window.print()" title="Imprimir">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
      </button>
      <button class="btn btn-ghost btn-sm" id="darkToggle" onclick="toggleDark()" title="Modo oscuro">
        <svg id="darkIcon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
    </div>'''

new_header_actions = '''    <div class="header-actions">
      <button class="btn btn-ghost btn-sm" id="dashBtn" onclick="openDashboard()" title="Dashboard" style="display:none">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      </button>
      <div class="user-bar" id="userBar" style="display:none">
        <span class="user-name" id="userNameDisplay"></span>
        <span class="shift-badge" id="userShiftBadge"></span>
        <button class="btn btn-logout" onclick="doLogout()">Salir</button>
      </div>
      <button class="btn btn-ghost btn-sm" onclick="window.print()" title="Imprimir">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
      </button>
      <button class="btn btn-ghost btn-sm" id="darkToggle" onclick="toggleDark()" title="Modo oscuro">
        <svg id="darkIcon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      </button>
    </div>'''

content = content.replace(old_header_actions, new_header_actions, 1)

# ============================================================
# 4. JS: Login system + Dashboard logic (before </script>)
# ============================================================

auth_js = r"""
// ===== AUTH SYSTEM =====
const USERS={
  OPERANOCHE:{pass:'noche1',shift:'TURNO NOCHE',cssClass:'shift-noche',role:'operator'},
  OPERAMANANA:{pass:'manana1',shift:'TURNO MANANA',cssClass:'shift-manana',role:'operator'},
  OPERATARDE:{pass:'tarde1',shift:'TURNO TARDE',cssClass:'shift-tarde',role:'operator'},
  OPERAADMIN:{pass:'nocadmin',shift:'ADMIN',cssClass:'shift-admin',role:'admin'}
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
  document.getElementById('loginOverlay').classList.add('hide');
  document.getElementById('userBar').style.display='flex';
  document.getElementById('userNameDisplay').textContent=u;
  const badge=document.getElementById('userShiftBadge');
  badge.textContent=user.shift;
  badge.className='shift-badge '+user.cssClass;
  if(user.role==='admin'){
    document.getElementById('dashBtn').style.display='';
  }
  document.getElementById('loginError').textContent='';
}
function doLogout(){
  currentUser=null;
  sessionStorage.removeItem('bitacora_user');
  document.getElementById('loginOverlay').classList.remove('hide');
  document.getElementById('userBar').style.display='none';
  document.getElementById('dashBtn').style.display='none';
  document.getElementById('loginUser').value='';
  document.getElementById('loginPass').value='';
}
function checkSession(){
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
      document.getElementById('dashBtn').style.display='';
    }
  }
}
document.getElementById('loginPass').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin();});
document.getElementById('loginUser').addEventListener('keydown',e=>{if(e.key==='Enter')document.getElementById('loginPass').focus();});
checkSession();

// ===== ADMIN DASHBOARD =====
function openDashboard(){
  if(!currentUser||currentUser.role!=='admin')return;
  document.getElementById('dashOverlay').classList.add('show');
  renderDashboard();
}
function closeDashboard(){
  document.getElementById('dashOverlay').classList.remove('show');
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
function fmtDate(d){return d.toISOString().split('T')[0];}
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
  const body=document.getElementById('dashBody');
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
      if(u==='OK'||u==='REALIZADO')okProcs++;
      else if(u==='N/A'||u==='N/C')ncProcs++;
      else if(u===''||u==='PEND REGIONAL')ncProcs++;
      else failProcs++;
      if(p.name)procNames[p.name]=(procNames[p.name]||0)+1;
    });

    dailyStats.push({
      date:dateStr,
      pollCompleted:Math.min(dayPollBeg,dayPollEnd),
      pollTotal:Math.max(dayPollBeg,dayPollEnd),
      bkpOk:day.backups.filter(b=>!(b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP')))).length,
      bkpFail:day.backups.filter(b=>b.status&&(b.status.toUpperCase().includes('FAIL')||b.status.toUpperCase().includes('SUSP'))).length,
      procOk:day.processes.filter(p=>{const u=(p.status||'').toUpperCase();return u==='OK'||u==='REALIZADO';}).length,
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
  h+='<div class="dash-stat dash-fail"><div class="dash-val">'+failProcs+'</div><div class="dash-lbl">Procesos fallidos</div></div>';
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
    h+='<div class="dash-bar-row"><span class="dash-bar-label" title="'+s.server+'">'+s.server+'</span><div class="dash-bar-track"><div class="dash-bar-fill" style="width:'+pct+'%;background:#059669"></div></div><span class="dash-bar-val">'+fmtSecs(s.avg)+'</span></div>';
  });
  if(!topFast.length)h+='<div class="dash-empty">Sin datos</div>';
  h+='</div></div>';
  h+='</div>';

  // Process status chart
  const procOkPct=totalProcs>0?Math.round(okProcs/totalProcs*100):0;
  const procNcPct=totalProcs>0?Math.round(ncProcs/totalProcs*100):0;
  const procFailPct=totalProcs>0?100-procOkPct-procNcPct:0;
  h+='<div class="dash-chart-row">';
  h+='<div class="dash-chart-card"><h4>Estado de Procesos</h4>';
  h+='<div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#059669">'+procOkPct+'%</div><div style="font-size:11px;color:var(--gray-500)">OK / Realizado ('+okProcs+')</div></div>';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#d97706">'+procNcPct+'%</div><div style="font-size:11px;color:var(--gray-500)">N/A / N/C ('+ncProcs+')</div></div>';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#dc2626">'+procFailPct+'%</div><div style="font-size:11px;color:var(--gray-500)">Fallidos ('+failProcs+')</div></div>';
  h+='</div></div>';
  // Backup status chart
  h+='<div class="dash-chart-card"><h4>Estado de Backups</h4>';
  h+='<div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">';
  h+='<div style="text-align:center"><div style="font-size:32px;font-weight:700;color:#059669">'+okBkps+'</div><div style="font-size:11px;color:var(--gray-500)">Completados</div></div>';
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
"""

# Insert auth+dashboard JS before the final loadStore();render();
# We replace "loadStore();render();" with the auth code + "loadStore();render();"
content = content.replace(
    "loadStore();render();\n</script>",
    auth_js + "\nloadStore();render();\n</script>",
    1
)

# ============================================================
# 5. Write output
# ============================================================
with open(OUT, "w", encoding="utf-8") as f:
    f.write(content)

print(f"OK: {OUT}")
print(f"Size: {len(content)} bytes")

# Verify key elements exist
checks = [
    "loginOverlay",
    "doLogin",
    "doLogout",
    "USERS",
    "dashOverlay",
    "renderDashboard",
    "openDashboard",
    "OPERANOCHE",
    "OPERAMANANA",
    "OPERATARDE",
    "OPERAADMIN",
    "dashPeriod",
    "serverDurs",
    "dailyStats",
]
for c in checks:
    found = c in content
    print(f"  {'OK' if found else 'FAIL'}: {c}")