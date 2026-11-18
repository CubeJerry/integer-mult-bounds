#!/usr/bin/env python3
"""Independent bitmask replay on native root-closure charts."""
import argparse,gzip,json
from collections import Counter
from hashlib import sha256
from pathlib import Path
from fractions import Fraction

def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 ap=argparse.ArgumentParser()
 for name in ['layout','word','proof','out']:ap.add_argument('--'+name,type=Path,required=True)
 a=ap.parse_args();lr=gzip.decompress(a.layout.read_bytes());need(sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
 L=json.loads(lr);R=L['root_table'];wr=a.word.read_bytes();W=json.loads(wr);donors=W['native_donors'];receivers=W['native_receivers'];n=len(donors);d=W['bank_field_dimension'];w=W['field_degree'];b=d*w
 need(n==7 and b==15 and len(set(donors))==len(set(receivers))==7,'native owners')
 dot=lambda x,y:sum(u*v for u,v in zip(x,y))
 for i in range(n):
  for j in range(n):need((dot(R[receivers[i]],R[donors[j]])==0)==(i!=j),'native pairing')
 charts={'Ground':(0,frozenset()),'Hub':(8,frozenset(range(120)))}
 def chart(name):
  if name not in charts:
   k=int(name[1:]);tag=name[0]
   if tag=='L':charts[name]=(1,frozenset([k]))
   elif tag=='H':charts[name]=(2,frozenset(L['A2'][k]))
   elif tag=='D':charts[name]=(4,frozenset(L['D4'][k]))
   elif tag=='F':charts[name]=(7,frozenset(j for j,r in enumerate(R)if dot(r,R[k])==0))
   elif tag=='K':charts[name]=(6,frozenset(j for j,r in enumerate(R)if all(dot(r,R[u])==0 for u in L['A2'][k])))
   else:raise ValueError('unknown chart')
  return charts[name]
 names=[f'{bank}{j}_{c}_b{t}'for bank in ['X','Y']for j in range(n)for c in range(d)for t in range(w)];initial={name:1<<k for k,name in enumerate(names)}
 def replay(events,corrupt=False):
  state=initial.copy();loc={f'X{j}_{c}_b{t}':'L'+str(donors[j])for j in range(n)for c in range(d)for t in range(w)}
  loc.update({f'Y{j}_{c}_b{t}':'Ground'for j in range(n)for c in range(d)for t in range(w)})
  if corrupt:state['Y0_0_b0']^=1
  owned=set();ever=set(names);counts=Counter();profile=Counter();dirty=peak=0
  for event in events:
   op=event[0];x=event[1];counts[op]+=1
   if op=='INIT':need(x not in ever,'fresh owner');ever.add(x);state[x]=0;loc[x]=event[2];chart(loc[x]);owned.add(x);peak=max(peak,len(owned))
   elif op=='ADD':
    y=event[2];need(x in state and y in state and x!=y and loc[x]==loc[y],'live colocated ADD');state[x]^=state[y]
   elif op=='MOVE':
    need(x in state,'live MOVE');before,after=chart(loc[x]),chart(event[2]);need(before[0]<after[0] and before[1]<after[1],'strict upward root inclusion');profile[after[0]-before[0]]+=1;loc[x]=event[2]
   elif op=='CLEAR':need(x in owned,'owned retirement');dirty+=bool(state[x]);owned.remove(x);del state[x];del loc[x]
   else:raise ValueError('unknown opcode')
  need(not owned and set(state)==set(names),'closed owners')
  for j in range(n):
   for c in range(d):
    for t in range(w):
     x=f'X{j}_{c}_b{t}';y=f'Y{j}_{c}_b{t}';target=initial[y]
     for k in range(n):
      if k!=j:target^=initial[f'X{k}_{c}_b{t}']
     need(state[x]==initial[x] and loc[x]=='Hub','original X restored');need(state[y]==target and loc[y]=='F'+str(receivers[j]),'all-input target')
  return {'counts':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),'dirty_CLEAR':dirty,'peak_owned':peak,'original_columns':len(names)}
 invoice=replay(W['events']);tests=[]
 for opcode in ['ADD','MOVE']:
  k=next(i for i,e in enumerate(W['events'])if e[0]==opcode and (opcode!='ADD' or e[1].startswith('Y')))
  try:replay(W['events'][:k]+W['events'][k+1:])
  except ValueError:tests.append('omitted_'+opcode)
  else:raise ValueError('mutation accepted')
 try:replay(W['events'],True)
 except ValueError:tests.append('arbitrary_Y_corruption')
 else:raise ValueError('Y mutation accepted')
 for label,predicate in [('K_ADD',lambda e:e[0]=='ADD' and e[1].startswith('M') and e[2].startswith('M')),('K_MOVE',lambda e:e[0]=='MOVE' and e[2].startswith('K'))]:
  k=next(i for i,e in enumerate(W['events'])if predicate(e))
  try:replay(W['events'][:k]+W['events'][k+1:])
  except ValueError:tests.append('omitted_'+label)
  else:raise ValueError('K mutation accepted')
 geometry=[]
 for j,k,h in W['plane_indices']:
  plane=set(L['A2'][h]);need({donors[j],donors[k]}<=plane,'actual pair plane');targets=[i for i in range(n)if i not in [j,k]];hist=Counter();triples=Counter()
  for D in L['D4']:
   if not plane<=set(D):continue
   seen=tuple(i for i in targets if all(dot(R[x],R[receivers[i]])==0 for x in D));hist[len(seen)]+=1
   if len(seen)==3:triples[seen]+=1
  need(hist==Counter({0:10,1:15,3:20}) and len(triples)==10 and set(triples.values())=={2},'native shared-port visibility');geometry.append([h,dict(sorted(hist.items()))])
 scale=10**40
 def power_interval(n):
  target=n**199*scale**200;lo,hi=0,n*scale+1
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**200<=target:lo=mid
   else:hi=mid
  return Fraction(lo,scale),Fraction(hi,scale)
 bounds={n:power_interval(n)for n in [2,3,5]};delta=[315*bounds[5][0]-315*bounds[2][1]-189*bounds[3][1]-126,315*bounds[5][1]-315*bounds[2][0]-189*bounds[3][0]-126]
 need(0<delta[0]<=delta[1],'strict K-merge improvement')
 result={'direct_minus_merged_movement_interval':[str(x)for x in delta],'status':'PASS_ROOT_K6_MERGE_ALL_COLUMNS','word_sha256':sha256(wr).hexdigest(),'reviewed_proof_sha256':sha256(a.proof.read_bytes()).hexdigest(),'invoice':invoice,'actual_pair_planes':len(geometry),'all_triples_have_two_real_D4_witnesses':True,'mutation_controls':tests,'scope':'Paid seven-source fragment; no complete native supplier or new kappa.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
