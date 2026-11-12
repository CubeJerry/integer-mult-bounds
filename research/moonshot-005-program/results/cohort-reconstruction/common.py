"""Fresh S008 source-coupling utilities; frozen source files are never changed."""
from collections import Counter, defaultdict
from fractions import Fraction as F
import gzip, hashlib, json
from pathlib import Path

SPIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PPIN='1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153'
PPAY='05b503f0c2f219f328353b984ca821db9d6c3cc0225ff3380c551708d247e8d8'
IPIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
SELECT={'one':[77],'two':[56,77],'three':[56,77,100],'eight':[5,56,65,69,77,96,100,103]}

def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def space(frame):
 S={0}
 for v in frame:S|={w^v for w in tuple(S)}
 return frozenset(S)
def basis(S):
 B=[];T={0}
 for v in sorted(S):
  if v not in T:B.append(v);T|={w^v for w in tuple(T)}
 need(T==set(S),'full binary span');return B
def root(v):
 bits=[i for i in range(9) if v>>i&1]
 if len(bits)==3:return [2*int(i in bits) for i in range(8)] if 8 in bits else [1 if i in bits else -1 for i in range(8)]
 need(len(bits)==7,'source root weight');i,j=[i for i in range(9) if i not in bits]
 return [1 if k==i else -1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def rank(A):
 if not A:return 0
 B=[list(map(F,r)) for r in A];k=0
 for j in range(len(B[0])):
  p=next((i for i in range(k,len(B)) if B[i][j]),None)
  if p is None:continue
  B[k],B[p]=B[p],B[k];q=B[k][j];B[k]=[v/q for v in B[k]]
  for i in range(len(B)):
   if i!=k and B[i][j]:q=B[i][j];B[i]=[a-q*b for a,b in zip(B[i],B[k])]
  k+=1
  if k==len(B):break
 return k
def inverse(A):
 n=len(A);B=[[F(x) for x in row]+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
 for j in range(n):
  p=next((i for i in range(j,n) if B[i][j]),None);need(p is not None,'invertible selected minor');B[j],B[p]=B[p],B[j];q=B[j][j];B[j]=[x/q for x in B[j]]
  for i in range(n):
   if i!=j:q=B[i][j];B[i]=[a-q*b for a,b in zip(B[i],B[j])]
 return [r[n:] for r in B]
def mul(A,B):return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]
def add(a,b,c=F(1)):
 a=a.copy()
 for j,v in b.items():
  q=a.get(j,F(0))+c*v
  if q:a[j]=q
  else:a.pop(j,None)
 return a
def ser(row):return [[i,str(c)] for i,c in sorted(row.items())]
def load_inputs(repo):
 d=repo/'research/moonshot-005-program/results';sb=(repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();pb=(d/'eight-packet-seven-corrections-fused/WORD.json.gz').read_bytes();ib=(d/'eight-packet-seven-corrections-fused/INPUT-INVOICE.json').read_bytes()
 need(sha(sb)==SPIN and sha(pb)==PPIN and sha(gzip.decompress(pb))==PPAY and sha(ib)==IPIN,'immutable source/parent/invoice pins')
 return json.loads(gzip.decompress(sb)),json.loads(gzip.decompress(pb)),json.loads(ib)
def source_data(s,p,selection):
 raw={int(x):r for x,r in p['private_role_map'].items()};xs=s['live'];roots={x:root(s['frames'][s['initial'][x]][0]) for x in xs};G={(x,d):sum(a*b for a,b in zip(roots[x],roots[d])) for x in xs for d in xs}
 need(all(xs.index(x) in s['hosted']['Dports'] for x in selection),'ordinary selected first pairs')
 ys=[x+112 for x in selection];weights={x+112:{d:-F(G[x,d],8) for d in xs if d!=x and G[x,d]} for x in selection};need(all(len(r)==48 for r in weights.values()),'48 foreign terms per receiver');facets={y:s['final'][y] for y in ys};spaces=list(map(space,s['frames']));donors=set().union(*(set(r) for r in weights.values()));classes=defaultdict(list)
 for d in sorted(donors):
  g=tuple(y for y in ys if d in weights[y]);need(g==tuple(y for y in ys if spaces[s['initial'][d]]<=spaces[facets[y]]),'coefficient support equals actual incidence');classes[g].append(d)
 return raw,weights,facets,dict(classes),spaces
def charts_for(facets,classes,spaces):
 decl=[];sites={}
 for g in sorted(classes):
  S=frozenset.intersection(*(spaces[facets[y]] for y in g))
  if S in spaces:c=spaces.index(S)
  else:c=len(spaces);spaces.append(S);decl.append({'index':c,'frame':basis(S),'source_facets':[facets[y] for y in g],'construction':'exact intersection of final facets'})
  sites[g]=c
 return sites,decl
class Emitter:
 def __init__(self):self.ops=[];self.lineage=[];self.mapping={}
 def emit(self,o,parent=None):
  i=len(self.ops);self.ops.append(o);self.lineage.append(parent);return i
def base_structure(s,p,raw):
 rawxs={raw[x] for x in s['live']};rev={r:x for x,r in raw.items()};events={i:rev[o[1]] for i,o in enumerate(p['program']) if o[0]=='MOVE' and o[1] in rawxs};need(list(events)==list(range(410,514)),'pure104 donor hoist block')
 for i,d in events.items():need(p['program'][i]==['MOVE',raw[d],s['initial'][d],127,False],'source direct donor route')
 return events,{d:i for i,d in events.items()}
def finish(s,p,name,E,weights,decl,owned,restored,completed,key,meta):
 from copy import deepcopy
 need(len(E.mapping)==len(p['program']),'every parent event accounted')
 changed={'program','marks','owned_fields','native_event_to_physical','corrections','schema','parent_event_of_output','parent_word_sha256','private_route_blocks'};w={k:deepcopy(v) for k,v in p.items() if k not in changed};marks={k:E.mapping[i] for k,i in p['marks'].items()};marks['all_active_donors_restored']=restored
 for y,e in completed.items():marks['receiver_corrected_'+str(y)]=e
 corrections=deepcopy(p['corrections'])
 for y,row in weights.items():corrections[str(y)]=ser(row)
 w.update(schema='moonshot-S008-fresh-source-coupling-'+name+'-v1',program=E.ops,marks=marks,owned_fields=owned,native_event_to_physical=[E.mapping[e] for e in p['native_event_to_physical']],corrections=corrections,parent_event_of_output=E.lineage,parent_word_sha256=PPIN,parent_fused_route_provenance=deepcopy(p['private_route_blocks']),additional_charts=decl,newly_completed_firstY_receivers=sorted(weights),reconstruction_provenance='Fresh S008 generator from source and S007 recovered recipes; no original generator byte identity claimed.');w[key]=meta;return w
