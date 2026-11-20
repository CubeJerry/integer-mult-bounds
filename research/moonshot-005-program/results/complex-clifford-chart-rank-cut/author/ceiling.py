"""Transfer a certified linear-volume and 199/200 price cut to a smaller saving."""
from fractions import Fraction as Q
from functools import cache
from pathlib import Path
from hashlib import sha256
from math import isqrt
import argparse,gzip,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import need
from flag import APPLICATION
GRID=1<<256

@cache
def lift(k,s):
    if k==1:return Q(1),Q(1)
    def mul(X,Y):return X[0]*Y[0]//GRID,-(-X[1]*Y[1]//GRID)
    a=b=k*GRID;z=(GRID,GRID);rem=s
    for _ in range(104):
        if not rem:break
        a=isqrt(a*GRID);w=isqrt(b*GRID);b=w+(w*w!=b*GRID);bit,rem=divmod(2*rem,1)
        if bit:z=mul(z,(a,b))
    if rem:z=(z[0],mul(z,(a,b))[1])
    return Q(z[0],GRID),Q(z[1],GRID)

def moment(hist,s):
    lo=hi=0
    for k,n in hist.items():
        a,b=lift(int(k),s);lo+=n*a;hi+=n*b
    return lo,hi

def check(app,M,V,micro):
    s0=Q(199,200);k=Q(micro,10**6);s=1-k
    ratios=[]
    for j in range(2,10):
        t0,t1=lift(j,s0);u0,_=lift(j,s);ratios.append((u0-t1)/(j-t0))
    lam=Q(int(min(ratios)*10**6),10**6)
    need(all(lift(j,s)[0]>=(1-lam)*lift(j,s0)[1]+lam*j for j in range(1,10)),'nine exact grade comparisons')
    lower=(1-lam)*M+lam*V;call=app['caller_census'];n=call['calls'];H=moment(app['native']['positive_helper_ranks'],s);T=moment(call['fixed_root_targets'],s);P=moment(call['fixed_caller_paid'],s);allowed=H[1]+(T[1]-P[0])/n
    return lower>allowed,{'saving_trial':str(k),'exponent':str(s),'linear_mix_weight':str(lam),'paid_native_moment_lower_exact':str(lower),'native_allowance_upper_exact':str(allowed),'strict_gap_lower_rounded_down_10dp':int((lower-allowed)*10**10)/10**10}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--application',type=Path,required=True);ap.add_argument('--flag-result',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=gzip.decompress(a.application.read_bytes());need(sha256(raw).hexdigest()==APPLICATION,'pinned caller');app=json.loads(raw);res=json.loads(a.flag_result.read_text());M=Q(res['weighted_flag_flow']['native_moment_lower']);V=res['optimal_cumulative_paid_grade'];lo,hi=3700,4900
    while hi-lo>1:
        mid=(lo+hi)//2;ok,receipt=check(app,M,V,mid)
        if ok:hi=mid
        else:lo=mid
    ok,receipt=check(app,M,V,hi);need(ok,'certificate at displayed trial');receipt['status']='PASS_FULL_INTERVAL_ARCHITECTURE_PRICE_CEILING';receipt['volume_lower']=V;receipt['moment_lower_at_199_over_200']=str(M);a.out.mkdir(exist_ok=True,parents=True);(a.out/'CEILING.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(receipt['saving_trial'],receipt['strict_gap_lower_rounded_down_10dp'])
if __name__=='__main__':main()
