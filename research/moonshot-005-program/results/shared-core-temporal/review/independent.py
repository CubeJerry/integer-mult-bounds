#!/usr/bin/env python3
"""Independent reverse-adjoint and finite noncommutative switch checks."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse,gzip,hashlib,json

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(p,msg):
    if not p: raise ValueError(msg)

def mm(a,b,p):
    return tuple(sum(a[2*i+k]*b[2*k+j] for k in range(2))%p
                 for i in range(2) for j in range(2))

def inv(a,p):
    d=(a[0]*a[3]-a[1]*a[2])%p
    q=pow(d,-1,p)
    return tuple(q*x%p for x in (a[3],-a[1],-a[2],a[0]))

def gf2_canonical(rows):
    out=[]
    for value in rows:
        for b in out: value=min(value,value^b)
        if value:
            out.append(value);out.sort(reverse=True)
            for i in range(len(out)):
                for j in range(i+1,len(out)): out[i]=min(out[i],out[i]^out[j])
    return tuple(sorted(out,reverse=True))

def backward(w,output,skeleton,mains):
    row=[F(0)]*(w['public']+w['owned_fields']);row[output]=F(1)
    for e in reversed(w['program']):
        op,a=e[:2]
        if op in ('INIT','CLEAR'):
            if not skeleton:row[a]=F(0)
        elif op=='SCALE':
            if not skeleton or a in mains:row[a]*=F(e[2])
        elif op in ('ADD','COPY'):
            if not skeleton or (a in mains and e[2] in mains):row[e[2]]+=F(e[3])*row[a]
        elif op!='MOVE':raise ValueError(op)
    return row

def run(path):
    raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'immutable source')
    w=json.loads(gzip.decompress(raw))
    mains=set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
    need(len(mains)==400,'main census')
    for e in w['program']:
        need(not(e[1] in mains and e[0] in ('COPY','INIT','CLEAR')),'invertible skeleton alphabet')
        if e[0]=='SCALE' and e[1] in mains:need(F(e[2])!=0,'nonzero skeleton scales')
    copies=[i for i,e in enumerate(w['program']) if e[0]=='COPY']
    need(copies==[31737] and w['program'][31736]==['INIT',1504,115], 'only COPY target immediately initialized')
    canonical=[gf2_canonical(frame) for frame in w['frames']]
    ins=[r for r in sorted(mains) if canonical[w['initial'][r]]==canonical[w['initial'][1]]]
    outs=[r for r in sorted(mains) if canonical[w['final'][r]]==canonical[w['final'][112]]]
    need(ins==[1,773] and outs==[112,882],'independent exact cohort census')
    skel=[backward(w,r,True,mains) for r in outs]
    full=[backward(w,r,False,mains) for r in outs]
    block=[[row[c] for c in ins] for row in skel]
    endpoint=[[row[c] for c in ins] for row in full]
    need(block==[[F(-1,2),F(0)],[F(0),F(0)]],'reverse skeleton block')
    need(endpoint==[[F(0),F(0)],[F(0),F(0)]],'reverse actual zero block')
    # Kernel algebra for arbitrary invertible cohort pre/post factors.
    matrices=[];nonsingular=[]
    for a in product((-1,0,1),repeat=4):
        if a[0]*a[3]-a[1]*a[2]:nonsingular.append(a)
    rank_block=[[F(-1,2),F(0)],[F(0),F(0)]]
    cohort_checks=0
    for a in nonsingular:
        for b in nonsingular:
            q=[[sum(F(a[2*i+k])*rank_block[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
            q=[[sum(q[i][k]*F(b[2*k+j]) for k in range(2)) for j in range(2)] for i in range(2)]
            need(any(v for row in q for v in row),'nonzero block under invertible cohorts')
            need(q[0][0]*q[1][1]-q[0][1]*q[1][0]==0,'rank remains one')
            cohort_checks+=1
    cases={}
    for p in (2,3):
        group=[a for a in product(range(p),repeat=4) if (a[0]*a[3]-a[1]*a[2])%p]
        inverses={a:inv(a,p) for a in group}
        total=0
        for k in group:
            for l in group:
                skeleton=mm(l,k,p)
                for e in group:
                    # Independent outputs force prefix P=L^-1 E, suffix A=E K^-1.
                    pp=mm(inverses[l],e,p);aa=mm(e,inverses[k],p)
                    need((mm(aa,pp,p)==e)==(e==skeleton),'one-switch equivalence')
                    total+=1
        cases[str(p)]={'GL2_size':len(group),'triples':total}
    # A forbidden omission of cross-mode leakage would accept E=-I != R=I.
    e=-1;pfx=-1;sfx=-1;k=l=1;bc=-2
    need(sfx*pfx+bc==e and l*pfx==e and sfx*k==e and bc!=0,'nonzero cross-mode leakage control')
    return {'status':'PASS_INDEPENDENT_FIXED_CHANNEL_AND_ONE_SWITCH_REVIEW','source_sha256':PIN,
      'method':'reverse adjoint, independent GF2 basis reduction, exact modular matrix enumeration',
      'entry_cohort':ins,'exit_cohort':outs,
      'skeleton_block':[[str(x) for x in row] for row in block],
      'actual_block':[[str(x) for x in row] for row in endpoint],
      'skeleton_invertibility_alphabet_checked':True,
      'only_COPY_preceded_by_target_INIT':True,
      'rational_cohort_factor_pairs':cohort_checks,'one_switch_matrix_checks':cases,
      'controls':['E=-I,R=I passes diagonal output equations but fails BC=0'],
      'scope':'Finite source facts and finite matrix corroboration; universal statements independently reviewed in REVIEW.md.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);a=ap.parse_args()
    print(json.dumps(run(a.source),indent=2,sort_keys=True))
