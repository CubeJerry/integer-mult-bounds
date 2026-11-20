#!/usr/bin/env python3
"""Check the literal source stars and D120 word on actual H/D owners."""
from __future__ import annotations
import argparse
from collections import defaultdict
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
import numpy as np


def require(condition, message):
    if not condition:
        raise ValueError(message)


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def array(rows):
    result=np.array(rows,dtype=np.uint8)
    require(np.all(result<64),'all coefficients in GF64')
    return result


def doubled(A):
    return np.kron(np.eye(2,dtype=np.uint8),A)


def extend(rows,width,atlas):
    result=list(rows)
    require(atlas.rank(np.array(result))==len(result),'independent pivot rows')
    added=[]
    for unit in np.eye(width,dtype=np.uint8):
        if len(result)==width:
            break
        trial=np.array(result+[unit])
        if atlas.rank(trial)>len(result):
            result.append(unit)
            added.append(unit)
    require(len(result)==width,'complete local physical word')
    return added


def physical_D(atlas,routes,W,hs,ks,compiler):
    d=120
    actual=[r for r in routes if r[4]==d]
    def layout(kind,index):
        grouped=defaultdict(list)
        for row in actual:
            if row[0]==kind:
                grouped[row[index]].append((row[1],row[2]))
        slots={}
        for key in sorted(grouped,key=lambda x: -1 if x is None else x):
            for t,owner in enumerate(sorted(grouped[key])):
                slots[key,t]=owner
        return slots
    EI,LI=layout('X',3),layout('Y',3)
    EO,LO=layout('X',5),layout('Y',5)
    ne,nl=len(EI),len(LI)
    require([ne,nl,len(EO),len(LO)]==[19,17,19,17],'true D phase counts')
    require([h for h in hs if (h,1) in EI]==[17,263,388],'true fully early H inputs')
    require([q for q in ks if (q,0) not in EO]==[601],'true fully late K exit')
    require(all((h,0) in EI and atlas.planes[h]<=atlas.charts[d] for h in hs),'first proper lane available early')
    inputs=sorted(EI.values())+sorted(LI.values())
    def ix(group,key,wave):
        return (inputs[:ne] if wave==0 else inputs[ne:]).index(group[key])+(ne if wave else 0)
    outgoing=sorted(EO.values())+sorted(LO.values())
    def ox(group,key,wave):
        return (outgoing[:ne] if wave==0 else outgoing[ne:]).index(group[key])+(ne if wave else 0)
    require(inputs==outgoing and len(set(inputs[:ne]))==ne and len(set(inputs[ne:]))==nl,'true phase owner sets')
    M=np.zeros((ne+nl,ne+nl),dtype=np.uint8)
    cols={};rows={}
    for h in hs:
        cols[h,0]=ix(EI,(h,0),0)
        cols[h,1]=ix(EI,(h,1),0) if (h,1) in EI else ix(LI,(h,0),1)
    for q in ks:
        rows[q,0]=ox(EO,(q,0),0) if (q,0) in EO else ox(LO,(q,0),1)
        rows[q,1]=ox(LO,(q,1),1) if (q,1) in LO else ox(LO,(q,0),1)
    for lane in range(2):
        M[np.ix_([rows[q,lane] for q in ks],[cols[h,lane] for h in hs])]=W
    hub=[ox(EO,(None,t),0) for t in range(4)]
    kept=[v for v in range(ne) if v not in hub]
    M[hub,:ne]=extend(M[kept,:ne],ne,atlas)
    ground=[ix(LI,(None,t),1) for t in range(4)]
    kept=[v for v in range(ne,ne+nl) if v not in ground]
    M[ne:,ground]=np.array(extend(M[ne:,kept].T,nl,atlas)).T
    require(not np.any(M[:ne,ne:]) and atlas.rank(M[:ne,:ne])==ne and atlas.rank(M[ne:,ne:])==nl,'causal invertible physical D')
    cross=M[ne:,:ne]
    saved=[q for q in range(ne) if np.any(cross[:,q])]
    binary_cross=compiler.bit_rows(cross.tolist())
    addE=len(compiler.compile_binary(compiler.bit_rows(M[:ne,:ne].tolist())))
    addL=len(compiler.compile_binary(compiler.bit_rows(M[ne:,ne:].tolist())))
    cross_add=sum(int.bit_count(x) for x in binary_cross)
    cache=6*len(saved)
    receipt={'true_early_fields':ne,'true_late_fields':nl,'coupled_source_fields_per_copy':cache//6,
             'forward_early_ADD_per_copy':addE,'forward_late_diagonal_ADD_per_copy':addL,
             'forward_cross_ADD_per_copy':cross_add,'copies':8,'INIT':8*cache,'dirty_CLEAR':8*cache,
             'forward_throughput_ADD':8*(addE+addL+cross_add+cache),'paid_pure_early_inverse_ADD':8*addE,
             'forward_plus_reserved_early_inverse_ADD':8*(2*addE+addL+cross_add+cache)}
    return M,cols,rows,receipt


def inspect_sources(atlas,f,stars,U,M,cols,rows,hs,ks,receivers,keep_h263):
    roots=sorted(atlas.charts[120]&atlas.native)
    native_views=sorted(i for i in atlas.native if atlas.charts[120]<=atlas.adj[i])
    require(roots==sorted(stars) and len(roots)==12 and len(native_views)==11,'actual D incidence')
    locals_132=0
    for i in native_views:
        outputs=[rows[q,b] for b in range(2) for q in ks if i in atlas.planes[q]]
        for j in roots:
            inputs=[cols[h,b] for b in range(2) for h in hs if j in atlas.planes[h]]
            require(len(inputs)==len(outputs)==8 and atlas.rank(M[np.ix_(outputs,inputs)])==8,'all true proper D minors')
            locals_132+=1
    restricted={};common_full={};proper_views=0;single_views=0;unrestricted_full=0;negative=0
    plane_ports={h:[d for d in sorted(atlas.marked) if atlas.planes[h]<=atlas.charts[d]] for j in roots for h in atlas.by_donor[j]}
    for j in roots:
        entry=stars[j];F={int(h):array(A) for h,A in entry['F'].items()}
        P={int(h):array(A) for h,A in entry['P'].items()};Q={int(h):array(A) for h,A in entry['Q'].items()}
        require(set(F)==set(P)==set(atlas.by_donor[j]),'all actual 28 source planes')
        X={};early=[]
        for h,src in F.items():
            grade=atlas.quota[j,h]//15
            require(src.shape==(3,48) and P[h].shape==(6,6) and atlas.rank(P[h])==6,'ordinary raw quotient frame')
            X[h]=atlas.mm(P[h],doubled(src))
            if grade==3:
                require(Q[h].shape==(3,96),'singleton extra genuine early inputs')
                X[h]=np.vstack([X[h],Q[h]])
            early.append(X[h][:3*grade])
        E=np.vstack(early)
        require(E.shape==(96,96) and atlas.rank(E)==96,'genuine early original-coordinate source basis')
        for i in sorted(atlas.adj[j]&atlas.native):
            visible=[h for h in F if atlas.planes[h]<=atlas.adj[i]]
            require(len(visible)==16 and atlas.rank(np.vstack([F[h] for h in visible]))==48,'all scalar ordinary native source cuts')
            physical=[];outside=[];drecord=np.zeros((36,96),dtype=np.uint8)
            for h in visible:
                ports=plane_ports[h];seen=[d for d in ports if atlas.charts[d]<=atlas.adj[i]]
                nodes=[ports.index(d)+1 for d in seen]
                require(len(ports)==9 and len(seen)==3,'marked real H view')
                donors=sorted(atlas.planes[h]&atlas.native);grade=atlas.quota[j,h]//15
                v=atlas.vandermonde(nodes,9)
                if len(donors)==3:
                    a=3*donors.index(j);B=doubled(v[:,a:a+3])
                elif len(donors)==2 and grade==2:
                    B=np.vstack([v[:,:6],np.array([atlas.hermite(n,2,6)[1] for n in nodes])])
                elif len(donors)==2:
                    require(grade==1,'other donor split 3+3')
                    Z=np.zeros((3,3),dtype=np.uint8);B=np.block([[v[:,6:],Z],[Z,v[:,:3]]])
                else:
                    require(len(donors)==1 and grade==3,'singleton jet on its nine actual records')
                    B=f.singleton_jet(atlas,h,3,i);single_views+=1
                HX=atlas.mm(B,X[h]);physical.append(HX)
                if i not in receivers:
                    continue
                for b in range(2):
                    for t,d in enumerate(seen):
                        if d==120:
                            drecord[cols[h,b]]=HX[3*b+t]
                        else:
                            outside.append(HX[3*b+t])
            require(atlas.rank(np.vstack(physical))==96,'full actual H-jet receiver view')
            proper_views+=1
            if i not in receivers:
                continue
            require(len(outside)==88 and atlas.rank(np.array(outside))==88,'exact isolated-D dimension')
            lift=doubled(U[i]);require(not np.any(atlas.mm(np.array(outside),lift)),'every other visible D kills its shared original-input fibre')
            outputs=[rows[q,b] for b in range(2) for q in ks if i in atlas.planes[q]]
            full=atlas.mm(M[outputs],drecord);actual=atlas.mm(full,lift)
            require(atlas.rank(actual)==8,'D120 reads all eight isolated field inputs')
            if i in restricted:
                require(np.array_equal(actual,restricted[i]),'actual H/D lift and readout agree across all twelve donors')
            else:
                restricted[i]=actual
            if keep_h263 and j in (0,61,62):
                if i in common_full:
                    require(np.array_equal(full,common_full[i]),'three original H263 stars agree even on unrestricted original inputs')
                else:
                    common_full[i]=full
                unrestricted_full+=1
            if j==61:
                altered=drecord.copy();a=cols[384,0];altered[a]=atlas.product[2,altered[a]]
                mutated=atlas.mm(M[outputs],atlas.mm(altered,lift))
                require(not np.array_equal(mutated,actual),'negative control with an invertible H input coordinate rescaling')
                negative+=1
    return restricted,{'true_source_early_bases':len(roots),'all_native_source_H_foreign_cuts_on_twelve_donors':proper_views,
            'actual_singleton_H_foreign_cuts':single_views,'actual_D_minors':locals_132,'common_isolated_D_fibres':len(receivers)*len(roots),
            'isolated_D_rank_per_two_spinors':8,'direct_original_scalar_fibre_span':atlas.rank(np.hstack(list(U.values()))),
            'unrestricted_source_readouts_at_three_H263_donors':unrestricted_full,'rank_preserving_negative_controls':negative}


def complete_global_source(atlas,f,stars,small,keep_h263):
    predecessor_path=atlas.previous_path/'output/COEFFICIENTS.json.gz'
    raw=predecessor_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest()==atlas.previous.COEFFICIENT_SHA,'published H263 component pin')
    tables=json.loads(gzip.decompress(raw))['components']
    original={0,61,62}
    if keep_h263:
        chart=f.Chart(atlas,263,3)
        for j in original:
            source={int(h):array(v) for h,v in stars[j]['F'].items()}
            require(np.array_equal(array(stars[j]['P']['263']),np.eye(6,dtype=np.uint8)),'unaltered fully early central H263 inputs')
            points={int(x):array(v) for x,v in tables['3']['off_H'].items()}
            expected=chart.maps(points,j)
            require(all(np.array_equal(source[h],expected[h]) for h in source),'H263 source quotient kernels kept on all three donors')
        chart.check_readouts(points,chart.controls)
    chart=f.Chart(atlas,263,12)
    datasets=(atlas.algebra,atlas.planes,atlas.charts,atlas.masks,atlas.adj,atlas.quota,atlas.spread)
    native=[i for i in chart.views if i in atlas.native]
    ports=[d for d,D in enumerate(atlas.charts) if atlas.planes[263]<=D]
    parts=chart.donors,chart.point,chart.singular,native,chart.views,ports
    atlas.previous.check_component(12,parts,datasets,tables['12'],(atlas.product,atlas.inverse))
    result={}
    for k,used in [(3,set(stars)),(12,original)]:
        views=0;singletons={}
        for j in sorted(atlas.native-used):
            nodes=atlas.previous.ordinary_source(j,atlas.planes,atlas.quota)
            for i in sorted(atlas.adj[j]&atlas.native):
                visible=[v for h,v in nodes.items() if atlas.planes[h]<=atlas.adj[i]]
                require(len(visible)==len(set(visible))==16,'ordinary distinct-node MDS cuts')
                views+=1
            scale=f.generic_singleton(atlas,j,k)
            if scale:
                singletons[j]=scale
        own=small if k==3 else sum(len(atlas.adj[j]&atlas.native) for j in original)
        require(views+own==6470,'all actual foreign cuts in this spread component')
        result[k]={'special_source_donors':sorted(used),'special_foreign_pairs':own,'generic_foreign_pairs':views,
                   'generic_singleton_scales':singletons,'all_physical_source_H_foreign_pairs':6470,'early_bases':111}
    return result


def main():
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--repo',type=Path,required=True);cli.add_argument('--out',type=Path,required=True)
    args=cli.parse_args();base=args.repo/'research/moonshot-005-program/results'
    f=module(base/'bit-spread-disjoint-h-sources/author/families.py','families')
    compiler=module(base/'bit-spread-rs-physical-word/author/build.py','h_compiler')
    atlas=f.Atlas(args.repo)
    all_native=sorted(i for i in atlas.native if atlas.charts[120]<=atlas.adj[i])
    variants=[('retained_H263','TABLES.json.gz','688380f3b2e65521d6abff2e9267b6460039325bfc60c5b05a4c5cffa052c5d8',[5,10,95],True),
              ('all_D120_receivers','ALL-RECEIVERS.json.gz','3d2fbd7fc6eb74e006d6910f812d6d1a7487cf47c59d75844e08b69c8dd98747',all_native,False)]
    results={}
    for label,name,pin,expected,keep_h263 in variants:
        raw=(Path(__file__).parent/'output'/name).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==pin,'literal source/H/D tables pin')
        answer=json.loads(gzip.decompress(raw));I=answer['receivers'];require(I==expected,'actual designated receivers')
        W=array(answer['W']);U={int(i):array(u) for i,u in answer['U'].items()};stars={int(j):p for j,p in answer['stars'].items()}
        require(W.shape==(16,16) and atlas.rank(W)==16 and atlas.rank(np.hstack(list(U.values())))==4*len(I),'independent original fibres and genuine scalar D code')
        routes=[json.loads(line) for line in atlas.previous.pinned(base,'routes').splitlines()]
        hs=sorted(h for h,H in enumerate(atlas.planes) if H<=atlas.charts[120]);ks=sorted({r[5] for r in routes if r[4]==120 and r[5] is not None})
        require(len(hs)==len(ks)==16,'sixteen true H and K neighbours of D120')
        M,cols,rows,bill=physical_D(atlas,routes,W,hs,ks,compiler)
        responses,receipt=inspect_sources(atlas,f,stars,U,M,cols,rows,hs,ks,I,keep_h263)
        word_dir=base/'bit-spread-rs-physical-word/author'
        sys.path.insert(0,str(word_dir.resolve()))
        terminal=module(word_dir/'terminal.py','spread_terminal')
        rs=module(word_dir/'rs_source.py','spread_rs')
        endpoint=module(Path(__file__).parent/'endpoint.py','endpoint_calibration')
        receipt['actual_K_F_endpoint']=endpoint.forward(base,atlas,terminal,rs,compiler,routes,rows,ks,U,responses)
        receipt['global_source']= complete_global_source(atlas,f,stars,receipt['all_native_source_H_foreign_cuts_on_twelve_donors'],keep_h263)
        receipt.update({'physical_D_word':bill,'D':120,'receivers':I,'donors':sorted(stars),'modulus':67,'universal_factorization':False})
        results[label]=receipt
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print('PASS',[(label,x['common_isolated_D_fibres']) for label,x in results.items()])

if __name__=='__main__':
    main()
