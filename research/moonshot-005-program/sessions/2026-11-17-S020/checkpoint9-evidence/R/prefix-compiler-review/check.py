"""Independent exact primitive checks for the fixed-prefix compiler lemma."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib
import sympy as s

def units(q):
    out=[]
    for phase,x in [(1,s.re(q)),(s.I,s.im(q))]:
        x=s.Rational(x);n=int(x.p);den=int(x.q)
        assert den&(den-1)==0
        k=den.bit_length()-1;sg=1 if n>=0 else -1;n=abs(n);bit=0
        while n:
            if n&1:out.append(phase*sg*s.Rational(2)**(bit-k))
            bit+=1;n>>=1
    assert s.expand(sum(out)-q)==0
    return out

def cross(d,t,src,u,v,q):
    word=[];delta=u^v
    for mask in range(d):
        sign=(-1)**((mask&v).bit_count())
        dest=[j^delta for j in range(d)]
        phase=[(-1)**((mask&j).bit_count()) for j in range(d)]
        ip=[phase[j^delta] for j in range(d)]
        for c in units(s.expand(q*sign/d)):
            word += [('MONO',src,dest,phase),('SCALE',src,c),('ADD',src,t),
                     ('SCALE',src,s.simplify(1/c)),('MONO',src,dest,ip)]
    return word

def cross_two_term(d,t,src,u,v,q):
    word=[];perm=list(range(d));perm[u],perm[v]=perm[v],perm[u]
    minus=[1]*d;minus[v]=-1
    for c in units(s.expand(q/2)):
        for scalar,phase in [(c,[1]*d),(-c,minus)]:
            inverse_phase=[phase[perm[j]] for j in range(d)]
            word += [('MONO',src,perm,phase),('SCALE',src,scalar),('ADD',src,t),
                     ('SCALE',src,s.simplify(1/scalar)),('MONO',src,perm,inverse_phase)]
    return word

def elementary(d,row,col,q,builder=cross):
    t,u=divmod(row,d);src,v=divmod(col,d)
    assert row!=col
    if t!=src:return builder(d,t,src,u,v,q)
    helper=1-t
    # Chronological reverse of E01(P) E10(Q) E01(-P) E10(-Q).
    return (builder(d,helper,t,v,v,-1)+builder(d,t,helper,u,v,-q)+
            builder(d,helper,t,v,v,1)+builder(d,t,helper,u,v,q))

def replay(d,word,omit=None):
    M=s.eye(2*d)
    for ix,op in enumerate(word):
        if ix==omit:continue
        kind,b,*args=op;rr=list(range(b*d,(b+1)*d))
        if kind=='SCALE':
            c=args[0];assert c!=0
            for r in rr:
                for j in range(2*d):M[r,j]=s.expand(c*M[r,j])
        elif kind=='ADD':
            dst=args[0]
            for k in range(d):
                for j in range(2*d):M[dst*d+k,j]=s.expand(M[dst*d+k,j]+M[b*d+k,j])
        else:
            assert kind=='MONO';dest,phase=args;old=M[rr,:]
            assert sorted(dest)==list(range(d)) and all(p in [1,-1,s.I,-s.I] for p in phase)
            for k in range(d):M[b*d+dest[k],:]=phase[k]*old[k,:]
    return M

def valuation(q):
    q=s.expand(q);a=s.Rational(s.re(q));b=s.Rational(s.im(q));den=s.ilcm(a.q,b.q)
    assert int(den)&(int(den)-1)==0
    x=int(a*den);y=int(b*den);assert x or y
    v=-2*(int(den).bit_length()-1)
    while (x-y)%2==0:x,y=(x+y)//2,(y-x)//2;v+=1
    return v

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    checks=[];controls=[]
    for d,row,col,q in [(2,0,3,3),(4,1,6,(3+5*s.I)/8),(4,1,3,(3+5*s.I)/8),(4,2,0,-3)]:
        word=elementary(d,row,col,q);want=s.eye(2*d);want[row,col]=q
        assert replay(d,word)==want
        j=next(i for i,o in enumerate(word) if o[0]=='ADD')
        assert replay(d,word,j)!=want;controls.append({'d':d,'row':row,'col':col,'omitted_ADD':j})
        checks.append({'d':d,'row':row,'col':col,'coefficient':str(q),'literal_primitives':len(word),
                       'ADD':sum(o[0]=='ADD' for o in word),'arbitrary_other_bank_restored':row//d==col//d})
    odd=[]
    for row,col in [(0,5),(1,2)]:
        d=3;q=(3+5*s.I)/8;word=elementary(d,row,col,q,cross_two_term)
        want=s.eye(6);want[row,col]=q;assert replay(d,word)==want
        odd.append({'d':d,'row':row,'col':col,'literal_primitives':len(word),'all_columns_exact':True})
    d=4;u=1+s.I;v=s.simplify(1/u)
    factors=[(0,1,u),(1,0,-v),(0,1,u),(0,1,-1),(1,0,1),(0,1,-1)]
    word=[]
    for row,col,q in reversed(factors):word+=elementary(d,row,col,q)
    want=s.eye(2*d);want[0,0]=u;want[1,1]=v
    assert replay(d,word)==want
    vals=[{'scalar':str(q),'valuation':valuation(q)} for q in [1+s.I,2,(1-s.I)/2,s.I,1/s.Integer(2)]]
    assert [x['valuation'] for x in vals]==[1,2,-1,0,-2]
    # All tested source-scaling coefficients and their inverses are R-units.
    for op in word:
        if op[0]=='SCALE':
            z=op[2];norm=s.expand(z*s.conjugate(z));assert norm>0
            n=s.Rational(norm);assert abs(int(n.p))&(abs(int(n.p))-1)==0 and int(n.q)&(int(n.q)-1)==0
    bad={'d':4,'target':'diag(2,1,1,1) with arbitrary other banks restored','determinant_valuation':2,'divisible_by_d':False}
    assert valuation(2)%4!=0 and valuation((1+s.I)**4)%4==0
    result={'status':'PASS_INDEPENDENT_PREFIX_COMPILER_PRIMITIVES','cross_and_internal_shears':checks,
      'odd_dimension_two_term_selectors':odd,
      'paired_unit_diagonal':{'unit':str(u),'literal_primitives':len(word),'all_columns_exact':True,'borrower_restored':True},
      'scalar_valuations':vals,'determinant_obstruction':bad,'negative_controls':controls,
      'scope':'Finite exact primitive checks support the separate all-d proof; no general elimination implementation, physical compiler, or kappa claim.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
