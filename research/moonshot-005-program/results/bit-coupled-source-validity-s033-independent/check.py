"""Independent S033 source and propagation replay, from pinned JSON only.
@CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json
import numpy as np

def run(repo,out):
 b=repo/'research/moonshot-005-program/results';four=b/'bit-simultaneous-d1509-s032/output';author=b/'bit-coupled-source-validity-s033';helper=b/'bit-global-gauge-lift-s033/verify.py'
 s=importlib.util.spec_from_file_location('root_gf',helper);g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
 read,mm,rank,inv,need=g.read,g.mm,g.rank,g.inverse,g.need
 files=[four/'SOURCES.json.gz',four/'EARLY.json.gz',b/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',b/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz',b/'bit-source-d-tangent-s032/CERTIFICATE.json.gz',author/'CANDIDATE.json.gz',author/'output/CONTROLS.json']
 old,early,layout,fibres,t1data,cand,controls=[read(p)for p in files]
 roots=layout['root_table'];planes=list(map(set,layout['A2']));adj=[{j for j,y in enumerate(roots)if i!=j and sum(a*c for a,c in zip(x,y))==0}for i,x in enumerate(roots)]
 need(all(len(v)==63 for v in adj),'source geometry degrees')
 prot=g.PROTECTED;pr=[0,1,2,15,16,17];comp=[x for x in range(480)if x not in prot];cr=[x for x in range(30)if x not in pr]
 oldsrc={int(j):{int(h):np.array(F,dtype=np.uint8)for h,F in row.items()}for j,row in old['paired_maps'].items()};src={j:{h:F.copy()for h,F in row.items()}for j,row in oldsrc.items()}
 changed=[]
 for key,v in cand['source_protected_delta'].items():
  j,h=map(int,key.split('/'));D=np.array(v,dtype=np.uint8);src[j][h][np.ix_(pr,prot)]^=D
  if np.any(D):changed.append((j,h))
 donors=sorted({j for j,h in changed});need(donors==[0,32,35]and len(changed)==12,'modified quotient census')
 views={};inverses={};records=[];early_records=[]
 for j in sorted(src):
  views[j]={};inverses[j]={}
  for h,F in src[j].items():
   need(not np.any(F[np.ix_(pr,comp)])and not np.any(F[np.ix_(cr,prot)]),'protected block separation')
   need(np.array_equal(F[np.ix_(cr,comp)],oldsrc[j][h][np.ix_(cr,comp)]),'unchanged complement')
  for r in sorted(adj[j]):
   hs=[h for h in sorted(src[j])if planes[h]<=adj[r]];need(len(hs)==16,'sixteen visible planes')
   A=np.vstack([src[j][h][np.ix_(pr,prot)]for h in hs]);need(rank(A)==96,'protected source rank')
   views[j][r]=hs;records.append([j,r,96])
   if j in donors:inverses[j][r]=inv(A)
  if j in donors:
   E=np.array(early[str(j)]['physical_matrix'],dtype=np.uint8);counts={}
   for h,owner in early[str(j)]['row_owners']:
    q=counts.get(h,0);counts[h]=q+1;Q=np.array(old['frames'][f'{j}/{h}'],dtype=np.uint8);E[owner]=mm(Q[q:q+1],src[j][h])[0]
   need(rank(E)==480,'true early physical basis');early_records.append([j,480])
  print('SOURCE',j,len(views[j]),flush=True)
 propagation={}
 for j in donors:
  hist={};rr=[]
  for h in sorted(src[j]):
   for k in sorted(src[j]):
    if h==k:continue
    blocks=[]
    for r,hs in views[j].items():
     if h in hs and k in hs:
      pos=hs.index(h);blocks.append(inverses[j][r][:,6*pos:6*pos+6])
    need(bool(blocks),'nonempty propagation');rk=rank(np.hstack(blocks));hist[rk]=hist.get(rk,0)+1;rr.append([h,k,rk])
  bound=360 if j==0 else 120;need(len(rr)==756 and max(hist)+bound<450,'complete strict propagation')
  propagation[j]={'histogram':hist,'protected_maximum':max(hist),'inherited_complement_bound':bound,'full_bound':max(hist)+bound,'records':rr}
  print('PROPAGATION',j,hist,flush=True)
 H=[]
 for hs,rr in fibres.items():
  h=int(hs)
  for rs,z in rr.items():
   r=int(rs);K=np.array(z['kernel'],dtype=np.uint8);zero=np.zeros_like(K);KK=np.block([[K,zero],[zero,K]])
   for j in src:
    if j not in planes[h]:continue
    for q,F in src[j].items():
     if q==h or planes[q]<=adj[r]:need(not np.any(mm(F^oldsrc[j][q],KK)),'full H observation unchanged')
   H.append([h,r])
 collisions=[]
 for z in controls['t1_full_rank_failures']:
  j,r=z['donor'],z['receiver'];hs=[h for h in sorted(oldsrc[j])if planes[h]<=adj[r]];need(hs==z['source_planes'],'collision plane binding');Fs=[]
  for h in hs:
   F=oldsrc[j][h].copy();delta=t1data['candidate']['source_protected_delta'].get(f'{j}/{h}')
   if delta is not None:F[np.ix_(pr,prot)]^=np.array(delta,dtype=np.uint8)
   Fs.append(F)
  A=np.vstack(Fs);v=np.zeros((480,1),dtype=np.uint8);v[prot,0]=z['protected_collision']
  need(np.any(v)and not np.any(mm(A,v)),'explicit full480 t1 collision');need(rank(np.vstack([F[np.ix_(pr,prot)]for F in Fs]))==95,'rank95 exact')
  w=v.copy();w[0,0]^=1;need(np.any(mm(A,w)),'corrupted collision rejected');collisions.append([j,r,479])
 out.mkdir(parents=True,exist_ok=True)
 result={'status':'PASS_INDEPENDENT_T26_SOURCES_PROPAGATION_H','geometric_source_views':len(records),'native_source_views':sum(r<111 for j,r,k in records),'changed_early_bases':early_records,'unchanged_early_bases_reused':8,'propagation':propagation,'whole_H_observations':len(H),'native_H_observations':sum(r<111 for h,r in H),'full_t1_collisions':collisions,'collision_mutations_rejected':len(collisions),'whole_D_author_replay_and_proof_review_only':True,'compiler_independently_replayed':False,'new_complete_kappa':False}
 g.write_json(out/'RESULT.json',result);g.write_json(out/'SOURCE-PINS.json',{str(p.relative_to(repo)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files+[helper]});print(result['status'],flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);q=p.parse_args();run(q.repo.resolve(),q.out.resolve())
