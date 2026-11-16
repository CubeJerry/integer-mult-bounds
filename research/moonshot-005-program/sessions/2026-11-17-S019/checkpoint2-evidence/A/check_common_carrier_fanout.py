"""Source-sensitive checking and destructive controls for common-meet carrier fanout.

This is author-side verification, not an independent review. It reconstructs
cohorts and cut identities from native roots and never imports the builder.
"""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from collections import defaultdict

PIN='f5acfcb454d6d50dfdb7d66acd2c33980e4aed17826afafbb67fbeb2168f58c1'
SOURCE_PIN='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'

def module(p):
 s=importlib.util.spec_from_file_location('semantic_fanout_native',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def trace(ops,points):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};out={}
 for k,o in enumerate(ops):
  if k in points:out[k]=(v.copy(),at.copy())
  typ,n,*q=o
  if typ=='INIT':v[n]=0;at[n]=q[0]
  elif typ=='MOVE':at[n]=q[0]
  elif typ=='ADD':v[q[0]]^=v[n]
  elif typ=='CLEAR':del v[n];del at[n]
 if len(ops)in points:out[len(ops)]=(v,at)
 return out

def verify(w,R,e):
 C,_,stats=e.replay(w,R)
 T=w['targets'];U=sorted(set(range(111))-set(T));J=w['fanout']['common_chart'];dot=lambda i,j:sum(a*b for a,b in zip(R[i],R[j]));groups=defaultdict(list)
 for j in range(111):groups[tuple(i for i in T if dot(i,j)==0)].append(j)
 E=groups[tuple(T)];A=w['fanout']['assignments'];assert len(A)==len({z['carrier']for z in A})
 assert all(z['carrier']in E for z in A)
 mixed=sorted(g for g in groups if 1<len(g)<len(T));assert sorted((tuple(z['group']),z['receiver'])for z in A)==sorted((g,i)for g in mixed for i in g)
 K=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)]
 points=set(w['milestones'].values())|{w['carrier_interface_before_operation']};states=trace(w['operations'],points)
 v,at=states[w['milestones']['common_raw_capture_end']];assert v['COMMON_SUM']==sum(1<<i for i in E)and at['COMMON_SUM']==J
 for i in T:
  mask=sum(1<<z['carrier']for z in A if z['receiver']==i);assert v[f'MASK_{i}']==mask and at[f'MASK_{i}']==J
 for z in A:assert v[f'X{z["carrier"]}']==1<<z['carrier']and at[f'X{z["carrier"]}']==J
 v,at=states[w['milestones']['cohort_acquisition_end']]
 for k,g in enumerate(mixed):
  assert v[f'COHORT_SUM_{k}']==sum(1<<j for j in groups[g]);assert C[at[f'COHORT_SUM_{k}']]==e.chart({'kind':'ann','rows':[R[i]for i in g]})
  for j in groups[g]:assert v[f'X{j}']==1<<j and at[f'X{j}']=='Hub'
 v,at=states[w['milestones']['all_originals_restored_before_canonical']]
 for j in range(111):assert v[f'X{j}']==1<<j and at[f'X{j}']=='Hub'
 v,at=states[w['milestones']['canonical_before_Y_departure']]
 basis_roles=w['fanout']['canonical_basis_roles'];modes=w['fanout']['canonical_fields'];assert len(e.bb(K[i]for i in basis_roles))==9
 for k,n in enumerate(modes):assert v[n]==K[basis_roles[k]]and at[n]=='zero'
 for i in range(111):assert at[f'Y{i}']=='zero'and v[f'Y{i}']==((1<<(111+i))^(K[i]if i in T else 0))
 cut=w['carrier_interface_before_operation'];v,at=states[cut]
 for j in range(111):assert v[f'X{j}']==1<<j and at[f'X{j}']=='Hub'and v[f'NATIVE_RAW_{j}']==1<<j and at[f'NATIVE_RAW_{j}']==f'L{j}'
 for i in range(111):assert v[f'Y{i}']==((1<<(111+i))^((1<<i)if i in T else 0))and at[f'Y{i}']==(f'F{i}'if i in T else'zero')
 for i in T:
  mask=sum(1<<z['carrier']for z in A if z['receiver']==i);foreign=K[i]^(1<<i);assert v[f'MASK_{i}']==mask;assert v[f'FACET_SUM_{i}']==foreign^sum(1<<j for j in E)^mask
 original={f'{p}{i}'for p in ['X','Y']for i in range(111)};assert all(z>>111==0 for n,z in v.items()if n not in original)
 loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owners=set();owned_moves=[]
 for typ,n,*q in w['operations']:
  if typ=='INIT':owners.add(n);loc[n]=q[0]
  elif typ=='MOVE':
   if n in owners:owned_moves.append((n,loc[n],q[0]))
   loc[n]=q[0]
  elif typ=='CLEAR':owners.remove(n);del loc[n]
 assert sorted(n for n,_,_ in owned_moves)==sorted(modes)
 assert all(s=='Hub'and t=='zero'for _,s,t in owned_moves)
 return {'stats':stats,'cut':cut,'T':T,'U':U,'common':E,'branches':A,'all_originals_restored_before_canonical':True,'unfinished_Ys_raw_at_ground':True,'canonical_available_at_ground':True,'only_nine_owned_movements':True}

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;w=json.loads(raw);sraw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sraw).hexdigest()==SOURCE_PIN==w['source_sha256'];R=json.loads(sraw)['native_roots'];e=module(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py');report=verify(w,R,e);controls=[]
 def reject(label,changed):
  try:verify(changed,R,e)
  except (AssertionError,KeyError,IndexError)as ex:controls.append({'control':label,'rejected':True,'failure_type':type(ex).__name__})
  else:raise AssertionError('accepted mutation '+label)
 # True deletion controls adjust only boundary indices; the remaining
 # original word is otherwise unchanged. A missing source capture can leave
 # all final endpoints correct and still fail the declared continuation source.
 def omit(index):
  z=copy.deepcopy(w);z['operations'].pop(index)
  z['milestones']={k:v-int(v>index)for k,v in z['milestones'].items()}
  z['carrier_interface_before_operation']-=int(z['carrier_interface_before_operation']>index)
  return z
 names=['native_captures','common_captures','mask_captures','group_captures','singleton_captures','carrier_injections','carrier_deposits','carrier_restorations','canonical_loads','canonical_preloads','receiver_reads']
 for kind in names:
  idx=w['semantic_operation_indices'][kind][0];assert w['operations'][idx][0]=='ADD';reject('omit '+kind+' first actual ADD',omit(idx))
 for j,idx in enumerate(w['semantic_operation_indices']['carrier_deposits']):
  reject('omit actual fanout branch deposit '+str(j),omit(idx))
 z=copy.deepcopy(w);n=z['fanout']['canonical_fields'][0];idx=next(i for i,o in enumerate(z['operations'])if o==['MOVE',n,'zero']);z['operations'][idx]=['MOVE',n,'F0'];reject('redirect actual canonical descent away from ground',z)
 z=copy.deepcopy(w);idx=next(i for i,o in enumerate(z['operations'])if o==['CLEAR','NATIVE_RAW_0']);z['operations'].pop(idx);reject('omit owned retirement',z)
 z=copy.deepcopy(w);z['fanout']['assignments'][1]['carrier']=z['fanout']['assignments'][0]['carrier'];reject('reuse a native original for two incomparable fanout branches',z)
 a.out.parent.mkdir(parents=True,exist_ok=True);result={'status':'PASS_SOURCE_SEMANTICS_AND_CONTROLS','word_sha256':PIN,'source_sha256':SOURCE_PIN,'report':report,'negative_controls':controls,'independent_review':False,'scope':'Source-sensitive author verification; universal correctness rests on the explicit fanout proof, not finite mutation tests.'};a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],'controls',len(controls))
if __name__=='__main__':main()
