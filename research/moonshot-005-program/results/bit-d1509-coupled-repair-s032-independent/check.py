#!/usr/bin/env python3
"""Reconstruct the physical ingress and audit the bounded D-word repair.

Imports only the earlier independent generic GF64 algebra, not author code.
"""
import argparse, gzip, hashlib, json, runpy
from collections import defaultdict
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent; BASE=HERE.parent; ROOT=BASE.parents[2]
H=runpy.run_path(str(BASE/'bit-simultaneous-d1509-s032-independent/check_frames.py'))
mm,rank,inverse,rd,wr,need=[H[k] for k in ['mm','rank','inverse','rd','wr','need']]
null=H['ALG']['null']

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out',type=Path,default=HERE/'output'); args=ap.parse_args()
    for file,digest in rd(HERE/'SOURCE-PINS.json')['files'].items():
        need(hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,'source binding '+file)
    four=BASE/'bit-simultaneous-d1509-s032/output'; author=BASE/'bit-d1509-coupled-repair-s032'
    source,hp,dw,gg=[rd(four/n) for n in ['SOURCES.json.gz','H-PHYSICAL.json.gz','D-WORD.json.gz','CONSTRAINED-GAUGES.json.gz']]
    data=rd(author/'DATA.json.gz'); candidate=rd(author/'ALL-DONOR-VECTOR.json')['witness']
    witness=rd(BASE/'bit-fifth-receiver-quotient-s032/WITNESS.json')
    layout=rd(BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz')
    roots=np.array(layout['root_table'],dtype=np.int64); dots=roots@roots.T
    need(roots.shape==(120,8) and np.all(np.diag(dots)==4),'root norms')
    adj=[set(np.flatnonzero(row==0).tolist()) for row in dots]
    planes=[set(z) for z in layout['A2']]; charts=[set(z) for z in layout['D4']]
    marked=set(rd(BASE/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')['selected_D'])
    routes=[json.loads(z) for z in gzip.decompress((BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()]
    X,Y,Xj,Yj=[defaultdict(list) for _ in range(4)]
    for r in routes:
        if r[3] is None: continue
        (X if r[0]=='X' else Y)[r[3]].append(r)
        if r[0]=='X': Xj[r[1],r[3]].append(r)
        elif r[6] is not None: Yj[r[6],r[3]].append(r)
    for tab in [X,Y,Xj,Yj]:
        for key in tab: tab[key].sort(key=lambda r:(r[1],r[2]))
    owners=sorted([r for r in routes if r[4]==1509 and r[0]=='X'],key=lambda r:(r[1],r[2]))+sorted([r for r in routes if r[4]==1509 and r[0]=='Y'],key=lambda r:(r[1],r[2]))
    need(owners==dw['owners'] and len(owners)==35,'raw route D ownership')
    oi={(r[0],r[1],r[2]):i for i,r in enumerate(owners)}
    receivers=[r for r in range(120) if charts[1509]<=adj[r]]
    outs={r:[i for i,x in enumerate(owners) if x[5] is not None and r in planes[x[5]]] for r in receivers}
    ins={j:[i for i,x in enumerate(owners) if x[3] is not None and j in planes[x[3]]] for j in charts[1509]}
    donors=sorted(map(int,source['paired_maps'])); retained=gg['receivers']; L=np.array(gg['common_frames'],dtype=np.uint8)
    need(retained==[6,9,48,73] and donors==sorted(j for j in charts[1509] if j<111),'literal native donor and retained receiver sets')
    v=np.array(witness['vector'],dtype=np.uint8).reshape(96,1); coeff=np.zeros((32,1),dtype=np.uint8)
    for t,c in witness['four_frame_coefficients']: coeff[t]=c
    need(np.array_equal(mm(L,coeff),v),'literal vector in four-frame span')
    prot=list(range(48))+list(range(240,288)); P={}; O={}
    for j in donors:
        ingress=np.zeros((35,96),dtype=np.uint8); off={r:[] for r in retained+[95]}
        for hs,F0 in source['paired_maps'][str(j)].items():
            h=int(hs); F=np.array(F0,dtype=np.uint8)[:,prot]; Q=np.array(source['frames'][f'{j}/{h}'],dtype=np.uint8)
            need(hp[hs]['X_owners']==X[h] and hp[hs]['Y_owners']==Y[h],'raw H owners')
            ne,nl=len(X[h]),len(Y[h]); E=np.array(hp[hs]['early'],dtype=np.uint8).reshape(ne,ne)
            B=np.array(hp[hs]['late'],dtype=np.uint8).reshape(nl,nl); C=np.array(hp[hs]['cross'],dtype=np.uint8).reshape(nl,ne)
            xe=np.zeros((ne,30),dtype=np.uint8); yl=np.zeros((nl,30),dtype=np.uint8)
            xi={(x[1],x[2]):t for t,x in enumerate(X[h])}; yi={(x[1],x[2]):t for t,x in enumerate(Y[h])}
            for t,x in enumerate(Xj[j,h]): xe[xi[x[1],x[2]]]=Q[t]
            for t,x in enumerate(Yj[j,h]): yl[yi[x[1],x[2]]]=Q[len(Xj[j,h])+t]
            values=[mm(mm(E,xe),F),mm(mm(C,xe)^mm(B,yl),F)]
            for phase,seq,A in [('X',X[h],values[0]),('Y',Y[h],values[1])]:
                for t,x in enumerate(seq):
                    if x[4]==1509: ingress[oi[phase,x[1],x[2]]]=A[t]
                    elif x[4] in marked:
                        for r in off:
                            if planes[h]<=adj[r] and charts[x[4]]<=adj[r]: off[r].append(A[t])
        need(np.array_equal(ingress,np.array(data['ingress'][str(j)],dtype=np.uint8)),'independent actual ingress '+str(j))
        P[j]=ingress
        for r in off:
            O[j,r]=np.array(off[r],dtype=np.uint8)
            need(O[j,r].shape==(88,96) and rank(O[j,r])==88,'entire protected off-D restriction')
    M={(j,r):mm(P[j],L[:,8*t:8*t+8]) for j in donors for t,r in enumerate(retained)}
    T=np.array(dw['matrix'],dtype=np.uint8); delta=np.array(data['partial_delta'],dtype=np.uint8)
    S=np.array(candidate['matrix'],dtype=np.uint8); q=mm(P[0]^P[61],v)
    need(np.array_equal(q,np.array(data['source_difference'],dtype=np.uint8)),'actual pair ingress difference')
    before=mm(T[outs[95]],q)[:,0]; need(before.tolist()==[0,28,45,17,0,62,23,17],'old actual mismatch')
    freedom=[]
    for row in range(35):
        n=19 if row<19 else 35; seen=[r for r in retained if row in outs[r]]
        C=np.hstack([M[j,r][:n] for r in seen for j in donors]) if seen else np.zeros((n,0),dtype=np.uint8)
        freedom.append({'row':row,'allowed_columns':n,'constraint_rank':rank(C),'dimension':n-rank(C)})
    need(sum(z['dimension'] for z in freedom)==360,'exact homogeneous phase-legal freedom')
    def audit_word(W):
        need(W.shape==(35,35) and not np.any(W[:19,19:]),'19/16 phase causality')
        need(rank(W[:19,:19])==19 and rank(W[19:,19:])==16 and rank(W)==35,'invertible physical phases')
        count=0
        for j in ins:
            for r in receivers:
                need(rank(W[np.ix_(outs[r],ins[j])])==8,'actual geometric D section')
                count+=1
        for j in donors:
            for t,r in enumerate(retained):
                U=L[:,8*t:8*t+8]
                need(not np.any(mm(O[j,r],U)),'retained whole fibre isolation')
                need(np.array_equal(mm(W[outs[r]],M[j,r]),np.eye(8,dtype=np.uint8)),'retained oriented readout')
        return count
    sections_pair=audit_word(T^delta); sections_all=audit_word(S)
    need(rank(delta)==1 and not np.any(mm((T^delta)[outs[95]],q)),'rank-one pair repair')
    need(rank(S^T)==6 and np.array_equal(mm(S,np.array(candidate['inverse'],dtype=np.uint8)),np.eye(35,dtype=np.uint8)),'rank-six all-donor word and literal inverse')
    readouts={j:mm(S[outs[95]],mm(P[j],v))[:,0].tolist() for j in donors}
    need(len({tuple(x) for x in readouts.values()})==1 and readouts[61]==candidate['all_donor_readout'],'all eleven actual forced-vector readouts')
    Z=np.hstack([mm(P[j]^P[61],v) for j in donors if j!=61])
    need(rank(Z[:19])==10 and rank(Z)==10,'all-donor contrast dimensions')
    fifth={}; leakage={}
    for j in donors:
        U=null(O[j,95]); need(U.shape==(96,8),'whole frozen fifth isolated subspace')
        C=mm(S[outs[95]],mm(P[j],U)); need(rank(C)==8,'new fifth section on entire isolated subspace')
        fifth[j]=mm(U,inverse(C)); leakage[j]=rank(mm(O[j,95],v))
    need(leakage[0]==1 and leakage[61]==0,'unchanged off-D leakage still prevents a common fifth fibre')
    join=rank(np.hstack([fifth[0],fifth[61]])); need(join>8,'new readouts do not align the whole fifth fibre')
    old_readouts=[mm(T[outs[95]],mm(P[j],v))[:,0].tolist() for j in donors]
    need(len({tuple(x) for x in old_readouts})>1,'unmodified word negative control')
    # This four-dimensional intersection is reconstructed from the actual off-D
    # kernel, independently of the author's saved collision basis.
    U61=null(O[61,95]); rel=null(np.hstack([L,U61])); I=H['basis'](mm(U61,rel[32:]))
    need(I.shape==(96,4) and rank(np.hstack([I,v]))==4,'entire forced four-space')
    contrasts=np.hstack([mm(P[j]^P[61],I) for j in donors if j!=61])
    annihilator=null(contrasts.T).T; common=mm(annihilator,mm(P[61],I))
    need(contrasts.shape==(35,40) and rank(contrasts)==30,'entire forced-space contrast rank')
    need(annihilator.shape==(5,35) and not np.any(mm(annihilator,contrasts)) and rank(annihilator)==5,'complete common-row annihilator')
    need(rank(mm(P[61],I))==4 and rank(common)==2,'strict common response rank loss')
    augmented_rank=rank(np.hstack([contrasts,mm(P[61],I)]))
    need(augmented_rank==32 and augmented_rank-rank(contrasts)==rank(common),'rank-difference common response formula')
    ac=rd(author/'FULL-COLLISION-CERTIFICATE.json.gz'); AI=np.array(ac['forced_space'],dtype=np.uint8)
    need(rank(np.hstack([I,AI]))==4,'independent forced-space agreement')
    # Audit the changed chronological binary word directly on all 210 inputs.
    binary=runpy.run_path(str(BASE/'bit-simultaneous-d1509-s032-independent/check_compiler_delta.py'))
    lift,compile_matrix=binary['lift'],binary['compile_matrix']; dwnew=rd(author/'D-WORD.json.gz')
    need(dwnew['owners']==owners and dwnew['matrix']==candidate['matrix'] and dwnew['inverse']==candidate['inverse'],'compiled word binds actual D candidate')
    ep,lp=dwnew['early_elimination_ADD'],dwnew['late_elimination_ADD']; cross=dwnew['late_cross_from_original_early_cache_ADD']
    E,_=compile_matrix(S[:19,:19]); B,_=compile_matrix(S[19:,19:])
    need(len(ep)==E['ADD_per_direction']==6672 and len(lp)==B['ADD_per_direction']==4732,'independent binary phase bills')
    cache=[1<<i for i in range(114)]; early=cache[:]; late=[1<<(114+i) for i in range(96)]
    for t,s in reversed(ep): early[t]^=early[s]
    for t,s in reversed(lp): late[t]^=late[s]
    for t,s in cross: late[t]^=cache[s]
    need(early+late==lift(S),'chronological word on all 210 columns')
    for n,ops in [(114,ep),(96,lp)]:
        state=[1<<i for i in range(n)]
        for t,s in reversed(ops): state[t]^=state[s]
        for t,s in ops: state[t]^=state[s]
        need(state==[1<<i for i in range(n)],'literal pure phase inverse')
    expected_cross=[(t,s) for t,row in enumerate(lift(S[19:,:19])) for s in range(114) if row>>s&1]
    need(cross==[list(x) for x in expected_cross] and len(cross)==4337,'every original-early-cache cross ADD')
    need(dwnew['cache_labels']==dw['compiler']['cache_labels'] and len(dwnew['cache_labels'])==114,'unchanged stationary early cache owners')
    oe,_=compile_matrix(T[:19,:19]); ob,_=compile_matrix(T[19:,19:])
    old_bill=2*(oe['ADD_per_direction']+ob['ADD_per_direction'])+114+sum(x.bit_count() for x in lift(T[19:,:19]))
    new_bill=2*(len(ep)+len(lp))+114+len(cross)
    prior=rd(BASE/'bit-simultaneous-d1509-s032-independent/compiler-output/RESULT.json')
    total=prior['fullbank_ADD']+8*(new_bill-old_bill)
    need(old_bill==26996 and new_bill==27259 and total==453939712,'exact independently recounted changed D invoice')
    claimed_bill=rd(author/'COMPILER-RESULT.json')
    need(total==claimed_bill['new_fullbank_source_H_D_ADD'] and claimed_bill['fullbank_ADD_delta']==2104,'author incremental bill agreement')
    need(prior['fullbank_INIT']==prior['fullbank_dirty_CLEAR']==279648 and prior['retained_gap6_field_exports']==16,'inherited unchanged source/H allocation')
    broken=S.copy(); row=outs[retained[0]][0]; col=int(np.flatnonzero(M[donors[0],retained[0]][:,0])[0]); broken[row,col]^=1
    need(not np.array_equal(mm(broken[outs[retained[0]]],M[donors[0],retained[0]]),np.eye(8,dtype=np.uint8)),'retained readout mutation control')
    result={'status':'PASS_INDEPENDENT_BOUNDED_COUPLED_D_REPAIR','retained_receivers':retained,'native_donors':donors,'independently_reconstructed_ingress_matrices':len(P),'phase_dimensions':[19,16],'phase_legal_homogeneous_freedom':360,'row_freedom':freedom,'pair_delta_rank':1,'all_donor_delta_rank':6,'geometric_sections_checked_each_word':sections_all,'retained_whole_fibres_checked_each_word':44,'old_pair_mismatch':before.tolist(),'common_vector_readout':readouts[61],'all_donor_contrast_rank_early':rank(Z[:19]),'all_donor_contrast_rank_full':rank(Z),'fifth_vector_off_D_leakage_rank':leakage,'new_fifth_fibre_join_rank_donors_0_61':join,'full_collision_dimension':4,'full_collision_contrast_rank':30,'full_collision_common_row_dimension':5,'full_collision_common_response_rank':2,'compiler':{'early_ADD_per_direction':len(ep),'late_ADD_per_direction':len(lp),'cross_ADD':len(cross),'cache_copy_ADD':114,'old_D_ADD':old_bill,'new_D_ADD':new_bill,'fullbank_delta':8*(new_bill-old_bill),'fullbank_ADD':total,'INIT':279648,'dirty_CLEAR':279648,'gap6_field_exports':16,'all_original_binary_columns':210},'controls':['unmodified D word fails the all-donor vector interface','retained output coefficient mutation fails its oriented readout'],'new_author_executable_imports':False,'complete_fifth_receiver_repair':False,'full_global_invoice':False,'new_kappa':False}
    need(sections_pair==sections_all==144,'144 geometric sections per candidate')
    wr(args.out/'RESULT.json',result); wr(args.out/'RECONSTRUCTED-INGRESS.json.gz',{j:A.tolist() for j,A in P.items()})
    wr(args.out/'FULL-COLLISION-CERTIFICATE.json.gz',{'forced_space':I.tolist(),'contrasts':contrasts.tolist(),'annihilator':annihilator.tolist(),'common_response':common.tolist()})
    print(json.dumps({k:v for k,v in result.items() if k!='row_freedom'},sort_keys=True),flush=True)

if __name__=='__main__': main()
