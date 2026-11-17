#!/usr/bin/env python3
"""Independent exact flag-rank census and price; no root/author imports."""
import argparse,hashlib,json
from fractions import Fraction as Q
from functools import cache
from pathlib import Path

def require(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def binary_rank(rows):
    piv={}
    for row in rows:
        row=set(row)
        while row:
            p=min(row)
            if p in piv:row^=piv[p]
            else:piv[p]=row;break
    return len(piv)

@cache
def root_interval(d):
    scale=10**31;target=d**199*scale**200;lo=0;hi=d*scale+1
    while lo+1<hi:
        x=(lo+hi)//2
        if x**200<=target:lo=x
        else:hi=x
    if lo**200==target:hi=lo
    return Q(lo,scale),Q(hi,scale)

def price(profile):
    low=high=Q(0)
    for d,c in profile.items():
        x,y=root_interval(d);low+=c*(x if c>=0 else y);high+=c*(y if c>=0 else x)
    return low,high

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    require(sha(a.native)=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native pin')
    require(sha(a.word)=='74fb050a6afb8d8e1b6895b0f092220f8e6852365a7516ef4db2284c43c1a5ee','word pin')
    roots=json.loads(a.native.read_text())['native_roots'];word=json.loads(a.word.read_text());cert=json.loads(a.certificate.read_text())
    U=sorted(set(range(111))-set(word['targets']));require(len(U)==54,'unknown partition')
    neigh={i:{j for j in U if sum(x*y for x,y in zip(roots[i],roots[j]))==0}for i in U}
    rows={i:neigh[i]|{i}for i in U};require(binary_rank(rows.values())==9,'canonical rank nine')
    for i in U:require(binary_rank([r-neigh[i]for r in rows.values()])==9,'zero canonical/local intersection')
    order=cert['coordinate_flag'];require(order==[7,6,5,4,3,2,0,1] and sorted(order)==list(range(8)),'full exact coordinate flag')
    groups=[];ranks=[]
    for k,c in enumerate(order):
        # Flag stratum = support contained in first k+1 coordinates and using c.
        previous=set(order[:k]);allowed=previous|{c}
        roles=[i for i in U if roots[i][c]!=0 and {j for j,x in enumerate(roots[i])if x}<=allowed]
        rank=binary_rank([rows[i]for i in roles]);entry=cert['strata'][k]
        require(entry['level']==k+1 and entry['added_coordinate']==c and entry['roles']==roles,'independent exact stratum')
        require(entry['canonical_row_rank']==rank,'stratum rank')
        given=[{j for j in U if int(x,16)>>j&1}for x in entry['binary_basis_hex']]
        require(len(given)==binary_rank(given)==rank and binary_rank(given+[rows[i]for i in roles])==rank,'provided rank basis spans actual rows')
        if roles:
            # This property is checked for every vector in a stratum, not just one witness.
            require(all(roots[i][c]!=0 and all(roots[i][q]==0 for q in order[k+1:])for i in roles),'universal leading-coordinate pattern')
            groups.append({'last_coordinate':c,'roles':roles,'canonical_rank':rank});ranks.append(rank)
    require(ranks==[1,4,6,7,8] and sum(ranks)==26,'five-stratum rank sum')
    require(sorted(i for g in groups for i in g['roles'])==U,'disjoint complete partition')
    packet=tuple(Q(26,5)*x for x in root_interval(5));base=price({1:165,6:108,7:114});gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    cap=tuple(x/6 for x in price(gate));gap=(base[0]+packet[0]-cap[1],base[1]+packet[1]-cap[0]);require(gap[0]>Q(3,2),'strict excess > 1.5')
    imported_gap=list(map(Q,cert['excess']['rational']));require(gap[0]<=imported_gap[0]<=imported_gap[1]<=gap[1],'independent enclosure contains root enclosure')
    enlarged=neigh[5]|{5};require(binary_rank([r-enlarged for r in rows.values()])==8,'own-input source control')
    require(binary_rank(rows.values())==9,'single collapsed stratum only gives nine')
    from decimal import Decimal,localcontext
    with localcontext()as ctx:
        ctx.prec=60;display=[str(Decimal(q.numerator)/Decimal(q.denominator))for q in gap]
    result={'status':'PASS_INDEPENDENT_ANY_IMMUTABLE_CANONICAL_BANK_FLAG_GATE','source_pins':{'native':sha(a.native),'word':sha(a.word),'certificate':sha(a.certificate)},'strata':groups,'stratum_ranks':ranks,'rank_sum':26,'packet_floor_rational':list(map(str,packet)),'excess_rational':list(map(str,gap)),'excess_decimal':display,'allfield_scope':'Every characteristic-two field, every positive block width, arbitrary finite redundant fixed canonical packet bank; all other postcut inward information excluded.','controls':['own x5 grant invalidates uniqueness','collapsed flag only gives9'],'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'],ranks,'excess',display[0])

if __name__=='__main__':main()
