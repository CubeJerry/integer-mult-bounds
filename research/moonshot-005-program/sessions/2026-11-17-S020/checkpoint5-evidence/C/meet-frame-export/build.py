#!/usr/bin/env python3
"""Pure frame sum exported from its rank3 source to the rank1 meet."""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
PARENT='4628d085fc99ea258f03c374926e1a97852497ff7fe0cec1206cb32bc0bb2c9f'
SOURCE='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
ALGEBRA='f7666c123fdcd1df5b46adb3920ebffff55c0e306a2104397961343ae88070d2'
def load(path,pin,name):
    assert hashlib.sha256(path.read_bytes()).hexdigest()==pin
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser()
    for flag,default in [('native','workers/C/native.json'),('parent','workers/A/ground-retention-known8/WORD.json'),
     ('source-review','workers/C/proper-query-export-review/check.py'),('arithmetic','workers/C/four-plane-review/check.py'),
     ('algebra','workers/C/all-source-exit-review/check.py')]:p.add_argument('--'+flag,type=Path,default=BASE/default)
    p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    m=load(a.source_review,SOURCE,'own_replay');m.geo=m.load_arithmetic(a.arithmetic);b=load(a.algebra,ALGEBRA,'own_algebra')
    assert hashlib.sha256(a.native.read_bytes()).hexdigest()==b.NATIVE and hashlib.sha256(a.parent.read_bytes()).hexdigest()==PARENT
    R=json.loads(a.native.read_text())['native_roots'];w=json.loads(a.parent.read_text());oldops=w['operations'];oldcut=w['carrier_interface_before_operation']
    C={n:m.geo.chart(z)for n,z in w['charts'].items()};D=[int(x,16)for x in w['Y_correction_rows_hex']]
    _,PV,PP=m.replay(w,C,D,check_cut=False);assert oldcut==794
    S=[73,78,81,86];h=sum(1<<i for i in S);H='MEET_FRAME_SOURCE';I='MEET_FRAME_LINE';owner='MEET_FRAME_EXPORT';collector='X73'
    line=[0,1,0,0,1,0,0,0];w['charts'][H]={'kind':'span','rows':[R[i]for i in S]};w['charts'][I]={'kind':'span','rows':[line]}
    C[H]=m.geo.chart(w['charts'][H]);C[I]=m.geo.chart(w['charts'][I]);Q=C['G2_A-1'];J=m.geo.basis(C[H]+Q)
    assert len(C[H])==3 and len(C[I])==1 and m.geo.contained(C[I],C[H])
    assert len(J)==5 and m.geo.contained(C[I],Q)and len(C[H])+len(Q)-len(J)==1
    assert all(m.geo.contained(C[I],C[f'F{i}'])for i in [81,86])
    assert all(PV[f'X{i}']==1<<i and PP[f'X{i}']==f'L{i}'for i in S)
    ops=[];sem={};oldkeys={j:key for key,VV in w['semantic_operation_indices'].items()for j in VV}
    def emit(op,key):sem.setdefault(key,[]).append(len(ops));ops.append(op)
    for j,op in enumerate(oldops[:oldcut]):emit(op,oldkeys[j])
    for i in S:emit(['MOVE',f'X{i}',H],'meet_frame_native_gather')
    for i in S[1:]:emit(['ADD',f'X{i}',collector],'meet_frame_encode')
    emit(['INIT',owner,H],'meet_frame_owner_birth');emit(['ADD',collector,owner],'meet_frame_actual_capture')
    emit(['MOVE',owner,I],'meet_frame_paid_rank2_descent');cut=len(ops);assert cut==804
    inserted=False
    for j,op in enumerate(oldops[oldcut:],oldcut):
        if not inserted and oldkeys[j]=='deferred_sign_inverse_at_Hub':
            for i in S[1:]:emit(['ADD',f'X{i}',collector],'meet_frame_inverse_at_Hub')
            inserted=True
        emit(op,oldkeys[j])
    assert inserted;emit(['CLEAR',owner],'meet_frame_retirement')
    w['operations']=ops;w['semantic_operation_indices']=sem;w['carrier_interface_before_operation']=cut
    w['schema']='pure-frame-meet-export-v1';w['construction']['parent_word_sha256']=PARENT
    w['construction']['pure_meet_frame']={'roles':S,'row_hex':hex(h),'source_chart':H,'destination_chart':I,
     'destination_direction':line,'comparison_query':'G2_A-1','comparison_join_rank':5,'collector':collector,'owner':owner}
    w['scope']='Actual pure frame sum acquired at rank3 and exported by one paid rank2 descent to its rank1 meet with old query G2_A-1. All public Y states and old pair carriers remain unchanged. No original carrier is loaded with the nonlocal mode. Eight completed coordinate outputs only; no complete supplier.'
    stats,V,P=m.replay(w,C,D,check_cut=False);EV,EP=PV.copy(),PP.copy()
    for i in S:EP[f'X{i}']=H
    EV[collector]=h;EV[owner]=h;EP[owner]=I
    assert V==EV and P==EP and len(V)==342 and len(b.basis(V[f'X{i}']for i in range(111)))==111
    assert stats['counts']=={'INIT':120,'ADD':610,'MOVE':315,'CLEAR':120}
    assert stats['movement_profile']=={1:72,2:21,4:16,5:20,6:16,7:170}
    assert stats['owned_downward_profile']=={1:8,2:1}and stats['dirty_CLEAR']==stats['peak_owned']==120
    finish(a,b,m,R,w,C,D,S,h,H,I,owner,stats,V,P,EV,EP,sem)

def finish(a,b,m,R,w,C,D,S,h,H,I,owner,stats,V,P,EV,EP,sem):
    groups=defaultdict(list)
    for i in range(8,111):groups[tuple(j for j,x in enumerate(R[i])if x)].append(i)
    halfrows=[sum(1<<i for i in roles if R[i][p]==s*R[i][q])for support,roles in groups.items()for p,q in combinations(support,2)for s in [1,-1]]
    halfbank=list(b.basis(halfrows+[1<<j for j in range(8)]).values());assert len(halfbank)==64 and b.residual(h,b.basis(halfbank))
    N=[sum(1<<j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0)for i in range(111)]
    K=[(1<<i)^N[i]for i in range(111)];bank=b.basis(K+[d&~255 for d in D]+[1<<j for j in range(8)]+[h]);assert len(bank)==30
    controls={}
    for key in ['meet_frame_native_gather','meet_frame_encode','meet_frame_actual_capture','meet_frame_paid_rank2_descent','meet_frame_inverse_at_Hub']:
        alt=json.loads(json.dumps(w));j=sem[key][0];del alt['operations'][j]
        if j<804:alt['carrier_interface_before_operation']-=1
        try:
            _,av,ap=m.replay(alt,C,D,check_cut=False)
            assert av==EV and ap==EP
        except(ValueError,AssertionError)as err:controls['omit_'+key]=str(err)
        else:raise AssertionError('missing frame operation accepted')
    alt=json.loads(json.dumps(w));alt['charts'][I]={'kind':'span','rows':[[1,0,0,0,0,0,0,0]]};badC={n:m.geo.chart(z)for n,z in alt['charts'].items()}
    try:m.replay(alt,badC,D,check_cut=False)
    except ValueError as err:controls['nonnested_meet_rejected']=str(err)
    else:raise AssertionError('invalid meet accepted')
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));moment=m.geo.moment(stats['movement_profile']);room=(ceiling[0]-moment[1],ceiling[1]-moment[0])
    raw=(json.dumps(w,indent=2)+'\n').encode();pin=hashlib.sha256(raw).hexdigest();(a.out/'WORD.json').write_bytes(raw)
    result={'status':'PASS_ACTUAL_PURE_MEET_FRAME_EXPORT','word_sha256':pin,'parent_word_sha256':PARENT,'native_sha256':b.NATIVE,
     'cut':804,'live_fields':342,'frame_roles':S,'frame_row_hex':hex(h),'source_rank':3,'destination_rank':1,'paid_descent_rank':2,
     'comparison_join_rank':5,'comparison_query_rank':3,'comparison_intersection_rank':1,'old_public_Y_states_unchanged':True,
     'old_pair_carriers_unchanged':True,'original_X_rank':111,'pure_frame_owner_at_meet':owner,'code_C_queries_axes_frame_rank':30,
     'complete_axis_half_bank_rank':64,'frame_outside_complete_axis_half_bank':True,'own_input_fields_inside_facets':[81,86],
     'stats':stats,'moment':b.record(moment),'necessary_limiting_room':b.record(room),'negative_controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'CUT-INVENTORY.json').write_text(json.dumps({'word_sha256':pin,'fields':[{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())]},indent=2)+'\n')
    print(result['status'],pin);print('necessary room',b.record(room)['decimal'][0])

if __name__=='__main__':main()

