#!/usr/bin/env python3
"""Exact rank-one line audit from raw geometry and independent local systems."""
from pathlib import Path
import argparse,gzip,hashlib,json,runpy
import numpy as np
HERE=Path(__file__).resolve().parent
BASE=HERE.parent

def rd(p):
    data=p.read_bytes()
    return json.loads(gzip.decompress(data) if p.suffix=='.gz' else data)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    for name,digest in rd(HERE/'independent-line-review-b-pins.json')['files_relative_to_results'].items():
        assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==digest,name
    alg=runpy.run_path(str(BASE/'bit-d1509-nonlinear-partition-gate-s032/independent-review-b.py'))
    MUL,INV,rank=alg['MUL'],alg['INV'],alg['rank']
    def mm(A,B):
        A=np.asarray(A,dtype=np.uint8);B=np.asarray(B,dtype=np.uint8)
        C=np.zeros((A.shape[0],B.shape[1]),dtype=np.uint8)
        for i in range(A.shape[1]):C^=MUL[A[:,i,None],B[i,None,:]]
        return C
    def inverse(A):
        A=np.array(A,dtype=np.uint8);n=len(A)
        B=np.hstack([A,np.eye(n,dtype=np.uint8)])
        for j in range(n):
            p=j+int(np.flatnonzero(B[j:,j])[0]);B[[j,p]]=B[[p,j]]
            B[j]=MUL[INV[B[j,j]],B[j]]
            for i in range(n):
                if i!=j:B[i]^=MUL[B[i,j],B[j]]
        return B[:,n:]
    layout=rd(BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz')
    roots=np.array(layout['root_table'],dtype=np.int64)
    adj=[set(np.flatnonzero(z==0).tolist()) for z in roots@roots.T]
    planes=[set(z) for z in layout['A2']];charts=[set(z) for z in layout['D4']]
    routepath=BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    routes=[json.loads(line) for line in gzip.decompress(routepath.read_bytes()).splitlines()]
    owners=sorted([z for z in routes if z[4]==1509 and z[0]=='X'],key=lambda z:(z[1],z[2]))+sorted([z for z in routes if z[4]==1509 and z[0]=='Y'],key=lambda z:(z[1],z[2]))
    dw=rd(BASE/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz')
    assert owners==dw['owners']
    T=np.array(dw['matrix'],dtype=np.uint8)
    assert not np.any(T[:19,19:])
    gg=rd(BASE/'bit-simultaneous-d1509-s032/output/CONSTRAINED-GAUGES.json.gz')
    L=np.array(gg['common_frames'],dtype=np.uint8);R=gg['receivers'];J=sorted(map(int,gg['gauges']))
    geomJ=sorted(charts[1509]);geomR=[r for r in range(120) if charts[1509]<=adj[r]]
    I={j:[i for i,z in enumerate(owners) if z[3] is not None and j in planes[z[3]]] for j in geomJ}
    O={r:[i for i,z in enumerate(owners) if z[5] is not None and r in planes[z[5]]] for r in geomR}
    candidate=rd(HERE/'CERTIFICATE.json.gz')['candidate']
    delta=np.array(candidate['delta_D'],dtype=np.uint8)
    assert delta.shape==(35,35) and np.count_nonzero(delta)==1 and delta[0,0]==1
    systems=rd(BASE/'bit-source-d-interpolation-s032-independent/output/RECONSTRUCTED-MATRICES.json.gz')
    ci={};slopes={};derivatives={};poles=set();geometric=[];pole_controls=0
    for j in geomJ:
        for r in geomR:
            A=T[np.ix_(O[r],I[j])];E=delta[np.ix_(O[r],I[j])]
            assert A.shape==(8,8) and rank(A)==8 and rank(E)<=1
            ai=inverse(A);Q=mm(ai,E);lam=int(np.bitwise_xor.reduce(np.diag(Q)))
            assert np.array_equal(mm(Q,Q),MUL[lam,Q])
            assert rank(A^E)==8
            if lam:
                pole=int(INV[lam]);poles.add(pole)
                assert rank(A^MUL[pole,E])==7
                pole_controls+=1
            geometric.append({'donor':j,'receiver':r,'slope':lam})
            if j in J and r in R:
                ci[j,r]=ai;slopes[j,r]=lam;derivatives[j,r]=mm(Q,ai)
    assert len(geometric)==144
    phase_poles=set();phase_records=[]
    for start,stop in [(0,19),(19,35)]:
        A=T[start:stop,start:stop];E=delta[start:stop,start:stop];n=stop-start
        assert rank(A)==n and rank(E)<=1
        Q=mm(inverse(A),E);lam=int(np.bitwise_xor.reduce(np.diag(Q)))
        assert np.array_equal(mm(Q,Q),MUL[lam,Q]) and rank(A^E)==n
        if lam:
            pole=int(INV[lam]);phase_poles.add(pole)
            assert rank(A^MUL[pole,E])==n-1
        phase_records.append({'range':[start,stop],'slope':lam})
    group_records=[];changed=[]
    for j in J:
        for r in R:
            stack=np.vstack([z['target_maps'][str(r)] for key,z in systems.items() if int(key.split('/')[0])==j])
            assert stack.shape==(24,8) and rank(stack)==8
    for key,z in systems.items():
        j=int(key.split('/')[0]);F=np.array(z['source'],dtype=np.uint8)
        C=np.array(z['native_H_span'],dtype=np.uint8);N=np.array(z['relations'],dtype=np.uint8)
        X=np.hstack([C,L]);groups={}
        for t,r in enumerate(R):
            M=np.array(z['target_maps'][str(r)],dtype=np.uint8)
            term=mm(mm(M,derivatives[j,r]),N[C.shape[1]+8*t:C.shape[1]+8*t+8])
            groups.setdefault(slopes[j,r],np.zeros_like(term));groups[slopes[j,r]]^=term
        assert all(not np.any(v) for v in groups.values())
        D=np.array(candidate['source_protected_delta'][key],dtype=np.uint8)
        target=np.hstack([mm(F,C)]+[mm(np.array(z['target_maps'][str(r)],dtype=np.uint8),inverse((T^delta)[np.ix_(O[r],I[j])])) for r in R])
        assert np.array_equal(mm(F^D,X),target)
        if np.any(D):changed.append(key)
        group_records.append({'system':key,'slopes':sorted(groups),'group_residual_ranks':{str(k):rank(v) for k,v in groups.items()}})
    assert len(group_records)==44 and len(changed)==12
    allowed=[t for t in range(1,64) if t not in poles|phase_poles]
    claimed=rd(HERE/'LIFT-RESULT.json')
    assert sorted(poles)==[2,7,21,36,37,45,48,53,60]
    assert sorted(phase_poles)==[46] and len(allowed)==53
    assert claimed['all_geometric_section_poles']==sorted(poles)
    assert claimed['phase_poles']==sorted(phase_poles)
    assert claimed['nonzero_parameters_preserving_all_D_sections_and_phases']==allowed
    result={'status':'PASS_INDEPENDENT_B_EXACT_LOCAL_RATIONAL_LINE','raw_D_owners_reconstructed':len(owners),'geometric_sections':144,'pole_rank_drop_controls':pole_controls,'geometric_section_poles':sorted(poles),'phase_poles':sorted(phase_poles),'allowed_nonzero_parameters':allowed,'allowed_count':len(allowed),'grouped_local_systems_checked':44,'rank8_parent_stacks_checked':44,'exact_t1_source_equations_checked':44,'changed_t1_quotients':changed,'new_author_executable_imports':False,'full_source_validity_checked':False,'source_word_compiled':False,'fifth_whole_fibre_proved':False,'new_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    (args.out/'CERTIFICATE.json').write_text(json.dumps({'geometric_sections':geometric,'phases':phase_records,'grouped_residuals':group_records},sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
