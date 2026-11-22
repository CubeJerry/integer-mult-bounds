#!/usr/bin/env python3
"""Independent physical reconstruction of the bounded source/D interpolation screen."""
import argparse, gzip, hashlib, json, runpy
from collections import defaultdict, Counter
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; ROOT=BASE.parents[2]
H=runpy.run_path(str(BASE/'bit-simultaneous-d1509-s032-independent/check_frames.py'))
mm,rank,inverse,basis,rd,wr,need=[H[k] for k in ['mm','rank','inverse','basis','rd','wr','need']]
null=H['ALG']['null']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=HERE/'output');args=ap.parse_args()
    for file,digest in rd(HERE/'SOURCE-PINS.json')['files'].items():
        need(hashlib.sha256((ROOT/file).read_bytes()).hexdigest()==digest,'source binding '+file)
    four=BASE/'bit-simultaneous-d1509-s032/output'
    source,hp,dw,gg=[rd(four/n) for n in ['SOURCES.json.gz','H-PHYSICAL.json.gz','D-WORD.json.gz','CONSTRAINED-GAUGES.json.gz']]
    layout=rd(BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz')
    roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(z==0).tolist()) for z in roots@roots.T]
    planes=[set(z) for z in layout['A2']];charts=[set(z) for z in layout['D4']]
    marked=set(rd(BASE/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')['selected_D'])
    routes=[json.loads(z) for z in gzip.decompress((BASE/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()]
    X,Y,Xj,Yj=[defaultdict(list) for _ in range(4)]
    for r in routes:
        if r[3] is None:continue
        (X if r[0]=='X' else Y)[r[3]].append(r)
        if r[0]=='X':Xj[r[1],r[3]].append(r)
        elif r[6] is not None:Yj[r[6],r[3]].append(r)
    for tab in [X,Y,Xj,Yj]:
        for key in tab:tab[key].sort(key=lambda z:(z[1],z[2]))
    owners=sorted([z for z in routes if z[4]==1509 and z[0]=='X'],key=lambda z:(z[1],z[2]))+sorted([z for z in routes if z[4]==1509 and z[0]=='Y'],key=lambda z:(z[1],z[2]))
    need(owners==dw['owners'],'D owners reconstructed from raw routes')
    donors=sorted(map(int,source['paired_maps']));R=gg['receivers'];L=np.array(gg['common_frames'],dtype=np.uint8)
    need(donors==sorted(j for j in charts[1509] if j<111) and R==[6,9,48,73] and rank(L)==32,'actual native donors and common receiver frames')
    ins={j:[i for i,z in enumerate(owners) if z[3] is not None and j in planes[z[3]]] for j in donors}
    outs={r:[i for i,z in enumerate(owners) if z[5] is not None and r in planes[z[5]]] for r in R}
    hf=rd(BASE/'bit-simultaneous-d1509-s032-independent/output/H-FIBRES.json.gz')
    prot=list(range(48))+list(range(240,288));pr=[0,1,2,15,16,17];local={};records=[]
    for j in donors:
        parent=[int(h) for h in source['paired_maps'][str(j)] if planes[int(h)]<=charts[1509]]
        need(len(parent)==4,'four actual D-parent source quotients')
        ii={tuple(owners[i][:3]):q for q,i in enumerate(ins[j])}
        for h in sorted(parent):
            hs=str(h);full=np.array(source['paired_maps'][str(j)][hs],dtype=np.uint8);F=full[np.ix_(pr,prot)]
            need(rank(F)==6 and not np.any(full[np.ix_([i for i in range(30) if i not in pr],prot)]),'protected six-row family')
            vs=[]
            for key,a in hf.get(str(j),{}).items():
                centre,r=map(int,key.split('/'))
                if r<111 and planes[h]<=adj[r]:vs.append(np.array(a,dtype=np.uint8))
            C=basis(np.hstack(vs)) if vs else np.zeros((96,0),dtype=np.uint8)
            need(np.array_equal(mm(np.array(gg['gauges'][str(j)],dtype=np.uint8),C),C),'native H generators retain the same source coordinates after the four-receiver gauge')
            XX=np.hstack([C,L]);N=null(XX)
            Q=np.array(source['frames'][f'{j}/{h}'],dtype=np.uint8);ne,nl=len(X[h]),len(Y[h])
            need(hp[hs]['X_owners']==X[h] and hp[hs]['Y_owners']==Y[h],'actual H phase owners')
            E=np.array(hp[hs]['early'],dtype=np.uint8).reshape(ne,ne);B=np.array(hp[hs]['late'],dtype=np.uint8).reshape(nl,nl);cross=np.array(hp[hs]['cross'],dtype=np.uint8).reshape(nl,ne)
            xe=np.zeros((ne,6),dtype=np.uint8);yl=np.zeros((nl,6),dtype=np.uint8)
            xi={(z[1],z[2]):q for q,z in enumerate(X[h])};yi={(z[1],z[2]):q for q,z in enumerate(Y[h])}
            for q,z in enumerate(Xj[j,h]):xe[xi[z[1],z[2]]]=Q[q,pr]
            for q,z in enumerate(Yj[j,h]):yl[yi[z[1],z[2]]]=Q[len(Xj[j,h])+q,pr]
            responses=[mm(E,xe),mm(cross,xe)^mm(B,yl)];maps={};labels={}
            for r in R:
                need(planes[h]<=adj[r],'D parent visible at retained receiver')
                rows=[];labs=[]
                for seq,A in [(X[h],responses[0]),(Y[h],responses[1])]:
                    for q,z in enumerate(seq):
                        if z[4] in marked and charts[z[4]]<=adj[r]:rows.append(A[q]);labs.append(tuple(z[:3]))
                BB=np.array(rows,dtype=np.uint8);need(BB.shape==(6,6) and rank(BB)==6,'actual invertible H-to-proper six-row map')
                select=np.zeros((6,8),dtype=np.uint8)
                for q,lab in enumerate(labs):
                    if lab in ii:select[q,ii[lab]]=1
                maps[r]=mm(inverse(BB),select);labels[r]=labs
            local[j,h]={'F':F,'C':C,'X':XX,'N':N,'maps':maps}
            records.append({'donor':j,'H':h,'native_H_span_dimension':C.shape[1],'interpolation_domain_rank':rank(XX),'relation_dimension':N.shape[1],'proper_row_owners':labels})
    need(len(local)==44,'all 44 actual interpolation systems')
    def inverses(T):
        out={}
        for j in donors:
            for r in R:
                A=T[np.ix_(outs[r],ins[j])]
                if rank(A)!=8:return None,['singular_section',j,r]
                out[j,r]=inverse(A)
        return out,None
    def residual(ci,j,h):
        z=local[j,h];YY=np.hstack([mm(z['F'],z['C'])]+[mm(z['maps'][r],ci[j,r]) for r in R])
        return mm(YY,z['N']),YY
    T=np.array(dw['matrix'],dtype=np.uint8);S=np.array(rd(BASE/'bit-d1509-coupled-repair-s032/D-WORD.json.gz')['matrix'],dtype=np.uint8)
    controls=[]
    for name,M in [('original_D_word',T),('admitted_six_free_row_D_word',S)]:
        ci,bad=inverses(M);need(bad is None,'positive control sections')
        for (j,h),z in local.items():
            res,YY=residual(ci,j,h)
            need(not np.any(res) and np.array_equal(YY,mm(z['F'],z['X'])),'unchanged source is an exact positive interpolation solution')
        controls.append({'word':name,'local_systems_passed':44,'unchanged_source_solution':True})
    author=rd(BASE/'bit-source-d-interpolation-s032/RESULT.json')
    used=sorted(set(sum(outs.values(),[])));pairs=[(q,p) for q in used for p in range(35) if q!=p and (q>=19 or p<19)]
    pairs=sorted(pairs,key=lambda z:hashlib.sha256(str(z).encode()).digest())[:128]
    need([z['output_shear'] for z in author['records']]==[[q,p,1] for q,p in pairs],'exact deterministic bounded family')
    checks=[]
    for (q,p),record in zip(pairs,author['records']):
        M=T.copy();M[q]^=T[p];need(not np.any(M[:19,19:]) and rank(M)==35,'phase-legal invertible elementary output shear')
        need(any(np.any(M[np.ix_(outs[r],ins[j])]^T[np.ix_(outs[r],ins[j])]) for j in donors for r in R),'trial changes an actual retained section')
        ci,bad=inverses(M);claimed=record['status']
        if bad:
            need(claimed==bad,'independent first singular section')
            checks.append({'output_shear':[q,p,1],'status':bad})
        else:
            need(isinstance(claimed,list) and claimed[0]=='H_source_interpolation_inconsistent','claimed interpolation failure type')
            j,h,k=claimed[1:];res,_=residual(ci,j,h)
            need(rank(res)==k and k>0,'independently reconstructed exact relation violation')
            checks.append({'output_shear':[q,p,1],'status':['H_source_interpolation_inconsistent',j,h,k]})
    counts=Counter(z['status'][0] for z in checks)
    need(len(checks)==128 and author['candidate'] is None,'bounded rejection only')
    result={'status':'PASS_INDEPENDENT_SOURCE_D_INTERPOLATION_REDUCTION','actual_local_systems':44,'protected_source_rows':6,'protected_source_columns':96,'retained_receivers':R,'native_H_observations_only':True,'local_maps_reconstructed_from_physical_H':True,'new_author_executable_imports':False,'positive_controls':controls,'deterministic_shears_checked':128,'classification_counts':dict(counts),'necessity_and_sufficiency_scope':'linear protected six-row source interpolation equations; no full source-rank or supplier sufficiency','general_no_go':False,'complete_fifth_receiver':False,'new_kappa':False}
    wr(args.out/'RESULT.json',result);wr(args.out/'LOCAL-SYSTEMS.json.gz',records);wr(args.out/'TRIAL-WITNESSES.json',checks)
    wr(args.out/'RECONSTRUCTED-MATRICES.json.gz',{f'{j}/{h}':{'source':z['F'].tolist(),'native_H_span':z['C'].tolist(),'relations':z['N'].tolist(),'target_maps':{r:A.tolist() for r,A in z['maps'].items()}} for (j,h),z in local.items()})
    print(json.dumps(result,sort_keys=True),flush=True)

if __name__=='__main__':main()
