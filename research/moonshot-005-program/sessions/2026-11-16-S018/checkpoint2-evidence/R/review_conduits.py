#!/usr/bin/env python3
"""Independent protected-conduit premises and pruned-source audit."""
import argparse,hashlib,json,copy,sys
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['repo','word','pruned','pruned-result','proof','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();prog=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(prog/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from price import invoice
base=prog/'results/bit-canonical-mask-source/author/early-paid46/WORD.json';old=json.loads(base.read_bytes());w=json.loads(a.word.read_bytes());q=json.loads(a.pruned.read_bytes());qr=json.loads(a.pruned_result.read_bytes())
assert hashlib.sha256(base.read_bytes()).hexdigest()=='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd'
assert hashlib.sha256(a.word.read_bytes()).hexdigest()=='075896b6aafe6d0bbb6d406a2cca367c644357f57e01a7888cdfde843f61bd4b'
assert hashlib.sha256(a.pruned.read_bytes()).hexdigest()=='c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245'
ws=independent_replay(w);qs=independent_replay(q);os,_=trace(old);ss,_=trace(w);ts,_=trace(q)
paths={7:('RAW7','P0',[]),11:('RAW11','P1',[]),12:('RAW12','P2',['E77']),19:('HRAW19','P6',['E75','E77','E79']),27:('HRAW27','P7',['E1','E73','E75','E79'])}
D=set(w['released_carriers']);assert len(D)==78;dm=sum(1<<i for i in D)
proof_checks=[]
for d,(r,packet,masks)in paths.items():
 assert not any(o[0]=='ADD'and o[2]==f'X{d}'for o in old['operations'])
 assert [o for o in old['operations']if o[0]=='ADD'and o[2]==r]==[['ADD',f'X{d}',r]]
 assert [o for o in old['operations']if o[0]=='INIT'and o[1]==r]==[['INIT',r,f'L{d}']]
 assert not any(o[0]=='MOVE'and o[1]==r for o in old['operations'])
 k=old['operations'].index(['ADD',r,packet]);v,at=os[k]
 assert v[packet]==0 and v[r]==1<<d and at[r]==at[packet]==f'L{d}'
 suffix=old['operations'][k+1:]
 assert [o for o in suffix if o[0]=='ADD'and o[1]==packet]==[['ADD',packet,f'Y{d}']]
 actual_masks=[o[1]for o in suffix if o[0]=='ADD'and o[2]==packet];assert actual_masks==masks
 for z in masks:
  ix=next(j for j in range(k+1,len(old['operations']))if old['operations'][j]==['ADD',z,packet]);assert os[ix][1][z]=='zero'and os[ix][1][packet]=='zero'and os[ix][0][z]&dm==0
 for op in [['ADD',f'X{d}',r],['ADD',r,packet],['ADD',packet,f'Y{d}']]:assert op in w['operations']
 proof_checks.append({'original':d,'native_cache':r,'packet':packet,'old_zero_before_load':True,'ground_masks':masks,'single_own_output_suffix_reader':True})
def rank(rows):
 b={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j]
   else:b[j]=x;break
 return len(b)
wcut=w['carrier_interface_before_operation'];qcut=qr['interface_index'];wv,wa=ss[wcut];qv,qa=ts[qcut]
for vv,aa in [(wv,wa),(qv,qa)]:
 assert all(vv[f'X{i}']==1<<i and aa[f'X{i}']==(f'L{i}'if i in D else'Hub')for i in range(111))
 for d,(r,packet,masks)in paths.items():
  val=vv[packet];assert aa[packet]=='zero'
  for z in masks:assert aa[z]=='zero';val^=vv[z]
  assert val==1<<d
fields={n:z for n,z in wv.items()if wa[n]=='zero'and z and z>>111==0}
assert len(fields)==25 and rank(fields.values())==25
assert all(qa[n]=='zero'and qv[n]==z for n,z in fields.items())
S=set(q['targets'])|{61,67};Sbits=sum(1<<i for i in S)
assert all(z&~Sbits==0 for n,z in qv.items()if not(n[0]in'XY'and n[1:].isdigit()))
controls=[]
for d in [7,27]:
 r,packet,_=paths[d];bad=copy.deepcopy(w);bad['operations'].remove(['ADD',r,packet])
 try:independent_replay(bad)
 except(AssertionError,KeyError)as e:controls.append({'omitted_load':d,'rejected':True,'reason':str(e)})
 else:raise AssertionError('accepted omitted protected load')
out={'status':'PASS_ROOT_PROTECTED_CONDUITS_AND_PRUNED78_REVIEW','proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'pruned_word_sha256':hashlib.sha256(a.pruned.read_bytes()).hexdigest(),'five_protected_path_premises':proof_checks,'raw_native_carriers':78,'raw_Hub_originals':33,'individual_common_fields_preserved':list(fields),'common_rank':25,'owned_support_coordinate_count':len(S),'owned_support_outside_completed':[61,67],'released_stats':ws,'pruned_stats':qs,'released_price':invoice(ws['movement_profile']),'pruned_price':invoice(qs['movement_profile']),'independent_controls':controls,'scope':'Universal protected-suffix argument reviewed separately; exact source premises,222-column native geometry/endpoints/lifetimes and prices reconstructed with disclosed independent predecessor engines. No author C/A module imported; no new supplier.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
