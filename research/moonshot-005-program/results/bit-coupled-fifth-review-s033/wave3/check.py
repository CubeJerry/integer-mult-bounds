#!/usr/bin/env python3
"""Independent diagonal-code readout and forced proper-isolation audit."""
from pathlib import Path
import argparse, hashlib, importlib.util, json
import numpy as np
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_gf64',HERE.parent/'check.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def main(repo,candidate,gauge_file,out):
    root=repo/'research/moonshot-005-program/results';four=root/'bit-simultaneous-d1509-s032/output'
    names=[root/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',four/'D-WORD.json.gz',
           four/'READOUTS.json.gz',four/'PROPER.json.gz',four/'CONSTRAINED-GAUGES.json.gz',
           four/'SOURCES.json.gz',four/'H-PHYSICAL.json.gz',candidate,gauge_file]
    z,dw,readouts,proper,old_gauges,sources,physical,new,lift=map(m.read,names)
    T=np.array(dw['matrix'],dtype=np.uint8);TT=np.array(new['D_matrix'],dtype=np.uint8)
    m.need(np.array_equal(np.array(lift['D_matrix'],dtype=np.uint8),TT),'same gauge candidate')
    I={int(j):v for j,v in z['D_inputs'].items()};O={int(r):v for r,v in z['D_outputs'].items()}
    J=z['donors'];R=z['retained_receivers'];F=[4,5,7,8];V=sorted(set(sum(I.values(),[])))
    L=np.array(z['common_frames'],dtype=np.uint8);W=np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8);K=m.mm(L,W)
    m.need(np.array_equal(TT[np.ix_(sorted(set(sum(O.values(),[]))),F)],T[np.ix_(sorted(set(sum(O.values(),[]))),F)]),'fixed rectangle')
    m.need(not np.any(TT[:19,19:]) and m.rank(TT[:19,:19])==19 and m.rank(TT[19:,19:])==16,'legal phases')
    B,Z,result=m.contrasts(TT,z,W,I,O,J);o95=[10,13,16,18,30,31,32,33]
    m.need(result==dict(contrast_rank=24,augmented_rank=28,abstract_common_response_rank=4),'pencil ranks')
    m.need(not np.any(m.mm(TT[o95],Z)) and m.rank(m.mm(TT[o95],B[61]))==4,'actual95 common injective readout')
    m.need(m.rank(TT[np.ix_(o95,V)])==8,'eight actual native rows')
    m.need(16-m.rank(np.vstack([TT[np.ix_(O[48],V)],TT[np.ix_(O[73],V)]]))==2,'two-row intersection')
    d=np.array(new['d'],dtype=np.uint8);P=np.array(new['M'],dtype=np.uint8);Q=np.array(new['N'],dtype=np.uint8)
    m.need(not np.any(d==0) and not np.any(d==1),'diagonal units and complements')
    G=TT[O[48]];H=TT[O[73]];A=TT[o95]
    m.need(m.rank(P)==8 and m.rank(Q)==8,'pencil row transformations')
    m.need(np.array_equal(H,m.MUL[m.mm(P,G),d[None,:]]),'second receiver diagonal code')
    m.need(np.array_equal(A,m.MUL[m.mm(Q,G),m.MUL[d,m.INV[d^1]][None,:]]),'actual95 diagonal code')
    C48=m.solve(T[np.ix_(O[48],F)],W[16:24]);C73=m.solve(T[np.ix_(O[73],F)],W[24:32]);H0=C48^C73
    alpha=np.array([53,53,58,58],dtype=np.uint8);Dalpha=np.diag(alpha)
    m.need(np.array_equal(m.mm(C48,m.inverse(H0)),Dalpha),'first coefficient profile')
    m.need(np.array_equal(m.mm(C73,m.inverse(H0)),np.eye(4,dtype=np.uint8)^Dalpha),'second coefficient profile')
    m.need(np.array_equal(m.MUL[d[F],alpha^1],alpha),'diagonal transfer identity')
    common=m.mm(m.mm(m.mm(Q,G[:,F]),Dalpha),H0)
    for j in J:m.need(np.array_equal(m.mm(A,B[j]),common),'all eleven actual readouts')
    section_count=0
    for donor,receivers in readouts.items():
        for receiver,section in receivers.items():
            m.need(m.rank(TT[np.ix_(section['D_outputs'],section['D_inputs'])])==8,'native/geometric section')
            section_count+=1
    m.need(section_count==132,'all native/geometric sections')
    # Source extension identities and extension-independent parent leakage.
    h_of={tuple(x[:3]):int(h) for h,block in physical.items() for name in ['X_owners','Y_owners'] for x in block[name]}
    protected=list(range(48))+list(range(240,288));prows=[0,1,2,15,16,17]
    leaks=[];gauge_records=[];local_equations=0
    for j in J:
        labels=[tuple(x) for x in proper[str(j)]['95']['labels']]
        baseline=m.mm(np.array(proper[str(j)]['95']['matrix'],dtype=np.uint8),np.array(old_gauges['gauges'][str(j)],dtype=np.uint8))
        canonical=baseline.copy();parent_rows=[];target_rows=[]
        for key,system in z['systems'].items():
            jj,h=map(int,key.split('/'))
            if jj!=j:continue
            oldF=np.array(system['old_protected_map'],dtype=np.uint8)
            delta=np.array(new['source_protected_delta'][key],dtype=np.uint8)
            newF=oldF^delta
            C=np.array(system['H_observation_core'],dtype=np.uint8)
            maps=[np.array(M,dtype=np.uint8) for M in system['receiver_ingress_to_quotient_maps']]
            wanted=np.hstack([m.mm(M,m.inverse(TT[np.ix_(O[r],I[j])])) for M,r in zip(maps,R)])
            m.need(np.array_equal(m.mm(newF,L),wanted) and np.array_equal(m.mm(newF,C),m.mm(oldF,C)),'exact quotient images')
            local_equations+=1
            rows=[q for q,label in enumerate(labels) if h_of[label]==h]
            actualF=np.array(sources['paired_maps'][str(j)][str(h)],dtype=np.uint8)[np.ix_(prows,protected)]
            m.need(np.array_equal(actualF,oldF),'actual source quotient binding')
            pivots=m.rref(oldF)[1]
            to_proper=m.mm(baseline[rows][:,pivots],m.inverse(oldF[:,pivots]))
            m.need(np.array_equal(m.mm(to_proper,oldF),baseline[rows]),'source-to-proper factor')
            canonical[rows]^=m.mm(to_proper,delta)
            parent_rows.extend(rows)
            # The following image depends on the prescribed L images only.
            target=m.mm(m.mm(to_proper,wanted),W)
            target_rows.extend((q,target[t]) for t,q in enumerate(rows))
        input_labels=[tuple(dw['owners'][q][:3]) for q in I[j]]
        inrows=[labels.index(label) for label in input_labels]
        offrows=[q for q in range(96) if q not in inrows]
        parentoff=sorted(set(parent_rows)-set(inrows))
        m.need(len(parentoff)==16,'sixteen proper offD parent rows')
        canonical_K=m.mm(canonical,K)
        gauge=np.array(lift['source_right_gauges'][str(j)],dtype=np.uint8)
        m.need(m.rank(gauge)==96,'full source gauge invertible')
        targetL=np.hstack([m.mm(L[:,8*k:8*k+8],m.mm(T[np.ix_(O[r],I[j])],m.inverse(TT[np.ix_(O[r],I[j])]))) for k,r in enumerate(R)])
        m.need(np.array_equal(m.mm(gauge,L),targetL),'oriented global source images')
        global_K=m.mm(m.mm(baseline,gauge),K)
        for q,target in target_rows:
            m.need(np.array_equal(canonical_K[q],target) and np.array_equal(global_K[q],target),'forced parent image independent of extension')
        m.need(np.array_equal(canonical_K[inrows],B[j][I[j]]) and np.array_equal(global_K[inrows],B[j][I[j]]),'actual ingress formula')
        forced=canonical_K[parentoff]
        leaks.append(dict(donor=j,forced_parent_offD_rank=m.rank(forced),canonical_all_offD_rank=m.rank(canonical_K[offrows]),
                          global_all_offD_rank=m.rank(global_K[offrows]),proper_rows=parentoff,
                          proper_labels=[labels[q] for q in parentoff],forced_matrix=forced.tolist()))
        gauge_records.append(dict(donor=j,rank=96,oriented_frame_equations=True))
    expected={0:2,32:4,35:4,38:4,45:2,61:0,62:2,68:4,69:4,90:4,100:2}
    m.need({x['donor']:x['forced_parent_offD_rank'] for x in leaks}==expected,'literal forced leakage profile')
    # Controls: perturb one actual output row and one transfer diagonal.
    bad=A.copy();bad[1,0]^=1
    m.need(np.any(m.mm(bad,Z)),'actual output mutation rejected')
    bad_d=d.copy();bad_d[0]^=1
    m.need(not np.array_equal(H,m.MUL[m.mm(P,G),bad_d[None,:]]),'diagonal mutation rejected')
    result.update(status='PASS_INDEPENDENT_PENCIL_ACTUAL95_AND_ISOLATION_REVIEW',
                  actual95_contrast_response_rank=0,actual95_common_response_rank=4,
                  actual95_native_row_rank=8,common_annihilator_dimension=8,old_receiver_intersection_dimension=2,
                  common_rows_outside_intersection=6,independently_checked_sections=section_count,
                  exact_local_source_systems=local_equations,
                  forced_parent_leakage_ranks={x['donor']:x['forced_parent_offD_rank'] for x in leaks},
                  fifth_whole_receiver=False,all_source_extensions_excluded=False,
                  literal_candidate_protected_quotient_complement_repairs_excluded=True,
                  new_complete_kappa=False,negative_controls=['actual output coefficient','transfer diagonal'])
    pins={str(p.relative_to(repo)) if p.is_relative_to(repo) else str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in names}
    expected_pins=HERE/'SOURCE-PINS.json'
    if expected_pins.exists():m.need(pins==m.read(expected_pins),'source pins')
    out.mkdir(parents=True,exist_ok=True)
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'CERTIFICATE.json').write_text(json.dumps(dict(common_actual_response=common.tolist(),forced_isolation_leaks=leaks,
        independently_checked_gauges=gauge_records),indent=2,sort_keys=True)+'\n')
    (out/'SOURCE-PINS.json').write_text(json.dumps(pins,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--candidate',type=Path,required=True)
    p.add_argument('--gauges',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args()
    main(q.repo.resolve(),q.candidate.resolve(),q.gauges.resolve(),q.out.resolve())
