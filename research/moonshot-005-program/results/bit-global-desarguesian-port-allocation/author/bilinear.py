#!/usr/bin/env python3
"""Seven alternating forms construct the marking and one global GF64 node map."""
import argparse,gzip,hashlib,importlib.util,json
from collections import Counter,defaultdict
from pathlib import Path
FORMS=[138420225,16418,16777284,131088,33587328,135406080,67637248]
PAIRS=[(i,j)for i in range(8)for j in range(i+1,8)]
def need(x,s):
    if not x:raise ValueError(s)
def xor(xs):
    z=0
    for x in xs:z^=x
    return z
def wedge(x,y):return sum(((((x>>i)&1)*((y>>j)&1))^(((x>>j)&1)*((y>>i)&1)))<<p for p,(i,j)in enumerate(PAIRS))
def C(x,y):
    w=wedge(x,y);return sum(((w&f).bit_count()%2)<<p for p,f in enumerate(FORMS))
def Q(u):return (((u>>1)&1)*((u>>3)&1))^(((u>>2)&1)*((u>>4)&1))^((u&1)*((u>>5)&1))
def mul(x,y):
    z=0
    while y:
        if y&1:z^=x
        y>>=1;x<<=1
        if x&64:x^=67
    return z
def power(x,n):
    z=1
    while n:
        if n&1:z=mul(z,x)
        x=mul(x,x);n>>=1
    return z
def qfield(x):return power(x,9)^power(x,18)^power(x,36)
def witt(q):
    space=set(range(64));basis=[];b=lambda x,y:q(x^y)^q(x)^q(y)
    while len(space)>1:
        zeros=sorted(x for x in space if x and not q(x))
        if zeros:e=zeros[0];f=next(x for x in zeros if b(e,x))
        else:e=min(space-{0});f=min(space-{0,e})
        basis.extend([e,f]);space={x for x in space if not b(x,e)and not b(x,f)}
    return basis
def module(path,name):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    package=Path(__file__).resolve().parents[1];base=a.repo/'research/moonshot-005-program/results'
    for p,h in json.loads((package/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((a.repo/p).read_bytes()).hexdigest()==h,'pin '+p)
    G=module(base/'bit-orthogonal-spread-port-allocation/review/check.py','bilinear_geometry');A=module(package/'author/check.py','bilinear_helpers')
    L=json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()));B=json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text());cols=B['lattice_basis_columns'];inv=G.inv([[cols[j][i]for j in range(8)]for i in range(8)])
    change={xor(B['hyperbolic_basis_masks'][k]for k in range(8)if x>>k&1):x for x in range(256)};roots=[]
    for root in L['root_table']:
        cs=[sum(x*y for x,y in zip(row,root))for row in inv];need(all(x.denominator==1 for x in cs),'integer root');roots.append(change[sum((int(x)&1)<<k for k,x in enumerate(cs))])
    need(len(A.independent(FORMS))==7,'independent forms');rank_hist=Counter();identities=0
    for x in range(256):
        for y in range(256):need((C(x,y)&1)==G.polar(x,y),'first coordinate is polar form')
        if not x:continue
        rank=len(A.independent(C(x,1<<p)for p in range(8)));rank_hist[G.q(x),rank]+=1;need(rank==(7 if G.q(x)else 4),'all contraction ranks')
        if G.q(x):
            for y in range(256):
                if G.polar(x,y):need(G.q(y)==Q(C(x,y)>>1),'common affine quadratic identity');identities+=1
    chosen={c for c in range(1,128,2)if Q(c>>1)};c0=min(chosen);q6=lambda x:1^Q((c0>>1)^x)
    source_basis,target_basis=witt(q6),witt(qfield);theta={xor(source_basis[p]for p in range(6)if m>>p&1):xor(target_basis[p]for p in range(6)if m>>p&1)for m in range(64)}
    need(len(theta)==64 and all(q6(x)==qfield(theta[x])for x in range(64)),'one global GF64 quadratic isometry')
    H=[set(ids)for ids in L['A2']];D=[set(ids)for ids in L['D4']];labels=[];nodes=[]
    for ids in H:
        hs=[roots[j]for j in ids];c=C(hs[0],hs[1]);need(c in chosen and all(C(x,y)==c for x in hs for y in hs if x!=y),'shared H label');labels.append(c);nodes.append(theta[(c^c0)>>1])
    need(Counter(labels)==Counter({c:40 for c in chosen}),'28 parallel classes of40 H')
    stars=[[h for h,ids in enumerate(H)if j in ids]for j in range(120)];need(all(len(s)==28 and {labels[h]for h in s}==chosen for s in stars),'bijective source stars')
    adj=[{j for j,y in enumerate(roots)if j!=i and not G.polar(x,y)}for i,x in enumerate(roots)];fq=[qfield(x)for x in range(64)];fb=[[fq[x^y]^fq[x]^fq[y]for y in range(64)]for x in range(64)]
    views=native=0;parameters={}
    for j,x in enumerate(roots):
        parameters[str(j)]={}
        for i in adj[j]:
            v=theta[C(x,roots[i])>>1];need(v!=0,'nonzero receiver parameter');parameters[str(j)][str(i)]=v
            expected={h for h in stars[j]if fb[v][nodes[h]]==(1^fq[v])};actual={h for h in stars[j]if H[h]<=adj[i]}
            need(expected==actual and len(actual)==16,'actual view equals field block');views+=1;native+=int(i<111 and j<111)
    W=json.loads(gzip.decompress((package/'author/WITNESS.json.gz').read_bytes()));selected=set(W['selected_D']);derived=[];triples=0;bylabel=defaultdict(set)
    for d,ids in enumerate(D):
        V=G.span(roots[j]for j in ids);rad={x for x in V if all(not G.polar(x,y)for y in V)};u,v=sorted(rad-{0})[:2]
        if not C(u,v):derived.append(d)
    need(set(derived)==selected,'bilinear zero rule gives exact630 D')
    for h,ids in enumerate(H):
        aa,bb,cc=sorted(ids);hp={x for x in range(256)if all(not G.polar(x,roots[j])for j in ids)};left={C(roots[aa],x)>>1:x for x in hp};need(len(left)==64,'perpendicular contraction bijection')
        J={x:left[C(roots[bb],x)>>1]for x in hp};s=W['local_structures'][h];basis=s['coordinate_basis'];coord={xor(basis[p]for p in range(6)if t>>p&1):t for t in range(64)};back={v:k for k,v in coord.items()};fixed={x:back[A.apply(s['J'],coord[x])]for x in hp}
        need(J==fixed or J=={x:fixed[fixed[x]]for x in hp},'derive local field operator from C')
        target=[C(roots[bb],left[1<<p])>>1 for p in range(6)];square=[xor(target[p]for p in range(6)if y>>p&1)for y in target];bylabel[labels[h]].add(min(tuple(target),tuple(square)))
        for i in range(120):
            if roots[i]not in hp:continue
            vs=[parameters[str(j)][str(i)]for j in ids];need(len(set(vs))==3 and xor(vs)==0,'three receiver parameters sum to zero');triples+=1
    need(views==7560 and native==6470 and triples==40320,'all finite quantifiers')
    result={'status':'PASS_GLOBAL_BILINEAR_MARKING_AND_SHARED_NODES','alternating_forms':FORMS,'contraction_rank_histogram':[[q,r,n]for(q,r),n in sorted(rank_hist.items())],'common_quadratic_identities':identities,'shared_node_labels':28,'H_per_label':40,'source_stars':120,'geometric_source_views':views,'native_source_views':native,'receiver_parameter_triples':triples,'bilinear_selected_D':len(derived),'derived_local_F4_structures':1120,'distinct_target_J_per_label_histogram':dict(Counter(len(s)for s in bylabel.values())),'new_complete_kappa':False,'common_H_word':False}
    (a.out/'BILINEAR-RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.out/'GLOBAL-NODES.json').write_text(json.dumps({'coset_base':c0,'source_Witt_basis':source_basis,'field_Witt_basis':target_basis,'theta':theta,'H_labels':labels,'H_nodes':nodes,'receiver_parameters':parameters},separators=(',',':'))+'\n');print(result['status'],28,7560,6470,40320,flush=True);print('J_PER_LABEL',result['distinct_target_J_per_label_histogram'],flush=True)
if __name__=='__main__':main()
