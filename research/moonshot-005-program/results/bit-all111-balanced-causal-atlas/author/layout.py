#!/usr/bin/env python3
"""Construct the entire 45-port middle diagram and an integral public-route assignment."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import maximum_flow
from atlas import source,bits,mask

NATIVE='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'

def need(x,msg):
 if not x:raise ValueError(msg)

def construct(native):
 need(sha256(native.read_bytes()).hexdigest()==NATIVE,'native pin');R,O,A,D,dual,inc=source(native);aid={a:n for n,a in enumerate(A)};did={d:n for n,d in enumerate(D)}
 # Each incidence H<D is a single full record port. Distribute the three parent labels
 # 15 times each, placing absent parent roots where spare public endpoints can carry them.
 left=[[] for d in D];missing_at=Counter()
 for a in sorted(A,key=lambda a:(sum(j<111 for j in bits(a)),aid[a])):
  jset=list(bits(a));miss=[j for j in jset if j>=111];present=[j for j in jset if j<111]
  ds=sorted((did[d] for d in inc[a]),key=lambda n:(missing_at[n],n))
  need(len(ds)==45,'45 D4s above each A2')
  for slot,n in enumerate(ds):
   j=(miss+present)[slot//15];left[n].append((aid[a],j))
   if j>=111:missing_at[n]+=1
 # Exact flow selects 240 independent X origin banks per native j, and either 8 or 9
 # of sixteen inputs at every D. The dual construction gives the same bounds at output.
 caps=Counter((j,d) for d,flags in enumerate(left) for a,j in flags if j<111)
 nD=len(D);sink=112+nD;nn=sink+1;edges=[]
 for j in range(111):edges.append((0,1+j,240))
 for (j,d),v in sorted(caps.items()):edges.append((1+j,112+d,v))
 extra=111*240-8*nD
 # Grant extra demand where most native flags occur.
 nine=set(sorted(range(nD),key=lambda d:(missing_at[d],d))[:extra]);
 for d in range(nD):edges.append((112+d,sink,8+int(d in nine)))
 ii,jj,vv=zip(*edges);G=coo_matrix((vv,(ii,jj)),shape=(nn,nn)).tocsr();flow=maximum_flow(G,0,sink)
 need(flow.flow_value==111*240,'complete source-to-middle b matching')
 used=Counter({(j,d):int(flow.flow[1+j,112+d]) for j,d in caps});assigned=[]
 for d,flags in enumerate(left):
  out=[]
  for h,j in sorted(flags):
   isx=bool(j<111 and used[j,d]);out.append([h,j,isx]);used[j,d]-=int(isx)
  assigned.append(out)
 need(not any(used.values()),'all source labels realized')
 # Left blank slots end on Y and right blank slots begin on X. Right flags are obtained
 # by dualizing the same allocation at D-perp. Each native receiver gets 240 real Ys.
 routes=[]
 for d,ls in enumerate(assigned):
  rs=assigned[did[dual[D[d]]]];LX=[v for v in ls if v[2]];LY=[v for v in ls if not v[2]];RX=[v for v in rs if not v[2]];RY=[v for v in rs if v[2]]
  need(len(LX)>=len(RX) and len(RY)>=len(LY),'local two-colour flow')
  for (h,j,_),(k,i,_) in zip(LY,RY):routes.append(['Y',d,h,j,k,i])
  for (h,j,_),(k,i,_) in zip(LX,RX):routes.append(['X',d,h,j,k,i])
  for (h,j,_),(k,i,_) in zip(LX[len(RX):],RY[len(LY):]):
   routes.append(['X',d,h,j,None,None]);routes.append(['Y',d,None,None,k,i])
 # Root code block indices. Assign 240 systematic X slots for each native j across
 # 15 RS stripes (16 of 28 distinct evaluation nodes per stripe). The complementary
 # 180 Y slots receive the other 12 evaluations. The balanced cyclic assignment
 # ensures each H's 15 occurrences receive different stripe indices.
 lookup=defaultdict(lambda:defaultdict(list));dest=defaultdict(lambda:defaultdict(list))
 for n,(kind,d,h,j,k,i) in enumerate(routes):
  if j is not None and j<111:lookup[j][h].append(n)
  if i is not None and i<111:dest[i][k].append(n)
 def label(index,wanted):
  out={}
  for j,byH in index.items():
   need(len(byH)==28,'all 28 A2 pencil nodes');position=0
   for alpha,(h,slots) in enumerate(sorted(byH.items())):
    yes=sorted(n for n in slots if routes[n][0]==wanted);no=sorted(set(slots)-set(yes));need(len(slots)==15,'all 15 stripes')
    stripes=[(position+k)%15 for k in range(len(yes))];other=sorted(set(range(15))-set(stripes));position+=len(yes)
    for n,z in zip(yes+no,stripes+other):out[n]=(alpha,z)
   need(position==240,'240 systematic slots')
   for s in range(15):need(sum(routes[n][0]==wanted and out[n][1]==s for h in byH for n in byH[h])==16,'16 systematic coordinates every stripe')
  return out
 src=label(lookup,'X');dst=label(dest,'Y')
 payload={'schema':'all111-a2-d4-e6-fractional-ports-v1','native_sha256':NATIVE,'root_table':R,'A2':[list(bits(a)) for a in A],
      'D4':[list(bits(d)) for d in D],'dual_D4':[did[dual[d]] for d in D],
      'routes':[[*r,list(src[n]) if n in src else None,list(dst[n]) if n in dst else None] for n,r in enumerate(routes)]}
 return payload

def verify(w):
 A=list(map(mask,w['A2']));D=list(map(mask,w['D4']));R=w['root_table'];P=w['dual_D4'];N=(1<<111)-1;orth=[mask(j for j,r in enumerate(R) if sum(a*b for a,b in zip(s,r))==0) for s in R]
 # Reconstruct the signed-root geometry. Matrix coordinate checks are intrinsic to masks.
 for d,dd in enumerate(D):
  pp=__import__('functools').reduce(int.__and__,[orth[j] for j in bits(dd)]);need(pp==D[P[d]] and P[P[d]]==d,'exact D4 complement')
 L=Counter();T=Counter();X=Counter();Y=Counter();LH=Counter();RK=Counter();sg=Counter();tg=Counter();pitch=Counter();profile=Counter();first=defaultdict(set);last=defaultdict(set);tally=Counter()
 for kind,d,h,j,k,i,sc,dc in w['routes']:
  ranks=[1] if kind=='X' else [0];
  if kind=='X':need(j is not None and j<111,'real X source');X[j]+=1
  else:need(i is not None and i<111,'real Y endpoint');Y[i]+=1
  if h is not None:
   need((A[h]>>j)&1 and A[h]&D[d]==A[h],'nested first A2');L[h,d]+=1;LH[h,j]+=1
   if kind=='Y' and j<111:ranks.append(1)
   ranks.append(2);first[h].add(d)
  ranks.append(4)
  if k is not None:
   need((A[k]>>i)&1 and A[k]&D[P[d]]==A[k],'nested last E6');T[d,k]+=1;RK[k,i]+=1;ranks.append(6);last[k].add(P[d])
   if i<111:ranks.append(7)
  if kind=='X':ranks.append(8)
  for x,y in zip(ranks,ranks[1:]):need(y>x,'monotone rank');profile[y-x]+=1
  if sc:
   a,s=sc;sg[j,a,s]+=1
   if kind=='X':pitch['x',j,s]+=1
  if dc:
   a,s=dc;tg[i,a,s]+=1
   if kind=='Y':pitch['y',i,s]+=1
  tally[(kind,'none' if j is None else 'native' if j<111 else 'padding','none' if i is None else 'native' if i<111 else 'padding')]+=1
 need(set(X.values())=={240} and set(Y.values())=={240} and len(X)==len(Y)==111,'native multiplicity')
 need(len(L)==len(T)==1120*45 and set(L.values())==set(T.values())=={1},'every port exactly once')
 need(len(LH)==len(RK)==3360 and set(LH.values())==set(RK.values())=={15},'all slots uniform including zero origins')
 need(len(sg)==len(tg)==111*28*15 and set(sg.values())==set(tg.values())=={1} and set(pitch.values())=={16},'MDS emission stripes and endpoint dual stripes')
 pairs=Counter();targetcounts=Counter()
 for h,hm in enumerate(A):
  I=__import__('functools').reduce(int.__and__,[orth[j] for j in bits(hm)]);need(len(first[h])==len(last[h])==45,'full fractional middle cover');
  for i in bits(I):
   c=sum((D[P[d]]>>i)&1 for d in first[h]);e=sum((D[P[d]]>>i)&1 for d in last[h]);need(c==e==15,'uniform 15-of-45 middle restriction')
  if hm&N:targetcounts[(I&N).bit_count()]+=1
 for j in range(111):
  pen=[n for n,a in enumerate(A) if a>>j&1];need(len(pen)==28,'native pencil')
  for i in bits(orth[j]&N):
   q=sum((A[h]&orth[i])==A[h] for h in pen);need(q==16,'exact 16-of-28 incidence');pairs[q]+=1
 profile[8]+=9*240
 return {'status':'PASS_GLOBAL_111_COUPLED_PORTS','parent_A2':len(A),'parent_D4':len(D),'foreign_pairs':sum(pairs.values()),
         'actual_public_field_record_routes':len(w['routes']),'GF_symbol_paid_native_copies':240,'GF64_binary_paid_native_copies':1440,
         'directed_A2_D4_ports_per_side':len(L),'per_native_pencil':28,'per_pencil_foreign_compatible':16,'per_A2_D4_neighbours':45,'per_A2_foreign_compatible_D4':15,
         'route_kind_source_end_census':[[*k,v] for k,v in sorted(tally.items())],
         'scalar_GF_profile_with_canonical_descents':dict(sorted(profile.items())),
         'normalized_profile':{k:str(Fraction(v,240)) for k,v in sorted(profile.items())},
         'global_decoder_constructed':False}

if __name__=='__main__':
 ap=ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);w=construct(a.native);r=verify(w)
 data=json.dumps(w,separators=(',',':')).encode()+b'\n';import gzip
 (a.out/'LAYOUT.json.gz').write_bytes(gzip.compress(data,mtime=0));r['layout_uncompressed_sha256']=sha256(data).hexdigest();(a.out/'LAYOUT-RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['normalized_profile'],r['layout_uncompressed_sha256'])
