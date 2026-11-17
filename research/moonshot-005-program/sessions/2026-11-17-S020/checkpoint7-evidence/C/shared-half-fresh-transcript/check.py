#!/usr/bin/env python3
"""Fresh post-service entropy certificate with explicit16-source conditioning."""
from pathlib import Path
from itertools import permutations
import argparse,hashlib,importlib.util,json
BASE=Path('/workspace/scratch/2a62370e4336')
PINS={'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'word':'91d4a24a995a18ed306b6c657e76e9cac1f14c8077b4143aae94581b50e2eb6e',
 'old_dual':'67b8f94d20704d20e5a609755b692d0bcc85cb264c67a346c01b099a17e2b20e',
 'source_review':'37d995575ad179e524c0de505e5d56f45749b5da73ce3750244c5594e41a9402',
 'arithmetic':'41b4d0ec79abc43cc32a9b97d8a36fb3805e5602630b07c2f74a5999a281a565',
 'entropy_review':'582f534eefdac53c4b4a284c01ce24454969327e13014c8d56270ce75b875e23'}
def need(x,s):
    if not x:raise ValueError(s)
def module(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def normalize(r):
    sign=1 if next(x for x in r if x)>0 else-1;return tuple(sign*x for x in r)
def main():
    ap=argparse.ArgumentParser()
    defaults={'native':'workers/C/native.json','word':'workers/A/proper-half-service/WORD.json',
      'old_dual':'workers/R/fresh-transcript-nine/output/MAPPED-DUAL.json','source_review':'workers/C/proper-query-export-review/check.py',
      'arithmetic':'workers/C/four-plane-review/check.py','entropy_review':'workers/C/entropy54-review/check.py'}
    for k,p in defaults.items():ap.add_argument('--'+k.replace('_','-'),type=Path,default=BASE/p)
    ap.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=ap.parse_args()
    for k,pin in PINS.items():need(hashlib.sha256(getattr(a,k).read_bytes()).hexdigest()==pin,'authenticated '+k)
    R=json.loads(a.native.read_bytes())['native_roots'];w=json.loads(a.word.read_bytes());old=json.loads(a.old_dual.read_bytes())
    m=module(a.source_review,'fresh_half_source');m.geo=m.load_arithmetic(a.arithmetic);g=m.geo
    C={n:g.chart(z)for n,z in w['charts'].items()};stats,V,P=m.replay(w,C,[int(z,16)for z in w['Y_correction_rows_hex']],check_cut=False)
    need(w['carrier_interface_before_operation']==2089 and len(V)==420,'actual shared-half cut')
    source_mask=0
    for z in w['construction']['proper_half_service']['exports']:
        row=V[z['export_owner']];need(row==int(z['payload_hex'],16),'actual pure exported row');source_mask|=row
    E=[i for i in range(111)if source_mask>>i&1];need(E==[22,23,26,27,42,43,44,45,73,74,75,76,77,78,79,80],'literal16 export-source coordinates')
    U=sorted(set(range(8,111))-set(E));need(len(U)==87,'87 remaining independent unknown inputs')
    before_leaks=[];checks=[];unknown_mask=sum(1<<i for i in U);nonaxis=((1<<111)-1)^255
    for i in range(8,111):
        N=sum(1<<j for j,r in enumerate(R)if sum(x*y for x,y in zip(R[i],r))==0)
        inside=[n for n in V if g.contained(C[P[n]],C[f'F{i}'])]
        for n in inside:
            bad=V[n]&nonaxis&~N
            if bad:before_leaks.append({'receiver':i,'field':n,'forbidden_mask_hex':hex(bad)})
            need(V[n]&unknown_mask&~N==0,'every actual inside field is native-local after conditioning16')
        if i in U:checks.append({'receiver':i,'inside_fields':inside})
    need(len(before_leaks)==66 and len(checks)==87,'all66 actual leaks handled,87 receiver audits')
    old_roles=old['roles']+old['isolates'];need(not set(old_roles)<=set(U),'old mapped witness is not inherited')
    lookup={normalize(r):i for i,r in enumerate(R)};found=None;attempts=0
    for perm in permutations(range(8)):
        for mask in range(128):
            attempts+=1;new=[]
            for i in old_roles:
                row=[0]*8
                for k,x in enumerate(R[i]):row[perm[k]]=(-x if mask>>k&1 else x)
                j=lookup.get(normalize(row))
                if j not in U:break
                new.append(j)
            if len(new)==14:found=(perm,mask,new);break
        if found:break
    need(found is not None,'fresh87-role embedding found');perm,mask,new=found
    need(len(set(new))==14,'distinct witness roles')
    for i,u in zip(old_roles,new):
        for j,v in zip(old_roles,new):need((sum(x*y for x,y in zip(R[i],R[j]))==0)==(sum(x*y for x,y in zip(R[u],R[v]))==0),'exact196 graph incidences')
    mapped=json.loads(json.dumps(old));mapped['roles']=new[:11];mapped['isolates']=new[11:]
    mapped['transport']={'source_certificate_sha256':PINS['old_dual'],'coordinate_permutation':list(perm),
      'old_coordinate_sign_mask':mask,'role_map':[{'old_role':i,'new_role':j}for i,j in zip(old_roles,new)]}
    h=module(a.entropy_review,'fresh_half_entropy');h.CORE=new[:11];h.ISO=new[11:];exact=h.review_dual(mapped,R)
    bad=json.loads(json.dumps(mapped));bad['terms'].pop()
    try:h.review_dual(bad,R)
    except(ValueError,AssertionError)as e:control=str(e)
    else:raise ValueError('deleted entropy term accepted')
    profile=dict(stats['movement_profile']);profile[1]+=9;lower=g.moment(profile);gate={127:37,64:74,1:-74}
    for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
    ceiling=tuple(v/6 for v in g.moment(gate));room=(ceiling[0]-lower[1],ceiling[1]-lower[0])
    a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(mapped,indent=2)+'\n').encode();(a.out/'MAPPED-DUAL.json').write_bytes(raw)
    result={'status':'PASS_FRESH_NINE_FUTURE_DESCENTS_AFTER_SHARED_HALF_SERVICE','pins':PINS,'source_cut':2089,'live_fields':420,
      'explicitly_conditioned_export_source_roles':E,'remaining_unknown_input_count':87,'unconditioned_forbidden_incidences':before_leaks,
      'all87_actual_field_locality_checks':checks,'new_core':new[:11],'new_isolates':new[11:],'signed_permutation':list(perm),
      'sign_mask':mask,'deterministic_search_attempts':attempts,'new_mapped_certificate_sha256':hashlib.sha256(raw).hexdigest(),
      'exact_dual':exact,'future_whole_record_owned_downward_moves_lower_bound':9,'minimum_necessary_profile':profile,
      'remaining_necessary_limiting_room_after_future9':m.record(room),'missing_entropy_term_control':control,
      'scope':'Actual2089 cut with all66 leaked field/facet incidences handled by explicitly conditioning the16 export-source inputs, only as a lower-bound relaxation. A fresh14-role witness among87 independent remaining inputs gives17/2 entropy and at least9 further whole-record descents. Monotone publics, arbitrary paid nested owners, fixed-schedule finite-alphabet zero-error continuation; future code banks unrestricted.'}
    (a.out/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'],new[:11],new[11:],'room',m.record(room)['decimal'][0])
if __name__=='__main__':main()
