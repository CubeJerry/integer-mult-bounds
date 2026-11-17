"""Earlier Y collectors, late canonical queries, and held original code delivery.

New source interface.  Frozen common-six/D4 packages are read-only dependencies.
"""
from pathlib import Path
import argparse,collections,hashlib,importlib.util,itertools,json
from build_common_carrier_fanout import SOURCE,SOURCE_SHA,DEFAULT_TARGETS,binary_basis,coeff,save,moment,record

def assignments(T,mixed):
 options=[[g for g in mixed if i in g]for i in T]
 for ds in itertools.product(*options):
  direct=dict(zip(T,ds));left={g:[i for i in g if direct[i]!=g]for g in mixed}
  if any(not v for v in left.values()):continue
  for picks in itertools.product(*(left[g]for g in mixed)):
   own=dict(zip(mixed,picks));masked=[(g,i)for g in mixed for i in left[g]if i!=own[g]];cnt=collections.Counter(i for g,i in masked)
   if len(masked)==5 and max(cnt.values())==1:return direct,own,masked
 raise AssertionError('no balanced literal assignment')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA;R=json.loads(raw)['native_roots'];T=DEFAULT_TARGETS;dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));G=collections.defaultdict(list)
 for j in range(111):G[tuple(i for i in T if dot(i,j)==0)].append(j)
 common=G[tuple(T)];mixed=sorted(g for g in G if 1<len(g)<len(T));direct,own,masked=assignments(T,mixed);codes=dict(zip(T,common[:6]));foreign=[{'group':list(g),'receiver':i,'carrier':common[6+k]}for k,(g,i)in enumerate(masked)];maskroles={i:[codes[i]]+[q['carrier']for q in foreign if q['receiver']==i]for i in T};held=set(codes.values());foreignroles={q['carrier']for q in foreign};jgroup={j:g for g,ds in G.items()for j in ds}
 ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';sp=importlib.util.spec_from_file_location('interleaved_native',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
 charts={'Hub':{'kind':'span','rows':[[int(i==j)for j in range(8)]for i in range(8)]},'zero':{'kind':'span','rows':[]},'COMMON':{'kind':'ann','rows':[R[i]for i in T]}}
 for i in range(111):charts[f'L{i}']={'kind':'span','rows':[R[i]]};charts[f'F{i}']={'kind':'ann','rows':[R[i]]}
 for i in T:charts[f'MASK_CHART_{i}']={'kind':'span','rows':[R[j]for j in maskroles[i]]}
 gnum={g:k for k,g in enumerate(mixed)}
 for g,k in gnum.items():charts[f'GROUP_CHART_{k}']={'kind':'ann','rows':[R[i]for i in g]}
 C={h:e.chart(z)for h,z in charts.items()};assert len(C['COMMON'])==5;assert all(len(C[f'MASK_CHART_{i}'])==len(maskroles[i])for i in T)
 ops=[];owners=[];marks={};semantic=collections.defaultdict(list)
 def emit(o,key=None):
  if key:semantic[key].append(len(ops))
  ops.append(o)
 def init(n,h):owners.append(n);emit(['INIT',n,h])
 def move(n,old,new):
  if C[old]!=C[new]:emit(['MOVE',n,new])
  return new
 for j in range(111):init(f'NATIVE_RAW_{j}',f'L{j}');emit(['ADD',f'X{j}',f'NATIVE_RAW_{j}'],'native_captures')
 init('COMMON_SUM','COMMON')
 for i in T:init(f'MASK_{i}',f'MASK_CHART_{i}')
 for j in common:
  here=f'L{j}';dest=next((i for i in T if j in maskroles[i]),None)
  if dest is not None:here=move(f'X{j}',here,f'MASK_CHART_{dest}');emit(['ADD',f'X{j}',f'MASK_{dest}'],'mask_captures')
  here=move(f'X{j}',here,'COMMON');emit(['ADD',f'X{j}','COMMON_SUM'],'common_captures')
  if j not in held|foreignroles:emit(['MOVE',f'X{j}','Hub'])
 marks['common_raw_masks_captured']=len(ops)
 singleton={};pivots={}
 for g,donors in sorted(G.items()):
  if g==tuple(T):continue
  if not g:
   for j in donors:emit(['MOVE',f'X{j}','Hub'])
  elif len(g)==1:
   assert len(donors)==1;singleton[g[0]]=donors[0];emit(['MOVE',f'X{donors[0]}',f'F{g[0]}'])
  else:
   k=gnum[g];h=f'GROUP_CHART_{k}';z=f'GROUP_SUM_{k}';p=donors[0];pivots[g]=p;init(z,h);emit(['MOVE',f'X{p}',h]);emit(['ADD',f'X{p}',z],'group_captures')
   for j in donors[1:]:emit(['MOVE',f'X{j}',h]);emit(['ADD',f'X{j}',z],'group_captures');emit(['ADD',f'X{j}',f'X{p}'],'pivot_coding');emit(['MOVE',f'X{j}','Hub'])
 marks['source_groups_ready_before_Y']=len(ops)
 # The receivers depart before even the first canonical owner is born.
 for i in T:
  emit(['MOVE',f'Y{i}',f'MASK_CHART_{i}']);emit(['ADD',f'MASK_{i}',f'Y{i}'],'receiver_mask_reads');g=direct[i];emit(['MOVE',f'Y{i}',f'GROUP_CHART_{gnum[g]}']);emit(['ADD',f'GROUP_SUM_{gnum[g]}',f'Y{i}'],'early_direct_cohort_reads');emit(['MOVE',f'Y{i}',f'F{i}']);j=singleton[i];emit(['ADD',f'X{j}',f'Y{i}'],'early_singleton_reads');emit(['MOVE',f'X{j}','Hub'])
 marks['all_six_Y_waiting_at_facets']=len(ops)
 for g in mixed:
  p=pivots[g];i=own[g];emit(['MOVE',f'X{p}',f'F{i}']);emit(['ADD',f'X{p}',f'Y{i}'],'pivot_receiver_reads');emit(['MOVE',f'X{p}','Hub'])
  for j in G[g][1:]:emit(['ADD',f'X{j}',f'X{p}'],'pivot_restorations')
 for q in foreign:
  g=tuple(q['group']);i=q['receiver'];j=q['carrier'];h=f'GROUP_CHART_{gnum[g]}';emit(['MOVE',f'X{j}',h]);emit(['ADD',f'GROUP_SUM_{gnum[g]}',f'X{j}'],'masked_foreign_injections');emit(['MOVE',f'X{j}',f'F{i}']);emit(['ADD',f'X{j}',f'Y{i}'],'masked_foreign_receiver_reads');emit(['MOVE',f'X{j}','Hub'])
  for d in G[g]:emit(['ADD',f'X{d}',f'X{j}'],'masked_foreign_restorations')
 marks['only_six_raw_code_originals_held']=len(ops)
 K=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];rows=[];basisroles=[]
 for i,row in enumerate(K):
  if len(binary_basis(rows+[row]))>len(rows):rows.append(row);basisroles.append(i)
 assert len(rows)==9;B=binary_basis(rows);decode={i:coeff(B,K[i])for i in T};canonical=[]
 for i in T:init(f'LATE_CODE_{i}','COMMON');emit(['ADD','COMMON_SUM',f'LATE_CODE_{i}'],'common_code_compensation')
 for k,row in enumerate(rows):
  n=f'CANONICAL_{k}';canonical.append(n);init(n,'Hub')
  for j in range(111):
   if row>>j&1 and j not in held:emit(['ADD',f'X{j}',n],'canonical_hub_projections')
  emit(['MOVE',n,'COMMON'],'canonical_proper_descents')
  for j in sorted(held):
   if row>>j&1:emit(['ADD',f'X{j}',n],'actual_held_queries')
  for i in T:
   if decode[i]>>k&1:emit(['ADD',n,f'LATE_CODE_{i}'],'proper_code_captures')
  emit(['MOVE',n,'zero'],'canonical_ground_descents')
 marks['canonical_ground_while_six_held']=len(ops)
 for i in T:
  j=codes[i];emit(['ADD',f'LATE_CODE_{i}',f'X{j}'],'late_code_injections');emit(['MOVE',f'X{j}',f'F{i}']);emit(['ADD',f'X{j}',f'Y{i}'],'late_code_receiver_reads');emit(['MOVE',f'X{j}','Hub']);P=K[i]^sum(1<<d for d in common);assert not(P&sum(1<<d for d in common))
  for d in range(111):
   if P>>d&1:emit(['ADD',f'X{d}',f'X{j}'],'late_code_restorations')
 cut=len(ops)
 for i in range(111):
  if i not in T:emit(['MOVE',f'Y{i}',f'F{i}'])
 for n in owners:emit(['CLEAR',n])
 w={'schema':'early-y-late-canonical-original-carriers-v1','source_path':SOURCE,'source_sha256':SOURCE_SHA,'charts':charts,'operations':ops,'targets':T,'carrier_interface_before_operation':cut,'milestones':marks,'construction':{'common_roles':common,'groups':[{'receivers':list(g),'donors':d}for g,d in sorted(G.items())],'mixed_group_order':[list(g)for g in mixed],'direct_group':{str(i):list(g)for i,g in direct.items()},'own_pivot_receiver':{str(gnum[g]):own[g]for g in mixed},'own_pivots':{str(gnum[g]):pivots[g]for g in mixed},'foreign_masked_routes':foreign,'code_carrier':codes,'raw_mask_roles':maskroles,'canonical_basis_roles':basisroles,'canonical_fields':canonical,'canonical_decoder_masks':{str(i):hex(z)for i,z in decode.items()},'native_cache_count':111},'semantic_operation_indices':dict(semantic),'scope':'Actual earlier Y acquisition with six raw original code carriers held at rank5, literal Hub projections and held queries, canonical9 retained atground, late proper-chart original delivery and actual Hub restoration. Six outputs only; all105 unfinished Y rawground atcut. No complete supplier or new kappa.'}
 _,_,stats=e.replay(w,R)
 # Explicit milestone/cut contracts, in addition to the native endpoint replay.
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};contracts={}
 for k,o in enumerate(ops[:cut+1]):
  if k in marks.values()or k==cut:
   if k==marks['all_six_Y_waiting_at_facets']:
    assert all(at[f'Y{i}']==f'F{i}'for i in T);assert not any(n.startswith('CANONICAL_')for n in v);contracts['Y_departure_before_canonical']=True
   if k in[marks['only_six_raw_code_originals_held'],marks['canonical_ground_while_six_held']]:
    assert all(v[f'X{j}']==1<<j and at[f'X{j}']==('COMMON'if j in held else'Hub')for j in range(111));contracts['actual_105_raw_Hub_6_raw_held']=True
    for i in T:
     expect=(1<<(111+i))^(1<<codes[i])^sum(1<<j for j in range(111)if dot(i,j)==0 and j not in common);assert v[f'Y{i}']==expect and at[f'Y{i}']==f'F{i}'
   if k==marks['canonical_ground_while_six_held']:
    for h,n in enumerate(canonical):assert v[n]==rows[h]and at[n]=='zero'
    for i in T:assert v[f'LATE_CODE_{i}']==K[i]^sum(1<<j for j in common)
    contracts['canonical9_actual_before_held_release']=True
   if k==cut:
    assert all(v[f'X{j}']==1<<j and at[f'X{j}']=='Hub'and v[f'NATIVE_RAW_{j}']==1<<j for j in range(111));assert all(v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in T else 0)and at[f'Y{i}']==(f'F{i}'if i in T else'zero')for i in range(111));contracts['all222_cut_columns']=True;break
  typ,n,*q=o
  if typ=='INIT':v[n]=0;at[n]=q[0]
  elif typ=='ADD':v[q[0]]^=v[n]
  elif typ=='MOVE':at[n]=q[0]
  else:del v[n];del at[n]
 pin=save(a.out/'WORD.json',w);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(z/6 for z in moment(gate));q=moment(stats['movement_profile']);proper_visibility={str(i):[j for j in range(111)if j not in T and e.sub(C[f'MASK_CHART_{i}'],C[f'F{j}'])]for i in T};result={'status':'PASS_EARLY_Y_LATE_CANONICAL_ORIGINAL_CARRIERS','word_sha256':pin,'targets':T,'stats':stats,'contracts':contracts,'source_cut':cut,'milestones':marks,'mask_dimensions':{str(i):len(C[f'MASK_CHART_{i}'])for i in T},'unfinished_mask_visibility':proper_visibility,'moment':record(q),'necessary_limiting_room':record((ceiling[0]-q[1],ceiling[1]-q[0])),'scope':w['scope']};save(a.out/'RESULT.json',result);print(json.dumps({k:result[k]for k in ['status','word_sha256','stats','contracts','source_cut','milestones','mask_dimensions','moment','necessary_limiting_room']}))
if __name__=='__main__':main()
