#!/usr/bin/env python3
"""Independent native restriction distance and matrix cancellation controls.
@CubeJerry/OpenAI; Apache-2.0. No author checker imported.
"""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
def need(ok,msg):
    if not ok:raise ValueError(msg)
def basis(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j not in piv:piv[j]=x;break
            x^=piv[j]
    return list(piv.values())
def span(rows):
    out={0}
    for x in rows:out|={v^x for v in tuple(out)}
    return out
M=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
def main():
    p=argparse.ArgumentParser()
    for name in ['native','package','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='57cd33afbd532d8b0b95522c3656f15f6bb4222c6a19008bea6b0768feac82e9','proof pin')
    n=json.loads(gzip.decompress(raw));R=[]
    for i in range(111):R.append(list(map(F,n['frames'][str(n['start'][i])]['B'][0])))
    K=[sum(int(i==j or sum(x*y for x,y in zip(R[i],R[j]))==0)<<j for j in range(111)) for i in range(111)]
    C=span(basis(K));need(len(C)==512,'exact canonical dimension9')
    full=(1<<111)-1;distances=[];example=None
    for i in range(111):
        Z=full^K[i];restriction={word&Z for word in C}
        need(len(restriction)==256 and {word for word in C if not word&Z}=={0,K[i]},'restricted rank8 and exact canonical kernel')
        minimum=min(word.bit_count() for word in restriction if word);distances.append(minimum)
        if minimum==18 and example is None:
            word=min(word for word in restriction if word.bit_count()==18);points=[j for j in range(111) if word>>j&1]
            first=sum(1<<j for j in points[:9]);second=word^first
            need(first not in restriction and second not in restriction and first^second in restriction,'two nine-point nonzero residuals coincide')
            example=dict(receiver=i,restriction_word=points,first=points[:9],second=points[9:])
    need(dict(Counter(distances))=={18:7,19:24,20:52,21:16,22:11,23:1},'all111 exact minimum distances')
    controls={}
    for V,field in [(2,4),(3,2),(4,2)]:
        checked=0;erasures=0
        for t in range(V):
            for c in range(1,field):
                for u in itertools.product(range(field),repeat=V):
                    base=[[int(i==j)^(M[c][u[i]] if j==t else 0) for j in range(V)] for i in range(V)]
                    for s in range(V):
                        for v in itertools.product(range(field),repeat=V):
                            checked+=1
                            erased=all((base[i][j]^(v[i] if j==s else 0))==0 for i in range(V) for j in range(V))
                            if erased:
                                erasures+=1
                                need(V==2 and s==1-t and all(M[c][u[i]]==int(i==t) for i in range(V)) and all(v[i]==int(i==s) for i in range(V)),'only proved opposite-channel width2 cancellation')
        need((erasures==6 if V==2 else erasures==0),'exact cancellation boundary')
        controls[str((V,field))]=dict(checked=checked,erasures=erasures)
    i=next(j for j in range(111) if K[j].bit_count()-1==55);contacts=[j for j in range(111) if j!=i and K[i]>>j&1];T=contacts[:3]
    need(len([j for j in contacts if j not in T])==52,'width2 true single-saving support control')
    report=dict(status='PASS_INDEPENDENT_DISJOINT_SPARSE_GATE_PREMISES',canonical_words=len(C),restricted_rank=8,forbidden_distance_histogram=dict(Counter(distances)),nine_point_threshold_counterexample=example,matrix_controls=controls,width2_positive_control=dict(receiver=i,three_deleted_contacts=T,foreign_support=52),scope='Finite exact source premises plus separately reviewed all-field sparse-residual proof. Overlapping components and arbitrary halfclass linear combinations remain outside the theorem; no new kappa.')
    a.output.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
if __name__=='__main__':main()
