#!/usr/bin/env python3
"""Independent literal support, noncommutative block and routing proof audit."""
from __future__ import annotations
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as s

def tidy(m):return m.applyfunc(s.expand)
def same(x,y):assert s.expand(x-y)==0,(x,y)

def main():
    parser=argparse.ArgumentParser()
    for n in ['repo','proof','author-result','out']:parser.add_argument('--'+n,type=Path,required=True)
    args=parser.parse_args();I=s.eye(16);P=s.zeros(16);phase=s.eye(16);X=s.zeros(16)
    for j in range(16):
        P[(j>>1)|((j&1)<<3),j]=1
        phase[j,j]=-1 if(j&13)==13 else 1
        X[j^2,j]=1
    C=((1+s.I)*I+(1-s.I)*X)/2;S=phase*P;A=tidy(C*S)
    assert tidy(A.conjugate().T*A)==I and tidy(S.conjugate().T*S)==I
    D={b:s.diag(*[s.I if j&b else 1 for j in range(16)])for b in [1,2,4,8]}
    powers={k:tidy(A**k)for k in range(1,5)}
    support=[]
    for k in range(1,4):
        counts=[[sum(powers[k][r,m]!=0 and A[m,c]!=0 for m in range(16))for c in range(16)]for r in range(16)]
        assert all(z in [0,1]for row in counts for z in row)
        assert all(sum(row)==2**(k+1)for row in counts)
        assert all(sum(counts[r][c]for r in range(16))==2**(k+1)for c in range(16))
        support.append({'word':'A^'+str(k)+' d A','nonzero_intermediate_paths_per_entry':1,'row_and_column_support':2**(k+1),'scope':'Every diagonal d with all entries nonzero, by unique intermediate paths.'})
    assert all(sum(A[r,c]!=0 for c in range(16))==2 for r in range(16))
    gauge_checks=[]
    for k,b in [(1,1),(2,8),(3,4)]:
        for u,v in itertools.product(range(4),repeat=2):
            left=tidy(powers[k]*D[2]**u*D[4]**v*A)
            right=tidy(D[b]**u*powers[k+1]*D[8]**v)
            assert left==right
        gauge_checks.append({'power':k,'left_phase_bit':b,'right_phase_bit':8,'literal_quarter_pairs':16})
    for u in range(4):
        assert tidy(A*D[2]**u)==tidy(D[1]**u*A)
        assert tidy(D[4]**u*A)==tidy(A*D[8]**u)
    # Arbitrary d lies between two operators on the same b-pair. Its values
    # may cause cancellation but can never create entries outside that pair.
    Csupport=[[int(C[r,c]!=0)for c in range(16)]for r in range(16)]
    paired=[[any(Csupport[r][m]and Csupport[m][c]for m in range(16))for c in range(16)]for r in range(16)]
    assert all(sum(row)==2 for row in paired)
    clock_checks=[]
    for theta in range(4):
        h=tidy(S.conjugate().T*D[2]**theta)
        assert tidy(A*h)==tidy(C*D[2]**theta)
        for u,v in itertools.product(range(4),repeat=2):
            d=D[2]**u*D[4]**v;z=tidy(A*h*d*A)
            assert z==tidy(C*D[2]**theta*d*C*S)
            assert all(sum(z[r,c]!=0 for c in range(16))<=2 for r in range(16))
        clock_checks.append({'theta':theta,'arbitrary_diagonal_support_bound':2,'literal_joint_controls':16})

    # Noncommutative symbols preserve the order of every source and control.
    a,h,f=s.symbols('a h f',commutative=False);q=s.Matrix(3,3,lambda i,j:s.Symbol(f'q{i}{j}',commutative=False));g=1-f
    L=s.Matrix([[a,0,0],[1,a,0],[0,0,1]]);U=s.Matrix([[a,-a*a,0],[0,a,0],[0,0,1]])
    routing=s.Matrix([[1,0,0],[0,h*f,h*g],[0,g,f]])
    full=tidy(L*routing*U*q*L)
    same(full[0,0],a*a*q[0,0]*a+a*a*q[0,1]-a**3*q[1,0]*a-a**3*q[1,1])
    same(full[0,1],a*a*q[0,1]*a-a**3*q[1,1]*a)
    same(full[0,2],a*a*q[0,2]-a**3*q[1,2])
    partial=full.subs({q[0,1]:0,q[1,2]:0})
    same(partial[1,1],(a*h*f*a-a*a)*q[1,1]*a+a*h*g*q[2,1]*a)
    zero={q[0,0]:0,q[0,1]:0,q[1,1]:0,q[1,2]:0};forced=tidy(full.subs(zero))
    same(forced[2,0],g*a*q[1,0]*a+f*q[2,0]*a+f*q[2,1])
    same(forced[0,0],-a**3*q[1,0]*a);same(forced[0,2],a*a*q[0,2])
    swapped=tidy(forced.subs(f,0));same(swapped[2,0],a*q[1,0]*a);assert swapped[2,2]==0
    # Column order (2,0,1) makes the forced Q block lower triangular.
    qforced=q.subs(zero);permuted=qforced[:,[2,0,1]]
    assert permuted==s.Matrix([[q[0,2],0,0],[0,q[1,0],0],[q[2,2],q[2,0],q[2,1]]])

    # Keep all routing coefficients formal and the before-routing clock exact.
    r=s.Matrix(3,3,lambda i,j:0 if(i,j)==(2,0)else s.Symbol(f'r{i}{j}',commutative=False));t=s.Symbol('t')
    before=tidy(L*r*s.diag(1,h,1)*U*q*L)
    highest=before.applyfunc(lambda z:s.expand(z.subs(a,t*a)).coeff(t,4))
    expected=s.zeros(3)
    for i,j in itertools.product(range(2),repeat=2):expected[i,j]=-a*r[i,0]*a*a*q[1,j]*a
    assert tidy(highest-expected)==s.zeros(3)
    # At each physical sector R_a is a bank permutation; its active first
    # column is carried back exactly to e0 by the inverse permutation.
    routing_cases=0
    for perm in itertools.permutations(range(3)):
        M=s.zeros(3)
        for j,i in enumerate(perm):M[i,j]=1
        if perm[0]<2:
            assert M.T*M[:,0]==s.Matrix([1,0,0]);routing_cases+=1
    assert routing_cases==4
    sector_counts={}
    for width in [1,2,3,4,7]:
        counts=[sum(s.binomial(width,k)for k in range(width+1)if k%4==u)for u in range(4)]
        joint=[[int(4**width*counts[u]*counts[v])for v in range(4)]for u in range(4)]
        assert sum(map(sum,joint))==16**width
        assert all(x>0 for row in joint for x in row)==(width>=3)
        sector_counts[str(width)]=joint
    bad=s.Matrix([[1,0,0],[0,0,1],[0,1,0]]);assert bad.det()!=0 and bad[1,0]==bad[1,1]==0
    assert tidy(A*D[2])!=tidy(D[2]*A),'Wrong untranslated output control must fail'
    paths=['research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md','research/moonshot-005-program/results/complex-middle-native-interface/author/PROOF.md']
    result={'status':'PASS_ROOT_INDEPENDENT_SOURCE_TRANSPORT_ROUTING_REVIEW','proof_sha256':hashlib.sha256(args.proof.read_bytes()).hexdigest(),'author_result_sha256':hashlib.sha256(args.author_result.read_bytes()).hexdigest(),'method':'Independent SymPy literal16-address source and formal noncommutative block identities; author code is not imported. Written tensor-separation and rank argument reviewed separately.','arbitrary_diagonal_unique_path_proof':support,'explicit_joint_source_gauges':gauge_checks,'clock_support_checks':clock_checks,'forced_block_formulas_and_triangular_unit_pattern':True,'reversed_order_highest_degree_formula':True,'active_sector_permutation_cases':routing_cases,'joint_quarter_sector_counts':sector_counts,'negative_controls':['Invertible scalar sector with zero active row pair loses the full rank-four component.','Untransported Db output control fails the literal source identity.'],'source_pins':{p:hashlib.sha256((args.repo/p).read_bytes()).hexdigest()for p in paths},'scope':'Scoped all-width clock-after-routing obstruction and explicit transported output decoder for the opposite order. No general ordinary-interface impossibility, no actual421 endpoint, no new complete kappa.'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
