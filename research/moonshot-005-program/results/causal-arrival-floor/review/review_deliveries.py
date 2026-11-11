#!/usr/bin/env python3
"""Independent exact replay of the frozen-main causal delivery lower bound."""
from __future__ import annotations
import argparse,gzip,hashlib,json,math,platform
from pathlib import Path
from collections import defaultdict,Counter
from fractions import Fraction
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
RELATIVE_SOURCE='research/shared-wire-split-composition/data/final.json.gz'
def default_source():
 for base in Path(__file__).resolve().parents:
  for candidate in (base/RELATIVE_SOURCE,base/'moonshot'/RELATIVE_SOURCE):
   if candidate.is_file():return candidate
 return Path(RELATIVE_SOURCE)
def require(p,msg):
 if not p:raise ValueError(msg)
def primitive(row):
 if not row:return {}
 den=1
 for v in row.values():den=math.lcm(den,v.denominator)
 out={k:int(v*den) for k,v in row.items() if v}
 d=0
 for v in out.values():d=math.gcd(d,abs(v))
 s=1 if out[max(out)]>0 else -1
 return {k:v//d*s for k,v in out.items()}
def residual(row,basis):
 out=primitive(row)
 while out:
  pivot=max(out)
  if pivot not in basis:return out
  a=out[pivot];b=basis[pivot];c=b[pivot]
  keys=set(out)|set(b)
  out=primitive({j:Fraction(c*out.get(j,0)-a*b.get(j,0)) for j in keys if c*out.get(j,0)-a*b.get(j,0)})
 return out
def add_basis(row,basis):
 out=residual(row,basis)
 if not out:return False
 basis[max(out)]=out;return True
def frame_span(frame):
 result={0}
 for a in frame:result|={b^a for b in result}
 return frozenset(result)
def closure(vectors):
 out={0}
 for a in vectors:out|={b^a for b in out}
 return frozenset(out)
def potential_controls():
 subspaces={closure([i for i in range(1,8) if mask>>(i-1)&1]) for mask in range(128)}
 n_paid=n_free=n_demand=0
 for G in subspaces:
  for A in subspaces:
   if not G<=A:continue
   p0=(len(A).bit_length()-len(G).bit_length())
   for v in range(8):
    A1=closure(list(A)+[v]);G1=closure(list(G)+[v])
    p_paid=len(A1).bit_length()-len(G).bit_length()
    require(0<=p_paid-p0<=1,'paid-arrival potential');n_paid+=1
    p_free=len(A1).bit_length()-len(G1).bit_length()
    require(p_free<=p0,'shared free-arrival potential');n_free+=1
    if v in A and v not in G:
     require(len(A).bit_length()-len(G1).bit_length()==p0-1,'innovation spends one potential');n_demand+=1
 # A demand required before a later free copy still costs one; final rank alone misses it.
 B={};require(add_basis({0:Fraction(1)},B),'early demand');require(not add_basis({0:Fraction(1)},B),'later free does not refund delivery')
 # Duplicate/scaled demands do not constitute fresh information.
 require(not add_basis({0:Fraction(7)},B),'redundant scaled demand')
 # Equal data in another chart cannot be used without a transport.
 charts={0:{},1:{}};add_basis({0:Fraction(1)},charts[0]);require(bool(residual({0:Fraction(1)},charts[1])),'cross-chart alias rejected')
 # A temporarily repurposed already paid main MOVE is an excluded escape.
 d,e=Fraction(3),Fraction(5);m=d;peer=d;m+=e
 carried=m;side=carried-peer;m-=side
 require(m==d and side==e and carried!=d,'nonliteral main-MOVE escape control')
 return {'subspaces_F2_3':len(subspaces),'paid_cases':n_paid,'free_cases':n_free,'innovation_cases':n_demand,'nonliteral_main_payload_escape':{'literal_payload':'3','actual_payload':'8','restored_main':'3','extra_delivered_row':'5','extra_MOVEs':0}}
def run(source):
 raw=source.read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'immutable source pin');require(hashlib.sha256(raw+b'!').hexdigest()!=PIN,'source-corruption control');w=json.loads(gzip.decompress(raw))
 frames=list(map(frame_span,w['frames']));require(all(len(s)==1<<len(f) for s,f in zip(frames,w['frames'])),'frame basis independence');require(len(set(frames))==1094,'all frame aliases enumerated'); canonical={i:frames.index(s) for i,s in enumerate(frames)}
 mains=set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);require(len(mains)==400,'main inventory')
 rows=[{} for _ in range(w['public']+w['owned_fields'])]
 for r in mains:rows[r]={r:Fraction(1)}
 current=list(w['initial'])+[None]*w['owned_fields'];basis=defaultdict(dict)
 for r in sorted(mains):add_basis(rows[r],basis[canonical[current[r]]])
 innov=[];by_chart=Counter();free_innov=0;main_moves=0;aux_moves=0;owned_moves=0;nonzero_coeff=0;demand_count=0;copy_count=0
 coefficients={}
 for index,e in enumerate(w['program']):
  op,d=e[:2]
  if op=='INIT':require(current[d] is None,'INIT fresh owner');current[d]=e[2];rows[d]={}
  elif op=='CLEAR':require(current[d]==e[2],'CLEAR chart');current[d]=None;rows[d]={}
  elif op=='MOVE':
   require(current[d]==e[2],'MOVE source chart');current[d]=e[3]
   if d in mains:
    main_moves+=1;free_innov+=add_basis(rows[d],basis[canonical[e[3]]])
   else:aux_moves+=1;owned_moves+=d>=w['public']
  elif op=='SCALE':
   require(current[d]==e[3],'SCALE chart');c=coefficients.setdefault(e[2],Fraction(e[2]));require(c,'nonzero SCALE');rows[d]={j:v*c for j,v in rows[d].items()}
  elif op in ('ADD','COPY'):
   s=e[2];c=coefficients.setdefault(e[3],Fraction(e[3]));require(c,'nonzero source coefficient');nonzero_coeff+=1
   require(current[d]==current[s]==e[4],'ADD source/destination cochart');require(d!=s,'distinct source/destination')
   if op=='COPY':require(not rows[d],'COPY zero homogeneous target');copy_count+=1
   if d in mains and s not in mains:
    demand_count+=1
    if add_basis(rows[s],basis[canonical[e[4]]]):innov.append(index);by_chart[canonical[e[4]]]+=1
   for j,v in rows[s].items():
    z=rows[d].get(j,Fraction(0))+c*v
    if z:rows[d][j]=z
    else:rows[d].pop(j,None)
   if d in mains:require(not residual(rows[d],basis[canonical[e[4]]]),'post-event literal main difference must be reference-known')
  else:raise ValueError('unknown opcode '+op)
 require(current[:w['public']]==w['final'],'final charts');require(not any(x is not None for x in current[w['public']:]),'owned owners retired')
 require((len(innov),main_moves,aux_moves,owned_moves)==(984,1710,4600,47),'source census')
 return {'status':'PASS_INDEPENDENT_FROZEN_MAIN_DELIVERY_REVIEW','source_sha256':PIN,'source_events':len(w['program']),'method':'exact Fraction source rows; primitive-integer row basis with maximum pivots; no author code imported','innovations':len(innov),'free_main_innovations':free_innov,'main_moves':main_moves,'auxiliary_moves':aux_moves,'owned_moves':owned_moves,'demand_count':demand_count,'nonzero_add_coefficients':nonzero_coeff,'COPY_zero_checks':copy_count,'events':innov,'by_chart':dict(sorted(by_chart.items())),'controls':potential_controls(),'python':platform.python_version(),'scope':'Exact finite-source invariant for frozen literal main-prefix rows; altered main encodings excluded; no new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=default_source());p.add_argument('--output',type=Path);p.add_argument('--author-certificate',type=Path);a=p.parse_args();r=run(a.source)
 if a.author_certificate:
  raw=a.author_certificate.read_bytes();cert=json.loads(raw)
  require(cert['source_sha256']==PIN,'author source pin')
  require([x[0] for x in cert['records']]==r['events'],'all author innovation events')
  require(cert['by_chart']=={str(k):v for k,v in r['by_chart'].items()},'all author chart counts')
  require(cert['free_main_innovations']==r['free_main_innovations'],'author free count')
  r['author_certificate_sha256']=hashlib.sha256(raw).hexdigest();r['all_author_records_match']=True
 s=json.dumps(r,indent=2)+'\n'
 if a.output:a.output.write_text(s)
 print(json.dumps({k:v for k,v in r.items() if k not in ('events','by_chart')},indent=2))
