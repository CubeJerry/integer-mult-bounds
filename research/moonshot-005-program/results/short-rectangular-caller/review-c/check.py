#!/usr/bin/env python3
"""Independent exact group-algebra replay of the short rectangular caller.

No author builder, replay or geometry implementation is imported.
@CubeJerry with OpenAI assistance. Apache-2.0.
"""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations

BASE=Path(__file__).resolve().parents[2]
CALLER_PIN='094cb202e20f9e56cda9931f0c19801f9f9689f220d4aa3f829c262781b04111'
NATIVE_PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'

def need(ok,msg):
    if not ok:raise ValueError(msg)

def load(p):return json.loads(gzip.decompress(p.read_bytes())if p.suffix=='.gz'else p.read_bytes())
def plusz(a,b):return(a[0]+b[0],a[1]+b[1])
def mulz(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
ZERO=(F(0),F(0));ONE=(F(1),F(0))

def add(a,b,c=ONE,qshift=0,stages=()):
    out=dict(a)
    for (j,q,exp),value in b.items():
        e=list(exp)
        for s in stages:e[s-1]+=1
        key=(j,(q+qshift)%4,tuple(e));v=plusz(out.get(key,ZERO),mulz(c,value))
        if v!=ZERO:out[key]=v
        else:out.pop(key,None)
    return out

def scaled(row,c=ONE,qshift=0,stages=()):return add({},row,c,qshift,stages)

def replay(w,mutation=None):
    n=w['roles'];st=w['stages'];zero=(0,)*st
    rows=[{(i,0,zero):ONE}for i in range(n)];counts=Counter();queries=[];hosts=[];idles=[];peak=1;maxdegree=0
    for t,event in enumerate(w['events']):
        if t==mutation:continue
        op=event[0];counts[op]+=1
        if op=='ADD':
            _,d,s,c=event;need(d!=s and 0<=d<n and 0<=s<n,'actual nonself ordinary ADD');rows[d]=add(rows[d],rows[s],(F(c),F(0)))
        elif op=='SCALE':
            _,d,c=event;need(F(c)!=0,'invertible ordinary scalar');rows[d]=scaled(rows[d],(F(c),F(0)))
        elif op=='SWAP':
            _,a,b=event;need(a!=b and 0<=a<n and 0<=b<n,'actual nonself swap');rows[a],rows[b]=rows[b],rows[a]
        elif op=='LAMBDA':
            _,d,s=event;need(s in(-1,1),'lambda sign');rows[d]=add(scaled(rows[d],(F(1,2),F(s,2))),rows[d],(F(1,2),-F(s,2)),qshift=2)
        elif op=='QUERY':
            _,d,s,e=event;need(d!=s and 0<=d<n and 0<=s<n and e==-1,'literal distinct-field Q inverse shear');rows[d]=add(rows[d],rows[s],qshift=e);queries.append(t)
        elif op=='IDLE_ONE':
            _,d,mask=event;need(mask and len(mask)==len(set(mask))and all(1<=j<=st for j in mask),'whole idle has distinct real stage axes');rows[d]=scaled(rows[d],stages=mask);idles.append((d,tuple(mask)))
        elif op=='HOST2':
            _,j,x,y,u,v=event;need(len({x,y,u,v})==4 and all(0<=z<n for z in[x,y,u,v]),'four distinct actual native mains')
            need(1<=j<=st,'actual stage index');a,b,c,d=[rows[z]for z in[x,y,u,v]]
            rows[x]=scaled(a,stages=[j]);rows[y]=scaled(add(b,a,qshift=-1),stages=[j]);rows[u]=scaled(add(c,d,(-F(1),F(0)),qshift=1),stages=[j]);rows[v]=scaled(d,stages=[j]);hosts.append((j,x,y,u,v))
        else:raise ValueError('undeclared/free/empty operation '+op)
        peak=max(peak,max(map(len,rows)));maxdegree=max(maxdegree,max((max(key[2],default=0)for row in rows for key in row),default=0))
    expected=[]
    need(len(w['endpoint'])==n and sorted(ep['role']for ep in w['endpoint'])==list(range(n)),'complete arbitrary-input target set')
    for ep in sorted(w['endpoint'],key=lambda e:e['role']):
        mask=ep['stages'];need(ep['head_exponent']==-1 and len(mask)==len(set(mask)),'whole endpoint orientation/mask');ex=tuple(int(j in mask)for j in range(1,st+1));expected.append({(ep['role'],3,ex):ONE})
    bad=[i for i in range(n)if rows[i]!=expected[i]]
    if mutation is not None:return bad
    need(not bad,'exact identity in Q(i)[Q,D]/(Q^4-1)')
    need(len(queries)==4 and len(hosts)==st==2*w['arms'] and [h[0]for h in hosts]==list(range(1,st+1)),'four literal nonself queries and all distinct HOST2 stages')
    need(n==4*w['arms']+2 and w['arms']>=1 and w['native_dimension']==18 and w['body_dimension']==17,'reviewed exact short caller dimensions')
    need(dict(counts)==w['counts'],'literal complete event counts')
    target=Counter(1+17*len(ep['stages'])for ep in w['endpoint']);paid=Counter({1:len(queries)})
    for _,mask in idles:paid[17*len(mask)]+=1
    need(dict(target)=={**{1+17*j:4 for j in range(1,w['arms']+1)},1+17*st:2}and dict(paid)=={1:4,**{17*j:4 for j in range(1,w['arms'])}},'complete wrapper target and paid profiles')
    for k,v in [('T',target),('P',paid)]:need({int(n):c for n,c in w['wrapper_invoice_per_port'][k].items()}==dict(v),'advertised wrapper agrees with literal operations')
    controls=[]
    for name in ['ADD','HOST2','IDLE_ONE','LAMBDA','QUERY']:
        t=next(t for t,e in enumerate(w['events'])if e[0]==name);bad=replay(w,t);need(bad,'deleted '+name+' detected');controls.append({'removed_opcode':name,'event':t,'incorrect_outputs':bad})
    return {'status':'PASS_EXACT_GROUP_ALGEBRA','method':'Sparse direct Q(i)[Q,D1,...,D8]/(Q^4-1), no evaluation of D and no spectral sampling of Q','all_arbitrary_inputs':n,'events':len(w['events']),'counts':dict(counts),'queries':queries,'hosts':hosts,'idle_jobs':idles,'peak_formal_terms_per_row':peak,'maximum_intermediate_stage_exponent':maxdegree,'target_per_port':dict(target),'paid_per_port':dict(paid),'negative_controls':controls}


def binary_rank(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in piv:x^=piv[j]
            else:piv[j]=x;break
    return len(piv)

def basis_low(rows):
    piv={}
    for x in rows:
        while x:
            j=(x&-x).bit_length()-1
            if j in piv:x^=piv[j]
            else:piv[j]=x;break
    return list(piv.values())

def parity(x,y):return (x&y).bit_count()%2

def fresh_orthonormal(q,h):
    chosen=[q];W=basis_low([(1<<j)^(q if parity(1<<j,q)else 0)for j in range(h-1,-1,-1)])
    while W:
        char=(1<<h)-1
        for z in chosen:char^=z
        odd=[v for v in W if v.bit_count()%2];even=[v for v in W if not v.bit_count()%2]
        cand=odd+[a^b for a in odd for b in even]
        cand=[v for v in cand if len(W)==1 or v!=char]
        need(cand,'nonalternating orthogonal completion exists')
        z=max(cand);chosen.append(z);W=basis_low([v^(z if parity(v,z)else 0)for v in W])
    need(len(chosen)==h and all(parity(x,y)==int(i==j)for i,x in enumerate(chosen)for j,y in enumerate(chosen)),'fresh independent orthonormal head basis')
    return chosen

def phase_polynomial(vectors,h):
    linear=[sum(v>>i&1 for v in vectors)%4 for i in range(h)]
    quadratic={(i,j):(-2*sum((v>>i&1)*(v>>j&1)for v in vectors))%4 for i in range(h)for j in range(i)}
    return linear,quadratic

def geometry(native,w,cert):
    source=[native['frames'][native['initial'][i]][0]for i in native['live']]
    need(len(source)==len(set(source))==104 and binary_rank(source)==9 and all(q.bit_count()%2 for q in source),'actual104 distinct odd source labels')
    qs=source+[q<<9 for q in source];need(len(set(qs))==208 and binary_rank(qs)==18,'legal208 two-tag labels span18')
    need(all(parity(a,b<<9)==0 for a in source for b in source),'orthogonal tag factors')
    entries=cert['port_bases'];need([z['label']for z in entries]==qs,'exact prospective geometry port order')
    h=18;b=17;st=w['stages'];N=h+b*st;axes=[1<<j for j in range(N)];boundaries=0;fresh=[];changed=0
    for entry in entries:
        q=entry['label'];B=entry['basis'];need(len(B)==18 and B[0]==q and all(0<v<1<<h for v in B),'actual head basis starts with port')
        need(all(parity(x,y)==int(i==j)for i,x in enumerate(B)for j,y in enumerate(B)),'actual recorded orthonormal basis')
        independent=fresh_orthonormal(q,h);changed+=independent!=B;fresh.append({'label':q,'basis':independent})
        lin,quad=phase_polynomial(B,h);need(all(x==0 for x in quad.values()),'all quadratic phase coefficients cancel mod4')
        trans=sum((((v-1)%4)//2)<<i for i,v in enumerate(lin));need(all((v-1)%2==0 for v in lin)and trans==entry['phase_translation'],'exact ordinary translation correction')
        for j in range(1,st+1):
            common=B[1:]+axes[h:h+(j-1)*b];E=axes[h+(j-1)*b:h+j*b];head=[q]+E
            need(len(E)==17 and len(set(E))==17 and all(v.bit_count()==1 for v in E),'fresh disjoint17-axis block')
            need(all(parity(x,y)==0 for x in common for y in head),'orthogonal common/native embedding')
            need(binary_rank(common+head)==h+j*b,'absolute common plus native rank')
            charts=[common+[q],common,common+[q]+E,common+E]
            need([binary_rank(z)for z in charts]==[17*j+1,17*j,17*j+18,17*j+17],'all four actual boundary dimensions')
            counters=[Counter(z)for z in charts]
            def diff(i,k):
                ds=dict(counters[i])
                for v,c in counters[k].items():ds[v]=ds.get(v,0)-c
                return {v:c for v,c in ds.items()if c}
            body={v:1 for v in E}
            need(diff(2,0)==body and diff(3,1)==body,'two complete diagonal jobs D_j')
            need(diff(3,0)=={**body,q:-1}and diff(2,1)=={**body,q:1},'absolute forward and reverse Q signs')
            boundaries+=4
    need(changed>0,'fresh completion is independent of stored bases')
    target=Counter();idle=Counter()
    for ep in w['endpoint']:
        selected=[axes[h+(j-1)*b+k]for j in ep['stages']for k in range(b)]
        for q in qs:
            need(binary_rank([q]+selected)==1+b*len(ep['stages']),'full productive Gaussian rank');target[1+b*len(ep['stages'])]+=1
    for op in w['events']:
        if op[0]=='IDLE_ONE':
            selected=[axes[h+(j-1)*b+k]for j in op[2]for k in range(b)];need(binary_rank(selected)==b*len(op[2]),'full idle Gaussian rank');idle[b*len(op[2])]+=208
    need(boundaries==208*4*st and N==18+17*st and max(target)==1+17*st,'ambient distinct from largest productive rank')
    need({int(k):v for k,v in cert['target_histogram'].items()}==dict(target)and{int(k):v for k,v in cert['idle_histogram'].items()}==dict(idle),'exact full208 geometry invoices')
    q=qs[0];E=axes[h:h+b];need(binary_rank([q]+E[:-1]+E[:1])<18,'duplicated native axis detected')
    need(Counter(E)!=Counter([q]+E),'omitted head factor detected')
    return {'status':'PASS_INDEPENDENT_WHOLE_JOB_GEOMETRY','ports':208,'ambient_dimension':N,'native_dimension':18,'fresh_body_dimension':17,'absolute_boundaries':boundaries,'all_type_A_distinct_main_assignments':208*st*4,'maximum_target_rank':1+17*st,'target_histogram':dict(target),'idle_histogram':dict(idle),'fresh_orthonormal_completions_different_from_author':changed,'fresh_port_bases':fresh,'negative_controls':['duplicated_fresh_axis','omitted_head_factor'],'scope':'Prospective exact HOST2 geometry only; no h18 native, helper source or acquisition word supplied.'}


def rational_matrix_identity(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def r1_apply(M,x,y,c):
    ym=[sum(y[i]*M[i][j]for i in range(len(M)))for j in range(len(M))]
    return [[v+c*x[i]*ym[j]for j,v in enumerate(row)]for i,row in enumerate(M)]

def chain_sites(a):
    n=2*a+1;left=[];right=[]
    for i in range(1,a+1):
        x=[F(0)]*n;y=[F(0)]*n;x[0]=1;x[i]=1;y[0]=1;y[i]=-1
        for j in range(1,i):x[j]=2
        left.append((x,y))
        x=[F(0)]*n;y=[F(0)]*n;x[0]=-1;x[a+i]=1;y[0]=1;y[a+i]=1
        for j in range(i+1,a+1):x[a+j]=2
        right.append((x,y))
    return left,right

def universal_lemma_controls():
    cases=[]
    for a in [1,2,3,4,5,6,9,12]:
        n=2*a+1;left,right=chain_sites(a);eps=(-1)**a
        w=[F(1)]+[F(1)]*a+[-F(1)]*a;v=[-F(1)]+[F(0)]*a+[F(2)]*a;e=[F(1)]+[F(0)]*(n-1)
        y=[F(1-eps)]+[-F(eps*((-1)**i))for i in range(1,a+1)]+[-F((-1)**i)for i in range(1,a+1)]
        need(sum(x*z for x,z in zip(e,w))==1 and sum(x*z for x,z in zip(y,w))==sum(x*z for x,z in zip(y,v))==0,'universal middle annihilators')
        L_inv=rational_matrix_identity(n)
        for x,z in reversed(left):L_inv=r1_apply(L_inv,x,z,2)
        L_formula=rational_matrix_identity(n);L_formula[0]=[F(2-eps)]+[F(2*((-1)**i))for i in range(1,a+1)]+[F(0)]*a
        for i in range(1,a+1):L_formula[i]=[F(2)]+[F(-int(j==i))for j in range(1,n)]
        need(L_inv==L_formula,'triangular left inverse formula')
        R_inv=rational_matrix_identity(n)
        for x,z in reversed(right):R_inv=r1_apply(R_inv,x,z,2)
        Aprime=[F(eps)]+[F(0)]*a+[F(2*((-1)**i))for i in range(1,a+1)]
        R_formula=rational_matrix_identity(n);R_formula[0]=Aprime
        for i in range(1,a+1):R_formula[a+i]=[-2*t-F(j==a+i)for j,t in enumerate(Aprime)]
        need(R_inv==R_formula,'triangular right inverse formula')
        M=rational_matrix_identity(n)
        for x,z in left:M=r1_apply(M,x,z,-2)
        M=r1_apply(M,w,e,-2);M=r1_apply(M,v,y,-2)
        for x,z in right:M=r1_apply(M,x,z,-2)
        need(M==[[-F(i==j)for j in range(n)]for i in range(n)],'full S=-1 chain identity')
        cases.append({'arms':a,'roles_per_chain':n,'parity':eps,'exact_inverse_and_middle':True})
    # The three-query involution gadget is checked directly in the Q^2 subring.
    z=();r=[{(j,0,z):ONE}for j in range(4)];a,b,c,d=r
    p=[c,add(a,d),add(b,c),d];p[0]=add(p[0],p[1],qshift=2);p[1]=add(p[1],add(p[2],p[0],(-F(1),F(0))),qshift=2);p[2]=add(p[2],add(p[3],p[1],(-F(1),F(0))),qshift=2);p[0]=add(p[0],p[2],(-F(1),F(0)))
    need(p==[scaled(a,qshift=2),scaled(b,qshift=2),add(c,d,qshift=2),d],'all-four-input three-query involution identity')
    return {'finite_chain_controls':cases,'three_query_identity':'exact in abstract involution subring','scope':'Finite controls substantiate a separately reviewed universal induction/idempotent proof; not an extrapolation from these cases.'}


def exact_tariff_screen():
    scale=10**32;cache={}
    def power(n):
        if n not in cache:
            goal=n**199*scale**200;lo=0;hi=n*scale+1
            while hi-lo>1:
                x=(lo+hi)//2
                if x**200<=goal:lo=x
                else:hi=x
            need(lo**200<=goal<hi**200,'exact rational power bracket');cache[n]=(F(lo,scale),F(hi,scale))
        return cache[n]
    def moment(profile):
        lo=hi=F(0)
        for n,c in profile.items():
            a,b=power(n);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
        return lo,hi
    def profile(a,r):
        z=Counter({1+34*a:2})
        for j in range(1,a+1):z[1+17*j]+=4
        z[1]-=4
        for j in range(1,a):z[17*j]-=4
        z[17]-=8*a;z[r]-=F(2*a,13)
        return {n:c for n,c in z.items()if c}
    def combine(*pairs):
        z={}
        for c,p in pairs:
            for n,v in p.items():z[n]=z.get(n,F(0))+c*v
        return {n:c for n,c in z.items()if c}
    cases={}
    for r in[14,16]:
        cases[r]=[{'arms':a,'stages':2*a,'per_port_total_room':moment(profile(a,r)),'per_port_per_native_room':tuple(v/(2*a)for v in moment(profile(a,r)))}for a in range(1,7)]
    need(moment(combine((1,profile(4,14)),(-1,profile(3,14))))[0]>0 and moment(combine((1,profile(5,14)),(-1,profile(4,14))))[1]<0,'concave total-room maximum at a4 for stipulated14')
    need(moment(combine((1,profile(2,16)),(-1,profile(1,16))))[0]>0 and moment(combine((1,profile(3,16)),(-1,profile(2,16))))[1]<0,'concave total-room maximum at a2 for rank16')
    need(moment(profile(2,16))[1]<0,'rank16 account fails even at its universal maximum')
    need(moment(combine((2,profile(3,14)),(-3,profile(2,14))))[0]>0 and moment(combine((3,profile(4,14)),(-4,profile(3,14))))[1]<0,'per-native room universally maximized at a3')
    delta=moment({8:1,9:1,17:-1});need(delta[0]>0,'real tag-stop split surcharge')
    limit=cases[14][2]['per_port_per_native_room'];need(limit[1]-2*delta[0]<0,'two tag stops per port already exceed best stipulated14 allowance')
    stops=[]
    for a in[3,4]:
        room=cases[14][a-1]['per_port_per_native_room'];ratio=(208*room[0]/delta[1],208*room[1]/delta[0]);lo=ratio[0].numerator//ratio[0].denominator;hi=ratio[1].numerator//ratio[1].denominator
        need(lo==hi and F(lo)<ratio[0]and F(lo+1)>ratio[1],'exact integer shared-stage stop cap')
        stops.append({'arms':a,'maximum_additional_rank8_plus_rank9_tag_stops_per_native_at_stipulated_row14':lo,'strict_allowance_ratio':ratio})
    return {'exponent':'199/200','model':'All208 ports type A, four cheapest rank17 mains per port per native;16 separately charged rows of stipulated rank r per native; zero other net helper/ordinary/source expense. This is not a realized native.','cases':cases,'universal_concavity_formula':'F_(a+1)-F_a=2[(1+34(a+1))^t-(1+34a)^t]+4[(18+17a)^t-(17a)^t]-2[4*17^t+r^t/13], strictly decreasing for0<t<1.','rank14_total_room_optimizer':4,'per_native_room_optimizer':3,'rank16_total_room_optimizer':2,'rank16_all_positive_arms_excluded_under_stated_net_expense_scope':True,'tag_stop_surcharge':delta,'two_stops_per_port_excluded_at_all_arms_under_stated_scope':True,'integer_stop_caps':stops,'scope':'Optimistic stipulated-row and scoped negative accounting only; legitimate additional productive-helper credit is not excluded by setting it to zero.'}


def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v)for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v)for v in x]
    return x

def predecessor_check(author):
    p=author/'source/root_A_efree.json';pin='64486cd1c5a879ffc0312195a39ce4a2ef288f81afb47232c244b9b6f46683d0'
    need(hashlib.sha256(p.read_bytes()).hexdigest()==pin,'retained a9 root pin')
    old=load(p);a=9;n=19;left,right=chain_sites(a)
    w=[F(1)]+[F(1)]*a+[-F(1)]*a;v=[-F(1)]+[F(0)]*a+[F(2)]*a;e=[F(1)]+[F(0)]*(n-1)
    y=[F(2)]+[F((-1)**i)for i in range(1,a+1)]+[-F((-1)**i)for i in range(1,a+1)]
    sites=left+[(w,e),(v,y)]+right;X=[];Y=[]
    for x,z in sites:
        for tag in[0,1]:
            X.append(([F(0)]*n if tag else[])+x+([]if tag else[F(0)]*n));Y.append(([F(0)]*n if tag else[])+z+([]if tag else[F(0)]*n))
    need(X==[[F(v)for v in r]for r in old['X']]and Y==[[F(v)for v in r]for r in old['Y']],'all40 inherited a9 X/Y unit vectors agree exactly')
    q=author/'source/query-only-PROOF.md';qpin='0cede285a98dd61b78020651202729c6d9cd16fb078ee5fe9a01aa2400df5432'
    need(hashlib.sha256(q.read_bytes()).hexdigest()==qpin,'inherited three-query gadget source pin')
    return {'a9_root_sha256':pin,'a9_units_identical':40,'three_query_predecessor_sha256':qpin,'credit':'The chain and three-query four-input gadget are inherited; the reviewed contribution is the parity-uniform extension and actual short caller/interface.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=BASE/'worker-a/short-rectangular-caller');p.add_argument('--native',type=Path,default=BASE/'worker-b/singular-gram-history/dependencies/native.json.gz');p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));args=p.parse_args()
    need(hashlib.sha256(args.native.read_bytes()).hexdigest()==NATIVE_PIN,'native104 source pin')
    native=load(args.native);freeze=args.author/'FREEZE.json';freeze_pin='9449d75137f8905ed30d5d4e8330532caf631979c7733dfcf722e0c199e4f8e2';need(hashlib.sha256(freeze.read_bytes()).hexdigest()==freeze_pin,'author scientific freeze pin')
    for file,pin in load(freeze).items():need(hashlib.sha256((args.author/file).read_bytes()).hexdigest()==pin,'frozen scientific file '+file)
    pins={'author_freeze':freeze_pin,'native':NATIVE_PIN,'proof':'f32879fe9ef366ebbf30d4ac7c5e1871870003431b1f1388953b3921a35cad18'}
    need(hashlib.sha256((args.author/'PROOF.md').read_bytes()).hexdigest()==pins['proof'],'frozen proof pin')
    variants=[]
    for a,pin in[(3,'4b4bb800d1c1360d462ac2a89a1aa41eeaf0db1cda2b3eba9b7fb3dfbae640a8'),(4,CALLER_PIN)]:
        folder=args.author/f'a{a}-h18';raw=(folder/'CALLER.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==pin,'frozen exact caller pin');pins[f'caller_a{a}']=pin
        w=json.loads(gzip.decompress(raw));cert=load(folder/'GEOMETRY.json.gz');r=replay(w);g=geometry(native,w,cert);variants.append({'arms':a,'formal_replay':r,'geometry':g});print(json.dumps({'arms':a,'status':'PASS','arbitrary_inputs':w['roles'],'events':len(w['events']),'whole_boundaries':g['absolute_boundaries']}),flush=True)
    lemmas=universal_lemma_controls();tariff=exact_tariff_screen();predecessor=predecessor_check(args.author)
    result={'status':'PASS_INDEPENDENT_SHORT_RECTANGULAR_CALLER','pins':pins,'variants':variants,'universal_lemma_controls':lemmas,'tariff_screen':tariff,'predecessor':predecessor,'classification':'Universal caller algebra reviewed; two finite source words checked directly; prospective native/whole-job geometry conditional; no h18 native or new kappa.'}
    args.output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n');print('PASS: exact non-sampled group algebra, all arbitrary endpoints, prospective geometry and exact scoped invoice')

if __name__=='__main__':main()
