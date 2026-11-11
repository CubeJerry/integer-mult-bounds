"""Freeze a finite modular rejection screen from the exact selected word."""
from pathlib import Path
from fractions import Fraction
from collections import Counter
import gzip,hashlib,json,random,sys
P=Path(sys.argv[2])
b=Path(sys.argv[1]).read_bytes()
pin='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
if hashlib.sha256(b).hexdigest()!=pin:raise ValueError('source pin')
w=json.loads(gzip.decompress(b));h=w['hosted'];p=1000000007
main=sorted(set(w['live'])|{x+112 for x in w['live']}|set(h['X2'])|set(h['Y2']))
mi={r:i for i,r in enumerate(main)}
core=[r for r in range(w['public']+w['owned_fields']) if r not in mi]
ci={r:i for i,r in enumerate(core)};helpers=sum(r<w['public'] for r in core)
tot=Counter();combined=Counter()
for e in w['program']:
 if e[0] in ('ADD','COPY') and ((e[1] in mi)!=(e[2] in mi)):
  k='load' if e[2] in mi else'read';r=e[2] if k=='load' else e[1]
  tot[k,r]+=1;combined[r]+=1
seen=Counter();both=Counter();ops=[]
def qm(x):
 f=Fraction(x)
 return f.numerator%p*pow(f.denominator,-1,p)%p
for event,e in enumerate(w['program']):
 op,r=e[:2];loc=mi[r] if r in mi else ci[r]
 if op=='MOVE':continue
 if op in ('INIT','CLEAR'):
  if r in mi:raise ValueError('main reset')
  ops.append([6,ci[r],0,0,0,1,0,1,0,event]);continue
 if op=='SCALE':ops.append([5 if r in mi else 4,loc,0,qm(e[2]),0,1,0,1,len(w['frames'][e[-1]]),event]);continue
 if op not in ('ADD','COPY'):raise ValueError(op)
 s=e[2];typ=(1 if r in mi else 0)+(2 if ((r in mi)!=(s in mi)) else 0)
 # type0 core-core,1 main-main,2 core<-main,3 main<-core
 if op=='COPY' and r in mi:raise ValueError('main COPY')
 a=b1=0;n=n1=1
 if typ in (2,3):
  k='load' if typ==2 else'read';rr=s if typ==2 else r
  a=seen[k,rr];n=tot[k,rr];b1=both[rr];n1=combined[rr]
  seen[k,rr]+=1;both[rr]+=1
 ops.append([typ,loc,mi[s] if s in mi else ci[s],qm(e[3]),a,n,b1,n1,len(w['frames'][e[-1]]),event])
rng=random.Random(20261111)
aa=[rng.randrange(p) for _ in main];bb=[rng.randrange(p) for _ in main];uu=[rng.randrange(p) for _ in range(helpers)]+[0]*w['owned_fields']
def endpoint(z):
 out=z[:];D=set(h['Dports'])
 for i,x in enumerate(w['live']):
  y=x+112;a=mi[x];b=mi[y]
  if i in D:out[b]=(z[b]+z[a])%p
  else:out[a]=(z[a]-z[b])%p;out[b]=(z[a]+z[b])*pow(2,-1,p)%p
 for x,y in zip(h['X2'],h['Y2']):out[mi[x]]=(z[mi[x]]-z[mi[y]])%p
 return out
header=[len(main),len(core),helpers,len(ops),len(w['program'])]
lines=[' '.join(map(str,header))]
for v in (aa,bb,uu,endpoint(aa),endpoint(bb)):lines.append(' '.join(map(str,v)))
lines.extend(' '.join(map(str,e)) for e in ops)
data=('\n'.join(lines)+'\n').encode();(P/'screen-input.txt').write_bytes(data)
meta={'base_sha':'e54523517d0f03e58352e647c403a5af3e525a57','source_sha256':pin,
      'screen_input_sha256':hashlib.sha256(data).hexdigest(),'prime':p,'seed':20261111,
      'main_roles':main,'core_roles':core,'helpers':helpers,'scalar_events':len(ops),
      'event_types':dict(Counter(e[0] for e in ops))}
(P/'INPUT.json').write_text(json.dumps(meta,indent=2)+'\n')
print({k:v for k,v in meta.items() if k not in ('main_roles','core_roles')})
