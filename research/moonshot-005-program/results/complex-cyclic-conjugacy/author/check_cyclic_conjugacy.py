#!/usr/bin/env python3
"""Construct and verify cyclic native conjugacies from exact scalar data."""
from pathlib import Path
import hashlib, json

helper=Path(__file__).with_name('check_cyclic_quarter.py')
source=helper.read_text()
require_marker='sectors=[eye(),'
if source.count(require_marker)!=1:raise RuntimeError('Unexpected arithmetic-helper boundary')
exec(compile(source.split(require_marker)[0],str(helper),'exec'))

def rank(a):
    a=[list(r)for r in a];row=0
    for c in range(len(a[0])):
        pivot=next((r for r in range(row,len(a))if a[r][c]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row];iv=a[row][c].inv();a[row]=[z*iv for z in a[row]]
        for r in range(len(a)):
            if r==row:continue
            z=a[r][c]
            if z:a[r]=[x-z*y for x,y in zip(a[r],a[row])]
        row+=1
        if row==len(a):break
    return row
def mv(a,v):return [sum((z*w for z,w in zip(row,v)),zero)for row in a]
def vm(v,a):return [sum((v[r]*a[r][c]for r in range(3)),zero)for c in range(3)]
def dot(u,v):return sum((x*y for x,y in zip(u,v)),zero)
def assembled(ms):return [[ms[s][t][r][c]for t in range(4)for c in range(3)]for s in range(4)for r in range(3)]
Pzero=mat([[0,0,0],[0,0,0],[0,0,1]])
E01=mat([[0,1,0],[0,0,0],[0,0,0]])

def solve(ps,ms):
    for s,p in enumerate(ps):
        if mm(p,p)!=p or rank(p)!=1:raise ValueError('sector_projector')
    if any(not any(z for row in b for z in row)for rr in ms for b in rr):raise ValueError('zero_channel_block')
    M=assembled(ms)
    if rank(M)!=1:raise ValueError('coherence_rank')
    i,j=next((i,j)for i,row in enumerate(M)for j,z in enumerate(row)if z)
    u=[-row[j]for row in M];v=[z/M[i][j]for z in M[i]]
    require(all(-u[r]*v[c]==M[r][c]for r in range(12)for c in range(12)),'Global rank-one factor')
    qs=[];rs=[]
    for s,p in enumerate(ps):
        us=u[3*s:3*s+3];vs=v[3*s:3*s+3]
        if any(mv(p,us))or any(vm(vs,p))or dot(vs,us):raise ValueError('local_flag')
        col=next(c for c in range(3)if any(p[r][c]for r in range(3)))
        w=[p[r][col]for r in range(3)]
        j=next(j for j,z in enumerate(vs)if z)
        z=[((one if r==j else zero)-p[r][j])/vs[j]for r in range(3)]
        rmat=[[us[r],z[r],w[r]]for r in range(3)]
        qmat,ops=minverse(rmat)
        require(qmat is not None,'Constructed sector unit')
        require(mm(mm(rmat,Pzero),qmat)==p,'Recovered sector projector')
        rs.append(rmat);qs.append(qmat)
    for s in range(4):
        for t in range(4):require(ms[s][t]==mscale(mm(mm(rs[s],E01),qs[t]),-1),'Recovered cross-sector conjugacy')
    return qs,rs

# Distinct source units include actual complex coefficients and a genuine
# mixing of the idle sector with the active two-dimensional complement.
original_q=[eye(),mat([[1,G(F(1),F(1)),0],[0,1,0],[0,0,1]]),mat([[0,1,0],[1,0,0],[0,0,1]]),mat([[1,1,1],[0,1,1],[0,0,1]])]
original_r=[minverse(q)[0]for q in original_q]
ps=[mm(mm(original_r[s],Pzero),original_q[s])for s in range(4)]
ms=[[mscale(mm(mm(original_r[s],E01),original_q[t]),-1)for t in range(4)]for s in range(4)]
recovered_q,recovered_r=solve(ps,ms)
qpoly=interpolate(recovered_q);rpoly=interpolate(recovered_r)
require(mul_poly(qpoly,rpoly)==[eye(),zmat(),zmat(),zmat()]and mul_poly(rpoly,qpoly)==[eye(),zmat(),zmat(),zmat()],'Recovered all-width ordinary inverse')

# Exact conversion between a bi-cyclic word coefficient table and its sixteen
# source-channel matrices; no physical projection is implemented for free.
N=[[mscale(sum_m([mscale(ms[s][t],ipow(-s*j-t*k))for s in range(4)for t in range(4)]),F(1,16))for k in range(4)]for j in range(4)]
require(all(sum_m([mscale(N[j][k],ipow(s*j+t*k))for j in range(4)for k in range(4)])==ms[s][t]for s in range(4)for t in range(4)),'Double Fourier source-channel coefficients')

rejected=[]
def rejects(p,m,expected):
    try:solve(p,m)
    except ValueError as e:
        require(str(e)==expected,f'Unexpected rejection: {e}');rejected.append(expected);return
    raise ValueError('Invalid conjugacy admitted')
badms=[[mscale(E01,-F(3,2)if s==t==3 else-1)for t in range(4)]for s in range(4)]
require(all(rank(b)==1 for rr in badms for b in rr)and rank(assembled(badms))==2,'Incoherent blocks each rank1 but jointly rank2')
rejects([Pzero for _ in range(4)],badms,'coherence_rank')
badps=[row for row in ps];badps[0]=mat([[1,0,0],[0,0,0],[0,0,0]])
rejects(badps,ms,'local_flag')
badps2=[row for row in ps];badps2[3]=zmat()
rejects(badps2,ms,'sector_projector')
badms2=[[b for b in row]for row in ms];badms2[3][3]=zmat()
rejects(ps,badms2,'zero_channel_block')

# A cyclic ordinary idempotent may have physical rank D for EVERY positive
# width while its sector ranks are(2,0,2,0), so the sector test is indispensable.
allwidth_rank_control=[]
for width in range(1,8):
    counts=[sum(comb(width,k)for k in range(width+1)if k%4==s)*8**width for s in range(4)]
    require(sum(r*c for r,c in zip([2,0,2,0],counts))==16**width,'All-width physical rank does not fix cyclic sector rank')
    allwidth_rank_control.append({'width':width,'physical_rank':16**width,'sector_ranks':[2,0,2,0]})

# Actual32 nonzero source entries: P cycles the coordinates and C_b either
# keeps or flips the second output bit. Each has a nonzero exact dyadic phase.
phase_functions=[lambda a,b,c,d:b,lambda a,b,c,d:c,lambda a,b,c,d:b^(c*d),lambda a,b,c,d:c^(a*b)]
witnesses=[]
for fn in phase_functions:
    pairs={}
    for x in range(16):
        a,b,c,d=[(x>>j)&1 for j in range(4)]
        for epsilon in range(2):
            ybits=(b,c^epsilon,d,a);y=sum(z<<j for j,z in enumerate(ybits))
            pair=(fn(*ybits),fn(a,b,c,d));pairs.setdefault(pair,{'input':x,'output':y,'epsilon':epsilon})
    require(set(pairs)=={(0,0),(0,1),(1,0),(1,1)},'Actual source phase-bit channel support')
    tensor_witness=[]
    for s in range(4):
        for t in range(4):
            cols=[pairs[(int(j<s),int(j<t))]for j in range(3)]
            outcount=sum(fn(*[(q['output']>>j)&1 for j in range(4)])for q in cols)
            incount=sum(fn(*[(q['input']>>j)&1 for j in range(4)])for q in cols)
            require(outcount==s and incount==t,'All sixteen source channels at width3')
            tensor_witness.append({'output_sector':s,'input_sector':t,'columns':cols})
    witnesses.append({'one_column':[{'phase_pair':list(k),**v}for k,v in sorted(pairs.items())],'width3':tensor_witness})

result={
 'status':'PASS_CONSTRUCTIVE_CYCLIC_NATIVE_CONJUGACY',
 'baseline':'3057acc9311101cfedfcfacf7f68fb0866507871',
 'scope':'Necessary and sufficient criterion for the explicit cyclic P / bi-cyclic a-channel T interface. Ordinary C and independent421 endpoint remain separate obligations.',
 'P_sector_matrices':[ser_mat(p)for p in ps],
 'M_channel_matrices':[[ser_mat(b)for b in row]for row in ms],
 'joint_scalar_rank':rank(assembled(ms)),
 'recovered_sector_units':[ser_mat(q)for q in recovered_q],
 'recovered_sector_inverses':[ser_mat(r)for r in recovered_r],
 'recovered_polynomial_units':[ser_mat(q)for q in qpoly],
 'recovered_polynomial_inverses':[ser_mat(r)for r in rpoly],
 'source_channel_witnesses':witnesses,
 'negative_controls':rejected,
 'allwidth_physical_rank_counterexample':allwidth_rank_control,
 'arithmetic_helper_sha256':hashlib.sha256(helper.read_bytes()).hexdigest(),
 'new_kappa':False,
}
out=Path(__file__).with_name('CONJUGACY-RESULT.json');out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'joint_scalar_rank':result['joint_scalar_rank'],'exact_conjugacy_equations':16,'source_controls':4,'channels_per_control':16,'negative_controls':rejected,'ordinary_C_remains_open':True,'new_kappa':False},indent=2))
