#!/usr/bin/env python3
"""Independent literal source and primitive checks for non-diagonal controls."""
from __future__ import annotations
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as s

def tidy(m):return m.applyfunc(s.expand)
def scalar(z):return s.Rational(z[0])+s.I*s.Rational(z[1])
def matrix(rows):return s.Matrix([[scalar(z)for z in row]for row in rows])

def main():
    parser=argparse.ArgumentParser()
    for name in ['author-result','proof','out']:parser.add_argument('--'+name,type=Path,required=True)
    args=parser.parse_args();data=json.loads(args.author_result.read_text())
    primitive_summaries=[];mutations=[]
    for number,case in enumerate(data['cases']):
        m=case['order'];zeta=s.I**(4//m);qs=[matrix(q)for q in case['sectors']]
        ds=[s.expand(q.det())for q in qs];assert ds==[scalar(case['determinant'])]*m and ds[0]!=0
        def op_matrix(op,sector):
            out=s.eye(3);kind=op[0]
            if kind=='MONOMIAL':out[op[1],op[1]]=zeta**(sector*op[2])
            elif kind=='SCALE':out[op[1],op[1]]=scalar(op[2])
            elif kind=='ADD':
                assert scalar(op[3])==1 and op[1]!=op[2]
                out[op[1],op[2]]=1
            else:raise AssertionError(kind)
            return out
        def execute(ops,sector):
            out=s.eye(3)
            for op in ops:out=tidy(op_matrix(op,sector)*out)
            return out
        fwd,inv=case['primitive_forward'],case['primitive_inverse']
        for sector in range(m):
            forward=execute(fwd,sector);inverse=execute(inv,sector)
            assert forward==qs[sector]
            assert tidy(inverse*forward)==tidy(forward*inverse)==s.eye(3)
        poly=[matrix(q)for q in case['polynomial_coefficients']]
        ipoly=[matrix(q)for q in case['inverse_coefficients']]
        for sector in range(m):
            assert tidy(sum((zeta**(sector*j)*poly[j]for j in range(m)),s.zeros(3)))==qs[sector]
            assert tidy(sum((zeta**(sector*j)*ipoly[j]for j in range(m)),s.zeros(3)))==tidy(qs[sector].inv())
        for left,right in [(poly,ipoly),(ipoly,poly)]:
            for k in range(m):
                actual=tidy(sum((left[j]*right[(k-j)%m]for j in range(m)),s.zeros(3)))
                assert actual==(s.eye(3)if k==0 else s.zeros(3))
        counts={name:sum(op[0]==name for op in fwd)for name in ['ADD','SCALE','MONOMIAL']}
        assert counts==case['counts']
        assert counts['ADD']<=27*m*m and counts['SCALE']<=54*m*m+1 and counts['MONOMIAL']<=54*m*(m-1)
        assert all(len(recipe)<=27 for recipe in case['reductions'])
        primitive_summaries.append({'case':number,'order':m,'forward':counts,'inverse':{name:sum(op[0]==name for op in inv)for name in counts}})
        ix=next(i for i,o in enumerate(fwd)if o[0]=='MONOMIAL');bad=fwd[:ix]+fwd[ix+1:]
        assert any(execute(bad,sector)!=qs[sector]for sector in range(m))
        mutations.append('one monomial service omitted, case'+str(number))

    def elementary(i,j,c):
        out=s.eye(3);out[i,j]=c;return out
    def w(i,j,t):return tidy(elementary(i,j,t)*elementary(j,i,-1/t)*elementary(i,j,t))
    for t in [s.Rational(2),s.I,1+s.I,s.Rational(1,3)-2*s.I]:
        assert tidy(w(0,1,t)*w(0,1,-s.Integer(1)))==tidy(s.diag(t,1/t,1))
        for sector in range(4):
            z=s.I**sector;g=s.diag(1,z,1);scale=s.diag(1,t,1)
            assert tidy(g.inv()*scale.inv()*elementary(0,1,1)*scale*g)==tidy(elementary(0,1,t*z))

    # Four local sign cases prove the arbitrary fixed Boolean-table formula.
    x=s.Matrix([[0,1],[1,0]]);z=s.diag(1,-1);y=s.Matrix([[0,-s.I],[s.I,0]])
    c=((1+s.I)*s.eye(2)+(1-s.I)*x)/2
    for mu,nu in itertools.product(range(2),repeat=2):
        sign=(-1)**mu*z**nu
        assert tidy(c.conjugate().T*sign*c)==(-1)**mu*y**nu
        assert tidy(c*sign*c.conjugate().T)==(-1)**mu*(-y)**nu

    identity=s.eye(16);rotation=s.zeros(16);cubic=s.eye(16);flip=s.zeros(16)
    for j in range(16):
        rotation[(j>>1)|((j&1)<<3),j]=1;cubic[j,j]=-1 if(j&13)==13 else 1;flip[j^2,j]=1
    a=tidy(((1+s.I)*identity+(1-s.I)*flip)*cubic*rotation/2);ai=a.conjugate().T
    assert tidy(ai*a)==identity
    def from_table(table):
        out=s.zeros(16)
        for j,(destination,phase)in enumerate(table):out[destination,j]=s.I**phase
        return out
    controls={}
    for entry in data['general_sign_family_controls']:
        fs=entry['boolean_table'];h=s.diag(*[(-1)**f for f in fs]);actual=[tidy(ai*h*a),tidy(a*h*ai)]
        for orientation,k in enumerate(actual):
            assert k==from_table(entry['control_tables'][orientation])
            assert tidy(k*k)==identity and tidy(k.conjugate().T*k)==identity
            assert all(sum(k[i,j]!=0 for i in range(16))==1 for j in range(16))
        for width in [1,2,3,7]:
            n=16**width;trace=(16-2*sum(fs))**width
            assert entry['sector_counts'][str(width)]==[(n+trace)//2,(n-trace)//2]
        controls[entry['name']]={'negative_multiplicity':sum(fs),'moved_addresses':[sum(pair[0]!=j for j,pair in enumerate(table))for table in entry['control_tables']]}
    quartic=s.diag(*[-1 if j==15 else 1 for j in range(16)]);km,kp=tidy(ai*quartic*a),tidy(a*quartic*ai)
    assert km==from_table(data['control_tables']['Kminus']) and kp==from_table(data['control_tables']['Kplus'])
    assert tidy(a*km)==tidy(quartic*a) and tidy(kp*a)==tidy(a*quartic)
    channel_counts={}
    for name,k in [('Kminus',km),('Kplus',kp)]:
        assert s.trace(k)==14;projectors=[(identity+k)/2,(identity-k)/2]
        channel_counts[name]=sum(tidy(left*a*right)!=s.zeros(16)for left in projectors for right in projectors)
        assert channel_counts[name]==4
    wrong=km.conjugate();assert wrong!=km and tidy(a*wrong)!=tidy(quartic*a)
    mutations.append('conjugated source phases violate actual intertwining')

    # Only the idle image column is rescaled, leaving all active channels fixed.
    old_q=[matrix(q)for q in data['cases'][0]['sectors']];old_q[1]=s.diag(2,1,1)*old_q[1]
    old_r=[tidy(q.inv())for q in old_q];p=s.diag(0,0,1);e=s.zeros(3);e[0,1]=1
    new_r=[];new_q=[]
    for r in old_r:
        normalized=tidy(r*s.diag(1,1,1/r.det()));q=tidy(normalized.inv())
        assert normalized.det()==q.det()==1;new_r.append(normalized);new_q.append(q)
    for i in range(2):assert tidy(new_r[i]*p*new_q[i])==tidy(old_r[i]*p*old_q[i])
    for i,j in itertools.product(range(2),repeat=2):assert tidy(new_r[i]*e*new_q[j])==tidy(old_r[i]*e*old_q[j])
    author_normalized=[matrix(q)for q in data['cases'][3]['sectors']];author_inverse=[tidy(q.inv())for q in author_normalized]
    for i in range(2):assert tidy(author_inverse[i]*p*author_normalized[i])==tidy(old_r[i]*p*old_q[i])
    for i,j in itertools.product(range(2),repeat=2):assert tidy(author_inverse[i]*e*author_normalized[j])==tidy(old_r[i]*e*old_q[j])
    assert old_q[0].det()!=old_q[1].det()
    result={'status':'PASS_ROOT_INDEPENDENT_NONDIAGONAL_CYCLIC_IMPLEMENTATION','proof_sha256':hashlib.sha256(args.proof.read_bytes()).hexdigest(),'author_result_sha256':hashlib.sha256(args.author_result.read_bytes()).hexdigest(),
      'method':'Independent SymPy exact scalar, spectral and literal16-address matrix calculations; no author code imported.','primitive_recipe_checks':primitive_summaries,'all_four_two_by_two_sign_cases':True,'source_controls':controls,'quartic_nonzero_source_channels':channel_counts,
      'idle_column_determinant_normalization_preserves_all_cross_channels':True,'negative_controls':mutations,'universal_scope':'Written finite elementary-factor/source-table proof; no profitable endpoint or complete supplier. Norm equality requires every spectral sector to occur.','new_complete_kappa':False}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
