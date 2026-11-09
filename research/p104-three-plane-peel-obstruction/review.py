"""Independent dual functional check of the two endpoint-peel obstructions.

@CubeJerry; substantial OpenAI assistance.  No author-code imports. The
author builds forward full matrices; this checker pulls back scalar
functionals and verifies the four relevant inverse rows by composition.
"""
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
import argparse, gzip, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PKG = HERE if (HERE/'data/word.json.gz').is_file() else ROOT/'worker-b-peel/research/p104-three-plane-peel-obstruction'
PIN='ab5c1c05383a8d3a84995f1a8368e08173e776608d635ff06871651d9e494590'

def need(x, message):
    if not x: raise ValueError(message)

def pullback(events, form, count):
    x=[Q(0)]*count
    for i,value in form.items(): x[i]=Q(value)
    for e in reversed(events):
        op,r=e[:2]
        if op=='ADD': x[e[2]]+=Q(e[3])*x[r]
        elif op=='COPY':
            v=x[r]; x[r]=Q(0); x[e[2]]+=Q(e[3])*v
        elif op=='SCALE': x[r]*=Q(e[2])
        elif op in ('INIT','CLEAR'): x[r]=Q(0)
        elif op!='MOVE': raise ValueError(op)
    return {i:v for i,v in enumerate(x) if v}

def subspace(frame):
    # Enumerate subsets directly rather than using the author's iterative
    # span update.  The frames have at most nine independent generators.
    values=[]
    for m in range(1<<len(frame)):
        z=0
        for j,v in enumerate(frame):
            if m & (1<<j): z^=v
        values.append(z)
    need(len(set(values))==len(values),'dependent frame')
    return frozenset(values)

def rank3(M):
    # Nonzero minors characterize rank, without Gaussian elimination.
    a=M
    det=(a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
        -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
        +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))
    if det: return 3
    for i in range(3):
        for j in range(i+1,3):
            for k in range(3):
                for l in range(k+1,3):
                    if a[i][k]*a[j][l] != a[i][l]*a[j][k]: return 2
    return int(any(v for row in a for v in row))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--package', type=Path, default=PKG,
                    help='Frozen package directory containing data/word.json.gz')
    ap.add_argument('--output', type=Path,
                    help='Optional receipt destination; omitted runs read-only')
    args=ap.parse_args()
    raw=(args.package/'data/word.json.gz').read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'frozen source')
    w=json.loads(gzip.decompress(raw)); p=w['program']; n=w['public']; nn=n+w['owned_fields']
    mov=[i for i,e in enumerate(p) if e[0]=='MOVE']; lo,hi=min(mov),max(mov)
    core=p[lo:hi+1]
    Tinv=[]
    for x in w['live']: Tinv.append(['ADD',x+112,x,'-1'])
    for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']): Tinv.append(['ADD',x,y,'1'])
    inverse_sequence=p[hi+1:]+Tinv+p[:lo]
    rows=[159,931,1352]; cols=[47,819,793,1202]
    K={r:pullback(core,{r:1},nn) for r in rows}
    KI={r:pullback(inverse_sequence,{r:1},n) for r in cols}
    inverse_controls=[]
    for r,row in KI.items():
        composition={i:v for i,v in pullback(core,row,nn).items() if i<n}
        need(composition=={r:Q(1)},'independent inverse row product')
        bad=dict(row);bad[r]=bad.get(r,Q(0))+1
        composition={i:v for i,v in pullback(core,bad,nn).items() if i<n}
        need(composition!={r:Q(1)},'mutated inverse functional control')
        inverse_controls.append(r)
    frames=[subspace(f) for f in w['frames']]
    ini=[frames[f] for f in w['initial']]; fin=[frames[f] for f in w['final']]
    zero,full=frozenset([0]),frozenset(range(512))
    moves=defaultdict(list)
    for i,e in enumerate(p):
        if e[0]=='MOVE':moves[e[1]].append((i,e))
    mains=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    nx=ny=pairs=0
    for q in w['ports']:
        need(q.bit_count()%2==1,'anisotropic source port')
        line=frozenset([0,q]); perp=frozenset(x for x in range(512) if not ((x&q).bit_count()%2))
        candidates=[r for r in range(n) if r not in mains and ini[r]==zero and fin[r]==full and moves[r]]
        hs=[r for r in candidates if frames[moves[r][0][1][2]]==zero and frames[moves[r][0][1][3]]==line]
        gs=[r for r in candidates if frames[moves[r][-1][1][2]]==perp and frames[moves[r][-1][1][3]]==full]
        need(not set(hs)&set(gs),'a helper cannot play both anisotropic endpoint roles')
        nx+=len(hs);ny+=len(gs);pairs+=len(hs)*len(gs)
    need((nx,ny,pairs)==(363,295,984),'independent finite family census')
    cases=[]
    for h in [793,1202]:
        q=268; I=[47,819,h]; O=[159,931,1352]
        line=frozenset([0,q]); perp=frozenset(x for x in range(512) if not ((x&q).bit_count()%2))
        need([r for r in range(n) if ini[r]==line]+[h]==I,'entire new input group')
        need([r for r in range(n) if fin[r]==perp]+[1352]==O,'entire new output group')
        f=[[K[r].get(c,Q(0)) for c in I] for r in O]
        b=[[KI[r].get(c,Q(0)) for c in O] for r in I]
        want_f=[[1,0,0],[0,0,0],[0,0,0]]
        want_b=[[0,0,0],[0,1,Q(1,2)],[0,0,0]]
        need(f==want_f and b==want_b,'both exact residual blocks')
        need((rank3(f),rank3(b))==(1,1),'actual minor ranks')
        tf=[row[:] for row in want_f];tf[2][2]=1
        # Target source inverse has its reverse-plane unit at [1,1];
        # the frozen core's [1,2]=1/2 is irrelevant to that target.
        ti=[[0,0,0],[0,1,0],[0,0,0]];ti[2][2]=1
        need(rank3(tf)==2 and rank3(ti)==2,'independent extra-plane rank demand')
        cases.append({'q':q,'h':h,'g':1352,'forward':[[str(x) for x in r] for r in f],
                      'inverse':[[str(x) for x in r] for r in b],
                      'actual_ranks':[1,1],'forward_target_ranks':[2,1],
                      'reverse_target_ranks':[1,2]})
    receipt={'source_gzip_sha256':PIN,'source_events':len(p),'core_range':[lo,hi],
      'method':'Reverse scalar functionals, inverse-row composition, direct minor ranks; no producer imports',
      'independent_census':{'input_helpers':nx,'output_helpers':ny,'pairs':pairs},
      'inverse_rows_checked':cols,'mutated_inverse_rows_rejected':inverse_controls,
      'residual_cases':cases,
      'scope':'Independent two-block obstruction and finite family size. Nonresidual zero-block witnesses remain author checks, supported by separately reviewed rank-invariance proof.'}
    if args.output:
        args.output.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2)); print('PASS_INDEPENDENT_ENDPOINT_PEEL_BLOCKS')

if __name__=='__main__':main()
