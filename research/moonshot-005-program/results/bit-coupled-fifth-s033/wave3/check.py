"""Exact diagonal-pencil readout certificate; no whole fifth fibre claimed.
@CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import argparse,importlib.util,hashlib,json,gzip
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('s033_arithmetic',HERE.parent/'check.py');alg=importlib.util.module_from_spec(spec);spec.loader.exec_module(alg)
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
 W=np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8);L=np.array(z['common_frames'],dtype=np.uint8);need(not np.any(W[:16]),'only48/73 forcedK coefficients')
 C48=solve(old[np.ix_(O[48],F)],W[16:24]);C73=solve(old[np.ix_(O[73],F)],W[24:32]);H0=C48^C73;need(rank(H0)==4,'reference K profile')
 alpha=np.array([53,53,58,58],dtype=np.uint8);Dalpha=np.diag(alpha);need(np.array_equal(mm(C48,inverse(H0)),Dalpha),'two exact scalar sectors')
 d=np.array(c['d'],dtype=np.uint8);need(d.shape==(35,)and not np.any(d==0)and not np.any(d==1),'nonzero pencil denominators');need(np.array_equal(d[F],P[alpha,INV[alpha^1]]),'F pencil parameters')
 M=np.array(c['M'],dtype=np.uint8);N=np.array(c['N'],dtype=np.uint8);G=T[O[48]];H=T[O[73]];Q=T[O[95]];need(rank(M)==rank(N)==8,'row changes')
 need(np.array_equal(H,P[mm(M,G),d[None,:]]),'73 diagonal scaling');need(np.array_equal(Q,P[mm(N,G),P[d,INV[d^1]][None,:]]),'actual95 weighted code')
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
  expected=mm(mm(mm(N,G[:,F]),Dalpha),H0);need(np.array_equal(mm(Q,BK[j]),expected),'actual95 common response identity')
 need(rank(expected)==4,'injective forcedK response')
 for key,v in z['systems'].items():
  j,h=map(int,key.split('/'));oldF=np.array(v['old_protected_map'],dtype=np.uint8);newF=oldF^np.array(c['source_protected_delta'][key],dtype=np.uint8);C=np.array(v['H_observation_core'],dtype=np.uint8)
  need(np.array_equal(mm(oldF,C),mm(newF,C)),'H images')
  for t,r in enumerate(R):need(np.array_equal(mm(newF,L[:,8*t:8*t+8]),mm(np.array(v['receiver_ingress_to_quotient_maps'][t],dtype=np.uint8),ss[j,r])),'four retained D images')
 V=sorted(set(sum([I[j]for j in J],[])));need(len(V)==32,'native support');Z=np.hstack([BK[j]^BK[61]for j in J if j!=61]);cr=rank(Z);aug=rank(np.hstack([Z,BK[61]]));inter=16-rank(np.vstack([G[:,V],H[:,V]]));need((cr,aug,inter)==(24,28,2),'exact new dimensions');need(not np.any(mm(Q,Z))and rank(Q[:,V])==8,'eight actual common rows')
 changed=Q.copy();changed[1,0]^=1;need(np.any(mm(changed,Z)),'actual95 coefficient corruption rejected')
 bad_d=d.copy();bad_d[0]^=1;need(not np.array_equal(H,P[mm(M,G),bad_d[None,:]]),'pencil parameter corruption rejected')
 out.mkdir(parents=True,exist_ok=True);save(out/'CERTIFICATE.json.gz',{'K_factors':{'48':C48.tolist(),'73':C73.tolist()},'K_reference_profile':H0.tolist(),'source_K_ingress':{j:A.tolist()for j,A in BK.items()},'contrast':Z.tolist(),'actual95_common_response':expected.tolist(),'geometric_section_ranks':sections,'actual95_rows':O[95],'native_union':V})
 result={'status':'PASS_ACTUAL95_DIAGONAL_PENCIL_FORCED_K_READOUT','native_donors':len(J),'retained_local_systems':44,'geometric_sections':len(sections),'phase_ranks':[19,16],'contrast_rank':cr,'joined_K_ingress_rank':aug,'common_response_rank':4,'actual95_common_output_rows':8,'actual95_response_rank':4,'actual95_contrast_response_rank':0,'native_common_decoder_dimension':len(V)-cr,'retained48_73_intersection_dimension':inter,'decoders_beyond_intersection':len(V)-cr-inter,'fixed_K_dimension':4,'whole_fifth_fibre_dimension_required':8,'full_source_validity_from_canonical_extension':False,'whole_fifth_receiver':False,'compiler_cost_claimed_here':False,'new_complete_kappa':False};save(out/'RESULT.json',result);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
