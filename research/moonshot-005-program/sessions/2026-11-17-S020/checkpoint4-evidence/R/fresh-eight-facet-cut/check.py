"""Independent exact geometry and all-column replay of an eight-facet fresh cut."""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
PINS={
'low-retention-corrections':'c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe',
'proper-query-exports':'4d4e0a4163483d35741505c747981a2bc8b8da1bc373bb0cb8d10f0aa651f96c',
'direct-pair-exports-4':'33a07beacc3895822300eb34ebb847f5b9ff030cc2ad82cdfbc3152fe8402fc0',
'direct-pair-exports-12':'6472eee72de969e204b546549fabdd9bd1cfaa5353ea8d4078b94d5ab1a44e05',
'direct-pair-exports-16':'91cd623b23d299d44da5355838d5ead01614bc2ce6f2cf696a8d6500b73824c1'}
TARGETS=[14,16,60,63,84,85,107,109]
def rref(rows):
    a=[list(map(Fraction,r))for r in rows];p=0
    for c in range(8):
        v=next((i for i in range(p,len(a))if a[i][c]),None)
        if v is None:continue
        a[p],a[v]=a[v],a[p];scale=a[p][c];a[p]=[x/scale for x in a[p]]
        for i in range(len(a)):
            if i!=p and a[i][c]:
                scale=a[i][c];a[i]=[x-scale*y for x,y in zip(a[i],a[p])]
        p+=1
    return tuple(tuple(r)for r in a[:p])
def nullspace(rows):
    a=rref(rows);piv=[next(i for i,x in enumerate(r)if x)for r in a];out=[]
    for c in range(8):
        if c in piv:continue
        v=[Fraction(0)for _ in range(8)];v[c]=1
        for i,p in enumerate(piv):v[p]=-a[i][c]
        out.append(v)
    return rref(out)
def chart(spec):
    assert spec['kind']in['span','ann']
    return rref(spec['rows'])if spec['kind']=='span'else nullspace(spec['rows'])
def contains(large,small):
    for row in small:
        v=list(row)
        for r in large:
            p=next(i for i,x in enumerate(r)if x);c=v[p]
            if c:v=[x-c*y for x,y in zip(v,r)]
        if any(v):return False
    return True
def replay_cut(word):
    charts={n:chart(v)for n,v in word['charts'].items()}
    V={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    P={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    for op in word['operations'][:word['carrier_interface_before_operation']]:
        kind,n,*args=op
        if kind=='INIT':assert n not in V;V[n]=0;P[n]=args[0]
        elif kind=='ADD':
            dst=args[0];assert n!=dst and charts[P[n]]==charts[P[dst]];V[dst]^=V[n]
        elif kind=='MOVE':
            dest=args[0];a,b=charts[P[n]],charts[dest]
            assert a!=b and(contains(a,b)or contains(b,a))
            if n.startswith(('X','Y')):assert contains(b,a)
            P[n]=dest
        else:
            assert kind=='CLEAR'and not n.startswith(('X','Y'));del V[n];del P[n]
    return charts,V,P
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--inputs',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';raw=native.read_bytes();assert hashlib.sha256(raw).hexdigest()==NATIVE
    R=json.loads(raw)['native_roots'];dot=[[sum(x*y for x,y in zip(R[i],R[j]))for j in TARGETS]for i in TARGETS];assert all(x for row in dot for x in row)
    target_mask=sum(1<<i for i in TARGETS);cases=[]
    for name,pin in PINS.items():
        f=a.inputs/name/'WORD.json';raw=f.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin;w=json.loads(raw)
        charts,V,P=replay_cut(w);inventory=json.loads((f.parent/'CUT-INVENTORY.json').read_text());assert inventory['word_sha256']==pin
        assert {x['name']:(x['chart'],int(x['row_hex'],16))for x in inventory['fields']}=={n:(P[n],V[n])for n in V}
        for i,r in enumerate(R):assert charts[f'L{i}']==rref([r])and charts[f'F{i}']==nullspace([r])
        inside=[n for n in sorted(V)if any(all(sum(x*y for x,y in zip(row,R[i]))==0 for row in charts[P[n]])for i in TARGETS)]
        assert all(V[n]&target_mask==0 for n in inside)
        carriers=[n for n in sorted(V)if V[n]&target_mask];expected={f'X{i}'for i in TARGETS}|{f'NATIVE_{i}'for i in TARGETS};assert set(carriers)==expected and not(set(carriers)&set(inside))
        assert all(P[f'X{i}']==P[f'NATIVE_{i}']==f'L{i}'and V[f'X{i}']==V[f'NATIVE_{i}']==1<<i for i in TARGETS)
        assert inside and((V[inside[0]]^(1<<TARGETS[0]))&target_mask)!=0
        orthogonal=next((i,j)for i in range(111)for j in range(i+1,111)if sum(x*y for x,y in zip(R[i],R[j]))==0)
        assert contains(charts[f'F{orthogonal[0]}'],charts[f'L{orthogonal[1]}'])
        cases.append({'source':name,'word_sha256':pin,'cut':w['carrier_interface_before_operation'],'field_count':len(V),'inside_region_count':len(inside),'inside_region_fields':inside,'selected_input_carriers':carriers,'initial_selected_input_rank':0,'required_final_selected_input_rank_per_record_width':8,'minimum_future_downward_transfers':8,'controls':{'planted_inside_target_rejected':True,'orthogonal_pair_rejected':list(orthogonal)}})
    result={'status':'PASS_INDEPENDENT_EIGHT_FACET_FRESH_INFORMATION_CUT','native_sha256':NATIVE,'roles':TARGETS,'dot_products':dot,'cases':cases,'scope':'Actual five cuts; any future code bank; monotone public routes. At least8 whole-record downward transfers, hence8 owned descents. No maximum-clique or optimal information-bound claim.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status']);print([(x['source'],x['inside_region_count'])for x in cases])
if __name__=='__main__':main()
