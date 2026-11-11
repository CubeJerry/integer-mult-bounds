"""Fresh independent compiler-specification audit; no author scientific imports."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from arithmetic import F,S,need,exact,add,sub,mul,scale,div,log,power,moment,report

def main(source):
    raw=source.read_bytes()
    need(hashlib.sha256(raw).hexdigest()=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','source SHA')
    j=json.loads(raw);original={int(r):n for r,n in j['invoice']['T'].items()};P={int(r):n for r,n in j['invoice']['P'].items()};H={int(r):n for r,n in j['native']['helpers'].items()}
    new=Counter()
    for r,n in H.items():
        for i in range(n):
            if r==9:p=(3,3,3) if i<554 else (4,5)
            elif r>=6:p=(r//2,r-r//2)
            else:p=(r,)
            need(sum(p)==r,'partition conservation');new.update(p)
    need(sum(new.values())-sum(H.values())==1276,'extra native targets')
    T=Counter(original)
    for r,n in H.items():T[r]-=18*n
    for r,n in new.items():T[r]+=18*n
    T={r:n for r,n in T.items() if n}
    need((sum(T.values()),sum(P.values()))==(46360,117612),'complete counts')
    need(sum(r*n for r,n in T.items())==321364 and sum(r*n for r,n in P.items())==319844,'complete masses')
    C=F(500007,100000000);t=1-C;u=F(1,7);v=1920
    TT=moment(T,t);PP=moment(P,t);alpha=div(PP,TT)
    gamma=div(moment(P,t+u),mul(power(11,u),TT))
    lam=div(mul(power(12,u),moment(T,t-u)),TT)
    bounds=[F(12499990009,12500000000),F(19,20),F(977,1000)]
    for a,b in zip((alpha,gamma,lam),bounds):need(F(a[1],S)<b<1,'strict ratio')
    a,g,l=bounds;complete=1/(1+v*(1-a))+2*g**v+l**v
    need(complete<F(999,1000),'full paid plus lost-target tail')
    completion=div(exact(12*sum(T.values())),mul(power(11,C),TT));need(completion[0]>S,'old completion test fails')
    old=div(PP,moment(original,t));need(old[0]>S,'unfragmented invoice fails')
    need(11**29<12**28 and 2*11**(1920*29)<=153**(1920*28),'theta and actual ambient')
    theta=sub(log(28),log(29));logt=sub(log(t.numerator),log(t.denominator))
    def log_checks(ambient,p):
        base=scale(log(ambient),1920*C);eta=sub(logt,base)
        return sub(eta,scale(theta,p)),sub(scale(log(2),p),base)
    lm=log_checks(153,1377);need(all(a[0]>0 for a in lm),'log majorant')
    need(log_checks(153,1376)[0][1]<0,'previous p fails')
    need(log_checks(145,1362)[0][0]>0 and log_checks(153,1362)[0][1]<0,'false ambient fails actual requirement')
    step=100000000;idx=58398;HH=step*idx;p=1377
    need((HH+1)**p<2**idx,'uniform threshold')
    need((step*(idx-1)+1)**p>=2**(idx-1),'previous grid fails')
    # An unrelated exact toy detects retaining discarded target credits.
    def square(h):
        z=Counter()
        for r,n in h.items():
            for s,m in h.items():z[r*s]+=n*m
        return z
    toyT=square({2:3,7:1});toyP=square({1:4,4:1})
    keep={r:n for r,n in toyT.items() if r>=16};drop={r:n for r,n in toyT.items() if r<16}
    split=Counter()
    for r,n in toyP.items():
        q,s=divmod(r,9);split[9]+=q*n
        if s:split[s]+=n
    split={r:n for r,n in split.items() if n};mass=lambda h:sum(r*n for r,n in h.items())
    before=mass(toyT)-mass(toyP);after=mass(keep)-mass(split)
    need(mass(split)==mass(toyP),'all paid rank retained')
    need(before-after==mass(drop) and before>0>after,'lost target debit changes conclusion')
    need(max(split)<min(keep),'separated toy sizes')
    need(256>16+2*64,'u<C invalid-tail counterexample')
    for k in range(1,7):
        z=sum(46360**(k-1-i)*117612**i for i in range(k))
        need(z==(1 if k==1 else 46360*prev+117612**(k-1)),'raw occurrence count');prev=z
    return {'status':'PASS_INDEPENDENT_COMPILER_SPECIFICATION_REVIEW','no_new_kappa':True,
      'source_sha256':hashlib.sha256(raw).hexdigest(),'target':T,'paid':P,'tested_C':str(C),
      'moment':report(sub(TT,PP)),'alpha':report(alpha),'gamma':report(gamma),'lambda':report(lam),
      'tail_upper':float(complete),'tail_less_than':'999/1000','log_margins':[report(a) for a in lm],
      'log_power':p,'H':HH,'old_completion':report(completion),'unfragmented_alpha':report(old),
      'toy':{'before':before,'after':after,'discarded_mass':mass(drop),'split_paid':split},
      'controls':['unfragmented fails','old completion fails','false145 ambient fails153','p1376 fails','previous H fails','omitted target debit','u<C'],
      'scope':'Sufficient arithmetic specification only; physical1276 native and covered BIT remain unbuilt.'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=HERE.parent/'source/research/shared-wire-split-composition/FULL-RESULT.json');a=ap.parse_args()
    print(json.dumps(main(a.source),indent=2))
