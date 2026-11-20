#!/usr/bin/env python3
"""Independent dyadic review of the covariant BIT tariff and its single-grade width."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from math import isqrt
import json
from pathlib import Path
import subprocess


BASE = "914097a04bb93f730b805e9d4f036b46707c8675"
PINS = {
    "paired": ("research/paired-query-only-bit/EFREE-RESULT.json",
               "a46b6c6040f75184cab5467656811ad988c216e3bc8e44d595a5015b6e49620b"),
    "budget": ("research/moonshot-005-program/results/bit-asymmetric-balanced-atlas/author/output/BUDGET.json",
               "b82eebcefb3dd80df57582793cb7d0ad89cf2da4ef196fc79714c2a29c2e29cd"),
    "endpoint": ("research/moonshot-005-program/results/bit-two-sided-covariant-target/author/output/RESULT.json",
                 "4151df493670c7912ef613e8d6de490bcb2af9b1f95d9dc065e05594da2ef4c1"),
}
GRID = 1 << 360
BITS = 140
TARGET = F(1,200)
RAW = F(".0050000005")
LANES = 23040
V = 1 << 42


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def read(repo, key):
    name, digest = PINS[key]
    local = repo / name
    raw = (local.read_bytes() if local.is_file() else
           subprocess.check_output(["git", "-C", str(repo), "show", f"{BASE}:{name}"]))
    need(sha256(raw).hexdigest() == digest, f"source pin {key}")
    return json.loads(raw)


def bounds(x):
    return (F(x).__floor__(), F(x).__ceil__())


def mul(x, y):
    """Outward fixed-grid multiplication of nonnegative endpoints."""
    return x[0]*y[0]//GRID, -(-x[1]*y[1]//GRID)


def sqrt_interval(x):
    lo, upper = isqrt(x[0]*GRID), x[1]*GRID
    h = isqrt(upper)
    return lo, h + (h*h != upper)


@cache
def power(base, s):
    """No transcendental functions: repeated square roots and binary exponent expansion."""
    base, s = F(base), F(s)
    need(base >= 1 and 0 <= s <= 1, "power domain")
    root = bounds(base*GRID)
    if s == 1:
        return F(root[0], GRID), F(root[1], GRID)
    result = (GRID, GRID)
    tail = s
    for _ in range(BITS):
        if not tail:
            break
        root = sqrt_interval(root)
        bit, tail = divmod(2*tail, 1)
        if bit:
            result = mul(result, root)
    if tail:
        result = (result[0], mul(result, root)[1])
    return F(result[0], GRID), F(result[1], GRID)


@cache
def log2_range(base):
    """Binary logarithm by interval squaring and reduction to [1,2)."""
    base = F(base)
    need(base >= 1, "log domain")
    e = base.numerator.bit_length()-base.denominator.bit_length()
    if F(2)**e > base:
        e -= 1
    z = base/F(2)**e
    if z == 1:
        return F(e), F(e)
    y = bounds(z*GRID)
    bits, length = 0, 0
    for _ in range(BITS):
        y = mul(y,y)
        if y[0] >= 2*GRID:
            y = y[0]//2,-(-y[1]//2)
            bit = 1
        elif y[1] < 2*GRID:
            bit = 0
        else:
            break
        bits = 2*bits + bit
        length += 1
    return e+F(bits,2**length),e+F(bits+1,2**length)


def total(terms):
    lo = hi = F(0)
    for a, (x,y) in terms:
        if a < 0:
            x,y = y,x
        lo += a*x
        hi += a*y
    return lo,hi


def ln2_range():
    # -log(1-x)=sum x^j/j; the residual is bounded by a geometric series.
    last = 140
    lo = sum(F(1,j*2**j) for j in range(1,last+1))
    return lo, lo+F(1,(last+1)*2**last)


def centered_logs(profile, c, weighted):
    base_lo,base_hi = log2_range(c)
    lo,hi = total((z*(r if weighted else 1), (log2_range(r)[0]-base_hi,log2_range(r)[1]-base_lo))
                  for r,z in profile.items())
    u,v = ln2_range()
    return min(lo*u,lo*v), max(hi*u,hi*v)


def enclosure(x, digits=20):
    scale = 10**digits
    p = (x[0]*scale).__floor__()
    q = (x[1]*scale).__ceil__()
    return [str(F(p,scale)),str(F(q,scale))]


def from_json(h):
    return {int(r):F(n) for r,n in h.items()}


def combine(*parts):
    out = Counter()
    for weight, hist in parts:
        for k, val in hist.items():
            out[k] += weight*val
    return {k:v for k,v in out.items() if v}


def profiles(repo):
    paired,budget,endpoint = (read(repo, key) for key in ("paired","budget","endpoint"))
    pure = paired["ordinary_admitted"]
    need(F(pure) == F(".00385248"), "historical ordinary offer")
    # Use the literal two-call receipt and a physical, four-binary-copy movement count.
    old_p,old_t = from_json(paired["paid"]),from_json(paired["targets"])
    n,h = from_json(paired["native_paid"]),from_json(paired["native_helpers"])
    bank = budget["base_bank"]
    old_move = from_json(budget["invoices"]["4"]["MOVE"])
    ratio = F(endpoint["retained_repair_rank"],endpoint["bank"])
    need(F(endpoint["return_rank"],endpoint["bank"]) == 9+ratio and ratio == F(1,30),"return")
    q = combine((F(1,4*bank),old_move),(ratio,{8:1}))
    need(q == {1:F(4451,8),2:F(7213,16),4:24,8:F(271,30)}, "tariff from proper movements")
    def at(m):
        return (combine((F(m,2),old_p),(-18*(m-1),n),(18*(m-1),q)),
                combine((F(m,2),old_t),(-18*(m-1),h)))
    at2,at4 = at(2),at(4)
    derivative = tuple(combine((F(1,2),b),(-F(1,2),a)) for a,b in zip(at2,at4))
    return at,derivative


def moment(profile, s):
    return total((count,power(k,s)) for k,count in profile.items())


def gap(pair, saving):
    paid,productive = pair
    return moment(combine((1,productive),(-1,paid)),1-saving)


def slope_checks(at,derivative):
    sums={}
    for key,pair,c,t_min,p_max in [("m2",at(2),9,4171,-27247),
                                  ("m4",at(4),13,3617,-116067),
                                  ("m_linear_coefficient",derivative,13,1944,-1810)]:
        paid,productive=pair
        t = centered_logs(productive,c,False)
        p = centered_logs(paid,c,True)
        need(t[0]>t_min and p[1]<p_max,f"slope bounds {key}")
        sums[key]={"at_log_center":c,"productive_derivative_at_zero":enclosure(t),
                   "paid_derivative_at_one":enclosure(p)}
    need(centered_logs(at(2)[1],13,False)[1]<0,"m=2 needs its own certified separator")
    return sums


def bracket_checks(at,derivative):
    bounds={}
    for label,pair,literal in [
            ("870",at(870),(".00500000060450",".00500000060451")),
            ("asymptotic",derivative,(".00500220831285",".00500220831286"))]:
        l,r = map(F,literal)
        a,b = gap(pair,l),gap(pair,r)
        need(a[0] > 0 > b[1], f"crossing {label}")
        bounds[label]={"saving":list(literal),"left_gap":enclosure(a),"right_gap":enclosure(b)}
    need(gap(at(2),TARGET)[1]<0<gap(derivative,TARGET)[0],"intercept barrier")
    need(gap(at(868),TARGET)[1]<0<gap(at(870),TARGET)[0],"first even multiplicity")
    need(gap(at(870),F(".0050000007"))[1]<0,"overpriced finite word")
    return bounds


def multinomial_mode(areas,v):
    """Divisor search gives the v largest W_k k^t/j weights; certify the last cut."""
    intervals = {rank:(n*power(rank,1-RAW)[0],n*power(rank,1-RAW)[1]) for rank,n in areas.items()}
    midpoint = {k: (a+b)/2 for k,(a,b) in intervals.items()}
    whole = sum(midpoint.values())
    low,high = F(v,whole),F(v+2*len(midpoint),whole)
    def count(scale):
        return {k:(scale*w).__floor__() for k,w in midpoint.items()}
    need(sum(count(low).values()) <= v <= sum(count(high).values()), "mode divisor bracket")
    for _ in range(250):
        scale = (low+high)/2
        counts = count(scale)
        n = sum(counts.values())
        if n==v:
            break
        if n<v:
            low=scale
        else:
            high=scale
    else:
        raise ValueError("mode unresolved")
    selected_min = min(intervals[k][0]/n for k,n in counts.items() if n)
    unselected_max = max(intervals[k][1]/(n+1) for k,n in counts.items())
    need(selected_min>unselected_max, "modal exchange strictly optimal for exact real weights")
    return counts,selected_min-unselected_max


def grade_checks(pair):
    raw_paid,raw_target=pair
    paid, target = (combine((LANES,h)) for h in (raw_paid,raw_target))
    need(all(x.denominator==1 for table in (paid,target) for x in table.values()), "integer roles")
    t=1-RAW
    P_t,T_t,P_1=moment(paid,t),moment(target,t),sum(r*n for r,n in paid.items())
    need((sum(paid.values()),sum(target.values())) == (416127105216,42455715840),
         "full productive and paid lane counts")
    counts,mode_gap=multinomial_mode(target,V)
    base=F(99,2)
    log_lo,log_hi=log2_range(base)
    grade_add=total((n,(log2_range(k)[0]-log_hi,log2_range(k)[1]-log_lo)) for k,n in counts.items())
    need(grade_add[0]>0, "grade above (99/2)^v")
    cutoffs={}
    for label,cut,savingpower in [("original",13,RAW),("integral_quadratic",160,RAW/2)]:
        c_lo,c_hi=power(cut,savingpower)
        deficit= min(1-P_t[1]/T_t[0],1-P_1/(T_t[0]*c_lo))
        need(V*deficit>630>13*43+3,"funded single grade")
        cutoffs[label]={"v_times_slack_lower":str(F((V*deficit*10**12).__floor__(),10**12))}
    need(49**19 > sum(target.values())*13**19 and 49**18 < sum(target.values())*13**18,
         "author cutoff degree")
    need(99**18 > sum(target.values())*(4*160)**9, "improved width degree")
    need((F(99,2)**2/F(160))**F(17,1)<sum(target.values())**2,"coarse degree-17 check")
    # Universal restrictions for every funded single-grade word at the stated price.
    s=F(1,1000)
    shifted=moment(target,t+s)
    k_obstruction=power(50,s)[0]*P_t[0]-shifted[1]
    h_obstruction=P_1-power(F(25,2),RAW)[1]*T_t[1]
    b_obstruction=P_t[0]-4**17*power(50,t)[1]
    need(min(k_obstruction,h_obstruction,b_obstruction)>0,"universal K,h,B bounds")
    need(F(156)<F(25,2)**2,"too-aggressive cutoff fails even perfect integer packing")

    return {"raw_t":"1989999999/2000000000","product_power":V,"type_counts":counts,
            "scaled_paid_slots":int(sum(paid.values())),"scaled_productive_slots":int(sum(target.values())),
            "strict_modal_exchange_lower":str(F((mode_gap*10**18).__floor__(),10**18)),
            "log2_K_minus_v_log2_99_over_2":enclosure(grade_add,10),
            "funding_certificates":cutoffs,"new_cutoff":"160^(v/2)",
            "conditional_productive_width":"N^18",
            "width_proof_lhs":99**18,"width_proof_rhs":int(sum(target.values()))*(4*160)**9,
            "sharpness_for_fixed_7828_schedule":{
                "T_t_upper_times_12_5_power_below_P1_by_at_least":int(h_obstruction),
                "P_t_lower_times_50_power_s_above_T_shifted_by_at_least":int(k_obstruction),
                "P_t_lower_above_4_power_17_50_power_t_by_at_least":int(b_obstruction),
                "saving":str(RAW),"shift_s":str(s),
                "necessary_relations":["h>(25/2)^v","K<50^v","B>4^(17v)","B>(K/h)^17"],
                "excluded":"W_N=O(N^17) for any one fixed funded macro using the specified homogeneous batch B^D"
            }}


def service_checks():
    old=F(".00385248")
    U,C,O=F(".0050000004"),F(".0050000003"),F(".0050000002")
    r=F(1,128)
    threshold=TARGET*(1-old)/(1-TARGET)
    need(threshold>F(".00500220831286"),"all-m one stage obstruction")
    stages=[old]
    for _ in range(4):
        stages.append(C/(1+C-stages[-1]))
    need(stages[2]<TARGET<stages[3]<O<stages[4],"minimum ideal stage counts")
    need(TARGET<O<C<U<RAW and C<min(r,1-r),"strict open ordinary guards")
    need(F(1,250)<TARGET,"old atom power fails")
    return {"one_stage_required_covered":str(threshold),"finite_stage_suprema":[str(z) for z in stages],
            "self_hosted_atom":str(r),"ordinary_offer":str(O)}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--repo",type=Path,required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    at,delta=profiles(args.repo)
    need(power(16,F(1,4))==(2,2) and power(81,F(1,2))==(9,9),"positive power controls")
    for k,a,b in [(2,F(1,3),F(2,3)),(127,F(123,257),F(134,257))]:
        x,y=power(k,a),power(k,b)
        need(x[0]*y[0]<=k<=x[1]*y[1],"complementary power bounds")
    need(70+16>18*4 and 70+256>18*16 and 70+64<18*8,"chord failure away from raw endpoint")
    check={"status":"PASS_INDEPENDENT_SINGLE_GRADE_REVIEW_AND_SHARP_INTEGER_WIDTH",
           "sources":{key:{"path":path,"sha256":digest} for key,(path,digest) in PINS.items()},
           "slope_separation":slope_checks(at,delta),"strict_price_brackets":bracket_checks(at,delta),
           "m870_gap_at_chosen_saving":enclosure(gap(at(870),RAW),17),
           "compiler":grade_checks(at(870)),"ordinary":service_checks(),
           "negative_controls":["old atom exponent","small m with unqualified cutoff 13",
              "interior chord obstruction","m=868","overpriced finite word","all-m one-stage",
              "cutoff 156^(v/2)","degree 17 homogeneous restored-batch schedule"],
           "new_complete_kappa":False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"RESULT.json").write_text(json.dumps(check,indent=2,sort_keys=True)+"\n")
    print(check["status"])
    print("power",V,"certified sharp integer width degree",18)


if __name__=="__main__":
    main()
