#!/usr/bin/env python3
"""Independent set-valued222-column replay of the two joint constructions."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,gzip,hashlib,json
def need(x,s):
 if not x:raise ValueError(s)
def rank(rows):
 b={}
 for row in rows:
  r=list(map(F,row))
  for p,v in sorted(b.items()):
   if r[p]:c=r[p];r=[x-c*y for x,y in zip(r,v)]
  p=next((p for p,x in enumerate(r) if x),None)
  if p is not None:c=r[p];b[p]=[x/c for x in r]
 return len(b)
def main(a):
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');s=json.loads(gzip.decompress(raw));packed=a.word.read_bytes();w=json.loads(gzip.decompress(packed));pure=a.variant=='pure'
 need(w['public']==222 and w['start']==s['start'][:222] and w['final']==s['final'][:222],'native public interface')
 frames={int(k):v for k,v in w['frames'].items()}
 for v in frames.values():
  A=[[F(x) for x in r] for r in v['A']];B=[[F(x) for x in r] for r in v['B']]
  need(rank(A)==8-v['dim'] and rank(B)==v['dim'] and all(sum(x*y for x,y in zip(r,t))==0 for r in A for t in B),'exact chart and complement')
 pairs={tuple(o[2:]) for o in w['program'] if o[0]=='MOVE'}
 for x,y in pairs:need(abs(frames[x]['dim']-frames[y]['dim'])==1 and rank(frames[x]['B']+frames[y]['B'])==max(frames[x]['dim'],frames[y]['dim']),'unit nested chart map')
 roots=[[F(x) for x in s['frames'][str(s['start'][i])]['B'][0]] for i in range(111)];K=[{j for j in range(111) if j==i or sum(x*y for x,y in zip(roots[i],roots[j]))==0} for i in range(2)];L=[k^set(range(8)) for k in K];H=[K[i]^{i} for i in range(2)];common=L[0]&L[1];need(len(common)==22,'common22 support')
 ps=[224,225] if pure else [222,223];facets=s['final'][111:113];hub=w['hub'];ground=s['start'][111];expected={'MOVE':1571 if pure else 1570,'ADD':296 if pure else 292,'INIT':4 if pure else 2,'CLEAR':4 if pure else 2}
 def replay(ops):
  values={i:{i} for i in range(222)};loc=dict(enumerate(w['start']));born=set();moves=Counter();counts=Counter();peak=0;erased=[];arr=[[],[]];entries=[];extra=0
  for t,o in enumerate(ops):
   op=o[0];counts[op]+=1
   if op=='INIT':
    _,r,c=o;need(222<=r<222+w['owned_fields'] and r not in born,'actual owned birth');born.add(r)
    if r in ps:
     i=ps.index(r);need(c==hub and all(values[j]=={j} and loc[j]==hub for j in range(111)),'all X restored before packet birth')
     if pure:need(values[222+i]==L[i] and loc[222+i]==facets[i],'actual pure preload')
     want=({111+i}|(set(range(8))^{i})) if pure else ({111+i}|H[i]);need(values[111+i]==want,'actual arbitrary-Y preload')
    values[r]=set();loc[r]=c;peak=max(peak,len(values)-222)
   elif op=='MOVE':
    _,r,x,y=o;need(r in loc and loc[r]==x and (x,y) in pairs,'actual MOVE source');delta=frames[y]['dim']-frames[x]['dim']
    if r<222:need(delta==1,'original monotone path')
    elif r in ps:need(delta==-1,'packet monotone path')
    else:
     need(pure and r==223 and delta==1 and values[r]==common and y==facets[1],'paid common upward copy');extra+=1
    if r in ps:
     i=ps.index(r)
     if x==hub:need(values[r]==K[i],'true current Hub acquisition')
     if x==facets[i]:
      want=L[i] if pure else ({111+i}|H[i]);need(values[r]==want and values[111+i]=={111+i,i},'complete exchange and retained old value');entries.append({'port':i,'outgoing':sorted(values[r])})
     if y==ground:need(values[r]==(L[i] if pure else ({111+i}|H[i])),'first-ground actual history')
    for i,f in enumerate(facets):
     if r<111 and y==f:arr[i].append(r)
    loc[r]=y;moves[r]+=1
   elif op=='ADD':
    _,r,z,c=o;need(r!=z and r in values and z in values and loc[r]==loc[z]==c,'actual cochart ADD');values[r]^=values[z]
   elif op=='CLEAR':
    _,r,c=o;need(r>=222 and r in values and loc[r]==c,'actual owned CLEAR')
    if r in ps:i=ps.index(r);need(c==ground and values[r]==(L[i] if pure else ({111+i}|H[i])),'packet erasure operand')
    else:i=r-222;need(pure and c==facets[i] and values[r]==K[i],'retained old pure mode')
    erased.append({'field':r,'chart':c,'input_columns':sorted(values[r])});del values[r];del loc[r]
   else:raise ValueError('opcode')
  need(set(values)==set(range(222)) and all(loc[j]==w['final'][j] for j in values),'final public charts')
  need(all(values[j]=={j} for j in range(111)),'restored X endpoints')
  need(all(values[111+i]==({111+i,i} if i<2 else {111+i}) for i in range(111)),'all222 input/output columns')
  need(counts==expected and all(moves[j]==7 for j in range(222)) and all(moves[p]==8 for p in ps),'complete partial invoice')
  need(extra==int(pure) and peak==(3 if pure else 1),'extra transport and peak')
  need(sorted(arr[0])==([1,8,52,73] if pure else [1,8,73]) and sorted(arr[1])==[0,14,66],'facet arrivals')
  return {'counts':dict(counts),'peak_owned':peak,'extra_upward_MOVEs':extra,'X_facet_arrivals':arr,'outgoing_histories':entries,'nonzero_clear_operands':erased}
 out=replay(w['program']);ops=w['program'];mutants=[]
 # Delete genuine source contributions and restoration, located from operations.
 patterns=[('common_read',lambda o:o[0]=='ADD' and o[1]==(223 if pure else 111) and o[2]==52),('restore_common',lambda o:o[0]=='ADD' and o[1]==52 and o[3]==hub),('exclusive_read',lambda o:o[0]=='ADD' and o[1]==(222 if pure else 111) and o[2]==73),('coordinate_preload',lambda o:o[0]=='ADD' and o[1]==111 and o[2]==1)]
 for name,pred in patterns:
  t=next(t for t,o in enumerate(ops) if pred(o));mutants.append((name,ops[:t]+ops[t+1:]))
 if pure:
  t=next(t for t,o in enumerate(ops) if o[0]=='MOVE' and o[1]==223);mutants.append(('free_nonlocal_copy',ops[:t]+ops[t+1:]))
 for i,p in enumerate(ps):
  indices=[t for t,o in enumerate(ops) if o[0]=='ADD' and o[3]==facets[i] and (o[1]==p or o[2]==p)]
  b=[o[:] for o in ops];x,y=indices[:2];b[x],b[y]=b[y],b[x];mutants.append(('reverse_exchange_'+str(i),b))
 rejected=[]
 for name,bad in mutants:
  try:replay(bad)
  except ValueError as e:rejected.append({'name':name,'rejected':True,'reason':str(e)})
  else:raise ValueError('accepted mutant '+name)
 result={'status':'PASS_INDEPENDENT_JOINT_PARTIAL_WORD','variant':a.variant,'native_sha256':hashlib.sha256(raw).hexdigest(),'word_sha256':hashlib.sha256(packed).hexdigest(),'original_columns':222,'exact_chart_count':len(frames),'nested_chart_pairs':len(pairs),'result':out,'negative_controls':rejected,'scope':'Exact finite scalar logical word and rational chart chronology; identities tensor over characteristic-two fields. Physical all-width compiler/phase interface,109 remaining outputs and complete supplier remain open.'}
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'variant':a.variant,'counts':out['counts'],'peak':out['peak_owned'],'negative_controls':len(rejected)}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','word','output']:p.add_argument('--'+k,type=Path,required=True)
 p.add_argument('--variant',choices=['pure','mixed'],required=True);main(p.parse_args())
