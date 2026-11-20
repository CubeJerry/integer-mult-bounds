"""Bound the paid-tail infimum over every tilt on the grade-14 native target tariff."""
import argparse,importlib.util,json
from fractions import Fraction as F
from pathlib import Path

def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    r=a.repo/'research/moonshot-005-program/results';n=module('native',r/'bit-covariant-single-grade-budget/author/check.py');b=module('rebalance',r/'bit-covariant-rebalanced-cutoffs/author/check.py')
    P,T=n.histograms(n.ordered_profiles(a.repo),870);k=F('0.0050000005');t=1-k
    den=n.moment(T,k);alpha=b.div(n.moment(P,k),den)
    def priced(u):
        v=(F(0),F(0));d=v
        for rank,count in P.items():
            ll=n.add(n.log_int(rank),n.scale(-1,n.log_int(14)))
            s=n.add(n.scale(t,n.log_int(rank)),n.scale(u,ll))
            ww=n.scale(count,(b.exp_at(s[0])[0],b.exp_at(s[1])[1]))
            v=n.add(v,ww);d=n.add(d,b.mult(ww,ll))
        return b.div(v,den),b.div(d,den)
    lo=F(46,1000);hi=F(49,1000)
    fl,dl=priced(lo);fh,dh=priced(hi);assert dl[1]<0<dh[0]
    # A tangent underestimates this convex sum everywhere; to the right its negative slope costs at most the interval width.
    lower=fl[0]+(hi-lo)*dl[0]
    gl=F('0.99743');al=F('0.99999999985663')
    assert lower>gl and alpha[0]>al
    def cert(v):return 1/(1+v*(1-al))+2*gl**v
    assert cert(5500)>1 and cert(832)>F(123,100)
    g22=priced(F(11,50))[0];assert g22[0]>1
    rec={'upstream_head':'43007c979859fa84ccc3a3509ccacc9620d181fa','raw_price':str(k),'raw_source':'m=870, h=128, same paid and target ranks','paid_cut_base':14,'all_real_tilts_paid_ratio_strictly_above':str(gl),'paid_mass_ratio_strictly_above':str(al),'smallest_certified_excluded_range':[1,5500],'published_copies':832,'published_tilt':'11/50','published_tilt_paid_ratio_above_one':True,'at_832_normalized_bill_strictly_above':'123/100','productive_tail_omitted_from_lower_bound':True}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
