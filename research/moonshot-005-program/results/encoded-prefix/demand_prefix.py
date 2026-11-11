"""Literal prefix realizing main demands while retaining pending input information."""
from __future__ import annotations
import argparse,gzip,hashlib,json,collections
from pathlib import Path
from fractions import Fraction as F
from demand_graph import build,load_source,source_default,need,PIN

def construct(w,cut):
 g=build(w,cut);n=w['public'];m=g['mains'];np=n+len(m);ns=w['owned_fields'];keep=set(g['kept_ids']);nodes=g['nodes'];carriers={r:n+i for i,r in enumerate(m)};holder={i:carriers[r] for i,r in enumerate(m)};carrier_node={r:i for i,r in enumerate(m)};physical_frames={carriers[r]:w['initial'][r] for r in m};ops=[['ADD',carriers[r],r,'-1',w['initial'][r]] for r in m];owned=[];deliveries=[];parks=[];node_by_event={node['source_event']:node for node in nodes if node['kind'] in ('aux','main') and node['id'] in keep}
 def actual(r):return r if r<n else r+len(m)
 def init(frame):
  owner=np+ns+len(owned);owned.append(owner);ops.append(['INIT',owner,frame]);physical_frames[owner]=frame;return owner
 def materialize(dst,node):
  frame=node['source_chart']
  for p,c in node['parents']:
   src=holder[p];need(physical_frames[src]==frame and src!=dst,'current stable DAG operand');ops.append(['ADD',dst,src,c,frame])
 for k,e in enumerate(w['program'][:cut]):
  op,r=e[:2]
  if op=='MOVE':
   f,h=e[2:4];node=node_by_event.get(k)
   if r in carriers:
    need(node is not None and node['kind']=='main','every main departure is demanded');q=carriers[r];need(physical_frames[q]==f,'main carrier chart');oldnode=carrier_node[r];t=init(f);ops.append(['ADD',t,q,'1',f]);holder[oldnode]=t;ops.append(['ADD',q,t,'-1',f]);materialize(q,node);ops.append(['MOVE',q,f,h,False]);physical_frames[q]=h;holder[node['id']]=q;carrier_node[r]=node['id'];parks.append({'event':k,'owner':t,'main':r,'retained_node':oldnode})
   elif node is not None:
    t=init(f);materialize(t,node);ops.append(['MOVE',t,f,h,True]);physical_frames[t]=h;holder[node['id']]=t;deliveries.append({'event':k,'owner':t,'virtual_owner':r,'rank':node['rank']})
   ops.append([op,actual(r),f,h,e[4]])
  elif op in ('ADD','COPY'):ops.append([op,actual(r),actual(e[2]),e[3],e[4]])
  elif op=='SCALE':ops.append([op,actual(r),e[2],e[3]])
  elif op in ('INIT','CLEAR'):ops.append([op,actual(r),e[2]])
  else:raise ValueError(op)
 decoders=[]
 for ident in g['output_ids']:
  node=nodes[ident];expr=[]
  for p,c in node['parents']:
   q=holder[p];need(physical_frames[q]==node['frame'],'boundary demand current chart');expr.append([q,c])
  decoders.append({'owner':node['virtual_owner'],'frame':node['frame'],'expression':expr})
 inputs=[]
 for i,r in enumerate(m):
  q=holder[i];need(physical_frames[q]==w['initial'][r],'retained input q chart');inputs.append({'main_input':r,'holder':q,'frame':physical_frames[q]})
 transcript={'schema':'moonshot-main-demand-prefix-v1','source_sha256':PIN,'source_cut':cut,'source_public':n,'public':np,'source_owned':ns,'new_owned':len(owned),'carrier_map':{str(r):q for r,q in carriers.items()},'initial':w['initial']+[w['initial'][r] for r in m],'frames':w['frames'],'program':ops,'current_decoders':decoders,'current_firstcopy_charts':g['source_current_charts'],'retained_input_differences':inputs,'deliveries':deliveries,'parks':parks,'contract':'All first-copy roles and 400 second-copy current main values are represented; every original q input remains physically retained. No all-live second-helper cochart decoder is claimed.'}
 payload=(json.dumps(transcript,sort_keys=True,separators=(',',':'))+'\n').encode();result={'status':'CONSTRUCTED_MAIN_DEMAND_PREFIX','source_sha256':PIN,'cut':cut,'source_prefix_counts':dict(collections.Counter(e[0] for e in w['program'][:cut])),'physical_prefix_counts':dict(collections.Counter(e[0] for e in ops)),'physical_events':len(ops),'extra_paid_histogram':dict(sorted(collections.Counter(d['rank'] for d in deliveries).items())),'live_owned':len(owned),'deliveries':deliveries,'main_parks':parks,'main_decoders':len(decoders),'retained_input_differences':len(inputs),'transcript_payload_sha256':hashlib.sha256(payload).hexdigest(),'scope':transcript['contract']+' Partial prefix only; deferred demands and complete cost remain open.'}
 return transcript,payload,result

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=source_default());ap.add_argument('--cut',type=int,default=25728);ap.add_argument('--transcript',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args();t,payload,r=construct(load_source(a.source),a.cut)
 if a.transcript:a.transcript.write_bytes(gzip.compress(payload,mtime=0))
 s=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(s)
if __name__=='__main__':main()
