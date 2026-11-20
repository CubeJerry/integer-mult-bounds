#!/usr/bin/env python3
"""Independent certificate replay; complete the two missing local H lines."""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def need(ok,why):
 if not ok:raise ValueError(why)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))if p.suffix=='.gz'else json.loads(p.read_text())
ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();here=Path(__file__).resolve().parent;base=args.repo/'research/moonshot-005-program/results';author=here.parent/'author'
for p,h in read(here/'SOURCE-PINS.json')['files'].items():need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest()==h,'pin '+p)
spec=importlib.util.spec_from_file_location('retained_exact_geometry',base/'bit-coupled-native-geometric-cycle-source/review-c/check.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
lit=read(author/'SOURCE-COEFFICIENTS.json.gz');cert=read(author/'output/CROSS-CERTIFICATES.json.gz');L=read(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');roots=g.roots_from_files(L,read(base/'bit-clifford-one-evaluation-gate/author/BASIS.json'))
H=[set(x)for x in L['A2']];D=[set(x)for x in L['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not g.b(x,y)}for j,x in enumerate(roots)];marked=set(read(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')['selected_D'])
Q={int(j):{int(h):np.array(F,dtype=np.uint8)for h,F in row.items()}for j,row in lit['maps'].items()};donors=sorted(Q);need(donors==[0,45,61,62,100],'one exact five-source tuple');stars={j:[h for h,P in enumerate(H)if j in P]for j in donors};view={};cuts=[]
for j in donors:
 need(set(Q[j])==set(stars[j])and all(F.shape==(12,192)for F in Q[j].values()),'complete literal source')
 for i in sorted(adj[j]):
  hs=[h for h in stars[j]if H[h]<=adj[i]];view[j,i]=hs;need(len(hs)==16 and g.rank(np.vstack([Q[j][h]for h in hs]))==192,'full actual source cut');cuts.append((j,i))
 print('ROOT_RECIPROCAL_SOURCE',j,63,flush=True)
ports={h:[d for d,S in enumerate(D)if H[h]<=S and d not in marked]for h in [263,642]};P={h:np.array(lit['H'][str(h)]['word'],dtype=np.uint8)for h in ports};fibres={};reads=0;native=0
for h in ports:
 need(ports[h]==lit['H'][str(h)]['ports']and len(ports[h])==36 and g.rank(P[h])==36,'full current physical provider')
 js=sorted(H[h])
 for i in range(120):
  if not H[h]<=adj[i]:continue
  K=g.null(np.vstack([Q[js[0]][a]for a in view[js[0],i]if a!=h]));need(K.shape==(192,12),'whole off-H fibre')
  rr=[p for p,d in enumerate(ports[h])if D[d]<=adj[i]];R=[]
  for t,j in enumerate(js):
   need(not np.any(g.mm(np.vstack([Q[j][a]for a in view[j,i]if a!=h]),K)),'common full fibre')
   R.append(g.mm(P[h][np.ix_(rr,range(12*t,12*t+12))],g.mm(Q[j][h],K)))
  need(len(rr)==12 and g.rank(R[0])==12 and all(np.array_equal(R[0],r)for r in R[1:]),'whole common physical readout')
  fibres[h,i]=(K,R[0],[ports[h][p]for p in rr]);reads+=1;native+=i<111
quota=Counter()
for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
 phase,j,x,h,d,k,source,target=json.loads(line)
 if phase=='X'and j in donors:need(j==source,'actual X owner');quota[j,h]+=1

def determinant(A):
 A=A.copy();n=len(A);out=1
 for j in range(n):
  choices=np.flatnonzero(A[j:,j]);need(len(choices)>0,'early basis pivot');k=j+int(choices[0]);A[[j,k]]=A[[k,j]];out=int(g.M[out,A[j,j]]);A[j,j:]=g.M[g.INV[A[j,j]],A[j,j:]]
  if j+1<n:A[j+1:,j:]^=g.M[A[j+1:,j,None],A[j,None,j:]]
 return out
early=[]
for j in donors:
 rows=[];chart=263 if j in [0,61,62]else 642
 for h in stars[j]:
  F=Q[j][h];count=quota[j,h]//15;need(count in [1,2],'ordinary early quota')
  if count==2:rows.extend([np.hstack([F,np.zeros_like(F)]),np.hstack([np.zeros_like(F),F])])
  elif h in ports:rows.append(np.hstack([F,np.zeros_like(F)]))
  else:
   A=np.frombuffer(hashlib.shake_256(f'early/{chart}/12/{j}/{h}/{lit["early_seeds"][str(j)]}'.encode()).digest(288),dtype=np.uint8).reshape(12,24)&63
   rows.append(np.hstack([g.mm(A[:,:12],F),g.mm(A[:,12:],F)]))
 M=np.vstack(rows);need(M.shape==(384,384),'actual two-copy early basis');early.append(determinant(M))
need(early==[1,36,48,33,4],'independently computed early determinants')
inv={};completions=[];hist=Counter();partial_checks=0
for rec in cert['four_spaces']:
 d,i=rec['D'],rec['receiver'];need(D[d]<=adj[i]and d in set(ports[263])&set(ports[642]),'actual common D cut');U=np.array(rec['space'],dtype=np.uint8);need(U.shape==(192,4)and g.rank(U)==4,'literal four-space')
 V=[]
 for h in ports:
  K,R,ps=fibres[h,i];v=g.mm(K,g.invert(R)[:,ps.index(d):ps.index(d)+1]);V.append(v)
  need(np.array_equal(v[:,0],cert['directions'][f'{d}/{i}'][str(h)]),'normalized actual H-isolated direction')
 need(g.rank(np.hstack(V))==2 and g.rank(np.hstack([U]+V))==4,'both isolated directions inside four-space')
 lines={int(h):np.array(v,dtype=np.uint8)[:,None]for h,v in rec['H_lines'].items()};need(len(lines)==14,'known fourteen lines')
 for j in donors:
  hs=view[j,i]
  if(j,i)not in inv:inv[j,i]=g.invert(np.vstack([Q[j][h]for h in hs]))
  sum_proj=np.zeros_like(U);inside=[]
  for t,h in enumerate(hs):
   image=g.mm(Q[j][h],U)
   if not H[h]<=D[d]:need(not np.any(image),'every outside-D source quotient vanishes');continue
   need(g.rank(image)==1,'rank-one in-D quotient');proj=g.mm(inv[j,i][:,12*t:12*t+12],image);sum_proj^=proj;inside.append(h)
   need(h in lines and g.rank(np.hstack([lines[h],proj]))==1 and g.rank(np.hstack([U,proj]))==4,'actual coordinate projection gives the shared H line')
  need(len(inside)==4 and np.array_equal(sum_proj,U)and g.rank(np.hstack([lines[h]for h in inside]))==4,'four actual projections resolve the identity')
 for h in ports:
  wrong=[p for p,e in enumerate(ports[h])if e!=d and D[e]<=adj[i]]
  for t,j in enumerate(sorted(H[h])):need(not np.any(g.mm(P[h][np.ix_(wrong,range(12*t,12*t+12))],g.mm(Q[j][h],U))),'all known wrong-D H values vanish on the whole four-space')
 Hs=[h for h,S in enumerate(H)if S<=D[d]];need(len(Hs)==16,'sixteen actual H parents')
 def partial_ok(line_dict):
  for j in D[d]:
   js=[h for h in Hs if j in H[h]and h in line_dict]
   if js and g.rank(np.hstack([line_dict[h]for h in js]))!=len(js):return False
  return True
 need(partial_ok(lines),'all twelve current partial stars independent');partial_checks+=len(D[d]);chosen=[]
 # New root continuation: two missing lines can be chosen on a degree-three curve.
 for h in sorted(set(Hs)-set(lines)):
  for t in range(64):
   v=g.mm(U,np.array([[1],[t],[g.power(t,2)],[g.power(t,3)]],dtype=np.uint8));candidate={**lines,h:v}
   if partial_ok(candidate):lines=candidate;chosen.append({'H':h,'curve_parameter':t});break
  else:raise ValueError('finite curve line completion failed')
 need(len(lines)==16 and partial_ok(lines),'all twelve complete four-line stars')
 completions.append({'D':d,'receiver':i,'chosen_missing_lines':chosen,'completed_H_lines':{str(h):v[:,0].tolist()for h,v in lines.items()}});hist[rec['envelope_dimension']]+=1
 print('ROOT_RECIPROCAL_FOUR_SPACE',d,i,flush=True)
need(len(completions)==48 and sum(r['receiver']<111 for r in completions)==46,'all geometric/native D cuts')
whole=[]
for h,j,k in [(116,0,45),(643,62,100)]:
 for i in range(120):
  if not H[h]<=adj[i]:continue
  kernels=[g.null(np.vstack([Q[t][a]for a in view[t,i]if a!=h]))for t in [j,k]];r=g.rank(np.hstack(kernels));need(r>12,'whole unbuilt H fibres remain incompatible');whole.append(r)
result={'status':'PASS_ROOT_RECIPROCAL_PORT_LOCAL_SPACES','source_geometric_cuts':len(cuts),'source_native_cuts':sum(i<111 for j,i in cuts),'whole_H_readouts':reads,'native_H_readouts':native,'actual_early_determinants':early,'common_four_spaces':48,'native_common_four_spaces':46,'geometric_partial_star_checks':partial_checks,'known_H_lines_per_cut':14,'completed_abstract_H_lines_per_cut':16,'completed_geometric_donor_stars':12,'author_envelope_dimension_histogram_not_recomputed':dict(hist),'unbuilt_whole_H_fibre_join_ranks':sorted(set(whole)),'new_author_executable_imported':False,'retained_arithmetic_dependency_reused':True,'physical_D_word_constructed':False,'other_source_systems_constructed':False,'global_H_completion':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');payload=json.dumps(completions,separators=(',',':')).encode();(args.out/'LINE-COMPLETIONS.json.gz').write_bytes(gzip.compress(payload,mtime=0));print(result['status'],315,291,72,67,48,46,16,flush=True)
