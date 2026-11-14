#!/usr/bin/env python3
"""Independent BIT chart/value replay and fixed-prefix facet invoice.
@CubeJerry with OpenAI assistance. No author engine imported.
"""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

@lru_cache(None)
def rref(rows):
    a=[list(map(F,r)) for r in rows];out=0
    for j in range(8):
        z=next((z for z in range(out,len(a)) if a[z][j]),None)
        if z is None:continue
        a[out],a[z]=a[z],a[out];v=a[out][j];a[out]=[x/v for x in a[out]]
        for z in range(len(a)):
            if z!=out and a[z][j]:
                c=a[z][j];a[z]=[x-c*y for x,y in zip(a[z],a[out])]
        out+=1
    return tuple(tuple(x) for x in a[:out])

def chart(f):return rref(tuple(tuple(map(F,r)) for r in f['B']))

def load(p):return json.loads(gzip.decompress(p.read_bytes()))

def replay(w,native,events=False):
    spaces={int(k):chart(v) for k,v in w['frames'].items()}
    need(all(len(spaces[int(k)])==v['dim'] for k,v in w['frames'].items()),'true chart rank')
    facets={chart(native['frames'][str(native['final'][111+i])]):i for i in range(111)}
    rows={i:1<<i for i in range(222)};loc=dict(enumerate(w['start']));moves=Counter();counts=Counter();arr=Counter();dep=Counter();anchors=set();peak=0;lifetimes=0
    for op in w['program']:
        code,f=op[:2];counts[code]+=1
        if code=='INIT':
            _,f,c=op;need(f>=222 and f not in rows,'fresh owner');rows[f]=0;loc[f]=c;lifetimes+=1
        elif code=='ADD':
            _,f,j,c=op;need(f in rows and j in rows and spaces[loc[f]]==spaces[c]==spaces[loc[j]],'cocharted ADD');rows[f]^=rows[j]
        elif code=='CLEAR':
            _,f,c=op;need(f>=222 and f in rows and spaces[loc[f]]==spaces[c],'actual owned retirement');del rows[f];del loc[f]
        elif code=='MOVE':
            _,f,c,d=op;need(f in rows and spaces[loc[f]]==spaces[c],'actual departure');a,b=spaces[c],spaces[d]
            need(len(a)!=len(b) and rref(a+b)==(a if len(a)>len(b) else b),'strict nested MOVE')
            moves[abs(len(a)-len(b))]+=1;loc[f]=d
            if events:
                if f<222:need(len(b)>len(a),'monotone fixed public prefix')
                if len(b)>len(a) and b in facets:
                    i=facets[b]
                    if f==111+i and f not in anchors:anchors.add(f)
                    else:arr[i]+=1
                if len(b)<len(a) and a in facets:dep[facets[a]]+=1
        else:raise ValueError('unexpected opcode '+code)
        peak=max(peak,len(rows)-222)
    need(all(spaces[loc[i]]==spaces[w['final'][i]] for i in range(222)),'all222 actual endpoint charts')
    need(all(rows[i]==1<<i for i in range(111)),'all111 X restored')
    done=[]
    for i in range(111):
        z=rows[111+i]
        need(z>>111==1<<i,'all arbitrary Y baselines retained independently')
        if z==((1<<(111+i))^(1<<i)):done.append(i)
    need(all(i in done for i in range(111) if events and w['final'][111+i]==native['final'][111+i]),'every own-facet handoff target actually complete')
    need(set(i for i in rows if i>=222)==set(w.get('end_owned',[])),'declared retained owner set')
    return dict(profile=dict(moves),counts=dict(counts),peak=peak,lifetimes=lifetimes,completed=done,public_rows=[rows[i] for i in range(222)],owned_rows={str(i):rows[i] for i in rows if i>=222},arrival=dict(arr),departure=dict(dep),anchor_receivers=sorted(i-111 for i in anchors))

def integer_root(n,k):
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//pow(x,k-1))//k
        if y>=x:break
        x=y
    while pow(x,k)>n:x-=1
    while pow(x+1,k)<=n:x+=1
    return x

@lru_cache(None)
def interval(r):
    D=10**30;n=pow(r,199)*pow(D,200);z=integer_root(n,200)
    need(pow(z,200)<=n<pow(z+1,200),'integer-root enclosure')
    return F(z,D),F(z if pow(z,200)==n else z+1,D)

def add(*parts):
    d=Counter()
    for c,p in parts:
        for r,v in p.items():d[int(r)]+=F(c)*F(v)
    return {r:v for r,v in d.items() if v}

def moment(p):
    lo=hi=F(0)
    for r,c in p.items():
        a,b=interval(r);lo+=c*(a if c>0 else b);hi+=c*(b if c>0 else a)
    return lo,hi

def fmt(v):return dict(rational=list(map(str,v)),lower_decimal=float(v[0]),upper_decimal=float(v[1]))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--package',type=Path,required=True);ap.add_argument('--native',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--programme',type=Path,required=True);a=ap.parse_args()
    need(hashlib.sha256(a.native.read_bytes()).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    native=load(a.native)
    proof_pins={'PROOF.md':'07e112c2f60ef4e7c6e1f81955c2f406655b6078d03c38d0876c887bb24e4cad','ALL-ROUTE-EXTENSION.md':'4b7e838beae11241d6ea5c1363c5b0385ab26d50bbad8513534b32656b48f557'}
    for name,digest in proof_pins.items():need(hashlib.sha256((a.package/name).read_bytes()).hexdigest()==digest,'author proof pin')
    N=Counter(abs(native['frames'][str(op[3])]['dim']-native['frames'][str(op[2])]['dim']) for op in native['program'] if op[0]=='MOVE')
    H={2:1,4:25,6:1,8:410}
    P2=add((36,N),(444,{1:1}),(444,{7*j:1 for j in range(1,9)}))
    T2=add((36,H),(222,{127:1}),(444,{1+7*j:1 for j in range(1,10)}))
    S=add((F(1,36),T2),(-F(1,36),P2));need(moment(S)[1]<0,'finite-m correction negative')
    B=add((1,N),(-1,H),(1,S))
    formula=add((F(37,6),{127:1}),(F(37,3),{64:1,1:-1}),(F(37,3),{7*j+1:1 for j in range(1,9)}),(-F(37,3),{7*j:1 for j in range(1,9)}))
    need(B==formula,'independent closed caller formula')
    phi={0:{},**{r:{r:1} for r in range(1,6)},6:{7:1,1:-1},7:{7:1,1:-1},8:{7:1}}
    inequalities=0
    for x in range(9):
        for y in range(9):
            if x==y:continue
            e=int((x==7 and y<7) or (x<7 and y==7))
            need(moment(add((1,{abs(x-y):1}),(-1,phi[x]),(1,phi[y]),(-e,{1:1})))[0]>=0,'facet potential edge')
            inequalities+=1
    c=moment({1:1,8:1,7:-1});need(1<c[0]<=c[1]<2,'excursion coefficient')
    answers=[]
    expected={'canonical-pivot':(18,60),'halfclass-banks':(16,58),'halfclass-two-triples':(10,52),'plain':(12,54),'joined':(10,52)}
    for name,caps in expected.items():
        pre=load(a.package/name/'COALESCED-PREFIX.json.gz');closed=load(a.package/name/'COALESCED-CLOSED-PARTIAL.json.gz')
        pr=replay(pre,native,True);cr=replay(closed,native)
        if name=='canonical-pivot':
            old_path=a.programme/'results/bit-retained-canonical-pivot/author/PREFIX.json.gz'
            old=load(old_path);oldr=replay(old,native,True)
            need(oldr['public_rows']==pr['public_rows'] and oldr['owned_rows']==pr['owned_rows'],'independent agreement with published literal pivot')
            bad=copy.deepcopy(pre);idx=next(j for j,op in enumerate(bad['program']) if op[0]=='MOVE' and op[1]<111 and len(chart(bad['frames'][str(op[3])]))==7);bad['program'][idx][3]=pre['hub']
            try:replay(bad,native,True);rejected=False
            except ValueError:rejected=True
            need(rejected,'mandatory facet access cannot be coalesced away')
        need(pr['arrival']=={0:56} and pr['departure']=={0:1},'exact concentrated prefix traffic')
        need(pr['public_rows']==cr['public_rows'],'closed partial public map')
        need(not cr['owned_rows'],'all closed owners retired')
        need(all(pre['final'][i]==native['final'][i] for i in range(111)),'X at Hub at handoff')
        remaining=sum(pre['final'][111+i]!=native['final'][111+i] for i in range(111))
        need(all(pre['final'][111+i] in (0,native['final'][111+i]) for i in range(111)),'actual handoff Y chart')
        need(Counter(cr['profile'])==Counter(pr['profile'])+Counter({7:remaining}),'only direct public closing routes')
        R=moment(add((1,B),(-1,cr['profile'])));E=moment(add((1,B),(-1,cr['profile']),(-6,{7:1})))
        sixcap=2+int(E[1]//1);need(int(E[0]//1)==int(E[1]//1),'unambiguous strict six-mode floor')
        weighted=(2*R[0]/c[1],2*R[1]/c[0]);allcap=2+int(weighted[1]//1)
        need(int(weighted[0]//1)==int(weighted[1]//1),'unambiguous all-route floor')
        need((sixcap,allcap)==caps,'exact fitting caps')
        author=json.loads((a.package/name/'RESULT.json').read_text())
        need(sixcap==author['full_fitting_foreign_support_charge_cap'],'six-mode author agreement')
        need({str(k):v for k,v in cr['profile'].items()}==author['coalesced_receipts']['closed']['paid_profile'],'independent source profile')
        answers.append(dict(case=name,completed=pr['completed'],prefix_public_rows_checked=222,closed_profile=cr['profile'],prefix_arrival=pr['arrival'],prefix_departure=pr['departure'],R=fmt(R),future_six_mode_events=fmt(E),six_mode_fitting_cap=sixcap,all_route_fitting_cap=allcap,weighted_future_count=fmt(weighted),counts=cr['counts'],owned_lifetimes=cr['lifetimes'],peak_owned=cr['peak']))
    out=dict(status='PASS_INDEPENDENT_FIXED_PREFIX_FACET_SOURCE_AND_PRICE',native_sha256=hashlib.sha256(a.native.read_bytes()).hexdigest(),proof_pins=proof_pins,negative_controls=['unread-stop substitution at mandatory facet rejected by cochart replay'],potential_edges=inequalities,c=fmt(c),finite_m_correction=fmt(moment(S)),cases=answers,scope='Actual finite partial maps, geometry and exact movement inequalities independently checked; universal occurrence normalization inherited and direct proof separately reviewed; no new kappa.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],[(v['case'],v['six_mode_fitting_cap'],v['all_route_fitting_cap']) for v in answers])
if __name__=='__main__':main()
