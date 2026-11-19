#!/usr/bin/env python3
"""Compile a phasewise K370 Cauchy mixer on its actual original owners."""
import argparse,gzip,hashlib,json
from pathlib import Path
POLY=529
L_PIN='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
R_PIN='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
def need(ok,label):
    if not ok:raise ValueError(label)
def mul(a,b):
    out=0
    while b:
        if b&1:out^=a
        a<<=1
        if a&512:a^=POLY
        b>>=1
    return out
def power(a,n):
    out=1
    while n:
        if n&1:out=mul(out,a)
        a=mul(a,a);n>>=1
    return out
def inv(a):
    need(a!=0,'nonzero inverse');r=power(a,510)
    need(mul(a,r)==1,'inverse identity');return r
def rank(M):
    A=[r[:]for r in M];h=0
    for c in range(len(A[0])if A else 0):
        k=next((k for k in range(h,len(A))if A[k][c]),None)
        if k is None:continue
        A[h],A[k]=A[k],A[h];z=inv(A[h][c]);A[h]=[mul(z,x)for x in A[h]]
        for i in range(h+1,len(A)):
            z=A[i][c]
            if z:A[i]=[x^mul(z,y)for x,y in zip(A[i],A[h])]
        h+=1
        if h==len(A):break
    return h
def rem(a,b):
    while a and a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
    return a
def gcd(a,b):
    while b:a,b=b,rem(a,b)
    return a
def binary(M):
    n=len(M);rows=[0]*(9*n)
    for i in range(n):
        for j in range(n):
            for s in range(9):
                v=mul(M[i][j],1<<s)
                for t in range(9):
                    if v>>t&1:rows[9*i+t]^=1<<(9*j+s)
    return rows
def compile_word(M):
    n=len(M);A=M[:];undo=[]
    def add(d,s):
        need(d!=s,'distinct ADD');A[d]^=A[s];undo.append([d,s])
    for c in range(n):
        k=next((k for k in range(c,n)if A[k]>>c&1),None)
        need(k is not None,'invertible binary map')
        if k!=c:add(c,k);add(k,c);add(c,k)
        for i in range(n):
            if i!=c and A[i]>>c&1:add(i,c)
    need(A==[1<<i for i in range(n)],'reduction identity')
    word=undo[::-1];state=[1<<i for i in range(n)]
    for d,s in word:state[d]^=state[s]
    need(state==M,'literal all-input forward word')
    for d,s in reversed(word):state[d]^=state[s]
    need(state==[1<<i for i in range(n)],'literal inverse word')
    return word
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    rp=base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    lr,rr=gzip.decompress(lp.read_bytes()),gzip.decompress(rp.read_bytes())
    need(hashlib.sha256(lr).hexdigest()==L_PIN,'layout pin');need(hashlib.sha256(rr).hexdigest()==R_PIN,'routes pin')
    l=json.loads(lr);routes=[json.loads(x)for x in rr.splitlines()];roots=l['root_table'];D=list(map(set,l['D4']));K=set(l['A2'][370])
    source=[j for j in range(111)if all(sum(x*y for x,y in zip(roots[j],roots[i]))==0 for i in K)]
    need(K=={1,73,80}and len(source)==36,'K370 geometry')
    need(power(2,512)==2 and gcd(power(2,8)^2,POLY)==1,'degree9 irreducibility')
    xs=list(range(45));ys=list(range(64,109));need(len(set(xs+ys))==90,'Cauchy nodes')
    C=[[inv(x^y)for y in ys]for x in xs];need(rank(C)==45,'full Cauchy inverse')
    receiver_order=[1,73,80];phases={};words={};minors=0
    for phase in ['X','Y']:
        selected=[r for r in routes if r[0]==phase and r[5]==370]
        need(len(selected)==45,'actual phase quota')
        def fid(r):return (0 if phase=='X'else 53280)+480*r[1]+r[2]
        by_D={r[4]:r for r in selected};ds=sorted(by_D);need(len(ds)==45,'one owner per D flag')
        inp=[fid(by_D[d])for d in ds];out=[]
        for i in receiver_order:
            block=sorted(fid(r)for r in selected if(r[7]if phase=='X'else r[1])==i)
            need(len(block)==15,'receiver phase quota');out+=block
        owners=sorted(inp);need(set(owners)==set(out)and len(set(owners))==45,'same physical owner set')
        index={f:i for i,f in enumerate(owners)};physical=[[0]*45 for _ in range(45)]
        for i,fo in enumerate(out):
            for j,fi in enumerate(inp):physical[index[fo]][index[fi]]=C[i][j]
        B=binary(physical);word=compile_word(B);words[phase]=word
        for j in source:
            cols=[c for c,d in enumerate(ds)if j in D[d]];need(len(cols)==15,'donor incoming cut')
            for k,i in enumerate(receiver_order):
                need(rank([[C[r][c]for c in cols]for r in range(15*k,15*(k+1))])==15,'native donor minor');minors+=1
        phases[phase]={'owner_order':owners,'input_D_order':ds,'input_owner_order':inp,'output_owner_order':out,
                       'forward_ADD':len(word),'inverse_ADD':len(word),'binary_matrix_sha256':hashlib.sha256(json.dumps(B).encode()).hexdigest()}
    bad=[r[:]for r in C];bad[0]=bad[1][:];need(rank(bad)==44,'duplicate output-row fault')
    cols=[c for c,d in enumerate(phases['X']['input_D_order'])if source[0]in D[d]]
    bad=[[C[r][c]for c in cols]for r in range(15)]
    for r in bad:r[0]=0
    need(rank(bad)==14,'omitted donor direction fault')
    a.out.mkdir(parents=True,exist_ok=True)
    raw=json.dumps({'schema':'K370-Cauchy-ADD-words/1','bit_order':'9*local_owner_index + field_basis_bit','phases':words},separators=(',',':')).encode()
    (a.out/'WORD.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    matrix={'field_polynomial':POLY,'row_nodes':xs,'column_nodes':ys,'matrix':C,'receiver_order':receiver_order,'phases':phases}
    (a.out/'MATRIX.json').write_text(json.dumps(matrix,indent=2,sort_keys=True)+'\n')
    f=sum(x['forward_ADD']for x in phases.values())
    result={'status':'PASS_NATIVE_K370_DENSE_PHASE_MIXER','field':'GF512: z^9+z^4+1','exact_minors_checked':minors,'minor_rank':15,
      'one_body_forward_ADD':f,'one_body_forward_plus_inverse_ADD':2*f,'minimum_b3840_forward_plus_inverse_ADD':16*f,
      'new_INIT':0,'new_CLEAR':0,'extra_owned_records':0,'additional_MOVE':0,'retained_entire_atlas_movement_charged':True,
      'word_payload_sha256':hashlib.sha256(raw).hexdigest(),'phases':{k:{z:v for z,v in x.items()if z.endswith('ADD')or z.endswith('sha256')}for k,x in phases.items()},
      'precondition':'Each incoming donor-to-K quotient has rank30s; this package does not establish that premise.',
      'achieves':'Three fullrank30s receiver quotients and their common rank15s early flag at K370.',
      'not_achieved':'Specified target B, source/D gluing, Clifford phase frames, complete supplier or new kappa.',
      'source_pins':[{'path':str(p.relative_to(a.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,rp]],
      'negative_controls':['duplicate row rank45->44','omitted donor direction rank15->14'],'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['exact_minors_checked','one_body_forward_ADD','one_body_forward_plus_inverse_ADD','minimum_b3840_forward_plus_inverse_ADD']},sort_keys=True))
if __name__=='__main__':main()
