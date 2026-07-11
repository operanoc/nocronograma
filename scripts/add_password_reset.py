#!/usr/bin/env python3
"""Add password reset feature for admin.

1. Add menu item "Blanquear contrase\u00f1as" in admin menu
2. Add CSS for the password reset form
3. Add JS functions: openResetPassModal, resetPassword
4. Store custom passwords in localStorage as override (USERS stays as default)
"""

FILE = '/home/z/my-project/download/bitacora_noc_con_login.html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

# === 1. Add menu item in admin menu (before the closing </div> of admin-menu) ===
menu_btn = '''  <button class="menu-item" onclick="openResetPassModal();closeAdminMenu()"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/><circle cx="12" cy="16" r="1"/></svg> Blanquear contrase\u00f1as</button>
</div>'''

old_menu_end = '''  <button class="menu-item" onclick="document.getElementById('xlsxImportInput').click();closeAdminMenu()"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg> Importar XLSX</button>
</div>'''

if old_menu_end not in content:
    print("ERROR: Could not find admin menu end")
    exit(1)

content = content.replace(old_menu_end, menu_btn, 1)
print("1. Added menu item")

# === 2. Add CSS for password reset form (before </style>) ===
css_block = """
.resetpass-list{max-height:320px;overflow-y:auto;display:flex;flex-direction:column;gap:6px;margin-bottom:16px}
.resetpass-row{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--gray-100);border-radius:8px;border:1px solid var(--gray-200);transition:border-color .15s}
.resetpass-row:hover{border-color:var(--emerald-600)}
.resetpass-info{display:flex;flex-direction:column;gap:2px}
.resetpass-user{font-weight:600;font-size:13px;color:var(--gray-900)}
.resetpass-name{font-size:11px;color:var(--gray-500)}
.resetpass-role{font-size:10px;padding:1px 8px;border-radius:99px;font-weight:600}
.resetpass-role.op{background:rgba(0,229,184,.12);color:var(--sky-600)}
.resetpass-role.adm{background:rgba(168,85,247,.12);color:var(--emerald-600)}
.resetpass-actions{display:flex;gap:6px;align-items:center}
.resetpass-input{width:130px;padding:6px 10px;font-size:12px;border:1px solid var(--gray-200);border-radius:6px;background:var(--white);color:var(--gray-900);outline:none;transition:border-color .15s}
.resetpass-input:focus{border-color:var(--emerald-600)}
.resetpass-apply{padding:6px 12px;font-size:11px;font-weight:600;border:none;border-radius:6px;cursor:pointer;transition:all .15s;background:var(--emerald-600);color:#fff}
.resetpass-apply:hover{opacity:.85}
.resetpass-apply:disabled{opacity:.4;cursor:not-allowed}
.resetpass-reset{padding:6px 10px;font-size:11px;font-weight:500;border:1px solid var(--gray-200);border-radius:6px;cursor:pointer;background:transparent;color:var(--gray-500);transition:all .15s}
.resetpass-reset:hover{border-color:var(--gray-400);color:var(--gray-700)}
.resetpass-hint{text-align:center;font-size:11px;color:var(--gray-500);margin-top:4px}
"""

style_close = "</style>"
if style_close not in content:
    print("ERROR: </style> not found")
    exit(1)

content = content.replace(style_close, css_block + style_close, 1)
print("2. Added CSS")

# === 3. Add JS functions before the final loadStoreLocal line ===
js_functions = """
// ===== PASSWORD RESET (ADMIN) =====
function _getPasswordOverrides(){
  try{return JSON.parse(localStorage.getItem('bitacora_pass_overrides'))||{};}catch(e){return{};}
}
function _savePasswordOverrides(overrides){
  try{localStorage.setItem('bitacora_pass_overrides',JSON.stringify(overrides));}catch(e){}
}
function _getEffectivePass(username){
  var overrides=_getPasswordOverrides();
  if(overrides[username])return overrides[username];
  var u=USERS[username];
  return u?u.pass:null;
}

function openResetPassModal(){
  _adminGate(function(){
    var h='<div class=\\"resetpass-list\\">';
    var keys=Object.keys(USERS).sort();
    for(var i=0;i<keys.length;i++){
      var k=keys[i];
      var u=USERS[k];
      var isOp=u.role==='operator';
      var roleClass=isOp?'op':'adm';
      var roleLabel=isOp?'Operador':'Admin';
      var name=u.name||k;
      var currentPass=_getEffectivePass(k);
      var masked=currentPass?('\\u2022'.repeat(Math.min(currentPass.length,8))):'---';
      h+='<div class=\\"resetpass-row\\" id=\\"rprow_'+k+'\\">'
        +'<div class=\\"resetpass-info\\">'
        +'<span class=\\"resetpass-user\\">'+k+'</span>'
        +'<span class=\\"resetpass-name\\">'+escHtml(name)+'</span>'
        +'<span class=\\"resetpass-role '+roleClass+'\\">'+roleLabel+'</span>'
        +'</div>'
        +'<div class=\\"resetpass-actions\\">'
        +'<span style=\\"font-size:11px;color:var(--gray-400);margin-right:4px\\">Actual: '+masked+'</span>'
        +'<input class=\\"resetpass-input\\" type=\\"password\\" id=\\"rpinput_'+k+'\\" placeholder=\\"Nueva contrase\u00f1a\\" onkeydown=\\"if(event.key===\\'Enter\\')resetPass(\\''+k+'\\')\\">'
        +'<button class=\\"resetpass-apply\\" onclick=\\"resetPass(\\''+k+'\\')\\">Guardar</button>'
        +(currentPass&&!isOp?'':'<button class=\\"resetpass-reset\\" onclick=\\"resetToDefault(\\''+k+'\\')\\">Blanquear</button>')
        +'</div></div>';
    }
    h+='</div><div class=\\"resetpass-hint\\">Las contrase\u00f1as se guardan localmente en este navegador.</div>';

    document.getElementById('modalTitle').textContent='Blanquear / Cambiar Contrase\u00f1as';
    document.getElementById('modalBody').innerHTML=h;
    document.getElementById('modalFooter').innerHTML='<button class=\\"btn btn-outline\\" onclick=\\"closeModal()\\">Cerrar</button>';
    openModal();
  });
}

function resetPass(username){
  var input=document.getElementById('rpinput_'+username);
  if(!input)return;
  var newPass=input.value.trim();
  if(!newPass){
    toast('Ingrese una contrase\u00f1a','warn');
    return;
  }
  if(newPass.length<4){
    toast('M\u00ednimo 4 caracteres','warn');
    return;
  }
  var overrides=_getPasswordOverrides();
  overrides[username]=newPass;
  _savePasswordOverrides(overrides);
  USERS[username].pass=newPass;
  toast('Contrase\u00f1a de '+username+' actualizada');
  // Refresh modal to show updated masked password
  openResetPassModal();
}

function resetToDefault(username){
  var u=USERS[username];
  if(!u)return;
  // Default passwords: operators -> Atos.123$, others keep whatever they had originally
  var defaultPass='Atos.123$';
  var overrides=_getPasswordOverrides();
  if(overrides[username]){
    delete overrides[username];
    _savePasswordOverrides(overrides);
  }
  // For operators we know the default. For admins we can't really "reset" to a known default
  // so we just remove the override - the code-level default stays.
  // But we DO set operators to the known default
  if(u.role==='operator'){
    u.pass=defaultPass;
  }
  toast('Contrase\u00f1a de '+username+' restaurada');
  openResetPassModal();
}

// Patch doLogin to use _getEffectivePass instead of USERS[u].pass
const __origDoLogin2=doLogin;
doLogin=function(){
  var u=document.getElementById('loginUser').value.trim().toUpperCase();
  var p=document.getElementById('loginPass').value;
  var user=USERS[u];
  var effectivePass=_getEffectivePass(u);
  if(!user||p!==effectivePass){
    document.getElementById('loginError').textContent='Usuario o contrase\u00f1a incorrectos';
    document.getElementById('loginPass').value='';
    return;
  }
  // Credentials valid, proceed with original logic (shift selection etc)
  if(user.role==='operator'){
    var avail=getOperatorAvailableShifts(u);
    if(avail.length>1){
      document.getElementById('loginOverlay').classList.add('hide');
      showShiftSelector(u);
      return;
    }
  }
  enterApp(u);
};
"""

# Insert before the final "loadStoreLocal();checkSession();render();"
target = "loadStoreLocal();checkSession();render();"
if target not in content:
    print("ERROR: target not found")
    exit(1)

content = content.replace(target, js_functions + target, 1)
print("3. Added JS functions")

# === 4. Also need to load overrides on startup so USERS is up to date ===
# Add an init block that restores passwords from localStorage into USERS object
init_block = """
// Restore password overrides into USERS on load
(function(){
  var overrides=_getPasswordOverrides();
  var keys=Object.keys(overrides);
  for(var i=0;i<keys.length;i++){
    if(USERS[keys[i]]){USERS[keys[i]].pass=overrides[keys[i]];}
  }
})();
"""

content = content.replace(target, init_block + target, 1)
print("4. Added init block for password overrides")

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nAll changes applied successfully!")