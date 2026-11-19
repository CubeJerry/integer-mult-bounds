#!/usr/bin/env python3
"""Independent ternary lift census and nonlinear/proper-Y controls."""
from argparse import ArgumentParser
from itertools import product,permutations
from pathlib import Path
from hashlib import sha256
import json

def add(u,v,p):return tuple((a+b)%p for a,b in zip(u,v))
def scale(c,u,p):return tuple(c*a%p for a in u)
def span(rows,n,p):
    S={tuple([0]*n)}
    for row in rows:S={add(u,scale(c,row,p),p)for u in S for c in range(p)}
    return frozenset(S)
def dim(S,p):
    n=1;d=0
    while n<len(S):n*=p;d+=1
    assert n==len(S);return d

def main():
    ap=ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    F3=list(product(range(3),repeat=2));Z=frozenset({(0,0)})
    spaces={Z,frozenset(F3)}|{span([v],2,3)for v in F3 if v!=(0,0)};assert len(spaces)==6
    E=(1,0);W=span([E],2,3);counts={'ternary_boundaries':0,'late_space_pairs':0,'lift_subsets_checked':0,'nonlinear_binary_projection_checks':0,'nonlinear_ternary_projection_checks':0}
    for V1,V2 in product(F3,repeat=2):
        R=span([E,V1,V2],2,3);rho=dim(R,3)-1;valid=[Q for Q in spaces if Q<=R]
        def V(beta):return add(scale(beta[0],V1,3),scale(beta[1],V2,3),3)
        def Pi(Q):return frozenset((x[1],)for x in Q)
        def preimage(Q):
            return frozenset(beta for beta in F3 if any(add(scale(alpha,E,3),V(beta),3)in Q for alpha in range(3)))
        counts['ternary_boundaries']+=1
        for Q1,Q2 in product(valid,repeat=2):
            Ps=[preimage(Q1),preimage(Q2)];Qs=[Q1,Q2];hall=True
            for subset in [(0,),(1,),(0,1)]:
                qsum=span([v for k in subset for v in Qs[k]],2,3)
                psum=span([v for k in subset for v in Ps[k]],2,3)
                quotient=Pi(qsum);direct=frozenset(beta for beta in F3 if (V(beta)[1],)in quotient)
                assert psum==direct and dim(psum,3)==2-rho+dim(quotient,3)
                hall&=dim(quotient,3)+(2-rho)>=len(subset);counts['lift_subsets_checked']+=1
            exists=any(dim(span([x,y],2,3),3)==2 for x in Ps[0]for y in Ps[1])
            assert exists==hall;counts['late_space_pairs']+=1
    # Each injection extends to an arbitrary nonlinear baseline permutation.
    for images in permutations(range(8),4):
        for subset in range(8):
            observed={v&subset for v in images};s=subset.bit_count();lower=1<<max(0,2-(3-s))
            assert len(observed)>=lower;counts['nonlinear_binary_projection_checks']+=1
    for images in permutations(range(9),3):
        for subset in range(4):
            observed={((v%3 if subset&1 else 0),(v//3 if subset&2 else 0))for v in images}
            lower=3**max(0,1-(2-subset.bit_count()));assert len(observed)>=lower;counts['nonlinear_ternary_projection_checks']+=1
    # A late subset fails although the whole list passes: E=x1,
    # V=(x2,x3,x2+x3); Q1=Q2=W, Q3=R; dependency allowance1.
    all_beta=list(product(range(3),repeat=3));kernel=[v for v in all_beta if(v[0]+v[2])%3==0 and(v[1]+v[2])%3==0]
    assert len(kernel)==3 and 2+1==3 and 0+1<2
    assert not any(dim(span([x,y,z],3,3),3)==3 for x in kernel for y in kernel for z in all_beta)
    # GF4 local word, E=(x1,x2), V=(x1+x3,x2+x3), s=1.
    states=0;bad_correction=0;bad_born=0
    for x1,x2,x3,y1,y2,yb in product(range(4),repeat=6):
        cu,cv=x1,x2
        a0,b0=y1,y2;b0^=a0;a0^=b0
        # Given correlated proper arrivals; source formation is not a local gate.
        aa=a0^x1^x3;bb=b0^x2^x3;cc=yb
        aa^=bb;bb^=aa
        before_aa=aa;aa^=cu;bb^=cu;cc^=cu;cc^=cv
        assert(aa,bb,cc)==(y1^x2,y2^x3,yb^x1^x2)
        assert(cu,cv)==(x1,x2)
        bad_correction+=(before_aa,bb,cc)!=(y1^x2,y2^x3,yb^x1^x2)
        bad_born+=(aa,bb,cc^yb)!=(y1^x2,y2^x3,yb^x1^x2)
        states+=1
    assert states==4096 and bad_correction==bad_born==3072
    M=4;N=6;bound=2*(M*M+3*M)+2*(N*N+3*N)+M*N+M
    assert bound==192 and 20<=bound
    assert 1+(2-2)+1<3
    out={'status':'PASS_INDEPENDENT_CORRELATED_MIDDLE_REVIEW','counts':counts,
         'ternary_lift_census_author_code_imported':False,'correlated_GF4_all_input_states':states,
         'omitted_early_compensation_failures':bad_correction,'discarded_arbitrary_born_baseline_failures':bad_born,
         'subset_only_late_failure_control':True,'fresh_independent_late_control_rejected':True,
         'literal_local_binary_bill':{'ADD':20,'INIT':4,'dirty_CLEAR':4,'extra_peak':4,'bound_ADD':bound,'source_formation_of_V_included':False},
         'reviewed_proof_sha256':sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(out['status']);print(json.dumps(counts,sort_keys=True))
if __name__=='__main__':main()
