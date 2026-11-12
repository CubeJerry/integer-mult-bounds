#!/usr/bin/env python3
"""Exact finite source identities for the general minimal-eight-packet barrier.

The universal transport/rank argument is in PROOF.md; this verifies its complete
finite source domain, rational factorization and directed power arithmetic.
"""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
D42PIN='77c996ff9233f087a0e024c107b552f022adeca51cf5540c2487ef80cb2a2506'
PRIME=65537
EXPECTED_SPECTRUM={0:1,20:3,22:48,24:28,26:96,28:28,30:48,32:3,52:1}

def need(q,m):
 if not q:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def span(vs):
 S={0}
 for v in vs:S|={x^v for x in tuple(S)}
 return frozenset(S)
def binary_rank(vs):
 B={}
 for v in vs:
  for k in sorted(B,reverse=True):
   if v>>k&1:v^=B[k]
  if v:B[v.bit_length()-1]=v
 return len(B)
def root(v):
 one=[i for i in range(9) if v>>i&1]
 if len(one)==3:return [2*int(i in one) for i in range(8)] if 8 in one else [1 if i in one else -1 for i in range(8)]
 need(len(one)==7,'root source weight');i,j=[i for i in range(9) if i not in one]
 return [1 if k==i else -1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def rational_rank_by_modular_witness(rows):
 # Every k-by-k root minor, k<=8, has absolute determinant<=8^(k/2)<=4096.
 # PRIME>4096, so rank mod PRIME is exactly rational rank, not a heuristic.
 M=[list(r) for r in rows];labels=list(range(len(M)));k=0;pivots=[]
 if not M:return 0,[]
 for j in range(len(M[0])):
  p=next((i for i in range(k,len(M)) if M[i][j]%PRIME),None)
  if p is None:continue
  M[k],M[p]=M[p],M[k];labels[k],labels[p]=labels[p],labels[k];q=pow(M[k][j]%PRIME,-1,PRIME);M[k]=[x*q%PRIME for x in M[k]]
  for i in range(k+1,len(M)):
   c=M[i][j]%PRIME
   if c:M[i]=[(x-c*y)%PRIME for x,y in zip(M[i],M[k])]
  pivots.append(labels[k]);k+=1
  if k==len(M):break
 return k,pivots
def inverse(M):
 n=len(M);B=[[Q(x) for x in r]+[Q(i==j) for j in range(n)] for i,r in enumerate(M)];det=Q(1)
 for j in range(n):
  p=next(i for i in range(j,n) if B[i][j])
  if p!=j:B[p],B[j]=B[j],B[p];det=-det
  q=B[j][j];det*=q;B[j]=[x/q for x in B[j]]
  for i in range(n):
   if i!=j:
    q=B[i][j]
    if q:B[i]=[x-q*y for x,y in zip(B[i],B[j])]
 return [r[n:] for r in B],det
def power(r):
 if not r:return Q(0),Q(0)
 den=1<<120;target=r**199*den**200;lo,hi=0,r*den+1
 while lo+1<hi:
  m=(lo+hi)//2
  if m**200<=target:lo=m
  else:hi=m
 need(lo**200<=target<(lo+1)**200,'directed rational power enclosure')
 return Q(lo,den),Q(lo+1,den)
def interval(C):
 lo=hi=Q(0)
 for r,c in C.items():
  a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi

def main(a):
 sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();ib=(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes()
 need(sha(sb)==SPIN and sha(ib)==IPIN,'immutable source and invoice pins')
 if a.distance42:need(sha((a.distance42/'PROOF.md').read_bytes())==D42PIN,'exact distance42 theorem dependency')
 s=json.loads(gzip.decompress(sb));invoice=json.loads(ib);xs=s['live'];N={x:s['frames'][s['initial'][x]][0] for x in xs};A={x:root(N[x]) for x in xs};normals=list(N.values())
 omitted=[v for v in range(512) if v.bit_count() in (3,7) and v not in normals]
 need(len(xs)==104 and len(set(normals))==104 and len(omitted)==16,'actual104-source and16 omitted directions')
 need(all(PRIME%d for d in range(2,257)) and PRIME>4096,'exact modular rank bound prime')
 need(all(dot(r,r)==8 for r in A.values()),'Hadamard minor bound root norms')
 need(rational_rank_by_modular_witness(list(A.values()))[0]==8,'source E8 evaluation space dimension8')
 facets={x:span(s['frames'][s['final'][x+112]]) for x in xs}
 for x in xs:
  need(len(facets[x])==256 and facets[x]==frozenset(v for v in range(512) if not (v&N[x]).bit_count()%2),'actual full firstY facet')
  need(len(s['frames'][s['initial'][x+112]])==0,'actual firstY initial empty chart')
 locality=[];rank7=[]
 for z in range(1,512):
  bad=[x for x in xs if (N[x]&z).bit_count()%2];r,piv=rational_rank_by_modular_witness([A[x] for x in bad])
  need(r in(7,8),'every nonzero line locality rank at least7')
  if r==7:
   rank7.append(z);need(z in omitted and all(dot(root(z),A[x])==0 for x in bad),'unique omitted-root null line')
  locality.append({'chart_line':z,'forbidden_receiver_count':len(bad),'rational_root_rank':r,'independent_root_source_roles':[bad[i] for i in piv]})
 need(rank7==omitted,'only16 omitted root lines admit any nonzero decoder row')
 spectra=[];code_map={};support_map={};pair_patterns=[]
 for z in omitted:
  support=[x for x in xs if dot(root(z),A[x])];need(len(support)==52,'exact omitted-root decoder support52')
  need(all(bool(dot(root(z),A[x]))==(not((N[x]&z).bit_count()%2)) for x in xs),'root support equals source chart incidence')
  need(frozenset.intersection(*(facets[x] for x in support))==span([z]),'root packet facet intersection exact line')
  code={u:sum(((N[x]&u).bit_count()%2)<<i for i,x in enumerate(support)) for u in range(512)};words=set(code.values());spectrum=Counter(w.bit_count() for w in words);p=(1<<52)-1
  need(len(words)==256 and [u for u,w in code.items() if not w]==[0,z] and p in words,'source evaluation code dimension8/kernel/current normal/allones')
  need(dict(spectrum)==EXPECTED_SPECTRUM and 32<2*20,'complete code spectrum and minimal-word gap')
  proper=[w for w in words if w not in(0,p)]
  need(all(not(u&v) and (u^v)==p for u in proper for v in proper if not(u&v)),'all disjoint proper nonzero pairs are complements')
  code_map[z]=code;support_map[z]=support
  spectra.append({'normal':z,'source_roles':support,'code_dimension':8,'code_words':len(words),'spectrum':dict(sorted(spectrum.items()))})
  for a0,b0 in itertools.combinations([q for q in omitted if q!=z],2):
   u,v=code[a0],code[b0];counts=Counter(((u>>i)&1,(v>>i)&1) for i in range(52))
   need(len(counts)==4 and min(counts.values())>=7,'all four preceding-root patterns survive source omission')
   need(p not in{0,u,v,u^v} and len({0,u,v,u^v})==4,'rank2 containing-triple projection excludes allones')
   pair_patterns.append({'current':z,'prior':[a0,b0],'counts':[counts[(0,0)],counts[(0,1)],counts[(1,0)],counts[(1,1)]]})
 need(len(pair_patterns)==1680,'all current-root and prior-pair cases')
 # Show that genuine nonorthogonal decoder roots still factor the same full map.
 example=[25,42,52,67,76,82,97,127];W=[[root(z)[j] for z in example] for j in range(8)];Wi,det=inverse(W)
 need(any(dot(root(x),root(y)) for x,y in itertools.combinations(example,2)),'example is genuinely nonorthogonal')
 E=[[sum(Wi[i][k]*A[x][k] for k in range(8)) for x in xs] for i in range(8)]
 hosted={xs[i] for i in s['hosted']['Dports']};scale={x:Q(1) if x in hosted else Q(1,2) for x in xs}
 D=[[scale[x]*Q(dot(A[x],root(z)),8) for z in example] for x in xs]
 need(all(sum(D[i][k]*E[k][j] for k in range(8))==scale[x]*Q(dot(A[x],A[y]),8) for i,x in enumerate(xs) for j,y in enumerate(xs)),'all104-by104 exact rational dual-encoder identities including coupled halves')
 # Exact basis count is corroboration; the theorem quantifies any invertible basis.
 basis_hist=Counter();orthogonal=0;basis_count=0
 for I in itertools.combinations(omitted,8):
  if rational_rank_by_modular_witness([root(z) for z in I])[0]==8:
   basis_count+=1;basis_hist[binary_rank(I)]+=1;orthogonal+=all(dot(root(x),root(y))==0 for x,y in itertools.combinations(I,2))
 need(basis_count==8766,'complete independent omitted-root basis census')
 # Meaningful false-scope controls.
 z=omitted[0];prior=omitted[1];u=code_map[z][prior];p=(1<<52)-1;v=p^u
 need(u and v and not(u&v),'rank2 subcode containing allones really disconnects into complements')
 need(binary_rank([z,511,prior])==3,'counterexample rank2 chart lift')
 need(any((w^p)!=p and w not in(0,p) for w in code_map[z].values()),'allones is a required exceptional nonminimal codeword')
 e1=[1]+[0]*7;general_support=[N[x] for x in xs if dot(e1,A[x])]
 need(binary_rank(general_support)==9,'non-root decoder example has no shared nonzero chart')
 # Complete favorable H4 accounting, granting all raw routes direct rank8.
 raw=set(xs)|{x+112 for x in xs}|set(s['hosted']['X2'])|set(s['hosted']['Y2']);need(len(raw)==400,'raw inventory')
 for x in raw:need(len(s['frames'][s['final'][x]])-len(s['frames'][s['initial'][x]])==8 and span(s['frames'][s['initial'][x]])<=span(s['frames'][s['final'][x]]),'direct rank8 optimistic source route')
 old=Counter(abs(len(s['frames'][e[3]])-len(s['frames'][e[2]])) for e in s['program'] if e[0]=='MOVE' and e[1] in raw)
 T=Counter({int(k):v for k,v in invoice['T4'].items()});P=Counter({int(k):v for k,v in invoice['P4'].items()})
 for r,c in old.items():P[r]-=18*c
 P[8]+=18*400;packet_floor={9:6,8:1,7:1,1:1}
 for r,c in packet_floor.items():P[r]+=18*c
 h0,h1=interval({r:T[r]-P[r] for r in T.keys()|P.keys()});h0/=18;h1/=18;f0,f1=power(5);f0*=10;f1*=10
 need(power(9)[0]>power(7)[1]+1 and f0>h1,'fewer cheap packets cannot improve bound, exact42 fresh return remains unaffordable')
 result={'status':'PASS_MINIMAL_EIGHT_PURE_PACKET_BARRIER_SOURCE_CERTIFICATE','source_sha256':SPIN,'invoice_sha256':IPIN,'distance42_proof_sha256':D42PIN,'source_rows':104,'gram_rank':8,'all_volume_extension':'Exactly8 dimension-V packets, rank8V factorization, each packet and its copies transported as a full field; coordinate mixing inside a packet permitted. No fractional-volume fragments or intermediate mixing of distinct packet payloads.','locality':{'tested_lines':511,'rank7_lines':omitted,'rank8_lines':495,'method':'Exact modular rank with65537 prime exceeding every possible root minor absolute value4096; unique null vectors checked over integers.'},'recipient_binary_code_spectrum':EXPECTED_SPECTRUM,'preceding_pair_cases':len(pair_patterns),'minimum_four_pattern_count':min(min(r['counts']) for r in pair_patterns),'independent_omitted_root_bases':basis_count,'orthogonal_bases':orthogonal,'basis_binary_dimension_histogram':dict(sorted(basis_hist.items())),'nonorthogonal_dual_example':{'roots':example,'determinant':str(det),'inverse':[[str(x) for x in row] for row in Wi],'encoder_support_sizes':[sum(bool(x) for x in row) for row in E],'encoder_max_abs':str(max(abs(x) for row in E for x in row)),'full_factorization_entries':104*104,'coupled_half_factors_retained':True},'at_most_two_packets_cheaper_than':'9^(199/200)','whole_eight_packet_price_lower':'6*9^(199/200)+8^(199/200)+7^(199/200)+1','optimistic_headroom_lower':str(h0),'optimistic_headroom_upper':str(h1),'fresh_unchanged_source_return_floor_lower':str(f0),'fresh_unchanged_source_return_floor_upper':str(f1),'deficit_lower':str(f0-h1),'deficit_upper':str(f1-h0),'negative_controls':{'rank2_allones_exception_chart':[z,511,prior],'complement_disjoint_weights':[u.bit_count(),v.bit_count()],'nonroot_decoder_example':[1,0,0,0,0,0,0,0],'nonroot_decoder_source_normal_rank':9},'classification':'Finite exact source identities plus the general mathematical rank/copy-genealogy proof in PROOF.md. Independent review pending. No new kappa.','scope':'Exactly8 pure full-field packets for the104-row scaled Gram block; global delivery order; unchanged monotone receiver paths and endpoint duties; every informative owned movement paid. Arbitrary intermediate and delivery charts and arbitrary minimal factorization allowed. Interleaving, more than8 packets, changed receiver contracts, funded data and mixed packet payloads remain open.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.output/'LOCALITY.json').write_text(json.dumps(locality,indent=2,sort_keys=True)+'\n');(a.output/'SPECTRA.json').write_text(json.dumps(spectra,indent=2,sort_keys=True)+'\n');(a.output/'PATTERNS.json').write_text(json.dumps(pair_patterns,indent=2,sort_keys=True)+'\n');print(result['status']);print('bases',basis_count,'binary dimensions',dict(sorted(basis_hist.items())),'orthogonal',orthogonal,'gap',float(f0-h1))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--distance42',type=Path);ap.add_argument('--output',type=Path,required=True);main(ap.parse_args())
