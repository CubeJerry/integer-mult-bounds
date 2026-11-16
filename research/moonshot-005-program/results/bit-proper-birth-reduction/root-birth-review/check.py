#!/usr/bin/env python3
"""Independent audit of a zero-prefix birth relocation, including all costs."""
from __future__ import annotations
import argparse,copy,hashlib,json
from fractions import Fraction
from pathlib import Path
from optimize_word import independent_replay


def main():
    p=argparse.ArgumentParser()
    for key in ['base','word','out']:p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();raw=a.word.read_bytes();w=json.loads(raw);base_raw=a.base.read_bytes();base=json.loads(base_raw)
    assert w['base_word_sha256']==hashlib.sha256(base_raw).hexdigest()
    assert w['targets']==base['targets'] and w['charts']==base['charts']
    replacements={'P6':('Extra6','EXTRA_AFF'),'P7':('D3_21','AFF0')}
    for name,(chart,first_source) in replacements.items():
        uses=[o for o in base['operations'] if o[1]==name or (o[0]=='ADD' and o[2]==name)]
        assert uses[:3]==[['INIT',name,'Hub'],['MOVE',name,chart],['ADD',first_source,name]]
    expected=[]
    for op,n,*q in base['operations']:
        if n in replacements and op=='INIT':expected.append([op,n,replacements[n][0]])
        elif n in replacements and op=='MOVE' and q[0]==replacements[n][0]:continue
        else:expected.append([op,n,*q])
    assert expected==w['operations']
    before,after=independent_replay(base),independent_replay(w)
    delta={d:after['movement_profile'].get(d,0)-before['movement_profile'].get(d,0) for d in range(1,9)}
    assert {d:n for d,n in delta.items() if n}=={2:-2}
    assert after['counts']['MOVE']==before['counts']['MOVE']-2
    for k in ['INIT','ADD','CLEAR']:assert after['counts'][k]==before['counts'][k]
    scale=1<<160
    def power_interval(n):
        if n==1:return Fraction(1),Fraction(1)
        target=n**199*scale**200;lo,hi=0,n*scale+1
        while hi-lo>1:
            mid=(hi+lo)//2
            if mid**200<=target:lo=mid
            else:hi=mid
        assert lo**200<=target<(lo+1)**200
        return Fraction(lo,scale),Fraction(lo+1,scale)
    def moment(profile):
        low=high=Fraction(0)
        for n,c in profile.items():
            x,y=power_interval(n)
            low+=c*(x if c>=0 else y);high+=c*(y if c>=0 else x)
        return low,high
    q=moment(after['movement_profile']);invoice={127:37,64:74,1:-74}
    for j in range(1,9):invoice[1+7*j]=invoice.get(1+7*j,0)+74;invoice[7*j]=invoice.get(7*j,0)-74
    limit=tuple(x/6 for x in moment(invoice));room=limit[0]-q[1],limit[1]-q[0]
    assert room[0]>0
    controls=[]
    for n,(chart,_) in replacements.items():
        bad=copy.deepcopy(w);bad['operations'][bad['operations'].index(['INIT',n,chart])]=['INIT',n,'zero']
        try:independent_replay(bad)
        except AssertionError:controls.append(n)
        else:raise AssertionError('accepted uncocharted birth')
    def encode(v):return {'lower_fraction':str(v[0]),'upper_fraction':str(v[1])}
    report={'status':'PASS_ROOT_INDEPENDENT_ZERO_PREFIX_BIRTH_RELOCATION',
      'base_word_sha256':hashlib.sha256(base_raw).hexdigest(),'word_sha256':hashlib.sha256(raw).hexdigest(),
      'both_first_use_witnesses_verified':True,'operations_exactly_two_birth_relocations_and_two_MOVE_deletions':True,
      'before':before,'after':after,'exact_movement_saving':'2[2]',
      'independent_price':{'method':'binary fixed point2^160, exact integer200th roots','moment':encode(q),'limiting_room':encode(room),'saving':encode(moment({2:2}))},
      'wrong_ground_birth_controls_rejected':controls,
      'scope':'All222 exact formal endpoints, rational chart geometry, custody and complete movement invoice. No old history/stock/source-cut inheritance; full supplier and all foundations remain open.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(report['status'])


if __name__=='__main__':main()
