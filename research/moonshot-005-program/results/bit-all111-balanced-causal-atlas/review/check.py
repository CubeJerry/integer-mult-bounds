#!/usr/bin/env python3
"""Independent finite geometry, all-field-holder matching and scalar coding constraints."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from functools import lru_cache
from hashlib import sha256
import gzip,itertools,json,struct
from pathlib import Path

NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
LAYOUT='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FACTOR='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'
B=5760;UNIT=24

def gf(x,y):
    p=0
    for j in range(6):
        if x>>j&1:p^=y<<j
    for k in range(10,5,-1):
        if p>>k&1:p^=67<<(k-6)
    return p

def outside(forms):
    """Avoid m proper homogeneous hyperplanes over GF64, one at a time."""
    assert 0<len(forms)<64
    def value(a,x):
        v=0
        for c,d in zip(a,x):v^=gf(c,d)
        return v
    v=[0]*len(forms[0]);kept=[]
    for f in forms:
        if not value(f,v):
            j=next(i for i,x in enumerate(f) if x)
            for t in range(64):
                w=v.copy();w[j]^=t
                if all(value(g,w) for g in kept+[f]):v=w;break
            else:raise AssertionError('finite bad values')
        kept.append(f)
    assert all(value(f,v) for f in forms);return v

def base(native,layout,factor):
    nr=native.read_bytes();wr=gzip.decompress(layout.read_bytes());fr=factor.read_bytes()
    assert [sha256(v).hexdigest() for v in (nr,wr,fr)]==[NATIVE,LAYOUT,FACTOR]
    w=json.loads(wr);R=w['root_table'];assert R[:111]==json.loads(nr)['native_roots'];F=json.loads(fr);assert F['denominator']==2
    factors=dict(F['factors']);assert len(factors)==len(F['factors'])==172
    A=list(map(frozenset,w['A2']));D=list(map(frozenset,w['D4']));dual=w['dual_D4'];native_ids=set(range(111));N=[a&native_ids for a in A]
    orth=[{j for j,r in enumerate(R) if not sum(v*x for v,x in zip(q,r))} for q in R]
    planes={a:h for h,a in enumerate(A)};dh=[sorted(planes[p] for p in map(frozenset,itertools.combinations(dd,3)) if p in planes) for dd in D]
    assert all(len(z)==16 for z in dh);hd=[set() for a in A]
    for d,hs in enumerate(dh):
        for h in hs:hd[h].add(d)
        assert set.intersection(*(orth[j] for j in D[d]))==D[dual[d]]
    assert all(len(z)==45 for z in hd)
    pens=[{h for h,p in enumerate(N) if j in p} for j in range(111)];assert all(len(v)==28 for v in pens)
    assert all(v in (1,2) and len(N[h])==3 for h,v in factors.items())
    x=[12//len(p)+factors.get(h,0) if p else 0 for h,p in enumerate(N)]
    e=[max(8,t) for t in x];early=[len(p)*x[h] for h,p in enumerate(N)];assert set(early)=={0,12,15,18}
    assert all(sum(45*x[h] for h in pen)==B for pen in pens)
    assert all(len(p)*e[h]<=UNIT for h,p in enumerate(N));assert sum(not p for p in N)==1
    for bad in factors:assert any(sum(45*(x[h]-(h==bad)) for h in pens[j])!=B for j in N[bad])
    return A,D,dual,N,orth,dh,hd,pens,x,e,early

def physical(A,D,dual,N,orth,dh,hd,pens,x,e,early):
    src=Counter();dst=Counter();hist=Counter();handoff=Counter();dig=sha256();role_counter=[Counter(),Counter()]
    def flags(h):
        out=[(h,j,True) for j in sorted(N[h]) for _ in range(x[h])]
        out.extend((h,j,False) for j in sorted(N[h]) for _ in range(e[h]-x[h]))
        out.extend([(h,-1,False)]*(UNIT-len(out)))
        return out
    by_h=list(map(flags,range(len(A))));slots=[[v for h in hs for v in by_h[h]] for hs in dh]
    def route(kind,d,left,right):
        h,j,_=left if left else(-1,-1,False);k,i,_=right if right else(-1,-1,False)
        if kind==0:assert j>=0;src[j]+=1;start=1;owner=role_counter[0][j];role_counter[0][j]+=1
        else:assert i>=0;dst[i]+=1;start=0;owner=role_counter[1][i];role_counter[1][i]+=1
        ranks=[start]
        if h!=-1:
            assert A[h]<=D[d] and (j<0 or j in A[h]);
            if kind and j>=0:ranks.append(1)
            ranks.append(2)
        ranks.append(4)
        if k!=-1:
            assert A[k]<=D[dual[d]] and (i<0 or i in A[k]);ranks.append(6)
            if i>=0:ranks.append(7)
        if not kind:ranks.append(8)
        for s,t in zip(ranks,ranks[1:]):assert t>s;hist[t-s]+=1
        dig.update(struct.pack('<Bhhhhhh',kind,d,h,j,k,i,owner))
    for d,left in enumerate(slots):
        right=slots[dual[d]];lx=[v for v in left if v[2]];ly=[v for v in left if not v[2]];rx=[v for v in right if not v[2]];ry=[v for v in right if v[2]]
        assert len(lx)+len(ly)==len(rx)+len(ry)==384 and len(lx)>=len(rx) and len(ry)>=len(ly)
        for a,b in zip(lx,rx):route(0,d,a,b)
        for a,b in zip(ly,ry):route(1,d,a,b)
        for a,b in zip(lx[len(rx):],ry[len(ly):]):route(0,d,a,None);route(1,d,None,b);handoff[d]+=1
    assert len(src)==len(dst)==111 and set(src.values())==set(dst.values())=={B}
    assert sum(handoff.values())==69120;hist[8]+=9*B
    assert hist=={1:((555*8+11)*B)//8,2:((903*8-11)*B)//16,4:24*B,8:9*B}
    return {'public_field_holders':sum(src.values())+sum(dst.values()),'split_XY_symbol_pairs':sum(handoff.values()),'actual_route_stream_sha256':dig.hexdigest(),'scalar_movement':dict(sorted(hist.items()))}

def paths(A,D,dual,N,orth,dh,hd,pens,x,e,early):
    native=set(range(111));facets=[set.intersection(*(orth[j]for j in a))&native for a in A]
    db=[{d for d,dd in enumerate(D) if j in dd} for j in range(111)]
    rec=Counter();cut=Counter();prefix=sha256();bounds=Counter();pairs=0
    for j in range(111):
        for i in sorted(orth[j]&native):
            pairs+=1;hs={h for h in pens[j] if i in facets[h]};ks={k for k in pens[i] if j in facets[k]};ds={d for d in db[j] if i in D[dual[d]]}
            assert len(hs)==len(ks)==16 and len(ds)==60
            for h in sorted(hs):
                n=len(hd[h]&ds);assert n==15;outX=n*early[h];availX=45*x[h];availY=45*(e[h]-x[h]);chosenX=min(360,availX)
                assert 0<=outX<=chosenX<=360 and 360-chosenX<=availY
                cut['H early-to-late']+=chosenX-outX
            for k in sorted(ks):
                n=sum(dual[d] in hd[k] for d in ds);assert n==15;incoming_early=n*(24-early[k]);available_late=45*x[k];available_early=45*(e[k]-x[k]);selected_late=min(360,available_late)
                assert 360-selected_late<=incoming_early and 360-selected_late<=available_early
                cut['K early-to-late']+=incoming_early-(360-selected_late)
            for d in sorted(ds):
                h=hs.intersection(dh[d]);k=ks.intersection(dh[dual[d]]);assert len(h)==len(k)==4
                xin=sum(early[t]for t in h);xout=sum(24-early[t]for t in k);assert 0<=xout<=xin<=96
                cut['D early-to-late']+=xin-xout
                prefix.update(struct.pack('<BBHBB',j,i,d,xin,xout))
            rec['unit_path_witnesses']+=len(ds)*4*UNIT;assert len(ds)*4*UNIT==B
    for h in range(len(A)):
        if N[h]:bounds['L_or_F_coordinate']=max(bounds['L_or_F_coordinate'],len(facets[h]))
        for d in hd[h]:
            nh=len(N[h]);ni=len(D[dual[d]]&native)
            bounds['H_or_K_coordinate']=max(bounds['H_or_K_coordinate'],ni)
            bounds['H_D_or_D_K_edge']=max(bounds['H_D_or_D_K_edge'],nh*ni)
            for k in dh[dual[d]]:bounds['D_coordinate']=max(bounds['D_coordinate'],nh*len(N[k]))
    bounds['final_proper_commodities']=max(len(x&native)for x in orth[:111]);assert pairs==6470
    inddeg=max(bounds[k] for k in ('L_or_F_coordinate','H_or_K_coordinate','D_coordinate'))+2
    hyper=max(bounds['H_D_or_D_K_edge'],bounds['L_or_F_coordinate'],bounds['final_proper_commodities'])+1
    assert inddeg<=38 and hyper<=63
    return {'ordered_proper_pairs':pairs,'all_unit_paths_counted_with_multiplicity':rec['unit_path_witnesses'],'pair_time_matching_sha256':prefix.hexdigest(),'early_to_late_units_in_witnesses':dict(cut),'local_support_bounds':dict(bounds),'max_individual_degree_bound':inddeg,'max_forbidden_hyperplanes_bound':hyper,'negative_single_middle_lane_bound':B-1}

def main():
    p=ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--layout',type=Path,required=True);p.add_argument('--factor',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    data=base(a.native,a.layout,a.factor);r=physical(*data);s=paths(*data);pows=[1]
    for _ in range(62):pows.append(gf(pows[-1],2))
    assert len(set(pows))==63 and gf(2,pows[-1])==1
    examples=[outside([(1,t) for t in range(63)]),outside([(t,1,1)for t in range(1,64)])]
    assert all(any(sum(a*b for a,b in zip(f,v))%2==0 for f in [[1,0],[0,1],[1,1]])for v in itertools.product(range(2),repeat=2))
    out={'status':'PASS_BALANCED_CAUSAL_WITNESSES_AND_DETERMINISTIC_GF64_SELECTION_GATE','pinned_sources':[NATIVE,LAYOUT,FACTOR],**r,**s,'extension_degree':6,'binary_copies_per_role':B*6,'all_rank_coefficients_materialized':False,'hyperplane_negative_base_field':True,'avoid_63_controls':examples,'local_factor_mutations_rejected':172,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],r['actual_route_stream_sha256'],s['local_support_bounds'])
if __name__=='__main__':main()
