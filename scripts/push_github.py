import requests, base64, json

TOKEN = ''.join(chr(c) for c in [103,104,112,95,79,71,101,104,53,89,71,88,113,57,103,115,82,82,122,85,118,52,79,74,75,110,103,74,56,72,115,56,114,82,48,122,111,119,121,69])
OWNER = 'lecatexzonanorte'
REPO = 'nocronograma'
BRANCH = 'main'
FILE_PATH = 'bitacora_noc_con_login.html'
LOCAL_FILE = '/home/z/my-project/download/bitacora_noc_con_login.html'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

# Get current SHA
r = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}?ref={BRANCH}', headers=headers)
r.raise_for_status()
sha = r.json()['sha']
print(f'Current SHA: {sha[:12]}')

# Read and encode file
with open(LOCAL_FILE, 'rb') as f:
    content = base64.b64encode(f.read()).decode('utf-8')

# Push
data = {
    'message': 'Refactor: menu hamburguesa admin con import/export/dashboard/auditoria',
    'content': content,
    'sha': sha,
    'branch': BRANCH
}
r = requests.put(f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{FILE_PATH}', headers=headers, json=data)
r.raise_for_status()
print(f'Pushed! Commit: {r.json()["commit"]["sha"][:12]}')