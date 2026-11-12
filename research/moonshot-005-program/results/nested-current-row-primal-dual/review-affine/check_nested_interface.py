#!/usr/bin/env python3
"""Worker A independent source/current-row review of Worker B nested word.

Imports no author generator, validator, or algebra helper. Full literal emitter
independence belongs to the separate Worker C review, not this interface audit.
"""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PPIN='1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153'
WPAY='77d2e907d74c2539b115d8ad60367ee74939cca2eda9e10bcf28fb2b4e7ee42c'
def need(ok,message):
 if not ok:raise ValueError(message)
def sh(b):return hashlib.sha256(b).hexdigest()
def span(frame):
 S={0}
 for v in frame:S.update([x^v for x in tuple(S)])
 return S
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def root(v):
 B={i for i in range(9) if v>>i&1}
 if len(B)==3:
  return [2*int(i in B) for i in range(8)] if 8 in B else [2*int(i in B)-1 for i in range(8)]
 need(len(B)==7,'E8 source line type');i,j=sorted(set(range(9))-B)
 return [2*int(k==i)-1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def plus(a,b,c=Q(1)):
 out=a.copy()
 for j,x in b.items():
  v=out.get(j,Q(0))+c*x
  if v:out[j]=v
  else:out.pop(j,None)
 return out
def mm(A,B):return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in zip(*B)] for row in A]
def tr(A):return list(map(list,zip(*A)))
def inv(A):
 n=len(A);R=[[Q(v) for v in row]+[Q(i==j) for j in range(n)] for i,row in enumerate(A)]
 for j in range(n):
  k=next((i for i in range(j,n) if R[i][j]),None);need(k is not None,'invertible current-coordinate matrix');R[j],R[k]=R[k],R[j];q=R[j][j];R[j]=[v/q for v in R[j]]
  for i in range(n):
   if i!=j and R[i][j]:q=R[i][j];R[i]=[x-q*y for x,y in zip(R[i],R[j])]
 return [r[n:] for r in R]
def rank(A):
 if not A:return 0
 R=[[Q(v) for v in row] for row in A];k=0
 for j in range(len(R[0])):
  p=next((i for i in range(k,len(R)) if R[i][j]),None)
  if p is None:continue
  R[k],R[p]=R[p],R[k];q=R[k][j];R[k]=[v/q for v in R[k]]
  for i in range(k+1,len(R)):
   q=R[i][j];R[i]=[x-q*y for x,y in zip(R[i],R[k])]
  k+=1
  if k==len(R):break
 return k
def main(a):
 sb=a.source.read_bytes();pb=a.parent.read_bytes();wb=a.word.read_bytes();payload=gzip.decompress(wb)
 need(sh(sb)==SPIN and sh(pb)==PPIN and sh(payload)==WPAY,'frozen source/parent/candidate pins')
 s=json.loads(gzip.decompress(sb));p=json.loads(gzip.decompress(pb));w=json.loads(payload);raw={int(r):j for r,j in w['private_role_map'].items()};hosted={s['live'][i]:(x,y) for i,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};roots={i:root(s['frames'][s['initial'][i]][0]) for i in s['live']};selected=[0,1,2,98,99,103];oldY=[112,113,210];newY=[114,211,215]
 W={i+112:{j:-Q(dot(roots[i],roots[j]),8) for j in s['live'] if i!=j and dot(roots[i],roots[j])} for i in selected};groups={}
 for d in s['live']:
  key=tuple(y for y in sorted(W) if d in W[y])
  if key:groups.setdefault(key,[]).append(d)
 frames=s['frames']+[d['frame'] for d in w['additional_charts']];spaces=list(map(span,frames));records=w['nested_acquisition']['records'];primitives={tuple(r['support']):r for r in records if 'support' in r};joins={tuple(r['pair']):r for r in records if 'pair' in r};need(set(primitives)==set(groups) and len(groups)==7 and len(joins)==3,'complete source support partition')
 algebra={};hooks={};receipts=[]
 def qform(coeff):return {raw[r]:Q(c) for r,c in coeff.items() if c}
 def hook(t,fields,expected,C,label):hooks.setdefault(t,[]).append((fields,expected,C,label))
 for g,ds in groups.items():
  rec=primitives[g];H=[d for d in ds if d in hosted];U=[d for d in ds if d not in hosted];pair=sorted(set(g)&set(oldY));targets=[114] if g==tuple(newY) else [pair[0]] if len(g)==3 else pair+[min(set(g)-set(oldY))];C=rec['chart'];intersection=set.intersection(*(spaces[s['final'][y]] for y in g))
  need(spaces[C]==intersection and len(intersection)==64,'source dimension-six intersection');need(rec['hosted_donors']==H and rec['coupled_controls']==U and rec['target_rows']==targets,'source hosted/affine-control partition');need(len(ds)==(13 if len(g)==3 else 11),'source star/cycle donor count');rows=[[W[y][d] for d in H] for y in targets];need(rank(rows)==len(targets),'source hosted rank survives control removal');piv=rec['pivot_first_donors'];J=[H.index(d) for d in piv];M=[[Q(i==j) for j in range(len(H))] for i in range(len(H))]
  for j,row in zip(J,rows):M[j]=row
  Mi=inv(M);D=tr(Mi);need([[Q(x) for x in row] for row in rec['primal_encoder']['matrix']]==M,'actual source primal matrix');need([[Q(x) for x in row] for row in rec['dual_encoder']['matrix']]==D,'actual inverse-transpose matrix');primal=[{d:c for d,c in zip(H,row) if c} for row in M]
  for j,y in zip(J,targets):primal[j].update({u:W[y][u] for u in U})
  dual=[{hosted[d][0]:c for d,c in zip(H,row) if c} for row in D]
  hook(rec['primal_encoder']['begin'],H,[qform({d:1}) for d in H],C,'primitive original primal')
  hook(rec['dual_encoder']['begin'],H,list(map(qform,primal)),C,'primitive affine primal')
  hook(rec['dual_encoder']['begin'],[hosted[d][0] for d in H],[qform({hosted[d][0]:1}) for d in H],C,'primitive original dual')
  hook(rec['dual_encoder']['end'],[hosted[d][0] for d in H],list(map(qform,dual)),C,'primitive encoded dual')
  algebra[g]={'H':H,'U':U,'M':M,'Mi':Mi,'D':D,'J':J,'piv':piv,'targets':targets,'primal':primal,'dual':dual};receipts.append({'support':g,'donors':len(ds),'hosted':len(H),'affine_controls':U,'rank':len(targets),'chart':C})
 join_receipts=[]
 for pair,rec in joins.items():
  gs=[g for g in groups if set(pair)<=set(g)];need(len(gs)==2,'two actual source groups at join');star=next(g for g in gs if len(g)==3);cycle=next(g for g in gs if len(g)==4);ps,pc=algebra[star],algebra[cycle];C=rec['chart'];need(spaces[C]==set.intersection(*(spaces[s['final'][y]] for y in pair)) and len(spaces[C])==128,'actual dimension-seven join');roles=ps['piv']+pc['piv'];Arows=[];Brows=[]
  for g,primitive in [(star,ps),(cycle,pc)]:
   for j in primitive['J']:
    Arows.append(primitive['primal'][j]);Brows.append(primitive['dual'][j].copy())
  new=next(y for y in star if y not in oldY);ref=ps['targets'][0];d=groups[star][0];beta=W[new][d]/W[ref][d];need(all(W[new][d]==beta*W[ref][d] for d in groups[star]),'complete affine star relation');Brows[0][hosted[new-112][1]]=-beta
  alpha=[W[y][groups[star][0]]/W[ref][groups[star][0]] for y in pair];Qm=[[alpha[0],Q(1),Q(0),Q(0)],[alpha[1],Q(0),Q(1),Q(0)],[Q(1),Q(0),Q(0),Q(0)],[Q(0),Q(0),Q(0),Q(1)]];Qdual=tr(inv(Qm));need([[Q(x) for x in row] for row in rec['primal_encoder']['matrix']]==Qm,'join reads current basis, not original donors');need([[Q(x) for x in row] for row in rec['dual_encoder']['matrix']]==Qdual,'nested actual inverse-transpose matrix');need(rec['four_current_carriers']==roles and rec['four_current_dual_carriers']==[hosted[d][0] for d in roles],'current pivot role linkage')
  for name,want in [('incoming_current_rows',Arows),('incoming_dual_rows',Brows)]:need([{int(d):Q(c) for d,c in row} for row in rec[name]]==want,'source-derived '+name)
  hook(rec['before_primal'],roles,list(map(qform,Arows)),C,'four actual encoded primal rows');hook(rec['before_primal'],[hosted[d][0] for d in roles],list(map(qform,Brows)),C,'four actual encoded dual rows')
  def combine(M,rows):
   out=[]
   for coeff in M:
    row={}
    for c,r in zip(coeff,rows):row=plus(row,r,c)
    out.append(row)
   return out
  joined=combine(Qm,Arows);dual_joined=combine(Qdual,Brows)
  for i,y in enumerate(pair):need(joined[i]=={d:W[y][d] for d in groups[star]+groups[cycle]},'two old whole-cohort rows from four current rows')
  hook(rec['primal_encoder']['end'],roles,list(map(qform,joined)),C,'nested affine primal output');hook(rec['dual_encoder']['end'],[hosted[d][0] for d in roles],list(map(qform,dual_joined)),C,'nested dual output')
  visible=[x+112 for x in s['live'] if spaces[C]<=spaces[s['final'][x+112]]];need(visible==list(pair),'join permits exactly its two old receiver facets')
  join_receipts.append({'pair':pair,'chart':C,'four_real_primal_supports':[len(r) for r in Arows],'four_real_dual_supports':[len(r) for r in Brows],'current_early_Y2_term':{'role':hosted[new-112][1],'coefficient':str(-beta)},'reachable_active_receiver_facets':visible,'remaining_cycle_direction_not_deliverable_to_new_facet_after_join':True})
 forward={y:W[y].copy() for y in oldY}
 for y in newY:
  star=next(g for g in groups if len(g)==3 and y in g and len(set(g)&set(oldY))==2);ds=groups[star]+(groups[tuple(newY)] if y==114 else []);forward[y]={d:W[y][d] for d in ds}
 reverse={}
 for y,row in forward.items():
  for d,c in row.items():
   if d in hosted:reverse.setdefault(hosted[d][0],{})[hosted[y-112][1]]=-c
 need(sum(map(len,forward.values()))==196 and sum(map(len,reverse.values()))==183,'full claimed coefficient counts')
 for key,table in [('forward_correction_rows',forward),('reverse_correction_rows',reverse)]:need({int(k):{int(d):Q(c) for d,c in row} for k,row in w['nested_acquisition'][key].items()}==table,'full source-derived '+key)
 cache_expected={}
 for c in w['nested_acquisition']['cache_declarations']:
  y=c['receiver'];C=c['chart']
  if c['kind']=='new_receiver_star_read':g=next(g for g,r in primitives.items() if r['chart']==C);ds=groups[g]
  elif c['kind']=='fourth_star_facet_read':ds=groups[tuple(newY)]
  else:
   pair=next(pair for pair,r in joins.items() if r['chart']==C) if c['kind']=='old_receiver_join_read' else next(pair for pair in joins if y=={(112,113):113,(112,210):112,(113,210):210}[pair])
   ds=[d for g,cohort in groups.items() if set(pair)<=set(g) for d in cohort]
  cache_expected[c['event']]=(c['owner'],qform({d:W[y][d] for d in ds}),C)
 entry=w['program'][:400];need(entry==p['program'][:400] and len(raw)==400 and set(raw.values())==set(range(1480,1880)),'all independent difference-entry fields retained');rev={j:r for r,j in raw.items()}
 need({o[1] for o in entry}==set(rev) and all(o==['ADD',o[1],rev[o[1]],'-1',s['initial'][rev[o[1]]]] for o in entry),'exact v−u entry transformation')
 old_reads={i for i,o in enumerate(p['program'][:p['marks']['common_starts']]) if o[0]=='ADD' and o[1]>=1880 and o[2] in {raw[x] for x in s['live']} and o[4]==127};need(len(old_reads)==520,'literal parent E8 donor source census')
 def replay(candidate,check_gates):
  rows={i:{i:Q(1)} for i in range(1880)};loc=dict(enumerate(candidate['initial']));count=0;read_count=0
  localspaces=list(map(span,s['frames']+[d['frame'] for d in candidate.get('additional_charts',[])]))
  for t,o in enumerate(candidate['program'][400:candidate['marks']['common_starts']],400):
   if check_gates:
    for roles,expected,C,label in hooks.get(t,[]):
     need(all(loc[raw[r]]==C and rows[raw[r]]==want for r,want in zip(roles,expected)),label+' at '+str(t));count+=len(roles)
    parent_event=candidate['parent_event_of_output'][t]
    if parent_event in old_reads:
     need(o==p['program'][parent_event] and rows[o[2]]=={o[2]:Q(1)} and loc[o[2]]==127,'actual original E8 donor at '+str(t));read_count+=1
   op,d=o[:2]
   if op=='INIT':need(d>=1880 and d not in rows and d<1880+candidate['owned_fields'],'fresh owned field');rows[d]={};loc[d]=o[2]
   elif op=='CLEAR':need(d>=1880 and loc.get(d)==o[2],'owned clear at actual chart');del rows[d];del loc[d]
   elif op=='MOVE':
    ca,cb,owned=o[2:];need(loc.get(d)==ca and type(owned)is bool and owned==(d>=1880),'actual MOVE source');need(localspaces[ca]<localspaces[cb] or owned and localspaces[cb]<localspaces[ca],'legal nested MOVE');loc[d]=cb
   elif op=='SCALE':need(loc.get(d)==o[3] and Q(o[2]),'cochart nonzero SCALE');rows[d]={k:Q(o[2])*v for k,v in rows[d].items()}
   elif op in ['ADD','COPY']:
    source,c,C=o[2:];need(d!=source and d in rows and source in rows and loc[d]==loc[source]==C,'actual cochart source at '+str(t));need(op!='COPY' or not rows[d],'zero-copy destination');rows[d]=plus(rows[d],rows[source],Q(c))
   else:raise ValueError('unknown opcode')
   if check_gates and t in cache_expected:
    owner,want,C=cache_expected[t];need(rows[owner]==want and loc[owner]==C,'source-derived actual forward observation')
   if check_gates and t+1==candidate['marks']['all_active_donors_restored']:
    need(all(rows[raw[x]]=={raw[x]:Q(1)} and loc[raw[x]]==127 for x in s['live']),'all104 actual originals restored');need(all(rows[raw[d]]=={raw[d]:Q(1)} for d in s['hosted']['Y2']),'all96 actual reverse sources unchanged')
  if check_gates:need(read_count==520,'all original E8 donor reads covered')
  return rows,loc,count
 before,loc0,_=replay(p,False);actual,loc1,gate_count=replay(w,True);wanted={r:v.copy() for r,v in before.items()}
 for table in [forward,reverse]:
  for r,coeff in table.items():wanted[raw[r]]=plus(wanted[raw[r]],qform(coeff))
 need(actual==wanted and loc0==loc1,'all1880 independent (u,q) columns and source charts')
 tail=w['program'][w['marks']['common_starts']:];need(tail==p['program'][p['marks']['common_starts']:],'literal common suffix unchanged')
 for r in set(forward)|set(reverse)|{hosted[x][1] for x in selected}:
  touched=[o for o in tail if o[1]==raw[r] or o[0] in ('ADD','COPY') and o[2]==raw[r]];need(touched==[['ADD',raw[r],r,'1',s['final'][r]]],'no outgoing feedback after common entry')
 def type_walk(candidate):
  charts=dict(enumerate(candidate['initial']));S=list(map(span,s['frames']+[d['frame'] for d in candidate.get('additional_charts',[])]));ops=Counter();hist=Counter();raw_hist=Counter();live=peak=0
  for e in candidate['program']:
   kind,j=e[:2];ops[kind]+=1
   if kind=='INIT':need(j not in charts and j>=1880,'typed fresh owner');charts[j]=e[2];live+=1;peak=max(peak,live)
   elif kind=='CLEAR':need(j>=1880 and charts.get(j)==e[2],'typed owned clear');del charts[j];live-=1
   elif kind=='MOVE':
    ca,cb,owned=e[2:];need(charts.get(j)==ca and owned==(j>=1880),'typed current MOVE');need(S[ca]<S[cb] or owned and S[cb]<S[ca],'typed nested MOVE');r=abs((len(S[ca]).bit_length()-1)-(len(S[cb]).bit_length()-1));hist[r]+=1
    if j in rev:raw_hist[r]+=1
    charts[j]=cb
   elif kind=='SCALE':need(charts.get(j)==e[3] and Q(e[2]),'typed SCALE')
   else:need(kind in ['ADD','COPY'] and charts.get(j)==charts.get(e[2])==e[4],'typed cochart arithmetic')
  need(live==0,'all owned lifetimes closed');return charts,{'instructions':sum(ops.values()),'opcode_counts':dict(sorted(ops.items())),'raw_histogram':dict(sorted(raw_hist.items())),'raw_calls':sum(raw_hist.values()),'raw_rank_mass':sum(r*n for r,n in raw_hist.items()),'move_histogram':dict(sorted(hist.items())),'peak_owned':peak,'final_owned':live}
 final,bill=type_walk(w);oldfinal,_=type_walk(p);need(final==oldfinal and bill['raw_calls']==614 and bill['raw_rank_mass']==3200,'full type interface and monotone raw invoice')
 X,Y=s['hosted']['X2'],s['hosted']['Y2'];R=[[Q(i==j)+reverse.get(x,{}).get(y,Q(0)) for j,y in enumerate(Y)] for i,x in enumerate(X)];need(rank(R)==95,'actual reverse residual rank')
 ib=a.parent.parent.joinpath('INPUT-INVOICE.json').read_bytes();need(sh(ib)=='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248','complete caller invoice pin');iv=json.loads(ib);T=Counter({int(r):n for r,n in iv['T4'].items()});P=Counter({int(r):n for r,n in iv['P4'].items()});Rsrc=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw);Rn=Counter(bill['raw_histogram'])
 for r in set(Rsrc)|set(Rn):P[r]+=18*(Rn[r]-Rsrc[r])
 P[9]+=18*8;need(all(n>=0 for n in P.values()),'all paid caller calls retained');scale=10**24;low=high=Q(0)
 for r in sorted(set(T)|set(P)):
  coefficient=T[r]-P[r]
  if not coefficient:continue
  value=pow(r,199)*pow(scale,200);L,H=0,r*scale+1
  while H-L>1:
   mid=(L+H)//2
   if pow(mid,200)<=value:L=mid
   else:H=mid
  bounds=[Q(L,scale),Q(H,scale)]
  if coefficient<0:bounds.reverse()
  low+=coefficient*bounds[0];high+=coefficient*bounds[1]
 low/=18;high/=18;need(Q(42172356520999,10**12)<low<high<Q(42172356521001,10**12),'independent exact caller moment interval')
 mutants={}
 def reject(name,candidate):
  try:
   rows,loc,_=replay(candidate,True);need(rows==wanted and loc==loc0,'wrong1880-column prefix');type_walk(candidate)
  except (ValueError,KeyError,IndexError) as error:mutants[name]=str(error)
  else:raise ValueError('mutant survived: '+name)
 Uall={u for z in algebra.values() for u in z['U']};control_fields={raw[u] for u in Uall};net=w['nested_acquisition'];first_join=next(iter(joins.values()));tests=[]
 t=next(t for t,e in enumerate(w['program']) if net['begin']<=t<net['restored'] and e[0]=='ADD' and e[2] in control_fields and e[4]==127);tests.append(('missing_coupled_affine_restoration',t,3,'0'))
 Dfields={raw[hosted[x][1]] for x in selected};Bfields={raw[hosted[d][0]] for d in hosted}
 t=next(t for t,e in enumerate(w['program']) if net['begin']<=t<net['restored'] and e[0]=='ADD' and e[1] in Bfields and e[2] in Dfields and len(spaces[e[4]])==64);tests.append(('lost_early_dual_source_term',t,3,'0'))
 t=first_join['dual_encoder']['begin']+2*len(first_join['four_current_dual_carriers']);need(w['program'][t][0]=='ADD','specific dual mutation');tests.append(('wrong_nested_inverse_transpose',t,3,'0'))
 for name,t,j,value in tests:
  m=copy.deepcopy(w);m['program'][t][j]=value;reject(name,m)
 d=hosted[2][1];t=next(t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1]==raw[d] and e[2]==3);m=copy.deepcopy(w);m['program'][t][3]=s['final'][d];reject('reverse_source_skips_acquisition',m)
 C=first_join['chart'];carrier=first_join['four_current_carriers'][-1];new_target=next(y for y in newY if not spaces[C]<=spaces[s['final'][y]]);t=next(t for t,e in enumerate(w['program']) if e[0]=='MOVE' and e[1]==raw[carrier] and e[2]==C);m=copy.deepcopy(w);m['program'][t][3]=s['final'][new_target];reject('free_extra_delivery_after_join',m)
 result={'status':'PASS_INDEPENDENT_NESTED_AFFINE_CURRENT_ROW_REVIEW','source_sha256':SPIN,'parent_sha256':PPIN,'word_payload_sha256':WPAY,'word_sha256':sh(wb),'reviewer_imports_author_code':False,'input_basis':'All1480 common u and400 independent differences q=v−u; entry transformation checked literally','actual_current_rows_checked':gate_count,'primitive_source_receipts':receipts,'join_source_receipts':join_receipts,'original_E8_source_reads_checked':520,'new_forward_coefficients':196,'new_hosted_reverse_coefficients':183,'reverse_residual_rank':95,'literal_suffix_and_no_feedback':True,'bill':bill,'independent_remaining_moment_bounds':[str(low),str(high)],'independent_remaining_moment_decimal':float(low),'mutants':mutants,'scope':'Independent source geometry, matrices, affine controls, actual1880-column prefix and full typed invoice. Separate C review supplies literal full re-emission and final inverse audit; no new kappa.'};a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ['status','actual_current_rows_checked','new_forward_coefficients','new_hosted_reverse_coefficients','reverse_residual_rank','bill','independent_remaining_moment_decimal','mutants']},indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser()
 for key in ['source','parent','word','output']:parser.add_argument('--'+key,type=Path,required=True)
 main(parser.parse_args())
