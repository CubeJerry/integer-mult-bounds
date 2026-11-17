"""Actual direct-known57 source with all54 unknown originals held at rank two.

Source creation is exact; no complete decoder or supplier is claimed.
"""
from pathlib import Path
import argparse, collections, hashlib, importlib.util, json, sys

SOURCE = 'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SOURCE_SHA = '8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PARENT = 'research/moonshot-005-program/sessions/2026-11-16-S018/checkpoint5-evidence/R/initial-chart-cut/control/NATIVE-CACHED57-WORD.json'
PARENT_SHA = '7df1fc8f696545185c417c6df4161b324869bf084b503138506425510e841fa2'
CHECK = 'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py'
HELPER = 'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint3-evidence/A/build_common_carrier_fanout.py'

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec); spec.loader.exec_module(obj)
    return obj

def build(repo, matching, out):
    out.mkdir(parents=True, exist_ok=True)
    h = load_module(repo/HELPER, 'all54_exact_helpers')
    e = load_module(repo/CHECK, 'all54_native_checker')
    raw = (repo/SOURCE).read_bytes(); assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA
    R = json.loads(raw)['native_roots']
    old = (repo/PARENT).read_bytes(); assert hashlib.sha256(old).hexdigest() == PARENT_SHA
    S = sorted(json.loads(old)['targets']); U = sorted(set(range(111))-set(S))
    assert len(S) == 57 and len(U) == 54
    pairs = [(int(p['unknown']), int(p['known'])) for p in matching['pairs']]
    assert len(pairs) == 54 and {u for u,c in pairs} == set(U)
    assert len({c for u,c in pairs}) == 54 and {c for u,c in pairs} <= set(S)
    dot = lambda i,j: sum(a*b for a,b in zip(R[i],R[j]))
    charts = {'Hub': {'kind':'span','rows':[[int(i==j) for j in range(8)] for i in range(8)]}, 'zero': {'kind':'span','rows':[]}}
    for i,r in enumerate(R):
        charts[f'L{i}'] = {'kind':'span','rows':[r]}
        charts[f'F{i}'] = {'kind':'ann','rows':[r]}
    operations=[]; owners=[]; semantic=collections.defaultdict(list)
    val={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i) for i in range(111)}
    at={f'X{i}':f'L{i}' for i in range(111)}|{f'Y{i}':'zero' for i in range(111)}
    def emit(o, kind=None):
        if kind: semantic[kind].append(len(operations))
        operations.append(o); op,n,*q=o
        if op=='INIT': val[n]=0; at[n]=q[0]; owners.append(n)
        elif op=='ADD': val[q[0]]^=val[n]
        elif op=='MOVE': at[n]=q[0]
        elif op=='CLEAR': del val[n],at[n]; owners.remove(n)
        else: raise ValueError(o)
    def init(n,p): emit(['INIT',n,p])
    # Every initial native value has an actual stationary record.
    for i in range(111):
        init(f'NATIVE_{i}',f'L{i}'); emit(['ADD',f'X{i}',f'NATIVE_{i}'],'native_capture')
    ground={}
    for c in S:
        n=f'GROUND_{c}';ground[c]=n;init(n,f'L{c}')
        emit(['ADD',f'X{c}',n],'known_capture');emit(['MOVE',n,'zero'],'known_descent')
        emit(['ADD',n,f'Y{c}'],'known_endpoint');emit(['MOVE',f'Y{c}',f'F{c}'])
    direct_cut=len(operations)
    pair_data=[]
    for k,(u,c) in enumerate(pairs):
        p=f'PAIR_{k}';charts[p]={'kind':'span','rows':[R[u],R[c]]}
        emit(['MOVE',f'X{u}',p],'held_unknown_arrival');emit(['MOVE',f'X{c}',p],'known_pair_arrival')
        emit(['ADD',f'X{u}',f'X{c}'],'known_proxy_encoding')
        emit(['MOVE',f'X{c}','Hub'],'masked_Hub_arrival')
        pair_data.append({'unknown':u,'known':c,'chart':p,'unfinished_facets':sum(dot(i,u)==dot(i,c)==0 for i in U)})
    um=sum(1<<u for u in U);rows=[];basis_roles=[]
    for i in U:
        row=((1<<i)^sum(1<<j for j in U if dot(i,j)==0))&um
        if len(h.binary_basis(rows+[row])) > len(rows):rows.append(row);basis_roles.append(i)
    assert len(rows)==9
    mapping=dict(pairs);hub=[];corrections=[];masks=[]
    for k,row in enumerate(rows):
        n=f'CODE_{k}';m=f'MASK_{k}';init(n,'Hub');init(m,'zero');hub.append(n);corrections.append(m);mask=0
        for u in U:
            if row>>u&1:
                c=mapping[u];emit(['ADD',f'X{c}',n],'masked_source_read');emit(['ADD',ground[c],m],'known_correction_read');mask^=1<<c
        assert val[n]==row^mask and val[m]==mask;masks.append(mask)
    cut=len(operations);cutval=val.copy();cutat=at.copy();cutowners=owners.copy()
    for u,c in pairs:emit(['MOVE',f'X{u}','Hub'],'held_unknown_return')
    for u,c in pairs:emit(['ADD',f'X{u}',f'X{c}'],'actual_proxy_inverse')
    for i in range(111):
        if at[f'X{i}']!='Hub':emit(['MOVE',f'X{i}','Hub'])
        if at[f'Y{i}']!=f'F{i}':emit(['MOVE',f'Y{i}',f'F{i}'])
    for n in list(owners):emit(['CLEAR',n])
    w={'schema':'direct-known57-all54-held-source-v1','source_path':SOURCE,'source_sha256':SOURCE_SHA,'charts':charts,'operations':operations,'targets':S,'carrier_interface_before_operation':cut,'construction':{'known_roles':S,'unknown_roles':U,'pairs':pair_data,'ground_raw_names':{str(c):ground[c] for c in S},'masked_canonical_basis_roles':basis_roles,'canonical_unknown_rows_hex':list(map(hex,rows)),'known_correction_rows_hex':list(map(hex,masks)),'Hub_source_fields':hub,'ground_correction_fields':corrections,'direct_known_cut':direct_cut},'semantic_operation_indices':dict(semantic),'source_contract_change':'Direct known57 acquisition; no inherited KEEP/proper mask fields and no preserved earlier operation prefix.','scope':'Actual all54-held masked source;57 completed outputs,111 actual native caches,9 masked canonical Hub fields and9 actual ground corrections. No code delivery or complete supplier.'}
    C,hist,stats=e.replay(w,R)
    assert stats['movement_profile']=={1:165,6:108,7:114},stats
    assert all(cutval[f'NATIVE_{i}']==1<<i and cutat[f'NATIVE_{i}']==f'L{i}' for i in range(111))
    assert len(h.binary_basis([cutval[f'X{c}']&um for u,c in pairs]))==54
    assert len(h.binary_basis([cutval[f'X{i}'] for i in range(111)]))==111
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(z/6 for z in h.moment(gate));q=h.moment(stats['movement_profile'])
    pin=h.save(out/'WORD.json',w)
    h.save(out/'MATCHING.json',{'schema':'all54-known-proxy-matching-v1','pairs':[{'unknown':u,'known':c} for u,c in pairs],'status':'Frozen feasible input; no optimization claim.'})
    h.save(out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[{'name':n,'chart':cutat[n],'rank':len(C[cutat[n]]),'row_hex':hex(x)} for n,x in sorted(cutval.items())],'held_access':{str(i):[p['unknown'] for p in pair_data if e.sub(C[p['chart']],C[f'F{i}'])] for i in U}})
    result={'status':'PASS_ACTUAL_DIRECT_KNOWN57_ALL54_HELD_SOURCE','word_sha256':pin,'stats':stats,'source_cut':cut,'live_fields':len(cutval),'unknown_Hub_quotient_rank':54,'original_rank':111,'held_unknown_originals':54,'actual_native_values':111,'canonical_rank':9,'moment':h.record(q),'necessary_limiting_room':h.record((ceiling[0]-q[1],ceiling[1]-q[0])),'source_contract_change':w['source_contract_change'],'scope':w['scope']}
    h.save(out/'RESULT.json',result)
    print(json.dumps(result))
    return w,result

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--matching',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    build(a.repo,json.loads(a.matching.read_text()),a.out)

if __name__=='__main__':main()
