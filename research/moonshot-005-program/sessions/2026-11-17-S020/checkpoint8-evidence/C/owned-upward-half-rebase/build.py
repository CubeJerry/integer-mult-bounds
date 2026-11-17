#!/usr/bin/env python3
"""Literal paid upward reuse of an actual exported half field."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
PARENT='91d4a24a995a18ed306b6c657e76e9cac1f14c8077b4143aae94581b50e2eb6e'
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
ARITH='41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'
def need(x,s):
    if not x:raise ValueError(s)
def replay(w,C,expected,g):
    V={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
    P={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
    owners=set();born=set();counts=Counter();moves=Counter();up=Counter();down=Counter();peak=dirty=0;cut=None
    for ix,(op,n,*args)in enumerate(w['operations']):
        if ix==w['carrier_interface_before_operation']:cut=V.copy(),P.copy(),owners.copy()
        counts[op]+=1
        if op=='INIT':
            need(n not in V and n not in born and args[0]in C,'fresh owned zero');born.add(n);owners.add(n);V[n]=0;P[n]=args[0]
        elif op=='ADD':
            d=args[0];need(n in V and d in V and n!=d and C[P[n]]==C[P[d]],'actual cochart ADD');V[d]^=V[n]
            if d.startswith('X'):need(V[d]>>111==0,'no Y in original X')
        elif op=='MOVE':
            need(n in V and args[0]in C,'actual live movement');A,B=C[P[n]],C[args[0]];delta=len(B)-len(A)
            need(delta!=0,'positive movement gap')
            if n in owners:
                need(g.contained(A,B)if delta>0 else g.contained(B,A),'owned nested direction')
                (up if delta>0 else down)[abs(delta)]+=1
            else:need(delta>0 and g.contained(A,B),'monotone public route')
            moves[abs(delta)]+=1;P[n]=args[0]
        elif op=='CLEAR':
            need(n in owners,'only owned retirement');dirty+=bool(V[n]);owners.remove(n);del V[n],P[n]
        else:raise ValueError('unknown primitive')
        peak=max(peak,len(owners))
    need(cut is not None and len(V)==222 and not owners,'closed public endpoints')
    for i in range(111):
        need(V[f'X{i}']==1<<i and P[f'X{i}']=='Hub','raw X Hub endpoint')
        need(V[f'Y{i}']==(1<<(111+i))^expected[i]and P[f'Y{i}']==f'F{i}','all arbitrary Y and actual partial corrections')
    return {'counts':dict(counts),'movement_profile':dict(sorted(moves.items())),'owned_upward_profile':dict(sorted(up.items())),
      'owned_downward_profile':dict(sorted(down.items())),'peak_owned':peak,'dirty_CLEAR':dirty},cut[0],cut[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--parent',type=Path,default=BASE/'workers/A/proper-half-service/WORD.json')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for p,pin in[(a.native,NATIVE),(a.parent,PARENT),(a.arithmetic,ARITH)]:need(hashlib.sha256(p.read_bytes()).hexdigest()==pin,'source authentication')
    s=importlib.util.spec_from_file_location('own_exact_geometry',a.arithmetic);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
    R=json.loads(a.native.read_bytes())['native_roots'];parent=json.loads(a.parent.read_bytes());w=json.loads(json.dumps(parent))
    C={n:g.chart(z)for n,z in w['charts'].items()};D=[int(v,16)for v in parent['Y_correction_rows_hex']]
    ps,pv,pp=replay(parent,C,D,g)
    target,courier,owner=20,96,'HALF_SERVICE_EXPORT_2';T=pp['Y20'];H=pp['Y96'];P=pp[owner]
    need(P=='HALF_SERVICE_P2'and H=='HALF_SERVICE_J3'and len(C[P])==2 and len(C[H])==4,'actual lower export and raised courier')
    need(g.contained(C[P],C[H]),'owned upward path really nested')
    J='UPWARD_HALF_REBASE_J';w['charts'][J]={'kind':'span','rows':w['charts'][T]['rows']+w['charts'][H]['rows']};C[J]=g.chart(w['charts'][J])
    need(len(C[J])==6 and g.contained(C[J],C['F20'])and g.contained(C[J],C['F96']),'actual common rank6 rendezvous')
    half=pv[owner];p20=D[20]&~255;p96=(D[96]&~255)^half
    need(p20.bit_count()==p96.bit_count()==3 and half.bit_count()==4,'actual previously acquired correction rows')
    N=[sum(1<<j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0)for i in range(111)]
    need(not(p20&~N[96])and not(p96&~N[20]),'exchanged three-term sums native to receiving destinations')
    need(half&~N[20]!=0,'the actual half must be removed before it reaches receiver20')
    ops=[];sem={}
    def emit(o,key):sem.setdefault(key,[]).append(len(ops));ops.append(o)
    for ix,o in enumerate(parent['operations'][:2089]):
        if ix==1921:
            emit(['ADD','Y20','Y96'],'earlier_inverse');emit(['ADD','Y96','Y20'],'earlier_inverse')
        emit(o,'parent_prefix')
    emit(['MOVE',owner,H],'paid_owned_upward_rebase');emit(['ADD',owner,'Y96'],'remove_actual_half_at_courier')
    emit(['MOVE','Y20',J],'target_rank6_arrival');emit(['MOVE','Y96',J],'courier_rank6_arrival')
    emit(['ADD','Y96','Y20'],'cross_parity_forward');emit(['ADD','Y20','Y96'],'native_courier_cleanup')
    cut=len(ops);need(cut==2097,'actual new cut')
    for o in parent['operations'][2089:]:emit(o,'parent_suffix')
    expected=D.copy();expected[20]=(D[20]&255)^p20^p96;expected[96]=(D[96]&255)^p20
    w['schema']='paid-owned-upward-half-rebase-and-cross-parity-exchange-v1';w['operations']=ops;w['semantic_operation_indices']=sem
    w['carrier_interface_before_operation']=cut;w['Y_correction_rows_hex']=list(map(hex,expected))
    w['construction']['parent_word_sha256']=PARENT;w['construction']['owned_upward_half_rebase']={
      'target':20,'courier':96,'actual_export_owner':owner,'initial_export_chart':P,'courier_chart':H,'rendezvous_chart':J,
      'actual_half_hex':hex(half),'target_prior_parity_hex':hex(p20),'courier_prior_parity_hex':hex(p96),'inverse_before_parent_operation':1921}
    w['scope']='One explicit paid owned ascent2→4 reuses an actual exported half to remove its term from a raised courier. Two public records then meet at6 and exchange native parity information using an earlier two-ADD ground inverse. Zero added descents;8 complete axis values only; no cost dominance or full supplier.'
    stats,V,at=replay(w,C,expected,g)
    ev=pv.copy();ep=pp.copy();ev['Y20']=(1<<131)^expected[20];ev['Y96']=(1<<207)^expected[96]
    ep['Y20']=ep['Y96']=J;ep[owner]=H;need((V,at)==(ev,ep)and len(V)==420,'all420 exact current fields')
    need(stats['counts']=={'INIT':198,'ADD':1466,'MOVE':544,'CLEAR':198},'literal complete invoice')
    need(stats['movement_profile']=={1:200,2:123,3:22,4:103,7:96},'full endpoint-inclusive profile')
    need(stats['owned_upward_profile']=={2:1}and stats['owned_downward_profile']=={1:40},'one actual ascent, no added descent')
    need(sum(z.bit_count()for z in expected[8:])==484,'actual changed foreign count; no dominance claim')
    need(all(not(expected[i]&~N[i])for i in range(8,111)),'all unfinished target corrections native')
    controls={}
    for key in ['earlier_inverse','paid_owned_upward_rebase','remove_actual_half_at_courier','cross_parity_forward','native_courier_cleanup']:
        alt=json.loads(json.dumps(w));ix=sem[key][0];del alt['operations'][ix];alt['carrier_interface_before_operation']-=1
        try:
            _,bv,bp=replay(alt,C,expected,g);need((bv,bp)==(V,at),'all cut fields')
        except(ValueError,AssertionError)as e:controls[key]=str(e)
        else:raise ValueError('missing paid rebase operation accepted')
    from decimal import Decimal,localcontext
    def record(pair):
        with localcontext()as ctx:
            ctx.prec=55;return {'rational':list(map(str,pair)),'decimal':[str(Decimal(x.numerator)/Decimal(x.denominator))for x in pair]}
    Q=g.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(x/6 for x in g.moment(gate));delta=g.moment({1:2,2:2,4:-1});a.out.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(w,indent=2)+'\n').encode();pin=hashlib.sha256(raw).hexdigest();(a.out/'WORD.json').write_bytes(raw)
    result={'status':'PASS_LITERAL_OWNED_UPWARD_HALF_REBASE_PENDING_INDEPENDENT_REVIEW','word_sha256':pin,'parent_sha256':PARENT,
      'cut':cut,'live_fields':420,'stats':stats,'new_receiver20_native_terms':6,'courier96_native_terms':3,'total_foreign_terms':484,
      'completed_diagonal_values':8,'actual_reused_half_field':owner,'owned_ascent_gap':2,'additional_owned_descents':0,
      'moment':record(Q),'necessary_limiting_room':record((ceiling[0]-Q[1],ceiling[1]-Q[0])),
      'movement_cost_added':record(delta),'negative_controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'CUT-INVENTORY.json').write_text(json.dumps({'word_sha256':pin,'cut_before_operation':cut,'fields':[
      {'name':n,'chart':at[n],'rank':len(C[at[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())]},indent=2)+'\n')
    print(result['status'],pin,'one owned ascent,all222/420,5controls,room',record((ceiling[0]-Q[1],ceiling[1]-Q[0]))['decimal'][0])
if __name__=='__main__':main()
