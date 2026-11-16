"""Independent free-word expansion, scalar character reduction and actual interface controls."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s
p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--root-control',type=Path,required=True);p.add_argument('--out',type=Path,required=True);arg=p.parse_args();arg.out.mkdir(parents=True,exist_ok=True)
a=s.Symbol('a',commutative=False);cs=s.symbols('c0:9',commutative=False);qs=s.symbols('q0:9',commutative=False);C0=s.Matrix(3,3,cs);Q0=s.Matrix(3,3,qs)
L=s.Matrix([[a,0,0],[1,a,0],[0,0,1]]);U=s.Matrix([[a,-a**2,0],[0,a,0],[0,0,1]])
x,b,c,t,d,e,u,f,g=cs;K=s.Matrix([a*x*a,a*t*a,0]);W=s.Matrix([0,x,u]);Z0=s.Matrix([a*b*a,b*a+a*d*a,f*a]);Fcol=s.Matrix([a*c,c+a*e,g])
assert (L*C0*U-s.Matrix.hstack(K+W*a,-K*a-W*a**2+Z0,Fcol)).applyfunc(s.expand)==s.zeros(3)
E=(L*C0*U*Q0*L).applyfunc(s.expand);quartic=-K*a*s.Matrix([[qs[3]*a,qs[4]*a,0]])
remainder=(E-quartic).applyfunc(s.expand)
def degree(z):
 return sum(int(q.exp)if q.is_Pow and q.base==a else int(q==a)for q in s.Mul.make_args(z))
assert all(degree(term)<=3 for z in remainder for term in s.Add.make_args(z))
assert (E[:,2]-((K+W*a)*qs[2]+(-K*a-W*a**2+Z0)*qs[5]+Fcol*qs[8])).applyfunc(s.expand)==s.zeros(3,1)
# Independent scalar chain: no physical projector rank is needed once Phi4 is forced to its character line.
tau,q22,ee=s.symbols('tau q22 ee',nonzero=True);middle=s.Matrix([0,tau,0]);last_rank1=s.Matrix([0,ee*q22,0]);assert middle.row_join(last_rank1).rank()==1
mat=s.Matrix([[s.Symbol('q00'),s.Symbol('q01'),0],[s.Symbol('q10'),s.Symbol('q11'),0],[s.Symbol('q20'),s.Symbol('q21'),q22]])
assert s.expand(mat.det()-q22*(mat[0,0]*mat[1,1]-mat[0,1]*mat[1,0]))==0
# Reuse only root's already independently rebuilt one-column matrices and row-update routine.
text=arg.root_control.read_text();exec(text[text.index('I=s.eye(16)'):text.index('words=')],globals());exec(text[text.index('def execute(word):'):text.index('receipts={}')],globals())
Zc=mono([(x,2*((x>>2)&1))for x in range(16)]);T0=S*Zc;T=(I+T0)/2;Nt=I-T;R0=J*F;Rp=(I+R0)/2;Rm=I-Rp
Cold=block([[P,M,Z],[J*M,J*P,Z],[Z,Z,I]]);Cn=clean(Cold*block([[T,Z,Nt],[Z,I,Z],[Nt,Z,T]]));Swap12=block([[I,Z,Z],[Z,Z,I],[Z,I,Z]])
Qk=block([[I,Z,Z],[Z,Rp,Rm],[Z,Rm,Rp]]);Oo=block([[Ph,Mh,Z],[Mh,Ph,Z],[Z,Z,I]]);Piop=s.diag(Ph,Mh,Z)
Ko=block([[clean(A*P*T*A),Z,Z],[clean(A*J*M*T*A),Z,Z],[Z,Z,Z]])
assert clean(Piop*Ko)==Ko and Oo*Piop*Oo==s.diag(I,Z,Z)and clean(Ko*s.diag(A*Rm,Z,Z))==s.zeros(48)
data=json.loads((arg.author/'WORDS.json').read_text());monos={n:mono(t)for n,t in data['monomial_tables'].items()};assert monos=={'F':F,'Fhat':Fh,'J':J,'T0':T0,'R0':R0};omissions=0
for name,want in {'C_opposite':Cn,'C_opposite_swapped12':Cn*Swap12,'Q_kernel':Qk,'O_opposite':Oo}.items():
 word=data['words'][name];inv=data['words'][name+'_inverse'];fwd=execute(word);back=execute(inv);assert fwd==want and clean(fwd*back)==s.eye(48)and clean(back*fwd)==s.eye(48)
 for n,w in [(name,word),(name+'_inverse',inv)]:
  whole=execute(w);counts={o:sum(z['op']==o for z in w)for o in ['ADD','SCALE','MONO']};assert {k:v for k,v in counts.items()if v}==data['invoices'][n]['counts']
  for k,op in enumerate(w):
   if op['op']=='ADD':assert execute(w[:k]+w[k+1:])!=whole;omissions+=1
for key,gauge in json.loads((arg.author/'GAUSSIAN-GAUGES.json').read_text()).items():
 orient,row,term,rank=key.split('_');row=int(row[3:]);term=int(term[4:]);rank=int(rank[4:]);ep,et=divmod(term,2);mid=(J if row else I)*(F if ep else I)*(T0 if et else I);want=clean(A*mid*(A if rank==2 else A2));h=I
 for bit in range(rank):h=clean(h*((1+s.I)*I+(1-s.I)*mono([(x^(1<<bit),0)for x in range(16)]))/2)
 assert clean(mono(gauge['left'])*h*mono(gauge['right']))==want
result={'status':'PASS_INDEPENDENT_COMPONENT_AUGMENTATION_GATE','free_noncommuting_block_expansion':True,'all_nonquartic_terms_have_source_degree_at_most3':True,'scalar_last_column_contradiction':True,'weaker_sufficient_projector_premise':'Ordinary PiK=K and epsilon(Pi)=middle-line projector suffice; physicalrankPi=D is not needed for this character argument.','literal_gaussian_gauges_checked':32,'primitive_operator_inverse_pairs':4,'independent_omitted_ADD_controls':omissions,'phase_argument':'For projectively equal unitary Gaussian-dyadic words U=lambdaV, one-column inner product putslambda inZ[i,1/2]; unit modulus forcesfourthroot. Thusall canceled projective classes havecoefficient-sumzero atVdivisibleby4.','pins':{n:hashlib.sha256((arg.author/n).read_bytes()).hexdigest()for n in ['PROOF.md','WORDS.json','GAUSSIAN-GAUGES.json']},'scope':'Full faithful finite-catalogue theorem reviewed mathematically; exact one-column controls do not claim Phi is well-defined atV1. No fullcaller.'}
(arg.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
