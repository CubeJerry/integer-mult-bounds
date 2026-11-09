"""Independent rational budgets and additional genuine native scalar endpoints."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import argparse,json,sys
def need(ok,message):
    if not ok:raise ValueError(message)
def arithmetic():
    cases=0
    for b in range(1,14):
        for S in sorted({1,3,(1<<b)-1}):
            if not 0<S<1<<b:continue
            for G in (0,1,2,7,31):
                a=2*(S-1).bit_length()+2*b+7;lam=F(1,1<<G);eps=F(1,1<<a);eta=lam**3*eps
                q=a+3*G+7;delta=F(2,1<<q);first=lam/4+eta;product=first**2+delta
                opposite=lam*product+eta;final=(eta+lam*((lam/2)*eta+eta**2+delta))/lam**3
                need(first<F(1,2) and product<F(1,4) and opposite<F(1,2),'actual-input radius induction')
                need(final<2*eps and final*S*S*(1<<(2*b+4))<F(1,4),'strict recovery margin')
                W=q+3*G+4*b+6;shift=2*b+4+3*G
                need((1<<(q-1))*S*S*(1<<shift)<1<<(W-1),'largest exact scalar intermediate')
                for m in (1,3,16,31):
                    tau=a+2*G+2;z=tau+G+(m-1).bit_length()+1
                    need(2*m*F(1,1<<z)<=F(1,1<<(tau+G)),'raw group budget uses full Gamma')
                    for U in (0,1,z+2,z+31):need(max(1,z+2-U)<=max(1,z+2),'source-first target order')
                cases+=1
    tau,Kf,Kc=40,1,3;G=Kf+Kc
    need(F(9,5)*F(1,1<<(tau+Kc+1))>F(1,1<<(tau+G)),'missing Kf target increase detected')
    a,G=15,8;lam=F(1,1<<G);eps=F(1,1<<a)
    need(F(2,1<<(a+G+7))/lam**2>2*eps,'underfunded restored product grid detected')
    return dict(cases=cases,group_budget_cases=4*cases,target_order_cases=16*cases,negative_controls=['missing compression target increase','underfunded restored product grid'])
def native(pkg):
    sys.path.insert(0,str(pkg));from source_binding import opened
    receipts=[]
    with opened() as state:
        from deferred_tail import DeferredTail
        from cardinal_counts import Count
        from records import Tape
        from ring_words import Signed,write_signed
        from router_metadata import owned
        from session import initialize_marker,erase_marker
        from check_support import no_decode
        def field(pairs,width):
            t=Tape();erase_marker(t);initialize_marker(t)
            with owned(Count.literal(width)) as (w,):
                for pair in pairs:
                    for v in pair:
                        with owned(Signed(Count.literal(abs(v)),v<0)) as (n,):write_signed(n,t,w)
            t.rewind();return t
        def read(t,count,width):
            bits=t.cells[1:1+count*width];need(len(bits)==count*width,'complete result');values=[]
            for i in range(count):
                row=bits[i*width:(i+1)*width];need(all(v in (0,1) for v in row),'binary signed word')
                values.append(sum(v<<j for j,v in enumerate(row))-(row[-1]<<width))
            return values
        def clean(t):t.clear();erase_marker(t)
        for S,b,G in ((1,1,0),(3,2,1),(7,3,5)):
            shift=2*b+4+3*G;q=shift+2;W=q+3*G+4*b+6;half=1<<(q-1)
            params=[Count.literal(v) for v in (S,b,q,G)];saved=[bytes(x.tape.cells) for x in params]
            owner=DeferredTail(state,*params);xs=[half,-half,3,-3,1,-1,0][:S]
            src=field([(x,0) for x in xs],q+2);before=bytes(src.cells)
            with no_decode():out=owner.run(src)
            target=[F(x*S*S*(1<<shift),1<<q) for x in xs]
            expected=[(v+F(1,2)).numerator//(v+F(1,2)).denominator for v in target]
            need(read(out,S,W)==expected,'full-width exact two-S/deferred-shift recovery')
            need(bytes(src.cells)==before and src.head==1,'borrowed field unchanged');owner.consume()
            left=field([(half,0)]*S,q+2);right=field([(0,-half)]*S,q+2)
            with no_decode():product=owner.run(left,right)
            need(read(product,2*S,q+2)==[v for _ in range(S) for v in (0,-(1<<(q-2)))],'half-disk boundary to quarter-disk product')
            owner.consume();wide=field([(0,half)]*S,q+3)
            with no_decode():narrow=owner.carrier(wide,conjugate=True)
            need(read(narrow,2*S,q+2)==[v for _ in range(S) for v in (0,-half)],'exact carrier/conjugation at radius boundary')
            owner.consume();need(all(bytes(x.tape.cells)==raw and x.tape.head==1 for x,raw in zip(params,saved)),'borrowed encoded descriptors protected')
            receipts.append(dict(S=S,b=b,Gamma=G,q=q,W=W,recovered=expected,scalar_calls=dict(owner.word.calls)));owner.close()
            for t in (src,left,right,wide):clean(t)
            for x in params:x.close()
    return receipts
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('package',type=Path);p.add_argument('--output',type=Path);a=p.parse_args();pkg=a.package.resolve()
    r=dict(status='independent budget and scalar endpoint checks passed',mathematics=arithmetic(),native_endpoints=native(pkg),production_transforms_executed=False,extraction_or_CRT_executed=False,reviewed_files={n:sha256((pkg/n).read_bytes()).hexdigest() for n in ('PROOF.md','deferred_tail.py','allocation.py')})
    if a.output:a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,sort_keys=True))
