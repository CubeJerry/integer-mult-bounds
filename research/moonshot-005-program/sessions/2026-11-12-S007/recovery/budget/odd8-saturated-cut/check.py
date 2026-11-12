#!/usr/bin/env python3
import argparse,gzip,hashlib,json,time
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from decimal import Decimal,localcontext
HERE=Path(__file__).resolve().parent
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
INVOICE_PIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
CHOSEN=[24,103,0,32,97,72,37,86]
DEN=10**24

def need(ok,message):
 if not ok:raise ValueError(message)
def span(frame):
 s={0}
 for a in frame:s.update(v^a for v in tuple(s))
 return frozenset(s)
def rank_certificate(rows,allowed_columns):
 basis={};pivots=[];det=Q(1)
 for label,row in rows:
  a={k:v for k,v in row.items() if k in allowed_columns}
  while a:
   p=min(a);q=a[p]
   if p not in basis:
    basis[p]={k:v/q for k,v in a.items()};pivots.append({'output_role':label,'input_role':p,'pivot':str(q)});det*=q;break
   for k,v in basis[p].items():
    u=a.get(k,Q(0))-q*v
    if u:a[k]=u
    else:a.pop(k,None)
 return {'rank':len(basis),'minor_pivots':pivots,'minor_determinant':str(det)}
def addto(a,b,c):
 for k,v in tuple(b.items()):
  q=a.get(k,Q(0))+c*v
  if q:a[k]=q
  else:a.pop(k,None)
def root_floor(value,degree):
 x=1<<((value.bit_length()+degree-1)//degree)
 while True:
  y=((degree-1)*x+value//x**(degree-1))//degree
  if y>=x:break
  x=y
 while (x+1)**degree<=value:x+=1
 while x**degree>value:x-=1
 need(x**degree<=value<(x+1)**degree,'integer power enclosure');return x
def power(r):
 v=r**199*DEN**200;x=root_floor(v,200);return x,x if x**200==v else x+1
def decimal(q):
 with localcontext() as c:c.prec=50;return str(Decimal(q.numerator)/Decimal(q.denominator))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds'));ap.add_argument('--out',type=Path,default=HERE/'RESULT.json');args=ap.parse_args();start=time.monotonic()
 src=args.repo/'research/shared-wire-split-composition/data/final.json.gz';raw=src.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'immutable native source');w=json.loads(gzip.decompress(raw));P=w['program'];n=w['public'];need(n==1480,'common public dimension')
 frames=list(map(span,w['frames']));ports=[w['ports'][i] for i in CHOSEN];inside=[any(a in f for a in ports) for f in frames];Dports=w['hosted']['Dports'];need(len(set(CHOSEN))==8 and set(CHOSEN)<=set(Dports),'eight distinct hosted ports');need(all((a&b).bit_count()%2==1 for a in ports for b in ports),'all64 binary pairings odd')
 pairs=[{'port_index':i,'port':w['ports'][i],'first_X':w['live'][i],'X2':w['hosted']['X2'][Dports.index(i)],'Y2':w['hosted']['Y2'][Dports.index(i)]} for i in CHOSEN]
 in0={j for j,c in enumerate(w['initial']) if inside[c]};inf={j for j,c in enumerate(w['final']) if inside[c]};outside0=set(range(n))-in0
 target=[{j:Q(1)} for j in range(n)]
 for i,x in enumerate(w['live']):
  y=x+112
  if i in Dports:target[y][x]=Q(1)
  else:target[x][y]=Q(-1);target[y]={x:Q(1,2),y:Q(1,2)}
 for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):target[x][y]=Q(-1)
 M=set(w['live'])|{x+112 for x in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(len(M)==400,'400 raw mains')
 common_rank=rank_certificate([(j,target[j]) for j in sorted(inf)],outside0)
 private_rank=rank_certificate([(j,target[j]) for j in sorted(inf&M)],outside0&M)
 incoming=[];outgoing=[];oldraw=Counter();raw_cross=Counter()
 for t,e in enumerate(P):
  if e[0]!='MOVE':continue
  _,j,a,b,owned=e;need((frames[a]<frames[b]) if not owned else(frames[a]<frames[b] or frames[b]<frames[a]),'nested source MOVE')
  item={'event':t,'role':j,'from':a,'to':b,'owned':owned,'rank':abs(len(w['frames'][b])-len(w['frames'][a]))}
  if not inside[a] and inside[b]:incoming.append(item)
  if inside[a] and not inside[b]:outgoing.append(item)
  if j in M:
   need(not owned and frames[a]<frames[b],'raw-source public ascent');oldraw[item['rank']]+=1
   if not inside[a] and inside[b]:raw_cross[j]+=1
 for j in M:
  need(frames[w['initial'][j]]<frames[w['final'][j]],'direct raw ascent');need(len(w['frames'][w['final'][j]])-len(w['frames'][w['initial'][j]])==8,'direct rank8')
  need(raw_cross[j]==int(j in outside0 and j in inf),'one raw cut entry fixed by endpoints')
 raw_in=sum(raw_cross.values());need(oldraw.total()==1710 and sum(k*v for k,v in oldraw.items())==3200,'original raw invoice')
 forward=[{'type':'first_Y_forward','port_index':i,'from':127,'to':w['final'][x+112]} for i,x in enumerate(w['live'])]
 returns=[{'type':'coupled_reverse','port_index':i,'from':w['final'][x+112],'to':127} for i,x in enumerate(w['live']) if i not in set(Dports)]
 for e in forward+returns:need(abs(len(w['frames'][e['from']])-len(w['frames'][e['to']]))==1,'reserved packet rank1')
 packet_in=[e for e in forward+returns if not inside[e['from']] and inside[e['to']]];packet_out=[e for e in forward+returns if inside[e['from']] and not inside[e['to']]]
 need(len(forward)==104 and len(returns)==8 and not packet_in,'reserved112 legs have no inward crossing')
 outside_facets=[i for i,x in enumerate(w['live']) if not inside[w['final'][x+112]]];need(set(outside_facets)==set(CHOSEN),'exactly eight selected active facets outside')
 funded=len(incoming)+raw_in+len(packet_in);required=common_rank['rank']+private_rank['rank'];gap=required-funded
 need((len(in0),len(inf),common_rank['rank'],private_rank['rank'],len(incoming),raw_in,gap)==(53,1300,1255,376,1255,368,8),'exact rank and capacity ledger')
 # Reauthenticate the native's complete inside public-output map on all common inputs.
 adj=[{j:Q(1)} if j in inf else{} for j in range(n)]+[{} for _ in range(w['owned_fields'])]
 for e in reversed(P):
  op,j=e[:2]
  if op in ('INIT','CLEAR'):adj[j]={}
  elif op=='ADD':addto(adj[e[2]],adj[j],Q(e[3]))
  elif op=='SCALE':adj[j]={k:Q(e[2])*v for k,v in adj[j].items()}
  elif op=='COPY':addto(adj[e[2]],adj[j],Q(e[3]));adj[j]={}
 expected=[{} for _ in range(n)]
 for j in inf:
  for k,v in target[j].items():expected[k][j]=v
 need(adj[:n]==expected,'fresh full-source inside-output Jacobian')
 print('Source/rank/capacity verified',required,funded,gap,'seconds',round(time.monotonic()-start,2),flush=True)
 partial=[dict(row) for row in target]
 for x,y in zip(w['hosted']['X2'],w['hosted']['Y2']):partial[x].pop(y,None)
 partial_rank=rank_certificate([(j,partial[j]) for j in sorted(inf&M)],outside0&M)
 mutated=[dict(row) for row in target];mutated[pairs[0]['X2']].pop(pairs[0]['Y2'])
 mutated_rank=rank_certificate([(j,mutated[j]) for j in sorted(inf&M)],outside0&M)
 need((partial_rank['rank'],mutated_rank['rank'])==(368,375),'target-mutation negative controls')
 extra_channels=[]
 for p in pairs:
  a=w['final'][p['Y2']];b=127
  need(not inside[a] and inside[b] and frames[a]<frames[b] and len(w['frames'][b])-len(w['frames'][a])==1,'eight rank1 cut-filling witnesses')
  extra_channels.append({'role':p['Y2'],'from':a,'to':b,'rank':1})
 ip=args.repo/'research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json';ib=ip.read_bytes();need(hashlib.sha256(ib).hexdigest()==INVOICE_PIN,'inherited invoice pin');iv=json.loads(ib)
 T=Counter({int(r):v for r,v in iv['T4'].items()});oldP=Counter({int(r):v for r,v in iv['P4'].items()});newP=oldP.copy()
 for r,v in oldraw.items():newP[r]-=18*v
 newP[8]+=18*400;newP[1]+=18*112
 need(all(v>=0 for v in newP.values()) and sum(newP.values())==130860,'complete direct comparison paid profile')
 powers={r:power(r) for r in set(T)|set(oldP)|set(oldraw)|{1,8,9}}
 def moment(hist):
  lo=sum(v*powers[r][0 if v>=0 else 1] for r,v in hist.items());hi=sum(v*powers[r][1 if v>=0 else 0] for r,v in hist.items());return Q(lo,DEN),Q(hi,DEN)
 base=T.copy();base.subtract(oldP);blo,bhi=(x/18 for x in moment(base))
 save=oldraw.copy();save[8]-=400;slo,shi=moment(save)
 margin=T.copy();margin.subtract(newP);lo,hi=(x/18 for x in moment(margin));need(6<lo<=hi<7<gap,'strict eight-field budget failure')
 deficit=(Q(gap)-hi,Q(gap)-lo)
 c_lo=Q(powers[9][0],9*DEN);r8_hi=Q(powers[8][1],DEN)
 raw_cycle_slack=10*c_lo-r8_hi-1;raw_cycle_slope=2*c_lo-1
 need(raw_cycle_slack>0 and raw_cycle_slope>0,'arbitrary nested raw-route charging inequality')
 even_frame=[(1<<k)^256 for k in range(8)];even_space=span(even_frame)
 need(len(even_space)==256 and even_space<frames[127] and all(x.bit_count()%2==0 for x in even_space),'even hyperplane rank1 hub edge')
 need(len(w['ports'])==104 and all(a.bit_count()%2==1 for a in w['ports']),'all104 active ports odd')
 need(not any(a in even_space for a in w['ports']),'universal edge crosses every nonempty odd-port-generated cut')
 endpoint_classes=Counter(('inside' if j in in0 else 'outside')+'->'+('inside' if j in inf else 'outside') for j in M)
 out={
  'status':'PASS_EXACT_SATURATED_SPATIAL_CUT',
  'source_sha256':PIN,'invoice_sha256':INVOICE_PIN,
  'chosen_port_indices':CHOSEN,'chosen_pairs':pairs,
  'odd_pairing_matrix':[[(a&b).bit_count()%2 for b in ports] for a in ports],
  'inside_chart_ids':[c for c,b in enumerate(inside) if b],
  'inside_initial_common_roles':sorted(in0),'inside_final_common_roles':sorted(inf),
  'inside_initial_private_roles':sorted(in0&M),'inside_final_private_roles':sorted(inf&M),
  'common_conditional_matrix':{'rows':[{'output_role':j,'outside_input_coefficients':[[k,str(v)] for k,v in sorted(target[j].items()) if k in outside0]} for j in sorted(inf)],**common_rank},
  'private_conditional_matrix':{'rows':[{'output_role':j,'outside_input_coefficients':[[k,str(v)] for k,v in sorted(target[j].items()) if k in outside0&M]} for j in sorted(inf&M)],**private_rank},
  'native_inward_MOVEs':incoming,'native_outward_MOVEs':outgoing,
  'native_inward_count_by_ownership':dict(Counter('owned' if e['owned'] else 'public' for e in incoming)),
  'raw_endpoint_classes':dict(sorted(endpoint_classes.items())),
  'raw_inward_roles':sorted(raw_cross),
  'reserved_packet_legs':forward+returns,'reserved_inward_legs':packet_in,'reserved_outward_legs':packet_out,
  'required_conditional_rank':required,'funded_inward_field_capacity':funded,'additional_inward_field_lower_bound':gap,
  'negative_controls':{
   'omit_all96_private_hosted_reverse_terms':{'private_rank':partial_rank['rank'],'deficit':common_rank['rank']+partial_rank['rank']-funded},
   'omit_first_selected_private_hosted_reverse_term':{'omitted_X2':pairs[0]['X2'],'omitted_Y2':pairs[0]['Y2'],'private_rank':mutated_rank['rank'],'deficit':common_rank['rank']+mutated_rank['rank']-funded},
   'eight_rank1_extra_inward_legs_fill_cut_capacity_only':extra_channels,
  },
 }
 out['moment']={
  'exponent':'199/200','power_denominator':str(DEN),
  'integer_power_enclosures':{str(r):[str(a),str(b)] for r,(a,b) in sorted(powers.items())},
  'native_repetitions':18,'T4':dict(sorted(T.items())),
  'P4_original':dict(sorted(oldP.items())),
  'raw_original_histogram':dict(sorted(oldraw.items())),
  'raw_direct_histogram':{'8':400},
  'P4_direct_plus112_rank1':dict(sorted((r,v) for r,v in newP.items() if v)),
  'paid_count':sum(newP.values()),
  'base_margin_bounds':[str(blo),str(bhi)],
  'raw_direct_saving_bounds':[str(slo),str(shi)],
  'remaining_margin_bounds':[str(lo),str(hi)],
  'remaining_margin_decimal_bounds':[decimal(lo),decimal(hi)],
  'additional_paid_moment_lower_bound':8,
  'deficit_bounds':[str(x) for x in deficit],
  'deficit_decimal_bounds':[decimal(x) for x in deficit],
  'nonmonotone_raw_route_extension':{
   'max_MOVE_rank':9,'net_raw_dimension_increase':8,
   'cycle_slack_rational_lower_bound':str(raw_cycle_slack),
   'cycle_slope_rational_lower_bound':str(raw_cycle_slope),
   'claim':'Every nested raw path of the same endpoints costs at least 8^(199/200) plus its inward cut crossings beyond the endpoint-implied 0 or 1. Extra cut entries therefore cannot be hidden by rerouting a raw carrier.',
  },
 }
 out['scope']={
  'native_common_slots':'Keep the native common MOVE chart endpoints and multiplicities. Payloads, local operations, and chronology may be recoded arbitrarily.',
  'raw_paths':'400 raw carrier paths retain their initial and final charts. Monotone paths have exactly 368 inward entries; arbitrary nested paths have their extra inward entries charged by the proved moment inequality.',
  'reserved_packets':'104 hub-to-firstY facet legs and 8 unhosted facet-to-hub legs keep their chart endpoints, but may be arbitrarily recoded. All 112 contribute zero inward cut capacity.',
  'local_information':'All initial inside common and private fields are conditioned upon; all inside final common and private fields must have their required target values. This permits global inside decoding, arbitrary dirty mixtures, and feedback. No fixed-original-history premise is used.',
  'budget':'Use the inherited H4 target and all source reservations, replacing only 1710 raw legs by 400 direct rank8 legs and adding the 112 comparison rank1 legs. Apply per native template; no unrestricted cross-template coding theorem is asserted.',
  'not_claimed':'No obstruction for a changed common MOVE skeleton, changed reserved packet endpoints, or another unpaid source of cross-cut communication; no global kappa impossibility or sufficiency of eight added legs for all 96 duties.',
 }
 out['universal_edge_weighting_limit']={
  'even_hyperplane_normal':511,'even_hyperplane_frame':even_frame,
  'even_hyperplane_source_chart_ids':[i for i,f in enumerate(frames) if f==even_space],
  'all104_active_ports_have_odd_parity':True,'all96_hosted_ports_have_odd_parity':True,
  'edge_to_hub':{'rank':1,'moment':1},
  'proposition':'For every nonempty cut generated upward by odd active port lines, the even-parity hyperplane is outside and the full hub is inside. Hence every nonnegative weighted family of eight-deficit cuts, normalized against all allowed nested binary-chart MOVEs, has sum(weights)<=1 and objective<=8.',
  'scope':'This bounds the strength of that spatial-cut dual. It neither provides informative fields at the even hyperplane nor asserts an eight-call completion. Acquisition and decoding costs remain unpriced by these cuts.',
 }
 args.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'required':required,'funded':funded,'additional_fields':gap,'margin':[decimal(lo),decimal(hi)],'moment_deficit':[decimal(x) for x in deficit],'raw_route_cycle_slack':decimal(raw_cycle_slack),'output':str(args.out)},indent=2),flush=True)

if __name__=='__main__':main()
