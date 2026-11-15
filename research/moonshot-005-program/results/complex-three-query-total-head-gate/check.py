#!/usr/bin/env python3
"""Exact finite controls for the Gaussian Schur and maximal-endpoint arguments."""
import argparse,hashlib,importlib.util,json,sys
from pathlib import Path

def rank(rows,p=101):
    a=[[(x+10*y)%p for x,y in row] for row in rows];r=0
    for j in range(len(a[0])):
        z=next((k for k in range(r,len(a)) if a[k][j]),None)
        if z is None:continue
        a[r],a[z]=a[z],a[r];iv=pow(a[r][j],-1,p);a[r]=[(iv*x)%p for x in a[r]]
        for k in range(r+1,len(a)):
            c=a[k][j]
            if c:a[k]=[(x-c*y)%p for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r

def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--output',type=Path);ar=ap.parse_args()
    helper=ar.repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
    sha=hashlib.sha256(helper.read_bytes()).hexdigest();assert sha=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
    sp=importlib.util.spec_from_file_location('retained_dyadic_total',helper);m=importlib.util.module_from_spec(sp);sys.modules[sp.name]=m;sp.loader.exec_module(m)
    I=m.eye(16);Z=m.zero(16)
    def C(bit):
        x=m.monomial([j^(1<<bit) for j in range(16)],[0]*16)
        return m.M((I.scale((1,1))+x.scale((1,-1))).a,1).norm()
    ca,cb,cc,cd=[C(i) for i in range(4)]
    perm=[3,0,1,2];smap=[sum(((j>>k)&1)<<perm[k] for k in range(4)) for j in range(16)]
    S=m.monomial(smap,[0]*16);a=cb@S
    assert S@cb@S.star()==ca and ca.star()@S@cb@S==S.power(2)
    assert S.star()@ca@S.power(2)==a
    assert ca@cb@S.power(2)==a.power(2)
    assert a.power(4)==ca@cb@cc@cd and a.power(16)==I
    pattern=[m.gaussian_rank(a.power(k)) for k in range(16)]
    assert pattern==[0,1,2,3,4,3,2,1]*2
    assert m.gaussian_rank(a.power(4).tp(2))==8
    G4=ca@cb@cc@cd;H=ca@cb;g=ca;k=cb
    pa=m.monomial(list(range(16)),[j&1 for j in range(16)])
    pb=m.monomial(list(range(16)),[(j>>1)&1 for j in range(16)])
    P=I+pa;Q=I+pb;P1=I;P2=pa;Q1=I;Q2=pb
    X1=g.star()@P1@H;X2=g.star()@P2@H
    Y1=H@Q1@k.star();Y2=H@Q2@k.star()
    assert [m.gaussian_rank(t) for t in (X1,X2,Y1,Y2)]==[1,2,1,2]
    X=X1+X2;Y=Y1+Y2;A2=X2@H.star()@Y2
    assert A2==g.star()@P2@H@Q2@k.star() and m.gaussian_rank(A2)==2
    N2=m.block([[A2,X2],[Y2,H]])
    assert rank(N2.a)==16
    mutant=m.block([[A2+H,X2],[Y2,H]])
    assert rank(mutant.a)==32
    low=cc
    N=m.block([[A2+low,X],[Y,H]])
    M=m.diagonal([g,I])@N@m.diagonal([k,I])
    G=g@low@k+(P@H@Q).scale((-1,0))+P2@H@Q2
    assert M==m.block([[G+P@H@Q,P@H],[H@Q,H]])
    assert m.gaussian_rank(g@low@k)==3
    # The actual homogeneous endpoint H is essential for coefficient partition.
    Hsum=H+(pa@H).scale((2,0))
    assert rank(Hsum.a)==16
    assert g.star()@Hsum==X1+X2.scale((2,0))
    # One ordinary basis term now produces both ranks1,2; normalization is needed.
    # A changed query/image leaving F2 must be rejected before the Schur step.
    swap=m.monomial([((j&1)<<2)|((j&4)>>2)|(j&10) for j in range(16)],[0]*16)
    rank3=g.star()@swap@H
    assert m.gaussian_rank(rank3)==3
    # Independent rank4 column is unchanged by inverse outer shear, but an
    # in-place inverse can lower it to rank3. Both statements are exact.
    endpoint=m.diagonal([G4,H]);shear=m.block([[I,g.scale((-1,0))],[Z,I]])
    before_shear=shear@endpoint
    assert before_shear.a[:16]==m.block([[G4,(g@H).scale((-1,0))],[Z,H]]).a[:16]
    assert before_shear.a[:16] != m.block([[Z,(g@H).scale((-1,0))],[Z,H]]).a[:16]
    lower=g.star()@G4;assert m.gaussian_rank(lower)==3
    before_inplace=m.diagonal([g.star(),I])@endpoint
    assert before_inplace==m.diagonal([lower,H])
    # Changing the independent endpoint to a duplicate lowers physical rank.
    duplicate=m.block([[G4,Z],[G4,Z]])
    assert rank(duplicate.a)==16 and rank(endpoint.a)==32
    out={'status':'PASS_EXACT_TOTAL_HEAD_AND_GAUSSIAN_SCHUR_CONTROLS','helper_sha256':sha,
      'four_head_source':{'one_column_size':16,'rank_powers_mod16':pattern,'width2_fourth_power_rank':8,'cycle_gauge_identities':True,'spectator_volume_factor':'4^V relative to two-head source; not a free compiled supplier'},
      'schur':{'ordinary_partition_ranks':[1,2,1,2],'rank_of_pure_E2_block':rank(N2.a),'mutant_rank_with_extra_independent_E2_corner':rank(mutant.a),'reconstructed_high_residual_max_rank':3,'all_columns_checked':32},
      'negative_controls':{'omit_one_query_high_component_rank_gate_rejected':True,'nonhomogeneous_H_needs_prior_Gaussian_normalization':True,'rank3_cross_entry_violates_F2_preword':True,'outer_shear_preserves_isolated_rank4_column':True,'outer_inplace_can_reduce_rank4_to3':True,'duplicate_rank4_outputs_have_only_half_required_rank':True},
      'scope':'Exact finite source/Schur controls; written universal proof separate. No exhaustive caller search, four-head supplier or new kappa.', 'new_kappa':False}
    txt=json.dumps(out,indent=2)+'\n'
    if ar.output:ar.output.write_text(txt)
    print(txt,end='')
if __name__=='__main__':main()
