"""Known-mask Hub proxies preserve raw unknown originals at rank-two charts.

Resumes the exact native-cached57 cut; no abstract source/reset substitution.
"""
from pathlib import Path
import argparse,collections,hashlib,importlib.util,json
from build_common_carrier_fanout import binary_basis,coeff,save,moment,record
BASE='research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint5-evidence/R/initial-chart-cut/control/NATIVE-CACHED57-WORD.json'
BASE_SHA='7df1fc8f696545185c417c6df4161b324869bf084b503138506425510e841fa2'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--matching',type=Path);ap.add_argument('--discover-matching',action='store_true');a=ap.parse_args();
 if a.matching is None and not a.discover_matching:ap.error('pass --matching MATCHING.json; --discover-matching is optional candidate discovery only')
 a.out.mkdir(parents=True,exist_ok=True);raw=(a.repo/BASE).read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE_SHA;w0=json.loads(raw);R=json.loads((a.repo/w0['source_path']).read_text())['native_roots'];ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';sp=importlib.util.spec_from_file_location('masked_hub_native',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);S=w0['targets'];U=sorted(set(range(111))-set(S));cut0=w0['carrier_interface_before_operation'];ops=w0['operations'][:cut0].copy();charts=w0['charts'].copy();v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};owners=[]
 for typ,n,*q in ops:
  if typ=='INIT':v[n]=0;at[n]=q[0];owners.append(n)
  elif typ=='ADD':v[q[0]]^=v[n]
  elif typ=='MOVE':at[n]=q[0]
  else:del v[n];del at[n];owners.remove(n)
 unknown_native=[u for u in U if at[f'X{u}']==f'L{u}'];known_native=[c for c in S if at[f'X{c}']==f'L{c}'];unknown_hub=[u for u in U if at[f'X{u}']=='Hub'];assert(len(unknown_native),len(known_native),len(unknown_hub))==(35,57,19);dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));cover=lambda u,c:sum(dot(i,u)==dot(i,c)==0 for i in U)
 if a.matching is not None:
  matching=json.loads(a.matching.read_text());assert matching['parent_word_sha256']==BASE_SHA;pairs=[{'unknown':z['unknown'],'known':z['known'],'unfinished_facets':cover(z['unknown'],z['known'])}for z in matching['pairs']]
 else:
  import numpy as np
  from scipy.optimize import linear_sum_assignment
  matrix=np.array([[cover(u,c)for c in known_native]for u in unknown_native],dtype=np.int64);cost=-matrix*10000+np.array(known_native,dtype=np.int64)[None,:];rr,cc=linear_sum_assignment(cost);pairs=[{'unknown':unknown_native[r],'known':known_native[c],'unfinished_facets':int(matrix[r,c])}for r,c in zip(rr,cc)]
 assert len(pairs)==35 and {p['unknown']for p in pairs}==set(unknown_native) and len({p['known']for p in pairs})==35 and {p['known']for p in pairs}<=set(known_native)
 save(a.out/'MATCHING.json',{'schema':'native57-known-mask-matching-v1','parent_word_sha256':BASE_SHA,'pairs':[dict(p)for p in pairs],'status':'Frozen feasible matching; no optimality claim is a proof premise.'})
 semantic=collections.defaultdict(list);marks={'retained_native57_cut':cut0};ground=w0['source_interface']['ground_raw_names'];oldowners=owners.copy()
 def emit(o,key=None):
  if key:semantic[key].append(len(ops))
  ops.append(o);typ,n,*q=o
  if typ=='INIT':v[n]=0;at[n]=q[0];owners.append(n)
  elif typ=='ADD':v[q[0]]^=v[n]
  elif typ=='MOVE':at[n]=q[0]
  else:del v[n];del at[n];owners.remove(n)
 def init(n,h):emit(['INIT',n,h])
 for k,p in enumerate(pairs):
  u,c=p['unknown'],p['known'];h=f'PROXY_PAIR_{k}';p['chart']=h;charts[h]={'kind':'span','rows':[R[u],R[c]]}
  for j in[u,c]:init(f'PROXY_NATIVE_{j}',f'L{j}');emit(['ADD',f'X{j}',f'PROXY_NATIVE_{j}'],'native_preservation')
  emit(['MOVE',f'X{u}',h],'unknown_low_ascent');emit(['MOVE',f'X{c}',h],'known_low_ascent');emit(['ADD',f'X{u}',f'X{c}'],'known_mask_encoding');emit(['MOVE',f'X{c}','Hub'],'masked_proxy_Hub_arrival')
 marks['all_unknown_information_at_Hub_mod_known']=len(ops)
 um=sum(1<<u for u in U);K=[((1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0))&um for i in U];rows=[];basisroles=[]
 for i,row in zip(U,K):
  if len(binary_basis(rows+[row]))>len(rows):rows.append(row);basisroles.append(i)
 assert len(rows)==9;mapping={p['unknown']:p['known']for p in pairs};hubfields=[];maskfields=[];maskrows=[]
 for k,row in enumerate(rows):
  n=f'UNKNOWN_CANONICAL_PROXY_{k}';m=f'KNOWN_CORRECTION_{k}';hubfields.append(n);maskfields.append(m);init(n,'Hub');init(m,'zero');mask=0
  for u in U:
   if not(row>>u&1):continue
   if u in mapping:
    c=mapping[u];emit(['ADD',f'X{c}',n],'actual_Hub_proxy_reads');emit(['ADD',ground[str(c)],m],'actual_ground_known_reads');mask^=1<<c
   else:emit(['ADD',f'X{u}',n],'actual_Hub_raw_reads')
  assert v[n]==row^mask and v[m]==mask;maskrows.append(mask)
 cut=len(ops);marks['masked_canonical_bank_ready']=cut
 # Freeze the useful actual cut before restoring the low original subsystem.
 cutv=v.copy();cutat=at.copy();allowners=owners.copy()
 for p in pairs:emit(['MOVE',f'X{p["unknown"]}','Hub'],'held_unknown_Hub_return')
 for p in pairs:emit(['ADD',f'X{p["unknown"]}',f'X{p["known"]}'],'actual_proxy_inverse')
 for i in range(111):
  if at[f'X{i}']!='Hub':emit(['MOVE',f'X{i}','Hub'])
 for i in range(111):
  if at[f'Y{i}']!=f'F{i}':emit(['MOVE',f'Y{i}',f'F{i}'])
 for n in allowners:emit(['CLEAR',n])
 w={'schema':'native57-known-mask-Hub-proxy-source-v1','source_path':w0['source_path'],'source_sha256':w0['source_sha256'],'charts':charts,'operations':ops,'targets':S,'carrier_interface_before_operation':cut,'milestones':marks,'parent_word_path':BASE,'parent_word_sha256':BASE_SHA,'construction':{'known_roles':S,'unknown_roles':U,'original_unknown_Hub_roles':unknown_hub,'pairs':pairs,'masked_canonical_basis_roles':basisroles,'canonical_unknown_rows_hex':list(map(hex,rows)),'known_correction_rows_hex':list(map(hex,maskrows)),'Hub_source_fields':hubfields,'ground_correction_fields':maskfields,'old_source_interface':w0['source_interface'],'matching_primary_objective':'maximize total unfinished-facet containment of the35 actual pair charts','matching_total_coverage':sum(p['unfinished_facets']for p in pairs)},'semantic_operation_indices':dict(semantic),'scope':'Actual extension of native-cached57: all54 unknown input directions available in54 Hub originals modulo actual57 ground-known inputs,35 raw unknown originals retained at rank2 charts,22 raw known originals still native, all111 native values preserved. Nine actual masked canonical Hub fields and nine actual ground correction fields; no code delivery, complete supplier or new kappa.'};_,_,stats=e.replay(w,R);_,_,base_stats=e.replay(w0,R);delta=collections.Counter({int(d):n for d,n in stats['movement_profile'].items()});delta.subtract({int(d):n for d,n in base_stats['movement_profile'].items()});delta={d:n for d,n in sorted(delta.items())if n};assert delta=={1:70,6:70,7:-70};C={n:e.chart(z)for n,z in charts.items()};Sset=set(S);knownmask=sum(1<<s for s in S)
 assert all(cutv[f'X{p["unknown"]}']==1<<p['unknown']and cutat[f'X{p["unknown"]}']==p['chart']and len(C[p['chart']])==2 for p in pairs)
 assert all(cutv[f'X{p["known"]}']==(1<<p['unknown'])^(1<<p['known'])and cutat[f'X{p["known"]}']=='Hub'for p in pairs)
 hubrows=[cutv[f'X{i}']for i in range(111)if cutat[f'X{i}']=='Hub'];assert len(hubrows)==54 and len(binary_basis([r&um for r in hubrows]))==54
 for i in range(111):
  assert any(cutat[n]==f'L{i}'and x==1<<i for n,x in cutv.items()),('missing actual native point',i)
  assert cutv[f'Y{i}']==(1<<(111+i))^((1<<i)if i in Sset else 0)
 for k in range(9):assert cutv[hubfields[k]]^cutv[maskfields[k]]==rows[k]
 access=[{'receiver':i,'held_unknown_originals':[p['unknown']for p in pairs if e.sub(C[p['chart']],C[f'F{i}'])],'raw_known_native_originals':[c for c in known_native if c not in mapping.values()and e.sub(C[f'L{c}'],C[f'F{i}'])]}for i in U];pin=save(a.out/'WORD.json',w);save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[{'name':n,'chart':cutat[n],'rank':len(C[cutat[n]]),'row_hex':hex(x)}for n,x in sorted(cutv.items())],'unfinished_movable_access':access,'scope':'Physical state and separate containment counts; no joint route or free code transport asserted.'});gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(z/6 for z in moment(gate));q=moment(stats['movement_profile']);result={'status':'PASS_NATIVE57_MASKED_HUB_WITH35_RAW_UNKNOWN_HELD','word_sha256':pin,'parent_word_sha256':BASE_SHA,'stats':stats,'movement_delta':delta,'moment':record(q),'necessary_limiting_room':record((ceiling[0]-q[1],ceiling[1]-q[0])),'cut':cut,'unknown_Hub_quotient_rank':54,'restricted_canonical_rank':9,'raw_unknown_held_rank2':35,'raw_known_still_native':22,'actual_native_input_values':111,'held_original_access_histogram':dict(collections.Counter(len(z['held_unknown_originals'])for z in access)),'each_unfinished_facet_has_movable_unknown_access':all(z['held_unknown_originals']for z in access),'matching_total_coverage':sum(p['unfinished_facets']for p in pairs),'scope':w['scope']};save(a.out/'RESULT.json',result);print(json.dumps(result))
if __name__=='__main__':main()
