#!/usr/bin/env python3
"""Actual orthogonal staircase followed by harvesting a local section moment."""
import argparse,gzip,hashlib,json,itertools
from collections import Counter
from pathlib import Path
from primitives import PIN,need,rank,dot,nullspace,F

def basis(rows):
 B=[]
 for r in rows:
  if rank(B+[r])>len(B):B.append(r)
 return B

def emit(n,S):
 R=[list(map(F,n['frames'][str(n['start'][k])]['B'][0])) for k in range(111)]
 need(1<=len(S)<=8 and len(set(S))==len(S),'positive distinct orthogonal set')
 need(all(dot(R[i],R[j])==0 for i,j in itertools.combinations(S,2)),'actual pairwise orthogonality')
 K=[sum(int(k==l or dot(R[k],R[l])==0)<<l for l in range(111)) for k in range(111)]
 h=(1<<111)-1
 for i in S:h&=K[i]
 raw_product=h
 for i in S:h^=1<<i
 common=[k for k in range(111) if h>>k&1]
 frames=json.loads(json.dumps(n['frames']));hub=n['final'][0];ground=n['start'][111];Cs=[hub]
 for z in range(1,len(S)+1):
  A=[R[i] for i in S[:z]];B=nullspace(A);d=8-z;found=None
  for f,Fm in frames.items():
   if Fm['dim']==d and all(dot(v,r)==0 for v in Fm['B'] for r in A):found=int(f);break
  if found is None:
   found=max(map(int,frames))+1;frames[str(found)]={'dim':d,'B':[[str(x) for x in row] for row in B],'A':[[str(x) for x in row] for row in A]}
  Cs.append(found)
 need(all(all(dot(R[k],R[i])==0 for i in S) for k in common),'literal common support')
 Q=333;P=334;ops=[]
 def move(k,a,b):
  if a!=b:ops.append(['MOVE',k,a,b])
 for k in range(111):ops.extend([['INIT',222+k,n['start'][k]],['ADD',222+k,k,n['start'][k]]])
 ops.append(['INIT',Q,Cs[-1]])
 for k in common:
  move(k,n['start'][k],Cs[-1]);ops.append(['ADD',Q,k,Cs[-1]]);move(k,Cs[-1],hub)
 for k in range(111):
  if k not in S and k not in common:move(k,n['start'][k],hub)
 for a in range(1,len(S)):ops.append(['ADD',111+S[a],111+S[a-1],ground])
 for a,k in enumerate(S,1):move(111+k,ground,Cs[a])
 if len(S)==1:move(S[0],n['start'][S[0]],hub)
 else:
  for a,k in enumerate(S[:-1]):move(k,n['start'][k],Cs[a])
  acc=S[-1];move(acc,n['start'][acc],Cs[-2])
  for a in range(len(S)-1,0,-1):
   ops.append(['ADD',111+S[a-1],acc,Cs[a]])
   move(acc,Cs[a],Cs[a-1])
   if a>1:
    k=S[a-1];ops.append(['ADD',acc,k,Cs[a-1]]);move(k,Cs[a-1],hub)
  for k in S[1:-1]:ops.append(['ADD',acc,k,hub])
 ops.append(['INIT',P,hub])
 for k in S:ops.append(['ADD',P,k,hub])
 for a,k in enumerate(S,1):
  move(P,Cs[a-1],Cs[a]);ops.extend([['ADD',111+k,P,Cs[a]],['ADD',P,111+k,Cs[a]]]);move(111+k,Cs[a],n['final'][111+k])
 ops.extend([['ADD',P,Q,Cs[-1]],['ADD',Q,P,Cs[-1]],['ADD',P,Q,Cs[-1]]]);move(P,Cs[-1],ground)
 final=n['final'][:111]+[n['final'][111+k] if k in S else ground for k in range(111)]
 word={'schema':'native_nested_linear_partial_word','public':222,'owned_fields':list(range(222,335)),'start':n['start'][:222],'final':final,'frames':frames,'program':ops[:],'end_owned':list(range(222,335)),'scope':'Orthogonal outputs completed, pure common-section moment retained; partial source only.'}
 for k in range(111):
  if k not in S:move(111+k,ground,n['final'][111+k])
 for k in range(111):ops.append(['CLEAR',222+k,n['start'][k]])
 ops.extend([['CLEAR',Q,Cs[-1]],['CLEAR',P,ground]])
 closed={**word,'program':ops,'final':n['final'][:222],'end_owned':[],'scope':'Closed partial source; only selected orthogonal outputs updated.'}
 C=basis(K);Q2=basis(C+[x&y for x,y in itertools.combinations(C,2)]);E=Q2+[1<<k for k in list(range(8))+list(S)]
 info={'selected':list(S),'charts':Cs,'common_inputs':common,'product_hex':hex(raw_product),'harvest_hex':hex(h),'canonical_rank':len(C),'quadratic_rank':len(Q2),'quadratic_plus_selected_and_coordinate_rank':rank(E),'quadratic_plus_selected_and_coordinate_plus_harvest_rank':rank(E+[h])}
 if S==(8,10,12):need(len(common)==13 and rank(E)==47 and rank(E+[h])==48,'actual cubic reservoir escape')
 if S==(8,10,12,13):
  parts=[[0,3,5,6],[103,106,108,109],[104,105,107,110]];need(sorted(sum(parts,[]))==common,'actual D4 partition');need(all(dot(R[u],R[v])==0 for T in parts for u,v in itertools.combinations(T,2)),'all3orthogonal four-sets');need(all(dot(R[u],R[v])!=0 for a,A in enumerate(parts) for B in parts[a+1:] for u in A for v in B),'no cross-frame D4 orthogonality');need(all(all(R[k][t]==0 for t in (1,2,4,7)) and dot(R[k],R[k])==(1 if k<8 else 4) for k in common),'literal rank4 coordinate-section roots');need(raw_product==(K[8]&K[10]&K[12]),'cubic and fourfold products agree on source');need(rank(E)==48 and rank(E+[h])==49,'actual D4 reservoir escape');info['D4_orthogonal_components']=parts
 return word,closed,info,R

def replay(w,n,info,closed=False):
 loc=dict(enumerate(w['start']));rows={k:1<<k for k in range(222)};born=set(loc);counts=Counter();profile=Counter();peak=0;clears=[]
 for at,op in enumerate(w['program']):
  t,k=op[:2];counts[t]+=1
  if t=='INIT':need(k>=222 and k not in born,'fresh real owner');born.add(k);loc[k]=op[2];rows[k]=0;peak=max(peak,len(loc)-222)
  elif t=='ADD':
   _,k,l,C=op;need(k!=l and loc.get(k)==loc.get(l)==C,'actual cochart ADD');rows[k]^=rows[l]
  elif t=='MOVE':
   _,k,a,b=op;need(loc.get(k)==a,'actual MOVE source');fa,fb=w['frames'][str(a)],w['frames'][str(b)];delta=fb['dim']-fa['dim'];need(delta!=0,'nonzero movement');small,large=(fa,fb) if delta>0 else(fb,fa)
   need(all(dot(u,v)==0 for u in small['B'] for v in large['A']),'exact nested real charts');need((delta>0) if k<222 else(k==334 and delta<0),'ascending originals and unique descending owner');loc[k]=b;profile[abs(delta)]+=1
  elif t=='CLEAR':
   need(k>=222 and loc.get(k)==op[2],'real retirement');clears.append({'record':k,'chart':op[2],'value_hex':hex(rows[k])});del loc[k];del rows[k]
  else:raise ValueError(t)
 S=info['selected'];h=int(info['harvest_hex'],16);y=sum(1<<(111+k) for k in S)
 for k in range(111):
  need(rows[k]==1<<k and loc[k]==n['final'][k],'all original X restored');need(rows[111+k]==((1<<(111+k))^((1<<k) if k in S else 0)),'full222-column public map');need(loc[111+k]==(n['final'][111+k] if closed or k in S else n['start'][111+k]),'actual original Y endpoints')
 if closed:need(set(loc)==set(range(222)),'complete retirement')
 else:
  need(set(loc)==set(range(335)),'exact retained lifetime set')
  for k in range(111):need(rows[222+k]==1<<k and loc[222+k]==n['start'][k],'genuine stationary source copy')
  need(rows[333]==y and loc[333]==info['charts'][-1],'pure original-Y mask retained on final section');need(rows[334]==h and loc[334]==n['start'][111],'pure harvested moment at ground')
 return {'counts':dict(counts),'profile':dict(sorted(profile.items())),'rank_length':sum(k*v for k,v in profile.items()),'peak_owned':peak,'live_owned':len(loc)-222,'clears':clears},loc,rows

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--selected',default='8,10,12');ap.add_argument('--outdir',type=Path,required=True);a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin');n=json.loads(gzip.decompress(raw));S=tuple(map(int,a.selected.split(',')));p,c,info,R=emit(n,S);rp,loc,rows=replay(p,n,info);rc,_,_=replay(c,n,info,True);a.outdir.mkdir(parents=True,exist_ok=True)
 need(rc['rank_length']==1562,'one complete width of new descending rank length')
 controls=[]
 for name,pred in [('section acquisition',lambda o:o[0]=='ADD' and o[1]==333),('Y prefix mask',lambda o:o[0]=='ADD' and o[1]<222 and o[2]<222 and o[-1]==n['start'][111]),('tail preload',lambda o:o[0]=='ADD' and 111<=o[1]<222 and o[2]<111),('original restoration',lambda o:o[0]=='ADD' and o[1]<111 and o[-1]==n['final'][0]),('packet acquisition',lambda o:o[0]=='ADD' and o[1]==334 and o[2]<111),('masked output',lambda o:o[0]=='ADD' and 111<=o[1]<222 and o[2]==334),('final harvest swap',lambda o:o[:3]==['ADD',333,334])]:
  q=next((z for z,o in enumerate(p['program']) if pred(o)),None)
  if q is None:continue
  m={**p,'program':p['program'][:q]+p['program'][q+1:]}
  try:replay(m,n,info)
  except ValueError:controls.append(name)
  else:raise ValueError('mutation accepted:'+name)
 pins={}
 for name,w in [('PREFIX.json.gz',p),('CLOSED-PARTIAL.json.gz',c)]:
  payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(payload,mtime=0);(a.outdir/name).write_bytes(compressed);pins[name]={'gzip_sha256':hashlib.sha256(compressed).hexdigest(),'canonical_json_sha256':hashlib.sha256(payload).hexdigest()}
 out={'status':'PASS_ACTUAL_ORTHOGONAL_MOMENT_HARVEST','native_sha256':PIN,'source':info,'prefix':rp,'closed_partial':rc,'negative_controls':controls,'word_pins':pins,'complete_source':False,'new_kappa':None,'qualification':'One actual packet completes selected orthogonal targets and retains one acquired common-section mode. No complete continuation or multiplier.'}
 (a.outdir/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'source':info,'prefix_counts':rp['counts'],'closed_counts':rc['counts'],'profile':rc['profile']}))
if __name__=='__main__':main()
