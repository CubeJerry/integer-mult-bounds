#!/usr/bin/env python3
"""Construct Gray-controlled words and literal fixed-table permutation recipes."""
import argparse, hashlib, itertools, json, random
from collections import Counter
from fractions import Fraction
from pathlib import Path


def gray(g):
    vertices=[j^(j>>1)for j in range(1<<g)]
    edges=[]
    for a,b in zip(vertices,vertices[1:]+[0]):
        x=a^b;assert x and x&(x-1)==0
        k=x.bit_length()-1;edges.append((k,1 if b>>k&1 else -1))
    assert len(set(vertices))==1<<g and vertices[0]==0
    return vertices,edges


def modular(g,f,K,G,rho):
    n=f-1;B=1<<G;js=[rho+i*K for i in range(n)]
    us=[f'u{k}'for k in range(g)];xs=[f'x{k}'for k in range(g)]
    def dig(s,v,i):return(s[v]>>(i*G))&(B-1)
    def bit(s,i):return int(all(dig(s,u,i)&1 for u in us))
    def pack(s,v):return sum(((s[v]>>j)&1)<<(i*G)for i,j in enumerate(js))
    ops=[]
    def sw(a,b):ops.append(('swap',a,b))
    def rt(v,ctrl,fun):ops.append(('rotate',v,tuple(ctrl),fun))
    def toggle():
        rt('y',us+['t'],lambda s:sum(2*bit(s,i)*dig(s,'t',i)*(1<<j)for i,j in enumerate(js)))
        sw('t','b');rt('b',['y'],lambda s:pack(s,'y'));sw('t','b')
        rt('y',us+['t'],lambda s:sum(bit(s,i)*(1-2*dig(s,'t',i))*(1<<j)for i,j in enumerate(js)))
        sw('t','b');rt('b',us+['y'],lambda s:-sum((((s['y']>>j)&1)^bit(s,i))<<(i*G)for i,j in enumerate(js)));sw('t','b')
    for k,sign in gray(g)[1]:
        toggle();sw(us[k],'b')
        rt('b',[xs[k]],lambda s,k=k,sign=sign:sign*pack(s,xs[k]));sw(us[k],'b')
    sizes={v:n*G for v in us+['t','b']}|{v:f*K for v in xs+['y']}
    def run(s,inv=False):
        s=s.copy()
        for o in (reversed(ops)if inv else ops):
            if o[0]=='swap':s[o[1]],s[o[2]]=s[o[2]],s[o[1]]
            else:s[o[1]]=(s[o[1]]+(-1 if inv else 1)*o[3](s))% (1<<sizes[o[1]])
        return s
    def ideal(s):
        s=s.copy()
        for j in js:s['y']^=int(all(s[x]>>j&1 for x in xs))<<j
        return s
    def bad(s):
        return any(dig(s,v,i)==B-1 for v in us+['t']for i in range(n))or any(not 2*B<=((s['y']>>j)&((1<<K)-1))//2<(1<<(K-1))-2*B for j in js)
    # Every active slot may be arbitrarily ordered: only its position before
    # b is used in loads; target rotations use front fields exclusively.
    for targetpos in range(g+1):
        active=xs.copy();active.insert(targetpos,'y');order=us+['t']+active+['b']
        for o in ops:
            if o[0]=='rotate':assert all(order.index(v)<order.index(o[1])for v in o[2])
    count=Counter(o[0]for o in ops)
    assert count=={'swap':6*(1<<g),'rotate':5*(1<<g)}
    return sizes,run,ideal,bad


def edge_path(a,b):
    out=[];x=a
    for k in range((a^b).bit_length()):
        if(a^b)>>k&1:
            y=x^(1<<k);out.append((x,y));x=y
    assert x==b and out
    return out+out[-2::-1]


def decompose(perm):
    seen=set();edges=[]
    for start in range(len(perm)):
        if start in seen:continue
        cycle=[];x=start
        while x not in seen:
            seen.add(x);cycle.append(x);x=perm[x]
        assert x==start
        for x in cycle[1:]:edges.extend(edge_path(start,x))
    return edges


def lower(edges,h):
    word=[]
    for a,b in edges:
        delta=a^b;assert delta and delta&(delta-1)==0
        k=delta.bit_length()-1;mask=((1<<h)-1)^(1<<k)
        zeros=[j for j in range(h)if j!=k and not(a>>j&1)]
        word.extend(('N',j,0)for j in zeros)
        word.append(('C',k,mask))
        word.extend(('N',j,0)for j in reversed(zeros))
    return word


def evaluate(word,x):
    for op,k,mask in word:
        if op=='N'or x&mask==mask:x^=1<<k
    return x


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();here=Path(__file__).resolve().parent
    dep=json.loads((here/'DEPENDENCIES.json').read_text())
    for row in dep['canonical_sources']+[dep['toffoli_proof']]:
        assert hashlib.sha256((here/row['retained_copy']).read_bytes()).hexdigest()==row['sha256']
    gray_cases=omission=closedge=0
    for g in range(1,7):
        vs,es=gray(g);full=(1<<g)-1
        for u,x in itertools.product(range(1<<g),repeat=2):
            got=0
            for v in vs:got^=int((u^(v&x))==full)
            assert got==int(x==full);gray_cases+=1
        for missing in vs:
            u=full^missing;x=full
            got=0
            for v in vs:
                if v!=missing:got^=int((u^(v&x))==full)
            assert got!=1;omission+=1
        for x in range(1<<g):
            state=[3]*(g)
            for k,sign in es:state[k]+=sign*((x>>k)&1)
            assert state==[3]*g
        k,_=es[-1];state=[3]*g
        for k1,sign in es[:-1]:state[k1]+=sign*int(k1==k)
        assert state!=[3]*g;closedge+=1
    rng=random.Random(0xC005);modcases=modgood=modbad_diff=0
    for g in range(1,6):
        f,K,G,rho=3,7,2,6
        sizes,run,ideal,bad=modular(g,f,K,G,rho)
        for sample in range(1024):
            s={v:rng.randrange(1<<w)for v,w in sizes.items()}
            if sample%2==0:
                for v in [f'u{k}'for k in range(g)]+['t']:s[v]=sum(rng.randrange(3)<<(i*G)for i in range(f-1))
                for i in range(f-1):
                    j=rho+i*K;seg=2*rng.randrange(8,56)+rng.randrange(2)
                    s['y']=(s['y']&~(127<<j))|(seg<<j)
            got=run(s);want=ideal(s)
            assert run(got,True)==s and bad(got)==bad(s)
            if not bad(s):assert got==want;modgood+=1
            else:modbad_diff+=got!=want;assert ideal(run(got,True))==want
            modcases+=1
    permutations=0;maxedges=0;maxtranslations=0
    for perm in itertools.permutations(range(8)):
        edges=decompose(perm);word=lower(edges,3)
        assert len(edges)<=35
        assert tuple(evaluate(word,x)for x in range(8))==perm
        assert all(evaluate(list(reversed(word)),perm[x])==x for x in range(8))
        permutations+=1;maxedges=max(maxedges,len(edges));maxtranslations=max(maxtranslations,sum(op=='N'for op,_,_ in word))
    # Four-bit coverage exhausts every arbitrary transposition, then samples
    # full permutations. The general theorem is proved by cycle decomposition.
    transpositions=0
    for a1,b in itertools.combinations(range(16),2):
        word=lower(edge_path(a1,b),4)
        assert all(evaluate(word,x)==(b if x==a1 else a1 if x==b else x)for x in range(16));transpositions+=1
    for _ in range(256):
        perm=list(range(16));rng.shuffle(perm);word=lower(decompose(perm),4)
        assert [evaluate(word,x)for x in range(16)]==perm
    # Negative controls independently check both path returns and pattern
    # translations, which a pure adjacency-table check could miss.
    badpath=edge_path(0,7)[:3]
    assert [evaluate(lower(badpath,3),x)for x in range(8)]!=[7,1,2,3,4,5,6,0]
    stripped=[o for o in lower([(0,1)],3)if o[0]!='N']
    assert [evaluate(stripped,x)for x in range(8)]!=[1,0,2,3,4,5,6,7]
    phasecases=phasebadabs=phasebadinverse=0
    perm=[1,2,0,4,3,7,5,6];inv=[perm.index(x)for x in range(8)];q=[0,1,3,2,1,2,0,3];absolute=1
    for f in range(1,5):
        for x in itertools.product(range(8),repeat=f):
            y=tuple(perm[z]for z in x);ph=(absolute*f+sum(q[z]for z in x))%4
            iph=(-absolute*f-sum(q[inv[z]]for z in y))%4
            assert (ph+iph)%4==0 and tuple(inv[z]for z in y)==x
            phasebadabs+=(absolute+sum(q[z]for z in x))%4!=ph
            phasebadinverse+=(ph-absolute*f-sum(q[z]for z in y))%4!=0
            phasecases+=1
    assert phasebadabs and phasebadinverse and modbad_diff
    guardcases=0
    for g in range(1,9):
        for p in range(2,130):
            ell=(p-1).bit_length();G=4*ell+6;K=G+4*ell+10
            bound=Fraction(p*((g+1)*(1<<K)+8*(1<<(2*G))),1<<(G+K))
            assert bound<=Fraction(2*g+3,128*p**3);guardcases+=1
    out={'status':'PASS_FIXED_MONOMIAL_COMPACT_BRIDGE','gray_identity_cases':gray_cases,
         'missing_vertex_controls':omission,'missing_closing_edge_controls':closedge,
         'modular_cases':modcases,'modular_good_cases':modgood,'modular_bad_cases_differing':modbad_diff,
         'all_three_bit_permutations':permutations,'max_observed_h3_edge_gates':maxedges,
         'max_observed_h3_negative_control_translations':maxtranslations,
         'all_four_bit_transpositions':transpositions,'four_bit_full_permutation_samples':256,
         'phase_inverse_cases':phasecases,'unlifted_absolute_phase_rejected':phasebadabs,
         'wrong_inverse_phase_index_rejected':phasebadinverse,'exact_guard_cases':guardcases,
         'proof_sha256':hashlib.sha256((here/'PROOF.md').read_bytes()).hexdigest(),
         'scope':'Finite checks corroborate universal fixed-g/fixed-table conditional theorem; no growing-table claim and no new kappa'}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

if __name__=='__main__':main()
