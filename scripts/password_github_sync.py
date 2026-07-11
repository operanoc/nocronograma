#!/usr/bin/env python3
"""Refactor password reset to use GitHub storage instead of localStorage.

Creates/updates data/passwords.json in the repo so all browsers share the same overrides.
On login and on app load, fetches passwords.json from GitHub and applies overrides.
"""

FILE = '/home/z/my-project/download/bitacora_noc_con_login.html'

with open(FILE, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the exact line ranges for the old password code
# Old functions to replace: _getPasswordOverrides, _savePasswordOverrides, _getEffectivePass,
#   openResetPassModal, resetPass, resetToDefault, the doLogin patch, and the init block

# Find start line of _getPasswordOverrides
start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if '_getPasswordOverrides()' in line and 'function _getPasswordOverrides' in lines[i-1] if i > 0 else False:
        pass
    # Find "function _getPasswordOverrides"
    if 'function _getPasswordOverrides' in line:
        start_idx = i
    # Find the end: the line after "loadStoreLocal();checkSession();render();" 
    # which is the last line before </script>
    if 'loadStoreLocal();checkSession();render();' in line:
        end_idx = i + 1  # include this line

print(f"Start idx: {start_idx}, End idx: {end_idx}")

if start_idx is None or end_idx is None:
    print("ERROR: Could not find boundaries")
    exit(1)

# Build the new replacement code
new_code = '''function _getPasswordOverrides(){return _passOverrides||{};}
function _setPasswordOverrides(o){_passOverrides=o;}
var _passOverrides=null;
var _passFileSHA=null;

// Fetch password overrides from GitHub (data/passwords.json)
async function ghFetchPasswords(){
  try{
    const path='data/passwords.json';
    const resp=await fetch(GH_API+'/'+path+'?ref='+GH_CONFIG.branch,{headers:GH_HEADERS});
    if(resp.status===404){_passOverrides={};_passFileSHA=null;return;}
    if(!resp.ok)return;
    const data=await resp.json();
    _passFileSHA=data.sha;
    const parsed=JSON.parse(decodeURIComponent(escape(atob(data.content))));
    _passOverrides=parsed;
    // Apply to USERS in memory
    _applyPasswordOverrides();
  }catch(e){console.warn('Failed to fetch passwords',e);}
}

// Push password overrides to GitHub (data/passwords.json)
async function ghPushPasswords(){
  if(!_passOverrides)return;
  try{
    const path='data/passwords.json';
    const content=utf8ToBase64(JSON.stringify(_passOverrides,null,2));
    const body={message:'passwords: actualizar contrase\u00f1as',content:content,branch:GH_CONFIG.branch};
    if(_passFileSHA)body.sha=_passFileSHA;
    const resp=await fetch(GH_API+'/'+path,{method:'PUT',headers:GH_HEADERS,body:JSON.stringify(body)});
    if(!resp.ok){console.warn('Failed to push passwords',await resp.text());return;}
    const data=await resp.json();
    _passFileSHA=data.content.sha;
  }catch(e){console.warn('Failed to push passwords',e);}
}

function _applyPasswordOverrides(){
  var overrides=_getPasswordOverrides();
  var keys=Object.keys(overrides);
  for(var i=0;i<keys.length;i++){
    if(USERS[keys[i]]){USERS[keys[i]].pass=overrides[keys[i]];}
  }
}

function _getEffectivePass(username){
  var overrides=_getPasswordOverrides();
  if(overrides&&overrides[username])return overrides[username];
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
    h+='</div><div class=\\"resetpass-hint\\">Las contrase\\u00f1as se sincronizan con GitHub (todos los navegadores).</div>';

    document.getElementById('modalTitle').textContent='Blanquear / Cambiar Contrase\\u00f1as';
    document.getElementById('modalBody').innerHTML=h;
    document.getElementById('modalFooter').innerHTML='<button class=\\"btn btn-outline\\" onclick=\\"closeModal()\\">Cerrar</button>';
    openModal();
  });
}

async function resetPass(username){
  var input=document.getElementById('rpinput_'+username);
  if(!input)return;
  var newPass=input.value.trim();
  if(!newPass){
    toast('Ingrese una contrase\\u00f1a','warn');
    return;
  }
  if(newPass.length<4){
    toast('M\\u00ednimo 4 caracteres','warn');
    return;
  }
  var overrides=_getPasswordOverrides();
  overrides[username]=newPass;
  _setPasswordOverrides(overrides);
  USERS[username].pass=newPass;
  // Sync to GitHub
  await ghPushPasswords();
  toast('Contrase\\u00f1a de '+username+' actualizada y sincronizada');
  openResetPassModal();
}

async function resetToDefault(username){
  var u=USERS[username];
  if(!u)return;
  var defaultPass='Atos.123$';
  var overrides=_getPasswordOverrides();
  if(overrides&&overrides[username]){
    delete overrides[username];
    _setPasswordOverrides(overrides);
  }
  if(u.role==='operator'){
    u.pass=defaultPass;
  }
  // Sync to GitHub
  await ghPushPasswords();
  toast('Contrase\\u00f1a de '+username+' restaurada y sincronizada');
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
    document.getElementById('loginError').textContent='Usuario o contrase\\u00f1a incorrectos';
    document.getElementById('loginPass').value='';
    return;
  }
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

// On load, fetch password overrides from GitHub
(async function(){
  await ghFetchPasswords();
  loadStoreLocal();checkSession();render();
})();

'''

# Replace the old block
new_lines = lines[:start_idx] + [new_code] + lines[end_idx:]

with open(FILE, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("SUCCESS: Password system now uses GitHub storage")
print(f"Old block: lines {start_idx+1}-{end_idx}")
print(f"New file: {len(new_lines)} lines")