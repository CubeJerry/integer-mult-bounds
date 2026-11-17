#!/usr/bin/env python3
"""Independent95-ground-Y source and actual40-up+9-down interface."""
from pathlib import Path
from collections import defaultdict,Counter
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
WORD='4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f'
PARENT='1e25b33b748e5ef5599394167acd207d4d3f91afcc202192969adb41734879e7'
SOURCE='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
FANOUT='f7666c123fdcd1df5b46adb3920ebffff55c0e306a2104397961343ae88070d2'
FANOUT_CERT='1aadaa3f045080410a86adbb602d3b6c99e6a2fb03ab4353e3fda4cf74639eba'
ENTROPY='582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23'
MAPPED='67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e'
def load(path,pin,name):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser()
    for flag,default in [('native','workers/C/native.json'),('word','workers/A/ground-retention-known8/WORD.json'),
     ('parent','workers/A/early-axis-known8/WORD.json'),('source-review','workers/C/proper-query-export-review/check.py'),
     ('arithmetic','workers/C/four-plane-review/check.py'),('fanout-review','workers/C/all-source-exit-review/check.py'),
     ('fanout-certificate','workers/C/all-source-exit-review/output/CERTIFICATE.json'),
     ('entropy-review','workers/C/entropy54-review/check.py'),('mapped','workers/R/fresh-transcript-nine/output/MAPPED-DUAL.json')]:p.add_argument('--'+flag,type=Path,default=BASE/default)
    p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    m=load(a.source_review,SOURCE,'own_source');m.geo=m.load_arithmetic(a.arithmetic)
    b=load(a.fanout_review,FANOUT,'own_algebra');e=load(a.entropy_review,ENTROPY,'own_entropy')
    for path,pin in [(a.native,b.NATIVE),(a.word,WORD),(a.parent,PARENT),(a.fanout_certificate,FANOUT_CERT),(a.mapped,MAPPED)]:assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    R=json.loads(a.native.read_text())['native_roots'];w=json.loads(a.word.read_text());old=json.loads(a.parent.read_text())
    C={n:m.geo.chart(z)for n,z in w['charts'].items()};assert w['charts']==old['charts']and w['construction']['parent_word_sha256']==PARENT
    N=[{j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0}for i in range(111)]
    masks=[sum(1<<j for j in I)for I in N];parentD=[int(x,16)for x in old['Y_correction_rows_hex']]
    _,PV,PP=m.replay(old,C,parentD,check_cut=False);groups=defaultdict(list)
    for i in range(8,111):groups[PP[f'Y{i}']].append(i)
    representatives=sorted(min(I)for I in groups.values());deferred=sorted(set(range(8,111))-set(representatives))
    assert len(representatives)==16 and len(deferred)==87
    assert w['construction']['representative_query_Y_roles']==representatives and w['construction']['deferred_ground_Y_roles']==deferred
    expectedD=[(masks[i]&255)if i in deferred else parentD[i]for i in range(111)]
    assert w['Y_correction_rows_hex']==list(map(hex,expectedD));kept=[];removed=[];deferred_names={f'Y{i}'for i in deferred}
    for j,op in enumerate(old['operations']):
        target=op[1]if op[0]=='MOVE'else op[2]if op[0]=='ADD'else''
        if 666<=j<1142 and target in deferred_names:removed.append(j)
        else:kept.append(op)
    assert len(removed)==348 and w['operations']==kept and w['carrier_interface_before_operation']==794
    assert Counter(old['operations'][j][0]for j in removed)=={'MOVE':174,'ADD':174}
    stats,V,P=m.replay(w,C,expectedD,check_cut=False);EV,EP=PV.copy(),PP.copy()
    for i in deferred:EV[f'Y{i}']=(1<<(111+i))^expectedD[i];EP[f'Y{i}']='zero'
    assert V==EV and P==EP and len(V)==341
    assert stats['counts']=={'INIT':119,'ADD':603,'MOVE':310,'CLEAR':119}
    assert stats['movement_profile']=={1:72,2:16,4:16,5:16,6:16,7:174}
    assert stats['owned_downward_profile']=={1:8}and stats['dirty_CLEAR']==stats['peak_owned']==119
    assert Counter(len(C[P[f'Y{i}']])for i in range(111))=={0:95,3:16}
    assert len(b.basis(V[f'X{i}']for i in range(111)))==111 and sum(expectedD[i].bit_count()for i in range(8,111))==476
    closure=[op for op in w['operations'][794:]if op[0]=='MOVE']
    assert len(closure)==222 and len({op[1]for op in closure})==222
    assert all(op[2]==('Hub'if op[1].startswith('X')else f"F{op[1][1:]}")for op in closure)
    controls={}
    for key in ['actual_native_axis_capture','paid_native_axis_descent','prepare_axis_diagonal_value','ground_native_axis_preload',
     'G0:early_pair_read','G1:later_pair_read','G2:pair_encode','G3:later_pair_read','deferred_sign_inverse_at_Hub']:
        alt=json.loads(json.dumps(w));j=alt['semantic_operation_indices'][key][0];del alt['operations'][j]
        if j<794:alt['carrier_interface_before_operation']-=1
        try:m.replay(alt,C,expectedD,check_cut=False)
        except ValueError as err:controls['omit_'+key]=str(err)
        else:raise AssertionError('missing operation accepted')
    finish(a,b,m,e,R,w,C,N,masks,parentD,stats,V,P,representatives,deferred,controls)

def finish(a,b,m,e,R,w,C,N,masks,parentD,stats,V,P,representatives,deferred,controls):
    K=[(1<<i)^masks[i]for i in range(111)]
    G=list(b.basis(K+[d&~255 for d in parentD[8:]]+[1<<j for j in range(8)]).values());assert len(G)==29
    prior=json.loads(a.fanout_certificate.read_text());witnesses=[]
    for z in prior['source_witnesses']:
        j=z['native_role'];I=z['independent_receiver_roles'];rb=m.geo.basis(tuple(tuple(R[i])for i in I))
        assert len(rb)==7 and m.geo.kernel(rb)==C[f'L{j}']
        for entry in z['dual_witnesses']:
            i=entry['receiver'];d=int(entry['dual_hex'],16)
            assert d>>i&1 and d>>j&1 and all((d&v).bit_count()%2==0 for v in G)
            assert all(not(d>>h&1)for h in N[i]if h!=j)
            for n,v in V.items():
                if not m.geo.contained(C[P[n]],C[f'F{i}']):continue
                native_j=C[P[n]]==C[f'L{j}']and v==1<<j
                assert(d&(v&((1<<111)-1))).bit_count()%2==int(native_j)
        witnesses.append(z)
    assert len(witnesses)==103 and sum(len(z['dual_witnesses'])for z in witnesses)==721
    native_public=[i for i in range(8,111)if P[f'X{i}']==f'L{i}'];ground=[i for i in range(111)if not C[P[f'Y{i}']]]
    assert len(native_public)==71 and len(ground)==95 and 206-len(native_public)-len(ground)==40
    mapped=json.loads(a.mapped.read_text());e.CORE=mapped['roles'];e.ISO=mapped['isolates'];exact=e.review_dual(mapped,R)
    assert exact['terms']==106 and exact['full_bound']=='17/2'
    fresh=sorted(set(range(8,111))-(set(range(22,46))|set(range(88,96))));assert len(fresh)==71
    freshmask=sum(1<<j for j in fresh);audits=[]
    for i in fresh:
        names=[n for n in V if m.geo.contained(C[P[n]],C[f'F{i}'])]
        assert all(not(V[n]&freshmask&~masks[i])for n in names)
        audits.append({'receiver':i,'inside_fields':len(names)})
    assert set(e.CORE+e.ISO)<=set(fresh)
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));Q=m.geo.moment(stats['movement_profile']);room=(ceiling[0]-Q[1],ceiling[1]-Q[0])
    mandatory=dict(stats['movement_profile']);mandatory[1]+=49;lower=m.geo.moment(mandatory)
    residual_room=(ceiling[0]-lower[1],ceiling[1]-lower[0]);assert residual_room[0]>0
    result={'status':'PASS_INDEPENDENT95_GROUND_Y_SOURCE_AND_SCOPED49_MOVE_INTERFACE','native_sha256':b.NATIVE,'word_sha256':WORD,
     'parent_sha256':PARENT,'cut':794,'live_fields':341,'stats':stats,'representative_roles':representatives,'deferred_roles':deferred,
     'completed_diagonal_values_at_ground':8,'unfinished_native_foreign_coefficients':476,'source_original_X_rank':111,
     'moment':b.record(Q),'necessary_room':b.record(room),'negative_controls':controls,
     'fixed_bank_rank':29,'prior_dual_certificate_sha256':FANOUT_CERT,'reverified_source_witnesses':witnesses,
     'native_departure_lower_bound':206,'native_public_departure_credit':71,'ground_public_departure_credit':95,
     'owned_upward_lower_bound':40,'mapped_entropy_certificate_sha256':MAPPED,'fresh_locality_audits':audits,
     'bank_independent_owned_descent_lower_bound':9,'conditional_future_owned_move_lower_bound':49,
     'mandatory_profile':mandatory,'residual_necessary_room':b.record(residual_room),'strict_exclusion':False,
     'scope':'Exact95-ground-Y source accepted all222. The40-up bound assumes linear continuation with downward X histories in C+signqueries+axes;9-down is independent of that bank. Arbitrary paid owned ascents and turns are allowed, public routes are monotone. Positive margin is necessary only.'}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())],indent=2)+'\n')
    print(result['status']);print('40 ascents +9 descents, residual necessary room',b.record(residual_room)['decimal'][0])

if __name__=='__main__':main()

