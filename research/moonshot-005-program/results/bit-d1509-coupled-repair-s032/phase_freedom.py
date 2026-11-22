"""Phase-legal D1509 changes preserving actual four-receiver ingress readouts."""
from pathlib import Path
import importlib.util,gzip,json,numpy as np
repo=Path.cwd();base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032';here=Path(__file__).parent
s=importlib.util.spec_from_file_location('s032_solve',four/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);g,a,ff,Ks,C=m.common_data(repo)
src=m.ex.read(four/'output/SOURCES.json.gz');ph=m.ex.read(four/'output/H-PHYSICAL.json.gz');dw=m.ex.read(four/'output/D-WORD.json.gz');gg=m.ex.read(four/'output/CONSTRAINED-GAUGES.json.gz');w=json.loads((base/'bit-fifth-receiver-quotient-s032/WITNESS.json').read_text());L=np.array(gg['common_frames'],dtype=np.uint8);R=gg['receivers'];v=np.array(w['vector'],dtype=np.uint8);prot=list(range(48))+list(range(240,288));T=np.array(dw['matrix'],dtype=np.uint8);owners=dw['owners'];di={tuple(x[:3]):q for q,x in enumerate(owners)}
outputs={i:[q for q,x in enumerate(owners)if x[5]is not None and i in a.planes[x[5]]]for i in R+[95]}
P={}
for js,mm in src['paired_maps'].items():
 j=int(js);ingress=np.zeros((35,96),dtype=np.uint8)
 for hs,F0 in mm.items():
  h=int(hs)
  if not a.planes[h]<=a.charts[1509]:continue
  F=np.array(F0,dtype=np.uint8)[:,prot];Q=np.array(src['frames'][f'{j}/{h}'],dtype=np.uint8);z=ph[hs];xs=z['X_owners'];ys=z['Y_owners'];xx=[q for q,x in enumerate(xs)if x[1]==j];yy=[q for q,x in enumerate(ys)if x[6]==j];state=a.mm(Q,F);XE=np.zeros((len(xs),96),dtype=np.uint8);YL=np.zeros((len(ys),96),dtype=np.uint8);XE[xx]=state[:len(xx)];YL[yy]=state[len(xx):];E=np.array(z['early'],dtype=np.uint8);B=np.array(z['late'],dtype=np.uint8).reshape(len(ys),len(ys));G=np.array(z['cross'],dtype=np.uint8).reshape(len(ys),len(xs));RX=a.mm(E,XE);RY=a.mm(G,XE)^a.mm(B,YL)
  for rr,values in [(xs,RX),(ys,RY)]:
   for x,row in zip(rr,values):
    if x[4]==1509:ingress[di[tuple(x[:3])]]=row
 P[j]=ingress
 for r in R:
  need=a.mm(T[outputs[r]],a.mm(ingress,L[:,8*R.index(r):8*R.index(r)+8]));assert np.array_equal(need,np.eye(8,dtype=np.uint8))
print('INGRESS_RANKS',[(j,a.rank(A))for j,A in P.items()],flush=True)
M={(j,r):a.mm(A,L[:,8*R.index(r):8*R.index(r)+8])for j,A in P.items()for r in R}
Z=a.mm(P[0]^P[61],v[:,None]);d=a.mm(T[outputs[95]],Z)[:,0]
rows=[];delta=np.zeros((35,35),dtype=np.uint8);free_total=0;unrepairable=[]
for q in range(35):
 allowed=list(range(19 if q<19 else 35));seen=[r for r in R if q in outputs[r]];B=np.hstack([M[j,r][allowed]for r in seen for j in sorted(P)])if seen else np.zeros((len(allowed),0),dtype=np.uint8);ann=m.null(B.T,g,a).T;free_total+=len(ann);effect=a.mm(ann,Z[allowed])[:,0];desired=int(d[outputs[95].index(q)])if q in outputs[95]else None;rec={'row':q,'owner':owners[q],'allowed_columns':len(allowed),'retained_receivers':seen,'constraint_rank':a.rank(B),'homogeneous_freedom':len(ann),'receiver95_effect_rank':int(np.any(effect))if q in outputs[95]else None,'desired_change':desired}
 if desired:
  if not np.any(effect):unrepairable.append(q)
  else:
   p=int(np.flatnonzero(effect)[0]);delta[q,allowed]=a.product[a.product[desired,a.inverse[effect[p]]],ann[p]]
 rows.append(rec)
print('TOTAL_FREEDOM',free_total,'DISCREPANCY',d.tolist(),'UNREPAIRABLE',unrepairable,flush=True)
print('TARGET_ROWS',[(z['row'],z['retained_receivers'],z['homogeneous_freedom'],z['receiver95_effect_rank'],z['desired_change'])for z in rows if z['row']in outputs[95]],flush=True)
result={'status':'EXACT_PHASE_FREEDOM_SCREEN','retained_receivers':R,'target_receiver':95,'outputs':outputs,'D_phase_dimensions':[19,16],'total_homogeneous_matrix_freedom':free_total,'fixed_ingress_discrepancy':d.tolist(),'unrepairable_target_rows':unrepairable,'row_data':rows,'delta_repairs_all_discrepancy':not unrepairable,'complete_coupled_source_D_repair':False}
here.mkdir(exist_ok=True);(here/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');payload={'ingress':{j:A.tolist()for j,A in P.items()},'common_frames':L.tolist(),'source_difference':Z.tolist(),'partial_delta':delta.tolist()};(here/'DATA.json.gz').write_bytes(gzip.compress((json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
