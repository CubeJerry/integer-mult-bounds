"""Price the information-theoretic ideal and certify the least finite multiplicity."""
import argparse
from fractions import Fraction as Q
import importlib.util
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--repo',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    a=p.parse_args()
    R=a.repo/'research/moonshot-005-program/results'
    s=importlib.util.spec_from_file_location('s029_tariff',R/'bit-covariant-single-grade-budget/author/check.py')
    x=importlib.util.module_from_spec(s);s.loader.exec_module(x)
    P,T,q=x.ordered_profiles(a.repo)
    ideal=dict(q);ideal[8]=Q(9)
    profile=lambda M,h:x.histograms((P,T,{**ideal,8:Q(9)+Q(h,3840)}),M)
    for M,c in [(2,9),(4,13),(None,13)]:
        H,K=profile(M,0)
        assert x.centered_log(H,0,c)[1]<0 and x.centered_log(K,1,c)[0]>0
    def bracket(M):
        lo=0;hi=10**12
        while hi>lo+1:
            mid=(lo+hi)//2;g=x.raw_gap(profile(M,0),Q(mid,10**14))
            if g[0]>0:lo=mid
            elif g[1]<0:hi=mid
            else:raise ValueError('precision exhausted')
        return [f'{z//10**14}.{z%10**14:014d}' for z in (lo,hi)]
    ideal_m=bracket(870);lim=bracket(None)
    assert x.raw_gap(profile(2,0),Q(lim[0]))[1]<0
    least={}
    for h in [0,1,16,32,64,96,120,127,128,129,130,134,135]:
        slope=x.raw_gap(profile(None,h),Q(1,200))
        g2=x.raw_gap(profile(2,h),Q(1,200))
        if slope[1]<=0:
            assert g2[1]<=0
            least[h]=None
            continue
        assert slope[0]>0
        # Start at a rational estimate and certify both neighboring even integers.
        m=max(2,2*int(-g2[0]/(2*slope[0]))+2)
        while x.raw_gap(profile(m,h),Q(1,200))[0]<=0:m+=2
        while m>2 and x.raw_gap(profile(m-2,h),Q(1,200))[0]>0:m-=2
        assert m==2 or x.raw_gap(profile(m-2,h),Q(1,200))[1]<0
        least[h]=m
    assert least[0]==46 and least[64]==86 and least[128]==870 and least[135] is None
    assert ideal_m==['0.00504096857045','0.00504096857046']
    assert lim==['0.00504325518580','0.00504325518581']
    rec={'price':'1/200','ideal_870_raw_open_bracket':ideal_m,'unattained_ideal_limit_open_bracket':lim,
         'minimum_even_m_by_excess_at_1_over_200':least,'floor_at_bank3840':34560,
         'contract':'all nonreturn ranks and the movement tariff fixed; necessary raw paid/productive comparison only'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')


if __name__=='__main__':
    main()
