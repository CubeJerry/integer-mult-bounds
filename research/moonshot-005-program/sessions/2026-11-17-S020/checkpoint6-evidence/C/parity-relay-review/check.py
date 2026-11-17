#!/usr/bin/env python3
"""Independent literal-word and eight-baseline proof of public-Y parity relays."""
from pathlib import Path
from collections import Counter
from itertools import combinations
import argparse,hashlib,importlib.util,json

BASE=Path('/workspace/scratch/2a62370e4336')
PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'word':'eb49a700e9d815d975120ba56271d414a2a15ee01254c8f5f3203fdfb52c2a59',
 'parent':'6f1bd8465c7a4fa5b7b59888fb5dbd9bbbb88dc3306c984bd71497fd4be7d980',
 'source_review':'37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402',
 'arithmetic':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565'}
SPECS=[([0,2,4,6],[14,17,19,20],[1,3,5,7]),([1,3,5,7],[96,99,101,102],[0,2,4,6])]

def need(ok,why):
    if not ok:raise ValueError(why)

def load(path,name):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def local_algebra():
    # Formal baselines b_a,b_b,b_c,b_d,b_ha,b_hb,b_hc,b_hd and four new
    # independent source inputs. No ground baseline is assumed zero or pureY.
    v=[1<<i for i in range(8)];x=[1<<(8+i)for i in range(4)]
    forward=[(0,2),(1,3),(4,0),(5,1),(6,2),(7,3)]
    for s,t in reversed(forward):v[t]^=v[s]
    prepared=v.copy()
    for i,j in enumerate([1,0,3,2]):v[i]^=x[j]
    v[2]^=v[0];v[3]^=v[1]
    for h,term in [(4,x[2]^x[3]),(5,x[2]^x[3]),(6,x[0]),(7,x[1])]:v[h]^=term
    for h,t in [(4,0),(5,1),(6,2),(7,3)]:v[t]^=v[h]
    for h,term in [(4,x[2]^x[3]),(5,x[2]^x[3]),(6,x[0]),(7,x[1])]:v[h]^=term
    wanted=[(1<<i)^sum(x[j]for j in range(4)if j!=i)for i in range(4)]+[1<<i for i in range(4,8)]
    need(v==wanted,'formal8-baseline and4-source exact identity')
    return {'initial_baseline_count':8,'independent_source_count':4,'ground_preconditioned_rows_hex':list(map(hex,prepared)),
            'final_rows_hex':list(map(hex,v)),'six_ADD_inverse_order':[list(z)for z in reversed(forward)]}

def main():
    ap=argparse.ArgumentParser()
    defaults={'native':'workers/C/native.json','word':'workers/A/parity-receiver-relays/WORD.json',
      'parent':'workers/A/full-half-reservoir/WORD.json','source_review':'workers/C/proper-query-export-review/check.py',
      'arithmetic':'workers/C/four-plane-review/check.py'}
    for k,p in defaults.items():ap.add_argument('--'+k.replace('_','-'),type=Path,default=BASE/p)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for k,pin in PINS.items():need(hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==pin,'authenticated '+k)
    R=json.loads(a.native.read_bytes())['native_roots'];w=json.loads(a.word.read_bytes());parent=json.loads(a.parent.read_bytes())
    m=load(a.source_review,'independent_parity_source');m.geo=m.load_arithmetic(a.arithmetic);g=m.geo
    C={n:g.chart(z)for n,z in w['charts'].items()};PC={n:g.chart(z)for n,z in parent['charts'].items()}
    need(all(C[n]==v for n,v in PC.items()),'all parent chart geometry unchanged')
    N=[sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(r,s))==0)for r in R]
    target=[1<<i if i<8 else N[i]&255 for i in range(111)]
    expected_ops=[];extra=[];insert={};configs=[];events={}
    def emit(op,key='parent'):
        events.setdefault(key,[]).append(len(expected_ops));expected_ops.append(op)
    first_hub=next(i for i,o in enumerate(parent['operations'])if o[0]=='MOVE'and o[1].startswith('X')and o[2]=='Hub')
    cleanup=[]
    for k,(support,S,helpers)in enumerate(SPECS):
        aa,bb,cc,dd=S;tag=f'PARITY_{k}'
        need(all(sum(x*y for x,y in zip(R[i],R[j]))==0 for i,j in combinations(S,2)),'actual orthogonal frame')
        need(all([j for j,x in enumerate(R[i])if x]==support for i in S),'frame coordinate support')
        G=next(q['quartet_chart']for q in parent['construction']['quartets']if q['support']==support)
        pair={'cd':tag+'_CD','bd':tag+'_BD','ac':tag+'_AC'};T={i:tag+'_T'+str(i)for i in S}
        for name,I in [(pair['cd'],[cc,dd]),(pair['bd'],[bb,dd]),(pair['ac'],[aa,cc])]:
            need(C[name]==g.basis(tuple(tuple(R[i])for i in I))and len(C[name])==2,'actual orthogonal pair chart')
        for i,P in T.items():
            need(C[P]==g.basis(tuple(tuple(R[j])for j in S if j!=i))and len(C[P])==3,'actual three-neighbour chart')
            need(g.contained(C[P],C[f'F{i}']),'target can finish monotonically')
            target[i]^=sum(1<<j for j in S if j!=i)
        need(all(g.contained(C[G],C[f'F{i}'])for i in helpers),'all four axis helpers can finish from G')
        po=tag+'_PAIR_SOURCE';raw={i:tag+'_RAW'+str(i)for i in S};extra.append(po);extra+=list(raw.values())
        ix=min(i for i,o in enumerate(parent['operations'][:1893])if o[0]=='MOVE'and o[1]in[f'X{cc}',f'X{dd}'])
        insert[ix]=[(['MOVE',f'X{cc}',pair['cd']],'pair_arrival'),(['MOVE',f'X{dd}',pair['cd']],'pair_arrival'),
          (['ADD',f'X{dd}',f'X{cc}'],'pair_encode'),(['INIT',po,pair['cd']],'pair_birth'),
          (['ADD',f'X{cc}',po],'pair_capture'),(['ADD',f'X{dd}',f'X{cc}'],'pair_inverse')]
        for i in S:cleanup += [(['INIT',raw[i],G],'cleanup_birth'),(['ADD',f'X{i}',raw[i]],'cleanup_capture')]
        configs.append((S,helpers,G,pair,T,po,raw))
    for ix,o in enumerate(parent['operations'][:1893]):
        for z,key in insert.get(ix,[]):emit(z,key)
        if ix==first_hub:
            for z,key in cleanup:emit(z,key)
        emit(o)
    need(len(expected_ops)==1921,'actual augmented-reservoir stage')
    for S,H,G,P,T,po,raw in configs:
        aa,bb,cc,dd=S;ha,hb,hc,hd=H
        for s,t in [(hd,dd),(hc,cc),(hb,bb),(ha,aa),(bb,dd),(aa,cc)]:emit(['ADD',f'Y{s}',f'Y{t}'],'ground_inverse')
        for i,j in [(aa,bb),(bb,aa),(cc,dd),(dd,cc)]:
            emit(['MOVE',f'Y{i}',f'L{j}'],'target_native_arrival');emit(['ADD',f'NATIVE_{j}',f'Y{i}'],'target_native_read')
        for i in [aa,cc]:emit(['MOVE',f'Y{i}',P['bd']],'target_pair_arrival')
        emit(['ADD',f'Y{aa}',f'Y{cc}'],'target_pair_forward')
        for i in [bb,dd]:emit(['MOVE',f'Y{i}',P['ac']],'target_pair_arrival')
        emit(['ADD',f'Y{bb}',f'Y{dd}'],'target_pair_forward')
        for i in S:emit(['MOVE',f'Y{i}',T[i]],'target_triple_arrival')
        for h,i in [(ha,aa),(hb,bb)]:
            emit(['MOVE',f'Y{h}',P['cd']],'helper_pair_arrival');emit(['ADD',po,f'Y{h}'],'helper_pair_read')
            emit(['MOVE',f'Y{h}',T[i]],'helper_triple_arrival');emit(['ADD',f'Y{h}',f'Y{i}'],'helper_forward')
        for h,i,j in [(hc,cc,aa),(hd,dd,bb)]:
            emit(['MOVE',f'Y{h}',f'L{j}'],'helper_native_arrival');emit(['ADD',f'NATIVE_{j}',f'Y{h}'],'helper_native_read')
            emit(['MOVE',f'Y{h}',T[i]],'helper_triple_arrival');emit(['ADD',f'Y{h}',f'Y{i}'],'helper_forward')
        for h,J in [(ha,[cc,dd]),(hb,[cc,dd]),(hc,[aa]),(hd,[bb])]:
            emit(['MOVE',f'Y{h}',G],'helper_cleanup_arrival')
            for j in J:emit(['ADD',raw[j],f'Y{h}'],'helper_cleanup')
    need(len(expected_ops)==2021,'exact new cut')
    for o in parent['operations'][1893:]:emit(o)
    extra=[z[5]for z in configs]+[n for z in configs for n in z[6].values()]
    for name in extra:emit(['CLEAR',name],'added_retirement')
    need(w['operations']==expected_ops,'whole literal source/delivery/suffix word independently reconstructed')
    need(w['carrier_interface_before_operation']==2021 and w['Y_correction_rows_hex']==list(map(hex,target)),'actual cut and independent target map')
    stats,V,at=m.replay(w,C,target,check_cut=False)
    need(stats['counts']=={'INIT':194,'ADD':1422,'MOVE':516,'CLEAR':194},'complete primitive invoice')
    need(stats['movement_profile']=={1:187,2:107,3:8,4:111,7:103},'actual full route profile')
    need(stats['owned_downward_profile']=={1:36}and stats['dirty_CLEAR']==stats['peak_owned']==194,'no added owned MOVE, all retirements')
    pstats,pv,pa=m.replay(parent,PC,[int(x,16)for x in parent['Y_correction_rows_hex']],check_cut=False)
    expV=pv.copy();expA=pa.copy()
    for S,H,G,P,T,po,raw in configs:
        cc,dd=S[2:];expV[po]=(1<<cc)^(1<<dd);expA[po]=P['cd']
        for i,name in raw.items():expV[name]=1<<i;expA[name]=G
        for i in S:expV[f'Y{i}']=(1<<(111+i))^target[i];expA[f'Y{i}']=T[i]
        for i in H:expA[f'Y{i}']=G
    need((V,at)==(expV,expA)and len(V)==416,'all416 independently expected cut fields')
    need(Counter(len(C[at[f'Y{i}']])for i in range(111))=={0:95,3:8,4:8},'actual public Y geography')
    need(sum(v.bit_count()for v in target[8:])==436,'all436 foreign coefficients')
    xmask=(1<<111)-1;inside_counts=[]
    for i in range(8,111):
        inside=[name for name in V if g.contained(C[at[name]],C[f'F{i}'])]
        need(all(V[n]&xmask&~255&~N[i]==0 for n in inside),'all inside unknown information remains native-local')
        inside_counts.append(len(inside))
    controls={}
    for key in ['pair_capture','pair_inverse','cleanup_capture','ground_inverse','target_native_read','target_pair_forward',
                'helper_pair_read','helper_native_read','helper_forward','helper_cleanup']:
        k=events[key][0];alt=json.loads(json.dumps(w));del alt['operations'][k];alt['carrier_interface_before_operation']-=1
        try:
            _,bv,ba=m.replay(alt,C,target,check_cut=False);need((bv,ba)==(V,at),'complete cut')
        except (ValueError,AssertionError)as e:controls[key]=str(e)
        else:raise ValueError('accepted omitted essential relay '+key)
    profile=stats['movement_profile'];Q=g.moment(profile);QP=g.moment(pstats['movement_profile'])
    delta={1:48,2:4,3:8,4:8,7:-16};need(all(profile.get(k,0)-pstats['movement_profile'].get(k,0)==delta.get(k,0)for k in set(profile)|set(pstats['movement_profile'])),'independent route delta')
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in g.moment(gate));room=(ceiling[0]-Q[1],ceiling[1]-Q[0])
    result={'status':'PASS_INDEPENDENT_ACTUAL_PUBLIC_Y_PARITY_RELAYS','pins':PINS,'source_cut':2021,'augmented_source_cut':1921,
      'whole_literal_word_reconstructed':True,'all222_columns':True,'all416_cut_fields':True,'local_formal_algebra':local_algebra(),
      'frames':SPECS,'new_corrected_targets':8,'new_foreign_coefficients':24,'total_foreign_coefficients':436,
      'completed_diagonal_values':8,'helpers_restored_to_actual_correct_coordinate_baseline':True,'stats':stats,
      'parent_to_new_profile_delta':delta,'additional_movement_cost':m.record((Q[0]-QP[1],Q[1]-QP[0])),
      'source_moment':m.record(Q),'necessary_limiting_room':m.record(room),'all103_facet_locality_inside_counts':inside_counts,
      'negative_controls':controls,'scope':'Two literal forward-only public-Y correction modules with exact ground preconditioning and actual raw cleanup. Every characteristic-two field and positive block width. Eight new three-neighbour corrections; no new completed diagonal outputs or full supplier.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    (a.out/'INDEPENDENT-CUT.json').write_text(json.dumps([{'name':n,'chart':at[n],'rank':len(C[at[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())],indent=2)+'\n')
    print(result['status'],'whole literal word,all222/all416,8-baseline identity,10controls')

if __name__=='__main__':main()
