"""Apply the inherited monotone-frame obstruction to certified quiet loans.
Reachability grants unlimited caches and unbounded payloads, so cannot certify
feasibility. It can certify source-specific missing endpoint coefficients.
"""
from bisect import bisect_right
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse,gzip,hashlib,json
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
SOURCE='research/shared-wire-split-composition/data/final.json.gz'
def default_source():
 for p in Path(__file__).resolve().parents:
  for b in (p,p/'moonshot'):
   if (b/SOURCE).is_file():return b/SOURCE
 return Path(SOURCE)
def need(c,m):
 if not c:raise ValueError(m)
def basis(rows):
 b={}
 for a in rows:
  while a:
   p=a.bit_length()-1
   if p in b:a^=b[p]
   else:b[p]=a;break
 return b
def contained(rows,b):
 for a in rows:
  while a:
   p=a.bit_length()-1
   if p not in b:return False
   a^=b[p]
 return True
def add(a,b,c):
 for j,v in b.items():
  z=a.get(j,F(0))+c*v
  if z:a[j]=z
  else:a.pop(j,None)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=default_source());ap.add_argument('--output',type=Path);args=ap.parse_args()
 raw=args.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source SHA');w=json.loads(gzip.decompress(raw))
 mains=sorted(set(w['live'])|{r+112 for r in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));ms=set(mains);ix={r:i for i,r in enumerate(mains)}
 bs=[basis(x) for x in w['frames']];cur=w['initial'][:]+[None]*w['owned_fields'];rows=[{r:F(1)} if r in ms else {} for r in range(len(cur))];uses=defaultdict(list);visits=defaultdict(list);mainmoves=0
 for r in mains:visits[r,cur[r]].append(-1)
 for k,e in enumerate(w['program']):
  op,r=e[:2];uses[r].append(k)
  if op in ('ADD','COPY'):
   uses[e[2]].append(k);need(cur[r]==cur[e[2]]==e[4],'source cochart')
   if op=='COPY':need(not rows[r],'zero virtual COPY')
   add(rows[r],rows[e[2]],F(e[3]))
  elif op=='SCALE':rows[r]={j:v*F(e[2]) for j,v in rows[r].items()}
  elif op in ('INIT','CLEAR'):rows[r]={};cur[r]=e[2] if op=='INIT' else None
  elif op=='MOVE':
   a,b=e[2:4];need(cur[r]==a,'MOVE source')
   if r in ms:
    need(len(w['frames'][a])<len(w['frames'][b]) and contained(w['frames'][a],bs[b]),'strict ascending main')
    mainmoves+=1;visits[r,b].append(k)
   cur[r]=b
 final=cur[:];required=[{'output':r,'input':s,'coefficient':str(c),'input_frame':w['initial'][s],'output_frame':final[r]} for r in mains for s,c in sorted(rows[r].items()) if s!=r]
 forbidden=[x for x in required if not contained(w['frames'][x['input_frame']],bs[x['output_frame']])]
 cur=w['initial'][:]+[None]*w['owned_fields'];cohort=defaultdict(set);loans=[]
 for r in mains:cohort[cur[r]].add(r)
 for k,e in enumerate(w['program']):
  op,r=e[:2]
  if op=='MOVE':
   a,b=e[2:4]
   if r not in ms:
    j=bisect_right(uses[r],k);deadline=uses[r][j] if j<len(uses[r]) else len(w['program'])
    for donor in sorted(cohort[a]):
     ts=visits.get((donor,b),[]);z=bisect_right(ts,k)
     if z<len(ts) and ts[z]<deadline:
      need(contained(w['frames'][a],bs[b]),'ascending quiet loan');loans.append({'start':k,'close':ts[z],'helper_next_use':deadline,'helper':r,'donor':donor,'from':a,'to':b})
   if r in ms:cohort[a].remove(r);cohort[b].add(r)
   cur[r]=b
  elif op=='INIT':cur[r]=e[2]
  elif op=='CLEAR':cur[r]=None
 at=defaultdict(list)
 for x in loans:at[x['start']].append(x)
 def reach(with_loans,injection=None):
  cache=[0]*len(w['frames'])
  for r in mains:cache[w['initial'][r]]|=1<<ix[r]
  if injection:cache[injection[1]]|=1<<ix[injection[0]]
  for k,e in enumerate(w['program']):
   if e[0]=='MOVE' and e[1] in ms:cache[e[3]]|=cache[e[2]]
   if with_loans:
    for x in at.get(k,()):cache[x['to']]|=cache[x['from']]
  return cache
 no=reach(False);yes=reach(True)
 for f,bits in enumerate(yes):
  for r in mains:
   if bits>>ix[r]&1:need(contained(w['frames'][w['initial'][r]],bs[f]),'illegal reachable input')
 blocked=[x for x in required if not yes[final[x['output']]]>>ix[x['input']]&1];missing={(x['output'],x['input']) for x in blocked}
 need(all((x['output'],x['input']) in missing for x in forbidden),'geometric subset')
 empty=next(i for i,a in enumerate(w['frames']) if not a);control=forbidden[0];injected=reach(True,(control['input'],empty));need(injected[final[control['output']]]>>ix[control['input']]&1,'nonmonotone escape control')
 result={'status':'PASS_QUIET_LOAN_MONOTONE_SCOPE','source_sha256':PIN,'source_events':len(w['program']),'main_count':len(mains),'source_main_moves':mainmoves,'all_main_moves_strictly_ascending':True,'quiet_loans':len(loans),'all_quiet_loans_ascending':True,'required_off_diagonal_terms':len(required),'geometrically_forbidden_terms':len(forbidden),'optimistic_temporally_blocked_terms':len(blocked),'optimistic_reachable_without_loans':sum(bool(no[final[x['output']]]>>ix[x['input']]&1) for x in required),'optimistic_reachable_with_loans':len(required)-len(blocked),'newly_reachable_terms':[x for x in required if yes[final[x['output']]]>>ix[x['input']]&1 and not no[final[x['output']]]>>ix[x['input']]&1],'forbidden_terms':forbidden,'blocked_terms':blocked,'descent_escape_control':control|{'injected_at_chart':empty,'target_reachable':True},'scope':'Inherited monotone-frame obstruction applied to quiet loans. Necessary reachability only, unlimited caches and unbounded payload per route. 104 blocked terms do not mean 104 extra MOVE jobs. No mixed common/difference payloads or descending difference routes. No new kappa.'}
 need(len(loans)==354 and len(forbidden)==104 and len(required)==208,'pinned source exact census')
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},indent=2))
if __name__=='__main__':main()
