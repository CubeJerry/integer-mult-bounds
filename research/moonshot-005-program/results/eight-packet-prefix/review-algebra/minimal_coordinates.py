#!/usr/bin/env python3
"""Independent source check of coordinate-side-information minimality.
Imports only this reviewer's own exact elimination, not the construction code.
"""
import json
from pathlib import Path
from check import eliminate,odd,need,Q
p=Path(__file__).resolve().parent;c=json.loads((p/'CERTIFICATE.json').read_text());A=c['rows'];V=c['ports'];roles=c['roles'];ranks=[]
for i,v in enumerate(V):
    unknown=[j for j,z in enumerate(V) if j!=i and odd(v&z)];rank,_,_=eliminate([A[j] for j in unknown]);need(rank==7,'odd-neighbor span dimension7');ranks.append(rank)
i=0;j=next(j for j in range(104) if j!=i and not odd(V[i]&V[j]));labels=[k for k in range(104) if k!=i and odd(V[i]&V[k])]+[j,i];rank,_,relations=eliminate([A[k] for k in labels]);rel=relations[-1];need(rank==8 and rel.get(len(labels)-1)==1,'target ambiguity');z={labels[k]:v for k,v in rel.items()};need(all(sum(v*A[k][d] for k,v in z.items())==0 for d in range(8)),'packets fixed')
out={'status':'PASS_IDEAL_COORDINATE_SIDE_INFORMATION_MINIMALITY','source_sha256':c['source_sha256'],'receivers_checked':104,'all_odd_neighbor_ranks':sorted(set(ranks)),'removed_even_coordinate_example':{'receiver_role':roles[i]+112,'removed_donor_role':roles[j],'kernel':[[roles[k],str(v)] for k,v in sorted(z.items())]},'interpretation':'With only individual even coordinates granted and no odd coordinates, every one of the48 even coordinates is necessary for this fixed8packet code. One suitable aggregate can replace them; this is not a48packet lower bound.','new_complete_kappa':None}
(p/'MINIMAL-COORDINATES.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
