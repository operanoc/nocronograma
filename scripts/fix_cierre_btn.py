#!/usr/bin/env python3
"""Fix: cierreBtn not showing for operators who go through shift selector.

Problem: The patched doLogin calls showTurnoButtons() after __origDoLogin(),
but when an operator has multiple shifts, __origDoLogin() shows the shift
selector and returns WITHOUT calling enterApp(). So currentUser is still null
when showTurnoButtons() runs.

Additionally, selectShift() calls enterApp() but never calls showTurnoButtons()
or the other post-login helpers (populateOperatorSelect, renderNovedades, etc).

Fix: Patch enterApp() to call showTurnoButtons + helpers at the end.
This covers ALL login paths: direct, shift selector, and session restore.
"""

FILE = '/home/z/my-project/download/bitacora_noc_con_login.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# The current patch section that we need to replace
old_patch = """// Patch doLogin, checkSession, render and doLogout
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
};"""

new_patch = """// Post-login helpers (called after enterApp succeeds)
function _postLogin(){
  showTurnoButtons();
  populateOperatorSelect();
  if(currentUser){
    const day=getDay(currentDate);
    renderNovedades(day);updateNotifBadge(day);renderTimeline(day);
    syncFromGitHub();
  }
}

// Patch enterApp so post-login runs for ALL login paths
const __origEnterApp=enterApp;
enterApp=function(username,forceShift){
  __origEnterApp(username,forceShift);
  _postLogin();
};

// Patch doLogin (single-shift operators go straight to enterApp, already covered)
const __origDoLogin=doLogin;
doLogin=function(){
  __origDoLogin();
  // If currentUser is set here, enterApp was called inside __origDoLogin
  // and _postLogin already ran via the enterApp patch above.
  // Multi-shift path: __origDoLogin shows shift selector and returns,
  // _postLogin will run after selectShift->enterApp.
};

// Patch checkSession (session restore)
const __origCheckSession=checkSession;
checkSession=function(){
  __origCheckSession();
  // enterApp is called inside __origCheckSession, so _postLogin ran already
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
};"""

if old_patch not in content:
    print("ERROR: Could not find the old patch block!")
    # Show context around "Patch doLogin" for debugging
    idx = content.find('// Patch doLogin')
    if idx >= 0:
        print(f"Found '// Patch doLogin' at index {idx}")
        print("Context around it:")
        print(repr(content[idx:idx+500]))
    else:
        print("Could not find '// Patch doLogin' at all!")
    exit(1)

content = content.replace(old_patch, new_patch, 1)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: Patched enterApp to call _postLogin() for all login paths.")