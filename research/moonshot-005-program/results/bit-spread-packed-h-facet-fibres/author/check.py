#!/usr/bin/env python3
"""Price and verify the simultaneous original-coordinate terminal word for all 31 packed H centres."""
import argparse,gzip,hashlib,importlib.util,json,sys
from functools import lru_cache
from collections import Counter
from pathlib import Path
import numpy as np
from source import prepare
def one(h,k,i):
    c,maps,grp=pack[h,k];j=c.donors[0];off=sorted(set(N.views[j,i])-{h})
    pos=[t for t,d in enumerate(c.ports)if N.D[d]<=N.adj[i]];ds=[c.ports[t]for t in pos]
    V=c.V[pos]
    L=inverse(np.vstack([a.ops.matmul(V[:,:k],maps[j][h])]+[maps[j][t]for t in off]))[:,:k]
    for j1 in c.donors:
        q=c.ix[j1];assert np.array_equal(a.ops.matmul(a.ops.matmul(V[:,q*k:(q+1)*k],maps[j1][h]),L),np.eye(k,dtype=np.uint8))
    domain=np.kron(np.eye(2,dtype=np.uint8),L)
    atten=a.phase[str(h)];seq=[('X',t)for t in range(atten['early'])]+[('Y',t)for t in range(atten['late'])];assert len(seq)==2
    fac=a.right(i);Z=[];w=32*k;start=0 if k==3 else 96
    for ph,t in seq:
        for d in ds:
            u=a.left_flags[h,d,ph][t];M,owners=a.middle_matrix(d);cidx=owners.index(u);rs=[p for p,v in enumerate(owners)if v in fac]
            assert len(rs)==8
            R=np.stack([fac[owners[r]][start:start+w]for r in rs]).T
            Z.append(a.ops.matmul(R,M[rs,cidx,None])[:,0])
    return domain,np.stack(Z).T
def main(args):
    if args.compiler:
        p=importlib.util.spec_from_file_location('price_compiler',args.compiler);comp=importlib.util.module_from_spec(p);p.loader.exec_module(comp)
    else:comp=None
    hs=sorted(set(v[0]for v in pack));assert len(hs)==31
    panels=hashlib.sha256();wordinfo={};counts=Counter();pairs=Counter();sizes=Counter();price=0
    for i in range(111):
        visible=[h for h in hs if i in pack[h,3][0].receivers]
        if not visible:continue
        assert i!=80;sizes[len(visible)]+=1
        for k in (3,12):
            Ls=[];Zs=[]
            for h in visible:
                L,Z=one(h,k,i);Ls.append(L);Zs.append(Z)
                if k==3:
                    counts[h]+=1
                    for j in pack[h,k][0].donors:
                        assert j!=10 and i in N.adj[j];pairs[i,j]+=1
                panels.update(bytes([i]));panels.update(h.to_bytes(2,'little'));panels.update(bytes([k]));panels.update(L.tobytes());panels.update(Z.tobytes())
            L=np.hstack(Ls);Z=np.hstack(Zs);t=2*k*len(visible)
            assert rank_fast(L)==rank_fast(Z)==t
            O=a.ops.matmul(extend_rows(L.T),inverse(extend_rows(Z.T)))
            assert np.array_equal(a.ops.matmul(O,Z),L) and rank_fast(O)==32*k
            cost=price_map(comp,O)+18*shuffle(16*k);price+=cost
            wordinfo[f'{i}/{k}']={'columns':t,'controls':len(visible),'matrix_sha256':hashlib.sha256(O.tobytes()).hexdigest(),'binary_ADD_each_direction':cost}
        print('terminal',i,'charts',len(visible),flush=True)
    assert sum(counts.values())==1041 and sum(pairs.values())==3123
    result={'native_centres':hs,'native_chart_receiver_fibres':sum(counts.values()),'three_donor_endpoint_instances':sum(pairs.values()),
            'distinct_native_ordered_donor_receiver_pairs':len(pairs),'native_receivers':sum(sizes.values()),
            'chart_degree_histogram':dict(sizes),'native_chart_counts':dict(counts),'per_native_pair_instantiated_H_count':{f'{i}/{j}':c for (i,j),c in pairs.items()},
            'coordinates_per_native_donor_receiver_H':240,'total_native_original_field_directions':240*sum(pairs.values()),
            'terminal_gauges':wordinfo,'price_mode':'exact native compiler' if comp else 'upper bound','terminal_ADD_forward':price,'ground_preload_inverse_ADD':price,
            'extra_MOVE_INIT_DIRTY_CLEAR':0,'native_panel_stream_sha256':panels.hexdigest(),'raw_input_source_coordinates':'16s+8h+copy','physical_RS_terminal_order':'copy,channel,degree prior to paid reorder',
            'complete_word_scope':'all 31 named H-only input fibres for every native receiver and all three incident original donors; remaining directions and global return unresolved'}
    args.out.mkdir(exist_ok=True,parents=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('realised',sum(counts.values()),sum(pairs.values()),'distinct pairs',len(pairs),'terminal ADD each direction',price,flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('repo','h-author','isolated-author','middle-author','k-words','d-charts','packing-review','field-review','parameters','out'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--library',type=Path);p.add_argument('--inverse-library',type=Path);p.add_argument('--compiler',type=Path)
    args=p.parse_args();sys.path.insert(0,str(args.h_author));sys.path.insert(0,str(args.isolated_author));sys.path.insert(0,str(args.middle_author))
    from transfer import Atlas,rank_fast
    from body import inverse
    from slices import extend_rows
    from verify import price_map,shuffle
    if args.inverse_library:
        from fast import Arithmetic
        fast=Arithmetic(args.inverse_library.resolve());inverse=fast.inverse
    a=Atlas(args.repo,args.k_words,args.d_charts,args.library)
    require_pin='972939d6c9937d1c18cf90f69399112bf2c9c95eab1b194186b164a2331f5d6c'
    assert hashlib.sha256(args.parameters.read_bytes()).hexdigest()==require_pin
    N,pack,groups=prepare(args.repo,args.packing_review,args.field_review,args.parameters)
    main(args)
