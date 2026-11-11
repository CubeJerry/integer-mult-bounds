#!/usr/bin/env python3
"""Exact endpoint-only communication obstruction; no search in verification."""
import argparse,bisect,collections,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PRELOAD='ea6d8fb4aed4870dc2394df85de577c2c85a6a2e4e9ab858f64c8e16137131f1'
def need(c,m):
 if not c:raise ValueError(m)
def canon(a):
 B={}
 for x in a:
  for p,y in sorted(B.items(),reverse=True):
   if x>>p&1:x^=y
  if x:
   p=x.bit_length()-1
   for q,y in list(B.items()):
    if y>>p&1:B[q]=y^x
   B[p]=x
 return tuple(y for p,y in sorted(B.items()))
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def endpoints(w,M):
 rows=[{i:F(1)} if i in M else {} for i in range(w['public']+w['owned_fields'])]
 for e in w['program']:
  if e[0]=='ADD':add(rows[e[1]],rows[e[2]],F(e[3]))
  elif e[0]=='SCALE':rows[e[1]]={j:F(e[2])*a for j,a in rows[e[1]].items()}
  elif e[0]=='COPY':need(not rows[e[1]],'source COPY zero');rows[e[1]]=rows[e[2]].copy()
  elif e[0] in ('INIT','CLEAR'):rows[e[1]]={}
 return rows

def quiet(w,M,C):
 P=w['program'];end=len(P);touch=collections.defaultdict(list);visits={};state={i:(-1,w['initial'][i]) for i in M}
 for k,e in enumerate(P):
  touch[e[1]].append(k)
  if e[0] in ('ADD','COPY'):touch[e[2]].append(k)
  if e[0]=='MOVE' and e[1] in M:
   i=e[1];a,f=state[i];need(f==e[2] and (i,C[f]) not in visits,'single monotone main visit');visits[i,C[f]]=(a,k);state[i]=(k,e[3])
 for i,(a,f) in state.items():visits[i,C[f]]=(a,end)
 out=[]
 for k,e in enumerate(P):
  if e[0]!='MOVE' or e[1] in M:continue
  h,s,d=e[1:4];at=bisect.bisect_right(touch[h],k);deadline=touch[h][at] if at<len(touch[h]) else end
  for q in sorted(M):
   a,b=visits.get((q,C[s])),visits.get((q,C[d]))
   if a and b and a[0]<k<a[1] and k<b[0]<deadline:out.append({'event':k,'close':b[0],'helper':h,'donor':q,'source':s,'target':d,'next_touch':deadline})
 return out

def propagation(w,M,C,loans,all_helpers=False,preloads=False):
 B=collections.defaultdict(int)
 for i in M:B[C[w['initial'][i]]]|=1<<i
 if preloads:
  for d in (470,431,394,520):B[C[d]]|=B[C[3]]
 extra=collections.defaultdict(set)
 for q in loans:extra[q['event']].add((q['source'],q['target']))
 for k,e in enumerate(w['program']):
  if e[0]=='MOVE' and (all_helpers or e[1] in M or e[4]):B[C[e[3]]]|=B[C[e[2]]]
  for s,d in extra[k]:B[C[d]]|=B[C[s]]
 return B

def check_witness(w,C,rows,B,pairs):
 inputs=[q['input'] for q in pairs];outputs=[q['output'] for q in pairs];need(len(inputs)==len(set(inputs))==len(set(outputs))==46,'distinct46pairs');K=sum(1<<j for j in inputs);det=F(1)
 for q in pairs:
  i,j=q['output'],q['input'];need(w['final'][i]==q['target_chart'],'actual target chart');need(not (B[C[w['final'][i]]]&K),'all chosen inputs absent at each chosen sink');need({k:v for k,v in rows[i].items() if k in inputs}=={j:F(q['coefficient'])} and F(q['coefficient'])!=0,'diagonal nonsingular endpoint restriction');need(len(C[w['initial'][j]])==1,'nonempty initial input');det*=F(q['coefficient'])
 need(det==F(1,8),'exact diagonal determinant');return K,det

def run(source,certificate,preload_result):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));cert=json.loads(certificate.read_text());need(cert['source_sha256']==PIN,'certificate pin');pr=preload_result.read_bytes();need(hashlib.sha256(pr).hexdigest()==PRELOAD,'preload pin');pre=json.loads(pr);M=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);C=[canon(f) for f in w['frames']];rows=endpoints(w,M);loans=quiet(w,M,C);need(len(loans)==354 and len({q['event'] for q in loans})==141,'complete quiet census');need(len(set(C))==1094,'equal-span quotient');cases={};pairs=cert['witness_pairs'];K=None
 for name,L,pregrant in [('main_owned',[],False),('with_quiet',loans,False),('with_quiet_and_entry_grants',loans,True)]:
  B=propagation(w,M,C,L,preloads=pregrant);missing=[{'output':i,'input':j,'coefficient':str(c),'target_chart':w['final'][i]} for i in sorted(M) for j,c in sorted(rows[i].items()) if not(B[C[w['final'][i]]]>>j&1)];need(len(missing)==102,'exact missing endpoint coefficients');K,d=check_witness(w,C,rows,B,pairs);cases[name]={'missing_coefficients':len(missing),'missing':missing,'selected_endpoint_rank':46,'selected_determinant':str(d),'selected_sink_funded_projection_ranks':[0]*46}
 for q in pre['preloads']:need(all(not(K>>j&1) for j,c in q['row'] if F(c)),'all four existing preloads vanish on selected inputs')
 # Controls remove premises or corrupt the actual witness.
 full=propagation(w,M,C,loans,all_helpers=True);need(all(full[C[w['final'][i]]]>>j&1 for i in M for j in rows[i]),'all-source-route positive escape');controls=[]
 for name,bad,info in [('wrong_endpoint_coefficient',[dict(q) for q in pairs],B),('all_helper_q_routes',[dict(q) for q in pairs],full),('free_global_input_rereads',[dict(q) for q in pairs],collections.defaultdict(lambda:sum(1<<i for i in M)))]:
  if name=='wrong_endpoint_coefficient':bad[0]['coefficient']='3'
  try:check_witness(w,C,rows,info,bad)
  except ValueError as e:controls.append({'mutation':name,'rejection':str(e)})
  else:raise ValueError('control accepted '+name)
 # This rank bound is tight for the selected witness after granting46 global fields.
 need(all(F(q['coefficient']) for q in pairs),'46 global basis fields cover selected witness')
 loan_bytes=json.dumps(loans,sort_keys=True,separators=(',',':')).encode()
 return {'status':'PASS_ENDPOINT_ONLY_46_GLOBAL_FIELD_OBSTRUCTION','source_sha256':PIN,'certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),'preload_result_sha256':PRELOAD,'mains':len(M),'funded_main_arrivals':sum(e[0]=='MOVE' and e[1] in M for e in w['program']),'funded_owned_arrivals':sum(e[0]=='MOVE' and e[4] for e in w['program']),'quiet_windows':len(loans),'unique_quiet_starts':len({q['event'] for q in loans}),'quiet_window_sha256':hashlib.sha256(loan_bytes).hexdigest(),'canonical_chart_spans':len(set(C)),'selected_input_roles':[q['input'] for q in pairs],'selected_output_roles':[q['output'] for q in pairs],'cases':cases,'existing_preloads_projection_rank':0,'additional_field_lower_bound':46,'new_q_informative_transmissions_needed_if_at_most3_new_paid_arrivals':43,'negative_controls':controls,'scope':'Endpoint-only linear q information: all main/all47owned and simultaneous quiet loans granted, plus existing pure-entry preloads. Other q-informative helper traffic, changed calendars and joint recoding are outside.46 is a certified lower bound, not the optimum or an unconditional global MOVE floor.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,default=Path(__file__).with_name('CERTIFICATE.json'));p.add_argument('--preload-result',type=Path,required=True);p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.source,a.certificate,a.preload_result);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in r.items() if k!='cases'},indent=2,sort_keys=True))
