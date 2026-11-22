#!/usr/bin/env python3
"""Independent alternate-receiver necessary screen; no existence conclusion.
@CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import argparse, gzip, hashlib, importlib.util, itertools, json
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('independent_screen_gf', HERE.parent/'check.py')
a = importlib.util.module_from_spec(spec); spec.loader.exec_module(a)

def basis(A):
    return A[:, a.rref(A)[1]]

def meet(A, B):
    N = a.null(np.hstack([A, B]))
    return basis(a.mm(A, N[:A.shape[1]]))

def same(A, B):
    return a.rank(A) == a.rank(B) == a.rank(np.hstack([A, B]))

def main(repo, out):
    base = repo/'research/moonshot-005-program/results'
    four = base/'bit-simultaneous-d1509-s032/output'
    paths = [base/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz',
             four/'SOURCES.json.gz', four/'H-PHYSICAL.json.gz', four/'PROPER.json.gz',
             four/'D-WORD.json.gz', four/'CONSTRAINED-GAUGES.json.gz', four/'READOUTS.json.gz',
             base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
             base/'bit-simultaneous-d1509-s032-independent/output/H-FIBRES.json.gz',
             base/'bit-coupled-fifth-s033/other-receivers/output/RESULT.json',
             base/'bit-coupled-fifth-s033/other-receivers/output/CERTIFICATE.json.gz',
             HERE.parent/'check.py']
    z, source, hp, proper, dw, gauges, readouts, layout, oldhf, author, authorcert = map(a.read, paths[:-1])
    L = np.array(z['common_frames'], dtype=np.uint8)
    R, J = z['retained_receivers'], z['donors']
    T = np.array(dw['matrix'], dtype=np.uint8)
    roots = layout['root_table']; planes = list(map(set, layout['A2'])); charts = list(map(set, layout['D4']))
    adj = [{j for j, y in enumerate(roots) if j != r and sum(x*v for x,v in zip(roots[r],y)) == 0}
           for r in range(len(roots))]
    targets = [r for r in range(111) if charts[1509] <= adj[r] and r not in R]
    a.need(targets == author['fifth_candidates'] == [52,54,74,85,87,95,98], 'all native fifth candidates')
    targets += [6]
    prot = list(range(48))+list(range(240,288)); local = [0,1,2,15,16,17]
    F = {(j,int(h)):np.array(f,dtype=np.uint8)[:,prot] for j in J for h,f in source['paired_maps'][str(j)].items()}
    parents = {j:sorted(h for jj,h in F if jj==j and planes[h] <= charts[1509]) for j in J}
    a.need(all(len(v)==4 for v in parents.values()), 'four actual D parents per donor')
    Hby = {tuple(v[:3]):int(h) for h,p in hp.items() for name in ['X_owners','Y_owners'] for v in p[name]}
    # Reconstruct every native retained H fibre from the literal old source maps.
    hf = {}; hcount = 0
    for j in J:
        hf[j] = []
        for label, expected in oldhf.get(str(j),{}).items():
            centre, r = map(int,label.split('/'))
            if r >= 111: continue
            hs = sorted(h for jj,h in F if jj==j and planes[h] <= adj[r])
            A = np.vstack([F[j,h][local] for h in hs])
            E = np.zeros((96,6),dtype=np.uint8)
            E[6*hs.index(centre):6*hs.index(centre)+6] = np.eye(6,dtype=np.uint8)
            U = a.mm(a.inverse(A), E)
            a.need(np.array_equal(U,np.array(expected,dtype=np.uint8)), 'literal native H fibre')
            hf[j].append((r,U)); hcount += 1
    C = {}
    for j,h in F:
        cols = [U for r,U in hf[j] if planes[h] <= adj[r]]
        C[j,h] = basis(np.hstack(cols)) if cols else np.zeros((96,0),dtype=np.uint8)
    # Obtain fixed-on-all-four-parents subspace geometrically, then compare rectangle description.
    fixed = {}
    for j in J:
        P = L
        for h in parents[j]: P = meet(P,C[j,h])
        special = sorted(set(z['D_inputs'][str(j)]) & {4,5,7,8})
        E = np.zeros((32,4*len(special)),dtype=np.uint8)
        for t,r in enumerate(R):
            E[8*t:8*t+8,len(special)*t:len(special)*(t+1)] = T[np.ix_(z['D_outputs'][str(r)],special)]
        a.need(same(P,a.mm(L,E)), 'all-parent fixed subspace versus rectangle')
        fixed[j] = P
    # Raw full-thirty-input physical H maps, with literal route labels.
    full = {}
    for j,h in F:
        p = hp[str(h)]; xs,ys = p['X_owners'],p['Y_owners']
        Q = np.array(source['frames'][f'{j}/{h}'],dtype=np.uint8)
        ix = [i for i,x in enumerate(xs) if x[1]==j]
        iy = [i for i,x in enumerate(ys) if x[6]==j]
        a.need(len(ix)+len(iy)==30 and a.rank(Q)==30, 'full source frame')
        XE=np.zeros((len(xs),30),dtype=np.uint8); YL=np.zeros((len(ys),30),dtype=np.uint8)
        XE[ix]=Q[:len(ix)]; YL[iy]=Q[len(ix):]
        E=np.array(p['early'],dtype=np.uint8).reshape(len(xs),len(xs))
        B=np.array(p['late'],dtype=np.uint8).reshape(len(ys),len(ys))
        X=np.array(p['cross'],dtype=np.uint8).reshape(len(ys),len(xs))
        raw=np.vstack([a.mm(E,XE),a.mm(X,XE)^a.mm(B,YL)])
        full[j,h]=(raw,xs+ys,[tuple(v[:3]) for v in xs+ys])
    section_cache={}
    def section(j,h,r):
        key=(j,h,r)
        if key not in section_cache:
            raw,owners,labels=full[j,h]
            ix=[i for i,x in enumerate(owners) if charts[x[4]] <= adj[r]]
            B=raw[ix]
            a.need(B.shape==(30,30) and a.rank(B)==30,'invertible full H section')
            section_cache[key]=(B,[labels[i] for i in ix])
        return section_cache[key]
    # Full retained isolation gives unique source restrictions for arbitrary changed full tuples.
    retained_sections=0
    for j in J:
        inputs=[tuple(dw['owners'][i][:3]) for i in z['D_inputs'][str(j)]]
        for h in parents[j]:
            for t,r in enumerate(R):
                B,labels=section(j,h,r)
                E=np.zeros((30,8),dtype=np.uint8)
                for i,label in enumerate(labels):
                    if label in inputs:E[i,inputs.index(label)]=1
                S=T[np.ix_(z['D_outputs'][str(r)],z['D_inputs'][str(j)])]
                a.need(np.array_equal(a.mm(a.mm(a.mm(B,F[j,h]),L[:,8*t:8*t+8]),S),E),
                       'full retained source identity')
                retained_sections+=1
    cache={}; partitions=[]
    for target in targets:
        for j in J:
            item=proper[str(j)][str(target)]; labels=list(map(tuple,item['labels']))
            A=a.mm(np.array(item['matrix'],dtype=np.uint8),np.array(gauges['gauges'][str(j)],dtype=np.uint8))
            inputs=[tuple(dw['owners'][q][:3]) for q in z['D_inputs'][str(j)]]
            oldoff=[i for i,l in enumerate(labels) if Hby[l] in parents[j] and l not in inputs]
            rows=[]; wholelabels=[]
            for h in parents[j]:
                B,ls=section(j,h,target); rows.append(a.mm(B,F[j,h])); wholelabels+=ls
            whole=np.vstack(rows); off=[i for i,l in enumerate(wholelabels) if l not in inputs]
            a.need(len(wholelabels)==120 and len(set(wholelabels))==120 and len(off)==112,
                   '120 actual parent outputs minus eight D inputs')
            for i in oldoff:
                a.need(np.array_equal(A[i],whole[wholelabels.index(labels[i])]), 'physical proper row')
            M=a.mm(whole[off],L); Mp=a.mm(A[oldoff],L)
            a.need(len(oldoff)==16 and same(M.T,Mp.T), 'full 112 and protected16 have identical row spaces on L')
            rhs=np.zeros((96,8),dtype=np.uint8)
            sec=np.array(readouts[str(j)][str(target)]['section'],dtype=np.uint8)
            si=a.inverse(sec)
            for k,label in enumerate(inputs):rhs[labels.index(label)]=si[k]
            U=a.mm(a.inverse(A),rhs)
            a.need(not np.any(a.mm(A[[i for i,l in enumerate(labels) if l not in inputs]],U)), 'old whole fibre')
            cache[j,target]=(M,U)
            partitions.append(dict(donor=j,target=target,protected_off_rows=16,full_off_rows=112,
                                   full_rank=a.rank(M),same_restricted_row_space=True))
    certificates={(v['target'],v['anchor']):v for v in authorcert}
    records=[]; joined={}; gate_count=0
    for target in targets:
        allK=[]
        for anchor in [0,45,61,62,100]:
            K=meet(cache[anchor,target][1],fixed[anchor]); initial=K.shape[1]
            for j,h in F:
                if j != anchor or not planes[h] <= adj[target]:continue
                pieces=[C[j,h]]
                if h not in parents[j]:
                    for t,r in enumerate(R):
                        if planes[h] <= adj[r]:
                            B,ls=section(j,h,r)
                            a.need(not np.any(a.mm(a.mm(B,F[j,h]),L[:,8*t:8*t+8])), 'whole zero-D source restriction')
                            pieces.append(L[:,8*t:8*t+8])
                K=meet(K,basis(np.hstack(pieces)))
            record=dict(target=target,anchor=anchor,forced_dimension=K.shape[1],initial_dimension=initial)
            authorrec=next(v for v in author['records'] if v['target']==target and v['anchor']==anchor)
            a.need(record['forced_dimension']==authorrec['forced_dimension'] and initial==authorrec['initial_parent_fixed_fibre_dimension'], 'forced dimensions')
            if not K.shape[1]:records.append(record);continue
            # Check every actual old target output, including the complement
            # of the protected 96-row presentation, before calling K forced.
            input_labels={tuple(dw['owners'][q][:3]) for q in z['D_inputs'][str(anchor)]}
            target_hs=[h for j,h in F if j==anchor and planes[h] <= adj[target]]
            a.need(len(target_hs)==16,'all target-visible source tuples')
            for h in target_hs:
                B,labels=section(anchor,h,target)
                rows=[i for i,label in enumerate(labels) if label not in input_labels]
                a.need(not np.any(a.mm(a.mm(B[rows],F[anchor,h]),K)), 'all actual off-target outputs vanish on forced K')
            allK.append(K); W=a.solve(L,K); cert=certificates[target,anchor]
            a.need(same(K,np.array(cert['K'],dtype=np.uint8)), 'forced space itself')
            active=[t for t in range(4) if np.any(W[8*t:8*t+8])]
            a.need([R[t] for t in active]==authorrec['active_receivers'], 'active retained blocks')
            indices=sum([list(range(8*t,8*t+8)) for t in active],[])
            bad=[]; profiles=[]
            for j in J:
                M=cache[j,target][0][:,indices]; N=a.null(M)
                for size in range(1,len(active)+1):
                    for sub in itertools.combinations(range(len(active)),size):
                        ni=sum([list(range(8*t,8*t+8)) for t in sub],[])
                        wi=sum([list(range(8*active[t],8*active[t]+8)) for t in sub],[])
                        required,available=a.rank(W[wi]),a.rank(N[ni]); gate_count+=1
                        cs=next(v for v in cert['donor_gates'] if v['donor']==j)
                        cp=next(v for v in cs['projections'] if v['receiver_blocks']==[R[active[t]] for t in sub])
                        a.need((required,available)==(cp['required_rank'],cp['available_rank']), 'independent block projection ranks')
                        profiles.append(dict(donor=j,blocks=[R[active[t]] for t in sub],required=required,available=available))
                        if required>available:bad.append(j)
            a.need(sorted(set(bad))==authorrec['blocked_donors'], 'exact rejected donors')
            record.update(active_receivers=[R[t] for t in active],blocked_donors=sorted(set(bad)),profiles=profiles)
            records.append(record)
        joined[target]=a.rank(np.hstack(allK)) if allK else 0
    a.need(all(joined[t]==2 for t in [52,54,74,85,87,98]) and joined[95]==4,'joined anchor dimensions')
    a.need(all(not v.get('blocked_donors') for v in records if v['target']!=95), 'six targets and retained positive control pass necessary screen')
    a.need(next(v for v in records if v['target']==95 and v['anchor']==61)['blocked_donors']==[32,35,38,45,68,69,90,100], 'known95 negative control')
    # A one-entry kernel corruption must fail an actual annihilation identity.
    controlM=cache[32,95][0][:,16:32]; controlN=a.null(controlM)
    corrupt=controlN.copy(); col=int(np.flatnonzero(np.any(controlM,axis=0))[0]);corrupt[col,0]^=1
    a.need(not np.any(a.mm(controlM,controlN)) and np.any(a.mm(controlM,corrupt)), 'kernel corruption control')
    result=dict(status='PASS_INDEPENDENT_ALTERNATIVE_RECEIVER_NECESSARY_SCREEN',
                targets=targets[:-1],forced_joined_dimensions=joined,anchor_cases=len(records),
                checked_native_H_fibres=hcount,full_retained_H_sections=retained_sections,
                full_H_sections_total=len(section_cache),actual_parent_output_partitions=len(partitions),
                block_subset_tests=gate_count,all_actual112_off_parent_rows_checked=True,
                passes_are_existence_claims=False,new_complete_kappa=False,
                six_not_excluded=[52,54,74,85,87,98],negative_control=95,positive_control=6)
    pins={str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    expected=HERE/'SOURCE-PINS.json'
    if expected.exists():a.need(pins==a.read(expected),'source pins')
    out.mkdir(parents=True,exist_ok=True)
    for name,data in [('RESULT',result),('CERTIFICATE',dict(records=records,partitions=partitions)),('SOURCE-PINS',pins)]:
        (out/(name+'.json')).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
