"""Exact physical source injection and full native arrowhead rank certificate."""
import hashlib
import numpy as np


def need(condition,message):
    if not condition:
        raise ValueError(message)


def dual_N(i,j,g,f,state,widths):
 P=state['P'];copy=state['copy'];body=state['body'];terms=state['terms'];mm=state['field'].mm
 Pi=P[:widths[i]];Z=np.zeros((len(Pi),480),dtype=np.uint8)
 if (i,j)not in terms:return Z
 y,x,T=terms[i,j];yr=np.arange(64*y,64*(y+1));xr=np.arange(64*x,64*(x+1));yo=np.flatnonzero(copy[yr]==g);xi=np.flatnonzero(copy[xr]==f)
 if len(yo)and len(xi):Z[:,body[xr[xi]]]=mm(Pi[:,body[yr[yo]]],T[np.ix_(yo,xi)])
 return Z

def cross_terms(s,pr,t,mm):
 rows=[];cols=[]
 if t in s['z']:
  ids,m=s['z'][t];rows.append(np.eye(480,dtype=np.uint8)[:,ids]);cols.append(mm(m,s['E']))
 if t in pr:
  h,v=pr[t];rows.append(mm(s['L'],h));cols.append(v)
 if not rows:return None
 return np.hstack(rows),np.vstack(cols)

def verify_donor(j,field,coefficients,state,params,late_cache,minor):
 mm=field.mm;rank=field.rank;JS=state['adj'];Es=state['E'];Bs=state['B'];VS=state['VS'];actual=state['updates'];U=state['U'];tiers=state['tiers'];widths=params['output_dimensions'];P=state['P'];spec=params['donors'][str(j)]
 js=JS[j];ell=Es[j].shape[1];rels=np.load(late_cache/f'L{j}.npy',mmap_mode='r',allow_pickle=False);need(hashlib.sha256(rels).hexdigest()==spec['late_transfer_sha256'],'true native late-to-facet coefficient pin');assert rels.shape==(len(js),480,ell)
 facts=[];qmain=[];qzero=[];other={(0,r):[]for r in range(1,8)};other.update({(r,0):[]for r in range(1,8)});ui=U[:,:tiers[j]];pu=field.pivots(ui.T);ui_inv=field.invert_and_price(ui[pu])[0]
 for i,L in zip(js,rels):
  k=JS[i].index(j);E=Es[i][k];B=Bs[i][k];V,S=VS[i];F=mm(V,B^mm(S,E));z=actual.get(i,{})
  m=F.copy()
  if (0,0)in z:
   ids,Z=z[0,0];m[ids]^=mm(Z,E)
  s={'i':i,'L':L,'E':E,'B':F,'B00':m,'z':z};facts.append(s)
  Pi=P[:widths[i]];main=Pi^mm(Pi,F);qmain.append(main);qzero.append(Pi^mm(Pi,m)^dual_N(i,j,0,0,state,widths))
  for gf,arr in other.items():
   tmp=dual_N(i,j,*gf,state,widths)
   if gf in z:
    ids,Z=z[gf];tmp^=mm(mm(Pi[:,ids],Z),E)
   arr.append(tmp)
 A=np.vstack([mm(P[:widths[Z['i']]],Z['L'])for Z in facts]);pA=field.pivots(A);assert len(pA)==sum(widths[i]for i in js);iv=field.invert_and_price(A[:,pA])[0];lift=np.zeros((ell,len(A)),dtype=np.uint8);lift[pA]=iv
 pr={};crosscost=0
 for gf,uu in other.items():
  Q=np.vstack(uu);a=np.flatnonzero(np.any(Q,axis=1))
  if not len(a):continue
  H=lift[:,a];G=Q[a];assert not np.any(mm(G,ui));pr[gf]=(H,G);R=mm(H,G);assert np.array_equal(mm(A,R),Q);crosscost+=int(field.weights[R].sum())
 def diagonal(Q,items,tag):
  assert not np.any(mm(Q,ui));Lall=np.vstack(rels);Fl=np.vstack(items)
  for trial in [spec[tag]]:
   R=coefficients(f'dual native variable row/{tag}/{j}/{trial}',(ell,480)).copy();R[:,pu]^=mm(mm(R,ui),ui_inv);R[pA]^=mm(iv,Q^mm(A,R));assert np.array_equal(mm(A,R),Q)and not np.any(mm(R,ui));words=(Fl^mm(Lall,R)).reshape(-1,480,480)
   if all(rank(M)==480 for M in words):return R,words,trial
  raise ValueError(('diagonal',j,tag))
 Rmain,Bmain,trial1=diagonal(np.vstack(qmain),[s['B']for s in facts],'rim')
 schurs=[];pairs=0;additional=0
 for s,B1 in zip(facts,Bmain):
  mid=s['B00'].copy();invB=None
  for u in range(1,8):
   if ((0,u)not in s['z']and(0,u)not in pr) or ((u,0)not in s['z']and(u,0)not in pr):continue
   X=cross_terms(s,pr,(0,u),mm);Y=cross_terms(s,pr,(u,0),mm);assert X is not None and Y is not None
   if invB is None:invB=field.invert_and_price(B1)[0];pairs+=1
   Xl,Xr=X;Yl,Yr=Y;middle=mm(Xr,mm(invB,Yl));mid^=mm(Xl,mm(middle,Yr));additional+=1
  schurs.append(mid)
 R0,B0,trial0=diagonal(np.vstack(qzero),schurs,'central')
 native_ids=np.load(late_cache/f'IDs{j}.npy',allow_pickle=False);need(len(native_ids)==ell and hashlib.sha256(native_ids).hexdigest()==spec['late_owner_ids_sha256'],'actual physical source late holder order')
 cost=7*int(field.weights[Rmain].sum())+int(field.weights[R0].sum())+crosscost
 for i,M in zip(js,Bmain):
  if max(i,j)<12:minor[480*i:480*(i+1),480*j:480*(j+1)]=M
 return {'j':j,'rim':trial1,'central':trial0,'ell':ell,'cross_blocks':len(pr),'native_schurs':pairs,'schur_terms':additional,'binary_add':cost},(Rmain,R0,pr)
