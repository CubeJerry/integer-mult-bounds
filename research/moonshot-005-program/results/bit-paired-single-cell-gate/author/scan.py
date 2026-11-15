import json,sys
from pathlib import Path
root=Path(__file__).resolve().parent.parent.parent
R=json.loads((root/'programme/research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_text())['native_roots'];w=json.loads((root/'worker-a/paired-flag-source/output/WORD.json').read_text())
D=[[sum(a*b for a,b in zip(x,y))for y in R]for x in R]
def star(F,E):
 if set(F)&E:return None
 ed={}
 for i in range(111):
  if i in E or i in F:continue
  p=tuple(j for j,f in enumerate(F)if D[i][f]==0)
  if len(p)==2:
   if p in ed:return None
   ed[p]=i
 deg=[sum(j in p for p in ed)for j in range(8)]
 if min(deg)<4:return None
 if any(D[ed[p]][ed[q]]==0 for p in ed for q in ed if p<q and set(p)&set(q)):return None
 return {'frame':F,'edges':[{'pair':list(p),'role':i}for p,i in sorted(ed.items())],'degrees':deg}
def find(E,limit=1000000):
 keep=[i for i in range(111)if i not in E];adj={i:sum(1<<j for j in keep if j>i and D[i][j])for i in keep};count=0
 def rec(F,M):
  nonlocal count
  if count>=limit:return
  if len(F)==8:
   count+=1;return star(F,E)
  if M.bit_count()<8-len(F):return
  while M:
   v=(M&-M).bit_length()-1;M&=M-1
   s=rec(F+[v],M&adj[v])
   if s:return s
 return rec([],sum(1<<i for i in keep)),count
out={}
for C in ['A3','A7','A15','A31','A63','L7','A12','A28','A60','A124','A252','L1']:
 c=w['charts'][C]
 if c['kind']=='ann':
  norm=c['rows'];local=[j for j,r in enumerate(R)if all(sum(a*b for a,b in zip(r,n))==0 for n in norm)];axes=[i for i in range(8)if any(n[i]for n in norm)];seen=[i for i,r in enumerate(R)if all(not r[j]or j in axes for j in range(8))]
 else:p=int(C[1:]);local=[p];seen=[i for i in range(111)if D[p][i]==0]
 ans={}
 for kind,E in [('puncture',set(local)),('placement',set(seen))]:
  s,n=find(E);ans[kind]={'deleted':sorted(E),'star':s,'frames_examined':n};print(C,kind,len(E),None if s is None else s['frame'],n,flush=True)
 out[C]=ans
 Path(__file__).with_name('SCAN.json').write_text(json.dumps(out,indent=2)+'\n')
