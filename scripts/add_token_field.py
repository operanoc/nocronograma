#!/usr/bin/env python3
"""Add GitHub token input to login form and make token dynamic (sessionStorage)."""

SRC = '/home/z/my-project/download/bitacora_noc_con_login.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. Add token field in login form (before the login button)
# ============================================================
old_login_btn = '''    <button class="btn-login" onclick="doLogin()">Ingresar</button>'''

new_login_btn = '''    <div class="form-group">
      <label>Token GitHub</label>
      <input type="password" id="loginToken" autocomplete="off" placeholder="ghp_xxxx...">
    </div>
    <button class="btn-login" onclick="doLogin()">Ingresar</button>'''

html = html.replace(old_login_btn, new_login_btn)

# ============================================================
# 2. Replace hardcoded token in GH_CONFIG with placeholder
# ============================================================
html = html.replace(
    "  token:'[REDACTED:github_token]',",
    "  token:'',"
)

# ============================================================
# 3. Add refreshGHHeaders() and token persistence after GH_HEADERS
# ============================================================
old_headers = """const GH_HEADERS={
  'Authorization':'Bearer '+GH_CONFIG.token,
  'Accept':'application/vnd.github.v3+json',
  'Content-Type':'application/json'
};"""

new_headers = """function refreshGHHeaders(){
  GH_HEADERS={
    'Authorization':'Bearer '+GH_CONFIG.token,
    'Accept':'application/vnd.github.v3+json',
    'Content-Type':'application/json'
  };
}
let GH_HEADERS={};
refreshGHHeaders();"""

html = html.replace(old_headers, new_headers)

# ============================================================
# 4. Modify doLogin to capture token and refresh headers
# ============================================================
old_dologin_end = """  currentUser={username:u,...user};
  sessionStorage.setItem('bitacora_user',u);
  document.getElementById('loginOverlay').classList.add('hide');"""

new_dologin_end = """  currentUser={username:u,...user};
  sessionStorage.setItem('bitacora_user',u);
  const tk=document.getElementById('loginToken').value.trim();
  if(tk){sessionStorage.setItem('gh_token',tk);GH_CONFIG.token=tk;refreshGHHeaders();}
  document.getElementById('loginOverlay').classList.add('hide');"""

html = html.replace(old_dologin_end, new_dologin_end, 1)  # only first occurrence

# ============================================================
# 5. Modify checkSession to restore token from sessionStorage
# ============================================================
old_checksession = """function checkSession(){
  const u=sessionStorage.getItem('bitacora_user');
  if(u&&USERS[u]){"""

new_checksession = """function checkSession(){
  const tk=sessionStorage.getItem('gh_token');
  if(tk){GH_CONFIG.token=tk;refreshGHHeaders();}
  const u=sessionStorage.getItem('bitacora_user');
  if(u&&USERS[u]){"""

html = html.replace(old_checksession, new_checksession)

# ============================================================
# 6. Pre-fill token field if already in sessionStorage (add after loginPass keydown listener)
# ============================================================
old_keydown = """document.getElementById('loginPass').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin();});"""

new_keydown = """document.getElementById('loginPass').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin();});
document.getElementById('loginToken').addEventListener('keydown',e=>{if(e.key==='Enter')doLogin();});
// Pre-fill token if saved
(function(){const tk=sessionStorage.getItem('gh_token');if(tk)document.getElementById('loginToken').value=tk;})();"""

html = html.replace(old_keydown, new_keydown)

# ============================================================
# 7. Allow Enter on token field too
# ============================================================

# ============================================================
# Verify
# ============================================================
checks = {
    'loginToken field': 'id="loginToken"' in html,
    'No hardcoded ghp_': 'ghp_OGeh' not in html,
    'refreshGHHeaders fn': 'function refreshGHHeaders' in html,
    'sessionStorage gh_token in doLogin': "sessionStorage.setItem('gh_token',tk)" in html,
    'sessionStorage restore in checkSession': "sessionStorage.getItem('gh_token')" in html,
    'prefill token': "document.getElementById('loginToken').value=tk" in html,
    'GH_CONFIG token empty': "token:''" in html,
}

all_ok = True
for name, ok in checks.items():
    status = '✓' if ok else '✗ FAILED'
    if not ok: all_ok = False
    print(f"  {status} {name}")

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n{'ALL OK' if all_ok else 'SOME FAILED'} - {len(html):,} bytes")