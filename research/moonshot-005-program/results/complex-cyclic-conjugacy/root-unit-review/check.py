#!/usr/bin/env python3
"""Independent exact Fourier/unit and literal scalar-recipe controls."""
from __future__ import annotations
import argparse,hashlib,itertools,json,math
from pathlib import Path
import sympy as s


def main():
    p=argparse.ArgumentParser();p.add_argument('--author-result',type=Path,required=True);p.add_argument('--proof',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();auth=json.loads(a.author_result.read_text())
    def scalar(z):return s.Rational(z[0])+s.I*s.Rational(z[1])
    def matrix(x):return s.Matrix([[scalar(z)for z in row]for row in x])
    def norm(m):return m.applyfunc(s.expand)
    sectors=[matrix(q)for q in auth['sector_matrices']]
    inverses=[norm(q.inv())for q in sectors]
    assert inverses==[matrix(q)for q in auth['sector_inverse_matrices']]
    Q=[norm(sum((s.I**(-j*k)*sectors[k]for k in range(4)),s.zeros(3))/4)for j in range(4)]
    R=[norm(sum((s.I**(-j*k)*inverses[k]for k in range(4)),s.zeros(3))/4)for j in range(4)]
    assert Q==[matrix(q)for q in auth['polynomial_coefficients']]
    assert R==[matrix(q)for q in auth['inverse_polynomial_coefficients']]
    def convolution(x,y):return [norm(sum((x[j]*y[(k-j)%4]for j in range(4)),s.zeros(3)))for k in range(4)]
    assert convolution(Q,R)==convolution(R,Q)==[s.eye(3),s.zeros(3),s.zeros(3),s.zeros(3)]

    def elementary(op):
        m=s.eye(3);kind,i=op[:2]
        if kind=='ADD':m[i,op[2]]=scalar(op[3])
        elif kind=='SCALE':m[i,i]=scalar(op[2])
        elif kind=='SWAP':m.row_swap(i,op[2])
        else:raise ValueError(kind)
        return m
    expanded=[]
    for sector,recipe in zip(sectors,auth['reduction_recipes']):
        literal=[]
        for op in recipe:
            if op[0]=='ADD':
                c=scalar(op[3]);assert c!=0
                src=op[2];dest=op[1]
                scale=s.eye(3);scale[src,src]=c
                add=s.eye(3);add[dest,src]=1
                unscale=s.eye(3);unscale[src,src]=1/c
                assert norm(unscale*add*scale)==elementary(op)
                literal.extend([scale,add,unscale])
            else:literal.append(elementary(op))
        product=s.eye(3)
        for e in literal:product=norm(e*product)
        assert norm(product*sector)==norm(sector*product)==s.eye(3)
        forward=s.eye(3)
        for e in reversed(literal):forward=norm(e.inv()*forward)
        assert forward==sector
        nadd=sum(o[0]=='ADD'for o in recipe);nscale=sum(o[0]=='SCALE'for o in recipe);nswap=sum(o[0]=='SWAP'for o in recipe)
        assert nadd<=6 and nscale<=3 and nswap<=3
        expanded.append({'unweighted_ADD':nadd,'SCALE':nscale+2*nadd,'SWAP':nswap})

    # Literal 16-address monomial tables from the independent bit formulas.
    def monomial(perm,phase):
        m=s.zeros(16)
        for x in range(16):
            bits=[(x>>j)&1 for j in range(4)];dest=perm(*bits);m[sum(z<<j for j,z in enumerate(dest)),x]=s.I**(phase(*bits)%4)
        return m
    identity=s.eye(16)
    source_s=monomial(lambda a,b,c,d:(b,c,d,a),lambda a,b,c,d:2*a*b*d)
    left=monomial(lambda a,b,c,d:(a,b^(c*d),c,d),lambda a,b,c,d:c*d*(2*a+2*b-1))
    right=monomial(lambda a,b,c,d:(a,b,c^(a*b),d),lambda a,b,c,d:a*b*(1+2*c+2*d))
    db=s.diag(*[s.I**((x>>1)&1)for x in range(16)])
    tables=[]
    for adapter in [identity,source_s,left,source_s*right]:
        h=norm(adapter.conjugate().T*db*adapter)
        beta=[]
        for x in range(16):
            pi=next(y for y in range(16)if adapter[y,x]!=0);beta.append((pi>>1)&1)
        assert h==s.diag(*[s.I**b for b in beta])
        assert beta.count(0)==beta.count(1)==8
        assert h**4==identity
        tables.append(beta)
    assert len({tuple(b)for b in tables})==4
    assert norm(right*db*right)==db
    if 'direct_phase_tables'in auth:assert tables==auth['direct_phase_tables']
    counts={}
    for width in range(1,8):
        row=[8**width*sum(math.comb(width,k)for k in range(width+1)if k%4==j)for j in range(4)]
        assert sum(row)==16**width
        if width>=3:assert all(row)
        counts[width]=row
    assert counts[1][3]==counts[2][3]==0
    # Enumerate all literal addresses through width3, with a nonlinear table.
    for width in [1,2,3]:
        got=[0]*4
        for xs in itertools.product(range(16),repeat=width):got[sum(tables[3][x]for x in xs)%4]+=1
        assert got==counts[width]
    bad=sectors[:];bad[3]=s.diag(1,1,0)
    rank_by_width={v:sum(counts[v][j]*bad[j].rank()for j in range(4))for v in [1,2,3]}
    assert rank_by_width[1]==3*16 and rank_by_width[2]==3*16**2 and rank_by_width[3]<3*16**3
    # Compare every diagonal column at width2, including the nonlinear table.
    mismatches=0
    for x,y in itertools.product(range(16),repeat=2):
        u,v=tables[3][x],tables[3][y]
        collective=1+s.Rational(1,2)*s.I**(u+v)
        wrong=(1+s.Rational(1,2)*s.I**u)*(1+s.Rational(1,2)*s.I**v)
        mismatches+=s.expand(collective-wrong)!=0
    assert mismatches==256
    out={'status':'PASS_ROOT_INDEPENDENT_CYCLIC_UNIT_AND_DIRECT_CONTROL',
      'author_result_sha256':hashlib.sha256(a.author_result.read_bytes()).hexdigest(),'proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),
      'independent_method':'SymPy Gaussian-rational inversion/convolution and explicit elementary matrices; no author code imported.',
      'both_inverse_polynomial_products':True,'actual_expanded_recipes':expanded,
      'universal_conservative_unweighted_instruction_bound':{'ADD':24,'SCALE':60,'SWAP':12,'monomial_adapters':0},
      'direct_beta_tables':tables,'spectrum_counts':counts,
      'singular_sector_control_ranks':rank_by_width,
      'tensor_of_sum_control_disagrees_on_width2_columns':mismatches,
      'all_actual_addresses_checked_through_width':3,
      'scope':'Finite algebra and implementation controls plus separately reviewed universal Fourier/direct-scan proof. Fixed scalar arithmetic, precision/tape/compiler contracts and all supplier expenses retained; no independent421 endpoint or new kappa.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])


if __name__=='__main__':main()
