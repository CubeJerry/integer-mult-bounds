#!/usr/bin/env python3
"""Independent finite premises for the all-width canonical pair gate."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(c,m):
    if not c:raise ValueError(m)
def basis(rows):
    out={}
    for w in rows:
        while w:
            p=w.bit_length()-1
            if p in out:w^=out[p]
            else:out[p]=w;break
    return list(out.values())
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def rank(rows,p=103):
    a=[[int(x)%p for x in r]for r in rows];k=0
    for j in range(len(a[0]) if a else 0):
        t=next((i for i in range(k,len(a))if a[i][j]),None)
        if t is None:continue
        a[k],a[t]=a[t],a[k];z=pow(a[k][j],-1,p);a[k]=[x*z%p for x in a[k]]
        for i in range(k+1,len(a)):
            z=a[i][j];a[i]=[(x-z*y)%p for x,y in zip(a[i],a[k])]
        k+=1
    return k
def run(repo,cert):
    raw=(repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'actual source');s=json.loads(gzip.decompress(raw));R=[]
    for i in range(111):
        r=list(map(F,s['frames'][str(s['start'][i])]['B'][0]))
        if sum(bool(x)for x in r)==1:r=[2*x for x in r]
        need(dot(r,r)==4 and all(x.denominator==1 for x in r),'integral normalized norm4');R.append(tuple(map(int,r)))
    K=[sum(int(i==j or dot(r,v)==0)<<j for j,v in enumerate(R))for i,r in enumerate(R)];C=basis(K);need(len(C)==9,'canonical rank9');allbits=(1<<111)-1
    pair_hist=Counter();exclusive_hist=Counter();pair_common_max=0;supports={}
    for i,j in itertools.combinations(range(111),2):
        forbidden=allbits^(K[i]|K[j]);r=len(basis(v&forbidden for v in C));need(r==7 and len(basis([K[i],K[j]]))==2,'pair canonical restriction kernel exactly two');pair_hist[r]+=1
        if dot(R[i],R[j])==0:pair_common_max=max(pair_common_max,(K[i]&K[j]).bit_count())
        else:
            need(abs(dot(R[i],R[j]))==2,'root nonorthogonal angle')
            for a,b in ((i,j),(j,i)):
                S=[k for k in range(111)if k!=a and K[a]>>k&1 and not(K[b]>>k&1)];supports[a,b]=S
                rr=rank([R[k]for k in S]);need(rr==7 and all(dot(R[a],R[k])==0 for k in S),'every ordered exclusive support spans facet');exclusive_hist[rr]+=1
    need(sum(pair_hist.values())==6105 and sum(exclusive_hist.values())==5740 and pair_common_max<=32,'complete pair census')
    author=json.loads(cert.read_text());matching=author['matching'];need(len(matching)==55 and len({i for pair in matching for i in pair})==110,'55 disjoint pairs')
    witnesses=[]
    for i,j in matching:
        valid=[]
        for a,b in ((i,j),(j,i)):
            need((a,b)in supports,'matching pair nonorthogonal');S=supports[a,b]
            if len(S)!=27:continue
            pivot=next(k for k,x in enumerate(R[a])if x);coords=[k for k in range(8)if k!=pivot]
            lift=[[R[k][u]*R[k][v]for u,v in itertools.combinations_with_replacement(coords,2)]for k in S]
            if rank(lift)!=27:continue
            # A codimension-one quadratic kernel, with the known rank-seven form.
            need(all(dot(R[b],R[k])**2==dot(R[k],R[k]) for k in S),'exclusive split-norm vanishing')
            need(F(dot(R[b],R[b]))-F(dot(R[a],R[b])**2,dot(R[a],R[a]))==3,'projected normal norm3; form eigenvalues2,-1^6')
            valid.append((a,b))
        need(valid,'each matching edge has an irreducible exclusive end');witnesses.append({'pair':[i,j],'certified_end':list(valid[0])})
    need(rank([[1,0,0],[0,1,0]])==2,'rank routine boundary')
    bad=matching+[matching[0]];need(len({i for pair in bad for i in pair})!=2*len(bad),'duplicate matching-edge negative control')
    return {'status':'PASS_INDEPENDENT_CANONICAL_PAIR_GATE_PREMISES','source_sha256':PIN,'pair_restriction_rank_histogram':dict(pair_hist),'ordered_exclusive_real_rank_histogram':dict(exclusive_hist),'quadratic_minor_prime':103,'matching':witnesses,'matching_size':55,'orthogonal_pair_closed_intersection_max':pair_common_max,'all_width_argument':'reviewed separately; dimE<2V forces pairwise intersections of positive-saving row V-planes','result_chi_at_least':165,'new_complete_kappa':False}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=run(a.repo,a.certificate);a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items()if k!='matching'}))
