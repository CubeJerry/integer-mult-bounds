#!/usr/bin/env python3
"""Independent exact static-code gate and source-cut audit; no author imports."""
from __future__ import annotations
import argparse, hashlib, json
from fractions import Fraction
from functools import cache
from pathlib import Path

NATIVE_PATH='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
WORD_PATH='research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint3-evidence/A/native57-masked-hub/WORD.json'
NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD_SHA='f21de38f4a8adc1a55920c16b684285f62607829fe512a0088fe5ecb217fcfdd'
REMOTE_SHA='93b11dd75d7ffda723204bd212e5728cbea95592'
U=[5,13,14,15,17,18,24,25,26,31,32,33,35,52,53,54,55,56,57,58,59,60,62,63,66,68,69,70,71,72,81,82,83,84,85,86,87,89,91,93,95,96,97,98,99,100,101,102,103,105,106,107,109,110]
J=[14,18,31,35,55,56,105,109]
E=[66,69,70,89,93]
T=[18,55,56,105,109]
Z=15
SUPPORTS={66:[55,109],69:[56,105],70:[55,105],89:[18,109],93:[18,105]}

def need(ok,message):
    if not ok:raise ValueError(message)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,data):path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def validate_witness(roots,extra_edges=frozenset()):
    def dot(i,j):return sum(a*b for a,b in zip(roots[i],roots[j]))
    def adjacent(i,j):return (i,j) in extra_edges or (i!=j and dot(i,j)==0)
    need(set(J+E+[Z])<=set(U),'witness in exact unfinished set')
    need(all(not adjacent(i,j) for i in J for j in J),'frame principal block is identity')
    supports={e:[j for j in J if adjacent(e,j)] for e in E}
    need(supports==SUPPORTS,'literal frame supports')
    need(set(sum(supports.values(),[]))==set(T),'five-channel union')
    pairs=[]
    for a,e in enumerate(E):
        for f in E[a+1:]:
            overlap=sorted(set(supports[e])&set(supports[f]))
            need(not overlap or not adjacent(e,f),'overlapping edge roles have zero fitting entry')
            pairs.append({'roles':[e,f],'intersection':overlap,'real_dot':dot(e,f),'zero_reason':'disjoint factor supports' if not overlap else 'forbidden native adjacency'})
    need([j for j in J if adjacent(Z,j)]==T,'final row uses saturated channels')
    need(all(not adjacent(Z,e) and not adjacent(e,Z) for e in E),'final row annihilates all five channels')
    return {'frame':J,'edge_roles':E,'channel_roles':T,'final_role':Z,'role_roots':{i:roots[i] for i in J+E+[Z]},'ordered_frame_dots':[[dot(i,j) for j in J] for i in J],'frame_supports':supports,'edge_pair_checks':pairs,'final_frame_neighbors':T,'final_edge_dots':{e:dot(Z,e) for e in E}}

def canonical_certificate(roots):
    rows=[sum(1<<j for j,v in enumerate(U) if u==v or sum(a*b for a,b in zip(roots[u],roots[v]))==0) for u in U]
    pivots={};original_basis=[];basis_roles=[]
    for role,original in zip(U,rows):
        row=original;recipe=0
        while row:
            pivot=row.bit_length()-1
            if pivot in pivots:
                p,combo=pivots[pivot];row^=p;recipe^=combo
            else:
                index=len(original_basis)
                pivots[pivot]=(row,recipe^(1<<index))
                original_basis.append(original);basis_roles.append(role)
                break
    need(len(original_basis)==9,'fresh binary canonical rank nine')
    recipes=[]
    for i,original in enumerate(rows):
        row=original;recipe=0
        while row:
            pivot=row.bit_length()-1;need(pivot in pivots,'basis spans canonical row')
            p,combo=pivots[pivot];row^=p;recipe^=combo
        reconstructed=0
        for j,b in enumerate(original_basis):
            if recipe>>j&1:reconstructed^=b
        need(reconstructed==original,'exact binary expansion')
        need(original>>i&1,'canonical own coefficient');recipes.append(recipe)
    return {'ordered_unknown_roles':U,'rows_hex':list(map(hex,rows)),'basis_roles':basis_roles,'basis_rows_hex':list(map(hex,original_basis)),'row_recipes_hex':list(map(hex,recipes)),'rank':9,'scope':'Exact binary identities extend to every characteristic-two field; nine whole-width records suffice statically.'}

@cache
def reduced(rows):
    a=[list(map(Fraction,r)) for r in rows];k=0
    for col in range(8):
        row=next((row for row in range(k,len(a)) if a[row][col]),None)
        if row is None:continue
        a[k],a[row]=a[row],a[k];q=a[k][col];a[k]=[x/q for x in a[k]]
        for row in range(len(a)):
            if row!=k and a[row][col]:
                q=a[row][col];a[row]=[x-q*y for x,y in zip(a[row],a[k])]
        k+=1
    return tuple(tuple(row) for row in a[:k])

def inside_facet(spec,root):
    rows=tuple(tuple(row) for row in spec['rows'])
    if spec['kind']=='span':return all(sum(x*y for x,y in zip(row,root))==0 for row in rows)
    need(spec['kind']=='ann','recognized literal chart')
    return len(reduced(rows+(tuple(root),)))==len(reduced(rows))

def prefix_state(word):
    values={f'X{i}':1<<i for i in range(111)}
    values.update({f'Y{i}':1<<(111+i) for i in range(111)})
    loc={f'X{i}':f'L{i}' for i in range(111)}
    loc.update({f'Y{i}':'zero' for i in range(111)})
    cut=word['carrier_interface_before_operation'];need(cut==1129,'exact admitted cut')
    for tag,name,*arg in word['operations'][:cut]:
        if tag=='INIT':need(name not in values,'fresh field');values[name]=0;loc[name]=arg[0]
        elif tag=='ADD':values[arg[0]]^=values[name]
        elif tag=='MOVE':loc[name]=arg[0]
        elif tag=='CLEAR':del values[name];del loc[name]
        else:raise ValueError('unknown opcode')
    need(len(values)==392,'all actual fields audited')
    need(all(values[f'Y{i}']==1<<(111+i) for i in U),'unfinished Y fields remain arbitrary')
    return values,loc

def scope_audit(word,roots,values,loc):
    mask=sum(1<<u for u in U);receipts=[];leaks=[]
    for i in U:
        neighbors={u for u in U if sum(x*y for x,y in zip(roots[i],roots[u]))==0}
        neighbor_mask=sum(1<<u for u in neighbors);count=0
        for name,row in values.items():
            if inside_facet(word['charts'][loc[name]],roots[i]):
                count+=1;bad=row&mask&~neighbor_mask
                if bad:leaks.append({'receiver':i,'name':name,'chart':loc[name],'nonlocal_roles':[u for u in U if bad>>u&1]})
        receipts.append({'receiver':i,'inside_fields':count,'native_neighbors':sorted(neighbors)})
    return {'cut_before_operation':word['carrier_interface_before_operation'],'live_fields':len(values),'receivers':receipts,'nonlocal_dependencies':leaks,'all_source_dependencies_native_local':not leaks}

def rank_eight_control(roots,include_final,extra_edges):
    assigned={j:j for j in J}|{66:55,69:56,70:105,89:109,93:18}
    if include_final:assigned[Z]=55
    roles=list(assigned)
    for i in roles:
        for j in roles:
            entry=int(assigned[i]==assigned[j])
            if i==j:need(entry==1,'control diagonal')
            elif sum(a*b for a,b in zip(roots[i],roots[j]))!=0 and (i,j) not in extra_edges:
                need(entry==0,'control forbidden entry')
    need(set(assigned.values())==set(J),'control rank exactly eight')
    return {'roles':roles,'channel_assignment':assigned,'rank':8,'scope':'Only this modified witness, not the full 54-role graph.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path);p.add_argument('--native',type=Path);p.add_argument('--word',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.repo:native_path=a.repo/NATIVE_PATH;word_path=a.repo/WORD_PATH
    else:
        need(a.native is not None and a.word is not None,'provide --repo or --native and --word')
        native_path=a.native;word_path=a.word
    need(digest(native_path)==NATIVE_SHA,'exact native source bytes')
    need(digest(word_path)==WORD_SHA,'exact admitted source word bytes')
    roots=json.loads(native_path.read_text())['native_roots'];word=json.loads(word_path.read_text())
    need(len(roots)==111 and all(len(r)==8 for r in roots),'native dimensions')
    need(sorted(set(range(111))-set(word['targets']))==U,'same 57-known/54-unknown partition')
    need(word['construction']['unknown_roles']==U,'metadata partition agreement')
    witness=validate_witness(roots);canonical=canonical_certificate(roots)
    values,loc=prefix_state(word);scope=scope_audit(word,roots,values,loc)
    need(scope['all_source_dependencies_native_local'],'actual source application premise')
    no_final=rank_eight_control(roots,False,frozenset());extra=frozenset({(Z,66),(66,Z)})
    extra_edge=rank_eight_control(roots,True,extra)
    try:validate_witness(roots,extra)
    except ValueError as exc:bad_geometry=str(exc)
    else:raise ValueError('changed forbidden-edge geometry accepted')
    bad_scope=scope_audit(word,roots,values|{'SCOPE_CONTROL_LEAK':1<<Z},loc|{'SCOPE_CONTROL_LEAK':'zero'})
    need(not bad_scope['all_source_dependencies_native_local'],'planted nonlocal source rejected')
    need(any(z['receiver']==Z and z['name']=='SCOPE_CONTROL_LEAK' for z in bad_scope['nonlocal_dependencies']),'own-input leakage control')
    a.out.mkdir(parents=True,exist_ok=True)
    cert={'remote_programme_sha':REMOTE_SHA,'native_source':{'path':NATIVE_PATH,'sha256':NATIVE_SHA},'word':{'path':WORD_PATH,'sha256':WORD_SHA},'witness':witness,'canonical_upper_bound':canonical,'actual_source_scope':scope,'controls':{'remove_final_demand':no_final,'grant_missing_edge':extra_edge,'changed_geometry_rejected':bad_geometry,'planted_source_leak_rejected':bad_scope['nonlocal_dependencies']}}
    write(a.out/'CERTIFICATE.json',cert)
    result={'status':'PASS_FOURTEEN_ROLE_BLOCK_FACTOR_OBSTRUCTION_AND_CURRENT_SOURCE_SCOPE','unknown_roles':54,'known_roles':57,'witness_roles':14,'canonical_scalar_rank_characteristic_two':9,'all_fields_all_positive_block_lengths':'broadcast dimension > 8m','whole_record_linear_broadcast_count_characteristic_two':9,'vector_rank_at_least_9m_claimed':False,'actual_cut':1129,'audited_fields':392,'source_leaks':0,'linear_future_strict_owned_downward_transfers_at_least':9,'nine_distinct_lifetimes_claimed':False,'nonlinear_lower_bound_claimed':False,'new_complete_kappa':False,'controls':['13-role rank8 fit','14-role added-edge rank8 fit','changed forbidden-edge certificate rejected','planted initial-source leakage rejected']}
    write(a.out/'RESULT.json',result);print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
