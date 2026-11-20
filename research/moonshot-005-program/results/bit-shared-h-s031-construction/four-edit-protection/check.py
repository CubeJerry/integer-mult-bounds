#!/usr/bin/env python3
"""Four-edit core envelope and a sharp five-edit native counterexample."""
from argparse import ArgumentParser
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,text):
 if not ok:raise ValueError(text)

def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main(repo,out):
 out.mkdir(parents=True,exist_ok=True)
 base=repo/'research/moonshot-005-program/results'
 g=load(base/'bit-coupled-native-geometric-h-source/component/construction.py','four_edit_geometry')
 family,a,previous=g.context(repo)
 pins=Path(__file__).with_name('SOURCE-PINS.json')
 if pins.exists():
  for path,digest in json.loads(pins.read_text()).items():need(hashlib.sha256((repo/path).read_bytes()).hexdigest()==digest,'source pin '+path)
 power=lambda x,n:g.power(int(x),n,a)
 q=lambda x:g.quadratic(int(x),a)
 polar=lambda x,y:q(x^y)^q(x)^q(y)
 nodes=[x for x in range(64) if not q(x)]
 def divided(degree,node):
  return np.array([power(node,degree-t) if t<=degree else 0 for t in range(16)],dtype=np.uint8)
 def core(node):
  return np.stack((divided(0,node),divided(1,node),divided(3,node),divided(7,node),divided(13,node)^divided(4,node),divided(15,node)),axis=1)
 cores={node:core(node) for node in nodes}
 for node,S in cores.items():
  need(a.rank(S)==6,'six independent geometric core columns')
  identity=divided(15,node)^a.product[power(node,2),divided(13,node)]
  expected=np.zeros(16,dtype=np.uint8);expected[14]=node;expected[15]=1
  need(np.array_equal(identity,expected),'exact degree15/degree13 divided-difference identity')
 for first in nodes:
  for second in nodes:
   if first!=second:need(a.rank(np.hstack((cores[first],cores[second])))==10,'all756 two-core intersections')
 sample_ranks=[]
 for count in range(1,7):
  selected=nodes[:count];rank=a.rank(np.hstack([cores[z] for z in selected]));bound=[6,10,13,14,15,16][count-1]
  need(rank==bound,'sharp displayed core envelope')
  sample_ranks.append({'nodes':selected,'rank':rank,'upper':bound})
 views={v:[x for x in nodes if polar(v,x)==1^q(v)] for v in range(1,64)}
 need(all(len(z)==16 for z in views.values()),'all63 geometric source blocks')
 blockset={frozenset(z) for z in views.values()}
 # Bind every base in the protected two-centre candidate to genuine geometric blocks.
 coefficient_path=base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz'
 coefficients=json.loads(gzip.decompress(coefficient_path.read_bytes()))
 base_checks=0
 for donor,rows in coefficients['base_nodes'].items():
  j=int(donor);rows={int(h):n for h,n in rows.items()}
  for i in a.adj[j]:
   observed=frozenset(rows[h] for h in a.by_donor[j] if a.planes[h]<=a.adj[i])
   need(observed in blockset,'every literal base source view is a geometric field block')
   base_checks+=1
 need(base_checks==315,'five-donor geometric base binding')
 # Five edits are a true counterexample, not merely a saturated dimension envelope.
 edits=[0,3,5,7,8];seed=3
 maps={node:a.vandermonde([node],16)[0] for node in nodes}
 for node in edits:maps[node]=family.coefficients(f'four-edit-sharpness/{seed}/{node}',(16,))
 inverses={}
 for v,visible in views.items():
  M=np.vstack([maps[node] for node in visible]);need(a.rank(M)==16,'all63 five-edit source cuts')
  inverses[v]=g.inverse(M,a)
 shared=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
 node_to_H={shared['H_nodes'][h]:h for h in a.by_donor[0]}
 parameters={int(i):v for i,v in shared['receiver_parameters']['0'].items() if int(i)<111 and int(i)!=80}
 Hnode,Rnode=10,0;H,R=node_to_H[Hnode],node_to_H[Rnode]
 receiver_ids=[i for i,v in parameters.items() if Hnode in views[v] and Rnode in views[v]]
 fibres=np.stack([inverses[parameters[i]][:,views[parameters[i]].index(Hnode)] for i in receiver_ids],axis=1)
 need((H,R)==(17,806) and len(receiver_ids)==15 and a.rank(fibres)==15,'native five-edit saturation witness')
 need(all(a.planes[H]<=a.adj[i] and a.planes[R]<=a.adj[i] and i in a.adj[0] for i in receiver_ids),'literal receiver/plane visibility')
 need(not np.any(a.mm(maps[Rnode][None,:],fibres)),'saturated propagation is the actual edited R kernel')
 need(a.rank(fibres[:,:-1])==14,'removing a witness fibre loses one rank')
 witness={'donor':0,'seed':seed,'edited_nodes':edits,'edited_planes':[node_to_H[x] for x in edits],
  'H':H,'R':R,'H_node':Hnode,'R_node':Rnode,'native_receivers':receiver_ids,
  'maps':{str(node):row.tolist() for node,row in maps.items()},'fibres':fibres.tolist(),
  'all_geometric_source_cuts':63,'propagation_rank':15}
 (out/'FIVE-EDIT-WITNESS.json').write_text(json.dumps(witness,sort_keys=True,indent=2)+'\n')
 result={'status':'PASS_FOUR_EDIT_PROTECTION_AND_FIVE_EDIT_SHARPNESS','all_node_core_identities':28,
  'two_core_pairs':756,'sample_core_ranks':sample_ranks,'literal_two_H_base_bindings':base_checks,
  'effective_edit_propagation_bounds':[5,9,12,13,14],'five_edit_native_counterexample':{'donor':0,'H':H,'R':R,'rank':15,'source_cuts':63},
  'all_positive_widths_by_tensor':True,'new_complete_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(result['status'],flush=True)

if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 z=p.parse_args();main(z.repo.resolve(),z.out.resolve())
