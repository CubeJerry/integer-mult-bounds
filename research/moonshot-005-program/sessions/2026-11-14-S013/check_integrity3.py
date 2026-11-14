"""Authenticate checkpoint3 evidence while retaining qualified historic absences."""
import argparse
from pathlib import Path
import hashlib
import json
import subprocess

ap = argparse.ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
a = ap.parse_args()
repo = a.repo.resolve()
prefix = 'research/moonshot-005-program/'
p = repo / prefix
baseline = '5f4f9a1be068937d0e3ae1a78e81bf7f6b0a6e9d'
def need(ok, message):
    if not ok:
        raise ValueError(message)
def old(name):
    return json.loads(subprocess.check_output(['git','show',baseline+':'+prefix+name],cwd=repo))
ledger = json.loads((p/'SCIENTIFIC-FILES.json').read_text())
prior = old('SCIENTIFIC-FILES.json')
need(ledger['files'][:len(prior['files'])] == prior['files'], 'Historic ledger modified')
need(ledger['unavailable_historical_entries'] == prior['unavailable_historical_entries'], 'Historic qualification changed')
allowed = {x['path'] for x in ledger['unavailable_historical_entries']}
seen, absent, checked = set(), [], 0
for row in ledger['files']:
    name = row['path']
    need(name not in seen, 'Duplicate ledger path: '+name)
    seen.add(name)
    f = p/name
    if not f.is_file():
        need(name in allowed, 'Unexpected absent evidence: '+name)
        absent.append(name)
        continue
    data = f.read_bytes()
    need(hashlib.sha256(data).hexdigest() == row['sha256'], 'Hash mismatch: '+name)
    need(len(data) == row['bytes'], 'Byte mismatch: '+name)
    checked += 1
registry = json.loads((p/'REGISTERED-RESULTS.json').read_text())
prior_registry = old('REGISTERED-RESULTS.json')
need(registry['results'][:len(prior_registry['results'])] == prior_registry['results'], 'Historic registry modified')
for row in registry['results'][len(prior_registry['results']):]:
    need((p/row['path']).is_file(), 'Missing admission')
    review = p/row['review']
    need(review.is_file(), 'Missing review')
    manifest = json.loads((review.parent/'MANIFEST.json').read_text())
    for name, sha in manifest['files'].items():
        need(hashlib.sha256((review.parent/name).read_bytes()).hexdigest() == sha, 'Review hash mismatch')
count = 0
for f in p.rglob('*.json'):
    json.loads(f.read_text())
    count += 1
validation = json.loads((p/'sessions/2026-11-14-S013/CHECKPOINT3-VALIDATION.json').read_text())
need(validation['status'] == 'PASS', 'Reproduction not PASS')
result = {'status':'PASS_WITH_PRESERVED_HISTORICAL_QUALIFICATIONS',
          'baseline_sha':baseline, 'prior_scientific_entries':len(prior['files']),
          'scientific_entries':len(ledger['files']), 'authenticated_files':checked,
          'preserved_absences':absent, 'registered_results':len(registry['results']),
          'json_files_parsed':count, 'new_packages':len(registry['results'])-len(prior_registry['results']),
          'complete_supplier_or_new_kappa':False}
a.out.parent.mkdir(parents=True,exist_ok=True)
a.out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
