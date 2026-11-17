"""Full canonical acquisition using actual local triangular source compression.

Four code forms per support quartet ascend;47 raw originals remain low.
"""
from pathlib import Path
import argparse,collections,hashlib,importlib.util,json

SOURCE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
HELPER='research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint3-evidence/A/build_common_carrier_fanout.py'
CHECK='research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py'

def module(p,n):
    sp=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m

def reduced_rows(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    for p in sorted(b):
        for q in b:
            if q!=p and b[q]>>p&1:b[q]^=b[p]
    assert all((v>>q&1)==(p==q)for p,v in b.items()for q in b)
    return dict(sorted(b.items()))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--ground-code',action='store_true');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    h=module(a.repo/HELPER,'quartet_helpers');e=module(a.repo/CHECK,'quartet_native')
    raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots'];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
    K=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];B=[];basis_roles=[]
    for i,row in enumerate(K):
        if len(h.binary_basis(B+[row]))>len(B):B.append(row);basis_roles.append(i)
    assert len(B)==9
    charts={'Hub':{'kind':'span','rows':[[int(i==j)for j in range(8)]for i in range(8)]},'zero':{'kind':'span','rows':[]}}
    for i,r in enumerate(R):charts[f'L{i}']={'kind':'span','rows':[r]};charts[f'F{i}']={'kind':'ann','rows':[r]}
    groups=collections.defaultdict(list)
    for i,r in enumerate(R):groups[tuple(j for j,x in enumerate(r)if x)].append(i)
    ops=[];owners=[];sem=collections.defaultdict(list);values={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    def emit(o,key=None):
        if key:sem[key].append(len(ops))
        ops.append(o);typ,n,*q=o
        if typ=='INIT':values[n]=0;at[n]=q[0];owners.append(n)
        elif typ=='ADD':values[q[0]]^=values[n]
        elif typ=='MOVE':at[n]=q[0]
        elif typ=='CLEAR':del values[n],at[n];owners.remove(n)
    def init(n,p):emit(['INIT',n,p])
    for i in range(111):init(f'NATIVE_{i}',f'L{i}');emit(['ADD',f'X{i}',f'NATIVE_{i}'],'native_capture')
    data=[];hub=[];held=[]
    for g,I in sorted(groups.items()):
        if len(g)==1:
            assert len(I)==1;i=I[0];emit(['MOVE',f'X{i}','Hub']);hub.append(i);data.append({'support':list(g),'roles':I,'pivots':I,'held':[],'local_code_rows_hex':[hex(1<<i)],'chart':'Hub'});continue
        assert len(g)==4;G=f'QUARTET_{len(data)}';charts[G]={'kind':'span','rows':[R[i]for i in I]};assert len(e.chart(charts[G]))==4
        mask=sum(1<<i for i in I);local=reduced_rows([r&mask for r in B]);assert len(local)==4
        P=sorted(local);H=sorted(set(I)-set(P));held+=H;hub+=P
        for i in I:emit(['MOVE',f'X{i}',G],'quartet_arrival')
        for p in P:
            assert local[p]==(1<<p)^sum(1<<j for j in H if local[p]>>j&1)
            for j in H:
                if local[p]>>j&1:emit(['ADD',f'X{j}',f'X{p}'],'triangular_encode')
            assert values[f'X{p}']==local[p];emit(['MOVE',f'X{p}','Hub'],'coded_pivot_Hub')
        data.append({'support':list(g),'roles':I,'pivots':P,'held':H,'local_code_rows_hex':[hex(local[p])for p in P],'chart':G})
    assert len(hub)==64 and len(held)==47
    for k,row in enumerate(B):
        n=f'CANONICAL_{k}';init(n,'Hub')
        for g in data:
            for p in g['pivots']:
                if row>>p&1:emit(['ADD',f'X{p}',n],'actual_local_code_read')
        assert values[n]==row
        if a.ground_code:emit(['MOVE',n,'zero'],'full_code_descent')
    cut=len(ops);cv=values.copy();ca=at.copy()
    for i in held:emit(['MOVE',f'X{i}','Hub'],'held_raw_return')
    for g in data:
        for p,hexrow in zip(g['pivots'],g['local_code_rows_hex']):
            row=int(hexrow,16)
            for j in g['held']:
                if row>>j&1:emit(['ADD',f'X{j}',f'X{p}'],'actual_triangular_inverse')
    for i in range(111):emit(['MOVE',f'Y{i}',f'F{i}'])
    for n in list(owners):emit(['CLEAR',n])
    w={'schema':'quartet-triangular-full-canonical-source-v1','source_path':SOURCE,'source_sha256':SHA,'charts':charts,'operations':ops,'targets':[],'carrier_interface_before_operation':cut,'construction':{'groups':data,'canonical_basis_roles':basis_roles,'canonical_rows_hex':list(map(hex,B)),'canonical_fields':[f'CANONICAL_{k}'for k in range(9)],'code_location':'zero'if a.ground_code else'Hub','held_raw_roles':held,'Hub_original_roles':hub},'semantic_operation_indices':dict(sem),'scope':'Actual full111-variable canonical source with47 raw originals held at rank4 support quartets and111 native caches. All original inputs restored by actual inverses. No receiver endpoint completed; no supplier or kappa.'}
    C,hist,stats=e.replay(w,R);expected={3:103,4:103,7:119}
    if a.ground_code:expected[8]=9
    assert stats['movement_profile']==expected
    assert len(h.binary_basis([cv[f'X{i}']for i in range(111)]))==111
    assert all(cv[f'X{i}']==1<<i and len(C[ca[f'X{i}']])==4 for i in held)
    q=h.moment(expected);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceil=tuple(x/6 for x in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[{'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(x)}for n,x in sorted(cv.items())]})
    result={'status':'PASS_QUARTET_COMPRESSION_FULL_CANONICAL_SOURCE','word_sha256':pin,'source_cut':cut,'groups':14,'held_raw_originals':47,'actual_native_caches':111,'Hub_originals':64,'canonical_rank':9,'code_location':w['construction']['code_location'],'stats':stats,'moment':h.record(q),'necessary_limiting_room':h.record((ceil[0]-q[1],ceil[1]-q[0])),'complete_outputs':0,'scope':w['scope']};h.save(a.out/'RESULT.json',result);print(json.dumps(result))

if __name__=='__main__':main()
