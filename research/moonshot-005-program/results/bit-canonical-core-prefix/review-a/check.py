#!/usr/bin/env python3
"""Independent native algebra and literal replay; never imports C's builder."""
import argparse,gzip,hashlib,json,runpy
from collections import defaultdict
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(b,m):
 if not b:raise ValueError(m)
def rank(rows):
 p={}
 for r in rows:
  while r:
   i=r.bit_length()-1
   if i in p:r^=p[i]
   else:p[i]=r;break
 return len(p)
def xor(rows):
 r=0
 for v in rows:r^=v
 return r
def main(a):
 raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw))
 m=runpy.run_path(str(a.geometry));replay=runpy.run_path(str(a.replayer))['replay']
 roots=[[m['F'](x)for x in n['frames'][str(n['start'][i])]['B'][0]]for i in range(111)]
 K=[sum(1<<j for j in range(111)if i==j or m['dot'](roots[i],roots[j])==0)for i in range(111)]
 indices=[0,1,2,4,8,9,14,30,59];G=[K[i]for i in indices];need(rank(K)==rank(G)==9,'native rank9')
 code=json.loads((a.author/'CODE.json').read_text());need([int(x,16)for x in code['canonical_rows_hex']]==K,'native fitting')
 coeff={xor(G[j]for j in range(9)if(mask>>j)&1):mask for mask in range(512)};need(len(coeff)==512,'basis injective')
 alpha=[coeff[k]for k in K];core=G[:3];R=[xor(core[j]for j in range(3)if(al>>j)&1)for al in alpha]
 need(code['receiver_coefficients_9']==alpha and code['receiver_core_coefficients']==[x&7 for x in alpha],'coefficient identity')
 need([int(x,16)for x in code['receiver_preload_rows_hex']]==R,'preload identity')
 groups=defaultdict(list)
 for i,r in enumerate(roots):
  supp=tuple(j for j,x in enumerate(r)if x);key=(supp,sum(x<0 for x in r)%2)if len(supp)>1 else(supp,0);groups[key].append(i)
 groups=list(groups.values());D=[sum(1<<j for j in g)for g in groups];need(len(groups)==rank(D)==36,'group partition')
 z=[row for row in coeff if row&255==0];need(len(z)==32 and rank(z)==5,'whole zero-coordinate kernel')
 need(all(all(len({(row>>j)&1 for j in g})==1 for g in groups)for row in z),'all kernel rows groupconstant')
 need(9+36-rank(K+D)==6,'C intersection D dimension6')
 masks=[3,5,9,48,465];need(rank(masks)==5 and all(xor(G[j]for j in range(9)if(c>>j)&1)in z for c in masks),'displayed kernel basis')
 def load(f):
  w=json.loads(gzip.decompress((a.author/f).read_bytes()));need(w['start']==n['start'][:222],'native starting charts');w['directions']={str(i):'down'for i in(333,334,335)};return w
 pre=load('PREFIX.json.gz');closed=load('CLOSED-PARTIAL.json.gz');pr=replay(pre,m);cr=replay(closed,m)
 want=[(1<<i)if i<111 else(1<<i)^R[i-111]for i in range(222)]
 owned={str(222+j):hex(1<<j)for j in range(111)}|{str(336+j):hex(core[j])for j in range(3)}
 need(pr['rows']==cr['rows']==want and pr['owned_rows']==owned,'all222 columns and exact live modes')
 need(pr['owned_where']==({str(222+j):n['start'][j]for j in range(111)}|{str(336+j):0 for j in range(3)}),'all actual cache locations')
 need(pr['counts']=={'INIT':117,'ADD':462,'MOVE':114,'CLEAR':3} and pr['paid_profile']=={7:111,8:3} and pr['peak_owned']==115,'prefix invoice')
 need(cr['counts']=={'INIT':117,'ADD':462,'MOVE':225,'CLEAR':117} and cr['paid_profile']=={7:222,8:3} and cr['peak_owned']==115,'closed invoice')
 need(closed['final']==n['final'][:222],'closed native endpoints')
 S=[4,8,9,14,30,73]
 def inside(c):return any(all(m['dot'](roots[i],v)==0 for v in m['rref'](pre['frames'][str(c)]['B']))for i in S)
 obs=[v for i,v in enumerate(pr['rows'])if inside(pre['final'][i])]+[int(v,16)for i,v in pr['owned_rows'].items()if inside(pr['owned_where'][i])]
 r0=rank(obs);r1=rank(obs+[(1<<i)^(1<<(111+i))for i in S]);need((r0,r1)==(216,222),'literal6cut')
 outside=[j for j in range(111)if not any(m['dot'](roots[i],roots[j])==0 for i in S)];need(outside==[4,8,9,14,30,31,73,77,88],'outside nuisance sources')
 mutants=[]
 for name,pred in [('point_copy',lambda o:o[:3]==['ADD',222,0]),('core_cache',lambda o:o[0]=='ADD'and o[1]==336),('encoder_read',lambda o:o[0]=='ADD'and o[1]==333),('Y_deposit',lambda o:o[0]=='ADD'and 111<=o[1]<222),('Hub_departure',lambda o:o[:2]==['MOVE',333])]:
  w=json.loads(json.dumps(pre));k=next(k for k,o in enumerate(w['program'])if pred(o));del w['program'][k]
  try:r=replay(w,m);bad=r['rows']!=want or r['owned_rows']!=owned
  except ValueError:bad=True
  need(bad,'mutant accepted '+name);mutants.append(name)
 out={'status':'PASS_INDEPENDENT_CANONICAL_CORE_UNIVERSAL_GAUGE_REVIEW','native_sha256':PIN,'native_rank':9,'coordinate_rank':4,'zero_coordinate_kernel_dimension':5,'C_intersection_D':6,'groups':36,'prefix_counts':pr['counts'],'closed_counts':cr['counts'],'literal_cut':{'S':S,'observation_rank':r0,'augmented_rank':r1,'deficit':r1-r0},'mutants_rejected':mutants,'scope':'Independent native algebra and C literal-word replay using A prior independently reviewed geometry/replayer; no C builder import or execution; no repeated clique census.','pins':{str(p):hashlib.sha256(p.read_bytes()).hexdigest()for p in[a.geometry,a.replayer,*[a.author/f for f in['PROOF.md','CODE.json','PREFIX.json.gz','CLOSED-PARTIAL.json.gz','build.py']]]},'new_kappa':False}
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k]for k in['status','native_rank','zero_coordinate_kernel_dimension','C_intersection_D','literal_cut']}))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for n in('native','author','geometry','replayer','output'):p.add_argument('--'+n,type=Path,required=True)
 main(p.parse_args())
