#!/usr/bin/env python3
"""Exact controls for the scope of the raw-donor zero-slice argument."""
from argparse import ArgumentParser
from pathlib import Path
import gzip, json


def rank(rows):
    p={}
    for v in rows:
        while v:
            k=v.bit_length()-1
            if k not in p:p[k]=v;break
            v^=p[k]
    return len(p)


def solution(equations):
    piv={}
    for v,c in equations:
        while v:
            k=v.bit_length()-1
            if k not in piv:piv[k]=(v,c);break
            w,d=piv[k];v^=w;c^=d
        else:assert c==0
    x=0
    for k,(v,c) in sorted(piv.items()):
        if ((v&x).bit_count()&1)!=c:x^=1<<k
    assert all(((v&x).bit_count()&1)==c for v,c in equations)
    return x


def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--census',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();p=a.repo/'research/moonshot-005-program/results'
    lay=json.loads(gzip.decompress((p/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
    old=json.loads(gzip.decompress((p/'bit-stripe-varying-port-cut/review/output/RESULT.json.gz').read_bytes()))
    records=json.loads(gzip.decompress(a.census.read_bytes()))['donors'];roots=lay['root_table'][:111]
    K=[sum(1<<j for j,v in enumerate(roots) if i==j or sum(x*y for x,y in zip(u,v))==0) for i,u in enumerate(roots)]
    assert rank(K)==9 and rank(K+[1,2])==11
    x=solution([(v,0) for v in K]+[(1,0),(2,1)])
    # X_0=0 and KX=0 do not neutralize the mixed helper X_0+X_1.
    assert x&1==0 and (x>>1)&1==1 and all((v&x).bit_count()%2==0 for v in K)
    oldcaps={z['plane']:z['rank_cap'] for z in old['records']}
    increases=[(z['zeroed_donor'],d['H'],oldcaps[d['H']],d['alpha']) for z in records
               for d in z['changed_color_instances'] if oldcaps[d['H']]<d['alpha']]
    assert increases
    result={'status':'PASS_RAW_DONOR_SCOPE_CONTROLS','mixed_helper_not_neutralized':True,
            'mixed_helper_donors':[0,1],'canonical_zero_witness_hex':hex(x),
            'old_color_caps_cannot_be_reused':True,'increased_color_caps':len(increases),
            'first_increased_cap':list(increases[0]),'arbitrary_mixed_helper_transfer_rejected':True}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CONTROLS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])


if __name__=='__main__':main()
