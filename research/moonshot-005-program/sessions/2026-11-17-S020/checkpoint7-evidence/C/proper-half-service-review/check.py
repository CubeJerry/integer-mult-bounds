#!/usr/bin/env python3
"""Independent literal shared-export and arbitrary-baseline service review."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'word':'91d4a24a995a18ed306b6c657e76e9cac1f14c8077b4143aae94581b50e2eb6e',
 'parent':'eb49a700e9d815d975120ba56271d414a2a15ee01254c8f5f3203fdfb52c2a59',
 'source_review':'37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402',
 'arithmetic':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'}
PLAN=[(14,97,'HALF_4_1',[42,45]),(17,98,'HALF_2_2',[23,26]),(19,100,'HALF_2_2',[23,26]),
 (96,15,'HALF_9_1',[77,80]),(99,16,'HALF_9_1',[77,80]),(101,18,'HALF_9_0',[74,75]),(102,21,'HALF_9_0',[74,75])]
def need(x,s):
    if not x:raise ValueError(s)
def module(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def formal_identity():
    # independent baselines b_i,b_k, later native correction D and half payload R
    i,k,D,R=1,2,4,8;k^=i;i^=k
    prepared=[i,k];i^=D;k^=R;i^=k;k^=i
    need([i,k]==[1^4^8,2^4],'two complete arbitrary baselines restored')
    return {'columns':['b_i','b_k','D','R'],'prepared_rows':prepared,'final_rows':[i,k]}
def main():
    ap=argparse.ArgumentParser()
    defaults={'native':'workers/C/native.json','word':'workers/A/proper-half-service/WORD.json',
      'parent':'workers/A/parity-receiver-relays/WORD.json','source_review':'workers/C/proper-query-export-review/check.py',
      'arithmetic':'workers/C/four-plane-review/check.py'}
    for k,p in defaults.items():ap.add_argument('--'+k.replace('_','-'),type=Path,default=BASE/p)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for k,pin in PINS.items():need(hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==pin,'authenticated '+k)
    R=json.loads(a.native.read_bytes())['native_roots'];w=json.loads(a.word.read_bytes());parent=json.loads(a.parent.read_bytes())
    m=module(a.source_review,'independent_shared_half_source');m.geo=m.load_arithmetic(a.arithmetic);g=m.geo
    C={n:g.chart(z)for n,z in w['charts'].items()};PC={n:g.chart(z)for n,z in parent['charts'].items()}
    need(all(C[n]==v for n,v in PC.items()),'parent real charts unchanged')
    D=[int(x,16)for x in parent['Y_correction_rows_hex']];ps,pv,pp=m.replay(parent,PC,D,check_cut=False)
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    exports={};services=[];expected=D.copy();need(len({i for i,k,h,P in PLAN}|{k for i,k,h,P in PLAN})==14,'all seven pairs disjoint')
    for serial,(i,k,h,plane_roles)in enumerate(PLAN):
        row=pv[h];H=pp[h];T=pp[f'Y{i}'];key=(h,tuple(plane_roles))
        need(len(C[H])==3 and row.bit_count()==4,'actual four-input proper half')
        if key not in exports:
            n=len(exports);P=f'HALF_SERVICE_P{n}';owner=f'HALF_SERVICE_EXPORT_{n}'
            need(C[P]==g.basis(tuple(tuple(R[j])for j in plane_roles))and len(C[P])==2,'actual export plane from native roots')
            need(g.contained(C[P],C[H]),'one real rank descent')
            exports[key]={'source':h,'H':H,'P':P,'owner':owner,'row':row,'plane_roles':plane_roles}
        e=exports[key];P=e['P'];J=f'HALF_SERVICE_J{serial}'
        need(C[J]==g.basis(C[T]+C[P])and len(C[J])==4 and len(C[T])==3,'exact receiver/courier joint plane')
        need(g.contained(C[J],C[f'F{i}'])and g.contained(C[J],C[f'F{k}'])and pp[f'Y{k}']=='zero','both actual upward public routes')
        parity=D[i]&~255;need(parity.bit_count()==3,'existing three-neighbour correction')
        need(row&~N[i]==0 and parity&~N[k]==0 and row&~N[k]!=0,'target native half, courier native parity, real unwanted half terms')
        expected[i]^=row;expected[k]^=parity
        services.append({'target':i,'courier':k,'H':H,'T':T,'P':P,'J':J,'owner':e['owner'],'half':row,'parity':parity})
    need(len(exports)==4,'four physically shared export fields')
    ops=[];events={}
    def emit(o,key):events.setdefault(key,[]).append(len(ops));ops.append(o)
    for ix,o in enumerate(parent['operations'][:2021]):
        if ix==1921:
            for z in reversed(services):
                emit(['ADD',f"Y{z['target']}",f"Y{z['courier']}"],'earlier_inverse')
                emit(['ADD',f"Y{z['courier']}",f"Y{z['target']}"],'earlier_inverse')
        emit(o,'parent')
    for e in exports.values():
        emit(['INIT',e['owner'],e['H']],'export_birth');emit(['ADD',e['source'],e['owner']],'actual_half_capture')
        emit(['MOVE',e['owner'],e['P']],'actual_half_descent')
    for z in services:
        i,k=z['target'],z['courier']
        emit(['MOVE',f'Y{k}',z['P']],'courier_pair_arrival');emit(['ADD',z['owner'],f'Y{k}'],'actual_half_read')
        emit(['MOVE',f'Y{k}',z['J']],'courier_joint_arrival');emit(['MOVE',f'Y{i}',z['J']],'target_joint_arrival')
        emit(['ADD',f'Y{k}',f'Y{i}'],'target_half_delivery');emit(['ADD',f'Y{i}',f'Y{k}'],'courier_garbage_cancellation')
    need(len(ops)==2089,'actual new cut')
    for o in parent['operations'][2021:]:emit(o,'parent_suffix')
    for e in exports.values():emit(['CLEAR',e['owner']],'export_retirement')
    need(w['operations']==ops,'complete literal extension independently reconstructed')
    need(w['carrier_interface_before_operation']==2089 and w['Y_correction_rows_hex']==list(map(hex,expected)),'exact new interface')
    stats,V,P=m.replay(w,C,expected,check_cut=False)
    ev=pv.copy();ep=pp.copy()
    for e in exports.values():ev[e['owner']]=e['row'];ep[e['owner']]=e['P']
    for z in services:
        i,k=z['target'],z['courier'];ev[f'Y{i}']=(1<<(111+i))^expected[i];ev[f'Y{k}']=(1<<(111+k))^expected[k]
        ep[f'Y{i}']=ep[f'Y{k}']=z['J']
    need((V,P)==(ev,ep)and len(V)==420,'complete420-field inventory')
    need(all(expected[i]&~N[i]==0 for i in range(8,111)),'all output corrections native; courier garbage really removed')
    need(sum(v.bit_count()for v in expected[8:])==485,'49 actual additional foreign coefficients')
    need(stats['counts']=={'INIT':198,'ADD':1461,'MOVE':541,'CLEAR':198},'full primitive invoice')
    need(stats['movement_profile']=={1:198,2:121,3:22,4:104,7:96},'closed movement profile')
    need(stats['owned_downward_profile']=={1:40}and stats['peak_owned']==stats['dirty_CLEAR']==198,'four added owned descents and explicit retirement')
    need(Counter(len(C[P[f'Y{i}']])for i in range(111))=={0:88,3:1,4:22},'actual Y locations')
    controls={}
    for key in ['earlier_inverse','actual_half_capture','actual_half_descent','actual_half_read','target_half_delivery','courier_garbage_cancellation']:
        alt=json.loads(json.dumps(w));ix=events[key][0];del alt['operations'][ix];alt['carrier_interface_before_operation']-=1
        try:
            _,bv,bp=m.replay(alt,C,expected,check_cut=False);need((bv,bp)==(V,P),'whole current state')
        except(ValueError,AssertionError)as e:controls[key]=str(e)
        else:raise ValueError('missing indispensable operation accepted '+key)
    alt=json.loads(json.dumps(w));ix=events['earlier_inverse'][0];o=alt['operations'].pop(ix)
    ix=next(j for j,z in enumerate(alt['operations'])if z[:2]==['MOVE',o[1]]);alt['operations'].insert(ix+1,o)
    try:m.replay(alt,C,expected,check_cut=False)
    except(ValueError,AssertionError)as e:controls['late_ground_inverse']=str(e)
    else:raise ValueError('late inverse accepted')
    xmask=((1<<111)-1)^255;leaks=[];conditioned=0
    for e in exports.values():conditioned|=e['row']
    conditioned_checks=[]
    for i in range(8,111):
        inside=[n for n in V if g.contained(C[P[n]],C[f'F{i}'])]
        for n in inside:
            if V[n]&xmask&~N[i]:leaks.append({'receiver':i,'field':n,'forbidden_mask_hex':hex(V[n]&xmask&~N[i])})
        need(all(V[n]&xmask&~conditioned&~N[i]==0 for n in inside),'locality after explicit16-input conditioning')
        conditioned_checks.append({'receiver':i,'inside_fields':len(inside)})
    possible_nonnative={e['owner']for e in exports.values()}|{f"Y{z['target']}"for z in services}
    need(conditioned.bit_count()==16 and leaks and all(z['field']in possible_nonnative for z in leaks),'new nonlocal source facts explicit')
    Q=g.moment(stats['movement_profile']);QP=g.moment(ps['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in g.moment(gate));delta={1:11,2:14,3:14,4:-7,7:-7}
    need(all(stats['movement_profile'].get(k,0)-ps['movement_profile'].get(k,0)==delta.get(k,0)for k in set(stats['movement_profile'])|set(ps['movement_profile'])),'exact changed endpoint pricing')
    result={'status':'PASS_INDEPENDENT_ACTUAL_SHARED_HALF_SERVICE','pins':PINS,'cut':2089,'all222':True,'all420_fields':True,
      'formal_four_column_identity':formal_identity(),'independent_plan':PLAN,'pure_export_count':4,'receiver_courier_pairs':7,
      'new_target_foreign_terms':28,'new_courier_foreign_terms':21,'total_foreign_terms':485,'completed_diagonal_values':8,
      'stats':stats,'profile_delta':delta,'movement_cost_added':m.record((Q[0]-QP[1],Q[1]-QP[0])),
      'moment':m.record(Q),'necessary_limiting_room':m.record((ceiling[0]-Q[1],ceiling[1]-Q[0])),
      'explicit_nonnative_export_leaks':leaks,'conditioning_roles':[i for i in range(111)if conditioned>>i&1],
      'conditioned_locality_checks':conditioned_checks,'negative_controls':controls,
      'scope':'Actual four shared proper exports and seven public-Y deliveries with complete arbitrary-baseline cancellation. Whole-width characteristic-two source identity. Pure exported owners remain nonnative inside some facets, so no prior entropy graph is inherited unchanged.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())],indent=2)+'\n')
    print(result['status'],'all222/420,wholeword,7controls,nonlocal export incidences',len(leaks))
if __name__=='__main__':main()
