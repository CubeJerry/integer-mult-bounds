"""Fresh one/two/three-facet collection from the pinned fused parent."""
from common import *
from copy import deepcopy

def build(s,p,name):
 raw,W,Fc,classes,spaces=source_data(s,p,SELECT[name]);sites,decl=charts_for(Fc,classes,spaces);ys=sorted(W);donors=set().union(*(set(d) for d in classes.values()));groups={d:g for g,ds in classes.items() for d in ds};events,old=base_structure(s,p,raw);receivers={}
 for y in ys:
  es=[i for i,o in enumerate(p['program']) if o[0]=='MOVE' and o[1]==raw[y]];need(len(es)==1 and p['program'][es[0]]==['MOVE',raw[y],3,Fc[y],False],'direct receiver route');receivers[es[0]]=y
 own={};charts={};info={};slot=1880+p['owned_fields']
 for g in sorted(classes,key=lambda g:(len(g),g)):
  for y in g:own[g,y]=slot;charts[slot]=sites[g];info[slot]=(g,y);slot+=1
 pivots=[10,0,6] if name=='three' else [];delivery={10:189,0:168,6:212};visit={168:(168,189),189:(189,212),212:(168,212)};E=Emitter();inits={};clears={};terms=[];routes=[];restored=None
 def ordinary(d,i):
  g=groups[d];C=sites[g];first=E.emit(['MOVE',raw[d],s['initial'][d],C,False],i);enc=[]
  for y in g:t=E.emit(['ADD',own[g,y],raw[d],str(W[y][d]),C]);enc.append({'event':t,'receiver':y,'owner':own[g,y],'coefficient':str(W[y][d])})
  last=E.emit(['MOVE',raw[d],C,127,False],i);terms.append({'donor':d,'support':list(g),'first_move_event':first,'hub_move_event':last,'parent_move_event':i,'route':[s['initial'][d],C,127],'encoding':enc})
 def pivot(d):
  g=groups[d];C=sites[g];y=delivery[d];z=next(z for z in g if z!=y);i=old[d];a=W[y][d];E.mapping[i]=len(E.ops);first=E.emit(['MOVE',raw[d],s['initial'][d],C,False],i);t=E.emit(['ADD',own[g,z],raw[d],str(W[z][d]),C]);enc=[{'event':t,'receiver':z,'owner':own[g,z],'coefficient':str(W[z][d])}];scale=E.emit(['SCALE',raw[d],str(a),C]);acc=E.emit(['ADD',raw[d],own[g,y],'1',C]);clears[own[g,y]]=E.emit(['CLEAR',own[g,y],C]);facet=E.emit(['MOVE',raw[d],C,Fc[y],False],i);deliver=E.emit(['ADD',own[(y,),y],raw[d],'1',Fc[y]]);hub=E.emit(['MOVE',raw[d],Fc[y],127,False],i);recover=[]
  for v in classes[g]:
   if v!=d:k=-W[y][v];t=E.emit(['ADD',raw[d],raw[v],str(k),127]);recover.append({'source_donor':v,'coefficient':str(k),'event':t})
  inv=E.emit(['SCALE',raw[d],str(1/a),127]);terms.append({'donor':d,'support':list(g),'parent_move_event':i,'pivot':True,'delivered_receiver':y,'visiting_receiver':z,'route':[s['initial'][d],C,Fc[y],127],'first_move_event':first,'facet_move_event':facet,'facet_delivery_event':deliver,'hub_move_event':hub,'pivot_scale_event':scale,'pivot_accumulate_event':acc,'inverse_scale_event':inv,'pivot_coefficient':str(a),'hub_recovery_events':recover,'encoding':enc})
 for i,o in enumerate(p['program']):
  if i==410:
   for r,C in charts.items():inits[r]=E.emit(['INIT',r,C])
  if i in events and events[i] in pivots:continue
  E.mapping[i]=len(E.ops)
  if i in events and events[i] in donors:ordinary(events[i],i)
  elif i in receivers:
   y=receivers[i];gs=[tuple(ys),visit[y],(y,)] if name=='three' else sorted([g for g in classes if y in g],key=lambda g:-len(g));prev=3;path=[3];reads=[]
   for g in gs:C=sites[g];r=own[g,y];t=E.emit(['MOVE',raw[y],prev,C,False],i);a=E.emit(['ADD',raw[y],r,'1',C]);clears[r]=E.emit(['CLEAR',r,C]);reads.append({'chart':C,'move_event':t,'read_event':a,'owner':r,'support':list(g)});path.append(C);prev=C
   routes.append({'receiver':y,'parent_move_event':i,'route':path,'reads':reads})
  else:E.emit(deepcopy(o),i)
  if i==513:
   for d in pivots:pivot(d)
   restored=len(E.ops)
 collectors=[{'owner':r,'chart':C,'support':list(info[r][0]),'receiver':info[r][1],'init_event':inits[r],'clear_event':clears[r]} for r,C in charts.items()];meta={'receivers':ys,'facets':Fc,'parent_hoist_block':[410,513],'collectors':collectors,'donor_terms':terms,'receiver_routes':routes,'support_classes':[{'receivers':list(g),'donors':ds,'chart':sites[g]} for g,ds in sorted(classes.items())],'pivots':[{'donor':d,'support':list(groups[d])} for d in pivots],'owned_moves':0}
 return finish(s,p,name,E,W,decl,slot-1880,restored,{y:clears[own[(y,),y]] for y in ys},'facet_collection',meta)
