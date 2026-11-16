#!/usr/bin/env python3
"""Exact source-specific no-descent / native-port continuation certificate.

This derives source rows from the full 222-column word using C's independent
interpreter. It imports no construction-author code. The universal causal and
nonlinear implications are proved in PROOF.md.
"""
import argparse,hashlib,importlib.util,json
from collections import Counter
from pathlib import Path


def bits(z):return sum(1<<i for i in z)
def inds(z):return [i for i in range(111)if z>>i&1]
def parity(z):return z.bit_count()&1

def solve(equations):
    basis={}
    for z,b in equations:
        while z:
            p=z.bit_length()-1
            if p in basis:z^=basis[p][0];b^=basis[p][1]
            else:basis[p]=(z,b);break
        if not z and b:raise ValueError('inconsistent binary equations')
    answer=0
    for p,(z,b)in sorted(basis.items()):
        if b^parity(z&answer):answer|=1<<p
    if not all(parity(z&answer)==b for z,b in equations):raise ValueError('bad independently solved collision')
    return answer


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--audit-module',type=Path,default=Path(__file__).resolve().parents[1]/'portable'/'audit_cp6.py');a=ap.parse_args()
    sp=importlib.util.spec_from_file_location('own_independent_native',a.audit_module);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);need=m.insist
    w=json.loads(a.word.read_text());need(m.sha(a.word)=='f5acfcb454d6d50dfdb7d66acd2c33980e4aed17826afafbb67fbeb2168f58c1','source word pin')
    s=json.loads((a.repo/w['source_path']).read_text());need(m.sha(a.repo/w['source_path'])=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native root pin')
    cut=w['carrier_interface_before_operation'];stats,snaps,C,events=m.replay(w,s,[cut]);v,l=snaps[cut];T=set(w['targets']);U=set(range(111))-T;R=s['native_roots'];need(len(T)==6 and len(U)==105,'source receiver split')
    for i in range(111):
        need(v[f'X{i}']=={i}and C[l[f'X{i}']]==C['Hub'],'all raw X originals already at Hub')
        need(v[f'NATIVE_RAW_{i}']=={i}and C[l[f'NATIVE_RAW_{i}']]==C[f'L{i}'],'actual raw native source')
        need(v[f'Y{i}']==({111+i,i}if i in T else{111+i}),'arbitrary original Y at cut')
        need(C[l[f'Y{i}']]==C[f'F{i}']if i in T else C[l[f'Y{i}']]==C['zero'],'actual current Y location')
    need(len({C[f'L{i}']for i in range(111)})==111,'111 genuinely distinct native lines')
    code=[set(v[f'CANONICAL_{a}'])for a in range(9)]
    need(all(C[l[f'CANONICAL_{a}']]==C['zero']for a in range(9)),'all code really at ground')
    cb=m.binary_basis(code);need(len(cb)==9,'actual rank-nine code')
    N={i:{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)}
    originals={f'X{i}'for i in range(111)}|{f'Y{i}'for i in range(111)}
    proper=[n for n in v if n not in originals and 1<len(C[l[n]])<8]
    need(len(proper)==20,'all twenty proper-chart owners counted')
    need(all(not m.subset(C[l[n]],C[f'F{i}'])for i in U for n in proper),'no proper-chart owner accessible to any unfinished final facet')
    need(all(not m.subset(C[f'F{j}'],C[f'F{i}'])for i in U for j in T),'completed receiver facets inaccessible')
    full_allowed={f'NATIVE_RAW_{j}'for j in range(111)}|{f'CANONICAL_{a}'for a in range(9)}|set(proper)|originals
    need(set(v)==full_allowed,'no hidden additional source field at cut')
    codewords=[]
    for mask in range(512):
        z=set()
        for b in range(9):
            if mask>>b&1:z^=code[b]
        codewords.append(z)
    need(len({bits(z)for z in codewords})==512,'complete codeword enumeration')
    profile=[]
    for i in sorted(U):
        ki=N[i]|{i};need(ki in codewords,'canonical fitting row present')
        need(all(not z or not z<=N[i]for z in codewords),'no nonzero code supported on native neighbors')
        other_min=min(len(z-N[i])for z in codewords if z and z!=ki)
        need(other_min>=18,'distance gap to every alternative fitting row')
        need(len(m.binary_basis(code+[{j}for j in N[i]]))==9+len(N[i]),'independent rank version of uniqueness')
        need(m.in_span({i},m.binary_basis(code+[{j}for j in N[i]])),'positive all-native-grant decoding control')
        profile.append({'receiver':i,'neighbors':sorted(N[i]),'code_neighbor_intersection_dimension':0,'minimum_other_code_support_outside_neighbors':other_min})
    forced_targets=[0,2,4,5];need(set(forced_targets)<=U,'four unfinished witness receivers')
    need(set.union(*(N[i]for i in forced_targets))==set(range(111)),'four receivers force every native input')
    witnesses=[]
    for j in range(111):
        i=next(i for i in forced_targets if j in N[i]);eq=[(bits(z),0)for z in code]+[(1<<k,0)for k in sorted(N[i]-{j})]+[(1<<i,1)]
        h=solve(eq);need((h>>j)&1==1,'missing raw site changes on witness')
        need(not m.in_span({i},m.binary_basis(code+[{k}for k in N[i]-{j}])),'missing-site decoding really impossible')
        need(m.in_span({i},m.binary_basis(code+[{k}for k in N[i]])),'granting omitted raw site destroys obstruction')
        witnesses.append({'native_site':j,'receiver':i,'collision_difference_support':inds(h)})
    counts={j:len(N[j]&U)for j in range(111)};need(min(counts.values())==49,'robust unfinished-neighbor count')
    # Independent interval budget arithmetic. The baseline word closes each
    # unfinished Y with one direct rank-seven move after the source cut.
    suffix_moves=[e for e in events if e[0]>=cut]
    need(len(suffix_moves)==105 and all(n.startswith('Y')and int(n[1:])in U and src=='zero'and dst==f'F{int(n[1:])}'and d==7 and not owned for k,n,src,dst,d,owned in suffix_moves),'exact baseline pending movement')
    delta=m.moment({1:1,6:1,7:-1});need(0<delta[0]<delta[1]<1,'strict native-line route surcharge')
    native_floor=m.moment({1:111,6:105,7:-105})
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    allowance=tuple(z/6 for z in m.moment(gate));q=m.moment(stats['movement_profile']);room=(allowance[0]-q[1],allowance[1]-q[0]);remaining=(room[0]-native_floor[1],room[1]-native_floor[0])
    ports={}
    for k in [6,7,8]:
        f=(k+(111-k)*delta[0],k+(111-k)*delta[1]);left=(room[0]-f[1],room[1]-f[0]);ports[k]={'optimistic_added_moment':m.interval_json(f),'remaining_moment_room':m.interval_json(left)}
    need(ports[7]['remaining_moment_room']['rational']and room[0]>(7+104*delta[1]),'seven-port optimistic floor not excluded')
    need(room[1]<(8+103*delta[0]),'eight-port optimistic floor excluded')
    result={'status':'PASS_SOURCE_SPECIFIC_FANOUT_NATIVE_EXPOSURE_GATE','word_sha256':m.sha(a.word),'source_sha256':w['source_sha256'],'cut_before_operation':cut,'targets':sorted(T),'unfinished':sorted(U),'proper_owners_inaccessible_to_every_unfinished_facet':proper,'code_rank':9,'minimum_nonzero_code_weight':min(len(z)for z in codewords if z),'code_weight_histogram':dict(sorted(Counter(map(len,codewords[1:])).items())),'receiver_uniqueness_and_distance':profile,'four_forcing_receivers':forced_targets,'all111_independent_functional_collision_witnesses':witnesses,'native_neighbor_count_among_unfinished':counts,'minimum_unfinished_neighbors_per_native_site':min(counts.values()),'no_new_owned_move':{'native_sites_forced':111,'available_ascending_originals':105,'maximum_native_lines_per_original':1,'status':'impossible for this cut, even with local nonlinear Y feedback and fixed schedule'},'native_only_downward_ports':{'source_charts':'exact native lines; each nontrivial owned descent is to zero','at_least_ports':6,'code_distance_argument_for_distinct_ports_at_most':17,'native_route_surcharge':m.interval_json(delta),'optimistic_added_moment_floor':m.interval_json(native_floor),'original_baseline_moment':m.interval_json(q),'necessary_limiting_allowance':m.interval_json(allowance),'remaining_moment_after_floor':m.interval_json(remaining),'port_count_budget_screens':ports,'necessary_port_counts_to_survive_movement_screen':[6,7]},'negative_controls':{'full_native_antichain_grant_decodes_every_receiver':True,'granting_each_omitted_raw_site_kills_its_dual_collision':True,'eight_port_lower_bound_exceeds_room':True,'seven_port_lower_bound_remains_below_room':True},'scope':'Fixed source and input-independent schedules; arbitrary local nonlinear processing and original Y interactions. No ownership/storage/erasure invoice, no assertion a six- or seven-port completion exists, no strict supplier and no new kappa. Earlier source changes and descents from nonnative source charts remain outside the native-only theorem.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print('No-descent:111 required native sites >105 available Y originals.');print('Native-only added moment floor:',m.interval_json(native_floor)['decimal']);print('Remaining necessary allowance:',m.interval_json(remaining)['decimal'])
if __name__=='__main__':main()
