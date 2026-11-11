"""Independent exact dual certificate and Abel-product obstruction. No author imports."""
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent
def need(b,msg):
    if not b:raise ValueError(msg)
def combine(*terms):
    out=Counter()
    for c,h in terms:
        for r,n in h.items():out[r]+=c*n
    return {r:n for r,n in sorted(out.items()) if n}
D=10**24;cache={}
def power(r):
    if r not in cache:
        z=r**199*D**200;lo=0;hi=r*D+1
        while hi-lo>1:
            mid=(lo+hi)//2
            if mid**200<=z:lo=mid
            else:hi=mid
        cache[r]=(Q(lo,D),Q(hi,D))
    return cache[r]
def interval(h):
    lo=hi=Q(0)
    for r,c in h.items():
        a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi
def view(h):
    a,b=interval(h)
    return {'lower':str(a),'upper':str(b),'midpoint':float((a+b)/2)}
def partitions(n,minimum=1):
    if not n:yield ();return
    for r in range(minimum,n+1):
        for p in partitions(n-r,r):yield (r,)+p
def witness_partition(r):return (r,) if r<=5 else (r//2,r-r//2)
def gain(r,p):return combine((1,Counter(p)),(-1,{r:1}))
def main(source):
    raw=source.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    need(sha=='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7','source SHA')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='ff3256f0d3ffbfc56b062f9ec0fdbbc7b30e76d5','source blob')
    j=json.loads(raw);T={int(r):n for r,n in j['invoice']['T'].items()};P={int(r):n for r,n in j['invoice']['P'].items()}
    H={int(r):n for r,n in j['native']['helpers'].items()}
    need(H=={1:13,2:18,3:44,4:215,5:68,6:42,7:18,8:67,9:595},'source helpers')
    need((sum(T.values()),sum(P.values()))==(23392,117612),'source counts')
    mass=lambda h:sum(r*n for r,n in h.items())
    need((mass(T),mass(P),mass(H))==(321364,319844,7650),'source masses')
    root=combine((1,T),(-18,H));need(all(c>=0 for c in root.values()) and sum(root.values())==3952,'fixed root')
    original=combine((1,T),(-1,P));lam={3:3,4:-1,5:-1}
    need(interval(lam)[0]>0,'positive dual multiplier')
    L={};checked=0;ties=[]
    for r in range(1,10):
        base=witness_partition(r)
        L[r]=combine((1,gain(r,base)),(-(len(base)-1),lam))
        for p in partitions(r):
            score=combine((1,gain(r,p)),(-(len(p)-1),lam),(-1,L[r]))
            if score:need(interval(score)[1]<0,'dual domination '+str((r,p)))
            else:ties.append([r,list(p)])
            checked+=1
    need(checked==96,'all partitions')
    def dual(q):return combine((1,original),(q,lam),*((18*n,L[r]) for r,n in H.items()))
    def target(extra):
        h=Counter(root)
        for r,n in H.items():
            for s in witness_partition(r):h[s]+=18*n
        need(0<=extra-12996<=10710,'rank9 replacement domain')
        return combine((1,h),(extra-12996,lam))
    for q in (22953,22954):
        need(combine((1,target(q)),(-1,P))==dual(q),'dual-attaining witness')
        need(mass(target(q))==mass(T) and sum(target(q).values())==sum(T.values())+q,'witness conservation')
    need(interval(dual(22953))[1]<0 and interval(dual(22954))[0]>0,'sharp global threshold')
    need(interval(dual(18*1275))[1]<0 and interval(dual(18*1276))[0]>0,'sharp repeated threshold')
    new=Counter()
    for r,n in H.items():
        for s in witness_partition(r):new[s]+=n
    new=combine((1,new),(554,lam))
    need(new=={1:13,2:18,3:1808,4:408,5:109},'repeated profile')
    need(sum(new.values())==sum(H.values())+1276 and mass(new)==mass(H),'native conservation')
    binary=Counter(root)
    for r,n in H.items():
        for s in ((1,) if r==1 else (r//2,r-r//2)):binary[s]+=18*n
    d=combine((1,binary),(-1,P));need(interval(d)[1]<0,'binary endpoint negative')
    # log-tail positivity, checked as exact products, implies derivative sign
    # by Abel summation for EVERY real t>=0, without sampled exponents.
    numerator=denominator=1;tails=[]
    for r in sorted((r for r in d if r>1),reverse=True):
        c=d[r]
        if c>0:numerator*=r**c
        else:denominator*=r**(-c)
        need(numerator>denominator,'positive exact logarithmic tail')
        tails.append({'least_rank':r,'numerator_bits':numerator.bit_length(),'denominator_bits':denominator.bit_length()})
    need(len(tails)==24,'all derivative tails')
    # Controls isolate real errors, not harmless numeric perturbations.
    need(interval(combine((1,d),(18,H)))[0]>0,'duplicate original helper credit detected')
    need(interval(combine((1,d),(100,{1:1})))[0]>0,'omitted100 paid rank1 changes sign')
    wrong=combine((1,gain(9,(3,3,3))),(-1,gain(9,(4,5))),(-1,{1:1}))
    need(interval(wrong)[1]<0,'wrong dual unit cannot tie both rank9 maximizers')
    return {'status':'PASS_INDEPENDENT_DUAL_ABEL_REVIEW','base':'e54523517d0f03e58352e647c403a5af3e525a57',
      'source_sha256':sha,'no_new_kappa':True,'partition_cases':checked,'dual_ties':ties,'lambda':view(lam),
      'threshold_moments':{str(q):view(dual(q)) for q in (22953,22954,18*1275,18*1276)},
      'binary_moment':view(d),'binary_target':dict(sorted(binary.items())),'log_tails':tails,
      'repeated_native_profile':new,'repeated_target':target(18*1276),'paid':P,
      'negative_controls':['duplicate old helper credit','omit100 paid rank1','wrong dual multiplier'],
      'scope':'Integer partitions within each original helper; fixed paid/root; no physical realization or admission.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=HERE/'source/FULL-RESULT.json');a=p.parse_args()
    print(json.dumps(main(a.source),indent=2))
