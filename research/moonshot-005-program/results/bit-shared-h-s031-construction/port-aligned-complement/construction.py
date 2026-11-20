"""Current-port aligned two-centre width12 source construction."""
from pathlib import Path
import gzip,hashlib,importlib.util,json
import numpy as np

def context(repo):
 global g,family,a,previous
 base=repo/'research/moonshot-005-program/results'
 spec=importlib.util.spec_from_file_location('aligned_geometry',base/'bit-coupled-native-geometric-h-source/component/construction.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 family,a,previous=g.context(repo)
 witness=json.loads(gzip.decompress((base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz').read_bytes()));a.marked=set(witness['selected_D'])
 return g,family,a,previous


def build_aligned(k,core_seed,fill_seed,early=False):
 centres=[263,642];primary=61;charts=[family.Chart(a,h,k) for h in centres];w=k//3;dim=12*k;core=[];controls=[]
 for side,chart in enumerate(charts):
  shares=chart.core(core_seed);by_plane={}
  for h,x in chart.point[primary].items():
   row=np.zeros((w,dim),dtype=np.uint8);row[:,6*k*side:6*k*(side+1)]=shares[x];by_plane[h]=row
  core.append(by_plane);read={}
  for s,j in enumerate(chart.donors):
   row=np.zeros((k,dim),dtype=np.uint8);row[:,6*k*side+s*k:6*k*side+(s+1)*k]=np.eye(k,dtype=np.uint8);read[j]=row
  controls.append(read)
 common=sorted(set(charts[0].ports)&set(charts[1].ports));need=lambda ok,txt:None if ok else (_ for _ in ()).throw(ValueError(txt));need(len(common)==w,'common current D count')
 relations=[];selectors=[]
 for side in [0,1]:
  chart=charts[side];s=chart.donors.index(primary);selector=chart.V[np.ix_([chart.ports.index(D) for D in common],range(s*k,(s+1)*k))];selectors.append(selector)
  # The other chart's point-share rows occur in the same ascending common-D order.
  other=charts[1-side];x=other.point[primary][centres[side]];inc=[D for D in other.ports if x in other.radical[D]];need(inc==common,'exact point-share to physical D indexing')
  relations.append(a.mm(selector,controls[side][primary])^core[1-side][centres[side]])
 rel=np.vstack(relations);lift=previous.null_basis(rel,a);base=dim-2*w;tail=16*k-base;need(lift.shape==(dim,base),'aligned cross equations have full rank')
 central={}
 for t,h in enumerate(a.by_donor[primary]):
  if h in centres:
   C=a.mm(controls[centres.index(h)][primary],lift);central[h]=np.hstack([C,np.zeros((k,tail),dtype=np.uint8)])
  else:
   M=a.mm(np.vstack([core[0][h],core[1][h]]),lift);fixed=np.hstack([M,np.zeros((2*w,tail),dtype=np.uint8)]);random=family.coefficients(f'aligned-pair-fill/{k}/{core_seed}/{fill_seed}/{h}',(w,base));central[h]=np.vstack([fixed,np.hstack([random,a.hermite(t+1,w,tail)])])
 maps={};early_seeds={};signs={}
 for side,chart in enumerate(charts):
  for j in chart.donors:
   read=a.mm(controls[side][j],lift);signs[chart.h,j]=np.hstack([read,np.zeros((k,tail),dtype=np.uint8)])
  points={x:central[h] for h,x in chart.point[primary].items()};chart.check_readouts(points,[signs[chart.h,j] for j in chart.donors])
  for j in chart.donors:
   rows=chart.maps(points,j,signs[chart.h,j])
   if j in maps:need(all(np.array_equal(rows[h],maps[j][h]) for h in rows),'one shared source')
   else:
    chart.source_views(rows,j);maps[j]=rows
    if early:
     for es in range(100):
      try:chart.early(j,rows,es,fixed_centres=centres);early_seeds[j]=es;break
      except ValueError:pass
     else:raise ValueError('no actual early frame')
 return {'charts':charts,'maps':maps,'selectors':selectors,'relations':rel,'lift':lift,'early_seeds':early_seeds,'core_seed':core_seed,'fill_seed':fill_seed}

def cross_check(result,k):
 charts=result['charts'];maps=result['maps'];fs={};W={c.h:c.V for c in charts};ports={c.h:c.ports for c in charts};common=sorted(set(ports[263])&set(ports[642]));counts={'views':0,'cross_fail':0,'outside_fail':0};records=[]
 for c in charts:
  fs[c.h]={}
  j=c.donors[0]
  for i in c.views:
   K=previous.null_basis(np.vstack([maps[j][q] for q in a.by_donor[j] if q!=c.h and a.planes[q]<=a.adj[i]]),a);vis=[r for r,D in enumerate(c.ports) if a.charts[D]<=a.adj[i]];R=a.mm(c.V[np.ix_(vis,range(k))],a.mm(maps[j][c.h],K));fs[c.h][i]=(K,R,vis)
 for D in common:
  for i in a.native:
   if not a.charts[D]<=a.adj[i]:continue
   vectors={};bad=[];outside=[]
   for h in [263,642]:
    K,R,vis=fs[h][i];pos=vis.index(ports[h].index(D));vectors[h]=a.mm(K,g.inverse(R,a)[:,pos:pos+1])
   for ha in [263,642]:
    hb=905-ha;c=charts[[263,642].index(hb)];other=[r for r,Q in enumerate(c.ports) if Q!=D and a.charts[Q]<=a.adj[i]]
    for s,j in enumerate(c.donors):
     y=a.mm(c.V[np.ix_(other,range(s*k,(s+1)*k))],a.mm(maps[j][hb],vectors[ha]));
     if np.any(y):bad.append([ha,hb,j,int(np.count_nonzero(y))])
    for j in maps:
     if j in a.planes[ha] or j not in a.charts[D]:continue
     qs=[q for q in a.by_donor[j] if a.planes[q]<=a.adj[i] and not a.planes[q]<=a.charts[D]]
     if np.any(a.mm(np.vstack([maps[j][q] for q in qs]),vectors[ha])):outside.append([ha,j])
   counts['views']+=1;counts['cross_fail']+=bool(bad);counts['outside_fail']+=bool(outside);records.append({'D':D,'receiver':i,'cross':bad,'outside':outside})
 return counts,records
