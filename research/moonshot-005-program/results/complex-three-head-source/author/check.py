#!/usr/bin/env python3
"""Exact Gaussian-dyadic checks for the quadratic-phase pentagonal source.
Only Python's standard library is used. No floating-point arithmetic.
"""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import dataclass
from pathlib import Path

G = tuple[int, int]
def ga(a:G,b:G)->G:return a[0]+b[0],a[1]+b[1]
def gm(a:G,b:G)->G:return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def gc(a:G)->G:return a[0],-a[1]
Z=(0,0); O=(1,0); II=(0,1)
@dataclass(frozen=True)
class M:
    a:tuple[tuple[G,...],...]
    k:int=0
    def norm(self):
        a=self.a;k=self.k
        while k and all(not (x&1 or y&1) for row in a for x,y in row):
            a=tuple(tuple((x//2,y//2) for x,y in row) for row in a);k-=1
        return M(a,k)
    @property
    def n(self):return len(self.a)
    def __matmul__(self,b):
        n=self.n;out=[]
        for row in self.a:
            nz=[(j,v) for j,v in enumerate(row) if v!=Z]
            nr=[]
            for l in range(n):
                r=Z
                for j,v in nz:
                    if b.a[j][l]!=Z:r=ga(r,gm(v,b.a[j][l]))
                nr.append(r)
            out.append(tuple(nr))
        return M(tuple(out),self.k+b.k).norm()
    def __add__(self,b):
        k=max(self.k,b.k);sa=1<<(k-self.k);sb=1<<(k-b.k)
        return M(tuple(tuple((sa*x[0]+sb*y[0],sa*x[1]+sb*y[1]) for x,y in zip(ra,rb)) for ra,rb in zip(self.a,b.a)),k).norm()
    def scale(self,c:G):return M(tuple(tuple(gm(c,v) for v in row) for row in self.a),self.k).norm()
    def star(self):return M(tuple(tuple(gc(self.a[j][i]) for j in range(self.n)) for i in range(self.n)),self.k)
    def power(self,k):
        if k<0:return self.star().power(-k)
        r=eye(self.n);b=self
        while k:
            if k&1:r=r@b
            b=b@b;k>>=1
        return r
    def trace(self):
        r=Z
        for j in range(self.n):r=ga(r,self.a[j][j])
        assert not r[0]%(1<<self.k) and not r[1]%(1<<self.k)
        return r[0]//(1<<self.k),r[1]//(1<<self.k)
    def tensor(self,b):
        out=[]
        for ra in self.a:
            for rb in b.a:
                out.append(tuple(gm(x,y) for x in ra for y in rb))
        return M(tuple(out),self.k+b.k).norm()
    def tp(self,v):
        r=eye(1)
        for _ in range(v):r=r.tensor(self)
        return r

def eye(n):return M(tuple(tuple(O if i==j else Z for j in range(n)) for i in range(n)))
def zero(n):return M(tuple(tuple(Z for _ in range(n)) for _ in range(n)))
def monomial(p,q):
    n=len(p);a=[[Z for _ in range(n)] for _ in range(n)];u=[O,II,(-1,0),(0,-1)]
    for j in range(n):a[p[j]][j]=u[q[j]%4]
    return M(tuple(tuple(row) for row in a))
def block(rows):
    n=rows[0][0].n;k=max(x.k for row in rows for x in row);out=[]
    for rr in rows:
        for i in range(n):
            row=[]
            for x in rr:
                s=1<<(k-x.k);row.extend((s*a,s*b) for a,b in x.a[i])
            out.append(tuple(row))
    return M(tuple(out),k).norm()
def diagonal(ms):return block([[ms[i] if i==j else zero(ms[0].n) for j in range(len(ms))] for i in range(len(ms))])
def invblock2(a,b,c,d):
    return block([[a,b],[c,d]])
def gaussian_rank(m):
    counts={sum(v!=Z for v in row) for row in m.a}
    assert len(counts)==1
    size=counts.pop();assert size and size&(size-1)==0
    return size.bit_length()-1

def check(repo:Path):
    source=repo/'research/moonshot-005-program/results/quadratic-sign-query-gate/author/PROOF.md'
    expected='1bc214b889a5d9ecee6fa887966dd828a4aeee95b5584379e5d249d9ceddea01'
    assert hashlib.sha256(source.read_bytes()).hexdigest()==expected
    id4=eye(4);xa=monomial([1,0,3,2],[0]*4);xb=monomial([2,3,0,1],[0]*4)
    qa=M((id4.scale((1,1))+xa.scale((1,-1))).a,1).norm()
    qb=M((id4.scale((1,1))+xb.scale((1,-1))).a,1).norm()
    s=monomial([0,3,1,2],[0,2,0,0])
    r=monomial([0,3,2,1],[0,3,3,0])
    assert r==qa.star()@s@qb@s
    a=qb@s;b=a.scale(II)
    assert a.power(5)==id4.scale((0,-1)) and b.power(5)==id4
    ranks=[gaussian_rank(b.power(k)) for k in range(5)]
    assert ranks==[0,1,2,2,1]
    assert [b.power(k).trace() for k in range(1,5)]==[(-1,0)]*4
    sum1=zero(4)
    for k in range(5):sum1=sum1+b.power(k)
    assert sum1==zero(4)
    g1=s.scale(II);g2=r.scale((-1,0));h2=s.star().scale((0,-1))
    assert g1==monomial([0,3,1,2],[1,3,1,1])
    assert g2==monomial([0,3,2,1],[2,1,1,2])
    assert h2==monomial([0,2,3,1],[3,3,3,1])
    for g in [qa,qb,s,r,a,b,g1,g2,h2]:assert g@g.star()==id4
    width_checks=[]
    for v in [1,2,3]:
        qav=qa.tp(v);qbv=qb.tp(v);bv=b.tp(v);iv=eye(4**v);zv=zero(4**v)
        # All four independent source columns, field-level sums outside tensor powers.
        source4=block([[qbv,zv,zv,zv],[iv,qav,zv,zv],[zv,zv,qbv,(qav@qbv).scale((-1,0))],[zv,zv,zv,qav]])
        pre=diagonal([g1.tp(v),g2.tp(v),g1.tp(v),g2.tp(v)])
        post=diagonal([iv,h2.tp(v),iv,h2.tp(v)])
        expected4=block([[bv,zv,zv,zv],[iv,bv,zv,zv],[zv,zv,bv,bv.power(2).scale((-1,0))],[zv,zv,zv,bv]])
        assert post@source4@pre==expected4
        assert bv.power(5)==iv
        assert [gaussian_rank(bv.power(k)) for k in range(5)]==[0,v,2*v,2*v,v]
        width_checks.append({'width':v,'independent_inputs':4,'matrix_dimension':4*(4**v),'all_columns':True,'order_five':True})
    # Formal block inverses; positive body follows by the separately paid F^2 translation.
    lower=block([[b,zero(4)],[id4,b]])
    upper=block([[b,b.power(2).scale((-1,0))],[zero(4),b]])
    li=block([[b.power(-1),zero(4)],[b.power(-2).scale((-1,0)),b.power(-1)]])
    ui=block([[b.power(-1),id4],[zero(4),b.power(-1)]])
    assert lower@li==eye(8) and li@lower==eye(8)
    assert upper@ui==eye(8) and ui@upper==eye(8)
    # Negative controls: deleting the CZ phase, scalar normalization, or a boundary map fails.
    p=monomial([0,3,1,2],[0]*4)
    assert (qb@p).scale(II).power(5)!=id4
    assert a.power(5)!=id4 and a.tp(2).power(5)!=eye(16)
    source2=block([[qb,zero(4)],[id4,qa]])
    pre2=diagonal([g1,g2]);target2=lower
    assert source2@pre2!=target2
    assert diagonal([id4,h2])@source2@diagonal([g1,eye(4)])!=target2
    b2=b.tp(2);sum2=zero(16)
    for k in range(5):sum2=sum2+b2.power(k)
    assert sum2!=zero(16) and sum2@sum2==sum2.scale((5,0))
    assert sum2.trace()==(20,0) # rank four since sum2/5 is an idempotent.
    multiplicities=[]
    for v in range(1,13):
        triv=(4**v+4*(-1)**v)//5;other=(4**v-(-1)**v)//5
        assert triv+4*other==4**v and (v==1 or min(triv,other)>0)
        multiplicities.append({'width':v,'trivial':triv,'each_nontrivial':other})
    return {'status':'PASS_EXACT_PENTAGONAL_NATIVE_PHASE_GAUGE','source_sha256':expected,'baseline':'9fb0a34adad2f5903d3169fee7f7a7fcb6f03e3a','one_column_order':5,'gaussian_rank_pattern':ranks,'boundary_monomials':{'pre_first':{'permutation':[0,3,1,2],'input_phase_mod4':[1,3,1,1]},'pre_second':{'permutation':[0,3,2,1],'input_phase_mod4':[2,1,1,2]},'post_second':{'permutation':[0,2,3,1],'input_phase_mod4':[3,3,3,1]}},'forward_half_additional_ordinary_services':{'coordinate_permutations':3,'unit_phase_passes':3,'unit_phase_applications_upper_bound':'3D','new_owned_fields':0,'new_gaussian_calls':0,'added_denominator_factor':1},'width_checks':width_checks,'cyclic_tensor_multiplicities':multiplicities,'negative_controls':{'omit_quadratic_phase_rejected':True,'omit_width_scalar_rejected':True,'omit_post_second_rejected':True,'incorrect_pre_second_rejected':True,'one_column_cyclotomic_shortcut_rejected_at_width2':True},'claim_scope':'Exact source gauge and uniform ordinary service description, not a completed caller, supplier, foundation discharge, or new kappa.','new_kappa':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--output',type=Path)
    args=ap.parse_args();result=check(args.repo);text=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
