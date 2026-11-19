#!/usr/bin/env python3
"""Fresh zero-slice census, using a distinct inherited color-search algorithm."""
import argparse
from fractions import Fraction
import gzip
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

def rank(rows):
    piv={}
    for row in rows:
        while row:
            bit=row & -row
            if bit not in piv: piv[bit]=row; break
            row ^= piv[bit]
    return len(piv)

def packing(edges,k):
    for chosen in itertools.combinations(edges,k):
        if all(not(a&b) for a,b in itertools.combinations(chosen,2)):return True
    return False

def coloring(edges,n,k,colors):
    if len(colors)!=n or set(colors)!=set(range(k)):return False
    classes=[sum(1 << v for v in range(n) if colors[v]==c) for c in range(k)]
    return all(any((e>>v)&1 and e&classes[colors[v]]==e for e in edges) for v in range(n))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    pg=a.repo/'research/moonshot-005-program'; resultbase=pg/'results'
    lp=resultbase/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    fp=resultbase/'bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json'
    cp=resultbase/'bit-stripe-varying-port-cut/review/output/RESULT.json.gz'
    alternate=resultbase/'bit-stripe-varying-port-cut/author/check.py'
    layout=json.loads(gzip.decompress(lp.read_bytes()));factor=dict(json.loads(fp.read_text())['factors'])
    old={v['plane']:v for v in json.loads(gzip.decompress(cp.read_bytes()))['records']}
    submitted=json.loads(gzip.decompress((a.author/'output/RESULT.json.gz').read_bytes()))
    spec=importlib.util.spec_from_file_location('distinct_historical_search',alternate)
    solver=importlib.util.module_from_spec(spec);spec.loader.exec_module(solver)
    roots=layout['root_table']; native=(1 << 111)-1
    O=[sum(1 << j for j,y in enumerate(roots) if sum(u*v for u,v in zip(x,y))==0) for x in roots[:111]]
    K=[(O[i]&native) ^ (1 << i) for i in range(111)];assert rank(K)==9
    H=[sum(1 << v for v in row) for row in layout['A2']]
    D=[sum(1 << v for v in row) for row in layout['D4']]
    visible=[[i for i in range(111) if h&O[i]==h] for h in H]
    dvisible=[{i for i in range(111) if d&O[i]==d} for d in D]
    donors=[[v for v in range(111) if (h>>v)&1] for h in H]
    capacity=[[0]*111 for _ in range(111)]; early=[0]*111
    for hi,js in enumerate(donors):
        if not js:continue
        x=12//len(js)+factor.get(hi,0)
        for j in js:early[j]+=45*x
        for i in visible[hi]:
            for j in js:capacity[i][j]+=45*max(8,x)
    assert set(early)=={5760}
    tight=[{j for j in range(111) if capacity[i][j]==5760} for i in range(111)]
    assert sum(map(len,tight))==6110
    prepared={}
    for hi,js in enumerate(donors):
        if len(js)<2:continue
        targets=[i for i in visible[hi] if set(js)<=tight[i]]
        exits=[d for d,mask in enumerate(D) if mask&H[hi]==H[hi]]
        assert len(exits)==45 and targets==old[hi]['joint_tight_receivers']
        edges=[sum(1 << p for p,i in enumerate(targets) if i in dvisible[d]) for d in exits]
        assert sorted(set(edges)-{0})==old[hi]['port_neighborhoods']
        prepared[hi]=(targets,exits,12//len(js)+factor.get(hi,0))
    cache={};distinct_calls=0;alternate_nodes=0;sat_witnesses=0;packing_exclusions=0
    census=[];increased=0
    for zero in range(111):
        assert rank([row & (native ^ (1 << zero)) for row in K])==9
        for i in range(111):
            if i!=zero:assert rank([row & native & ~O[i] & ~(1 << zero) for row in K])==9
        reported=submitted['donors'][zero]
        assert reported['zeroed_donor']==zero
        changed={v['H']:v for v in reported['changed_color_instances']}
        binary=Fraction(0);general=Fraction(0);min_margin=10**9;decisions=0
        for hi,js in enumerate(donors):
            m=len(js)
            if zero in js:
                grant=2*(m-1) if m>=2 else 0
                binary+=grant;general+=grant;continue
            if m<2:
                if m==1:binary+=3;general+=3
                continue
            targets,exits,x=prepared[hi];retained=[i for i in targets if i!=zero]
            masks=[sum(1 << p for p,i in enumerate(retained) if i in dvisible[d]) for d in exits]
            uncovered=masks.count(0);edges=tuple(sorted(set(masks)-{0}));n=len(retained)
            if zero not in targets:
                alpha=old[hi]['rank_cap'];assert hi not in changed
            else:
                decisions+=1;entry=changed[hi];alpha=entry['alpha'];assert entry['uncovered']==uncovered
                for k,label in [(2,'k2'),(3,'k3')]:
                    decision=entry[label]
                    if decision is None:continue
                    key=(n,k,edges)
                    if decision['sat']:
                        assert coloring(edges,n,k,decision['colors']);sat_witnesses+=1
                        assert not coloring(edges,n,k,[0]*n)
                    elif not packing(edges,k):packing_exclusions+=1
                    elif key not in cache:
                        check=solver.solve(edges,n,k);assert check['status']=='UNSAT'
                        cache[key]=False;distinct_calls+=1;alternate_nodes+=check['nodes']
                expected=1 if not entry['k2']['sat'] else 2 if m==2 or not entry['k3']['sat'] else 3
                assert alpha==expected
                increased+=alpha>old[hi]['rank_cap']
            margin=45*(m-1)*x-uncovered*m*x-180
            assert margin>0;min_margin=min(min_margin,margin)
            binary+=alpha+1+Fraction(2*uncovered,15)
            general+=(alpha+1 if alpha<m else 2*m)+Fraction(2*uncovered,15)
        assert decisions==len(changed)
        assert binary==Fraction(reported['binary_capacity']) and general==Fraction(reported['general_field_capacity'])
        assert min_margin==reported['minimum_top_gate_margin']
        assert binary<3232 and general<3232
        census.append({'donor':zero,'binary':str(binary),'general':str(general),'margin':min_margin})
        if zero%10==0:print(json.dumps({'reviewed_donors':zero+1,'distinct_second_solver_calls':distinct_calls,'nodes':alternate_nodes}),flush=True)
    assert max(Fraction(v['general']) for v in census)==Fraction(14089,5)
    assert max(Fraction(v['binary']) for v in census)==Fraction(13844,5)
    assert min(v['margin'] for v in census)==24 and increased==84
    assert rank(K+[1,2])==11 # arbitrary mixed donor helpers need not vanish on the chosen zero slice
    pins=[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [lp,fp,cp,alternate,a.author/'PROOF.md',a.author/'check.py',a.author/'output/RESULT.json.gz']]
    out={'status':'PASS_INDEPENDENT_RAW_HELPER_REVIEW','canonical_restrictions':12210,'donors':census,
         'minimum_general_deficit_r180':74556,'minimum_binary_deficit_r180':83376,'minimum_early_margin':24,
         'increased_caps':increased,'independently_validated_SAT_witnesses':sat_witnesses,
         'packing_exclusions':packing_exclusions,'distinct_alternate_solver_calls':distinct_calls,
         'alternate_solver_nodes':alternate_nodes,'new_author_code_imported':False,
         'different_historical_solver_reused':True,'source_pins':pins,'arbitrary_mixed_helpers_excluded':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status'],flush=True)
if __name__=='__main__':main()
