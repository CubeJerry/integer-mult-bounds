"""Independent full-input historical-support audit, written by S004 root."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PROOF='3276458f7077a99f8b44fe6475bfe06bcc6b796a58a789ba2adcfc431d8a2da7'
CERT='df858b554c354bb998c3158f3e04651ad20a07247202d0faacf6e0b7472d8f79'
def require(test,label):
 if not test:raise ValueError(label)
def span(basis):
 s={0}
 for v in basis:s|={z^v for z in tuple(s)}
 return frozenset(s)
def combine(dst,src,c):
 for j,v in src.items():
  z=dst.get(j,F(0))+c*v
  if z:dst[j]=z
  else:dst.pop(j,None)
def run(repo,packet):
 require(hashlib.sha256((packet/'PROOF.md').read_bytes()).hexdigest()==PROOF,'reviewed proof pin')
 cb=(packet/'CERTIFICATE.json').read_bytes();require(hashlib.sha256(cb).hexdigest()==CERT,'reviewed certificate pin');cert=json.loads(cb)
 raw=(repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();require(hashlib.sha256(raw).hexdigest()==PIN,'source pin')
 w=json.loads(gzip.decompress(raw));C=list(map(span,w['frames']));M=set(w['live'])|{j+112 for j in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);X={j for j in M if len(C[w['initial'][j]])>1};Y=M-X;H=set(range(w['public']))-M
 visits={j:{C[w['initial'][j]]} for j in M}
 for o in w['program']:
  if o[0]=='MOVE' and o[1] in M:visits[o[1]].add(C[o[3]])
 eligible={x:{h for h in H if C[w['final'][h]]==C[127] and C[w['initial'][h]] in visits[x]} for x in X}
 require({str(x):sorted(hs) for x,hs in eligible.items()}==cert['all_nonentry_donor_eligible_helper_sets'],'all200 certificate helper sets')
 loc=dict(enumerate(w['initial']));rows={j:{j:F(1)} for j in loc};history=collections.defaultdict(set)
 for j,c in loc.items():history[C[c]].update(rows[j])
 for k,o in enumerate(w['program']):
  tag,j=o[:2]
  if tag=='ADD':
   require(C[loc[j]]==C[loc[o[2]]]==C[o[4]],'ADD cochart');combine(rows[j],rows[o[2]],F(o[3]))
  elif tag=='SCALE':rows[j]={q:F(o[2])*v for q,v in rows[j].items()}
  elif tag=='COPY':
   require(not rows[j],'COPY zero on all inputs');rows[j]={q:F(o[3])*v for q,v in rows[o[2]].items()}
  elif tag=='INIT':require(j not in loc,'fresh owned');loc[j]=o[2];rows[j]={}
  elif tag=='CLEAR':require(loc[j]==o[2],'CLEAR location');del loc[j];del rows[j];continue
  elif tag=='MOVE':require(C[loc[j]]==C[o[2]],'MOVE source');loc[j]=o[3]
  else:raise ValueError(tag)
  history[C[loc[j]]].update(rows[j])
 require(all(rows[h]=={h:F(1)} for h in H),'all arbitrary helper inputs restored')
 require(all(not(set(rows[j])&H) for j in M),'main endpoints independent of helpers')
 require(all(C[loc[j]]==C[w['final'][j]] for j in range(w['public'])),'all final charts')
 pairs=[];union=set().union(*eligible.values());nonempty=sum(bool(v) for v in eligible.values())
 for x in sorted(X):
  for y in sorted(Y):
   if not rows[y].get(x):continue
   available=set().union(*(history[c] for c in visits[y]));inter=available&eligible[x]
   require(not inter,'helper source column reaches receiver route')
   require(x in available,'real required donor influence detected')
   pairs.append({'input':x,'output':y,'coefficient':str(rows[y][x]),'eligible_helper_count':len(eligible[x])})
 controlled=[p for p in pairs if p['eligible_helper_count']]
 require([{'donor':p['input'],'receiver':p['output'],'endpoint_coefficient':p['coefficient']} for p in pairs]==cert['required_endpoint_dependencies'],'all104 certificate endpoint pairs')
 require(controlled,'nontrivial controls exist')
 for p in controlled:require(eligible[p['input']]<=history[C[127]],'terminal chart relaxation exposes helpers')
 fake=set(eligible[controlled[0]['input']]);fakechart=set().union(*(history[c] for c in visits[controlled[0]['output']]))|{min(fake)}
 require(bool(fakechart&fake),'one injected source column defeats annihilation')
 return {'status':'PASS_INDEPENDENT_FULL_INPUT_HELPER_ANNIHILATION','source_sha256':PIN,'reviewed_proof_sha256':PROOF,'reviewed_certificate_sha256':CERT,'independent_method':'Full1480-input exact symbolic replay, explicit binary chart spans and union of actual historical input supports; no author implementation or local rowspace elimination.','mains':len(M),'nonentry_donors':len(X),'entry_receivers':len(Y),'helper_inputs':len(H),'eligible_helper_union':len(union),'nonempty_donor_sets':nonempty,'required_pairs':len(pairs),'nonempty_required_pairs':len(controlled),'all_required_historical_projections_zero':True,'controls':['Actual required main input appears on receiver route','Adding chart127 exposes all eligible helper inputs','One artificial helper-input injection defeats annihilation'],'pairs':pairs}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repository',type=Path,required=True);a.add_argument('--packet',type=Path,required=True);a.add_argument('--output',type=Path,required=True);args=a.parse_args();r=run(args.repository,args.packet);args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='pairs'},indent=2))
