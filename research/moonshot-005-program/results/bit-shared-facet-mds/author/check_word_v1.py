#!/usr/bin/env python3
import json,hashlib,argparse,copy
from pathlib import Path
from collections import Counter
from functools import lru_cache
import sympy as sp

def chart(c):
 M=sp.Matrix(c['rows'])if c['rows']else sp.zeros(0,8);v=M.rowspace()if c['kind']=='span'else M.nullspace();return tuple(tuple(x)for x in v)
def replay(w,R):
 copies=4;C={n:chart(c)for n,c in w['charts'].items()};dim={n:len(v)for n,v in C.items()}
 @lru_cache(None)
 def sub(a,b):return(sp.Matrix(C[a]+C[b]).rank()if C[a]+C[b]else 0)==dim[b]
 for j,r in enumerate(R):assert C[f'L{j}']==chart({'kind':'span','rows':[r]})and C[f'F{j}']==chart({'kind':'ann','rows':[r]})
 assert all(dim[f'C{t}']==6 for t in range(4));i=w['receiver'];X={f'X{j}_{k}':(j,k)for j in range(111)for k in range(4)};Y={f'Y{j}_{k}':(j,k)for j in range(111)for k in range(4)};v={n:1<<(4*j+k)for n,(j,k)in X.items()}|{n:1<<(444+4*j+k)for n,(j,k)in Y.items()};loc={n:f'L{j}'for n,(j,k)in X.items()}|{n:'zero'for n in Y};counts=Counter();moves=Counter();owned=set();born=set();dirty=0;milestones={}
 def restored():return all(v[n]==1<<(4*j+k)and loc[n]=='Hub'for n,(j,k)in X.items())
 for step,op in enumerate(w['operations']):
  kind,n,*a=op;counts[kind]+=1
  if kind=='ADD':
   t=a[0];assert n in v and t in v and n!=t;assert sub(loc[n],loc[t])and sub(loc[t],loc[n]),('cochart',step,op);v[t]^=v[n]
  elif kind=='MOVE':
   dest=a[0];assert n in v and dim[dest]!=dim[loc[n]];assert sub(dest,loc[n])if n in owned else sub(loc[n],dest),('direction',step,op);moves[abs(dim[dest]-dim[loc[n]])]+=1;loc[n]=dest
  elif kind=='INIT':
   assert n not in v and n not in born;assert restored(),'late Ki source not restored';v[n]=0;loc[n]=a[0];owned.add(n);born.add(n)
  elif kind=='CLEAR':
   assert n in owned;dirty+=bool(v[n]);owned.remove(n);del v[n],loc[n]
  else:raise AssertionError(kind)
  for label,idx in w['milestones'].items():
   if step+1==idx:milestones[label]={'all_X_at_Hub':all(loc[n]=='Hub'for n in X),'all_X_restored':restored(),'nonrestored_X_count':sum(v[n]!=1<<(4*j+k)for n,(j,k)in X.items())}
 assert restored()and not owned
 foreign=[j for j in range(111)if j!=i and sum(a*b for a,b in zip(R[i],R[j]))==0];assert foreign==w['foreign_indices']
 for n,(j,k)in Y.items():
  want=1<<(444+4*j+k)
  if j==i:want^=(1<<(4*i+k))if w.get('late_proper_Ki_completion')else sum(1<<(4*t+k)for t in foreign)
  assert v[n]==want,('output',n);assert loc[n]==f'F{j}'
 if not w.get('late_proper_Ki_completion'):assert counts==Counter({'ADD':1188,'MOVE':1128})and dict(moves)=={5:232,2:228,7:652,6:4,1:12}
 else:assert counts==Counter({'INIT':4,'ADD':1428,'MOVE':1132,'CLEAR':4})and dirty==4 and dict(moves)=={5:232,2:228,7:652,6:4,1:16}
 return {'status':'PASS_LITERAL_FOUR_BINARY_COPY_CHART_CODING','columns':888,'counts':dict(counts),'dirty_clears':dirty,'movement_profile':dict(sorted(moves.items())),'milestones':milestones,'actual_native_targets_completed':[i]if w.get('late_proper_Ki_completion')else[],'local_foreign_correction_operator':True,'new_complete_kappa':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--dir',type=Path,default=Path(__file__).parent/'four-chart-word');a=p.parse_args();nb=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(nb).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(nb)['native_roots'];w=json.loads((a.dir/'WORD.json').read_text());out=a.dir/'verification';out.mkdir(exist_ok=True)
 for label,word in [('LOCAL',w)]:
  r=replay(word,R);(out/f'{label}-RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(label,r,flush=True)
 complete=copy.deepcopy(w);complete['late_proper_Ki_completion']=True;complete['expected_local_map']='Y3_k -> Y3_k+X3_k; all X restored, other Y unchanged; four actual late Ki imports charged'
 for k in range(4):
  n=f'LATE_K{k}';complete['operations'].append(['INIT',n,'Hub']);complete['operations'] += [['ADD',f'X{j}_{k}',n]for j in complete['foreign_indices']+[3]];complete['operations'] += [['MOVE',n,'F3'],['ADD',n,f'Y3_{k}'],['CLEAR',n]]
 r=replay(complete,R);(a.dir/'COMPLETED-CONTROL-WORD.json').write_text(json.dumps(complete,indent=2)+'\n');(out/'COMPLETED-CONTROL-RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print('COMPLETED',r,flush=True)
 tests=[('remove_source_encoding',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X')),('omit_pivot_aggregation',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('X')and o[1].split('_')[0]!=o[2].split('_')[0]),('omit_foreign_chart_delivery',lambda o:o[0]=='ADD'and o[1].startswith('X')and o[2].startswith('Y')),('omit_pivot_hub_return',lambda o:o[0]=='MOVE'and o[1]=='X1_2'and o[2]=='Hub'),('omit_late_Ki_route',lambda o:o==['MOVE','LATE_K0','F3'])];res=[]
 for label,pred in tests:
  bad=copy.deepcopy(complete);idx=next(i for i,o in enumerate(bad['operations'])if pred(o));bad['operations'].pop(idx);bad['milestones']={k:v-int(idx<v)for k,v in bad['milestones'].items()}
  try:replay(bad,R)
  except AssertionError as e:res.append({'name':label,'rejected':True,'reason':str(e)})
  else:raise AssertionError(label)
 (out/'NEGATIVE-CONTROLS.json').write_text(json.dumps(res,indent=2)+'\n');print('mutants',len(res))
