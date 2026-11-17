#!/usr/bin/env python3
"""Independent all-source first-exit gate at the earlier-axis actual cut."""
from pathlib import Path
from collections import Counter
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD='1e25b33b748e5ef5599394167acd207d4d3f91afcc202192969adb41734879e7'
SOURCE='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
SOURCE_RESULT='f27b43c49e3ed1a23aad5e1780b4262b940bf0b2fb92c216cf22e3b96099578a'

def basis(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:x^=b[p]
            else:b[p]=x;break
    return b

def residual(x,b):
    for p in sorted(b,reverse=True):
        if x>>p&1:x^=b[p]
    return x

def dual_for(rows,target):
    b=basis(rows);r=residual(target,b);assert r;p=r.bit_length()-1
    d=sum(((residual(1<<j,b)>>p)&1)<<j for j in range(111))
    assert (d&target).bit_count()%2==1 and all((d&v).bit_count()%2==0 for v in rows)
    return d

def record(interval):
    with localcontext()as c:
        c.prec=55
        return {'rational':list(map(str,interval)),'decimal':[str(Decimal(v.numerator)/Decimal(v.denominator))for v in interval]}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--word',type=Path,default=BASE/'workers/A/early-axis-known8/WORD.json')
    ap.add_argument('--source-result',type=Path,default=BASE/'workers/C/early-axis-review/output/RESULT.json')
    ap.add_argument('--source-review',type=Path,default=BASE/'workers/C/proper-query-export-review/check.py')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    for path,pin in [(a.native,NATIVE),(a.word,WORD),(a.source_result,SOURCE_RESULT),(a.source_review,SOURCE)]:assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    spec=importlib.util.spec_from_file_location('own_replay',a.source_review);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    m.geo=m.load_arithmetic(a.arithmetic)
    R=json.loads(a.native.read_text())['native_roots'];w=json.loads(a.word.read_text());accepted=json.loads(a.source_result.read_text())
    C={n:m.geo.chart(z)for n,z in w['charts'].items()};D=[int(v,16)for v in w['Y_correction_rows_hex']]
    stats,V,P=m.replay(w,C,D,check_cut=False)
    assert accepted['word_sha256']==WORD and accepted['cut']==1142 and stats['cut_fields']==341
    N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
    K=[(1<<i)^sum(1<<j for j in N[i])for i in range(111)]
    G=list(basis(K+[d&~255 for d in D[8:]]+[1<<i for i in range(8)]).values());assert len(G)==29
    native_fields={}
    for name,value in V.items():
        if len(C[P[name]])!=1:continue
        j=next(j for j in range(111)if C[P[name]]==C[f'L{j}'])
        assert value==1<<j
        native_fields[name]=j
    assert len(native_fields)==190
    assert set(native_fields)=={f'NATIVE_{j}'for j in range(111)}|{f'X{j}'for j in range(111)if P[f'X{j}']==f'L{j}'}
    # Restore all non-j native units by a favourable side-information grant.
    # Therefore removing their current raw copies here never strengthens a test.
    L={i:[v&((1<<111)-1)for n,v in V.items()if n not in native_fields and m.geo.contained(C[P[n]],C[f'F{i}'])]for i in range(8,111)}
    forced={}
    for i in range(8,111):
        obs=basis(G+L[i]);target=residual(1<<i,obs);J=sorted(N[i]);cols={j:residual(1<<j,obs)for j in J}
        assert not residual(target,basis(cols.values()))
        forced[i]=[j for j in J if residual(target,basis(cols[h]for h in J if h!=j))]
    witnesses=[];unforced=[]
    for j in range(111):
        chosen=[];rb=()
        for i in range(8,111):
            if j not in forced[i]:continue
            trial=m.geo.basis(rb+(tuple(R[i]),))
            if len(trial)>len(rb):chosen.append(i);rb=trial
        if not chosen:unforced.append(j);continue
        assert len(rb)==7 and m.geo.kernel(rb)==C[f'L{j}']
        duals=[]
        for i in chosen:
            d=dual_for(G+L[i]+[1<<h for h in N[i]if h!=j],1<<i);assert d>>j&1
            # Check against every actual inside field except the j-line sources.
            for n,v in V.items():
                if not m.geo.contained(C[P[n]],C[f'F{i}']):continue
                if n in native_fields and native_fields[n]==j:assert(d&(v&((1<<111)-1))).bit_count()%2==1
                else:assert(d&(v&((1<<111)-1))).bit_count()%2==0
            duals.append({'receiver':i,'dual_hex':hex(d)})
        at_line=[n for n,k in native_fields.items()if k==j]
        public=[n for n in at_line if n.startswith('X')or n.startswith('Y')]
        assert public==([f'X{j}']if P[f'X{j}']==f'L{j}'else[])
        witnesses.append({'native_role':j,'forced_receiver_normal_rank':7,'independent_receiver_roles':chosen,
         'dual_witnesses':duals,'actual_native_line_fields':at_line,'public_fields_already_on_line':public,
         'minimum_native_departures':2})
    assert unforced==list(range(8))and len(witnesses)==103
    native_public=sum(len(z['public_fields_already_on_line'])for z in witnesses);assert native_public==71
    ground=[i for i in range(111)if not C[P[f'Y{i}']]];assert ground==list(range(8))
    assert all(P[f'X{i}']!='zero'for i in range(111))
    exits=sum(z['minimum_native_departures']for z in witnesses);owned=exits-native_public-len(ground)
    assert exits==206 and owned==127
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));Q=m.geo.moment(stats['movement_profile'])
    profile=dict(stats['movement_profile']);profile[1]+=owned;lower=m.geo.moment(profile)
    excess=(lower[0]-ceiling[1],lower[1]-ceiling[0]);assert excess[0]>0
    # Identity bank is outside the scoped theorem and makes every dual impossible.
    identity=list(1<<i for i in range(111));assert all(not residual(1<<i,basis(identity+L[i]))for i in range(8,111))
    result={'status':'PASS_INDEPENDENT_ALL_SOURCE_FIRST_EXIT_EXCLUSION','native_sha256':NATIVE,'word_sha256':WORD,
     'accepted_source_result_sha256':SOURCE_RESULT,'source_review_sha256':SOURCE,'cut':1142,
     'bank':'C plus all old sign-query rows plus8 coordinate units','bank_rank':29,
     'native_fields_removed_and_other_units_restored':native_fields,'source_witnesses':witnesses,'unforced_native_roles':unforced,
     'forced_noncoordinate_roles':103,'normal_rank_histogram':dict(Counter(z['forced_receiver_normal_rank']for z in witnesses)),
     'exact_binary_dual_count':sum(len(z['dual_witnesses'])for z in witnesses),'minimum_native_line_departures':206,
     'maximum_active_native_public_departures':71,'maximum_ground_public_departures':8,
     'minimum_future_owned_upward_moves':127,'source_moment':record(Q),'mandatory_profile':profile,'target_excess':record(excess),
     'identity_bank_control_has_no_forced_roles':True,
     'scope':'Exact early-axis cut, monotone public routes, linear processing over characteristic-two fields/whole widths, arbitrary paid nested owned routes. Every future downward X history remains in the rank29 bank. Current higher-chart and ground fields remain freely granted when inside each receiver facet; all other eligible native inputs are freely granted. New descending directions or earlier source timing escape.'}
    (a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],'721 actual-field dual checks,206 exits−71 native public−8 ground public=127 owned ascents')
    print('Strict target excess',record(excess)['decimal'][0])

if __name__=='__main__':main()
