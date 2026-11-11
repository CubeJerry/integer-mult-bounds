import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def check(x,m):
 if not x:raise ValueError(m)
def span(frame):
 s={0}
 for x in frame:s|={x^v for v in list(s)}
 return frozenset(s)
def add(a,b,c):
 a=a.copy()
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
 return a
def insert(B,row):
 a=row.copy()
 while a:
  p=min(a)
  if p in B:a=add(a,B[p],-a[p])
  else:
   v=a[p];B[p]={j:z/v for j,z in a.items()};return

def main(args):
 p=args.repository/'research/shared-wire-split-composition/data/final.json.gz';raw=p.read_bytes();check(hashlib.sha256(raw).hexdigest()==PIN,'native pin');w=json.loads(gzip.decompress(raw));P=w['program'];C=list(map(span,w['frames']));cert=json.loads((args.package/'CERTIFICATE.json').read_text());check(cert['source_sha256']==PIN,'certificate pin');stations={C[i] for i in cert['stations']};check(len(stations)==220,'station census');X,Y=cert['donor'],cert['receiver'];route={C[w['initial'][Y]]}|{C[e[3]] for e in P if e[0]=='MOVE' and e[1]==Y};check(not route&stations,'receiver/station disjointness')
 rows={j:{j:F(1)} for j in range(w['public'])};obs={};B={}
 def record(t,j,c):
  if C[c] in route:obs[t,j]=(c,rows[j].copy());insert(B,rows[j])
 for j,c in enumerate(w['initial']):record(-1,j,c)
 for t,e in enumerate(P):
  op,j=e[:2]
  if op=='INIT':rows[j]={}
  elif op=='CLEAR':rows.pop(j,None)
  elif op=='ADD':rows[j]=add(rows[j],rows[e[2]],F(e[3]))
  elif op=='COPY':check(not rows[j],'native COPY zero');rows[j]={k:F(e[3])*v for k,v in rows[e[2]].items()}
  elif op=='SCALE':rows[j]={k:F(e[2])*v for k,v in rows[j].items() if F(e[2])*v}
  elif op=='MOVE':record(t,j,e[3])
 check(len(obs)==1065 and len(B)==1056,'complete historical rank');check(rows[Y].get(X)==1,'required q77 endpoint coefficient');RB={}
 def verify_relation(rel,allowed):
  impulse=collections.defaultdict(list);native={};indices={}
  for z in rel:
   t,j,c,v=z['after_event'],z['role'],z['chart'],F(z['coefficient']);check((t,j) in obs and obs[t,j][0]==c,'actual observation');native=add(native,obs[t,j][1],v);impulse[t].append((j,c,v));indices[t,j]=indices.get((t,j),F(0))+v
  check(not native,'zero baseline identity');a={};loc=dict(enumerate(w['final']))
  def station_zero(j):check(j not in loc or C[loc[j]] not in allowed or not a.get(j),'history identity sensitive to a station control')
  for t in reversed(range(len(P))):
   for j,c,v in impulse[t]:check(loc[j]==c,'post-event chart');a=add(a,{j:F(1)},v);station_zero(j)
   e=P[t];op,j=e[:2];changed=[]
   if op=='ADD':s=e[2];a=add(a,{s:F(1)},a.get(j,F(0))*F(e[3]));changed=[s]
   elif op=='COPY':s=e[2];check(s!=j,'distinct COPY');a=add(a,{s:F(1)},a.get(j,F(0))*F(e[3]));a.pop(j,None);changed=[s,j]
   elif op=='SCALE':
    v=a.get(j,F(0))*F(e[2]);a.pop(j,None)
    if v:a[j]=v
    changed=[j]
   elif op=='MOVE':loc[j]=e[2];changed=[j]
   elif op=='CLEAR':loc[j]=e[2];a.pop(j,None);changed=[j]
   elif op=='INIT':loc.pop(j,None);a.pop(j,None)
   for j in changed:station_zero(j)
  for j,c,v in impulse[-1]:check(loc[j]==c,'initial chart');a=add(a,{j:F(1)},v);station_zero(j)
  check(not a,'independent backwards baseline identity');return indices
 for rel in cert['relations']:insert(RB,verify_relation(rel,stations))
 check(len(cert['relations'])==len(RB)==9==len(obs)-len(B),'complete left-kernel basis')
 controls=[];bad=[dict(z) for z in cert['relations'][0]];bad[0]['coefficient']=str(F(bad[0]['coefficient'])+1)
 for name,rel,allowed in [('wrong relation coefficient',bad,stations),('additional q control at chart3',cert['relations'][0],stations|{C[3]})]:
  try:verify_relation(rel,allowed)
  except ValueError as e:controls.append({'mutation':name,'rejection':str(e)})
  else:raise ValueError('negative control accepted')
 out={'status':'PASS_220_STATION_ADDITIVE_HISTORY_CERTIFICATE','source_sha256':PIN,'certificate_sha256':hashlib.sha256((args.package/'CERTIFICATE.json').read_bytes()).hexdigest(),'station_charts':220,'donor':X,'receiver':Y,'observations':len(obs),'native_history_rank':len(B),'independent_complete_relations':len(RB),'relation_term_counts':[len(r) for r in cert['relations']],'all_relations_annihilate_every_station_control_at_every_time':True,'endpoint_neutrality_not_needed':True,'negative_controls':controls,'review_status':'Author certificate; independent review pending','scope':'Additive q-derived controls whose q=0 baseline is the original native common execution. Does not include common-input-dependent replacement, altered outside-station common processing, extra observer charts or new transport. No new kappa.'};args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--package',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
