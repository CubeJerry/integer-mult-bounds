"""Independent row-kernel static-cut audit; no author imports."""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from pathlib import Path
import argparse,gzip,hashlib,json
def need(b,s):
    if not b:raise ValueError(s)
def add(a,b,c):
    for j,z in b.items():
        z=a.get(j,0)+c*z
        if z:a[j]=z
        else:a.pop(j,None)
def pivots(rows):
    p={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j not in p:p[j]=x;break
            x^=p[j]
    return p
def included(a,b):return len(pivots(a+b))==len(b)
def pure(rows,roles,G):
    # Row-image elimination, unlike the author's transposed constraints.
    pivot={};out=[]
    for r in sorted(roles,reverse=True):
        v={j:z for j,z in rows[r].items() if j not in G};c={r:Q(1)}
        while v:
            j=max(v)
            if j not in pivot:
                z=v[j];pivot[j]=({k:x/z for k,x in v.items()},{k:x/z for k,x in c.items()});break
            w,d=pivot[j];z=-v[j];add(v,w,z);add(c,d,z)
        if not v:
            image={}
            for i,z in c.items():add(image,rows[i],z)
            need(set(image)<=G,'pure image support');out.append((c,image))
    return out
def main(path):
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    need(sha=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','source SHA')
    need(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()=='74563a7867d9d762b6588f65362369668841bb3e','source blob')
    w=json.loads(gzip.decompress(raw));n=w['public'];N=n+w['owned_fields'];ff=w['frames'];events=w['program']
    need(all(all(type(x) is int and 0<x<512 for x in f) and len(pivots(f))==len(f) for f in ff),'all independent GF2^9 frames')
    relevant=[i for i,f in enumerate(ff) if len(f) in (3,6)]
    need(not any(included(ff[a],ff[b]) and len(ff[a])==len(ff[b]) for j,a in enumerate(relevant) for b in relevant[j+1:]),'no relevant chart aliases')
    G={i for i in range(n) if w['initial'][i]==3 and w['final'][i]==127};need(len(G)==595,'exact current group')
    state=list(w['initial'])+[None]*(N-n);at=defaultdict(set)
    for i,f in enumerate(state):
        if f is not None:at[f].add(i)
    need(all(not(G&at[f]) for f in relevant),'initial cuts have no G inputs')
    rows=[{i:Q(1)} if i<n else {} for i in range(N)];snap=defaultdict(list);counts=Counter();total=0
    for t,e in enumerate(events):
        op,r=e[:2]
        if op=='MOVE':
            u,v=e[2:4];need(state[r]==u and (included(ff[u],ff[v]) or included(ff[v],ff[u])),'nested MOVE')
            at[u].remove(r);at[v].add(r);state[r]=v;touched={u,v}
        elif op=='INIT':
            need(r>=n and state[r] is None,'owned INIT');state[r]=e[2];at[e[2]].add(r);rows[r]={};touched={e[2]}
        elif op=='CLEAR':
            need(r>=n and state[r]==e[2],'owned CLEAR');touched={e[2]};at[e[2]].remove(r);state[r]=None;rows[r]={}
        elif op=='SCALE':
            need(state[r]==e[-1],'SCALE chart');rows[r]={j:Q(e[-2])*z for j,z in rows[r].items() if Q(e[-2])*z};touched={state[r]}
        elif op in ('ADD','COPY'):
            need(state[r]==state[e[2]]==e[-1],'contact chart')
            if op=='COPY':need(not rows[r],'COPY zero destination')
            add(rows[r],rows[e[2]],Q(e[-2]));touched={state[r]}
        else:raise ValueError(op)
        for f in sorted(touched):
            if len(ff[f]) not in (3,6) or not at[f]:continue
            roles=sorted(at[f]);A=pure(rows,roles,G);total+=1
            if any(img for c,img in A):snap[t].append((f,roles,A))
            else:counts['no_pure_prefix']+=1
    need(state==w['final']+[None]*(N-n),'all source final frames')
    need(all(rows[r]=={r:Q(1)} for r in G),'all595 group identities')
    need(all(not rows[r] for r in range(n,N)),'owned final zero')
    cols=[{i:Q(1)} if i<n else {} for i in range(N)];classes=[]
    for t in range(len(events)-1,-1,-1):
        for f,roles,A in snap[t]:
            B=pure(cols,roles,G)
            if not any(img for c,img in B):kind='no_pure_suffix'
            else:
                need(all(sum(x*b.get(i,0) for i,x in a.items())==0 for a,c in A for b,d in B),'nonzero local pairing')
                kind='zero_local_pairing'
            counts[kind]+=1;classes.append({'cut_after':t,'frame':f,'roles':roles,'rank':len(ff[f]),'prefix_dimension':len(A),'suffix_dimension':len(B),'kind':kind})
        e=events[t];op,r=e[:2]
        if op in ('INIT','CLEAR'):cols[r]={}
        elif op=='SCALE':cols[r]={j:Q(e[-2])*z for j,z in cols[r].items() if Q(e[-2])*z}
        elif op in ('ADD','COPY'):add(cols[e[2]],cols[r],Q(e[-2]))
    need(total==4657 and dict(counts)=={'no_pure_prefix':4496,'no_pure_suffix':136,'zero_local_pairing':25},'complete static census')
    A=pure([{0:Q(1)}],[0],{0})
    need(A==[({0:Q(1)},{0:Q(1)})] and sum(x*x for x in A[0][0].values())==1,'positive cut survives')
    Z=pure([{},{}],[0,1],{0});need(len(Z)==2 and not any(v for c,v in Z),'zero-image directions retained')
    C=pure([{0:Q(1),2:Q(2)},{1:Q(1),2:Q(4)}],[0,1],{0,1})
    need(len(C)==1 and C[0][1] and not(2 in C[0][1]),'outside cancellation')
    return {'status':'PASS_INDEPENDENT_STATIC_3_6_REVIEW','source_sha256':sha,'frame_count':len(ff),
      'relevant_frames_without_aliases':len(relevant),'events':len(events),'classes_count':total,'counts':dict(counts),
      'classes':sorted(classes,key=lambda c:(c['cut_after'],c['frame'])),
      'controls':['positive cut survives','zero image coefficients retained','outside cancellation'],
      'no_new_kappa':True,'scope':'All existing rank3/6 source frames; all coframed roles; fixed scalar order;595 current rank9 boundary group.'}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);a=p.parse_args()
    print(json.dumps(main(a.source),indent=2))
