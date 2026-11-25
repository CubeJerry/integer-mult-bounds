#!/usr/bin/env python3
"""Finite exact checks for the E002 masked-translation lemma (not tape execution)."""
from dataclasses import dataclass
from functools import cached_property, lru_cache
from itertools import product
from pathlib import Path
import json, platform, sys


def mul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def addto(m, key, value):
    if value:
        m[key] = m.get(key, 0) ^ value
        if not m[key]:
            del m[key]


@dataclass(frozen=True)
class F:
    tag: str
    args: tuple
    d: int

    @cached_property
    def dims(self):
        if self.tag == 'leaf':
            return ()
        if self.tag in ('pad', 'scale'):
            return self.args[0].dims
        a,b = self.args
        return ((self.d,) if self.tag == 'add' else ()) + a.dims+b.dims

    @cached_property
    def width(self):
        z=1
        for d in self.dims:z*=d
        return z

    @cached_property
    def size(self):
        if self.tag=='leaf':return 1
        if self.tag in ('pad','scale'):return 1+self.args[0].size
        return 1+sum(x.size for x in self.args)


def leaf(c0,c1,c2):return F('leaf',(c0,c1,c2),1)
def pad(a,d):
    assert d>=a.d
    return a if d==a.d else F('pad',(a,),d)
def scale(a,c):return F('scale',(a,c),a.d)
def prod(a,b):return F('mul',(a,b),a.d+b.d)
def plus(a,b,d):
    assert d>0 and not d&(d-1)
    return F('add',(pad(a,d),pad(b,d)),d)


def pack(row,dims):
    z=0
    for a,d in zip(row,dims):z=z*d+a
    return z


def unpack(z,dims):
    ans=[]
    for d in reversed(dims):ans.append(z%d);z//=d
    assert z==0
    return tuple(reversed(ans))


@lru_cache(None)
def factor(f,t):
    """Independent dense formal-affine construction, coefficients in F4."""
    assert 0<=t<f.d
    tag=f.tag
    if tag=='leaf':return {(0,0,v):c for v,c in enumerate(f.args) if c}
    if tag=='pad':
        a,=f.args
        if t<a.d:return dict(factor(a,t))
        return {(i,i,0):1 for i in range(f.width)}
    if tag=='scale':
        a,c=f.args
        return {key:mul(v,c) if t==0 else v for key,v in factor(a,t).items() if t!=0 or mul(v,c)}
    a,b=f.args;out={}
    if tag=='mul':
        if t<a.d:
            for (u,v,j),c in factor(a,t).items():
                for k in range(b.width):addto(out,(u*b.width+k,v*b.width+k,j),c)
        else:
            for (u,v,j),c in factor(b,t-a.d).items():
                for k in range(a.width):addto(out,(k*b.width+u,k*b.width+v,j),c)
        return out
    assert tag=='add'
    for g in range(f.d):
        for (u,v,j),c in factor(a,g).items():
            for k in range(b.width):
                o=((g+1)%f.d*a.width+u)*b.width+k
                i=(g*a.width+v)*b.width+k
                addto(out,(o,i,j),c)
        for (u,v,j),c in factor(b,(t-g)%f.d).items():
            for k in range(a.width):
                addto(out,((g*a.width+k)*b.width+u,(g*a.width+k)*b.width+v,j),c)
    return out


def paths(f):
    """Static polynomial list; no row indices are enumerated here."""
    if f.tag=='leaf':return [('leaf',j) for j in range(3)]
    if f.tag=='pad':return [('in',p) for p in paths(f.args[0])]+[('id',)]
    if f.tag=='scale':return [('scale',p) for p in paths(f.args[0])]
    a,b=f.args
    return [('left',p) for p in paths(a)]+[('right',p) for p in paths(b)]


def eval_path(f,t,row,path,wrong=None):
    """One path evaluates to (translated row, affine variable, coefficient)."""
    if f.tag=='leaf':
        _,j=path
        return row,j,f.args[j]
    if f.tag=='pad':
        a,=f.args
        if path[0]=='id':return row,0,int(t>=a.d)
        if t>=a.d:return row,0,0
        return eval_path(a,t,row,path[1],wrong)
    if f.tag=='scale':
        a,c=f.args
        target,j,v=eval_path(a,t,row,path[1],wrong)
        return target,j,mul(c,v) if t==0 else v
    a,b=f.args; side=path[0]
    if f.tag=='mul':
        cut=len(a.dims);ra,rb=row[:cut],row[cut:]
        if side=='left':
            if t>=a.d:return row,0,0
            ta,j,c=eval_path(a,t,ra,path[1],wrong)
            return ta+rb,j,c
        if t<a.d:return row,0,0
        tb,j,c=eval_path(b,t-a.d,rb,path[1],wrong)
        return ra+tb,j,c
    assert f.tag=='add'
    g=row[0];cut=1+len(a.dims);ra,rb=row[1:cut],row[cut:]
    if side=='left':
        ta,j,c=eval_path(a,g,ra,path[1],wrong)
        gp=g if wrong=='omit_rotation' else (g+1)%f.d
        return (gp,)+ta+rb,j,c
    child_t=(t+g)%f.d if wrong=='wrong_grade' else (t-g)%f.d
    tb,j,c=eval_path(b,child_t,rb,path[1],wrong)
    return (g,)+ra+tb,j,c


def translation(f,path):
    if f.tag=='leaf':return ()
    if f.tag=='pad':
        return (0,)*len(f.dims) if path[0]=='id' else translation(f.args[0],path[1])
    if f.tag=='scale':return translation(f.args[0],path[1])
    a,b=f.args
    left=path[0]=='left'
    z=(translation(a,path[1])+(0,)*len(b.dims)) if left else ((0,)*len(a.dims)+translation(b,path[1]))
    return ((int(left),)+z) if f.tag=='add' else z


def from_paths(f,t,wrong=None):
    out={}
    for p in paths(f):
        delta=translation(f,p)
        for i in range(f.width):
            row=unpack(i,f.dims)
            target,j,c=eval_path(f,t,row,p,wrong)
            if c and not wrong:
                expected=tuple((x+e)%d for x,e,d in zip(row,delta,f.dims))
                assert target==expected,(f,t,p,row,target,expected)
            addto(out,(pack(target,f.dims),i,j),c)
    return out


def scalar(f,values):
    if f.tag=='leaf':return f.args[0]^mul(f.args[1],values[0])^mul(f.args[2],values[1])
    if f.tag=='pad':return scalar(f.args[0],values)
    if f.tag=='scale':return mul(scalar(f.args[0],values),f.args[1])
    a,b=f.args
    return scalar(a,values)^scalar(b,values) if f.tag=='add' else mul(scalar(a,values),scalar(b,values))


def numeric(mat,values):
    out={}
    for (o,i,j),c in mat.items():addto(out,(o,i),mul(c,1 if j==0 else values[j-1]))
    return out


def mm(a,b):
    by={}
    for (o,i),v in a.items():by.setdefault(i,[]).append((o,v))
    out={}
    for (o,i),v in b.items():
        for z,c in by.get(o,[]):addto(out,(z,i),mul(c,v))
    return out


def main():
    a=leaf(0,1,0);b=leaf(1,0,2);z=leaf(0,0,0)
    c=plus(a,b,2)
    e=plus(prod(c,pad(a,2)),pad(b,4),4)
    cases=[a,b,z,pad(a,4),scale(pad(b,4),0),scale(c,2),c,
           plus(z,a,2),plus(prod(a,b),a,2),prod(c,plus(b,a,2)),e,
           plus(prod(plus(a,b,2),plus(b,a,2)),prod(a,pad(b,3)),4),
           plus(scale(e,3),pad(prod(c,b),4),4)]
    formal=terms=rows=cyclic=0; negative={'omit_rotation':0,'wrong_grade':0}
    for f in cases:
        assert len(paths(f))<=4*f.size
        for t in range(f.d):
            expected=factor(f,t)
            assert expected==from_paths(f,t)
            formal+=1;terms+=len(paths(f));rows+=f.width*len(paths(f))
            for bad in negative:
                negative[bad]+=expected!=from_paths(f,t,bad)
        if f.width<=64:
            for values in product(range(4),repeat=2):
                mats=[numeric(factor(f,t),values) for t in range(f.d)]
                desired=scalar(f,values)
                target={(i,i):desired for i in range(f.width)} if desired else {}
                for start in range(f.d):
                    out={(i,i):1 for i in range(f.width)}
                    for k in range(f.d):out=mm(mats[(start+k)%f.d],out)
                    assert out==target,(f,values,start)
                    cyclic+=1
    assert all(negative.values())
    result={'status':'PASS_FINITE_EXACT_MASKED_TRANSLATION_AND_CYCLIC_CHECKS',
            'formula_cases':len(cases),'exact_formal_affine_factors':formal,
            'path_descriptions_checked':terms,'path_row_evaluations':rows,
            'cyclic_numeric_products_over_F4':cyclic,'max_row_dimension':max(f.width for f in cases),
            'negative_controls_rejected':negative,
            'scope':'Finite exact formal affine identities and full cyclic products. Not asymptotic proof, tape execution or complete multiplier.',
            'python':sys.version,'platform':platform.platform()}
    print(json.dumps(result,indent=2))
    Path('succinct-cyclic-verification.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
