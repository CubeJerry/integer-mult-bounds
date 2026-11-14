#!/usr/bin/env python3
"""Sum actual intermediate-port terms, then certify all-width support separation."""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict,Counter
import json,gzip,hashlib,argparse
HERE=Path(__file__).resolve().parent
PINS={'R0-WORD.json.gz':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','ROUTES.json':'ff3464b51b7240c97294c9a843dace84f17e717db1c7299a85646cd9c70f6c3a'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(name):
 b=(HERE/'source'/name).read_bytes();need(hashlib.sha256(b).hexdigest()==PINS[name],'source pin');return json.loads(gzip.decompress(b)if name.endswith('.gz')else b)
def dot(a,b):return(a&b).bit_count()%2
def rowadd(a,b,c):
 r=dict(a)
 for j,v in b.items():
  r[j]=r.get(j,F(0))+c*v
  if not r[j]:del r[j]
 return r
def matrix(w):
 roles=w['logical_involution']['role_map'];ports=w['logical_involution']['ports'];rows=[{i:F(1)}for i in range(w['public'])]
 for e in w['program']:
  if e[0]=='ADD':rows[e[1]]=rowadd(rows[e[1]],rows[e[2]],F(e[3]))
  else:need(e[0]=='MOVE','owner-free source')
 R={}
 for h in ports:
  y=roles['Y'][str(h)];r=dict(rows[y]);need(r.pop(y)==1,'arbitrary Y');R[h]={j:r[roles['X'][str(j)]]for j in ports if roles['X'][str(j)]in r}
  need(len(R[h])==4 and r=={roles['X'][str(j)]:v for j,v in R[h].items()}and all(abs(v)==F(1,2)for v in R[h].values()),'exact four-term R0 row')
 return R
def apply(cols,x):
 y=0
 while x:
  z=x&-x;y^=cols[z.bit_length()-1];x^=z
 return y
def main(out):
 w=load('R0-WORD.json.gz');rr=load('ROUTES.json');R=matrix(w);rec={(x['stage'],x['port']):x for x in rr['route_records']};q={h:rec[1,h]['normal']for h in R}
 def route(s,h,x):
  r=rec[s,h];es=[1<<(9+8*(s-1)+k)for k in range(8)];z=x&~(511|sum(es));head=x&511
  if dot(head,r['normal']):z^=r['normal']
  for b,e in zip(r['orthogonal_complement'],es):
   if dot(head,b):z^=e
   if x&e:z^=b
  return z
 def term(s,t,h,k,j,z):
  u=route(s,h,z);v=route(t,k,route(s,k,u));dest=route(t,j,v)
  phase=dot(rec[s,h]['input_translation']^rec[s,k]['input_translation'],u)^dot(rec[t,k]['input_translation']^rec[t,j]['input_translation'],v)
  return dest,phase
 def terms(s,t,h,j):
  d=defaultdict(F)
  for k in R[h]:
   if j not in R[k]:continue
   a=[term(s,t,h,k,j,1<<i)for i in range(25)];key=tuple(v[0]for v in a),sum(1<<i for i,v in enumerate(a)if v[1])
   if s!=t:
    for x in [0]+[1<<i for i in range(25)]:
     y=route(s,h,x)^rec[s,h]['input_translation'];y=route(s,k,y^rec[s,k]['input_translation']);y=route(t,k,y)^rec[t,k]['input_translation'];y=route(t,j,y^rec[t,j]['input_translation'])
     need(y==apply(key[0],x^key[1]),'direct spatial recipe agrees including translation')
   d[key]+=R[h][k]*R[k][j]
  return {key:v for key,v in d.items()if v}
 allterms={(h,j):terms(1,2,h,j)for h in R for j in R};allterms={key:d for key,d in allterms.items()if d}
 need(len(allterms)==448 and all(len(d)==4 for d in allterms.values()),'all four-path sums retained exactly')
 cov=[];separators=[]
 candidates=[1<<i for i in range(25)]+[(1<<i)|(1<<j)for i in range(25)for j in range(i)]
 for (h,j),d in sorted(allterms.items()):
  witness=None
  for z in candidates:
   row=defaultdict(F)
   for (cols,phase),a in d.items():row[apply(cols,z)]+=(-1)**dot(phase,z)*a
   bad={v:a for v,a in row.items()if a and dot(q[h],z)!=dot(q[j],v)}
   if bad:witness={'output':h,'input':j,'frequency':z,'remaining_wrong_phase_outputs':{str(v):str(a)for v,a in sorted(bad.items())}};break
  need(witness is not None,'actual summed covariance witness');cov.append(witness)
 def support(key,h,j,x):
  cols,phase=key;b=apply(cols,x^phase);u=apply(cols,q[h]);v=q[j]
  return sorted({b,b^u,b^v,b^u^v})
 for h in sorted(R):
  blocks={j:d for (i,j),d in allterms.items()if i==h};need(len(blocks)==4,'four input-port blocks')
  witness=None
  for x in [0]+[1<<i for i in range(25)]:
   record=[];good=True
   for j,d in sorted(blocks.items()):
    ss=[support(key,h,j,x)for key in d]
    if any(len(s)!=4 for s in ss)or len(set(v for s in ss for v in s))!=16:good=False;break
    record.append({'input_port':j,'term_supports':ss,'term_coefficients':[str(v)for v in d.values()]})
   if good:witness={'output_port':h,'spatial_row':x,'input_blocks':record};break
  need(witness is not None,'disjoint affine supports for every output port');separators.append(witness)
  need(sum(a*a for d in blocks.values()for a in d.values())==1,'whole-row norm for every width')
 # Full same-stage cancellation is the positive control: four paths sum to identity.
 identity=tuple(1<<i for i in range(25)),0
 for h in R:
  for j in R:need(terms(1,1,h,j)==({identity:F(1)}if h==j else{}),'same-stage R_s squared control')
 # Removing any one of the16 paths loses exactly1/16 of row squared norm.
 coefficients=[a for d in blocks.values()for a in d.values()]
 deleted=sum(a*a for a in coefficients[1:]);need(deleted==F(15,16)and deleted!=1,'deleted actual path normalization control')
 # Whole-bank R coefficients occur once. Wrongly tensoring them fails at V2.
 wrong=sum(a**4 for a in coefficients);need(wrong==F(1,16)and wrong!=1,'wrong tensor-of-R coefficient control')
 result={'status':'PASS_ACTUAL_INTERSTAGE_SUM_AND_ALL_WIDTH_SUPPORT_CERTIFICATE','source_pins':PINS,
 'stages':[1,2],'port_count':112,'nonzero_blocks':448,'terms_per_block':4,'covariance_failures':cov,'support_separators':separators,
 'all_width_row_support':'16*4^V for each certified repeated spatial row','all_width_entry_magnitude':'2^(-V-2)',
 'ordinary_add_lower_bound':'L >= 2V+4; fixed ordinary templates are excluded',
 'same_stage_control':'all112x112 blocks equal identity exactly after four-path summation',
 'deleted_path_squared_norm':'15/16','wrong_tensor_R_width2_squared_norm':'1/16',
 'scope':'Retained actual port adapters only. No lower bound for new paid circuits, productive helpers, alternative adapters or redesigned callers. No new kappa.'}
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=HERE/'RESULT.json');main(a.parse_args().out)
