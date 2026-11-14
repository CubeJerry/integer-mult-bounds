#!/usr/bin/env python3
"""Independent all-column replay, chronology and residual cut for the C5 word."""
import argparse,gzip,hashlib,json,copy
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(ok,msg):
 if not ok:raise ValueError(msg)

def echelon(rows):
 b={}
 for row in rows:
  v=list(map(F,row))
  for p,u in sorted(b.items()):
   c=v[p]
   if c:v=[x-c*y for x,y in zip(v,u)]
  p=next((i for i,x in enumerate(v) if x),None)
  if p is not None:
   c=v[p];b[p]=tuple(x/c for x in v)
 return b

def subset(a,b):
 for u in a.values():
  v=list(u)
  for p,r in sorted(b.items()):
   c=v[p]
   if c:v=[x-c*y for x,y in zip(v,r)]
  if any(v):return False
 return True

def binary_basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return b

TARGETS=[92,36,54,38,55]
RESIDUAL=[8,9,14,15,30,31,59]
NATIVE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
PIVOTS='8c11ca368995bc6a77f8d0425ac259384a7edf6164bc4254dfc0c7d780e26e19'

def setup(native,pivots):
 roots=[list(map(F,native['frames'][str(native['start'][i])]['B'][0])) for i in range(111)]
 dot=lambda x,y:sum(a*b for a,b in zip(x,y))
 groups={}
 for i,r in enumerate(roots):
  support=tuple(j for j,x in enumerate(r) if x);sign=1 if r[support[0]]>0 else-1
  groups.setdefault((support,sum(x*sign<0 for x in r)%2),[]).append(i)
 groups=list(groups.values());piv=list(range(8))+pivots
 need(all(p in g for p,g in zip(piv,groups)),'independent pivot grouping')
 masks=[sum(1<<j for j in g) for g in groups]
 E=[]
 for i,x in enumerate(roots):
  row=sum(int(i==j or dot(x,y)==0)<<j for j,y in enumerate(roots))
  for mask,p in zip(masks,piv):
   if row>>p&1:row^=mask
  E.append(row)
 need(len(binary_basis(E))==3,'actual core rank')
 for a,i in enumerate(TARGETS):
  for b,j in enumerate(TARGETS):
   if a!=b:need((dot(roots[i],roots[j])==0)==((a-b)%5 in (1,4)),'actual C5 geometry')
 return roots,E,groups,piv

def replay(word,native,E,closed=False):
 need(word['public']==222 and word['start']==native['start'][:222],'actual public inputs')
 bases={int(c):echelon(f['B']) for c,f in word['frames'].items()}
 dims={int(c):f['dim'] for c,f in word['frames'].items()}
 need(all(len(bases[c])==dims[c] for c in bases),'rational chart ranks')
 loc=dict(enumerate(word['start']));rows={i:1<<i for i in range(222)}
 born=set(loc);peak=0;counts=Counter();pairs=set();trajectories={};erasures=[]
 for k,op in enumerate(word['program'],1):
  t,i=op[:2];counts[t]+=1
  if t=='INIT':
   need(i>=222 and i not in born,'fresh actual zero INIT');born.add(i);loc[i]=op[2];rows[i]=0
   peak=max(peak,len(loc)-222)
  elif t=='CLEAR':
   need(i>=222 and loc.get(i)==op[2],'owned erasure at actual chart')
   erasures.append((k,i,op[2],rows[i]));del loc[i];del rows[i]
  elif t=='MOVE':
   _,i,u,v=op;need(loc.get(i)==u,'actual MOVE source');d=dims[v]-dims[u]
   need(abs(d)==1,'literal unit MOVE')
   if i<222:need(d>0,'all original physical paths ascend')
   if (u,v) not in pairs:
    lo,hi=(u,v) if d>0 else(v,u);need(subset(bases[lo],bases[hi]),'actual nested MOVE');pairs.add((u,v))
   trajectories.setdefault(i,[]).append((dims[u],dims[v],k));loc[i]=v
  elif t=='ADD':
   _,i,j,c=op;need(i!=j and i in loc and j in loc and loc[i]==loc[j]==c,'actual cochart ADD')
   rows[i]^=rows[j]
  else:raise ValueError('unknown operation '+t)
 for i in range(111):
  expected=(1<<(111+i)) ^ ((1<<i) if i in TARGETS else E[i])
  need(rows[111+i]==expected,'exact arbitrary-Y endpoint '+str(i))
  if closed or i in TARGETS:need(subset(bases[loc[111+i]],echelon(native['frames'][str(native['final'][111+i])]['B'])) and dims[loc[111+i]]==7,'native Y endpoint')
  else:need(dims[loc[111+i]]==0,'uncompleted Y remains at ground')
  if closed:need(rows[i]==1<<i and dims[loc[i]]==8,'all original X restored at Hub')
 if closed:need(len(loc)==222,'all owned lifetimes closed')
 else:
  need(len(loc)==336,'114 retained caches')
  need(all(rows[222+i]==1<<i and loc[222+i]==native['start'][i] for i in range(111)),'111 actual stationary pure copies')
 return {'counts':dict(counts),'peak_owned':peak,'owned_live':len(loc)-222,
         'distinct_MOVE_pairs':len(pairs),'nonmonotone_owned':{str(i):p for i,p in trajectories.items() if i>=222 and len({b-a for a,b,k in p})>1},
         'erased_nonzero_values':sum(bool(r) for k,i,c,r in erasures)},loc,rows,bases,trajectories,erasures

def residual_cut(loc,rows,bases,roots):
 inside={c:any(all(sum(x*y for x,y in zip(v,roots[i]))==0 for v in b.values())
               for i in RESIDUAL) for c,b in bases.items()}
 selected=[i for i,c in loc.items() if inside[c]]
 observation=[rows[i] for i in selected]
 targets=[(1<<i)^(1<<(111+i)) for i in RESIDUAL]
 r0=len(binary_basis(observation));r1=len(binary_basis(observation+targets))
 return {'receivers':RESIDUAL,'inside_fields':len(selected),'observation_rank':r0,
         'augmented_rank':r1,'deficit':r1-r0,
         'completed_Y_inside':sum(111+i in selected for i in TARGETS)}

def main():
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True)
 p.add_argument('--pivots',type=Path,required=True);p.add_argument('--package',type=Path,required=True)
 p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 nr=a.native.read_bytes();pr=a.pivots.read_bytes()
 need(hashlib.sha256(nr).hexdigest()==NATIVE,'native pin');need(hashlib.sha256(pr).hexdigest()==PIVOTS,'pivot pin')
 native=json.loads(gzip.decompress(nr));pivots=json.loads(pr)['pivots']
 roots,E,groups,piv=setup(native,pivots)
 partial=json.loads(gzip.decompress((a.package/'PARTIAL-WORD.json.gz').read_bytes()))
 closed=json.loads(gzip.decompress((a.package/'CLOSED-WORD.json.gz').read_bytes()))
 author=json.loads((a.package/'RESULT.json').read_text())
 rp,loc,rows,bases,trajectories,erasures=replay(partial,native,E)
 rc,*_=replay(closed,native,E,True)
 need(rp['counts']=={'INIT':122,'ADD':555,'MOVE':756,'CLEAR':8} and rp['peak_owned']==117,'partial full invoice')
 need(rc['counts']=={'INIT':122,'ADD':616,'MOVE':1598,'CLEAR':122} and rc['peak_owned']==117,'closed full invoice')
 need(rp['nonmonotone_owned'].keys()=={'343'},'exactly one reflected route')
 need([(u,v) for u,v,k in trajectories[343]]==[(5,6),(6,5)],'paid rank5-to6-to5 turn')
 for i in range(111):
  g=next(g for g in groups if i in g);pivot=next(p for p,g0 in zip(piv,groups) if g0==g)
  dirty=i>=8 and i==pivot and i not in TARGETS
  expected=sum(1<<j for j in g) if dirty else 1<<i
  need(rows[i]==expected,'actual partial original X value')
  if dirty:need(subset(bases[loc[i]],echelon([roots[j] for j in g])) and
                subset(echelon([roots[j] for j in g]),bases[loc[i]]),'actual dirty halfbank location')
  else:need(len(bases[loc[i]])==8,'restored original has reached Hub')
 core=[rows[i] for i in range(336,339)]
 need(all(loc[i]==0 for i in range(336,339)) and len(binary_basis(core+E))==3,'three actual ground core caches')
 cut=residual_cut(loc,rows,bases,roots)
 need((cut['observation_rank'],cut['augmented_rank'],cut['deficit'])==(211,217,6),'all222-column residual cut')
 need(cut['completed_Y_inside']==0,'completed targets outside residual downset')
 md=author['metadata'];controls=[]
 reflected=[i for i,o in enumerate(closed['program']) if o[0]=='MOVE' and o[1]==343]
 local_move=next(i for i,o in enumerate(closed['program']) if o[0]=='MOVE' and o[1]==339)
 omitted={'local_copy_ascent':local_move,'reflection_ascent':reflected[0],
          'reflection_descent':reflected[1],'core_undo':md['core_undo'][0],
          'arbitrary_Y_precode':md['precode'][0],'Y4_history_recoding':md['copy_recoding'],
          'remaining_X_restore':md['remaining_restoration'][0],'Y2_decode':md['Y2_decoding']}
 for name,event in omitted.items():
  mutant=copy.deepcopy(closed);del mutant['program'][event]
  try:replay(mutant,native,E,True)
  except (ValueError,KeyError) as error:controls.append({'name':name,'rejected':True,'reason':str(error)})
  else:raise ValueError('mutant incorrectly accepted: '+name)
 mutant=copy.deepcopy(closed);at=md['packets'][0]['completion']
 need(mutant['program'][at][0]==mutant['program'][at+1][0]=='ADD','actual two-ADD exchange')
 mutant['program'][at],mutant['program'][at+1]=mutant['program'][at+1],mutant['program'][at]
 try:replay(mutant,native,E,True)
 except (ValueError,KeyError) as error:controls.append({'name':'reverse_ordered_exchange','rejected':True,'reason':str(error)})
 else:raise ValueError('reversed exchange accepted')
 mutant=copy.deepcopy(closed)
 at=next(i for i,o in enumerate(mutant['program']) if o[0]=='CLEAR' and o[1]==343)
 mutant['program'][at][2]=0
 try:replay(mutant,native,E,True)
 except (ValueError,KeyError) as error:controls.append({'name':'uncharged_erasure_relocation','rejected':True,'reason':str(error)})
 else:raise ValueError('free proper-to-ground erasure accepted')
 need(cut['deficit']>4,'five local completions do not reduce residual packet need to four')
 pins={name:hashlib.sha256((a.package/name).read_bytes()).hexdigest() for name in
       ('PROOF.md','build_braid.py','PARTIAL-WORD.json.gz','CLOSED-WORD.json.gz','RESULT.json')}
 out={'status':'PASS_INDEPENDENT_ACTUAL_C5_PARTIAL_SOURCE','author_code_imported':False,
      'input_columns':222,'native_sha256':NATIVE,'pivot_sha256':PIVOTS,'reviewed_pins':pins,
      'partial':rp,'closed':rc,'residual_cut':cut,'negative_controls':controls,
      'scope':'Paid reflected partial source; six future inward channels still necessary in stated continuation; no full supplier or kappa.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'controls':len(controls),'residual_deficit':cut['deficit']}))

if __name__=='__main__':main()

