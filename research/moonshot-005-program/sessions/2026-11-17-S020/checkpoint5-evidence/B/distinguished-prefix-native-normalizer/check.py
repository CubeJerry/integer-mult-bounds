#!/usr/bin/env python3
"""Exact paid prefix compiler, arbitrary-bank restoration and native gauges."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'

def run(repo,out):
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('prefix_normalizer_exact',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 I=m.eye(16);Z=m.zero(16)
 def cmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
 def cinv(a):
  norm=a[0]*a[0]+a[1]*a[1];assert norm;return (a[0]/norm,-a[1]/norm)
 def scale(x,c):
  re,im=map(F,c);den=max(re.denominator,im.denominator);assert den&(den-1)==0
  y=x.scale((int(re*den),int(im*den)));return m.M(y.a,y.k+den.bit_length()-1).norm()
 def tab(dest,phase):return m.monomial([dest(*[(x>>k)&1 for k in range(4)]) for x in range(16)],[phase(*[(x>>k)&1 for k in range(4)])%4 for x in range(16)])
 R=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);X=m.monomial([x^2 for x in range(16)],[0]*16)
 Zb=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:2*b);Db=tab(lambda a,b,c,d:a+2*b+4*c+8*d,lambda a,b,c,d:b)
 Cb=scale(I,(F(1,2),F(1,2)))+scale(X,(F(1,2),F(-1,2)));A=Cb@R
 mon={'I':I,'X':X,'Z':Zb,'ZX':Zb@X,'R':R,'Ri':R.star(),'D':Db,'Di':Db.star()}
 for x in mon.values():assert x.k==0 and m.gaussian_rank(x)==0 and x@x.star()==I
 def shear(ws,target,source,terms):
  for name,c in terms:
   c=tuple(map(F,c));assert c!=(0,0)
   if name!='I':ws.append({'op':'MONO','bank':source,'name':name,'inverse':False})
   ws.append({'op':'SCALE','bank':source,'coefficient':list(map(str,c))});ws.append({'op':'ADD','target':target,'source':source})
   ws.append({'op':'SCALE','bank':source,'coefficient':list(map(str,cinv(c)))})
   if name!='I':ws.append({'op':'MONO','bank':source,'name':name,'inverse':True})
 def local(ws,u,v,lam):
  P=[('X',cmul(lam,(F(1,2),0))),('ZX',cmul(lam,(F((-1)**u,2),0)))];Q=[('I',(F(1,2),0)),('Z',(F((-1)**v,2),0))]
  neg=lambda terms:[(name,(-c[0],-c[1])) for name,c in terms]
  for target,source,terms in [(1,0,neg(Q)),(0,1,neg(P)),(1,0,Q),(0,1,P)]:shear(ws,target,source,terms)
 words=[{'op':'MONO','bank':0,'name':'R','inverse':False},{'op':'MONO','bank':0,'name':'D','inverse':False}]
 for u,v,lam in [(0,1,(0,-1)),(1,0,(F(1,2),F(-1,2))),(0,1,(-1,0))]:local(words,u,v,lam)
 inverse=[]
 for u,v,lam in [(0,1,(1,0)),(1,0,(F(-1,2),F(1,2))),(0,1,(0,1))]:local(inverse,u,v,lam)
 inverse.extend([{'op':'MONO','bank':0,'name':'D','inverse':True},{'op':'MONO','bank':0,'name':'R','inverse':True}])
 def replay(ws,omit=None):
  b=[[I,Z],[Z,I]];bound=F(1)
  for k,op in enumerate(ws):
   if k==omit:continue
   if op['op']=='ADD':
    d,s=op['target'],op['source'];b[d]=[x+y for x,y in zip(b[d],b[s])]
   elif op['op']=='SCALE':b[op['bank']]=[scale(x,tuple(map(F,op['coefficient']))) for x in b[op['bank']]]
   else:
    g=mon[op['name']];g=g.star() if op['inverse'] else g;b[op['bank']]=[g@x for x in b[op['bank']]]
   for rr in b:
    for j in range(16):bound=max(bound,sum(F(abs(v[0])+abs(v[1]),1<<x.k) for x in rr for v in x.a[j]))
  return m.block(b),bound
 want=m.diagonal([A,I]);wanti=m.diagonal([A.star(),I]);got,pb=replay(words);goti,pbi=replay(inverse)
 assert got==want and goti==wanti and got@goti==goti@got==m.eye(32)
 counts=dict(Counter(op['op'] for op in words));icounts=dict(Counter(op['op'] for op in inverse));assert counts==icounts=={'MONO':38,'SCALE':48,'ADD':24}
 for ws,w in [(words,want),(inverse,wanti)]:
  for k,op in enumerate(ws):
   if op['op']=='ADD':assert replay(ws,k)[0]!=w
 controls=[]
 for V in [1,2]:
  tail=m.eye(16**(V-1));p=A.tensor(tail);b=I.tensor(A.tp(V-1));a=A.tp(V);iv=m.eye(16**V);zv=m.zero(16**V)
  assert p@b==b@p==a
  left=m.diagonal([p.star(),iv]);right=m.diagonal([iv,p.star()])
  la=m.block([[a,zv],[iv,a]]);lb=m.block([[b,zv],[iv,b]])
  ua=m.block([[a,(a@a).scale((-1,0))],[zv,a]]);ub=m.block([[b,(b@b).scale((-1,0))],[zv,b]])
  assert left@la@right==lb and left@ua@right==ub
  assert m.diagonal([p,iv])@m.diagonal([p.star(),iv])==m.eye(2*16**V)
  controls.append({'width':V,'native_all_input_columns':2*16**V,'lower_and_upper_normalized':True,'borrowed_bank_restored_by_local_word':True})
 out.mkdir(parents=True,exist_ok=True)
 result={'status':'PASS_PAID_DISTINGUISHED_PREFIX_NATIVE_NORMALIZER','scope':'local declared primitive compiler and native gauge; no complete endpoint/supplier','counts_forward':counts,'counts_inverse':icounts,'prefix_gaussian_l1_forward':str(pb),'prefix_gaussian_l1_inverse':str(pbi),'uniform_prefix_bound':str(max(pb,pbi)),'primitive_omitted_ADD_failures':48,'all_width_basis':'fixed-prefix commutator identity and tensoring identities','width_controls':controls,'one_normalized_native_additional':{'ADD':48,'SCALE':96,'MONO':76},'three_normalized_natives_additional':{'ADD':144,'SCALE':288,'MONO':228},'new_gaussian_queries':0,'new_owners':0,'new_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(out/'WORDS.json').write_text(json.dumps({'forward':words,'inverse':inverse},indent=2)+'\n')
 manifest={'engine':ENGINE,'engine_sha256':SHA,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json',out/'WORDS.json']}}
 (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],counts,'prefix',pb,pbi)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();run(args.repo,args.out)
