#!/usr/bin/env python3
"""Actual full1880-input replay using the pinned parent rational interpreter."""
from common import *
import argparse,importlib.util,sys
def main(a):
 s,p,_=load_inputs(a.repo);base=a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections';path=base/'verify.py';need(sha(path.read_bytes())=='0367ae2b674de218acaad4528a5efb1ff488b136f5a2cec867829ff1ea4adfaa','pinned parent rational interpreter')
 spec=importlib.util.spec_from_file_location('fresh_parent_exact',path);m=importlib.util.module_from_spec(spec);sys.modules['fresh_parent_exact']=m;spec.loader.exec_module(m)
 cert=json.loads((base/'INPUT-CONTROLLERS.json').read_text());prefix=json.loads(gzip.decompress((base/'INPUT-PREFIX.json.gz').read_bytes()));T,Z,decoders,scalings,guards=m.source_certificate(s,cert);raw={int(x):r for x,r in p['private_role_map'].items()};targets,q,weights,residuals=m.prefix_targets(s,prefix,raw);caches={int(x):r for x,r in p['donor_caches'].items()}
 for name in list(SELECT) if a.variant=='all' else [a.variant]:
  target=a.output/name;wb=(target/'WORD.json.gz').read_bytes();w=json.loads(gzip.decompress(wb));extended=dict(s,frames=s['frames']+[d['frame'] for d in w['additional_charts']]);corr={int(y):{d:F(c) for d,c in row} for y,row in w['corrections'].items()};receipt=m.execute(extended,prefix,w,raw,T,Z,targets,q,corr,caches);receipt.update(status='PASS_FULL1880_INPUT_WORD_AND400_ROW_INVERSE',word_sha256=sha(wb),source_sha256=SPIN,parent_interpreter_sha256=sha(path.read_bytes()),scope='Full exact rational word replay with existing pinned interpreter; separate independent review remains required.');(target/'FULL-REPLAY.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(name,'full1880-word PASS',len(w['program']),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--variant',choices=['all']+list(SELECT),default='eight');main(ap.parse_args())
