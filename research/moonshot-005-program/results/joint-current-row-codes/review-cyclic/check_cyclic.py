#!/usr/bin/env python3
"""Independent source reconstruction of cyclic dual rank82; no author imports."""
import argparse,copy,gzip,importlib.util,json,sys
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path
from independent_engine import need,sha,span,root9,dot,replay,rowplus,interval
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='54b268f4e67e696b6e7e1bdbabb8fd136a434d312f2e305bd714e1f245e2473a'
FRAME='3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101'
WORD='ca493a06385fc55a1b1b2d30ddb638c7f5b021d19459aa6b0b8c85e3797510d2'
PAIRED='bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17'
INVOICE='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
GROUPS=[{'B':[5,56,69,100],'S':[0,46,57,111],'T':[54,67,102]},
        {'B':[65,77,96,103],'S':[7,20,27,36],'T':[8,18,26]}]
B=[5,56,65,69,77,96,100,103]
EXTERNAL=[12,31]
EXTRA_READS=[{56:F(-1,2),100:F(1,2)},{77:F(1,2),103:F(-1,2)}]
def rank(A):
 if not A:return 0
 D=[list(map(F,r)) for r in A];k=0
 for j in range(len(D[0])):
  i=next((i for i in range(k,len(D)) if D[i][j]),None)
  if i is None:continue
  D[k],D[i]=D[i],D[k];c=D[k][j];D[k]=[v/c for v in D[k]]
  for i in range(k+1,len(D)):
   c=D[i][j]
   if c:D[i]=[u-c*v for u,v in zip(D[i],D[k])]
  k+=1
  if k==len(D):break
 return k
def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();pb=(a.parent/'WORD.json.gz').read_bytes();fb=(a.repo/'research/moonshot-005-program/results/orthogonal-frame-feedback/output/WORD.json.gz').read_bytes();db=(a.repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz').read_bytes();wb=a.word.read_bytes()
 need((sha(sb),sha(pb),sha(fb),sha(db),sha(wb))==(SOURCE,PARENT,FRAME,PAIRED,WORD),'all frozen source pins')
 s,p,f,d,w=[json.loads(gzip.decompress(b)) for b in (sb,pb,fb,db,wb)];author=json.loads((a.word.parent/'RESULT.json').read_text())
 raw={int(k):v for k,v in p['private_role_map'].items()};xs=s['live'];H=[xs[i] for i in s['hosted']['Dports']];host=dict(zip(H,zip(s['hosted']['X2'],s['hosted']['Y2'])))
 roots={h:root9(s['frames'][s['initial'][h]][0]) for h in H};G={(i,j):F(dot(roots[i],roots[j]),18) for i in H for j in H};K=[h for g in GROUPS for family in ['B','S','T'] for h in g[family]]
 need(len(K)==len(set(K))==22 and set(K+EXTERNAL)<=set(H),'22 distinct genuine hosted pairs plus external records')
 for g in GROUPS:
  for family in g.values():need(all(G[i,j]==(i==j) for i in family for j in family),'orthogonal within every source family')
 need(all(not G[i,j] for i in K[:11] for j in K[11:]),'two orthogonal real source subspaces')
 frames=s['frames']+[z['frame'] for z in w['additional_charts']];spaces=list(map(span,frames));need(w['additional_charts'][:len(p['additional_charts'])]==p['additional_charts'],'all inherited charts retained')
 need(all(len(spaces[i])==2**len(fr) for i,fr in enumerate(frames)),'independent declared frame bases')
 def chart(ds):return spaces.index(span([s['frames'][s['initial'][h]][0] for h in ds]))
 def locate(block):
  hits=[i for i,e in enumerate(p['program']) if e==block[0] and p['program'][i:i+len(block)]==block];need(len(hits)==1,'unique actual inherited block');return hits[0]
 meta=f['second_frame_feedback'];need(meta==p['parent_second_frame_feedback_provenance'],'exact frame ancestry')
 frame_block=f['program'][meta['begin']:meta['end']];start=locate(frame_block);offset=start-meta['begin'];drop=set();removed_blocks=[]
 # Rebuild each complete original paired frame block, tagging genuine banks.
 for group in GROUPS:
  fg=next(g for g in meta['groups'] if g['donors']==group['B']);bs=group['B'];ss=group['S'];C=fg['chart'];matrix=[[-G[t,b] for b in bs] for t in ss];mt=[list(z) for z in zip(*matrix)]
  temps=meta['temporaries'];tagged=[]
  def emit_old(e,bank):tagged.append((e,bank))
  def dense_old(rs,M,at,bank):
   for i,r in enumerate(rs):emit_old(['INIT',temps[i],at],bank);emit_old(['ADD',temps[i],r,'1',at],bank)
   for i,r in enumerate(rs):
    emit_old(['ADD',r,temps[i],'-1',at],bank)
    for j,c in enumerate(M[i]):
     if c:emit_old(['ADD',r,temps[j],str(c),at],bank)
   for z in temps:emit_old(['CLEAR',z,at],bank)
  ar=[raw[b] for b in bs];br=[raw[host[b][0]] for b in bs]
  for rs,bank in [(ar,'primal'),(br,'dual')]:
   for b,r in zip(bs,rs):emit_old(['MOVE',r,s['initial'][b],C,False],bank)
  dense_old(ar,matrix,C,'primal');dense_old(br,matrix,C,'dual')
  for t,ar0,br0 in zip(ss,ar,br):
   F0=s['final'][t+112];collector=int(meta['collectors'][str(t)])
   emit_old(['MOVE',ar0,C,F0,False],'primal');emit_old(['MOVE',br0,C,F0,False],'dual');emit_old(['ADD',collector,ar0,'1',F0],'primal');emit_old(['ADD',br0,raw[host[t][1]],'-1',F0],'dual');emit_old(['MOVE',ar0,F0,127,False],'primal');emit_old(['MOVE',br0,F0,127,False],'dual')
  dense_old(ar,mt,127,'primal');dense_old(br,mt,127,'dual')
  need([e for e,bank in tagged]==f['program'][fg['begin']:fg['end']],'entire old paired frame block independently reconstructed')
  drop.update(fg['begin']+i+offset for i,(e,bank) in enumerate(tagged) if bank=='dual')
  old_group=next(g for g in p['parent_cohort_collection_provenance']['groups'] if set(g['donors'])==set(group['S']+group['T']))
  dg=next(g for g in p['parent_paired_collection_provenance']['groups'] if g['chart']==old_group['chart']);block=d['program'][dg['begin']:dg['end']];where=locate(block)
  need(set(dg['first_donors'])==set(group['S']+group['T']),'whole old hosted S/T cohort replaced')
  drop.update(range(where,where+len(block)));removed_blocks.append([where,where+len(block)])
 ext=next(g for g in p['parent_paired_collection_provenance']['groups'] if g['chart']==1105)
 need(ext['first_donors']==EXTERNAL and ext['kind']=='rank2_direct_cochart','two real external source records')
 extblock=d['program'][ext['begin']:ext['end']];ext_start=locate(extblock);drop.update(range(ext_start,ext_start+len(extblock)))
 extreceivers=set(EXTRA_READS[0])|set(EXTRA_READS[1]);old_external={j:{h:F(0) for h in extreceivers} for j in EXTERNAL}
 for e in extblock:
  need(e[0] in ('ADD','MOVE'),'unmixed actual direct external block')
  if e[0]=='ADD':
   j=next((j for j in EXTERNAL if e[1]==raw[host[j][0]]),None);h=next((h for h in extreceivers if e[2]==raw[host[h][1]]),None)
   need(j is not None and h is not None,'genuine old external observation');old_external[j][h]+=F(e[3])
 need(all(old_external[j][h]==G[j,h] for j in EXTERNAL for h in extreceivers),'full old external coefficients independently derived, including d77 sign')
 for h in extreceivers:
  need((old_external[12][h]+old_external[31][h])/2==EXTRA_READS[0].get(h,0) and (old_external[12][h]-old_external[31][h])/2==EXTRA_READS[1].get(h,0),'actual rank1-plus-rank1 external factorization')
 for j in K:
  r=host[j][1];events=[i for i,e in enumerate(p['program']) if e[0]=='MOVE' and e[1]==raw[r]]
  if j in extreceivers:need(len(events)==2 and set(events)<=drop,'both genuine split Y2 path segments removed once')
  else:need(len(events)==1 and p['program'][events[0]]==['MOVE',raw[r],s['initial'][r],s['final'][r],False],'original genuine direct Y2 path');drop.add(events[0])
 need(all(i>=start for i in drop) and not set(p['native_event_to_physical'])&drop,'no preceding dependency or native instruction removed')
 entry,entryloc,_=replay(p,spaces,start,True);q={r:{raw[r]:F(1),r:F(-1)} for r in raw}
 for j in K:
  for r in host[j]:need(entry[raw[r]]==q[r] and entryloc[raw[r]]==s['initial'][r],'actual untouched paired entry field')
 for j in EXTERNAL:
  r=host[j][0];need(entry[raw[r]]==q[r] and entryloc[raw[r]]==s['initial'][r],'actual untouched external input')
 # Construct the cyclic schedule from source spans and actual Gram entries.
 cyc=[];where={};control={};geometries=[]
 def emit(e):cyc.append(e);return len(cyc)-1
 def move(r,x,y):
  need(x!=y and spaces[x]<spaces[y],'proper ascending source route')
  need(where.get(r,s['initial'][r])==x,'actual current raw site in cyclic builder');emit(['MOVE',raw[r],x,y,False]);where[r]=y
 def read(donors,receivers,at,label):
  for x in donors:
   for y in receivers:
    b0,d0=host[x][0],host[y][1];need(where[b0]==where[d0]==at and abs(G[x,y])==F(1,2),'actual source cochart and cross-family coefficient')
    event=emit(['ADD',raw[b0],raw[d0],str(G[x,y]),at]);control.setdefault(label,event)
 E=chart(EXTERNAL);Jextra=[chart(EXTERNAL+g['S']+g['T']) for g in GROUPS];need(len(spaces[E])==4 and all(len(spaces[J])==32 for J in Jextra),'true external dimension2 and dimension5 joins')
 bp,bm=[host[j][0] for j in EXTERNAL]
 for b0 in (bp,bm):move(b0,s['initial'][b0],E)
 emit(['ADD',raw[bm],raw[bp],'-1',E]);control['external_half']=emit(['ADD',raw[bp],raw[bm],'1/2',E]);emit(['SCALE',raw[bm],'-1/2',E])
 for b0,J in zip((bp,bm),Jextra):move(b0,E,J)
 for gi,g in enumerate(GROUPS):
  bb,ss,tt=[g[k] for k in ('B','S','T')];D={k:chart(g[k]) for k in g};J={'BS':chart(bb+ss),'BT':chart(bb+tt),'ST':chart(ss+tt)}
  need(all(len(spaces[c])==8 for c in D.values()) and all(len(spaces[c])==16 for c in J.values()),'source family and pair-join dimensions3/4')
  for pair,third in [('BS','T'),('BT','S'),('ST','B')]:
   need(all(spaces[J[pair]]<spaces[s['final'][host[h][1]]] for h in g[third]),'actual third-family facet containments')
  for family in ('B','S','T'):
   for h in g[family]:r=host[h][0];move(r,s['initial'][r],D[family])
  for family,dest in [('B','T'),('S','B'),('T','S')]:
   for h in g[family]:r=host[h][1];move(r,s['initial'][r],D[dest])
  read(tt,bb,D['T'],'old_T_from_B');read(bb,ss,D['B'],'old_B_from_S');read(ss,tt,D['S'],'new_S_from_T')
  for family,pair in [('B','BS'),('S','ST'),('T','BT')]:
   for h in g[family]:r=host[h][0];move(r,where[r],J[pair])
  for family,pair in [('B','ST'),('S','BT'),('T','BS')]:
   for h in g[family]:r=host[h][1];move(r,where[r],J[pair])
  read(ss,bb,J['ST'],'old_S_from_B');read(tt,ss,J['BT'],'new_T_from_S');read(bb,tt,J['BS'],'new_B_from_T')
  for family in ('B','S','T'):
   for h in g[family]:
    b0,d0=host[h];move(b0,where[b0],127);move(d0,where[d0],Jextra[gi] if h in EXTRA_READS[gi] else s['final'][d0])
  encoded=(bp,bm)[gi]
  for h,c0 in EXTRA_READS[gi].items():
   d0=host[h][1];need(where[d0]==where[encoded]==Jextra[gi],'genuine externally needed receiver read')
   event=emit(['ADD',raw[encoded],raw[d0],str(c0),Jextra[gi]]);control.setdefault('external_receiver',event);move(d0,Jextra[gi],s['final'][d0])
  move(encoded,Jextra[gi],127);geometries.append({'families':g,'single_charts':D,'pair_charts':J,'external_join':Jextra[gi]})
 emit(['ADD',raw[bp],raw[bm],'1',127]);control['external_inverse']=emit(['SCALE',raw[bm],'-2',127]);emit(['ADD',raw[bm],raw[bp],'1',127])
 ops=[];lineage=[];bound={};insert=None
 for i,e in enumerate(p['program']):
  if i==start:insert=len(ops);ops.extend(cyc);lineage.extend([None]*len(cyc))
  bound[i]=len(ops)
  if i not in drop:ops.append(copy.deepcopy(e));lineage.append(i)
 need(ops==w['program'],'all78011 operations independently reconstructed')
 need(lineage==w['parent_event_of_output'],'exact independent parent lineage')
 need(w['marks']=={name:bound[i] for name,i in p['marks'].items()} and w['native_event_to_physical']==[bound[i] for i in p['native_event_to_physical']],'every retained cut and native operation map')
 first_raw={raw[z] for x in xs for z in (x,x+112)}
 def touches_first(e):return e[1] in first_raw or e[0] in ('ADD','COPY') and e[2] in first_raw
 need([e for e in ops if touches_first(e)]==[e for e in p['program'] if touches_first(e)],'all208 first-bank instruction projection literal and unchanged')
 before,bl,_=replay(p,spaces,p['marks']['common_starts'],True);actual,al,_=replay(w,spaces,w['marks']['common_starts'],True);want={r:row.copy() for r,row in before.items()};newterms=[]
 for g in GROUPS:
  for outfamily,infamily in [('B','T'),('S','T'),('T','S')]:
   for h in g[outfamily]:
    for j in g[infamily]:
     b0,d0=host[h][0],host[j][1];c0=G[h,j];need(c0 and not before[raw[b0]].get(raw[d0]),'genuinely absent parent transpose coefficient')
     want[raw[b0]]=rowplus(want[raw[b0]],q[d0],c0);newterms.append((h,j,c0))
 need(len(newterms)==72 and actual==want and al==bl,'exact all1880 inputs: only72 new transpose coefficients')
 need(all(actual[raw[host[h][1]]]==q[host[h][1]] for h in H),'all96 true d values remain unchanged')
 need(all(actual[raw[z]]==before[raw[z]] for x in xs for z in (x,x+112)),'all208 current first-bank rows unchanged')
 for h in EXTERNAL:need(actual[raw[host[h][0]]]==before[raw[host[h][0]]],'complete external two-record duties preserved')
 suffix=w['program'][w['marks']['common_starts']:];need(suffix==p['program'][p['marks']['common_starts']:],'literal identical common suffix')
 for h in K:
  r=host[h][0];uses=[e for e in suffix if e[1]==raw[r] or e[0] in ('ADD','COPY') and e[2]==raw[r]]
  need(uses==[['ADD',raw[r],r,'1',s['final'][r]]],'no later use of changed reverse field before final recoupling')
  recovered=actual[raw[r]]
  for i,j,c0 in newterms:
   if i==h:recovered=rowplus(recovered,actual[raw[host[j][1]]],-c0)
  need(recovered==before[raw[r]],'actual information inverse using preserved d records')
 M={}
 for h in H:
  r=host[h][0];coeff={j:actual[raw[r]].get(raw[host[j][1]],F(0)) for j in H};expected=q[r]
  for j,c0 in coeff.items():
   if c0:expected=rowplus(expected,q[host[j][1]],c0)
  need(actual[raw[r]]==expected,'complete actual reverse row has no hidden input dependence')
  need({int(j):F(c0) for j,c0 in w['paired_reverse_corrections'][str(r)]}=={host[j][1]:c0 for j,c0 in coeff.items() if c0},'all96 current reverse metadata rows exact')
  M[h]={j:c0+F(h==j) for j,c0 in coeff.items() if c0+F(h==j)}
 outside=[h for h in H if h not in K];pivots=[h for h in K if h not in B]
 need(len(outside)==74 and len(pivots)==14,'22-port principal block and14 kernel pivots')
 need(all(M[i].get(j,F(0))==G[i,j] for i in K for j in K) and all(not M[i].get(j) for i in K for j in outside),'actual closed22-port Gram block')
 kernel=[]
 for u in pivots:
  z={h:-G[h,u] if h in B else F(h==u) if h in pivots else G[h,u] for h in H}
  need(all(sum(c0*z[j] for j,c0 in M[i].items())==0 for i in H),'fourteen full actual residual kernels')
  kernel.append({str(h):str(c0) for h,c0 in z.items() if c0})
 minor=B+outside
 need(len(minor)==82 and all(M[i].get(j,F(0))==(i==j) for i in B for j in minor) and all(M[i].get(j,F(0))==(i==j) for i in outside for j in outside),'explicit unit block-triangular82 minor')
 _,final,bill=replay(w,spaces);_,parentfinal,oldbill=replay(p,spaces);need(final==parentfinal and set(final)==set(range(1880)),'all final locations and owned retirement')
 need(json.loads(json.dumps(bill))==author['bill'],'independently counted full typed bill')
 delta=Counter(bill['raw_histogram']);delta.subtract(oldbill['raw_histogram']);delta={r:n for r,n in delta.items() if n}
 need(delta=={1:34,2:2,3:20,4:20,5:-2,6:-4,8:-18} and sum(r*n for r,n in bill['raw_histogram'].items())==3200,'complete signed raw invoice and conserved rankmass')
 need(all(bill['move_rank_histogram'].get(r,0)-bill['raw_histogram'].get(r,0)==oldbill['move_rank_histogram'].get(r,0)-oldbill['raw_histogram'].get(r,0) for r in set(bill['move_rank_histogram'])|set(oldbill['move_rank_histogram'])),'identical paid owned profile at every rank')
 ordinary={op:bill['opcode_counts'].get(op,0)-oldbill['opcode_counts'].get(op,0) for op in sorted(set(bill['opcode_counts'])|set(oldbill['opcode_counts']))}
 need(ordinary=={'ADD':-110,'CLEAR':-44,'COPY':0,'INIT':-44,'MOVE':52,'SCALE':2},'complete actual ordinary increment')
 ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes();need(sha(ib)==INVOICE,'H4 original invoice pin');iv=json.loads(ib)
 originalraw=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw)
 targets=Counter({int(k):v for k,v in iv['T4'].items()});paid=Counter({int(k):v for k,v in iv['P4'].items()})
 for r in set(originalraw)|set(bill['raw_histogram']):paid[r]+=18*(bill['raw_histogram'].get(r,0)-originalraw[r])
 paid[9]+=144;paid[1]+=144
 need({str(r):n for r,n in paid.items()}==author['conditional_caller']['P_partial'],'all full H4,8rank9,8rank1 obligations charged')
 lo,hi=interval({r:targets[r]-paid[r] for r in targets.keys()|paid.keys()});lo/=18;hi/=18;claimed=author['conditional_caller']
 need(F(claimed['remaining_moment_per_native_lower'])<=lo<=hi<=F(claimed['remaining_moment_per_native_upper']),'fresh160-bit directed complete margin')
 fee_lo,fee_hi=interval(delta)
 result={'status':'PASS_INDEPENDENT_CYCLIC_DUAL_RANK82','source_sha256':SOURCE,'parent_sha256':PARENT,'frame_sha256':FRAME,'word_sha256':sha(wb),'word_payload_sha256':sha(gzip.decompress(wb)),'exact_input_columns':1880,'independently_reconstructed_operations':len(ops),'source_geometries':geometries,'new_transpose_coefficients':[[i,j,str(c0)] for i,j,c0 in newterms],'closed_principal_ports':K,'actual_reverse_rank':82,'explicit_kernel_basis':kernel,'unit82_minor_order':minor,'all208_first_bank_rows_and_instruction_projection_unchanged':True,'original_external_coefficients':{str(j):{str(h):str(c0) for h,c0 in row.items()} for j,row in old_external.items()},'new_owned_moves':0,'full_bill':bill,'raw_increment':delta,'ordinary_increment':ordinary,'fresh_margin_lower':str(lo),'fresh_margin_upper':str(hi),'fresh_extra_fee_lower':str(fee_lo),'fresh_extra_fee_upper':str(fee_hi),'scope':'Exact finite current-source rank82 block and full provisional tariff; no complete supplier or new kappa.'}
 mutants={}
 def reject(name,m):
  try:
   mr,ml,_=replay(m,spaces,m['marks']['common_starts'],True);need(mr==want and ml==bl,'mutated exact1880 source state')
  except (ValueError,KeyError,IndexError) as e:mutants[name]=str(e)
  else:raise ValueError('unrejected actual word mutation '+name)
 for name,key,value in [('missing_new_transpose','new_B_from_T','0'),('missing_old_T_from_B','old_T_from_B','0'),('wrong_external_half','external_half','1'),('wrong_external_hub_inverse','external_inverse','2')]:
  m=copy.deepcopy(w);event=insert+control[key];m['program'][event][2 if m['program'][event][0]=='SCALE' else 3]=value;reject(name,m)
  if name=='missing_new_transpose':
   mr,_,_=replay(m,spaces,m['marks']['common_starts'],True);mutant_rank=rank([[mr[raw[host[h][0]]].get(raw[host[j][1]],F(0))+F(h==j) for j in H] for h in H]);need(mutant_rank==83,'actual one-missing-coefficient rank83');result['missing_one_coefficient_actual_rank']=mutant_rank
 event=next(i for i,e in enumerate(cyc) if e==['ADD',raw[bm],raw[host[77][1]],'1/2',Jextra[1]])
 m=copy.deepcopy(w);m['program'][insert+event][3]='-1/2';reject('wrong_source_d77_external_sign',m)
 m=copy.deepcopy(w);at=m['marks']['common_starts'];r=host[5][1];m['program'].insert(at,['MOVE',raw[r],s['initial'][r],s['final'][r],False]);m['marks']['common_starts']+=1;reject('spent_Y2_original_route_reused',m)
 m=copy.deepcopy(w);at=insert+len(cyc);r=5+112;m['program'].insert(at,['MOVE',raw[r],s['initial'][r],geometries[0]['single_charts']['T'],False]);m['marks']['common_starts']+=1;reject('first_Y_hoisted_before_E8_read',m)
 result['negative_controls']=mutants
 frozen=a.repo/'research/shared-wire-split-composition/frozen';pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def load_engine(filename):
  path=frozen/filename;need(sha(path.read_bytes())==pins[filename],'frozen physical map engine');spec=importlib.util.spec_from_file_location('independent_cyclic_'+filename[:-3],path);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod
 c=load_engine('clifford_exact.py');v=load_engine('native_verify.py');oldpairs={(e[2],e[3]) for e in p['program'] if e[0]=='MOVE'};pairs={(e[2],e[3]) for e in ops if e[0]=='MOVE'};maps=[]
 for x,y in sorted(pairs-oldpairs):
  recipe,_=c.lower_child(c.canonical_frame(9,tuple(frames[x])).adjoint().then(c.canonical_frame(9,tuple(frames[y]))));v.equal(v.recipe(recipe),v.adjoint(v.frame(frames[x],9))+v.frame(frames[y],9),'independent actual cyclic map')
  need(recipe['rank']==abs(len(frames[y])-len(frames[x])),'actual exact recursive map rank');maps.append({'source':x,'target':y,'recipe':recipe})
 need(len(maps)==74,'all74 distinct introduced map pairs')
 bad=copy.deepcopy(maps[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong global phase')
 except ValueError:result['wrong_global_phase_rejected']=True
 else:raise ValueError('wrong global phase survived')
 result['introduced_map_count']=len(maps);result['engine_pins']=pins
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.output/'MAPS.json').write_text(json.dumps(maps,indent=2,sort_keys=True)+'\n');print(result['status'],len(ops),'rank82',float(lo))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
