#!/usr/bin/env python3
"""Dedicated m=870 study of the native PR 7835 grade-14 paid cutoff."""
import argparse,gzip,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from price import D,Q,LOW,HIGH,build,moment,power,product,quotient,need,exact

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--upstream-replay',type=Path);a=p.parse_args()
    P,T=build(a.repo);t=D('.9949999995');c=14;b=16;M=moment(T,t);A=quotient(moment(P,t),M)
    def terms(u):return {r:quotient(product(exact(n),power(r,LOW.add(t,u))),product(power(c,u),M))for r,n in P.items()}
    def deriv(u):
        lo=hi=D(0)
        for r,v in terms(u).items():
            c0=LOW.ln(D(c));r0=LOW.ln(D(r));L=(LOW.subtract(LOW.next_minus(r0),HIGH.next_plus(c0)),HIGH.subtract(HIGH.next_plus(r0),LOW.next_minus(c0)))
            x,y=product(v,L);lo=LOW.add(lo,x);hi=HIGH.add(hi,y)
        return lo,hi
    low=D('.0475140288');high=D('.0475140290');sg0,sg1=deriv(low),deriv(high)
    need(sg0[1]<0<sg1[0],'strict convex optimum bracket')
    le,ri=terms(low),terms(high);gmin=sum(Q(min(le[r][0],ri[r][0]))for r in P)
    G=quotient(moment(P,t+D('.047514029')),product(power(c,D('.047514029')),M));L=quotient(product(power(b,D('.3')),moment(T,t-D('.3'))),M)
    round_up=lambda x:Q((Q(x)*10**15).__ceil__(),10**15)
    aup,gup,lup=map(round_up,[A[1],G[1],L[1]])
    alo=Q((Q(A[0])*10**15).__floor__(),10**15);glo=Q((gmin*10**15).__floor__(),10**15)
    lower=lambda v:alo**v+2*glo**v
    upper=lambda v:1/(1+v*(1-aup))+2*gup**v+lup**v
    need(lower(5754)>1 and upper(5755)<1,'minimum powers across every nonnegative paid tilt, even free target tail in lower bound')
    original=quotient(moment(P,t+D('.22')),product(power(c,D('.22')),M));need(original[0]>1,'literal grade14 tilt cannot fund any positive power')
    result={'parameters':{'m':870,'trial_saving':'0.0050000005','paid_cutoff':14,'productive_floor':16},'exact_7835_tilt_paid_ratio_lower':str(original[0]),'all_nonnegative_tilts_minimizer_bracket':[str(low),str(high)],'derivative_outer_bounds':[str(sg0[1]),str(sg1[0])],'global_paid_ratio_lower_15_digits':str(glo),'paid_ratio_witness_upper':str(gup),'raw_ratio_upper':str(aup),'discarded_target_upper':str(lup),'positive_tilt_witness':'0.047514029','first_feasible_power':5755,'previous_power_lower_gap':float(lower(5754)-1),'first_power_upper_gap':float(1-upper(5755)),'v832_lower_excess':float(lower(832)-1),'v88_lower_excess':float(lower(88)-1),'m870_mixed31_power':88,'scope':'same separately bounded tilted prepaid split and target discard certificate'}
    if a.upstream_replay:
        src=Path(__file__).resolve().parents[1]/'sources';dig={}
        for nm in ('RESULT.json','BIT.json','AUDIT.json'):
            raw=(a.upstream_replay/nm).read_bytes();need(raw==(src/nm).read_bytes(),'pinned upstream replay '+nm);dig[nm]=hashlib.sha256(raw).hexdigest()
        result['upstream_replayed_receipts_sha256']=dig
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result)
if __name__=='__main__':main()
