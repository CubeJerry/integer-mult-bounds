"""Bounded search for a D word agreeing on the forced vector at all donors."""
from pathlib import Path
import importlib.util,gzip,json,hashlib,numpy as np
repo=Path.cwd();base=repo/'research/moonshot-005-program/results';four=base/'bit-simultaneous-d1509-s032';here=Path(__file__).parent
s=importlib.util.spec_from_file_location('s032_solve',four/'solve_gauges.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);g,a,*_=m.common_data(repo)
data=m.ex.read(here/'DATA.json.gz');res=json.loads((here/'RESULT.json').read_text());dw=m.ex.read(four/'output/D-WORD.json.gz');w=json.loads((base/'bit-fifth-receiver-quotient-s032/WITNESS.json').read_text());T=np.array(dw['matrix'],dtype=np.uint8);P={int(j):np.array(A,dtype=np.uint8)for j,A in data['ingress'].items()};v=np.array(w['vector'],dtype=np.uint8);Z=np.hstack([a.mm(P[j]^P[61],v[:,None])for j in sorted(P)if j!=61]);owners=dw['owners'];rows=[13,16,18,31,32,33];null={n:m.null(Z[:n].T,g,a).T for n in [19,35]};print('CONTRAST_RANKS',a.rank(Z[:19]),a.rank(Z),flush=True)
section=[]
for j in sorted(a.charts[1509]):
 inn=[q for q,x in enumerate(owners)if x[3]is not None and j in a.planes[x[3]]]
 for i in range(120):
  if not a.charts[1509]<=a.adj[i]:continue
  oo=[q for q,x in enumerate(owners)if x[5]is not None and i in a.planes[x[5]]];section.append((j,i,oo,inn))
trials=[];best=None
for seed in range(96):
 S=T.copy()
 for q in rows:
  n=19 if q<19 else 35;N=null[n];alpha=np.frombuffer(hashlib.shake_256(f'S032-all-donor-D-vector/{seed}/{q}'.encode()).digest(len(N)),dtype=np.uint8)&63;S[q]=0;S[q,:n]=a.mm(alpha[None,:],N)[0]
 if a.rank(S[:19,:19])<19 or a.rank(S[19:,19:])<16:trials.append({'seed':seed,'failure':'phase'});continue
 bad=[]
 for j,i,oo,inn in section:
  if a.rank(S[np.ix_(oo,inn)])<8:bad.append([j,i])
 if bad:
  trials.append({'seed':seed,'failure':'section','count':len(bad),'first':bad[0]})
  if seed<5:print('TRY',seed,'BAD',len(bad),bad[0],flush=True)
  continue
 for r in res['retained_receivers']:
  oo=res['outputs'][str(r)]
  for j,A in P.items():need=a.mm(S[oo],a.mm(A,np.array(data['common_frames'],dtype=np.uint8)[:,8*res['retained_receivers'].index(r):8*res['retained_receivers'].index(r)+8]));assert np.array_equal(need,np.eye(8,dtype=np.uint8))
 oo=res['outputs']['95'];ys={j:a.mm(S[oo],a.mm(A,v[:,None]))[:,0]for j,A in P.items()};assert all(np.array_equal(y,ys[61])for y in ys.values());best={'seed':seed,'matrix':S.tolist(),'inverse':g.inverse(S,a).tolist(),'delta_rank':a.rank(S^T),'all_donor_readout':ys[61].tolist(),'section_checks':len(section)};print('SUCCESS',seed,'DELTA_RANK',best['delta_rank'],'READOUT',best['all_donor_readout'],flush=True);break
result={'status':'CONSTRUCTED_ALL_DONOR_FORCED_VECTOR_D_WORD'if best else'NO_WITNESS_IN_BOUNDED_SEARCH','contrast_rank_early':a.rank(Z[:19]),'contrast_rank_full':a.rank(Z),'null_dimensions':{n:len(N)for n,N in null.items()},'trials':trials,'witness':best,'complete_receiver95_fibre':False,'new_complete_kappa':False};(here/'ALL-DONOR-VECTOR.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
