#!/usr/bin/env python3
"""Bounded normal/optimized reproduction of the frozen source receipts."""
import argparse,gzip,hashlib,json,subprocess,sys,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
EXPECTED={'base':'58186c21ef28a9ae71e8c14dd82c12a01bf50f33db28e23eadc23755e905b139','expanded':'0df1ceb9babf6931572f7aa558ec8fadfe9ca2966540ca0d92a06a9d1b157864'}
p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,default=HERE/'VERIFICATION.json');args=p.parse_args()
if hashlib.sha256(args.source.read_bytes()).hexdigest()!=PIN:raise ValueError('source SHA256')
checks=[]
with tempfile.TemporaryDirectory(prefix='moonshot-side-info-') as td:
    for kind,script in [('base','verify.py'),('expanded','expanded_graph.py')]:
        for optimized in [False,True]:
            output=Path(td)/(kind+('-optimized' if optimized else '-normal')+'.json.gz')
            cmd=[sys.executable]+(['-O'] if optimized else [])+[str(HERE/script),'--source',str(args.source),'--output',str(output)]
            if kind=='expanded':cmd+=['--base',str(HERE/'RESULT.json.gz')]
            run=subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=60)
            payload=gzip.decompress(output.read_bytes());sha=hashlib.sha256(payload).hexdigest()
            if sha!=EXPECTED[kind]:raise ValueError('receipt changed: '+kind)
            checks.append(dict(kind=kind,optimized=optimized,payload_sha256=sha,summary=json.loads(run.stdout)))
receipt=dict(schema='moonshot-side-information-reproduction-v1',source_sha256=PIN,per_command_timeout_seconds=60,checks=checks,status='PASS: all four source-bound receipts reproduce exactly; normal and optimized payloads agree.')
args.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(receipt['status'])
