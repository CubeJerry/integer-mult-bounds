"""A real D4 decoder on P4 while retaining the five useful source directions."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
PIN='14503b00ad6f9d1e4d85ec09769a51c14eca36d61edabe19d9ae2907608c7501'
FRAME=[74,80,90,92];PRIMARY=74;OTHER=[80,90,92]
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(p,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/work-S018/A/shared-proper-five46/WORD.json'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));a=ap.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','mode_d4_engine');t=load(Path(__file__).with_name('build_d4_cohort.py'),'mode_d4_trace');pr=load(Path(__file__).with_name('price_d4_cohort.py'),'mode_d4_price');C,_,before=e.replay(w,R);bt=t.trace(w['operations']);oldcut=w['carrier_interface_before_operation'];charts=copy.deepcopy(w['charts']);common='MODE_D4_COMMON';charts[common]={'kind':'ann','rows':[R[i]for i in FRAME]};Z=e.chart(charts[common]);assert len(Z)==4 and e.sub(Z,C['M1']);names={f'X{i}'for i in FRAME};ys={f'Y{i}'for i in FRAME};assert not any(o[0]=='ADD'and o[2]in names for o in w['operations']);assert not any(o[0]=='ADD'and o[1]in ys for o in w['operations']);cap=w['operations'].index(['ADD','P4','ZFIRST4']);reset=w['operations'].index(['ADD','ZFIRST4','P4']);assert[o for o in w['operations'][:cap+1]if o[0]=='ADD'and o[1]=='P4']==[['ADD','P4','ZFIRST4']];ops=[];caches=[]
 def add(*rows):ops.extend([list(o)for o in rows])
 add(('MOVE','Y74','M1'),('INIT','MODE_INITIAL_Y74','M1'),('ADD','Y74','MODE_INITIAL_Y74'),('MOVE','Y74','F74'))
 for start,i in enumerate(OTHER):
  for size in[1,2]:
   inter=[OTHER[(start+h)%3]for h in range(size)];lab=f'MODE_D4_FLAG_{i}_{size}';charts[lab]={'kind':'ann','rows':[R[k]for k in FRAME if k not in inter]};assert len(e.chart(charts[lab]))==4+size;cache=f'MODE_D4_RAW_{i}_{size}';caches.append(cache);add(('MOVE',f'X{i}',lab),('INIT',cache,lab),('ADD',f'X{i}',cache))
  add(('MOVE',f'X{i}','F74'),('ADD',f'X{i}','Y74'),('MOVE',f'X{i}','Hub'))
 add(('MOVE','X74','Hub'));prelude=len(ops);mapping={};kept={};cell=None;cut=None;decode=None
 for k,o in enumerate(w['operations']):
  if k==oldcut:
   decode=len(ops);add(('MOVE','ZFIRST4',common))
   for idx,i in enumerate(OTHER):
    add(('MOVE',f'Y{i}',common),('ADD','ZFIRST4',f'Y{i}'))
    for size in[1,2]:
     foreign=OTHER[(idx-size)%3];add(('MOVE',f'Y{i}',f'MODE_D4_FLAG_{foreign}_{size}'),('ADD',f'MODE_D4_RAW_{foreign}_{size}',f'Y{i}'))
    add(('MOVE',f'Y{i}',f'F{i}'))
   cut=len(ops)
  typ,n,*q=o
  if(typ=='MOVE'and n in names)or(typ=='ADD'and n in names)or n in ys or(typ=='ADD'and q[0]in ys)or(typ=='ADD'and q[0]=='P4'and k<cap):mapping[k]=len(ops);continue
  if typ=='MOVE'and n=='P4'and bt[k][1]['P4']=='Hub':
   for i in FRAME:add(('ADD',f'X{i}','P4'))
  if o==['ADD','P4','ZFIRST4']:add(('ADD','MODE_INITIAL_Y74','P4'))
  kept[k]=len(ops);add(o)
  if o==['MOVE','P4','F74']:
   pos=len(ops);add(('ADD','P4','Y74'),('ADD','Y74','P4'));cell={'before_operation':pos,'after_operation':len(ops)}
  if o==['ADD','ZFIRST4','P4']:add(('CLEAR','MODE_INITIAL_Y74'))
  mapping[k]=len(ops)
 assert cut is not None and cell is not None;add(*[('CLEAR',n)for n in caches]);nw=copy.deepcopy(w);nw.update(schema='mode-preserving-one-D4-primary48-v1',base_word_sha256=PIN,charts=charts,operations=ops,targets=sorted(set(w['targets'])|set(FRAME)),carrier_interface_before_operation=cut,mode_preserving_d4={'frame':FRAME,'primary':PRIMARY,'other':OTHER,'common':common,'field':'ZFIRST4','prelude_end':prelude,'decode_start':decode,'feedback_cell':cell,'continuation_before_operation':cut},scope='Actual new receivers90 and92 while retaining all five tested nonlocal unknown directions. Only the old P4 first segment is reprogrammed; proper correction groups on P0/P1/P2/P3/P5 remain actual. One unit retained-field descent and chronological cyclic caches, all cut owners pureX. No all111 supplier or kappa.')
 sm=nw['shared_proper_masks'];sm['source_add_indices']=[kept[k]for k in sm['source_add_indices']if k in kept];sm['correction_add_indices']=[kept[k]for k in sm['correction_add_indices']if k in kept];sm['prelude_end']=mapping[w['shared_proper_masks']['prelude_end']-1];sm['continuation_before_operation']=cut
 CC,_,after=e.replay(nw,R);nt=t.trace(ops);v,at=nt[cut];mask=sum(1<<i for i in FRAME);comp=0
 assert v['ZFIRST4']==sum(1<<i for i in OTHER)and at['ZFIRST4']==common
 for k,o in enumerate(w['operations']):
  if k>=oldcut:break
  ov,oa=bt[k+1];vv,aa=nt[mapping[k]]
  for n,z in ov.items():
   if n in names|ys or n=='ZFIRST4'or(n=='P4'and k<=reset):continue
   assert n in vv and vv[n]==z&~mask,(k,o,n);assert CC[aa[n]]==C[oa[n]],(k,n,'chart');comp+=1
 J=[5,35,93,96,97,109,110];jm=sum(1<<i for i in J);born={o[1]for o in ops if o[0]=='INIT'};owned={n:z for n,z in v.items()if n in born};assert all(z>>111==0 for z in owned.values());rows=[];certificate=[]
 for n,z in owned.items():
  loc=sum(1<<i for i in J if e.sub(CC[f'L{i}'],CC[at[n]]));r=z&jm&~loc
  if r:rows.append(r);certificate.append({'owner':n,'chart':at[n],'row_hex':hex(r)})
 assert len(e.bb(rows))==5
 for p,f,i,loc,readers in w['shared_proper_masks']['plan']:assert v[f]&jm==bt[oldcut][0][f]&jm
 for i in range(111):
  assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
  if i not in nw['targets']:assert v[f'Y{i}']==1<<(111+i)and at[f'Y{i}']=='zero'
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 lim=tuple(x/6 for x in pr.moment(gate));q=pr.moment(after['movement_profile']);qo=pr.moment(before['movement_profile']);a.out.mkdir(parents=True,exist_ok=True);sha=write(a.out/'WORD.json',nw);res={'status':'PASS_REAL_NEW_RECEIVERS_WITH_FIVE_MODES_RETAINED','word_sha256':sha,'base_word_sha256':PIN,'before':before,'after':after,'new_targets':[90,92],'all_targets':nw['targets'],'interface':cut,'clique':J,'clique_nonlocal_projection_rank':5,'clique_certificate':certificate,'unaffected_projected_comparisons':comp,'whole_moment':pr.record(q),'moment_increment':pr.record((q[0]-qo[1],q[1]-qo[0])),'necessary_limiting_room':pr.record((lim[0]-q[1],lim[1]-q[0])),'scope':nw['scope']};write(a.out/'RESULT.json',res);print(json.dumps({k:res[k]for k in['status','word_sha256','after','new_targets','whole_moment','necessary_limiting_room']}))
if __name__=='__main__':main()
