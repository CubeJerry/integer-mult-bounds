"""Independent raw-source preparation for a complete selector witness audit."""
from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
from itertools import product
import gzip,hashlib,json,math,random,csv,argparse
ap=argparse.ArgumentParser()
for name in ('word','screen-input','witnesses','output'):ap.add_argument('--'+name,type=Path,required=True)
args=ap.parse_args();p=1000000007
def need(b,s):
    if not b:raise ValueError(s)
need(all(p%d for d in range(2,math.isqrt(p)+1)),'prime modulus')
need(2*(p-1)**2+(p-1)<2**64,'unsigned64 products and sums')
raw=args.word.read_bytes()
need(hashlib.sha256(raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','word SHA')
w=json.loads(gzip.decompress(raw));h=w['hosted'];events=w['program'];N=w['public'];owned=w['owned_fields']
def rank(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j not in piv:piv[j]=x;break
            x^=piv[j]
    return len(piv)
need(all(all(type(x)is int and 0<x<512 for x in f) and rank(f)==len(f) for f in w['frames']),'GF2 frames')
need((h['alpha'],h['beta'],h['alpha2'],h['beta2'])==('-1','1/2','-1','0'),'actual endpoint conventions')
main=sorted(set(w['live'])|{r+112 for r in w['live']}|set(h['X2'])|set(h['Y2']));idx={r:i for i,r in enumerate(main)}
helpers=[i for i in range(N) if i not in idx];core=helpers+list(range(N,N+owned));ci={r:800+i for i,r in enumerate(core)}
need((len(main),len(helpers),len(core))==(400,1080,1131),'source partition')
def slot(r,c=0):return idx[r]+400*c if r in idx else ci[r]
rng=random.Random(20261111);initial=[rng.randrange(p) for _ in range(1880)]+[0]*owned
expected=initial[:]
for c in (0,1):
    for i,x in enumerate(w['live']):
        a,b=slot(x,c),slot(x+112,c);xx,yy=initial[a],initial[b]
        if i in h['Dports']:expected[b]=(xx+yy)%p
        else:expected[a]=(xx-yy)%p;expected[b]=(xx+yy)*pow(2,-1,p)%p
    for x,y in zip(h['X2'],h['Y2']):expected[slot(x,c)]=(initial[slot(x,c)]-initial[slot(y,c)])%p
def coefficient(x):
    q=Q(x);need(q.denominator%p!=0,'invertible denominator')
    return q.numerator*pow(q.denominator,-1,p)%p
counts=Counter();combined=Counter()
for e in events:
    if e[0] in ('ADD','COPY') and ((e[1] in idx)!=(e[2] in idx)):
        role=e[2] if e[2] in idx else e[1];direction=int(e[1] in idx)
        counts[role,direction]+=1;combined[role]+=1
seen=Counter();both=Counter();state=w['initial']+[None]*owned;instructions=[];denominators=set()
for i,e in enumerate(events):
    op,r=e[:2];d0=slot(r);d1=slot(r,1) if r in idx else -1
    if op=='MOVE':
        a,b=w['frames'][e[2]],w['frames'][e[3]]
        need(state[r]==e[2] and rank(a+b)==max(len(a),len(b)),'nested MOVE version');state[r]=e[3];continue
    if op in ('INIT','CLEAR'):
        need(r>=N,'owned reset')
        if op=='INIT':need(state[r] is None,'fresh INIT');state[r]=e[2]
        else:need(state[r]==e[2],'CLEAR chart');state[r]=None
        instructions.append((4,d0,-1,0,0,0,0));continue
    denominators.add(Q(e[-2]).denominator);q=coefficient(e[-2]);mask=0
    if op=='SCALE':
        need(state[r]==e[-1],'SCALE chart');instructions.append((3,d0,d1,0,0,q,0));continue
    need(op in ('ADD','COPY'),'known scalar opcode');s=e[2]
    need(state[r]==state[s]==e[-1],'same-chart source contact')
    s0=slot(s);s1=slot(s,1) if s in idx else -1
    if (r in idx)!=(s in idx):
        role=s if s in idx else r;direction=int(r in idx);c=seen[role,direction];n=counts[role,direction];k=both[role];m=combined[role]
        bits=[0,1,c%2,int(c==0),int(c==n-1),int(2*c>=n),k%2,int(k==0),int(k==m-1),int(2*k>=m),len(w['frames'][state[r]])%2,int(2*i>=len(events)),idx[role]%2,int(c%3==0)]
        mask=sum(b<<j for j,b in enumerate(bits));seen[role,direction]+=1;both[role]+=1;typ=1+direction
    else:typ=0
    if op=='COPY':
        need(r>=N and events[i-1]==['INIT',r,e[-1]],'COPY immediate ideal-zero INIT');typ=5
    instructions.append((typ,d0,d1,s0,s1,q,mask))
need(state==w['final']+[None]*owned,'all final frames')
need(seen==counts and both==combined,'contact clocks cover source')
source_input=args.screen_input.read_bytes()
need(hashlib.sha256(source_input).hexdigest()=='de0e0fc24c0b816e3c1ca1aa6de1259ecd0725c2835b64c762b3cc49eb974d65','screen input pin')
lines=source_input.decode().splitlines()
need(list(map(int,lines[1].split()))==initial[:400] and list(map(int,lines[2].split()))==initial[400:800] and list(map(int,lines[3].split()))==initial[800:],'exact full input values')
need(list(map(int,lines[4].split()))==expected[:400] and list(map(int,lines[5].split()))==expected[400:800],'coupled8-port targets and second family')
raw_result=args.witnesses.read_bytes()
need(hashlib.sha256(raw_result).hexdigest()=='5c774b5db931cad2379307b1a97496d96d3501234bd31a77d83a758f61d0746a','witness receipt pin')
records=[list(map(int,line.split())) for line in raw_result.decode().splitlines()[1:]]
need(len(records)==19600 and {tuple(row[:6]) for row in records}==set(product(range(14),range(14),range(5),range(5),range(2),range(2))),'full Cartesian domain without duplicates')
need(all(0<=r[9]<1880 and 0<=r[10]<p and 0<=r[11]<p and r[10]!=r[11] for r in records),'nonzero witness records')
out=[f'1931 1880 {len(instructions)} 19600',' '.join(map(str,initial)),' '.join(map(str,expected))]
out+=[' '.join(map(str,r)) for r in instructions];out+=[' '.join(map(str,r)) for r in records]
args.output.write_text('\n'.join(out)+'\n')
print(json.dumps({'status':'PASS_INDEPENDENT_DOMAIN_PREPARATION','prime_trial_divisions':math.isqrt(p)-1,'denominators':sorted(denominators),'cases':len(records),'instructions':len(instructions),'word_sha256':hashlib.sha256(raw).hexdigest(),'source_receipt_sha256':hashlib.sha256(raw_result).hexdigest()},indent=2))
