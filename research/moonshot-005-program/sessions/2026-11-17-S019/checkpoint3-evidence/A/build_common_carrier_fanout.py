"""Actual fanout through common-meet originals, with native-meet mask cancellation.

New construction; retained exact native replay is a credited verifier dependency.
No complete supplier is asserted.
"""
from pathlib import Path
import argparse,collections,hashlib,importlib.util,itertools,json
from fractions import Fraction
from decimal import Decimal,localcontext

SOURCE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SOURCE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
DEFAULT_TARGETS=[1,3,73,76,77,80]

def save(path,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();path.write_bytes(raw);return hashlib.sha256(raw).hexdigest()

def binary_basis(rows):
 b={}
 for j,row in enumerate(rows):
  a=row;t=1<<j
  while a:
   p=a.bit_length()-1
   if p in b:a^=b[p][0];t^=b[p][1]
   else:b[p]=(a,t);break
 return b

def coeff(basis,row):
 out=0
 while row:
  p=row.bit_length()-1
  assert p in basis,'not in span'
  row^=basis[p][0];out^=basis[p][1]
 return out

def floor_root(n,k):
 lo=0;hi=1<<((n.bit_length()+k-1)//k)
 while lo+1<hi:
  mid=(lo+hi)//2
  if mid**k<=n:lo=mid
  else:hi=mid
 assert lo**k<=n<(lo+1)**k
 return lo

def moment(profile):
 scale=10**42;lo=hi=Fraction(0)
 for d,n in profile.items():
  d=int(d)
  if d==1:a=b=Fraction(1)
  else:
   q=floor_root(d**199*scale**200,200);a=Fraction(q,scale);b=Fraction(q+1,scale)
  lo+=n*(a if n>=0 else b);hi+=n*(b if n>=0 else a)
 return lo,hi

def record(pair):
 with localcontext()as c:
  c.prec=65
  dec=[str(Decimal(z.numerator)/Decimal(z.denominator))for z in pair]
 return {'rational':list(map(str,pair)),'decimal':dec}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--targets',default=','.join(map(str,DEFAULT_TARGETS)));a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 src=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(src).hexdigest()==SOURCE_SHA;R=json.loads(src)['native_roots'];T=sorted(map(int,a.targets.split(',')));assert len(T)==len(set(T))
 ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';sp=importlib.util.spec_from_file_location('fanout_native',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
 charts={'Hub':{'kind':'span','rows':[[int(i==j)for j in range(8)]for i in range(8)]},'zero':{'kind':'span','rows':[]}}
 for i,r in enumerate(R):charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
 J='FANOUT_COMMON';charts[J]={'kind':'ann','rows':[R[i]for i in T]};C={n:e.chart(d)for n,d in charts.items()};c=len(C[J]);assert c>1
 dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));G=collections.defaultdict(list)
 for j in range(111):G[tuple(i for i in T if dot(i,j)==0)].append(j)
 common=G[tuple(T)];mixed=sorted(g for g in G if 1<len(g)<len(T));branches=[(g,i)for g in mixed for i in g];assert len(common)>=len(branches),(len(common),len(branches))
 assignments=[{'group':list(g),'receiver':i,'carrier':common[k]}for k,(g,i)in enumerate(branches)];carrier_set={z['carrier']for z in assignments};owners=[];ops=[];marks={};semantic={key:[]for key in ['native_captures','common_captures','mask_captures','group_captures','singleton_captures','carrier_injections','carrier_deposits','carrier_restorations','canonical_loads','canonical_descents','canonical_preloads','receiver_reads']}
 def emit(o,key=None):
  if key:semantic[key].append(len(ops))
  ops.append(o)
 def init(n,h):owners.append(n);emit(['INIT',n,h])
 for i in range(111):init(f'NATIVE_RAW_{i}',f'L{i}');emit(['ADD',f'X{i}',f'NATIVE_RAW_{i}'],'native_captures')
 init('COMMON_SUM',J)
 for i in T:init(f'MASK_{i}',J);init(f'FACET_SUM_{i}',f'F{i}')
 group_name={}
 for k,g in enumerate(mixed):
  h=f'COHORT_CHART_{k}';charts[h]={'kind':'ann','rows':[R[i]for i in g]};C[h]=e.chart(charts[h]);n=f'COHORT_SUM_{k}';group_name[g]=(h,n);init(n,h)
 for j in common:
  emit(['MOVE',f'X{j}',J]);emit(['ADD',f'X{j}','COMMON_SUM'],'common_captures')
  matches=[z for z in assignments if z['carrier']==j]
  for z in matches:emit(['ADD',f'X{j}',f'MASK_{z["receiver"]}'],'mask_captures')
  if not matches:emit(['MOVE',f'X{j}','Hub'])
 marks['common_raw_capture_end']=len(ops)
 for g,donors in sorted(G.items()):
  if g==tuple(T):continue
  if not g:
   for j in donors:emit(['MOVE',f'X{j}','Hub'])
  elif len(g)==1:
   i=g[0]
   for j in donors:emit(['MOVE',f'X{j}',f'F{i}']);emit(['ADD',f'X{j}',f'FACET_SUM_{i}'],'singleton_captures');emit(['MOVE',f'X{j}','Hub'])
  else:
   h,n=group_name[g]
   for j in donors:emit(['MOVE',f'X{j}',h]);emit(['ADD',f'X{j}',n],'group_captures');emit(['MOVE',f'X{j}','Hub'])
 marks['cohort_acquisition_end']=len(ops)
 for z in assignments:
  g=tuple(z['group']);i=z['receiver'];j=z['carrier'];h,n=group_name[g]
  assert e.sub(C[J],C[h])and e.sub(C[h],C[f'F{i}'])
  emit(['MOVE',f'X{j}',h]);emit(['ADD',n,f'X{j}'],'carrier_injections');emit(['MOVE',f'X{j}',f'F{i}']);emit(['ADD',f'X{j}',f'FACET_SUM_{i}'],'carrier_deposits');emit(['MOVE',f'X{j}','Hub'])
  for d in G[g]:emit(['ADD',f'X{d}',f'X{j}'],'carrier_restorations')
 marks['all_originals_restored_before_canonical']=len(ops)
 K=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];selected=[];rows=[]
 for i,row in enumerate(K):
  if len(binary_basis(rows+[row]))>len(rows):selected.append(i);rows.append(row)
 assert len(rows)==9;B=binary_basis(rows);coeffs={i:coeff(B,K[i])for i in T};modes=[]
 for k,row in enumerate(rows):
  n=f'CANONICAL_{k}';modes.append(n);init(n,'Hub')
  for j in range(111):
   if row>>j&1:emit(['ADD',f'X{j}',n],'canonical_loads')
  emit(['MOVE',n,'zero'],'canonical_descents')
  for i in T:
   if coeffs[i]>>k&1:emit(['ADD',n,f'Y{i}'],'canonical_preloads')
 marks['canonical_before_Y_departure']=len(ops)
 for i in T:
  emit(['MOVE',f'Y{i}',J]);emit(['ADD','COMMON_SUM',f'Y{i}'],'receiver_reads');emit(['ADD',f'MASK_{i}',f'Y{i}'],'receiver_reads');emit(['MOVE',f'Y{i}',f'F{i}']);emit(['ADD',f'FACET_SUM_{i}',f'Y{i}'],'receiver_reads')
 cut=len(ops)
 for i in range(111):
  if i not in T:emit(['MOVE',f'Y{i}',f'F{i}'])
 for n in owners:emit(['CLEAR',n])
 w={'schema':'common-meet-mask-reversible-original-fanout-v1','source_path':SOURCE,'source_sha256':SOURCE_SHA,'charts':charts,'operations':ops,'targets':T,'carrier_interface_before_operation':cut,'milestones':marks,'fanout':{'common_chart':J,'common_dimension':c,'common_source_roles':common,'groups':[{'receivers':list(g),'donors':v}for g,v in sorted(G.items())],'assignments':assignments,'canonical_basis_roles':selected,'canonical_fields':modes,'canonical_decoder_masks':{str(i):hex(v)for i,v in coeffs.items()},'native_cache_count':111,'all_unknown_source_loads_actual':True},'semantic_operation_indices':semantic,'scope':'Actual alternative prefix: native-meet masks and reversible ascending original fanout replace mixed-cohort downward transport. Complete stated target subset only; nine canonical modes physically ground, all111 native raw caches and stationary proper caches retained at cut. Not a complete111-output supplier; no kappa.'}
 _,_,stats=e.replay(w,R)
 # Independent algebraic cut trace for all source/target columns (geometry is separately replayed).
 values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};cut_values=None
 for k,o in enumerate(ops):
  if k==cut:cut_values=values.copy();cut_at=at.copy()
  typ,n,*q=o
  if typ=='INIT':values[n]=0;at[n]=q[0]
  elif typ=='ADD':values[q[0]]^=values[n]
  elif typ=='MOVE':at[n]=q[0]
  elif typ=='CLEAR':del values[n];del at[n]
 assert cut_values is not None
 for j in range(111):assert cut_values[f'X{j}']==1<<j and cut_at[f'X{j}']=='Hub' and cut_values[f'NATIVE_RAW_{j}']==1<<j and cut_at[f'NATIVE_RAW_{j}']==f'L{j}'
 for i in T:assert cut_values[f'Y{i}']==(1<<(111+i))^(1<<i)and cut_at[f'Y{i}']==f'F{i}'
 for i in set(range(111))-set(T):assert cut_values[f'Y{i}']==1<<(111+i)and cut_at[f'Y{i}']=='zero'
 for k,n in enumerate(modes):assert cut_values[n]==rows[k] and cut_at[n]=='zero'
 assert cut_values['COMMON_SUM']==sum(1<<j for j in common)
 for z in assignments:
  assert z['carrier'] not in G[tuple(z['group'])]
 for i in T:
  mask=sum(1<<z['carrier']for z in assignments if z['receiver']==i);foreign=sum(1<<j for j in range(111)if dot(i,j)==0);assert cut_values[f'MASK_{i}']==mask;assert cut_values[f'FACET_SUM_{i}']==foreign^sum(1<<j for j in common)^mask
 pin=save(a.out/'WORD.json',w);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(z/6 for z in moment(gate));q=moment(stats['movement_profile']);result={'status':'PASS_COMMON_MEET_CARRIER_FANOUT','word_sha256':pin,'targets':T,'completed_outputs':len(T),'unfinished_outputs':111-len(T),'common_native_carriers_available':len(common),'carriers_used':len(assignments),'mixed_groups':len(mixed),'stats':stats,'all222_columns':True,'all_X_restored_before_nine_canonical_loads':True,'only_owned_MOVEs':[['Hub','zero']for _ in range(9)],'source_cut':cut,'canonical_rank':9,'moment':record(q),'necessary_limiting_room':record((ceiling[0]-q[1],ceiling[1]-q[0])),'source_sha256':SOURCE_SHA,'verifier_sha256':hashlib.sha256(ep.read_bytes()).hexdigest(),'scope':w['scope']};save(a.out/'RESULT.json',result);print(json.dumps({k:result[k]for k in ['status','completed_outputs','carriers_used','stats','moment','necessary_limiting_room']}))
if __name__=='__main__':main()
