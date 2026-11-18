#!/usr/bin/env python3
"""Compute static and one-way time-expanded single-pair mincuts."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
import gzip,json
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import maximum_flow
from atlas import bits,mask
from slack import audit
from layout import need

def flows(w,rows):
    N=(1<<111)-1;A=list(map(mask,w['A2']));D=list(map(mask,w['D4']));P=w['dual_D4'];R=w['root_table']
    O=[mask(j for j,t in enumerate(R) if sum(a*b for a,b in zip(s,t))==0) for s in R]
    la=defaultdict(Counter);ad=defaultdict(Counter);dk=defaultdict(Counter);kf=defaultdict(Counter)
    for kind,d,h,j,k,i,*_ in rows:
        z=int(kind=='Y')
        if h is not None:
            ad[h,d][z]+=1
            if j<111:la[j,h][z]+=1
        if k is not None:
            dk[d,k][z]+=1
            if i<111:kf[k,i][z]+=1
    pens={j:[h for h,a in enumerate(A) if a>>j&1] for j in range(111)}
    Ds={j:{d for d,x in enumerate(D) if x>>j&1} for j in range(111)}
    HbyD=defaultdict(list);KbyD=defaultdict(list)
    for h,d in ad:HbyD[d].append(h)
    for d,k in dk:KbyD[d].append(k)
    data=[]
    for j in range(111):
        for i in bits(O[j]&N):
            hs={h for h in pens[j] if A[h]&O[i]==A[h]};ks={k for k in pens[i] if A[k]&O[j]==A[k]};ds={d for d in Ds[j] if D[P[d]]>>i&1}
            need(len(hs)==len(ks)==16 and len(ds)==60,'pair geometry')
            hn={h:p for p,h in enumerate(sorted(hs),start=1)}
            dn={d:p for p,d in enumerate(sorted(ds),start=17)}
            kn={k:p for p,k in enumerate(sorted(ks),start=77)}
            edges=[]
            for h in hs:edges.append((0,hn[h],la[j,h]))
            for d in ds:
                hitsH=hs.intersection(HbyD[d]);hitsK=ks.intersection(KbyD[d]);need(len(hitsH)==len(hitsK)==4,'D-restricted four/four')
                for h in hitsH:edges.append((hn[h],dn[d],ad[h,d]))
                for k in hitsK:edges.append((dn[d],kn[k],dk[d,k]))
            for k in ks:edges.append((kn[k],93,kf[k,i]))
            def calc(timed):
                v=[]
                if timed:
                    for a,b,c in edges:
                        for z,cap in c.items():v.append((a+z*94,b+z*94,cap))
                    for node in range(94):v.append((node,node+94,1000))
                    size=188;s=0;t=187
                else:
                    for a,b,c in edges:v.append((a,b,sum(c.values())))
                    size=94;s=0;t=93
                ii,jj,val=zip(*v);g=coo_matrix((val,(ii,jj)),shape=(size,size)).tocsr();return int(maximum_flow(g,s,t).flow_value)
            data.append([j,i,calc(False),calc(True)])
    return data

def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--patch',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    raw=gzip.decompress(a.layout.read_bytes());w=json.loads(raw);rr=w['routes']
    need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    if a.patch:_,rr=audit(w,json.loads(gzip.decompress(a.patch.read_bytes())))
    rows=flows(w,rr);rec={'status':'PASS_EXACT_SINGLE_PAIR_MINCUTS','cases':len(rows),'single_pair_static':dict(sorted(Counter(r[2] for r in rows).items())),'single_pair_causal':dict(sorted(Counter(r[3] for r in rows).items())),'required_dimension':240,'optimistic_chart_local_mixing':True}
    b=json.dumps(rows,separators=(',',':')).encode()+b'\n';rec['pair_table_sha256']=sha256(b).hexdigest()
    a.out.mkdir(parents=True,exist_ok=True);tag='SLACK' if a.patch else 'BASE';(a.out/('PAIRS-'+tag+'.json.gz')).write_bytes(gzip.compress(b,mtime=0));(a.out/('FLOW-'+tag+'.json')).write_text(json.dumps(rec,indent=2)+'\n');print(tag,rec)
if __name__=='__main__':main()
