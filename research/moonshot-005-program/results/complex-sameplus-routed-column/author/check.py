#!/usr/bin/env python3
"""Exact changed-source units and one complete arbitrary endpoint column."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

PINS={
 'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py':
 '1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91',
 'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint10-evidence/B/return-clock-source-interface/PROOF.md':
 '82c0dec112b3f9eaf0a06cbf9b75c8b1be49ec70cb68d69f25c1cb0e7b778270',
}

def run(repo,out):
 for name,pin in PINS.items():assert hashlib.sha256((repo/name).read_bytes()).hexdigest()==pin
 spec=importlib.util.spec_from_file_location('sameplus_routed_exact',repo/next(iter(PINS)))
 m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 def sc(x,v):
  v=F(v);assert not v.denominator&(v.denominator-1)
  q=x.scale((v.numerator,0));return m.M(q.a,q.k+v.denominator.bit_length()-1).norm()
 def tab(dest,phase):
  bs=[tuple((x>>k)&1 for k in range(4)) for x in range(16)]
  return m.monomial([dest(*x) for x in bs],[phase(*x)%4 for x in bs])
 I16=m.eye(16);R=tab(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d)
 Xb=m.monomial([x^2 for x in range(16)],[0]*16)
 A=sc(I16.scale((1,1))+Xb.scale((1,-1)),F(1,2))@R
 s=tab(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0)
 s1=tab(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0)
 s2=tab(lambda a,b,c,d:b+2*a+4*c+8*d,lambda a,b,c,d:0)
 assert A.star()@s@A==s1 and A.power(-2)@s@A.power(2)==s2
 assert s@A@R==A@R@s2
 # Verify the literal R^2 address and phase proof independently of the formula.
 R2=tab(lambda a,b,c,d:c+2*d+4*a+8*b,lambda a,b,c,d:2*a*b*(c+d))
 assert R@R==R2 and s@R2==R2@s2
 I2=m.eye(2);Zsig=m.monomial([0,1],[0,2]);Xsig=m.monomial([1,0],[0,0])
 a=I2.tensor(A);R0=I2.tensor(R);S=Zsig.tensor(s);S2=Zsig.tensor(s2);X=Xsig.tensor(I16)
 d=a.n;I=m.eye(d);Z=m.zero(d)
 P=sc(I+S,F(1,2));N=I+sc(P,-1);P2=sc(I+S2,F(1,2));N2=I+sc(P2,-1)
 p=R0@N2;z=X@P2
 assert S@X==sc(X@S,-1) and S2@X==sc(X@S2,-1)
 assert P@a@p==P@a.power(2)@z==Z
 assert N@a@p==a@p and N@a.power(2)@z==a.power(2)@z
 assert p.star()@p==N2 and z.star()@z==P2

 def sm(xs):
  q=Z
  for x in xs:q=q+x
  return q
 def mm(x,y):return [[sm(x[i][k]@y[k][j] for k in range(len(y))) for j in range(len(y[0]))] for i in range(len(x))]
 def ident():return [[I if i==j else Z for j in range(3)] for i in range(3)]
 def shear(i,j,c):
  q=ident();q[i][j]=sc(I,c);return q
 def swmat(i,j,proj):
  q=ident();q[i][i]=q[j][j]=I+sc(proj,-1);q[i][j]=q[j][i]=proj;return q
 def diag(gs):return [[gs[i] if i==j else Z for j in range(3)] for i in range(3)]
 C=[[P,Z,sc(N,-1)],[P,I,sc(N,-1)],[N,Z,P]]
 Q=mm(mm(diag([R0,X,I]),swmat(1,2,P2)),swmat(0,2,N2))
 O=mm(shear(1,0,1),shear(2,1,-1))
 In=mm(diag([I,X,R0]),swmat(1,2,P2))
 assert [Q[i][2] for i in range(3)]==[p,z,Z]
 assert [In[i][2] for i in range(3)]==[Z,z,p]
 Cinv=mm([[P,Z,N],[Z,I,Z],[sc(N,-1),Z,P]],shear(1,0,-1))
 Qinv=mm(mm(swmat(0,2,N2),swmat(1,2,P2)),diag([R0.star(),X,I]))
 Oinv=mm(shear(2,1,1),shear(1,0,-1))
 Iinv=mm(swmat(1,2,P2),diag([I,X,R0.star()]))
 wanted={'C':(C,Cinv),'Q0':(Q,Qinv),'O':(O,Oinv),'I0':(In,Iinv)}
 for x,y in wanted.values():assert mm(x,y)==mm(y,x)==ident()

 L=[[a,Z,Z],[I,a,Z],[Z,Z,I]];U=[[a,sc(a.power(2),-1),Z],[Z,a,Z],[Z,Z,I]]
 mid=mm(mm(L,C),U);E=mm(mm(mid,Q),L);D=diag([a.power(4),a.power(2),a])
 target=mm(mm(O,D),In)
 assert [E[i][2] for i in range(3)]==[target[i][2] for i in range(3)]
 assert [mm(shear(1,0,-1),mm(mid,Q))[i][2] for i in range(3)]==[Z,a.power(2)@z,a@p+sc(a.power(2)@z,-1)]
 assert mm(Oinv,mid)==[[a@P@a,sc(a@P@a.power(2),-1),sc(a@N,-1)],
                      [P@a,N@a.power(2),sc(N,-1)],
                      [a,Z,S]]
 defect=[[E[i][j]+sc(target[i][j],-1) for j in range(3)] for i in range(3)]
 nonzero=[sum(v!=(0,0) for i in range(3) for row in defect[i][j].a for v in row) for j in range(3)]
 assert nonzero[2]==0 and any(nonzero[:2])

 def AD(i,j):return {'op':'ADD','target':i,'source':j}
 def SC(i,c):return {'op':'SCALE','bank':i,'coefficient':str(c)}
 def MO(i,g):return {'op':'MONO','bank':i,'name':g}
 def h2(i,j,inv=False):return [AD(i,j),SC(j,-2),AD(j,i)]+([SC(i,F(1,2)),SC(j,F(1,2))] if inv else [])
 def swap(i,j,g):return h2(i,j)+[MO(j,g)]+h2(i,j,True)
 def rot(i,j,g,inv=False):return [MO(i,g)]+swap(i,j,g) if inv else swap(i,j,g)+[MO(i,g)]
 def add(i,j,sgn=1):return [AD(i,j)] if sgn==1 else [SC(j,-1),AD(i,j),SC(j,-1)]
 words={
  'C':{'forward':rot(0,2,'S')+add(1,0),'inverse':add(1,0,-1)+rot(0,2,'S',True)},
  'Q0':{'forward':swap(0,2,'S2')+swap(1,2,'minus_S2')+[MO(0,'R0'),MO(1,'X')],
        'inverse':[MO(1,'X'),MO(0,'R0_inverse')]+swap(1,2,'minus_S2')+swap(0,2,'S2')},
  'O':{'forward':add(2,1,-1)+add(1,0),'inverse':add(1,0,-1)+add(2,1)},
  'I0':{'forward':swap(1,2,'minus_S2')+[MO(1,'X'),MO(2,'R0')],
        'inverse':[MO(2,'R0_inverse'),MO(1,'X')]+swap(1,2,'minus_S2')},
 }
 monos={'S':S,'S2':S2,'minus_S2':sc(S2,-1),'X':X,'R0':R0,'R0_inverse':R0.star()}
 def replay(word,omit=None):
  q=ident();bounds=[F(1)]*3;peak=F(1)
  for k,op in enumerate(word):
   if k==omit:continue
   if op['op']=='ADD':
    i,j=op['target'],op['source'];q[i]=[x+y for x,y in zip(q[i],q[j])];bounds[i]+=bounds[j]
   elif op['op']=='SCALE':
    i=op['bank'];c=F(op['coefficient']);q[i]=[sc(x,c) for x in q[i]];bounds[i]*=abs(c)
   else:
    i=op['bank'];q[i]=[monos[op['name']]@x for x in q[i]]
   peak=max(peak,*bounds)
  return q,peak
 receipts={};omissions=0
 for name,dirs in words.items():
  receipts[name]={}
  for ind,(direction,word) in enumerate(dirs.items()):
   actual,peak=replay(word);assert actual==wanted[name][ind]
   counts=dict(Counter(op['op'] for op in word))
   for k,op in enumerate(word):
    if op['op']=='ADD':assert replay(word,k)[0]!=actual;omissions+=1
   receipts[name][direction]={**{k:counts.get(k,0) for k in ['ADD','SCALE','MONO']},'uniform_triangle_prefix_bound':str(peak)}
 assert omissions==38
 assert {k:receipts['C']['forward'][k] for k in ['ADD','SCALE','MONO']}=={'ADD':5,'SCALE':4,'MONO':2}
 assert {k:receipts['C']['inverse'][k] for k in ['ADD','SCALE','MONO']}=={'ADD':5,'SCALE':6,'MONO':2}

 # Source-specific controls distinguish a genuine fixed sign bit and routing R.
 bad_p=N2
 bad_z=P2
 assert P@a@bad_p!=Z and P@a.power(2)@bad_z!=Z
 assert mm(mid,[[bad_p],[z],[Z]])!=mm(O,[[Z],[a.power(2)@z],[a@bad_p]])
 assert mm(mid,[[p],[bad_z],[Z]])!=mm(O,[[Z],[a.power(2)@bad_z],[a@p]])
 result={
  'status':'PASS_SAMEPLUS_ROUTED_ENDPOINT_COLUMN',
  'claim':'actual C,Q0,O,I0 units and full last-input-column endpoint identity; other columns open',
  'new_source_transport':'SWAP_cd A R = A R SWAP_ab, with literal cubic phases',
  'paid_fixed_prefix_normalization_retained':True,
  'active_prefix_bits':1,
  'tail_width_checked':1,
  'all_unit_input_columns':3*d,
  'both_inverse_orders':True,
  'complete_retained_column_dimension':d,
  'whole_last_column_has_only_gaussian_classes':[1,2],
  'actual_independent_endpoint_units':True,
  'quartic_input_component_of_verified_column':0,
  'full_endpoint_defect_nonzero_entries_by_input_bank':nonzero,
  'full_endpoint_claimed':False,
  'ADD_omission_controls':omissions,
  'omitted_R_and_omitted_prefix_flip_rejected':True,
  'receipts':receipts,
  'new_gaussian_queries':0,'new_owners':0,'new_kappa':False,
 }
 out.mkdir(parents=True,exist_ok=True)
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 tables={}
 for name,g in monos.items():
  destinations=[];phases=[];roots=[(1,0),(0,1),(-1,0),(0,-1)]
  assert g.k==0
  for j in range(d):
   i=next(i for i in range(d) if g.a[i][j]!=(0,0));destinations.append(i);phases.append(roots.index(g.a[i][j]))
  tables[name]={'destinations':destinations,'input_phases_mod4':phases}
 (out/'WORDS.json').write_text(json.dumps({'primitive_words':words,'literal_prefix_tail1_monomials':tables},indent=2)+'\n')
 files={'check.py':Path(__file__),'PROOF.md':Path(__file__).with_name('PROOF.md'),
        'output/RESULT.json':out/'RESULT.json','output/WORDS.json':out/'WORDS.json'}
 (out/'MANIFEST.json').write_text(json.dumps({'dependencies':PINS,'files':{k:hashlib.sha256(p.read_bytes()).hexdigest() for k,p in files.items()}},indent=2)+'\n')
 print(result['status'],'all unit columns',3*d,'ADD controls',omissions,'unfilled-input defects',nonzero,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
 a=p.parse_args();run(a.repo,a.out)
