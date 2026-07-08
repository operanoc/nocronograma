#!/usr/bin/env python3
"""Fix: load from localStorage instantly, sync GitHub after login."""

SRC = '/home/z/my-project/download/bitacora_noc_con_login.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

# ============================================================
# 1. Replace loadStore with sync version (localStorage first, instant)
# ============================================================
old_loadstore = """async function loadStore(){
  store={};
  setSyncStatus('saving');
  try{
    // Try GitHub first
    const ghData=await ghFetchAll();
    if(Object.keys(ghData).length>0){
      store=ghData;
    }else{
      // Repo is empty, push INITIAL_DATA
      for(const[k,v]of Object.entries(INITIAL_DATA)){
        store[k]=JSON.parse(JSON.stringify(v));
      }
      // Push all initial data to GitHub
      const promises=Object.entries(store).map(([k,v])=>ghPushDay(k,v));
      await Promise.all(promises);
    }
  }catch(e){
    console.warn('GitHub load failed, using localStorage fallback',e);
    setSyncStatus('error','Error al cargar desde GitHub');
    const s=localStorage.getItem('bitacora_v2');if(s)try{store=JSON.parse(s)}catch(ex){store={};}
  }
  // Merge any missing INITIAL_DATA days
  for(const[k,v]of Object.entries(INITIAL_DATA)){if(!store[k])store[k]=JSON.parse(JSON.stringify(v));}
  // Always cache to localStorage for offline
  try{localStorage.setItem('bitacora_v2',JSON.stringify(store));}catch(e){}
  setSyncStatus('ok');
}"""

new_loadstore = """function loadStoreLocal(){
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
}"""

html = html.replace(old_loadstore, new_loadstore)

# ============================================================
# 2. Replace the initialization: load local first, render immediately
# ============================================================
old_init = """(async function(){await loadStore();checkSession();render();})();"""
new_init = """loadStoreLocal();checkSession();render();"""
html = html.replace(old_init, new_init)

# ============================================================
# 3. Add syncFromGitHub() call after login (in the first doLogin patch)
# ============================================================
# Find the first doLogin patch that calls showTurnoButtons and add sync there
old_patch1 = """const __origDoLogin=doLogin;
doLogin=function(){
  __origDoLogin();
  showTurnoButtons();
  const day=getDay(currentDate);
  renderNovedades(day);updateNotifBadge(day);
};"""

new_patch1 = """const __origDoLogin=doLogin;
doLogin=function(){
  __origDoLogin();
  showTurnoButtons();
  const day=getDay(currentDate);
  renderNovedades(day);updateNotifBadge(day);
  syncFromGitHub();
};"""

html = html.replace(old_patch1, new_patch1)

# Also add sync after checkSession restores a session
old_patch_cs = """const __origCheckSession=checkSession;
checkSession=function(){
  __origCheckSession();
  showTurnoButtons();
  if(currentUser){
    const day=getDay(currentDate);
    renderNovedades(day);updateNotifBadge(day);
  }
};"""

new_patch_cs = """const __origCheckSession=checkSession;
checkSession=function(){
  __origCheckSession();
  showTurnoButtons();
  if(currentUser){
    const day=getDay(currentDate);
    renderNovedades(day);updateNotifBadge(day);
    syncFromGitHub();
  }
};"""

html = html.replace(old_patch_cs, new_patch_cs)

# ============================================================
# Verify
# ============================================================
checks = {
    'loadStoreLocal (sync)': 'function loadStoreLocal()' in html,
    'syncFromGitHub (async)': 'async function syncFromGitHub()' in html,
    'No await loadStore': 'await loadStore' not in html,
    'Init is sync': 'loadStoreLocal();checkSession();render();' in html,
    'sync after login': 'syncFromGitHub();' in html,
    'sync after checkSession': 'syncFromGitHub' in html.split('const __origCheckSession')[1].split('};')[0] if 'const __origCheckSession' in html else False,
}

all_ok = True
for name, ok in checks.items():
    status = 'OK' if ok else 'FAIL'
    if not ok: all_ok = False
    print(f'  [{status}] {name}')

with open(SRC, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'\n{"ALL OK" if all_ok else "SOME FAILED"} - {len(html):,} bytes')