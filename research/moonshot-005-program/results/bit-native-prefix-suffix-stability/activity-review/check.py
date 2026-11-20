#!/usr/bin/env python3
"""Independent native route and integer-charge check of the path-loss inequality."""
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from itertools import product
from pathlib import Path
def verify(a):
    base=a.repo/'research/moonshot-005-program/results'
    def load(key,digest):
        v=gzip.decompress((base/key).read_bytes());assert hashlib.sha256(v).hexdigest()==digest;return v
    layout=json.loads(load('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'))
    data=load('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
    root=layout['root_table'][:111];H=layout['A2'];D=layout['D4'];dual=layout['dual_D4']
    inputs=[defaultdict(list) for _ in D];outputs=[defaultdict(list)for _ in D];records=set()
    for row in data.splitlines():
        r=json.loads(row);phase,owner,slot,h,d,k=r[:6]
        name=(phase,owner,slot);assert name not in records;records.add(name)
        if d is None:continue
        if h is not None:
            for j in H[h]:
                if j<111:inputs[d][j].append(name)
        if k is not None:
            for i in H[k]:
                if i<111:outputs[d][i].append(name)
    assert len(records)==106560
    physical=defaultdict(list);M=[]
    for d in range(len(D)):
        assert set(inputs[d])=={j for j in D[d]if j<111}
        assert set(outputs[d])=={i for i in D[dual[d]]if i<111}
        for names in list(inputs[d].values())+list(outputs[d].values()):assert len(names)==len(set(names))==8
        current=list(product(outputs[d],inputs[d]));M.append(current)
        for edge in current:physical[edge].append(d)
    dot=lambda u,v:sum(x*y for x,y in zip(u,v))
    keys={(i,j)for i in range(111)for j in range(111)if dot(root[i],root[j])==0}
    assert set(physical)==keys and all(len(v)==len(set(v))==60 for v in physical.values())
    incoming=Counter(i for i,j in keys);supp=[{n for n,v in enumerate(r)if v}for r in root]
    weights=json.loads(a.weights.read_bytes());table={tuple(k):v for k,v in weights['weights_by_port_type']};assert len(table)==len(weights['weights_by_port_type'])and all(int(z)==z and z>0 for z in table.values())
    def tag(i,j):return(incoming[i],incoming[j],len(supp[i]),len(supp[j]),len(supp[i]&supp[j]))
    classes=Counter(tag(*q)for q in keys);assert set(table)<=classes.keys()
    val={q:table.get(tag(*q),0)for q in keys};mass=sum(val.values());charges=[sum(val[e]for e in row)for row in M];low=min(charges)
    assert low==weights['minimum_coverage']==10000032 and mass==571622576 and len(classes)==169
    dead=12*mass//low;assert dead==685 and 60*64==3840 and (dead+1)*low>12*mass
    receipt={'native_donor_receiver_pairs':len(keys),'physical_D_count':len(D),'actual_D_interfaces':sum(map(len,M)),
       'actual_per_pair_D_count':60,'unique_early_late_owner_records_per_side_per_section':8,'native_copies':8,'per_section_field_capacity':64,
       'rank_allowance_at_h128':6*128,'rank_allowance_at_h134':6*134,'max_fully_dead_sections_per_contact':12,'pair_types':len(classes),
       'positive_pair_types':len(table),'total_pair_weight':mass,'minimum_D_weight':low,'minimum_D_weight_at':charges.index(low),
       'charge_numerator':12*mass,'maximum_completely_dead_D':dead,'minimum_active_D':len(D)-dead,
       'one_more_dead_fails_numerator':(dead+1)*low,'weight_input_SHA256':hashlib.sha256(a.weights.read_bytes()).hexdigest()}
    exception={(7,80),(10,81),(80,96),(81,95)};exception|={(j,i)for i,j in exception};assert len(exception)==8 and exception<=keys
    exc=sum(val[q]for q in exception);new=2*mass+4*exc
    receipt.update(clebsch_exception_weights={str(q):val[q]for q in sorted(exception)},clebsch_total_exception_weight=exc,clebsch_max_dead_regular=2,clebsch_max_dead_exception=6,clebsch_weighted_numerator=new,clebsch_max_dead_all_D=new//low,clebsch_minimum_active_D=len(D)-new//low)
    a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ('repo','weights','out'):p.add_argument('--'+k,type=Path,required=True)
 verify(p.parse_args())
