"""Exact sparse-edge and extension certificate for global BIT rigidity; no SAT."""
import argparse,gzip,hashlib,itertools,json
from pathlib import Path
if not __debug__:raise SystemExit('Exact checks require Python without -O')
SP='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
FRAME=[0,16,17,32,36,38,67,71]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def basis(rows):
 b={};chosen=[]
 for n,v in enumerate(rows):
  while v:
   j=v.bit_length()-1
   if j not in b:b[j]=v;chosen.append(n);break
   v^=b[j]
 return b,chosen
def main(a):
 from fractions import Fraction as F
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==SP
 s=json.loads(gzip.decompress(raw));charts={int(k):v for k,v in s['frames'].items()};r=[[F(x) for x in charts[s['start'][i]]['B'][0]] for i in range(111)]
 v=[]
 for rr in r:
  n=dot(rr,rr);assert n in (1,4);vv=[x*(2 if n==1 else 1) for x in rr];assert all(x.denominator==1 for x in vv);v.append(list(map(int,vv)))
 assert all(dot(x,x)==4 for x in v)
 K=[]
 for i in range(111):
  row=0
  for j in range(111):
   z=dot(v[i],v[j]);assert z%2==0;row|=(1^(z//2%2))<<j
  K.append(row)
 def bit(i,j):return K[i]>>j&1
 assert all(bit(i,j)==int(i==j) for i in FRAME for j in FRAME)
 at={i:j for j,i in enumerate(FRAME)};bb=[sum(bit(i,j)<<k for k,j in enumerate(FRAME)) for i in range(111)]
 p=next(i for i in range(111) if i not in at and bb[i].bit_count()%2==0)
 x=[bb[i]|((bit(i,p)^((bb[i]&bb[p]).bit_count()%2))<<8) for i in range(111)]
 assert p==1 and all(((x[i]&x[j]).bit_count()%2)==bit(i,j) for i in range(111) for j in range(111))
 edges=[i for i in range(111) if x[i]>>8&1 and (x[i]&255).bit_count()==2]
 ep={i:tuple(a for a in range(8) if x[i]>>a&1) for i in edges}
 assert len(edges)==27 and set(ep.values())==set(itertools.combinations(range(8),2))-{(0,4)}
 degree={a:sum(a in ep[i] for i in edges) for a in range(8)};assert min(degree.values())==6
 assert all(bit(i,j)==int(not(set(ep[i])&set(ep[j]))) for i in edges for j in edges if i!=j)
 four=[]
 for W in itertools.combinations(range(8),4):
  es=[z for z in ep.values() if set(z)<=set(W)];assert len(es)>=5
  assert any(len(set(g)&set(h))==1 for g,h in itertools.combinations(es,2));four.append((W,len(es)))
 seed=sorted(set(FRAME+edges));assert len(seed)==35
 anchors=[]
 for i in range(111):
  if i in seed:continue
  available=[j for j in seed if not bit(i,j)];bs,sel=basis([x[j] for j in available]);assert len(bs)==8
  hh=[available[j] for j in sel];assert len(hh)==8 and all(not((x[i]&x[j]).bit_count()%2) for j in hh)
  piv=sorted(bs);minor=[sum((x[j]>>q&1)<<k for k,q in enumerate(piv)) for j in hh]
  assert len(basis(minor)[0])==8 and x[i].bit_count()%2==1
  anchors.append({'role':i,'eight_noncontact_seed_roles':hh,'nonzero_binary_minor_columns':piv,'canonical_factor':x[i]})
 assert len(anchors)==76
 assert len(basis([x[j] for j in anchors[0]['eight_noncontact_seed_roles'][:-1]])[0])==7
 assert len(basis(K)[0])==9 and len(basis([K[i]^(1<<i) for i in range(111)])[0])==108
 reached={0}
 while True:
  nxt=reached|{j for i in reached for j in range(111) if i!=j and bit(i,j)}
  if nxt==reached:break
  reached=nxt
 assert len(reached)==111
 out={'status':'PASS_EXACT_SPARSE_EDGE_SEED_AND_GLOBAL_EXTENSION_PREMISES','source_sha256':SP,'identity_frame_roles':FRAME,'canonical_factor_rows_9bit':x,'canonical_rank':9,'canonical_foreign_residual_rank':108,'canonical_extra_pivot_role':p,'sparse_edge_roles':[{'role':i,'endpoints':ep[i]} for i in edges],'edge_graph':'K8 minus edge(0,4)','edge_degrees':degree,'every_four_vertices_induce_at_least_five_edges':True,'four_vertex_subsets_checked':len(four),'seed_roles':seed,'remaining_role_count':76,'canonical_contact_graph_connected':True,'extension_anchors':anchors,'negative_controls':{'deleting_one_anchor_reduces_rank_to7':True},'scope':'Finite source premises. Global scalar/division-ring rigidity and all-V invertible-Schur/commuting-factor strata require PROOF.md. Arbitrary noncommuting singular-Schur block stratum remains open.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'CERTIFICATE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','edge_graph','edge_degrees','four_vertex_subsets_checked','remaining_role_count']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
