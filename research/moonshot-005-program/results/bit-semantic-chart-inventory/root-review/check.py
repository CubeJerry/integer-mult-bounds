#!/usr/bin/env python3
"""Recompute actual inventories using geometric charts, not their labels."""
from pathlib import Path
import argparse,hashlib,json
from review_leaf_capacity import chart_basis,binary_basis
from optimize_word import independent_replay

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();P=a.repo/'research/moonshot-005-program'
    paths=['results/bit-canonical-mask-source/author/early-paid46/WORD.json','results/bit-canonical-mask-source/author/masked-M1/WORD.json','results/bit-canonical-common-delivery/author/canonical-common-one/WORD.json','results/bit-canonical-common-delivery/author/canonical-common-two/WORD.json','results/bit-canonical-decoder34/author/WORD.json']
    reports=[]
    for path in paths:
        raw=(P/path).read_bytes();w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots'];replay=independent_replay(w)
        C={n:tuple(tuple(row)for row in chart_basis(rec))for n,rec in w['charts'].items()};assert C['M1']==C['C2'];aliases=sorted(n for n,c in C.items()if c==C['M1']);zeros=sorted(n for n,c in C.items()if not c)
        v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
        for step,(op,n,*q)in enumerate(w['operations']):
            if op=='CLEAR':break
            if op=='INIT':v[n],at[n]=0,q[0]
            elif op=='ADD':v[q[0]]^=v[n]
            elif op=='MOVE':at[n]=q[0]
        actual={n:z for n,z in v.items()if C[at[n]]==C['M1']};label={n:z for n,z in v.items()if at[n]=='M1'};code=binary_basis((1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(roots[i],roots[j]))==0)for i in range(111));assert len(code)==9
        rank=len(binary_basis(actual.values()));lr=len(binary_basis(label.values()));intersection=rank+9-len(binary_basis(list(actual.values())+code))
        assert rank==13 and lr==8 and intersection==(0 if path==paths[0]else 3)
        reports.append({'word_path':path,'word_sha256':hashlib.sha256(raw).hexdigest(),'actual_cut_before_first_CLEAR':step,'geometric_M1_aliases':aliases,'geometric_zero_aliases':zeros,'label_only_M1_rank':lr,'actual_geometric_M1_rank':rank,'actual_C9_intersection_rank':intersection,'actual_inventory':[{'field':n,'label':at[n],'row_hex':hex(z)}for n,z in sorted(actual.items())],'records_missed_by_label_filter':sorted(set(actual)-set(label)),'replay':replay})
    result={'status':'PASS_ROOT_INDEPENDENT_SEMANTIC_CHART_INVENTORY_CORRECTION','method':'Independent Fraction row-reduced chart equality and binary elimination at actual final-live cuts; no author inventory code imported.','supersedes':'Checkpoint5 supplementary final-live M1 rank8→8; the correct ranks are13→13 because C2=M1.','unchanged_claims':['All five literal words and their222-column endpoints, ownership and movements','Canonical intersection0→3','Actual shared custody and read chronology','Movement prices and physical decoder34'],'reports':reports,'negative_control':'The literal label-only filter reproduces the incorrect rank8 and omits the listed actual C2 records. It is explicitly rejected as an inventory definition.','new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'actual_ranks':[r['actual_geometric_M1_rank']for r in reports],'canonical_intersections':[r['actual_C9_intersection_rank']for r in reports]}))
if __name__=='__main__':main()
