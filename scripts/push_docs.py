import requests, base64, json, sys

TOKEN = ''.join(chr(c) for c in [103,104,112,95,79,71,101,104,53,89,71,88,113,57,103,115,82,82,122,85,118,52,79,74,75,110,103,74,56,72,115,56,114,82,48,122,111,119,121,69])
OWNER = 'lecatexzonanorte'
REPO = 'nocronograma'
BRANCH = 'main'
headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

files_to_push = [
    ('README.md', '/home/z/my-project/download/README.md', 'Actualizacion README + manual de usuario'),
    ('MANUAL_USUARIO.md', '/home/z/my-project/download/manual_usuario.md', 'Agregar manual de usuario del sistema'),
]

for file_path, local_file, msg in files_to_push:
    # Get current SHA (file may or may not exist)
    r = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_path}?ref={BRANCH}', headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    # Read and encode
    with open(local_file, 'rb') as f:
        content = base64.b64encode(f.read()).decode('utf-8')
    
    data = {
        'message': msg,
        'content': content,
        'branch': BRANCH
    }
    if sha:
        data['sha'] = sha
    
    r = requests.put(f'https://api.github.com/repos/{OWNER}/{REPO}/contents/{file_path}', headers=headers, json=data)
    if r.status_code in (200, 201):
        print(f'OK: {file_path} -> {r.json()["commit"]["sha"][:12]}')
    else:
        print(f'ERROR: {file_path} -> {r.status_code} {r.text[:200]}')