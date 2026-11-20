#!/usr/bin/env python3
"""Verify full terminal demand on every attached donor and every receiver of 42 native D charts."""
import argparse,gzip,hashlib,importlib.util,json,sys
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
import numpy as np

def null(A):
    rr,pi=row_reduce(A);n=A.shape[1];free=sorted(set(range(n))-set(pi))
    out=np.zeros((len(free),n),dtype=np.uint8)
    for k,t in enumerate(free):
        out[k,t]=1;out[k,pi]=rr[:,t]
    return out
allleft={};allright={}
def left(j):
    if j not in allleft:allleft[j]=spec.left(j)
    return allleft[j]
def right(i):
    if i not in allright:allright[i]=a.right(i)
    return allright[i]
def part(i,j,d):
    ds,inv=whole(i,j,d in a.marked)
    q=ds.index(d)
    return inv[:,8*q:8*q+8].T
@lru_cache(maxsize=1800)
def whole(i,j,small):
    n=96 if small else 384;start=0 if small else 96
    ds=[d for d in range(len(a.D))if j in a.D[d]and i in a.D[a.dual[d]]and (d in a.marked)==small]
    src=left(j);m=[]
    for d in ds:
        ids=a.middle[d,'X']+a.middle[d,'Y'];m.extend(src[t][start:start+n] for t in ids if t in src)
    z=np.stack(m);w=inverse(z)
    if (i+j)%39==0:assert np.array_equal(a.ops.matmul(z,w),np.eye(n,dtype=np.uint8))
    return ds,w
@lru_cache(maxsize=112)
def base_terminal(i):
    if i not in a.orth[0] or i==80:return None
    left0=left(0);right0=right(i);origin=np.zeros((480,480),dtype=np.uint8)
    for d in range(len(a.D)):
        if 0 not in a.D[d]or i not in a.D[a.dual[d]]:continue
        M,cols,rows=S.members(d);ids=a.middle[d,'X']+a.middle[d,'Y'];C=M[np.ix_(rows[i],cols[0])]
        L=np.stack([left0[ids[p]]for p in cols[0]]);R=np.stack([right0[ids[p]]for p in rows[i]]).T
        origin^=a.ops.matmul(a.ops.matmul(R,C),L)
    assert not np.any(origin[:96,96:])and not np.any(origin[96:,:96])
    return inverse(origin[:96,:96]),inverse(origin[96:,96:])
def section(i,j,d):
    M,cols,rows=S.members(d);ids=a.middle[d,'X']+a.middle[d,'Y'];small=d in a.marked;n=96 if small else 384
    shift=0 if small else 96
    R=np.stack([right(i)[ids[u]][shift:shift+n]for u in rows[i]]).T
    C=M[np.ix_(rows[i],cols[j])];V=part(i,j,d)
    U=R if varied_terminal(i)is None else a.ops.matmul(varied_terminal(i)[0 if small else 1],R)
    Q=a.ops.matmul(V.T,inverse(C))
    return U.T,Q.T
@lru_cache(maxsize=112)
def varied_terminal(i):
    dims=[96,384];keep=[[],[]];rng=np.random.default_rng(8701+i)
    anchor=base_terminal(i)
    if a.H[263]<=a.orth[i]:
        for k,n,idx in [(3,96,0),(12,384,1)]:
            planes=[h for h in a.ks[0]if a.H[h]<=a.orth[i]and h!=263]
            only=np.vstack([spec.quotient(0,h,k)for h in planes])
            K=np.kron(np.eye(2,dtype=np.uint8),null(only))
            assert K.shape==(2*k,n)
            keep[idx].extend(K)
        if i==5:keep[0].extend(np.array(wo['V'],dtype=np.uint8))
    out=[]
    for idx,n in enumerate(dims):
        if keep[idx]:
            from slices import row_reduce
            basis=row_reduce(np.array(keep[idx],dtype=np.uint8))[0]
            E=extend_rows(basis);e=len(basis)
        else:E=np.eye(n,dtype=np.uint8);e=0
        for tries in range(64):
            m=rng.integers(0,64,(n,n),dtype=np.uint8);m[:,:e]=0;m[:e,:e]=np.eye(e,dtype=np.uint8)
            try:inverse(m);break
            except ValueError:pass
        else:raise ValueError('draw singular')
        O=a.ops.matmul(a.ops.matmul(E,m),inverse(E)) if e else m
        if e:assert np.array_equal(a.ops.matmul(O,basis.T),basis.T)
        if anchor is not None:O=a.ops.matmul(O,anchor[idx])
        out.append(O)
    return tuple(out)

def arrival(i,j,V):
    total=np.zeros((480,V.shape[1]),dtype=np.uint8);p=left(j);r=right(i)
    for d in range(len(a.D)):
        if j not in a.D[d]or i not in a.D[a.dual[d]]:continue
        M,cols,rows=S.members(d);ids=a.middle[d,'X']+a.middle[d,'Y']
        image=a.ops.matmul(np.stack([p[ids[t]]for t in cols[j]]),V)
        if not image.any():continue
        C=M[np.ix_(rows[i],cols[j])];R=np.stack([r[ids[t]]for t in rows[i]]).T
        total^=a.ops.matmul(R,a.ops.matmul(C,image))
    O=varied_terminal(i)
    return np.vstack([a.ops.matmul(O[0],total[:96]),a.ops.matmul(O[1],total[96:])])

def verify(args):
    labels=json.loads(args.cuts.read_text());complete=labels['complete_charts'];native=set(range(111))
    assert len(complete)==len(set(complete))==42 and labels['partial_chart_receivers']==[[120,5]]
    assert sum(d in a.marked for d in complete)==6
    requests=defaultdict(lambda:[[],[]]);all_recs=set();exposures={};witness=hashlib.sha256();pair_count=Counter()
    sheets=[(d,sorted(a.D[a.dual[d]]&native))for d in complete]+[(120,[5])]
    for d,rs in sheets:
        js=sorted(a.D[d]&native);assert 10 not in js and 80 not in rs
        if d!=120:assert not set(js)&set(spec.donors)
        n=96 if d in a.marked else 384;exposures[d]=[len(js),len(rs)]
        for i in rs:
            all_recs.add(i)
            for j in js:
                U,Q=section(i,j,d);pair_count[i,j]+=1
                if j in spec.donors:assert np.array_equal(U,Q)
                else:requests[j,n][0].append(U);requests[j,n][1].append(Q)
                witness.update(bytes([i,j]));witness.update(d.to_bytes(2,'little'));witness.update(U.tobytes());witness.update(Q.tobytes())
        print('verified native sections',d,len(rs)*len(js),flush=True)
    hreceivers=sorted(i for i in native if a.H[263]<=a.orth[i]);assert len(hreceivers)==33
    for i in hreceivers:
        all_recs.add(i);ps=[]
        for k in (3,12):
            planes=[h for h in a.ks[0]if a.H[h]<=a.orth[i]and h!=263]
            K=np.kron(np.eye(2,dtype=np.uint8),null(np.vstack([spec.quotient(0,h,k)for h in planes])))
            x=np.zeros((480,2*k),dtype=np.uint8);lo=0 if k==3 else 96;x[lo:lo+32*k]=K.T;ps.append(x)
        V=np.hstack(ps);assert V.shape==(480,30)
        for j in spec.donors:assert np.array_equal(arrival(i,j,V),V)
    comp=None
    if args.compiler:
        mod=importlib.util.spec_from_file_location('binary_owner_compiler',args.compiler)
        comp=importlib.util.module_from_spec(mod);mod.loader.exec_module(comp)
    diagrams={};cost_in={};cost_out={};osh={}
    for i in sorted(all_recs):
        osh[i]=[hashlib.sha256(q.tobytes()).hexdigest()for q in varied_terminal(i)]
        cost_out[i]=sum(price_map(comp,Q)+18*shuffle(len(Q)//2)for Q in varied_terminal(i))
    for (j,n),(U,Q)in sorted(requests.items()):
        G,r=common_gauge(a,U,Q);key=f'{j}/{n}'
        diagrams[key]={'hash':hashlib.sha256(G.tobytes()).hexdigest(),'native_requests':len(U),'body_span':r}
        cost_in[key]=price_map(comp,G)+18*shuffle(n//2)
    total=sum(n*m for n,m in exposures.values())
    result={'whole_native_D':complete,'whole_native_D_count':len(complete),'whole_native_sections':total-12,'additional_D120_sections':12,'total_native_sections':total,
            'chart_native_donors_receivers':exposures,'unique_native_ordered_pairs':len(pair_count),'eightfold_directions_summed_over_sections':total*64,
            'H263_native_receivers':hreceivers,'H263_verified_full_endpoint_maps':3*len(hreceivers),'H263_endpoint_dimension_native_fields':240,
            'source_gauges':diagrams,'receiver_gauges':osh,'actual_equation_stream_sha256':witness.hexdigest(),
            'price_mode':'exact' if comp else 'binary_gaussian_upper_bound','input_gauge_ADD_per_direction':cost_in,'output_gauge_ADD_per_direction':cost_out,
            'native_source_forward_ADD':279328656+sum(cost_in.values()),'native_source_inverse_ADD':178690440+sum(cost_in.values()),
            'terminal_gauge_ADD_forward':sum(cost_out.values()),'ground_preload_inverse_ADD':sum(cost_out.values()),
            'gauge_extra_MOVE_INIT_DIRTY_CLEAR':0,'baseline_source_INIT_DIRTY_CLEAR_each':2540160}
    assert result['whole_native_sections']==4610
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'WHOLE-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print('complete native charts',len(complete),'proper sections',total,'H263 full terminal checks',3*len(hreceivers),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('repo','h-author','isolated-author','k-words','d-charts','source','repair','out'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--cuts',type=Path,default=Path(__file__).parent/'output/COMPLETE-CHARTS.json')
    p.add_argument('--library',type=Path);p.add_argument('--inverse-library',type=Path);p.add_argument('--compiler',type=Path)
    args=p.parse_args();sys.path.insert(0,str(args.h_author));sys.path.insert(0,str(args.isolated_author))
    from body import SpecialSource,inverse
    from transfer import Atlas
    import slices
    from slices import Slices,matched,common_gauge,extend_rows,row_reduce
    from verify import price_map,shuffle
    if args.inverse_library:
        from fast import Arithmetic
        fs=Arithmetic(args.inverse_library.resolve());inverse=fs.inverse;slices.inverse=inverse
    a=Atlas(args.repo,args.k_words,args.d_charts,args.library)
    raw=gzip.decompress(args.repair.read_bytes());assert hashlib.sha256(raw).hexdigest()=='f185c1d220f258b88159f50bcafe47c1b0fde53439320eb5d9313d06e74bc970'
    wo=json.loads(raw);spec=SpecialSource(a,args.repo,args.source,wo['frames']);S=Slices(a,spec,wo,{})
    verify(args)
