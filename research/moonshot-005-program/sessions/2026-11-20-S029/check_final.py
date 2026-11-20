"""Check every changed scientific file of the session, including sparse checkouts."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);args=ap.parse_args()
base=Path(__file__).resolve().parent
data=json.loads((base/'FINAL-VERIFICATION.json').read_bytes())
for row in data['files']:
    target=args.repo/row['path']
    raw=target.read_bytes() if target.is_file() else subprocess.check_output(['git','-C',str(args.repo),'show','HEAD:'+row['path']])
    assert hashlib.sha256(raw).hexdigest()==row['sha256'] and len(raw)==row['bytes'],row['path']
print('PASS',len(data['files']),'changed scientific files from S029')
