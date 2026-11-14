#!/usr/bin/env python3
"""Exact two-packet fork source for a native orthogonality pentagon."""
import argparse,gzip,hashlib,json,itertools
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
IDS=[92,36,54,38,55]
def need(b,m):
 if not b:raise ValueError(m)
def dot(a,b):return sum(F(x)*F(y) for x,y in zip(a,b))
def nullspace(A):
 A=[list(map(F,r)) for r in A];p=[]
 for c in range(8):
  h=next((h for h in range(len(p),len(A)) if A[h][c]),None)
  if h is None:continue
  k=len(p);A[k],A[h]=A[h],A[k];z=A[k][c];A[k]=[v/z for v in A[k]]
  for h in range(len(A)):
   if h!=k:
    z=A[h][c];A[h]=[u-z*v for u,v in zip(A[h],A[k])]
  p.append(c)
 out=[]
 for c in range(8):
  if c in p:continue
  r=[F(0)]*8;r[c]=1
  for k,j in enumerate(p):r[j]=-A[k][c]
  out.append(r)
 return out

def emit(n):
 frames=json.loads(json.dumps(n['frames']));R=[list(map(F,frames[str(n['start'][k])]['B'][0])) for k in IDS];need(all((dot(R[i],R[j])==0)==((i-j)%5 in[1,4]) for i,j in itertools.combinations(range(5),2)),'actual induced C5')
 def chart(norms):
  B=nullspace(norms);d=len(B)
  for c,f in frames.items():
   if f['dim']==d and all(dot(b,a)==0 for b in f['B'] for a in norms):return int(c)
  c=max(map(int,frames))+1;frames[str(c)]={'dim':d,'B':[[str(x) for x in b] for b in B],'A':[[str(x) for x in a] for a in norms]};return c
 F0=n['final'][111+IDS[0]];F2=n['final'][111+IDS[2]];F3=n['final'][111+IDS[3]];C02=chart([R[0],R[2]]);C03=chart([R[0],R[3]]);hub=n['final'][0];zero=n['start'][111]
 H,S1,S4,S3,S2,P,Q=range(222,229);ops=[]
 for own,C in [(H,F0),(S1,C02),(S4,C03),(S3,F2),(S2,F3)]:ops.append(['INIT',own,C])
 cache_by_source={IDS[1]:(S1,C02),IDS[4]:(S4,C03),IDS[3]:(S3,F2),IDS[2]:(S2,F3)}
 for k in range(111):
  if k in cache_by_source:
   own,C=cache_by_source[k];ops += [['MOVE',k,n['start'][k],C],['ADD',own,k,C],['MOVE',k,C,hub]]
  else:ops.append(['MOVE',k,n['start'][k],hub])
 for own in[P,Q]:ops.append(['INIT',own,hub])
 for a in[0,1,4]:ops.append(['ADD',P,IDS[a],hub])
 for k in IDS:ops.append(['ADD',Q,k,hub])
 ops += [['MOVE',P,hub,F0],['MOVE',Q,hub,F0],['ADD',H,Q,F0],['ADD',P,Q,F0],['ADD',Q,H,F0],['ADD',Q,P,F0]]
 for own,cache,C in [(P,S1,C02),(Q,S4,C03)]:
  ops += [['MOVE',own,F0,C],['ADD',own,cache,C],['ADD',cache,own,C],['ADD',own,cache,C],['MOVE',own,C,zero]]
 for a,own in[(1,P),(4,Q)]:
  y=111+IDS[a];ops += [['ADD',y,own,zero],['MOVE',y,zero,n['final'][y]]]
 y=111+IDS[0];ops += [['ADD',y,P,zero],['ADD',y,Q,zero],['MOVE',y,zero,C03],['ADD',y,S4,C03],['MOVE',y,C03,F0],['ADD',y,H,F0]]
 for a,C,old,Fi,local in[(2,C02,S1,F2,S3),(3,C03,S4,F3,S2)]:
  y=111+IDS[a];ops += [['MOVE',y,zero,C],['ADD',y,old,C],['MOVE',y,C,Fi],['ADD',y,local,Fi]]
 owned=list(range(222,229));end=n['final'][:111]+[n['final'][111+k] if k in IDS else zero for k in range(111)]
 info={'ids':IDS,'charts':{'F0':F0,'F2':F2,'F3':F3,'C02':C02,'C03':C03,'hub':hub,'zero':zero},'owners':{'H':H,'S1':S1,'S4':S4,'S3':S3,'S2':S2,'P':P,'Q':Q}}
 w={'schema':'two-packet-pentagon-fork-partial/1','public':222,'owned_fields':owned,'start':n['start'][:222],'final':end,'frames':frames,'program':ops[:],'end_owned':owned,'scope':'Five exact original targets, two full descending packets, five stationary caches. Other106originalYunchanged.'}
 close=[['MOVE',111+k,zero,n['final'][111+k]] for k in range(111) if k not in IDS]+[['CLEAR',own,C] for own,C in[(H,F0),(S1,C02),(S4,C03),(S3,F2),(S2,F3),(P,zero),(Q,zero)]]
 c={**w,'program':ops+close,'final':n['final'][:222],'end_owned':[],'scope':'Closed partial map completing exactly the five stated targets; not complete111-port supplier.'}
 return w,c,info

def replay(w,n,info,closed=False,live_sources=False):
 loc=dict(enumerate(w['start']));values={k:1<<k for k in range(222)};born=set(loc);counts=Counter();profile=Counter();clear=[];peak=0;hist=[]
 for at,op in enumerate(w['program']):
  t,k=op[:2];counts[t]+=1
  if t=='INIT':need(k>=222 and k not in born,'fresh zero owner');born.add(k);loc[k]=op[2];values[k]=0;peak=max(peak,len(loc)-222)
  elif t=='ADD':_,k,l,C=op;need(k!=l and loc.get(k)==loc.get(l)==C,'actual same-chart ADD');values[k]^=values[l]
  elif t=='MOVE':
   _,k,a,b=op;need(loc.get(k)==a,'actual MOVE source');fa,fb=w['frames'][str(a)],w['frames'][str(b)];delta=fb['dim']-fa['dim'];need(delta!=0,'nonzero MOVE');sm,lg=(fa,fb) if delta>0 else(fb,fa);need(all(dot(v,u)==0 for v in sm['B'] for u in lg['A']),'rational chart inclusion');need(delta>0 if k<222 else k in[227,228] and delta<0,'original ascending and only two descending owners');loc[k]=b;profile[abs(delta)]+=1
   if k>=222:hist.append({'operation':at,'record':k,'from':a,'to':b,'value_hex':hex(values[k])})
  elif t=='CLEAR':need(k>=222 and loc.get(k)==op[2],'charged actual owned clearing');clear.append({'record':k,'chart':op[2],'value_hex':hex(values[k])});del loc[k];del values[k]
  else:raise ValueError(t)
 for k in range(111):
  need(values[k]==1<<k and loc[k]==(n['start'][k] if live_sources and not closed and k not in IDS else n['final'][k]),'original X values and declared live-source endpoints')
  need(values[111+k]==(1<<(111+k))^((1<<k) if k in IDS else 0),'all222 independent input columns and exactly five completed outputs')
  need(loc[111+k]==(n['final'][111+k] if closed or k in IDS else n['start'][111+k]),'actual original Y endpoints')
 if closed:need(set(loc)==set(range(222)),'all owners cleared')
 else:
  u=(1<<IDS[2])^(1<<IDS[3]);target={222:sum(1<<k for k in IDS),223:u,224:u,225:1<<IDS[3],226:1<<IDS[2],227:1<<IDS[1],228:1<<IDS[4]};need(set(loc)==set(range(229)) and all(values[k]==v for k,v in target.items()),'actual retained fork histories')
 return {'counts':dict(counts),'movement_profile':dict(sorted(profile.items())),'rank_length':sum(r*c for r,c in profile.items()),'peak_owned':peak,'live_owned':len(loc)-222,'descending_histories':hist,'nonzero_clears':clear}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--native',type=Path,required=True);ap.add_argument('--outdir',type=Path,required=True);a=ap.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native exact pin');n=json.loads(gzip.decompress(raw));w,c,info=emit(n);rp=replay(w,n,info);rc=replay(c,n,info,True);need(rc['movement_profile']=={1:9,2:2,5:2,6:7,7:215} and rc['rank_length']==1570,'complete partial invoice');need(rp['counts']=={'INIT':7,'MOVE':129,'ADD':32},'prefix exact operation counts')
 controls=[]
 for label,pred in [('local1acquisition',lambda o:o[:2]==['ADD',223]),('local4acquisition',lambda o:o[:2]==['ADD',224]),('cross3acquisition',lambda o:o[:2]==['ADD',225]),('cross2acquisition',lambda o:o[:2]==['ADD',226]),('Hhistory',lambda o:o[:3]==['ADD',222,228]),('forkduplication',lambda o:o[:3]==['ADD',228,227]),('branch1swap',lambda o:o[:3]==['ADD',223,227]),('branch4swap',lambda o:o[:3]==['ADD',224,228]),('finalHread',lambda o:o[:3]==['ADD',111+IDS[0],222])]:
  q=next(j for j,o in enumerate(w['program']) if pred(o));m={**w,'program':w['program'][:q]+w['program'][q+1:]}
  try:replay(m,n,info)
  except ValueError:controls.append(label)
  else:raise ValueError('destructive operation deletion accepted: '+label)
 # Keep unserved original source lines physically live in the continuation variant.
 cut=lambda op:op[0]=='MOVE' and op[1]<111 and op[1] not in IDS
 cw={**w,'program':[op for op in w['program'] if not cut(op)],'final':[n['final'][k] if k in IDS else n['start'][k] for k in range(111)]+w['final'][111:],'scope':'Continuable five-target fork: unserved106 original X remain unchanged on their actual source lines; unservedYatground.'}
 cc={**c,'program':cw['program']+[['MOVE',k,n['start'][k],n['final'][k]] for k in range(111) if k not in IDS]+c['program'][len(w['program']):],'scope':'Closure of live-source fork: remaining original X ascend only after the five-target module; no complete supplier.'}
 rcp=replay(cw,n,info,live_sources=True);rcc=replay(cc,n,info,closed=True,live_sources=True);need(rcp['counts']=={'INIT':7,'MOVE':23,'ADD':32} and rcc['movement_profile']==rc['movement_profile'],'continuable word preserves exact closed invoice')
 a.outdir.mkdir(parents=True,exist_ok=True);pins={}
 for name,word in [('PREFIX.json.gz',w),('CLOSED-PARTIAL.json.gz',c),('CONTINUABLE-PREFIX.json.gz',cw),('CONTINUABLE-CLOSED-PARTIAL.json.gz',cc)]:
  payload=json.dumps(word,sort_keys=True,separators=(',',':')).encode();r=gzip.compress(payload,mtime=0);(a.outdir/name).write_bytes(r);pins[name]={'gzip_sha256':hashlib.sha256(r).hexdigest(),'canonical_json_sha256':hashlib.sha256(payload).hexdigest()}
 out={'status':'PASS_ACTUAL_TWO_PACKET_PENTAGON_FORK','native_sha256':PIN,'source':info,'prefix':rp,'closed_partial':rc,'continuable_prefix':rcp,'continuable_closed_partial':rcc,'remaining_source_status':{'all_Hub_control_prefix':'106 independent unserved source dimensions have no proper-chart observation; further proper-boundary entry capacity is at least106V. Not a target-feasible frontier.','continuable_prefix':'106 original X remain at actual source lines and106 Y atground; no future source-acquisition cost granted.'},'negative_controls':controls,'word_pins':pins,'complete_source':False,'new_kappa':None,'qualification':'Actual five-target joint source beats its isolated3-packet cover; remaining106targets and target supplier unresolved.'};(a.outdir/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'prefix_counts':rp['counts'],'closed_profile':rc['movement_profile'],'rank_length':rc['rank_length']}))
if __name__=='__main__':main()
