#!/usr/bin/env python3
"""Exact rational checks for the explicit hyperbolic address realization."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def plus(a,b,c=F(1)):
    z=dict(a)
    for i,v in b.items():
        z[i]=z.get(i,F(0))+c*v
        if not z[i]: del z[i]
    return z

def times(a,c): return {i:v*c for i,v in a.items() if v*c}
def unit(i): return {i:F(1)}

def scalar(a,b): return sum((v*b.get(i,F(0)) for i,v in a.items()),F(0))

class Geometry:
    def __init__(self,d,q):
        self.d=d; self.h=2*d-1; self.q=q
        self.words=list(product(range(q),repeat=self.h))
        self.widx={w:i for i,w in enumerate(self.words)}
        self.n0=len(self.words); self.r=2+self.h*self.n0; self.D=2*self.r
        self.C=[i for i in range(self.D) if i not in (0,1)]
    def fi(self,a,w): return 2+a*self.n0+self.widx[w]
    def decode(self,i):
        a,j=divmod(i-2,self.n0); return a,self.words[j]
    def far(self,u,v): return sum(x!=y for x,y in zip(u,v))==self.d
    def dot(self,x,y):
        z=F(2)*(x.get(0,0)*y.get(0,0)+x.get(1,0)*y.get(1,0))
        for i,a in x.items():
            if i>=self.r:
                z+=a*y.get(i-self.r,0)
            else:
                z+=a*y.get(i+self.r,0)
        xf=[(i,a) for i,a in x.items() if 2<=i<self.r]
        yf=[(i,a) for i,a in y.items() if 2<=i<self.r]
        for i,a in xf:
            p,u=self.decode(i)
            for j,b in yf:
                t,v=self.decode(j)
                if p==t and self.far(u,v): z-=F(4,self.d)*a*b
        return z
    def av(self,v): return {self.fi(a,w):F(1) for a,w in enumerate(v)}
    def zv(self,v): return plus(unit(1),self.av(v))
    def pair(self,v):
        z=self.zv(v)
        return times(plus(unit(0),z),F(1,2)),times(plus(unit(0),z,F(-1)),F(1,2))
    def project(self,v,w):
        z=self.zv(v)
        return plus(plus(w,unit(0),-self.dot(w,unit(0))/2),z,-self.dot(w,z)/2)
    def reserve_coords(self,v,w):
        z=plus(plus(w,unit(0),-w.get(0,0)),self.zv(v),-w.get(1,0))
        assert not z.get(0,0) and not z.get(1,0)
        return z
    def inverse_layout(self,v,w):
        x,y=self.pair(v); ax=self.dot(x,w); ay=self.dot(y,w)
        rem=plus(plus(w,x,-ax),y,-ay)
        return self.reserve_coords(v,rem),ax,ay
    def forward_layout(self,v,c,ax,ay):
        x,y=self.pair(v)
        return plus(plus(self.project(v,c),x,ax),y,ay)

G=Geometry(2,4)
innerL=[(0,a,0) for a in (0,1)]
innerK=[(1,a,0) for a in (2,3)]
common=(2,2,2)
Ls=[innerL,innerL,[common]]; Ks=[innerK,innerK,[common]]
labelsL=list(product(*Ls)); labelsK=list(product(*Ks))
l=tuple(z[0] for z in Ls); k=tuple(z[0] for z in Ks)
star_specs=[]
for side,sets,anchor in [('L',Ls,l),('K',Ks,k)]:
    for a,words in enumerate(sets):
        for w in words[1:]:
            star_specs.append((side,a,w,G.fi(a,w),G.fi(a,anchor[a])))
stars=[plus(unit(p),unit(a),F(-1)) for _,_,_,p,a in star_specs]
g=times(unit(1),F(-2))
avec={}
for a in range(G.h):
    g=plus(plus(g,unit(G.fi(a,l[a])),F(-1)),unit(G.fi(a,k[a])),F(-1))
    avec=plus(plus(avec,unit(G.fi(a,l[a]))),unit(G.fi(a,k[a])),F(-1))
anchor=G.fi(0,l[0])
pivots=[p for _,_,_,p,_ in star_specs]
CR=[i for i in G.C if i not in pivots+[anchor]]
assert len(CR)+len(stars)+1 == G.D-2

checks={'gram_blocks':0,'isotropic_pairs':0,'individual_layout_basis_vectors':0,
        'reserve_inverse_basis_vectors':0,'reserve_geometric_columns':0,'modular_scalings':0}
neg={'wrong_cross_sign':0,'wrong_endpoint_reserve_sign':0}
endpoints=[('L',v) for v in labelsL]+[('K',v) for v in labelsK]
for side,v in endpoints:
    xv,yv=G.pair(v)
    for side2,w in endpoints:
        xw,yw=G.pair(w)
        count=sum(G.far(a,b) for a,b in zip(v,w))
        assert G.dot(xv,xw)==1-F(count,G.d)
        assert G.dot(xv,yw)==F(count,G.d)
        assert G.dot(yv,xw)==F(count,G.d)
        assert G.dot(yv,yw)==1-F(count,G.d)
        # Rectangle orientations give the same identity Gram block.
        aa,bb=(xv,yv) if side=='L' else (yv,xv)
        cc,dd=(xw,yw) if side2=='L' else (yw,xw)
        assert [G.dot(aa,cc),G.dot(aa,dd),G.dot(bb,cc),G.dot(bb,dd)]==[1,0,0,1]
        checks['gram_blocks']+=1
    for e in stars+[g]:
        assert G.dot(e,xv)==G.dot(e,yv)==0
        for f in stars+[g]:
            assert G.dot(e,f)==0
            checks['isotropic_pairs']+=1
    for i in range(G.D):
        w=unit(i)
        c,ax,ay=G.inverse_layout(v,w)
        assert G.forward_layout(v,c,ax,ay)==w
        checks['individual_layout_basis_vectors']+=1
    desired=times(avec,F(1 if side=='L' else -1))
    active=[]
    for j,(ss,a,w,_,_) in enumerate(star_specs):
        if ss==side and v[a]==w:
            active.append(j); desired=plus(desired,stars[j],F(2))
    assert G.reserve_coords(v,g)==desired
    wrong=times(avec,F(-1 if side=='L' else 1))
    for j in active: wrong=plus(wrong,stars[j],F(2))
    neg['wrong_endpoint_reserve_sign']+=wrong!=desired
    for st in stars:
        assert G.reserve_coords(v,st)==st and G.project(v,st)==st
        checks['reserve_geometric_columns']+=1
    assert G.project(v,desired)==g
    checks['reserve_geometric_columns']+=1
    # Explicit reserve inverse, then forward, on every old coordinate basis.
    for i in G.C:
        old=unit(i); residual=dict(old); beta=[]
        for st,(_,_,_,p,_) in zip(stars,star_specs):
            b=residual.get(p,F(0)); beta.append(b); residual=plus(residual,st,-b)
        gamma=residual.get(anchor,F(0)); residual=plus(residual,avec,-gamma)
        assert all(j in CR for j in residual)
        endpoint_gamma=gamma if side=='L' else -gamma
        for j in active: beta[j]-=2*endpoint_gamma
        restored=dict(residual)
        for b,st in zip(beta,stars): restored=plus(restored,st,b)
        restored=plus(restored,desired,endpoint_gamma)
        assert restored==old
        checks['reserve_inverse_basis_vectors']+=1
    # A deliberately wrong cross vector need not be orthogonal.
    wrongg=plus(g,unit(1),F(4))
    neg['wrong_cross_sign']+=bool(G.dot(wrongg,xv) or G.dot(wrongg,yv))

# Modular diagonal units are powers of two; no radix search is needed.
for f in range(1,6):
    mod=3**f
    for c in (F(-2),F(-1),F(1,2),F(-1,2),F(2),F(1,4)):
        val=(c.numerator*pow(c.denominator,-1,mod))%mod
        assert len({val*x%mod for x in range(mod)})==mod
        checks['modular_scalings']+=1
assert all(neg.values())
result={'status':'passed','arithmetic':'exact fractions plus integer modular arithmetic',
        'parameters':{'d':G.d,'q':G.q,'h':G.h,'inner_words':G.n0,'ambient_dimension':G.D,
                      'source_endpoints':len(labelsL),'destination_endpoints':len(labelsK),'difference_dimension':len(stars)+1},
        'checks':checks,'negative_controls':neg,
        'scope':'Explicit Gram, pair complements, rectangle isotropy, reserve-only inverse, fixed odd radix units. No full tape router or multiplier execution.'}
Path(__file__).with_name('dyadic-geometry-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
