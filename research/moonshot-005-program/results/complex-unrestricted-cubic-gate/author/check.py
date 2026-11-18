"""Fresh exact controls for the unrestricted cubic theorem and 321 interface."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
from fractions import Fraction
import json
from pathlib import Path
import sympy as sp
from sympy import QQ_I
from sympy.polys.matrices import DomainMatrix

K=QQ_I
def dm(m):return DomainMatrix.from_Matrix(sp.Matrix(m).applyfunc(sp.expand)).convert_to(K)
def block(rows):
    return DomainMatrix.vstack(*(DomainMatrix.hstack(*row) for row in rows))
def adj(a):return dm(a.to_Matrix().H)
def require(test,label):
    if not test:raise AssertionError(label)
def table(f):
    out=sp.zeros(16)
    for j in range(16):
        x=tuple((j>>b)&1 for b in range(4));y,v=f(x)
        out[sum(a<<b for b,a in enumerate(y)),j]=v
    return dm(out)
def support(a):
    m=a.to_Matrix();rs={sum(v!=0 for v in m.row(j)) for j in range(m.rows)}
    cs={sum(v!=0 for v in m.col(j)) for j in range(m.cols)}
    require(len(rs)==len(cs)==1 and rs==cs,'flat support count');return next(iter(rs))
def projection_label(a):
    vals=list(a.to_Matrix());first=next(v for v in vals if v)
    return tuple(sp.simplify(v/first) for v in vals)
def swap_table(i,j):
    def f(x):
        y=list(x);y[i],y[j]=y[j],y[i];return y,1
    return table(f)

def moment_interval(n):
    scale=10**40;top=n**199*scale**200;lo=0;hi=n*scale+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=top:lo=mid
        else:hi=mid
    require(lo**200<=top<hi**200,'integer root enclosure')
    return Fraction(lo,scale),Fraction(hi,scale)

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    here=Path(__file__).resolve().parent;pins=json.loads((here/'SOURCE-PINS.json').read_text())
    for p,h in pins['dependencies'].items():require(sha256((args.repo/p).read_bytes()).hexdigest()==h,p)
    require(sha256((here/'PROOF.md').read_bytes()).hexdigest()==pins['local_proof_sha256'],'current proof pin')
    I=dm(sp.eye(16));Z=I*K.zero
    R=table(lambda x:((x[1],x[2],x[3],x[0]),(-1)**(x[0]*x[1]*x[3])))
    X=table(lambda x:((x[0],x[1]^1,x[2],x[3]),1))
    a=(I*K(1,1)+X*K(1,-1))*K.from_sympy(sp.Rational(1,2))*R;ai=adj(a)
    require(a*ai==ai*a==I,'source unitary')
    powers=[a**j for j in range(5)]
    require([support(v) for v in powers]==[1,2,4,8,16],'all source power classes')
    for r,v in enumerate(powers):
        require(all(sp.expand(z*sp.conjugate(z))==sp.Rational(1,2**r) for z in v.to_Matrix() if z),'flat source powers')
    L=block([[a,Z,Z],[I,a,Z],[Z,Z,I]])
    U=block([[a,-a**2,Z],[Z,a,Z],[Z,Z,I]])
    Li=block([[ai,Z,Z],[-ai**2,ai,Z],[Z,Z,I]])
    Ui=block([[ai,I,Z],[Z,ai,Z],[Z,Z,I]])
    EYE=block([[I,Z,Z],[Z,I,Z],[Z,Z,I]])
    require(L*Li==Li*L==U*Ui==Ui*U==EYE,'literal native inverses')
    monos=[I,swap_table(0,1),swap_table(1,2),swap_table(2,3)]
    bounds=0
    for g in monos:
        for r in (3,4):
            for v in (ai**2*g*powers[r],powers[r]*g*ai**2):
                require(all(sp.expand(z*sp.conjugate(z))<=sp.Rational(1,2) for z in v.to_Matrix()),'two-sided inverse nonmonomial bound');bounds+=1
    require(ai**2*powers[2]==I,'quadratic countercontrol; cannot extend theorem to all heads>=2')
    inner1=[g*a*h for g,h in product(monos,repeat=2)]
    inner2=[g*a**2*h for g,h in product(monos,repeat=2)]
    require(not ({projection_label(a*v) for v in inner1}&{projection_label(a*v) for v in inner2}),'common outer A preserves disjoint inner labels')
    # A deliberately noncommuting, invertible B and its physical flag C.
    h,s=monos[1],monos[3]
    B=block([[I,h],[s,I+s*h]]);Bi=block([[I+h*s,-h],[-s,I]])
    require(B*Bi==Bi*B==block([[I,Z],[Z,I]]),'active block inverse')
    C=block([[I,h,Z],[s,h,I],[s,I+s*h,Z]])
    Q=block([[h,I,h],[s,s,I+s*h],[I,Z,Z]])
    require(C.det()!=K.zero and Q.det()!=K.zero,'flag units')
    E=L*C*U*Q*L
    ent=lambda M,i,j:M.extract(list(range(16*i,16*i+16)),list(range(16*j,16*j+16)))
    require(ent(E,2,2)==s*a*h-s*a**2*(I+s*h)+(I+s*h)*a*(I+s*h),'flagged E22')
    require(ent(E,0,2)==a*(a*h-a**2*(I+s*h)+h*a*(I+s*h)),'flagged E02')
    v1=a*h;v2=a*(I+s*h)
    require(B*block([[v1],[v2]])!=block([[Z],[Z]]),'nonzero last column cannot satisfy both zero equations')
    # Literal 321 constructor; only positive ADDs and sign SCALEs are used.
    def add(i,j):
        m=[[I if r==c else Z for c in range(3)] for r in range(3)];m[i][j]=I;return block(m)
    def neg(i):
        m=[[I if r==c else Z for c in range(3)] for r in range(3)];m[i][i]=-I;return block(m)
    def signed_swap(i,j):return [('ADD',add(i,j)),('SCALE',neg(i)),('ADD',add(j,i)),('SCALE',neg(i)),('ADD',add(i,j))]
    ops=signed_swap(0,2)+[('ADD',add(2,1)),('NATIVE',L)]
    ops+=signed_swap(0,1)+signed_swap(1,2)+[('NATIVE',U)]
    ops += [('SCALE',neg(2)),('ADD',add(0,2)),('SCALE',neg(2)),('NATIVE',L)]
    target=block([[a**3,Z,Z],[Z,a**2,Z],[Z,Z,a]])
    def run(skip=None):
        out=EYE
        for j,(_,m) in enumerate(ops):
            if j!=skip:out=m*out
        return out
    require(run()==target,'all 48 independent columns of the 321 constructor')
    omitted=[]
    for j,(kind,_) in enumerate(ops):
        if kind!='NATIVE':require(run(j)!=target,'omission control');omitted.append(j)
    # Do not tensor an additive one-letter expansion termwise.
    actual=dm(sp.kronecker_product(a.to_Matrix(),a.to_Matrix()))
    bogus=dm((1+sp.I)/2*sp.kronecker_product(R.to_Matrix(),R.to_Matrix())+(1-sp.I)/2*sp.kronecker_product((X*R).to_Matrix(),(X*R).to_Matrix()))
    require(actual!=bogus,'width-two false linearization rejection')
    tariff=[(3,1),(6,7),(3,8),(-1,24),(-1,23),(-1,22)]
    movement=[sum(c*moment_interval(n)[(c<0)^j] for c,n in tariff) for j in (0,1)]
    require(movement[0]>0,'complete 321 movement deficit')
    counts={k:sum(kind==k for kind,_ in ops) for k in ('ADD','SCALE','NATIVE')}
    require(counts=={'ADD':11,'SCALE':8,'NATIVE':3},'actual primitive ledger')
    result={'status':'PASS_EXACT_UNRESTRICTED_CUBIC_CONTROLS','source_power_supports':[1,2,4,8,16],
      'inverse_modulus_probes':bounds,'noncommuting_flag_formulas':2,'constructor_original_columns':48,
      'constructor_profile':[3,2,1],'extra_ordinary_counts':{'ADD':11,'SCALE_minus_one':8},
      'rejected_primitive_omissions':len(omitted),'quadratic_pullback_control_is_ordinary':True,
      'false_tensor_linearization_rejected':True,'unrestricted_cubic_profile_excluded':[3,3,3],
      'movement_deficit_199_over_200':[str(x) for x in movement],
      'conservative_added_ordinary_supplement':{'ADD':12*24+11,'SCALE':12*48+8,'MONO':12*38+4},
      'profitable_cubic_profiles_remaining':[[3,2,2],[3,3,1],[3,3,2]],'new_complete_kappa':False,
      'scope':'Finite exact source controls support the separate all-width proof; the benchmark is not a supplier.',
      'proof_sha256':pins['local_proof_sha256'],'baseline':pins['baseline']}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
