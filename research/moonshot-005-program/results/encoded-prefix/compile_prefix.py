"""Construct a literal causal changed-main prefix; exact Fraction algebra.

Scratch exploration version. No full native or supplier admission.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json,collections,time
from functools import lru_cache
from pathlib import Path
from fractions import Fraction as F
SOURCE_SHA='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SOURCE_PATH='research/shared-wire-split-composition/data/final.json.gz'

def source_default():
 for parent in Path(__file__).resolve().parents:
  for base in (parent,parent/'moonshot'):
   candidate=base/SOURCE_PATH
   if candidate.is_file():return candidate
 return Path(SOURCE_PATH)

@lru_cache(None)
def root_interval(r):
 scale10=10**15;target=int(r)**199*scale10**200;left,right=0,int(r)*scale10+1
 while right-left>1:
  mid=(left+right)//2
  if mid**200<=target:left=mid
  else:right=mid
 return left,left if left**200==target else left+1

def moment_interval(hist):
 lo=hi=0
 for r,n in hist.items():
  a,b=root_interval(r);lo+=n*a;hi+=n*b
 return F(lo,10**15),F(hi,10**15)

def need(v,msg):
 if not v:raise ValueError(msg)
def add(row,other,c):
 for j,v in other.items():
  z=row.get(j,F(0))+c*v
  if z:row[j]=z
  else:row.pop(j,None)
def scale(row,c):return {j:v*c for j,v in row.items() if v*c}
def combination(target,owners,prows):
 basis={}
 for owner in sorted(owners):
  r=prows[owner].copy();exp={owner:F(1)}
  for p,(v,e) in basis.items():
   c=r.get(p,F(0))
   if c:add(r,v,-c);add(exp,e,-c)
  if r:
   p=min(r);c=r[p];basis[p]=(scale(r,1/c),scale(exp,1/c))
 r=target.copy();answer={}
 for p,(v,e) in basis.items():
  c=r.get(p,F(0))
  if c:add(r,v,-c);add(answer,e,c)
 return None if r else answer

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=source_default());ap.add_argument('--cut',type=int,default=25728);ap.add_argument('--output',type=Path);ap.add_argument('--transcript',type=Path);ap.add_argument('--max-live',type=int);ap.add_argument('--budget-moment');ap.add_argument('--retire',action='store_true');args=ap.parse_args()
 raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==SOURCE_SHA,'source pin');w=json.loads(gzip.decompress(raw));m=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));n=w['public'];public=n+len(m);source_owned=w['owned_fields'];carrier={a:n+i for i,a in enumerate(m)}
 def actual(a):return a if a<n else a+len(m)
 virtual=[{a:F(1)} if a in carrier else {} for a in range(n+source_owned)];current=w['initial'][:]+[None]*source_owned
 # Difference-only observations contain no dirty-helper/common contribution.
 prows={carrier[a]:{a:F(1)} for a in m};pframes={carrier[a]:w['initial'][a] for a in m};observers=collections.defaultdict(set)
 for a in m:observers[w['initial'][a]].add(carrier[a])
 program=[];new_owners=[];deliveries=[];main_parks=[];skipped=[];maxsupport=0;alive_source=set();peak=0;stop=None;actual_cut=args.cut;live_extra=set();free_owners=[];retirements=[];lifetimes=0
 for a in m:program.append(['ADD',carrier[a],actual(a),'-1',w['initial'][a]])
 def emit_copy(row,frame,reason,source_index):
  nonlocal maxsupport,peak,lifetimes
  exp=combination(row,observers[frame],prows);need(exp is not None,('cochart observation unavailable',source_index,reason));t=free_owners.pop() if free_owners else public+source_owned+len(new_owners)
  if t not in new_owners:new_owners.append(t)
  live_extra.add(t);lifetimes+=1;program.append(['INIT',t,frame])
  for s,c in sorted(exp.items()):program.append(['ADD',t,s,str(c),frame])
  prows[t]=row.copy();pframes[t]=frame;observers[frame].add(t);maxsupport=max(maxsupport,len(exp));peak=max(peak,len(live_extra)+len(alive_source));return t,exp
 def retire_unneeded(source_index):
  # Test needed virtual rows, not old representation coefficients.
  for t in sorted(live_extra):
   frame=pframes[t];available=observers[frame]-{t}
   basis={}
   for q in sorted(available):
    r=prows[q].copy()
    for p,v in basis.items():
     if r.get(p):add(r,v,-r[p])
    if r:
     p=min(r);basis[p]=scale(r,1/r[p])
   safe=True
   for a,row in enumerate(virtual):
    if current[a]!=frame or not row:continue
    residual=row.copy()
    for p,v in basis.items():
     if residual.get(p):add(residual,v,-residual[p])
    if residual:safe=False;break
   if safe:
    program.append(['CLEAR',t,frame]);live_extra.remove(t);free_owners.append(t);observers[frame].remove(t);prows.pop(t);pframes.pop(t);retirements.append({'after_event':source_index,'owner':t,'chart':frame})
 for k,e in enumerate(w['program'][:args.cut]):
  op,a=e[:2];phys=actual(a)
  if op=='MOVE':
   adds_owner=a in carrier or bool(virtual[a]) and combination(virtual[a],observers[e[3]],prows) is None
   adds_delivery=a not in carrier and adds_owner
   prospective=collections.Counter(d['rank'] for d in deliveries)
   if adds_delivery:prospective[abs(len(w['frames'][e[2]])-len(w['frames'][e[3]]))]+=1
   lo,hi=moment_interval(prospective)
   if args.max_live is not None and adds_owner and len(live_extra)+len(alive_source)>=args.max_live:
    actual_cut=k;stop={'reason':'owned capacity of this monotone retention rule','event':k,'next_event':e,'current_live':len(live_extra)+len(alive_source),'would_add_delivery':adds_delivery};break
   if args.budget_moment is not None and hi>=F(args.budget_moment):
    actual_cut=k;stop={'reason':'paid moment cap of this monotone retention rule','event':k,'next_event':e,'prospective_moment_interval':[str(lo),str(hi)]};break
  if op=='MOVE':
   src,dst=e[2:4];need(current[a]==src,'source MOVE entry')
   rank=abs(len(w['frames'][src])-len(w['frames'][dst]));need(rank>0,'positive MOVE rank')
   if a in carrier:
    q=carrier[a];need(pframes[q]==src,'main carrier source chart')
    # Snapshot before changing the carrier. All old observation versions survive.
    t,exp=emit_copy(prows[q],src,'park departing main code',k)
    old=prows[q].copy();program.append(['ADD',q,t,'-1',src]);prows[q]={}
    exp2=combination(virtual[a],observers[src]-{q},prows);need(exp2 is not None,'main rebase source')
    for s,c in sorted(exp2.items()):program.append(['ADD',q,s,str(c),src])
    prows[q]=virtual[a].copy();observers[src].remove(q);observers[dst].add(q);pframes[q]=dst
    program.append(['MOVE',q,src,dst,e[4]]);main_parks.append({'event':k,'main':a,'carrier':q,'parked_owner':t,'old_row':[[j,str(c)] for j,c in sorted(old.items())],'new_row':[[j,str(c)] for j,c in sorted(virtual[a].items())],'rebase_support':len(exp2)})
   elif virtual[a]:
    target_exp=combination(virtual[a],observers[dst],prows)
    if target_exp is None:
     t,exp=emit_copy(virtual[a],src,'deliver auxiliary difference',k);program.append(['MOVE',t,src,dst,True]);observers[src].remove(t);observers[dst].add(t);pframes[t]=dst
     deliveries.append({'event':k,'virtual_owner':a,'physical_owner':t,'source_chart':src,'destination_chart':dst,'rank':rank,'row':[[j,str(c)] for j,c in sorted(virtual[a].items())],'expression':[[j,str(c)] for j,c in sorted(exp.items())]})
    else:skipped.append({'event':k,'owner':a,'reason':'already in destination span'})
   else:skipped.append({'event':k,'owner':a,'reason':'zero difference'})
   current[a]=dst;program.append([op,phys,src,dst,e[4]])
  elif op in ('ADD','COPY'):
   b=e[2];c=F(e[3]);frame=e[4];need(current[a]==current[b]==frame,'source scalar cochart')
   # Frame-local closure proves no separate physical update of difference codes.
   if op=='COPY':need(not virtual[a],'virtual COPY zero')
   add(virtual[a],virtual[b],c);program.append([op,phys,actual(b),e[3],frame])
  elif op=='SCALE':
   c=F(e[2]);need(c!=0 and current[a]==e[3],'source invertible scalar');virtual[a]=scale(virtual[a],c);program.append([op,phys,e[2],e[3]])
  elif op=='INIT':
   current[a]=e[2];virtual[a]={};alive_source.add(a);program.append([op,phys,e[2]]);peak=max(peak,len(live_extra)+len(alive_source))
  elif op=='CLEAR':
   current[a]=None;virtual[a]={};alive_source.remove(a);program.append([op,phys,e[2]])
  else:raise ValueError(op)
  if args.retire and op=='MOVE':retire_unneeded(k)
 # Exact current-chart decode at the selected cut, all live virtual roles.
 decode=[]
 for a,row in enumerate(virtual):
  if current[a] is None:continue
  exp=combination(row,observers[current[a]],prows);need(exp is not None,('endpoint virtual decode',a))
  decode.append({'owner':a,'frame':current[a],'expression':[[j,str(c)] for j,c in sorted(exp.items())]})
 counts=dict(collections.Counter(e[0] for e in program));base=dict(collections.Counter(e[0] for e in w['program'][:actual_cut]));hist=dict(sorted(collections.Counter(str(d['rank']) for d in deliveries).items()))
 result={'status':'CONSTRUCTED_EXACT_CAUSAL_PREFIX','source_sha256':SOURCE_SHA,'cut_before_event':actual_cut,'requested_cut':args.cut,'stopped_before':stop,'source_prefix_counts':base,'physical_prefix_counts':counts,'extra_paid_histogram':hist,'extra_delivery_count':len(deliveries),'additional_live_owned':len(live_extra),'extra_owned_labels':len(new_owners),'extra_owned_lifetimes':lifetimes,'retirement_count':len(retirements),'retirements':retirements,'actual_peak_owned':peak,'source_owned_live':len(alive_source),'first_copy_public':n,'main_difference_carriers':len(m),'main_departures':len(main_parks),'max_snapshot_support':maxsupport,'deliveries':deliveries,'main_parks':main_parks,'skipped_auxiliary_moves':skipped,'decoded_virtual_roles_at_cut':len(decode),'scope':'Literal encoded source prefix only. Live sidecars, decoder and future transport/endpoint obligations remain; no new kappa.'}
 transcript={'schema':'moonshot-encoded-prefix-v1','source_sha256':SOURCE_SHA,'source_cut':actual_cut,'source_public':n,'public':public,'source_owned':source_owned,'new_owned':len(new_owners),'carrier_map':{str(a):q for a,q in carrier.items()},'initial':w['initial']+[w['initial'][a] for a in m],'frames':w['frames'],'program':program,'current_decoders':decode,'current_firstcopy_charts':current,'observations':[{ 'owner':a,'frame':pframes[a],'row':[[j,str(c)] for j,c in sorted(prows[a].items())]} for a in sorted(prows)]}
 payload=(json.dumps(transcript,sort_keys=True,separators=(',',':'))+'\n').encode();result['transcript_payload_sha256']=hashlib.sha256(payload).hexdigest();result['transcript_operations']=len(program);result['extra_paid_moment_interval']=[str(x) for x in moment_interval(collections.Counter(d['rank'] for d in deliveries))]
 if args.transcript:args.transcript.write_bytes(gzip.compress(payload,mtime=0))
 s=json.dumps(result,indent=2)+'\n'
 if args.output:args.output.write_text(s)
 print(s)
if __name__=='__main__':main()
