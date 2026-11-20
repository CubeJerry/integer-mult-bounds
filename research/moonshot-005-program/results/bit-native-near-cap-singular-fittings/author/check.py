"""Compile two concentrated and one all-edge bank-3840 near-canonical fitting."""
from collections import Counter
import argparse,gzip,json
from hashlib import sha256
from math import ceil
from pathlib import Path


def need(ok,label):
    if not ok:raise ValueError(label)

def gf2_rank(rows):
    b={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in b:x^=b[j]
            else:b[j]=x;break
    return len(b)

def atom(w,g):
    b=w['bank'];pair=w['erased_reciprocal_pair'];n=111;covered=[0]*n;cost=0;included=[[0]*n for i in range(n)]
    for spec in w['words']:
        S=spec['owners'];need(len(set(S)&set(pair))<=1,'removed reciprocal pair');kind=spec['kind']
        for _ in range(spec['multiplicity']):
            keep=[i for i in S if covered[i]<b];m=sum(1<<i for i in keep);rows=[]
            for i in keep:
                covered[i]+=1;allowed=g[i]|1<<i;row=m if kind=='clique' else m&allowed
                need(row>>i&1 and not row&~allowed,'true native sparse own row');rows.append(row)
                for j in keep:
                    if row>>j&1:included[i][j]+=1
            cost+=gf2_rank(rows)
    need(covered==[b]*n,'complete atomic bank');return cost,included

def concentrated(w,g,main,slack):
    b=w['bank'];q,mat=atom(w,g);r,j=w['erased_reciprocal_pair'];z=q-9*b;copies,spare=divmod(slack,z);pure_left=main-copies*b-spare
    need(pure_left>=0,'real native bank dimensions');K=[mask|1<<i for i,mask in enumerate(g)];altered=K.copy();altered[r]^=1<<j;need(gf2_rank(K)==9 and gf2_rank(altered)==10,'literal scalar canonical and single-arc ranks')
    finalrank=copies*q+pure_left*9+spare*10;dist=Counter();reverse=None
    for i in range(111):
        for s in range(111):
            if not g[i]>>s&1:continue
            h=copies*mat[i][s]+pure_left+spare*int((i,s)!=(r,j));dist[main-h]+=1
            if (i,s)==(j,r):reverse=main-h
    return {'erased_two_way_atomic_pair':[r,j],'atomic_bank':b,'atomic_rank':q,'atom_copies':copies,'canonical_original_coordinates':pure_left,'additional_directed_scalar_erasures':spare,'true_return_rank':finalrank,'bank':main,'target_directed_corank':copies*b+spare,'reverse_corank':reverse,'native_corank_histogram':dict(dist)}

def broad(parts,g,main):
    n=111;counts=Counter();ranks=[]
    for groups in parts:
        need(sorted(k for S in groups for k in S)==list(range(n)) and len(groups)==15,'actual fifteen independent owner sums')
        for S in groups:
            m=sum(1<<i for i in S)
            for i in S:
                need(not m&~(g[i]|1<<i),'native proper clique')
                for j in S:
                    if j!=i:counts[i,j]+=1
        ranks.append(len(groups))
    h=Counter(len(parts)-counts[i,j] for i in range(n) for j in range(n) if g[i]>>j&1);need(sum(h.values())==6470,'every true directed block counted');q=(main-len(parts))*9+sum(ranks)
    return {'bank':main,'canonical_original_coordinates':main-len(parts),'native_15_clique_grades':len(parts),'true_return_rank':q,'native_corank_histogram':dict(sorted(h.items())),'all_6470_proper_blocks_have_corank_at_least':min(h),'maximum_proper_corank':max(h)}

def main():
    here=Path(__file__).resolve().parent;p=argparse.ArgumentParser();p.add_argument('--layout',type=Path,default=here.parent.parent/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');p.add_argument('--data',type=Path,default=here/'output');p.add_argument('--out',type=Path,default=here/'output');a=p.parse_args();raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','published native root layout');v=json.loads(raw)['root_table'][:111];g=[sum(1<<j for j,b in enumerate(v) if sum(u*w for u,w in zip(r,b))==0) for r in v]
    special=concentrated(json.loads((a.data/'BANK13.json').read_bytes()),g,3840,128);regular=concentrated(json.loads((a.data/'BANK29.json').read_bytes()),g,3840,128);flat=broad(json.loads((a.data/'PARTITIONS.json').read_bytes()),g,3840)
    out={'concentrated_exceptional':special,'concentrated_regular':regular,'every_proper_edge_singular':flat};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    for k,v in out.items():print(k,v)

if __name__=='__main__':main()
