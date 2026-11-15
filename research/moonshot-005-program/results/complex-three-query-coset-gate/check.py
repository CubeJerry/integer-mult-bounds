#!/usr/bin/env python3
"""Exact finite diagnostics for the written coset gate, not a caller search."""
import argparse,hashlib,importlib.util,itertools,json,sys
from pathlib import Path

def rank2(cols):
    b={}
    for x in cols:
        while x:
            j=x.bit_length()-1
            if j in b:x^=b[j]
            else:b[j]=x;break
    return len(b)
def act(M,x):
    z=0
    for i,c in enumerate(M):
        if x>>i&1:z^=c
    return z
def mul(A,B):return tuple(act(A,b) for b in B)
def inv(M):
    images={act(M,x):x for x in range(1<<len(M))}
    return tuple(images[1<<i] for i in range(len(M)))
def grank(M):return rank2([c&7 for c in M[3:]])
def ordinary_group():
    out=[]
    for cols in itertools.product(range(1,8),repeat=3):
        if rank2(cols)!=3:continue
        ai=inv(cols);ait=tuple(sum(((ai[j]>>i)&1)<<j for j in range(3)) for i in range(3))
        diag=tuple(cols)+tuple(c<<3 for c in ait)
        for bits in range(64):
            K=[0,0,0];t=0
            for i in range(3):
                for j in range(i,3):
                    if bits>>t&1:K[i]^=1<<j;K[j]^=(1<<i) if i!=j else 0
                    t+=1
            phase=tuple((1<<i)|(K[i]<<3) for i in range(3))+tuple(1<<(i+3) for i in range(3))
            out.append(mul(phase,diag))
    H=set(out);assert len(H)==10752 and all(grank(h)==0 for h in H)
    return H

def cosets():
    I=tuple(1<<i for i in range(6));cb=list(I);cb[4]^=2;cb=tuple(cb)
    perm=(2,0,1);S=tuple(1<<perm[i] for i in range(3))+tuple(1<<(perm[i]+3) for i in range(3))
    a=inv(mul(cb,S));assert grank(a)==1 and grank(mul(a,a))==2
    H=ordinary_group();hs=sorted(H);Ha={mul(h,a) for h in H}
    queries=[mul(h,a) for h in hs[::1344]];rows=[]
    for g in queries:
        gH={mul(g,h) for h in H};gHa={mul(x,a) for x in gH}
        assert not gHa&gH and not gHa&Ha
        assert all(grank(x)==1 for x in gH|Ha)
        rows.append({'query_columns':list(g),'gH_size':len(gH),'gHa_size':len(gHa),'intersections':[len(gHa&gH),len(gHa&Ha)]})
    # Double coset exclusion is universal by ordinary rank preservation;
    # these exact two-sided products are a diagnostic, not exhaustive G enumeration.
    ais=inv(a);sample=hs[::672];cnt=0
    for x in sample:
        for y in sample:
            q=mul(mul(x,ais),y);assert grank(q)==1 and q not in H;cnt+=1
    # If either outside-H premise is deleted, the claimed disjointness fails.
    assert {mul(g,h) for h in H}=={mul(mul(g,h),I) for h in H}
    assert {mul(mul(I,h),a) for h in H}==Ha
    return {'ordinary_symplectic_group_size':len(H),'rank_one_queries':rows,'two_sided_products':cnt,'negative_controls':['a=I makes gHa=gH','g=I makes gHa=Ha'],'phase_scope':'symplectic quotient checks; exact scalar phases addressed by source identities and written twisted-algebra proof'}

def modular_rank(rows,p=101,ii=10):
    a=[[(x+ii*y)%p for x,y in row] for row in rows];r=0
    if not a:return 0
    for j in range(len(a[0])):
        piv=next((k for k in range(r,len(a)) if a[k][j]),None)
        if piv is None:continue
        a[r],a[piv]=a[piv],a[r];z=pow(a[r][j],-1,p);a[r]=[(z*x)%p for x in a[r]]
        for k in range(r+1,len(a)):
            z=a[k][j]
            if z:a[k]=[(x-z*y)%p for x,y in zip(a[k],a[r])]
        r+=1
        if r==len(a):break
    return r

def source_checks(repo):
    helper=repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
    assert hashlib.sha256(helper.read_bytes()).hexdigest()=='1d3c798c43b46e1983f4dc80d68e694b93d9cdee206ad4fe4d408e5f5e29ed91'
    spec=importlib.util.spec_from_file_location('retained_exact_gaussian',helper);m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    i=m.eye(8);xb=m.monomial([j^2 for j in range(8)],[0]*8)
    cb=m.M((i.scale((1,1))+xb.scale((1,-1))).a,1).norm()
    S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);a=(cb@S).star();P=m.monomial(list(range(8)),[(j>>2)&1 for j in range(8)])
    rows=[]
    for v in (1,2):
        av=a.tp(v);iv=m.eye(av.n);z=m.zero(av.n);d=av.n
        L=m.block([[av,iv],[z,av]]);D=m.diagonal([av,av]);qip=m.diagonal([av,iv]);qsh=m.block([[iv,av],[z,iv]])
        T=av.power(6);E=m.M((iv+T).a,(iv+T).k+1).norm();F=iv+E.scale((-1,0))
        assert E@E==E and E@av==av@E and E@F==z
        assert modular_rank(E.a)==d//2 and modular_rank(F.a)==d//2
        # All scalar coefficients are outside the tensor lift.
        for pname,p in [('phase',P.tp(v)),('singular_projector',E),('zero',z)]:
            target=m.block([[av.power(2),av@p@av],[av,iv+p@av]])
            O=m.block([[z,iv.scale((-1,0))],[iv,p]])
            assert qsh@O@L==target
            Oi=m.block([[p,iv],[iv.scale((-1,0)),z]]);assert O@Oi==m.eye(2*d)
            oi=m.block([[iv,p],[z,iv]]);mix=m.block([[iv,iv.scale((-1,0))],[z,iv]])
            expect=m.block([[av.power(2),av@p@av],[z,av]])
            assert mix@qip@oi@L==expect
            rows.append({'width':v,'p':pname,'first_shear_normal_form':True,'first_inplace_normal_form':True,'all_columns':2*d})
        # Singular individual ordinary blocks do not prevent a full pure-E2 row.
        O=m.block([[E,F],[F,E]]);assert O@O==m.eye(2*d)
        mix=m.block([[iv,E.scale((-1,0))],[z,iv]])
        W=mix@qip@O@L
        expected=m.block([[E@av.power(2),F@av.power(2)],[F@av,F+E@av]])
        assert W==expected and modular_rank(W.a)==2*d
        assert modular_rank(W.a[:d])==d
        assert modular_rank((E@av.power(2)).a)==d//2
        assert modular_rank((F@av.power(2)).a)==d//2
        # Dropping independent retained inputs permits a false "two outputs" certificate.
        cut=m.block([[iv,z],[z,z]]);copy=m.block([[iv,z],[iv,z]])
        fake=copy@qip@qip@L@cut
        assert fake==m.block([[av.power(3),z],[av.power(3),z]])
        assert modular_rank(fake.a)==d and modular_rank(m.diagonal([av.power(3),av.power(3)]).a)==2*d
        rows.append({'width':v,'singular_w1_and_z1_rank':d//2,'pure_E2_row_rank':d,'whole_intermediate_rank':2*d,'nonindependent_fake_output_rank':d})
    # A one-column equality is not a faithful collective group-algebra identity.
    alpha=(1,1);beta=(1,-1)
    one=m.M((i.scale(alpha)+xb.scale(beta)).a,1).norm();assert cb==one
    iv=m.eye(64);collective=m.M((iv.scale(alpha)+xb.tp(2).scale(beta)).a,1).norm();assert cb.tp(2)!=collective
    assert a.scale((-1,0)).tp(2)!=a.tp(2).scale((-1,0))
    return {'helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'source_rows':rows,'negative_controls':['singular w1,z1 are legal and not divided by','nonindependent duplicate endpoints have only half the required rank','one-column Gaussian expansion fails collectively at width2','minus sign inside tensor is wrong at even width'],'finite_scope':'widths1,2, exact Gaussian dyadics; modular rank uses Q(i)->F101 with i=10 for exact nonzero minors; universal proof separate'}

def main():
    if not __debug__:raise RuntimeError('Assertions must be enabled')
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=Path.cwd());ap.add_argument('--output',type=Path);args=ap.parse_args()
    data={'status':'PASS_EXACT_THREE_QUERY_COSET_DIAGNOSTICS','cosets':cosets(),'source':source_checks(args.repo),'scope':'Finite diagnostics accompanying PROOF.md; not an exhaustive caller search or a new multiplier','new_kappa':False}
    text=json.dumps(data,indent=2)+'\n'
    if args.output:args.output.write_text(text)
    print(text,end='')
if __name__=='__main__':main()
