#!/usr/bin/env python3
"""Exact rational group-algebra controls for the ordinary capacity theorem."""
import argparse,json
from fractions import Fraction as Q

def need(ok,why):
    if not ok:raise ValueError(why)

class Algebra:
    def __init__(self,size,product):
        self.n=size;self.product=product;self.zero=(Q(0),)*size;self.one=self.unit(0)
    def unit(self,g):return tuple(Q(int(i==g))for i in range(self.n))
    def add(self,*xs):return tuple(sum(x[i]for x in xs)for i in range(self.n))
    def scale(self,c,x):return tuple(Q(c)*a for a in x)
    def mul(self,x,y):
        out=[Q(0)]*self.n
        for g,a in enumerate(x):
            for h,b in enumerate(y):out[self.product(g,h)]+=a*b
        return tuple(out)
    def plus(self,g):
        need(g!=0 and self.product(g,g)==0,'nonidentity projective involution required')
        return self.scale(Q(1,2),self.add(self.one,self.unit(g)))
    def sub(self,x,y):return self.add(x,self.scale(-1,y))
    def regular(self,x):
        M=[[Q(0)]*self.n for _ in range(self.n)]
        for g,a in enumerate(x):
            for h in range(self.n):M[self.product(g,h)][h]+=a
        return M
    def mm(self,A,B):return [[self.add(*(self.mul(a,b)for a,b in zip(row,col)))for col in zip(*B)]for row in A]
    def identity(self,n):return [[self.one if i==j else self.zero for j in range(n)]for i in range(n)]
    def diagonal(self,entries):return [[entries[i]if i==j else self.zero for j in range(len(entries))]for i in range(len(entries))]

def rank(A):
    a=[list(map(Q,r))for r in A];k=0
    for j in range(len(a[0])if a else 0):
        i=next((i for i in range(k,len(a))if a[i][j]),None)
        if i is None:continue
        a[k],a[i]=a[i],a[k];q=a[k][j];a[k]=[x/q for x in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                q=a[i][j];a[i]=[x-q*y for x,y in zip(a[i],a[k])]
        k+=1
    return k

def stats(A,P):
    n=len(P);m=len(P[0]);blocks=[[A.regular(x)for x in row]for row in P]
    reg=[[blocks[i][j][a][b]for j in range(m)for b in range(A.n)]for i in range(n)for a in range(A.n)]
    eps=[[sum(x)for x in row]for row in P];r=rank(reg)
    return {'regular_rank':r,'regular_normalized_rank':str(Q(r,A.n)),'augmentation_rank':rank(eps)}

def main():
    from pathlib import Path
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    G=Algebra(4,lambda g,h:g^h);p=[G.plus(i)for i in [1,2,3]];m=[G.sub(G.one,x)for x in p]
    for x in p+m:need(G.mul(x,x)==x,'literal idempotent')
    plus=stats(G,G.diagonal(p[:2]));minus=stats(G,G.diagonal(m[:2]))
    need(plus=={'regular_rank':4,'regular_normalized_rank':'1','augmentation_rank':2},'two-plus mismatch')
    need(minus['augmentation_rank']==0,'minus has no trivial character')
    P=G.diagonal([p[0],m[0]]);C=[[p[0]],[m[0]]];D=[[p[0],m[0]]]
    need(G.mm(D,C)==G.identity(1) and G.mm(P,C)==C,'balanced split injection')
    route=[[p[0],m[0]],[m[0],p[0]]];need(G.mm(route,route)==G.identity(2),'controlled-route inverse')
    e=G.scale(Q(1,4),G.add(*(G.unit(i)for i in range(4))))
    inv=G.sub(G.one,G.scale(Q(2,3),e));summed=G.add(*p)
    need(summed==G.add(G.one,G.scale(2,e)),'three-plus sum')
    need(G.mul(inv,summed)==G.one and G.mul(summed,inv)==G.one,'actual aggregate inverse')
    C3=[[x]for x in p];D3=[[G.mul(inv,x)for x in p]];P3=G.diagonal(p)
    need(G.mm(D3,C3)==G.identity(1) and G.mm(P3,C3)==C3,'three-plus sharp injection')
    need(stats(G,P3)=={'regular_rank':6,'regular_normalized_rank':'3/2','augmentation_rank':3},'sharp strict capacity')
    H=Algebra(3,lambda g,h:(g+h)%3);avg=H.scale(Q(1,3),H.add(*(H.unit(i)for i in range(3))))
    need(H.mul(avg,avg)==avg,'order-three average')
    cycle=stats(H,H.diagonal([avg]*3));need(cycle=={'regular_rank':3,'regular_normalized_rank':'1','augmentation_rank':3},'cyclic-plus mismatch')
    cm=H.sub(H.one,avg);need(sum(cm)==0 and H.mul(cm,cm)==cm,'cyclic complement')
    try:G.plus(0)
    except ValueError as ex:identity_control=str(ex)
    else:raise ValueError('identity accepted as nonidentity')
    def permute(x,perm):
        bits=[(x>>(3-i))&1 for i in range(4)]
        return sum(bits[perm[i]]<<(3-i)for i in range(4))
    swaps={name:[permute(x,perm)for x in range(16)]for name,perm in {'ab':[1,0,2,3],'ad':[3,1,2,0],'cd':[0,1,3,2]}.items()}
    for s in swaps.values():
        need(s!=list(range(16)) and all(s[s[i]]==i for i in range(16)),'literal nonscalar involution')
        need(sum(s[i]==i for i in range(16))==8,'literal swap trace')
    physical=[{'width':v,'bank_dimension':16**v,'single_plus_rank':(16**v+8**v)//2,'two_plus_dimension_excess':8**v}for v in range(1,5)]
    encode=lambda x:[str(c)for c in x]
    controls={'group':'C2 x C2, XOR product','mixed_C':[encode(x[0])for x in C],'mixed_D':[encode(x)for x in D[0]],'mixed_route':[[encode(x)for x in row]for row in route],'three_plus_C':[encode(x[0])for x in C3],'three_plus_D':[encode(x)for x in D3[0]],'aggregate_inverse':encode(inv),'literal_swap_permutations':swaps}
    result={'status':'PASS_ORDINARY_REGULAR_CAPACITY_AND_SHARP_CONTROLS','two_plus':plus,'two_minus':minus,'balanced_mixed':stats(G,P),'three_plus_sharp':stats(G,P3),'three_cyclic_plus':cycle,'identity_control_rejected':identity_control,'spectator_physical_rank_controls':physical,'scope':'Written regular dimension/augmentation theorem; fixed finite root-four catalogue, sufficiently large faithful widths divisible by4.','sharp_control':'Three plus sectors contain one ordinary bank; balanced plus/minus pair exactly contains one.','unpriced_controls':True,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True)
    for name,data in [('RESULT.json',result),('ALGEBRAIC-CONTROLS.json',controls)]:(a.out/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
