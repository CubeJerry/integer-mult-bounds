"""Lead reverse-prefix audit; no worker scientific modules imported."""
from pathlib import Path
from fractions import Fraction as Q
import gzip
import hashlib
import json
ROOT=Path(__file__).resolve().parents[2]
CUT=36961

def need(ok,why):
    if not ok: raise ValueError(why)

def plus(dst,src,c):
    for j,v in src.items():
        t=dst.get(j,Q(0))+c*v
        if t: dst[j]=t
        else: dst.pop(j,None)

def rank(rows):
    pivots={}
    for row in rows:
        row=dict(row)
        while row:
            j=min(row)
            if j in pivots: plus(row,pivots[j],-row[j])
            else:
                c=row[j]; pivots[j]={k:v/c for k,v in row.items()}; break
    return len(pivots)

def reconstruct(w):
    n=w['public']; live=set()
    for e in w['program'][:CUT]:
        if e[0]=='INIT': live.add(e[1])
        if e[0]=='CLEAR': live.remove(e[1])
    owners=sorted(live)
    dual=[{} for _ in range(n+w['owned_fields'])]
    for i,o in enumerate(owners): dual[o]={i:Q(1)}
    for e in reversed(w['program'][:CUT]):
        op,a=e[:2]
        if op in ('ADD','COPY'): plus(dual[e[2]],dual[a],Q(e[-2]))
        elif op=='SCALE': dual[a]={k:Q(e[-2])*v for k,v in dual[a].items()}
        elif op in ('INIT','CLEAR'): dual[a]={}
        elif op!='MOVE': raise ValueError(op)
    rows=[{} for _ in owners]
    for j,col in enumerate(dual[:n]):
        for i,v in col.items(): rows[i][j]=v
    return owners,rows

def main():
    raw=(ROOT/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source pin')
    w=json.loads(gzip.decompress(raw)); owners,rows=reconstruct(w); n=w['public']
    mains=set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    mrows=[{j:v for j,v in r.items() if j in mains} for r in rows]
    paired=[]
    for plane in range(2):
        paired += [{(j+plane*n if j in mains else j+2*n):v for j,v in r.items()} for r in rows]
    full_r,main_r,pair_r=rank(rows),rank(mrows),rank(paired)
    need((len(owners),full_r,main_r,pair_r)==(42,26,21,47),'exact cut ranks')
    qrows=[{a:Q(1),b:Q(-1)} for a,b in [(623,768),(607,770),(728,1448),(723,1390),(1163,1397)]]
    need(rank(rows+qrows)==full_r and rank(qrows)==5,'helper quotient basis')
    dims=[]
    for k in range(6):
        obs=[{j+2*n:v for j,v in r.items()} for r in qrows[:k]]
        residual=rank(paired+obs)-rank(obs)
        need(residual==47-k,'sharp helper side-information quotient')
        dims.append(residual)
    need(rank(rows+rows)==26,'aliased-main control')
    mutant=[dict(r) for r in rows]; mutant[0][10*n]=Q(1)
    need(rank(mutant+rows)>26,'hidden independent information control')
    encoded=[{str(k):str(v) for k,v in sorted(r.items())} for r in rows]
    digest=hashlib.sha256(json.dumps(encoded,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    print(json.dumps({'status':'PASS_LEAD_REVERSE_OWNED_CUT','cut_before_event':CUT,
        'owned_live':len(owners),'rank_one_owned':full_r,'rank_main_projection':main_r,
        'rank_two_independent_mains_shared_helpers':pair_r,'optimal_pure_helper_observation_residuals':dims,
        'normalized_rows_sha256':digest,'controls':['aliased main copies have rank26','extra independent information detected'],
        'scope':'Normalized scalar-linear storage and chosen side observations; no physical43-field realization.'},indent=2))

if __name__=='__main__': main()
