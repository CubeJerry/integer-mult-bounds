#!/usr/bin/env python3
"""Independent exact replay of R's ordinary noncommuting compiler words."""
import argparse,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
import sympy as s
from release_projection import require
PROOF='d3ed2ad13a986486ce558f1afa8093f8b06c0fa6d0917aa175415b2cc62c3704'
PINS={'EXAMPLE-WORD':'1b09448f5c8121c3160b7bc9db9c54076a9f5d9d317fd2bea9485eea452ee57f','EXAMPLE-INVERSE-WORD':'b9efaf869029ca7d0dd096b8f5022c4cbb620cff0d36b261d821a455083566e7','GENERAL-WORD':'8af896d0f46c0dde492bcb8c826ace44f3f8e0cfbb5755d7111f45c783e8a63f','GENERAL-INVERSE-WORD':'d8c8dfa4c14a8bc2c518708a16d3f0dae2d7957eca5e9f0f88e8ec9fb71751f7'}
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();root=a.work/'R/noncommuting-compiler';proof=root/'PROOF.md'
 require(hashlib.sha256(proof.read_bytes()).hexdigest()==PROOF,'compiler proof pin')
 receipt=json.loads((root/'control/RESULT.json').read_bytes());words={}
 for name,pin in PINS.items():
  raw=(root/'control'/f'{name}.json').read_bytes();require(hashlib.sha256(raw).hexdigest()==pin,'primitive word pin');words[name]=json.loads(raw)
 w=words['EXAMPLE-WORD'];labels=w['group_labels'];tables=[tuple(tuple(z)for z in t)for t in w['literal_group_tables']]
 require(len(tables)==8 and len(set(tables))==8,'eight distinct literal tables')
 for ww in words.values():require(ww['group_labels']==labels and ww['literal_group_tables']==w['literal_group_tables'],'same literal group')
 for t in tables:require(sorted(v[0]for v in t)==list(range(16))and all(0<=v[1]<4 for v in t),'root-four monomial')
 def compose(t,u):return tuple((t[j][0],(e+t[j][1])%4)for j,e in u)
 mt=[[tables.index(compose(t,u))for u in tables]for t in tables]
 identity=tuple((j,0)for j in range(16));one=tables.index(identity)
 inv=[next(j for j in range(8)if mt[i][j]==mt[j][i]==one)for i in range(8)]
 x=labels.index([1,0,0]);y=labels.index([0,1,0]);t=labels.index([0,0,1])
 require(mt[x][x]==mt[y][y]==mt[t][t]==one and mt[x][y]==mt[y][x]and mt[mt[t][x]][t]==y,'literal D8 relations')
 require(mt[x][t]!=mt[t][x],'noncommutativity')
 def zero():return [Q(0)]*8
 def basis(g=one):v=zero();v[g]=Q(1);return v
 def plus(u,v):return [z+h for z,h in zip(u,v)]
 def times(u,v):
  out=zero()
  for i,z in enumerate(u):
   if z:
    for j,h in enumerate(v):
     if h:out[mt[i][j]]+=z*h
  return out
 def eye():return [[basis()if i==j else zero()for j in range(3)]for i in range(3)]
 def mm(A,B):
  out=[[zero()for j in range(3)]for i in range(3)]
  for i,j,k in itertools.product(range(3),repeat=3):out[i][j]=plus(out[i][j],times(A[i][k],B[k][j]))
  return out
 def run(ops):
  M=eye();peak=Q(1);counts=Counter()
  for op,*p in ops:
   require(op in {'ADD','SCALE','MONOMIAL'},'ordinary primitives only');counts[op]+=1
   if op=='ADD':
    src,dst=p;require(src!=dst and 0<=src<3 and 0<=dst<3,'distinct banks');M[dst]=[plus(u,v)for u,v in zip(M[dst],M[src])]
   elif op=='SCALE':
    bank,c=p;c=Q(c);require(c!=0,'invertible scalar');M[bank]=[[z*c for z in v]for v in M[bank]]
   else:
    bank,g=p;M[bank]=[times(basis(g),v)for v in M[bank]]
   peak=max(peak,max(sum(abs(z)for cell in row for z in cell)for row in M))
  return M,dict(counts),str(peak)
 units={tuple(map(int,k.strip('()').split(','))):list(map(Q,v))for k,v in receipt['matrix_units'].items()}
 require(len(units)==8 and s.Matrix(list(units.values())).rank()==8,'complete coefficient basis')
 products=0
 for (l,a1,b1),u in units.items():
  for (m,c1,d1),v in units.items():
   require(times(u,v)==(units[l,a1,d1]if l==m and b1==c1 else zero()),'matrix-unit product');products+=1
 total=zero()
 for (l,a1,b1),u in units.items():
  if a1==b1:total=plus(total,u)
 require(total==basis(),'matrix-unit identity sum')
 results={};matrices={}
 for name,ww in words.items():
  M,c,p=run(ww['operations']);matrices[name]=M;results[name]={'counts':c,'prefix_coefficient_l1_bound':p,'owner_births':0,'Gaussian_queries':0}
 target=eye();target[0][0]=plus(target[0][0],units[4,0,1])
 require(matrices['EXAMPLE-WORD']==target,'single-bank internal nonmonomial endpoint')
 for name in ['EXAMPLE','GENERAL']:
  F=matrices[name+'-WORD'];I=matrices[name+'-INVERSE-WORD'];require(mm(F,I)==mm(I,F)==eye(),'two-sided physical inverse')
 require(matrices['EXAMPLE-WORD'][1:]==eye()[1:],'arbitrary borrowed and idle banks restored')
 reps=[]
 for eps,eta in itertools.product([1,-1],repeat=2):reps.append([s.Matrix([[eps**(u+v)*eta**e]])for u,v,e in labels])
 X=s.diag(1,-1);Y=s.diag(-1,1);T=s.Matrix([[0,1],[1,0]])
 reps.append([X**u*Y**v*T**e for u,v,e in labels]);dims=[1,1,1,1,2]
 for rr in reps:
  for i,j in itertools.product(range(8),repeat=2):require(rr[i]*rr[j]==rr[mt[i][j]],'representation agrees with literal multiplication')
 determinants=[]
 for d,rr in zip(dims,reps):
  B=s.zeros(3*d)
  for i,j in itertools.product(range(3),repeat=2):
   cell=sum((s.Rational(c.numerator,c.denominator)*rr[g]for g,c in enumerate(matrices['GENERAL-WORD'][i][j])),s.zeros(d))
   B[i*d:(i+1)*d,j*d:(j+1)*d]=cell
  determinants.append(str(B.det()));require(B.det()==2**d,'actual component determinant delta^d')
 require(results['EXAMPLE-WORD']['counts']=={'MONOMIAL':28,'SCALE':32,'ADD':16},'actual example cost')
 require(results['GENERAL-WORD']['counts']=={'MONOMIAL':1098,'SCALE':1253,'ADD':628},'actual general cost')
 # Rebuild source A column-by-column from C_b D_acd P, without R code.
 A=s.zeros(16)
 for z in range(16):
  bits=[(z>>k)&1 for k in range(4)];rot=bits[1:]+bits[:1]
  q=sum(bit<<k for k,bit in enumerate(rot));sgn=(-1)**(rot[0]*rot[2]*rot[3])
  A[q,z]=sgn*(1+s.I)/2;A[q^2,z]=sgn*(1-s.I)/2
 A2=(A*A).applyfunc(s.simplify)
 diagonal_a=s.diag(*[(-1)**(z&1)for z in range(16)])
 diagonal_b=s.diag(*[(-1)**((z>>1)&1)for z in range(16)])
 expected_x=(A2.adjoint()*diagonal_a*A2).applyfunc(s.simplify)
 expected_y=(A2.adjoint()*diagonal_b*A2).applyfunc(s.simplify)
 literal=[]
 for table in tables:
  M=s.zeros(16)
  for j,(i,e)in enumerate(table):M[i,j]=s.I**e
  literal.append(M)
 require(literal[x]==expected_x and literal[y]==expected_y,'source-square controls from literal A')
 for z in range(16):
  aa,bb,cc,dd=[(z>>k)&1 for k in range(4)];target_address=aa+2*bb+4*(dd^(aa*bb))+8*(cc^(aa*bb))
  require(tables[t][z]==(target_address,0),'literal source-derived t table')
 # Confirm the stated t conjugation by building R2=(C_a C_b)^-1 A^2.
 def C(bit):
  out=s.zeros(16)
  for z in range(16):out[z,z]=(1+s.I)/2;out[z^(1<<bit),z]=(1-s.I)/2
  return out
 R2=(C(1).adjoint()*C(0).adjoint()*A2).applyfunc(s.simplify);swap=s.zeros(16)
 for z in range(16):swap[(z&12)|((z&1)<<1)|((z&2)>>1),z]=1
 require((R2.adjoint()*swap*R2).applyfunc(s.simplify)==literal[t],'actual R2 swap transport')
 E12=sum((s.Rational(c.numerator,c.denominator)*literal[g]for g,c in enumerate(units[4,0,1])),s.zeros(16))
 require(E12!=s.zeros(16)and E12*E12==s.zeros(16),'actual nonzero nilpotent internal field')
 require(any(sum(z!=0 for z in row)>1 for row in (s.eye(16)+E12).tolist()),'genuine nonmonomial single-bank unit')
 multiplicities=[]
 for V in range(1,5):
  mult=[]
  for rr in reps:
   val=s.simplify(sum(s.trace(literal[g])**V*s.trace(rr[inv[g]])for g in range(8))/8)
   require(val.is_Integer and val>=0,'actual nonnegative tensor multiplicity');mult.append(int(val))
  require(sum(d*m for d,m in zip(dims,mult))==16**V,'all tensor dimensions accounted for')
  multiplicities.append({'V':V,'multiplicities':mult})
 hidden=units[1,0,0];hidden_matrix=sum((s.Rational(c.numerator,c.denominator)*literal[g]for g,c in enumerate(hidden)),s.zeros(16))
 require(hidden_matrix==s.zeros(16)and multiplicities[1]['multiplicities'][1]==16,'hidden width-one component becomes real at width two')
 # A separate exact Gaussian-rational primitive control exercises exterior i.
 def lower(dst,src,row):
  ops=[]
  for g,c in enumerate(row):
   c=s.simplify(c)
   if not c:continue
   if g!=one:ops.append(['MONOMIAL',src,g])
   if c!=1:ops.append(['SCALE',src,str(c)])
   ops.append(['ADD',src,dst])
   if c!=1:ops.append(['SCALE',src,str(s.simplify(1/c))])
   if g!=one:ops.append(['MONOMIAL',src,inv[g]])
  return ops
 e11=units[4,0,0];e12=units[4,0,1]
 Xrow=[s.I*c for c in e11];Yrow=e12
 gaussian_ops=lower(1,0,[-z for z in Yrow])+lower(0,1,[-z for z in Xrow])+lower(1,0,Yrow)+lower(0,1,Xrow)
 def gaussian_run(ops):
  M=eye()
  for op,bank,arg in ops:
   if op=='ADD':M[arg]=[plus(u,v)for u,v in zip(M[arg],M[bank])]
   elif op=='SCALE':
    c=s.sympify(arg);M[bank]=[[s.expand(z*c)for z in row]for row in M[bank]]
   else:M[bank]=[times(basis(arg),row)for row in M[bank]]
  return [[[s.simplify(z)for z in row]for row in bank]for bank in M]
 gauss=gaussian_run(gaussian_ops);gauss_target=eye();gauss_target[0][0]=plus(gauss_target[0][0],[s.I*z for z in e12])
 require(gauss==gauss_target,'actual exterior-i internal transvection')
 require(gauss[1:]==eye()[1:],'Gaussian control restores arbitrary borrowed bank')
 controls=[]
 for op in ['ADD','MONOMIAL']:
  ops=words['EXAMPLE-WORD']['operations'];k=next(k for k,o in enumerate(ops)if o[0]==op)
  require(run(ops[:k]+ops[k+1:])[0]!=target,'real omitted primitive changes endpoint');controls.append({'omitted':ops[k],'rejected':True})
 require(run([['ADD',0,1],['ADD',0,1]])[0]!=eye(),'unweighted ADD is not its characteristic-zero inverse')
 controls.append({'naive_ADD_reversal_is_not_free':True})
 controls.append({'hidden_component_width1_identity_width2_singular':True,'width2_kernel_dimension_on_three_banks':48})
 controls.append({'exterior_i_vs_literal_one_column_i_at_width2':['i','-1'],'distinct':True})
 source_pins={}
 for name,pin in receipt['source_pins'].items():
  got=hashlib.sha256((a.repo/'research/moonshot-005-program'/name).read_bytes()).hexdigest();require(got==pin,'admitted source pin');source_pins[name]=got
 a.out.mkdir(parents=True,exist_ok=True)
 artifact={'operations':gaussian_ops,'group_labels':labels,'literal_group_tables':w['literal_group_tables'],'scope':'Independent C positive control for exterior Gaussian coefficient i, actual unweighted ADDs and source-restoring monomial services. No extra owner.'}
 data=(json.dumps(artifact,indent=2)+'\n').encode();(a.out/'GAUSSIAN-CONTROL-WORD.json').write_bytes(data)
 result={'status':'PASS_INDEPENDENT_SPLIT_NONCOMMUTING_COMPILER','proof_sha256':PROOF,'word_pins':PINS,
  'literal_group_table_compositions':64,'all_matrix_unit_products':products,'matrix_unit_basis_rank':8,
  'literal_A_source_and_R2_swap_verified':True,'actual_general_component_determinants':determinants,
  'words':results,'tensor_width_controls':multiplicities,'negative_controls':controls,'source_pins':source_pins,
  'independent_Gaussian_control':{'word_sha256':hashlib.sha256(data).hexdigest(),'target':'I+i E00 tensor e12_std','counts':dict(Counter(o[0]for o in gaussian_ops)),'borrowed_banks_restored':True},
  'scope':'Independent exact ordinary primitive/group-algebra replay and universal proof review. Group coefficients and table phases remain literal; tensor width tests are controls only. All five global foundations remain open. No421 caller, complete supplier or kappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k]for k in ['status','words','independent_Gaussian_control']},indent=2))
if __name__=='__main__':main()
