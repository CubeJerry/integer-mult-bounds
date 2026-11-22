"""Exact diagonal-pencil readout certificate; no whole fifth fibre claimed.
@CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import argparse,importlib.util,hashlib,json,gzip
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('s033_arithmetic',HERE.parents[1]/'check.py');alg=importlib.util.module_from_spec(spec);spec.loader.exec_module(alg)
mm,rank,inverse,solve,read,save,need,P,INV=[getattr(alg,x)for x in['mm','rank','inverse','solve','read','save','need','P','INV']]
BASE=Path('research/moonshot-005-program/results')
def main(repo,out):
 for p,h in read(HERE/'SOURCE-PINS.json').items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'source pin '+p)
 z=read(repo/BASE/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');dw=read(repo/BASE/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz');old=np.array(dw['matrix'],dtype=np.uint8);c=read(HERE/'PENCIL-CANDIDATE.json.gz');T=np.array(c['D_matrix'],dtype=np.uint8)
 layout=read(repo/BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(v==0))for v in roots@roots.T];planes=[set(v)for v in layout['A2']];charts=[set(v)for v in layout['D4']]
 routes=[json.loads(v)for v in gzip.decompress((repo/BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()];owners=sorted([v for v in routes if v[4]==1509 and v[0]=='X'],key=lambda v:(v[1],v[2]))+sorted([v for v in routes if v[4]==1509 and v[0]=='Y'],key=lambda v:(v[1],v[2]));need(owners==dw['owners'],'actual D owners')
 geomJ=sorted(charts[1509]);geomR=[r for r in range(120)if charts[1509]<=adj[r]];J=[j for j in geomJ if j<111];I={j:[q for q,v in enumerate(owners)if v[3]is not None and j in planes[v[3]]]for j in geomJ};O={r:[q for q,v in enumerate(owners)if v[5]is not None and r in planes[v[5]]]for r in geomR};R=z['retained_receivers'];F=[4,5,7,8]
 need(J==z['donors']and R==[6,9,48,73],'native configuration');need(all(I[j]==z['D_inputs'][str(j)]for j in J)and all(O[r]==z['D_outputs'][str(r)]for r in R),'retained incidence')
 U=sorted(set(sum([O[r]for r in R],[])));need(np.array_equal(T[np.ix_(U,F)],old[np.ix_(U,F)]),'exact affine family')
 records=read(HERE.parent/'output/CERTIFICATE.json.gz');target_record=next(v for v in records if v['target']==54);W=np.array(target_record['L_coordinates'],dtype=np.uint8);L=np.array(z['common_frames'],dtype=np.uint8);need(not np.any(W[:8])and not np.any(W[24:]),'only9/48 forcedK coefficients');E=[4,5]
 C9=solve(old[np.ix_(O[9],E)],W[8:16]);C48=solve(old[np.ix_(O[48],E)],W[16:24]);H0=C9^C48;need(rank(H0)==2,'reference K profile')
 alpha=np.array([35,35,58,58],dtype=np.uint8);Dalpha=np.diag(alpha[:2]);need(np.array_equal(mm(C9,inverse(H0)),Dalpha),'exact scalar sector')
 d=np.array(c['d'],dtype=np.uint8);need(d.shape==(35,)and not np.any(d==0)and not np.any(d==1),'nonzero pencil denominators');need(np.array_equal(d[F],P[alpha,INV[alpha^1]]),'F pencil parameters')
 M=np.array(c['M'],dtype=np.uint8);N=np.array(c['N'],dtype=np.uint8);G=T[O[9]];H=T[O[48]];Q=T[O[54]];need(rank(M)==rank(N)==8,'row changes')
 need(np.array_equal(H,P[mm(M,G),d[None,:]]),'48 diagonal scaling');need(np.array_equal(Q,P[mm(N,G),P[d,INV[d^1]][None,:]]),'actual54 weighted code')
 need(not np.any(T[:19,19:])and rank(T[:19,:19])==19 and rank(T[19:,19:])==16,'physical phases')
 sections=[]
 for j in geomJ:
  for r in geomR:
   k=rank(T[np.ix_(O[r],I[j])]);need(k==8,'geometric section');sections.append([j,r,k])
 need(len(sections)==144,'geometric census')
 BK={};ss={}
 for j in J:
  Z0=np.zeros((35,32),dtype=np.uint8)
  for r in R:ss[j,r]=inverse(T[np.ix_(O[r],I[j])])
  Z0[I[j]]=np.hstack([ss[j,r]for r in R]);BK[j]=mm(Z0,W)
  expected=mm(mm(mm(N,G[:,E]),Dalpha),H0);need(np.array_equal(mm(Q,BK[j]),expected),'actual54 common response identity')
 need(rank(expected)==2,'injective forcedK response')
 for key,v in z['systems'].items():
  j,h=map(int,key.split('/'));oldF=np.array(v['old_protected_map'],dtype=np.uint8);newF=oldF^np.array(c['source_protected_delta'][key],dtype=np.uint8);C=np.array(v['H_observation_core'],dtype=np.uint8)
  need(np.array_equal(mm(oldF,C),mm(newF,C)),'H images')
  for t,r in enumerate(R):need(np.array_equal(mm(newF,L[:,8*t:8*t+8]),mm(np.array(v['receiver_ingress_to_quotient_maps'][t],dtype=np.uint8),ss[j,r])),'four retained D images')
 V=sorted(set(sum([I[j]for j in J],[])));need(len(V)==32,'native support');Z=np.hstack([BK[j]^BK[61]for j in J if j!=61]);cr=rank(Z);aug=rank(np.hstack([Z,BK[61]]));inter=16-rank(np.vstack([G[:,V],H[:,V]]));need((cr,aug,inter)==(16,18,2),'exact new dimensions');need(not np.any(mm(Q,Z))and rank(Q[:,V])==8,'eight actual common rows')
 changed=Q.copy();changed[1,1]^=1;need(np.any(mm(changed,Z)),'actual54 coefficient corruption rejected')
 bad_d=d.copy();bad_d[0]^=1;need(not np.array_equal(H,P[mm(M,G),bad_d[None,:]]),'pencil parameter corruption rejected')
 off_records=[];leaking=[]
 for gate in target_record['donor_gates']:
  j=gate['donor'];Moff=np.array(gate['off_matrix'],dtype=np.uint8);need(Moff.shape[1]==16,'two retained blocks')
  S9=old[np.ix_(O[9],I[j])];S48=old[np.ix_(O[48],I[j])];A=mm(Moff[:,:8],S9);B=mm(Moff[:,8:],S48)
  coefficient=np.vstack([mm(mm(S9,ss[j,9]),W[8:16]),mm(mm(S48,ss[j,48]),W[16:24])]);leak=mm(Moff,coefficient)
  C=A^P[B,INV[d[I[j]]][None,:]];X=mm(ss[j,9],G[:,E]);factored=mm(mm(mm(C,X),Dalpha),H0)
  need(np.array_equal(leak,factored),'exact diagonal pencil isolation identity');need(rank(X)==2,'rank two isolation unknown');lr=rank(leak)
  if lr:leaking.append(j)
  off_records.append({'donor':j,'off_matrix':Moff.tolist(),'old9_section':S9.tolist(),'old48_section':S48.tolist(),'A':A.tolist(),'B':B.tolist(),'C_at_candidate':C.tolist(),'C_nullity':8-rank(C),'X_at_candidate':X.tolist(),'coefficient':coefficient.tolist(),'off54_response':leak.tolist(),'off54_rank':lr})
 need(leaking==[32,35,38,45,68,69,90,100],'literal parent leakage census')
 need(all(vv['off54_rank']==(2 if vv['donor']in leaking else 0)for vv in off_records),'leakage ranks')
 out.mkdir(parents=True,exist_ok=True);save(out/'CERTIFICATE.json.gz',{'K_factors':{'9':C9.tolist(),'48':C48.tolist()},'K_reference_profile':H0.tolist(),'source_K_ingress':{j:A0.tolist()for j,A0 in BK.items()},'contrast':Z.tolist(),'actual54_common_response':expected.tolist(),'geometric_section_ranks':sections,'actual54_rows':O[54],'native_union':V,'off54_isolation_equations':off_records})
 result={'status':'PASS_ACTUAL54_FORCED_TWO_SPACE_READOUT_WITH_PARENT_LEAKAGE','native_donors':len(J),'retained_local_systems':44,'geometric_sections':len(sections),'phase_ranks':[19,16],'contrast_rank':cr,'joined_K_ingress_rank':aug,'actual54_common_output_rows':8,'actual54_response_rank':2,'actual54_contrast_response_rank':0,'native_common_decoder_dimension':len(V)-cr,'retained9_48_intersection_dimension':inter,'fixed_K_dimension':2,'whole_fifth_fibre_dimension_required':8,'parent_off54_leakage_ranks':{v0['donor']:v0['off54_rank']for v0 in off_records},'pencil_C_nullities':{v0['donor']:v0['C_nullity']for v0 in off_records},'full_source_validity_from_canonical_extension':'not claimed','whole_fifth_receiver':False,'compiler_cost_claimed_here':False,'new_complete_kappa':False};save(out/'RESULT.json',result);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
