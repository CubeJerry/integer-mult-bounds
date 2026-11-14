#!/usr/bin/env python3
"""Independent rational/set-valued review of two paid point preloads."""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def need(b,m):
    if not b:raise ValueError(m)
def dot(x,y):return sum(Q(a)*Q(b) for a,b in zip(x,y))
def rank(A):
    p={}
    for x in A:
        while x:
            j=x.bit_length()-1
            if j in p:x^=p[j]
            else:p[j]=x;break
    return len(p)
def qrank(A):
    A=[list(map(Q,r)) for r in A];at=0
    for j in range(8):
        h=next((h for h in range(at,len(A)) if A[h][j]),None)
        if h is None:continue
        A[at],A[h]=A[h],A[at];z=A[at][j];A[at]=[v/z for v in A[at]]
        for h in range(at+1,len(A)):
            z=A[h][j]
            A[h]=[x-z*y for x,y in zip(A[h],A[at])]
        at+=1
    return at
def replay(w):
    state={i:(c,{i}) for i,c in enumerate(w['start'])};ever=set(state);counts=Counter();moves=Counter();peak=0
    for op in w['program']:
        t,i=op[:2];counts[t]+=1
        if t=='INIT':
            need(i>=222 and i not in ever,'fresh initialization');ever.add(i);state[i]=(op[2],set());peak=max(peak,len(state)-222)
        elif t=='ADD':
            _,i,j,c=op;need(i!=j and state[i][0]==state[j][0]==c,'cochart addition');state[i]=(c,state[i][1]^state[j][1])
        elif t=='MOVE':
            _,i,a,b=op;need(state[i][0]==a,'actual source chart');A,B=w['frames'][str(a)],w['frames'][str(b)];d=B['dim']-A['dim']
            need(d>0 if i<222 else (i in (334,335,336,337) and d<0),'monotone declared paths')
            small,large=(A,B) if d>0 else (B,A)
            need(all(dot(x,y)==0 for x in small['B'] for y in large['A']),'exact nested move');state[i]=(b,state[i][1]);moves[abs(d)]+=1
        elif t=='CLEAR':need(i>=222 and state[i][0]==op[2],'owned clear');del state[i]
        else:raise ValueError(t)
    return state,counts,moves,peak

def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');n=json.loads(gzip.decompress(raw))
    praw=a.prefix.read_bytes();w=json.loads(gzip.decompress(praw));need(w['start']==n['start'][:222] and w['public']==222,'source interface')
    for k,v in n['frames'].items():need(w['frames'][k]==v,'native frames unchanged')
    for k,f in w['frames'].items():
        if k not in n['frames']:
            need(qrank(f['B'])==f['dim'] and qrank(f['A'])==8-f['dim'],'new frame ranks')
            need(all(dot(b,c)==0 for b in f['B'] for c in f['A']),'new frame annihilator')
    R=[]
    for i in range(111):
        r=tuple(map(Q,n['frames'][str(n['start'][i])]['B'][0]));scale=(2 if dot(r,r)==1 else 1)*(1 if next(x for x in r if x)>0 else -1)
        R.append(tuple(scale*x for x in r))
    need(all(dot(r,r)==4 for r in R),'source normalized roots')
    K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(R)) for i,r in enumerate(R)]
    full=(1<<111)-1;T={15,92};tm=sum(1<<t for t in T)
    A=[K[j]&(K[92] if K[92]>>j&1 else full^K[92]) for j in range(111)]
    B=[1<<j if j in T else A[j]&~tm for j in range(111)]
    ell=K[92]&K[54]
    need(rank(A)==15 and rank(B)==17 and rank(B+[ell])==18 and rank(B+K)==18,'independent code ranks')
    need(rank(B+[ell,K[92]])==18,'actual cache fits enlarged coefficient space')

    # Reconstruct omitted full-E8 roots directly; do not consume the author's covers.
    blocks=sorted({tuple(j for j,x in enumerate(r) if x) for r in R if sum(bool(x) for x in r)==4})
    complete=[tuple(Q(2*int(i==j)) for i in range(8)) for j in range(8)]
    for block in blocks:
        for signs in itertools.product((-1,1),repeat=3):
            r=[Q(0)]*8;r[block[0]]=1
            for j,s in zip(block[1:],signs):r[j]=Q(s)
            complete.append(tuple(r))
    need(len(set(complete))==120 and set(R)<=set(complete),'independent full completion')
    omitted=set(complete)-set(R);covers=[];chi=Counter();newly_punctured=[]
    for j in range(111):
        S=[k for k in range(111) if k!=j and B[j]>>k&1]
        need(B[j]>>j&1 and not(B[j]&~K[j]),'own and forbidden fitting conditions')
        if j in T:need(not S,'completed row');chi[0]+=1;continue
        if K[92]>>j&1:
            normals=[R[92]];charge=0;need(qrank([R[k] for k in S])==6,'one-flat exact support rank')
        else:
            missing=[r for r in omitted if dot(r,R[j])==0 and dot(r,R[92])!=0]
            if missing:z=min(missing)
            else:z=R[15];newly_punctured.append(j)
            if dot(z,R[92])<0:z=tuple(-x for x in z)
            need(dot(z,R[92])==2 and dot(z,R[j])==0,'puncture root conditions')
            normals=[z,tuple(x-y for x,y in zip(z,R[92]))];charge=1
            need(qrank([R[k] for k in S])==7,'two-flat lower bound')
        need(all(qrank([R[j],v])==2 for v in normals),'all cover flats proper')
        need(all(any(dot(R[k],v)==0 for v in normals) for k in S),'independent literal two-flat cover')
        chi[charge]+=1;covers.append(dict(receiver=j,charge=charge,normals=[[str(x) for x in v] for v in normals]))
    need(chi==Counter({0:59,1:52}),'exact total charge52')
    need(newly_punctured==[21,33,45,51,68,76,84,99],'one actual source15 punctures all difficult rows')

    state,counts,moves,peak=replay(w);ground=n['start'][111]
    need(set(state)==set(range(335))|{336,337},'exact live owners')
    masks=[]
    for i in range(111):
        need(state[i]==(n['final'][i],{i}),'all originals restored')
        need(state[222+i]==(n['start'][i],{i}),'all actual stationary point copies')
        preload={i} if i in T else {t for t in T if A[i]>>t&1}
        need(state[111+i]==(n['final'][111+i] if i in T else ground,{111+i}^preload),'exact full-input Y state')
        if i not in T:
            aset={j for j in range(111) if A[i]>>j&1};bset={j for j in range(111) if B[i]>>j&1}
            need(preload^aset^bset^{i}=={i},'conditional decoder identity with original A packet')
            if preload:masks.append(i)
    need(len(masks)==82,'all nonzero Y preloads counted')
    need(state[336]==(ground,{92}) and state[337]==(ground,{15}),'paid ground coordinates')
    C=state[333][0]
    need(state[333][1]=={i for i in range(111) if K[92]>>i&1},'unchanged pure proper cache')
    need(state[334]==(ground,{i for i in range(111) if ell>>i&1}),'unchanged pure ground quadratic')
    need(counts==Counter(INIT=116,ADD=319,MOVE=177,CLEAR=1),'independent prefix operation counts')
    need(moves==Counter({1:31,2:32,5:32,6:27,7:55}) and peak==115,'independent movement and ownership')
    closed_profile=moves+Counter({7:109});need(closed_profile==Counter({1:31,2:32,5:32,6:27,7:164}),'derived closure profile')
    seven=[2,8,9,14,21,46,88]
    need(all(dot(R[i],R[j])!=0 for i,j in itertools.combinations(seven,2)),'matching nonorthogonal7')
    O=[]
    for chart,contents in state.values():
        if any(all(dot(b,R[t])==0 for b in w['frames'][str(chart)]['B']) for t in seven):O.append(sum(1<<i for i in contents))
    targets=[(1<<i)|(1<<(111+i)) for i in seven];rr=rank(O);need(rank(O+targets)-rr==7,'full222-column matching seven deficit')
    out=dict(status='PASS_INDEPENDENT_POINT_PUNCTURE_AND_DECODER_REVIEW',source_sha256=PIN,prefix_sha256=hashlib.sha256(praw).hexdigest(),chi_histogram=dict(chi),ranks=dict(original_code=15,punctured_fitting=17,with_retained_history=18),newly_punctured_receivers=newly_punctured,prefix_counts=dict(counts),prefix_movement=dict(moves),closure_movement=dict(closed_profile),peak_live_owners=peak,matching_cut=dict(receivers=seven,observation_rank=rr,target_augmented_rank=rank(O+targets),deficit=7),wrong_packet_B_leaves_preloads_on=82,independent_covers=covers,new_complete_kappa=False)
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='independent_covers'}))

if __name__=='__main__':main()
