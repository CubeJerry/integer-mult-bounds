"""Actual pair captures and four paid rank2-to-rank5 arrivals."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json
from build_quartet_compression_source import SOURCE,SHA,CHECK,HELPER,module
from build_four_plane_correction import replay_general
from review_owned_upward_rebase import paid_replay
PARENT_SHA='6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980'
A=[14,17,19,20];B=[96,101,99,102]

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,default=Path(__file__).resolve().parent/'full-half-reservoir/WORD.json');p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots']
 pb=a.parent.read_bytes();assert hashlib.sha256(pb).hexdigest()==PARENT_SHA;w=json.loads(pb)
 geo=module(a.repo/CHECK,'frame_repair_geometry');h=module(a.repo/HELPER,'frame_repair_intervals')
 C,pv,pp,ps=replay_general(w,R,geo)
 oldops=w['operations'];oldcut=w['carrier_interface_before_operation'];oldkeys={j:k for k,ii in w['semantic_operation_indices'].items() for j in ii}
 ops=[];sem={};values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
 places={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)}
 def chart(n,roles):
  w['charts'][n]={'kind':'span','rows':[R[i] for i in sorted(set(roles))]};C[n]=geo.chart(w['charts'][n]);return n
 def emit(op,key):
  sem.setdefault(key,[]).append(len(ops));ops.append(op);kind,n,*q=op
  if kind=='INIT':assert n not in values;values[n]=0;places[n]=q[0]
  elif kind=='ADD':assert C[places[n]]==C[places[q[0]]],(op,places[n],places[q[0]]);values[q[0]]^=values[n]
  elif kind=='MOVE':places[n]=q[0]
  elif kind=='CLEAR':del values[n],places[n]
 pairs=[[B[0],B[2]],[B[1],B[3]]];targets=[[1,3],[0,2]];paircharts=[chart(f'FRAME_PAIR_P{k}',v) for k,v in enumerate(pairs)]
 owners={j:f'FRAME_PAIR_TO_B{j}' for j in range(4)};done=set()
 for ix,op in enumerate(oldops[:oldcut]):
  if oldkeys[ix]=='direct_half_native_gather':
   for k,(u,v) in enumerate(pairs):
    if k not in done and op[1] in [f'X{u}',f'X{v}']:
     assert places[f'X{u}']==f'L{u}' and places[f'X{v}']==f'L{v}'
     for i in [u,v]:emit(['MOVE',f'X{i}',paircharts[k]],'pair_source_arrival')
     emit(['ADD',f'X{u}',f'X{v}'],'pair_source_encode')
     for j in targets[k]:
      emit(['INIT',owners[j],paircharts[k]],'pair_owner_birth');emit(['ADD',f'X{v}',owners[j]],'pair_actual_capture')
     emit(['ADD',f'X{u}',f'X{v}'],'pair_source_inverse');done.add(k)
  emit(op,oldkeys[ix])
 assert done=={0,1};augmented=len(ops)
 forward=[(B[(i+1)%4],A[i]) for i in range(4)]+[(A[i],B[(i+2)%4]) for i in range(4)]+[(B[(i+3)%4],A[i]) for i in range(4)]
 for src,dst in reversed(forward):emit(['ADD',f'Y{src}',f'Y{dst}'],'ground_network_inverse')
 history={}
 for i in range(4):
  for receiver,seed in [(A[i],B[i]),(B[i],A[i])]:
   emit(['MOVE',f'Y{receiver}',f'L{seed}'],'native_seed_arrival');emit(['ADD',f'NATIVE_{seed}',f'Y{receiver}'],'native_seed_read');history[receiver]={seed}
 for roundno,offset in [(1,1),(2,2),(3,3)]:
  if roundno==3:
   for j in range(4):
    history[B[j]]|={B[(j-1)%4],B[(j+1)%4]}
    name=chart(f'FRAME_PAIR_E{j}',history[B[j]]);assert len(C[name])==5 and geo.sub(C[name],C[f'F{B[j]}'])
    emit(['MOVE',owners[j],name],'paid_pair_owned_ascent');emit(['MOVE',f'Y{B[j]}',name],'pair_receiver_rank5_arrival');emit(['ADD',owners[j],f'Y{B[j]}'],'actual_pair_receiver_service')
  for i in range(4):
   j=(i+offset)%4;u,v=A[i],B[j];both=history[u]|history[v]
   name=chart(f'FRAME_MEET_R{roundno}_{i}',both);assert len(C[name])=={1:2,2:4,3:6}[roundno]
   assert geo.sub(C[name],C[f'F{u}']) and geo.sub(C[name],C[f'F{v}'])
   for r in [u,v]:emit(['MOVE',f'Y{r}',name],'actual_frame_rendezvous');history[r]=both.copy()
   src,dst=(u,v) if roundno==2 else (v,u);emit(['ADD',f'Y{src}',f'Y{dst}'],'frame_forward_network')
 cut=len(ops);expected=[int(x,16) for x in w['Y_correction_rows_hex']]
 for i in range(4):
  expected[A[i]]^=sum(1<<A[k] for k in range(4) if k!=i)^(1<<B[(i+1)%4])^(1<<B[(i+2)%4])
  expected[B[i]]^=sum(1<<B[k] for k in range(4) if k!=i)^(1<<A[(i-1)%4])^(1<<A[i])
 assert all(values[f'Y{i}']==(1<<(111+i))^expected[i] for i in range(111))
 for ix,op in enumerate(oldops[oldcut:],oldcut):emit(op,oldkeys[ix])
 for j in range(4):emit(['CLEAR',owners[j]],'pair_owner_retirement')
 w.update(schema='four-paid-pair-arrival-frame-service-v1',operations=ops,semantic_operation_indices=sem,carrier_interface_before_operation=cut,Y_correction_rows_hex=list(map(hex,expected)))
 w['construction']['parent_word_sha256']=PARENT_SHA;w['construction']['four_pair_arrival_frame_service']={'A':A,'B':B,'pair_sources':pairs,'pair_recipients':targets,'augmented_source_cut':augmented,'forward_Y_ADD_pairs':forward,'owned_upward_gaps':[3]*4}
 w['scope']='Actual early pair captures and four paid owned2-to5 ascents supply eight receivers with three own-frame neighbours plus two native cross-frame terms. All eight coordinate Ys stay complete at ground;103 Ys remain ground. No new diagonal output, complete supplier or cost dominance claim.'
 C,V,P,stats=paid_replay(w,R,geo);profile=Counter(ps['movement_profile']);profile.update({1:40,2:8,3:4,7:-8})
 assert stats['movement_profile']==dict(sorted(profile.items()))
 assert stats['counts']=={'INIT':188,'ADD':1400,'MOVE':508,'CLEAR':188},stats['counts']
 assert len(V)==410 and Counter(len(C[P[f'Y{i}']]) for i in range(111))=={0:103,6:8}
 assert len(stats['owned_upward_moves'])==4 and all(x['gap']==3 for x in stats['owned_upward_moves'])
 N=[sum(1<<j for j,q in enumerate(R) if sum(x*y for x,y in zip(r,q))==0) for r in R]
 assert all(not(expected[i]&~N[i]) for i in range(8,111))
 moment=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 ceiling=tuple(x/6 for x in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
 h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)} for n,v in sorted(V.items())]})
 controls=[]
 for key in ['pair_actual_capture','pair_source_inverse','ground_network_inverse','native_seed_read','frame_forward_network','paid_pair_owned_ascent','actual_pair_receiver_service']:
  bad=json.loads(json.dumps(w));ix=sem[key][0];del bad['operations'][ix];bad['carrier_interface_before_operation']-=1
  try:paid_replay(bad,R,geo)
  except AssertionError:controls.append('omit_'+key)
  else:raise AssertionError(key)
 result={'status':'PASS_ACTUAL_FOUR_PAID_PAIR_ARRIVAL_SERVICE','word_sha256':pin,'parent_word_sha256':PARENT_SHA,'cut':cut,'all_original_columns':222,'live_fields':410,'completed_outputs':8,'new_native_foreign_coefficients':40,'total_unknown_foreign_coefficients':452,'all_arbitrary_Y_baselines_restored':True,'original_X_restored_at_Hub':True,'public_Y_rank_histogram':{0:103,6:8},'stats':stats,'movement_delta':{1:40,2:8,3:4,7:-8},'added_moment':h.record(h.moment({1:40,2:8,3:4,7:-8})),'moment':h.record(moment),'necessary_limiting_room':h.record((ceiling[0]-moment[1],ceiling[1]-moment[0])),'negative_controls':controls,'scope':w['scope']}
 h.save(a.out/'RESULT.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
