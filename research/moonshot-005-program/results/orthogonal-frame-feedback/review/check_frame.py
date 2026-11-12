#!/usr/bin/env python3
"""Independent Q^9 source reconstruction and exact replay of the two-frame word.

Does not import the author generator or its replay/cost helpers.
"""
import argparse,copy,gzip,hashlib,importlib.util,json,sys
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path

SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PPAY='bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a'
B=[5,56,65,69,77,96,100,103]
S=[0,7,20,27,36,46,57,111]
def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def span(a):
 s={0}
 for x in a:s|={y^x for y in tuple(s)}
 return frozenset(s)
def rowplus(a,b,c=F(1)):
 r=a.copy()
 for k,v in b.items():
  q=r.get(k,F(0))+c*v
  if q:r[k]=q
  else:r.pop(k,None)
 return r
def root9(v):
 T=[i for i in range(9) if v>>i&1]
 if len(T)==3:return [2 if i in T else -1 for i in range(9)]
 need(len(T)==7,'source root type');i,j=[k for k in range(9) if k not in T]
 return [3*(int(k==i)-int(k==j)) for k in range(9)]
def matmul(A,B):return [[sum((a*b for a,b in zip(r,c)),F(0)) for c in zip(*B)] for r in A]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]

def replay(w,spaces,stop=None,arithmetic=False):
 loc=dict(enumerate(w['initial']));rows={i:{i:F(1)} for i in range(1880)} if arithmetic else None
 count=Counter();ranks=Counter();rawranks=Counter();raw=set(w['private_role_map'].values());peak=0;lifetimes=0
 for k,e in enumerate(w['program'][:stop] if stop is not None else w['program']):
  op,r=e[:2];count[op]+=1;need(0<=r<1880+w['owned_fields'],'declared role')
  if op=='INIT':
   need(r>=1880 and r not in loc,'fresh owner');loc[r]=e[2];lifetimes+=1
   if arithmetic:rows[r]={}
  elif op=='CLEAR':
   need(r>=1880 and loc.get(r)==e[2],'owned retirement');del loc[r]
   if arithmetic:del rows[r]
  elif op=='MOVE':
   x,y,o=e[2:];need(type(o)is bool and o==(r>=1880) and loc.get(r)==x,'typed route at '+str(k));need(spaces[x]<spaces[y] or o and spaces[y]<spaces[x],'nested route')
   dim=abs((len(spaces[x]).bit_length()-1)-(len(spaces[y]).bit_length()-1));ranks[dim]+=1;rawranks[dim]+=int(r in raw);loc[r]=y
  elif op=='SCALE':
   c=F(e[2]);need(c and loc.get(r)==e[3],'nonzero local scale')
   if arithmetic:rows[r]={j:c*v for j,v in rows[r].items()}
  elif op in ('ADD','COPY'):
   z,c,at=e[2:];need(z!=r and loc.get(z)==loc.get(r)==at,'cochart read at '+str(k))
   if arithmetic:
    need(op!='COPY' or not rows[r],'COPY zero guard');rows[r]=rowplus(rows[r],rows[z],F(c))
  else:raise ValueError(op)
  peak=max(peak,len(loc)-1880)
 return rows,loc,{'instructions':sum(count.values()),'opcode_counts':dict(sorted(count.items())),'move_rank_histogram':dict(sorted(ranks.items())),'raw_histogram':dict(sorted((r,n) for r,n in rawranks.items() if n)),'owned_lifetimes':lifetimes,'peak_owned':peak,'final_owned':len(loc)-1880}

def reconstruct(source,parent,word,G,hosted,raw,spaces):
 groups=defaultdict(list)
 for b in B:groups[tuple(t for t in S if G[t,b])].append(b)
 need(len(groups)==2 and all(len(t)==4 and len(d)==4 for t,d in groups.items()),'independent four-by-four cohort partition')
 remaining=set(B)|{hosted[b][0] for b in B}|{hosted[t][1] for t in S};oldroutes={}
 for r in remaining:
  at=[i for i,e in enumerate(parent['program']) if e[0]=='MOVE' and e[1]==raw[r]]
  need(len(at)==1,'single unspent original path');i=at[0]
  need(parent['program'][i]==['MOVE',raw[r],source['initial'][r],source['final'][r],False] and 400<=i<parent['marks']['common_starts'],'authentic source direct path');oldroutes[r]=i
 collectors={t:1880+parent['owned_fields']+i for i,t in enumerate(S)};temps=[1880+parent['owned_fields']+8+i for i in range(4)]
 ops=[];meta=[]
 def emit(e):ops.append(e)
 def dense(rs,M,c):
  for j,r in enumerate(rs):emit(['INIT',temps[j],c]);emit(['ADD',temps[j],r,'1',c])
  for i,r in enumerate(rs):
   emit(['ADD',r,temps[i],'-1',c])
   for j,v in enumerate(M[i]):
    if v:emit(['ADD',r,temps[j],str(v),c])
  for j in range(4):emit(['CLEAR',temps[j],c])
 def block():
  for t in S:
   f=source['final'][t+112];need(source['initial'][hosted[t][1]]==3 and source['final'][hosted[t][1]]==f,'authentic Y2 endpoint');emit(['INIT',collectors[t],f]);emit(['MOVE',raw[hosted[t][1]],3,f,False])
  for ts,ds in sorted(groups.items()):
   cs=frozenset.intersection(*(spaces[source['final'][t+112]] for t in ts));need(len(cs)==64,'dimension-six acquisition')
   charts=[i for i,a in enumerate(spaces) if a==cs];need(charts,'actual acquisition chart declared');c=charts[0]
   M=[[-G[t,b] for b in ds] for t in ts];Mt=[list(z) for z in zip(*M)];need(matmul(M,Mt)==eye(4) and matmul(Mt,M)==eye(4),'source Hadamard is orthogonal')
   for b in ds:need(spaces[source['initial'][b]]<cs,'donor line in acquisition chart')
   ar=[raw[b] for b in ds];br=[raw[hosted[b][0]] for b in ds]
   for rs in (ar,br):
    for b,r in zip(ds,rs):emit(['MOVE',r,source['initial'][b],c,False])
   dense(ar,M,c);dense(br,M,c)
   for t,r,z in zip(ts,ar,br):
    f=source['final'][t+112];emit(['MOVE',r,c,f,False]);emit(['MOVE',z,c,f,False]);emit(['ADD',collectors[t],r,'1',f]);emit(['ADD',z,raw[hosted[t][1]],'-1',f]);emit(['MOVE',r,f,127,False]);emit(['MOVE',z,f,127,False])
   dense(ar,Mt,127);dense(br,Mt,127);meta.append({'donors':ds,'receivers':list(ts),'chart':c,'matrix':[[str(v) for v in row] for row in M]})
 skip=set(oldroutes.values());rawY={raw[t+112]:t for t in S}
 for k,e in enumerate(parent['program']):
  if k==410:block()
  if k==parent['marks']['common_starts']:
   for t in S:
    f=source['final'][t+112];emit(['ADD',raw[t+112],collectors[t],'1',f]);emit(['CLEAR',collectors[t],f])
  if k in skip:continue
  emit(copy.deepcopy(e))
 if ops!=word['program']:
  first=next((i for i,(e,f) in enumerate(zip(ops,word['program'])) if e!=f),min(len(ops),len(word['program'])))
  raise ValueError('literal mismatch at '+str(first)+': '+str(ops[first:first+3])+' vs '+str(word['program'][first:first+3]))
 return meta,oldroutes

def exact_bounds(rank,precision=110):
 den=1<<precision;target=rank**199*den**200;lo=0;hi=rank*den+1
 while hi-lo>1:
  m=(hi+lo)//2
  if m**200<=target:lo=m
  else:hi=m
 need(lo**200<=target<(lo+1)**200,'dyadic exact root bracket');return F(lo,den),F(lo if lo**200==target else lo+1,den)

def main(a):
 sourcebytes=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();parentbytes=(a.repo/'research/moonshot-005-program/results/paired-cohort/output/WORD.json.gz').read_bytes();wb=a.word.read_bytes()
 need(sha(sourcebytes)==SPIN and sha(gzip.decompress(parentbytes))==PPAY,'immutable input pins')
 source=json.loads(gzip.decompress(sourcebytes));p=json.loads(gzip.decompress(parentbytes));w=json.loads(gzip.decompress(wb));author=json.loads((a.word.parent/'RESULT.json').read_text());raw={int(k):v for k,v in p['private_role_map'].items()}
 need(w['initial']==p['initial'] and w['private_role_map']==p['private_role_map'],'same1880 initial state')
 need(w['additional_charts'][:len(p['additional_charts'])]==p['additional_charts'],'unchanged existing charts')
 frames=source['frames']+[d['frame'] for d in w['additional_charts']];spaces=list(map(span,frames));need(all(len(spaces[i])==2**len(f) for i,f in enumerate(frames)),'independent actual frame bases')
 H=[source['live'][k] for k in source['hosted']['Dports']];hosted={h:(x,y) for h,x,y in zip(H,source['hosted']['X2'],source['hosted']['Y2'])};need(not(set(B)&set(S)) and set(B+S)<=set(H),'two disjoint independently hosted frames')
 r9={h:root9(source['frames'][source['initial'][h]][0]) for h in source['live']};G={(i,j):F(sum(a*b for a,b in zip(r9[i],r9[j])),18) for i in r9 for j in r9}
 need(all(G[i,j]==(i==j) for group in (B,S) for i in group for j in group),'independent Q9 orthogonal frames')
 groups,oldroutes=reconstruct(source,p,w,G,hosted,raw,spaces)
 need(all(str(t+112) not in p['corrections'] for t in S),'new first-Y rows disjoint from every prior correction')
 lineage=w['parent_event_of_output'];need(len(lineage)==len(w['program']),'complete parent lineage')
 occurrences=defaultdict(list)
 for j,k in enumerate(lineage):
  if k is not None:occurrences[k].append(j)
 replaced=set(oldroutes.values())
 for k,e in enumerate(p['program']):
  js=occurrences[k]
  if k in replaced:need(js and all(w['program'][j][0]=='MOVE' and w['program'][j][1]==e[1] for j in js),'rerouted parent move lineage')
  else:need(len(js)==1 and w['program'][js[0]]==e,'unchanged parent operation lineage')
 need([k for k in lineage if k is not None and k not in replaced]==[k for k in range(len(p['program'])) if k not in replaced],'retained parent chronology')
 need(w['native_event_to_physical']==[occurrences[k][0] for k in p['native_event_to_physical']],'actual native clock map')
 for name,k in p['marks'].items():
  if k not in replaced:need(w['marks'][name]==occurrences[k][0],'actual retained boundary '+name)
 prows,ploc,_=replay(p,spaces,p['marks']['common_starts'],True);rows,loc,_=replay(w,spaces,w['marks']['common_starts'],True)
 need(ploc==loc and set(prows)==set(rows),'same exact entry fields and chart locations');q={r:{raw[r]:F(1),r:F(-1)} for r in raw};expected={r:v.copy() for r,v in prows.items()}
 for t in S:
  for b in B:
   expected[raw[t+112]]=rowplus(expected[raw[t+112]],q[b],-G[t,b]);expected[raw[hosted[b][0]]]=rowplus(expected[raw[hosted[b][0]]],q[hosted[t][1]],G[b,t])
 need(rows==expected,'all1880 input columns of all prefix fields')
 suffix=w['program'][w['marks']['common_starts']:];need(suffix==p['program'][p['marks']['common_starts']:],'identical common suffix')
 for r in [t+112 for t in S]+[hosted[b][0] for b in B]:
  uses=[e for e in suffix if e[1]==raw[r] or e[0] in ('ADD','COPY') and e[2]==raw[r]];need(uses==[['ADD',raw[r],r,'1',source['final'][r]]],'changed row only recouples later')
 for b in B:
  need(rows[raw[b]]==q[b] and loc[raw[b]]==127,'actual donor restored before E8');v=rows[raw[hosted[b][0]]]
  for t in S:v=rowplus(v,rows[raw[hosted[t][1]]],-G[b,t])
  need(v==q[hosted[b][0]],'explicit hosted inverse')
 for t in S:
  need(rows[raw[hosted[t][1]]]==q[hosted[t][1]],'original reverse source retained');v=rows[raw[t+112]]
  for b in B:v=rowplus(v,rows[raw[b]],G[t,b])
  need(v==prows[raw[t+112]],'forward inverse returns parent')
 # Extract the residual from actual input coefficients, not metadata.
 M=[]
 for i,h in enumerate(H):
  x=hosted[h][0];coeff=[rows[raw[x]].get(raw[hosted[j][1]],F(0)) for j in H];want=q[x]
  for j,c in zip(H,coeff):want=rowplus(want,q[hosted[j][1]],c)
  need(rows[raw[x]]==want,'actual reverse row has no hidden source dependence');M.append([c+F(i==j) for j,c in enumerate(coeff)])
 idx={h:i for i,h in enumerate(H)};U=[h for h in H if h not in B];kernels=[]
 for t in S:
  k={h:F(0) for h in H}
  for b in B:k[b]=-G[b,t]
  for h in U:k[h]=sum((G[h,b]*G[b,t] for b in B),F(0))
  need(all(k[u]==(u==t) for u in S),'eight independent kernel pivots');need(all(sum(c*k[h] for c,h in zip(row,H))==0 for row in M),'actual full residual kernel');kernels.append({str(h):str(v) for h,v in k.items() if v})
 # Deleting S rows/columns gives an explicit unit block-triangular 88-minor.
 order=B+[h for h in H if h not in B+S]
 minor=[[M[idx[i]][idx[j]] for j in order] for i in order]
 need(len(minor)==88 and all(minor[i][j]==(i==j) for i in range(8) for j in range(88)) and all(minor[i][j]==(i==j) for i in range(8,88) for j in range(8,88)),'unit triangular88 minor')
 _,final,bill=replay(w,spaces);_,pfinal,pbill=replay(p,spaces);need(final==pfinal and set(final)==set(range(1880)),'all public endpoints and owned retirement');need(json.loads(json.dumps(bill))==author['bill'],'independent full typed bill')
 residual_before_history=0
 for t in source['live']:
  y=t+112;normal=F(1) if t in hosted else F(1,2);want=rowplus(q[y],q[t]);want={k:normal*v for k,v in want.items()};delta=rowplus(rows[raw[y]],want,-1)
  residual_before_history+=sum(bool(delta.get(raw[x])) for x in source['live'])
 need(residual_before_history==4576 and author['forward_residual_coefficients']==4576-7,'prefix residual and seven retained source-history cancellations distinguished')
 invoicepath=a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json';invoice=json.loads(invoicepath.read_text());need(sha(invoicepath.read_bytes())=='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248','complete invoice pin')
 oldraw=Counter(abs(len(source['frames'][e[3]])-len(source['frames'][e[2]])) for e in source['program'] if e[0]=='MOVE' and e[1] in raw);R=Counter(bill['raw_histogram']);T={int(r):n for r,n in invoice['T4'].items()};P={int(r):n for r,n in invoice['P4'].items()}
 for r in R.keys()|oldraw.keys():P[r]=P.get(r,0)+18*(R[r]-oldraw[r])
 P[9]=P.get(9,0)+18*8;need({str(r):n for r,n in P.items()}==author['conditional_caller']['P_partial'],'complete recomputed paid profile')
 lo=hi=F(0)
 for r in T.keys()|P.keys():
  c=T.get(r,0)-P.get(r,0);l,h=exact_bounds(r);lo+=c*(l if c>=0 else h);hi+=c*(h if c>=0 else l)
 lo/=18;hi/=18;need(F(author['conditional_caller']['remaining_moment_per_native_lower'])<=lo<=hi<=F(author['conditional_caller']['remaining_moment_per_native_upper']),'independent dyadic tariff refines claimed interval')
 result={'status':'PASS_INDEPENDENT_SOURCE_FRAME_WORD_RANK88','source_sha256':SPIN,'parent_payload_sha256':PPAY,'word_sha256':sha(wb),'word_payload_sha256':sha(gzip.decompress(wb)),'literal_operations_independently_reconstructed':len(w['program']),'input_columns':1880,'groups':groups,'actual_reverse_rank':88,'independent_kernel_rows':kernels,'unit_triangular_minor_order':order,'prefix_forward_residual':4576,'final_forward_residual':4569,'bill':bill,'independent_dyadic_margin_lower':str(lo),'independent_dyadic_margin_upper':str(hi),'scope':'Independent finite source proof and exact residual matrix audit; physical complete suppliers and all foundations remain.'}
 atrestore,restoreloc,_=replay(w,spaces,w['marks']['all_active_donors_restored'],True)
 need(all(atrestore[raw[x]]==q[x] and restoreloc[raw[x]]==127 for x in source['live']),'all104 authentic originals restored at the actual pre-E8 cut')
 mutants={}
 def reject(name,m):
  try:
   mr,ml,_=replay(m,spaces,m['marks']['common_starts'],True);need(mr==rows and ml==loc,'mutated exact prefix state')
  except (ValueError,KeyError,IndexError) as e:mutants[name]=str(e)
  else:raise ValueError('unrejected mutant '+name)
 meta=w['second_frame_feedback'];g=meta['groups'][0]
 for name,event,coeff in [('forward_original_not_cleared',g['forward_encode']['clear_original'][0],'0'),('reverse_original_not_cleared',g['reverse_encode']['clear_original'][0],'0'),('reverse_injection_sign',g['reads'][0]['reverse'],'1'),('forward_inverse_wrong_clear',g['forward_decode']['clear_original'][0],'0')]:
  m=copy.deepcopy(w);m['program'][event][3]=coeff;reject(name,m)
 m=copy.deepcopy(w);e=next(i for i,e in enumerate(m['program']) if e==['MOVE',raw[hosted[S[0]][1]],3,source['final'][S[0]+112],False]);m['program'][e][3]=127;reject('authentic_Y2_skips_actual_facet',m)
 m=copy.deepcopy(w);e=next(i for i,e in enumerate(m['program']) if e==['ADD',raw[S[0]+112],meta['collectors'][str(S[0])],'1',source['final'][S[0]+112]]);m['program'][e][3]='0';reject('forward_collector_unconsumed',m)
 m=copy.deepcopy(w);k=m['marks']['common_starts'];m['program'].insert(k,copy.deepcopy(p['program'][oldroutes[B[0]]]));m['marks']['common_starts']+=1;reject('old_direct_route_spent_twice',m)
 result['negative_controls']=mutants
 # Pinned physical lowering and a separately implemented Pauli/global-phase check.
 frozen=a.repo/'research/shared-wire-split-composition/frozen';pins={'clifford_exact.py':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962','native_verify.py':'3049471905b47b385c88378a1a3be7a18b8858aadd035b8a6da2f4a03b470f38'}
 def load_engine(filename):
  path=frozen/filename;need(sha(path.read_bytes())==pins[filename],'exact retained engine pin');spec=importlib.util.spec_from_file_location('independent_frame_'+filename[:-3],path);mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod
 c=load_engine('clifford_exact.py');v=load_engine('native_verify.py');prior={(e[2],e[3]) for e in p['program'] if e[0]=='MOVE'};now={(e[2],e[3]) for e in w['program'] if e[0]=='MOVE'};maps=[]
 for x,y in sorted(now-prior):
  recipe,_=c.lower_child(c.canonical_frame(9,tuple(frames[x])).adjoint().then(c.canonical_frame(9,tuple(frames[y]))));v.equal(v.recipe(recipe),v.adjoint(v.frame(frames[x],9))+v.frame(frames[y],9),'independent actual map')
  need(recipe['rank']==abs(len(frames[y])-len(frames[x])),'exact introduced rank');maps.append({'source':x,'target':y,'recipe':recipe})
 need(len(maps)==16,'sixteen distinct introduced chart pairs')
 bad=copy.deepcopy(maps[0]);bad['recipe']['left']['phase']=(bad['recipe']['left']['phase']+1)%4
 try:v.equal(v.recipe(bad['recipe']),v.adjoint(v.frame(frames[bad['source']],9))+v.frame(frames[bad['target']],9),'wrong phase')
 except ValueError:result['wrong_global_phase_rejected']=True
 else:raise ValueError('wrong global phase survived')
 result['introduced_maps']=maps;result['engine_pins']=pins
 a.output.mkdir(parents=True,exist_ok=True)
 (a.output/'FRAME-REVIEW.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ['status','literal_operations_independently_reconstructed','actual_reverse_rank','prefix_forward_residual','final_forward_residual','independent_dyadic_margin_lower','independent_dyadic_margin_upper']},indent=2))

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
