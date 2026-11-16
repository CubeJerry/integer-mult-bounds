"""Actual two-stage packet histories and cyclic lower decoders, all222 columns."""
import argparse,copy,hashlib,importlib.util,json,math
from pathlib import Path
from sympy import Matrix
PINS={'dd0af2d4467b722c1692fb60b883407b4a95a8ea10b112fca0683dfc4a930edf','bd7fd31ba6cfe1bc92d26619e513184e6ce5864653cf58be7e9b68668be0d987'}
PRIMARIES=[21,64,65]
FRAMES=[[16,18],[23,71,81],[22,68,85]]
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(path,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();path.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def ints(rows):
 ans=[]
 for row in rows:
  d=math.lcm(*(int(x.q) if hasattr(x,'q')else 1 for x in row));ans.append([int(d*x)for x in row])
 return ans
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.word.read_bytes();pin=hashlib.sha256(raw).hexdigest();assert pin in PINS;w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots']
 e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','lower_engine');tr=load(Path(__file__).with_name('build_d4_cohort.py'),'lower_trace');price=load(Path(__file__).with_name('price_d4_cohort.py'),'lower_price');C,_,before=e.replay(w,R);bt=tr.trace(w['operations']);oldcut=w['cohort']['continuation_before_operation'];charts=copy.deepcopy(w['charts']);packets=['P0','P1','P2'];upper=['KEEP_C0','KEEP_C1','KEEP_C2'];lower=['TRIAD'+str(f[0])for f in FRAMES]
 immutable=set(sum(FRAMES,[]));mutable=set(PRIMARIES);D=immutable|mutable;names={f'X{i}'for i in D};ys={f'Y{i}'for i in D};assert not D&set(w['cohort']['targets']);assert not any(o[0]=='ADD'and o[2]in{f'X{i}'for i in immutable}for o in w['operations']);assert not any(o[0]=='ADD'and o[1].startswith('Y')for o in w['operations'])
 caps={p:w['operations'].index(['ADD',p,f])for p,f in zip(packets,upper)};lcaps={p:w['operations'].index(['ADD',p,f])for p,f in zip(packets,lower)};resets={p:w['operations'].index(['ADD',f,p])for p,f in zip(packets,lower)}
 mutable_reads=[];mutable_writes=[]
 for k,o in enumerate(w['operations']):
  if o[0]=='ADD'and o[1]in{f'X{i}'for i in mutable}:assert o[2]in packets and k<caps[o[2]],(k,o);mutable_reads.append([k,o])
  if o[0]=='ADD'and o[2]in{f'X{i}'for i in mutable}:mutable_writes.append([k,o])
 assert len(mutable_writes)==6
 commons=[]
 for j,frame in enumerate(FRAMES):
  aa=PRIMARIES[j];t=frame[0];normal=Matrix(C['J'+str(t)]).nullspace();rec={'kind':'ann','rows':ints(normal)+[R[frame[1]]]};lab=f'LOWER_COMMON_{j}';charts[lab]=rec;Z=e.chart(rec);assert len(Z)==3 and e.sub(Z,C['J'+str(t)]);assert e.sub(Z,C[f'F{aa}']);commons.append(lab)
  assert all(e.sub(Z,C[f'F{i}'])and sum(x*y for x,y in zip(R[i],R[aa]))==0 for i in frame)
  assert all(sum(x*y for x,y in zip(R[i],R[k]))==0 for i in frame for k in frame if i!=k)
  for start,i in enumerate(frame):
   for size in range(1,len(frame)):
    inter=[frame[(start+h)%len(frame)]for h in range(size)];fl=f'LOWER_FLAG_{j}_{i}_{size}';charts[fl]={'kind':'span','rows':ints(Z)+[R[k]for k in inter]};assert len(e.chart(charts[fl]))==3+size and e.sub(e.chart(charts[fl]),C[f'F{aa}'])
 ops=[];newowners=[];caches=[]
 def add(*rows):ops.extend([list(z)for z in rows])
 for j,(aa,frame)in enumerate(zip(PRIMARIES,FRAMES)):
  snap=f'LOWER_INITIAL_Y{j}';newowners.append(snap);add(('MOVE',f'Y{aa}','M0'),('INIT',snap,'M0'),('ADD',f'Y{aa}',snap),('MOVE',f'Y{aa}',f'F{aa}'))
  for i in frame:
   for size in range(1,len(frame)):
    name=f'LOWER_RAW_{j}_{i}_{size}';lab=f'LOWER_FLAG_{j}_{i}_{size}';newowners.append(name);caches.append(name);add(('MOVE',f'X{i}',lab),('INIT',name,lab),('ADD',f'X{i}',name))
   add(('MOVE',f'X{i}',f'F{aa}'),('ADD',f'X{i}',f'Y{aa}'),('MOVE',f'X{i}','Hub'))
  add(('MOVE',f'X{aa}','Hub'))
 prelude=len(ops);mapping={};removed=[];cells=[];cut=None;decode_start=None;descent_indices=[]
 for k,o in enumerate(w['operations']):
  if k==oldcut:
   decode_start=len(ops)
   for j,f in enumerate(lower):descent_indices.append(len(ops));add(('MOVE',f,commons[j]))
   for j,(f,frame)in enumerate(zip(lower,FRAMES)):
    for idx,i in enumerate(frame):
     add(('MOVE',f'Y{i}',commons[j]),('ADD',f,f'Y{i}'))
     for size in range(1,len(frame)):
      foreign=frame[(idx-size)%len(frame)];add(('MOVE',f'Y{i}',f'LOWER_FLAG_{j}_{foreign}_{size}'),('ADD',f'LOWER_RAW_{j}_{foreign}_{size}',f'Y{i}'))
     add(('MOVE',f'Y{i}',f'F{i}'))
   cut=len(ops)
  typ,n,*q=o;skip=(typ=='MOVE'and n in names)or(typ=='ADD'and(n in names or q[0]in names))or n in ys or(typ=='ADD'and q[0]in ys)
  if typ=='ADD'and q[0]in packets and k<lcaps[q[0]]:skip=True
  if skip:removed.append([k,o]);mapping[k]=len(ops);continue
  oo=o.copy()
  if typ=='MOVE'and n in packets and bt[k][1][n]=='Hub':
   j=int(n[1:]);aa=PRIMARIES[j]
   for i in [aa]+FRAMES[j]:add(('ADD',f'X{i}',n))
   oo[2]=f'F{aa}';add(oo);pos=len(ops);add(('ADD',n,f'Y{aa}'),('ADD',f'Y{aa}',n));cells.append({'packet':n,'primary':aa,'before_operation':pos,'after_operation':len(ops)});mapping[k]=len(ops);continue
  if typ=='ADD'and n in packets and q[0]in upper:
   j=int(n[1:]);add(('ADD',f'LOWER_INITIAL_Y{j}',n),oo,('CLEAR',f'LOWER_INITIAL_Y{j}'));mapping[k]=len(ops);continue
  add(oo);mapping[k]=len(ops)
 assert cut is not None and len(cells)==3
 add(*[('CLEAR',n)for n in caches]);nw=copy.deepcopy(w);nw.update(schema='two-stage-primary-feedback-lower-clique-native-v1',base_word_sha256=pin,charts=charts,operations=ops,targets=sorted(set(w['targets'])|D),released_carriers=sorted(set(w['released_carriers'])-D),carrier_interface_before_operation=cut,lower_history={'primaries':PRIMARIES,'frames':FRAMES,'common_charts':commons,'upper_fields':upper,'lower_fields':lower,'feedback_cells':cells,'new_unit_descent_operations':descent_indices,'prelude_end':prelude,'decode_start':decode_start,'continuation_before_operation':cut,'mutable_originals':PRIMARIES,'deleted_mutable_reads':mutable_reads,'deleted_mutable_writes':mutable_writes,'projected_immutable_inputs':sorted(immutable)},scope='Five actual new own-coordinate receivers. Three first primary feedback cells purify a clique code at M0, preserve it through the paid M0-to-J descent, and reuse the actual TRIAD capture/reset. Three additional unit descents expose clique sums below J; every local cache is captured along an original input ascent before source loads. All owned cut fields pureX. No all111 completion or kappa.')
 nw['retained_d4_cohort']={z:copy.deepcopy(w['cohort'][z])for z in['meet','targets','frames','fields']};del nw['cohort']
 CC,_,after=e.replay(nw,R);nt=tr.trace(ops);v,at=nt[cut];xm=(1<<111)-1
 for j,(f,up,frame)in enumerate(zip(lower,upper,FRAMES)):
  code=sum(1<<i for i in frame);assert v[f]==v[up]==code and at[f]==commons[j]and CC[at[up]]==CC['M0'],(j,hex(v[f]),hex(v[up]),hex(code),at[f],at[up])
  cap=ops.index(['ADD',packets[j],f]);reset=ops.index(['ADD',f,packets[j]]);assert nt[cap][0][packets[j]]==code and nt[reset+1][0][packets[j]]==0
 for i in range(111):
  assert v[f'X{i}']==1<<i
  if i in nw['released_carriers']:assert at[f'X{i}']==f'L{i}'
  if i not in nw['targets']:assert v[f'Y{i}']==1<<(111+i)and at[f'Y{i}']=='zero'
 for cell,frame in zip(cells,FRAMES):
  aa=cell['primary'];q=sum(1<<i for i in frame);vv,_=nt[cell['before_operation']];assert vv[cell['packet']]==(1<<aa)^q and vv[f'Y{aa}']==(1<<(111+aa))^q;vv,_=nt[cell['after_operation']];assert vv[cell['packet']]==(1<<(111+aa))^q and vv[f'Y{aa}']==(1<<(111+aa))^(1<<aa)
 mask=sum(1<<i for i in D);comparisons=0
 for k,o in enumerate(w['operations']):
  if k>=oldcut:break
  ov,oa=bt[k+1];vv,aa=nt[mapping[k]]
  for n,z in ov.items():
   if n in names|ys or n in upper+lower or(n in packets and k<=resets[n]):continue
   assert n in vv and vv[n]==(z&~mask),(k,o,n,hex(vv.get(n,0)),hex(z&~mask))
   assert CC[aa[n]]==C[oa[n]],(k,n,'chart');comparisons+=1
 original={f'{s}{i}'for s in['X','Y']for i in range(111)};owned={n:z for n,z in v.items()if n not in original};assert all(z>>111==0 for z in owned.values());support=0
 for z in owned.values():support|=z
 for i in range(111):support|=v[f'Y{i}']^(1<<(111+i))
 S=[i for i in range(111)if support>>i&1];ground={n:z for n,z in owned.items()if len(CC[at[n]])==0 and z};gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 limit=tuple(x/6 for x in price.moment(gate));q=price.moment(after['movement_profile']);oq=price.moment(before['movement_profile']);a.out.mkdir(parents=True,exist_ok=True);sha=write(a.out/'WORD.json',nw)
 result={'status':'PASS_ACTUAL_TWO_STAGE_LOWER_HISTORY57','word_sha256':sha,'base_word_sha256':pin,'before':before,'after':after,'new_targets':sorted(set(nw['targets'])-set(w['targets'])),'all_targets':nw['targets'],'interface':cut,'lower_history':nw['lower_history'],'native_carrier_count':len(nw['released_carriers']),'remaining_ground_Y':111-len(nw['targets']),'full_cut_nonidentity_X_support':S,'full_cut_nonidentity_X_support_count':len(S),'owned_X_rank':len(e.bb(owned.values())),'owned_Y_rank':0,'ground_nonzero_owner_count':len(ground),'ground_X_rank':len(e.bb(ground.values())),'projected_old_state_comparisons':comparisons,'removed_old_operations':removed,'whole_moment':price.record(q),'moment_increment':price.record((q[0]-oq[1],q[1]-oq[0])),'necessary_limiting_room':price.record((limit[0]-q[1],limit[1]-q[0])),'scope':nw['scope']};write(a.out/'RESULT.json',result);print(json.dumps({k:result[k]for k in['status','word_sha256','after','new_targets','full_cut_nonidentity_X_support_count','whole_moment','necessary_limiting_room']}))
if __name__=='__main__':main()
