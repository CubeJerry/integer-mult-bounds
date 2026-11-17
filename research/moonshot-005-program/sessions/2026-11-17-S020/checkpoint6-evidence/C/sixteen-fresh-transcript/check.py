#!/usr/bin/env python3
"""New actual-cut locality and newly transported entropy witness after16 values."""
from pathlib import Path
from itertools import permutations
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'word':'6256e8349cd6b74e91bcd225141eb84325557eda92fba25cc51ed288dd4a7000',
 'old_dual':'67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e',
 'source_review':'37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402',
 'arithmetic':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
 'entropy_review':'582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23'}
DONE=list(range(8))+[14,17,19,20,96,99,101,102]
def need(x,msg):
    if not x:raise ValueError(msg)
def module(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def normalize(r):
    sign=1 if next(x for x in r if x)>0 else-1;return tuple(sign*x for x in r)
def main():
    ap=argparse.ArgumentParser()
    defaults={'native':'workers/C/native.json','word':'workers/C/parity-sixteen-diagonals/output/WORD.json',
      'old_dual':'workers/R/fresh-transcript-nine/output/MAPPED-DUAL.json','source_review':'workers/C/proper-query-export-review/check.py',
      'arithmetic':'workers/C/four-plane-review/check.py','entropy_review':'workers/C/entropy54-review/check.py'}
    for k,p in defaults.items():ap.add_argument('--'+k.replace('_','-'),type=Path,default=BASE/p)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for k,pin in PINS.items():need(hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==pin,'authenticated '+k)
    R=json.loads(a.native.read_bytes())['native_roots'];w=json.loads(a.word.read_bytes());old=json.loads(a.old_dual.read_bytes())
    source=module(a.source_review,'new_source_review');source.geo=source.load_arithmetic(a.arithmetic);g=source.geo
    C={n:g.chart(z)for n,z in w['charts'].items()};target=[int(v,16)for v in w['Y_correction_rows_hex']]
    stats,V,P=source.replay(w,C,target,check_cut=False)
    U=sorted(set(range(111))-set(DONE));need(len(U)==95 and len(V)==424,'actual newcut scope')
    need(all(V[f'Y{i}']==(1<<(111+i))^(1<<i)for i in DONE),'all16 actual completed values')
    old_roles=old['roles']+old['isolates'];need(not set(old_roles)<=set(U),'old witness is not reused unchanged')
    lookup={normalize(r):i for i,r in enumerate(R)};found=None;attempts=0
    for perm in permutations(range(8)):
        for mask in range(128):
            attempts+=1;new=[]
            for i in old_roles:
                r=[0]*8
                for k,x in enumerate(R[i]):r[perm[k]]=(-x if mask>>k&1 else x)
                j=lookup.get(normalize(r))
                if j not in U:break
                new.append(j)
            if len(new)==14:found=(perm,mask,new);break
        if found:break
    need(found is not None,'a new actual95-role entropy embedding exists')
    perm,mask,new=found;need(len(set(new))==14,'distinct remaining receivers')
    for i,u in zip(old_roles,new):
        for j,v in zip(old_roles,new):
            need((sum(x*y for x,y in zip(R[i],R[j]))==0)==(sum(x*y for x,y in zip(R[u],R[v]))==0),'all196 actual graph incidences preserved')
    mapped=json.loads(json.dumps(old));mapped['roles']=new[:11];mapped['isolates']=new[11:]
    mapped['transport']={'source_certificate_sha256':PINS['old_dual'],'coordinate_permutation':list(perm),'old_coordinate_sign_mask':mask,
      'role_map':[{'old_role':i,'new_role':j}for i,j in zip(old_roles,new)]}
    entropy=module(a.entropy_review,'new_entropy_review');entropy.CORE=new[:11];entropy.ISO=new[11:]
    exact=entropy.review_dual(mapped,R)
    mask_unknown=sum(1<<i for i in U);mask_nonaxis=((1<<111)-1)^255
    checks=[];leaks_done={}
    for i in range(8,111):
        neighbours=sum(1<<j for j,s in enumerate(R)if sum(x*y for x,y in zip(R[i],s))==0)
        inside=[n for n in V if g.contained(C[P[n]],C[f'F{i}'])]
        leaks=[n for n in inside if V[n]&mask_nonaxis&~neighbours]
        if i in U:
            need(not leaks,'strong native locality at every unfinished facet')
            need(all(not(V[n]&mask_unknown&~neighbours)for n in inside),'conditional95-input locality')
            checks.append({'receiver':i,'inside_field_count':len(inside),'inside_fields':inside})
        else:leaks_done[str(i)]=leaks
    need(set(map(int,leaks_done))==set(DONE)-set(range(8))and all(leaks_done.values()),'completed-role leaks are explicit')
    # Each new clique owner is forbidden-local only in its own completed facet.
    clique_geometry=[]
    for z in w['construction']['sixteen_diagonal_deliveries']:
        for d in z['deliveries']:
            n=d['owned_field'];bad=[]
            for i in range(8,111):
                if g.contained(C[P[n]],C[f'F{i}']):
                    N=sum(1<<j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0)
                    if V[n]&mask_nonaxis&~N:bad.append(i)
            need(bad==[d['receiver']],'clique leakage occurs only at its completed receiver')
            clique_geometry.append({'owner':n,'chart':P[n],'only_non_native_local_receiver':bad[0]})
    bad=json.loads(json.dumps(mapped));bad['terms'].pop()
    try:entropy.review_dual(bad,R)
    except (ValueError,AssertionError)as e:control=str(e)
    else:raise ValueError('omitted entropy row was accepted')
    Q=g.moment(stats['movement_profile']);profile=dict(stats['movement_profile']);profile[1]+=9;lower=g.moment(profile)
    gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in g.moment(gate));room=(ceiling[0]-lower[1],ceiling[1]-lower[0])
    a.out.mkdir(parents=True,exist_ok=True);mapped_raw=(json.dumps(mapped,indent=2)+'\n').encode();(a.out/'MAPPED-DUAL.json').write_bytes(mapped_raw)
    result={'status':'PASS_NEW_POST_SIXTEEN_DIAGONAL_17_OVER_2_WITNESS','pins':PINS,'cut':2091,'live_fields':424,
      'completed_diagonal_roles':DONE,'remaining_receiver_count':95,'new_core':new[:11],'new_isolates':new[11:],
      'signed_permutation':list(perm),'sign_mask':mask,'deterministic_search_attempts':attempts,
      'mapped_certificate_sha256':hashlib.sha256(mapped_raw).hexdigest(),'exact_dual':exact,
      'all95_actual_source_locality_checks':checks,'explicit_nonlocal_completed_receivers':leaks_done,
      'each_clique_packet_leaks_only_to_its_completed_receiver':clique_geometry,
      'minimum_future_whole_record_owned_downward_moves':9,'necessary_profile_with_future9':profile,
      'remaining_necessary_limiting_room_after_future9':source.record(room),'omitted_dual_term_rejected':control,
      'scope':'Nine further transfers from the actual2091 cut, based on a newly mapped14-role witness and all424 current fields. Arbitrary paid nested owned routes, monotone public routes, fixed-schedule finite-alphabet zero-error continuations. No claim that16 raw inputs are globally known; conditioning outside the witness is only a lower-bound relaxation.'}
    (a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],new[:11],new[11:],'future9,room',source.record(room)['decimal'][0])
if __name__=='__main__':main()
