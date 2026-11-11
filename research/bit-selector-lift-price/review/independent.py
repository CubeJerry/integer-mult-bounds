"""Independent reverse-adjoint selector-lift replay and exact tariff."""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import argparse,gzip,hashlib,json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from arithmetic import F,S,need,sub,scale,moment,report
def rank(matrix):
    a=[[F(x) for x in row] for row in matrix];p=0
    for j in range(8):
        k=next((k for k in range(p,len(a)) if a[k][j]),None)
        if k is None:continue
        a[p],a[k]=a[k],a[p];z=a[p][j];a[p]=[x/z for x in a[p]]
        for k in range(p+1,len(a)):
            z=a[k][j]
            if z:a[k]=[x-z*y for x,y in zip(a[k],a[p])]
        p+=1
    return p
def backward(events,public,total,main_only=False):
    cols=[1<<i if i<public else 0 for i in range(total)]
    for e in reversed(events):
        op,a=e[:2]
        if op=='ADD':
            if not main_only or (a<222 and e[2]<222):cols[e[2]]^=cols[a]
        elif op=='SWAP':
            if not main_only or (a<222 and e[2]<222):cols[a],cols[e[2]]=cols[e[2]],cols[a]
        elif op in ('INIT','CLEAR'):
            if not main_only:cols[a]=0
        elif op!='MOVE':raise ValueError(op)
    return cols
def main(path,caller):
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    need(sha=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','source SHA')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='b718d6b2848215ad785022106dfa9f871a3d1c0c','source blob')
    w=json.loads(gzip.decompress(raw));ff=w['frames'];n=w['public'];owned=w['owned_fields'];events=w['program']
    need((n,owned,len(events))==(659,237,34137),'source counts')
    for f in ff.values():
        B,A=f['B'],f['A'];d=f['dim']
        need(len(B)==rank(B)==d and len(A)==rank(A)==8-d,'frame ranks')
        need(all(sum(F(x)*F(y) for x,y in zip(b,a))==0 for b in B for a in A),'frame annihilators')
    @lru_cache(None)
    def included(a,b):
        return all(sum(F(x)*F(y) for x,y in zip(u,v))==0 for u in ff[str(a)]['B'] for v in ff[str(b)]['A'])
    def dim(a):return ff[str(a)]['dim']
    def frame_check(program,start,finish,public,total):
        state=list(start)+[None]*(total-public);P=Counter();life=0
        for e in program:
            op,a=e[:2]
            if op=='ADD':need(a!=e[2] and state[a]==state[e[2]]==e[3],'same-frame contact')
            elif op=='SWAP':state[a],state[e[2]]=state[e[2]],state[a]
            elif op=='MOVE':
                u,v=e[2:];need(state[a]==u and (included(u,v) or included(v,u)),'nested MOVE')
                r=abs(dim(u)-dim(v));need(r>0,'positive MOVE');P[r]+=1;state[a]=v
            elif op=='INIT':
                need(a>=public and state[a] is None,'owned activation');state[a]=e[2];life+=1
            elif op=='CLEAR':need(a>=public and state[a]==e[2],'owned erasure');state[a]=None
            else:raise ValueError(op)
        need(state==list(finish)+[None]*(total-public),'all final frames')
        return P,life
    paid,source_lives=frame_check(events,w['start'],w['final'],n,n+owned)
    need(all(e[1]>=222 for e in events if e[0] in ('INIT','CLEAR')),'main reset excluded')
    need(all((e[1]<222)==(e[2]<222) for e in events if e[0]=='SWAP'),'no cross-class swaps')
    col=backward(events,n,n+owned)
    need(all(col[i]==((1<<i)^((1<<(i+111)) if i<111 else 0)) for i in range(n)),'original adjoint endpoint')
    need(backward(events,222,222,True)==[1<<i for i in range(222)],'main-only adjoint identity')
    mainpaid=Counter();corepaid=Counter();H=Counter()
    for e in events:
        if e[0]=='MOVE':(mainpaid if e[1]<222 else corepaid)[abs(dim(e[2])-dim(e[3]))]+=1
    need(mainpaid+corepaid==paid,'all original paid jobs')
    for i in range(222,n):
        a,b=w['start'][i],w['final'][i];need(included(a,b) or included(b,a),'helper nesting');H[abs(dim(a)-dim(b))]+=1
    results=[]
    for m in (2,4,6):
        pub=222*m+n-222;total=pub+owned+1;temp=total-1
        def owner(a,c=0):return 222*c+a if a<222 else 222*m+a-222
        lifted=[]
        for e in events:
            op,a=e[:2]
            copies=range(m) if a<222 else (0,)
            for c in copies:
                z=[op,owner(a,c)]+e[2:]
                if op in ('ADD','SWAP'):z[2]=owner(e[2],c if a<222 and e[2]<222 else 0)
                lifted.append(z)
        before=backward(lifted,pub,total)
        missing=0
        for c in range(m):
            for i in range(222):
                a=owner(i,c);want=(1<<a)^((1<<owner(i+111,c)) if i<111 else 0)
                missing+=before[a]!=want
        need(missing==111*m,'adjoint missing columns include selected copy and every passive copy')
        for c in range(1,m):
            for i in range(111):
                x,x0,y=owner(i,c),owner(i),owner(i+111,c)
                u,v=w['final'][i],w['final'][i+111]
                need(dim(u)==8 and dim(v)==7 and included(v,u),'repair actual nesting')
                lifted += [['INIT',temp,u],['ADD',temp,x,u],['ADD',temp,x0,u],['MOVE',temp,u,v],['ADD',y,temp,v],['CLEAR',temp,v]]
        start=w['start'][:222]*m+w['start'][222:];finish=w['final'][:222]*m+w['final'][222:]
        P,lives=frame_check(lifted,start,finish,pub,total);col=backward(lifted,pub,total)
        need(all(col[i]==((1<<i)^((1<<(i+111)) if i<222*m and i%222<111 else 0)) for i in range(pub)),'repaired complete adjoint endpoint')
        expected=Counter({r:m*c for r,c in mainpaid.items()});expected.update(corepaid);expected[1]+=111*(m-1)
        need(P==expected,'literal full paid inventory')
        need(lives==source_lives+111*(m-1),'owned lifetimes')
        results.append({'m':m,'public':pub,'events':len(lifted),'owned_labels':owned+1,'owned_lifetimes':lives,'paid':dict(sorted(P.items())),'adjoint_bad_columns_before':missing,'adjoint_bad_columns_after':0})
    rawcaller=caller.read_bytes()
    need(hashlib.sha256(rawcaller).hexdigest()=='3828d53e80ea97e8b866320f081af20b6b93bfebd58b95b56b85a7afe151af5e','caller SHA')
    need(hashlib.sha1(b'blob '+str(len(rawcaller)).encode()+b'\0'+rawcaller).hexdigest()=='cf55f4271009a06ad192a070d330a4466b6d44fa','caller blob')
    c=json.loads(rawcaller);rootT=Counter();rootP=Counter();local=Counter();ops=Counter()
    for e in c['events']:
        if e[0]=='J':local[e[1]]+=2;continue
        if e[0]!='A':continue
        op=e[1];ops[op]+=1
        if op=='QUERY':rootP[1]+=111
        elif op=='IDLE_ONE':rootP[7*len(e[3])]+=111
    need(local=={j:2 for j in range(1,19)},'all36 native invocations')
    for row in c['types']['A']['diagonal']:
        need(row[0]%2==1 and all(z in (0,1) for z in row[2:]) and any(row[2:]),'nonempty target body')
        rootT[1+7*sum(row[2:])]+=111
    expectedT=Counter({127:222});expectedP=Counter({1:444})
    for j in range(1,10):expectedT[1+7*j]+=444
    for j in range(1,9):expectedP[7*j]+=444
    need(rootT==expectedT and rootP==expectedP,'literal complete root inventory')
    t=F(199,200);T2=Counter({r:36*c for r,c in H.items()});P2=Counter({r:36*c for r,c in paid.items()})
    T2.update(rootT);P2.update(rootP)
    M2=sub(moment(T2,t),moment(P2,t));D=sub(moment(corepaid,t),moment(H,t))
    need(M2[1]<-444*S and D[1]<88*S,'uniform complete moment obstruction')
    unpaid=add_interval(M2,scale(D,18));need(unpaid[0]>0,'omitting paid repair falsely crosses')
    return {'status':'PASS_INDEPENDENT_REVERSE_SELECTOR_LIFT','base':'e54523517d0f03e58352e647c403a5af3e525a57',
      'source_sha256':sha,'frames_checked':len(ff),'source_columns_checked':n,'main_only_identity':True,
      'no_main_core_swap':True,'main_paid':dict(sorted(mainpaid.items())),'core_paid':dict(sorted(corepaid.items())),
      'helpers':dict(sorted(H.items())),'finite_lifts':results,'M2':report(M2),'core_minus_helper':report(D),
      'omitted_repair_m2':report(unpaid),'root_targets':dict(sorted(rootT.items())),'root_paid':dict(sorted(rootP.items())),
      'all_even_m_bound':'-222*m-414*(m-1)<0',
      'no_new_kappa':True,'scope':'This literal selector lift plus one rank1 repair per port/passive copy; no repair optimality or general shared-core impossibility.'}
def add_interval(a,b):return a[0]+b[0],a[1]+b[1]
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True)
    ap.add_argument('--caller',type=Path,required=True);a=ap.parse_args()
    print(json.dumps(main(a.word,a.caller),indent=2))
