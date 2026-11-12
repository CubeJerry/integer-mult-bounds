import json,gzip,math
from pathlib import Path
H=Path(__file__).resolve().parent;P=H.parent
w=json.loads(gzip.decompress(Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds/research/shared-wire-split-composition/data/final.json.gz').read_bytes()));a=json.loads((P/'dual-facet-cuts/ADAPTIVE-SCREEN.json').read_text());cl=json.loads((P/'dual-facet-cuts/FRAMES.json').read_text())['eight_or_larger_cliques'];support=a['last_weight_support'];basis=a['source_chart_frames'];ports=w['ports'];DEN=10**9

def span(b):
 s={0}
 for v in b:s.update(x^v for x in tuple(s))
 return frozenset(s)
def canonical(rows):
 b=[0]*9
 for z in rows:
  for p in range(9):
   if not z>>p&1:continue
   if b[p]:z^=b[p]
   else:
    for q in range(p+1,9):
     if z>>q&1 and b[q]:z^=b[q]
    for q in range(p):
     if b[q]>>p&1:b[q]^=z
    b[p]=z;break
 return b
cells={};offset={};total=0
for d in range(10):
 for pm in range(512):
  if pm.bit_count()!=d:continue
  c=[(p,q) for p in range(9) if pm>>p&1 for q in range(p+1,9) if not pm>>q&1];cells[pm]=c;offset[pm]=total;total+=1<<len(c)
def sid(rows):
 b=canonical(rows);pm=sum(1<<p for p in range(9) if b[p]);ix=sum(((b[p]>>q)&1)<<j for j,(p,q) in enumerate(cells[pm]));return offset[pm]+ix
F=list(map(span,basis));pred=[[] for _ in F]
for j,v in enumerate(F):
 pred[j]=[i for i,u in enumerate(F) if len(u)<len(v) and u<v]
coeff=[];layer=[];gen=[];metadata=[];expected=[0]*len(F);obj=0
for t,s in enumerate(support):
 z=math.floor(s['weight']*DEN);assert z>0;coeff.append(z);cut=s['cut'];S=[ports[i] for i in cl[cut['frame']]];d=8 if cut['layer'] else 16-cut['owned_inward'];obj+=z*d;met={'coefficient':z,'deficit':d,'frame':cl[cut['frame']],'layer':cut['layer']}
 if cut['layer']:
  k=cut['layer'];pm=sum(1<<i for i in cl[cut['frame']]);layer.append((t,k,pm&((1<<64)-1),pm>>64))
  for p in S:gen.append((sid([p]),t))
  inside=[any(p in f for p in S) or (len(basis[j])>=k and all(any((p&v).bit_count()%2 for v in f) for p in S)) for j,f in enumerate(F)]
  sf=span(S);assert len(sf)==16 and set(S)=={v for v in sf if v.bit_count()%2}
 else:
  ins=set(cut['inside_charts']);mi=[j for j in ins if not any(i in ins for i in pred[j])];met['minimal_generator_frames']=[basis[j] for j in mi]
  for j in mi:gen.append((sid(basis[j]),t))
  inside=[any(F[g]<=f for g in mi) for f in F];assert {j for j,v in enumerate(inside) if v}==ins
 for j,v in enumerate(inside):
  if v:expected[j]|=1<<t
 metadata.append(met)
blocks=(len(coeff)+63)//64
with (H/'INPUT.txt').open('w') as f:
 print(len(coeff),blocks,obj,file=f);print(*coeff,file=f);print(len(layer),file=f)
 for row in layer:print(*row,file=f)
 print(len(gen),file=f)
 for row in gen:print(*row,file=f)
 print(len(F),file=f)
 for b,mask in zip(basis,expected):print(sid(b),*[mask>>(64*j)&((1<<64)-1) for j in range(blocks)],file=f)
 print(len(ports),*ports,file=f)
(H/'INPUT.json').write_text(json.dumps({'denominator':DEN,'coefficient_objective':obj,'support':metadata,'subspace_count':total,'blocks':blocks,'source_optimistic_objective':a['history'][-1]['objective'],'generator_flags':len(gen)},indent=2)+'\n')
print({'cuts':len(coeff),'blocks':blocks,'generators':len(gen),'subspaces':total,'objective':obj/DEN})
