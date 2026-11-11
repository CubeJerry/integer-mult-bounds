#!/usr/bin/env python3
"""Independent transposed modular source sweeps for the all-cut two-switch gate."""
from pathlib import Path
from fractions import Fraction
import argparse,gzip,hashlib,json
import numpy as np

PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
P=1000003

def need(ok,why):
    if not ok:raise ValueError(why)

def modular_rank(a):
    # Eliminate from the last columns and bottom rows, opposite the author order.
    a=a.copy(); last=len(a)-1; rank=0
    for col in range(a.shape[1]-1,-1,-1):
        choices=np.flatnonzero(a[:last+1,col])
        if not len(choices):continue
        pivot=int(choices[-1]);a[[pivot,last]]=a[[last,pivot]]
        a[last]=(a[last]*pow(int(a[last,col]),-1,P))%P
        if last:
            a[:last]=(a[:last]-a[:last,col,None]*a[last])%P
        rank+=1;last-=1
        if last<0:break
    return rank

def run(source,certificate):
    raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
    need(all(P%d for d in range(2,int(P**.5)+1)),'prime')
    w=json.loads(gzip.decompress(raw));events=w['program'];L=len(events)
    mains=sorted(set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']))
    pos={v:i for i,v in enumerate(mains)};N=len(mains);total=w['public']+w['owned_fields'];need(N==400,'main dimension')
    receipt=json.loads(certificate.read_text());cuts=sorted(set(receipt['cuts']));need(cuts[0]==0 and cuts[-1]==L,'full source coverage endpoints')
    cutset=set(cuts);coeff=[];forward_count=[0];backward_count=[0]
    for e in events:
        op,a=e[:2]
        scalar=Fraction(e[2] if op=='SCALE' else e[3]) if op in ('SCALE','ADD','COPY') else Fraction(0)
        need(scalar.denominator%P!=0,'denominator invertible mod prime')
        q=(scalar.numerator%P)*pow(scalar.denominator,-1,P)%P;coeff.append(q)
        if a in pos:
            need(op not in ('COPY','INIT','CLEAR'),'invertible skeleton alphabet')
            if op=='SCALE':need(q!=0,'nonzero modular main SCALE')
        if op in ('ADD','COPY'):need(a!=e[2],'nonself scalar event')
        forward_count.append(forward_count[-1]+int(op in ('ADD','COPY') and a in pos and e[2] not in pos))
        backward_count.append(backward_count[-1]+int(op in ('ADD','COPY') and a not in pos and e[2] in pos))
    base=np.zeros((N,total),dtype=np.int64)
    for r,j in pos.items():base[j,r]=1
    f=base.copy();prefix={0:N};skeleton=np.eye(N,dtype=np.int64)
    for i,e in enumerate(events):
        op,a=e[:2];q=coeff[i]
        if op in ('INIT','CLEAR'):f[:,a]=0
        elif op=='SCALE':
            f[:,a]=(q*f[:,a])%P
            if a in pos:skeleton[:,pos[a]]=(q*skeleton[:,pos[a]])%P
        elif op in ('ADD','COPY'):
            f[:,a]=(f[:,a]+q*f[:,e[2]])%P
            if a in pos and e[2] in pos:skeleton[:,pos[a]]=(skeleton[:,pos[a]]+q*skeleton[:,pos[e[2]]])%P
        if i+1 in cutset:prefix[i+1]=modular_rank(f[:,mains])
    residual_rank=modular_rank((f[:,mains]-skeleton)%P)
    s=base.copy();suffix={L:N}
    for i in range(L-1,-1,-1):
        e=events[i];op,a=e[:2];q=coeff[i]
        if op in ('INIT','CLEAR'):s[:,a]=0
        elif op=='SCALE':s[:,a]=(q*s[:,a])%P
        elif op in ('ADD','COPY'):s[:,e[2]]=(s[:,e[2]]+q*s[:,a])%P
        if i in cutset:suffix[i]=modular_rank(s[:,mains])
    need(prefix=={int(k):v for k,v in receipt['prefix_ranks'].items()},'all independently recomputed prefix ranks')
    need(suffix=={int(k):v for k,v in receipt['suffix_ranks'].items()},'all independently recomputed suffix ranks')
    bounds=[]
    for ranks,counts in ((prefix,forward_count),(suffix,backward_count)):
        local=[]
        for a,b in zip(cuts,cuts[1:]):
            distance=counts[b]-counts[a]
            local.append((ranks[a]+ranks[b]-distance+1)//2)
        bounds.append(min(local))
    need(residual_rank==275,'independent E-minus-R rank')
    need(sum(N-x for x in bounds)<residual_rank,'uniform two-switch obstruction')
    return {'status':'PASS_INDEPENDENT_ALL_CUT_TWO_SWITCH_EXCLUSION','source_sha256':PIN,
      'prime':P,'rank_method':'transposed state sweeps, reverse-pivot elimination; no author imports',
      'sample_cuts':len(cuts),'all_source_cuts':L+1,
      'all_sample_ranks_match':True,'prefix_all_cut_rank_lower':bounds[0],
      'suffix_all_cut_rank_lower':bounds[1],'residual_rank_lower':residual_rank,
      'max_nullity_sum':sum(N-x for x in bounds),
      'coefficient_denominators_invertible':True,'prime_verified_by_trial_division':True,
      'prefix_cross_updates':forward_count[-1],'suffix_cross_updates':backward_count[-1],
      'scope':'Canonical two global mode exchanges at source event cuts; no role-local codes, extra wrappers or changed itinerary.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);a=p.parse_args()
    print(json.dumps(run(a.source,a.certificate),indent=2,sort_keys=True))
