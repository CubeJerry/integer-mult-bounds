"""Independent literal homogeneous-rail interpretation; no author imports."""
import argparse,gzip,json,hashlib
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,s):
 if not x:raise ValueError(s)
def interpret(word,M,checks=()):
 n=word['public'];N=n+word['owned_fields'];values=[{r:Q(1)} if r in M else {} for r in range(N)];where=word['initial'][:]+[None]*(N-n);masks=[]
 for frame in word['frames']:
  points=[0]
  for g in frame:points += [x^g for x in points]
  need(len(set(points))==2**len(frame),'independent frame');masks.append(sum(1<<x for x in points))
 counts=Counter();hist=Counter();active=peak=life=0;marked={x['physical_before_event']:x for x in checks};checked=[]
 for i,e in enumerate(word['program']):
  if i in marked:
   x=marked[i];a=x['old_physical_owner'];b=x['new_physical_owner'];need(values[a]==values[b] and where[b]==x['destination'],'pre-retirement exact row equality');checked.append(x['event'])
  op,d=e[:2];need(0<=d<N,'holder range');counts[op]+=1
  if op=='INIT':
   need(d>=n and where[d] is None,'INIT');where[d]=e[2];values[d]={};active+=1;life+=1
  elif op=='CLEAR':
   need(d>=n and where[d]==e[2],'CLEAR');where[d]=None;values[d]={};active-=1
  elif op=='MOVE':
   need(type(e[4]) is bool and e[4]==(d>=n) and where[d]==e[2],'typed MOVE');a,b=masks[e[2]],masks[e[3]];up=(a&b)==a and a!=b;down=(a&b)==b and a!=b;need(up or d>=n and down,'nested MOVE');where[d]=e[3];hist[abs(len(word['frames'][e[2]])-len(word['frames'][e[3]]))]+=1
  elif op=='SCALE':
   c=Q(e[2]);need(c and where[d]==e[3],'SCALE');values[d]={k:v*c for k,v in values[d].items()}
  elif op in ('ADD','COPY'):
   s=e[2];c=Q(e[3]);need(0<=s<N and s!=d and c and where[d] is not None and where[d]==where[s]==e[4],'cochart ADD')
   if op=='COPY':need(not values[d],'COPYzero')
   row=values[d].copy()
   for k in set(row)|set(values[s]):
    v=row.get(k,0)+c*values[s].get(k,0)
    if v:row[k]=v
    else:row.pop(k,None)
   values[d]=row
  else:raise ValueError(op)
  peak=max(peak,active)
 need(len(checked)==len(checks),'all rebindings checked')
 return values,where,{'operations':dict(counts),'moves':dict(sorted(hist.items())),'peak_owned':peak,'lifetimes':life,'remaining_owned':active,'checked_rebindings':checked}
def run(source,transcript,author):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));t=json.loads(gzip.decompress(transcript.read_bytes()));M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(set(t['main_roles'])==M and t['frames']==w['frames'] and t['initial']==w['initial'] and t['public']==w['public'],'homogeneous interface');a,af,ab=interpret(w,M);b,bf,bb=interpret(t,M,t['rebindings']);need(a[:1480]==b[:1480] and af[:1480]==bf[:1480],'all1480 public endpoints');need(not bb['remaining_owned'],'final cleanup');delta=Counter(bb['operations']);delta.subtract(ab['operations']);need(delta==Counter({'ADD':9,'MOVE':-4,'INIT':4,'CLEAR':4}),'operation ledger');removed=Counter(ab['moves']);removed.subtract(bb['moves']);need(+removed=={2:3,5:1},'saved routes');need((bb['peak_owned'],bb['lifetimes'])==(44,58),'lifecycle bounds');r=json.loads(author.read_text());need(r['transcript_payload_sha256']==hashlib.sha256(gzip.decompress(transcript.read_bytes())).hexdigest(),'author payload binding')
 need(402 not in M,'negative-control helper partition')
 try:interpret(t,M|{402},t['rebindings'])
 except ValueError as ex:need(str(ex)=='pre-retirement exact row equality','specific helper-input failure')
 else:raise ValueError('wrong independent-helper domain accepted')
 return {'negative_control':'Adding independent entering helper difference402 invalidates the first return equality, confirming the required homogeneous input domain.','status':'PASS_INDEPENDENT_EXACT_CONDITIONAL_ACCUMULATOR_WORD','native_sha256':PIN,'transcript_sha256':hashlib.sha256(transcript.read_bytes()).hexdigest(),'formal_main_inputs':len(M),'public_endpoints_compared':1480,'all_rebinding_equalities':bb['checked_rebindings'],'operation_changes':dict(delta),'removed_moves':dict(+removed),'lifecycle':{'baseline_peak':ab['peak_owned'],'new_peak':bb['peak_owned'],'baseline_lifetimes':ab['lifetimes'],'new_lifetimes':bb['lifetimes'],'final_live_owned':bb['remaining_owned']},'method':'Independent exact rational typed interpreter and GF2-span bit masks; author scientific code not imported or run.','scope':'Complete supplied homogeneous delta rail only; no physical acquisition of helper differences or shared H4 native is proved.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--transcript',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.source,a.transcript,a.author);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
