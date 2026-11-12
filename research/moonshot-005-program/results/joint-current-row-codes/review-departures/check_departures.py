#!/usr/bin/env python3
"""Independent one/two genuine quotient exits; imports no author code."""
import argparse,copy,gzip,hashlib,importlib.util,itertools,json,sys
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from independent_engine import span,root9,dot,replay,rowplus,interval,need,sha
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='54b268f4e67e696b6e7e1bdbabb8fd136a434d312f2e305bd714e1f245e2473a'
WORDS={'one':'a214af51c5a6e9f7bd5863c629ffafbbc1a7791cfb3557ceeb895afee4c41a2b','two':'8679471f82cbb0fa850dd7b1f450e8c5d25b9f54b42f4df22bc9f7bac6a1e45d'}
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
ANCESTORS={'primal':('research/moonshot-005-program/results/cohort-reconstruction/eight/WORD.json.gz','9170345cd487cb996a3a793ade61072bbd169b69a9116e5216b52b05259b6754'),'dual':('research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz','bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17')}
B=[5,56,65,69,77,96,100,103];S=[0,7,20,27,36,46,57,111]
DONORS=[11,24,30,43,78,83,85,90];YS=[117,168,189,208]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def transpose(A):return [list(c) for c in zip(*A)]
def multiply(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def inverse(A):
 n=len(A);D=[list(map(F,r))+[F(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  i=next((i for i in range(j,n) if D[i][j]),None);need(i is not None,'invertible exact matrix');D[i],D[j]=D[j],D[i];c=D[j][j];D[j]=[v/c for v in D[j]]
  for i in range(n):
   if i!=j:
    c=D[i][j]
    if c:D[i]=[u-c*v for u,v in zip(D[i],D[j])]
 return [r[n:] for r in D]
def rank(A):
 if not A:return 0
 D=[list(map(F,r)) for r in A];k=0
 for j in range(len(D[0])):
  i=next((i for i in range(k,len(D)) if D[i][j]),None)
  if i is None:continue
  D[i],D[k]=D[k],D[i];c=D[k][j];D[k]=[v/c for v in D[k]]
  for i in range(k+1,len(D)):
   c=D[i][j]
   if c:D[i]=[u-c*v for u,v in zip(D[i],D[k])]
  k+=1
  if k==len(D):break
 return k
def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();pb=(a.parent/'WORD.json.gz').read_bytes();wb=a.word.read_bytes()
 need(sha(sb)==SOURCE and sha(pb)==PARENT and sha(wb)==WORDS[a.mode],'exact source and word pins')
 src,p,w=[json.loads(gzip.decompress(b)) for b in (sb,pb,wb)];author=json.loads((a.word.parent/'RESULT.json').read_text());prior=json.loads((a.parent/'RESULT.json').read_text())
 raw={int(k):v for k,v in p['private_role_map'].items()};xs=src['live'];H=[xs[i] for i in src['hosted']['Dports']];host=dict(zip(H,zip(src['hosted']['X2'],src['hosted']['Y2'])))
 roots={h:root9(src['frames'][src['initial'][h]][0]) for h in xs};G={(i,j):F(dot(roots[i],roots[j]),18) for i in xs for j in xs}
 pg=next(g for g in p['parent_cohort_collection_provenance']['groups'] if g['donors']==DONORS);C=pg['chart'];need(C==1097 and pg['receivers']==YS,'exact old source cohort')
 dg=next(g for g in p['parent_paired_collection_provenance']['groups'] if g['chart']==C)
 A=[[-G[y-112,j] for j in DONORS] for y in YS];need(A==[[F(v) for v in r] for r in pg['matrix']],'old coefficient matrix independently reconstructed from source roots')
 col={j:[row[k] for row in A] for k,j in enumerate(DONORS)}
 exits={90:0} if a.mode=='one' else {90:0,43:7};gamma={90:{78:F(-1),83:F(1),85:F(1)}} if a.mode=='one' else {90:{78:F(-1),83:F(1)},43:{11:F(1),85:F(1)}}
 involved=[78,83,85,90] if a.mode=='one' else [11,43,78,83,85,90]
 need(set(involved+list(exits.values()))<=set(H),'no coupled carrier used by the new paired code')
 shared=eye(8)
 if a.mode=='two':
  i,j=DONORS.index(83),DONORS.index(85);shared[i][i]=shared[i][j]=F(1,2);shared[j][i]=F(-1,2);shared[j][j]=F(1,2)
 N=eye(8)
 for j,gs in gamma.items():
  for k,c in gs.items():N[DONORS.index(k)][DONORS.index(j)]=c
 P=multiply(N,shared);Pinv=inverse(P);after=multiply(A,Pinv)
 need(multiply(P,Pinv)==eye(8) and multiply(Pinv,P)==eye(8),'true invertible shared-plus-branch code')
 need(all(not after[i][DONORS.index(j)] for i in range(4) for j in exits),'every exit column absent from current old duties')
 need(all(P[DONORS.index(j)]==eye(8)[DONORS.index(j)] for j in exits),'actual exit primal rows stay original')
 newcol={j:[after[i][k] for i in range(4)] for k,j in enumerate(DONORS) if j not in exits}
 if a.mode=='two':need(newcol[83]==[x+y for x,y in zip(col[83],col[85])] and newcol[85]==[-x+y for x,y in zip(col[83],col[85])],'current sum and difference columns')
 else:need(all(newcol[j]==col[j] for j in newcol),'single-exit surviving columns unchanged')
 frames=src['frames']+[d['frame'] for d in w['additional_charts']];spaces=list(map(span,frames))
 need(w['additional_charts'][:len(p['additional_charts'])]==p['additional_charts'],'all inherited charts unchanged')
 def donor_span(ds):return span([src['frames'][src['initial'][d]][0] for d in ds])
 D1=spaces.index(donor_span([78,83,85,90]));D2=spaces.index(donor_span([11,43,83,85])) if a.mode=='two' else None;D0=spaces.index(donor_span([83,85])) if a.mode=='two' else None
 Ds={90:D1} if a.mode=='one' else {90:D1,43:D2};Fs={j:src['final'][t+112] for j,t in exits.items()}
 for j,D in Ds.items():need(len(spaces[D])==8 and spaces[D]<spaces[C] and spaces[D]<spaces[Fs[j]],'actual dimension3 branch containment')
 if a.mode=='two':need(len(spaces[D0])==4 and spaces[D0]<spaces[D1] and spaces[D0]<spaces[D2] and D1!=D2,'two true branches from a dimension2 shared chart')
 ancestors={}
 for name,(path,pin) in ANCESTORS.items():
  b=(a.repo/path).read_bytes();need(sha(b)==pin,'pinned ancestor block source');ancestors[name]=json.loads(gzip.decompress(b))
 oldP=ancestors['primal']['program'][pg['begin']:pg['end']];oldD=ancestors['dual']['program'][dg['begin']:dg['end']]
 def locate(block):
  starts=[i for i,e in enumerate(p['program']) if e==block[0] and p['program'][i:i+len(block)]==block];need(len(starts)==1,'unique literal inherited block');return starts[0],starts[0]+len(block)
 ps,pe=locate(oldP);ds,de=locate(oldD);need(ds<de<ps<pe<p['marks']['common_starts'],'causal block order')
 need(not any(ds<=i<de or ps<=i<pe for i in p['native_event_to_physical']),'no native operation removed')
 need(not any(ds<i<de or ps<i<pe for i in p['marks'].values()),'no retained global cut hidden inside replacement')
 entry,loc,_=replay(p,spaces,ds,True);q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 for j in involved:
  for r in (j,host[j][0]):need(entry[raw[r]]==q[r] and loc[raw[r]]==src['initial'][r],'actual original incoming primal and dual')
 collectors={j:int(p['parent_second_frame_feedback_provenance']['collectors'][str(t)]) for j,t in exits.items()}
 for j,t in exits.items():need(entry[raw[host[t][1]]]==q[host[t][1]] and loc[raw[host[t][1]]]==loc[collectors[j]]==Fs[j],'actual arrived d and stationary collector')
 pre=[];control_events={}
 def put(e):pre.append(e);return len(pre)-1
 if a.mode=='one':
  for j in involved:
   for r in (j,host[j][0]):put(['MOVE',raw[r],src['initial'][r],D1,False])
 else:
  for j in [83,85]:
   for r in (j,host[j][0]):put(['MOVE',raw[r],src['initial'][r],D0,False])
  put(['ADD',raw[85],raw[83],'-1',D0]);control_events['shared_primal']=put(['ADD',raw[83],raw[85],'1/2',D0]);put(['SCALE',raw[85],'1/2',D0])
  put(['ADD',raw[host[85][0]],raw[host[83][0]],'-1',D0]);control_events['shared_dual']=put(['SCALE',raw[host[83][0]],'2',D0]);put(['ADD',raw[host[83][0]],raw[host[85][0]],'1',D0])
  for j,D in [(83,D1),(85,D2)]:
   for r in (j,host[j][0]):put(['MOVE',raw[r],D0,D,False])
  for D,js in [(D1,[78,90]),(D2,[11,43])]:
   for j in js:
    for r in (j,host[j][0]):put(['MOVE',raw[r],src['initial'][r],D,False])
 for j,gs in gamma.items():
  D=Ds[j]
  for k,c in gs.items():control_events.setdefault('absorption',put(['ADD',raw[k],raw[j],str(c),D]))
  for k,c in gs.items():put(['ADD',raw[host[j][0]],raw[host[k][0]],str(-c),D])
  t=exits[j];F0=Fs[j];c=G[t,j]
  put(['MOVE',raw[j],D,F0,False]);control_events.setdefault('collector',put(['ADD',collectors[j],raw[j],str(-c),F0]));put(['MOVE',raw[j],F0,127,False])
  put(['MOVE',raw[host[j][0]],D,F0,False]);control_events.setdefault('reverse_read',put(['ADD',raw[host[j][0]],raw[host[t][1]],str(c),F0]));put(['MOVE',raw[host[j][0]],F0,127,False])
 current={k:D1 for k in gamma[90]} if a.mode=='one' else {11:D2,78:D1,83:D1,85:D2}
 hs=[j for j in dg['first_donors'] if j not in exits];AH=[[newcol[j][i] for j in hs] for i in range(4)]
 if a.mode=='one':piv=dg['pivot_first_donors']
 else:
  choices=[]
  for inds in itertools.combinations(range(len(hs)),4):
   minor0=[[r[k] for k in inds] for r in AH]
   if rank(minor0)==4:choices.append((sum(bool(v) for row in inverse(minor0) for v in row),inds))
  need(choices,'restricted hosted full rank');piv=[hs[i] for i in min(choices)[1]]
 need(piv==([11,24,43,83] if a.mode=='one' else [11,24,78,83]),'independently selected true hosted pivots')
 M=eye(len(hs))
 for i,j in enumerate(piv):M[hs.index(j)]=AH[i][:]
 Minv=inverse(M);need(multiply(M,Minv)==eye(len(hs)),'true reduced dual inverse')
 dual=[];temps=p['parent_paired_collection_provenance']['temporaries'][:len(hs)]
 def dense(out,roles,matrix,at):
  for i,r in enumerate(roles):out.extend([['INIT',temps[i],at],['ADD',temps[i],raw[r],'1',at]])
  for i,r in enumerate(roles):
   out.append(['ADD',raw[r],temps[i],'-1',at])
   for j,c in enumerate(matrix[i]):
    if c:out.append(['ADD',raw[r],temps[j],str(c),at])
  for z in temps:out.append(['CLEAR',z,at])
 br=[host[j][0] for j in hs]
 for j,r in zip(hs,br):dual.append(['MOVE',raw[r],current.get(j,src['initial'][r]),C,False])
 dense(dual,br,transpose(Minv),C)
 for j,r in zip(hs,br):
  if j in piv:
   y=YS[piv.index(j)];f=src['final'][y];dual.extend([['MOVE',raw[r],C,f,False],['ADD',raw[r],raw[host[y-112][1]],'-1',f],['MOVE',raw[r],f,127,False]])
  else:dual.append(['MOVE',raw[r],C,127,False])
 dense(dual,br,transpose(M),127)
 for j,gs in gamma.items():
  for k,c in gs.items():dual.append(['ADD',raw[host[j][0]],raw[host[k][0]],str(c),127])
 if a.mode=='two':dual.extend([['ADD',raw[host[83][0]],raw[host[85][0]],'-1',127],['SCALE',raw[host[83][0]],'1/2',127],['ADD',raw[host[85][0]],raw[host[83][0]],'1',127]])
 I=pg['pivots'];non=[j for j in DONORS if j not in I and j not in exits];AI=[[newcol[j][i] for j in I] for i in range(4)];AIinv=inverse(AI)
 need(AI==[[F(v) for v in r] for r in pg['pivot_minor']],'unchanged actual primal pivot minor')
 acc=pg['accumulator_roles'];snaps=pg['snapshot_roles'];primal=[]
 for r in acc:primal.append(['INIT',r,C])
 for j in non:
  primal.append(['MOVE',raw[j],current.get(j,src['initial'][j]),C,False])
  for i,r in enumerate(acc):
   if newcol[j][i]:primal.append(['ADD',r,raw[j],str(newcol[j][i]),C])
  primal.append(['MOVE',raw[j],C,127,False])
 for j in I:primal.append(['MOVE',raw[j],current.get(j,src['initial'][j]),C,False])
 for r,j in zip(snaps,I):primal.extend([['INIT',r,C],['ADD',r,raw[j],'1',C]])
 for i,j in enumerate(I):
  primal.append(['ADD',raw[j],snaps[i],'-1',C])
  for k,r in enumerate(snaps):
   if AI[i][k]:primal.append(['ADD',raw[j],r,str(AI[i][k]),C])
  primal.append(['ADD',raw[j],acc[i],'1',C])
 for r in acc+snaps:primal.append(['CLEAR',r,C])
 for j,delivery in zip(I,pg['deliveries']):
  y=delivery['receiver'];f=src['final'][y];oldread=ancestors['primal']['program'][delivery['read']]
  need(oldread[0]=='ADD' and oldread[2]==raw[j] and oldread[3]=='1' and oldread[4]==f,'authentic retained old B collector read')
  primal.extend([['MOVE',raw[j],C,f,False],copy.deepcopy(oldread),['MOVE',raw[j],f,127,False]])
 for i,j in enumerate(I):
  for k in non:
   if newcol[k][i]:primal.append(['ADD',raw[j],raw[k],str(-newcol[k][i]),127])
 for r,j in zip(snaps,I):primal.extend([['INIT',r,127],['ADD',r,raw[j],'1',127]])
 for i,j in enumerate(I):
  primal.append(['ADD',raw[j],snaps[i],'-1',127])
  for k,r in enumerate(snaps):
   if AIinv[i][k]:primal.append(['ADD',raw[j],r,str(AIinv[i][k]),127])
 for r in snaps:primal.append(['CLEAR',r,127])
 for j,gs in gamma.items():
  for k,c in gs.items():primal.append(['ADD',raw[k],raw[j],str(-c),127])
 if a.mode=='two':primal.extend([['ADD',raw[83],raw[85],'-1',127],['SCALE',raw[85],'2',127],['ADD',raw[85],raw[83],'1',127]])
 ops=[];lineage=[];bound={};blocks={};i=0
 while i<len(p['program']):
  if i in (ds,ps):
   end=de if i==ds else pe;replacement=pre+dual if i==ds else primal;start=len(ops);blocks['dual' if i==ds else 'primal']=[start,start+len(replacement)];ops+=replacement;lineage.extend([None]*len(replacement))
   for oldi in range(i,end):bound[oldi]=start
   i=end
  else:bound[i]=len(ops);ops.append(copy.deepcopy(p['program'][i]));lineage.append(i);i+=1
 if ops!=w['program']:
  k=next((i for i,(x,y) in enumerate(zip(ops,w['program'])) if x!=y),min(len(ops),len(w['program'])))
  raise ValueError('literal reconstruction mismatch at '+str(k)+' '+str(ops[k:k+3])+' versus '+str(w['program'][k:k+3]))
 need(lineage==w['parent_event_of_output'],'entire independent parent lineage')
 need(w['native_event_to_physical']==[bound[i] for i in p['native_event_to_physical']],'all retained native event mappings')
 need(w['marks']=={name:bound[i] for name,i in p['marks'].items()},'all named boundary mappings')
 before,bl,_=replay(p,spaces,p['marks']['common_starts'],True);actual,al,_=replay(w,spaces,w['marks']['common_starts'],True)
 want={r:row.copy() for r,row in before.items()}
 for j,t in exits.items():
  want[raw[t+112]]=rowplus(want[raw[t+112]],q[j],-G[t,j]);want[raw[host[j][0]]]=rowplus(want[raw[host[j][0]]],q[host[t][1]],G[t,j])
 need(actual==want and al==bl,'all1880 current input columns and locations')
 suffix=w['program'][w['marks']['common_starts']:];need(suffix==p['program'][p['marks']['common_starts']:],'entire unchanged common suffix')
 for j,t in exits.items():
  for z in (t+112,host[j][0]):
   uses=[e for e in suffix if e[1]==raw[z] or e[0] in ('ADD','COPY') and e[2]==raw[z]]
   need(uses==[['ADD',raw[z],z,'1',src['final'][z]]],'changed raw row has no later feedback')
  need(actual[raw[j]]==q[j] and actual[raw[host[t][1]]]==q[host[t][1]],'actual inverse source rows remain authentic')
  need(rowplus(actual[raw[t+112]],actual[raw[j]],G[t,j])==before[raw[t+112]],'explicit forward information inverse')
  need(rowplus(actual[raw[host[j][0]]],actual[raw[host[t][1]]],-G[t,j])==before[raw[host[j][0]]],'explicit reverse information inverse')
  need(before[raw[t+112]].get(raw[j],F(0))==G[t,j] and not actual[raw[t+112]].get(raw[j]),'actual foreign forward coefficient cancelled')
 restored,rl,_=replay(w,spaces,w['marks']['all_preconditioned_donors_restored'],True)
 original_restored,orl,_=replay(p,spaces,p['marks']['all_preconditioned_donors_restored'],True)
 need(all(restored[raw[x]]==original_restored[raw[x]] and rl[raw[x]]==127 for x in xs),'all104 original/current donor duties restored before old E8 encoder')
 R={}
 for h in H:
  x=host[h][0];coeff={j:actual[raw[x]].get(raw[host[j][1]],F(0)) for j in H};expected=q[x]
  for j,c in coeff.items():
   if c:expected=rowplus(expected,q[host[j][1]],c)
  need(actual[raw[x]]==expected,'complete actual reverse row no hidden input terms')
  need({int(j):F(c) for j,c in w['paired_reverse_corrections'][str(x)]}=={host[j][1]:c for j,c in coeff.items() if c},'actual current reverse metadata matches')
  R[h]={j:c+F(h==j) for j,c in coeff.items() if c+F(h==j)}
 for t in S:
  left={h:-G[h,t] if h in B else F(h==t) if h in S else F(0) for h in H}
  need(all(sum(left[h]*R[h].get(j,F(0)) for h in B+S)==0 for j in H),'eight unchanged exact left-kernel vectors')
 small=B+[h for h in H if h not in B+S]
 need(len(small)==88 and all(R[i].get(j,F(0))==(i==j) for i in B for j in small) and all(R[i].get(j,F(0))==(i==j) for i in small[8:] for j in small[8:]),'unchanged unit88 minor')
 _,final,bill=replay(w,spaces);_,parentfinal,oldbill=replay(p,spaces);need(final==parentfinal and set(final)==set(range(1880)),'complete final locations and owned retirement')
 need(json.loads(json.dumps(bill))==author['bill'],'independent full typed bill')
 delta=Counter(bill['raw_histogram']);delta.subtract(oldbill['raw_histogram']);delta={r:n for r,n in delta.items() if n}
 expected_delta={1:2,2:8,3:4,5:-6} if a.mode=='one' else {1:12,2:8,3:4,5:-8}
 need(delta==expected_delta and sum(r*n for r,n in bill['raw_histogram'].items())==3200,'exact raw signed tariff and rankmass')
 need(all(bill['move_rank_histogram'].get(r,0)-bill['raw_histogram'].get(r,0)==oldbill['move_rank_histogram'].get(r,0)-oldbill['raw_histogram'].get(r,0) for r in set(bill['move_rank_histogram'])|set(oldbill['move_rank_histogram'])),'unchanged owned MOVE profile at every rank')
 ordinary={op:bill['opcode_counts'].get(op,0)-oldbill['opcode_counts'].get(op,0) for op in sorted(set(bill['opcode_counts'])|set(oldbill['opcode_counts']))}
 expected_ordinary={'ADD':-7,'CLEAR':-2,'COPY':0,'INIT':-2,'MOVE':8,'SCALE':0} if a.mode=='one' else {'ADD':-22,'CLEAR':-4,'COPY':0,'INIT':-4,'MOVE':16,'SCALE':4}
 need(ordinary==expected_ordinary,'complete independently counted ordinary increment')
 ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes();need(sha(ib)==INVOICE,'original complete caller invoice');iv=json.loads(ib)
 originalraw=Counter(abs(len(src['frames'][e[3]])-len(src['frames'][e[2]])) for e in src['program'] if e[0]=='MOVE' and e[1] in raw)
 targets=Counter({int(k):v for k,v in iv['T4'].items()});paid=Counter({int(k):v for k,v in iv['P4'].items()})
 for r in set(originalraw)|set(bill['raw_histogram']):paid[r]+=18*(bill['raw_histogram'].get(r,0)-originalraw[r])
 paid[9]+=144;paid[1]+=144
 need({str(r):n for r,n in paid.items()}==author['conditional_caller']['P_partial'],'all H4 costs plus8rank9 and8rank1 retained')
 lo,hi=interval({r:targets[r]-paid[r] for r in targets.keys()|paid.keys()});lo/=18;hi/=18;claimed=author['conditional_caller']
 need(F(claimed['remaining_moment_per_native_lower'])<=lo<=hi<=F(claimed['remaining_moment_per_native_upper']),'fresh160-bit directed margin refines author interval')
 result={'status':'PASS_INDEPENDENT_'+a.mode.upper()+'_QUOTIENT_DEPARTURE','source_sha256':SOURCE,'parent_sha256':PARENT,'word_sha256':sha(wb),'word_payload_sha256':sha(gzip.decompress(wb)),'exact_input_columns':1880,'independently_reconstructed_operations':len(ops),'exits':exits,'old_blocks':{'dual':[ds,de],'primal':[ps,pe]},'new_blocks':blocks,'shared_matrix':[[str(v) for v in r] for r in shared],'full_primal_matrix':[[str(v) for v in r] for r in P],'full_dual_matrix':[[str(v) for v in r] for r in transpose(Pinv)],'restricted_hosted_primal_matrix':[[str(v) for v in r] for r in M],'restricted_hosted_dual_matrix':[[str(v) for v in r] for r in transpose(Minv)],'actual_reverse_rank':88,'full_bill':bill,'raw_increment':delta,'ordinary_increment':ordinary,'fresh_margin_lower':str(lo),'fresh_margin_upper':str(hi),'new_owned_moves':0,'unchanged_literal_common_suffix':True,'scope':'Independent finite current-row source construction and full tariff. No new supplier or kappa.'}
 mutants={}
 def reject(name,m):
  try:
   mr,ml,_=replay(m,spaces,m['marks']['common_starts'],True);need(mr==want and ml==bl,'mutated exact1880 source state')
  except (ValueError,KeyError,IndexError) as e:mutants[name]=str(e)
  else:raise ValueError('unrejected actual word mutation '+name)
 for name,key in [('wrong_absorption_sign','absorption'),('wrong_reverse_receiver_sign','reverse_read'),('new_forward_collector_unconsumed','collector')]:
  m=copy.deepcopy(w);event=blocks['dual'][0]+control_events[key];m['program'][event][3]=str(-F(m['program'][event][3]));reject(name,m)
 event=next(i for i,e in enumerate(pre) if e[0]=='ADD' and e[1]==raw[host[90][0]] and e[2]==raw[host[78][0]])
 m=copy.deepcopy(w);event+=blocks['dual'][0];m['program'][event][3]=str(-F(m['program'][event][3]));reject('incorrect_inverse_transpose_absorption',m)
 event=next(i for i,e in enumerate(dual) if e==['ADD',raw[host[90][0]],raw[host[78][0]],'-1',127])+blocks['dual'][0]+len(pre)
 m=copy.deepcopy(w);m['program'][event][3]='1';reject('wrong_dual_hub_inverse',m)
 m=copy.deepcopy(w);at=m['marks']['common_starts'];m['program'].insert(at,copy.deepcopy(pre[0]));m['marks']['common_starts']+=1;reject('spent_initial_route_reused',m)
 if a.mode=='two':
  m=copy.deepcopy(w);event=blocks['dual'][0]+control_events['shared_primal'];m['program'][event][3]='1';reject('wrong_shared_primal_half',m)
  m=copy.deepcopy(w);event=blocks['dual'][0]+control_events['shared_dual'];m['program'][event][2]='1/2';reject('primal_scale_used_for_dual',m)
  event=next(i for i,e in enumerate(primal) if e[0]=='ADD' and e[2]==raw[83] and e[1] in acc and F(e[3])!=col[83][acc.index(e[1])]);m=copy.deepcopy(w);e=m['program'][blocks['primal'][0]+event];e[3]=str(col[83][acc.index(e[1])]);reject('stale_original_nonpivot_column',m)
 result['negative_controls']=mutants
 frozen=a.repo/'research/shared-wire-split-composition/frozen';pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def load_engine(filename):
  path=frozen/filename;need(sha(path.read_bytes())==pins[filename],'frozen physical map engine');spec=importlib.util.spec_from_file_location('independent_departure_'+filename[:-3],path);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod
 c=load_engine('clifford_exact.py');v=load_engine('native_verify.py');oldpairs={(e[2],e[3]) for e in p['program'] if e[0]=='MOVE'};pairs={(e[2],e[3]) for e in ops if e[0]=='MOVE'};maps=[]
 for x,y in sorted(pairs-oldpairs):
  recipe,_=c.lower_child(c.canonical_frame(9,tuple(frames[x])).adjoint().then(c.canonical_frame(9,tuple(frames[y]))));v.equal(v.recipe(recipe),v.adjoint(v.frame(frames[x],9))+v.frame(frames[y],9),'independent actual departure map')
  need(recipe['rank']==abs(len(frames[y])-len(frames[x])),'actual exact recursive map rank');maps.append({'source':x,'target':y,'recipe':recipe})
 need(len(maps)==(6 if a.mode=='one' else 12),'all distinct introduced map pairs')
 bad=copy.deepcopy(maps[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong global phase')
 except ValueError:result['wrong_global_phase_rejected']=True
 else:raise ValueError('wrong global phase survived')
 result['introduced_map_count']=len(maps);result['engine_pins']=pins
 if a.mode=='one':
  cases=[];classification=Counter();nullities=[];all_hosts=[]
  for group in p['parent_cohort_collection_provenance']['groups']:
   ds0=[h for h in group['donors'] if h in H];all_hosts+=ds0;rows0=[y-112 for y in group['receivers']];oldmatrix=[[-G[r,h] for h in ds0] for r in rows0];fullrank=rank(oldmatrix);nullities.append(len(ds0)-fullrank)
   for t in S:
    selected=[h for h in ds0 if spaces[src['initial'][h]]<=spaces[src['final'][t+112]]];cols=[[-G[r,h] for h in selected] for r in rows0];rr=rank(cols);classification[len(selected),rr]+=1
    record={'cohort_chart':group['chart'],'receiver':t,'hosted_donors':selected,'column_rank':rr}
    if len(selected)==4 and rr==3:
     need(len(donor_span(selected))==8,'actual binary dimension3 circuit')
     need(all(rank([[row[k] for k in range(4) if k!=j] for row in cols])==3 for j in range(4)),'all four coordinate exits legitimate algebraically')
     record['all_four_algebraic_exits']=True
    cases.append(record)
  need(len(cases)==112 and classification=={(3,3):46,(4,3):38,(2,2):14,(0,0):12,(1,1):2},'independent complete14-by8 entry census')
  need(len(all_hosts)==len(set(all_hosts))==88 and set(all_hosts)==set(H)-set(B),'hosted carriers partition into original B cohorts')
  need(sum(nullities)==34,'exact total original-cohort coordinate nullity')
  result['independent_entry_census']={'case_count':112,'classification':{str(k):n for k,n in classification.items()},'binary_dimension3_circuits':38,'coordinate_exit_nullity_sum':34,'scope':'Untouched-entry geometry and per-cohort coordinate quotient preservation only; not simultaneous routing admission or general coded-row bound.'}
  a.output.mkdir(parents=True,exist_ok=True);(a.output/'CENSUS.json').write_text(json.dumps(cases,indent=2,sort_keys=True)+'\n')
 a.output.mkdir(parents=True,exist_ok=True)
 (a.output/(a.mode+'-RESULT.json')).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 (a.output/(a.mode+'-MAPS.json')).write_text(json.dumps(maps,indent=2,sort_keys=True)+'\n')
 print(result['status'],len(ops),'rank88',float(lo))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--parent',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--mode',choices=['one','two'],required=True);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
