#!/usr/bin/env python3
"""Independent native review of A's primary-Y changing-history words."""
import argparse,copy,hashlib,itertools,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
PINS={
 'pruned78':('dd0af2d4467b722c1692fb60b883407b4a95a8ea10b112fca0683dfc4a930edf','c7e48e002da3ce642707b25d74dc15d0915945f319053eb97f2016045afe4615'),
 'paid46':('bd7fd31ba6cfe1bc92d26619e513184e6ce5864653cf58be7e9b68668be0d987','2d285de61add9fd9eb23bfaa3b9723a70382f56eb4faa5e4dc886a09e74f56f0')}
FRAMES=[[3,4,47,51],[74,80,90,92],[76,78,88,94]]
PRIMARIES=[4,74,78]

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--base',choices=PINS,required=True);a=ap.parse_args()
 bp=a.work/('A/d4-cohort-'+a.base)/'WORD.json';wp=a.work/('A/d4-feedback-'+a.base)/'WORD.json'
 br,wr=bp.read_bytes(),wp.read_bytes()
 require((hashlib.sha256(br).hexdigest(),hashlib.sha256(wr).hexdigest())==PINS[a.base],'pinned pure/feedback words')
 b,w=json.loads(br),json.loads(wr);sr=(a.repo/w['source_path']).read_bytes()
 require(hashlib.sha256(sr).hexdigest()==b['source_sha256']==w['source_sha256'],'native root pin')
 R=json.loads(sr)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
 for i in range(N):
  require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]}),'actual native line')
  require(C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'actual native facet')
 for n,z in b['charts'].items():require(w['charts'][n]==z,'inherited exact chart')
 before,bt,_=replay(b,collect=True);after,nt,_=replay(w,collect=True)
 require(w['targets']==b['targets']and len(w['targets'])==52,'same52 outputs')
 meta=w['cohort_feedback'];common=w['cohort']['meet'];cv=C[common]
 require(meta['frames']==FRAMES and meta['primaries']==PRIMARIES,'literal primary partition')
 D=sorted(i for g in FRAMES for i in g);others=[[i for i in g if i!=p]for g,p in zip(FRAMES,PRIMARIES)]
 pre=meta['prelude_end'];pv,pa=nt[pre];cache_names=[]
 expected_precoats=[['ADD',f'Y{p}',f'Y{i}']for p,g in zip(PRIMARIES,others)for i in g]
 require(w['operations'][:9]==expected_precoats,'actual ground precoat operations')
 for group,p,rest in zip(FRAMES,PRIMARIES,others):
  require(all(sum(x*y for x,y in zip(R[i],R[j]))==0 for i,j in itertools.combinations(group,2)),'orthogonal group')
  require(pv[f'Y{p}']==(1<<(N+p))^sum(1<<i for i in rest)and pa[f'Y{p}']==f'F{p}','actual primary local field at facet')
  for idx,j in enumerate(rest):
   require(pv[f'Y{j}']==(1<<(N+j))^(1<<(N+p))and pa[f'Y{j}']=='zero','actual precoat arbitrary y at ground')
   for k in [1,2]:
    interval=[rest[(idx+h)%3]for h in range(k)]
    expected=rref(cv+tuple(tuple(R[h])for h in interval))[0]
    name=f'D4_FB_RAW_{j}_{k}';loc=f'D4_FB_FLAG_{j}_{k}';cache_names.append(name)
    require(C[loc]==expected and len(expected)==4+k,'actual cyclic raw-cache chart')
    require(pv[name]==1<<j and pa[name]==loc,'actual raw stationary record')
    require(not any(o[0]=='MOVE'and o[1]==name for o in w['operations']),'cache stationarity')
  for j in group:require(pv[f'X{j}']==1<<j and pa[f'X{j}']=='Hub','source original raw at actual Hub')
 cells=[]
 for g,p,rest,packet,field,cell in zip(FRAMES,PRIMARIES,others,['P3','P4','P5'],['ZFIRST3','ZFIRST4','ZFIRST5'],meta['feedback_cells']):
  q=cell['before_operation'];v,at=nt[q]
  require(w['operations'][q:q+2]==[['ADD',packet,f'Y{p}'],['ADD',f'Y{p}',packet]],'actual feedback cell order')
  require(at[packet]==at[f'Y{p}']==f'F{p}','real primary facet feedback')
  require(v[packet]==sum(1<<i for i in g)and v[f'Y{p}']==(1<<(N+p))^sum(1<<i for i in rest),'actual cell inputs')
  v,at=nt[q+2];dirty=(1<<(N+p))^sum(1<<i for i in rest)
  require(v[packet]==dirty and v[f'Y{p}']==(1<<(N+p))^(1<<p),'primary completes and packet changes history')
  cap=w['operations'].index(['ADD',packet,field]);reset=w['operations'].index(['ADD',field,packet]);down=w['operations'].index(['MOVE',field,common])
  require(q+2<=cap<reset<down,'proper source-time chronology')
  require(nt[cap][0][packet]==dirty and nt[reset][0][field]==dirty,'actual dirty first retention')
  require(nt[reset+1][0][packet]==0,'all arbitrary-y packet residue reset')
  cells.append({'primary':p,'packet':packet,'cell':q,'capture':cap,'reset':reset,'descent':down,'dirty_row_hex':hex(dirty)})
 oldcut=b['cohort']['continuation_before_operation'];bv,ba=bt[oldcut]
 originals={f'{p}{i}'for p in ['X','Y']for i in range(N)}
 ground=sorted(n for n,z in bv.items()if n not in originals and z and len(C[ba[n]])==0)
 require(len(ground)==25,'actual predecessor25 ground fields')
 def interface(ww):
  _,tr,_=replay(ww,collect=True);v,at=tr[ww['cohort_feedback']['continuation_before_operation']]
  for n in ground:require(v[n]==bv[n]and len(C[at[n]])==0,('named ground field',n))
  for p,g,f in zip(PRIMARIES,others,['ZFIRST3','ZFIRST4','ZFIRST5']):
   require(v[f]==(1<<(N+p))^sum(1<<i for i in g)and C[at[f]]==cv,('actual dirty common field',f))
  for i in range(N):
   require(v[f'X{i}']==1<<i,'cut original raw')
   if i in ww['released_carriers']:require(at[f'X{i}']==f'L{i}','actual retained native original')
   if i in ww['targets']:require(v[f'Y{i}']==(1<<(N+i))^(1<<i)and at[f'Y{i}']==f'F{i}','actual completed output')
   else:require(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero','actual raw unfinished ground output')
  owned={n:z for n,z in v.items()if n not in originals}
  yrows={n:z>>N for n,z in owned.items()if z>>N}
  require(yrows=={f'ZFIRST{j}':1<<p for j,p in zip([3,4,5],PRIMARIES)},'exact owned y signature')
  return v,at,owned
 values,locations,owned=interface(w)
 require(w['released_carriers']==b['released_carriers'],'retained original interface unchanged')
 require(len(w['released_carriers'])==(72 if a.base=='pruned78'else 0),'actual native count')
 # Match the unchanged literal core, allowing only the six actual feedback ADDs.
 pos=pre;active=set();compared=0
 for k in range(b['cohort']['prelude_end'],b['cohort']['decode_begin']):
  o=b['operations'][k]
  require(w['operations'][pos]==o,('retained literal core',k,pos));pos+=1
  if o[0]=='MOVE'and o[1]in{'P3','P4','P5'}and o[2]==f'F{PRIMARIES[int(o[1][1:])-3]}':
   active.add(o[1]);pos+=2
  if o[0]=='ADD'and o[1]in{'ZFIRST3','ZFIRST4','ZFIRST5'}and o[2]in active:active.remove(o[2])
  ov,oa=bt[k+1];nv,na=nt[pos]
  for n,z in ov.items():
   if n.startswith('D4_RAW_')or n in active or n in{'ZFIRST3','ZFIRST4','ZFIRST5'}or(n.startswith('Y')and int(n[1:])in D):continue
   require(n in nv and nv[n]==z and C[na[n]]==C[oa[n]],('unaffected old state',k,n));compared+=1
 require(pos==meta['decode_begin'],'entire old core exhausted exactly')
 controls=[]
 def reject(label,bad,check=replay):
  try:check(bad)
  except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
  else:raise ValueError(('accepted feedback mutation',label))
 for label,event in [
  ('omit original-Y precoat',['ADD','Y4','Y3']),
  ('omit primary local observation',['ADD','X3','Y4']),
  ('omit actual changing-history feedback',['ADD','Y4','P3']),
  ('omit dirty reset',['ADD','ZFIRST3','P3']),
  ('omit stationary raw capture',['ADD','X3','D4_FB_RAW_3_1']),
  ('omit actual common descent',['MOVE','ZFIRST3',common]),
  ('omit owned retirement',['CLEAR','D4_FB_RAW_3_1'])]:
  bad=copy.deepcopy(w);bad['operations'].remove(event);reject(label,bad)
 cut=meta['continuation_before_operation'];bad=copy.deepcopy(w)
 bad['operations'].insert(cut,['ADD','ZFIRST4','ZFIRST3'])
 bad['cohort_feedback']['continuation_before_operation']=cut+1
 replay(bad);reject('post-decoder owned Y-signature alteration',bad,interface)
 xm=(1<<N)-1;support=0
 for z in owned.values():support|=z&xm
 for i in range(N):support|=values[f'Y{i}']&xm
 S=[i for i in range(N)if support>>i&1]
 require(len(S)==(54 if a.base=='pruned78'else 111),'exact X support size')
 if a.base=='pruned78':require(set(S)==set(w['targets'])|{61,67},'exact reset support S54')
 expected=({'INIT':112,'ADD':408,'MOVE':404,'CLEAR':112}if a.base=='pruned78'else{'INIT':145,'ADD':737,'MOVE':520,'CLEAR':145})
 require(after['counts']==expected,'complete instruction counts')
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6);q=moment(after['movement_profile']);oq=moment(before['movement_profile'])
 result={'status':'PASS_INDEPENDENT_D4_PRIMARY_Y_CHANGING_HISTORY','base_kind':a.base,
  'pure_word_sha256':PINS[a.base][0],'word_sha256':PINS[a.base][1],'native_source_sha256':w['source_sha256'],
  'before':before,'after':after,'all222_endpoints':True,'targets':w['targets'],'feedback_cells':cells,
  'actual_stationary_raw_caches':cache_names,'all25_ground_fields_unchanged':ground,
  'actual_common_owned_Y_signature':{f'ZFIRST{j}':p for j,p in zip([3,4,5],PRIMARIES)},
  'retained_native_originals':w['released_carriers'],'unfinished_ground_Y_count':N-len(w['targets']),
  'interface_index':cut,'unaffected_old_state_comparisons':compared,
  'live_owner_count':len(owned),'owner_X_rank':len(binary_basis(z&xm for z in owned.values())),
  'owner_Y_rank':len(binary_basis(z>>N for z in owned.values())),
  'full_owner_rank':len(binary_basis(owned.values())),'source_X_support':S,'source_X_support_size':len(S),
  'whole_moment':record(q),'moment_change':record((q[0]-oq[1],q[1]-oq[0])),
  'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'controls':controls,
  'scope':'Actual changing-history service with arbitrary original-Y inputs, real capture/reset/descent, full222 endpoints, source contracts and complete pricing. Five foundations remain; no all111 or kappa claim.'}
 if a.base=='pruned78':
  result['conditional_Y_skeleton_closed_prefix_profile']={1:54,3:3,4:3,7:219}
  result['conditional_Y_skeleton_closed_prefix_moment']=record(moment(result['conditional_Y_skeleton_closed_prefix_profile']))
  result['Y_skeleton_scope']='Three actual primary-Y copies at commonC reproduce all owned y-columns. Ground X preloads must precede these copies. Any future continuation still needs the actual invertible-X restoration condition.'
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in ['status','base_kind','after','owner_X_rank','owner_Y_rank','full_owner_rank','whole_moment']},indent=2))
if __name__=='__main__':main()
