import gzip,json,time,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path('/workspace/scratch/6a77123a1d61/integer-mult-bounds');HERE=Path(__file__).resolve().parent
w=json.loads(gzip.decompress((ROOT/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()));V=list(w['hosted']['Dports']);P=[w['ports'][i] for i in V];adj=[sum(1<<j for j,b in enumerate(P) if j!=i and (a&b).bit_count()%2) for i,a in enumerate(P)];cliques=[];counts=Counter()
def bk(R,A,B):
 if not A and not B:
  c=[V[i] for i in range(len(V)) if R>>i&1];counts[len(c)]+=1
  if len(c)>=8:cliques.append(c)
  return
 U=A|B
 if U:
  u=max((i for i in range(len(V)) if U>>i&1),key=lambda i:(A&adj[i]).bit_count());C=A&~adj[u]
 else:C=A
 while C:
  bit=C&-C;i=bit.bit_length()-1;C^=bit;bk(R|bit,A&adj[i],B&adj[i]);A^=bit;B|=bit
start=time.time();bk(0,(1<<len(V))-1,0)
out={'source_sha256':hashlib.sha256((ROOT/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()).hexdigest(),'maximal_clique_sizes':dict(sorted(counts.items())),'eight_or_larger_cliques':cliques}
(HERE/'FRAMES.json').write_text(json.dumps(out,indent=2)+'\n');print('enumerated',counts,'size8plus',len(cliques),'seconds',time.time()-start,flush=True)
