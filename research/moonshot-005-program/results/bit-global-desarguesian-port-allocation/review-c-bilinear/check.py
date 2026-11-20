#!/usr/bin/env python3
"""Independent audit: matrix bilinear forms and polynomial-convolution GF64.
No author code is imported. Every finite geometric identity is reconstructed.
"""
import argparse,gzip,hashlib,json
from collections import Counter,defaultdict
from itertools import combinations
from pathlib import Path
FORMS=(138420225,16418,16777284,131088,33587328,135406080,67637248)
PAIRS=list(combinations(range(8),2))
def need(x,s):
 if not x:raise AssertionError(s)
def xor(xs):
 z=0
 for x in xs:z^=x
 return z
def q(x):return((x&(x>>1))&85).bit_count()&1
def b(x,y):return(x&(((y&85)<<1)|((y&170)>>1))).bit_count()&1
def rank(rows):
 E={}
 for r in rows:
  while r:
   p=(r&-r).bit_length()-1
   if p in E:r^=E[p]
   else:E[p]=r;break
 return len(E)
def span(xs):
 V={0}
 for x in xs:V|={x^y for y in tuple(V)}
 return frozenset(V)
def Q(u):return (((u>>1)&1)&((u>>3)&1))^(((u>>2)&1)&((u>>4)&1))^((u&1)&((u>>5)&1))
def multiply(x,y):
 z=xor(1<<(i+j)for i in range(6)if x>>i&1 for j in range(6)if y>>j&1)
 for degree in range(10,5,-1):
  if z>>degree&1:z^=67<<(degree-6)
 return z
def qf(x):
 x2=multiply(x,x);x4=multiply(x2,x2);x8=multiply(x4,x4);x9=multiply(x8,x);x18=multiply(x9,x9);return x9^x18^multiply(x18,x18)
def linear(columns,x):return xor(columns[j]for j in range(len(columns))if x>>j&1)
def roots_from_files(L,B):
 A=[[B['lattice_basis_columns'][j][i]for j in range(8)]for i in range(8)];basis=B['hyperbolic_basis_masks'];inverse={linear(basis,x):x for x in range(256)};need(len(inverse)==256,'native binary coordinates');roots=[]
 for root in L['root_table']:
  c=[0]*8
  for i in range(7,-1,-1):c[i],r=divmod(root[i]-sum(A[i][j]*c[j]for j in range(i+1,8)),A[i][i]);need(r==0,'exact physical root back-substitution')
  roots.append(inverse[sum((x&1)<<j for j,x in enumerate(c))])
 need(len(roots)==len(set(roots))==120 and set(roots)=={x for x in range(256)if q(x)},'all actual nonsingular roots');return roots

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);base=a.repo/'research/moonshot-005-program/results';package=base/'bit-global-desarguesian-port-allocation';here=Path(__file__).resolve().parent
 for path,h in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((a.repo/path).read_bytes()).hexdigest()==h,'input snapshot '+path)
 L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());W=json.loads(gzip.decompress((package/'author/WITNESS.json.gz').read_bytes()));nodes=json.loads((package/'author/output/GLOBAL-NODES.json').read_text());roots=roots_from_files(L,B);H=[set(ids)for ids in L['A2']];D=[set(ids)for ids in L['D4']]
 matrices=[]
 for f in FORMS:
  rows=[0]*8
  for k,(i,j)in enumerate(PAIRS):
   if f>>k&1:rows[i]^=1<<j;rows[j]^=1<<i
  matrices.append(rows)
 need(rank(FORMS)==7,'independent alternating forms');C=[]
 for x in range(256):
  columns=[sum(((row[j]&x).bit_count()%2)<<k for k,row in enumerate(matrices))for j in range(8)];C.append([linear(columns,y)for y in range(256)])
 need(all((C[x][y]&1)==b(x,y)for x in range(256)for y in range(256)),'first coordinate is actual polar form')
 need(all(C[x][x]==0 and C[x][y]==C[y][x]for x in range(256)for y in range(256)),'alternating symmetric convention')
 contraction=Counter();singular_kernels={};common_identity=0
 for x in range(1,256):
  r=rank(C[x][1<<j]for j in range(8));contraction[q(x),r]+=1;kernel=frozenset(y for y in range(256)if not C[x][y]);need(r==(7 if q(x)else 4),'all contraction ranks')
  if q(x):
   need(kernel=={0,x},'exact nonsingular line kernel')
   for y in range(256):
    if b(x,y):need(q(y)==Q(C[x][y]>>1),'common quadratic identity');common_identity+=1
  else:need(len(kernel)==16 and all(not q(y)for y in kernel),'singular kernel is maximal singular');singular_kernels[x]=kernel
 need(common_identity==15360 and len(set(singular_kernels.values()))==135,'complete quadratic and kernel census')
 all_zero_lines={frozenset((0,x,y,x^y))for x,y in combinations(range(1,256),2)if not C[x][y]};need(len(all_zero_lines)==315 and all(all(not q(x)for x in R)for R in all_zero_lines),'exact315 common-zero planes without singularity prefilter')
 radicals=[]
 for ids in D:
  V=span(roots[j]for j in ids);rad=frozenset(x for x in V if all(not b(x,y)for y in V));need(len(rad)==4,'literal D radical');radicals.append(rad)
 selected=set(W['selected_D']);need({radicals[d]for d in selected}==all_zero_lines and {d for d,R in enumerate(radicals)if R in all_zero_lines}==selected,'exact630 marked D labels')
 wedges=[]
 for R in all_zero_lines:
  x,y=sorted(R-{0})[:2];z=sum(((((x>>i)&1)&((y>>j)&1))^(((x>>j)&1)&((y>>i)&1)))<<k for k,(i,j)in enumerate(PAIRS));wedges.append(z);need(all(not(z&f).bit_count()%2 for f in FORMS),'all marked Pluecker equations')
 need(rank(wedges)==21,'complete seven-dimensional annihilator')
 kernel_line_hist=Counter(sum(R<=K for R in all_zero_lines)for K in singular_kernels.values());need(kernel_line_hist=={7:135},'135 distinguished four-spaces each contain7 marked lines')
 form_rank_hist=Counter(rank(xor(matrices[j][i]for j in range(7)if m>>j&1)for i in range(8))for m in range(1,128));need(form_rank_hist=={8:64,4:63},'all127 nonzero forms')
 reference=next(x for x in range(1,256)if q(x));truth={}
 for y in range(256):
  c=C[reference][y]
  if c&1:need(c not in truth or truth[c]==q(y),'well-defined affine function');truth[c]=q(y)
 need(set(truth)==set(range(1,128,2))and sum(truth.values())==28,'complete affine truth table')
 anf=[truth[1|(u<<1)]for u in range(64)]
 for bit in range(6):
  for u in range(64):
   if u>>bit&1:anf[u]^=anf[u^(1<<bit)]
 need([u for u,z in enumerate(anf)if z]==[10,20,33],'ANF u1u3+u2u4+u0u5')
 chosen={c for c,z in truth.items()if z};labels=[]
 for ids in H:
  xs=[roots[j]for j in ids];values={C[x][y]for x in xs for y in xs if x!=y};need(len(values)==1,'basis-independent H label');label=values.pop();need(label in chosen,'one of28 labels');labels.append(label)
 need(Counter(labels)==Counter({c:40 for c in chosen}),'28 classes of40 H')
 stars=[[h for h,ids in enumerate(H)if j in ids]for j in range(120)];need(all(len(s)==28 and {labels[h]for h in s}==chosen for s in stars),'120 bijective donor stars');need(nodes['H_labels']==labels,'emitted H labels')
 fieldq=[qf(x)for x in range(64)];need(set(fieldq)=={0,1}and fieldq.count(0)==28,'GF64 minus quadratic form');need(all(multiply(x,y)<64 for x in range(64)for y in range(64)),'field multiplication range')
 theta={int(k):v for k,v in nodes['theta'].items()};need(set(theta)==set(theta.values())==set(range(64)),'bijective field-node map');need(all(theta[x^y]==theta[x]^theta[y]for x in range(64)for y in range(64)),'theta is linear')
 c0=nodes['coset_base'];need(c0==min(chosen)==21,'common affine origin');q6=lambda t:1^Q((c0>>1)^t)
 need(all(q6(t)==fieldq[theta[t]]for t in range(64)),'one global quadratic isometry');need(len(nodes['source_Witt_basis'])==len(nodes['field_Witt_basis'])==6 and span(nodes['source_Witt_basis'])==span(nodes['field_Witt_basis'])==set(range(64))and[theta[t]for t in nodes['source_Witt_basis']]==nodes['field_Witt_basis'],'literal Witt-basis mapping')
 Hnodes=[theta[(c^c0)>>1]for c in labels];need(Hnodes==nodes['H_nodes']and set(Hnodes)=={t for t in range(64)if not fieldq[t]},'shared28 GF64 zero nodes')
 fieldb=[[fieldq[x^y]^fieldq[x]^fieldq[y]for y in range(64)]for x in range(64)];adj=[{i for i,y in enumerate(roots)if i!=j and not b(x,y)}for j,x in enumerate(roots)];parameters={};views=native=0
 for j,x in enumerate(roots):
  parameters[j]={i:theta[C[x][roots[i]]>>1]for i in adj[j]};need(set(parameters[j].values())==set(range(1,64))and len(parameters[j])==63,'each donor bijects onto all63 nonzero receiver parameters')
  need(parameters[j]=={int(i):v for i,v in nodes['receiver_parameters'][str(j)].items()},'emitted receiver parameters')
  for i,v in parameters[j].items():
   actual={h for h in stars[j]if H[h]<=adj[i]};expected={h for h in stars[j]if fieldb[v][Hnodes[h]]==1^fieldq[v]};need(actual==expected and len(actual)==16,'actual source view is common-field16 block');views+=1;native+=i<111 and j<111
 need(views==7560 and native==6470,'complete source view census')
 triples=0;Jcounts=defaultdict(set);Jclass_by_H=[]
 for h,ids in enumerate(H):
  aa,bb,cc=sorted(ids);ar,br=roots[aa],roots[bb];hp=frozenset(x for x in range(256)if all(not b(x,roots[j])for j in ids));left={C[ar][x]>>1:x for x in hp};need(set(left)==set(range(64)),'H-perpendicular contraction isomorphism')
  derived={x:left[C[br][x]>>1]for x in hp};s=W['local_structures'][h];back=[linear(s['coordinate_basis'],t)for t in range(64)];coord={x:t for t,x in enumerate(back)};cols=[(s['J']>>(6*p))&63 for p in range(6)];fixed={x:back[linear(cols,coord[x])]for x in hp};need(derived==fixed or derived=={x:fixed[fixed[x]]for x in hp},'bilinear local field operator is certified J or conjugate')
  need(all(b(x,fixed[x])==q(x)for x in hp),'Hermitian norm identity')
  orth=set(hp);unitary=[]
  for stage in range(3):
   e=min(x for x in orth if q(x));unitary.extend([e,fixed[e]]);orth={x for x in orth if not b(e,x)and not b(e,fixed[x])};need(len(orth)==4**(2-stage),'Hermitian orthogonal complement dimensions')
  need(span(unitary)==hp and all(q(linear(unitary,t)) == (sum(bool(t & (3 << (2*k))) for k in range(3)) % 2) for t in range(64)), 'literal three-dimensional unitary norm form')
  target=tuple(C[br][left[1<<p]]>>1 for p in range(6));square=tuple(linear(target,t)for t in target);canonical=min(target,square);Jcounts[labels[h]].add(canonical);Jclass_by_H.append(canonical)
  for j,k in ((j,k)for j in ids for k in ids if j!=k):
   invj={C[roots[j]][x]>>1:x for x in hp};T=tuple(C[roots[k]][invj[1<<p]]>>1 for p in range(6));T2=tuple(linear(T,t)for t in T);need(min(T,T2)==canonical,'unordered field-generator pair independent of H basis')
  for i,y in enumerate(roots):
   if y in hp:
    vals=[parameters[j][i]for j in ids];need(all(vals)and len(set(vals))==3 and xor(vals)==0,'distinct nonzero receiver triple with zero sum');triples+=1
 need(triples==40320 and Counter(len(s)for s in Jcounts.values())=={40:28},'all receiver triples and40 distinct structures per label')
 # Adversarial controls separate coordinate convention, linearity and equations.
 need(any((C[x][y]>>1)!=b(x,y)for x in range(256)for y in range(256)),'wrong polar coordinate rejected')
 wrong_theta=dict(theta);wrong_theta[1]^=1;need(any(wrong_theta[x^y]!=wrong_theta[x]^wrong_theta[y]for x in range(64)for y in range(64)),'node-map mutation rejected')
 rotated=list(FORMS);rotated[1]^=1;need(any((wedge&rotated[1]).bit_count()%2 for wedge in wedges),'alternating-form mutation rejected')
 result={'status':'PASS_INDEPENDENT_GLOBAL_BILINEAR_MARKING_AND_SHARED_NODES','no_author_code_imported':True,'forms':list(FORMS),'selected_common_zero_planes':315,'selected_D':630,'marked_Pluecker_rank':21,'alternating_form_span_dimension':7,'nonzero_form_rank_histogram':dict(form_rank_hist),'contraction_rank_histogram':[[qx,r,n]for(qx,r),n in sorted(contraction.items())],'distinct_singular_kernel_four_spaces':135,'singular_kernel_marked_line_histogram':dict(kernel_line_hist),'common_quadratic_identities':common_identity,'affine_quadratic_ANF_masks':[10,20,33],'shared_labels':sorted(chosen),'H_per_label':40,'source_stars':120,'common_GF64_nodes':sorted(set(Hnodes)),'source_receiver_parameter_bijections':120,'geometric_source_views':views,'native_source_views':native,'receiver_parameter_triples':triples,'bilinear_local_field_structures':1120,'ordered_H_basis_checks':6720,'explicit_local_unitary_bases_checked':1120,'distinct_target_J_per_label_histogram':dict(Counter(len(s)for s in Jcounts.values())),'negative_controls':['wrong polar-coordinate extraction','single theta-table mutation','single alternating-form coefficient mutation'],'common_H_word_certified':False,'source_word_certified':False,'complete_kappa_claimed':False}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.out/'GLOBAL-INDEPENDENT.json').write_text(json.dumps({'H_labels':labels,'H_nodes':Hnodes,'J_classes_by_H':Jclass_by_H,'theta':theta},separators=(',',':'))+'\n');print(result['status'],315,28,7560,6470,40320,flush=True)

if __name__=='__main__':main()
