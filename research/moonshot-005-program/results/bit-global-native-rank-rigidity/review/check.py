"""Independent edge-wise exterior-clique closure and disjoint pivot witnesses."""
import argparse
from collections import Counter
from copy import deepcopy
import gzip
import hashlib
import json
from pathlib import Path
import random


def need(x,label):
    if not x:raise ValueError(label)


def determinant(mat):
    a=[list(row) for row in mat];n=len(a);sg=prev=1
    for i in range(n-1):
        u=next((u for u in range(i,n) if a[u][i]),None)
        if u is None:return 0
        if i!=u:a[i],a[u]=a[u],a[i];sg=-sg
        z=a[i][i]
        for j in range(i+1,n):
            for k in range(i+1,n):
                val=a[j][k]*z-a[j][i]*a[i][k];need(val%prev==0,'integer Bareiss divisibility');a[j][k]=val//prev
        prev=z
    return sg*a[-1][-1]


def source(repo):
    p=repo/'research/moonshot-005-program/results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';data=gzip.decompress(p.read_bytes())
    need(hashlib.sha256(data).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','original root source')
    roots=json.loads(data)['root_table'][:111];return [[int(sum(u*v for u,v in zip(a,b))==0) for b in roots] for a in roots]


def closure(g,cert):
    tree=[tuple(e) for e in cert['tree']];native={(i,j) for i,row in enumerate(g) for j,bit in enumerate(row) if bit};vertices=222
    adjacency=[set() for _ in range(vertices)]
    for i,j in tree:adjacency[i].add(111+j);adjacency[111+j].add(i)
    reached={0};todo=[0]
    while todo:
        for v in adjacency[todo.pop()]-reached:reached.add(v);todo.append(v)
    need(len(tree)==len(set(tree))==221 and set(tree)<=native and len(reached)==vertices,'spanning bipartite native tree')
    weights={e:0 for e in tree};pos=0;anchor_set=set();degree=Counter()
    for count in cert['layers']:
        old=dict(weights)
        for target,r,s,c,d,anchors in cert['forced'][pos:pos+count]:
            edge=divmod(target,111);corners={(r,c),(r,d),(s,c),(s,d)}
            need(len(corners)==4 and corners<=native and len({r,s,c,d})==4,'genuine disjoint row/column rectangle')
            need(corners-set(old)=={edge} and edge not in weights,'three corners from earlier certified levels')
            need(len(anchors)==len(set(anchors))==8 and not set(anchors).intersection({r,s,c,d}),'eight separate exterior diagonal roles')
            need(all(not g[x][y] for x in anchors for y in anchors),'native own diagonal scaffold')
            for x,y in corners:need(all(not(g[x][p] and g[p][y]) for p in anchors),'no nonzero two-step Schur entry')
            w=1+sum(old[e] for e in corners if e!=edge);weights[edge]=w;degree[w]+=1;anchor_set.add(tuple(sorted(anchors)))
        pos+=count
    need(pos==len(cert['forced']) and set(weights)==native and max(weights.values())<=4,'entire physical support closure')
    return weights,{'native_edges':len(native),'tree_edges':len(tree),'layer_sizes':cert['layers'],'actual_path_error_weight_histogram':dict(degree),'distinct_used_8cliques':len(anchor_set)}


def independent_first(masks,domain):
    piv={};which=[]
    for i in domain:
        x=masks[i]
        while x:
            p=x.bit_length()-1
            if p not in piv:piv[p]=x;which.append(i);break
            x^=piv[p]
    return which


def pivots(g,weight):
    K=[sum((v^(i==j))<<j for j,v in enumerate(row)) for i,row in enumerate(g)];result={};gen=random.Random(271890)
    for i in range(111):
        other=[p for p in range(111) if p!=i]
        for _ in range(150):
            gen.shuffle(other);R=independent_first(K,other)
            rest=[j for j in other if j not in R];cols=[sum(g[r][j]<<s for s,r in enumerate(R)) for j in range(111)]
            C=independent_first(cols,rest)
            if len(R)==len(C)==9:break
        else:raise ValueError('native disjoint nine pivot')
        matrix=[[g[x][y] for y in C] for x in R];p=determinant(matrix)
        full=[[g[x][y] if x!=y else 1 for y in C+[i]] for x in R+[i]]
        need(len(set(R+C+[i]))==19 and p%2 and determinant(full)%2==0,'actual char-two bordered pivot')
        cost=sum(weight.get((x,y),0) for x in R+[i] for y in C+[i] if x!=y)
        result[i]={'rows':R,'columns':C,'signed_9det':p,'signed_10det':determinant(full),'perturbation_weight':cost}
    return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--closure',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    g=source(a.repo);raw=a.closure.read_bytes();c=json.loads(raw);wt,stats=closure(g,c);sr=random.Random(129);odd=None
    for it in range(2048):
        vs=sr.sample(range(111),20);R,C=vs[:10],vs[10:];det=determinant([[g[x][y] for y in C] for x in R])
        if abs(det)==2:odd={'rows':R,'columns':C,'determinant':det,'support_weight':sum(wt.get((x,y),0) for x in R for y in C)};break
    need(odd is not None,'all odd characteristic exclusion')
    fault={}
    wrong=deepcopy(c);wrong['forced'][0][-1][0]=wrong['forced'][0][1]
    try:closure(g,wrong)
    except ValueError as e:fault['nonexterior_anchor']=str(e)
    wrong=deepcopy(c);wrong['forced'][0],wrong['forced'][-1]=wrong['forced'][-1],wrong['forced'][0]
    try:closure(g,wrong)
    except ValueError as e:fault['wrong_layer']=str(e)
    need(len(fault)==2,'specific negative controls')
    rr=pivots(g,wt);out={'closure_file_sha256':hashlib.sha256(raw).hexdigest(),'closure':stats,'bordered_nine_pivots_for_all_roles':rr,'odd_characteristic_witness':odd,'faults':fault}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(stats,odd,fault)


if __name__=='__main__':main()
