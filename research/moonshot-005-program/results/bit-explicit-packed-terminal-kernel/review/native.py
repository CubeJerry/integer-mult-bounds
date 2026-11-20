"""Forward original data through native spread owners once per common-mode batch."""
from collections import defaultdict
from pathlib import Path
import hashlib
import numpy as np
def modes(sector,j,w,d):
    seed=f'known-original-S029-four-copy-v1/{sector}/zero-slack-0/role-{j}'.encode('ascii')
    return np.frombuffer(hashlib.shake_256(seed).digest(w*d*4),dtype=np.uint8).reshape(w,d,4)&63
def arrivals(nat,alg,mm,sector):
    w,d,k,n,lo=(96,168,3,9,0)if sector=='small'else(384,672,12,36,96)
    zs=[modes(sector,j,w,d).reshape(w,4*d) for j in range(111)]
    # Actual H outputs, actual D outputs and actual K outputs share these same owner IDs.
    signals=np.zeros((106560,4*d),dtype=np.uint8)
    for h,outs in nat.byh.items():
        p=nat.p[h]
        if not p["m"]:continue
        sub=sorted(z for z in set(t[1]for t in outs)if (z in nat.mark)==(n==9))
        assert len(sub)==n;V=np.array(nat.hword[n]['V'],dtype=np.uint8);stored={}
        for ph,tag in (('X','early'),('Y','late')):
            for stripe in range(p[tag]):
                values=np.zeros((n,4*d),dtype=np.uint8)
                for j in nat.H[h]:
                    if j>=111:continue
                    raw=nat.source_in(j,h,ph,n,stripe)[:,lo:lo+w]
                    values^=mm(raw,zs[j])
                got=mm(V,values)
                if ph=='X':stored[stripe]=values
                elif p['m']<3:
                    kind='singleton' if p['m']==1 else 'two'
                    got^=mm(np.array(nat.hword[n][kind]['cross_coefficients'],dtype=np.uint8),stored[stripe])
                for t,z in enumerate(sub):signals[outs[ph,z][stripe]]=got[t]
    for z,(idx,e,y,weights)in enumerate(nat.dword):
        if (z in nat.mark)!=(n==9):continue
        xs,ys=nat.byd[z]['X'],nat.byd[z]['Y'];X=signals[xs];Y=signals[ys]
        signals[xs]=mm(alg.cauchy(range(e),range(e)),X);late=mm(alg.cauchy(range(y),range(y)),Y)
        if weights:
            r=len(weights);temp=mm(alg.cauchy(range(e,e+r),range(e)),X)
            late^=mm(alg.cauchy(range(y),range(y,y+r)),alg.MUL[np.array(weights,dtype=np.uint8)[:,None],temp])
        signals[ys]=late
    owners=defaultdict(lambda:defaultdict(list))
    for h,kw in nat.kwords['spread'].items():
        updates=[];local=set()
        for ph,src,dst in kw['stripes']:
            if len(src)!=n:continue
            z=mm(np.ascontiguousarray(alg.POWER[1:n+1,:n].T),signals[src]);updates.append((dst,z));local.update(dst)
            for u in dst:
                r=nat.rt[u];i=r[1] if ph=='Y' else r[7]
                if i is not None:owners[i][ph].append(u)
        for dst,z in updates:signals[dst]=z
        for e,y in kw['early_cache_to_late']:
            if y in local:assert e in local;signals[y]^=signals[e]
    return signals,{i:(sorted(v['X']),sorted(v['Y']))for i,v in owners.items()},zs
