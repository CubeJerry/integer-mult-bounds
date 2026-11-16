"""Literal D4 cohort routing through reversible originals; partial 12-target source.

Search choices are candidate data, not proof.  Every chart, field, operation,
column, source restoration, and price is independently checked by exact replay.
"""
from pathlib import Path
import argparse, collections, hashlib, importlib.util, json
from build_common_carrier_fanout import SOURCE,SOURCE_SHA,binary_basis,coeff,save,moment,record

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--problem',type=Path,default=Path(__file__).with_name('D4-ROUTE-PROBLEM.json'));ap.add_argument('--candidate',type=Path,default=Path(__file__).with_name('D4-HYBRID-HEURISTIC.json'));a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE_SHA;R=json.loads(raw)['native_roots'];P=json.loads(a.problem.read_text());candidate=json.loads(a.candidate.read_text());T=P['targets'];common=P['common'];groups=P['groups'];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));actual=collections.defaultdict(list)
 for j in range(111):actual[tuple(i for i in T if dot(i,j)==0)].append(j)
 assert actual.pop(tuple(T))==common and not actual.get(())
 assert {tuple(g['receivers']):g['donors']for g in groups}==dict(actual)
 bygroup=[[p for p in P['paths']if p['group']==g]for g in range(len(groups))];flags={i:P['flags'][str(i)][candidate['choices'][k]]for k,i in enumerate(T)};selected={g:[bygroup[g][j]for j in candidate['selected_paths'][g]]for g in range(len(groups))}
 extras=sorted([(max(0,len(z)-1),g)for g,z in selected.items()],reverse=True);nextra=sum(x for x,g in extras);desc=[]
 for x,g in extras:
  if nextra<=len(common):break
  desc.append(g);nextra-=x
 for g in desc:selected[g]=[]
 assert nextra<=len(common)
 charts={'Hub':{'kind':'span','rows':[[int(i==j)for j in range(8)]for i in range(8)]},'zero':{'kind':'span','rows':[]},'D4_COMMON':{'kind':'ann','rows':[R[i]for i in T]}}
 for i in range(111):charts[f'L{i}']={'kind':'span','rows':[R[i]]};charts[f'F{i}']={'kind':'ann','rows':[R[i]]}
 for g,G in enumerate(groups):charts[f'GROUP_CHART_{g}']={'kind':'ann','rows':[R[i]for i in G['receivers']]}
 for k,p in enumerate(P['planes']):charts[f'PLANE_CHART_{k}']={'kind':'ann','rows':[R[i]for i in p]}
 planeindex={tuple(p):k for k,p in enumerate(P['planes'])};ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';s=importlib.util.spec_from_file_location('native_d4',ep);e=importlib.util.module_from_spec(s);s.loader.exec_module(e);C={h:e.chart(z)for h,z in charts.items()};assert len(C['D4_COMMON'])==4;assert all(len(C[f'GROUP_CHART_{g}'])==5 for g in range(24));assert all(len(C[f'PLANE_CHART_{k}'])==6 for k in range(len(P['planes'])))
 ops=[];owners=[];semantic=collections.defaultdict(list);marks={};routes=[];cursor=0
 def emit(o,key=None):
  if key:semantic[key].append(len(ops))
  ops.append(o)
 def init(n,h):owners.append(n);emit(['INIT',n,h])
 for g,paths in selected.items():
  for k,p in enumerate(paths):
   masked=k>0;carrier=common[cursor]if masked else groups[g]['donors'][0]
   if masked:cursor+=1
   q=dict(p,carrier=carrier,masked=masked,route=len(routes));routes.append(q)
 assert cursor==nextra
 for i in range(111):init(f'NATIVE_RAW_{i}',f'L{i}');emit(['ADD',f'X{i}',f'NATIVE_RAW_{i}'],'native_captures')
 init('COMMON_SUM','D4_COMMON');maskedcarriers={q['carrier']for q in routes if q['masked']}
 for j in common:
  emit(['MOVE',f'X{j}','D4_COMMON']);emit(['ADD',f'X{j}','COMMON_SUM'],'common_captures')
  if j in maskedcarriers:init(f'RAW_MASK_{j}','D4_COMMON');emit(['ADD',f'X{j}',f'RAW_MASK_{j}'],'mask_captures')
  else:emit(['MOVE',f'X{j}','Hub'])
 marks['common_capture_end']=len(ops)
 for g,G in enumerate(groups):
  h=f'GROUP_CHART_{g}';z=f'GROUP_SUM_{g}';init(z,h);pivot=next((q['carrier']for q in routes if q['group']==g and not q['masked']),None)
  if pivot is not None:
   emit(['MOVE',f'X{pivot}',h]);emit(['ADD',f'X{pivot}',z],'group_captures')
  for j in G['donors']:
   if j==pivot:continue
   emit(['MOVE',f'X{j}',h]);emit(['ADD',f'X{j}',z],'group_captures')
   if pivot is not None:emit(['ADD',f'X{j}',f'X{pivot}'],'pivot_coding')
   emit(['MOVE',f'X{j}','Hub'])
  if g in desc:emit(['MOVE',z,'D4_COMMON'],'cohort_descents')
 marks['group_acquisition_end']=len(ops)
 # Own-donor pivots all reach Hub and restore before common masked carriers use them.
 for q in sorted(routes,key=lambda q:q['masked']):
  g=q['group'];j=q['carrier'];r=q['route'];h=f'GROUP_CHART_{g}'
  if q['masked']:emit(['MOVE',f'X{j}',h]);emit(['ADD',f'GROUP_SUM_{g}',f'X{j}'],'masked_injections')
  if q['plane']is not None:
   ph=f'PLANE_CHART_{planeindex[tuple(q["plane"]) ]}';emit(['MOVE',f'X{j}',ph]);init(f'ROUTE_{r}_PLANE',ph);emit(['ADD',f'X{j}',f'ROUTE_{r}_PLANE'],'route_deposits')
  fh=f'F{q["end"]}';emit(['MOVE',f'X{j}',fh]);init(f'ROUTE_{r}_FACET',fh);emit(['ADD',f'X{j}',f'ROUTE_{r}_FACET'],'route_deposits');emit(['MOVE',f'X{j}','Hub'])
  for d in groups[g]['donors']:
   if not q['masked']and d==j:continue
   emit(['ADD',f'X{d}',f'X{j}'],'carrier_restorations')
 marks['all_originals_restored_before_canonical']=len(ops)
 K=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];rows=[];basisroles=[]
 for i,row in enumerate(K):
  if len(binary_basis(rows+[row]))>len(rows):rows.append(row);basisroles.append(i)
 assert len(rows)==9;B=binary_basis(rows);decode={i:coeff(B,K[i])for i in T};canonical=[]
 for k,row in enumerate(rows):
  n=f'CANONICAL_{k}';canonical.append(n);init(n,'Hub')
  for j in range(111):
   if row>>j&1:emit(['ADD',f'X{j}',n],'canonical_loads')
  emit(['MOVE',n,'zero'],'canonical_descents')
  for i in T:
   if decode[i]>>k&1:emit(['ADD',n,f'Y{i}'],'canonical_preloads')
 marks['canonical_before_Y_departure']=len(ops);reads={}
 for i in T:
  f=flags[i];read={'common':['COMMON_SUM'],'group':[],'plane':[],'facet':[],'masks':[],'by_group':{}}
  for g,G in enumerate(groups):
   if i not in G['receivers']:continue
   if g in desc:n=f'GROUP_SUM_{g}';where='common'
   elif g==f['first_group']:n=f'GROUP_SUM_{g}';where='group'
   else:
    match=[q for q in routes if q['group']==g and(q['plane']==f['plane']or q['end']==i)];assert match,(i,g,f);q=min(match,key=lambda q:(q['masked'],q['route']));r=q['route']
    if q['plane']==f['plane']:n=f'ROUTE_{r}_PLANE';where='plane'
    else:n=f'ROUTE_{r}_FACET';where='facet'
    if q['masked']:read['masks'].append(f'RAW_MASK_{q["carrier"]}')
   read[where].append(n);read['by_group'][str(g)]={'field':n,'where':where}
  reads[str(i)]=read;emit(['MOVE',f'Y{i}','D4_COMMON'])
  for n in read['common']+read['masks']:emit(['ADD',n,f'Y{i}'],'receiver_reads')
  emit(['MOVE',f'Y{i}',f'GROUP_CHART_{f["first_group"]}'])
  for n in read['group']:emit(['ADD',n,f'Y{i}'],'receiver_reads')
  emit(['MOVE',f'Y{i}',f'PLANE_CHART_{planeindex[tuple(f["plane"]) ]}'])
  for n in read['plane']:emit(['ADD',n,f'Y{i}'],'receiver_reads')
  emit(['MOVE',f'Y{i}',f'F{i}'])
  for n in read['facet']:emit(['ADD',n,f'Y{i}'],'receiver_reads')
 cut=len(ops)
 for i in range(111):
  if i not in T:emit(['MOVE',f'Y{i}',f'F{i}'])
 for n in owners:emit(['CLEAR',n])
 w={'schema':'d4-routed-cohort-hybrid-v1','source_path':SOURCE,'source_sha256':SOURCE_SHA,'charts':charts,'operations':ops,'targets':T,'carrier_interface_before_operation':cut,'milestones':marks,'construction':{'common_roles':common,'groups':groups,'descended_groups':desc,'routes':routes,'flags':flags,'receiver_reads':reads,'canonical_basis_roles':basisroles,'canonical_fields':canonical,'native_cache_count':111,'problem_sha256':hashlib.sha256(a.problem.read_bytes()).hexdigest(),'candidate_sha256':hashlib.sha256(a.candidate.read_bytes()).hexdigest()},'semantic_operation_indices':dict(semantic),'scope':'Literal partial 12-target source with six unit cohort descents plus nine canonical ground descents; reversible own-donor and common masked original fanout across rank5/6/7 charts. All99 unfinished Y raw atground atcut. No complete supplier; no new kappa.'}
 _,_,stats=e.replay(w,R);values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 for k,o in enumerate(ops[:cut]):
  if k==marks['all_originals_restored_before_canonical']:assert all(values[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111))
  typ,n,*q=o
  if typ=='INIT':values[n]=0;at[n]=q[0]
  elif typ=='ADD':values[q[0]]^=values[n]
  elif typ=='MOVE':at[n]=q[0]
  else:del values[n];del at[n]
 assert all(values[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111));assert all(values[f'NATIVE_RAW_{i}']==1<<i and at[f'NATIVE_RAW_{i}']==f'L{i}'for i in range(111));assert all(values[f'Y{i}']==(1<<(111+i))^((1<<i)if i in T else 0)and at[f'Y{i}']==(f'F{i}'if i in T else'zero')for i in range(111))
 for k,n in enumerate(canonical):assert values[n]==rows[k]and at[n]=='zero'
 for q in routes:
  row=sum(1<<j for j in groups[q['group']]['donors'])^((1<<q['carrier'])if q['masked']else 0);assert values[f'ROUTE_{q["route"]}_FACET']==row
  if q['plane']is not None:assert values[f'ROUTE_{q["route"]}_PLANE']==row
 pin=save(a.out/'WORD.json',w);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(z/6 for z in moment(gate));q=moment(stats['movement_profile']);result={'status':'PASS_D4_ROUTED_COHORT_HYBRID','word_sha256':pin,'targets':T,'completed_outputs':len(T),'unfinished_outputs':111-len(T),'descended_groups':desc,'common_carriers_used':nextra,'unmasked_pivots_used':sum(not z['masked']for z in routes),'total_routes':len(routes),'stats':stats,'all222_columns':True,'all_X_restored_before_nine_canonical_loads':True,'source_cut':cut,'moment':record(q),'necessary_limiting_room':record((ceiling[0]-q[1],ceiling[1]-q[0])),'scope':w['scope']};save(a.out/'RESULT.json',result);print(json.dumps(result))
if __name__=='__main__':main()
