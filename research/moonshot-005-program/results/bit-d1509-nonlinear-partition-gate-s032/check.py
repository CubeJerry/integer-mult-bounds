#!/usr/bin/env python3
"""Check D1509 rank witnesses and finite all-fibre/zero-fibre partition controls."""
import argparse,hashlib,itertools,json,runpy
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'bit-simultaneous-d1509-s032-independent'
HELP=runpy.run_path(str(PREV/'check_frames.py'))
rd,wr,mm,rank,need=[HELP[k] for k in ['rd','wr','mm','rank','need']]
echelon=HELP['ALG']['echelon']
ROOT=HELP['ROOT']
def canonical(cells):return tuple(sorted(tuple(sorted(c)) for c in cells))
def span(vs):
 s={0}
 for v in vs:s|={x^v for x in list(s)}
 return s
def cosets(n,U):return canonical({frozenset(x^u for u in U) for x in range(1<<n)})
def join(n,parts):
 parent=list(range(1<<n))
 def find(x):
  while parent[x]!=x:parent[x]=parent[parent[x]];x=parent[x]
  return x
 for part in parts:
  for cell in part:
   for x in cell[1:]:parent[find(x)]=find(cell[0])
 groups={}
 for x in range(1<<n):groups.setdefault(find(x),[]).append(x)
 return canonical(groups.values())
def maps_parts(g,P,Q):return all(canonical([g[x] for x in cell] for cell in p)==q for p,q in zip(P,Q))
def check_rank(A,c):
 r=c['rank'];rows=c['minor_rows'];cols=c['minor_columns'];M=A[np.ix_(rows,cols)]
 _,piv,det=echelon(M);N=np.array(c['kernel'],dtype=np.uint8).reshape(A.shape[1],A.shape[1]-r)
 need(len(rows)==len(cols)==len(piv)==r and det==c['minor_determinant']!=0,'nonzero exact lower minor')
 need(not np.any(mm(A,N)) and rank(N)==A.shape[1]-r,'complete upper kernel')
 return r
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=HERE/'output');args=ap.parse_args()
 pins=rd(HERE/'SOURCE-PINS.json')
 for path,digest in pins['files'].items():need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'source binding '+path)
 frames={int(j):{int(r):np.array(a,dtype=np.uint8) for r,a in row.items()} for j,row in rd(PREV/'output/FRAMES.json.gz').items()}
 witnesses=rd(PREV/'candidate-output/FIVE-RECEIVER-WITNESSES.json.gz');native=sorted(r for r in frames[0] if r<111)
 need(len(native)==11 and sorted(tuple(w['receivers']) for w in witnesses)==list(itertools.combinations(native,5)),'complete duplicate-free five-set coverage')
 counts={};rankpairs={}
 for w in witnesses:
  got=[]
  for j,c in zip(w['donor_pair'],w['certificates']):got.append(check_rank(np.hstack([frames[j][r] for r in w['receivers']]),c))
  need(got==w['ranks'] and got[0]!=got[1],'strict join-rank discrepancy')
  key=str(w['donor_pair'][1]);counts[key]=counts.get(key,0)+1;k='/'.join(map(str,got));rankpairs[k]=rankpairs.get(k,0)+1
 U=[span([x]) for x in [1,2,3]];V=[span([x]) for x in [1,2,4]]
 P=[cosets(3,u) for u in U];Q=[cosets(3,v) for v in V]
 g=list(range(8));g[3],g[4]=g[4],g[3]
 need(all({g[x] for x in u}==v for u,v in zip(U,V)) and not maps_parts(g,P,Q),'zero fibres do not imply whole partitions')
 joined1,joined2=join(3,P),join(3,Q)
 need({len(c) for c in joined1}=={4} and {len(c) for c in joined2}=={8},'distinct join-class sizes')
 fixed={0:0,1:1,2:2,3:4};free=[4,5,6,7];available=[3,5,6,7];trials=0
 for perm in itertools.permutations(available):
  p=fixed|dict(zip(free,perm));need(not maps_parts(p,P,Q),'all prescribed zero-fibre alignments rejected');trials+=1
 positive=[x^(1 if (x&4 and x&8) else 0) for x in range(16)]
 parts=[cosets(4,span([x])) for x in [1,2]]
 need(len(set(positive))==16 and all(positive[positive[x]]==x for x in range(16)),'nonlinear positive bijection')
 need(positive[4]^positive[8]!=positive[12] and maps_parts(positive,parts,parts),'nonlinear whole-partition control accepted')
 need({len(c) for c in join(4,parts)}=={4},'positive join size')
 corrupted=dict(witnesses[0]['certificates'][0]);corrupted['minor_determinant']=0
 rejected=False
 try:check_rank(np.hstack([frames[witnesses[0]['donor_pair'][0]][r] for r in witnesses[0]['receivers']]),corrupted)
 except AssertionError:rejected=True
 need(rejected,'bad rank certificate rejected')
 result={'status':'PASS_D1509_NONLINEAR_WHOLE_PARTITION_GATE','native_receivers':native,'five_sets':len(witnesses),'witness_donor_counts':counts,'rank_pairs':rankpairs,'zero_only_control':{'n':3,'permutation':g,'join_cell_sizes':[4,8],'prescribed_zero_alignments_excluded':trials},'nonlinear_positive_control':{'n':4,'permutation':positive,'whole_partitions_preserved':True,'join_cell_size':4},'rank_mutation_rejected':rejected,'theorem_scope':'all whole fibres over finite coefficient extensions and fixed lane repetition; arbitrary bank bijections and quotient labels','zero_only_or_arbitrary_supplier_excluded':False,'new_kappa':False}
 wr(args.out/'RESULT.json',result);print(result,flush=True)
if __name__=='__main__':main()

