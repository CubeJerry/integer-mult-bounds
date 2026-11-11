import argparse,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(c,m):
 if not c:raise ValueError(m)
def adjoint(w,role,cut,main):
 a={role:F(1)}
 for e in reversed(w['program'][:cut]):
  op,h=e[:2]
  if op in ('INIT','CLEAR'):a.pop(h,None)
  elif op=='SCALE':
   if h in a:a[h]*=F(e[2])
  elif op in ('ADD','COPY'):
   c=a.get(h,F(0))
   if op=='COPY':a.pop(h,None)
   if c:
    s=e[2];z=a.get(s,F(0))+c*F(e[3])
    if z:a[s]=z
    else:a.pop(s,None)
 return {i:v for i,v in sorted(a.items()) if i in main and v}
def combine(*terms):
 a={}
 for c,row in terms:
  for q,v in row.items():
   z=a.get(q,F(0))+c*v
   if z:a[q]=z
   else:a.pop(q,None)
 return a
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args();raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));M=set(w['live'])|{q+112 for q in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2'])
 cases=[(151,30773),(130,30773),(399,30775),(1507,30807),(151,30821),(1481,30824)];rows={f'{r}@{t}':adjoint(w,r,t,M) for r,t in cases}
 a,b,c,o,d,z=[rows[f'{r}@{t}'] for r,t in cases]
 need(a=={55:F(1,2),101:F(-1,2),130:F(1,2)},'three-input entering helper difference')
 need(d==combine((-1,a),(1,b),(-1,c),(1,o)),'chronological local update identity')
 need(z=={q:v/2 for q,v in d.items()},'owned scaling aftercopy')
 need(len(z)==59 and z[55]==F(-1,4),'source authentic59-term payload')
 need(z[7]==F(-1,4) and o.get(7,0)==a.get(7,0)==0,'q7 reduced-interface counterexample')
 uses=[(t,e) for t,e in enumerate(w['program']) if 30820<=t<=30837 and e[0] in ('ADD','COPY') and e[2]==1481]
 need([t for t,e in uses]==[30825,30827,30829,30833,30837],'all five immediate owned external uses')
 all_uses=[(t,e) for t,e in enumerate(w['program']) if 30820<=t<40843 and e[0] in ('ADD','COPY') and e[2]==1481]
 need([t for t,e in all_uses]==[30825,30827,30829,30833,30837,37665,38529,38547,38550,39049,39083,39501,39544],
      'all thirteen complete-lifetime external uses')
 result={'status':'PASS_INDEPENDENT_SOURCE_RELAY_ROWS','source_sha256':PIN,'rows':{k:{str(q):str(v) for q,v in r.items()} for k,r in rows.items()},'support_counts':{k:len(r) for k,r in rows.items()},'immediate_owned_external_uses':[{'source_event':t,'instruction':e} for t,e in uses],
 'all_owned_lifetime_external_uses':[{'source_event':t,'instruction':e} for t,e in all_uses],
 'counterexample_to_rawq_plus_incoming1507_only':{'input':{'7':'1'},'raw_local_q130_q899_and_q55_q101':0,'delta1507':0,'required_delta1481':'-1/4'},'scope':'Exact source expectations for an independent relay review. The q7 counterexample excludes only the specified insufficient boundary observations, not an interface supplying actualdelta130 or delta399.'}
 args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS; source delta1481 has59terms, five downstream reads, and the q7 omission control is nonzero')
