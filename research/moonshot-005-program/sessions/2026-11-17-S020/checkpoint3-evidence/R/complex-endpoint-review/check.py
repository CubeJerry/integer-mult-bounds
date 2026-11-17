"""Independent literal premises and C4 word audit for two scoped endpoint gates."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import Counter
import argparse,hashlib,importlib.util,json

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--c4-package',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 helper=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint2-evidence/C/klein-interface-review/check.py'
 assert hashlib.sha256(helper.read_bytes()).hexdigest()=='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
 spec=importlib.util.spec_from_file_location('separate_qi_arithmetic',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 I=m.eye();Z=[{}for _ in range(16)]
 def mul(*terms):
  out=I
  for term in terms:out=m.mm(out,term)
  return out
 def plus(B):return m.scale(m.add(I,B),F(1,2))
 def minus(B):return m.scale(m.add(I,m.scale(B,-1)),F(1,2))
 R=m.mono([[((x>>1)&1)+2*((x>>2)&1)+4*((x>>3)&1)+8*(x&1),2*((x&1)*((x>>1)&1)*((x>>3)&1))]for x in range(16)])
 Xb=m.mono([[x^2,0]for x in range(16)])
 A=mul(m.add(m.scale(I,(F(1,2),F(1,2))),m.scale(Xb,(F(1,2),F(-1,2)))),R);U=mul(A,A)
 assert mul(m.star(A),A)==I
 s=m.mono([[(x&3)|((x&4)<<1)|((x&8)>>1),0]for x in range(16)]);t=m.mono([[x^12,0]for x in range(16)])
 s1=mul(m.star(A),s,A);t1=mul(m.star(A),t,A);s2=mul(m.star(U),s,U);t2=mul(m.star(U),t,U);tp=mul(A,t,m.star(A))
 for M in [s1,t1,s2,t2,tp]:m.table(M);assert mul(M,M)==I
 assert mul(s1,t1)==mul(t1,s1)
 e=mul(plus(s1),minus(t1));P=plus(tp);M=minus(tp)
 assert mul(e,e)==e and m.star(e)==e and m.col_rank(e)==4
 nonordinary=mul(U,s1,m.star(U));assert set(map(len,nonordinary))=={4}
 assert mul(U,t1,m.star(U))==tp
 assert mul(U,e)==m.scale(m.add(mul(M,U),mul(M,U,s1)),F(1,2))
 assert mul(P,U,e)==Z
 h=m.mono([[x^(4*int((x&1)==((x>>3)&1))),((1-2*((x>>2)&1))*int((x&1)==((x>>3)&1)))%4]for x in range(16)])
 assert mul(h,h)==I and mul(h,s1)==mul(s1,h)and mul(h,t1)==mul(t1,h)
 N0=mul(minus(s1),plus(h));R1=mul(minus(s1),minus(t1));assert N0==R1 and mul(N0,e)==Z
 G=m.mono([[dest,2 if x in[13,15]else 0]for x,dest in enumerate([0,1,3,5,7,9,4,13,2,8,6,11,10,15,14,12])])
 for B in [mul(U,h,m.star(U)),mul(U,s1,t2,s1,m.star(U))]:m.table(B)
 assert mul(G,s1,m.star(G))==s2 and mul(G,h,m.star(G))==mul(s2,t2)
 R2=mul(minus(s2),minus(t2));assert mul(G,N0,m.star(G))==R2
 return_g=mul(m.star(R),Xb);m.table(return_g)
 assert mul(A,return_g,A)==R
 V=mul(G,N0);pp=m.add(I,m.scale(N0,-1));E1=mul(minus(s1),plus(t1))
 q2=[mul(U,m.add(mul(plus(s1),pp),m.scale(mul(E1,V),-1))),mul(U,m.add(mul(plus(t1),pp),mul(m.add(I,m.scale(E1,-1)),V))),m.scale(mul(U,V),-1)]
 assert [mul(B,e)for B in q2]==[mul(U,e),Z,Z]
 traces=[]
 for exponents in product([0,1],repeat=3):
  B=mul(*(T if exponent else I for T,exponent in zip([s1,t1,h],exponents)));tr=m.trace(B);assert tr[1]==0
  traces.append({'exponents':exponents,'trace':int(tr[0])})
 ranks=[]
 for width in range(1,7):
  kernel=sum((-1)**sum(x['exponents'])*x['trace']**width for x in traces)//8
  assert kernel==(16**width-2*8**width)//8
  ranks.append({'width':width,'quadratic_kernel':kernel,'quadratic_rank':16**width-kernel})
 assert ranks[1]['quadratic_kernel']==16
 # Every four-source path uses C's first column. This is a formal path census.
 Ldeg={(0,0):1,(1,0):0,(1,1):1,(2,2):0};Udeg={(0,0):1,(0,1):2,(1,1):1,(2,2):0}
 def paths(mask):
  maximum=[0,0,0];quartic=set()
  for i,j in product(range(3),repeat=2):
   for aa,bb,cc,dd in product(range(3),repeat=4):
    if(i,aa)not in Ldeg or(aa,bb)not in mask or(bb,cc)not in Udeg or(dd,j)not in Ldeg:continue
    degree=Ldeg[i,aa]+Udeg[bb,cc]+Ldeg[dd,j];maximum[i]=max(maximum[i],degree)
    if degree==4:quartic.add((aa,bb))
  return maximum,sorted(quartic)
 klein_paths=paths({(0,0),(0,1),(0,2),(1,0),(1,1),(2,0),(2,2)})
 rotation_paths=paths({(0,0),(0,2),(1,1),(2,0),(2,2)})
 assert klein_paths==([4,4,3],[(0,0),(1,0)])and rotation_paths==([4,3,3],[(0,0)])
 g=m.mono([[(x&3)|((x&4)<<1)|((x&8)>>1),2*((x>>2)&1)]for x in range(16)]);g3=m.power(g,3)
 assert m.power(g,4)==I and g!=I and mul(g,g)!=I
 for B in [mul(m.star(A),g,A),mul(m.star(U),g,U)]:m.table(B)
 T=m.add(m.scale(I,F(1,2)),m.scale(g,(F(1,4),F(-1,4))),m.scale(g3,(F(1,4),F(1,4))))
 assert mul(T,T)==T and m.star(T)==T;N=m.add(I,m.scale(T,-1))
 character_values=[]
 for lam in m.ROOTS:
  val=m.plus((F(1,2),F(0)),m.plus(m.times((F(1,4),F(-1,4)),lam),m.times((F(1,4),F(1,4)),m.times(m.times(lam,lam),lam))))
  character_values.append(val)
 assert character_values==[m.O,m.O,m.Z,m.Z]
 def bankmul(B,D):return[[m.add(*(mul(B[i][k],D[k][j])for k in range(3)))for j in range(3)]for i in range(3)]
 id3=[[I if i==j else Z for j in range(3)]for i in range(3)]
 expected={'forward':[[T,Z,m.scale(N,-1)],[Z,I,Z],[N,Z,T]],'inverse':[[T,Z,N],[Z,I,Z],[m.scale(N,-1),Z,T]]}
 def replay(ops):
  X=[[I if i==j else Z for j in range(3)]for i in range(3)]
  for op in ops:
   if op['op']=='ADD':
    d,s=op['dest'],op['src'];X[d]=[m.add(x,m.scale(y,op['sign']))for x,y in zip(X[d],X[s])]
   elif op['op']=='SCALE':
    b=op['bank'];c=tuple(F(x,2**op['denpow'])for x in op['num']);X[b]=[m.scale(B,c)for B in X[b]]
   else:
    assert op['op']=='MONO';b=op['bank'];B={'g':g,'g3':g3}[op['name']];B=m.star(B)if op['inverse']else B;X[b]=[mul(B,D)for D in X[b]]
  return X
 words_path=a.c4_package/'WORDS.json';words=json.loads(words_path.read_text());controls=0
 for name,ops in words.items():
  assert replay(ops)==expected[name]and Counter(x['op']for x in ops)=={'ADD':9,'SCALE':18,'MONO':12}
  for j,op in enumerate(ops):
   if op['op']=='ADD':assert replay(ops[:j]+ops[j+1:])!=expected[name];controls+=1
 assert bankmul(expected['forward'],expected['inverse'])==bankmul(expected['inverse'],expected['forward'])==id3
 assert controls==18
 # Noncommuting test values verify the independently derived last-column formula.
 L=[[A,Z,Z],[I,A,Z],[Z,Z,I]];Ub=[[A,m.scale(U,-1),Z],[Z,A,Z],[Z,Z,I]]
 pp0,zz,ww=R,h,G;assert mul(R,h)!=mul(h,R)
 for TT in [plus(s),minus(s),T]:
  NN=m.add(I,m.scale(TT,-1));T1=mul(m.star(A),TT,A);T2=mul(m.star(U),TT,U);N1=m.add(I,m.scale(T1,-1));N2=m.add(I,m.scale(T2,-1))
  Crot=[[TT,Z,m.scale(NN,-1)],[Z,I,Z],[NN,Z,TT]];B=bankmul(bankmul(L,Crot),Ub)
  actual=[m.add(mul(B[i][0],pp0),mul(B[i][1],zz),mul(B[i][2],ww))for i in range(3)]
  formal=[m.add(mul(U,T1,pp0),m.scale(mul(A,U,T2,zz),-1),m.scale(mul(A,NN,ww),-1)),m.add(mul(A,T1,pp0),mul(U,N2,zz),m.scale(mul(NN,ww),-1)),m.add(mul(A,N1,pp0),m.scale(mul(U,N2,zz),-1),mul(TT,ww))]
  assert actual==formal
 uniform_bounds=[F(1)+F(3,2),F(1)+F(3,2)*F(5,2),F(5,2)+F(3,2)*F(19,4)];assert uniform_bounds==[F(5,2),F(19,4),F(77,8)]
 result={'status':'PASS_INDEPENDENT_ENDPOINT_GATE_LITERAL_PREMISES_AND_C4_WORDS','arithmetic_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'c4_words_sha256':hashlib.sha256(words_path.read_bytes()).hexdigest(),'c4_proof_sha256':hashlib.sha256((a.c4_package/'PROOF.md').read_bytes()).hexdigest(),'nonordinary_A2_s1_conjugate_column_support':4,'Ue_two_coset_identity':True,'transferred_column_identity_on_e':True,'quartic_path_census':{'klein':klein_paths,'rotation':rotation_paths},'kernel_traces':traces,'all_width_rank_formula_controls':ranks,'c4_character_values':[list(map(str,x))for x in character_values],'c4_forward_inverse_counts':{'ADD':9,'SCALE':18,'MONO':12},'omitted_ADD_controls':controls,'uniform_C4_prefix_bounds':list(map(str,uniform_bounds)),'three_noncommuting_last_column_identity_checks':3,'proof_scope':'The universal endpoint exclusions are proved in the separate written review using actual encoders/decoders, finite-catalogue separation and ordinary capacity. Finite source checks alone do not prove them.','new_complete_kappa':False}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
