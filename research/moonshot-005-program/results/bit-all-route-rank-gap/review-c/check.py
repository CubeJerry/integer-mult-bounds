#!/usr/bin/env python3
"""Independent exact endpoint and native public-route review."""
import argparse,gzip,hashlib,json
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

def exact_budget(parent):
 scale=1<<176;cache={0:(F(0),F(0)),1:(F(1),F(1))}
 def power(n):
  if n not in cache:
   target=n**199*scale**200;low,high=0,n*scale+1
   while high-low>1:
    mid=(low+high)//2
    if mid**200<=target:low=mid
    else:high=mid
   need(low**200<=target<high**200,'outward integer root')
   cache[n]=(F(low,scale),F(high,scale))
  return cache[n]
 def interval(coeff):
  lo=hi=F(0)
  for n,c in coeff.items():
   a,b=power(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
  return lo,hi
 def add(coeff,n,c):
  if n:coeff[n]=coeff.get(n,F(0))+c
  if coeff.get(n)==0:del coeff[n]
 terms={127:F(37,6),64:F(37,3),1:F(-37,3)}
 for j in range(1,9):add(terms,7*j+1,F(37,3));add(terms,7*j,F(-37,3))
 add(terms,7,-222);E=interval(terms);c=interval({1:F(1),8:F(1),7:F(-1)})
 need(82<E[0]<=E[1]<83 and 1<c[0]<=c[1]<2,'exact endpoint ranges')
 need(42*c[0]>E[1],'weighted count84 excluded')
 need(1+41*c[1]<E[0],'weighted count83 remains arithmetically possible')
 caps=[]
 for d in range(42):
  lo=E[0]-d*c[1];hi=E[1]-d*c[0]
  floor=lo.numerator//lo.denominator
  need(F(floor)<lo<=hi<F(floor+1),'exact integer cap')
  need(floor==parent['caps'][d]['owned_positive_at_most'],'parent cap agreement')
  caps.append(floor)
 equal=0;positive=0
 for kind in ('X','Y'):
  for a in range(9):
   for b in range(9):
    if a==b:continue
    coeff={};add(coeff,abs(a-b),F(1))
    if kind=='Y':add(coeff,a,F(1));add(coeff,b,F(-1))
    else:add(coeff,8-b,F(1));add(coeff,8-a,F(-1))
    if a>b:
     for n,v in ((1,-1),(8,-1),(7,1)):add(coeff,n,F(v))
    if not coeff:equal+=1
    else:
     need(interval(coeff)[0]>0,'strict finite potential inequality');positive+=1
    for endpoint in (0,1):
     value=sum(v*((1 if n>0 else 0) if endpoint==0 else n) for n,v in coeff.items())
     need(value>=0,'potential endpoint inequality')
 for key,own in [('E_star',E),('c_star',c)]:
  p=tuple(map(F,parent[key]));need(p[0]<=own[0]<=own[1]<=p[1],'fresh tighter interval inside reviewed interval')
 return {'dyadic_bits':176,'E':[str(v) for v in E],'c':[str(v) for v in c],
         'caps_owned_by_public_down':caps,'potential_equalities':equal,
         'strict_potential_edges':positive,'M_plus_2D_at_most':83,'ell_at_most':194}

def replay(path,native,translated):
 word=json.loads(gzip.decompress(path.read_bytes()))
 need(word['public']==222 and word['start']==native['start'][:222],'native independent public inputs')
 bases={int(c):echelon(frame['B']) for c,frame in word['frames'].items()}
 dims={int(c):frame['dim'] for c,frame in word['frames'].items()}
 need(all(len(bases[c])==dims[c] for c in bases),'all rational chart ranks')
 loc=dict(enumerate(word['start']));rows={i:1<<i for i in range(222)}
 profile=Counter();down=[];upfacets=Counter();own_anchor=set();facet_departures=0
 for event,op in enumerate(word['program']):
  t,i=op[:2];need(i<222,'no owned record in sharpness control')
  if t=='MOVE':
   _,i,u,v=op;need(loc[i]==u,'actual MOVE source')
   d=dims[v]-dims[u];need(d!=0,'positive MOVE')
   lo,hi=(u,v) if d>0 else(v,u);need(subset(bases[lo],bases[hi]),'nested actual MOVE')
   profile[abs(d)]+=1
   if d<0:
    down.append({'field':i,'destination':v,'value':rows[i],'event':event})
    facet_departures+=int(dims[u]==7)
   elif dims[v]==7:
    upfacets[i]+=1
    if i>=111 and subset(bases[v],echelon(native['frames'][str(native['final'][i])]['B'])):own_anchor.add(i)
   loc[i]=v
  elif t=='ADD':
   _,i,j,c=op;need(i!=j and loc[i]==loc[j]==c,'actual cochart ADD');rows[i]^=rows[j]
  else:raise ValueError('unexpected operation')
 for i in range(222):
  expected=(1<<i)^((1<<(i-111)) if i>=111 and i-111 in translated else 0)
  need(rows[i]==expected,'all222-column partial endpoint')
  target=echelon(native['frames'][str(native['final'][i])]['B'])
  need(subset(bases[loc[i]],target) and subset(target,bases[loc[i]]),'native endpoint geometry')
 dx=sum(entry['field']<111 for entry in down);dy=len(down)-dx
 need(sum(v for i,v in upfacets.items() if i<111)<=111+dx,'X facet occurrence injection')
 need(sum(v for i,v in upfacets.items() if i>=111)-len(own_anchor)<=dy,'unanchored Y occurrence injection')
 return {'profile':dict(sorted(profile.items())),'public_down':len(down),
         'upward_own_Y_anchors':len(own_anchor),'X_down':dx,'Y_down':dy,
         'down':down,'bases':bases,'facet_departures':facet_departures,
         'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def main():
 p=argparse.ArgumentParser();p.add_argument('--package',type=Path,required=True)
 p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 nr=a.native.read_bytes();need(hashlib.sha256(nr).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
 native=json.loads(gzip.decompress(nr));parent=json.loads((a.package/'RESULT.json').read_text())
 numerical=exact_budget(parent);reports={}
 for name,translated in [('sharp_X_public_descent',{0}),('sharp_Y_public_descent',{0}),('same_public_record_repeated_facet',set())]:
  path=a.package/'native-controls'/f'{name}.json.gz';r=replay(path,native,translated)
  if name.startswith('sharp'):
   need(r['profile']=={1:1,7:221,8:1} and r['public_down']==1,'exact sharp excursion profile')
  else:
   need(r['profile']=={1:4,7:222} and r['public_down']==2,'actual repeated-facet profile')
   down=r['down'];need([d['field'] for d in down]==[0,0] and [d['value'] for d in down]==[1,2],'same physical record independent histories')
   need(down[0]['destination']==down[1]['destination'],'actual same foreign facet')
   chart=r['bases'][down[0]['destination']]
   local=[1<<i for i in range(111) if subset(echelon(native['frames'][str(native['start'][i])]['B']),chart)]
   y=[1<<i for i in range(111,222)]
   for held,missing in ((1,2),(2,1)):
    known=binary_basis(local+y+[held])
    need(len(binary_basis(list(known.values())+[missing]))>len(known),'first/last-only visit collapse must fail')
  if name=='sharp_Y_public_descent':need(r['upward_own_Y_anchors']==110,'Y0 has no upward own-facet anchor')
  del r['bases'];reports[name]=r
 pins={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in a.package.iterdir() if p.is_file()}
 out={'status':'PASS_INDEPENDENT_ALL_ROUTE_RANK_GAP_REVIEW','author_code_imported':False,
      'input_columns':222,'reviewed_files':pins,'numerical':numerical,'native_words':reports,
      'controls':['charge2 instead of sharp c is false','weighted count83 is not excluded',
                  'collapse same record to first visit fails','collapse same record to last visit fails',
                  'Y own-facet upward anchor may be absent'],
      'scope':'Universal argument independently read; finite exact controls; retained-caller conditional rank floor; no new kappa.'}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':out['status'],'potential_edges':numerical['potential_equalities']+numerical['strict_potential_edges'],'native_words':len(reports)}))

if __name__=='__main__':main()

