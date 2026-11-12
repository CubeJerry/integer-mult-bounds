#!/usr/bin/env python3
"""Independent complete-first-family and append-only boundary review."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import gzip,json,hashlib,importlib.util
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';PACK=BASE/'root-research/complete-first-family';OUT=Path(__file__).resolve().parent
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';WPIN='0ba02fedfecb6f118441cd6b2cb7e008ad4153e3e015d377f1374ffeecc1ef4f';PAY='e5d4fbe7a43231b8b2534551f6b3315ac38539e613e680d3f916385d0904bd25';IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
def need(b,m):
 if not b:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def add(a,b,c=F(1)):
 for k,v in b.items():
  x=a.get(k,F(0))+c*v
  if x:a[k]=x
  else:a.pop(k,None)
def helper():
 p=BASE/'worker-review/route-fusion/check_fusion.py';need(digest(p.read_bytes())=='cd0a90cc2773d144a1c106245d14c5a6f6ee9fad76dca64383a5dc2d7fa04763','own physical/moment helper')
 s=importlib.util.spec_from_file_location('own_route_review',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
 h=helper();sb=(REPO/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(digest(sb)==SPIN,'source pin');src=json.loads(gzip.decompress(sb));wb=(PACK/'WORD.json.gz').read_bytes();need(digest(wb)==WPIN and digest(gzip.decompress(wb))==PAY,'word pins');w=json.loads(gzip.decompress(wb));report=json.loads((PACK/'RESULT.json').read_text())
 n=src['public'];mainroles=sorted(set(src['live'])|{x+112 for x in src['live']}|set(src['hosted']['X2'])|set(src['hosted']['Y2']));need(n==1480 and len(mainroles)==400,'actual400 main roles');raw={r:1480+i for i,r in enumerate(mainroles)}
 need(w['difference_role_map']=={str(r):p for r,p in raw.items()},'complete raw role map');D=set(src['hosted']['Dports']);coupled=[x for i,x in enumerate(src['live']) if i not in D];need(len(D)==96 and len(src['live'])==104 and len(coupled)==8,'source partition')
 T={r:{r:F(1)} for r in mainroles}
 for i,x in enumerate(src['live']):
  y=x+112
  if i in D:T[y]={x:F(1),y:F(1)}
  else:T[x]={x:F(1),y:F(-1)};T[y]={x:F(1,2),y:F(1,2)}
 for x,y in zip(src['hosted']['X2'],src['hosted']['Y2']):T[x]={x:F(1),y:F(-1)}
 adj=[{} for _ in range(n+src['owned_fields'])]
 for r in mainroles:adj[r]={r:F(1)}
 for o in reversed(src['program']):
  kind,j=o[:2]
  if kind in ('ADD','COPY'):
   add(adj[o[2]],adj[j],F(o[3]))
   if kind=='COPY':adj[j]={}
  elif kind=='SCALE':adj[j]={r:F(o[2])*c for r,c in adj[j].items()}
  elif kind in ('INIT','CLEAR'):adj[j]={}
  elif kind!='MOVE':raise ValueError(kind)
 actual={r:{} for r in mainroles}
 for j,row in enumerate(adj):
  for r,c in row.items():actual[r][j]=c
 need(actual==T,'all400 native main rows on all1480 common inputs, with no auxiliary contamination')
 P=w['program'];m=w['marks'];tmp=n+400+src['owned_fields'];need(w['public']==1880 and w['owned_fields']==src['owned_fields']+1 and w['initial']==src['initial']+[src['initial'][r] for r in mainroles],'physical namespace')
 need(m['differences']==400 and m['raw_final']==800 and m['common_finished']==800+len(src['program'])==72061,'block boundaries')
 need(P[:400]==[['ADD',raw[r],r,'-1',src['initial'][r]] for r in mainroles],'all400 entry differences')
 need(P[400:800]==[['MOVE',raw[r],src['initial'][r],src['final'][r],False] for r in mainroles],'all400 direct routes')
 native=[]
 for o in src['program']:
  v=o.copy();v[1]+=400 if v[1]>=n else 0
  if v[0] in ('ADD','COPY'):v[2]+=400 if v[2]>=n else 0
  native.append(v)
 need(P[800:72061]==native and w['native_event_to_physical']==list(range(800,72061)),'literal full common native retained once')
 routes=[];oldprofile=Counter();spaces=list(map(h.space,src['frames']))
 for idx,r in enumerate(mainroles):
  events=[e for e,o in enumerate(src['program']) if o[0]=='MOVE' and o[1]==r];current=src['initial'][r]
  for e in events:
   o=src['program'][e];need(o[2]==current and spaces[o[2]]<spaces[o[3]],'continuous proper original raw route');oldprofile[len(src['frames'][o[3]])-len(src['frames'][o[2]])]+=1;current=o[3]
  need(current==src['final'][r] and spaces[src['initial'][r]]<spaces[current] and len(src['frames'][current])-len(src['frames'][src['initial'][r]])==8,'proper rank8 direct route')
  routes.append({'physical_event':400+idx,'role':r,'source_events':events})
 need(routes==w['raw_route_lineage'],'exact route provenance');need(len(w['new_packets'])==112,'actual112 packet macros');position=72061;packets=[]
 for i,x in enumerate(src['live']):
  y=x+112;c='1' if i in D else '1/2';facet=src['final'][y];begin=position
  expected=[['INIT',tmp,127],['ADD',tmp,raw[x],'1',127],['MOVE',tmp,127,facet,True]]
  if c!='1':expected.append(['SCALE',raw[y],c,facet])
  expected.extend([['ADD',raw[y],tmp,c,facet],['CLEAR',tmp,facet]])
  need(P[position:position+len(expected)]==expected,'forward packet and actual normalization');position+=len(expected);packets.append({'kind':'forward','start':begin,'stop':position,'x':x,'y':y})
 need(position==m['all_first_Y_correct']==72589,'all forward uses precede reverse changes')
 for x in coupled:
  y=x+112;facet=src['final'][y];begin=position
  expected=[['INIT',tmp,facet],['ADD',tmp,raw[y],'1',facet],['MOVE',tmp,facet,127,True],['SCALE',raw[x],'2',127],['ADD',raw[x],tmp,'-2',127],['CLEAR',tmp,127]]
  need(P[position:position+6]==expected,'exact coupled reverse macro');position+=6;packets.append({'kind':'coupled_reverse','start':begin,'stop':position,'x':x,'y':y})
 need(position==m['all_first_pairs_correct']==72637 and packets==w['new_packets'],'complete packet partition')
 need(P[position:]==[['ADD',raw[r],r,'1',src['final'][r]] for r in mainroles] and len(P)==73037,'all400 recouplings and no other operations')
 qstate={raw[r]:{r:F(1)} for r in mainroles}
 for o in P[72061:72637]:
  kind,j=o[:2]
  if kind=='INIT':qstate[j]={}
  elif kind=='CLEAR':del qstate[j]
  elif kind=='ADD':add(qstate[j],qstate[o[2]],F(o[3]))
  elif kind=='SCALE':qstate[j]={r:F(o[2])*c for r,c in qstate[j].items()}
  elif kind!='MOVE':raise ValueError(kind)
 L={r:qstate[raw[r]] for r in mainroles};want={r:T[r].copy() for r in mainroles}
 for x in src['hosted']['X2']:want[x]={x:F(1)}
 need(L==want,'actual400 private rows; exactly96 missing hosted reverse terms')
 inverse={r:{r:F(1)} for r in mainroles}
 for i,x in enumerate(src['live']):
  y=x+112
  if i in D:inverse[y]={y:F(1),x:F(-1)}
  else:inverse[x]={x:F(1,2),y:F(1)};inverse[y]={y:F(1),x:F(-1,2)}
 for r,row in inverse.items():
  check={}
  for s,c in row.items():add(check,L[s],c)
  need(check=={r:F(1)},'all400 explicit inverse rows')
 physical=h.typed(src,w);need(dict(physical['counts'])==report['word']['counts'] and physical['peak']==43,'literal physical counts and peak')
 need({str(r):c for r,c in physical['ranks'].items()}==report['word']['MOVE_rank_histogram'],'actual MOVE rank histogram')
 need(physical['rawranks']==Counter({8:400}) and all(physical['final_locations'][raw[r]]==src['final'][r] for r in mainroles),'raw charts and profile')
 nativeprofile=Counter(abs(len(src['frames'][o[3]])-len(src['frames'][o[2]])) for o in src['program'] if o[0]=='MOVE');newpaid=physical['ranks']-nativeprofile-physical['rawranks'];need(newpaid==Counter({1:112}),'all112 new packets charged')
 # The terminal common rows are formal s_j=(Tu)_j; the private rows are s_r+Lq.
 # Restricting to hosted qY2 leaves96 independent facet fields and zero hub span.
 donorY=set(src['hosted']['Y2']);need(len(donorY)==96 and all(src['final'][x]==127 for x in src['hosted']['X2']),'96 target outputs at hub')
 for r,row in L.items():need({y:c for y,c in row.items() if y in donorY}==({r:F(1)} if r in donorY else {}),'sole terminal occurrences of each independent hosted qY2')
 need(all(len(src['frames'][src['final'][y]])==8 and src['final'][y]!=127 for y in donorY),'all96 sole donor fields on proper facets')
 terminal={j:{j:F(1)} for j in range(n)}
 for r in mainroles:
  terminal[raw[r]]={r:F(1)}
  for s,c in L[r].items():terminal[raw[r]][raw[s]]=c
 suffix=[]
 for p,x,y in zip(src['hosted']['Dports'],src['hosted']['X2'],src['hosted']['Y2']):
  facet=src['final'][y];need(facet==src['final'][src['live'][p]+112],'repair uses inverse of an existing forward packet map')
  suffix.extend([['INIT',tmp,facet],['ADD',tmp,raw[y],'1',facet],['ADD',tmp,y,'-1',facet],['MOVE',tmp,facet,127,True],['ADD',raw[x],tmp,'-1',127],['CLEAR',tmp,127]])
 for o in suffix:
  kind,j=o[:2]
  if kind=='INIT':terminal[j]={}
  elif kind=='CLEAR':del terminal[j]
  elif kind=='ADD':add(terminal[j],terminal[o[2]],F(o[3]))
  elif kind!='MOVE':raise ValueError(kind)
 for r in mainroles:
  expected={r:F(1)}
  for s,c in T[r].items():expected[raw[s]]=c
  need(terminal[raw[r]]==expected,'attaining suffix completes every private native main row')
 need(all(terminal[j]=={j:F(1)} for j in range(n)),'attaining suffix preserves every common endpoint')
 appended=h.typed(src,dict(w,program=P+suffix));need(appended['peak']==43 and appended['ranks']-physical['ranks']==Counter({1:96}),'actual96 rank1 inbound packets with unchanged peak')
 appendix={'schema':'independent-append-only-hosted-repair-v1','terminal_word_payload_sha256':PAY,'public':1880,'owned_fields':w['owned_fields'],'program':suffix,'scope':'Copy privateY2 minus cochart commonY2; one rank1 inward field per hosted reverse. Actual576-operation suffix,96 inbound packets and288 ADDs.'}
 ab=json.dumps(appendix,sort_keys=True,separators=(',',':')).encode();(OUT/'APPENDIX-WORD.json').write_bytes(ab+b'\n')
 invoice_bytes=(REPO/'research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json').read_bytes();need(digest(invoice_bytes)==IPIN,'authentic H4 invoice');invoice=json.loads(invoice_bytes);targets={int(r):c for r,c in invoice['T4'].items()};oldpaid={int(r):c for r,c in invoice['P4'].items()};newraw=Counter({8:400})
 paid={r:oldpaid.get(r,0)+18*(newraw[r]-oldprofile[r])+18*newpaid[r] for r in oldpaid.keys()|oldprofile.keys()|newraw.keys()|newpaid.keys()}
 bill=report['cost'];need(sum(oldprofile.values())==1710 and sum(r*c for r,c in oldprofile.items())==3200,'original1710-call raw invoice')
 need({str(r):c for r,c in paid.items()}==bill['paid_histogram'] and {str(r):c for r,c in targets.items()}==bill['T4'],'complete actual conditional caller histogram')
 need(all(c>=0 for c in paid.values()) and sum(paid.values())==bill['paid_positions']==130860 and sum(targets.values())==bill['target_positions']==27344,'nonnegative full paid and target counts')
 surplus=sum(r*(targets.get(r,0)-paid.get(r,0)) for r in targets.keys()|paid.keys());need(surplus==bill['rank_surplus']==3040,'exact rank surplus')
 powers={r:h.root_bracket(r) for r in targets.keys()|oldpaid.keys()|paid.keys()};saving=h.moment_interval({r:oldprofile[r]-newraw[r] for r in oldprofile.keys()|newraw.keys()},powers);margin=tuple(v/18 for v in h.moment_interval({r:targets.get(r,0)-paid.get(r,0) for r in targets.keys()|paid.keys()},powers))
 need(F(bill['saved_moment_bounds'][0])<=saving[0]<=saving[1]<=F(bill['saved_moment_bounds'][1]),'exact raw-saving enclosure')
 need(F(bill['remaining_moment_per_native_bounds'][0])<=margin[0]<=margin[1]<=F(bill['remaining_moment_per_native_bounds'][1]),'exact complete remaining-margin enclosure')
 need(6<margin[0]<=margin[1]<7,'sharp integer ceiling of6 additional positive-rank field calls for this fixed invoice')
 appendmargin=tuple(v-96 for v in margin);need(appendmargin[1]<0,'sharp96-field append repair exceeds this fixed budget')
 charts=json.loads((PACK/'CHART-MAPS.json').read_text());oldmaps={(o[2],o[3]) for o in src['program'] if o[0]=='MOVE'};newmaps={(o[2],o[3]) for o in P if o[0]=='MOVE'};introduced=newmaps-oldmaps
 need(len(charts['recipes'])==len(introduced)==309 and {(r['source'],r['target']) for r in charts['recipes']}==introduced,'all309 introduced maps covered')
 for r in charts['recipes']:need(r['recipe']['rank']==abs(len(src['frames'][r['target']])-len(src['frames'][r['source']])),'correct absolute rank for both up and down transports')
 need(charts['source_sha256']==charts['parent_sha256']==SPIN and charts['word_sha256']==WPIN and charts['wrong_global_phase_rejected'],'exact chart receipt interface')
 for name,pin in charts['engine_pins'].items():need(digest((REPO/'research/shared-wire-split-composition/frozen'/name).read_bytes())==pin,'frozen chart engine')
 wrong_x=coupled[0];wrong_y=wrong_x+112;wrong={wrong_x:F(2)};add(wrong,L[wrong_y],F(-1));err=wrong.copy();add(err,L[wrong_x],F(-1));need(err=={wrong_x:F(1,2),wrong_y:F(1,2)},'wrong reverse coefficient creates a nonzero half-sum')
 result={'status':'PASS_INDEPENDENT_COMPLETE_FIRST_FAMILY_AND_SHARP_APPEND_BOUNDARY','source_sha256':SPIN,'word_compressed_sha256':WPIN,'word_payload_sha256':PAY,'source_main_endpoint_identities_on1480_inputs':400,'common_native_operations_literal':71261,'entry_differences':400,'final_recouplings':400,'instructions':len(P),'counts':dict(physical['counts']),'MOVE_profile':dict(sorted(physical['ranks'].items())),'actual_raw_MOVEs':400,'actual_raw_profile':{8:400},'actual_paid_packet_profile':{1:112},'forward_packets':104,'coupled_reverse_packets':8,'all_first_pairs_completed':104,'hosted_reverse_remaining':96,'private_inverse_rows_verified':400,'peak_owned':physical['peak'],'no_terminal_owned_fields':True,'terminal_hosted_qY2_support':'Each independent hosted qY2 occurs solely in its one privateY2 facet field; all other current fields have zero coefficient. A clean qY2 is acquired there as privateY2 minus cochart commonY2.','introduced_chart_recipe_pairs_checked_for_pins_coverage_rank':309,'actual_conditional_paid_histogram':dict(sorted(paid.items())),'conditional_target_positions':27344,'conditional_paid_positions':130860,'conditional_rank_surplus':3040,'saved_raw_moment_exact_bounds':[str(v) for v in saving],'saved_raw_moment_approximate':float(saving[0]),'remaining_moment_exact_bounds':[str(v) for v in margin],'remaining_moment_approximate':float(margin[0]),'fixed_invoice_further_positive_rank_field_ceiling':6,'append_only_inbound_hub_field_lower_bound':96,'append_only_recursive_moment_minimum':96,'attaining_suffix_instructions':len(suffix),'attaining_suffix_ADDs':288,'attaining_suffix_rank1_MOVEs':96,'attaining_suffix_INIT_CLEAR_pairs':96,'attaining_suffix_sha256':digest(ab+b'\n'),'attaining_full_word_instructions':len(P)+len(suffix),'attaining_full_word_counts':dict(appended['counts']),'attaining_full_word_peak_owned':appended['peak'],'remaining_margin_after_sharp_append_repair_bounds':[str(v) for v in appendmargin],'remaining_margin_after_sharp_append_repair_approximate':float(appendmargin[0]),'negative_controls':{'wrong_coupled_reverse_coefficient':{str(r):str(c) for r,c in err.items()},'omitting_eight_reverse_call_fees_spuriously_adds_moment':8,'copying_terminal_privateY2_without_subtracting_common':'Leaves a common-Y2 contamination; the explicit suffix includes its subtraction.'},'scope':'Independent source endpoint adjoints, literal400+400+native+112-packet+400 word partition, full actual physical walk,400-variable private replay/inverse and complete exact caller invoice. Sharp96-field cut applies only to appending from this terminal state, with no unrecorded history or free communication; joint replanning is not bounded. Chart-engine recipe verification is inherited and credited, not re-authored. All general physical, compiler, scalar and supplier obligations remain.'}
 (OUT/'REVIEW-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
