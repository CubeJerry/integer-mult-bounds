#!/usr/bin/env python3
"""Independent coherent-pivot normalization and ordered block verification."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s

def tidy(m):return m.applyfunc(s.expand)
def blocks(rows):return s.Matrix.vstack(*(s.Matrix.hstack(*row)for row in rows))
def same(x,y):assert s.expand(x-y)==0,(x,y)

def main():
    p=argparse.ArgumentParser()
    for n in ['proof','support-proof','support-review','author-result','out']:p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();I=s.eye(16);Z=s.zeros(16);rotation=s.zeros(16);phase=s.eye(16);flip=s.zeros(16)
    for j in range(16):rotation[(j>>1)|((j&1)<<3),j]=1;phase[j,j]=-1 if(j&13)==13 else 1;flip[j^2,j]=1
    source=tidy(((1+s.I)*I+(1-s.I)*flip)*phase*rotation/2)
    Da=s.diag(*[s.I if j&1 else 1 for j in range(16)]);Db=s.diag(*[s.I if j&2 else 1 for j in range(16)])
    sx=[s.Integer(1),s.Integer(2),s.I,-s.Integer(1)];tv=[s.Integer(0),s.Integer(1),1+s.I,-s.Integer(2)]
    def evaluate(values,D):
        coeff=[s.expand(sum(values[k]*s.I**(-k*j)for k in range(4))/4)for j in range(4)]
        return tidy(sum((coeff[j]*D**j for j in range(4)),Z))
    models=[('literal16_native',source,Da,Db)]
    # This all-sector model satisfies only the transport relation needed by
    # the normalization and makes every joint x,y phase pair visible.
    x=s.diag(*[s.I**(j//4)for j in range(16)]);y=s.diag(*[s.I**(j%4)for j in range(16)]);T=s.zeros(16)
    for j in range(16):u,v=divmod(j,4);T[4*v+(u+1)%4,j]=s.I**(j%4)
    assert T*y==x*T;models.append(('all16_joint_phase_pairs',T,x,y));normalizations=[]
    for label,A,Dx,Dy in models:
        assert tidy(A*Dy)==tidy(Dx*A)
        sb,tb=evaluate(sx,Dy),evaluate(tv,Dy);sa,ta=evaluate(sx,Dx),evaluate(tv,Dx);sai=evaluate([1/z for z in sx],Dx)
        assert tidy(sa*sai)==I
        Gb=blocks([[sb,Z,Z],[tb,sb,Z],[Z,Z,I]]);Gai=blocks([[sai,Z,Z],[-sai*ta*sai,sai,Z],[Z,Z,I]])
        L=blocks([[A,Z,Z],[I,A,Z],[Z,Z,I]]);w=tidy(sai*sb);Lw=blocks([[A,Z,Z],[w,A,Z],[Z,Z,I]])
        assert tidy(Gai*L*Gb)==Lw and w!=I
        lower_b=blocks([[I,Z,Z],[tb,I,Z],[Z,Z,I]]);lower_ai=blocks([[I,Z,Z],[-ta,I,Z],[Z,Z,I]])
        assert tidy(lower_ai*L*lower_b)==L
        normalizations.append({'model':label,'normalization':True,'cross_unit_nontrivial':True,'leading_lower_shear_is_output_gauge':True})

    aa,b,c,d,e,f,g,h,w=s.symbols('a b c d e f g h w',commutative=False)
    q=s.Matrix(3,3,lambda i,j:s.Symbol(f'q{i}{j}',commutative=False));L=s.Matrix([[aa,0,0],[1,aa,0],[0,0,1]]);Lw=s.Matrix([[aa,0,0],[w,aa,0],[0,0,1]]);U=s.Matrix([[aa,-aa**2,0],[0,aa,0],[0,0,1]])
    first=s.Matrix([[1,b*h,c],[0,d*h,e],[0,f*h,g]]);pre=tidy(Lw*first*U)
    expected=s.Matrix([[aa**2,-aa**3+aa*b*h*aa,aa*c],[w*aa,-w*aa**2+w*b*h*aa+aa*d*h*aa,w*c+aa*e],[0,f*h*aa,g]])
    assert tidy(pre-expected)==s.zeros(3)
    E=tidy(pre*q*L);partial=E.subs({q[0,1]:0,q[1,2]:0})
    same(partial[1,1],-w*aa**2*q[1,1]*aa+(w*b*h*aa+aa*d*h*aa)*q[1,1]*aa+(w*c+aa*e)*q[2,1]*aa)
    forced=tidy(E.subs({q[0,0]:0,q[0,1]:0,q[1,1]:0,q[1,2]:0}))
    same(forced[0,2],aa**2*q[0,2]+aa*c*q[2,2]);same(forced[2,0],f*h*aa*q[1,0]*aa+g*q[2,0]*aa+g*q[2,1]);same(forced[2,2],g*q[2,2])
    assert forced[2,2].subs(g,0)==0
    same(forced[2,0].subs(g,0),f*h*aa*q[1,0]*aa)
    # Proper pivot projections evade the unit premise while leaving the
    # conditional bank matrix invertible in every sector.
    sector_matrices=[s.eye(3),s.Matrix([[0,1,0],[1,0,0],[0,0,1]]),s.eye(3),s.eye(3)]
    assert all(M.det()!=0 for M in sector_matrices)and[ M[0,0]for M in sector_matrices]==[1,0,1,1]
    support=json.loads(a.support_review.read_text());assert support['status']=='PASS_ROOT_INDEPENDENT_SOURCE_TRANSPORT_ROUTING_REVIEW'and support['proof_sha256']==hashlib.sha256(a.support_proof.read_bytes()).hexdigest()
    result={'status':'PASS_ROOT_INDEPENDENT_COHERENT_FIRST_PIVOT','author_proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'author_result_sha256':hashlib.sha256(a.author_result.read_bytes()).hexdigest(),'support_proof_sha256':hashlib.sha256(a.support_proof.read_bytes()).hexdigest(),'independent_support_review_sha256':hashlib.sha256(a.support_review.read_bytes()).hexdigest(),'method':'Independent exact SymPy literal source/all-sector transport models and noncommutative block formulas; no author code imported. The general normalization and support/rank proof are reviewed in writing.','exact_transport_normalizations':normalizations,'ordered_coherent_block_formulas':True,'conditional_first_pivot_counterexample_to_unit_premise':{'sector_pivots':[1,0,1,1],'all_sector_matrices_invertible':True},'negative_controls':['For the nonconstant scalar unit s, replacing w by I changes the actual normalized native.','Invertibility of the full conditional routing does not imply its first entry is a unit.'],'scope':'R20=0, unit R00 in all four sectors, one declared clock, arbitrary fixed diagonal Q and ordinary outer encodings. Other first pivots and non-diagonal Q remain open. No new complete kappa.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
