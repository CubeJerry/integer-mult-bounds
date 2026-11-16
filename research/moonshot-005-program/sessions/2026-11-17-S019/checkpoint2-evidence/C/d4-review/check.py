#!/usr/bin/env python3
"""Independent D4 source review, importing only C's own native interpreter."""
import argparse,copy,importlib.util,json
from collections import defaultdict
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--audit-module',type=Path,default=Path(__file__).resolve().parents[1]/'portable'/'audit_cp6.py');a=ap.parse_args();sp=importlib.util.spec_from_file_location('own',a.audit_module);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);need=m.insist
 w=json.loads(a.word.read_text());need(m.sha(a.word)=='20b6e4e1488bcbe475f19461517d5ad3e4be565b823fc9a1017d8581ca4bd336','frozen D4 word');source=a.repo/w['source_path'];need(m.sha(source)=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','root pin');s=json.loads(source.read_text());R=s['native_roots'];T=w['targets'];U=set(range(111))-set(T);data=w['construction'];groups=data['groups'];routes=data['routes'];desc=set(data['descended_groups']);ops=w['operations'];marks=w['milestones'];cut=w['carrier_interface_before_operation'];snap=set(marks.values())|{cut}
 for k,o in enumerate(ops):
  if o[0]in{'ADD','MOVE'}and any(isinstance(x,str)and x.startswith('X')for x in o[1:]):snap|={k,k+1}
 stats,tr,C,events=m.replay(w,s,snap);need(T==[3,4,47,51,74,76,78,80,88,90,92,94]and len(U)==99,'actual target set')
 G=defaultdict(list)
 for j in range(111):G[tuple(i for i in T if sum(x*y for x,y in zip(R[i],R[j]))==0)].append(j)
 common=G.pop(tuple(T));need(common==data['common_roles']and len(common)==12,'actual common roots');need({tuple(g['receivers']):g['donors']for g in groups}==dict(G)and len(groups)==24,'complete disjoint cohorts');J=C['D4_COMMON'];need(J==m.chart({'kind':'ann','rows':[R[i]for i in T]})and len(J)==4,'actual common rank4')
 for g,d in enumerate(groups):need(C[f'GROUP_CHART_{g}']==m.chart({'kind':'ann','rows':[R[i]for i in d['receivers']]})and len(C[f'GROUP_CHART_{g}'])==5,'actual cohort rank5')
 own=[q for q in routes if not q['masked']];masked=[q for q in routes if q['masked']];need(len(own)==18 and len(masked)==12 and len({q['carrier']for q in routes})==30,'thirty distinct actual carriers');need({q['carrier']for q in masked}==set(common),'twelve distinct common masks');need({q['group']for q in own}==set(range(24))-desc and len(desc)==6,'one pivot per retained cohort')
 for q in own:need(q['carrier']in groups[q['group']]['donors'],'pivot is real own donor')
 cv,cl=tr[marks['common_capture_end']];need(cv['COMMON_SUM']==set(common)and C[cl['COMMON_SUM']]==J,'actual common sum')
 for q in masked:
  p=q['carrier'];need(cv[f'RAW_MASK_{p}']=={p}and C[cl[f'RAW_MASK_{p}']]==J and cv[f'X{p}']=={p},'raw mask before mutation')
 gv,gl=tr[marks['group_acquisition_end']]
 for g,d in enumerate(groups):need(gv[f'GROUP_SUM_{g}']==set(d['donors'])and C[gl[f'GROUP_SUM_{g}']]==(J if g in desc else C[f'GROUP_CHART_{g}']),'actual group and custody')
 for q in own:need(gv[f'X{q["carrier"]}']==set(groups[q['group']]['donors'])and C[gl[f'X{q["carrier"]}']]==C[f'GROUP_CHART_{q["group"]}'],'pivot group acquired')
 chronology=[];own_ends=[];mask_starts=[]
 for q in routes:
  r=q['route'];p=q['carrier'];g=q['group'];ds=set(groups[g]['donors']);row=ds^({p}if q['masked']else set());x=f'X{p}';dp=ops.index(['ADD',x,f'ROUTE_{r}_PLANE']);df=ops.index(['ADD',x,f'ROUTE_{r}_FACET']);rest=[k for k,o in enumerate(ops)if o[0]=='ADD'and o[2]==x and o[1].startswith('X')and k>df];arrival=next(k for k in range(df+1,len(ops))if ops[k]==['MOVE',x,'Hub']);need([int(ops[k][1][1:])for k in rest]==sorted(ds if q['masked']else ds-{p}),'exact inverse donor list');pv,pl=tr[dp];fv,fl=tr[df];H=m.chart({'kind':'ann','rows':[R[i]for i in q['plane']]});need(pv[x]==fv[x]==row and C[pl[x]]==H and len(H)==6 and C[fl[x]]==C[f'F{q["end"]}'],'actual route values and copy charts');need(m.subset(C[f'GROUP_CHART_{g}'],H)and m.subset(H,C[f'F{q["end"]}']),'strict real chain')
  for k in rest:
   vv,ll=tr[k];j=int(ops[k][1][1:]);need(vv[f'X{j}']=={j}and C[ll[x]]==C[ll[f'X{j}']]==C['Hub'],'raw actual Hub inverse donor')
  end=(rest[-1]+1)if rest else arrival+1;need(tr[end][0][x]=={p}and C[tr[end][1][x]]==C['Hub'],'actual restored original')
  if q['masked']:
   inj=ops.index(['ADD',f'GROUP_SUM_{g}',x]);iv,il=tr[inj];need(iv[x]=={p}and iv[f'GROUP_SUM_{g}']==ds and C[il[x]]==C[f'GROUP_CHART_{g}'],'real stationary injection source');mask_starts.append(inj)
  else:own_ends.append(end)
  chronology.append({'route':r,'group':g,'carrier':p,'masked':q['masked'],'plane_deposit':dp,'facet_deposit':df,'Hub_arrival':arrival,'restoration_operations':rest,'raw_before':end})
 need(max(own_ends)<min(mask_starts),'own pivots restored before masked inverses');rv,rl=tr[marks['all_originals_restored_before_canonical']]
 for j in range(111):need(rv[f'X{j}']=={j}and C[rl[f'X{j}']]==C['Hub'],'all raw atHub before code')
 v,l=tr[cut];N={i:{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)};K=[N[i]^{i}for i in range(111)];code=[v[f'CANONICAL_{b}']for b in range(9)];basis=m.binary_basis(code);need(len(basis)==9 and all(m.in_span(z,basis)for z in K),'full canonical rowspace')
 for b in range(9):need(C[l[f'CANONICAL_{b}']]==C['zero'],'code physically ground')
 for j in range(111):need(v[f'NATIVE_RAW_{j}']=={j}and C[l[f'NATIVE_RAW_{j}']]==C[f'L{j}'],'native custody');need(v[f'Y{j}']==({111+j,j}if j in T else{111+j})and C[l[f'Y{j}']]==(C[f'F{j}']if j in T else C['zero']),'exact Y source interface')
 for i in T:
  read=data['receiver_reads'][str(i)];need(set(map(int,read['by_group']))=={g for g,z in enumerate(groups)if i in z['receivers']},'exact once-per-cohort incidence');correction=set()
  for kind in['common','group','plane','facet','masks']:
   for n in read[kind]:correction^=v[n]
  need(correction==N[i],'actual copied fields plus masks exactly give foreign row')
 owned=[e for e in events if e[-1]];need(len(owned)==15 and sum(d==8 and src=='Hub'and dst=='zero'for k,n,src,dst,d,z in owned)==9,'owned canonical invoice');need({int(n.rsplit('_',1)[1])for k,n,src,dst,d,z in owned if d==1 and dst=='D4_COMMON'and n.startswith('GROUP_SUM_')}==desc,'six actual group descents');need(stats['counts']=={'INIT':217,'ADD':1193,'MOVE':456,'CLEAR':217}and stats['dirty_clear']==217,'exact instruction counts');need(stats['movement_profile']=={1:144,3:93,4:111,7:99,8:9},'exact rank profile')
 orig={f'X{i}'for i in range(111)}|{f'Y{i}'for i in range(111)};proper=[n for n in v if n not in orig and 1<len(C[l[n]])<8];need(len(proper)==97 and all(not m.subset(C[l[n]],C[f'F{i}'])for i in U for n in proper),'actual97 proper owners inaccessible to99 outsiders');need(len(v)==222+111+9+97,'no hidden source field');need(len(m.reduced(tuple(tuple(R[i])for i in U)))==8,'unfinished facet normals span whole real space');gap=min(len(N[i]-N[h])for i in U for h in U if i!=h);need(gap==21,'last-shared-chart source pair premise')
 need(len({C[f'L{j}']for j in range(111)})==111,'distinct real native lines')
 codewords=[]
 for b in range(512):
  z=set()
  for cbit in range(9):
   if b>>cbit&1:z^=code[cbit]
  codewords.append(z)
 gaps={i:min(len(z-N[i])for z in codewords if z and z!=(N[i]|{i}))for i in U}
 need(min(gaps.values())>=18 and all(not any(z and z<=N[i]for z in codewords)for i in U),'all99 actual canonical uniqueness and alternative gaps')
 normals=[]
 for i in sorted(U):
  if len(m.reduced(tuple(tuple(R[j])for j in normals+[i])))>len(normals):normals.append(i)
 need(len(normals)==8,'explicit normal basis')
 def first(key):return ops[w['semantic_operation_indices'][key][0]]
 chosen=[('raw mask',first('mask_captures')),('pivot coding',first('pivot_coding')),('masked injection',first('masked_injections')),('paid cohort descent',first('cohort_descents')),('proper deposit',['ADD','X51','ROUTE_0_PLANE']),('facet deposit',['ADD','X51','ROUTE_0_FACET']),('pivot inverse',ops[next(k for z in chronology if not z['masked']and z['restoration_operations']for k in z['restoration_operations'])]),('masked inverse',ops[next(k for z in chronology if z['masked']for k in z['restoration_operations'])]),('canonical load',first('canonical_loads')),('receiver mask',['ADD','RAW_MASK_7','Y3'])];controls=[]
 for label,event in chosen:
  bad=copy.deepcopy(w);bad['operations'].remove(event)
  try:m.replay(bad,s)
  except(ValueError,KeyError)as err:controls.append({'omission':label,'operation':event,'rejected':str(err)})
  else:raise ValueError('omission escaped: '+label)
 q=m.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 allowance=tuple(z/6 for z in m.moment(gate));room=(allowance[0]-q[1],allowance[1]-q[0]);need(room[1]<m.power_interval(2)[0]and room[1]<2,'at most one rank-one future descent fits movement screen')
 result={'status':'PASS_INDEPENDENT_D4_ROUTED_COHORT_SOURCE','word_sha256':m.sha(a.word),'source_sha256':w['source_sha256'],'cut':cut,'stats':stats,'targets':T,'unfinished_count':99,'common_roles':common,'actual_disjoint_cohorts':groups,'descending_cohort_indices':sorted(desc),'all30_carrier_chronologies':chronology,'all111_raw_originals_before_canonical':True,'all111_native_caches_at_cut':True,'all99_unfinished_Y_raw_at_ground':True,'canonical_ground_rank':9,'owned_moves':{'rank1_group_to_common':6,'rank8_Hub_to_ground':9},'moment':m.interval_json(q),'necessary_movement_room':m.interval_json(room),'destructive_controls':controls,'changed_source_continuation_premises':{'proper_owners':97,'all_proper_owners_inaccessible_to_all99_unfinished_facets':True,'minimum_ordered_unfinished_pair_neighborhood_difference':gap,'unfinished_normals_real_rank':8,'explicit_unfinished_normal_basis_roles':normals,'canonical_alternative_support_gaps':gaps,'one_descent_gate_added_moment_floor':m.interval_json(m.power_interval(2)),'one_descent_gate_strict_excess':m.interval_json((q[0]+m.power_interval(2)[0]-allowance[1],q[1]+m.power_interval(2)[1]-allowance[0])),'affordable_future_owned_MOVEs':'At most one rank-one descent; two unit descents or any rank-two descent exceed the necessary movement room.'},'scope':'Actual partial twelve-output word, source-aware characteristic-two identities at every width, no route-search optimality or complete supplier/new kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print(stats['counts']);print('Q',m.interval_json(q)['decimal']);print('Necessary movement room',m.interval_json(room)['decimal'])
if __name__=='__main__':main()
