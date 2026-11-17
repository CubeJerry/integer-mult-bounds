#!/usr/bin/env python3
"""Actual earlier-axis removal and eight proper one-rank clique deliveries."""
from pathlib import Path
from collections import Counter
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
PARENT='eb49a700e9d815d975120ba56271d414a2a15ee01254c8f5f3203fdfb52c2a59'
NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
SOURCE='37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402'
FRAMES=[([14,17,19,20],[0,2,4,6]),([96,99,101,102],[1,3,5,7])]
def need(x,s):
    if not x:raise ValueError(s)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=BASE/'workers/C/native.json')
    ap.add_argument('--parent',type=Path,default=BASE/'workers/A/parity-receiver-relays/WORD.json')
    ap.add_argument('--source-review',type=Path,default=BASE/'workers/C/proper-query-export-review/check.py')
    ap.add_argument('--arithmetic',type=Path,default=BASE/'workers/C/four-plane-review/check.py')
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for path,pin in[(a.native,NATIVE),(a.parent,PARENT),(a.source_review,SOURCE)]:need(hashlib.sha256(path.read_bytes()).hexdigest()==pin,'source authentication')
    spec=importlib.util.spec_from_file_location('own_positive_source_replay',a.source_review);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.geo=m.load_arithmetic(a.arithmetic)
    R=json.loads(a.native.read_bytes())['native_roots'];parent=json.loads(a.parent.read_bytes());w=json.loads(json.dumps(parent))
    charts={n:m.geo.chart(c)for n,c in w['charts'].items()};ops=[];sem={};new=[];details=[]
    def emit(o,key):sem.setdefault(key,[]).append(len(ops));ops.append(o)
    for k,o in enumerate(parent['operations'][:2021]):
        if k==1921:
            for S,support in FRAMES:
                for i in S:
                    for j in range(8):
                        if j not in support:emit(['ADD',f'AXIS_{j}',f'Y{i}'],'remove_target_axis_at_ground')
        emit(o,'parent_prefix')
    need(len(ops)==2053,'32 actual earlier axis-removal ADDs')
    for k,(S,support)in enumerate(FRAMES):
        tag=f'PARITY_{k}';G=next(q['quartet_chart']for q in parent['construction']['quartets']if q['support']==support)
        row=sum(1<<i for i in S);collector=f'DIAGONAL_CLIQUE_{k}';emit(['INIT',collector,G],'actual_clique_birth');new.append(collector)
        for i in S:emit(['ADD',f'{tag}_RAW{i}',collector],'actual_clique_raw_gather')
        destinations=[]
        for j,i in enumerate(S):
            if j<len(S)-1:
                name=f'DIAGONAL_COPY_{k}_{i}';new.append(name);emit(['INIT',name,G],'actual_clique_copy_birth');emit(['ADD',collector,name],'actual_clique_copy')
            else:name=collector
            T=f'{tag}_T{i}';need(len(charts[G])==4 and len(charts[T])==3 and m.geo.contained(charts[T],charts[G]),'actual unit descent')
            emit(['MOVE',name,T],'proper_diagonal_unit_descent');emit(['ADD',name,f'Y{i}'],'proper_diagonal_actual_add')
            destinations.append({'receiver':i,'chart':T,'owned_field':name,'clique_row_hex':hex(row)})
        details.append({'support':support,'frame':S,'source_chart':G,'clique_row_hex':hex(row),'deliveries':destinations})
    cut=len(ops);need(cut==2091,'actual16-diagonal source cut')
    for o in parent['operations'][2021:]:emit(o,'parent_suffix')
    for name in new:emit(['CLEAR',name],'diagonal_owned_retirement')
    corrections=[int(v,16)for v in parent['Y_correction_rows_hex']]
    for S,_ in FRAMES:
        for i in S:corrections[i]=1<<i
    w['schema']='actual-sixteen-diagonal-values-proper-clique-delivery-v1';w['operations']=ops;w['semantic_operation_indices']=sem
    w['carrier_interface_before_operation']=cut;w['Y_correction_rows_hex']=list(map(hex,corrections))
    w['construction']['parent_word_sha256']=PARENT;w['construction']['sixteen_diagonal_deliveries']=details
    w['scope']='Eight earlier axis-preload removals, actual pure four-root clique gathers from retained raw G4 owners, and eight actual G4 to T3 unit descents complete eight noncoordinate diagonal values in addition to the eight coordinate values. Sixteen completed output values are not16 globally known raw inputs. Remaining95 Y stayground; no full supplier.'
    stats,V,at=m.replay(w,charts,corrections,check_cut=False)
    complete=list(range(8))+[i for S,_ in FRAMES for i in S]
    need(all(V[f'Y{i}']==(1<<(111+i))^(1<<i)for i in complete),'all16 correct arbitrary-Y diagonal values')
    need(sum(V[f'Y{i}']==(1<<(111+i))^(1<<i)for i in range(111))==16,'exactly16 completed diagonal values')
    need(len(V)==424 and stats['cut_owned']==202,'complete actual current field inventory')
    need(stats['counts']=={'INIT':202,'ADD':1476,'MOVE':524,'CLEAR':202},'full primitive invoice')
    need(stats['movement_profile']=={1:195,2:107,3:8,4:111,7:103},'fullclosed movement profile')
    need(stats['owned_downward_profile']=={1:44}and stats['peak_owned']==stats['dirty_CLEAR']==202,'all44 owned unit descents and retirements')
    need(Counter(len(charts[at[f'Y{i}']])for i in range(111))=={0:95,3:8,4:8},'unchanged actual Y positions')
    for group in details:
        row=int(group['clique_row_hex'],16)
        for d in group['deliveries']:need(V[d['owned_field']]==row and at[d['owned_field']]==d['chart'],'actual sameclique packet at each proper target')
    need(all(V[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111)),'all111 original X restored at Hub')
    controls={}
    for key in ['remove_target_axis_at_ground','actual_clique_raw_gather','actual_clique_copy','proper_diagonal_unit_descent','proper_diagonal_actual_add']:
        alt=json.loads(json.dumps(w));ix=sem[key][0];del alt['operations'][ix];alt['carrier_interface_before_operation']-=1
        try:
            _,bv,ba=m.replay(alt,charts,corrections,check_cut=False);need((bv,ba)==(V,at),'all current field values')
        except (ValueError,AssertionError)as e:controls[key]=str(e)
        else:raise ValueError('accepted missing proper delivery '+key)
    alt=json.loads(json.dumps(w));ix=sem['remove_target_axis_at_ground'][0];o=alt['operations'].pop(ix)
    iy=next(i for i,z in enumerate(alt['operations'])if z[:2]==['MOVE',o[2]])
    alt['operations'].insert(iy+1,o)
    try:m.replay(alt,charts,corrections,check_cut=False)
    except (ValueError,AssertionError)as e:controls['late_axis_strip_is_not_a_past_read']=str(e)
    else:raise ValueError('accepted unavailable late ground axis read')
    Q=m.geo.moment(stats['movement_profile']);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in m.geo.moment(gate));a.out.mkdir(parents=True,exist_ok=True)
    raw=(json.dumps(w,indent=2)+'\n').encode();pin=hashlib.sha256(raw).hexdigest();(a.out/'WORD.json').write_bytes(raw)
    result={'status':'PASS_ACTUAL_SIXTEEN_DIAGONAL_VALUES_PENDING_INDEPENDENT_REVIEW','word_sha256':pin,'parent_sha256':PARENT,
      'cut':cut,'live_fields':len(V),'completed_diagonal_roles':complete,'completed_diagonal_count':16,
      'globally_known_raw_coordinates':list(range(8)),'remaining_unknown_output_roles':[i for i in range(111)if i not in complete],
      'remaining_Y_at_ground':95,'pure_clique_packets_at_proper_charts':details,'stats':stats,
      'source_moment':m.record(Q),'necessary_limiting_room':m.record((ceiling[0]-Q[1],ceiling[1]-Q[0])),
      'negative_controls':controls,'scope':w['scope']}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'CUT-INVENTORY.json').write_text(json.dumps({'word_sha256':pin,'cut_before_operation':cut,
      'fields':[{'name':n,'chart':at[n],'rank':len(charts[at[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())]},indent=2)+'\n')
    print(result['status'],pin,'cut2091,all222,16 diagonal values,95 Yground,8 actual added unit descents')

if __name__=='__main__':main()
