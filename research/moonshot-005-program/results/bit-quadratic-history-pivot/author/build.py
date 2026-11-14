#!/usr/bin/env python3
"""Actual one-packet native BIT quadratic-history pivot, all222 original columns."""
import argparse,gzip,hashlib,json,itertools
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(b,m):
 if not b:raise ValueError(m)
def rank(rows):
 p={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in p:x^=p[j]
   else:p[j]=x;break
 return len(p)
def dot(a,b):return sum(F(x)*F(y) for x,y in zip(a,b))
def nullspace(A,n=8):
 a=[list(map(F,r)) for r in A];p=[]
 for c in range(n):
  h=next((h for h in range(len(p),len(a)) if a[h][c]),None)
  if h is None:continue
  k=len(p);a[k],a[h]=a[h],a[k];z=a[k][c];a[k]=[v/z for v in a[k]]
  for h in range(len(a)):
   if h!=k:
    z=a[h][c];a[h]=[u-z*v for u,v in zip(a[h],a[k])]
  p.append(c)
 out=[]
 for j in range(n):
  if j not in p:
   r=[F(0)]*n;r[j]=1
   for k,c in enumerate(p):r[c]=-a[k][j]
   out.append(r)
 return out

def setup(n,i,j):
 R=[list(map(F,n['frames'][str(n['start'][k])]['B'][0])) for k in range(111)]
 need(i!=j and dot(R[i],R[j])!=0,'distinct nonorthogonal pivot pair')
 K=[sum(int(k==l or dot(R[k],R[l])==0)<<l for l in range(111)) for k in range(111)]
 L=K[i]&K[j];need(not (L>>i&1) and not (L>>j&1),'quadratic mode has zero pivot own blocks')
 need(all(dot(R[k],R[i])==dot(R[k],R[j])==0 for k in range(111) if L>>k&1),'actual common proper support')
 frames=json.loads(json.dumps(n['frames']));C=None
 for s,f in frames.items():
  if f['dim']==6 and all(dot(b,R[i])==dot(b,R[j])==0 for b in f['B']):C=int(s);break
 if C is None:
  C=max(map(int,frames))+1;B=nullspace([R[i],R[j]])
  need(len(B)==6,'common chart dimension6')
  frames[str(C)]={'dim':6,'B':[[str(x) for x in row] for row in B],'A':[[str(x) for x in row] for row in (R[i],R[j])]}
 common=[k for k in range(111) if L>>k&1];exclusive=[k for k in range(111) if k!=i and (K[i]>>k&1) and not (L>>k&1)]
 other=[k for k in range(111) if k not in common and k not in exclusive]
 need(rank(K)==9 and rank(K+[1<<i,L])==11,'new coordinate and quadratic directions')
 need(rank(K+[1<<k for k in range(8)]+[L])==rank(K+[1<<k for k in range(8)])+1,'quadratic direction beyond all eight coordinate patches')
 return R,K,L,frames,C,common,exclusive,other

def emit(n,i,j):
 R,K,L,frames,C,common,exclusive,other=setup(n,i,j)
 hub=n['final'][0];ground=n['start'][111];Fi=n['final'][111+i];Q=333;P=334;ops=[]
 for k in range(111):ops.extend([['INIT',222+k,n['start'][k]],['ADD',222+k,k,n['start'][k]]])
 ops.append(['INIT',Q,C])
 for k in common:
  ops.extend([['MOVE',k,n['start'][k],C],['ADD',Q,k,C],['MOVE',k,C,hub]])
 ops.extend([['MOVE',111+i,ground,C],['ADD',111+i,Q,C],['MOVE',111+i,C,Fi]])
 for k in exclusive:
  ops.extend([['MOVE',k,n['start'][k],Fi],['ADD',111+i,k,Fi],['MOVE',k,Fi,hub]])
 for k in other:ops.append(['MOVE',k,n['start'][k],hub])
 ops.append(['INIT',P,hub])
 for k in range(111):
  if K[i]>>k&1:ops.append(['ADD',P,k,hub])
 ops.extend([['MOVE',P,hub,Fi],['ADD',111+i,P,Fi],['ADD',P,111+i,Fi],['MOVE',P,Fi,C],['ADD',P,Q,C],['ADD',Q,P,C],['ADD',P,Q,C],['MOVE',P,C,ground]])
 owned=list(range(222,335));final=n['final'][:111]+[n['final'][111+k] if k==i else ground for k in range(111)]
 word={'schema':'native_nested_linear_partial_word','public':222,'owned_fields':owned,'start':n['start'][:222],'final':final,'frames':frames,'program':ops[:],'end_owned':owned,'scope':'One completed original target;111 point copies, pure quadratic ground mode and dirty proper-chart history retained. Not a complete supplier.'}
 for k in range(111):
  if k!=i:ops.append(['MOVE',111+k,ground,n['final'][111+k]])
 for k in range(111):ops.append(['CLEAR',222+k,n['start'][k]])
 ops.extend([['CLEAR',Q,C],['CLEAR',P,ground]])
 closed={**word,'program':ops,'final':n['final'][:222],'end_owned':[],'scope':'Closed partial source: only selected Y_i gains X_i;110 other Y unchanged. Not complete.'}
 info={'i':i,'j':j,'common_chart':C,'common_inputs':common,'exclusive_inputs':exclusive,'other_inputs':other,'K_hex':hex(K[i]),'lambda_hex':hex(K[i]^(1<<i)),'quadratic_hex':hex(L),'canonical_rank':9,'canonical_plus_coordinate_plus_quadratic_rank':11}
 return word,closed,info,K,R

def replay(w,n,info,closed=False):
 loc=dict(enumerate(w['start']));rows={k:1<<k for k in range(222)};born=set(loc);counts=Counter();profile=Counter();peak=0;clears=[]
 for at,op in enumerate(w['program']):
  t,k=op[:2];counts[t]+=1
  if t=='INIT':
   need(k>=222 and k not in born,'genuine fresh owned INIT');born.add(k);loc[k]=op[2];rows[k]=0;peak=max(peak,len(loc)-222)
  elif t=='ADD':
   _,k,l,C=op;need(k!=l and loc.get(k)==loc.get(l)==C,'genuine cochart ADD');rows[k]^=rows[l]
  elif t=='MOVE':
   _,k,a,b=op;need(loc.get(k)==a,'actual MOVE source');fa,fb=w['frames'][str(a)],w['frames'][str(b)];delta=fb['dim']-fa['dim'];need(delta!=0,'no fictitious zero-rank movement')
   small,large=(fa,fb) if delta>0 else(fb,fa)
   need(all(dot(u,v)==0 for u in small['B'] for v in large['A']),'exact real nested geometry')
   need((delta>0) if k<222 else (k==334 and delta<0),'public ascending, only one genuinely descending owned record')
   loc[k]=b;profile[abs(delta)]+=1
  elif t=='CLEAR':
   need(k>=222 and loc.get(k)==op[2],'actual owned CLEAR');clears.append({'record':k,'chart':op[2],'value_hex':hex(rows[k])});del rows[k];del loc[k]
  else:raise ValueError(t)
 i=info['i'];L=int(info['quadratic_hex'],16);lam=int(info['lambda_hex'],16)
 for k in range(111):
  need(rows[k]==1<<k and loc[k]==n['final'][k],'all original X restored')
  need(rows[111+k]==((1<<(111+k))^((1<<k) if k==i else 0)),'exact full222-input public map')
  need(loc[111+k]==(n['final'][111+k] if closed or k==i else n['start'][111+k]),'original Y endpoint')
 if closed:need(set(loc)==set(range(222)),'all owners retired')
 else:
  need(set(loc)==set(range(335)),'exact retained lifetime set')
  for k in range(111):need(rows[222+k]==1<<k and loc[222+k]==n['start'][k],'stationary original point copy')
  need(rows[333]==(1<<(111+i))^lam and loc[333]==info['common_chart'],'actual dirty proper history')
  need(rows[334]==L and loc[334]==n['start'][111],'actual pure quadratic ground mode')
 return {'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'rank_length':sum(k*v for k,v in profile.items()),'owned_peak':peak,'owned_live':len(loc)-222,'nonzero_clears':clears},loc,rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);ap.add_argument('--i',type=int,default=92);ap.add_argument('--j',type=int,default=54);a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw));a.outdir.mkdir(parents=True,exist_ok=True)
 p,c,info,K,R=emit(n,a.i,a.j);rp,loc,rows=replay(p,n,info);rc,_,_=replay(c,n,info,True)
 if(a.i,a.j)==(92,54):
  need(len(info['common_inputs'])==32 and len(info['exclusive_inputs'])==25,'chosen exact source partition');need(rc['movement_profile']=={1:28,2:32,5:32,6:27,7:164},'chosen complete partial invoice')
  need(rc['rank_length']==1562 and rc['counts']['ADD']==232 and rc['counts']['INIT']==113,'exact operation counts')
 controls=[]
 preds=[('common quadratic acquisition',lambda o:o[0]=='ADD' and o[1]==333),('exclusive local acquisition',lambda o:o[0]=='ADD' and o[1]==111+a.i and o[2]<111),('quadratic preload into Y',lambda o:o[:3]==['ADD',111+a.i,333]),('canonical packet acquisition',lambda o:o[0]=='ADD' and o[1]==334 and o[2]<111),('masked completion',lambda o:o[:3]==['ADD',111+a.i,334]),('swap purification',lambda o:o[:3]==['ADD',333,334])]
 for name,pred in preds:
  q=next(k for k,o in enumerate(p['program']) if pred(o));m={**p,'program':p['program'][:q]+p['program'][q+1:]}
  try:replay(m,n,info)
  except ValueError:controls.append(name)
  else:raise ValueError('accepted destructive mutation '+name)
 try:setup(n,0,8)
 except ValueError:controls.append('orthogonal pair without own-block correction')
 else:raise ValueError('orthogonal-pair mode was accepted as common-only')
 # A genuine future receiver-region cut; all8 nonorthogonal coordinate normals exclude the chosen diagonal only if i absent.
 # Search source-independent pairwise-nonorthogonal8 sets and evaluate actual full222-column observations.
 full=(1<<111)-1;adj=[full^k for k in K];witness=None
 def walk(S,cand):
  nonlocal witness
  if witness:return
  if len(S)==8:
   def inside(C):return any(all(dot(b,R[t])==0 for b in p['frames'][str(C)]['B']) for t in S)
   O=[rows[k] for k,C in loc.items() if inside(C)];T=[(1<<t)^(1<<(111+t)) for t in S];r0=rank(O);r1=rank(O+T)
   if r1-r0==8:witness={'receivers':S,'observation_rank':r0,'target_augmented_rank':r1,'future_deficit':8,'proper_dirty_cache_inside':inside(info['common_chart'])}
   return
  if cand.bit_count()<8-len(S):return
  while cand and witness is None:
   bit=cand&-cand;cand^=bit;t=bit.bit_length()-1;walk(S+[t],cand&adj[t])
 walk([],full&~(1<<a.i));need(witness is not None,'actual future eight-width cut witness')
 pins={}
 for name,w in [('PREFIX.json.gz',p),('CLOSED-PARTIAL.json.gz',c)]:
  payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();raw=gzip.compress(payload,mtime=0);(a.outdir/name).write_bytes(raw);pins[name]={'gzip_sha256':hashlib.sha256(raw).hexdigest(),'canonical_json_sha256':hashlib.sha256(payload).hexdigest()}
 out={'status':'PASS_ACTUAL_QUADRATIC_HISTORY_PIVOT','native_sha256':PIN,'source':info,'prefix':rp,'closed_partial':rc,'future_cut':witness,'negative_controls':controls,'word_pins':pins,'complete_source':False,'new_kappa':None,'qualification':'One real new quadratic history and one target; no static8-mode complement or physical continuation is claimed.'}
 (a.outdir/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'source':info,'prefix_counts':rp['counts'],'closed_counts':rc['counts'],'profile':rc['movement_profile'],'future_cut':witness}))
if __name__=='__main__':main()
