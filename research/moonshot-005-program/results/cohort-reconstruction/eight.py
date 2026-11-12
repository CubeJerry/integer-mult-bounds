"""Fresh literal reconstruction of fourteen reversible cohort transfers."""
from common import *
from copy import deepcopy
from itertools import combinations

def build(s,p):
 selected=SELECT['eight'];raw,W,Fc,classes,spaces=source_data(s,p,selected)
 need(len(classes)==14 and Counter(map(len,classes.values()))=={4:2,7:8,8:4},'fourteen source cohorts');need(all(len(g)==4 for g in classes),'four recipients per cohort')
 sites,decl=charts_for(Fc,classes,spaces);need(len(decl)==14 and all(len(d['frame'])==6 for d in decl),'fourteen dimension-six charts')
 events,old=base_structure(s,p,raw);E=Emitter();ys=sorted(W);base=1880+p['owned_fields'];own={y:base+i for i,y in enumerate(ys)};acc=[base+8+i for i in range(4)];snap=[base+12+i for i in range(4)];groups=[];inits={};clears={};reads=[];receivers={};restored=None
 for y in ys:
  es=[i for i,o in enumerate(p['program']) if o[0]=='MOVE' and o[1]==raw[y]];need(len(es)==1 and p['program'][es[0]]==['MOVE',raw[y],3,Fc[y],False],'direct receiver route');receivers[es[0]]=y
 def group(g,ds):
  C=sites[g];A=[[W[y][d] for d in ds] for y in g];choices=[]
  for J in combinations(range(len(ds)),4):
   minor=[[r[k] for k in J] for r in A]
   if rank(minor)==4:
    inv=inverse(minor);choices.append((sum(bool(v) for row in inv for v in row),J))
  need(choices,'a source invertible four-column minor');inds=list(min(choices)[1])
  need(len(inds)==4,'source cohort full rank');I=[ds[j] for j in inds];N=[d for d in ds if d not in I];AI=[[W[y][d] for d in I] for y in g];B=inverse(AI);unit=[[F(i==j) for j in range(4)] for i in range(4)];need(mul(AI,B)==unit==mul(B,AI),'two-sided inverse')
  rec={'receivers':list(g),'chart':C,'donors':ds,'pivots':I,'nonpivots':N,'matrix':[[str(v) for v in r] for r in A],'pivot_minor':[[str(v) for v in r] for r in AI],'inverse_minor':[[str(v) for v in r] for r in B],'begin':len(E.ops),'accumulator_roles':acc,'snapshot_roles':snap,'acquisition_reads':[],'recovery_reads':[],'deliveries':[]}
  for r in acc:E.emit(['INIT',r,C])
  for d in N:
   E.mapping[old[d]]=len(E.ops);E.emit(['MOVE',raw[d],s['initial'][d],C,False],old[d])
   for k,y in enumerate(g):t=E.emit(['ADD',acc[k],raw[d],str(W[y][d]),C]);rec['acquisition_reads'].append({'event':t,'donor':d,'receiver':y})
   E.emit(['MOVE',raw[d],C,127,False],old[d])
  for d in I:E.mapping[old[d]]=len(E.ops);E.emit(['MOVE',raw[d],s['initial'][d],C,False],old[d])
  for r,d in zip(snap,I):E.emit(['INIT',r,C]);E.emit(['ADD',r,raw[d],'1',C])
  rec['snapshots']=len(E.ops)
  for k,d in enumerate(I):
   E.emit(['ADD',raw[d],snap[k],'-1',C])
   for j,r in enumerate(snap):
    if AI[k][j]:E.emit(['ADD',raw[d],r,str(AI[k][j]),C])
   E.emit(['ADD',raw[d],acc[k],'1',C])
  rec['payloads']=len(E.ops)
  for r in acc+snap:E.emit(['CLEAR',r,C])
  for d,y in zip(I,g):
   a=E.emit(['MOVE',raw[d],C,Fc[y],False],old[d]);b=E.emit(['ADD',own[y],raw[d],'1',Fc[y]]);c=E.emit(['MOVE',raw[d],Fc[y],127,False],old[d]);rec['deliveries'].append({'donor':d,'receiver':y,'facet_move':a,'read':b,'hub_move':c})
  rec['payloads_at_hub']=len(E.ops)
  for k,d in enumerate(I):
   for v in N:t=E.emit(['ADD',raw[d],raw[v],str(-W[g[k]][v]),127]);rec['recovery_reads'].append({'event':t,'donor':v})
  for r,d in zip(snap,I):E.emit(['INIT',r,127]);E.emit(['ADD',r,raw[d],'1',127])
  rec['inverse_snapshots']=len(E.ops)
  for k,d in enumerate(I):
   E.emit(['ADD',raw[d],snap[k],'-1',127])
   for j,r in enumerate(snap):
    if B[k][j]:E.emit(['ADD',raw[d],r,str(B[k][j]),127])
  rec['originals_restored']=len(E.ops)
  for r in snap:E.emit(['CLEAR',r,127])
  rec['end']=len(E.ops);rec['annihilator']=[v for v in range(512) if all((v&w).bit_count()%2==0 for w in spaces[C])];actual=[x+112 for x in s['live'] if spaces[C]<=spaces[s['final'][x+112]]];need(actual==list(g),'exact cohort containment');rec['active_facets_containing_chart']=actual;groups.append(rec)
 for i,o in enumerate(p['program']):
  if i==410:
   for y in ys:inits[y]=E.emit(['INIT',own[y],Fc[y]])
   for d in selected:E.mapping[old[d]]=len(E.ops);E.emit(['MOVE',raw[d],s['initial'][d],127,False],old[d])
   for g,ds in sorted(classes.items()):group(g,ds)
   restored=len(E.ops)
  if i in events:continue
  E.mapping[i]=len(E.ops);E.emit(deepcopy(o),i)
  if i in receivers:
   y=receivers[i];t=E.emit(['ADD',raw[y],own[y],'1',Fc[y]]);clears[y]=E.emit(['CLEAR',own[y],Fc[y]]);reads.append({'receiver':y,'parent_move':i,'read':t,'clear':clears[y]})
 meta={'receivers':ys,'facets':Fc,'facet_records':[{'receiver':y,'role':own[y],'init':inits[y],'clear':clears[y]} for y in ys],'frame_donors':selected,'groups':groups,'owned_moves':0,'parent_hoist_block':[410,513],'receiver_reads':reads}
 return finish(s,p,'eight',E,W,decl,base+16-1880,restored,clears,'cohort_collection',meta)
