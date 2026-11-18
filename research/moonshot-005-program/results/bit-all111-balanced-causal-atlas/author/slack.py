#!/usr/bin/env python3
"""Construct simultaneous strictly surplus pair cuts on the paid 111-role layout."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from fractions import Fraction
from functools import reduce
from hashlib import sha256
from heapq import heapify,heappop,heappush
from pathlib import Path
import gzip,json
from atlas import bits,mask
from layout import need

def design(w):
    N=(1<<111)-1
    A=list(map(mask,w['A2']));D=list(map(mask,w['D4']));P=w['dual_D4'];R=w['root_table'];routes=w['routes']
    O=[mask(j for j,t in enumerate(R) if sum(a*b for a,b in zip(s,t))==0) for s in R]
    J=[reduce(int.__and__,[O[j] for j in bits(h)])&N for h in A]
    pairindex={(j,i):n for n,(j,i) in enumerate((j,i) for j in range(111) for i in bits(O[j]&N))};n=len(pairindex)
    need(n==6470,'foreign pair count')
    def setp(js,Is):
        return mask(pairindex[j,i] for j in bits(js) for i in bits(Is))
    HL=defaultdict(list);left_short=defaultdict(list);right_short=defaultdict(list);left_aux=defaultdict(list);right_aux=defaultdict(list)
    for z,(kind,d,h,j,k,i,*_) in enumerate(routes):
        if h is not None:HL[d].append(h)
        if j is None:left_short[d].append(z)
        elif j>=111:left_aux[h].append(z)
        if i is None:right_short[d].append(z)
        elif i>=111:right_aux[k].append(z)
    need(all(len(left_short[d])==len(right_short[P[d]]) for d in range(len(D))),'dual short inventory')
    need(all(len(left_aux[h])==len(right_aux[h]) for h in range(len(A))),'dual aux inventory')
    ops=[];caps=[];used=Counter()
    def group(cap):
        caps.append(cap);return len(caps)-1
    for h in sorted(left_aux):
        if left_aux[h]:
            g=group(len(left_aux[h]))
            for j in bits(A[h]&N):ops.append((g,'aux',h,-1,j,setp(1<<j,J[h])))
    for d in sorted(left_short):
        if left_short[d]:
            g=group(len(left_short[d]))
            for h in sorted(HL[d]):
                js=A[h]&N;middle=setp(js,D[P[d]]&N)<<n
                for j in bits(js):ops.append((g,'short',h,d,j,middle|setp(1<<j,J[h])))
    target=(1<<(2*n))-1
    possible=reduce(int.__or__,(v[-1] for v in ops),0)
    need(possible==target,'every pair individually available')
    heap=[(-v[-1].bit_count(),k) for k,v in enumerate(ops)];heapify(heap)
    deficit=target;patch=[]
    while deficit and heap:
        neg,k=heappop(heap);g,kind,h,d,j,cover=ops[k]
        if used[g]==caps[g]:continue
        score=(cover&deficit).bit_count()
        if not score:continue
        if score!= -neg:
            heappush(heap,(-score,k));continue
        if kind=='short':l=left_short[d][used[g]];r=right_short[P[d]][used[g]]
        else:l=left_aux[h][used[g]];r=right_aux[h][used[g]]
        patch.append([kind,l,j,h,r,j,h]);used[g]+=1;deficit&=~cover
    need(not deficit,'simultaneous distinct real resource cover')
    return patch

def audit(w,patch):
    A=list(map(mask,w['A2']));D=list(map(mask,w['D4']));P=w['dual_D4'];R=w['root_table'];N=(1<<111)-1
    O=[mask(j for j,t in enumerate(R) if sum(a*b for a,b in zip(s,t))==0) for s in R];J=[reduce(int.__and__,[O[j] for j in bits(h)])&N for h in A]
    routes=[list(r) for r in w['routes']];sused=set();tused=set();ints=Counter()
    for kind,l,j,h,r,i,k in patch:
        L,T=routes[l],routes[r];need(L[0]=='Y' and T[0]=='X' and l not in sused and r not in tused,'each actual spare used once')
        sused.add(l);tused.add(r);need(j<111 and i<111 and (1<<j)&A[h] and (1<<i)&A[k],'native labels')
        need(A[h]&D[L[1]]==A[h] and A[k]&D[P[T[1]]]==A[k],'nested real visits')
        if kind=='aux':need(L[2]==h and L[3]>=111 and T[4]==k and T[5]>=111,'genuine padding port')
        else:need(kind=='short' and L[2:4]==[None,None] and T[4:6]==[None,None],'genuine short port')
        L[2:4]=[h,j];T[4:6]=[k,i];ints[kind]+=2
    c=[Counter() for _ in range(4)];mov=Counter();origins=Counter();ends=Counter();H_count=Counter();K_count=Counter()
    for kind,d,h,j,k,i,*_ in routes:
        ranks=[1] if kind=='X' else [0]
        if h is not None:
            H_count[h,d]+=1
            if j<111:
                origins[j]+=1
                for ii in bits(J[h]):c[0][j,ii]+=1
                if kind=='Y':ranks.append(1)
            ranks.append(2)
            for jj in bits(A[h]&N):
                for ii in bits(D[P[d]]&N):c[1][jj,ii]+=1
        ranks.append(4)
        if k is not None:
            K_count[d,k]+=1
            for jj in bits(D[d]&N):
                for ii in bits(A[k]&N):c[2][jj,ii]+=1
            ranks.append(6)
            if i<111:
                ends[i]+=1
                for jj in bits(J[k]):c[3][jj,i]+=1
                ranks.append(7)
        if kind=='X':ranks.append(8)
        for a,b in zip(ranks,ranks[1:]):need(a<b,'strict monotone geometry');mov[b-a]+=1
    mov[8]+=9*240
    legal={(j,i) for j in range(111) for i in bits(O[j]&N)}
    need(all(set(v)==legal for v in c),'only geometric foreign pairs')
    need(all(min(z.values())>=241 for z in c),'all four strict native pair cuts')
    return {'status':'PASS_STRICT_4_CUT_111_ROLE_LAYOUT','normalized_movement_profile':{q:str(Fraction(v,240)) for q,v in sorted(mov.items())},
            'paid_field_copies':240,'GF_movement_profile':dict(sorted(mov.items())),'real_public_routes':len(routes),
            'new_line_or_facet_visits':dict(sorted(ints.items())),'foreign_pairs':len(legal),
            'four_cut_histograms':[dict(sorted(Counter(z.values()).items())) for z in c],
            'native_source_distinct_evaluation_slots':[min(origins.values()),max(origins.values())],
            'native_output_distinct_evaluation_slots':[min(ends.values()),max(ends.values())],
            'H_D_multiplicities':dict(sorted(Counter(H_count.values()).items())),'D_K_multiplicities':dict(sorted(Counter(K_count.values()).items())),
            'source_MDS_field':'GF(1024)','required_pair_dimension':240,
            'accepted_physical_full_diagonal':False},routes

def main():
    a=ArgumentParser();a.add_argument('--layout',type=Path,required=True);a.add_argument('--out',type=Path,required=True);v=a.parse_args()
    raw=gzip.decompress(v.layout.read_bytes());w=json.loads(raw);need(sha256(raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    patch=design(w);r,_=audit(w,patch);b=json.dumps(patch,separators=(',',':')).encode()+b'\n';r['base_layout_sha256']=sha256(raw).hexdigest();r['patch_sha256']=sha256(b).hexdigest()
    v.out.mkdir(parents=True,exist_ok=True);(v.out/'SLACK-PATCH.json.gz').write_bytes(gzip.compress(b,mtime=0));(v.out/'SLACK-RESULT.json').write_text(json.dumps(r,indent=2)+'\n')
    print(r['status'],r['new_line_or_facet_visits'],[min(d) for d in r['four_cut_histograms']],r['normalized_movement_profile'])
if __name__=='__main__':main()
