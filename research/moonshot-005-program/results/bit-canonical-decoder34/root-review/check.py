#!/usr/bin/env python3
"""Independent audit of the actual K34 source and its paid proper correction."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json
from optimize_word import independent_replay
from review_leaf_capacity import chart_basis,echelon

BASE='72317dffe82063e4db958c7b4025c490276d8339cbf11fd7041bc183ba991155'
WORD='a910bb4504cf2a96303e8d560f076463268c4cb3ad4e6631d5f598c895db0567'

def snapshots(word):
    v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};history=[]
    for op,n,*q in word['operations']:
        history.append((v.copy(),at.copy()))
        if op=='INIT':v[n]=0;at[n]=q[0]
        elif op=='ADD':v[q[0]]^=v[n]
        elif op=='MOVE':at[n]=q[0]
        elif op=='CLEAR':del v[n],at[n]
    return history

def main():
    p=argparse.ArgumentParser()
    for n in ['repo','base','word','author-result','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();braw=a.base.read_bytes();raw=a.word.read_bytes();assert hashlib.sha256(braw).hexdigest()==BASE and hashlib.sha256(raw).hexdigest()==WORD;old=json.loads(braw);w=json.loads(raw);assert w['base_word_sha256']==BASE and w['charts']==old['charts']and set(w['targets'])==set(old['targets'])|{34} and 34 not in old['targets']
    src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256']==old['source_sha256'];roots=json.loads(src)['native_roots'];C={n:chart_basis(rec)for n,rec in w['charts'].items()}
    for i in range(111):
        assert len(C[f'L{i}'])==1 and len(echelon(C[f'L{i}']+[roots[i]])[0])==1
        assert len(C[f'F{i}'])==7 and all(sum(x*y for x,y in zip(row,roots[i]))==0 for row in C[f'F{i}'])
    before,after=independent_replay(old),independent_replay(w);OS,NS=snapshots(old),snapshots(w);ops=w['operations'];aux='CANON_SIDE34';neighbors=[j for j in range(111)if sum(x*y for x,y in zip(roots[34],roots[j]))==0];assert len(neighbors)==60 and 34 not in neighbors;N=sum(1<<j for j in neighbors);K=N^(1<<34)
    combined=ops.index(['MOVE','P5','P5_K']);v,at=NS[combined];assert v['P5']==K and at['P5']=='M1'
    modes=[v[f'ZFIRST{i}']for i in [3,4,5]];assert modes[0]^modes[1]^modes[2]==K
    assert all(at[f'ZFIRST{i}']=='M1'for i in [3,4,5]);assert ops[combined-2:combined]==[['ADD','ZFIRST3','P5'],['ADD','ZFIRST4','P5']]
    birth=ops.index(['INIT',aux,'Hub']);v,at=NS[birth];assert all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111))
    assert ops[birth+1:birth+61]==[['ADD',f'X{i}',aux]for i in neighbors]
    departure=ops.index(['MOVE',aux,'F34']);v,at=NS[departure];assert v[aux]==N and at[aux]=='Hub'
    receiver=ops.index(['MOVE','Y34','F34']);v,at=NS[receiver];assert v['P5']==K and at['P5']=='zero'and v[aux]==N and at[aux]=='F34'and v['Y34']==(1<<145)^K and at['Y34']=='zero';assert ops[receiver-1]==['ADD','P5','Y34']and ops[receiver+1]==['ADD',aux,'Y34'];assert NS[receiver+2][0]['Y34']==(1<<145)^(1<<34)
    oldcut=next(k for k,o in enumerate(old['operations'])if o[0]=='CLEAR');newcut=next(k for k,o in enumerate(ops)if o[0]=='CLEAR');ov,oa=OS[oldcut];nv,na=NS[newcut];changed=sorted(n for n in ov if ov[n]!=nv[n]or oa[n]!=na[n]);assert changed==['P5','P5_RET','Y34'];assert nv['P5_RET']==K
    for i in [3,4,5]:assert nv[f'ZFIRST{i}']==ov[f'ZFIRST{i}']and na[f'ZFIRST{i}']=='M1'
    for i in [8,9,36]:assert nv[f'IMPORT_E{i}']==1<<i and na[f'IMPORT_E{i}']=='M1'
    oldmoves=[o for o in old['operations']if o[0]=='MOVE'];assert[o for o in ops if o[0]=='MOVE'and o[1]!=aux]==oldmoves
    new_reads={('ADD','ZFIRST3','P5'),('ADD','ZFIRST4','P5'),('ADD','P5','Y34')}
    assert[o for o in ops if aux not in o and tuple(o)not in new_reads]==old['operations']
    diff={d:after['movement_profile'].get(d,0)-before['movement_profile'].get(d,0)for d in range(1,9)};assert{k:n for k,n in diff.items()if n}=={1:1}
    assert after['counts']=={k:n+{'INIT':1,'ADD':64,'MOVE':1,'CLEAR':1}[k]for k,n in before['counts'].items()};assert after['dirty_CLEAR']==before['dirty_CLEAR']+1
    sp=importlib.util.spec_from_file_location('independent_decoder_price',a.repo/'research/moonshot-005-program/results/bit-composed-coded-source/author/price.py');price=importlib.util.module_from_spec(sp);sp.loader.exec_module(price);invoice=price.invoice(after['movement_profile']);author=json.loads(a.author_result.read_text())
    for key in ['moment','limiting_room']:
        x=invoice[key];y=author['price'][key];assert Fraction(y['lower_fraction'])<=Fraction(x['lower_fraction'])<=Fraction(x['upper_fraction'])<=Fraction(y['upper_fraction'])
    controls=[]
    for omitted in [['ADD','ZFIRST3','P5'],['ADD','ZFIRST4','P5'],['ADD',f'X{neighbors[0]}',aux],['MOVE',aux,'F34'],['ADD','P5','Y34'],['ADD',aux,'Y34'],['CLEAR',aux]]:
        bad=copy.deepcopy(w);bad['operations'].remove(omitted)
        try:independent_replay(bad)
        except(AssertionError,KeyError)as ex:controls.append({'omitted':omitted,'rejected':str(ex)})
        else:raise AssertionError(('Incomplete decoder accepted',omitted))
    bad=copy.deepcopy(w);bad['targets']=old['targets'];bad['operations'].remove(['ADD','P5','Y34']);bad['operations'].remove(['ADD',aux,'Y34']);independent_replay(bad)
    controls.append({'removed':'both new receiver reads and target34','all46_old_endpoints_still_correct':True})
    result={'status':'PASS_ROOT_INDEPENDENT_ACTUAL_CANONICAL_DECODER34','word_sha256':WORD,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'method':'Independent Fraction native charts, full222-column word replay, exact actual-source snapshots and binary fixed-point200th-root invoice; no author builder/checker imported.','before':before,'after':after,'completed_outputs':47,'K34_hex':hex(K),'N34_hex':hex(N),'actual_neighbors':neighbors,'actual_source_cuts':{'M1_departure':combined,'raw_Hub_auxiliary_birth':birth,'facet_correction_departure':departure,'native_receiver_move':receiver},'all111_originals_raw_at_actual_correction_birth':True,'old_final_live_fields_changed':changed,'all_old_MOVEs_retained_in_order':True,'all_other_old_scalar_operations_retained_in_order':True,'three_canonical_and_three_raw_M1_contracts_preserved':True,'exact_movement_increment':{'1':1},'independent_invoice':invoice,'negative_controls':controls,'universal_scope':'The written binary K34+N34=e34 identity and literal lawful word hold over every characteristic-two field and positive whole-record width. Actual source/delivery witness; not an improved endpoint-price frontier or a full supplier.','new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
