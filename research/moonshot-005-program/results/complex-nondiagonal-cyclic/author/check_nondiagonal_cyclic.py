#!/usr/bin/env python3
"""Exact elementary lowering for common-determinant cyclic ordinary units."""
from pathlib import Path
import importlib.util,sys,hashlib,json

helper=Path(__file__).with_name('check_cyclic_quarter.py')
exec(compile(helper.read_text().split('sectors=[eye(),')[0],str(helper),'exec'))

def determinant(a):
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def elementary(i,j,c):
    require(i!=j,'Off-diagonal elementary factor');a=eye();a[i][j]=lift(c);return a
def w_ops(i,j,t):
    t=lift(t);require(bool(t),'Balanced scale unit')
    return [('ADD',i,j,t),('ADD',j,i,-t.inv()),('ADD',i,j,t)]
def balanced_scale_ops(i,j,t):return w_ops(i,j,-one)+w_ops(i,j,t)
def sl_reduction(q):
    require(determinant(q)==one,'SL3 input')
    a=[list(r)for r in q];ops=[]
    def append(op):
        nonlocal a
        a=apply_op(a,op);ops.append(op)
    for c in range(3):
        if not a[c][c]:
            r=next((r for r in range(c+1,3)if a[r][c]),None)
            require(r is not None,'Invertible pivot')
            for op in w_ops(c,r,one):append(op)
        for r in range(3):
            if r!=c and a[r][c]:append(('ADD',r,c,-a[r][c]/a[c][c]))
    require(all(not a[r][c]for r in range(3)for c in range(3)if r!=c),'Diagonal reduction')
    d=[a[j][j]for j in range(3)]
    for i,j,t in [(0,1,d[0].inv()),(1,2,(d[0]*d[1]).inv())]:
        if t!=one:
            for op in balanced_scale_ops(i,j,t):append(op)
    require(a==eye()and len(ops)<=27,'Finite elementary reduction bound')
    forward=eye()
    for op in reversed(ops):forward=apply_op(forward,inverse_op(op))
    require(forward==q,'Exact elementary reconstruction')
    return ops

def pzero(order):return [zmat()for _ in range(order)]
def peye(order):return [eye()]+[zmat()for _ in range(order-1)]
def pmul(a,b):
    order=len(a);out=pzero(order)
    for j in range(order):
        for k in range(order):out[(j+k)%order]=madd(out[(j+k)%order],mm(a[j],b[k]))
    return out
def sector_interpolation(qs):
    order=len(qs);return [mscale(sum_m([mscale(qs[s],ipow(-(4//order)*s*j))for s in range(order)]),F(1,order))for j in range(order)]
def pshear(order,i,j,c,e):
    out=peye(order);out[e%order][i][j]+=c;return out
def pscale(order,bank,c):
    out=peye(order);out[0][bank][bank]=c;return out
def pmonomial(order,bank,e):
    out=peye(order);out[0][bank][bank]=zero;out[e%order][bank][bank]+=one;return out
def operation_matrix(op,order):
    if op[0]=='MONOMIAL':return pmonomial(order,op[1],op[2])
    if op[0]=='SCALE':return pscale(order,op[1],op[2])
    if op[0]=='ADD':
        require(op[3]==one,'Physical ADD must be unweighted');return pshear(order,op[1],op[2],one,0)
    raise ValueError(op)
def invert_primitive(op):
    if op[0]=='MONOMIAL':return(op[0],op[1],-op[2])
    if op[0]=='SCALE':return(op[0],op[1],op[2].inv())
    # An inverse ADD is represented by the same source-restoring lowering
    # for coefficient -1, not relabelled as a free weighted primitive.
    if op[0]=='ADD':return('SUB',op[1],op[2])
    raise ValueError(op)
def compile_monomial_shear(order,i,j,c,e):
    require(bool(c)and i!=j,'Monomial shear data');ops=[]
    if e%order:ops.append(('MONOMIAL',j,e%order))
    ops.extend([('SCALE',j,c),('ADD',i,j,one),('SCALE',j,c.inv())])
    if e%order:ops.append(('MONOMIAL',j,(-e)%order))
    out=peye(order)
    for op in ops:out=pmul(operation_matrix(op,order),out)
    require(out==pshear(order,i,j,c,e),'Literal source-restoring monomial shear')
    return ops
def compile_sectors(qs):
    order=len(qs);require(order in [2,4],'Declared cyclic order')
    determinants=[determinant(q)for q in qs]
    if not determinants[0]or any(d!=determinants[0]for d in determinants):raise ValueError('common_nonzero_determinant')
    delta=determinants[0];reductions=[];elementaries=[];primitive=[]
    for s,q in enumerate(qs):
        adjusted=apply_op(q,('SCALE',0,delta.inv()));red=sl_reduction(adjusted);reductions.append(red)
        forward=[inverse_op(op)for op in reversed(red)]
        for _,i,j,c in forward:
            elementaries.append((s,i,j,c))
            for e in range(order):
                alpha=c*ipow(-(4//order)*s*e)/order
                primitive.extend(compile_monomial_shear(order,i,j,alpha,e))
    if delta!=one:primitive.append(('SCALE',0,delta))
    out=peye(order)
    for op in primitive:out=pmul(operation_matrix(op,order),out)
    expected=sector_interpolation(qs);require(out==expected,'Compiled cyclic polynomial identity')
    # Inverse is generated at the elementary level to retain the same
    # unweighted ADD / explicit SCALE accounting as the forward recipe.
    inverse_primitive=[]
    if delta!=one:inverse_primitive.append(('SCALE',0,delta.inv()))
    for s,i,j,c in reversed(elementaries):
        for e in reversed(range(order)):
            alpha=-c*ipow(-(4//order)*s*e)/order
            inverse_primitive.extend(compile_monomial_shear(order,i,j,alpha,e))
    inverse=peye(order)
    for op in inverse_primitive:inverse=pmul(operation_matrix(op,order),inverse)
    require(pmul(out,inverse)==peye(order)and pmul(inverse,out)==peye(order),'Literal cyclic inverse recipe')
    count={name:sum(op[0]==name for op in primitive)for name in ['ADD','SCALE','MONOMIAL']}
    require(count['ADD']<=27*order**2 and count['SCALE']<=54*order**2+1 and count['MONOMIAL']<=54*order*(order-1),'Conservative full primitive bound')
    return {'order':order,'determinant':delta.serial(),'sectors':[ser_mat(q)for q in qs],'elementary_factor_count':len(elementaries),'reductions':[ser_ops(r)for r in reductions],'elementary_forward':[[s,i,j,c.serial()]for s,i,j,c in elementaries],'primitive_forward':ser_ops(primitive),'primitive_inverse':ser_ops(inverse_primitive),'counts':count,'polynomial_coefficients':[ser_mat(a)for a in expected],'inverse_coefficients':[ser_mat(a)for a in inverse]}

cycle=mat([[0,0,1],[1,0,0],[0,1,0]])
q0=mm(elementary(0,1,G(F(1),F(1))),elementary(2,0,-1))
q1=mm(cycle,mm(elementary(1,2,2),elementary(0,2,-1)))
q2=mat([[2,0,0],[0,F(1,2),0],[0,0,1]])
q3=mm(elementary(0,2,1),mm(elementary(2,1,-2),elementary(1,0,1)))
cases=[compile_sectors([q0,q1]),compile_sectors([q0,q1,q2,q3]),compile_sectors([apply_op(q,('SCALE',0,ii))for q in [q0,q1]])]
bad=[q0,apply_op(q1,('SCALE',0,lift(2)))]
require(all(minverse(q)[0]is not None for q in bad),'Unequal determinant control remains an algebraic unit')
try:compile_sectors(bad)
except ValueError as e:require(str(e)=='common_nonzero_determinant','Correct scope rejection')
else:raise ValueError('Admitted unimplemented determinant variation')

def native_recover_special_linear(ps,ms):
    order=len(ps);M=[[ms[s][t][r][c]for t in range(order)for c in range(3)]for s in range(order)for r in range(3)]
    i,j=next((i,j)for i,row in enumerate(M)for j,z in enumerate(row)if z)
    u=[-row[j]for row in M];v=[z/M[i][j]for z in M[i]]
    require(all(-u[r]*v[c]==M[r][c]for r in range(3*order)for c in range(3*order)),'Global native source-channel coherence')
    pp=mat([[0,0,0],[0,0,0],[0,0,1]]);nn=mat([[0,1,0],[0,0,0],[0,0,0]])
    qs=[];rs=[];before=[]
    for s,pj in enumerate(ps):
        require(mm(pj,pj)==pj and sum((pj[j][j]for j in range(3)),zero)==one,'Rank-one sector projector')
        us=u[3*s:3*s+3];vs=v[3*s:3*s+3]
        require(all(not sum((pj[r][c]*us[c]for c in range(3)),zero)for r in range(3))and all(not sum((vs[r]*pj[r][c]for r in range(3)),zero)for c in range(3))and not sum((x*y for x,y in zip(vs,us)),zero),'Native local flags')
        wcol=next(c for c in range(3)if any(pj[r][c]for r in range(3)));w=[pj[r][wcol]for r in range(3)]
        j=next(j for j,z in enumerate(vs)if z);z=[((one if r==j else zero)-pj[r][j])/vs[j]for r in range(3)]
        rmat=[[us[r],z[r],w[r]]for r in range(3)];d=determinant(rmat);require(bool(d),'Constructive native sector basis');before.append(d)
        rmat=[[row[0],row[1],row[2]/d]for row in rmat];qmat=minverse(rmat)[0]
        require(determinant(rmat)==one and determinant(qmat)==one,'Idle-column determinant normalization')
        require(mm(mm(rmat,pp),qmat)==pj,'Normalized native projector remains exact')
        rs.append(rmat);qs.append(qmat)
    require(all(ms[s][t]==mscale(mm(mm(rs[s],nn),qs[t]),-1)for s in range(order)for t in range(order)),'All cross-sector native channels survive determinant normalization')
    return qs,before
pp=mat([[0,0,0],[0,0,0],[0,0,1]]);nn=mat([[0,1,0],[0,0,0],[0,0,0]])
bad_inverse=[minverse(q)[0]for q in bad]
native_ps=[mm(mm(r,pp),q)for q,r in zip(bad,bad_inverse)]
native_ms=[[mscale(mm(mm(bad_inverse[s],nn),bad[t]),-1)for t in range(2)]for s in range(2)]
native_qs,pre_normalization_dets=native_recover_special_linear(native_ps,native_ms)
cases.append(compile_sectors(native_qs))

# The literal source is independently rebuilt from its defining16-address
# matrices; no modular word-search or candidate files enter this verification.
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);repo=parser.parse_args().repo
mp=repo/'research/moonshot-005-program/results/complex-nonordinary-row-seed/worker-b/check.py'
sp=importlib.util.spec_from_file_location('exact_source_matrices',mp);src=importlib.util.module_from_spec(sp);sys.modules[sp.name]=src;sp.loader.exec_module(src)
I16=src.eye(16);Xb=src.monomial([x^2 for x in range(16)],[0]*16)
Cb=src.M((I16.scale((1,1))+Xb.scale((1,-1))).a,1).norm()
P=src.monomial([(x>>1)|((x&1)<<3)for x in range(16)],[0]*16)
Df=src.monomial(list(range(16)),[2*((x&1)*((x>>2)&1)*((x>>3)&1))for x in range(16)])
A=Cb@Df@P;H=src.monomial(list(range(16)),[2*int(x==15)for x in range(16)])
Km=A.star()@H@A;Kp=A@H@A.star()
def formula(minus):
    perm=[];phase=[]
    for x in range(16):
        a,b,c,d=[(x>>j)&1 for j in range(4)]
        gate=a*b*d if minus else a*c*d
        perm.append(x^((4 if minus else 2)*gate))
        phase.append((gate*((1-2*c)if minus else(2*b-1)))%4)
    return src.monomial(perm,phase),list(zip(perm,phase))
fm,tm=formula(True);fp,tp=formula(False)
require(Km==fm and Kp==fp,'Exact non-diagonal control formulas and phases')
require(Km.power(2)==I16 and Kp.power(2)==I16,'Actual involutions')
require(A@Km==H@A and Kp@A==A@H,'Actual source intertwining')
require(Km.trace()==(14,0)and Kp.trace()==(14,0),'Actual plus/minus multiplicities')
sign_functions=[
 ('quartic',lambda a,b,c,d:a*b*c*d),
 ('b_xor_acd',lambda a,b,c,d:b^(a*c*d)),
 ('c_xor_abd',lambda a,b,c,d:c^(a*b*d)),
 ('a_xor_bcd',lambda a,b,c,d:a^(b*c*d)),
 ('d_xor_abc',lambda a,b,c,d:d^(a*b*c)),
 ('ab_xor_cd',lambda a,b,c,d:(a*b)^(c*d)),
 ('b_xor_c_xor_ad',lambda a,b,c,d:b^c^(a*d)),
 ('quadratic_path',lambda a,b,c,d:(a*b)^(b*c)^(c*d)^a^d),
]
sign_family=[]
for name,f in sign_functions:
    fs=[f(*[(x>>j)&1 for j in range(4)])for x in range(16)];hf=src.monomial(list(range(16)),[2*z for z in fs]);tables=[]
    for minus in [True,False]:
        pp=[];qq=[]
        for x in range(16):
            a,b,c,d=[(x>>j)&1 for j in range(4)]
            mu=f(b,0,d,a)if minus else f(d,a,0,c)
            nu=mu^(f(b,1,d,a)if minus else f(d,a,1,c))
            pp.append(x^((4 if minus else 2)*nu));qq.append((2*mu+nu*((1-2*c)if minus else(2*b-1)))%4)
        actual=A.star()@hf@A if minus else A@hf@A.star();expected=src.monomial(pp,qq)
        require(actual==expected and actual.power(2)==I16,'Literal arbitrary sign-table conjugation')
        tables.append(list(zip(pp,qq)))
    w=sum(fs);require(0<w<16,'Both source involution eigenvalues occur')
    counts={str(v):[(16**v+(16-2*w)**v)//2,(16**v-(16-2*w)**v)//2]for v in [1,2,3,7]}
    require(all(min(z)>0 and sum(z)==16**int(v)for v,z in counts.items()),'Every-width involution sector counts')
    sign_family.append({'name':name,'boolean_table':fs,'negative_multiplicity':w,'control_tables':tables,'sector_counts':counts})
channels={}
for name,k in [('Kminus',Km),('Kplus',Kp)]:
    projectors=[src.M((I16+k.scale((sign,0))).a,1).norm()for sign in [1,-1]]
    witnesses=[]
    for s in range(2):
        for t in range(2):
            channel=projectors[s]@A@projectors[t]
            nonzero=next(((r,c,z)for r,row in enumerate(channel.a)for c,z in enumerate(row)if z!=(0,0)),None)
            require(nonzero is not None,'Every actual source spectral channel is nonzero')
            witnesses.append({'output_sector':s,'input_sector':t,'entry':nonzero,'denominator_power':channel.k})
    channels[name]=witnesses

paths=['research/moonshot-005-program/results/complex-four-bit-cubic-source/author/PROOF.md','research/moonshot-005-program/results/fixed-monomial-compact-bridge/author/PROOF.md']
result={'status':'PASS_NONDIAGONAL_CYCLIC_ORDINARY_IMPLEMENTATION','baseline':'3057acc9311101cfedfcfacf7f68fb0866507871','scope':'Explicit common-sector-determinant cyclic implementation for fixed monomial controls; no independent421 endpoint or profitable caller. Unequal determinants of a specified Q are outside this recipe, but every admitted native cyclic conjugacy can be normalized to determinant one.','control_tables':{'Kminus':tm,'Kplus':tp},'general_sign_family_controls':sign_family,'all_source_spectral_channels':channels,'cases':cases,'native_conjugacy_normalization':{'original_sector_determinants':[determinant(q).serial()for q in bad],'constructed_basis_determinants_before':[d.serial()for d in pre_normalization_dets],'constructed_sector_determinants':[determinant(q).serial()for q in native_qs],'all_four_source_channels_preserved':True},'negative_controls':['unequal sector determinants of the specified Q rejected despite scalar invertibility'],'source_sha256':{p:hashlib.sha256((repo/p).read_bytes()).hexdigest()for p in paths},'arithmetic_helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'source_matrix_helper_sha256':hashlib.sha256(mp.read_bytes()).hexdigest()}
Path(__file__).with_name('NONDIAGONAL-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'case_counts':[x['counts']for x in cases],'all_source_channels':8},indent=2))
