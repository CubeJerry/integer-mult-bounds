#!/usr/bin/env python3
"""Exact source and rational representation witness for joint endpoint capacity."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
import sympy as sp
ENGINE='research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
SHA='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'

def run(repo,out):
 ep=repo/ENGINE;assert hashlib.sha256(ep.read_bytes()).hexdigest()==SHA
 spec=importlib.util.spec_from_file_location('row_capacity_exact_engine',ep);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
 I=m.eye(16);Z=m.zero(16)
 def frac(x,c):
  c=F(c);assert c.denominator&(c.denominator-1)==0;y=x.scale((c.numerator,0));return m.M(y.a,y.k+c.denominator.bit_length()-1).norm()
 def pp(x):return frac(I+x,F(1,2))
 def nn(x):return frac(I+x.scale((-1,0)),F(1,2))
 def table(dest,phase):return m.monomial([dest(*[(x>>j)&1 for j in range(4)]) for x in range(16)],[phase(*[(x>>j)&1 for j in range(4)])%4 for x in range(16)])
 R=table(lambda a,b,c,d:b+2*c+4*d+8*a,lambda a,b,c,d:2*a*b*d);Xb=m.monomial([x^2 for x in range(16)],[0]*16)
 A=frac(I.scale((1,1))+Xb.scale((1,-1)),F(1,2))@R
 s=table(lambda a,b,c,d:a+2*b+4*d+8*c,lambda a,b,c,d:0);t=m.monomial([x^12 for x in range(16)],[0]*16)
 U=A.power(2);s1=A.star()@s@A;t1=A.star()@t@A
 h0=A@t@A.star();h1=U@t@U.star();h2=U@s1@t@s1@U.star()
 assert s@s==t@t==I and s@t==t@s
 assert s1==table(lambda a,b,c,d:d+2*b+4*c+8*a,lambda a,b,c,d:0)
 for h in [s1,t1,h0,h1,h2]:assert h@h==I and h.k==0 and m.gaussian_rank(h)==0
 assert U@t1@U.star()==h0
 assert m.gaussian_rank(U@s1@U.star())==2
 # Literal multiplicative identities certify the two distinct collective cosets.
 assert U@t==h1@U
 assert U@s1@t==h2@U@s1
 assert U@s1@t1==h0@U@s1
 ps,ns,pt,nt=pp(s),nn(s),pp(t),nn(t);ee=ns@pt;ff=ns@nt
 C=m.block([[ps,ee.scale((-1,0)),ff.scale((-1,0))],[pp(s@t),Z,I+ff.scale((-1,0))],[pt,I+ee.scale((-1,0)),Z]])
 L=m.block([[A,Z,Z],[I,A,Z],[Z,Z,I]]);UN=m.block([[A,A.power(2).scale((-1,0)),Z],[Z,A,Z],[Z,Z,I]])
 Q0=m.block([[pt,Z,nt],[Z,I,Z],[nt,Z,pt]])
 assert Q0@Q0==m.eye(48)
 # C is the row exchange of the already reviewed four-sector unit; verify inverse
 # from its sector matrices without importing the older checker.
 sectors={(u,v):pp(s.scale((u,0)))@pp(t.scale((v,0))) for u in [1,-1] for v in [1,-1]}
 vals={(1,1):sp.Matrix([[1,0,0],[1,0,1],[1,1,0]]),(1,-1):sp.Matrix([[1,0,0],[0,0,1],[0,1,0]]),(-1,1):sp.Matrix([[0,-1,0],[0,0,1],[1,0,0]]),(-1,-1):sp.Matrix([[0,0,-1],[1,0,0],[0,1,0]])}
 invblocks=[[Z for _ in range(3)] for _ in range(3)]
 for ch,P in sectors.items():
  vi=vals[ch].inv()
  for i in range(3):
   for j in range(3):invblocks[i][j]=invblocks[i][j]+P.scale((int(vi[i,j]),0))
 Ci=m.block(invblocks);assert C@Ci==Ci@C==m.eye(48)
 # Width-one replay is a control; the all-width identities are the literal
 # factor equalities above and the displayed formal block expansion.
 Efull=L@C@UN@Q0@L
 M0,M1,M2=nn(h0),nn(h1),nn(h2);P0=pp(h0)
 c1=[Z,ps@M0+P0,pt@M0]
 c20=[M1,M1,Z];c21=[M2,h0@M2,Z]
 for i in range(3):
  rhs=c1[i]@A+frac(c20[i]@U+c21[i]@U@s1,F(1,2))
  for r in range(16):
   for j in range(16):assert F(Efull.a[16*i+r][32+j][0],1<<Efull.k)==F(rhs.a[r][j][0],1<<rhs.k) and F(Efull.a[16*i+r][32+j][1],1<<Efull.k)==F(rhs.a[r][j][1],1<<rhs.k)
 def mono_table(h):
  roots=[m.O,m.II,(-1,0),(0,-1)];p=[];q=[]
  for j in range(16):
   nz=[i for i in range(16) if h.a[i][j]!=m.Z];assert len(nz)==1;p.append(nz[0]);q.append(roots.index(h.a[nz[0]][j]))
  return {'destinations':p,'input_phase_mod4':q}
 def standard(h):
  p=mono_table(h)['destinations'];D=sp.zeros(15)
  for j in range(15):
   if p[j]<15:D[p[j],j]+=1
   if p[15]<15:D[p[15],j]-=1
  return D
 J=sp.eye(15);O=sp.zeros(15);S,T,H0,H1,H2=map(standard,[s,t,h0,h1,h2])
 for h in [S,T,H0,H1,H2]:assert h*h==J
 PS=(J+S)/2;PT=(J+T)/2;MH0=(J-H0)/2;PH0=(J+H0)/2;MH1=(J-H1)/2;MH2=(J-H2)/2
 B=PS*MH0+PH0;D=PT*MH0
 K1=O.col_join(B).col_join(D)
 K2=MH1.row_join(MH2).col_join(MH1.row_join(H0*MH2)).col_join(O.row_join(O))
 ranks={'one_whole':K1.rank(),'one_third':D.rank(),'two_whole':K2.rank(),'two_third':0}
 assert ranks=={'one_whole':15,'one_third':4,'two_whole':13,'two_third':0}
 obstruction=ranks['one_whole']-ranks['one_third']+ranks['two_whole'];assert obstruction==24>15
 # Controls: individual component capacity passes; allowing the quartic encoder
 # outside the prescribed kernel removes this numerical contradiction (24<=30).
 assert max(ranks['one_whole'],ranks['two_whole'])<=15 and obstruction<=30
 assert (O.col_join(PS*MH0).col_join(D)).rank()!=ranks['one_whole']
 out.mkdir(parents=True,exist_ok=True)
 result={'status':'PASS_EXACT_JOINT_ROW_SUPPORT_ENDPOINT_GATE','engine_sha256':SHA,'representation':'15-dimensional standard permutation representation of the full projective ordinary monomial group; phases discarded','exact_rational_ranks':ranks,'required_joint_upper_bound':15,'actual_joint_value':obstruction,'scope':'all ordinary completions with Calt and Q[:,2]=(Nt,0,Pt), including right basis changes; not all Calt columns','literal_conjugates':{n:mono_table(h) for n,h in [('s',s),('t',t),('s1',s1),('h0',h0),('h1',h1),('h2',h2)]},'controls':{'actual_column_completion_and_inverse':True,'Calt_unit_inverse':True,'two_distinct_class2_left_cosets':True,'individual_component_tests_pass':True,'quartic_support_premise_needed':True,'omitted_P0_term_detected':True},'new_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 manifest={'source':ENGINE,'sha256':SHA,'source_remote_commit':'93b11dd75d7ffda723204bd212e5728cbea95592','files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_name('PROOF.md'),out/'RESULT.json']}}
 (out/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n');print(result['status'],ranks,'joint',obstruction,'>',15)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();run(a.repo,a.out)
