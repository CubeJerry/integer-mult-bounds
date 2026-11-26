"""Two-input jet-convolution replay with binary range padding and borrowed lanes."""
from itertools import product, zip_longest
from collections import Counter
from random import Random
from math import prod
from pathlib import Path
import json
import runpy

gf=runpy.run_path(str(Path(__file__).with_name("verify-fibre-join.py")))
mul,powf=gf["mul"],gf["power"]
binary_mul=gf["xor_product"]


def words_for_dft(p,root,field):
    """Explicit invertible small-axis program for the finite fixture."""
    size=1 << (field.bit_length()-1)
    mat=[[powf(root,i*j,field) for j in range(p)] for i in range(p)]
    def inv(x): return powf(x,size-2,field)
    reducing=[]
    for j in range(p):
        row=next(i for i in range(j,p) if mat[i][j])
        if row!=j:
            mat[j],mat[row]=mat[row],mat[j]
            reducing.append(('swap',j,row))
        lead=mat[j][j]
        if lead!=1:
            mat[j]=[mul(x,inv(lead),field) for x in mat[j]]
            reducing.append(('scale',j,inv(lead)))
        for i in range(p):
            if i!=j and mat[i][j]:
                scalar=mat[i][j]
                mat[i]=[x ^ mul(scalar,y,field) for x,y in zip(mat[i],mat[j])]
                reducing.append(('add',i,j,scalar))
    assert mat==[[int(i==j) for j in range(p)] for i in range(p)]
    letters=[]
    for op in reversed(reducing):
        if op[0]=='scale':
            letters.append(('scale',op[1],inv(op[2])))
        elif op[0]=='swap':
            letters.append(op)
        else:
            _,i,j,scalar=op
            if scalar!=1: letters.append(('scale',j,scalar))
            letters.append(('pair',i,j))
            if scalar!=1: letters.append(('scale',j,inv(scalar)))
    return letters


def jet_scale(x,scalar,e,r,field):
    mask=(1 << e)-1
    return sum(mul((x >> (e*k))&mask,scalar,field) << (e*k) for k in range(r))


def jet_mul(x,y,e,r,field):
    mask=(1 << e)-1
    out=0
    for i in range(r):
        for j in range(r-i):
            out ^= mul((x>>(e*i))&mask,(y>>(e*j))&mask,field) << (e*(i+j))
    return out


def decompose(x,radices):
    vals=[]
    for k in radices:
        vals.append(x%k)
        x//=k
    assert x==0
    return vals


def flatten(digits,radices):
    k=0
    for a,b in reversed(list(zip(digits,radices,strict=True))):
        assert 0<=a<b
        k=b*k+a
    return k


def pair_order(p,cap,M,letter):
    if letter[0]!='pair': return list(range(cap)),0
    _,target,source=letter
    active=[p*s+i for s in range(M) for i in (target,source)]
    excluded=set(active)
    return active+[i for i in range(cap) if i not in excluded],len(active)


class Layout:
    def __init__(self,primes,e,r,B):
        self.primes,self.e,self.r,self.B=primes,e,r,B
        G=len(primes)
        self.caps=[1 << (p*G-1).bit_length() for p in primes]
        self.lanes=[u//p for u,p in zip(self.caps,primes)]
        self.P=(B+prod(self.lanes)-1)//prod(self.lanes)
        self.field=gf['field_poly'](e)
        self.roots=[next(x for x in range(2,1<<e) if powf(x,p,self.field)==1) for p in primes]
        self.count=prod(self.caps)
        self.digits=[decompose(i,self.caps) for i in range(self.count)]

    def alloc(self):
        return [[0]*self.P for _ in range(self.count)]

    def locate(self,j,t):
        s,ell=divmod(t,self.P)
        ss=decompose(s,self.lanes)
        codes=[j%p+p*u for p,u in zip(self.primes,ss)]
        return flatten(codes,self.caps),ell

    def pack(self,polys,n):
        grid=self.alloc()
        e0,r0=(self.e+1)//2,(self.r+1)//2
        for t,x in enumerate(polys):
            for i in range(n):
                j,low=divmod(i,e0*r0)
                z,y=divmod(low,e0)
                pos,ell=self.locate(j,t)
                grid[pos][ell] ^= ((x>>i)&1) << (self.e*z+y)
        return grid

    def tensor(self,grid,inverse,counts):
        e,r,F=self.e,self.r,self.field
        words=[words_for_dft(p,powf(g,p-1,F) if inverse else g,F)
               for p,g in zip(self.primes,self.roots)]
        for letters in zip_longest(*words,fillvalue=('id',)):
            permuted=self.alloc()
            for i,row in enumerate(grid):
                codes=self.digits[i].copy()
                scale=1
                for g,(p,M,op) in enumerate(zip(self.primes,self.lanes,letters)):
                    s,x=divmod(codes[g],p)
                    if s==M: continue
                    if op[0]=='swap' and x in op[1:]:
                        codes[g]=s*p+(op[2] if x==op[1] else op[1])
                    if op[0]=='scale' and x==op[1]: scale=mul(scale,op[2],F)
                permuted[flatten(codes,self.caps)]=(row.copy() if scale==1 else
                                                 [jet_scale(z,scale,e,r,F) for z in row])
            layout=[pair_order(p,u,M,op) for p,u,M,op in
                    zip(self.primes,self.caps,self.lanes,letters)]
            grid=self.pairs(permuted,layout,counts)
        return grid

    def pairs(self,permuted,layout,counts):
        shaperad=[u//2 for u in self.caps]
        lowcap=[2]*len(layout)
        nextgrid=self.alloc()
        for hx in range(prod(shaperad)):
            hi=decompose(hx,shaperad)
            active=[g for g,(_,bound) in enumerate(layout) if 2*hi[g]<bound]
            addresses=[]
            for l in range(prod(lowcap)):
                low=decompose(l,lowcap)
                codes=[order[2*h+b] for h,b,(order,_) in zip(hi,low,layout)]
                addresses.append(flatten(codes,self.caps))
            data=[permuted[idx].copy() for idx in addresses]
            for g in active:
                for l in range(len(data)):
                    if not l & (1<<g):
                        data[l]=[x^y for x,y in zip(data[l],data[l+(1<<g)])]
            for idx,row in zip(addresses,data):
                nextgrid[idx]=row
            counts['prefixes_with_simultaneous_pairs']+=int(len(active)>=2)
        return nextgrid

    def unpack(self,grid,n):
        e,r=self.e,self.r
        e0,r0=(e+1)//2,(r+1)//2
        out=[0]*self.B
        for t in range(self.B):
            for j in range(prod(self.primes)):
                pos,ell=self.locate(j,t)
                cell=grid[pos][ell]
                for z in range(r):
                    for y in range(e):
                        idx=y+e0*(z+r0*j)
                        if idx < 2*n-1:
                            out[t] ^= ((cell>>(e*z+y))&1)<<idx
        return out

def one_case(primes,e,r,n,B,seed):
    shape=Layout(primes,e,r,B)
    e0,r0=(e+1)//2,(r+1)//2
    assert 2*(e0-1)<e and 2*(r0-1)<r
    assert 2*((n-1)//(e0*r0))<prod(primes)
    rng=Random(seed)
    left=[rng.getrandbits(n) for _ in range(B)]
    right=[rng.getrandbits(n) for _ in range(B)]
    if B>=4:
        left[:4]=[0,1,1<<(n-1),(1<<n)-1]
        right[:4]=[(1<<n)-1,(1<<n)-1,1<<(n-1),(1<<n)-1]
    a0,b0=shape.pack(left,n),shape.pack(right,n)
    stats=Counter()
    A=shape.tensor(a0,False,stats)
    Br=shape.tensor(b0,False,stats)
    assert shape.tensor(A,True,stats)==a0
    # Check the physical CRT order against a direct, independent mixed DFT.
    for t in range(min(B,9)):
        for v in range(prod(primes)):
            dest,ell=shape.locate(v,t)
            value=0
            for j in range(prod(primes)):
                src,_=shape.locate(j,t)
                scale=1
                for p,g in zip(primes,shape.roots):
                    scale=mul(scale,powf(g,(j%p)*(v%p),shape.field),shape.field)
                value^=jet_scale(a0[src][ell],scale,e,r,shape.field)
            assert value==A[dest][ell]
    products=[[jet_mul(x,y,e,r,shape.field) for x,y in zip(ra,rb)]
              for ra,rb in zip(A,Br)]
    out=shape.unpack(shape.tensor(products,True,stats),n)
    assert out==[binary_mul(x,y) for x,y in zip(left,right)]
    assert stats['prefixes_with_simultaneous_pairs']>0
    return dict(prefixes_with_simultaneous_pairs=stats['prefixes_with_simultaneous_pairs'],
                length=n,primes=primes,extension_degree=e,jet_length=r,independent_pairs=B,
                address_radices=shape.caps,borrowed_lanes=shape.lanes,residual_lanes=shape.P,
                unused_lanes=prod(shape.lanes)*shape.P-B,direct_DFT_checks=min(B,9)*prod(primes),
                high_product_bit=(out[2]>>(2*n-2)) if B>=4 else None)

if __name__=='__main__':
    cases=[one_case([3,5],4,5,n,B,337+B) for n,B in [(31,6),(35,11),(37,17),(41,35)]]
    print(json.dumps(dict(cases=cases,all_independent_products=sum(x['independent_pairs'] for x in cases),
                          source_word_scope="Finite fixture uses elementary Gaussian words. Source fast words, tape movement and asymptotic clocks are verified separately."),indent=2))
