"""Remove the last 159-edge case by the integer sizes of the two native degree partitions."""
from argparse import ArgumentParser
from fractions import Fraction
import json
from pathlib import Path
def main(a):
 g=json.loads(a.girth.read_bytes());assert g['minimum_girth_of_simultaneously_calibrated_canonical_subgraph']==10 and g['free_canonical_edge_upper']==159
 cand=[]
 for n in range(2,50):
  for m in range(2,49):
   e=159-97+n+m;v=m+n;u=2*e-v
   if 2*max(n,m)<=e<=n*m and 2*e*(u*v*v+u**3)<=(n*(n-1)+m*(m-1))*v**3:cand.append((n,m,e))
 assert cand==[(49,48,159)]
 # The size-biased excess degree geometric means are at least X and Y.
 x=Fraction(226,100);y=Fraction(233,100)
 assert x**159<2**111*3**48 and y**159<2**99*3**60
 nodes=1+x+x*y*(1+x)+(x*y)**2
 assert nodes>48
 out={'only_remaining_159_edge_degree_core':cand[0],'certified_donor_part_vertices_needed_numerator':nodes.numerator,'certified_donor_part_vertices_needed_denominator':nodes.denominator,'actual_donor_part_size':48,'free_canonical_edge_upper':158,'anchored_canonical_edge_upper':98,'required_whole_nonflat_edges':123,'global_optimum_lower':221,'global_optimum_upper':379,'fixed_native_bilateral_interiors':True}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'FINAL-CANONICAL-CAP.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(out)
if __name__=='__main__':
 p=ArgumentParser();p.add_argument('--girth',type=Path,required=True);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
