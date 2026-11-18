#!/usr/bin/env python3
"""Choose native A2 triples giving exact public X and Y multiplicities."""
from argparse import ArgumentParser
from hashlib import sha256
from collections import Counter,defaultdict
from pathlib import Path
import json,gzip
import numpy as np
from scipy.optimize import Bounds,LinearConstraint,milp
from scipy.sparse import coo_matrix
from atlas import bits,mask
from layout import need

def base(w):
    A=[tuple(a) for a in w['A2']];D=list(map(mask,w['D4']));P=w['dual_D4'];J=[tuple(k for k in h if k<111) for h in A];T=[h for h,v in enumerate(J) if len(v)==3];e=[h for h,v in enumerate(J) if not v];need(len(e)==1,'exact one empty A2');empty=mask(A[e[0]])
    deg=[0]*111
    for js in J:
        if js:
            a=6//len(js)
            for j in js:deg[j]+=45*a
    rem=[(2880-u)//45 for u in deg]
    need(all(u+45*r==2880 for u,r in zip(deg,rem)),'integral degree defect')
    loc=[d for d,dd in enumerate(P) if d<dd and (D[d]&empty==empty or D[dd]&empty==empty)]
    cov={d:[h for h in T if mask(A[h])&D[d]==mask(A[h]) or mask(A[h])&D[P[d]]==mask(A[h])] for d in loc}
    return A,D,P,J,T,e,rem,loc,cov

def choose(w,den):
    A,D,P,J,T,e,rem,loc,cov=base(w);tindex={h:p for p,h in enumerate(T)};row=[];col=[]
    for n,h in enumerate(T):
        for j in J[h]:row.append(j);col.append(n)
    for p,d in enumerate(loc):
        for h in cov[d]:row.append(111+p);col.append(tindex[h])
    M=coo_matrix((np.ones(len(row)),(row,col)),shape=(111+len(loc),len(T))).tocsr()
    lo=np.r_[np.array(rem)*den,[2.*den]*len(loc)];hi=np.r_[np.array(rem)*den,[np.inf]*len(loc)]
    r=milp(np.zeros(len(T)),integrality=np.ones(len(T)),bounds=Bounds(np.zeros(len(T)),np.ones(len(T))*den),constraints=LinearConstraint(M,lo,hi),options={'time_limit':80})
    need(r.x is not None,'integral b-matching found: '+str(r.message));return {'denominator':den,'factors':[[h,round(x)] for h,x in zip(T,r.x) if x>.5]}

def verify(w,factor):
    den=factor['denominator'];pick=dict(factor['factors'])
    A,D,P,J,T,e,rem,loc,cov=base(w);ss=set(pick)
    need(all(0<n<=den for n in pick.values()) and len(ss)==len(factor['factors']) and ss<=set(T),'distinct native-full A2 factors')
    need([sum(pick[h] for h in ss if j in J[h]) for j in range(111)]==[den*v for v in rem],'exact 111 degree equations')
    need(all(sum(pick[h] for h in ss.intersection(cov[d]))>=2*den for d in loc),'empty-flat carrier reserve')
    # Encode each H,D incident in twelve slots. A donor contributes n_x X and n_y
    # independent parity-on-Y arrivals to its H, while every remaining slot is a
    # genuine Y with no source-line visit. The other side is its time-dual.
    hx=[];he=[];sy=[]
    for h,js in enumerate(J):
        m=len(js);x=(6//m if m else 0)*den+pick.get(h,0);total=max(4*den,x);hx.append(m*x);he.append(x);sy.append(total-x)
        need(m*total<=12*den and (not m or (he[h]*45>=hx[h]*15 and (he[h]+sy[h])*45>=180*den)),'source causal inlet')
    dH=[[] for d in D]
    for d,dd in enumerate(D):
        allh=[h for h,a in enumerate(A) if mask(a)&dd==mask(a)]
        need(len(allh)==16,'D4 contains 16 planes');dH[d]=allh
    scores=[sum(hx[h] for h in hh) for hh in dH]
    local=[scores[d]+scores[P[d]]-192*den for d in range(len(D))]
    need(min(local)>=0,'global matching of genuine coloured public records')
    need(2*sum(local)==2*(111*2880-3150*96)*2*den,'split records census')
    return {'status':'PASS_TIME_BALANCED_NATIVE_TRIPLE_FACTOR','factor_denominator':den,'selected_count':len(ss),
            'defect_degree_histogram':dict(sorted(Counter(rem).items())),'empty_A2_index':e[0],'empty_dual_pair_reserves':len(cov),
            'native_roles':111,'paid_GF_copies':2880*den,'source_per_H_D_X_histogram':dict(sorted(Counter(hx).items())),
            'D_early_X_range':[min(scores),max(scores)], 'split_XY_pairs_per_D_histogram':dict(sorted(Counter(local).items())),
            'total_split_XY_pairs':sum(local),'supplementary_true_line_visits_per_side':sum(45*len(J[h])*(he[h]+sy[h]-4*den) for h in range(len(A)))}

def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--den',type=int,default=2);ap.add_argument('--factor',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin');w=json.loads(raw)
    factor=json.loads(a.factor.read_bytes()) if a.factor else choose(w,a.den);r=verify(w,factor);a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'BALANCED-FACTOR.json').write_text(json.dumps(factor,separators=(',',':'))+'\n');(a.out/'BALANCED-RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(factor['factors']),r['supplementary_true_line_visits_per_side'],r['total_split_XY_pairs'])
if __name__=='__main__':main()
