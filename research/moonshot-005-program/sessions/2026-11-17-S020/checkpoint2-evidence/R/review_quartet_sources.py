"""Independent physical and coefficient review of the S020 quartet sources.

Uses only the earlier independent Fraction/set interpreter. No current author
builder, geometry, elimination, tariff or source invoice is imported.
"""
from __future__ import annotations
import argparse,copy,hashlib,importlib.util,json
from collections import defaultdict,Counter
from pathlib import Path

PINS={
 'hub':'0b89346f8db49a1da62739e937ddc011f63c2fae223967569400d687085b2929',
 'ground':'ccb08f86b54924ae4f2af1a5647750ef00294666f3e8a80ec77761d8e1dc526d',
 'hierarchical':'318729fac41fa7871d1e74d440c5af977775655b6eb392ce6f9c1b66ee131176',
}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--kind',choices=PINS,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
 interpreter=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint3-evidence/C/portable/audit_cp6.py'
 spec=importlib.util.spec_from_file_location('prior_independent_geometry',interpreter);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);need=m.insist
 need(m.sha(a.word)==PINS[a.kind],'exact source word pin');need(m.sha(native)=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e','native source pin')
 w=json.loads(a.word.read_text());source=json.loads(native.read_text());R=source['native_roots'];c=w['construction'];cut=w['carrier_interface_before_operation'];hier=a.kind=='hierarchical';ground=a.kind!='hub'
 groups=defaultdict(set)
 for i,r in enumerate(R):groups[tuple(j for j,x in enumerate(r)if x)].add(i)
 need(Counter(map(len,groups))=={1:8,4:14},'exact support partition')
 need(Counter(len(v)for k,v in groups.items()if len(k)==4)=={6:2,7:5,8:7},'punctured quartet sizes')
 neighbours={i:{j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0}for i in range(111)}
 canonical={i:frozenset({i}^neighbours[i])for i in range(111)};canonical_basis=m.binary_basis(canonical.values());need(len(canonical_basis)==9,'full111 canonical rank9')
 extra=[]
 if hier:
  for g in c['groups']:
   for h in g['halves']:
    indices=[k for k,op in enumerate(w['operations'])if op[0]=='MOVE'and op[1]in{f'X{i}'for i in h['pivots']}and op[2]==g['chart']]
    need(len(indices)==3,'exact lower-stage arrival count');h['_review_snapshot']=max(indices)+1;extra.append(max(indices)+1)
 stats,snap,C,events=m.replay(w,source,[cut,*extra]);v,loc=snap[cut]
 need(not w['targets']and stats['completed_outputs']==[],'no receiver endpoint claimed')
 expected_counts={'INIT':148 if hier else 120,'ADD':850 if hier else 747,'MOVE':418 if hier else(334 if ground else 325),'CLEAR':148 if hier else 120}
 expected_profile={1:84,2:103,4:84,5:19,7:119,8:9}if hier else{3:103,4:103,7:119}
 if ground and not hier:expected_profile[8]=9
 need(stats['counts']==expected_counts and stats['movement_profile']==expected_profile,'independent complete invoice');need(stats['dirty_clear']==expected_counts['CLEAR'],'dirty retirement bill')
 need(cut==(1117 if hier else(902 if ground else 893))and len(v)==(370 if hier else 342),'actual cut dimensions')
 need(sum(e[-1]for e in events)==(9 if ground else 0),'only nine code owned descents when present')
 for i in range(111):
  need(v[f'NATIVE_{i}']=={i}and loc[f'NATIVE_{i}']==f'L{i}','actual native raw cache')
  need(v[f'Y{i}']=={111+i}and loc[f'Y{i}']=='zero','all arbitrary Y originals remain ground')
 need(len(m.binary_basis(v[f'X{i}']for i in range(111)))==111,'invertible original coefficient map')
 seen=set();all_hub=set();all_lower=set();all_mixed=set();half_rows=[];group_rows=[]
 for g in c['groups']:
  support=tuple(g['support']);I=set(g['roles']);need(support in groups and I==groups[support]and not(seen&I),'actual source partition');seen|=I
  if len(support)==1:
   i=next(iter(I));need(v[f'X{i}']=={i}and loc[f'X{i}']=='Hub','raw coordinate original at Hub');all_hub.add(i);continue
  chart=m.chart({'kind':'span','rows':[R[i]for i in sorted(I)]});need(len(chart)==4 and C[g['chart']]==chart,'exact quartet chart')
  local_rows=[row&I for row in canonical.values()];local_basis=m.binary_basis(local_rows);need(len(local_basis)==4,'canonical local rank4')
  pivots=g['Hub_pivots']if hier else g['pivots'];actual_rows=[v[f'X{i}']for i in pivots];actual_basis=m.binary_basis(actual_rows)
  need(len(pivots)==4 and len(actual_basis)==4 and all(row<=I for row in actual_rows),'actual four local pivots')
  need(all(m.in_span(row,actual_basis)for row in local_rows)and all(m.in_span(row,local_basis)for row in actual_rows),'actual local pivot span exactly desired code')
  need(all(loc[f'X{i}']=='Hub'for i in pivots),'actual local pivots at Hub');all_hub.update(pivots)
  if not hier:
   held=set(g['held']);need(held==I-set(pivots),'nonpivot role partition')
   for i in held:need(v[f'X{i}']=={i}and C[loc[f'X{i}']]==chart,'actual raw rank4 hold')
   for p,row in zip(pivots,actual_rows):need(row&set(pivots)=={p},'identity pivot block')
   all_lower|=held
  else:
   half_seen=set();lower_pivots=set();raws=set()
   for h in g['halves']:
    J={i for i in I if R[i][support[0]]==h['sign']*R[i][support[1]]};need(J==set(h['roles'])and not(J&half_seen),'exact pair-equality half');half_seen|=J
    H=m.chart({'kind':'span','rows':[R[i]for i in sorted(J)]});need(C[h['chart']]==H and len(H)==3,'actual half chart rank3')
    need(v[h['sum_field']]==J and C[loc[h['sum_field']]]==H,'actual stationary half sum')
    hp=set(h['pivots']);raw=set(h['raw_held']);need(len(hp)==3 and hp|raw==J and not(hp&raw),'lower pivot partition')
    need(all(v[f'X{i}']=={i}and C[loc[f'X{i}']]==H for i in raw),'raw lower original holds')
    lower_v,lower_l=snap[h['_review_snapshot']];lower_code=m.binary_basis(lower_v[f'X{i}']for i in hp);needed=[row&J for row in canonical.values()]
    need(len(lower_code)==3 and all(m.in_span(row,lower_code)for row in needed),'lower-stage actual desired row span')
    need(all(lower_l[f'X{i}']==g['chart']for i in hp),'lower code actually reaches upper chart')
    lower_pivots|=hp;raws|=raw
    half_rows.append({'roles':sorted(J),'rank':3,'raw_held':sorted(raw),'sum_row':sorted(v[h['sum_field']]),'source_snapshot':h['_review_snapshot']})
   mixed=set(g['mixed_held']);need(half_seen==I and mixed==lower_pivots-set(pivots),'upper-source partition')
   need(len(mixed)==2 and all(C[loc[f'X{i}']]==chart and v[f'X{i}']<=I for i in mixed),'actual mixed rank4 holds')
   all_lower|=raws;all_mixed|=mixed
  group_rows.append({'support':list(support),'roles':sorted(I),'local_canonical_rank':4,'Hub_pivots':pivots})
 need(seen==set(range(111))and len(all_hub)==64 and len(all_lower)==(19 if hier else 47)and len(all_mixed)==(28 if hier else 0),'complete actual carrier partition')
 need(all_hub|all_lower|all_mixed==set(range(111))and not(all_hub&all_lower or all_hub&all_mixed or all_lower&all_mixed),'disjoint complete carriers')
 code=[v[n]for n in c['canonical_fields']];code_basis=m.binary_basis(code);need(len(code)==9 and len(code_basis)==9,'actual nine independent canonical fields')
 need(all(m.in_span(row,code_basis)for row in canonical.values())and all(m.in_span(row,canonical_basis)for row in code),'exact whole canonical bank')
 need(all(loc[n]==('zero'if ground else'Hub')for n in c['canonical_fields']),'actual canonical custody')
 # Every noncanonical local value is genuinely native-supported. This is an
 # information fact, not permission to read it from another physical chart.
 for n,row in v.items():
  if n in c['canonical_fields']:continue
  for i in range(111):
   if m.subset(C[loc[n]],C[f'F{i}']):need((row&set(range(111)))<=neighbours[i],'noncanonical local field has no external support')
 controls=[]
 labels=['native_capture','proper_half_sum_capture','lower_triangular_encode','upper_triangular_encode','actual_hierarchical_code_read','canonical_descent','actual_upper_inverse','actual_lower_inverse']if hier else['native_capture','triangular_encode','actual_local_code_read','actual_triangular_inverse']+(['full_code_descent']if ground else[])
 for label in labels:
  k=w['semantic_operation_indices'][label][0];bad=copy.deepcopy(w);bad['operations'].pop(k);pos=cut-(k<cut)
  try:
   _,ss,_,_=m.replay(bad,source,[pos]);need(ss[pos][0]==v and ss[pos][1]==loc,'cut source changed')
  except(ValueError,KeyError)as error:controls.append({'omitted':label,'operation':k,'rejected':str(error)})
  else:raise ValueError('omission accepted: '+label)
 if hier:
  bad=copy.deepcopy(w);up=w['semantic_operation_indices']['actual_upper_inverse'];lo=w['semantic_operation_indices']['actual_lower_inverse'];inds=sorted(up+lo);ops=[w['operations'][i]for i in lo+up]
  for k,op in zip(inds,ops):bad['operations'][k]=op
  try:m.replay(bad,source,[cut])
  except(ValueError,KeyError)as error:controls.append({'mutation':'lower inverse before upper inverse','rejected':str(error)})
  else:raise ValueError('wrong inverse order unexpectedly accepted')
 q=m.moment(expected_profile);allow_profile={127:37,64:74,1:-74}
 for j in range(1,9):allow_profile[1+7*j]=allow_profile.get(1+7*j,0)+74;allow_profile[7*j]=allow_profile.get(7*j,0)-74
 allow=tuple(x/6 for x in m.moment(allow_profile));room=(allow[0]-q[1],allow[1]-q[0]);need(room[0]>0,'positive necessary room')
 result={'status':'PASS_INDEPENDENT_QUARTET_SOURCE','kind':a.kind,'source_sha256':m.sha(native),'word_sha256':m.sha(a.word),'interpreter_sha256':m.sha(interpreter),'cut':cut,'live_fields':len(v),'stats':stats,'canonical_rank':9,'actual_Hub_originals':64,'raw_held':len(all_lower),'mixed_held':len(all_mixed),'actual_half_sums':len(half_rows),'moment':m.interval_json(q),'necessary_room':m.interval_json(room),'negative_controls':controls,'all_noncanonical_local_fields_native_supported':True,'scope':'Actual partial all222-column source, blockwise every characteristic-two field/positive width. No receiver completion, free simultaneous access, complete supplier or new kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.out/'SOURCE-CONTRACT.json').write_text(json.dumps({'groups':group_rows,'halves':half_rows,'held_raw_roles':sorted(all_lower),'mixed_roles':sorted(all_mixed),'Hub_roles':sorted(all_hub)},indent=2,sort_keys=True)+'\n');print(result['status'],a.kind);print('moment',result['moment']['decimal']);print('necessary room',result['necessary_room']['decimal'])

if __name__=='__main__':main()
