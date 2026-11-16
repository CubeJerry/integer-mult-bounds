#!/usr/bin/env python3
from pathlib import Path
import json
from check import basis,rem
import argparse,hashlib
from sympy import Matrix
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--envelope',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
raw=args.word.read_bytes();w=json.loads(raw);q=json.loads(args.envelope.read_text());assert hashlib.sha256(raw).hexdigest()==q['word_sha256'];src=(args.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));banks={n:{'ports':b['ports'],'rows':[int(x,16)for x in b['rows_hex']]}for n,b in q['bank_description'].items()};ch=w['charts']['M1'];rr=Matrix(ch['rows']);mr=rr.rowspace()if ch['kind']=='span'else rr.nullspace();rows=[list(v)for v in mr];M=[j for j in range(111)if Matrix(rows+[R[j]]).rank()==len(rows)]
def closure(ports):
 bb={n:{'ports':(ports if n=='h1'else b['ports']),'rows':b['rows']}for n,b in banks.items()};known=set(w['targets']);RR=[]
 for i in range(111):
  rr=[1<<j for j in w['targets']]+[1<<j for j in range(111)if dot(i,j)==0]
  for b in bb.values():
   if any(dot(i,d)==0 for d in b['ports']):rr+=b['rows']
  RR.append(rr)
 while True:
  ns={i for i,rr in enumerate(RR)if rem(basis(rr+[1<<j for j in known]),1<<i)==0};assert known<=ns
  if ns==known:break
  known=ns
 return sorted(known)
out=[]
for k,old in enumerate([0,28,44]):
 for d in M:
  if d in[0,28,44]:continue
  p=[0,28,44];p[k]=d;f=closure(p);out.append({'old_port':old,'new_port':d,'new_ports':p,'closure_count':len(f),'excluded':[i for i in range(111)if i not in f]})
res={'scope':'One M1 leaf-line replacement in the optimistic full-bank model, still granting old34 completedpoints globally. Positivecoverage is not a physicaldecoder or one-rowcode.','M1_native_lines':M,'single_changes':out,'complete_relaxations':[r for r in out if r['closure_count']==111]};args.out.mkdir(parents=True,exist_ok=True);(args.out/'PORT-SCREEN.json').write_text(json.dumps(res,indent=2)+'\n');print('111relaxations',res['complete_relaxations']);print('bestcount',max(r['closure_count']for r in out))
