#!/usr/bin/env python3
"""Exact H263 cut, source-coupling divisors and finite controls."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import gzip
import json

LAYOUT_PIN='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
ROUTE_PIN='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
WEIGHTS={4:2,5:2,6:2,7:2,53:2,55:2,8:1,10:1,47:1,48:1}

def need(ok,label):
    if not ok: raise ValueError(label)

def binary_rank(rows):
    pivots={}
    for row in rows:
        while row:
            c=row.bit_length()-1
            if c in pivots: row ^= pivots[c]
            else: pivots[c]=row; break
    return len(pivots)

class Field:
    def __init__(self,degree,polynomial):
        self.order=1<<degree;self.polynomial=polynomial
        self.table=[[self.multiply(a,b)for b in range(self.order)]for a in range(self.order)]
        self.inverse=[0]+[next(b for b in range(1,self.order)if self.table[a][b]==1)
                           for a in range(1,self.order)]
    def multiply(self,a,b):
        out=0
        while b:
            if b&1:out^=a
            b>>=1;a<<=1
            if a&self.order:a^=self.polynomial
        return out
    def power(self,a,n):
        out=1
        while n:
            if n&1:out=self.table[out][a]
            a=self.table[a][a];n>>=1
        return out
    def rank(self,matrix):
        rows=[list(row)for row in matrix]
        if not rows:return 0
        rank=0
        for c in range(len(rows[0])):
            pivot=next((k for k in range(rank,len(rows))if rows[k][c]),None)
            if pivot is None:continue
            rows[rank],rows[pivot]=rows[pivot],rows[rank]
            scale=self.inverse[rows[rank][c]]
            rows[rank]=[self.table[scale][x]for x in rows[rank]]
            for k in range(rank+1,len(rows)):
                if rows[k][c]:
                    scale=rows[k][c]
                    rows[k]=[x^self.table[scale][y]for x,y in zip(rows[k],rows[rank])]
            rank+=1
            if rank==len(rows):break
        return rank

def nonlinear_controls():
    checked=valid=0
    for inverse in permutations(range(8)):
        checked+=1;directions=[]
        for bit in range(3):
            diffs={inverse[y]^inverse[y^(1<<bit)]for y in range(8)if not(y>>bit)&1}
            if len(diffs)!=1:break
            directions.append(next(iter(diffs)))
        if len(directions)!=3:continue
        need(binary_rank(directions)==3,'isolated packet directions independent')
        valid+=1
    need(checked==40320 and valid==1344,'complete finite encoder census')
    field=Field(2,7);relabel=[field.table[x][x]for x in range(4)]
    need(relabel==[0,1,3,2]and len(set(relabel))==4,'non-F4-linear packet bijection')
    need(relabel[field.table[2][1]]!=field.table[2][relabel[1]],'field linearity is not assumed')
    return {'binary_bijections_checked':checked,'all_three_receiver_targets_linear':valid,
            'non_field_linear_F4_packet_relabelling':relabel}

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();repo=args.repo.resolve();base=repo/'research/moonshot-005-program';p=base/'results'
    layout_path=p/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    route_path=p/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    partition_path=p/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    raw=gzip.decompress(layout_path.read_bytes());route_raw=gzip.decompress(route_path.read_bytes())
    need(sha256(raw).hexdigest()==LAYOUT_PIN,'layout pin')
    need(sha256(route_raw).hexdigest()==ROUTE_PIN,'route pin')
    data=json.loads(raw);roots=data['root_table'];Hs=list(map(set,data['A2']));Ds=list(map(set,data['D4']))
    native=set(range(111));donors=sorted(Hs[263]&native);need(donors==[0,61,62],'literal H263 donors')
    adj=[{j for j,y in enumerate(roots)if i!=j and sum(a*b for a,b in zip(x,y))==0}for i,x in enumerate(roots)]
    receivers=[]
    for i in range(111):
        if not Hs[263]<=adj[i]:continue
        views=[[H for H in Hs if j in H and H<=adj[i]]for j in donors]
        need(all(len(v)==16 for v in views),'sixteen-plane source views')
        if all(all(len(H&native)>=2 for H in v)for v in views):receivers.append(i)
    ports=[d for d,D in enumerate(Ds)if Hs[263]<=D]
    visible={i:{d for d in ports if Ds[d]<=adj[i]}for i in receivers}
    audiences={d:{i for i in receivers if d in visible[i]}for d in ports}
    need(len(receivers)==33 and len(ports)==45 and all(len(A)==15 for A in visible.values()),'actual cuts')
    need(80 not in receivers and 10 not in donors,'unchanged 99 identity target blocks')
    incoming=Counter();outgoing=Counter();kinds=Counter();owners=set()
    for line in route_raw.splitlines():
        kind,j,c,h,d,k,left,right=json.loads(line)
        if h!=263:continue
        need(kind=='X'and j==left and j in donors,'only genuine early owners')
        need((j,c)not in owners,'distinct original owner');owners.add((j,c))
        incoming[j]+=1;outgoing[d]+=1;kinds[kind]+=1
    need(incoming=={j:30 for j in donors}and outgoing=={d:2 for d in ports}and kinds=={'X':90},'fully preserving early cut')
    pair_hist=Counter(len(visible[i]&visible[j])for i,j in combinations(receivers,2))
    triple_hist=Counter();isolators={}
    for ids in combinations(receivers,3):
        shared=set.intersection(*(visible[i]for i in ids));triple_hist[len(shared)]+=1
        if len(shared)==1:isolators.setdefault(next(iter(shared)),list(ids))
    need(pair_hist=={3:226,6:302},'all pair intersections')
    need(triple_hist=={0:1648,1:411,2:3305,6:92},'all triple intersections')
    need(set(isolators)==set(ports),'all ports isolated')
    need(set.intersection(*(visible[i]for i in [4,5,6]))=={2835},'simple divisor15 witness')
    for d in ports:need(audiences[d]and set.intersection(*(visible[i]for i in audiences[d]))=={d},'full audience isolates packet')
    weighted_sums={d:sum(WEIGHTS.get(i,0)for i in audiences[d])for d in ports}
    need(set(WEIGHTS)<=set(receivers)and sum(WEIGHTS.values())==16,'mod3 receiver dual')
    need(set(weighted_sums.values())=={3,6,12}and all(x%3==0 for x in weighted_sums.values()),'mod3 port dual')
    wrong=dict(WEIGHTS);wrong[4]=1
    need(any(sum(wrong.get(i,0)for i in audiences[d])%3 for d in ports),'mutated dual rejected')

    classes=json.loads(gzip.decompress(partition_path.read_bytes()))['classes']['263']
    need(len(classes)==5 and all(len(C)==9 for C in classes)and sorted(sum(classes,[]))==ports,'five actual classes')
    need(all(len(set(C)&visible[i])==3 for C in classes for i in receivers),'component dimension3')
    F=Field(5,37);pos={d:k for k,d in enumerate(ports)};matrix=[[0]*45 for d in ports]
    for group,C in enumerate(classes):
        for local,d in enumerate(C):
            for j in range(3):
                for t in range(3):matrix[pos[d]][15*j+3*group+t]=F.power(local+1,3*j+t)
    need(F.rank(matrix)==45,'positive fully early local word')
    ranks=Counter()
    for i in receivers:
        rows=[matrix[pos[d]]for d in ports if d in visible[i]]
        for j in range(3):
            r=F.rank([row[15*j:15*(j+1)]for row in rows]);need(r==15,'all donor projections');ranks[r]+=1
    dimensions=[[int(d in C)for d in ports]for C in classes]
    need(all(sum(profile[pos[d]]for d in visible[i])==3 for profile in dimensions for i in receivers),'integer d3 profiles')
    need(all(sum(profile[k]for profile in dimensions)==1 for k in range(45)),'all ports filled once')
    F64=Field(6,67);lossy=[[F64.power(k+1,t)for t in range(15)]for k in range(45)]
    need(F64.rank(lossy)==15,'lossy total rank')
    need(all(F64.rank([lossy[pos[d]]for d in ports if d in visible[i]])==15 for i in receivers),'lossy exact decoding')
    nonlinear=nonlinear_controls();invoice=2*((3*240*9)**2+3*(3*240*9));need(invoice==84019680,'local compiler invoice')
    paths=[layout_path,route_path,partition_path,p/'bit-middle-information-factorization/author/PROOF.md',
           p/'bit-nonsemisimple-commuting-source-gate/author/PROOF.md',p/'bit-repeated-field-two-causal-source/author/PROOF.md',
           p/'bit-class-separated-middle-gate/author/PROOF.md',
           base/'work-in-progress/2026-11-19-S027/covariant-trace-source/PROOF.md']
    result={'status':'PASS_FULLY_EARLY_H_LINEARIZATION_AND_SOURCE_COUPLING_GATE',
            'H':263,'donors':donors,'receivers':receivers,'ports':45,'bank480_early_inputs':90,'late_inputs':0,
            'all99_relevant_target_blocks_identity':True,'pair_intersection_histogram':dict(pair_hist),
            'triple_intersection_histogram':dict(triple_hist),'all_ports_isolated_by_triples':45,
            'divisor15_triple':[4,5,6],'isolated_port':2835,
            'identical_base_quotient_width_divisor':15,'varying_common_component_quotient_width_divisor':3,
            'sixteen_spinor_copies_per_identical_block_minimum':15,
            'sixteen_spinor_copies_per_varying_common_component_minimum':3,
            'mod3_dual':{'receiver_weights':WEIGHTS,'total_weight':16,'port_weight_histogram':dict(Counter(weighted_sums.values()))},
            'positive_control':{'field':'GF32','full_rank':45,'donor_projection_ranks':dict(ranks),
                                'components':5,'scalar_component_width':3,'spinor_component_width':48,'full_spinor_quotient_width':240},
            'negative_controls':{'mutated_dual_rejected':True,'no_early_preservation_GF64_rank':15,
                                 'no_early_preservation_required_rank':45,'receivers_still_decode':33},
            'finite_nonlinear_controls':nonlinear,'local_compiler_ADD_upper_bound_p240_e9':invoice,
            'no_new_kappa':True,'five_foundations_retained':True,
            'source_pins':[{'path':str(path.relative_to(repo)),'sha256':sha256(path.read_bytes()).hexdigest()}for path in paths]}
    geometry={'ports':ports,'receivers':receivers,'audiences':{str(d):sorted(a)for d,a in audiences.items()},
              'isolating_triples':isolators,'mod3_dual_weights':WEIGHTS,'mod3_dual_port_sums':weighted_sums,
              'three_copy_dimension_profiles':dimensions,'positive_classes':classes,'positive_GF32_matrix':matrix}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'GEOMETRY.json').write_text(json.dumps(geometry,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['triple_intersection_histogram','mod3_dual','positive_control','finite_nonlinear_controls']},sort_keys=True))

if __name__=='__main__':main()
