#!/usr/bin/env python3
"""Independent native-chart and222-column review of the all-point-retention halfclass word."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,copy,gzip,hashlib,json
def need(b,s):
 if not b:raise ValueError(s)
def load(p,pin=None):
 b=p.read_bytes();need(pin is None or hashlib.sha256(b).hexdigest()==pin,'source pin');return json.loads(gzip.decompress(b))
def rref(rows):
 a=[list(map(F,r)) for r in rows];j=0
 for c in range(8):
  k=next((k for k in range(j,len(a)) if a[k][c]),None)
  if k is None:continue
  a[j],a[k]=a[k],a[j];z=a[j][c];a[j]=[v/z for v in a[j]]
  for k in range(len(a)):
   if k!=j:
    z=a[k][c];a[k]=[v-z*w for v,w in zip(a[k],a[j])]
  j+=1
 return tuple(tuple(r) for r in a[:j])
def inside(a,b):return len(rref(a+b))==len(b)
def rank(rows):
 b={}
 for x in rows:
  while x:
   j=x.bit_length()-1
   if j in b:x^=b[j]
   else:b[j]=x;break
 return len(b)
def main(a):
 n=load(a.native,'51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78')
 cert=json.loads((a.bundle/'CERTIFICATE.json').read_text());roots=[list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 groups={}
 for i,v in enumerate(roots[8:],8):groups.setdefault((tuple(j for j,x in enumerate(v) if x),sum(x<0 for x in v)%2),[]).append(i)
 need(list(groups.values())==[z['indices'] for z in cert['groups']],'all native halfclasses')
 piv=cert['pivots'];need(len(piv)==28 and all(p in g for p,g in zip(piv,groups.values())),'actual representative membership')
 K=[sum(1<<j for j,w in enumerate(roots) if i==j or sum(x*y for x,y in zip(v,w))==0) for i,v in enumerate(roots)]
 R=[]
 for v in K:
  x=v&~255
  for p,g in zip(piv,groups.values()):
   if v>>p&1:x^=sum(1<<j for j in g)
  R.append(x)
 B=[R[i] for i in (8,14,30)];need(rank(R)==rank(B)==3,'actual three global modes')
 need([hex(x) for x in R]==cert['gauged_rows_hex'] and [hex(x) for x in B]==cert['global_basis_hex'],'all independently reconstructed core rows')
 retained=cert['retained'];need(retained==list(range(111)),'all111 retained original point copies')
 pins={'PREFIX.json.gz':'a19e5d28edc7cbd0eea9a636233cf99a7b83693d955b4959f16fb59fc0299869','CLOSED-WORD.json.gz':'3cfc771872c2d5d656f62ac1d59fd771bb73e748eb8ef0ce04d6e0979782d393'}
 def replay(w,closed,zero_y=False):
  need(w['public']==222 and w['owned_fields']==117 and w['start']==n['start'][:222],'native input interface')
  frames={int(c):rref(f['B']) for c,f in w['frames'].items()};dim={c:len(b) for c,b in frames.items()}
  for c,b in frames.items():
   f=w['frames'][str(c)];A=rref(f['A']);need(len(b)==f['dim'] and len(A)==8-len(b),'complete chart ranks')
   need(all(sum(x*y for x,y in zip(v,u))==0 for v in b for u in A),'native frame equations')
  native_ids=set(n['start'][:222]+n['final'][:222]);checked_ids=native_ids&set(frames)
  need(set(n['start'][:222])<=checked_ids and (not closed or native_ids<=checked_ids),'all actually used native endpoint charts present')
  for c in checked_ids:need(frames[c]==rref(n['frames'][str(c)]['B']),'native physical endpoint subspace')
  at=dict(enumerate(w['start']));v={i:(0 if zero_y and i>=111 else 1<<i) for i in range(222)};born=set(at);counts=Counter();moves=Counter();peak=0;pairs=set();clears=[]
  for o in w['program']:
   op,i=o[:2];counts[op]+=1;need(0<=i<339,'declared source/owned range')
   if op=='INIT':need(i>=222 and i not in born,'fresh zero born');born.add(i);at[i]=o[2];v[i]=0;peak=max(peak,len(at)-222)
   elif op=='CLEAR':need(i>=222 and at.get(i)==o[2],'owned erasure');clears.append((i,at[i],v[i]));del at[i];del v[i]
   elif op=='ADD':
    _,i,j,c=o;need(i!=j and i in at and j in at and at[i]==at[j]==c,'actual cochart read');v[i]^=v[j]
   elif op=='MOVE':
    _,i,c,d=o;need(at.get(i)==c,'actual MOVE entrance');delta=dim[d]-dim[c];need(delta==(1 if i<222 else -1),'declared unit monotone movement')
    need(i<222 or 333<=i<=335,'only global packets move among owned')
    if (c,d) not in pairs:need(inside(frames[c],frames[d]) if delta>0 else inside(frames[d],frames[c]),'actual nested chart pair');pairs.add((c,d))
    at[i]=d;moves[abs(delta)]+=1
   else:raise ValueError('unsupported operation')
  expected={i:1<<i for i in range(222)}
  for i,x in enumerate(R):expected[111+i]^=x
  if not closed:
   for p,g in zip(piv,groups.values()):expected[p]=sum(1<<i for i in g)
   expected.update({222+t:1<<j for t,j in enumerate(retained)})
   expected.update({336+t:x for t,x in enumerate(B)})
  need(v==expected,'all222 public and all live owned coefficient rows')
  need([at[i] for i in range(222)]==w['final'],'actual public endpoint charts')
  if closed:need(w['final']==n['final'][:222] and len(at)==222,'closed original endpoints and owned lifetimes')
  else:
   need(all(at[222+t]==n['start'][j] for t,j in enumerate(retained)) and all(at[336+t]==0 for t in range(3)),'all live local copy placements')
   for p,g in zip(piv,groups.values()):need(frames[at[p]]==rref([roots[j] for j in g]),'bank at actual minimal real span')
  need(counts==({'INIT':117,'ADD':571,'MOVE':1578,'CLEAR':117} if closed else {'INIT':117,'ADD':496,'MOVE':680,'CLEAR':3}) and peak==115,'exact complete/prefix invoice')
  need([x for i,c,x in clears if 333<=i<=335]==B,'three actual global erasures')
  return dict(counts=dict(counts),peak_owned=peak,owned_live_at_end=len(at)-222,exact_nested_pairs=len(pairs),nonzero_erasures=sum(bool(x) for i,c,x in clears),all222_columns_checked=True,native_endpoint_chart_ids_checked=len(checked_ids))
 words={k:load(a.bundle/k,h) for k,h in pins.items()};receipts={k:replay(w,k.startswith('CLOSED')) for k,w in words.items()}
 controls=[]
 for label,name,predicate in [('missing_point_copy','PREFIX.json.gz',lambda o:o[0]=='ADD' and o[1]==222),('missing_pure_core_copy','PREFIX.json.gz',lambda o:o[0]=='ADD' and o[1]==336),('missing_pivot_restoration','CLOSED-WORD.json.gz',lambda o:o[0]=='ADD' and o[1] in piv and o[3]==1)]:
  w=copy.deepcopy(words[name]);t=next(i for i,o in enumerate(w['program']) if predicate(o));del w['program'][t]
  try:replay(w,name.startswith('CLOSED'))
  except ValueError:controls.append(label)
  else:raise ValueError('accepted missing source operation')
 w=copy.deepcopy(words['PREFIX.json.gz']);cid=str(n['start'][0]);w['frames'][cid]['B']=[[0,1,0,0,0,0,0,0]]
 try:replay(w,False)
 except ValueError:controls.append('wrong_initial_native_chart')
 else:raise ValueError('accepted wrong physical chart')
 try:replay(words['CLOSED-WORD.json.gz'],True,True)
 except ValueError:controls.append('unknown_original_Y_assumed_zero')
 else:raise ValueError('accepted zero-Y substitution')
 out=dict(status='PASS_INDEPENDENT_ALL_POINT_SOURCE_AND_CLOSURE',word_pins=pins,receipts=receipts,negative_controls=controls,core_rank=3,closed_target='X=x andY=y+Rx, NOT the requiredY=y+x',scope='Exact finite native source and scalar characteristic-two identity lift; all receiver-region cut sufficiency is NOT claimed; actual decoder remains open.',new_kappa=None)
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':out['status'],'controls':len(controls),'closed_source_MOVEs':1578}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','bundle','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
