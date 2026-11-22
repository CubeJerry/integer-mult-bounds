"""Exploratory exact cut screen for a price-preserving changed deletion family."""
from pathlib import Path
from itertools import combinations_with_replacement
from collections import defaultdict,Counter,deque
import importlib.util,json,sys,time
HERE=Path(__file__).resolve().parent;R=HERE.parent
src=R/'complex-native-funded-donor-cuts/inputs/7833-construction.py';spec=importlib.util.spec_from_file_location('native',src);S=importlib.util.module_from_spec(spec);spec.loader.exec_module(S);g=S.compensated(S.load_word(src.with_name('DOUBLE-CANDIDATE.json.gz')),True)
def span(f):
 a={0}
 for v in f:a|={x^v for x in a}
 return tuple(sorted(a))
sp=sorted({span(f)for f in g.frames});sid={s:i for i,s in enumerate(sp)};canon={c:sid[span(f)]for c,f in enumerate(g.frames)};N=len(sp);rep={v:min(c for c,w in canon.items()if w==v)for v in range(N)}
routes={e:(canon[a],canon[b])for e,(a,b)in g.routes.items()}
BASE=R/'complex-paid-export-s031-coupled-repair'
base=json.loads((BASE/'endpoint-screen/BASE-CUTS.json').read_text())['cuts']
new=json.loads((R/'complex-source-hub-s032/CUTS.json').read_text())['cuts']
for c in new:
 A={canon[u]for u in c['raw_charts']}
 base.append({'id':'s032-'+c['id'],'source_axes':c['input_axes'],'terminal_slots':c['terminal_slots'],'rank':c['rank'],'blocked_occurrences':[e for e,(u,v)in routes.items()if u in A and v not in A]})
V=S.all_public_rows(g)
for cut in base:
 n=len(cut['source_axes']);assert n==len(cut['terminal_slots'])==cut['rank']
 for i,e in enumerate(cut['terminal_slots']):
  den,row=V[e]
  for j,a in enumerate(cut['source_axes']):assert bool(row.get(a,0))==(i==j)
retire=int(sys.argv[1]);D={86,97232,97241,97320,97323,99064,retire};assert retire in[43,89777,96513,96404]
assert S.Counter(g.grade(g.routes[e])for e in D)=={3:1,4:5,5:1}
initial=[];reaches=[];bounds=[];capacities=[]
for cut in base:
 blocked=set(cut['blocked_occurrences'])|D
 reach=[1<<u for u in range(N)]
 for e,(u,v)in routes.items():
  if e not in blocked:reach[u]|=1<<v
 for k in range(N):
  bit,row=1<<k,reach[k]
  for u in range(N):
   if reach[u]&bit:reach[u]|=row
 A=0
 for j in cut['source_axes']:A|=reach[canon[g.inputs[~j]]]
 assert all(not(A>>canon[g.terminals[e]]&1)for e in cut['terminal_slots'])
 outgoing=[e for e,(u,v)in routes.items()if e not in D and A>>u&1 and not(A>>v&1)]
 assert set(outgoing)<=blocked
 initial.append(A);reaches.append(reach);bounds.append(sorted(set(cut['blocked_occurrences'])-D));capacities.append(len(outgoing))
assert capacities[2]==4
eligible=[]
for u,fu in enumerate(sp):
 for v,fv in enumerate(sp):
  if len(fu)*2!=len(fv)and len(fv)*2!=len(fu):continue
  if not(set(fu)<=set(fv)or set(fv)<=set(fu)):continue
  mask=sum(bool(A>>u&1 and not(A>>v&1))<<k for k,A in enumerate(initial))
  if mask&4:eligible.append((u,v,mask))
fixed=[]
for e,f in combinations_with_replacement(eligible,2):
 if all(capacities[k]+bool(e[2]>>k&1)+bool(f[2]>>k&1)>=cut['rank']for k,cut in enumerate(base)):fixed.append((e[:2],f[:2]))
print('D',sorted(D),'core eligible',len(eligible),'fixed',len(fixed),'caps',capacities,flush=True)
reclose=[];reject=Counter(); certificates={}
for pair in fixed:
 rejected=False
 for k,cut in enumerate(base):
  A=initial[k]
  for _ in range(3):
   before=A
   for u,v in pair:
    if A>>u&1:A|=reaches[k][v]
   if A==before:break
  else:raise ValueError('closure')
  outgoing=[e for e in bounds[k]if A>>routes[e][0]&1 and not(A>>routes[e][1]&1)]
  demanded=sum(not(A>>canon[g.terminals[e]]&1)for e in cut['terminal_slots'])
  if len(outgoing)<demanded:
   full_out=sorted(e for e,(u,v)in routes.items()if e not in D and A>>u&1 and not(A>>v&1))
   assert sorted(outgoing)==full_out
   assert all(not(A>>u&1 and not(A>>v&1))for u,v in pair)
   remaining=[i for i,e in enumerate(cut['terminal_slots'])if not(A>>canon[g.terminals[e]]&1)]
   cert={'canonical_bank_mask':hex(A),'source_axes':[cut['source_axes'][i]for i in remaining],'terminal_slots':[cut['terminal_slots'][i]for i in remaining],'rank':demanded,'old_exports':full_out,'parent_minor':cut['id']}
   certificates[(A,tuple(cert['source_axes']),tuple(cert['terminal_slots']))]=cert
   reject[cut['id']]+=1;rejected=True;break
 if not rejected:reclose.append(pair)
print('reclosed',len(reclose),dict(reject),flush=True)
# Reuse every explicit S031 flow-found chart set as an independently checked
# target-minor cut for this changed D. The stored old capacities are NOT reused.
oldcuts=json.loads((BASE/'endpoint-screen/output/CUT-REJECTIONS.json').read_text())
remain=[];extra=0
for pair in reclose:
 bad=False
 for c in oldcuts:
  A={canon[u]for u in c['raw_charts']};cut=next(x for x in base if x['id']==c['minor_id'])
  assert all(canon[g.inputs[~j]]in A for j in cut['source_axes'])and all(canon[g.terminals[e]]not in A for e in cut['terminal_slots'])
  cap=sum(e not in D and u in A and v not in A for e,(u,v)in routes.items())+sum(u in A and v not in A for u,v in pair)
  if cap<cut['rank']:bad=True;break
 if bad:extra+=1
 else:remain.append(sorted([[rep[u],rep[v]]for u,v in pair]))
remain.sort();print('prior explicit cuts reject',extra,'remain',len(remain),flush=True)
out=HERE/('swap-'+str(retire));out.mkdir(exist_ok=True)
(out/'CUT-CERTIFICATES.json').write_text(json.dumps(list(certificates.values()),indent=2)+'\n')
(out/'SCREEN.json').write_text(json.dumps({'status':'CORRECTED_EXACT_NECESSARY_SCREEN_AUTHOR_ONLY','deleted':sorted(D),'swap_restored':89777,'swap_deleted':retire,'same_grade_profile':{'3':1,'4':5,'5':1},'same_complete_allowance':True,'cut_certificates':len(certificates),'fixed_pairs':len(fixed),'reclosure_survivors':len(reclose),'old_explicit_cut_rejections':extra,'remaining_pair_count':len(remain),'pairs':remain,'complete_circuit':False},indent=2)+'\n')
