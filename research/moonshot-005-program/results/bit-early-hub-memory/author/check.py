#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
import json,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,default=Path(__file__).parent.parent/'shared-facet-coding');a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];w=json.loads((a.source/'four-chart-word/WORD.json').read_text());dot=lambda x,y:sum(a*b for a,b in zip(x,y))
def rank(rows):
 B={}
 for x in rows:
  while x:
   q=x.bit_length()-1
   if q in B:x^=B[q]
   else:B[q]=x;break
 return len(B)
X=[f'X{j}_{k}'for j in range(111)for k in range(4)];ids={n:i for i,n in enumerate(X)};val={n:1<<i for n,i in ids.items()};dual=val.copy();loc={n:f'L{ids[n]//4}'for n in X};updates=0;checks=0;cuts=[];K=[sum(1<<(4*j+k)for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)for k in range(4)];Cdim=rank(K);assert Cdim==36
# All charts in this literal word are native L/F, Hub/zero, or the4 rank6 C charts.
def contained(j,c):
 if c=='Hub':return True
 if c=='zero':return False
 if c.startswith('L'):return j==int(c[1:])
 if c.startswith('F'):return dot(R[j],R[int(c[1:])])==0
 q=w['chart_normal_native_indices'][int(c[1:])];return dot(R[j],R[3])==dot(R[j],R[q])==0
for step,o in enumerate(w['operations']):
 t=o[0]
 if t=='ADD'and o[1]in ids and o[2]in ids:
  src,dst=o[1:];val[dst]^=val[src];dual[src]^=dual[dst];updates+=1
  for n in [src,dst]:
   supp=sorted({k//4 for k in range(444)if dual[n]>>k&1});assert all(contained(j,loc[n])for j in supp);checks+=len(supp)
 if t=='MOVE'and o[1]in ids:loc[o[1]]=o[2]
 if step+1 in w['milestones'].values():
  label=next(k for k,v in w['milestones'].items()if v==step+1);H=[val[n]for n in X if loc[n]=='Hub'];held=[n for n in X if loc[n]!='Hub'];cert=[]
  for n in held:
   supp=sorted({k//4 for k in range(444)if dual[n]>>k&1})
   cert.append({'record':n,'chart':loc[n],'inverse_column_hex':hex(dual[n]),'original_role_support':supp,'canonical_projection_rank_nonzero':any((row&dual[n]).bit_count()%2 for row in K),'inside_chart':all(contained(j,loc[n])for j in supp)})
  cuts.append({'milestone':label,'Hub_X_rank':rank(H),'held_X_count':len(held),'canonical_rank':Cdim,'canonical_Hub_intersection':rank(H)+Cdim-rank(H+K),'held_dual_columns':cert})
assert all(val[n]==dual[n]==1<<ids[n]for n in X)
# A post-cut new global read is a genuine scope escape: all X can ascend Hub,
# copy n independent globals, descend those to zero and let each Y read its own.
# It uses full n global dimensions, not the frozen cut-Hub row space.
r={'status':'PASS_INDEPENDENT_INVERSE_COLUMN_LOCALITY_CONTROLS','word_sha256':hashlib.sha256((a.source/'four-chart-word/WORD.json').read_bytes()).hexdigest(),'original_X_columns':444,'X_X_ADD_updates':updates,'original_role_incidence_checks':checks,'cuts':cuts,'scope':'The tested word already copies X into Y before its useful Hub cut; it is a positive example outside the new no-side-memory premise, not a rejected local word.','universal_claim_proved_separately':True,'new_complete_kappa':False};(Path(__file__).parent/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print([(c['milestone'],c['Hub_X_rank'],c['held_X_count'],c['canonical_Hub_intersection'])for c in cuts])
