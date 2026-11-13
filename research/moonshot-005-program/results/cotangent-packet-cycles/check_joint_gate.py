#!/usr/bin/env python3
"""Exact native coupled Schur gate, without assumed source acquisition."""
import argparse,gzip,hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
def det(A):
    B=[list(r) for r in A];ans=F(1)
    for k in range(len(B)):
        z=next((i for i in range(k,len(B)) if B[i][k]),None)
        if z is None:return F(0)
        if z!=k:B[k],B[z]=B[z],B[k];ans=-ans
        c=B[k][k];ans*=c
        for i in range(k+1,len(B)):
            q=B[i][k]/c
            if q:B[i]=[x-q*y for x,y in zip(B[i],B[k])]
    return ans
def main(a):
    sys.path.insert(0,str(a.repo/'research/moonshot-005-program/results/joint-current-row-codes/review-star'))
    from engine import rank,root9
    blob=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();pin='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';assert hashlib.sha256(blob).hexdigest()==pin
    s=json.loads(gzip.decompress(blob));H=[s['live'][k] for k in s['hosted']['Dports']];U=[i for i in s['live'] if i not in H]
    roots={i:root9(s['frames'][s['initial'][i]][0]) for i in H+U};G=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))/2
    GH=[[G(i,j) for j in H] for i in H];A=[[G(i,j) for j in U] for i in H];T=[[G(i,j) for j in H] for i in U];C=[[G(i,j) for j in U] for i in U];D=[[F(i==j)-C[i][j] for j in range(8)] for i in range(8)]
    assert rank(GH)==8 and rank(C)==7 and rank(D)==8
    zero_top=[[F(0)]*8 for _ in H];zero_bottom=[[F(0)]*96 for _ in U];I=[[F(i==j) for j in range(8)] for i in range(8)]
    join=lambda X,Y,Z:[x+y for x,y in zip(GH,X)]+[x+y for x,y in zip(Y,Z)]
    cases={'independent_unchanged_coupled':rank(join(zero_top,zero_bottom,I)),'native_cross_both_without_coupled_self_response':rank(join(A,T,I)),'full_native_Gram_response':rank(join(A,T,C)),'native_cross_with_only_negative_identity_self_response':rank(join(A,T,[[F(0)]*8 for _ in U]))}
    assert cases=={'independent_unchanged_coupled':16,'native_cross_both_without_coupled_self_response':16,'full_native_Gram_response':8,'native_cross_with_only_negative_identity_self_response':15}
    u=[F(1),F(-1),F(0),F(-1),F(1),F(0),F(0),F(0)]
    assert all(sum(c*v for c,v in zip(row,u))==0 for row in C+A)
    S=[[C[i][j]-F(i==j) for j in range(8)] for i in range(8)];assert rank(S)==8
    assert [sum(c*v for c,v in zip(row,u)) for row in S]==[-v for v in u]
    B=[5,56,65,69,77,96,100,103]
    returned=[[G(b,j) for j in H+U] for b in B]
    retained=[[sum(C[i][k]*T[k][j] for k in range(8)) for j in range(96)]+[F(0)]*8 for i in range(8)]
    E=join(A,T,I);one=[F(0)]*104;one[96]=F(1)
    conditional={'retained_pure_observation_rank':rank(retained),'retained_plus_eight_Gram_return_rank':rank(retained+returned),'joint_target_rank_after_both':rank(retained+returned+E),'missing_dimensions_after_both':rank(retained+returned+E)-rank(retained+returned),'one_original_y17_information_completes':rank(retained+returned+[one])==16}
    assert conditional['retained_pure_observation_rank']==7 and conditional['retained_plus_eight_Gram_return_rank']==15 and conditional['missing_dimensions_after_both']==1 and conditional['one_original_y17_information_completes']
    r={'status':'PASS_EXACT_NATIVE_COUPLED_SCHUR_GATE','native_sha256':pin,'hosted_ports':H,'coupled_ports':U,'hosted_Gram_rank':8,'coupled_Gram_rank':7,'I_minus_coupled_Gram_rank':8,'det_I_minus_coupled_Gram':str(det(D)),'coupled_Gram':[[str(x) for x in row] for row in C],'coupled_Gram_kernel':list(map(str,u)),'full_required_coupled_self_response_rank':8,'joint_ranks':cases,'scope':'Characteristic-zero algebraic gate with stated final additive-decoder/no-extra-pure-observation premises. Native cross/self responses and full forward acquisition are not supplied; no source implementation or global impossibility claimed.'}
    r['conditional_original_coupled_X_cache_case']=conditional
    r['conditional_cache_premise']='Actual independently retained C*x_U, C=G_UU, plus actual native T=G_UH response. Neither premise is constructed; information count is not a transport upper bound.'
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','det_I_minus_coupled_Gram','joint_ranks','conditional_original_coupled_X_cache_case']},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
