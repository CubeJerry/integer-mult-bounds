#!/usr/bin/env python3
"""Independent exact112-port conditional invoice review.
Uses no author arithmetic or caller implementation. @CubeJerry/OpenAI.
"""
import argparse,hashlib,json
from fractions import Fraction as F
from pathlib import Path
from functools import lru_cache

BASE=Path(__file__).resolve().parents[2]
AUTHOR=BASE/'worker-a/involutive112-caller-budget'
NATIVE=BASE/'worker-b/logical-involution-112'
PREC=10**38
t=F(199,200)
def need(x,m):
    if not x:raise ValueError(m)
def interval_add(*args):return(sum(x[0]for x in args),sum(x[1]for x in args))
def scale(x,c):return(c*x[0],c*x[1])if c>=0 else(c*x[1],c*x[0])
def difference(x,y):return interval_add(x,scale(y,-1))
@lru_cache(None)
def power(n):
    if n in(0,1):return F(n),F(n)
    z=n**199*PREC**200;lo=0;hi=n*PREC+1
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**200<=z:lo=mid
        else:hi=mid
    need(lo**200<=z<hi**200,'exact integer200th-power enclosure')
    return F(lo,PREC),F(hi,PREC)
def moment(d):return interval_add(*(scale(power(int(k)),F(c))for k,c in d.items()))
def W(a):
    d={1:-4,1+16*a:2}
    for j in range(1,a+1):d[1+8*j]=d.get(1+8*j,0)+4
    for j in range(1,a):d[8*j]=d.get(8*j,0)-4
    return moment(d)
def deltaW(a):return interval_add(scale(difference(power(1+16*(a+1)),power(1+16*a)),2),scale(difference(power(9+8*a),power(8*a)),4))
def gain(a,Q):return difference(scale(W(a),112),scale(Q,2*a))
def increment(a,Q):return difference(scale(deltaW(a),112),scale(Q,2))
def target_delta(a,Q):return difference(scale(gain(a+1,Q),4*a+2),scale(gain(a,Q),4*a+6))

def long_gain(a,Q,prefix):
    M=a-1;L=prefix+1;need(1<=L<M,'nonempty integral tail')
    def g(x):return difference(power(8*x+1),power(8*x))
    def derivative(x):return scale(difference(scale(power(8*x+1),F(1,8*x+1)),scale(power(8*x),F(1,8*x))),8*t)
    def anti(x):return scale(difference(scale(power(8*x+1),8*x+1),scale(power(8*x),8*x)),F(1,8*(t+1)))
    head=interval_add(*(g(j)for j in range(1,L)))
    base=interval_add(difference(anti(M),anti(L)),scale(interval_add(g(L),g(M)),F(1,2)))
    error=scale(difference(derivative(M),derivative(L)),F(1,8));need(error[0]>0,'positive convex trapezoid error bound')
    tail=(base[0],base[1]+error[1]);total=interval_add(head,tail)
    ww=interval_add(scale(power(1+16*a),2),scale(power(1+8*a),4),(-F(4),-F(4)),scale(total,4))
    return difference(scale(ww,112),scale(Q,2*a)),{'exact_prefix_terms':prefix,'tail_range':[L,M],'tail_error_upper':error[1]}

def source_profiles():
    import gzip
    profiles={}
    pins={'R0':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','R1':'86b8a1098e8fd18959e9fbfbfcb84d9f4bd157838936aeb94d656be5ce8ed5c7','R0-minimal':'c06724af5a2c414e62887ea78124d268cad2cabf500f9963ad5d0e9758c8a336'}
    for name,pin in pins.items():
        blob=(NATIVE/'output'/name/'WORD.json.gz').read_bytes();need(hashlib.sha256(blob).hexdigest()==pin,'reviewed actual source pin')
        w=json.loads(gzip.decompress(blob));q={};raw={}
        for o in w['program']:
            if o[0]=='MOVE':
                r=abs(len(w['frames'][o[2]])-len(w['frames'][o[3]]));q[r]=q.get(r,0)+1
                if not o[4]:raw[r]=raw.get(r,0)+1
        need(sum(k*v for k,v in raw.items())==448*8,'all448 complete rank-eight raw paths')
        profiles[name]=q
    return profiles

def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return{str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return[enc(v)for v in x]
    return x
def main():
    global AUTHOR,NATIVE
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=AUTHOR);p.add_argument('--native',type=Path,default=NATIVE);p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args();AUTHOR=a.author;NATIVE=a.native
    pins={'PROOF.md':'8e160dec4ee5cfd899388b1e1d06ae0c5284f4d328532cdeec5ca1308e2ed826','check.py':'4a0f0c0451a3bfedec303aaa09d15dcf55036556bbd4e979490bc1117c5fd9be','RESULT.json':'ee0aaa4b9332d26dbd57f7fef13eb79cc6fa228127b38904a4ba8ec5b1d7a33f'}
    for name,pin in pins.items():need(hashlib.sha256((AUTHOR/name).read_bytes()).hexdigest()==pin,'frozen budget pin '+name)
    author=json.loads((AUTHOR/'RESULT.json').read_text());profiles=source_profiles();records=[]
    H5=difference(scale(W(6),5),scale(W(5),6));H6=difference(scale(W(7),6),scale(W(6),7));need(H5[0]>0 and H6[1]<0,'universal per-native maximum at a6')
    for label,name,at,aq in [('R','R1',7,19),('R0','R0',10,24812)]:
        q=profiles[name];Q=moment(q);need({int(k):v for k,v in author['sources'][label]['stipulated_profile'].items()}==q,'stipulated profile matches actual separately reviewed source')
        ds=[increment(aq-1,Q),increment(aq,Q)];js=[target_delta(at-1,Q),target_delta(at,Q)];need(ds[0][0]>0>ds[1][1]and js[0][0]>0>js[1][1],'both global optimizer crossings')
        small=scale(gain(6,Q),F(1,12));target=scale(gain(at,Q),F(1,4*at+2))
        if aq<100:query=scale(gain(aq,Q),F(1,4));method='direct exact finite sum'
        else:
            broad,_=long_gain(aq,Q,0);tight,method=long_gain(aq,Q,32);query=scale(tight,F(1,4));broad=scale(broad,F(1,4));need(broad[0]<=query[0]<query[1]<=broad[1],'independent32-term refinement lies within broad trapezoid enclosure')
        ref=list(map(F,author['sources'][label]['largest_query_only_debit']['exact']));need(max(query[0],ref[0])<=min(query[1],ref[1]),'independent query ceiling agrees with author interval')
        floor=scale(power(8),448);need(difference(Q,floor)[0]>0,'actual source exceeds all-raw direct floor')
        records.append({'source':label,'actual_profile':q,'source_moment':Q,'per_native_maximum_stages':12,'per_native_ceiling':small,'uniform_target_maximum_stages':2*at,'uniform_target_ceiling':target,'query_maximum_stages':2*aq,'query_ceiling':query,'query_signs':ds,'target_signs':js,'long_query_method':method})
    positive=difference(gain(6,moment(profiles['R0'])),(F(30*56),F(30*56)));need(positive[0]>0,'conditional56-unit query/target positive control')
    negative=difference(records[1]['uniform_target_ceiling'],(F(112),F(112)));need(negative[1]<0,'112-unit target repair excluded for every arm')
    smallconstants=[difference(power(2),(F(2),F(2))),difference(interval_add(scale(power(4),2),scale(power(2),4)),(F(16),F(16)))];need(all(z[1]<0 for z in smallconstants),'strict doublecaller coefficients')
    minimalQ=moment(profiles['R0-minimal']);minimal=scale(gain(6,minimalQ),F(1,12))
    result={'status':'PASS_INDEPENDENT_FULL112_CONDITIONAL_BUDGET_REVIEW','pins':pins,'all_arm_per_native_signs':[H5,H6],'sources':records,'conditional56_scenario':positive,'uniform112_target_repair_margin':negative,'doublecaller_strict_coefficients':smallconstants,'actual_smaller_meeting_per_native_allowance_at12':minimal,'scope':'Exact invoice implications and all-arm proof checks; physical caller/query/normalizer and baseline recursion remain premises. Actual native movement histograms are independently recounted. No new kappa.'}
    a.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n');print(json.dumps({'status':result['status'],'query_ceiling_refined':[float(x)for x in records[1]['query_ceiling']],'minimal_per_native':[float(x)for x in minimal]}))
if __name__=='__main__':main()
