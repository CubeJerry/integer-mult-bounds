"""Independent actual-bank reconstruction and exact envelope dual checks."""
from pathlib import Path
from functools import lru_cache
import argparse,hashlib,json,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.engine));from check import rr,null,rank
raw=a.word.read_bytes();w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];cert=json.loads(a.certificate.read_text());assert cert['word_sha256']==hashlib.sha256(raw).hexdigest()
C={n:rr(v['rows']) if v['kind']=='span' else null(v['rows']) for n,v in w['charts'].items()}
@lru_cache(None)
def sub(c,d):return len(rr(C[c]+C[d]))==len(C[d])
dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)};at={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)};vis=[set(),set()];cut=None
for step,o in enumerate(w['operations'],1):
 if o[0]=='INIT':v[o[1]]=0;at[o[1]]=o[2]
 elif o[0]=='ADD':v[o[2]]^=v[o[1]]
 elif o[0]=='MOVE':
  at[o[1]]=o[2]
  if o[1].startswith('X'):
   j=int(o[1][1:])
   for k,c in enumerate(['C0','M1']):
    if C[o[2]]==C[c] and v[o[1]]==1<<j:vis[k].add(j)
 elif o[0]=='CLEAR':del v[o[1]];del at[o[1]]
 if step==w['milestones']['seed8_before_Y']:cut=(dict(v),dict(at))
assert cut;v,at=cut;mask=(1<<111)-1;pure={n:x for n,x in v.items() if x&~mask==0};ground=[x for n,x in pure.items() if not C[at[n]]];banks=[[x for n,x in pure.items() if C[at[n]]==C[c]] for c in ['C0','M1']]
assert [sorted(s) for s in vis]==cert['source_visitors'];geometric=[[j for j in range(111) if sub(f'L{j}',c)] for c in ['C0','M1']]
removed={f'KEEP_M{q["b"]}' for q in w['multi_retention']}|{f'ZKEEP{q["b"]}' for q in w['m1_retention']};fixed={n:x for n,x in pure.items() if n not in removed};lines=[[7,11,12],[0,28,44]];cases={};duals=0
for mode,c in cert['cases'].items():
 B=[banks[k]+([1<<j for j in vis[k]] if mode!='retained' else []) for k in range(2)];rows=[];fits=[]
 for i in range(111):
  z=[x for n,x in fixed.items() if sub(at[n],f'F{i}')]+[1<<j for j in range(111) if dot(i,j)==0]
  for k in range(2):
   if mode.startswith('global_') or any(dot(d,i)==0 for d in lines[k]):z+=B[k]
  if mode.endswith('_plus_three_points'):z+=[1<<j for j in [8,9,20]]
  rows.append(z)
  if rank(z+[1<<i])==rank(z):fits.append(i)
 assert fits==c['fitting_upper_set']
 for rec in c['excluded_receivers']:
  i=rec['receiver'];lam=int(rec['dual_hex'],16);assert lam>>i&1 and all((lam&x).bit_count()%2==0 for x in rows[i]);duals+=1
 known=set(fits)
 while True:
  new={i for i in range(111) if i not in known and rank(rows[i]+[1<<j for j in known]+[1<<i])==rank(rows[i]+[1<<j for j in known])}
  if not new:break
  known|=new
 assert sorted(known)==c['feedback_closure']
 for rec in c['closure_duals']:
  i=rec['receiver'];lam=int(rec['dual_hex'],16);assert lam>>i&1 and all((lam&x).bit_count()%2==0 for x in rows[i]+[1<<j for j in known]);duals+=1
 cases[mode]={'fits':len(fits),'closed_points':len(known)}
G=ground+banks[0]+banks[1]+[1<<j for k in range(2) for j in vis[k]];K=[sum(1<<j for j in range(111) if i==j or dot(i,j)==0) for i in range(111)]
result={'status':'PASS_INDEPENDENT_ACTUAL_BANK_ENVELOPE','word_sha256':hashlib.sha256(raw).hexdigest(),'certificate_sha256':hashlib.sha256(a.certificate.read_bytes()).hexdigest(),'actual_raw_visitors':[sorted(x) for x in vis],'all_native_roots_in_acquisition_charts':geometric,'bank_ranks':[rank(x) for x in banks],'enlarged_bank_ranks':[rank(banks[k]+[1<<j for j in vis[k]]) for k in range(2)],'cases':cases,'checked_duals':duals,'global_common_rank':rank(G),'global_common_C9_intersection':9+rank(G)-rank(G+K),'canonical_completion_dimension':rank(G+K)-rank(G),'scope':'Frozen acquisition banks and explicit access relaxations; the canonical completion number is not a minimum fitting lower bound.','new_complete_kappa':False};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
