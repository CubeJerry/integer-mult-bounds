"""Changing-history D4 variant; independent original-Y inputs remain explicit."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
PINS={'dd0af2d4467b722c1692fb60b883407b4a95a8ea10b112fca0683dfc4a930edf','bd7fd31ba6cfe1bc92d26619e513184e6ce5864653cf58be7e9b68668be0d987'}
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(path,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();path.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()in PINS
 w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots']
 e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','feedback_engine');b=load(Path(__file__).with_name('build_d4_cohort.py'),'feedback_trace')
 C,_,before=e.replay(w,R);old_trace=b.trace(w['operations']);frames=w['cohort']['frames'];primaries=[4,74,78];common=w['cohort']['meet'];charts=copy.deepcopy(w['charts']);remaining=[[i for i in f if i!=p]for f,p in zip(frames,primaries)];ops=[];caches=[]
 def add(*rows):ops.extend([list(r)for r in rows])
 precoats=[]
 for p,others in zip(primaries,remaining):
  for i in others:precoats.append(len(ops));add(('ADD',f'Y{p}',f'Y{i}'))
 for frame,p,others in zip(frames,primaries,remaining):
  add(('MOVE',f'Y{p}',f'F{p}'))
  for start,j in enumerate(others):
   for k in(1,2):
    interval=[others[(start+h)%3]for h in range(k)];lab=f'D4_FB_FLAG_{j}_{k}';charts[lab]={'kind':'ann','rows':[R[z]for z in frame if z not in interval]};assert len(e.chart(charts[lab]))==4+k
    name=f'D4_FB_RAW_{j}_{k}';caches.append(name);add(('MOVE',f'X{j}',lab),('INIT',name,lab),('ADD',f'X{j}',name))
   add(('MOVE',f'X{j}',f'F{p}'),('ADD',f'X{j}',f'Y{p}'),('MOVE',f'X{j}','Hub'))
  add(('MOVE',f'X{p}','Hub'))
 prelude=len(ops);start=w['cohort']['prelude_end'];end=w['cohort']['decode_begin'];old_to_new={};cells=[]
 for k in range(start,end):
  o=w['operations'][k];add(o)
  if o[0]=='MOVE'and o[1]in{'P3','P4','P5'}:
   idx=int(o[1][1:])-3;p=primaries[idx]
   if o[2]==f'F{p}':
    pos=len(ops);add(('ADD',o[1],f'Y{p}'),('ADD',f'Y{p}',o[1]));cells.append({'packet':o[1],'primary':p,'before_operation':pos,'after_operation':len(ops)})
  old_to_new[k]=len(ops)
 assert len(cells)==3;decode_begin=len(ops)
 for field in w['cohort']['fields']:add(('MOVE',field,common))
 for field,others in zip(w['cohort']['fields'],remaining):
  for idx,i in enumerate(others):
   add(('MOVE',f'Y{i}',common),('ADD',field,f'Y{i}'))
   for k in(1,2):
    j=others[(idx-k)%3];add(('MOVE',f'Y{i}',f'D4_FB_FLAG_{j}_{k}'),('ADD',f'D4_FB_RAW_{j}_{k}',f'Y{i}'))
   add(('MOVE',f'Y{i}',f'F{i}'))
 interface=len(ops)
 for o in w['operations'][w['cohort']['continuation_before_operation']:]:
  if o[0]=='CLEAR'and o[1].startswith('D4_RAW_'):continue
  add(o)
 add(*[('CLEAR',n)for n in caches]);nw=copy.deepcopy(w)
 nw.update(charts=charts,operations=ops,schema='changing-history-D4-primary-feedback-v1',base_word_sha256=hashlib.sha256(raw).hexdigest(),carrier_interface_before_operation=interface,cohort_feedback={'frames':frames,'primaries':primaries,'remaining_frames':remaining,'precoat_operations':precoats,'feedback_cells':cells,'prelude_end':prelude,'decode_begin':decode_begin,'continuation_before_operation':interface},scope='Same52 native receivers with actual original-Y feedback. Three primaries finish at their facets before packet values change to dirty shared fields for9 later receivers. Early actual Y precoats cancel every unknown y. No all111 completion or new kappa.')
 nw['cohort']['prelude_end']=prelude;nw['cohort']['decode_begin']=decode_begin;nw['cohort']['continuation_before_operation']=interface
 CC,_,after=e.replay(nw,R);tr=b.trace(ops)
 for cell,frame,p,others in zip(cells,frames,primaries,remaining):
  vv,aa=tr[cell['before_operation']];assert vv[cell['packet']]==sum(1<<i for i in frame);assert vv[f'Y{p}']==(1<<(111+p))^sum(1<<i for i in others)
  vv,aa=tr[cell['after_operation']];assert vv[cell['packet']]==(1<<(111+p))^sum(1<<i for i in others);assert vv[f'Y{p}']==(1<<(111+p))^(1<<p)
 v,at=tr[interface]
 for field,p,others in zip(w['cohort']['fields'],primaries,remaining):assert v[field]==(1<<(111+p))^sum(1<<i for i in others)and at[field]==common
 born={o[1]for o in ops if o[0]=='INIT'};live=[n for n in born if n in v];xmask=(1<<111)-1;owner_support=sorted({i for n in live for i in range(111)if v[n]>>i&1});full_support=sorted(set(owner_support)|{i for j in range(111)for i in range(111)if v[f'Y{j}']>>i&1})
 active=set();checks=0
 for k in range(start,end):
  o=w['operations'][k]
  if o[0]=='MOVE'and o[1]in{'P3','P4','P5'}and o[2]in{f'F{p}'for p in primaries}:active.add(o[1])
  if o[0]=='ADD'and o[1]in w['cohort']['fields']and o[2]in active:active.remove(o[2])
  ov,oa=old_trace[k+1];nv,na=tr[old_to_new[k]]
  for n,z in ov.items():
   if n in active or n in w['cohort']['fields']or n.startswith('D4_RAW_'):continue
   if n.startswith('Y')and int(n[1:])in w['cohort']['targets']:continue
   if n not in nv:continue
   assert nv[n]==z and CC[na[n]]==C[oa[n]],(k,n);checks+=1
 a.out.mkdir(parents=True,exist_ok=True);sha=write(a.out/'WORD.json',nw)
 result={'status':'PASS_D4_CHANGING_HISTORY_THREE_PRIMARY_CELLS','word_sha256':sha,'base_word_sha256':hashlib.sha256(raw).hexdigest(),'before':before,'after':after,'feedback':nw['cohort_feedback'],'all_targets':nw['targets'],'new_targets':[],'continuation_index':interface,'retained_native_carriers':nw['released_carriers'],'all_live_owner_X_support':owner_support,'all_live_owner_X_support_count':len(owner_support),'owner_X_rank':len(e.bb(v[n]&xmask for n in live)),'owner_Y_rank':len(e.bb(v[n]>>111 for n in live)),'full_owned_222_column_rank':len(e.bb(v[n]for n in live)),'full_cut_nonidentity_X_support':full_support,'full_cut_nonidentity_X_support_count':len(full_support),'core_covariance_comparisons':checks,'scope':nw['scope']};write(a.out/'RESULT.json',result)
 print(json.dumps({k:result[k]for k in['status','word_sha256','after','owner_X_rank','owner_Y_rank','full_cut_nonidentity_X_support_count']}))
if __name__=='__main__':main()
