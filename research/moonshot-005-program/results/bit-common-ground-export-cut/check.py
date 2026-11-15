#!/usr/bin/env python3
"""Four exact frame cuts exclude fixed-handoff direct ground broadcasting."""
from __future__ import annotations
import argparse,hashlib,json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

FRAMES=[[0,14,18,30,69,70,107],[2,8,9,14,21,46,88,92],
        [4,11,12,16,36,37,74,78],[4,32,35,55,56,89,93]]
DONORS=[16,19,38,49,50,56,57]
EXPECTED_ACTIVE=[[0,30,69,70,107],[2,8,9,21,46,88,92],
                 [4,11,12,37,74,78],[32,35,89,93]]

def basis(rows):
    out={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in out:row^=out[p]
            else:out[p]=row;break
    return out

def residue(b,row):
    for p in sorted(b,reverse=True):
        if row>>p&1:row^=b[p]
    return row

def rref(rows):
    a=[[Fraction(x)for x in row]for row in rows];k=0
    for c in range(8):
        p=next((i for i in range(k,len(a))if a[i][c]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k];d=a[k][c];a[k]=[x/d for x in a[k]]
        for i in range(len(a)):
            if i!=k:
                d=a[i][c];a[i]=[x-d*y for x,y in zip(a[i],a[k])]
        k+=1
    return tuple(tuple(row)for row in a[:k])

def actual_handoff(word):
    records={f'X{i}':{'chart':f'L{i}','row':1<<i,'owned':False}for i in range(111)}
    records.update({f'Y{i}':{'chart':'zero','row':1<<(111+i),'owned':False}for i in range(111)})
    for op in word['operations']:
        k,n,*rest=op
        if k=='INIT':assert n not in records;records[n]={'chart':rest[0],'row':0,'owned':True}
        elif k=='ADD':
            t=rest[0];assert records[n]['chart']==records[t]['chart'];records[t]['row']^=records[n]['row']
        elif k=='MOVE':records[n]['chart']=rest[0]
        elif k=='CLEAR':assert records[n]['owned'];del records[n]
        else:raise ValueError(k)
    actual={n:{'chart':r['chart'],'value_hex':hex(r['row'])}for n,r in records.items()if r['owned']}
    assert actual==word['expected_owned_at_handoff']
    for i in range(111):
        assert records[f'X{i}']=={'chart':'Hub','row':1<<i,'owned':False}
        assert records[f'Y{i}']['row']==((1<<(111+i))^((1<<i)if i in[17,34]else 0))
    return records

def examine(word,roots,frames=FRAMES,donors=DONORS,mutant=None):
    for F in frames:
        assert len(set(F))==len(F)and not(set(F)&{17,34})
        assert all(sum(x*y for x,y in zip(roots[i],roots[j]))!=0 for i in F for j in F)
    rec=actual_handoff(word);X=(1<<111)-1
    G=[r['row']&X for r in rec.values()if r['chart']=='zero']+[1<<j for j in donors]
    cuts=[]
    for F in frames:
        fm=sum(1<<i for i in F);b=basis([g&fm for g in G])
        cuts.append({'roles':F,'mask':fm,'basis':b,'deficit':len(F)-len(b),
                     'active_points':[j for j in F if residue(b,1<<j)]})
    if mutant=='cross_chart_point':rec['R0']['row']=(1<<0)^(1<<2)
    if mutant=='unpaid_deep_payload':rec['DC0_5']['row']=sum(1<<j for j in[0,2,4,32])
    names=defaultdict(list);groups=defaultdict(list)
    for n,c in word['charts'].items():names[(c['kind'],rref(c['rows']))].append(n)
    for n,r in rec.items():
        c=word['charts'][r['chart']];groups[(c['kind'],rref(c['rows']))].append((n,r['row']&X))
    cells=[]
    for key,rows in groups.items():
        dim=len(key[1])if key[0]=='span'else 8-len(key[1])
        if not dim:continue
        B=list(basis([v for _,v in rows]).values())
        active=[i for i,c in enumerate(cuts)if any(residue(c['basis'],v&c['mask'])for v in B)]
        assert len(active)<=dim,('Cell activity exceeds its rank tariff',names[key],active,dim)
        cells.append({'charts':names[key],'dimension':dim,'records':[n for n,_ in rows],
                      'basis_rows_hex':[hex(v)for v in B],'active_frames':active})
    return {'ground_plus_free_donor_rank':len(basis(G)),
            'actual_ground_rows_hex':[hex(rec[f'P{i}']['row'])for i in range(8)],
            'frames':[{'roles':c['roles'],'rank':len(c['basis']),'deficit':c['deficit'],
                       'active_point_coordinates':c['active_points']}for c in cuts],
            'total_deficit':sum(c['deficit']for c in cuts),'cells':cells}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path)
    parser.add_argument('--out',type=Path,default=Path(__file__).parent/'RESULT.json');a=parser.parse_args()
    repo=a.repo or next((p for p in Path(__file__).resolve().parents if(p/'AGENTS.md').exists()),None)
    if repo is None:raise ValueError('Use --repo to specify the source checkout')
    repo=repo.resolve();programme=repo/'research/moonshot-005-program'
    geom=programme/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=geom.read_bytes()
    assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='8eba43d142c819c206dce5df87ea4571aaead287'
    roots=json.loads(raw)['native_roots'];assert len(roots)==111
    src=programme/'results/bit-coupled-singular-delivery/worker-a/two-receiver-output'
    result={'status':'PASS_FOUR_FRAME_GROUND_BROADCAST_OBSTRUCTION','source_pins':{},'variants':{},
            'negative_controls':{},'new_complete_kappa':False,
            'scope':'Fixed handoff; independent direct-to-ground exports with arbitrary local recoding; no free cross-chart recoding or intermediate source acquisition.'}
    for variant in['COUPLED','UNCOPLED']:
        path=src/(variant+'-WORD.json');word=json.loads(path.read_text())
        result['source_pins'][str(path.relative_to(repo))]=hashlib.sha256(path.read_bytes()).hexdigest()
        full=examine(word,roots);assert full['total_deficit']==10
        assert [c['deficit']for c in full['frames']]==[3,3,2,2]
        assert [c['active_point_coordinates']for c in full['frames']]==EXPECTED_ACTIVE
        actual_only=examine(word,roots,donors=[]);assert actual_only['total_deficit']==12
        full['without_free_donors_total_deficit']=actual_only['total_deficit'];result['variants'][variant]=full
    for mutant in['cross_chart_point','unpaid_deep_payload']:
        try:examine(word,roots,mutant=mutant)
        except AssertionError as e:result['negative_controls'][mutant]={'rejected':True,'reason':str(e)}
        else:raise AssertionError('Invalid source passed '+mutant)
    bad=[list(F)for F in FRAMES];bad[0][0]=17
    try:examine(word,roots,frames=bad)
    except AssertionError:result['negative_controls']['already_completed_role']={'rejected':True}
    else:raise AssertionError('Invalid frame passed')
    assert 8*989**200<1000**200
    pricepath=src/'PRICE.json';price=json.loads(pricepath.read_text());room=Fraction(price['limiting_room']['upper'])
    assert room<Fraction(37,4)<Fraction(989,100)
    result['price']={'t':'199/200','all_rank_tariffs_lower_multiplier':'989/1000',
       'rank_sum_lower_bound_with_free_donors':10,'movement_lower_bound_with_free_donors':'989/100',
       'source_limiting_room_upper':str(room),'strict_deficit_lower':str(Fraction(989,100)-room),
       'exact_power_check':'8*989^200 < 1000^200','source_price_sha256':hashlib.sha256(pricepath.read_bytes()).hexdigest()}
    result['positive_controls']={'all_111_point_coordinates_span_identity':len(basis([1<<i for i in range(111)]))==111,
       'remove_fourth_cut_deficit':examine(word,roots,frames=FRAMES[:3])['total_deficit']}
    result['source_pins'][str(geom.relative_to(repo))]=hashlib.sha256(raw).hexdigest()
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'frame_deficits':[3,3,2,2],
       'rank_cost_lower_bound':10,'movement_cost_lower_bound':'9.89','limiting_allowance_upper':'9.25',
       'negative_controls':list(result['negative_controls'])}))
if __name__=='__main__':main()
