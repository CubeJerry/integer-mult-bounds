#!/usr/bin/env python3
"""Independent operator-matrix and fixed-source tariff review.
No author scientific module imported. @CubeJerry with OpenAI assistance.
"""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
BASE=Path(__file__).resolve().parents[2]
FREEZE='ae7a8a4111f33907d04dd5f9e9c1b82e69e361497d811b008e69f62133c87122'

def need(ok,msg):
    if not ok:raise ValueError(msg)
def c(v,q=0,d=0):return{(q%4,d):F(v)}if v else{}
def padd(a,b):
    out=dict(a)
    for key,v in b.items():
        z=out.get(key,F(0))+v
        if z:out[key]=z
        else:out.pop(key,None)
    return out

def pmul(a,b):
    out={}
    for (q,d),v in a.items():
        for (r,e),w in b.items():out=padd(out,{((q+r)%4,d+e):v*w})
    return out

def eye():return[[c(int(i==j))for j in range(4)]for i in range(4)]
def mm(A,B):
    C=[[{}for j in range(4)]for i in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):C[i][j]=padd(C[i][j],pmul(A[i][k],B[k][j]))
    return C

def elementary(event):
    E=eye();op=event[0]
    if op=='SCALE':_,i,s=event;need(F(s)!=0,'invertible ordinary scale');E[i][i]=c(F(s))
    elif op=='QUERY':
        _,i,j,q=event;need(i!=j and q==1,'actual nonself positive query');E[i][j]=c(1,q)
    elif op=='IDLE':_,i=event;E[i][i]=c(1,d=1)
    elif op=='COUPLED':
        _,x,y=event;need(x!=y,'actual distinct coupled inputs');E[x][x]=c(1,d=1);E[x][y]=c(-1,q=1,d=1);E[y][x]=c(F(1,2),q=-1,d=1);E[y][y]=c(F(1,2),d=1)
    else:raise ValueError('unknown opcode')
    return E

def local_identity(events):
    want=eye()
    for j in range(4):want[j][j]=c(1,d=1)
    want[1][0]=c(1,q=-1,d=1);want[2][3]=c(-1,q=1,d=1)
    def product(skip=None):
        M=eye()
        for t,e in enumerate(events):
            if t!=skip:M=mm(elementary(e),M)
        return M
    need(product()==want,'full four-arbitrary-input HOST2 matrix')
    controls=[]
    for t,e in enumerate(events):need(product(t)!=want,'deleted actual conversion instruction');controls.append({'event':t,'opcode':e[0],'rejected':True})
    before=eye();before[1][1]=c(1,q=2);negative=eye();negative[0][1]=c(1,q=-1)
    need(mm(before,mm(negative,before))==elementary(['QUERY',0,1,1]),'positive query uses one negative query and two ordinary Q^2 translations')
    counts=Counter(e[0]for e in events);need(counts=={'SCALE':4,'QUERY':2,'COUPLED':1,'IDLE':2},'all local paid operations counted')
    return {'status':'PASS_EXACT_OPERATOR_MATRIX','counts':dict(counts),'arbitrary_inputs':4,'paid_addition_per_coupled_port':{'1':2,'8':2},'event_deletion_controls':controls,'positive_query_translation_identity':True,'scope':'Caller-level conversion. Not a native endpoint wrapper; all whole-body idles remain paid.'}


def invoice(full,caller):
    need(full['word_sha256']=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native word identity')
    A=caller['types']['A']['ports'];B=caller['types']['B']['ports'];need(len(A)==96 and len(B)==8 and not set(A)&set(B)and set(A+B)==set(range(104)),'actual source96A8B partition')
    Js=[e for e in caller['events']if e[0]=='J'];need(len(Js)==18 and all(F(e[3][2])==-1 and F(e[3][3])==F(1,2)for e in Js),'all actual coupled native coefficients')
    need(full['native']['public']==1480 and sum(full['native']['helpers'].values())==1080 and 4*len(A)+2*len(B)==400,'all actual main/helper inputs counted')
    den=10**34;cache={}
    def power(n):
        if n not in cache:
            goal=n**199*den**200;lo=0;hi=n*den+1
            while hi-lo>1:
                x=(lo+hi)//2
                if x**200<=goal:lo=x
                else:hi=x
            need(lo**200<=goal<hi**200,'exact200th-power bounds');cache[n]=F(lo,den),F(hi,den)
        return cache[n]
    def combine(*pairs):
        z={}
        for s,p in pairs:
            for n,v in p.items():z[int(n)]=z.get(int(n),F(0))+s*F(v)
        return {n:v for n,v in z.items()if v}
    def moment(p):
        lo=hi=F(0)
        for n,v in p.items():
            a,b=power(n);lo+=v*(a if v>=0 else b);hi+=v*(b if v>=0 else a)
        return lo,hi
    def wrapper(a):
        z=Counter({1+16*a:2})
        for j in range(1,a+1):z[1+8*j]+=4
        z[1]-=4
        for j in range(1,a):z[8*j]-=4
        return dict(z)
    net=combine((1,full['native']['paid']),(-1,full['native']['helpers']));conversion={1:16,8:16};cost=combine((1,net),(1,conversion));freeq=combine((1,net),(1,{8:16}))
    table=[]
    for a in[3,4,9]:
        paid=moment(combine((104,wrapper(a)),(-2*a,cost)));optim=moment(combine((104,wrapper(a)),(-2*a,freeq)))
        need(paid[1]<0 and optim[1]<0,'displayed retained h9 source screens')
        table.append({'arms':a,'stages':2*a,'complete_paid_gap':paid,'extra_queries_granted_free_gap':optim})
    H5=moment(combine((5,wrapper(6)),(-6,wrapper(5))));H6=moment(combine((6,wrapper(7)),(-7,wrapper(6))))
    need(H5[0]>0 and H6[1]<0,'unique global maximum of wrapper allowance per native at a6')
    max_profile=combine((F(104,12),wrapper(6)));ceiling=moment(max_profile)
    paid_deficit=moment(combine((1,max_profile),(-1,cost)));free_deficit=moment(combine((1,max_profile),(-1,freeq)))
    need(paid_deficit[1]<0 and free_deficit[1]<0,'all positive arm counts fail for fixed retained source')
    illicit=moment(combine((1,max_profile),(-1,net),(-1,{1:16})))
    need(illicit[0]>0,'omitting two required body idles creates a false-positive invoice')
    return {'native_public_fields':1480,'native_main_fields':400,'native_independent_helpers':1080,'actual_coupled_events_authenticated':18,'native_net':moment(net),'conversion_cost_per_native':moment(conversion),'displayed_cases':table,'all_arms_extension':{'wrapper_per_native_maximum_arms':6,'stages':12,'exact_H5':H5,'exact_H6':H6,'wrapper_allowance_ceiling':ceiling,'paid_conversion_maximum_gap_per_native':paid_deficit,'free_extra_queries_maximum_gap_per_native':free_deficit,'illicit_free_body_idles_false_positive_margin':illicit,'proof':'W_a has strictly decreasing first differences, hence H_a=aW_(a+1)-(a+1)W_a strictly decreases; exact signs H5>0,H6<0 locate the global ratio maximum. The maximum remains below both fixed source prices.'},'scope':'Fixed retained h9 native with this paid caller conversion, every positive integer arm count. Other roots, conversions, natives or independently justified changes remain open.'}


def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v)for v in x]
    return x

def main():
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=BASE/'worker-a/short-tensor-source-screen');p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));args=p.parse_args()
    freeze=args.author/'H9-FREEZE.json';need(hashlib.sha256(freeze.read_bytes()).hexdigest()==FREEZE,'author h9 freeze identity');pins=json.loads(freeze.read_bytes())
    for file,pin in pins.items():need(hashlib.sha256((args.author/file).read_bytes()).hexdigest()==pin,'frozen source '+file)
    cv=json.loads((args.author/'CONVERSION.json').read_bytes());full=json.loads((args.author/'source/retained-FULL-RESULT.json').read_bytes());caller=json.loads((args.author/'source/retained-caller.json').read_bytes())
    result={'status':'PASS_INDEPENDENT_H9_CONVERSION_AND_ALL_ARMS_SCREEN','source_pins':pins,'local':local_identity(cv['events']),'invoice':invoice(full,caller),'new_kappa':None}
    args.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n');print('PASS: exact four-input conversion,9 mutants, full source invoice and all-positive-arm exclusion')
if __name__=='__main__':main()
