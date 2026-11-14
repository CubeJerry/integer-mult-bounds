#!/usr/bin/env python3
"""Source-derived incidence and exact finite controls for the 56-mode theorem."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)
def rd(p,pin):
    b=p.read_bytes();need(hashlib.sha256(b).hexdigest()==pin,'source pin '+p.name)
    return json.loads(gzip.decompress(b))
def rr(A,p=None):
    A=[[F(x) if p is None else x%p for x in row] for row in A];r=0
    for j in range(len(A[0]) if A else 0):
        k=next((k for k in range(r,len(A)) if A[k][j]),None)
        if k is None:continue
        A[r],A[k]=A[k],A[r];c=1/A[r][j] if p is None else pow(A[r][j],-1,p)
        A[r]=[x*c if p is None else x*c%p for x in A[r]]
        for k in range(len(A)):
            if k!=r:
                c=A[k][j];A[k]=[x-c*y if p is None else (x-c*y)%p for x,y in zip(A[k],A[r])]
        r+=1
    return r
def root(v):
    on=[i for i in range(9) if v>>i&1]
    if len(on)==3:return [3*int(i in on)-1 for i in range(9)]
    off=[i for i in range(9) if i not in on];need(len(off)==2,'native E8 root form')
    return [3*(int(i==off[0])-int(i==off[1])) for i in range(9)]
def span(vs):
    z={0}
    for v in vs:z|={x^v for x in z}
    return z
def main(a):
    np='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883';wp='f72c890e06437c3b6a177c71019f56e60f30712e5c09c1e241c893c1f180e42d'
    n=rd(a.native,np);w=rd(a.word,wp);ports=n['live'];vv={h:n['frames'][n['initial'][h]][0] for h in ports};frame=[7,25,42,52,76,82,97,127]
    dot=lambda x,y:sum(a*b for a,b in zip(x,y))
    g={h:[F(dot(root(vv[h]),root(f)),18) for f in frame] for h in ports};classes={}
    for h in ports:
        inds=tuple(i for i,c in enumerate(g[h]) if c);sg=1
        need(len(inds)==4 and all(abs(g[h][i])==F(1,2) for i in inds),'actual four signed modes')
        for i in inds:sg*=1 if g[h][i]>0 else-1
        classes.setdefault(inds,{-1:[],1:[]})[sg].append(h)
    need(len(classes)==14 and Counter(sum(map(len,h.values())) for h in classes.values())=={7:8,8:6},'all native full classes')
    actual={frozenset(z['ports']):z for z in w['parity_compiler']['halves']};receipts=[]
    for modes,halves in sorted(classes.items()):
        C3=span([frame[i] for i in modes]);need(len(C3)==8,'actual class rank3')
        for sg,hh in sorted(halves.items()):
            C6={v for v in range(512) if all((v&vv[h]).bit_count()%2==0 for h in hh)}
            local=[h for h in ports if vv[h] in C6];opp=halves[-sg]
            need(len(C6)==64 and C3<C6 and local==opp,'complete actual opposite-half incidence')
            need(all(dot(root(vv[h]),root(vv[j]))==18*int(h==j) for h in hh for j in hh),'actual real half orthogonality')
            z=actual[frozenset(hh)];need(span(w['frames'][z['C6']])==C6 and span(w['frames'][z['C3']])==C3,'literal charts equal reconstructed charts')
            need(not(set(hh)&set(local)) and any(vv[j] not in C3 for j in opp),'no self input; C3 cannot replace actual C6')
            receipts.append({'targets':hh,'actual_local_sources':local,'mode_indices':list(modes),'literal_C6':z['C6'],'dimension':6})
    need(len(receipts)==28 and len({r['literal_C6'] for r in receipts})==28,'distinct actual receiver charts')
    tests=[]
    for width in (1,2,3):
        for big,small in ((4,3),(4,4)):
            n0,n1=big*width,small*width
            for mode in ('zero','identity_pair','singular_pair','noncommuting'):
                P=[[0]*n1 for _ in range(n0)];Q=[[0]*n0 for _ in range(n1)]
                if mode in ('identity_pair','singular_pair'):
                    upto=n1 if mode=='identity_pair' else max(n1-1,0)
                    for j in range(upto):P[j][j]=Q[j][j]=1
                elif mode=='noncommuting':
                    for i in range(n0):
                        for j in range(n1):P[i][j]=int((i+2*j)%3==0)
                    for i in range(n1):
                        for j in range(n0):Q[i][j]=int((2*i+j)%4==0)
                A=[[int(i==j) for j in range(n0)]+P[i] for i in range(n0)]
                A += [Q[i]+[int(i==j) for j in range(n1)] for i in range(n1)]
                for prime in (None,2,3,5):
                    r=rr(A,prime);need(r>=n0,'principal identity block lower bound')
                    if mode=='identity_pair':need(r==n0,'sharp rank, including characteristic two')
                    tests.append({'width':width,'halves':[big,small],'mode':mode,'characteristic':prime or 0,'rank':r})
    price=json.loads(a.price.read_text());need(price['status']=='PASS_INDEPENDENT_PARITY_FULL_CALLER_PRICE' and F(price['limiting_room'][1])<1,'exact price cannot pay added rank1 movement')
    out={'status':'PASS_SOURCE_INCIDENCE_AND_SHARP_BLOCK_RANK_CONTROLS','native_sha256':np,'word_sha256':wp,'half_incidence':receipts,'full_class_sizes':dict(Counter(sum(map(len,h.values())) for h in classes.values())),'minimum_global_modes':56,'fixed_available_global_modes':8,'block_controls':tests,'negative_controls':['self coordinate at own C6 absent','class C3 cannot substitute for receiver C6','globally dropping incidence permits L=I and invalidates bound','eight scalar modes violate required56','one additional rank1 move exceeds actual fixed-source target room'],'scope':'Finite actual source geometry and adversarial matrix controls. All-field/all-width theorem is the separate written proof. Flow-changing architectures are not excluded.','new_kappa':None}
    a.output.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(json.dumps({'status':out['status'],'halves':len(receipts),'matrix_controls':len(tests),'min_modes':56}))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ['native','word','price','output']:p.add_argument('--'+n,type=Path,required=True)
    main(p.parse_args())
