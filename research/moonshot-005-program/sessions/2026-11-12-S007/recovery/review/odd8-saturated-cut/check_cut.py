#!/usr/bin/env python3
"""Independent exact audit. Never imports the cut author's code."""
import gzip,hashlib,importlib.util,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
BASE=Path('/workspace/scratch/6a77123a1d61');REPO=BASE/'integer-mult-bounds';HERE=Path(__file__).resolve().parent
PACK=BASE/'worker-budget/odd8-saturated-cut'
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
RPIN='7c2e7f7d1c4db2c82ec020048432f7d5ef5a9244bc7fae3485aa711585994a51'
PPIN='2aae4529ce79f6918386ef0da0c13cb0fcdef4673f228397de27563e66b02fa4'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
PORTS=[24,103,0,32,97,72,37,86]
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(path,pin):
 b=path.read_bytes();need(sha(b)==pin,'pin: '+str(path));return json.loads(gzip.decompress(b) if path.suffix=='.gz' else b)
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in tuple(s)}
 return s
def axpy(dst,src,a):
 for k,v in tuple(src.items()):
  z=dst.get(k,F(0))+a*v
  if z:dst[k]=z
  else:dst.pop(k,None)
def rank(rows):
 # Deliberately reverse pivot ordering relative to the author's elimination.
 piv={}
 for row in rows:
  x=dict(row)
  while x:
   p=max(x);a=x[p]
   if p not in piv:piv[p]={k:v/a for k,v in x.items()};break
   axpy(x,piv[p],-a)
 return len(piv)
def determinant(rows,cols):
 # A separate pivoted sparse determinant of the explicit listed square minor.
 a=[{j:row[k] for j,k in enumerate(cols) if k in row} for row in rows];d=F(1);n=len(a)
 for j in range(n):
  p=next((i for i in range(j,n) if a[i].get(j)),None)
  if p is None:return F(0)
  if p!=j:a[p],a[j]=a[j],a[p];d=-d
  q=a[j][j];d*=q
  for i in range(j+1,n):
   if a[i].get(j):axpy(a[i],a[j],-a[i][j]/q)
 return d
def source_outputs(s,wanted):
 # Simultaneous exact reverse propagation of named output probes.
 v=[{} for _ in range(s['public']+s['owned_fields'])]
 for j in wanted:v[j][j]=F(1)
 for op in reversed(s['program']):
  k,j=op[:2]
  if k=='ADD':axpy(v[op[2]],v[j],F(op[3]))
  elif k=='SCALE':v[j]={r:a*F(op[2]) for r,a in v[j].items()}
  elif k=='COPY':axpy(v[op[2]],v[j],F(op[3]));v[j]={}
  elif k in ('INIT','CLEAR'):v[j]={}
  elif k!='MOVE':raise ValueError(k)
 out={j:{} for j in wanted}
 for i,col in enumerate(v[:s['public']]):
  for j,a in col.items():out[j][i]=a
 need(not any(v[s['public']:]),'no nonexistent owned input dependence')
 return out
def main():
 s=load(REPO/'research/shared-wire-split-composition/data/final.json.gz',SPIN)
 cert=load(PACK/'RESULT.json',RPIN);need(sha((PACK/'PROOF.md').read_bytes())==PPIN,'frozen proof')
 n=s['public'];need(n==1480 and len(s['initial'])==len(s['final'])==n,'source size')
 spaces=[span(v) for v in s['frames']]
 need(all(len(a)==2**len(b) and a<=set(range(512)) for a,b in zip(spaces,s['frames'])),'independent ambient-nine chart bases')
 ports=[s['ports'][i] for i in PORTS];host=set(s['hosted']['Dports']);xs=s['live']
 need(len(set(ports))==8 and set(PORTS)<=host,'eight hosted ports')
 pairings=[[(a&b).bit_count()%2 for b in ports] for a in ports]
 need(pairings==[[1]*8 for _ in range(8)]==cert['odd_pairing_matrix'],'all ordered binary dot products')
 inside={c for c,v in enumerate(spaces) if any(p in v for p in ports)}
 need(127 in inside and spaces[127]==set(range(512)) and 3 not in inside and spaces[3]=={0},'hub and zero side')
 M=set(xs)|{x+112 for x in xs}|set(s['hosted']['X2'])|set(s['hosted']['Y2']);need(len(M)==400,'main roles')
 I={j for j,c in enumerate(s['initial']) if c in inside};O={j for j,c in enumerate(s['final']) if c in inside}
 for key,val in [('inside_chart_ids',inside),('inside_initial_common_roles',I),('inside_final_common_roles',O),('inside_initial_private_roles',I&M),('inside_final_private_roles',O&M)]:need(cert[key]==sorted(val),'complete '+key)
 need((len(inside),len(I),len(O),len(I&M),len(O&M))==(377,53,1300,16,384),'cut dimensions')
 loc=dict(enumerate(s['initial']));inc=[];out=[];rawhist=Counter();rawentries=Counter();counts=Counter()
 for event,op in enumerate(s['program']):
  k,j=op[:2];counts[k]+=1
  if k=='INIT':need(j>=n and j not in loc,'INIT');loc[j]=op[2]
  elif k=='CLEAR':need(j>=n and loc.get(j)==op[2],'CLEAR');del loc[j]
  elif k=='MOVE':
   _,_,a,b,owned=op;need(loc.get(j)==a and owned==(j>=n),'actual MOVE endpoint and ownership')
   need(spaces[a]<spaces[b] or (owned and spaces[b]<spaces[a]),'native nesting')
   r=abs(len(s['frames'][a])-len(s['frames'][b]));rec={'event':event,'role':j,'from':a,'to':b,'owned':owned,'rank':r}
   if a not in inside and b in inside:inc.append(rec)
   if a in inside and b not in inside:out.append(rec)
   if j in M:
    need(not owned and spaces[a]<spaces[b],'original raw reservation is an ascent');rawhist[r]+=1
    if a not in inside and b in inside:rawentries[j]+=1
   loc[j]=b
  elif k in ('ADD','COPY'):need(j!=op[2] and loc[j]==loc[op[2]]==op[4],'local source arithmetic')
  elif k=='SCALE':need(loc[j]==op[3] and F(op[2])!=0,'local invertible scale')
  else:raise ValueError(k)
 need(loc==dict(enumerate(s['final'])),'actual complete native final locations')
 need(inc==cert['native_inward_MOVEs'] and out==cert['native_outward_MOVEs'],'entire funded crossing census')
 need(len(inc)==1255 and Counter(x['owned'] for x in inc)==Counter({False:1247,True:8}) and len(out)==8 and all(x['owned'] for x in out),'common crossing capacities')
 endpointclasses=Counter()
 for j in M:
  a,b=s['initial'][j],s['final'][j];need(spaces[a]<spaces[b] and len(s['frames'][b])-len(s['frames'][a])==8,'all400 nested endpoint gaps')
  need(rawentries[j]==int(j not in I and j in O),'raw endpoint crossing indicator')
  endpointclasses[('inside' if j in I else 'outside')+'->'+('inside' if j in O else 'outside')]+=1
 need(dict(endpointclasses)==cert['raw_endpoint_classes'] and sorted(rawentries)==cert['raw_inward_roles'],'raw endpoint classes')
 need(sum(rawentries.values())==368 and rawhist==Counter({1:990,2:360,3:105,4:112,5:133,6:8,7:2}),'368 extra raw entries and1710 old calls')
 legs=[{'type':'first_Y_forward','port_index':i,'from':127,'to':s['final'][x+112]} for i,x in enumerate(xs)]
 legs +=[{'type':'coupled_reverse','port_index':i,'from':s['final'][x+112],'to':127} for i,x in enumerate(xs) if i not in host]
 need(legs==cert['reserved_packet_legs'] and len(legs)==112,'exact fixed paid packet endpoints')
 need(all(abs(len(s['frames'][e['from']])-len(s['frames'][e['to']]))==1 and (spaces[e['from']]<spaces[e['to']] or spaces[e['to']]<spaces[e['from']]) for e in legs),'all112 rank-one nested legs')
 need(not any(e['from'] not in inside and e['to'] in inside for e in legs),'no reserved inward capacity')
 need([e for e in legs if e['from'] in inside and e['to'] not in inside]==cert['reserved_outward_legs'],'exact eight outward forward legs')
 need({i for i,x in enumerate(xs) if s['final'][x+112] not in inside}==set(PORTS),'only selected active facets outside')
 target={j:{j:F(1)} for j in range(n)}
 for i,x in enumerate(xs):
  y=x+112
  if i in host:target[y][x]=F(1)
  else:target[x][y]=F(-1);target[y]={x:F(1,2),y:F(1,2)}
 for x,y in zip(s['hosted']['X2'],s['hosted']['Y2']):target[x][y]=F(-1)
 actual=source_outputs(s,O);need(actual=={j:target[j] for j in O},'fresh exact source adjoints on all1480 inputs')
 need(all(set(actual[j])<=M for j in O&M),'private inside target has no common helper dependence')
 resultmat={}
 for name,outputs,columns in [('common',O,set(range(n))-I),('private',O&M,M-I)]:
  rows={j:{k:v for k,v in actual[j].items() if k in columns} for j in sorted(outputs)}
  a=cert[name+'_conditional_matrix'];serial=[{'output_role':j,'outside_input_coefficients':[[k,str(v)] for k,v in sorted(row.items())]} for j,row in rows.items()]
  need(a['rows']==serial,'entire source-derived '+name+' conditional matrix')
  r=rank(rows.values());pivs=a['minor_pivots'];rr=[e['output_role'] for e in pivs];cc=[e['input_role'] for e in pivs]
  need(r==a['rank']==len(rr)==len(set(rr))==len(set(cc)),name+' exact rank and minor dimensions')
  need(set(rr)<=set(rows) and set(cc)<=columns,'minor labels')
  det=determinant([rows[j] for j in rr],cc);need(det==F(a['minor_determinant'])==1,'independent '+name+' determinant-one minor')
  resultmat[name]={'rank':r,'rows':len(rows),'outside_columns':len(columns),'minor_determinant':str(det),'matrix_sha256':sha(json.dumps(serial,sort_keys=True,separators=(',',':')).encode())}
 need([resultmat[x]['rank'] for x in ['common','private']]==[1255,376],'1631 conditional dimensions')
 required=sum(x['rank'] for x in resultmat.values());funded=len(inc)+sum(rawentries.values());need((required,funded,required-funded)==(1631,1623,8),'eight-field capacity gap')
 selected=[]
 for i in PORTS:
  k=s['hosted']['Dports'].index(i);x=s['hosted']['X2'][k];y=s['hosted']['Y2'][k]
  selected.append({'port_index':i,'port':s['ports'][i],'first_X':xs[i],'X2':x,'Y2':y})
 need(selected==cert['chosen_pairs'],'chosen actual X2/Y2 pairs')
 p0={j:dict(actual[j]) for j in O&M}
 for x,y in zip(s['hosted']['X2'],s['hosted']['Y2']):
  if x in p0:p0[x].pop(y,None)
 minus96=rank({k:v for k,v in row.items() if k in M-I} for row in p0.values())
 p1={j:dict(actual[j]) for j in O&M};p1[selected[0]['X2']].pop(selected[0]['Y2'])
 minus1=rank({k:v for k,v in row.items() if k in M-I} for row in p1.values())
 need((minus96,minus1)==(368,375),'reverse-coefficient causal controls')
 fill=[{'role':d['Y2'],'from':s['final'][d['Y2']],'to':127,'rank':1} for d in selected]
 need(fill==cert['negative_controls']['eight_rank1_extra_inward_legs_fill_cut_capacity_only'],'eight filling edge witnesses')
 need(all(e['from'] not in inside and spaces[e['from']]<spaces[127] and len(spaces[e['from']])==256 for e in fill),'actual rank-one inward filling geometry')
 # A changed coefficient can retain rank but must fail the source map authentication.
 bad={j:dict(r) for j,r in actual.items()};j=next(j for j,r in bad.items() if j not in M and r=={j:F(1)});bad[j][j]=F(2)
 need(bad!={j:target[j] for j in O},'wrong-source coefficient rejected independently of rank')
 even=span([257,258,260,264,272,288,320,384]);need(len(even)==256 and even<spaces[127] and all(v.bit_count()%2==0 for v in even),'new even hyperplane')
 need(len(s['ports'])==104 and all(p.bit_count()%2==1 and p not in even for p in s['ports']),'universal edge excludes every active port')
 need(not any(p in even for p in ports),'same even edge crosses this cut')
 universal=cert['universal_edge_weighting_limit'];need(universal['even_hyperplane_source_chart_ids']==[i for i,a in enumerate(spaces) if a==even] and universal['even_hyperplane_frame']==[257,258,260,264,272,288,320,384],'universal edge certificate geometry')
 iv=load(REPO/'research/moonshot-005-program/results/eight-packet-budget-and-reverse/INVOICE-SOURCE.json',IPIN)
 T=Counter({int(k):v for k,v in iv['T4'].items()});P=Counter({int(k):v for k,v in iv['P4'].items()});Q=P.copy()
 for r,v in rawhist.items():Q[r]-=18*v
 Q[8]+=18*400;Q[1]+=18*112
 need(all(v>=0 for v in Q.values()) and sum(Q.values())==130860 and sum(T.values())==27344,'complete retained paid and target counts')
 need(sum(k*v for k,v in T.items())-sum(k*v for k,v in Q.items())==3040,'retained rank surplus')
 need({str(k):v for k,v in Q.items() if v}==cert['moment']['P4_direct_plus112_rank1'],'entire112-leg billed H4 profile')
 hp=BASE/'worker-review/route-fusion/check_fusion.py';hpin='cd0a90cc2773d144a1c106245d14c5a6f6ee9fad76dca64383a5dc2d7fa04763'
 need(sha(hp.read_bytes())==hpin,'prior independent exact-root helper pin')
 spec=importlib.util.spec_from_file_location('own_moment',hp);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
 powers={r:h.root_bracket(r) for r in set(T)|set(P)|set(rawhist)|{1,8,9}}
 bill=T.copy();bill.subtract(Q);lo,hi=[z/18 for z in h.moment_interval(bill,powers)]
 alo,ahi=map(F,cert['moment']['remaining_margin_bounds']);need(alo<=lo<=hi<=ahi and 6<lo<=hi<7<8,'exact tighter direct-baseline margin enclosure')
 den=int(cert['moment']['power_denominator']);need(den==10**24,'author exact power grid')
 for r,pair in cert['moment']['integer_power_enclosures'].items():
  a,b=map(int,pair);v=int(r)**199*den**200;need(a**200<=v<=b**200 and b-a in (0,1),'every author integer power enclosure')
 c=powers[9][0]/9;slack=10*c-powers[8][1]-1;slope=2*c-1
 need(slack>F(973,1000) and slope>0,'uniform descending-rank charge for all integer detours')
 dt=cert['moment']['nonmonotone_raw_route_extension'];need(F(dt['cycle_slack_rational_lower_bound'])<=slack and F(dt['cycle_slope_rational_lower_bound'])<=slope,'author detour lower bounds')
 need(8-hi>F(17,10),'strict capacity versus budget separation')
 out={
  'status':'PASS_INDEPENDENT_FIELD_LINEAR_SPATIAL_CUT',
  'source_sha256':SPIN,'author_result_sha256':RPIN,'author_proof_sha256':PPIN,'invoice_sha256':IPIN,
  'independent_full_source_adjoint_outputs':len(actual),'independent_initial_common_columns':n,
  'conditional_matrices':resultmat,'inside_chart_count':len(inside),
  'inside_initial_common':len(I),'inside_final_common':len(O),'inside_initial_private':len(I&M),'inside_final_private':len(O&M),
  'chosen_pairs':selected,'odd_pairing_matrix':pairings,
  'native_inward_public':1247,'native_inward_owned':8,'native_outward_owned':8,
  'raw_endpoint_classes':dict(endpointclasses),'raw_forced_inward_fields':368,
  'reserved_packet_legs_retained_and_charged':112,'reserved_packet_inward_fields':0,
  'conditional_target_rank':required,'funded_capacity':funded,'additional_inward_fields':8,
  'negative_controls':{'remove_all96_hosted_reverse_coefficients_rank':minus96,'remove_one_selected_reverse_coefficient_rank':minus1,'rank_preserving_wrong_source_coefficient_rejected':True},
  'exact_minor_determinants_independently_recomputed':True,
  'moment':{'exponent':'199/200','repetitions':18,'target_count':27344,'paid_count':130860,'rank_surplus':3040,'remaining_bounds':[str(lo),str(hi)],'remaining_decimal':str(float((lo+hi)/2)),'extra_required':8,'deficit_bounds':[str(8-hi),str(8-lo)],'raw_cycle_slack_lower':str(slack),'raw_cycle_slope_lower':str(slope),'root_helper_sha256':hpin,'scope':'Every source common slot and all112 fixed packet legs retained and charged; all other H4 reservations retained; arbitrary nested raw paths charged above400 direct rank8 moves. Conditional inherited profile, not unrestricted outer-template coding.'},
  'universal_even_hyperplane_edge':{'basis':[257,258,260,264,272,288,320,384],'source_chart_ids':[i for i,a in enumerate(spaces) if a==even],'rank':1,'all104_ports_excluded':True,'normalized_nonnegative_eight_deficit_weighted_bound':8},
  'accepted_scope':{'processing':'All intermediate fields and messages are field-linear functions of independent initial fields. Arbitrary local linear recoding, dirty common/private mixtures, and causal linear feedback are allowed. Unrestricted nonlinear or data-dependent encodings are excluded.','transport':'Fixed common MOVE chart endpoints and multiplicities; fixed112 packet endpoints and multiplicities;400 raw carrier endpoints fixed, with arbitrary nested paths in ambient dimension9. Extra branches must pay their actual MOVEs.','cut':'All initial inside common/private data conditioned upon; arbitrary joint inside decoding granted; no fixed-original-history matrix premise.','not_claimed':'No lower bound for changed common or packet geometry, removed billed reservations, unrestricted cross-template coding, or sufficiency of eight extra fields for all96 reverse duties.'}
 }
 (HERE/'REVIEW-RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'ranks':[1255,376],'funded':funded,'gap':8,'margin':out['moment']['remaining_decimal'],'negative_controls':out['negative_controls']},sort_keys=True))
if __name__=='__main__':main()
