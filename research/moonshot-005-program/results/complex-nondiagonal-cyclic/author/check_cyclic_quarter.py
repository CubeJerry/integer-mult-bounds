#!/usr/bin/env python3
"""Exact quarter-sector interpolation, all-width unit controls, and recipes."""
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from math import comb
import argparse, hashlib, json

@dataclass(frozen=True)
class G:
    x:F=F(0)
    y:F=F(0)
    def __add__(self,z):
        z=lift(z);return G(self.x+z.x,self.y+z.y)
    __radd__=__add__
    def __neg__(self):return G(-self.x,-self.y)
    def __sub__(self,z):return self+-lift(z)
    def __mul__(self,z):
        z=lift(z);return G(self.x*z.x-self.y*z.y,self.x*z.y+self.y*z.x)
    __rmul__=__mul__
    def inv(self):
        d=self.x*self.x+self.y*self.y
        if not d:raise ZeroDivisionError
        return G(self.x/d,-self.y/d)
    def __truediv__(self,z):return self*lift(z).inv()
    def __bool__(self):return bool(self.x or self.y)
    def bound(self):return abs(self.x)+abs(self.y)
    def serial(self):return [str(self.x),str(self.y)]
def lift(z):return z if isinstance(z,G)else G(F(z))
zero=G();one=G(F(1));ii=G(F(0),F(1))
def ipow(k):return [one,ii,-one,-ii][k%4]
def eye():return [[one if r==c else zero for c in range(3)]for r in range(3)]
def zmat():return [[zero for _ in range(3)]for _ in range(3)]
def mat(x):return [[lift(z)for z in row]for row in x]
def madd(a,b):return [[x+y for x,y in zip(ra,rb)]for ra,rb in zip(a,b)]
def mscale(a,z):return [[x*z for x in row]for row in a]
def mm(a,b):return [[sum((a[r][k]*b[k][c]for k in range(3)),zero)for c in range(3)]for r in range(3)]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def apply_op(a,op):
    a=[list(row)for row in a];kind,r=op[:2]
    if kind=='SWAP':a[r],a[op[2]]=a[op[2]],a[r]
    elif kind=='SCALE':a[r]=[z*op[2]for z in a[r]]
    elif kind=='ADD':a[r]=[z+op[3]*w for z,w in zip(a[r],a[op[2]])]
    else:raise ValueError(kind)
    return a
def inverse_op(op):
    if op[0]=='SWAP':return op
    if op[0]=='SCALE':return(op[0],op[1],op[2].inv())
    return(op[0],op[1],op[2],-op[3])
def expand_unweighted(ops):
    out=[]
    for op in ops:
        if op[0]!='ADD':out.append(op);continue
        _,dst,src,c=op
        require(bool(c) and dst!=src,'Nonzero weighted source-restoring ADD')
        out.extend([('SCALE',src,c),('ADD',dst,src,one),('SCALE',src,c.inv())])
    return out
def minverse(a):
    original=a;a=[list(r)for r in a];out=eye();ops=[]
    for c in range(3):
        pivot=next((r for r in range(c,3)if a[r][c]),None)
        if pivot is None:return None,[]
        if pivot!=c:
            op=('SWAP',c,pivot);a=apply_op(a,op);out=apply_op(out,op);ops.append(op)
        if a[c][c]!=one:
            op=('SCALE',c,a[c][c].inv());a=apply_op(a,op);out=apply_op(out,op);ops.append(op)
        for r in range(3):
            if r==c or not a[r][c]:continue
            op=('ADD',r,c,-a[r][c]);a=apply_op(a,op);out=apply_op(out,op);ops.append(op)
    require(a==eye()and mm(out,original)==eye()and mm(original,out)==eye(),'Exact scalar inverse')
    forward=eye()
    for op in reversed(ops):forward=apply_op(forward,inverse_op(op))
    require(forward==original,'Literal reversed scalar recipe')
    require(sum(op[0]=='ADD'for op in ops)<=6 and sum(op[0]=='SCALE'for op in ops)<=3 and sum(op[0]=='SWAP'for op in ops)<=3,'Conservative instruction bounds')
    expanded=expand_unweighted(ops);expanded_product=eye()
    for op in expanded:expanded_product=apply_op(expanded_product,op)
    require(expanded_product==out,'Expanded unweighted ADD recipe')
    require(sum(op[0]=='ADD'for op in expanded)<=6 and sum(op[0]=='SCALE'for op in expanded)<=15 and sum(op[0]=='SWAP'for op in expanded)<=3,'Expanded primitive instruction bounds')
    return out,ops
def interpolate(values):
    return [mscale(sum_m([mscale(values[s],ipow(-s*j))for s in range(4)]),F(1,4))for j in range(4)]
def sum_m(xs):
    out=zmat()
    for x in xs:out=madd(out,x)
    return out
def eval_poly(pol,s):return sum_m([mscale(pol[j],ipow(s*j))for j in range(4)])
def mul_poly(a,b):
    out=[zmat()for _ in range(4)]
    for i in range(4):
        for j in range(4):out[(i+j)%4]=madd(out[(i+j)%4],mm(a[i],b[j]))
    return out
def ser_mat(a):return [[z.serial()for z in row]for row in a]
def ser_ops(ops):return [[z.serial()if isinstance(z,G)else z for z in op]for op in ops]

sectors=[eye(),mat([[1,G(F(1),F(1)),0],[0,1,0],[0,0,1]]),mat([[0,1,0],[1,0,0],[0,0,1]]),mat([[1,1,1],[0,1,1],[0,0,1]])]
inverses=[];recipes=[]
for q in sectors:
    inverse,ops=minverse(q);require(inverse is not None,'Positive sector unit')
    inverses.append(inverse);recipes.append(ops)
Q=interpolate(sectors);R=interpolate(inverses)
require(all(eval_poly(Q,s)==sectors[s]and eval_poly(R,s)==inverses[s]for s in range(4)),'Fourier reconstruction')
require(mul_poly(Q,R)==[eye(),zmat(),zmat(),zmat()]and mul_poly(R,Q)==[eye(),zmat(),zmat(),zmat()],'Polynomial inverse modulo z^4-1')

# All four conditional bank permutations and their exact interpolated inverse.
perms=[(0,1,2),(1,2,0),(2,0,1),(1,0,2)]
perm_matrices=[[[one if p[c]==r else zero for c in range(3)]for r in range(3)]for p in perms]
perm_inverse=[minverse(q)[0]for q in perm_matrices]
require(mul_poly(interpolate(perm_matrices),interpolate(perm_inverse))==[eye(),zmat(),zmat(),zmat()],'Conditional routing inverse')

# Every spectrum count is exact for the actual16-address source: each b value
# has8 choices in one column. One bad sector is invisible at widths1 and2.
spectra={}
for v in [1,2,3,4,7]:
    counts=[sum(comb(v,k)for k in range(v+1)if k%4==s)*8**v for s in range(4)]
    require(sum(counts)==16**v,'Exact tensor spectrum multiplicities')
    spectra[v]=counts
require(spectra[1][3]==spectra[2][3]==0 and all(spectra[v][3]>0 for v in [3,4,7]),'Hidden fourth-sector control')
bad=sectors.copy();bad[3]=mat([[1,0,0],[0,1,0],[0,0,0]])
require(minverse(bad[3])[0]is None and all(minverse(bad[s])[0]is not None for s in range(3)),'Only fourth scalar sector is singular')
badpoly=interpolate(bad)
require(all(eval_poly(badpoly,s)==bad[s]for s in range(4)),'Singular-sector polynomial is exact')

# Collective polynomial, not tensoring a one-column sum.
f=lambda s:one+F(1,2)*ipow(s)
collective=[f(0),f(1),f(1),f(2)]
wrong=[f(0)*f(0),f(0)*f(1),f(1)*f(0),f(1)*f(1)]
require(collective!=wrong,'Tensor-of-sum negative control')

# Actual source conjugating monomial tables. A table records output address
# and input phase exponent mod4; composition preserves every quarter phase.
def tab(fn,phase):
    out=[]
    for x in range(16):
        bits=tuple((x>>j)&1 for j in range(4));bs=fn(*bits)
        out.append((sum(v<<j for j,v in enumerate(bs)),phase(*bits)%4))
    require(sorted(p for p,z in out)==list(range(16)),'Monomial bijection')
    return tuple(out)
def tmul(a,b):return tuple((a[p][0],(q+a[p][1])%4)for p,q in b)
def tinv(a):
    o=[None]*16
    for x,(p,q)in enumerate(a):o[p]=(x,-q%4)
    return tuple(o)
tid=tab(lambda a,b,c,d:(a,b,c,d),lambda a,b,c,d:0)
db=tab(lambda a,b,c,d:(a,b,c,d),lambda a,b,c,d:b)
ss=tab(lambda a,b,c,d:(b,c,d,a),lambda a,b,c,d:2*a*b*d)
ll=tab(lambda a,b,c,d:(a,b^(c*d),c,d),lambda a,b,c,d:c*d*(2*a+2*b-1))
rr=tab(lambda a,b,c,d:(a,b,c^(a*b),d),lambda a,b,c,d:a*b*(1+2*c+2*d))
adapters=[tid,ss,ll,tmul(ss,rr)]
controls=[tmul(tmul(tinv(t),db),t)for t in adapters]
require(len(set(controls))==4,'Four distinct cyclic controls')
for h in controls:
    require(tmul(tmul(h,h),tmul(h,h))==tid,'Exact order-four control')
    require(all(p==x and z in [0,1]for x,(p,z)in enumerate(h)),'Controlled quarter-phase table')
for t,h in zip(adapters,controls):
    beta=[(t[x][0]>>1)&1 for x in range(16)]
    require(h==tuple((x,beta[x])for x in range(16)),'Direct control: monomial phases cancel and no field adapters are needed')
require(tmul(rr,tmul(db,rr))==db,'Duplicate R4 Db R4 rejected')
clock=tmul(tinv(ss),db)
require(tmul(clock,tinv(clock))==tid,'Actual clock inverse')

ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/5b84182f4f70/programme'));ap.add_argument('--output',type=Path,default=Path(__file__).with_name('CYCLIC-RESULT.json'));args=ap.parse_args()
paths=['research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md','research/moonshot-005-program/results/fixed-monomial-compact-bridge/author/PROOF.md','research/moonshot-005-program/results/nonlinear-compact-control/author/PROOF.md']
result={
 'status':'PASS_EXACT_CYCLIC_INTERSTAGE_AND_INVERSE',
 'baseline':'3057acc9311101cfedfcfacf7f68fb0866507871',
 'scope':'Constructive all-width cyclic ordinary unit criterion and explicit inverse; no independent421 endpoint or complete supplier',
 'sector_matrices':[ser_mat(q)for q in sectors],
 'sector_inverse_matrices':[ser_mat(q)for q in inverses],
 'reduction_recipes':[ser_ops(ops)for ops in recipes],
 'polynomial_coefficients':[ser_mat(q)for q in Q],
 'inverse_polynomial_coefficients':[ser_mat(q)for q in R],
 'actual_monomial_conjugators':adapters,
 'distinct_quarter_controls':controls,
 'weighted_pass_bound_per_forward_or_inverse':{'conditional_weighted_ADD':24,'conditional_SCALE':12,'conditional_SWAP':12,'monomial_services':0},
 'instruction_bound_per_forward_or_inverse':{'conditional_unweighted_ADD':24,'conditional_SCALE':60,'conditional_SWAP':12,'monomial_services':0},
 'expanded_unweighted_reduction_recipes':[ser_ops(expand_unweighted(ops))for ops in recipes],
 'direct_phase_tables':[[z for p,z in h]for h in controls],
 'direct_control_credit':'Root: h=T^-1 Db T is diagonal with beta(x)=b(pi_T(x)); phases cancel, eliminating six initial adapter services. Separate clocks remain paid.',
 'control_cost':'O(N+V) combinatorial work, O(V) storage, O(N) retained scalar primitives; precision/tape prices still charged',
 'sector_norm_infinity_bounds':[str(max(sum(z.bound()for z in row)for row in q))for q in sectors],
 'inverse_sector_norm_infinity_bounds':[str(max(sum(z.bound()for z in row)for row in q))for q in inverses],
 'exact_spectrum_counts':spectra,
 'negative_controls':['singular sector3 invisible at widths1 and2, fails every V>=3','tensor-of-sum rejected','duplicate nonlinear-conjugation choice rejected'],
 'source_sha256':{p:hashlib.sha256((args.repo/p).read_bytes()).hexdigest()for p in paths},
 'new_kappa':False,
}
args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in ['sector_matrices','sector_inverse_matrices','reduction_recipes','polynomial_coefficients','inverse_polynomial_coefficients','actual_monomial_conjugators','distinct_quarter_controls']},indent=2))
