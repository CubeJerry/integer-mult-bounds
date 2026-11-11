"""Run one optimized verification group with explicit subprocess checks."""
from pathlib import Path
import argparse,subprocess,sys
H=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('group',choices=['author','independent']);a=p.parse_args()
if a.group=='author':
 commands=[['verify.py'],['compiler_certificate.py'],['static_cut.py']]
else:
 commands=[['review/fragmentation/independent.py','--source',str(H/'inputs/FULL-RESULT.json')],['review/compiler/independent.py','--source',str(H/'inputs/FULL-RESULT.json')],['review/static/independent.py','--source',str(H.parent/'shared-wire-split-composition/data/final.json.gz')]]
for entry in commands:
 subprocess.run([sys.executable,'-I','-O','-B',str(H/entry[0]),*entry[1:]],check=True)
