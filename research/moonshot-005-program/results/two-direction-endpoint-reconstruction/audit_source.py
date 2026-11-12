#!/usr/bin/env python3
"""Independent backward-adjoint audit of all1480 pinned native output rows."""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip,hashlib,json,time
from pathlib import Path
PIN="2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883"
def need(x,m):
 if not x:raise ValueError(m)
def axpy(a,b,c):
 for j,v in b.items():
  v=a.get(j,F(0))+c*v
  if v:a[j]=v
  else:a.pop(j,None)
def backward(program, seeds, total):
 a=[{} for _ in range(total)]
 for r,label in seeds.items():a[r][label]=F(1)
 for op in reversed(program):
  k,d=op[:2]
  if k in ("ADD","COPY"):
   axpy(a[op[2]],a[d],F(op[3]))
   if k=="COPY":a[d]={}
  elif k=="SCALE":a[d]={j:F(op[2])*v for j,v in a[d].items()}
  elif k in ("INIT","CLEAR"):a[d]={}
  elif k!="MOVE":raise ValueError(k)
 return a
def main(a):
 start=time.monotonic();b=a.source.read_bytes();need(hashlib.sha256(b).hexdigest()==PIN,"sourcepin");w=json.loads(gzip.decompress(b));n=w["public"];need(n==1480,"source count")
 X=list(w["live"]);D=set(w["hosted"]["Dports"]);M=set(X)|{x+112 for x in X}|set(w["hosted"]["X2"])|set(w["hosted"]["Y2"])
 target={i:{i:F(1)} for i in range(n)}
 for i,x in enumerate(X):
  y=x+112
  target[y]={x:F(1),y:F(1)} if i in D else {x:F(1,2),y:F(1,2)}
  if i not in D:target[x]={x:F(1),y:F(-1)}
 for x,y in zip(w["hosted"]["X2"],w["hosted"]["Y2"]):target[x]={x:F(1),y:F(-1)}
 adj=backward(w["program"],{i:i for i in range(n)},n+w["owned_fields"])
 actual={i:{} for i in range(n)}
 for source,row in enumerate(adj):
  for output,c in row.items():actual[output][source]=c
 need(actual==target,"all1480 native endpoint rows, including helpers, on all public input columns")
 guards=[]
 for event,op in enumerate(w["program"]):
  if op[0]!="COPY":continue
  g=backward(w["program"][:event],{op[1]:0},n+w["owned_fields"])
  need(not any(g),"COPY destination prehistory identically zero")
  guards.append({"event":event,"destination":op[1],"all_public_input_coefficients_zero":True})
 helpers=sorted(set(range(n))-M);need(len(helpers)==1080 and all(actual[r]=={r:F(1)} for r in helpers),"1080 independent helper identities")
 serial={str(r):{str(j):str(c) for j,c in sorted(row.items())} for r,row in sorted(actual.items())}
 raw=(json.dumps(serial,sort_keys=True,separators=(",",":"))+"\n").encode();a.output.mkdir(parents=True,exist_ok=True);(a.output/"SOURCE-ENDPOINTS.json.gz").write_bytes(gzip.compress(raw,mtime=0))
 result={"status":"PASS_FULL1480_SOURCE_ENDPOINTS_AND_COPY_GUARD","source_sha256":PIN,"native_instruction_count":len(w["program"]),"public_input_directions":n,"output_rows":n,"main_rows":len(M),"helper_identity_rows":len(helpers),"coupled_ports":len(X)-len(D),"hosted_forward_shears":len(D),"hosted_reverse_shears":len(w["hosted"]["X2"]),"COPY_guards":guards,"canonical_endpoint_payload_sha256":hashlib.sha256(raw).hexdigest(),"method":"Fresh all-output backward adjoint; COPY guard separately pulled back from exact prefix. No author scientific Python imported.","seconds":time.monotonic()-start,"scope":"Exact normalized finite source map; retained all-column, ownership, compiler, precision/tape and analytic foundations remain."}
 (a.output/"SOURCE-AUDIT.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n");print(json.dumps(result,indent=2))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--source",type=Path,required=True);p.add_argument("--output",type=Path,required=True);main(p.parse_args())

