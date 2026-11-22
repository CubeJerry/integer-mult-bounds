#!/usr/bin/env python3
"""Independent three-overlap and full-H gauge review."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import numpy as np

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('fifth_review_arithmetic',HERE.parent/'check.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def main(repo,candidate,gauge_file,out):
    root=repo/'research/moonshot-005-program/results'
    four=root/'bit-simultaneous-d1509-s032/output'
    files=[root/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',
           four/'D-WORD.json.gz',candidate]
    z,dw,new=map(m.read,files)
    T=np.array(dw['matrix'],dtype=np.uint8)
    TT=np.array(new['D_matrix'],dtype=np.uint8)
    I={int(j):v for j,v in z['D_inputs'].items()}
    O={int(r):v for r,v in z['D_outputs'].items()}
    J=z['donors'];V=sorted(set(sum(I.values(),[])))
    W=np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8)
    L=np.array(z['common_frames'],dtype=np.uint8);K=m.mm(L,W)
    F=[4,5,7,8]
    m.need(np.array_equal(TT[np.ix_(sorted(set(sum(O.values(),[]))),F)],
                          T[np.ix_(sorted(set(sum(O.values(),[]))),F)]),'fixed rectangle')
    m.need(not np.any(TT[:19,19:]) and m.rank(TT[:19,:19])==19 and m.rank(TT[19:,19:])==16,'phases')
    B,Z,result=m.contrasts(TT,z,W,I,O,J)
    m.need(result==dict(contrast_rank=27,augmented_rank=31,abstract_common_response_rank=4),'new rank profile')
    readouts_path=four/'READOUTS.json.gz'
    readouts=m.read(readouts_path)
    files.append(readouts_path)
    native_section_count=0
    for donor,receivers in readouts.items():
        for receiver,section in receivers.items():
            indices_in=section['D_inputs'];indices_out=section['D_outputs']
            m.need(m.rank(TT[np.ix_(indices_out,indices_in)])==8,'native donor/geometric receiver section')
            native_section_count+=1
    m.need(native_section_count==132,'all native donor/geometric receiver sections')
    row48=TT[np.ix_(O[48],V)];row73=TT[np.ix_(O[73],V)]
    join=np.vstack([row48,row73])
    intersection_dim=m.rank(row48)+m.rank(row73)-m.rank(join)
    m.need(m.rank(row48)==8 and m.rank(row73)==8 and m.rank(join)==11 and intersection_dim==5,'sharp overlap ceiling')
    combos={int(r):np.array(C,dtype=np.uint8) for r,C in new['receiver_combinations'].items()}
    common48=m.mm(combos[48],TT[O[48]])
    common73=m.mm(combos[73],TT[O[73]])
    m.need(np.array_equal(common48[:,V],common73[:,V]),'three exact native overlaps')
    m.need(m.rank(common48[2:,V])==1 and not np.any(common48[2:,F]),'nonzero zero-profile common row')
    for j in J:m.need(not np.any(m.mm(common48[2:],B[j])),'zero-profile row annihilates every donor image')
    A=np.vstack([TT[[10,30]],common48])
    m.need(m.rank(A[:,V])==5 and not np.any(m.mm(A,Z)) and m.rank(m.mm(A,B[61]))==4,'five common native rows, four response dimensions')
    actual95=[10,13,16,18,30,31,32,33]
    result.update(status='PASS_INDEPENDENT_THREE_OVERLAP_REVIEW',native_span_rank=m.rank(np.hstack(list(B.values()))),
                  overlap_dimension=intersection_dim,overlap_ceiling=5,actual_receiver_rows=8,
                  required_extra_common_rows_outside_overlap=3,
                  independently_checked_native_donor_geometric_receiver_sections=native_section_count,
                  actual95_contrast_response_rank=m.rank(m.mm(TT[actual95],Z)),
                  universal_span32_disproved=True,universal_contrast_lower_bound_claimed=False,
                  full_receiver_gate_passed=False,new_complete_kappa=False)
    if gauge_file:
        gauge=m.read(gauge_file)
        m.need(np.array_equal(np.array(gauge['D_matrix'],dtype=np.uint8),TT),'gauges belong to candidate')
        fibpath=root/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz'
        sourcepath=four/'SOURCES.json.gz'
        ingresspath=root/'bit-d1509-coupled-repair-s032/DATA.json.gz'
        files.extend([gauge_file,fibpath,sourcepath,ingresspath])
        fib,source,ingress=m.read(fibpath),m.read(sourcepath),m.read(ingresspath)['ingress']
        cores={}
        for h,rows in fib.items():
            C=np.hstack([np.array(v['kernel'],dtype=np.uint8)[:48,:3] for v in rows.values()])
            C=C[:,m.rref(C)[1]];zero=np.zeros_like(C)
            cores[int(h)]=np.block([[C,zero],[zero,C]])
        reviews=[]
        for j in J:
            hs=[C for h,C in cores.items() if str(h) in source['paired_maps'][str(j)]]
            H=np.hstack(hs) if hs else np.zeros((96,0),dtype=np.uint8)
            H=H[:,m.rref(H)[1]]
            G=np.array(gauge['source_right_gauges'][str(j)],dtype=np.uint8)
            target=np.hstack([m.mm(L[:,8*k:8*k+8],m.mm(T[np.ix_(O[r],I[j])],m.inverse(TT[np.ix_(O[r],I[j])]))) for k,r in enumerate(z['retained_receivers'])])
            m.need(m.rank(G)==96 and np.array_equal(m.mm(G,H),H),'fullH source gauge')
            m.need(np.array_equal(m.mm(G,L),target) and np.array_equal(m.mm(m.inverse(G),target),L),'whole frame images')
            dim=m.rank(H)+32-m.rank(np.hstack([H,L]))
            gcols=np.hstack([m.mm(L[:,8*k:8*k+8],T[np.ix_(O[r],sorted(set(I[j])&set(F)))]) for k,r in enumerate(z['retained_receivers'])])
            m.need(m.rank(gcols)==dim and m.rank(np.hstack([H,gcols]))==m.rank(H),'fullH intersection')
            if j==61:m.need(np.array_equal(m.mm(G,K),K),'forcedK fixed at61')
            direct=m.mm(m.mm(np.array(ingress[str(j)],dtype=np.uint8),G),K)
            m.need(np.array_equal(direct,B[j]),'direct physical ingress agrees with section formula')
            reviews.append(dict(donor=j,gauge_rank=96,H_rank=m.rank(H),intersection_dimension=dim))
        result['independent_full_source_gauge_review']=reviews
    pins={str(p.relative_to(repo)) if p.is_relative_to(repo) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    expected=HERE/'SOURCE-PINS.json'
    if expected.exists():m.need(pins==m.read(expected),'wave-two source pins')
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n')
    (out/'CERTIFICATE.json').write_text(json.dumps(dict(five_common_rows=A.tolist(),zero_profile_annihilator=common48[2].tolist()),indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--candidate',type=Path,required=True);p.add_argument('--gauges',type=Path)
    p.add_argument('--out',type=Path,required=True);q=p.parse_args()
    main(q.repo.resolve(),q.candidate.resolve(),q.gauges.resolve() if q.gauges else None,q.out.resolve())
