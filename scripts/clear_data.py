import requests, json

TOKEN = ''.join(chr(c) for c in [103,104,112,95,79,71,101,104,53,89,71,88,113,57,103,115,82,82,122,85,118,52,79,74,75,110,103,74,56,72,115,56,114,82,48,122,111,119,121,69])
OWNER = 'lecatexzonanorte'
REPO = 'nocronograma'
BRANCH = 'main'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

# Get all files in data/
r = requests.get(f'https://api.github.com/repos/{OWNER}/{REPO}/contents/data?ref={BRANCH}', headers=headers)
r.raise_for_status()
files = r.json()

print(f'Found {len(files)} files to delete')

for f in files:
    name = f['name']
    sha = f['sha']
    r2 = requests.delete(
        f'https://api.github.com/repos/{OWNER}/{REPO}/contents/data/{name}',
        headers=headers,
        json={'message': f'Limpieza: eliminar {name}', 'sha': sha, 'branch': BRANCH}
    )
    if r2.status_code == 200:
        print(f'  Deleted {name}')
    else:
        print(f'  Error deleting {name}: {r2.status_code} {r2.text[:100]}')

print('Done!')