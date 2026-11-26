#!/usr/bin/env python3
"""Exact component checks. The finite word and transition theorems are in the notes."""

import itertools
import json
import random
from fractions import Fraction


def unpack_label(x, h, t):
    mask = (1 << t) - 1
    return tuple((x >> (t * k)) & mask for k in reversed(range(h * h)))


def canonical(v, w, d, t):
    h = 2 * d - 1
    left, right = list(v), list(w)
    affected = 0
    for a in range(h):
        diff = [i for i in range(a*h, (a+1)*h) if v[i] != w[i]]
        if diff:
            if len(diff) != d:
                return None
            affected += 1
            for i in diff[1:]:
                low = (1 << ((v[i] ^ w[i]).bit_length()-1)) - 1
                left[i] &= ~low
                right[i] &= ~low
    return (tuple(left),tuple(right)) if affected == d else None


def side_test(z, l, k, d, right=False):
    h = 2*d-1
    chosen = k if right else l
    for a in range(h):
        first = True
        for i in range(a*h,(a+1)*h):
            if l[i] == k[i] or first:
                if z[i] != chosen[i]:
                    return False
                if l[i] != k[i]:
                    first = False
            else:
                shift = (l[i]^k[i]).bit_length()-1
                if z[i] >> shift != chosen[i] >> shift:
                    return False
    return True


def adjacency(v,w,d):
    h = 2*d-1
    ds = [sum(v[a*h+i] != w[a*h+i] for i in range(h)) for a in range(h)]
    return v == w or (ds.count(d)==d and ds.count(0)==h-d)


def inverse(rows,n):
    a = [value | (1 << (n+i)) for i,value in enumerate(rows)]
    for j in range(n):
        i=next(i for i in range(j,n) if a[i]>>j&1)
        a[j],a[i]=a[i],a[j]
        for i in range(n):
            if i!=j and a[i]>>j&1:
                a[i]^=a[j]
    assert all(x&((1<<n)-1)==1<<i for i,x in enumerate(a))
    return [x>>n for x in a]


def restrict(row,idx):
    return sum((row>>c&1)<<j for j,c in enumerate(idx))


def rank_check(p,ncols):
    a,u=p.copy(),[1<<i for i in range(len(p))]
    used=set(); I=[]; J=[]
    for j in range(ncols):
        i=next((i for i in range(len(a)) if i not in used and a[i]>>j&1),None)
        if i is None:
            continue
        I.append(i);J.append(j);used.add(i)
        for k in range(len(a)):
            if k!=i and a[k]>>j&1:
                a[k]^=a[i];u[k]^=u[i]
        mask=sum(1<<i for i in used)
        assert all((x&~mask)==(0 if k in used else 1<<k) for k,x in enumerate(u))
    coeff=[restrict(u[i],I) for i in I]
    assert coeff==inverse([restrict(p[i],J) for i in I],len(I))
    assert all(a[i]==0 for i in range(len(a)) if i not in used)
    def mix(rows,x):
        out=0
        while x:
            low=x&-x;out^=rows[low.bit_length()-1];x-=low
        return out
    assert all(mix([p[k] for k in I],mix(coeff,restrict(row,J)))==row for row in p)
    return len(I)


def label_checks(rng):
    d,t=2,1; h=2*d-1; n=1<<(t*h*h)
    labels=[unpack_label(i,h,t) for i in range(n)]
    rows=[]; canon=0; edges=0
    for v in labels:
        row=0
        for j,w in enumerate(labels):
            c=canonical(v,w,d,t); good=adjacency(v,w,d)
            assert good==(v==w or c is not None)
            if good:
                row|=1<<j
            if c is not None:
                assert c==(v,w) and side_test(v,*c,d) and side_test(w,*c,d,right=True)
                canon+=1;edges+=1
        rows.append(row)
    assert rank_check(rows,n)==64
    matrices=0
    for nrows,ncols in ((1,1),(2,3),(3,3),(3,2)):
        for bits in range(1<<(nrows*ncols)):
            p=[(bits>>(i*ncols)) & ((1<<ncols)-1) for i in range(nrows)]
            rank_check(p,ncols);matrices+=1
    for _ in range(100):
        nrows,ncols=rng.randrange(1,20),rng.randrange(1,20)
        rank_check([rng.randrange(1<<ncols) for _ in range(nrows)],ncols);matrices+=1
    free_suffix_cases=0
    for d,t in ((2,2),(2,3),(4,3)):
        h=2*d-1;q=1<<t
        for _ in range(80):
            v=[rng.randrange(q) for _ in range(h*h)];w=v.copy()
            for a in rng.sample(range(h),d):
                for p in rng.sample(range(h),d):
                    i=a*h+p;w[i]=(v[i]+rng.randrange(1,q))%q
            l,k=canonical(v,w,d,t)
            assert canonical(l,k,d,t)==(l,k)
            for v0,w0 in ((v,w),(list(l),list(k))):
                assert side_test(v0,l,k,d) and side_test(w0,l,k,d,True)
            for _ in range(8):
                v0,w0=list(l),list(k)
                for a in range(h):
                    diff=[i for i in range(a*h,(a+1)*h) if l[i]!=k[i]]
                    for i in diff[1:]:
                        shift=(l[i]^k[i]).bit_length()-1
                        v0[i]+=rng.randrange(1<<shift);w0[i]+=rng.randrange(1<<shift)
                assert canonical(v0,w0,d,t)==(l,k) and adjacency(v0,w0,d)
                assert side_test(v0,l,k,d) and side_test(w0,l,k,d,True)
                bad=v0.copy(); pos=next(i for i in range(h*h) if l[i]!=k[i]);bad[pos]=k[pos]
                assert not side_test(bad,l,k,d)
                free_suffix_cases+=1
    return {'binary_outer_labels':n,'binary_directed_rectangles':canon,'binary_directed_edges':edges,
            'actual_binary_rank':64,'other_binary_matrices':matrices,'free_suffix_pairs':free_suffix_cases}


def modrat(x, mod):
    x=Fraction(x)
    return x.numerator*pow(x.denominator,-1,mod)%mod


def act(ops, values, mod, invert=False):
    """Act on column coordinates for the given basis-construction column ops."""
    x=values.copy()
    for kind,i,j,c in (ops if invert else reversed(ops)):
        if kind=='add':
            x[j]=(x[j]+(-1 if invert else 1)*modrat(c,mod)*x[i])%mod
        elif kind=='scale':
            factor=modrat(c,mod);factor=pow(factor,-1,mod) if invert else factor
            x[i]=factor*x[i]%mod
        else:
            x[i],x[j]=x[j],x[i]
    return x


def shear(target,source,c):
    return ('add',target,source,Fraction(c))


def scale(position,c):
    return ('scale',position,position,Fraction(c))


def butterfly(x,y):
    return [shear(x,y,1),scale(y,-2),shear(y,x,1),scale(x,Fraction(1,2)),scale(y,Fraction(1,2))]


class Geometry:
    def __init__(self,d,t,l,k):
        self.d=d; self.t=t; self.h=2*d-1;self.q=1<<t
        self.words=list(itertools.product(range(self.q),repeat=self.h))
        self.r=2+self.h*len(self.words);self.dim=2*self.r
        self.l=self.split(l);self.k=self.split(k)
        def sides(a,side):
            head=list(l if side==0 else k)
            for u in self.words:
                head[a*self.h:(a+1)*self.h]=u
                if side_test(head,l,k,d,right=(side==1)):
                    yield self.feature(a,u)
        self.sides=[[list(sides(a,z)) for a in range(self.h)] for z in (0,1)]
        self.stars=[]
        for side,anchor in enumerate((self.l,self.k)):
            for a,row in enumerate(self.sides[side]):
                base=self.feature(a,anchor[a])
                for v in row:
                    if v!=base:
                        self.stars.append((v,base))
        self.starset={v for v,_ in self.stars}
        a0=next(a for a in range(self.h) if self.l[a]!=self.k[a]);self.p=self.feature(a0,self.l[a0])
        self.C=[i for i in range(2,self.dim) if i!=self.p and i not in self.starset]

    def split(self,label):
        return [tuple(label[a*self.h:(a+1)*self.h]) for a in range(self.h)]

    def feature(self,a,word):
        v=0
        for letter in word:
            v=v*self.q+letter
        return 2+a*len(self.words)+v

    def coeff(self,col,v,sig):
        if col>=self.r:
            i=col-self.r
            a=int(i==0);b=int(i==1 or i in {self.feature(a,w) for a,w in enumerate(v)})
        else:
            a=0
            block,word=divmod(col-2,len(self.words))
            b=Fraction(-4,self.d)*int(sum(x!=y for x,y in zip(self.words[word],v[block]))==self.d)
        return Fraction(a+sig*b,2),Fraction(a-sig*b,2)

    def individual(self,v,sig):
        ops=[shear(1,self.feature(a,w),1) for a,w in enumerate(v)]+butterfly(0,1)
        if sig==-1:
            ops.append(('swap',0,1,1))
        for c in range(2,self.dim):
            x,y=self.coeff(c,v,sig)
            if x: ops.append(shear(c,0,-x))
            if y: ops.append(shear(c,1,-y))
        return ops

    def reserve(self,v,sig):
        ops=[shear(u,a,-1) for u,a in self.stars]
        for a,(l,k) in enumerate(zip(self.l,self.k)):
            if l!=k:
                il=self.feature(a,l);ik=self.feature(a,k)
                if il!=self.p: ops.append(shear(self.p,il,1))
                ops.append(shear(self.p,ik,-1))
        if sig==-1: ops.append(scale(self.p,-1))
        for a,w in enumerate(v):
            pos=self.feature(a,w)
            if pos in self.starset: ops.append(shear(self.p,pos,2))
        return ops

    def common(self):
        ops=[shear(u,a,-1) for u,a in self.stars]+[scale(1,-2)]
        for a,(l,k) in enumerate(zip(self.l,self.k)):
            ops.extend([shear(1,self.feature(a,l),-1),shear(1,self.feature(a,k),-1)])
        ops+=[scale(self.p,Fraction(1,2)),shear(self.p,1,Fraction(-1,2))]
        for a,(l,k) in enumerate(zip(self.l,self.k)):
            if l!=k:
                il=self.feature(a,l);ik=self.feature(a,k)
                if il!=self.p: ops.append(shear(self.p,il,Fraction(1,2)))
                ops.append(shear(self.p,ik,Fraction(-1,2)))
        return ops+butterfly(0,self.p)

    def lower(self,v,sig,values,mod,wrong=False):
        # Slot 0 is H, 1 is N, self.p is g. On output N and g belong to
        # the self.p and 1 columns, respectively, of the common basis.
        y=values.copy(); H,N=y[0],y[1]
        for c in self.C:
            a,b=self.coeff(c,v,sig)
            H-=modrat(a,mod)*y[c];N-=modrat(b,mod)*y[c]
        H%=mod;N%=mod; delta=(H+N if wrong else H-N)*pow(2,-1,mod)%mod
        for a,w in enumerate(v):
            u=self.feature(a,w)
            if u in self.starset: y[u]=(y[u]+sig*delta)%mod
        g=(y[self.p]+int(sig==-1)*delta)%mod
        y[0],y[self.p],y[1]=H,N,g
        return y


def geometry_checks(rng):
    cases=0;negative=0;largest=0
    d=2;t=2;h=2*d-1;q=1<<t
    for sample in range(8):
        l=[rng.randrange(q) for _ in range(h*h)];k=l.copy()
        for a in rng.sample(range(h),d):
            for p in rng.sample(range(h),d):
                i=a*h+p;k[i]=(l[i]+rng.randrange(1,q))%q
        l,k=canonical(l,k,d,t);g=Geometry(d,t,l,k);common=g.common()
        assert len(common)<=16*g.dim
        for sig in (1,-1):
            for _ in range(3):
                val=list(l if sig==1 else k)
                for a in range(h):
                    diff=[i for i in range(a*h,(a+1)*h) if l[i]!=k[i]]
                    for i in diff[1:]:
                        val[i]+=rng.randrange(1<<((l[i]^k[i]).bit_length()-1))
                v=g.split(val);arb=g.individual(v,sig);res=g.reserve(v,sig)
                assert len(arb)<=16*g.dim and len(res)<=16*g.dim
                largest=max(largest,len(arb),len(res),len(common))
                for f in (1,2,4):
                    mod=3**f;vals=[rng.randrange(mod) for _ in range(g.dim)]
                    via_i=act(arb,act(res,vals,mod),mod)
                    lower=g.lower(v,sig,vals,mod)
                    assert via_i==act(common,lower,mod)
                    assert act(res,act(arb,via_i,mod,True),mod,True)==vals
                    assert act(common,via_i,mod,True)==lower
                    if act(common,g.lower(v,sig,vals,mod,True),mod)!=via_i:
                        negative+=1
                    cases+=1
    assert negative>0
    return {'full_independent_vectors':cases,'ambient_dimension':g.dim,'largest_emitted_list':largest,
            'wrong_lower_sign_detected':negative}


def f4_mul(a,b):
    v=0
    for _ in range(2):
        if b&1: v^=a
        b>>=1;a<<=1
        if a&4: a^=7
    return v


def red(poly,divisor,d):
    while poly.bit_length()>2*d:
        i=(poly.bit_length()-1)//2;coef=poly>>(2*i)
        for j in range(d+1):
            poly^=f4_mul(coef,(divisor>>(2*j))&3)<<(2*(i-d+j))
    return poly


class Field:
    def __init__(self,e):
        self.e=e; self.q=4**e
        self.mod=next(self.q+f for f in range(self.q)
                      if all(red(self.q+f,4**j+g,j)!=0
                             for j in range(1,e//2+1) for g in range(4**j)))
        self.table=[[self.compute(a,b) for b in range(self.q)] for a in range(self.q)]
        self.inverse=[0]+[self.table[a].index(1) for a in range(1,self.q)]

    def compute(self,a,b):
        p=0
        for i in range(self.e):
            for j in range(self.e):
                p^=f4_mul(a>>(2*i)&3,b>>(2*j)&3)<<(2*(i+j))
        return red(p,self.mod,self.e)

    def mul(self,a,b):
        return self.table[a][b]

    def power(self,a,n):
        x=1
        for i in range(n): x=self.mul(x,a)
        return x


def gauss_field(rows,F):
    n=len(rows)
    a=[row.copy()+[int(i==j) for j in range(n)] for i,row in enumerate(rows)]
    for i in range(n):
        pivot=next(j for j in range(i,n) if a[j][i]);a[pivot],a[i]=a[i],a[pivot]
        inv=F.inverse[a[i][i]];a[i]=[F.mul(x,inv) for x in a[i]]
        for j in range(n):
            if j!=i:
                c=a[j][i];a[j]=[x^F.mul(c,y) for x,y in zip(a[j],a[i])]
    assert all(a[i][:n]==[int(i==j) for j in range(n)] for i in range(n))
    return [row[n:] for row in a]


def lagrange(J,gs,F,p,q):
    n=len(J);val=0
    if max(p,q)>=n: return 0
    for i,node in enumerate(J):
        coef=[1]+[0]*(n-1);den=1;degree=0
        for other in J:
            if other!=node:
                degree+=1
                for k in range(degree,-1,-1):
                    coef[k]=F.mul(other,coef[k]) ^ (coef[k-1] if k else 0)
                den=F.mul(den,node^other)
        weight=F.mul(gs[i],F.inverse[den]);weight=F.mul(weight,weight)
        val^=F.mul(weight,F.mul(coef[p],coef[q]))
    return val


def spectral_checks(rng):
    counts=cases=zero_g=0
    for e in (1,2,3):
        F=Field(e)
        for n in range(min(F.q,11)+1):
            for _ in range(4):
                nodes=rng.sample(range(F.q),n);g=[rng.randrange(4) for _ in nodes]
                v=[[F.power(x,k) for x in nodes] for k in range(n)]
                inv=gauss_field(v,F)
                cases+=1;zero_g+=g.count(0)
                for p in range(n+2):
                    for q in range(n+2):
                        ans=0
                        if max(p,q)<n:
                            for i,gg in enumerate(g):
                                ans^=F.mul(F.mul(inv[i][p],inv[i][q]),F.mul(gg,gg))
                        assert ans==lagrange(nodes,g,F,p,q);counts+=1
    return {'independent_vandermonde_inverses':cases,'matrix_entries_and_padding':counts,
            'containing_set_zeros':zero_g,'field_orders':[4,16,64]}


if __name__=='__main__':
    rng=random.Random(20261126)
    report={'label_and_rank':label_checks(rng),'geometry':geometry_checks(rng),'spectral':spectral_checks(rng)}
    print(json.dumps(report,indent=2))
