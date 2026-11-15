#!/usr/bin/env python3
"""Independent inversion at the actual chronological cuts; no author imports."""
import argparse,collections,hashlib,json
from pathlib import Path
import sympy as sp

def rank(rows):
 p={}
 for x in rows:
  while x:
   j=(x&-x).bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)
def inverse(rows):
 n=len(rows);a=[r|(1<<(n+i))for i,r in enumerate(rows)]
 for j in range(n):
  i=next(i for i in range(j,n)if a[i]>>j&1);a[j],a[i]=a[i],a[j]
  for k in range(n):
   if k!=j and a[k]>>j&1:a[k]^=a[j]
 assert all(x&((1<<n)-1)==1<<i for i,x in enumerate(a));return[x>>n for x in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();base=a.repo/'research/moonshot-005-program';raw=(base/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];wb=(a.source/'four-chart-word/WORD.json').read_bytes();assert hashlib.sha256(wb).hexdigest()=='831ac2f8ba647a50866af61461f9f378c76a443801f372154745520b4caa96fa';w=json.loads(wb);X=[f'X{j}_{k}'for j in range(111)for k in range(4)];Y=[f'Y{j}_{k}'for j in range(111)for k in range(4)];ids={n:i for i,n in enumerate(X)};val={n:1<<i for n,i in ids.items()}|{n:0 for n in Y};loc={n:f'L{i//4}'for n,i in ids.items()}|{n:'zero'for n in Y};K=[sum(1<<(4*j+k)for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)for k in range(4)];assert rank(K)==36;cuts=[]
 for step,o in enumerate(w['operations']):
  t,n,*p=o
  if t=='ADD':
   dst=p[0];assert not(n in Y and dst in X),'X-only invertible block no longer valid';val[dst]^=val[n]
  elif t=='MOVE':loc[n]=p[0]
  else:raise AssertionError('Unexpected owned state in frozen local word')
  if step+1 not in w['milestones'].values():continue
  label=next(k for k,v in w['milestones'].items()if v==step+1);P=[val[n]for n in X];I=inverse(P);H=[val[n]for n in X if loc[n]=='Hub'];held=[n for n in X if loc[n]!='Hub'];groups=collections.defaultdict(list)
  for n in held:groups[loc[n]].append(n)
  records=[];allcols=[]
  for chart,names in sorted(groups.items()):
   cols=[sum(((I[j]>>ids[n])&1)<<j for j in range(444))for n in names];allcols+=cols;normal=w['chart_normal_native_indices'][int(chart[1:])];basis=sp.Matrix([R[3],R[normal]]).nullspace();B=sp.Matrix.hstack(*basis).T
   for col in cols:
    assert all(B.col_join(sp.Matrix([R[j//4]])).rank()==6 for j in range(444)if col>>j&1)
    assert not any((h&col).bit_count()%2 for h in H)
   restriction=lambda rows:[sum(((r&c).bit_count()%2)<<i for i,c in enumerate(cols))for r in rows]
   S=[val[n]for n in Y];leak=rank(restriction(S));cached=S+[val[n]for n in names];full=rank(restriction(cached));assert full==len(names)
   records.append({'chart':chart,'held':names,'inverse_columns_hex':list(map(hex,cols)),'earlier_Y_restriction_rank':leak,'required_side_rank':len(names),'actual_stationary_pivot_copies_pass_necessary_rank':full,'drop_one_of_these_cache_copies_rank':rank(restriction(S+[val[n]for n in names[:-1]]))})
  D=[val[n]for n in held];dC=rank(D)+36-rank(D+K);projC=36-dC
  cuts.append({'milestone':label,'Hub_X_rank':rank(H),'held_X':len(held),'canonical_Hub_intersection':rank(H)+36-rank(H+K),'held_original_Y_groups':records,'canonical_intersection_with_actual_held_rows':dC,'rank_canonical_plus_held':rank(K+D),'minimum_Hub_space_given_all_held_rows':projC})
 assert cuts[0]['Hub_X_rank']==440 and cuts[0]['canonical_Hub_intersection']==32 and cuts[0]['held_X']==4
 assert all(r['earlier_Y_restriction_rank']==0 and r['required_side_rank']==2 and r['drop_one_of_these_cache_copies_rank']==1 for r in cuts[0]['held_original_Y_groups'])
 assert cuts[0]['canonical_intersection_with_actual_held_rows']==0 and cuts[0]['rank_canonical_plus_held']==40 and cuts[0]['minimum_Hub_space_given_all_held_rows']==36
 assert all(c['Hub_X_rank']==444 and c['canonical_Hub_intersection']==36 for c in cuts[1:]);assert all(val[n]==1<<ids[n]for n in X)
 a.out.mkdir(parents=True,exist_ok=True);r={'status':'PASS_INDEPENDENT_CHRONOLOGY_AND_RETAINED_MEMORY_TEST','word_sha256':hashlib.sha256(wb).hexdigest(),'method':'Recompute complete444-dimensional inverse by augmented Gaussian elimination at each cut, not author incremental inverse updates.','cuts':cuts,'scope':'Necessary cache injectivity, not source sufficiency. Actual earlier Y copies fail at this cut. Four actual pivot copies pass only this necessary test. Canonical plus held rows require40 global modes, with at least36 from Hub.','new_complete_kappa':False};(a.out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r['cuts'][0],sort_keys=True))
if __name__=='__main__':main()
