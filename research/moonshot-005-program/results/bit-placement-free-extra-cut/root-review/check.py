#!/usr/bin/env python3
"""Root-independent finite hypotheses of the placement-free Extra6 cut."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
from review_leaf_capacity import binary_basis,chart_basis,dot,echelon


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--word',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    raw=args.word.read_bytes();w=json.loads(raw)
    src=(args.repo/w['source_path']).read_bytes()
    assert hashlib.sha256(src).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=json.loads(src)['native_roots']
    charts={name:chart_basis(rec) for name,rec in w['charts'].items()}
    values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
    locations={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)}
    history=[(n,locations[n],v) for n,v in values.items()]
    for op,n,*q in w['operations']:
        if op=='INIT':values[n],locations[n]=0,q[0]
        elif op=='ADD':values[q[0]]^=values[n];n=q[0]
        elif op=='MOVE':locations[n]=q[0]
        elif op=='CLEAR':del values[n],locations[n];continue
        else:raise ValueError(op)
        history.append((n,locations[n],values[n]))
    for i in range(111):
        assert values[f'X{i}']==1<<i
        assert values[f'Y{i}']==(1<<(111+i))^((1<<i) if i in w['targets'] else 0)
    J=[8,9,36,37];mask=sum(1<<i for i in J)
    assert set(J).isdisjoint(w['targets'])
    gram=[[dot(roots[i],roots[j]) for j in J] for i in J]
    assert all(x for row in gram for x in row)
    visible={}
    for i in J:
        records=[(n,c,v) for n,c,v in history if all(dot(roots[i],b)==0 for b in charts[c])]
        assert all(v&mask==0 for _,_,v in records)
        visible[str(i)]=len(records)
    donor=w['higher_source_delivery']
    donor_value=int(donor['first_retention_hex'],16)
    actual=[v for n,c,v in history if n==donor['first_retention'] and c==donor['first_chart'] and v]
    assert set(actual)=={donor_value}
    actual_donor=donor_value&mask
    assert actual_donor==sum(1<<j for j in (8,9,37))
    extra=set(w['history_extra_query_roles'])
    assert set(J)<=extra
    other_rows=[(1<<j)&mask for j in range(111) if j not in extra]+[actual_donor]
    assert len(binary_basis(other_rows))==1
    kernels=[(1<<8)^(1<<37),(1<<9)^(1<<37),1<<36]
    assert len(binary_basis(kernels))==3
    assert all((r&actual_donor).bit_count()%2==0 for r in kernels)
    assert len(binary_basis(other_rows+[1<<8,1<<36,1<<9]))==4
    assert len(binary_basis(other_rows+[1<<8,1<<9]))==3
    assert len(binary_basis(other_rows+[1<<36,1<<9]))==3
    pred=['J16','J23','J22','M1','M1','M1','Extra6','D3_21']
    domains=[]
    for name in pred:
        b=charts[name]
        domains.append([i for i in range(111) if len(echelon(b+[roots[i]])[0])==len(b)])
    counts={str(k):sum(math.prod(len(domains[j])-1 for j in js) for js in itertools.combinations(range(8),k)) for k in range(4)}
    assert counts=={'0':1,'1':137,'2':7812,'3':241054}
    assert len(charts['Extra6'])==6 and len(charts['M1'])==5
    assert len(echelon(charts['Extra6']+charts['M1'])[0])==6
    result={
      'status':'PASS_ROOT_INDEPENDENT_PLACEMENT_FREE_EXTRA6_CUT',
      'word_sha256':hashlib.sha256(raw).hexdigest(),'native_source_sha256':w['source_sha256'],
      'completed_endpoint_count':len(w['targets']),'all222_final_coefficients':True,
      'historical_states':len(history),'J':J,'gram':gram,
      'visible_history_counts':visible,'visible_history_projection_rank':0,
      'actual_donor_owner':donor['first_retention'],'actual_donor_projection_hex':hex(actual_donor),
      'all_nonExtra6_raw_coordinates_and_donor_globally_granted_rank':1,
      'kernel_basis_hex':[hex(r) for r in kernels],
      'P6_transcript_floor':'3V','additional_outside_P6_dimension_if_one_record':'2V',
      'candidate_leaf_domain_sizes':[len(d) for d in domains],
      'at_most_three_reassignments':sum(counts.values()),
      'two_import_global_span_repair_rank':4,'one_import_global_span_repair_rank':3,
      'Extra6_to_M1_owned_rank_drop':1,
      'scope':'Finite source hypotheses for a separate information proof. Other-bank grant is all raw coordinates outside Extra6 plus the fixed donor; changing the J projection of higher/common data or outside source banks can escape. No location restriction is used. No complete supplier or new kappa.'
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],len(w['targets']),len(history))


if __name__=='__main__':main()
