#!/usr/bin/env python3
"""Independent exact source premises for the last shared chart obstruction.

The universal chronological/nonlinear argument is in REVIEW.md. No root or
construction-author verifier is imported; C's own exact native replay is used.
"""
import argparse,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path

def bits(z):return sum(1<<i for i in z)
def solve(equations):
    basis={}
    for z,b in equations:
        while z:
            p=z.bit_length()-1
            if p in basis:z^=basis[p][0];b^=basis[p][1]
            else:basis[p]=(z,b);break
        if not z and b:raise ValueError('inconsistent requested collision')
    v=0
    for p,(z,b)in sorted(basis.items()):
        if ((z&v).bit_count()&1)^b:v|=1<<p
    if not all(((z&v).bit_count()&1)==b for z,b in equations):raise ValueError('collision solver failed')
    return v

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--audit-module',type=Path,default=Path(__file__).resolve().parents[1]/'portable'/'audit_cp6.py');a=ap.parse_args()
    sp=importlib.util.spec_from_file_location('own_native',a.audit_module);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);need=m.insist
    w=json.loads(a.word.read_text());need(m.sha(a.word)=='f5acfcb454d6d50dfdb7d66acd2c33980e4aed17826afafbb67fbeb2168f58c1','literal source word')
    source=a.repo/w['source_path'];need(m.sha(source)=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','literal native roots');s=json.loads(source.read_text());R=s['native_roots'];cut=w['carrier_interface_before_operation'];stats,snap,C,events=m.replay(w,s,[cut]);v,l=snap[cut];T=set(w['targets']);U=sorted(set(range(111))-T)
    need(len(U)==105,'unfinished count')
    orig={f'X{i}'for i in range(111)}|{f'Y{i}'for i in range(111)};proper=[n for n in v if n not in orig and 1<len(C[l[n]])<8];need(len(proper)==20,'complete proper-owner census')
    for i in U:
        need(v[f'Y{i}']=={111+i}and C[l[f'Y{i}']]==C['zero'],'raw unfinished receiver starts ground')
        need(all(not m.subset(C[l[n]],C[f'F{i}'])for n in proper),'initial proper owners inaccessible')
        need(all(not m.subset(C[f'F{h}'],C[f'F{i}'])for h in T),'completed receiver fields inaccessible')
    for j in range(111):need(v[f'X{j}']=={j}and C[l[f'X{j}']]==C['Hub'],'raw X already Hub');need(v[f'NATIVE_RAW_{j}']=={j}and C[l[f'NATIVE_RAW_{j}']]==C[f'L{j}'],'actual native cache')
    code=[set(v[f'CANONICAL_{b}'])for b in range(9)];need(all(C[l[f'CANONICAL_{b}']]==C['zero']for b in range(9)),'actual ground code');need(len(m.binary_basis(code))==9,'code rank')
    N={i:{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)}
    words=[]
    for mask in range(512):
        z=set()
        for b in range(9):
            if mask>>b&1:z^=code[b]
        words.append(z)
    gap={}
    for i in U:
        ki=N[i]|{i};need(ki in words,'canonical fitting row actual');need(not any(z and z<=N[i]for z in words),'canonical completion unique')
        gap[i]=min(len(z-N[i])for z in words if z and z!=ki);need(gap[i]>=18,'all-origin-set rank stability to seventeen grants')
    diffs={(i,h):len(N[i]-N[h])for i in U for h in U if i!=h};need(len(diffs)==10920 and min(diffs.values())==21,'all ordered unfinished-pair differences')
    witness_pair=min(diffs,key=lambda z:(diffs[z],z));i,h=witness_pair;D=sorted(N[i]-N[h]);grants=set(D[:17]);extra=D[17];missing=D[18];visible=(N[i]&N[h])|grants|{extra};need(i not in grants and missing not in visible,'worst-cardinality local omission')
    eq=[(bits(z),0)for z in code]+[(1<<j,0)for j in sorted((N[i]-{missing})|grants)]+[(1<<i,1)]
    collision=solve(eq);need((collision>>missing)&1 and not any((collision>>j)&1 for j in visible),'explicit nonlinear indistinguishability pair')
    need(not m.in_span({i},m.binary_basis(code+[{j}for j in visible])),'last-shared-chart observation cannot decode')
    need(m.in_span({i},m.binary_basis(code+[{j}for j in N[i]])),'full native grant positive control')
    # Giving all missing contact values at ground is outside the <=17 premise
    # and destroys the last-co-visit information obstruction.
    need(m.in_span({i},m.binary_basis(code+[{j}for j in (N[i]&N[h])|set(D)])),'large changed global grant positive control')
    q=m.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    allowance=tuple(z/6 for z in m.moment(gate));excess=(q[0]+18-allowance[1],q[1]+18-allowance[0]);need(excess[0]>0,'eighteen native ports exceed necessary allowance')
    result={'status':'PASS_INDEPENDENT_LAST_SHARED_CHART_NATIVE_ONLY_OBSTRUCTION','word_sha256':m.sha(a.word),'source_sha256':w['source_sha256'],'source_cut':cut,'unfinished_receivers':U,'initial_inaccessible_proper_fields':proper,'canonical_alternative_support_gap':gap,'ordered_unfinished_receiver_pairs':len(diffs),'neighborhood_difference_histogram':dict(sorted(Counter(diffs.values()).items())),'minimum_neighborhood_difference':21,'per_receiver_minimum_difference':[{'receiver':i,'other_receiver':min((h for h in U if h!=i),key=lambda h:(diffs[(i,h)],h)),'minimum_difference':min(diffs[(i,h)]for h in U if h!=i)}for i in U],'explicit_maximal_grant_collision':{'receiver':i,'last_co_visit_other_receiver':h,'seventeen_globally_granted_native_inputs':sorted(grants),'one_extra_native_suffix_input':extra,'missing_indispensable_input':missing,'difference_support':[j for j in range(111)if collision>>j&1],'all_ground_code_and_every_other_orthogonal_input_unchanged':True},'theorem':{'maximum_global_native_grants_excluded':17,'necessary_distinct_native_descent_origins_for_completion':18,'scope':'Every future owned MOVE starts at a native line and ends at ground; arbitrary local nonlinear computation, original Y feedback, Y-bearing stationary owners, and fixed schedules. Exact source cut retained.','last_shared_chart_definition':'The last chart on Y_i own ascending route that any different unfinished Y visits at any time, even at disjoint times.'},'movement_lower_bound':{'baseline':m.interval_json(q),'additional_native_ports_at_least':18,'necessary_allowance':m.interval_json(allowance),'strict_excess':m.interval_json(excess)},'controls':{'all_native_neighbors_granted_decodes':True,'granting_all21_missing_neighbors_is_outside_scope_and_decodes':True},'classification':'Independent mathematical verification of root last-co-visit argument, with freshly recomputed exact finite source premises. No new kappa; nonnative descending sources and earlier source changes remain open.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print('all10920 ordered pair gaps >=21; source alternatives need18 outside coordinates.');print('Strict native-only movement excess:',m.interval_json(excess)['decimal'])
if __name__=='__main__':main()
