#!/usr/bin/env python3
"""Exact port routes, stage obstruction and normalizer block ranks."""
from pathlib import Path
from fractions import Fraction as F
import gzip,json,hashlib,importlib.util,sys,argparse
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
PINS={'word':'d27892c4934f9b6fa08fd10b53a665f455020e6711db9378ab01f439ede2c56c','geometry':'e8e48d62be188293677d5c2f7c9a1b104e944bff8ac97669fbaa9a70b41613c6','clifford':'2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(name,key):
 raw=(HERE/'source'/name).read_bytes();need(hashlib.sha256(raw).hexdigest()==PINS[key],'source pin');return json.loads(gzip.decompress(raw)if name.endswith('.gz')else raw)
def module():
 p=HERE/'source/clifford_exact.py';need(hashlib.sha256(p.read_bytes()).hexdigest()==PINS['clifford'],'Clifford pin')
 s=importlib.util.spec_from_file_location('route_clifford',p);m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m);return m
def dot(x,y):return(x&y).bit_count()%2
def orthobasis(q):
 B=[q];need(dot(q,q)==1 and q!=511,'odd noncharacteristic label')
 while len(B)<9:
  e=511
  for v in B:e^=v
  d=9-len(B);v=next(v for v in range(1,512)if dot(v,v)and all(dot(v,z)==0 for z in B)and(d==1 or v!=e));B.append(v)
 need(all(dot(x,y)==(i==j)for i,x in enumerate(B)for j,y in enumerate(B)),'orthonormal completion');return B[1:]
def route(q,B,s,x):
 E=[1<<(9+8*(s-1)+k)for k in range(8)];head=x&511;out=x&~(511|sum(E))
 if dot(head,q):out^=q
 for b,e in zip(B,E):
  if dot(head,b):out^=e
  if x&e:out^=b
 return out
def terms(pairs):
 out={}
 for v,c in pairs:out[v]=(out.get(v,0)+c)%4
 return {v:c for v,c in out.items()if v and c}
def sub(a,b):return terms(list(a.items())+[(v,-c)for v,c in b.items()])
def phase(p,z):return sum(c*dot(v,z)for v,c in p.items())%4
def linear_translation(p,n):
 axes=[1<<i for i in range(n)];one=[phase(p,z)for z in axes];need(all(c%2==0 for c in one),'ordinary even phase')
 need(all(phase(p,x|y)==(one[i]+one[j])%4 for i,x in enumerate(axes)for j,y in enumerate(axes)if i<j),'no quadratic phase remains')
 return sum(x for x,c in zip(axes,one)if c==2)
def applyroute(p,q,B,s):return terms((route(q,B,s,v),c)for v,c in p.items())
def addrow(a,b,c):
 z=dict(a)
 for j,v in b.items():
  u=z.get(j,F(0))+c*v
  if u:z[j]=u
  else:z.pop(j,None)
 return z
def actual_R(w):
 n=w['public'];rows=[{j:F(1)}for j in range(n)];roles=w['logical_involution']['role_map'];P=w['logical_involution']['ports']
 for e in w['program']:
  if e[0]=='ADD':rows[e[1]]=addrow(rows[e[1]],rows[e[2]],F(e[3]))
  else:need(e[0]=='MOVE','owner-free R0 alphabet')
 R={}
 for h in P:
  x,y,b,d=[int(roles[k][str(h)])for k in ['X','Y','B','D']]
  need(rows[x]=={x:F(1)}and rows[d]=={d:F(1)},'original X/D')
  rr=dict(rows[y]);need(rr.pop(y)==1,'arbitrary Y baseline')
  R[h]={j:rr[int(roles['X'][str(j)])]for j in P if int(roles['X'][str(j)])in rr}
  need(rr=={int(roles['X'][str(j)]):v for j,v in R[h].items()},'no extra forward dependence')
  need(len(R[h])==4 and all(abs(v)==F(1,2)for v in R[h].values()),'four half-Hadamard contacts')
 for h in P:
  b=int(roles['B'][str(h)]);want={b:F(1)};want.update({int(roles['D'][str(j)]):-R[j][h]for j in P if h in R[j]});need(rows[b]==want,'paired reverse row')
 for h in P:
  need(all(R[h].get(j,F(0))==R[j].get(h,F(0)) for j in P),'symmetric exact R0')
  squared={}
  for j,v in R[h].items():squared=addrow(squared,R[j],v)
  need(squared=={h:F(1)},'exact R0 involution')
 return R
def main(out):
 w=load('R0-WORD.json.gz','word');g=load('GEOMETRY.json','geometry');c=module();R=actual_R(w)
 q={int(h):v for h,v in g['normal_by_port'].items()};bases={h:orthobasis(v)for h,v in q.items()};records=[];maps={}
 for s in [1,2]:
  n=9+8*s;axes=[1<<i for i in range(n)];old=terms((x,1)for x in axes[:9+8*(s-1)]);allp=terms((x,1)for x in axes);spec=terms((x,1)for x in axes[9:]);fresh=terms((x,1)for x in axes[-8:])
  for h in sorted(q):
   v=q[h];B=bases[h];f=lambda x:route(v,B,s,x)
   need(all(f(f(x))==x for x in axes)and f(v)==v,'route involution fixes q')
   need(all(dot(f(x),f(y))==(i==j)for i,x in enumerate(axes)for j,y in enumerate(axes)),'route orthogonal')
   xin=terms(list(spec.items())+[(v,1)]);yin=spec;xout=allp;yout=sub(allp,{v:1})
   tin=linear_translation(sub(xin,applyroute(old,v,B,s)),n)
   tin_y=linear_translation(sub(yin,applyroute(sub(old,{v:1}),v,B,s)),n)
   tout=linear_translation(sub(allp,applyroute(xout,v,B,s)),n)
   tout_y=linear_translation(sub(sub(allp,{v:1}),applyroute(yout,v,B,s)),n)
   need(tin==tin_y and tout==tout_y,'identical adapters on both pair fields')
   body=sub(terms((1<<i,1)for i in range(9)),{v:1})
   shift=linear_translation(sub(fresh,applyroute(body,v,B,s)),n)
   need(shift==tout^f(tin),'literal O B M = D including translation')
   need(shift!=(tout^1)^f(tin),'wrong translation control')
   maps[s,h]=dict(input_translation=tin,output_translation=tout)
   records.append(dict(stage=s,port=h,normal=v,orthogonal_complement=B,**maps[s,h]))
 witnesses=[];DG=c.fourier(17,range(9,17))
 for i in sorted(R):
  for j,a in sorted(R[i].items()):
   need(i!=j and dot(q[i],q[j])==0,'cross-half orthogonal distinct labels')
   bi,bj=bases[i],bases[j];pi=lambda z:route(q[i],bi,1,z);pj=lambda z:route(q[j],bj,1,z)
   k=next(k for k,b in enumerate(bi)if dot(q[j],b));z=1<<(9+k);image=pj(pi(z))
   need(image&511==q[j],'off-diagonal permutation creates head component')
   need((image>>9).bit_count()%2==0,'fresh parity changes')
   need((image>>9).bit_count()%4!=1,'own-body commutator nonzero')
   stage2=route(q[j],bj,2,route(q[i],bi,2,z));need(stage2==z and image!=z,'stage1 and stage2 differ')
   cols=[pi(pj(1<<k))for k in range(17)];P=c.perm(17,c.transpose(cols,17));op=DG.adjoint().then(P).then(DG)
   rank=c.rank([x for x,zz,p in op.tab[17:]]);need(rank==2,'output-normalizer block Gaussian rank2')
   witnesses.append(dict(output_port=i,input_port=j,coefficient=str(a),fresh_axis=k,frequency=z,permuted_frequency=image,block_gaussian_rank=rank))
 need(len(witnesses)==448,'all nonzero R0 blocks covered')
 result=dict(status='PASS_LITERAL_112_PORT_ADAPTER_INTERFACE',source_pins=PINS,port_count=112,stages_checked=[1,2],route_records=records,
  nonzero_R_blocks=witnesses,ordinary_boundary_normalizers='NORMALIZERS.json',
  exact_embedded_query='A_s=M_s^-1 (Q R0) M_s',stage_dependence=True,own_body_commutation=False,
  paid_common_service='N=Q^-1 R0 Q; T_s=O_s lambda(Q^2) N O_s^-1',
  scope='Source-bound finite adapter checks supporting universal algebra in PROOF.md. No complete service N or new kappa.')
 out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=HERE/'ROUTES.json');main(a.parse_args().out)
