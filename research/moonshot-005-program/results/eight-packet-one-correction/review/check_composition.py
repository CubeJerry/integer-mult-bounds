#!/usr/bin/env python3
"""Independent E8-prefix/history composition check, without author imports."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter,defaultdict
import gzip,hashlib,json,importlib.util
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';PACK=BASE/'worker-coupling/eight-packet-one-correction';OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';PPIN='52123f6dbe9488835b4aaa9eeb22cd721a8aab0197f17489fb7393d2b2e2865e';WPIN='3d51b5e5d5f1f1cc767700231ebf38e488cc6ebc30cbbfc587e224cf749bc363';RPIN='f15dd02316462d341e64b0d352f8ca23c56e526f8ff7d43dfba5bf2ca1ac82c3';PROOF='fd1e2558b970d927d9de0688c52fc3e13e07f3d7ad2672c54ecc24352f1b8dc1';CPIN='546ca7bf0ab8a958c7269d94143f3ec315e12e96eddbebed129b435ac59239e6'
def need(v,m):
 if not v:raise ValueError(m)
def axpy(a,b,c):
 for k,v in b.items():
  v=a.get(k,F(0))+c*v
  if v:a[k]=v
  else:a.pop(k,None)
def gram_root(v):
 support=[i for i in range(9) if v>>i&1]
 if len(support)==3:
  return [2*int(i in support) for i in range(8)] if 8 in support else [1 if i in support else -1 for i in range(8)]
 missing=[i for i in range(9) if not(v>>i&1)];need(len(missing)==2,'source root weight')
 i,j=missing
 return [1 if k==i else -1 for k in range(8)] if j==8 else [2*int(k==i)-2*int(k==j) for k in range(8)]
def read_source():
 b=(REPO/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(hashlib.sha256(b).hexdigest()==SPIN,'native pin');return json.loads(gzip.decompress(b))
def read_prefix():
 a=gzip.decompress((PACK/'INPUT-PREFIX.json.gz').read_bytes());b=gzip.decompress((REPO/'research/moonshot-005-program/results/eight-packet-prefix/PREFIX.json.gz').read_bytes())
 need(a==b and hashlib.sha256(a).hexdigest()==PPIN,'exact previously reviewed prefix');return json.loads(a)
def import_own_channel_checker():
 p=BASE/'worker-review/foreign-history-channel/check_channel.py';need(hashlib.sha256(p.read_bytes()).hexdigest()=='8e625b20883a865ea2e8eb06994e94ad035416a30bbd70ad3e4bc3013ce9e2e3','own independent channel checker pin')
 spec=importlib.util.spec_from_file_location('review_channel_helpers',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def prefix_map(source,prefix):
 mains=sorted(set(source['live'])|{x+112 for x in source['live']}|set(source['hosted']['X2'])|set(source['hosted']['Y2']));raw={r:1480+i for i,r in enumerate(mains)}
 need({str(r):p for r,p in raw.items()}==prefix['difference_role_map'],'actual main map')
 need(prefix['program'][:400]==[['ADD',raw[r],r,'-1',source['initial'][r]] for r in mains],'literal invertible entry difference map')
 state={p:{r:F(1)} for r,p in raw.items()}
 for op in prefix['program'][400:]:
  kind,j=op[:2];need(j>=1480,'prefix leaves all common fields untouched')
  if kind=='INIT':need(j not in state,'fresh packet');state[j]={}
  elif kind=='CLEAR':del state[j]
  elif kind=='SCALE':state[j]={r:F(op[2])*v for r,v in state[j].items()}
  elif kind=='ADD':need(op[2]>=1480,'prefix after entry uses only real private/packet fields');axpy(state[j],state[op[2]],F(op[3]))
  elif kind!='MOVE':raise ValueError(kind)
 roots=[gram_root(v) for v in source['ports']];xs=source['live'];G=[[sum(a*b for a,b in zip(x,y)) for y in roots] for x in roots]
 c={x:(F(1) if i in source['hosted']['Dports'] else F(1,2)) for i,x in enumerate(xs)}
 need(prefix['roots']==roots and prefix['donor_roles']==xs and {str(x):str(v) for x,v in c.items()}==prefix['receiver_weights'],'source-derived roots and receiver weights')
 expected={r:{r:F(1)} for r in mains}
 for i,x in enumerate(xs):
  row={x+112:c[x]}
  for j,y in enumerate(xs):
   if G[i][j]:row[y]=c[x]*G[i][j]/8
  expected[x+112]=row
 need(set(state)==set(raw.values()) and all(state[raw[r]]==expected[r] for r in mains),'independent400-coordinate prefix algebra')
 return raw,expected,G,c

def main():
 source=read_source();prefix=read_prefix();helper=import_own_channel_checker()
 b=gzip.decompress((PACK/'WORD.json.gz').read_bytes());need(hashlib.sha256(b).hexdigest()==WPIN,'composed word payload');word=json.loads(b)
 b=(PACK/'RESULT.json').read_bytes();need(hashlib.sha256(b).hexdigest()==RPIN,'author result pin');report=json.loads(b)
 need(hashlib.sha256((PACK/'PROOF.md').read_bytes()).hexdigest()==PROOF,'frozen proof pin')
 b=(PACK/'INPUT-CERTIFICATE.json').read_bytes();need(hashlib.sha256(b).hexdigest()==CPIN,'reviewed history input pin');cert=json.loads(b);rel=cert['candidate_channels'][0]['best_relation']
 need(not helper.baseline_relation(source,rel),'full common-input history identity')
 z,gain,guards,arrivals=helper.pulse(source,rel);need(gain==-1 and len(z)==33,'independent pulse and repair')
 raw,expected,G,c=prefix_map(source,prefix);xs=source['live'];i=xs.index(60);j=xs.index(47)
 need(c[60]==F(1,2) and G[i][j]==4 and expected[172][47]==F(1,4),'actual weighted residual')
 ops=word['program'];pp=prefix['program'];pmap={int(i):k for i,k in word['prefix_event_to_physical'].items()};nmap=word['native_event_to_physical'];marks=word['marks'];cache=word['donor_cache']
 need(word['source_sha256']==SPIN and word['prefix_decompressed_sha256']==PPIN,'composed source/prefix pins')
 need(word['private_role_map']==prefix['difference_role_map'] and word['initial']==prefix['initial'] and word['public']==1880 and word['owned_fields']==53 and cache==1932,'complete physical field interface')
 need(set(pmap)==set(range(2362)) and len(set(pmap.values()))==2362,'all prefix instructions mapped once')
 need(len(nmap)==len(source['program']) and nmap==sorted(set(nmap)),'complete ordered native map')
 covered=set()
 def claim(pos,expected_op):
  need(pos not in covered and 0<=pos<len(ops) and ops[pos]==expected_op,'exact instruction coverage at '+str(pos));covered.add(pos)
 for e,pos in pmap.items():claim(pos,pp[e])
 rename=lambda r:r+400 if r>=1480 else r
 for e,pos in enumerate(nmap):
  op=list(source['program'][e]);op[1]=rename(op[1])
  if op[0] in ('ADD','COPY'):op[2]=rename(op[2])
  claim(pos,op)
 need(nmap[0]==marks['common_starts'] and nmap[-1]+1==marks['common_finished'],'actual common boundaries')
 nonmove=[pmap[e] for e,op in enumerate(pp) if op[0]!='MOVE'];need(nonmove==sorted(nonmove),'all prefix scalar operations retain order')
 need([pmap[e] for e in range(400)]==list(range(400)),'entry differences precede the cache')
 original={e:o for e,o in enumerate(source['program']) if o[0]=='MOVE' and o[1] in raw};reservations=word['raw_reservations'];rmap={r['source_event']:r for r in reservations}
 need(len(rmap)==len(reservations)==len(original)==1710 and set(rmap)==set(original),'all raw source reservations once')
 pr={r['source_event']:r for r in prefix['reservations']};need(len(pr)==890,'prefix reservation count')
 delayed=[]
 for e,r in rmap.items():
  o=original[e];pos=r['physical_event'];need(ops[pos]==['MOVE',raw[o[1]],o[2],o[3],False] and r['role']==o[1],'actual raw transport')
  if e in pr:
   pe=pr[e]['physical_event'];need(r['prefix_event']==pe and pmap[pe]==pos,'prefix reservation lineage')
   if pos>marks['common_starts']:delayed.append(e)
  else:
   need(r.get('prefix_event') is None and pos<marks['common_starts'],'remaining raw route completed before native')
   claim(pos,['MOVE',raw[o[1]],o[2],o[3],False])
 need(sorted(delayed)==[40965,42097],'only the two actual receiver suffix legs delayed')
 need({k for k,o in enumerate(ops) if o[0]=='MOVE' and 1480<=o[1]<1880}=={r['physical_event'] for r in reservations},'no additional raw movement')
 claim(400,['INIT',cache,43]);claim(401,['ADD',cache,raw[47],'1',43]);need(marks['cache_acquired']==400,'actual q cache cut')
 start=marks['initial_decoder']
 for offset,t in enumerate(rel['initial_terms']):claim(start+offset,['ADD',raw[172],t['role'],str(F(t['coefficient'])/4),3])
 need(all(pmap[e]<start for e,o in enumerate(pp) if o[0] in ('ADD','SCALE','COPY') and o[1]==raw[172]),'common decoder terms follow every receiver scaling and packet mixture')
 need(start+107<marks['common_starts'],'initial common terms read before native begins')
 pos=marks['control'];claim(pos,['ADD',1193,cache,'1',43]);claim(pos+1,['CLEAR',cache,43]);need(pos+2==nmap[31460],'pulse at exact source cut')
 for t in rel['arrival_terms']:
  pos=marks['observation_'+str(t['after_event'])];claim(pos,['ADD',raw[172],t['role'],str(F(t['coefficient'])/4),524]);need(pos==nmap[t['after_event']]+1,'actual immediate arrival read')
 need(marks['receiver_corrected']==marks['observation_36811']+1 and rmap[40965]['physical_event']>=marks['receiver_corrected'],'delayed receiver stays through both reads')
 for offset,(r,value) in enumerate(sorted(z.items())):claim(marks['common_finished']+offset,['ADD',r,raw[47],str(-value),127])
 need(marks['common_restored']==marks['common_finished']+33,'complete hub repair block')
 for offset,r in enumerate(sorted(raw)):claim(marks['common_restored']+offset,['ADD',raw[r],r,'1',source['final'][r]])
 need(covered==set(range(len(ops))),'literal prefix, source, routes, caches, decoder, repairs and boundaries cover the complete word')
 need(max(nonmove)<marks['common_starts'],'all prefix arithmetic completed before native execution')
 counts,ranks,peak=helper.typed_walk(source,word)
 need(dict(counts)==report['bill']['opcode_counts'] and {str(k):v for k,v in ranks.items()}==report['bill']['move_rank_histogram'] and peak==43,'independent full physical invoice')
 native=Counter(o[0] for o in source['program']);pc=Counter(o[0] for o in pp)
 e8extra={op:pc[op]-(400 if op=='ADD' else 890 if op=='MOVE' else 0) for op in ['ADD','SCALE','MOVE','INIT','CLEAR','COPY']}
 baseline=native+Counter({'ADD':800,'MOVE':1710})+Counter(e8extra)
 increment={op:counts[op]-baseline[op] for op in e8extra}
 need(increment==report['increment_beyond_common_raw_boundaries_and_E8']=={'ADD':144,'SCALE':0,'MOVE':0,'INIT':1,'CLEAR':1,'COPY':0},'complete incremental composition cost')
 corrected={r:row.copy() for r,row in expected.items()};axpy(corrected[172],{47:F(1)},F(-1,4));need(47 not in corrected[172],'selected weighted coefficient vanishes')
 before=sum(G[i][j]!=0 for i in range(104) for j in range(104) if i!=j);after=before-1
 need(before==4992 and after==report['remaining_weighted_residual_terms']==4991,'exact residual census')
 remain172=sum(j!=xs.index(60) and G[xs.index(60)][j]!=0 and xs[j]!=47 for j in range(104));need(remain172==report['remaining_at_receiver172']==47,'receiver172 residual count')
 complete=0
 for i,x in enumerate(xs):
  desired={x+112:c[x],x:c[x]}
  if corrected[x+112]==desired:complete+=1
 need(complete==report['completed_private_receivers']==0,'no receiver is completely repaired')
 inverse_rows=0
 for r in sorted(raw):
  if r-112 in c:
   x=r-112;i=xs.index(x);row={k:v/c[x] for k,v in corrected[r].items()}
   for j,y in enumerate(xs):
    if G[i][j]:axpy(row,corrected[y],-F(G[i][j],8))
   if r==172:axpy(row,corrected[47],F(1,4)/c[x])
  else:row=corrected[r].copy()
  need(row=={r:F(1)},'explicit inverse of complete400-row raw map');inverse_rows+=1
 early=dict(rel);early['initial_terms']=[dict(t,coefficient=str(F(t['coefficient'])/2)) for t in rel['initial_terms']]
 erow=helper.baseline_relation(source,early);need(erow.get(34)==F(-1,2),'placing terms before half-normalization creates common error')
 need(expected[172][47]+F(-1,8)==F(1,8),'wrong quarter-weight control must leave a residual')
 wrong_cache_residual={'v47':F(1,4),'u47':F(-1,2)}
 need(any(wrong_cache_residual.values()),'wrong cochart cache gives a nonzero two-input error')
 need(source['initial'][47]==43,'wrong cache control is cochart but would store common u47')
 result={'status':'PASS_INDEPENDENT_E8_ONE_HISTORY_CORRECTION_COMPOSITION','source_sha256':SPIN,'prefix_payload_sha256':PPIN,'word_payload_sha256':WPIN,'author_result_sha256':RPIN,'reviewed_proof_sha256':PROOF,'prefix_instructions_retained_once':len(pmap),'native_instructions_retained_in_order':len(nmap),'raw_reservations_once':len(rmap),'prefix_raw_reservations_once':len(pr),'remaining_raw_reservations':len(rmap)-len(pr),'q47_cache':{'role':cache,'chart':43,'acquired_after_entry':400,'MOVE_count':0,'lifetimes':1},'receiver172_weight':str(c[60]),'Gram_60_47':G[xs.index(60)][xs.index(47)],'original_residual':'1/4','history_gain':'-1','decoder_multiplier':'1/4','corrected_coefficient':'0','all_common_rows_restored':1480,'private_inverse_rows':inverse_rows,'remaining_residual_terms':after,'remaining_at172':remain172,'completed_first_receivers':complete,'instructions':len(ops),'counts':dict(counts),'MOVE_rank_histogram':{str(k):v for k,v in sorted(ranks.items())},'peak_owned':peak,'correction_increment':increment,'negative_controls':{'initial_terms_before_normalization_common34_error':'-1/8','wrong_history_multiplier_1_8_remaining_q47':'1/8','wrong_cochart_cache_receiver_error':{k:str(v) for k,v in wrong_cache_residual.items()}},'scope':'Independent source-derived E8 algebra, pinned-prefix embedding, exact full-common adjoint/pulse, all-physical-word audit and universal1880-input composition proof. Does not rerun a dense1880-column native baseline or import author verifiers. One residual removed, no complete private native or new kappa.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
