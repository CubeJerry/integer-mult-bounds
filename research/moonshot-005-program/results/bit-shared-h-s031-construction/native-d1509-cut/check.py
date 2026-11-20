#!/usr/bin/env python3
"""Actual five-source two-wave prefix and one owner-bound D1509 common cut."""
from argparse import ArgumentParser
from pathlib import Path
from collections import defaultdict
import gzip,hashlib,importlib.util,json
import numpy as np

def need(v,m):
 if not v:raise ValueError(m)
def read(p):return json.loads(gzip.decompress(p.read_bytes()))
def block(ms):
 X=np.zeros((sum(M.shape[0]for M in ms),sum(M.shape[1]for M in ms)),dtype=np.uint8);r=c=0
 for M in ms:X[r:r+len(M),c:c+M.shape[1]]=M;r+=len(M);c+=M.shape[1]
 return X
def main(repo,out):
 out.mkdir(parents=True,exist_ok=True);here=Path(__file__).parent;base=repo/'research/moonshot-005-program/results';s=importlib.util.spec_from_file_location('D_actual_geometry',base/'bit-coupled-native-geometric-h-source/component/construction.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g);family,a,previous=g.context(repo)
 if(here/'SOURCE-PINS.json').exists():
  for p,d in json.loads((here/'SOURCE-PINS.json').read_text()).items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==d,'pin '+p)
 z=read(here/'COMPONENT.json.gz');source=z['source'];D=1509;i=6;donors=[0,45,61,62,100];three={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in vv.items()}for j,vv in source['maps'].items()};c12=read(base/'bit-shared-h-s031-construction/port-aligned-complement/SOURCE-COEFFICIENTS.json.gz');twelve={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in vv.items()}for j,vv in c12['maps'].items()};maps={j:{h:block([three[j][h],twelve[j][h]])for h in a.by_donor[j]}for j in donors};marked=set(read(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz')['selected_D']);L=np.array(source['L'],dtype=np.uint8);LF=np.zeros((480,8),dtype=np.uint8);LF[:48,:4]=L;LF[240:288,4:]=L
 need(a.rank(L)==4 and a.rank(LF)==8,'full selected single and paired source spaces')
 old3=read(base/'bit-shared-h-s031-construction/protected-d1509-tail-repair/SOURCE-COEFFICIENTS.json.gz');changes={}
 for j in donors:
  changes[j]=[h for h in maps[j]if not np.array_equal(three[j][h],np.array(old3['maps'][str(j)][str(h)],dtype=np.uint8))]
  need(all(a.planes[h]<=a.charts[D] and h not in [263,642]for h in changes[j]),'additional edits only at unbuilt H parents of D')
  for h in source['inside'][str(j)]:need(a.rank(a.mm(three[j][h],L))==1,'every in-D quotient has a one-dimensional restriction')
 lines={int(h):np.array(v,dtype=np.uint8)[:,None]for h,v in source['lines'].items()}
 for j in a.charts[D]:need(a.rank(np.hstack([lines[h]for h,H in enumerate(a.planes)if j in H and H<=a.charts[D]]))==4,'every geometric D donor has a full four-line basis')
 routes=[json.loads(x)for x in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()];HX=defaultdict(list);HY=defaultdict(list);Xj=defaultdict(list);Yj=defaultdict(list)
 for x in routes:
  if x[3]is None:continue
  (HX if x[0]=='X'else HY)[x[3]].append(x)
  if x[0]=='X':Xj[x[1],x[3]].append(x)
  elif x[6]is not None:Yj[x[6],x[3]].append(x)
 key=lambda x:(x[1],x[2])
 for dct in [HX,HY,Xj,Yj]:
  for q in dct:dct[q].sort(key=key)
 def complete(E):
  rows=list(E)
  for v in np.eye(E.shape[1],dtype=np.uint8):
   if a.rank(np.vstack(rows+[v]))>len(rows):rows.append(v)
   if len(rows)==E.shape[1]:break
  return np.array(rows,dtype=np.uint8)
 frames={};early={};late={};source_records=[];early_records=[];propagation={}
 for j in donors:
  rows=[];owners=[];Ephys=np.zeros((480,480),dtype=np.uint8);late[j]={};comp_early={3:[],12:[]};inv3={};views={}
  for h in sorted(maps[j]):
   quota=a.quota[j,h];T3=np.array(z['source_frames'][f'{j}/{h}'],dtype=np.uint8);need(a.rank(T3)==6,'full protected source phase frame')
   if quota==30:T12=np.eye(24,dtype=np.uint8)
   else:
    label=f'{263 if j in [0,61,62]else 642}/12/';T12=complete(family.coefficients(f'early/{label}{j}/{h}/0',(12,24)))
   need(a.rank(T12)==24,'full complementary source phase frame');Q=np.zeros((30,30),dtype=np.uint8);cp=[0,1,2,15,16,17];cq=list(range(3,15))+list(range(18,30))
   if quota==30:Q=np.eye(30,dtype=np.uint8)
   else:Q[np.ix_([0,1,2,15,16,17],cp)]=T3;Q[np.ix_(list(range(3,15))+list(range(18,30)),cq)]=T12
   need(a.rank(Q)==30,'full15 genuine paired quotient frame');frames[j,h]=Q;B=block([maps[j][h],maps[j][h]]);R=a.mm(Q,B);rr=Xj[j,h];need(len(rr)==quota,'actual source early quota')
   for t,x in enumerate(rr):Ephys[x[2]]=R[t]
   rows.extend(R[:quota]);owners.extend([[h,x[2]]for x in rr]);late[j][h]=R[quota:];need(len(Yj[j,h])==30-quota,'every late parity has one actual native Y visit')
   for k,T,C in [(3,T3,three),(12,T12,twelve)]:comp_early[k].extend(a.mm(T[:quota*k//15],block([C[j][h],C[j][h]])))
  E=np.array(rows,dtype=np.uint8);need(E.shape==(480,480)and a.rank(E)==a.rank(Ephys)==480,'one genuine full480 early source basis');need(sorted(x[1]for x in owners)==list(range(480)),'all actual source owners exactly once');need(all(a.rank(np.array(comp_early[k],dtype=np.uint8))==32*k for k in [3,12]),'both component early bases');early[j]={'matrix':E.tolist(),'physical_matrix':Ephys.tolist(),'row_owners':owners};early_records.append({'donor':j,'rank':480,'protected_seed':z['early_seeds'][str(j)],'complement_seed':0})
  for ii in sorted(a.adj[j]):
   vv=sorted(h for h in maps[j]if a.planes[h]<=a.adj[ii]);need(len(vv)==16 and a.rank(np.vstack([maps[j][h]for h in vv]))==240,'full240 source cut');source_records.append([j,ii]);views[ii]=vv;inv3[ii]=g.inverse(np.vstack([three[j][h]for h in vv]),a)
  maximum=0;rrs=[]
  for h in a.by_donor[j]:
   for q in a.by_donor[j]:
    if h==q:continue
    cols=[inv3[ii][:,3*vv.index(h):3*vv.index(h)+3]for ii,vv in views.items()if h in vv and q in vv];Z=np.hstack(cols);rk=a.rank(Z);need(rk<=42 and not np.any(a.mm(three[j][q],Z)),'all-pair protected nonsaturation');maximum=max(maximum,rk);rrs.append([h,q,rk])
  propagation[j]={'protected_maximum':maximum,'full_upper':maximum+180,'all_ordered_pairs':rrs};print('SOURCE_EARLY_PROPAGATION',j,63,480,maximum,flush=True)
 oldpair=read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/COEFFICIENTS.json.gz');oldfibres=read(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');retained=[]
 for h in [263,642]:
  W=np.array(oldpair['H'][str(h)]['word'],dtype=np.uint8);ps=oldpair['H'][str(h)]['ports'];ds=sorted(a.planes[h])
  for ii,ff in oldfibres[str(h)].items():
   ii=int(ii);K=np.array(ff['kernel'],dtype=np.uint8);vis=[p for p,d in enumerate(ps)if a.charts[d]<=a.adj[ii]];Rs=[]
   for t,j in enumerate(ds):
    off=[q for q in maps[j]if q!=h and a.planes[q]<=a.adj[ii]];need(not np.any(a.mm(np.vstack([maps[j][q]for q in off]),K)),'retained whole common H fibre');Rs.append(a.mm(W[np.ix_(vis,range(15*t,15*t+15))],a.mm(maps[j][h],K)))
   need(a.rank(Rs[0])==15 and all(np.array_equal(Rs[0],R)for R in Rs),'retained full15 H readout');retained.append([h,ii])
 providers={int(h):v for h,v in z['providers'].items()};Dparents=[h for h,H in enumerate(a.planes)if H<=a.charts[D]];V={k:np.array([[g.power(p+1,c,a)for c in range(3*k)]for p in range(3*k)],dtype=np.uint8)for k in [3,12]};DV={k:np.array([[g.power(p+1,c-1,a)if c%2 else 0 for c in range(3*k)]for p in range(3*k)],dtype=np.uint8)for k in [3,12]}
 for h in Dparents:
  if h in providers:continue
  ds=sorted(a.planes[h]&a.native);ps=[d for d,Q in enumerate(a.charts)if a.planes[h]<=Q and d in marked]
  if len(ds)==3:providers[h]={'kind':'double','donors':ds,'ports':ps,'early':V[3].tolist()}
  else:
   large=next(j for j in ds if a.quota[j,h]==30);small=next(j for j in ds if a.quota[j,h]==15);G=DV[3].copy();G[:,6:]=0;providers[h]={'kind':'partial','donors':ds,'ports':ps,'large':large,'small':small,'early':V[3].tolist(),'late':V[3].tolist(),'cross':G.tolist()}
 physical={};local_checks=0;Ddata=np.zeros((35,40),dtype=np.uint8);downers=sorted([x for x in routes if x[4]==D and x[0]=='X'],key=key)+sorted([x for x in routes if x[4]==D and x[0]=='Y'],key=key);need(downers==z['D_owners'],'exact35 D original owners');dindex={(x[0],x[1],x[2]):q for q,x in enumerate(downers)}
 for h,p3 in sorted(providers.items()):
  ds=p3['donors'];xs=HX[h];ys=HY[h];xi={(x[1],x[2]):q for q,x in enumerate(xs)};yi={(x[1],x[2]):q for q,x in enumerate(ys)};E=np.zeros((len(xs),len(xs)),dtype=np.uint8);B=np.zeros((len(ys),len(ys)),dtype=np.uint8);G=np.zeros((len(ys),len(xs)),dtype=np.uint8);psall=[d for d,Q in enumerate(a.charts)if a.planes[h]<=Q];ps={3:[d for d in psall if d in marked],12:[d for d in psall if d not in marked]};need(ps[3]==p3['ports'],'current actual marked H ports')
  def xcols(j,k,copy=None):
   rr=Xj[j,h];local=list(range(3))if k==3 else list(range(3,15))
   if copy is not None:local=[v+15*copy for v in local]
   elif len(rr)==30:local+=[v+15 for v in local]
   return[xi[rr[v][1],rr[v][2]]for v in local]
  def ycols(j,k):
   rr=Yj[j,h]if j is not None else[x for x in ys if x[6]is None];local=list(range(3))if k==3 else list(range(3,15))
   if j is None:local=list(range(6))if k==3 else list(range(6,30))
   return[yi[rr[v][1],rr[v][2]]for v in local]
  for k in [3,12]:
   if p3['kind']=='double':
    W=np.array(p3['early'],dtype=np.uint8)if k==3 else V[k]
    for copy in range(2):
     cols=sum([xcols(j,k,copy)for j in ds],[])
     for q,d in enumerate(ps[k]):
      rr=sorted([x for x in xs if x[4]==d],key=key);need(len(rr)==2,'two early H owners per D');row=xi[rr[copy][1],rr[copy][2]];E[row,cols]=W[q]
   else:
    if p3['kind']=='single':xe=sum([xcols(j,k)for j in ds],[]);yl=sum([ycols(j,k)for j in ds],[])
    else:xe=xcols(p3['large'],k)+xcols(p3['small'],k);yl=ycols(p3['small'],k)+ycols(None,k)
    PE=np.array(p3['early'],dtype=np.uint8)if k==3 else V[k];PL=np.array(p3['late'],dtype=np.uint8)if k==3 else V[k];PG=np.array(p3['cross'],dtype=np.uint8)if k==3 else DV[k].copy()if p3['kind']=='partial'else np.zeros_like(V[k])
    if k==12 and p3['kind']=='partial':PG[:,2*k:]=0
    for q,d in enumerate(ps[k]):
     xr=next(x for x in xs if x[4]==d);yr=next(x for x in ys if x[4]==d);rx=xi[xr[1],xr[2]];ry=yi[yr[1],yr[2]];E[rx,xe]=PE[q];B[ry,yl]=PL[q];G[ry,xe]=PG[q]
  need(a.rank(E)==len(E)-(2 if h==642 else 0),'physical early H rank');need(not len(B)or a.rank(B)==len(B),'physical late H invertibility')
  if h in [263,642]:need(np.array_equal(E,np.array(oldpair['H'][str(h)]['physical']['word'],dtype=np.uint8)),'both original owner-bound common H words unchanged')
  physical[h]={'kind':p3['kind'],'X_owners':xs,'Y_owners':ys,'early':E.tolist(),'late':B.tolist(),'cross':G.tolist(),'ports':psall}
  for j in ds:
   if j not in donors:continue
   Q=frames[j,h];XE=np.zeros((len(xs),30),dtype=np.uint8);YL=np.zeros((len(ys),30),dtype=np.uint8);quota=len(Xj[j,h])
   for t,x in enumerate(Xj[j,h]):XE[xi[x[1],x[2]]]=Q[t]
   for t,y in enumerate(Yj[j,h]):YL[yi[y[1],y[2]]]=Q[quota+t]
   RX=a.mm(E,XE);RY=a.mm(G,XE)^a.mm(B,YL)if len(B)else np.zeros((0,30),dtype=np.uint8)
   for ii in range(120):
    if not a.planes[h]<=a.adj[ii]:continue
    xx=[q for q,x in enumerate(xs)if a.charts[x[4]]<=a.adj[ii]];yy=[q for q,x in enumerate(ys)if a.charts[x[4]]<=a.adj[ii]];need(a.rank(np.vstack([RX[xx],RY[yy]]))==30,'every full donor/receiver H section');local_checks+=1
   if a.planes[h]<=a.adj[i]:
    state=a.mm(block([maps[j][h],maps[j][h]]),LF);DX=a.mm(RX,state);DY=a.mm(RY,state)
    for ph,rs,values in [('X',xs,DX),('Y',ys,DY)]:
     for q,x in enumerate(rs):
      if x[4]==D:Ddata[dindex[ph,x[1],x[2]],8*donors.index(j):8*donors.index(j)+8]=values[q]
      elif a.charts[x[4]]<=a.adj[i]:need(not np.any(values[q]),'all other proper D packets vanish on selected space')
  print('PHYSICAL_H',h,len(E),len(B),flush=True)if h in [263,642,947]else None
 need(len(providers)==136 and local_checks==5040,'complete134 five-source H stars plus two other D parents');need(np.array_equal(Ddata,np.array(z['D_data'],dtype=np.uint8)),'literal D ingress from full source and physical H owners')
 T=np.array(z['D_word'],dtype=np.uint8);Ti=np.array(z['D_inverse'],dtype=np.uint8);need(T.shape==(35,35)and not np.any(T[:19,19:])and a.rank(T[:19,:19])==19 and a.rank(T[19:,19:])==16,'actual D phase word');need(np.array_equal(a.mm(T,Ti),np.eye(35,dtype=np.uint8)),'actual D inverse')
 outputs=[q for q,x in enumerate(downers)if x[0]=='X'and x[5]is not None and i in a.planes[x[5]]]+[q for q,x in enumerate(downers)if x[0]=='Y'and i in a.planes[x[5]]];need(outputs==z['D_output_indices']and len(outputs)==8,'actual four early and four late right flags');need(np.array_equal(a.mm(T[outputs],Ddata),np.tile(np.eye(8,dtype=np.uint8),(1,5))),'one actual eight-output identity sum on five paired spaces')
 dsections=[]
 for j in sorted(a.charts[D]):
  inn=[q for q,x in enumerate(downers)if x[3]is not None and j in a.planes[x[3]]];need(len(inn)==8,'four H input flags per geometric D donor')
  for ii in range(120):
   if not a.charts[D]<=a.adj[ii]:continue
   oo=[q for q,x in enumerate(downers)if x[5]is not None and ii in a.planes[x[5]]];need(len(oo)==8 and a.rank(T[np.ix_(oo,inn)])==8,'every geometric D section');dsections.append([j,ii])
 def binary(A):
  return np.array([[int(a.product[A[r//6,c//6],1<<(c%6)])>>(r%6)&1 for c in range(6*A.shape[1])]for r in range(6*A.shape[0])],dtype=np.uint8)
 def compile_binary(A):
  R=binary(A);n=len(R);ops=[]
  def add(t,s):R[t]^=R[s];ops.append([t,s])
  for q in range(n):
   p=q+int(np.flatnonzero(R[q:,q])[0])
   if p!=q:add(q,p);add(p,q);add(q,p)
   for r in range(n):
    if r!=q and R[r,q]:add(r,q)
  need(np.array_equal(R,np.eye(n,dtype=np.uint8)),'exact ADD elimination');return ops
 eo=compile_binary(T[:19,:19]);lo=compile_binary(T[19:,19:]);cross=binary(T[19:,:19]);crossops=np.argwhere(cross).tolist();early_state=[1<<q for q in range(114)];late_state=[1<<(114+q)for q in range(96)];cache=early_state.copy()
 for t,s in reversed(eo):early_state[t]^=early_state[s]
 for t,s in reversed(lo):late_state[t]^=late_state[s]
 for t,s in crossops:late_state[t]^=cache[s]
 expected=binary(T);actual=early_state+late_state;need(actual==[sum(int(v)<<q for q,v in enumerate(row))for row in expected],'chronological D word on all arbitrary early/late original columns')
 for nn,ops in [(114,eo),(96,lo)]:
  check=[1<<q for q in range(nn)]
  for t,s in reversed(ops):check[t]^=check[s]
  for t,s in ops:check[t]^=check[s]
  need(check==[1<<q for q in range(nn)],'pure phase restoration inverse')
 dcompiler={'cache_labels':[f'D1509-X-cache/{x[1]}/{x[2]}/{bit}'for x in downers[:19]for bit in range(6)],'early_elimination_ADDs':eo,'late_elimination_ADDs':lo,'late_cross_from_cache_ADDs':crossops,'cache_copy_ADDs':114,'INIT':114,'dirty_CLEAR':114,'forward_ADDs':len(eo)+len(lo)+114+len(crossops),'including_pure_inverse_ADDs':2*(len(eo)+len(lo))+114+len(crossops),'extra_MOVE':0}
 def save(name,value):
  raw=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();(out/name).write_bytes(gzip.compress(raw,mtime=0));return hashlib.sha256(raw).hexdigest()
 hashes={};hashes['source']=save('SOURCES.json.gz',{'maps':{str(j):{str(h):M.tolist()for h,M in vv.items()}for j,vv in maps.items()},'frames':{f'{j}/{h}':M.tolist()for(j,h),M in frames.items()},'late_parities':{str(j):{str(h):M.tolist()for h,M in vv.items()}for j,vv in late.items()},'selected_original_space':LF.tolist()});hashes['early']=save('EARLY.json.gz',early);hashes['H']=save('H-PHYSICAL.json.gz',physical);hashes['D']=save('D-WORD.json.gz',{'owners':downers,'matrix':T.tolist(),'inverse':Ti.tolist(),'ingress':Ddata.tolist(),'selected_output_indices':outputs,'section_pairs':dsections,'compiler':dcompiler});hashes['checks']=save('CHECKS.json.gz',{'source_views':source_records,'retained_H_views':retained,'propagation':propagation})
 result={'status':'PASS_ACTUAL_FIVE_SOURCE_D1509_CUT','D':D,'receiver':i,'geometric_D_donors':sorted(a.charts[D]),'native_D_donors':sorted(a.charts[D]&a.native),'supplied_donors':donors,'missing_native_D_sources':sorted((a.charts[D]&a.native)-set(donors)),'geometric_source_cuts':len(source_records),'native_source_cuts':sum(ii in a.native for j,ii in source_records),'actual_full_early_bases':early_records,'retained_geometric_common_H_views':len(retained),'retained_native_common_H_views':sum(ii in a.native for h,ii in retained),'physical_H_modules':len(providers),'full_donor_H_section_checks':local_checks,'geometric_D_section_checks':len(dsections),'native_D_section_checks':sum(j in a.native and ii in a.native for j,ii in dsections),'D_actual_owners':35,'D_phase_dimensions':[19,16],'common_paired_space_dimension':8,'selected_output_count':8,'native_bank_repeats':8,'full_bank_common_space_dimension':64,'uniform_propagation_upper_by_donor':{str(j):propagation[j]['full_upper']for j in donors},'D_compiler_counts':{k:v for k,v in dcompiler.items()if isinstance(v,int)},'unchanged_H642_paid_field_exports':16,'other_H_whole_common_readouts':False,'other_D_common_cuts':False,'complete_K_facet_return_or_invoice':False,'all111_sources':False,'new_complete_kappa':False,'payload_sha256':hashes}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['status'],315,291,72,67,136,5040,144,121,35,8,flush=True)
if __name__=='__main__':
 p=ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
