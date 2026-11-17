"""Exact all-source first-exit certificate at the earlier-axis cut."""
from pathlib import Path
from collections import Counter
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json
WORD='1e25b33b748e5ef5599394167acd207d4d3f91afcc202192969adb41734879e7'
GEO='983c931bc9907de160fa59fc2011cff434766d7e7384ce898df05574cc5c61fc'
ARITH='41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def module(p,name):
    spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def basis(rows):
    b={}
    for v in rows:
        while v:
            p=(v&-v).bit_length()-1
            if p in b:v^=b[p]
            else:b[p]=v;break
    return b
def residual(v,b):
    for p in sorted(b):
        if v>>p&1:v^=b[p]
    return v
def dual(rows,target):
    b=basis(rows);v=residual(target,b);assert v;p=(v&-v).bit_length()-1
    d=sum(((residual(1<<j,b)>>p)&1)<<j for j in range(111));assert(d&target).bit_count()%2 and all((d&r).bit_count()%2==0 for r in rows);return d
def record(v):
    with localcontext()as c:
        c.prec=55;return {'rational':list(map(str,v)),'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator))for x in v]}
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--geometry',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert digest(a.word)==WORD and digest(a.geometry)==GEO;g=module(a.geometry,'root_separate_source_geometry')
    base=a.repo/'research/moonshot-005-program';native=base/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert digest(native)==g.NATIVE;R=json.loads(native.read_text())['native_roots']
    w=json.loads(a.word.read_text());charts,V,P=g.replay_cut(w);assert w['carrier_interface_before_operation']==1142 and len(V)==341
    xmask=(1<<111)-1;N=[{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)]
    K=[(1<<i)|sum(1<<j for j in N[i])for i in range(111)];signs=[V[f'Y{i}']&xmask&~255 for i in range(8,111)];bank=K+signs+[1<<j for j in range(8)];assert len(basis(bank))==29
    native_lines={charts[f'L{i}']:i for i in range(111)};native_fields={};other_fields=[]
    for n,v in V.items():
        line=native_lines.get(charts[P[n]])
        if line is None:other_fields.append(n)
        else:
            assert(v&xmask)in[0,1<<line];native_fields.setdefault(line,[]).append(n)
    assert set(native_fields)==set(range(111))
    observations={i:bank+[V[n]&xmask for n in other_fields if g.contains(charts[f'F{i}'],charts[P[n]])]for i in range(111)}
    demands={j:[]for j in range(111)}
    for i in range(8,111):
        assert residual(1<<i,basis(observations[i]+[1<<k for k in N[i]]))==0
        for j in N[i]:
            if residual(1<<i,basis(observations[i]+[1<<k for k in N[i]if k!=j])):demands[j].append(i)
    rows=[];witness_count=0
    for j in range(111):
        selected=[];normals=()
        for i in demands[j]:
            enlarged=g.rref(normals+(tuple(R[i]),))
            if len(enlarged)>len(normals):selected.append(i);normals=enlarged
        r=len(normals);assert r==(0 if j<8 else 7)
        if not r:continue
        assert g.nullspace(normals)==charts[f'L{j}'];witnesses=[]
        for i in selected:
            d=dual(observations[i]+[1<<k for k in N[i]if k!=j],1<<i);assert(d>>j)&1;witnesses.append({'receiver':i,'dual_hex':hex(d)})
        witness_count+=len(witnesses);public=[n for n in native_fields[j]if n.startswith(('X','Y'))];assert public in[[],[f'X{j}']]
        rows.append({'source_role':j,'all_forced_receivers':demands[j],'selected_independent_receivers':selected,'normal_rank':r,'duals':witnesses,'minimum_native_departures':2,'current_native_public_carriers':public})
    assert len(rows)==103 and witness_count==721
    total=sum(x['minimum_native_departures']for x in rows);public=sum(len(x['current_native_public_carriers'])for x in rows);ground=[n for n in V if n.startswith(('X','Y'))and not charts[P[n]]]
    assert total==206 and public==71 and ground==[f'Y{i}'for i in range(8)]
    owned=total-public-len(ground);assert owned==127
    # Check Q0 against the exact public closure; all extra owned moves are future.
    places={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};profile=Counter();suffix=set()
    for step,(kind,n,*args)in enumerate(w['operations']):
        if kind=='INIT':places[n]=args[0]
        elif kind=='MOVE':
            dest=args[0];profile[abs(len(charts[places[n]])-len(charts[dest]))]+=1
            if step>=1142:
                assert n.startswith(('X','Y'))and n not in suffix;suffix.add(n);assert dest==('Hub'if n.startswith('X')else'F'+n[1:])
            places[n]=dest
        elif kind=='CLEAR':del places[n]
    assert len(suffix)==222 and dict(profile)=={1:159,2:103,4:103,5:16,6:16,7:87}
    ar=base/'sessions/2026-11-17-S020/checkpoint2-evidence/C/four-plane-review/check.py';assert digest(ar)==ARITH;m=module(ar,'independent_interval_arithmetic')
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in m.moment(gate));Q0=m.moment(profile);mandatory=dict(profile);mandatory[1]+=owned;lower=m.moment(mandatory);excess=(lower[0]-ceiling[1],lower[1]-ceiling[0]);assert excess[0]>56
    # Independent parity verification uses no discovery elimination.
    for row in rows:
        j=row['source_role']
        for witness in row['duals']:
            i=witness['receiver'];d=int(witness['dual_hex'],16)
            assert(d>>i)&1 and(d>>j)&1 and all((d&x).bit_count()%2==0 for x in observations[i])and all(not(d>>k&1)for k in N[i]if k!=j)
    assert all(residual(1<<i,basis([1<<j for j in range(111)]))==0 for i in range(111))
    assert total-public-111==24<owned
    result={'status':'PASS_ALL_SOURCE_FIRST_EXIT_BOUND_AND_EARLY_AXIS_BANK_EXCLUSION','word_sha256':WORD,'native_sha256':digest(native),'geometry_sha256':GEO,'bank':'canonical+old_sign_queries+all8_coordinate_units','bank_rank':29,'cut':1142,'all_original_columns':222,'live_fields':341,'source_rows':rows,'verified_duals':721,'forced_sources':103,'native_departures':206,'native_public_departure_allowance':71,'ground_public_departure_allowance':8,'minimum_future_owned_ascents':127,'Q0_profile':dict(profile),'mandatory_profile':mandatory,'Q0':record(Q0),'target_excess':record(excess),'controls':{'granting_all_raw_units_removes_forcing':True,'counterfactual111_ground_public_allowances_gives_only24':True},'scope':'Exact earlier-axis cut; monotone public routes; linear processing; every future descending X payload lies in rank29 stated bank. Arbitrary paid nested owned turns allowed. All-field/block extension of binary duals in proof.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],witness_count,'duals;',owned,'owned ascents; excess',record(excess)['decimal'][0])
if __name__=='__main__':main()
