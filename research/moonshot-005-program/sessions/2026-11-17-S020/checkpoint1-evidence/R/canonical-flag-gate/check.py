"""Exact flag-rank obstruction for any number of immutable canonical packets."""
import argparse, copy, hashlib, importlib.util, json
from pathlib import Path
from fractions import Fraction as Q

def need(ok,msg):
    if not ok:raise ValueError(msg)
def basis(rows):
    b={}
    for z in rows:
        while z:
            p=z.bit_length()-1
            if p in b:z^=b[p]
            else:b[p]=z;break
    return b
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    w=json.loads(a.word.read_text());native=a.repo/w['source_path']
    need(hashlib.sha256(native.read_bytes()).hexdigest()==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native pin')
    need(hashlib.sha256(a.word.read_bytes()).hexdigest()=='74fb050a6afb8d8e1b6895b0f092220f8e6852365a7516ef4db2284c43c1a5ee','actual source pin')
    roots=json.loads(native.read_text())['native_roots'];known=set(w['targets']);U=sorted(set(range(111))-known);um=sum(1<<i for i in U)
    need(len(U)==54 and len(known)==57,'source partition')
    neighbours={i:sum(1<<j for j in U if sum(x*y for x,y in zip(roots[i],roots[j]))==0) for i in U}
    rows={i:(1<<i)^neighbours[i] for i in U};base=basis(rows.values());need(len(base)==9,'canonical dimension9')
    local_ranks={i:len(basis(z&(um^neighbours[i]) for z in base.values())) for i in U}
    need(set(local_ranks.values())=={9},'canonical/local intersections all zero')
    order=[7,6,5,4,3,2,0,1];position={j:k for k,j in enumerate(order)}
    need(sorted(order)==list(range(8)),'full real coordinate flag')
    strata=[]
    for k,j in enumerate(order):
        ids=[i for i in U if max(position[c] for c,x in enumerate(roots[i]) if x)==k]
        b=basis(rows[i] for i in ids)
        strata.append({'level':k+1,'added_coordinate':j,'roles':ids,'canonical_row_rank':len(b),'binary_basis_hex':[hex(x) for x in b.values()]})
    ranks=[s['canonical_row_rank'] for s in strata if s['roles']]
    need(ranks==[1,4,6,7,8] and sum(ranks)==26,'exact flag demand')
    selected=[]
    for s in strata:
        if s['roles']:selected.append(s['roles'][0])
    # Real independence follows from leading coordinates; verify triangular
    # witnesses directly without importing the author's geometry routines.
    for a0,i in enumerate(selected):
        level=max(position[c] for c,x in enumerate(roots[i]) if x)
        need(roots[i][order[level]]!=0 and all(roots[h][order[level]]==0 for h in selected[:a0]),'triangular real flag witness')
    mod=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint3-evidence/C/portable/audit_cp6.py'
    spec=importlib.util.spec_from_file_location('integer_root_price',mod);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    packet=tuple(Q(26,5)*x for x in m.power_interval(5))
    source=m.moment({1:165,6:108,7:114});gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    allowance=tuple(x/6 for x in m.moment(gate));excess=(source[0]+packet[0]-allowance[1],source[1]+packet[1]-allowance[0]);need(excess[0]>0,'strict target obstruction')
    # Granting an own coordinate changes the uniqueness premise.
    i=5;new_local=neighbours[i]|(1<<i);new_rank=len(basis(z&(um^new_local) for z in base.values()));need(new_rank==8,'own-input grant control')
    one_stratum_rank=len(base);need(one_stratum_rank==9,'collapsed flag gives only9, not26')
    out={'status':'PASS_ANY_IMMUTABLE_CANONICAL_BANK_FLAG_GATE','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'native_sha256':w['source_sha256'],'coordinate_flag':order,'strata':strata,'nonempty_strata':5,'rank_sum':26,'canonical_dimension':9,'all54_local_projection_ranks':local_ranks,'packet_cost_lower_bound':m.interval_json(packet),'source_movement':m.interval_json(source),'necessary_allowance':m.interval_json(allowance),'excess':m.interval_json(excess),'controls':{'grant_x5_canonical_local_intersection_dimension':9-new_rank,'collapsed_single_stratum_bound':one_stratum_rank},'scope':'Any finite number of fixed Hub-born whole-record payloads in the pinned canonical code, arbitrary characteristic-two fields/block width, only ascending/stationary relays after each read, no extra inward branch. Mutable/noncanonical/earlier-source packets outside. No new kappa.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status']);print('packet floor',out['packet_cost_lower_bound']['decimal']);print('excess',out['excess']['decimal'])
if __name__=='__main__':main()
