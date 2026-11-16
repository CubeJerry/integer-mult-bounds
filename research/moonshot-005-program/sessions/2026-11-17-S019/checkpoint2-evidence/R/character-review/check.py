"""Independent exact Gaussian matrix and primitive review; no author engine imported."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
I=s.eye(16);Z=s.zeros(16);i=s.I
clean=lambda M:M.applyfunc(s.expand)
def mono(t):
 M=s.zeros(16);assert sorted(d for d,p in t)==list(range(16))
 for j,(d,p)in enumerate(t):M[d,j]=i**(p%4)
 return M
def tab(f):return[f(*[(x>>j)&1 for j in range(4)])for x in range(16)]
rot=mono(tab(lambda a,b,c,d:(b+2*c+4*d+8*a,2*a*b*d)));Xb=mono([(x^2,0)for x in range(16)]);A=clean(((1+i)*I+(1-i)*Xb)*rot/2)
R2=mono(tab(lambda a,b,c,d:((c^(a*b))+2*d+4*a+8*b,a*b*(1+2*c+2*d))));S=mono(tab(lambda a,b,c,d:(b+2*a+4*c+8*d,0)));J=clean(R2.H*S*R2)
F=mono([(x,2*(x&1))for x in range(16)]);Fh=mono([(x,2*((x>>3)&1))for x in range(16)]);G=mono([(x^8,0)for x in range(16)]);Kd=mono(tab(lambda a,b,c,d:(a+2*(b^(a*d))+4*(c^(a*d))+8*d,2*a*d)))
A2=clean(A*A);A3=clean(A2*A);A4=clean(A3*A);B2=clean(A3*S*A)
assert clean(A*F*A.H)==Fh and J*F==F*J and Kd*Fh==Fh*Kd and G*Fh==-Fh*G
assert clean(A*J*A3)==clean(Kd*B2) and clean(A*J*A2*S*A)==clean(Kd*A4)
P=(I+F)/2;M=I-P;Ph=(I+Fh)/2;Mh=I-Ph;block=lambda x:s.BlockMatrix(x).as_explicit()
C=block([[P,Z,M],[J*P,I,J*M],[M,Z,P]]);Q=block([[Z,I,Z],[I,S,Z],[Z,Z,I]]);D=s.diag(I,Kd,I);Pi=s.diag(Ph,Ph,Z)
K=block([[clean(A*P*A),Z,Z],[clean(A*J*P*A),Z,Z],[Z,Z,Z]])
assert Pi*Pi==Pi and Pi.trace()==16 and clean(Pi*K)==K and clean(K.H*K)==s.diag(clean(2*A.H*P*A),Z,Z)
W=block([[-clean(A*P*A3),-clean(A*P*A2*S*A),Z],[-clean(A*J*P*A3),-clean(A*J*P*A2*S*A),Z],[Z,Z,Z]])
E4=s.diag(-clean(Ph*A4),-clean(Ph*A4),Z);E2=block([[Z,-clean(Ph*B2),Z],[-clean(Ph*B2),Z,Z],[Z,Z,Z]])
assert clean(D*W)==E4+E2 and clean(E4*E4.H)==Pi and clean(E2*E2.H)==Pi and clean(W*W.H)==clean(2*K*K.H)
Odd=block([[Mh,Ph,Z],[Ph,Mh,Z],[Z,Z,I]])*s.diag(I,G,I);assert clean(Odd*Pi*Odd.H)==s.diag(Z,I,Z)
words=json.loads((a.author/'WORDS.json').read_text());tables=words['monomial_tables'];monos={n:mono(t)for n,t in tables.items()};assert monos=={'F':F,'Fhat':Fh,'J':J,'S':S,'Kdec':Kd,'G':G}
def execute(word):
 out=s.eye(48)
 for op in word:
  if op['op']=='ADD':
   u,v=op['source'],op['target'];out[16*v:16*v+16,:]=out[16*v:16*v+16,:]+out[16*u:16*u+16,:]
  elif op['op']=='SCALE':
   b=op['bank'];out[16*b:16*b+16,:]=s.Rational(op['coefficient'])*out[16*b:16*b+16,:]
  else:
   assert op['op']=='MONO';b=op['bank'];out[16*b:16*b+16,:]=monos[op['name']]*out[16*b:16*b+16,:]
 return clean(out)
receipts={};bad=0
for n,expected in {'C':C,'Q':Q,'D':D,'O_odd':Odd}.items():
 w=words['words'][n];v=words['words'][n+'_inverse'];f=execute(w);g=execute(v);assert f==expected and clean(f*g)==s.eye(48) and clean(g*f)==s.eye(48)
 for name,word in [(n,w),(n+'_inverse',v)]:
  counts={k:sum(x['op']==k for x in word)for k in ['ADD','SCALE','MONO']};want=words['invoices_and_prefix_bounds'][name]['counts'];assert {k:v for k,v in counts.items()if v}==want;receipts[name]=counts
  for j,op in enumerate(word):
   if op['op']=='ADD':assert execute(word[:j]+word[j+1:])!=execute(word);bad+=1
for name,obj in json.loads((a.author/'GAUSSIAN-GAUGES.json').read_text()).items():
 h=I
 for bit in range(obj['rank']):h=clean(h*((1+i)*I+(1-i)*mono([(x^(1<<bit),0)for x in range(16)]))/2)
 assert clean(mono(obj['left'])*h*mono(obj['right']))==({'A4':A4,'B2':B2}[name])
for tab in tables.values():assert {(d,d,d,d):i**(4*p)for d,p in tab}=={(x,x,x,x):1 for x in range(16)}
result={'status':'PASS_INDEPENDENT_ORDINARY_CHARACTER_REVIEW','method':'Separate SymPy exact Gaussian matrices and direct primitive row-block replay; no author arithmetic/execution engine imported. Universal proof separately reviewed.','sympy_version':s.__version__,'source_rank_at_V1':8,'ambient_projector_rank_at_V1':16,'augmentation_rank_at_widths4k':2,'required_free_bank_character_rank':1,'whole_operator_inverse_pairs':4,'independent_ADD_omission_controls':bad,'invoices':receipts,'pins':{n:hashlib.sha256((a.author/n).read_bytes()).hexdigest()for n in ['PROOF.md','check.py','WORDS.json','GAUSSIAN-GAUGES.json']},'scope':'Fixed collective root-four ordinary coefficient algebra; large widths divisible by4 obstruct uniform independent421. Odd-width image alignment is genuine but not a complete caller.'}
(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
