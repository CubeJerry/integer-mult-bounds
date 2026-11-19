#!/usr/bin/env python3
"""Exact native terminal support gate, inheriting the admitted rank coefficients."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip,json
PINS={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','routes':'6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036','pairs':'9ec1cca0763b1c365a7c76a3ada6fcbd0ae90e434e9fed347cf5a958ff22ed50','rank_certificate':'e7015bd9e1111ec8d4c3ebaa30460d767b66ea1d7e8a33279b9f033c0053dc57'}

def load(p,key,jsonl=False):
    raw=gzip.decompress(p.read_bytes());assert sha256(raw).hexdigest()==PINS[key]
    return[json.loads(s)for s in raw.splitlines()]if jsonl else json.loads(raw)

def rank(vectors):
    p={}
    for x in vectors:
        while x:
            k=x.bit_length()-1
            if k in p:x^=p[k]
            else:p[k]=x;break
    return len(p)

def ceil(q):return -(-q.numerator//q.denominator)

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    L=load(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','layout')
    R=load(base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','routes',True)
    cuts=load(base/'bit-near-minimum-foreign-rank/author/output/ALL-PAIR-CUTS.json.gz','pairs')
    cert=load(base/'bit-near-minimum-foreign-rank/author/CERTIFICATE.json.gz','rank_certificate')
    roots=L['root_table'];H=list(map(set,L['A2']));D=list(map(set,L['D4']))
    orth=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))==0
    neighbors={i:{j for j in range(111)if orth(i,j)}for i in range(111)}
    assert sum(map(len,neighbors.values()))==6470 and max(len(d&set(range(111)))for d in D)==12
    early=Counter(r[7]for r in R if r[0]=='X'and r[7]is not None);late=Counter(r[1]for r in R if r[0]=='Y')
    assert len(R)==106560 and set(late.values())=={480}
    coefficients={}
    for x in cuts:
        i,j=x['receiver'],x['donor'];assert j in neighbors[i]
        assert (i,j)not in coefficients;coefficients[i,j]=Q(x['coefficient'])
    assert set(coefficients)=={(i,j)for i in range(111)for j in neighbors[i]}
    assert max(coefficients.values())==Q(9,2)
    rows=[]
    for i in range(111):
        cs=[coefficients[i,j]for j in sorted(neighbors[i])];capacity=12*(early[i]+late[i])
        hmin=next(h for h in range(481)if sum(max(0,480-int(c*h))for c in cs)<=capacity)
        ratio=(Q(len(cs))-Q(12*(early[i]+late[i]),480))/sum(cs)
        rows.append({'receiver':i,'donors':len(cs),'early':early[i],'late':late[i],'sum_coefficients':str(sum(cs)),
                     'rational_excess_ratio_floor':str(ratio),'first_h_passing_necessary_floor':hmin})
    chosen={i:next(x for x in rows if x['receiver']==i)for i in [26,34,80]}
    assert chosen[26]=={'receiver':26,'donors':60,'early':360,'late':480,'sum_coefficients':'363/2','rational_excess_ratio_floor':'26/121','first_h_passing_necessary_floor':104}
    assert chosen[34]['rational_excess_ratio_floor']=='26/121'and chosen[34]['first_h_passing_necessary_floor']==104
    assert chosen[80]['donors']==62 and chosen[80]['early']==360 and chosen[80]['sum_coefficients']=='14239/72'and chosen[80]['first_h_passing_necessary_floor']==100
    for i,special in [(26,[49,86,93]),(34,[8,40,82])]:
        assert Counter(coefficients[i,j]for j in neighbors[i])==Counter({Q(3):57,Q(7,2):3})
        assert sorted(j for j in neighbors[i]if coefficients[i,j]==Q(7,2))==special
    scaled=[]
    for b in [480,1920,5760]:
        cs=[coefficients[26,j]for j in sorted(neighbors[26])]
        h=next(h for h in range(b)if sum(max(0,b-int(c*h))for c in cs)<=21*b)
        before=sum(max(0,b-int(c*(h-1)))for c in cs);after=sum(max(0,b-int(c*h))for c in cs)
        assert before>21*b>=after
        scaled.append({'b':b,'h':h,'previous_left_side':before,'capacity':21*b,'passing_left_side':after})
    assert [x['h']for x in scaled]==[104,413,1238]
    assert Q(41,279)>Q(16,480)and Q(26,121)>Q(279,7000)
    assert 8**199>7**200 and Q(182,121)>Q(279,1000)
    uniform480=next(h for h in range(480)if 62*(480-(9*h)//2)<=21*480);assert uniform480==71
    # Independent native witness: five real D exits into one K with31 donor support.
    tiles=[12,99,549,600,968];k=370
    union=set().union(*(D[d]&set(range(111))for d in tiles));assert len(union)==31
    assert {1,80}<=H[k]
    fields=[]
    for d in tiles:
        assert H[k]<=D[L['dual_D4'][d]]
        matches=[r for r in R if r[0]=='Y'and r[4]==d and r[5]==k];assert len(matches)==1
        r=matches[0];fields.append(111*480+r[1]*480+r[2])
    assert len(set(fields))==5
    # Complete small linear domain with overlapping support sets{0,1},{1,2}.
    cases=0;maximum=0
    for p,q in product(range(16),repeat=2):
        packets=[p,q<<2]
        actual_support=sum(sum(bool(row&(3<<(2*j)))for j in range(3))for row in packets)
        for coefficients_out in product(range(4),repeat=2):
            output=[(packets[0]if t&1 else 0)^(packets[1]if t&2 else 0)for t in coefficients_out]
            total=sum(rank([(row>>(2*j))&3 for row in output])for j in range(3))
            assert total<=actual_support<=4;maximum=max(maximum,total);cases+=1
    assert cases==4096 and maximum==4
    # A shared K shear genuinely invalidates the one-D premise if misapplied.
    first=(1<<12)-1;second=first<<12;aggregate=first^second
    assert aggregate.bit_count()==24 and rank([3,2])==2
    assert all((aggregate>>j)&1 for j in range(24))and 24>12
    out={'status':'PASS_NATIVE_ONE_D_PACKET_TARGET_GATE','pins':PINS,'inherited_rank_certificate_frames':len(cert['frames']),
         'new_native_capacity_census':True,'inherited_rank_coefficients_reproved':False,'receivers':rows,'selected':chosen,
         'bank480_uniform_h_floor':uniform480,'scaled_bank480_exact_floors':scaled,
         'restricted_architecture':'each informative F arrival depends on donors from one D; all early+late arrivals counted',
         'shared_K_escape':{'K':k,'tiles':tiles,'native_donors':sorted(union),'late_owner_fields':fields,'support_size':31},
         'binary_small_support_cases':cases,'small_attained_support_bound':maximum,'shared_K_control_support':24,
         'universal_native_code_exclusion':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status']);print('receiver26 floor26/121; b480 h>=104; K370 shared support31')
if __name__=='__main__':main()
