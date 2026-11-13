#!/usr/bin/env python3
"""Exact canonical BIT proper shortenings and a literal partial acquisition."""
import argparse,collections,gzip,hashlib,importlib.util,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
DEP='a28c7e8037ae99b6aecf21a62a4f784c906016d5e12f100826062cf3d602c5b1'
def need(c,m):
 if not c:raise ValueError(m)
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def bb(rows):
 b={};chosen=[]
 for i,x in enumerate(rows):
  w=1<<i
  while x:
   p=x.bit_length()-1
   if p not in b:b[p]=(x,w);chosen.append(i);break
   z,v=b[p];x^=z;w^=v
 return b,chosen
def solve(b,x):
 w=0
 while x:
  p=x.bit_length()-1;need(p in b,'Binary representation');z,v=b[p];x^=z;w^=v
 return w
def rr(rows):
 a=[[F(x) for x in r] for r in rows];p=0;cols=[]
 for c in range(8):
  q=next((i for i in range(p,len(a)) if a[i][c]),None)
  if q is None:continue
  a[p],a[q]=a[q],a[p];z=a[p][c];a[p]=[x/z for x in a[p]]
  for i in range(len(a)):
   if i!=p and a[i][c]:z=a[i][c];a[i]=[x-z*y for x,y in zip(a[i],a[p])]
  cols.append(c);p+=1
 return a[:p],cols
def minor(rows,prime=1009):
 b={};chosen=[]
 for i,r in enumerate(rows):
  x=[int(z)%prime for z in r]
  for c in range(8):
   if not x[c]:continue
   if c not in b:z=pow(x[c],-1,prime);b[c]=[v*z%prime for v in x];chosen.append(i);break
   z=x[c];x=[(v-z*w)%prime for v,w in zip(x,b[c])]
 return chosen,sorted(b)
def canon(v):return tuple(-x for x in v) if next(x for x in v if x)<0 else tuple(v)
def main(a):
 dep=a.repo/'research/moonshot-005-program/results/bit-rank-nine-shared-interface/build_bit_nine_rail.py'
 need(hashlib.sha256(dep.read_bytes()).hexdigest()==DEP,'Frozen replay/price dependency')
 spec=importlib.util.spec_from_file_location('retained_bit_rail',dep);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'Native pin')
 s=json.loads(gzip.decompress(raw));frames={int(k):v for k,v in s['frames'].items()}
 roots=[[F(x) for x in frames[c]['B'][0]] for c in s['start'][:111]]
 roots=[tuple(int(x*(2 if dot(r,r)==1 else 1)) for x in r) for r in roots];need(all(dot(r,r)==4 for r in roots),'Norm4 roots')
 K=[sum(int(i==j or dot(roots[i],roots[j])==0)<<j for j in range(111)) for i in range(111)]
 _,chosen=bb(K);need(len(chosen)==9,'Canonical rank9');enc=[K[i] for i in chosen];words=[];proper=[];census=collections.Counter()
 for mask in range(1,512):
  row=0
  for q,z in enumerate(enc):
   if mask>>q&1:row^=z
  support=[i for i in range(111) if row>>i&1];selected,cols=minor([roots[i] for i in support]);rank=len(selected);need(rank in (7,8),'Rank lower certificate')
  rec={'mask':mask,'row':row,'weight':len(support),'real_rank':rank,'minor_source_rows':[support[i] for i in selected],'minor_columns':cols,'prime':1009}
  if rank==7:
   basis,piv=rr([roots[i] for i in support]);need(len(basis)==7,'Exact proper rank');free=next(c for c in range(8) if c not in piv);v=[F(0)]*8;v[free]=1
   for i,c in enumerate(piv):v[c]=-basis[i][free]
   den=math.lcm(*(x.denominator for x in v));v=[int(x*den) for x in v];g=math.gcd(*v);v=canon([x//g for x in v]);need(dot(v,v)==4,'Facet normal norm4')
   need(row==sum(int(dot(r,v)==0)<<i for i,r in enumerate(roots)),'Exact proper facet support');rec['normal']=v;proper.append(rec)
  census[rank,len(support)]+=1;words.append(rec)
 need(len(proper)==9 and len(bb([p['mask'] for p in proper])[0])==9,'Nine proper basis words')
 closure=set(map(canon,roots))
 while True:
  nxt=set(closure)
  for x,y in itertools.product(closure,repeat=2):
   z=dot(x,y);need(z%2==0,'Integral reflection');v=canon(tuple(u-(z//2)*w for u,w in zip(x,y)));need(dot(v,v)==4,'Reflected norm');nxt.add(v)
  need(len(nxt)<=120,'Finite reflection closure')
  if nxt==closure:break
  closure=nxt
 missing=closure-set(map(canon,roots));need(len(closure)==120 and missing=={tuple(p['normal']) for p in proper},'Exactly nine omitted roots')
 overlaps=[]
 for p,q in itertools.combinations(proper,2):
  overlaps.append((p['row']&q['row']).bit_count());union=p['row']|q['row'];need(len(minor([roots[i] for i in range(111) if union>>i&1])[0])==8,'Two proper supports span Hub')
 need((min(overlaps),max(overlaps))==(25,34),'Facet overlap range')
 first=min(proper,key=lambda p:(p['weight'],p['mask']));need(first['weight']==56,'Minimum proper support')
 packets=[first['row']]
 for row in enc:
  if len(bb(packets+[row])[0])>len(packets):packets.append(row)
 need(len(packets)==9,'Packet basis');basis,_=bb(packets);decoder=[solve(basis,row) for row in K]
 normal=list(first['normal']);p=next(i for i,z in enumerate(normal) if z);facet_basis=[]
 for j in range(8):
  if j==p:continue
  v=[F(0)]*8;v[j]=1;v[p]=-F(normal[j],normal[p]);facet_basis.append([x.numerator if x.denominator==1 else str(x) for x in v])
 facet=max(frames)+1;frames[facet]={'dim':7,'A':[normal],'B':facet_basis};hub=s['final'][0];zero=s['start'][111]
 need(all(c==hub for c in s['final'][:111]) and frames[hub]['dim']==8 and frames[zero]['dim']==0,'Endpoint Hub/zero')
 support={i for i in range(111) if first['row']>>i&1};ops=[['MOVE',i,s['start'][i],facet] for i in sorted(support)];packet=222
 def emit(q,c):
  ops.append(['INIT',packet,c])
  for i in range(111):
   if packets[q]>>i&1:ops.append(['ADD',packet,i,c])
  ops.append(['MOVE',packet,c,zero])
  for i in range(111):
   if decoder[i]>>q&1:ops.append(['ADD',111+i,packet,zero])
  ops.append(['CLEAR',packet,zero])
 emit(0,facet)
 for i in range(111):ops.append(['MOVE',i,facet if i in support else s['start'][i],hub])
 for q in range(1,9):emit(q,hub)
 for i in range(111):ops.append(['MOVE',111+i,zero,s['final'][111+i]])
 word={'public':222,'owned_fields':1,'start':s['start'][:222],'final':s['final'][:222],'frames':frames,'program':ops,'interface':'Canonical K partial map; all K+I corrections remain.'}
 rows,bill=old.replay(word,frames);need(rows[:111]==[1<<i for i in range(111)] and all(rows[111+i]==((1<<(111+i))^K[i]) for i in range(111)),'Exact all-input partial endpoint')
 need(bill['paid_profile']=={1:56,6:56,7:167,8:8},'Whole paid profile')
 gain=old.moment({8:1,7:55,6:-56,1:-56});need(gain[0]>0,'Strict price improvement')
 def show(pair):return {'lower':str(pair[0]),'upper':str(pair[1]),'decimal_midpoint':format(float(sum(pair)/2),'.16f')}
 a.output.mkdir(parents=True,exist_ok=True);word_sha=old.write_gzip(a.output/'PARTIAL-WORD.json.gz',word)
 result={'status':'PASS_CANONICAL_BIT_PROPER_SHORTENINGS_AND_LITERAL_PARTIAL_RAIL','native_sha256':PIN,'retained_replay_price_dependency_sha256':DEP,'encoder_source_roles':chosen,
  'all_511_nonzero_words':words,'rank_weight_census':[{'rank':r,'weight':w,'count':n} for (r,w),n in sorted(census.items())],
  'proper_word_masks':[p['mask'] for p in proper],'proper_word_basis_rank':9,'reflection_closure_lines':120,'missing_roots':sorted(missing),'proper_support_overlap_range':[min(overlaps),max(overlaps)],
  'partial_packet_rows':packets,'decoder_masks':decoder,'one_facet_mask':first['mask'],'partial_word_sha256':word_sha,'bill':bill,
  'saving_at_t_199_200':show(gain),'partial_price':show(old.moment(bill['paid_profile'])),
  'scope':'Finite premises and scalar word. Separate proof extends canonical shortenings to every characteristic-two field and V. All6470 foreign coefficients remain; no full physical admission, complete Q, supplier or new kappa.'}
 (a.output/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','proper_word_masks','proper_word_basis_rank','bill','saving_at_t_199_200']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
