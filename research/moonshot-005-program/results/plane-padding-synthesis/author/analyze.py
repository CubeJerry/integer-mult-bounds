#!/usr/bin/env python3
"""Exact64-subset screen for the common-P three-half source control."""
import argparse,hashlib,itertools,json
from fractions import Fraction as F
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'SCREEN.json');args=parser.parse_args()
source_metadata=json.loads((HERE/'SOURCE.json').read_text());pin=source_metadata['source_sha256']
if hashlib.sha256((HERE/'SOURCE-SCREEN.py').read_bytes()).hexdigest()!=pin:raise ValueError('exact predecessor source pin')
for name in('HALF-MANIFEST.json','HALF-PRICE.json'):
    if hashlib.sha256((HERE/name).read_bytes()).hexdigest()!=source_metadata[name+'_sha256']:raise ValueError('half source pin '+name)
halfprice=json.loads((HERE/'HALF-PRICE.json').read_text())
if halfprice['half_profile']!={'2':112,'3':112,'5':112,'6':112}:raise ValueError('authentic standalone half tariff')
p=s.symbols('p',nonzero=True);ds=s.symbols('d1:4');I=s.eye(4)
def E(d,src,c):
    M=s.eye(4);M[d,src]=c;return M
def simple(M):return M.applyfunc(s.cancel)
def iszero(M):return all(s.cancel(z)==0 for z in M)
def need(c,m):
    if not c:raise ValueError(m)
def enc(M):return [[str(s.factor(x))for x in row]for row in M.tolist()]
B=s.Matrix([[0,0,1,0],[1,0,0,1],[0,1,1,0],[0,0,0,1]])
post=E(0,2,-1);cleanup=E(2,3,-p);tail=cleanup*post
T2=E(2,0,-1);T3=E(3,1,-1)
H=[E(0,1,p),T2.inv()*E(1,2,1/p)*T2,T3.inv()*E(2,3,p)*T3]
head=simple(tail*H[2]*H[1]*H[0]*B);need(head==s.diag(p,1/p,1,1),'all arbitrary head baselines after cleanup')
transport=[tail*H[2]*H[1],tail*H[2]*T2.inv(),tail*T3.inv()]
active=[(0,1),(1,2),(2,3)];unused=[(2,3),(0,3),(0,1)]
element=[]
for W in transport:
    wi=W.inv();element.append([simple(W*s.diag(*[int(j==r)for j in range(4)])*wi)for r in range(4)])
accepted=[];census=[];same_at_plusminus1=0;commuting_at1=0
for bits in itertools.product((0,1),repeat=6):
    masks=[list(active[k])+[r for j,r in enumerate(unused[k])if bits[2*k+j]]for k in range(3)]
    P=[simple(sum((element[k][r]for r in masks[k]),s.zeros(4)))for k in range(3)]
    need(all(iszero(M*M-M)for M in P),'conjugated projector')
    parity=[iszero(M-M.subs(p,-p))for M in P]
    comm=[iszero(P[i]*P[j]-P[j]*P[i])for i in range(3)for j in range(i)]
    r={'idle_bits':list(bits),'idle_count':sum(bits),'stage_raw_roles':masks,'even_projectors':parity,'commuting_pairs':comm}
    parity1=[iszero(M.subs(p,1)-M.subs(p,-1))for M in P]
    comm1=[iszero((P[i]*P[j]-P[j]*P[i]).subs(p,1))for i in range(3)for j in range(i)]
    same_at_plusminus1+=all(parity1);commuting_at1+=all(comm1)
    if not all(parity1):
        k=next(k for k,good in enumerate(parity1)if not good);diff=P[k].subs(p,1)-P[k].subs(p,-1)
        a,b=next((a,b)for a in range(4)for b in range(4)if diff[a,b])
        r['parity_counterexample']={'stage':k+1,'row':a,'column':b,'p1_minus_pminus1':str(diff[a,b])}
    if all(parity)and all(comm):
        joint={}
        for pattern in itertools.product((0,1),repeat=3):
            J=I
            for t,M in zip(pattern,P):J=J*(M if t else I-M)
            J=simple(J);rank=J.subs(p,1).rank()
            if rank:joint[''.join(map(str,pattern))]={'rank':rank,'projector':enc(J)}
        r['projectors']=[enc(M)for M in P];r['joint_masks']=joint;accepted.append(r)
    census.append(r)
u,w=s.symbols('u w');closed=[]
expected=[s.Matrix([[1,0,0,p*(1-w)],[0,u,(u-1)/p,0],[0,0,1,0],[0,0,0,w]]),
          s.Matrix([[1,0,0,p*(1-w)],[0,1,0,0],[u-1,0,u,p*(u-1)],[0,0,0,w]]),
          s.Matrix([[u,0,u-1,p*(u-1)],[0,w,0,0],[0,p*(1-w),1,0],[0,w-1,0,1]])]
for k in range(3):
    M=simple(sum((element[k][r]for r in active[k]),s.zeros(4))+u*element[k][unused[k][0]]+w*element[k][unused[k][1]])
    need(iszero(M-expected[k]),'closed universal projector formula');closed.append(enc(M))
need(len(accepted)==1 and accepted[0]['idle_count']==6 and same_at_plusminus1==1,'unique full padding')
# With complete padding every stage body is scalar on all four roles.
full=simple(tail*(ds[2]*H[2])*(ds[1]*H[1])*(ds[0]*H[0])*B)
need(iszero(full-ds[0]*ds[1]*ds[2]*s.diag(p,1/p,1,1)),'all4 original full-padding target columns')
def power(r):
    den=10**40;n=r**199*den**200;lo=0;hi=r*den+1
    while hi-lo>1:
        mid=(hi+lo)//2
        if mid**200<=n:lo=mid
        else:hi=mid
    need(lo**200<=n<(lo+1)**200,'directed200th root');return F(lo,den),F(lo if lo**200==n else lo+1,den)
def moment(profile):
    lo=hi=F(0)
    for r,c in profile.items():
        a,b=power(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
    return [str(lo),str(hi)]
T={25:224,24:224};paid={1:112,2:336,3:336,5:336,6:336,8:672}
signed=T.copy()
for r,c in paid.items():signed[r]=signed.get(r,0)-c
gap=moment(signed);need(F(gap[0])>0,'conditional full-padding room')
extra=signed.copy();extra[1]-=112;need(F(moment(extra)[1])<0,'one additional query bank fails')
report={'status':'PASS_EXACT64_PADDING_SUBSETS','common_P_only':True,'cleanup_query_included_in_output_map':True,
        'head_endpoint':enc(head),'accepted':accepted,'all64':census,'closed_projectors_with_two_stage_idle_parameters':closed,
        'patterns_even_at_plusminus1':same_at_plusminus1,'patterns_commuting_at1':commuting_at1,
        'complete_full_padding_map':enc(full),'unique_target_masks':['111']*4,
        'conditional_full_invoice':{'T':T,'P':paid,'kappa':'1/200','exact_gap':gap,'extra_rank1_bank_gap':moment(extra)},
        'root_source_pin':pin,'half_source_pins':{n:source_metadata[n+'_sha256']for n in('HALF-MANIFEST.json','HALF-PRICE.json')},
        'sympy_version':s.__version__,'actual_Rs_caller_claimed':False,'new_kappa':False}
args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps({'accepted_count':len(accepted),'accepted':[{k:v for k,v in r.items()if k not in('projectors','joint_masks')}for r in accepted]},indent=2))
