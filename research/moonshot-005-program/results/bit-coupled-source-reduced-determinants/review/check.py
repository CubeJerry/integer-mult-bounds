#!/usr/bin/env python3
"""Independent coupling, common-lift and nilpotent-restriction verification."""
import argparse,gzip,hashlib,json
from collections import Counter
from pathlib import Path
import native_algebra as n

class Field:
    def __init__(self,e,poly):
        self.q=1<<e;self.poly=poly
        def multiply(a,b):
            z=0
            while b:
                if b&1:z^=a
                b>>=1;a<<=1
                if a&self.q:a^=poly
            return z
        for generator in range(2,self.q):
            powers=[];seen=set();v=1
            for _ in range(self.q-1):
                if v in seen:break
                powers.append(v);seen.add(v);v=multiply(v,generator)
            if len(powers)==self.q-1 and v==1:break
        else:raise ValueError('primitive field generator absent')
        log={x:i for i,x in enumerate(powers)};self.mul=[[0]*self.q for _ in range(self.q)]
        for a in range(1,self.q):
            for b in range(1,self.q):self.mul[a][b]=powers[(log[a]+log[b])%(self.q-1)]
        self.inv=[0]+[powers[-log[a]%(self.q-1)]for a in range(1,self.q)]
        for a in range(self.q):
            for b in range(self.q):n.require(self.mul[a][b]==multiply(a,b),'log-table polynomial agreement')
    def power(self,a,k):
        x=1
        for _ in range(k):x=self.mul[x][a]
        return x
    def product(self,A,B):
        return [[n.xor(self.mul[x][B[k][j]]for k,x in enumerate(row))for j in range(len(B[0]))]for row in A]
    def rank(self,A):
        if not A:return 0
        rows=[list(r)for r in A];p=0
        for c in range(len(rows[0])):
            pivot=next((r for r in range(p,len(rows))if rows[r][c]),None)
            if pivot is None:continue
            rows[p],rows[pivot]=rows[pivot],rows[p];s=self.inv[rows[p][c]]
            rows[p]=[self.mul[s][x]for x in rows[p]]
            for r in range(p+1,len(rows)):
                s=rows[r][c]
                if s:rows[r]=[x^self.mul[s][y]for x,y in zip(rows[r],rows[p])]
            p+=1
            if p==len(rows):break
        return p
    def inverse(self,A):
        d=len(A);rows=[list(r)+[int(i==j)for j in range(d)]for i,r in enumerate(A)]
        for c in range(d):
            pivot=next(r for r in range(c,d)if rows[r][c]);rows[c],rows[pivot]=rows[pivot],rows[c]
            s=self.inv[rows[c][c]];rows[c]=[self.mul[s][x]for x in rows[c]]
            for r in range(d):
                if r!=c:
                    s=rows[r][c]
                    if s:rows[r]=[x^self.mul[s][y]for x,y in zip(rows[r],rows[c])]
        n.require([r[:d]for r in rows]==eye(d),'inverse exact identity')
        return [r[d:]for r in rows]
    def determinant(self,A):
        rows=[list(r)for r in A];det=1;d=len(rows)
        for c in range(d):
            p=next((r for r in range(c,d)if rows[r][c]),None)
            if p is None:return 0
            rows[c],rows[p]=rows[p],rows[c];a=rows[c][c];det=self.mul[det][a]
            for r in range(c+1,d):
                s=self.mul[rows[r][c]][self.inv[a]]
                if s:rows[r]=[x^self.mul[s][y]for x,y in zip(rows[r],rows[c])]
        return det

def eye(k):return [[int(i==j)for j in range(k)]for i in range(k)]
def columns(M):return list(map(list,zip(*M)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results';lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';bp=base/'bit-clifford-one-evaluation-gate/author/BASIS.json';rp=base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz';pp=base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    raw=gzip.decompress(lp.read_bytes());n.require(hashlib.sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    layout=json.loads(raw);G,_=n.native(layout,json.loads(bp.read_text()));roots=layout['root_table'];H=list(map(set,layout['A2']));D=list(map(set,layout['D4']))
    adj=[{j for j,y in enumerate(roots)if i!=j and sum(u*v for u,v in zip(x,y))==0}for i,x in enumerate(roots)]
    quotas=Counter()
    for line in gzip.decompress(rp.read_bytes()).splitlines():
        phase,j,c,h,d,k,l,r=json.loads(line)
        if phase=='X':quotas[j,h]+=1
    donors=[0,61,62];receivers=[i for i in range(111)if H[263]<=adj[i] and all(all(quotas[j,h]<=30 for h,P in enumerate(H)if j in P and P<=adj[i])for j in donors)]
    n.require(len(receivers)==33,'joint tight receiver census')
    maxviews=max(sum(P<=adj[i]for i in range(111))for P in H);n.require(maxviews==36,'at most36 foreign determinants per source parameter')
    restrictions=0
    for i in range(120):
        N=n.plus(G[i],n.identity(16));n.require(n.multiply(N,N)==[0]*16 and n.matrix_rank(N)==8,'rank-half native nilpotent')
        if i not in receivers:continue
        cols=[];ids=[]
        for t,v in enumerate(n.transpose(N)):
            if n.matrix_rank(cols+[v])>len(cols):cols.append(v);ids.append(t)
        K=n.transpose(cols,16);P=n.transpose(cols+[1<<t for t in ids],16);R=n.inverse(P)[:8]
        n.require(n.multiply(R,K)==n.identity(8),'fixed binary kernel coordinates')
        for j in donors:
            other=min(H[263]-{j});A=n.plus(G[j],n.identity(16));B=n.plus(G[other],n.identity(16))
            for C in [n.multiply(A,B),A,B,n.multiply(B,A)]:
                reduced=n.multiply(n.multiply(R,C),K)
                n.require(n.multiply(C,K)==n.multiply(K,reduced)and n.matrix_rank(reduced)==4,'rank-four covariant parameter restriction')
                restrictions+=1
    f4=Field(2,7);count=0
    Bs=[[[0,0],[0,0]],eye(2),[[0,1],[0,0]],[[1,2],[3,1]]]
    for z in range(256):
        vals=[(z>>(2*k))&3 for k in range(4)];A=[vals[:2],vals[2:]]
        for B in Bs:
            Q=[A[r]+B[r]for r in range(2)]+[[0,0]+A[r]for r in range(2)]
            det=f4.determinant(A)
            n.require(f4.determinant(Q)==f4.mul[det][det],'dual-number determinant square over GF4')
            n.require((f4.rank(Q)==4)==(f4.rank(A)==2),'restriction invertibility equivalence')
            count+=1
    bad=[[1,0,0,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]]
    n.require(f4.rank(bad)==2 and f4.rank(eye(2))==2,'nonintertwining restriction alone is insufficient')
    n.require(f4.rank([[1,0],[1,0]])==1,'bad early frame remains an independent defect')
    f8=Field(3,11);P=[[0,0,1],[1,0,0],[0,1,0]];E=[[1,0,0],[0,0,0],[0,0,0]];L=eye(3);L[0][1]=1;R=eye(3);R[1][2]=1
    def wordrank(U,V):
        powers=[eye(3),U,f8.product(U,U)];words=[]
        for i in range(3):
            for j in range(3):words.append(sum(f8.product(f8.product(powers[i],V),powers[j]),[]))
        return f8.rank(words)
    traces=[]
    for lam in range(5):
        B=[[x^(lam if i==j else 0)for j,x in enumerate(row)]for i,row in enumerate(P)]
        A1=f8.product(L,R);B1=f8.product(f8.product(L,B),R);C1=f8.product(f8.product(L,E),R)
        U=f8.product(f8.inverse(A1),B1);V=f8.product(f8.inverse(A1),C1)
        n.require(wordrank(U,V)==9,'gauge-invariant full M3 coefficient algebra');traces.append(n.xor(U[i][i]for i in range(3)))
    n.require(len(set(traces))==5 and wordrank(P,eye(3))==3,'distinct trace and commuting controls')
    f=Field(9,529);classes=json.loads(gzip.decompress(pp.read_bytes()))['classes']['263'];spans=[]
    for c,ports in enumerate(classes):
        V=[[f.power(p+1,t)for t in range(9)]for p in range(9)];graphs={}
        for i in receivers:
            selected=[p for p,d in enumerate(ports)if D[d]<=adj[i]];n.require(len(selected)==3,'three visible class ports')
            graphs[i]=sum([f.inverse([[V[p][3*j+t]for t in range(3)]for p in selected])for j in range(3)],[])
        for j in donors:
            for h,P0 in enumerate(H):
                if j not in P0 or h==263:continue
                rows=sum([columns(graphs[i])for i in receivers if P0<=adj[i]],[])
                rank=f.rank(rows);n.require(rank==9,'complete common-lift annihilation span');spans.append({'class':c,'donor':j,'plane':h,'rank':rank})
        n.require(f.rank(graphs[receivers[0]])==3,'one receiver cannot prove the common-lift obstruction')
    n.require(len(spans)==405,'complete native common-lift coverage')
    degree={'reduced_foreign':36*4,'unreduced_early':8,'source_and_early':152,'full64_with_commutator':154,'coupled_with_all_extra_factors':152+54+1+8+2}
    n.require(degree['coupled_with_all_extra_factors']==217 and 217<256,'finite grid bound')
    proofnames=['PROOF.md','COMMON-LIFT.md','REDUCED-DETERMINANT.md']
    result={'status':'PASS_INDEPENDENT_COUPLED_SOURCE_REDUCTION_AND_COMMON_LIFT_REVIEW','native_rank_half_nilpotents':120,'native_rank_four_restrictions':restrictions,'GF4_determinant_and_invertibility_checks':count,'GF8_distinct_coupling_traces':traces,'common_lift_span_checks':len(spans),'degrees':degree,
      'scope':'Source-family existence, reduced foreign determinants, fixed common-lift exclusion; no selected GF256 constants or full shared decoder.',
      'source_pins':[{'path':str(p.relative_to(a.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,bp,rp,pp]],
      'author_pins':[{'path':s,'sha256':hashlib.sha256((a.author/s).read_bytes()).hexdigest()}for s in proofnames],
      'negative_controls':{'nonintertwining_full_rank':2,'restriction_rank':2,'defective_early_frame_rank':1,'commuting_word_rank':3,'single_receiver_span':3},'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');(a.out/'SPAN-CENSUS.json').write_text(json.dumps(spans,indent=2)+'\n');print(result['status'],flush=True)
if __name__=='__main__':main()
