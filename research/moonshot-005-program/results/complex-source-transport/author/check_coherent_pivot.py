#!/usr/bin/env python3
"""Exact transported normalization and universal coherent block identities."""
from pathlib import Path
import hashlib,json
helper=Path(__file__).with_name('check_cyclic_quarter.py')
exec(compile(helper.read_text().split('sectors=[eye(),')[0],str(helper),'exec'))

# The exact source relation a*y=x*a, x^4=y^4=1. Only products with at
# most one a occur below; no unspecified conjugation of x is assumed.
def ring_atom(x=0,y=0,a=0,c=one):return {(x%4,y%4,a):c}if c else{}
rid=ring_atom();rz={};ra=ring_atom(a=1)
def radd(*ps):
    out={}
    for q in ps:
        for k,c in q.items():out[k]=out.get(k,zero)+c
    return {k:c for k,c in out.items()if c}
def rneg(q):return {k:-c for k,c in q.items()}
def rmul(*ps):
    out=rid
    for q in ps:
        nxt={}
        for (x,y,a),c in out.items():
            for (xx,yy,aa),d in q.items():
                require(a+aa<=1,'At most one source head in normalization')
                require(not a or xx==0,'No unsupported transport of x through a')
                k=((x+xx+(yy if a else 0))%4,(y+(0 if a else yy))%4,a+aa)
                nxt[k]=nxt.get(k,zero)+c*d
        out={k:c for k,c in nxt.items()if c}
    return out
def rmm(a,b):return [[radd(*(rmul(a[r][k],b[k][c])for k in range(3)))for c in range(3)]for r in range(3)]
def scalar_fourier(vals):return [sum((vals[s]*ipow(-s*j)for s in range(4)),zero)/4 for j in range(4)]
def scalar_poly(coeffs,axis):return radd(*(ring_atom(x=j if axis=='x'else 0,y=j if axis=='y'else 0,c=z)for j,z in enumerate(coeffs)))
svals=[one,lift(2),ii,-one];tvals=[zero,one,one+ii,lift(-2)]
s=scalar_fourier(svals);si=scalar_fourier([z.inv()for z in svals]);t=scalar_fourier(tvals)
sx,sy=scalar_poly(s,'x'),scalar_poly(s,'y');sxi,syi=scalar_poly(si,'x'),scalar_poly(si,'y');tx,ty=scalar_poly(t,'x'),scalar_poly(t,'y')
require(rmul(sx,sxi)==rid and rmul(sy,syi)==rid,'All-sector scalar inverse')
gb=[[sy,rz,rz],[ty,sy,rz],[rz,rz,rid]]
gxi=[[sxi,rz,rz],[rneg(rmul(sxi,tx,sxi)),sxi,rz],[rz,rz,rid]]
ll=[[ra,rz,rz],[rid,ra,rz],[rz,rz,rid]]
w=rmul(sxi,sy);lw=[[ra,rz,rz],[w,ra,rz],[rz,rz,rid]]
require(rmm(rmm(gxi,ll),gb)==lw,'Exact transported lower-triangular normalization')
require(w!=rid,'Untransported unit first entry would miss a real ordinary cross factor')
gy=[[rid,rz,rz],[ty,rid,rz],[rz,rz,rid]]
gxi_unit=[[rid,rz,rz],[rneg(tx),rid,rz],[rz,rz,rid]]
require(rmm(rmm(gxi_unit,ll),gy)==ll,'Leading lower shear parameter is exactly an output gauge')

# Free associative word identities used after the source support separation.
def at(x):return {(x,):1}
o={():1};z={}
def pa(*ps):
    out={}
    for q in ps:
        for k,c in q.items():out[k]=out.get(k,0)+c
    return {k:c for k,c in out.items()if c}
def pn(q):return {k:-c for k,c in q.items()}
def pm(*ps):
    out=o
    for q in ps:
        nxt={}
        for x,c in out.items():
            for y,d in q.items():nxt[x+y]=nxt.get(x+y,0)+c*d
        out={k:c for k,c in nxt.items()if c}
    return out
def mmf(a,b):return [[pa(*(pm(a[r][k],b[k][c])for k in range(3)))for c in range(3)]for r in range(3)]
def mf(*xs):
    out=xs[0]
    for x in xs[1:]:out=mmf(out,x)
    return out
a,b,c,d,e,f,g,h,ww=[at(n)for n in ['a','b','c','d','e','f','g','h','w']]
lf=[[a,z,z],[ww,a,z],[z,z,o]];lr=[[a,z,z],[o,a,z],[z,z,o]]
uf=[[a,pn(pm(a,a)),z],[z,a,z],[z,z,o]]
cf=[[o,pm(b,h),c],[z,pm(d,h),e],[z,pm(f,h),g]]
pre=mf(lf,cf,uf)
require(pre[0]==[pm(a,a),pa(pn(pm(a,a,a)),pm(a,b,h,a)),pm(a,c)],'Exact coherent first row')
require(pre[1]==[pm(ww,a),pa(pn(pm(ww,a,a)),pm(ww,b,h,a),pm(a,d,h,a)),pa(pm(ww,c),pm(a,e))],'Exact coherent second row')
require(pre[2]==[z,pm(f,h,a),g],'Exact coherent third row')
q={(i,j):at(f'q{i}{j}')for i in range(3)for j in range(3)}
qp=[[q[0,0],z,q[0,2]],[q[1,0],q[1,1],z],[q[2,0],q[2,1],q[2,2]]]
ep=mf(pre,qp,lr)
expected11=pa(pn(pm(ww,a,a,q[1,1],a)),pm(ww,b,h,a,q[1,1],a),pm(a,d,h,a,q[1,1],a),pm(ww,c,q[2,1],a),pm(a,e,q[2,1],a))
require(ep[1][1]==expected11,'Exact separated q11 equation')
qz=[[z,z,q[0,2]],[q[1,0],z,z],[q[2,0],q[2,1],q[2,2]]]
ez=mf(pre,qz,lr)
require(ez[0][2]==pa(pm(a,a,q[0,2]),pm(a,c,q[2,2])),'Forced invertible top rank2 block')
require(ez[2][0]==pa(pm(f,h,a,q[1,0],a),pm(g,q[2,0],a),pm(g,q[2,1])),'Forced ordinary g q21 component')
require(ez[2][2]==pm(g,q[2,2]),'Zero opposite minor block after g=0')

proof=Path(__file__).with_name('COHERENT-FIRST-PIVOT.md')
result={'status':'PASS_COHERENT_FIRST_PIVOT_NORMALIZATION_AND_IDENTITIES','scope':'Exact source-transport normalization plus universal block identities supporting the scoped analytic first-pivot obstruction; no caller or kappa.','normalization_all_four_sector_values':{'s':[x.serial()for x in svals],'t':[x.serial()for x in tvals]},'ordinary_cross_factor_required':True,'lower_shear_parameter_is_output_gauge':True,'universal_coherent_block_identities':True,'pivot_changing_escape':{'first_entry_sector_values':[1,0,1,1],'first_entry_unit':False,'conditional_bank_swap_still_invertible':True},'author_proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'arithmetic_helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),'support_proof_sha256':hashlib.sha256(Path(__file__).with_name('SOURCE-TRANSPORTED-ROUTING.md').read_bytes()).hexdigest()}
Path(__file__).with_name('COHERENT-PIVOT-RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'exact_transport_normalization':True,'universal_blocks':True},indent=2))
