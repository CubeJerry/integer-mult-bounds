#!/usr/bin/env python3
"""Independent holder, coefficient, and literal ADD-word checks for F64 V45."""
from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json

LH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
FH='346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7'

def need(ok,why):
    if not ok:raise ValueError(why)

def polymul(a,b):
    value=0
    for k in range(6):
        if b>>k&1:value^=a<<k
    while value.bit_length()>6:value^=67<<(value.bit_length()-7)
    return value

MUL=[[polymul(a,b)for b in range(64)]for a in range(64)]
INV=[0]+[next(b for b in range(1,64)if MUL[a][b]==1)for a in range(1,64)]

def determinant(rows):
    a=[row[:]for row in rows];n=len(a);value=1
    for c in range(n):
        pivot=next((k for k in range(c,n)if a[k][c]),None)
        if pivot is None:return 0
        a[c],a[pivot]=a[pivot],a[c];q=a[c][c];value=MUL[value][q];inv=INV[q]
        a[c]=[MUL[x][inv]for x in a[c]]
        for k in range(c+1,n):
            q=a[k][c]
            if q:a[k]=[x^MUL[q][y]for x,y in zip(a[k],a[c])]
    return value

def replay(word,initial):
    state=initial[:]
    for dst,src in word:
        need(0<=dst<270 and 0<=src<270 and dst!=src,'valid distinct existing co-located ADD records')
        state[dst]^=state[src]
    return state

def expected_binary(V,order):
    answer=[]
    for row in V:
        for out in range(6):
            bits=0
            for column,coefficient in enumerate(row):
                for bit in range(6):
                    if MUL[coefficient][1<<bit]>>out&1:bits^=1<<(6*order[column]+bit)
            answer.append(bits)
    return answer

def holder_checks(V,word):
    identity=[1<<j for j in range(270)];patterns=[]
    for q in range(3):
        donor=[(q-p)%3 for p in range(45)]
        order=sorted(range(45),key=lambda p:(donor[p],p))
        need([donor[p]for p in order]==[j for j in range(3)for _ in range(15)],'three contiguous donor blocks')
        current=list(range(45));swaps=[];prefix=[]
        for pos,wanted in enumerate(order):
            at=current.index(wanted)
            if at==pos:continue
            current[pos],current[at]=current[at],current[pos];swaps.append([pos,at])
            for bit in range(6):
                a=6*pos+bit;b=6*at+bit;prefix.extend([[a,b],[b,a],[a,b]])
        need(current==order and len(swaps)<=44,'literal physical permutation')
        initial=replay(prefix,identity);result=replay(word,initial);need(result==expected_binary(V,order),'physical-holder matrix with actual column permutation')
        restored=replay(prefix[::-1],replay(word[::-1],result));need(restored==identity,'whole local transformation has paid ADD inverse')
        patterns.append({'donor_residue':q,'input_column_order_by_physical_port':order,'field_swaps':swaps,'binary_ADD':prefix,'binary_ADD_count':len(prefix)})
    need([len(p['field_swaps'])for p in patterns]==[42,42,40],'exact permutation counts')
    census=[]
    for x in[4,5,6]:
        covered=set();stripe_counts=Counter()
        for phase,a in[('early',x),('late',8-x)]:
            for sigma in range(3*a):
                holders=[((sigma//a-p)%3,p,sigma%a)for p in range(45)]
                need(Counter(j for j,p,s in holders)=={0:15,1:15,2:15},'fifteen true holders per donor and stripe')
                need(len({p for j,p,s in holders})==45,'one holder at each physical D4 port')
                for j,p,s in holders:
                    key=(phase,j,p,s);need(key not in covered,'no holder used twice');covered.add(key)
                    need(sigma==s+a*((j+p)%3),'literal local-ordinal stripe formula')
                stripe_counts[sigma//a]+=1
            expected={(phase,j,p,s)for j in range(3)for p in range(45)for s in range(a)}
            need({z for z in covered if z[0]==phase}==expected,'all actual early or late source flag holders once')
        need(len(covered)==1080 and stripe_counts=={0:8,1:8,2:8},'all twenty-four stripes respect actual phases')
        census.append({'x':x,'early_stripes':3*x,'late_stripes':3*(8-x),'total_actual_field_holders':len(covered),'permutation_residue_counts':dict(sorted(stripe_counts.items()))})
    total_prefix=sum(8*p['binary_ADD_count']for p in patterns)
    need(total_prefix==17856,'exact per-plane permutation invoice')
    return patterns,census,total_prefix

def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--factor',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    lr=gzip.decompress(a.layout.read_bytes());fr=a.factor.read_bytes();need(sha256(lr).hexdigest()==LH and sha256(fr).hexdigest()==FH,'pinned layout and factor');w=json.loads(lr);factor=dict(json.loads(fr)['factors'])
    coeff_raw=(a.author/'output/COEFFICIENTS.json').read_bytes();coeff=json.loads(coeff_raw);V=[]
    for t in range(1,46):
        row=[1]
        for _ in range(44):row.append(MUL[row[-1]][t])
        V.append(row)
    need(coeff=={'field_modulus':67,'nodes':list(range(1,46)),'matrix':V},'independent polynomial-product field matrix')
    need(determinant(V)!=0,'full45-dimensional invertibility')
    wr=gzip.decompress((a.author/'output/ADD-WORD.json.gz').read_bytes());payload=json.loads(wr);word=payload['ADD'];need(len(word)==31355,'literal ADD count')
    identity=[1<<j for j in range(270)];expected=expected_binary(V,list(range(45)));need(replay(word,identity)==expected,'all270 independent original columns')
    need(replay(word[:len(word)//2]+word[len(word)//2+1:],identity)!=expected,'omitted ADD detected')
    patterns,census,prefix_cost=holder_checks(V,word)
    author_raw=(a.author/'output/RESULT.json').read_bytes();author=json.loads(author_raw);need(author['binary_ADD_word_uncompressed_sha256']==sha256(wr).hexdigest(),'author word pin')
    roots=w['root_table'];planes=[set(h)for h in w['A2']];middles=[set(d)for d in w['D4']];native=set(range(111));perp=[{j for j,v in enumerate(roots)if sum(x*y for x,y in zip(u,v))==0}for u in roots[:111]]
    byH={z['H']:z for z in author['planes']};need(len(byH)==881,'distinct full plane certificates');hist=Counter();shared=Counter();incidences=0;detchecks=0
    @lru_cache(None)
    def det_base(ids):return determinant([[V[p][c]for c in range(15)]for p in ids])
    for h,H in enumerate(planes):
        if len(H&native)!=3:continue
        z=byH[h];ports=[d for d,D in enumerate(middles)if H<=D];need(len(ports)==45 and z['actual_D4_ports']==ports,'all actual D4 exit identities')
        x=4+factor.get(h,0);hist[x]+=1;need(z['x']==x and z['early_lanes_per_port']==3*x and z['late_lanes_per_port']==24-3*x,'all physical phase capacities')
        rec={i:tuple(p for p,d in enumerate(ports)if middles[d]<=perp[i])for i in range(111)if H<=perp[i]}
        need({int(i)for i in z['receiver_subsets']}==set(rec),'all actual receiver incidences')
        for i,ids in rec.items():
            need(len(ids)==15 and z['receiver_subsets'][str(i)]['ports']==list(ids),'all fifteen-port receiver identities');incidences+=1
            base=det_base(ids);need(base,'independent Gaussian donor determinant')
            dets=[]
            for j in range(3):
                det=base
                for p in ids:det=MUL[det][V[p][15*j]]
                need(det,'all scaled donor projections invertible');dets.append(det);detchecks+=1
            need(dets==z['receiver_subsets'][str(i)]['field_determinants'],'all actual published determinant values')
        for i,j in combinations(rec,2):shared[len(set(rec[i])&set(rec[j]))]+=1
    need(hist=={4:709,5:84,6:88} and incidences==29354 and detchecks==88062,'complete native census')
    need(shared=={3:203842,6:271177},'actual target-intersection dimensions72or144')
    count=24*len(word)+prefix_cost;need(count==770376,'exact physical ordinary compiler bound')
    out={'status':'PASS_INDEPENDENT_CAUSAL_FULL_PLANE_ARRAY_REVIEW','author_proof_sha256':sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'author_result_sha256':sha256(author_raw).hexdigest(),'coefficient_sha256':sha256(coeff_raw).hexdigest(),'word_uncompressed_sha256':sha256(wr).hexdigest(),'layout_uncompressed_sha256':LH,'factor_sha256':FH,'field_arithmetic':'independent carryless polynomial product and long reduction','full_native_planes':881,'factor_x_histogram':dict(sorted(hist.items())),'actual_receiver_incidences':incidences,'donor_projection_determinants_checked':detchecks,'distinct_Gaussian_base_determinants':det_base.cache_info().currsize,'receiver_pair_shared_port_histogram':dict(sorted(shared.items())),'literal_word_columns':270,'literal_word_ADD':len(word),'physical_holder_census':census,'literal_permutation_ADD_per_H':prefix_cost,'exact_ADD_per_H_with_physical_permutations':count,'exact_ADD_all881_H':count*881,'extra_INIT_CLEAR_MOVE':0,'author_code_imported':False,'global_source_compatibility_proved':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'HOLDER-PERMUTATIONS.json').write_text(json.dumps({'schema':'literal-field-holder-input-permutations-v1','patterns':patterns,'physical_cases':census},separators=(',',':'))+'\n');print(out['status'],incidences,'incidences',detchecks,'projectiondeterminants',count,'ADD/H',flush=True)

if __name__=='__main__':main()
