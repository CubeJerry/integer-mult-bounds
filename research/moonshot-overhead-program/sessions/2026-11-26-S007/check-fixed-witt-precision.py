"""Length-three ghosts, Hasse transport and literal monomial decoding vs direct Z/8."""
from functools import lru_cache
from itertools import product
from math import comb
from random import Random
import json


def rem(a,g):
    while a.bit_length()>=g.bit_length():
        a ^= g<<(a.bit_length()-g.bit_length())
    return a


def fmul(a,b,g):
    c=0
    while a:
        if a&1:
            c ^= b
        a >>= 1
        b <<= 1
    return rem(c,g)


class W3:
    def __init__(self,g):
        self.g=g
        self.d=g.bit_length()-1
        self.k=1<<self.d
        self.m=[[fmul(i,j,g) for j in range(self.k)] for i in range(self.k)]
        self.sq=[self.m[i][i] for i in range(self.k)]
        self.rt={a:i for i,a in enumerate(self.sq)}

    def add(self,a,b):
        x,y,z=a
        u,v,w=b
        m,s=self.m,self.sq
        xu=m[x][u]
        high=m[xu][s[x]^y^s[u]^v]^m[y][v]^z^w
        return x^u,xu^y^v,high

    def mul(self,a,b):
        x,y,z=a
        u,v,w=b
        m,s=self.m,self.sq
        x2,u2=s[x],s[u]
        high=m[s[x2]][w]^m[m[x2][y]][m[u2][v]]^m[s[y]][s[v]]^m[z][s[u2]]
        return m[x][u],m[x2][v]^m[y][u2],high

    def power(self,a,n):
        z=(1,0,0)
        while n:
            if n&1:
                z=self.mul(z,a)
            a=self.mul(a,a)
            n//=2
        return z

    def sub(self,a,b):
        return self.add(a,self.mul((1,1,1),b))

    def inv(self,a):
        z=self.power(a,(self.k-1)*self.k*self.k-1)
        assert self.mul(z,a)==(1,0,0)
        return z

    def divide2(self,a):
        assert not a[0]
        return (self.rt[a[1]],self.rt[a[2]],0)

    def horner(self,coeff,x):
        v=(0,0,0)
        for c in reversed(coeff):
            v=self.add(self.mul(v,x),(c&1,(c>>1)&1,(c>>2)&1))
        return v


def sqpoly(a):
    if not a:
        return []
    z=[0]*(2*len(a)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(a):
            z[i+j]+=x*y
    return z


@lru_cache(maxsize=8192)
def ghosts(coeff,precision=3):
    """Exact integer universal division; direct output is its binary reductions."""
    cs=[]
    for j in range(precision):
        d=1<<j
        row=[0]*(d*(len(coeff)-1)+1) if coeff else []
        for i,x in enumerate(coeff):
            row[d*i]=x
        for h,c in enumerate(cs):
            p=c
            for _ in range(j-h):
                p=sqpoly(p)
            for i,v in enumerate(p):
                row[i]-=(1<<h)*v
        assert all(n%d==0 for n in row)
        cs.append([n//d for n in row])
    return tuple(sum((n&1)<<i for i,n in enumerate(row)) for row in cs)


@lru_cache(maxsize=8192)
def hasse(coeff,h):
    return tuple((comb(i,h)*coeff[i])%8 for i in range(h,len(coeff)))


def taylor(r,coeff,step):
    c=(0,0,0)
    for j in (2,1,0):
        teich=tuple(rem(p,r.g) for p in ghosts(hasse(coeff,j)))
        c=r.add(r.mul(c,step),teich)
    return c


def root(r):
    g=tuple((r.g>>i)&1 for i in range(r.d+1))
    x=(rem(2,r.g),0,0)
    y=(0,0,0)
    for _ in range(2):
        value=taylor(r,g,y)
        deriv=taylor(r,hasse(g,1),y)
        y=r.sub(y,r.mul(value,r.inv(deriv)))
    a=r.add(x,y)
    assert r.horner(g,a)==(0,0,0) and a[0]==x[0]
    return a,y


def decode(r,w,y):
    out=[0]*r.d
    for step in range(3):
        binary=tuple((w[0]>>i)&1 for i in range(r.d))
        for i,c in enumerate(binary):
            out[i]|=c<<step
        w=r.divide2(r.sub(w,taylor(r,binary,y)))
    return out


def direct(coeff,g):
    d=g.bit_length()-1
    a=list(coeff)+[0]*d
    for i in reversed(range(d,len(a))):
        v=a[i]
        for j in range(d):
            if g>>j&1:
                a[i-d+j]=(a[i-d+j]-v)%8
    return a[:d]


def factors(b):
    fs=[]
    for d in range(1,b+1):
        if b%d:
            continue
        for g in range(1<<d,2<<d):
            if all(rem(g,h) for i in range(1,d//2+1) for h in range(1<<i,2<<i)):
                fs.append(g)
    return fs


def main():
    rng=Random(761415)
    c=dict(input_polynomials=0,coordinate_horner_checks=0,literal_factor_checks=0,
           proper_nonprime_subfield_checks=0,detected_dropped_third_ghost=0,
           detected_teich_root_substitution=0,failures_without_second_hasse_order=0,
           full_mod8_inputs_b2=0)
    for b in (1,2,3,4,6):
        n=1<<b
        if b<=2:
            inputs=product(range(8),repeat=n)
        else:
            sample=[tuple((v if i==j else 0) for i in range(n)) for j in range(n) for v in (1,2,7)]
            sample += [tuple(rng.randrange(8) for j in range(n)) for _ in range(32)]
            inputs=sample
        rings=[]
        for g in factors(b):
            r=W3(g)
            a,y=root(r)
            rings.append((r,a,y))
        for F in inputs:
            c['input_polynomials']+=1
            c['full_mod8_inputs_b2']+=int(b==2)
            global_coordinates=ghosts(F)
            for r,a,y in rings:
                teich=tuple(rem(p,r.g) for p in global_coordinates)
                z=(rem(2,r.g),0,0)
                assert r.horner(F,z)==teich
                c['coordinate_horner_checks']+=1
                actual=taylor(r,F,y)
                assert actual==r.horner(F,a)
                c['coordinate_horner_checks']+=1
                result=decode(r,actual,y)
                assert result==direct(F,r.g)
                c['literal_factor_checks']+=1
                c['proper_nonprime_subfield_checks']+=int(1<r.d<b)
                c['detected_dropped_third_ghost']+=int(teich[2]!=0)
                c['detected_teich_root_substitution']+=int(teich!=actual)
                first=tuple(rem(p,r.g) for p in ghosts(hasse(F,1)))
                c['failures_without_second_hasse_order']+=int(r.add(teich,r.mul(y,first))!=actual)
    for name in ('detected_dropped_third_ghost','detected_teich_root_substitution',
                 'failures_without_second_hasse_order','proper_nonprime_subfield_checks'):
        assert c[name]>0
    print(json.dumps(c,indent=2,sort_keys=True))




def fold(v,q,mod):
    row=[0]*q
    for i,x in enumerate(v):
        j=0 if i==0 else 1+(i-1)%(q-1)
        row[j]=(row[j]+x)%mod
    return row


def folded_ghosts(coeff,q,H):
    previous=[]
    for j in range(H):
        charge=1<<j
        mod=2*charge
        row=[0]*q
        for i,c in enumerate(coeff):
            dest=0 if i==0 else 1+(charge*i-1)%(q-1)
            row[dest]=(row[dest]+c)%mod
        for h,old in enumerate(previous):
            z=list(old)
            for _ in range(j-h):
                z=fold(sqpoly(z),q,mod)
            row=[(a-(1<<h)*v)%mod for a,v in zip(row,z)]
        assert all(a%charge==0 for a in row)
        previous.append([a//charge for a in row])
    return tuple(sum(x<<i for i,x in enumerate(v)) for v in previous)


def binary_crt(x,gs,q):
    def product_poly(a,b):
        z=0
        while a:
            if a&1: z ^= b
            a >>= 1
            b <<= 1
        return z
    P=(1<<q)^2
    f=0
    for a,g in zip(x,gs):
        v=P
        u=0
        while v.bit_length()>=g.bit_length():
            j=v.bit_length()-g.bit_length()
            u^=1<<j
            v^=g<<j
        assert not v
        inv=next(h for h in range(1,1<<(g.bit_length()-1)) if fmul(u,h,g)==1)
        f^=product_poly(u,fmul(a,inv,g))
    assert f.bit_length()<=q
    return tuple((f>>i)&1 for i in range(q))


def inverse_lift(residues,gs,fields,q):
    current=[list(v) for v in residues]
    f=[0]*q
    for step in range(3):
        low=[sum((x&1)<<i for i,x in enumerate(v)) for v in current]
        b=binary_crt(low,gs,q)
        for i,x in enumerate(b):
            f[i]|=x<<step
        for j,(r,a,y) in enumerate(fields):
            correction=decode(r,taylor(r,b,y),y)
            diff=[(u-v)%(8>>step) for u,v in zip(current[j],correction)]
            assert all(v%2==0 for v in diff)
            current[j]=[v//2 for v in diff]
    return tuple(f)


def extra_tests():
    counts=dict(folded_ghost_rows=0,positive_degree_stress=0,arbitrary_inverse_inputs=0,
                inverse_checked_factor_words=0)
    rng=Random(605717)
    for q in (4,8,16):
        for H in range(1,6):
            for _ in range(10):
                a=tuple(rng.randrange(1<<H) for j in range(q))
                raw=ghosts(a,H)
                reduced=tuple(sum(x<<i for i,x in enumerate(fold(
                    [(v>>j)&1 for j in range(v.bit_length())],q,2))) for v in raw)
                assert folded_ghosts(a,q,H)==reduced
                counts['folded_ghost_rows']+=H
            a=(1,)+(0,)*(q-2)+(1,)
            for j,v in enumerate(ghosts(a,H)):
                if j:
                    assert v.bit_length()-1==((1<<j)-1)*(q-1)
                    counts['positive_degree_stress']+=1
    for b in (2,3,4,6):
        q=1<<b
        gs=factors(b)
        fields=[]
        for g in gs:
            r=W3(g)
            a,y=root(r)
            fields.append((r,a,y))
        targets=(product(range(8),repeat=q) if b==2 else
                 [tuple(rng.randrange(8) for i in range(q)) for _ in range(12)])
        for target in targets:
            start=0
            rs=[]
            for g in gs:
                d=g.bit_length()-1
                rs.append(list(target[start:start+d]))
                start+=d
            F=inverse_lift(rs,gs,fields,q)
            assert [direct(F,g) for g in gs]==rs
            counts['arbitrary_inverse_inputs']+=1
            counts['inverse_checked_factor_words']+=len(gs)
    return counts


if __name__=='__main__':
    import contextlib,io
    out=io.StringIO()
    with contextlib.redirect_stdout(out):
        main()
    c=json.loads(out.getvalue())
    c.update(extra_tests())
    print(json.dumps(c,indent=2,sort_keys=True))
