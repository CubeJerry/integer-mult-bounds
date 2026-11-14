#!/usr/bin/env python3
"""Independent full-input replay; imports no author implementation."""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
WORD='8fc3983ea3b26f9c2977135387fb813b0a16aaf270de50fe2c83fefc1bbb229a'

def need(ok,message):
 if not ok:raise ValueError(message)

def echelon(rows):
 out={}
 for row in rows:
  v=list(map(F,row));need(len(v)==8,'ambient dimension')
  for p,b in sorted(out.items()):
   if v[p]:c=v[p];v=[x-c*y for x,y in zip(v,b)]
  p=next((i for i,x in enumerate(v) if x),None)
  if p is not None:
   c=v[p];out[p]=tuple(x/c for x in v)
 return out

def contained(a,b):
 for row in a.values():
  v=list(row)
  for p,r in sorted(b.items()):
   c=v[p]
   if c:v=[x-c*y for x,y in zip(v,r)]
  if any(v):return False
 return True

def replay(w,n,zero_original_y=False):
 need(w['public']==222,'public interface')
 need(w['start']==n['start'][:222] and w['final']==n['final'][:222],'native endpoints')
 bases={};dims={}
 for key,f in w['frames'].items():
  c=int(key);b=echelon(f['B']);a=echelon(f['A']);d=f['dim']
  need(len(b)==d and len(a)==8-d,'frame ranks')
  need(all(sum(x*y for x,y in zip(u,v))==0 for u in b.values() for v in a.values()),'orthogonal frame equations')
  bases[c]=b;dims[c]=d
 for c in set(w['start']+w['final']):
  b=echelon(n['frames'][str(c)]['B']);need(contained(b,bases[c]) and contained(bases[c],b),'native endpoint subspace')
 roots=[list(map(F,n['frames'][str(n['start'][i])]['B'][0])) for i in range(111)]
 groups=w['groups'];need(sorted(sum(groups,[]))==list(range(111)),'complete class partition')
 need(all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for g in groups for i in g for j in g if i!=j),'orthogonal classes')
 for g,chain in zip(groups,w['class_chains']):
  need(len(chain)==len(g)+1 and dims[chain[0]]==8,'complete chain')
  for i,c in enumerate(chain[1:],1):
   need(dims[c]==8-i,'chain codimension')
   need(all(sum(x*y for x,y in zip(b,roots[j]))==0 for b in bases[c].values() for j in g[:i]),'chain receiver intersection')
 loc=dict(enumerate(w['start']));row={i:(0 if zero_original_y and i>=111 else 1<<i) for i in range(222)}
 seen=set(range(222));counts=Counter();moves=Counter();peak=0;clear=[];first_birth=None;pairs=set()
 for t,op in enumerate(w['program']):
  tag,i=op[:2];counts[tag]+=1
  if tag=='MOVE':
   _,i,a,b=op;need(loc.get(i)==a,'actual MOVE source')
   need(dims[b]-dims[a]==(1 if i<222 else -1),'whole unit monotone MOVE')
   pair=(a,b)
   if pair not in pairs:
    small,large=(a,b) if dims[a]<dims[b] else (b,a)
    need(contained(bases[small],bases[large]),'exact nested MOVE');pairs.add(pair)
   loc[i]=b;moves[i]+=1
  elif tag=='ADD':
   _,i,j,c=op;need(i!=j and i in loc and j in loc and loc[i]==loc[j]==c,'actual cochart ADD')
   row[i]^=row[j]
  elif tag=='INIT':
   _,i,c=op;need(i>=222 and i not in seen and c==1,'fresh actual Hub packet')
   if first_birth is None:
    first_birth=t;need(all(row[j]==1<<j and loc[j]==1 for j in range(111)),'all X restored before packets')
    for g,chain in zip(groups,w['class_chains']):
     for k,j in enumerate(g,1):
      expected=sum(1<<(111+u) for u in g[:k])^sum(1<<u for u in g[k:])
      need(row[111+j]==expected and loc[111+j]==chain[k],'actual arbitrary-Y masked preload')
   seen.add(i);loc[i]=c;row[i]=0;peak=max(peak,len(loc)-222)
  elif tag=='CLEAR':
   _,i,c=op;need(i>=222 and i in loc and loc[i]==c==0,'owned ground erasure')
   clear.append(row[i]);del row[i];del loc[i]
  else:raise ValueError('unknown operation')
 need(set(loc)==set(range(222)),'all owned records closed')
 need(all(loc[i]==w['final'][i] for i in loc),'all final native charts')
 need(all(row[i]==1<<i for i in range(111)),'full X restoration')
 need(all(row[111+i]==((1<<i)^(1<<(111+i))) for i in range(111)),'full222-column target')
 need(clear==[sum(1<<(111+i) for i in g) for g in groups],'explicit arbitrary-Y erasure operands')
 need(counts=={'MOVE':1674,'ADD':687,'INIT':15,'CLEAR':15} and peak==1,'complete invoice')
 need(all(moves[i]==7 for i in range(222)) and all(moves[i]==8 for i in seen if i>=222),'per-record movement')
 return {'counts':dict(counts),'peak_owned':peak,'first_packet_operation':first_birth,
         'distinct_nested_MOVE_pairs':len(pairs),'all222_input_columns_checked':True,
         'nonzero_arbitrary_Y_clear_count':len(clear),'frame_count':len(bases)}

def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--word',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 nr=a.native.read_bytes();wr=a.word.read_bytes();need(hashlib.sha256(nr).hexdigest()==NATIVE,'native bytes');need(hashlib.sha256(wr).hexdigest()==WORD,'word bytes')
 n=json.loads(gzip.decompress(nr));w=json.loads(gzip.decompress(wr));receipt=replay(w,n);mutants=[]
 def check(label,v,zero=False):
  try:replay(v,n,zero)
  except ValueError as e:mutants.append({'case':label,'rejection':str(e)})
  else:raise ValueError('mutant accepted: '+label)
 operations=w['program'];first_birth=next(t for t,o in enumerate(operations) if o[0]=='INIT')
 controls={
  'omit_ground_Y_prefix':next(t for t,o in enumerate(operations) if o[0]=='ADD' and 111<=o[1]<222 and 111<=o[2]<222),
  'omit_borrowed_tail_read':next(t for t,o in enumerate(operations) if o[0]=='ADD' and 111<=o[1]<222 and o[2]<111),
  'omit_borrowed_X_restoration':next(t for t,o in enumerate(operations[:first_birth]) if o[0]=='ADD' and o[1]<111 and o[2]<111 and o[3]==1),
  'omit_one_MOVE':next(t for t,o in enumerate(operations) if o[0]=='MOVE'),
  'omit_owned_CLEAR':next(t for t,o in enumerate(operations) if o[0]=='CLEAR')}
 for label,t in controls.items():
  v=copy.deepcopy(w);del v['program'][t];check(label,v)
 t=next(t for t,o in enumerate(operations) if o[0]=='ADD' and 111<=o[1]<222 and o[2]>=222)
 v=copy.deepcopy(w);v['program'][t],v['program'][t+1]=v['program'][t+1],v['program'][t];check('reverse_two_ADD_exchange',v)
 check('assume_unknown_original_Y_zero',w,True)
 v=copy.deepcopy(w);v['final'][111]=v['final'][112];check('wrong_native_receiver_facet',v)
 out={'status':'PASS_INDEPENDENT_COMPLETE_ORTHOGONAL_STAIRCASE','native_sha256':NATIVE,'word_sha256':WORD,
      'author_code_imported':False,'receipt':receipt,'negative_controls':mutants,'full_physical_supplier_claimed':False,'new_kappa':None}
 a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'counts':receipt['counts'],'controls':len(mutants)}))

if __name__=='__main__':main()
