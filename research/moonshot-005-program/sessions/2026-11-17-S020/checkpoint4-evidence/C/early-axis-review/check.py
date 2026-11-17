#!/usr/bin/env python3
"""Independent earlier-axis source, forced exits and fresh-transcript review."""
from pathlib import Path
from collections import Counter
from decimal import Decimal,localcontext
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD='1e25b33b748e5ef5599394167acd207d4d3f91afcc202192969adb41734879e7'
PARENT='c77823c87362a56ed3c3f10f9808995285dd3f454e11443531f069075f59f4fe'
SOURCE='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
ENTROPY='582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23'
MAPPED='67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e'
CORE=[61,82,83,20,18,71,70,69,74,76,63];ISOLATES=[65,109,107]

def load(path,pin,name):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

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
    ap.add_argument('--parent',type=Path,default=BASE/'workers/A/low-retention-corrections/WORD.json')
    ap.add_argument('--source-review',type=Path,default=BASE/'workers/C/proper-query-export-review/check.py')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--entropy-review',type=Path,default=BASE/'workers/C/entropy54-review/check.py')
    ap.add_argument('--mapped',type=Path,default=BASE/'workers/R/fresh-transcript-nine/output/MAPPED-DUAL.json')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    for path,pin in [(a.native,NATIVE),(a.word,WORD),(a.parent,PARENT),(a.mapped,MAPPED)]:assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    m=load(a.source_review,SOURCE,'own_source');m.geo=m.load_arithmetic(a.arithmetic)
    e=load(a.entropy_review,ENTROPY,'own_entropy')
    R=json.loads(a.native.read_text())['native_roots'];w=json.loads(a.word.read_text());p=json.loads(a.parent.read_text())
    C={n:m.geo.chart(z)for n,z in w['charts'].items()};assert w['charts']==p['charts']
    assert w['construction']['parent_word_sha256']==PARENT
    eye=tuple(tuple(int(i==j)for j in range(8))for i in range(8))
    assert C['zero']==()and C['Hub']==eye
    for i,r in enumerate(R):assert C[f'L{i}']==m.geo.basis((tuple(r),))and C[f'F{i}']==m.geo.kernel((tuple(r),))
    N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
    masks=[sum(1<<j for j in J)for J in N];oldD=[int(v,16)for v in p['Y_correction_rows_hex']]
    _,PV,PP=m.replay(p,C,oldD,check_cut=False)
    expectedD=[1<<i if i<8 else(masks[i]&255)^(oldD[i]&~255)for i in range(111)]
    assert w['Y_correction_rows_hex']==list(map(hex,expectedD))
    assert all(expectedD[i].bit_count()==8 and not(expectedD[i]&~masks[i])for i in range(8,111))
    first=[]
    for i in range(111):first.extend([['INIT',f'NATIVE_{i}',f'L{i}'],['ADD',f'X{i}',f'NATIVE_{i}']])
    assert p['operations'][:222]==first
    bootstrap=[]
    for i in range(8):bootstrap.extend([['INIT',f'EARLY_AXIS_{i}',f'L{i}'],['ADD',f'X{i}',f'EARLY_AXIS_{i}'],['MOVE',f'EARLY_AXIS_{i}','zero'],['ADD',f'EARLY_AXIS_{i}',f'Y{i}']])
    bootstrap.extend([['ADD',f'EARLY_AXIS_{j}',f'Y{i}']for i in range(8,111)for j in range(8)if j in N[i]])
    assert len(bootstrap)==444
    coordinate_fields={f'{kind}{i}'for kind in ['X','Y']for i in range(8)}
    removed=[];sign_ops=[]
    for j,op in enumerate(p['operations'][222:p['carrier_interface_before_operation']],222):
        operands=op[1:3]if op[0]=='ADD'else op[1:2]
        if coordinate_fields&set(operands):removed.append(j)
        else:sign_ops.append(op)
    expected_ops=first+bootstrap+sign_ops+p['operations'][p['carrier_interface_before_operation']:]+[['CLEAR',f'EARLY_AXIS_{i}']for i in range(8)]
    assert w['operations']==expected_ops and len(removed)==138
    assert [z['old_index']for z in w['construction']['removed_parent_axis_courier_operations']]==removed
    assert w['carrier_interface_before_operation']==len(first+bootstrap+sign_ops)==1142
    stats,V,P=m.replay(w,C,expectedD,check_cut=False)
    EV,EP=PV.copy(),PP.copy()
    for i in range(111):EV[f'Y{i}']=(1<<(111+i))^expectedD[i]
    for i in range(8):
        EV[f'X{i}']=1<<i;EP[f'X{i}']=f'L{i}';EP[f'Y{i}']='zero'
        EV[f'EARLY_AXIS_{i}']=1<<i;EP[f'EARLY_AXIS_{i}']='zero'
    assert V==EV and P==EP and len(V)==341
    assert stats['counts']=={'INIT':119,'ADD':777,'MOVE':484,'CLEAR':119}
    assert stats['movement_profile']=={1:159,2:103,4:103,5:16,6:16,7:87}
    assert stats['owned_downward_profile']=={1:8}and stats['peak_owned']==stats['dirty_CLEAR']==119
    assert dict(Counter(len(C[P[f'X{i}']])for i in range(111)))=={1:79,2:16,3:16}
    assert dict(Counter(len(C[P[f'Y{i}']])for i in range(111)))=={0:8,3:103}
    assert len(basis(V[f'X{i}']for i in range(111)))==111
    closure=[op for op in w['operations'][1142:]if op[0]=='MOVE']
    assert len(closure)==222 and len({op[1]for op in closure})==222
    assert all(op[2]==('Hub'if op[1].startswith('X')else f"F{op[1][1:]}")for op in closure)
    controls={}
    for key in ['actual_native_axis_capture','paid_native_axis_descent','prepare_axis_diagonal_value',
     'ground_native_axis_preload','G0:early_pair_read','G1:later_pair_read','G2:pair_encode','G3:later_pair_read','deferred_sign_inverse_at_Hub']:
        alt=json.loads(json.dumps(w));j=alt['semantic_operation_indices'][key][0];del alt['operations'][j]
        if j<1142:alt['carrier_interface_before_operation']-=1
        try:m.replay(alt,C,expectedD,check_cut=False)
        except ValueError as err:controls['omit_'+key]=str(err)
        else:raise AssertionError('missing source step accepted')
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));Q=m.geo.moment(stats['movement_profile']);room=(ceiling[0]-Q[1],ceiling[1]-Q[0])
    K=[(1<<i)^masks[i]for i in range(111)]
    G=list(basis(K+[d&~255 for d in oldD]+[1<<i for i in range(8)]).values());assert len(G)==29
    E=[i for i in range(111)if len(C[P[f'X{i}']])>1];assert E==list(range(22,46))+list(range(88,96))
    assert all([n for n in V if C[P[n]]==C[f'L{j}']]==[f'NATIVE_{j}']for j in E)
    ground=[i for i in range(111)if not C[P[f'Y{i}']]];assert ground==list(range(8))
    L={i:[v&((1<<111)-1)for n,v in V.items()if not n.startswith('NATIVE_')and m.geo.contained(C[P[n]],C[f'F{i}'])]for i in range(8,111)}
    forced={}
    for i in range(8,111):
        b=basis(G+L[i]);target=residual(1<<i,b);J=sorted(set(E)&N[i]);cols={j:residual(1<<j,b)for j in J}
        assert not residual(target,basis(cols.values()))
        forced[i]=[j for j in J if residual(target,basis(cols[h]for h in J if h!=j))]
    fanout=[]
    for j in E:
        chosen=[];rb=()
        for i in range(8,111):
            if j not in forced[i]:continue
            trial=m.geo.basis(rb+(tuple(R[i]),))
            if len(trial)>len(rb):chosen.append(i);rb=trial
        assert len(rb)==7 and m.geo.kernel(rb)==C[f'L{j}']
        duals=[]
        for i in chosen:
            d=dual_for(G+L[i]+[1<<h for h in E if h in N[i]and h!=j],1<<i);assert d>>j&1
            duals.append({'receiver':i,'dual_hex':hex(d)})
        fanout.append({'expired_role':j,'demand_normal_rank':7,'independent_receiver_roles':chosen,'duals':duals,'native_departures':2})
    mapped=json.loads(a.mapped.read_text());e.CORE=CORE;e.ISO=ISOLATES;entropy=e.review_dual(mapped,R)
    assert entropy['terms']==106 and entropy['full_bound']=='17/2'
    fresh=sorted(set(range(8,111))-set(E));assert len(fresh)==71 and set(CORE+ISOLATES)<=set(fresh)
    mask=sum(1<<i for i in fresh)
    def audit(values,places):
        receipts=[]
        for i in fresh:
            names=[n for n in values if m.geo.contained(C[places[n]],C[f'F{i}'])]
            if any(values[n]&mask&~masks[i]for n in names):raise ValueError('nonlocal current fresh-input leak')
            receipts.append({'receiver':i,'inside_fields':len(names)})
        return receipts
    locality=audit(V,P)
    assert all(V[f'X{i}']==V[f'NATIVE_{i}']==1<<i and P[f'X{i}']==P[f'NATIVE_{i}']==f'L{i}'for i in fresh)
    planted=dict(V);places=dict(P);planted['LEAK_CONTROL']=1<<CORE[0];places['LEAK_CONTROL']='zero'
    try:audit(planted,places)
    except ValueError as err:leak_control=str(err)
    else:raise AssertionError('planted fresh source leak accepted')
    bad=json.loads(json.dumps(mapped));bad['terms'].pop()
    try:e.review_dual(bad,R)
    except ValueError as err:dual_control=str(err)
    else:raise AssertionError('missing dual term accepted')
    profile=dict(stats['movement_profile']);profile[1]+=65;lower=m.geo.moment(profile)
    residual_room=(ceiling[0]-lower[1],ceiling[1]-lower[0]);assert residual_room[0]>0
    source={'status':'PASS_INDEPENDENT_EARLY_AXIS_KNOWN_EIGHT_SOURCE','native_sha256':NATIVE,'word_sha256':WORD,
     'parent_sha256':PARENT,'source_review_sha256':SOURCE,'cut':1142,'live_fields':341,'stats':stats,
     'prepared_diagonal_values_at_ground':8,'completed_outputs_at_closed_facets':8,'unfinished_outputs':103,
     'native_foreign_axis_coefficients':412,'native_foreign_sign_coefficients':412,'original_X_rank':111,
     'moment':record(Q),'necessary_room':record(room),'negative_controls':controls}
    bound={'status':'PASS_SCOPED_56_UPWARD_PLUS_9_DOWNWARD_NECESSARY_BOUND','word_sha256':WORD,
     'fixed_bank':'C plus all old sign-query rows plus all8 raw axes','bank_rank':29,'fanout':fanout,
     'minimum_native_line_departures':64,'maximum_public_line_departures':8,'minimum_future_owned_upward_moves':56,
     'mapped_entropy_certificate_sha256':MAPPED,'entropy_review_sha256':ENTROPY,'exact_entropy_bound':'17/2',
     'fresh_roles':fresh,'fresh_locality_receipts':locality,'fresh_core':CORE,'fresh_isolates':ISOLATES,
     'bank_independent_future_owned_descent_lower_bound':9,'minimum_total_future_owned_moves':65,
     'mandatory_profile':profile,'residual_necessary_room':record(residual_room),'strict_exclusion':False,
     'planted_leak_rejected':leak_control,'missing_dual_term_rejected':dual_control,
     'scope':'Exact new cut; public routes monotone; arbitrary paid nested owned routes. The56 upward bound assumes linear processing and all future downward X histories in the rank29 bank. The9 downward bound is bank independent, with fixed schedule finite-alphabet zero-error scope and retained all-field linear block witness. Positive residual room is necessary only, not a completion.'}
    (a.out/'RESULT.json').write_text(json.dumps(source,indent=2)+'\n')
    (a.out/'CONTINUATION-CERTIFICATE.json').write_text(json.dumps(bound,indent=2)+'\n')
    (a.out/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())],indent=2)+'\n')
    print(source['status']);print(bound['status'],'remaining necessary room',record(residual_room)['decimal'][0])

if __name__=='__main__':main()
