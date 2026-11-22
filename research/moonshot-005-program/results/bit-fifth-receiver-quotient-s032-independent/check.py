#!/usr/bin/env python3
"""Independent literal-observation audit of the receiver95 source-quotient gate."""
import argparse,gzip,hashlib,json,runpy
from collections import defaultdict
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;BASE=HERE.parent;ROOT=BASE.parents[2]
PREV=BASE/'bit-simultaneous-d1509-s032-independent'
H=runpy.run_path(str(PREV/'check_frames.py'))
mm,rank,inverse,basis,rd,wr,need=[H[k] for k in ['mm','rank','inverse','basis','rd','wr','need']]
null,echelon=H['ALG']['null'],H['ALG']['echelon']
def decomposition(B,v):
 cols=echelon(B)[1];J=B[:,cols];K=null(np.hstack([J,v]))
 need(K.shape==(len(cols)+1,1) and K[-1,0]==1,'span membership certificate')
 need(np.array_equal(mm(J,K[:-1]),v),'exact local observation combination')
 return {'generator_columns':cols,'coefficients':K[:-1,0].tolist(),'rank':len(cols)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=HERE/'output');args=ap.parse_args()
 for file,digest in rd(HERE/'SOURCE-PINS.json')['files'].items():need(hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,'frozen source binding '+file)
 p=BASE/'bit-fifth-receiver-quotient-s032';candidate=BASE/'bit-simultaneous-d1509-s032/output'
 w=rd(p/'WITNESS.json');source=rd(candidate/'SOURCES.json.gz');hp=rd(candidate/'H-PHYSICAL.json.gz');dw=rd(candidate/'D-WORD.json.gz');gauge=rd(candidate/'CONSTRAINED-GAUGES.json.gz')
 layout=rd(BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');roots=np.array(layout['root_table']);adj=[set(np.flatnonzero(row==0).tolist()) for row in roots@roots.T];planes=[set(z) for z in layout['A2']];charts=[set(z) for z in layout['D4']]
 routes=[json.loads(z)for z in gzip.decompress((BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()]
 X,Y,Xj,Yj=[defaultdict(list) for _ in range(4)]
 for r in routes:
  if r[3] is None:continue
  (X if r[0]=='X' else Y)[r[3]].append(r)
  if r[0]=='X':Xj[r[1],r[3]].append(r)
  elif r[6] is not None:Yj[r[6],r[3]].append(r)
 for table in [X,Y,Xj,Yj]:
  for key in table:table[key].sort(key=lambda r:(r[1],r[2]))
 oldframes=rd(PREV/'output/FRAMES.json.gz');hf=rd(PREV/'output/H-FIBRES.json.gz')
 L=np.array(gauge['common_frames'],dtype=np.uint8);retained=gauge['receivers'];v=np.array(w['vector'],dtype=np.uint8).reshape(96,1)
 coeff=np.zeros((32,1),dtype=np.uint8)
 for t,x in w['four_frame_coefficients']:coeff[t,0]=x
 need(np.array_equal(mm(L,coeff),v) and rank(v)==1,'literal witness in retained four-frame span')
 G61=np.array(gauge['gauges']['61'],dtype=np.uint8);U=mm(inverse(G61),np.array(oldframes['61']['95'],dtype=np.uint8));intersection=mm(U,null(np.hstack([L,U]))[32:]);I=basis(intersection)
 need(I.shape==(96,4) and rank(np.hstack([I,v]))==4,'four-dimensional forced collision')
 view=[h for h,P in enumerate(planes) if 61 in P and P<=adj[95]];need(len(view)==16 and sorted(z['H'] for z in w['quotient_decompositions'])==view,'all actual receiver95 source quotients')
 local=[]
 for h in view:
  gen=[];labels=[]
  for key,F in sorted(hf['61'].items()):
   centre,rcv=map(int,key.split('/'))
   if rcv<111 and planes[h]<=adj[rcv]:
    A=np.array(F,dtype=np.uint8);gen.append(A);labels.extend([['H',centre,rcv,b]for b in range(6)])
  for t,rcv in enumerate(retained):
   if planes[h]<=adj[rcv]:gen.append(L[:,8*t:8*t+8]);labels.extend([['D',rcv,b]for b in range(8)])
  B=np.hstack(gen);need(rank(np.hstack([B,I]))==rank(B),'entire collision fixed by local necessary observations')
  cert=decomposition(B,v);local.append({'H':h,'generator_labels':labels,**cert})
  if h==333:
   row=np.zeros((1,96),dtype=np.uint8);pos=int(np.flatnonzero(v[:,0])[0]);row[0,pos]=H['ALG']['INV'][v[pos,0]]
   need(mm(row,v)[0,0]==1,'one-row edit changes the collision')
   values=mm(row,B)[0];hit=int(np.flatnonzero(values)[0]);need(labels[hit][0]=='H','invisible-to-four edit breaks native H observation')
   control={'H':333,'source_coordinate_in_protected96':pos,'coefficient':int(row[0,pos]),'changed_collision_value':1,'violated_native_H_generator':labels[hit],'generator_change':int(values[hit]),'not_a_valid_retained_interface_edit':True}
 prot=list(range(48))+list(range(240,288));owners=dw['owners'];D=np.array(dw['matrix'],dtype=np.uint8);owneridx={(r[0],r[1],r[2]):t for t,r in enumerate(owners)};outs=[t for t,r in enumerate(owners)if r[5]is not None and 95 in planes[r[5]]]
 need(len(outs)==8,'actual receiver95 output owners')
 responses={};nonproper={}
 for j in [0,61]:
  ingress=np.zeros((35,96),dtype=np.uint8);other=[]
  for hs,f0 in source['paired_maps'][str(j)].items():
   h=int(hs)
   if not planes[h]<=adj[95]:continue
   F=np.array(f0,dtype=np.uint8)[:,prot];Q=np.array(source['frames'][f'{j}/{h}'],dtype=np.uint8);ne,nl=len(X[h]),len(Y[h]);E=np.array(hp[hs]['early'],dtype=np.uint8).reshape(ne,ne);B=np.array(hp[hs]['late'],dtype=np.uint8).reshape(nl,nl);cross=np.array(hp[hs]['cross'],dtype=np.uint8).reshape(nl,ne)
   early=np.zeros((ne,30),dtype=np.uint8);late=np.zeros((nl,30),dtype=np.uint8);xi={(r[1],r[2]):t for t,r in enumerate(X[h])};yi={(r[1],r[2]):t for t,r in enumerate(Y[h])}
   for t,r in enumerate(Xj[j,h]):early[xi[r[1],r[2]]]=Q[t]
   for t,r in enumerate(Yj[j,h]):late[yi[r[1],r[2]]]=Q[len(Xj[j,h])+t]
   EX=mm(mm(E,early),F);LY=mm(mm(cross,early)^mm(B,late),F)
   for phase,seq,values in [('X',X[h],EX),('Y',Y[h],LY)]:
    for t,r in enumerate(seq):
     if r[4]==1509:ingress[owneridx[phase,r[1],r[2]]]=values[t]
     elif charts[r[4]]<=adj[95]:other.append(values[t])
  responses[j]=mm(D[outs],ingress);O=np.array(other,dtype=np.uint8);nonproper[j]=rank(mm(O,I))
  if j==61:need(not np.any(mm(O,I)),'entire collision remains isolated at donor61')
 read61=mm(responses[61],v)[:,0];read0=mm(responses[0],v)[:,0]
 need(read61.tolist()==w['actual_readout_donor61'] and read0.tolist()==w['actual_readout_donor0'] and (read61^read0).tolist()==w['difference'] and np.any(read61^read0),'actual conflicting D readouts')
 parentHs=[h for h,P in enumerate(planes) if 0 in P and P<=charts[1509]]
 need(len(parentHs)==4 and all(all(planes[h]<=adj[r] for r in retained)for h in parentHs),'every donor0 D-parent quotient constrained by all retained receivers')
 diff_rank=rank(mm(responses[0]^responses[61],I));need(diff_rank==2,'independent readout conflict rank')
 need(not np.array_equal(read0,read61),'zero conflict would fail')
 result={'status':'PASS_INDEPENDENT_RECEIVER95_QUOTIENT_OBSTRUCTION','forced_donor':61,'contradicting_donor':0,'receiver':95,'retained_receivers':retained,'forced_collision_dimension':4,'all_forced_source_quotients':view,'local_constraint_ranks':[z['rank']for z in local],'donor0_D_parent_H':parentHs,'readout_donor61':read61.tolist(),'readout_donor0':read0.tolist(),'difference':(read61^read0).tolist(),'collision_readout_difference_rank':diff_rank,'other_proper_packet_rank_on_collision':nonproper,'new_author_executable_imports':False,'scope':'independent linear source-quotient edits preserving literal retainedH/fourD observation values with unchanged H/D physical maps and local owner interfaces','complete_supplier':False,'new_kappa':False}
 result['only_native_H_observations_used']=True;result['released_H_constraint_control']=control
 wr(args.out/'RESULT.json',result);wr(args.out/'LOCAL-DECOMPOSITIONS.json.gz',local);print(result,flush=True)
if __name__=='__main__':main()

