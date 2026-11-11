#!/usr/bin/env python3
"""Exact source-bound helper fragmentation. No new kappa."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from functools import cmp_to_key,lru_cache
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE='e54523517d0f03e58352e647c403a5af3e525a57'
SOURCE_SHA='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
SOURCE_BLOB='ff3256f0d3ffbfc56b062f9ec0fdbbc7b30e76d5'
D=1<<128

def need(ok,message):
    if not ok:raise ValueError(message)

def authenticate(raw):
    need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'source SHA256 mismatch')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==SOURCE_BLOB,'source Git blob mismatch')
    return json.loads(raw)

def hist(raw):
    need(type(raw) is dict and bool(raw),'histogram object')
    out={}
    for key,count in raw.items():
        need(type(key) is str and key.isdigit() and str(int(key))==key,'canonical rank key')
        rank=int(key);need(1<=rank<=145,'rank range')
        need(type(count) is int and count>0,'positive integral multiplicity');out[rank]=count
    return out

def combine(*terms):
    out=Counter()
    for a,h in terms:
        for r,c in h.items():out[r]+=a*c
    return {r:c for r,c in sorted(out.items()) if c}

def floor_root(n,k):
    need(type(n) is int and n>=0 and type(k) is int and k>=1,'root domain')
    if n<2 or k==1:return n
    x=1<<((n.bit_length()+k-1)//k)
    for _ in range(n.bit_length()+k+8):
        y=((k-1)*x+n//pow(x,k-1))//k
        if y>=x:
            need(pow(x,k)<=n<pow(x+1,k),'root neighboring powers');return x
        x=y
    raise ValueError('root iteration bound')

@lru_cache(None)
def power(r):
    need(type(r) is int and 1<=r<=145,'power rank')
    n=pow(r,199)*pow(D,200);a=floor_root(n,200);b=a if pow(a,200)==n else a+1
    return Q(a,D),Q(b,D)

def interval(h):
    lo=hi=Q(0)
    for r,c in h.items():
        a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return lo,hi

def balanced(r,k):
    need(type(r) is int and type(k) is int and 1<=k<=r,'partition domain')
    q,s=divmod(r,k);out={q:k-s}
    if s:out[q+1]=s
    return out

def options(H):
    out=[]
    for r,n in sorted(H.items()):
        for k in range(1,r):
            delta=combine((1,balanced(r,k+1)),(-1,balanced(r,k)))
            need(interval(delta)[0]>0,'positive marginal gain')
            out.append({'rank':r,'from_parts':k,'multiplicity':n,'delta':delta})
    def cmp(a,b):
        diff=combine((1,a['delta']),(-1,b['delta']))
        if not diff:
            aa=(a['rank'],a['from_parts']);bb=(b['rank'],b['from_parts']);return (aa>bb)-(aa<bb)
        lo,hi=interval(diff);need(lo>0 or hi<0,'marginal ordering unresolved');return -1 if lo>0 else 1
    return sorted(out,key=cmp_to_key(cmp))

def allocation(T,H,opts,q,occurrences,repeat):
    need(type(q) is int and q>=0,'extra-target budget')
    out=dict(T);left=q;chosen=[];used={}
    for o in opts:
        take=min(left,o['multiplicity']*occurrences)
        if take:
            r,k=o['rank'],o['from_parts'];need(k==1 or take<=used.get((r,k-1),0),'chain predecessor')
            used[r,k]=take;out=combine((1,out),(repeat*take,o['delta']))
            chosen.append({'rank':r,'from_parts':k,'chosen':take});left-=take
    need(left==0,'extra-target capacity');need(all(c>0 for c in out.values()),'target multiplicity')
    return out,chosen

def threshold(T,P,H,opts,occurrences,repeat):
    maximum=occurrences*sum((r-1)*c for r,c in H.items())
    def margin(q):return interval(combine((1,allocation(T,H,opts,q,occurrences,repeat)[0]),(-1,P)))
    need(margin(0)[1]<0 and margin(maximum)[0]>0,'threshold endpoints')
    lo,hi=0,maximum
    while hi-lo>1:
        mid=(lo+hi)//2;a,b=margin(mid);need(a>0 or b<0,'threshold separation')
        if a>0:hi=mid
        else:lo=mid
    need(margin(lo)[1]<0 and margin(hi)[0]>0,'sharp threshold')
    target,chosen=allocation(T,H,opts,hi,occurrences,repeat)
    return {'minimum_extras':hi,'previous_margin':margin(lo),'minimum_margin':margin(hi),'target':target,'allocation':chosen}

def tails(T2,P):
    d=combine((1,T2),(-1,P));num=den=1;out=[]
    for r in sorted((r for r in d if r>=2),reverse=True):
        c=d[r]
        if c>0:num*=pow(r,c)
        else:den*=pow(r,-c)
        need(num>den,'nonpositive descending logarithmic tail')
        out.append({'minimum_rank':r,'numerator_bits':num.bit_length(),'denominator_bits':den.bit_length(),'strict_positive':True})
    return out

def partitions(n,least=1):
    if n==0:yield ();return
    for a in range(least,n+1):
        for rest in partitions(n-a,a):yield (a,)+rest

def controls(raw,T,P,H,T2):
    bad=[{}, {'01':1},{'0':1},{'146':1},{'1':0},{'1':-1},{'1':True},{1:1}]
    for x in bad:
        try:hist(x)
        except ValueError:pass
        else:raise ValueError('malformed histogram accepted')
    for x in [raw+b' ',raw.replace(b'73766',b'73666',1)]:
        try:authenticate(x)
        except ValueError:pass
        else:raise ValueError('changed source accepted')
    count=0
    for r in range(1,10):
        for p in partitions(r):
            diff=combine((1,dict(Counter(p))),(-1,balanced(r,len(p))))
            need(not diff or interval(diff)[1]<0,'unbalanced partition exceeds optimum');count+=1
    need(count==96,'partition coverage')
    need(interval(combine((1,T2),(-1,P),(100,{1:1})))[0]>0,'missing-paid sensitivity')
    refined=combine((1,T2),(-1,T),(18,H))
    need(interval(combine((1,T),(1,refined),(-1,P)))[0]>0,'missing original debit sensitivity')
    return {'malformed_histograms_rejected':len(bad),'source_mutations_rejected':2,'exact_partitions':count,'unpaid_100_rank1_false_crossing_detected':True,'undeleted_original_target_false_crossing_detected':True}

def encode(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(y) for y in x]
    return x

def compute(raw):
    s=authenticate(raw);need(s['status']=='PASS_INDEPENDENT_FULL_GATE','source status')
    T=hist(s['invoice']['T']);P=hist(s['invoice']['P']);H=hist(s['native']['helpers'])
    need(s['gate']['claim']=='363005817/100000000000','source claim')
    need(s['precision']['rounded_envelope']['caller']['fresh_arbitrary_helpers']==18*sum(H.values()),'18 distinct invocations')
    root=combine((1,T),(-18,H));need(all(c>0 for c in root.values()),'root remainder')
    need(sum(r*c for r,c in T.items())-sum(r*c for r,c in P.items())==s['invoice']['S']==1520,'surplus')
    need(sum(T.values())==23392 and sum(P.values())==117612 and sum(H.values())==1080,'source counts')
    opts=options(H);refined={}
    for limit in (1,2,3,9):
        hh={}
        for r,c in H.items():hh=combine((1,hh),(c,balanced(r,min(r,limit))))
        tt=combine((1,root),(18,hh));refined[limit]={'target':tt,'margin':interval(combine((1,tt),(-1,P)))}
    need(refined[2]['margin'][1]<0<refined[3]['margin'][0],'binary/ternary discrimination')
    free=threshold(T,P,H,opts,18,1);same=threshold(T,P,H,opts,1,18)
    need(free['minimum_extras']==22954 and same['minimum_extras']==1276,'sharp threshold changed')
    hh=combine((1,same['target']),(-1,root));need(all(c%18==0 for c in hh.values()),'helper divisibility')
    hh={r:c//18 for r,c in hh.items()};need(hh=={1:13,2:18,3:1808,4:408,5:109},'threshold helper profile')
    return encode({'status':'PASS_SHARP_HELPER_FRAGMENTATION','base':BASE,'source_sha256':SOURCE_SHA,'target_kappa':'1/200','t':'199/200','classification':'Exact invoice-level relaxation and source-bound binary ceiling; No new kappa','T':T,'P':P,'H':H,'root_targets':root,'rank_surplus':1520,'at_most_descendants':refined,'arbitrary_occurrence_threshold':free,'identical_native_threshold':same,'threshold_native_helpers':hh,'paid_slack_per_native':[x/18 for x in same['minimum_margin']],'marginal_order':opts,'binary_log_tail_certificate':tails(refined[2]['target'],P),'controls':controls(raw,T,P,H,refined[2]['target'])})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--source',type=Path,default=HERE/'inputs/FULL-RESULT.json');args=ap.parse_args()
    result=compute(args.source.read_bytes());receipt=HERE/'RESULT.json'
    if args.write:receipt.write_text(json.dumps(result,indent=2)+'\n')
    else:need(json.loads(receipt.read_text())==result,'frozen result mismatch')
    print('PASS_SHARP_HELPER_FRAGMENTATION')
    print('extras: caller=22954; repeated_native=1276; ternary_rank9_helpers=554')
    print('binary continuum: positive exact log tails; kappa>=1/200 rejected in stated scope')
    print('No new kappa; no physical fragmentation construction or complete assembly claimed.')

if __name__=='__main__':main()
