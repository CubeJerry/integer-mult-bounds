"""Exact finite recovery core, for @CubeJerry with OpenAI Codex; Apache-2.0."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from math import prod
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent
ROOT=P.parents[1]
A,B,D=51008161,50979600,50983170

def require(ok,message):
    if not ok: raise ValueError(message)

def source(path):
    pins=json.loads((P/'SOURCES.json').read_text())['files']
    pin=next(x for x in pins if x['path']==path)
    data=(ROOT/path).read_bytes()
    require(hashlib.sha256(data).hexdigest()==pin['sha256'],'source SHA256 '+path)
    return data

def source_code():
    cs=json.loads(source('research/precision-state-frontier/FIXTURE.json'))['mode_columns']
    require(len(cs)==8 and all(len(c)==112 for c in cs),'matrix dimensions')
    require(all(type(x) is int for c in cs for x in c),'integer matrix')
    gram=[[sum(x*y for x,y in zip(c,d)) for d in cs] for c in cs]
    require(gram==[[56*int(i==j) for j in range(8)] for i in range(8)],'source Gram')
    rows=[sum((cs[j][i]%2)<<j for j in range(8)) for i in range(112)]
    code=[v for v in range(256) if all((v&r).bit_count()%2==0 for r in rows)]
    require(len(code)==16,'code size')
    require(Counter(v.bit_count() for v in code)=={0:1,4:14,8:1},'code weights')
    require(all((u&v).bit_count()%2==0 for u in code for v in code),'self-dual code')
    masses={}
    for v in range(256):
        coset=frozenset(v^c for c in code)
        value=sum(7**(8-u.bit_count())*6**u.bit_count() for u in coset)
        expected=A if v in code else (D if v.bit_count()%2 else B)
        require(value==expected,'literal coset mass')
        masses[coset]=value
    require(Counter(masses.values())=={A:1,B:7,D:8},'quotient classes')

def mass(v): return A if v==0 else (D if v&1 else B)

def table(cs):
    out=[0]*16
    for u in range(1,16):
        b=(u&-u).bit_length()-1
        out[u]=out[u^(1<<b)]^cs[b]
    return out

def map_domination():
    counts=Counter()
    for cs in product(range(16),repeat=4):
        vs=table(cs); parity=sum((c&1)<<i for i,c in enumerate(cs))
        if parity:
            low=[D if (u&parity).bit_count()%2 else B for u in range(1,16)]
            counts['nonzero_parity']+=1
        else:
            ks=[u for u in range(1,16) if vs[u]==0]
            require(ks,'even image has kernel')
            low=[A if u==min(ks) else B for u in range(1,16)]
            counts['zero_parity']+=1
        require(all(mass(vs[u])>=low[u-1] for u in range(1,16)),'map domination')
    require(sum(counts.values())==65536,'all maps')
    return dict(counts)

def allocate(forms):
    a,d=F(A,B),F(D,B)
    ws=[d**sum((u&p).bit_count()%2 for p in forms) for u in range(1,16)]
    xs=[0]*15
    for _ in range(27-len(forms)):
        k=min(range(15),key=lambda j:ws[j]*a**xs[j]);xs[k]+=1
    return sum(w*a**x for w,x in zip(ws,xs))*B**27,xs

def optimum():
    target=3*A*B**26+12*A*A*B**25
    require(D**8>A*B**7,'monotone product ratio')
    require(15**15*A**23*D**32*B**350>target**15,'AM-GM Y>=4')
    receipts=[]
    for y in range(4):
        values=[]
        for forms in combinations_with_replacement(range(1,16),y):
            value,xs=allocate(forms)
            require(value.denominator==1,'integral count')
            require(value>=target and (y==0 or value>target),'claimed minimum')
            if y==0:require(Counter(xs)=={1:3,2:12},'balanced kernels')
            values.append(int(value))
        receipts.append({'Y':y,'multisets':len(values),'minimum':min(values)})
    require([r['multisets'] for r in receipts]==[1,15,120,680],'complete small-Y domain')
    return target,receipts

def abstract_relation():
    kernels=list(range(1,16))+list(range(4,16));maps=[]
    for k in kernels:
        pivot=(k&-k).bit_length()-1;other=[i for i in range(4) if i!=pivot];vs=[]
        for u in range(16):
            v=u^(k if (u>>pivot)&1 else 0)
            vs.append(sum(((v>>i)&1)<<(j+1) for j,i in enumerate(other)))
        require([u for u,v in enumerate(vs) if v==0]==[0,k],'rank-three kernel')
        require(all(v%2==0 for v in vs),'even image')
        require(all(vs[u^v]==vs[u]^vs[v] for u in range(16) for v in range(16)),'linear map')
        maps.append(vs)
    words=[tuple(m[u] for m in maps) for u in range(16)]
    require(len(set(words))==16,'four-dimensional relation')
    require(all(sum(v!=0 for v in w)>=25 for w in words[1:]),'no one-coordinate relation')
    value=sum(prod(mass(v) for v in w) for w in words)
    require(value==A**27+3*A*B**26+12*A*A*B**25,'abstract count')
    return value

def main():
    source('research/refined-native-recovery/CHAIN_PROOF.md');source_code()
    maps=map_domination();target,minima=optimum();zero=abstract_relation()
    low,upper=A**27+15*B**27,16*A**27
    require(2**695<low<=zero<=upper<2**696,'696-bit bracket')
    receipt={'schema':'refined-recovery-overload-core-v1','depth':27,'A':A,'B':B,'D':D,
             'map_counts':maps,'Y_multiset_minima':minima,'minimum_zero_fiber':zero,
             'generic_lower':low,'uniform_syndrome_upper':upper,'minimum_tag_bits':696,
             'new_kappa':False}
    print(json.dumps(receipt,sort_keys=True,separators=(',',':')))
    print('PASS_REFINED_RECOVERY_OVERLOAD_CORE maps=65536 multisets=816 tag_bits=696')

if __name__=='__main__':main()
