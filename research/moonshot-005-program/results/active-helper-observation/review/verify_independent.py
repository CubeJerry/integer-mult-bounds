#!/usr/bin/env python3
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def add(a,b,c):
 r=a.copy()
 for j,v in b.items():
  t=r.get(j,F(0))+c*v
  if t:r[j]=t
  else:r.pop(j,None)
 return r
def scale(a,c):return {j:v*c for j,v in a.items() if v*c}
def span(a):
 s={0}
 for v in a:s|={x^v for x in tuple(s)}
 return frozenset(s)
def run(a):
 for f,pin in json.loads((a.review/'REVIEWED-FILES.json').read_text()).items():need(sha(a.packet/f)==pin,'frozen '+f)
 path=a.repository/'research/shared-wire-split-composition/data/final.json.gz';need(sha(path)==PIN,'source');w=json.loads(gzip.decompress(path.read_bytes()));P=w['program'];C=list(map(span,w['frames']))
 items=json.loads((a.packet/'OBSERVATIONS.json').read_text())['observations'];events={r['event']:i for i,r in enumerate(items)};need(len(items)==len(events)==31,'31 modules');reads=collections.defaultdict(list);decoded=[{} for _ in items];cut={};charts=[[] for _ in items]
 for i,r in enumerate(items):
  for o in r['historical_decoder']:reads[o['after_event']].append((i,o))
 rows={j:{j:F(1)} for j in range(1480)};loc=dict(enumerate(w['initial']))
 def observe(t):
  for i,o in reads[t]:
   j=o['role'];need(loc[j]==o['chart'],'observation chart');decoded[i]=add(decoded[i],rows[j],F(o['coefficient']));charts[i].append(C[loc[j]])
 observe(-1)
 for k,e in enumerate(P):
  if k in events:
   i=events[k];h=items[i]['helper'];need(e[:2]==['MOVE',h],'source cut');cut[i]={j:v for j,v in rows[h].items() if j<1480};rows[h]=add(rows[h],{1480+i:F(1)},F(1))
  op,j=e[:2]
  if op=='INIT':loc[j]=e[2];rows[j]={}
  elif op=='CLEAR':del loc[j];del rows[j]
  elif op=='MOVE':need(loc[j]==e[2],'native MOVE');loc[j]=e[3]
  elif op=='ADD':rows[j]=add(rows[j],rows[e[2]],F(e[3]))
  elif op=='SCALE':rows[j]=scale(rows[j],F(e[2]))
  elif op=='COPY':need(not rows[j],'31 perturbations preserve COPY');rows[j]=scale(rows[e[2]],F(e[3]))
  observe(k)
 W={j:{i:v for i,v in r.items() if i<1480} for j,r in rows.items() if j<1480};summaries=[]
 for i,r in enumerate(items):
  h={int(j):F(v) for j,v in r['hrow'].items()};need({j:v for j,v in decoded[i].items() if j<1480}==cut[i]==h,'full-input decoder row');beta=decoded[i].get(1480+i,F(0));need(beta==F(r['decoder_sensitivity']) and beta*F(r['gain'])==1,'gain');recovery={}
  for j,v in r['lambda_hub'].items():j=int(j);need(C[w['final'][j]]==C[127],'hub location');recovery=add(recovery,W[j],F(v))
  need(recovery==h,'hub recovery');x,y=r['donor'],r['receiver'];xp=[C[w['initial'][x]]]+[C[e[3]] for e in P if e[0]=='MOVE' and e[1]==x];yp=[C[w['initial'][y]]]+[C[e[3]] for e in P if e[0]=='MOVE' and e[1]==y]
  need(C[r['source_chart']] in xp and all(c in yp for c in charts[i]),'route access');levels=[yp.index(c) for c in charts[i]];ordered=all(p<=q for p,q in zip(levels,levels[1:]));need(ordered==r['strict_receiver_itinerary_order'],'chronology')
  z={j:row[1480+i] for j,row in rows.items() if j<1480 and 1480+i in row};off={j:v for j,v in z.items() if C[w['final'][j]]!=C[127]};need(len(z)==r['public_suffix_support'] and {str(j):str(v) for j,v in off.items()}==r['offhub_suffix_rows'],'response')
  summaries.append({'donor':x,'receiver':y,'gain':r['gain'],'ordered':ordered,'stationary_charts':len(set(charts[i])),'offhub_residual':len(off)})
 selected=next(i for i,r in enumerate(items) if r['donor']==77 and r['receiver']==189);z={j:r[1480+selected] for j,r in rows.items() if j<1480 and 1480+selected in r}
 word=json.loads(gzip.decompress((a.packet/'OBSERVATION-WORD.json.gz').read_bytes()));qm={int(j):v for j,v in word['difference_role_map'].items()};raw=set(qm.values());need(word['public']==1880 and len(raw)==400 and word['owned_fields']==51,'namespace');core=[]
 for e in word['program']:
  if e[1] in raw or e[0] in ('ADD','COPY') and e[2] in raw:continue
  f=e.copy();f[1]=f[1]-400 if f[1]>=1880 else f[1]
  if f[0] in ('ADD','COPY'):f[2]=f[2]-400 if f[2]>=1880 else f[2]
  core.append(f)
 need(core==P,'entire common native in order');expected={k:e for k,e in enumerate(P) if e[0]=='MOVE' and e[1] in qm};res=word['raw_reservations'];need(len(res)==len(expected)==1710 and {r['source_event'] for r in res}==set(expected),'unique raw reservations')
 for r in res:
  e=expected[r['source_event']];need(word['program'][r['physical_event']]==['MOVE',qm[e[1]],e[2],e[3],False],'physical funded route')
 def replay(ops,state=None):
  out={j:{j:F(1)} for j in range(1880)} if state is None else {j:r.copy() for j,r in state[0].items()};pos=dict(enumerate(word['initial'])) if state is None else state[1].copy();counts=collections.Counter();life=peak=0
  for e in ops:
   op,j=e[:2];need(0<=j<1931,'declared role');counts[op]+=1
   if op=='INIT':need(j>=1880 and j not in pos,'fresh owned');pos[j]=e[2];out[j]={};life+=1
   elif op=='CLEAR':need(j>=1880 and pos.get(j)==e[2],'owned CLEAR');del pos[j];del out[j]
   elif op=='MOVE':
    f,g,own=e[2:];need(pos.get(j)==f and type(own)is bool and own==(j>=1880),'typed MOVE');need(C[f]<C[g] or own and C[g]<C[f],'nested MOVE');pos[j]=g
   elif op=='SCALE':need(pos[j]==e[3],'SCALE chart');out[j]=scale(out[j],F(e[2]))
   elif op in ('ADD','COPY'):
    src,c,f=e[2:];need(j!=src and C[pos[j]]==C[pos[src]]==C[f],'cochart scalar operation')
    if op=='COPY':need(not out[j],'actual zero COPY');out[j]=scale(out[src],F(c))
    else:out[j]=add(out[j],out[src],F(c))
   else:raise ValueError('unknown operation')
   peak=max(peak,len(pos)-1880)
  return out,pos,{'instructions':len(ops),'counts':dict(sorted(counts.items())),'owned_lifetimes':life,'peak_owned':peak,'final_owned':len(pos)-1880}
 out,pos,bill=replay(word['program']);delta={qm[77]:F(1),77:F(-2)}
 for j in range(1480):need(out[j]==add(W[j],delta,z.get(j,F(0))) and pos[j]==w['final'][j],'all1480 common outputs')
 for j,r in qm.items():
  want=delta if j==77 else {r:F(1),j:F(-1)}
  if j==189:want=add(want,{qm[77]:F(1),77:F(-1)},F(1))
  need(out[r]==want and pos[r]==w['final'][j],'all400 raw outputs')
 need(bill=={'instructions':73378,'counts':{'ADD':61587,'CLEAR':54,'COPY':1,'INIT':54,'MOVE':8020,'SCALE':3662},'owned_lifetimes':54,'peak_owned':43,'final_owned':0},'full core bill')
 corr=json.loads((a.packet/'HUB-CORRECTIONS.json').read_text());normal,npos,cbill=replay(corr['program'],(out,pos));off={j:v for j,v in z.items() if C[w['final'][j]]!=C[127]}
 need(len(z)==431 and len(off)==60 and len(corr['program'])==372,'exact residual and correction counts')
 for j in range(1480):need(normal[j]==add(W[j],delta,off.get(j,F(0))),'exact partial common repair')
 need(normal[qm[77]]=={qm[77]:F(1),77:F(-1)},'donor restored');need(normal[qm[189]]==out[qm[189]],'receiver preserved')
 need(all(normal[j]!=W[j] for j in off),'all60 offhub residuals are real');need(word['final_recoupling_included'] is False,'400 recouplings still owed')
 # Independent algebraic and inventory controls; no sampled numerical inputs.
 need(add(cut[selected],{953:F(1)},F(8))!=cut[selected],'missing initial term changes source row')
 need(F(items[selected]['gain'])*2*F(items[selected]['decoder_sensitivity'])!=1,'wrong gain')
 duplicate=res+[res[0]];need(len(duplicate)!=len({r['source_event'] for r in duplicate}),'duplicate reservation count')
 return {'status':'PASS_INDEPENDENT_31_OBSERVATIONS_AND_1880_INPUT_CORE','source_sha256':PIN,'reviewed_files_manifest_sha256':sha(a.review/'REVIEWED-FILES.json'),'method':'Fresh combined1480-common/31-perturbation row replay and separate1880-physical-input replay; no author verifier imports; exact common subsequence and raw reservation binding.','source_modules':summaries,'source_gain_histogram':dict(collections.Counter(r['gain'] for r in summaries)),'direct_chronological_modules':sum(r['ordered'] for r in summaries),'physical_input_directions':1880,'core_bill':bill,'raw_reservations_used_once':1710,'common_response_support':len(z),'hub_correction_ADDs':len(corr['program']),'unrepaired_offhub_fields':len(off),'final_recouplings_still_owed':400,'controls':['missing initial -8u953 changes full-input decoder','doubled gain is not normalized','duplicate raw reservation rejected','all60 residual common fields differ from reference'],'scope':'Accept source-specific individual observation modules and literal partial word. Common repair remains incomplete, joint compatibility and all other raw endpoint duties remain open. No new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--review',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(r['status'])
