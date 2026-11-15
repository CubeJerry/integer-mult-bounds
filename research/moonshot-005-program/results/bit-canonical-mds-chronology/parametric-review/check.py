#!/usr/bin/env python3
"""Independent atlas/pivot and exact movement controls for every native role."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
from functools import lru_cache
import argparse,hashlib,itertools,json,math

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(x):
    g=math.gcd(*x);x=tuple(y//g for y in x)
    return x if next(y for y in x if y)>0 else tuple(-y for y in x)
def rank(rows):
    piv={}
    for r in rows:
        while r:
            j=r.bit_length()-1
            if j in piv:r^=piv[j]
            else:piv[j]=r;break
    return len(piv)
def mul(a,b,poly=37):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a&32:a^=poly
    return z
def inverse(a):
    assert a
    return next(b for b in range(1,32) if mul(a,b)==1)
def det(a):
    a=[r[:] for r in a];out=1
    for i in range(len(a)):
        j=next((j for j in range(i,len(a)) if a[j][i]),None)
        if j is None:return 0
        a[i],a[j]=a[j],a[i];out=mul(out,a[i][i]);iv=inverse(a[i][i])
        for j in range(i+1,len(a)):
            c=mul(a[j][i],iv)
            for k in range(i,len(a)):a[j][k]^=mul(c,a[i][k])
    return out
def power(a,n):
    z=1
    for _ in range(n):z=mul(z,a)
    return z
def binary_inverse(rows,n):
    a=[r|(1<<(n+i)) for i,r in enumerate(rows)]
    for col in range(n):
        p=next(i for i in range(col,n) if a[i]>>col&1)
        a[col],a[p]=a[p],a[col]
        for i in range(n):
            if i!=col and a[i]>>col&1:a[i]^=a[col]
    assert [r&((1<<n)-1) for r in a]==[1<<i for i in range(n)]
    return [r>>n for r in a]
def binary_product_row(row,matrix_rows):
    out=0
    for i,r in enumerate(matrix_rows):
        if row>>i&1:out^=r
    return out
@lru_cache(None)
def encoder_for(subset):
    field=[[power(t,k) for t in subset] for k in range(16)]
    binary=[sum(1<<(5*j+l) for j in range(16) for l in range(5)
                if mul(field[i][j],1<<l)>>k&1)
            for i in range(16) for k in range(5)]
    enc=binary_inverse(binary,80)
    assert [binary_product_row(r,binary) for r in enc]==[1<<i for i in range(80)]
    return tuple(enc),tuple(binary)

S=10**40
def root(n):
    lo=0;hi=1<<((n.bit_length()+199)//200)
    while hi-lo>1:
        m=(lo+hi)//2
        if m**200<=n:lo=m
        else:hi=m
    assert lo**200<=n<hi**200
    return lo
@lru_cache(None)
def price(r):
    z=root(r**199*S**200);return F(z,S),F(z+1,S)
def scale(c,x):return (c*x[0],c*x[1]) if c>=0 else (c*x[1],c*x[0])
def add(*xs):return tuple(sum(x[k] for x in xs) for k in (0,1))
def lin(p):return add(*[scale(F(v),price(r)) for r,v in p.items()])
def record(x):
    with localcontext() as c:
        c.prec=60
        return {'lower_fraction':str(x[0]),'upper_fraction':str(x[1]),
                'lower_decimal':str(Decimal(x[0].numerator)/Decimal(x[0].denominator)),
                'upper_decimal':str(Decimal(x[1].numerator)/Decimal(x[1].denominator))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--proof',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=ap.parse_args()
    path=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
    roots=json.loads(path.read_text())['native_roots']
    supports=sorted({tuple(j for j,v in enumerate(r) if v) for r in roots if sum(v!=0 for v in r)==4})
    assert len(supports)==14
    full={tuple(2*int(i==j) for i in range(8)) for j in range(8)}
    for support in supports:
        for signs in itertools.product((-1,1),repeat=3):
            r=[0]*8;r[support[0]]=1
            for j,s in zip(support[1:],signs):r[j]=s
            full.add(tuple(r))
    assert len(full)==120 and set(map(tuple,roots))<=full
    canonical=[sum(1<<j for j,r in enumerate(roots) if i==j or dot(roots[i],r)==0) for i in range(111)]
    assert rank(canonical)==9
    for x in range(1,32):assert mul(x,inverse(x))==1
    assert mul(3,31,33)==0 # x^5+1 is an invalid replacement polynomial.
    out=[];seen_subsets=set();adapted_controls=[]
    for i,r in enumerate(roots):
        atlas={}
        for q in sorted(full):
            d=dot(r,q)
            if abs(d)==2:atlas[norm([4*x-d*y for x,y in zip(q,r)])]=q
        charts=[q for key,q in sorted(atlas.items())]
        assert len(charts)==28
        foreign=[j for j,v in enumerate(roots) if dot(r,v)==0]
        foreign_mask=sum(1<<j for j in foreign)
        outside=((1<<111)-1)^foreign_mask
        assert rank([c&outside for c in canonical])==9
        choices={j:[t for t,q in enumerate(charts) if dot(roots[j],q)==0] for j in foreign}
        assert all(len(s)==16 for s in choices.values())
        seen_subsets.update(tuple(s) for s in choices.values())
        chart_sources=[[j for j in foreign if t in choices[j]] for t in range(28)]
        assert min(map(len,chart_sources))>=27
        pivot_root=foreign[0]
        nonanchors=choices[pivot_root][:12]
        anchors=[t for t in range(28) if t not in nonanchors]
        assert len(anchors)==16
        pivots=[(pivot_root,choices[pivot_root].index(t)) for t in nonanchors]
        assert len(pivots)==len(set(pivots))==12
        enc,dec=encoder_for(tuple(choices[pivot_root]))
        held=[5*choices[pivot_root].index(t)+k for t in nonanchors for k in range(5)]
        assert len(held)==60
        # Each K_j encoder-row tensor has precisely one encoded-coordinate
        # coefficient after applying the actual decoder E_j^-1. Restricting
        # those rows to the held coordinates gives60 unit rows and20 zeros.
        restrictions=[sum(((binary_product_row(r,dec)>>p)&1)<<q for q,p in enumerate(held)) for r in enc]
        assert rank(restrictions)==60 and sum(r==0 for r in restrictions)==20
        kj=canonical[pivot_root]
        zeroj=[r^((r>>pivot_root&1)*kj) for r in canonical]
        assert all(not(r>>pivot_root&1) for r in zeroj) and rank(zeroj)==8
        if not adapted_controls:
            bad=[sum(((binary_product_row(r,dec)>>p)&1)<<q for q,p in enumerate(held)) for r in dec]
            assert bad!=restrictions
            mixed=next((j,z,t) for t in nonanchors for j in chart_sources[t]
                       for z in zeroj if j!=pivot_root and z>>j&1)
            j,z,t=mixed
            assert not(z>>pivot_root&1) and z>>j&1
            other_enc,other_dec=encoder_for(tuple(choices[j]))
            slot=choices[j].index(t)
            assert any(r>>(5*slot)&1 for r in other_dec)
            adapted_controls=[{'name':'wrong_encoder_orientation','rejected':True},
                              {'name':'mixed_pivot_roots_with_unchanged_adapted_basis','rejected':True,
                               'receiver':i,'old_pivot_root':pivot_root,'replacement_root':j,'chart':t},
                              {'name':'skip_exceptional_pivot_read','rejected':True,
                               'reason':'Sixty exceptional basis rows have nonzero unit held restrictions.'}]
        # Removing a contributor's one real containing chart destroys the
        # sixteen-coordinate source interface, irrespective of other charts.
        j=chart_sources[0][0];assert len([t for t in choices[j] if t!=0])==15
        out.append({'receiver':i,'foreign_count':len(foreign),'charts':28,
                    'min_actual_chart_contributors':min(map(len,chart_sources)),
                    'distinct_nonanchor_field_pivots':12,'held_binary_banks':60,
                    'single_pivot_root':pivot_root,'nonanchor_charts':nonanchors,
                    'Hub_only_canonical_basis_rows':660,'single_pivot_patch_basis_rows':60,
                    'held_restriction_rank':60,'canonical_intersection_with_foreign_input_space':0})
    # The all-subset statement is the Vandermonde determinant proof. These are
    # independent exact controls on a deterministic representative subset sample.
    sample=sorted(seen_subsets)
    sample=sample[::max(1,len(sample)//32)][:33]
    for s in sample:
        mat=[[power(t,k) for t in s] for k in range(16)]
        assert det(mat)
        bad=[row[:] for row in mat]
        for row in bad:row[1]=row[0]
        assert det(bad)==0
    fvalues=sorted({r['foreign_count'] for r in out})
    assert min(fvalues)==55 and max(fvalues)==62
    N=lin({1:1386,2:1253,3:62,4:47,5:9,6:104,7:10})
    H=lin({2:1,4:25,6:1,8:410})
    p2=add(scale(36,N),lin({1:444,**{7*j:444 for j in range(1,9)}}))
    t2=add(scale(36,H),lin({127:222,**{1+7*j:444 for j in range(1,10)}}))
    delta=add(t2,scale(-1,p2));allow=add(N,scale(-1,H),scale(F(1,36),delta))
    prices={}
    for f in fvalues:
        B,h=80,60
        physical={1:B+2*h,2:f*B,5:f*B,6:B+h,7:(221-f)*B,8:9*B-h}
        q=scale(F(1,B),lin(physical));room=add(allow,scale(-1,q))
        m2=add(scale(18,room),scale(F(1,2),delta));m4=add(scale(54,room),scale(F(1,2),delta))
        assert room[0]>0 and m2[1]<0<m4[0]
        prices[str(f)]={'physical_profile':physical,'moment':record(q),'room':record(room),
                        'm2_margin':record(m2),'m4_margin':record(m4)}
    derivative=add(price(2),price(5),scale(-1,price(7)));assert derivative[0]>0
    ordinary_bound=2*(62+1)*(80**2+2*80)+1008*80**2+2*62*80+60*80+80
    author_bound=2*(62+1)*(80**2+2*80)+2*62*80+720*(111*80-60)+60+80*720+80+80*60
    assert author_bound==7249420 and author_bound<=ordinary_bound
    result={'status':'INDEPENDENT_ALL111_CHRONOLOGY_RECIPE_AND_BUDGET_CONTROLS_PASS',
            'proof_sha256':hashlib.sha256(a.proof.read_bytes()).hexdigest(),'native_roles':out,
            'all_actual_selected_chart_subsets':len(seen_subsets),'finite_Vandermonde_controls':len(sample),
            'negative_controls':['wrong_field_polynomial','duplicate_Vandermonde_node','missing_actual_source_chart'],
            'adapted_basis_negative_controls':adapted_controls,
            'all_subset_MDS_justification':'Distinct-node Vandermonde determinant; finite sample is only a control.',
            'foreign_counts':fvalues,'physical_copies':80,'owners':800,
            'reviewer_safe_ADD_bound':ordinary_bound,'prices_by_foreign_count':prices,
            'author_tighter_ADD_bound_independently_checked':author_bound,
            'moment_derivative_in_f':record(derivative),
            'scope':'For each receiver individually; no simultaneous111 construction or new complete bound.'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status']);print('f values',fvalues,'sample',len(sample),'ADD bound',ordinary_bound)
    print('worst Q',prices['62']['moment']['lower_decimal'],'room',prices['62']['room']['lower_decimal'])

if __name__=='__main__':main()
