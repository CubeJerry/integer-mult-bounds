"""Use two already-paid proper descents for actual local pair codes."""
import argparse,copy,hashlib,importlib.util,json,math
from pathlib import Path
PIN='dba6b8219052642d2f4940714ea2f9bda1271b8216df263126e79afed914a4c1'
MODE_PIN='28f6825bf0c35f0e76d856c269b1602caa91aefa9bb8b6db2b64f7d6659ec3dc'
PLAN=[['P1','J23','L11','KEEP_M23',38,54],['P2','J22','L12','KEEP_M22',39,53]]
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def ints(rows):
 out=[]
 for row in rows:
  d=math.lcm(*(int(x.q)if hasattr(x,'q')else 1 for x in row));out.append([int(d*x)for x in row])
 return out
def write(p,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));a=ap.parse_args();raw=a.word.read_bytes();source_pin=hashlib.sha256(raw).hexdigest();assert source_pin in{PIN,MODE_PIN};w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','localpair_engine');tr=load(Path(__file__).with_name('build_d4_cohort.py'),'localpair_trace');pr=load(Path(__file__).with_name('price_d4_cohort.py'),'localpair_price');C,_,before=e.replay(w,R);bt=tr.trace(w['operations']);oldcut=w['carrier_interface_before_operation'];charts=copy.deepcopy(w['charts']);D={i for row in PLAN for i in row[-2:]};names={f'X{i}'for i in D};ys={f'Y{i}'for i in D};assert not any(o[0]=='ADD'and o[2]in names for o in w['operations']);assert not any(o[0]=='ADD'and o[1]in ys for o in w['operations']);ops=[];owners=[]
 def add(*rows):ops.extend([list(o)for o in rows])
 for j,(p,top,port,field,aa,bb)in enumerate(PLAN):
  assert sum(x*y for x,y in zip(R[aa],R[bb]))==0
  for i in[aa,bb]:
   assert e.sub(C[f'L{i}'],C[top])and e.sub(C[port],C[f'F{i}']);fl=f'LOCAL_PAIR_FLAG_{i}';charts[fl]={'kind':'span','rows':ints(C[port])+[R[i]]};assert len(e.chart(charts[fl]))==2 and e.sub(e.chart(charts[fl]),C[top]);ra=f'LOCAL_PAIR_RAW_{i}';so=f'LOCAL_PAIR_SOURCE_{i}';owners.extend([ra,so]);add(('MOVE',f'X{i}',fl),('INIT',ra,fl),('ADD',f'X{i}',ra),('MOVE',f'X{i}',top),('INIT',so,top),('ADD',f'X{i}',so),('MOVE',f'X{i}','Hub'))
 prelude=len(ops);mapping={};newcut=None;programs=[]
 for k,o in enumerate(w['operations']):
  if k==oldcut:
   for p,top,port,field,aa,bb in PLAN:
    for i,foreign in[(aa,bb),(bb,aa)]:add(('MOVE',f'Y{i}',port),('ADD',field,f'Y{i}'),('MOVE',f'Y{i}',f'LOCAL_PAIR_FLAG_{foreign}'),('ADD',f'LOCAL_PAIR_RAW_{foreign}',f'Y{i}'),('MOVE',f'Y{i}',f'F{i}'))
   newcut=len(ops)
  typ,n,*q=o
  if(typ=='MOVE'and n in names)or(typ=='ADD'and n in names)or n in ys or(typ=='ADD'and q[0]in ys):mapping[k]=len(ops);continue
  for p,top,port,field,aa,bb in PLAN:
   if o==['MOVE',p,port]:
    assert bt[k][0][p]==1<<aa and C[bt[k][1][p]]==C[top];programs.append({'packet':p,'old_index':k,'new_index':len(ops),'pair':[aa,bb]});add(('ADD',f'LOCAL_PAIR_SOURCE_{aa}',p),('ADD',f'LOCAL_PAIR_SOURCE_{bb}',p))
  add(o);mapping[k]=len(ops)
 assert newcut is not None and len(programs)==2;add(*[('CLEAR',n)for n in owners]);nw=copy.deepcopy(w);nw.update(schema='three-stage-history-with-local-pair59-v1',base_word_sha256=PIN,charts=charts,operations=ops,targets=sorted(set(w['targets'])|D),released_carriers=sorted(set(w['released_carriers'])-D),carrier_interface_before_operation=newcut,local_pair_extension={'plan':PLAN,'prelude_end':prelude,'programs':programs,'continuation_before_operation':newcut},scope='Adds53 and54 using two actual pair codes gathered at J22/J23 and carried through existing P2/P1 descents to L12/L11. No added owned movement. Every raw cache is actual and two paired decoder routes are explicit. Earlier two-stage lower source preserved modulo four released immutable coordinates; all111-column native end conditions. No all111 completion or kappa.')
 def boundary(k):return prelude if k==0 else mapping[k-1]
 if 'lower_history'in w:
  for key in ['prelude_end','decode_start']:nw['lower_history'][key]=boundary(w['lower_history'][key])
  for cell in nw['lower_history']['feedback_cells']:
   for key in ['before_operation','after_operation']:cell[key]=boundary(cell[key])
  nw['lower_history']['new_unit_descent_operations']=[boundary(k)for k in w['lower_history']['new_unit_descent_operations']]
  nw['lower_history']['continuation_before_operation']=newcut
 else:
  nw['schema']='five-mode-preserving-D4-and-local-pair50-v1';nw['base_word_sha256']=source_pin;nw['scope']='Actual receivers90,92,53,54 added to early46 while retaining all five nonlocal clique directions. D4 P4 and P1/P2 local pair delivery use chronological native caches; only one additional owned unit descent in the combined construction. No all111 supplier or kappa.'
  for key in['prelude_end','decode_start']:nw['mode_preserving_d4'][key]=boundary(w['mode_preserving_d4'][key])
  for key in['before_operation','after_operation']:nw['mode_preserving_d4']['feedback_cell'][key]=boundary(w['mode_preserving_d4']['feedback_cell'][key])
  nw['mode_preserving_d4']['continuation_before_operation']=newcut
  for key in['source_add_indices','correction_add_indices']:nw['shared_proper_masks'][key]=[boundary(k)for k in w['shared_proper_masks'][key]]
  nw['shared_proper_masks']['prelude_end']=boundary(w['shared_proper_masks']['prelude_end']);nw['shared_proper_masks']['continuation_before_operation']=newcut
 CC,_,after=e.replay(nw,R);nt=tr.trace(ops);v,at=nt[newcut];mask=sum(1<<i for i in D);fields={row[3]for row in PLAN};packets={row[0]for row in PLAN};comp=0
 for p,top,port,field,aa,bb in PLAN:assert v[field]==(1<<aa)^(1<<bb)and at[field]==port
 for k in range(oldcut):
  ov,oa=bt[k+1];vv,aa=nt[mapping[k]]
  for n,z in ov.items():
   if n in names|ys|fields|packets:continue
   assert n in vv and vv[n]==z&~mask,(k,n,hex(vv.get(n,0)),hex(z&~mask));assert CC[aa[n]]==C[oa[n]];comp+=1
 for i in range(111):
  assert v[f'X{i}']==1<<i
  if i not in nw['targets']:assert v[f'Y{i}']==1<<(111+i)and at[f'Y{i}']=='zero'
 original={f'{s}{i}'for s in['X','Y']for i in range(111)};owned={n:z for n,z in v.items()if n not in original};assert all(z>>111==0 for z in owned.values());support=0
 for z in owned.values():support|=z
 for i in range(111):support|=v[f'Y{i}']^(1<<(111+i))
 S=[i for i in range(111)if support>>i&1];gate={127:37,64:74,1:-74}
 if source_pin==MODE_PIN:
  J=[5,35,93,96,97,109,110];jm=sum(1<<i for i in J);rows=[]
  for n,z in owned.items():
   lm=sum(1<<i for i in J if e.sub(CC[f'L{i}'],CC[at[n]]));rows.append(z&jm&~lm)
  assert len(e.bb(rows))==5
  for _,f,_,_,_ in w['shared_proper_masks']['plan']:assert v[f]&jm==bt[oldcut][0][f]&jm
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 lim=tuple(x/6 for x in pr.moment(gate));q=pr.moment(after['movement_profile']);qo=pr.moment(before['movement_profile']);a.out.mkdir(parents=True,exist_ok=True);sha=write(a.out/'WORD.json',nw);res={'status':'PASS_ACTUAL_THREE_STAGE_PAID59','word_sha256':sha,'base_word_sha256':PIN,'before':before,'after':after,'new_targets':[53,54],'all_targets':nw['targets'],'interface':newcut,'source_support':S,'source_support_count':len(S),'owned_X_rank':len(e.bb(owned.values())),'owned_Y_rank':0,'projected_comparisons':comp,'whole_moment':pr.record(q),'moment_increment':pr.record((q[0]-qo[1],q[1]-qo[0])),'necessary_limiting_room':pr.record((lim[0]-q[1],lim[1]-q[0])),'scope':nw['scope']}
 if source_pin==MODE_PIN:res.update(status='PASS_ACTUAL_FIVE_MODE_PRESERVING50',base_word_sha256=source_pin,clique=J,clique_nonlocal_projection_rank=5)
 write(a.out/'RESULT.json',res);print(json.dumps({k:res[k]for k in['status','word_sha256','after','source_support_count','whole_moment','necessary_limiting_room']}))
if __name__=='__main__':main()
