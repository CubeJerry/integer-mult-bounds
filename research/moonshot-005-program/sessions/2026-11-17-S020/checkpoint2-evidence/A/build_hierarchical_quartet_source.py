"""Two-stage proper-chart compression with actual half-sum owners and raw holds."""
from pathlib import Path
import argparse,collections,hashlib,importlib.util,json
from build_quartet_compression_source import SOURCE,SHA,HELPER,CHECK,module,reduced_rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--ground-code',action='store_true');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    h=module(a.repo/HELPER,'hierarchy_helpers');e=module(a.repo/CHECK,'hierarchy_native');raw=(a.repo/SOURCE).read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA;R=json.loads(raw)['native_roots'];dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));K=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];B=[];basis_roles=[]
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
    data=[];hub=[];lower_inverses=[];upper_inverses=[];lower_held=[];upper_held=[];half_fields=[]
    for g,I in sorted(groups.items()):
        if len(g)==1:
            i=I[0];emit(['MOVE',f'X{i}','Hub']);hub.append(i);data.append({'support':list(g),'roles':I,'Hub_pivots':I,'Hub_rows_hex':[hex(1<<i)],'halves':[]});continue
        k=len(data);G=f'QUARTET_{k}';charts[G]={'kind':'span','rows':[R[i]for i in I]};assert len(e.chart(charts[G]))==4
        halves=[];incoming=[]
        for sg in [1,-1]:
            J=[i for i in I if R[i][g[0]]==sg*R[i][g[1]]];assert J
            H=f'HALF_{k}_{sg}';charts[H]={'kind':'span','rows':[R[i]for i in J]};d=len(e.chart(charts[H]));assert 2<=d<=3
            m=sum(1<<i for i in J);local=reduced_rows([r&m for r in B]);P=sorted(local);D=sorted(set(J)-set(P));assert len(P)==d
            for i in J:emit(['MOVE',f'X{i}',H],'half_arrival')
            n=f'ACTUAL_HALF_SUM_{k}_{sg}';init(n,H);half_fields.append(n)
            for i in J:emit(['ADD',f'X{i}',n],'proper_half_sum_capture')
            assert values[n]==m
            for p in P:
                ds=[j for j in D if local[p]>>j&1]
                for j in ds:emit(['ADD',f'X{j}',f'X{p}'],'lower_triangular_encode')
                assert values[f'X{p}']==local[p];lower_inverses.append((p,ds));emit(['MOVE',f'X{p}',G],'lower_code_to_quartet')
            incoming+=P;lower_held+=D
            halves.append({'sign':sg,'chart':H,'roles':J,'rank':d,'pivots':P,'raw_held':D,'code_rows_hex':[hex(local[p])for p in P],'sum_field':n})
        assert len(incoming)+sum(len(z['raw_held'])for z in halves)==len(I)
        inc_rows=[values[f'X{p}']for p in incoming];inc_basis=h.binary_basis(inc_rows);assert len(inc_basis)==len(incoming)
        mask=sum(1<<i for i in I);target_coeff=[h.coeff(inc_basis,row&mask)for row in B];upper=reduced_rows(target_coeff);assert len(upper)==4
        upperP=sorted(upper);upperD=sorted(set(range(len(incoming)))-set(upperP));newH=[]
        for p in upperP:
            n=incoming[p];ds=[incoming[j]for j in upperD if upper[p]>>j&1]
            for j in ds:emit(['ADD',f'X{j}',f'X{n}'],'upper_triangular_encode')
            upper_inverses.append((n,ds));newH.append(n);emit(['MOVE',f'X{n}','Hub'],'global_code_pivot_Hub')
        hub+=newH;upper_held += [incoming[j]for j in upperD]
        data.append({'support':list(g),'roles':I,'chart':G,'halves':halves,'Hub_pivots':newH,'Hub_rows_hex':[hex(values[f'X{p}'])for p in newH],'mixed_held':[incoming[j]for j in upperD]})
    assert len(hub)==64 and len(lower_held)+len(upper_held)==47
    for k,row in enumerate(B):
        n=f'CANONICAL_{k}';init(n,'Hub')
        for g in data:
            mask=sum(1<<i for i in g['roles']);rr=[int(x,16)for x in g['Hub_rows_hex']];c=h.coeff(h.binary_basis(rr),row&mask)
            for j,p in enumerate(g['Hub_pivots']):
                if c>>j&1:emit(['ADD',f'X{p}',n],'actual_hierarchical_code_read')
        assert values[n]==row
        if a.ground_code:emit(['MOVE',n,'zero'],'canonical_descent')
    cut=len(ops);cv=values.copy();ca=at.copy()
    for i in lower_held+upper_held:emit(['MOVE',f'X{i}','Hub'],'held_endpoint_return')
    for n,ds in reversed(upper_inverses):
        for j in ds:emit(['ADD',f'X{j}',f'X{n}'],'actual_upper_inverse')
    for n,ds in reversed(lower_inverses):
        for j in ds:emit(['ADD',f'X{j}',f'X{n}'],'actual_lower_inverse')
    for i in range(111):emit(['MOVE',f'Y{i}',f'F{i}'])
    for n in list(owners):emit(['CLEAR',n])
    w={'schema':'hierarchical-quartet-canonical-source-v1','source_path':SOURCE,'source_sha256':SHA,'charts':charts,'operations':ops,'targets':[],'carrier_interface_before_operation':cut,'construction':{'groups':data,'canonical_basis_roles':basis_roles,'canonical_rows_hex':list(map(hex,B)),'canonical_fields':[f'CANONICAL_{k}'for k in range(9)],'code_location':'zero'if a.ground_code else'Hub','raw_lower_held':lower_held,'mixed_quartet_held':upper_held,'Hub_original_roles':hub,'actual_half_sum_fields':half_fields},'semantic_operation_indices':dict(sem),'scope':'Actual two-level canonical source with proper half-sums, raw rank2/3 holds, mixed rank4 holds, and all native caches. Full originals restore from actual operands; no completed receiver or supplier.'}
    C,hist,stats=e.replay(w,R);assert len(h.binary_basis([cv[f'X{i}']for i in range(111)]))==111
    assert all(cv[f'X{i}']==1<<i for i in lower_held)
    q=h.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceil=tuple(x/6 for x in h.moment(gate));pin=h.save(a.out/'WORD.json',w)
    h.save(a.out/'CUT-INVENTORY.json',{'word_sha256':pin,'cut_before_operation':cut,'fields':[{'name':n,'chart':ca[n],'rank':len(C[ca[n]]),'row_hex':hex(x)}for n,x in sorted(cv.items())]})
    result={'status':'PASS_HIERARCHICAL_QUARTET_CANONICAL_SOURCE','word_sha256':pin,'source_cut':cut,'raw_lower_held':len(lower_held),'raw_lower_rank_histogram':dict(collections.Counter(len(C[ca[f'X{i}']])for i in lower_held)),'mixed_rank4_held':len(upper_held),'actual_half_sum_fields':len(half_fields),'proper_sum_rank_histogram':dict(collections.Counter(len(C[ca[n]])for n in half_fields)),'Hub_originals':64,'canonical_rank':9,'code_location':w['construction']['code_location'],'stats':stats,'moment':h.record(q),'necessary_limiting_room':h.record((ceil[0]-q[1],ceil[1]-q[0])),'complete_outputs':0,'scope':w['scope']};h.save(a.out/'RESULT.json',result);print(json.dumps(result))

if __name__=='__main__':main()
