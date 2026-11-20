"""Test the common-primitive requirement from the live Gaussian outer caller against the actual BIT tariff."""
import argparse,json,importlib.util
from fractions import Fraction as F
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    rr=a.repo/'research/moonshot-005-program/results'
    spec=importlib.util.spec_from_file_location('moment',rr/'bit-covariant-single-grade-budget/author/check.py')
    t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t);p,u,s=t.ordered_profiles(a.repo)
    k=F(1,200);d=k/(1-k);assert d==F(1,199)
    def gap(h,m):return t.raw_gap(t.histograms((p,u,{**s,8:F(9)+F(h,3840)}),m),d)
    def sign(h,m):
        l,r=gap(h,m)
        assert l>0 or r<0
        return 1 if l>0 else -1
    maxima={}
    for m in [46,86,156,404,870,1226,6750,None]:
        if sign(0,m)<0:maxima[str(m)]=None;continue
        lo=0;hi=135;assert sign(hi,m)<0
        while hi>lo+1:
            mid=(lo+hi)//2
            if sign(mid,m)>0:lo=mid
            else:hi=mid
        maxima[str(m)]=lo
    least={}
    for h in [0,8,16,24,32,40,48,49,50,51,52,53,54,55,56,57,58,64,128]:
        if sign(h,None)<0:
            assert sign(h,2)<0;least[h]=None;continue
        lo=2;hi=4
        while sign(h,hi)<0:lo=hi;hi*=2
        while hi>lo+2:
            mid=2*((lo+hi)//4)
            if sign(h,mid)>0:hi=mid
            else:lo=mid
        assert sign(h,hi)>0 and sign(h,hi-2)<0
        least[h]=hi
    dr=F(997,1000);native=F(1737,10**6)
    assert dr*native==F(1731789,10**9)
    # Strict numerical example, tested against each term of the PR's published fixed-tape invoice.
    delta=F(503,100000);axis=F(99499,100000);B=F(9,8);W=F(1,2)
    powers={'dense':axis,'permutations_and_butterflies':1-axis*delta,'cached_chirps':2*(1-axis),
            'sparse_arithmetic_boundary':axis+2*W-B,'sparse_arithmetic_holes':axis+B-2+W,
            'moving_boundary':1+W-B,'moving_holes':1+B-2,'setup_per_bank':0}
    assert max(powers.values())<1-k
    assert 1/(1+delta)==1-delta/(1+delta)
    ceiling=F('0.00504325518581')
    ordinary=ceiling*(1-ceiling)
    assert ordinary<d and ordinary/(1+ordinary)<k
    assert F('0.00505063')*(1-F('0.00505063'))<d<F('0.005051')*(1-F('0.005051'))
    out={'old_compact_wrapper':{'ideal_raw_upper':str(ceiling),'ordinary_saving_upper_from_this_invoice':str(ordinary),'outer_saving_upper_from_this_invoice':str(ordinary/(1+ordinary))},'upstream':'4f0c67d5bb41d4af5501dcd40b3b388b35e0ff02','unchanged_PR_outer_saving':str(dr*native),'common_inner_saving_strictly_above':str(d),'target':str(k),
         'max_excess_by_even_m_for_raw_threshold':maxima,'first_even_m_for_raw_threshold':least,'explicit_conditional_exponent_example':{'inner':str(delta),'axis':str(axis),'cost_powers':{k:str(v) for k,v in powers.items()}},
         'assumptions':'same strength on complete physical ordinary CNOT and grouped complex butterfly suppliers, and valid PR analytical and tape setup on retuned axis; native return options are raw prices only'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(maxima,least)
if __name__=='__main__':main()
