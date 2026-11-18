#!/usr/bin/env python3
"""Independent actual-geometry/full-matrix/holder replay of punctured arrays."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from pathlib import Path
import gzip,json,struct,subprocess

LH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'

def need(ok,why):
    if not ok:raise ValueError(why)

def poly(a,b):
    q=0
    for k in range(7):
        if b>>k&1:q^=a<<k
    while q.bit_length()>7:q^=131<<(q.bit_length()-8)
    return q

MUL=[[poly(a,b)for b in range(128)]for a in range(128)]
need(all(any(MUL[a][b]==1 for b in range(1,128))for a in range(1,128)),'independent F128 field inverses')

def matrix(n):
    V=[]
    for a in range(1,n+1):
        row=[1]
        for _ in range(n-1):row.append(MUL[row[-1]][a])
        V.append(row)
    return V

def binary(rows,order=None):
    if order is None:order=list(range(len(rows[0])))
    result=[]
    for row in rows:
        for bit in range(7):
            r=0
            for c,v in enumerate(row):
                for k in range(7):
                    if MUL[v][1<<k]>>bit&1:r^=1<<(7*order[c]+k)
            result.append(r)
    return result

def apply(word,state):
    value=state[:]
    for a,b in word:
        need(0<=a<len(value)and 0<=b<len(value)and a!=b,'valid distinct ADD operands')
        value[a]^=value[b]
    return value

def permutation(order):
    current=list(range(len(order)));swaps=[];ops=[]
    for p,want in enumerate(order):
        q=current.index(want)
        if p==q:continue
        current[p],current[q]=current[q],current[p];swaps.append([p,q])
        for bit in range(7):
            a,b=7*p+bit,7*q+bit;ops.extend([[a,b],[b,a],[a,b]])
    need(current==order,'literal physical contents permutation')
    return swaps,ops

def physical_orders():
    early=[2*p+j for j in range(2)for p in range(45)];early_swaps,early_ops=permutation(early)
    late=[];coverage=set();counts=[];ground_at_port=[0]*45
    for sigma in range(6):
        holders=[]
        for p in range(45):
            source=[(j,p,sigma%2)for j in range(2)if (j+p)%3==sigma//2]
            need(len(source)<=1,'at most one source late holder per stripe and port')
            cell=[('L',j,p,s)for j,p,s in source]
            while len(cell)<2:
                cell.append(('Z',-1,p,ground_at_port[p]));ground_at_port[p]+=1
            for holder in cell:need(holder not in coverage,'actual late holder used once');coverage.add(holder)
            holders.extend(cell)
        need(Counter(h[1]for h in holders)=={0:15,1:15,-1:60},'actual late stripe count15+15+60')
        order=sorted(range(90),key=lambda p:(0 if holders[p][1]==0 else 1 if holders[p][1]==1 else 2,p))
        swaps,ops=permutation(order);late.append({'stripe':sigma,'order':order,'swaps':swaps,'ADD':ops});counts.append(len(swaps))
    expected={('L',j,p,s)for j in range(2)for p in range(45)for s in range(2)}|{('Z',-1,p,s)for p in range(45)for s in range(8)}
    need(coverage==expected and ground_at_port==[8]*45,'all real source and pure-Y late holders once')
    return {'early_order':early,'early_swaps':early_swaps,'early_ADD':early_ops,'late':late,'early_field_swap_count':len(early_swaps),'late_field_swap_counts':counts}

def replay_causal(V,C,word,physical):
    n=630;identity=[1<<j for j in range(2*n)];cross=binary(C);tested=0
    for late in physical['late']:
        early=apply(physical['early_ADD'],identity[:n]);cache=early[:]
        early=apply(word,early)
        late_input=apply(late['ADD'],identity[n:]);outlate=apply(word,late_input)
        crosscount=0
        for i,r in enumerate(cross):
            while r:
                bit=r&-r;r^=bit;outlate[i]^=cache[bit.bit_length()-1];crosscount+=1
        expected=binary(V,physical['early_order'])+[a^(b<<n)for a,b in zip(binary(C,physical['early_order']),binary(V,late['order']))]
        need(early+outlate==expected,'complete1260-column causal word in actual physical-holder order')
        need(all(c and c.bit_count()==1 for c in cache),'all actual stationary cache owners remain dirty')
        if tested==0:
            bad=outlate[:]
            for i,r in enumerate(cross):
                if r&1:bad[i]^=cache[0]
            need(bad!=outlate,'omitted early-cache copy detected')
            need(apply(word,late_input)!=outlate,'omitted crosswave stage detected')
        tested+=1
    return {'physical_stripes_replayed':tested,'original_columns_each':1260,'cache_INIT_copyADD_dirtyCLEAR_each_per_stripe':630,'sample_crosswave_ADD':crosscount}

def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==LH,'geometry pin');w=json.loads(raw);roots=w['root_table'];H=list(map(set,w['A2']));D=list(map(set,w['D4']));native=set(range(111));perp=[{j for j,v in enumerate(roots)if sum(x*y for x,y in zip(u,v))==0}for u in roots[:111]]
    cr=(a.author/'output/COEFFICIENTS.json').read_bytes();coeff=json.loads(cr);author_raw=(a.author/'output/RESULT.json').read_bytes();author=json.loads(author_raw);need(author['coefficient_json_sha256']==sha256(cr).hexdigest(),'author coefficient pin')
    byh={z['H']:z for z in coeff['planes']};geometry={z['H']:z for z in author['geometry']};need(len(byh)==len(geometry)==227,'all unique punctured planes')
    packed=bytearray(struct.pack('<I',227));counters=Counter();native_conditions=0;cross_cost=[];first_C=None
    weights=[sum(MUL[c][1<<b].bit_count()for b in range(7))for c in range(128)]
    for h,P in enumerate(H):
        if len(P&native)!=2:continue
        ports=[d for d,Q in enumerate(D)if P<=Q];need(len(ports)==45,'all actual plane exits');rec={i:[2*p+b for p,d in enumerate(ports)if D[d]<=perp[i]for b in range(2)]for i in range(111)if P<=perp[i]}
        g=geometry[h];need(g['D4_ports']==ports and g['native_donors']==sorted(P&native)and g['receivers']==list(rec),'complete independent geometric identities')
        need(len(rec)<=36 and all(len(S)==30 for S in rec.values()),'native polynomial degree and actual row count')
        z=byh[h];C=[list(bytes.fromhex(row))for row in z['C_hex_rows']];need(len(C)==90 and all(len(row)==90 and max(row)<128 for row in C),'literal90by90 coefficients')
        if first_C is None:first_C=C
        need({(i,j)for i,j,d in z['conditions']}=={(i,j)for i in rec for j in range(2)}and all(d for i,j,d in z['conditions']),'all claimed reduced conditions once and nonzero')
        counters[z['trial']]+=1;cross_cost.append(sum(weights[c]for row in C for c in row));native_conditions+=2*len(rec)
        packed.extend(struct.pack('<II',h,len(rec)));packed.extend(bytes(c for row in C for c in row))
        for i,S in rec.items():packed.extend(struct.pack('<I',i));packed.extend(bytes(S))
    need(native_conditions==15098 and counters=={1:128,2:55,3:23,4:10,5:11},'exact native determinant/trial census')
    inp=a.out/'DIRECT-INPUT.bin';inp.write_bytes(packed);exe=a.out/'direct';src=Path(__file__).with_name('direct.cpp')
    subprocess.run(['g++','-std=c++17','-O3',str(src),'-o',str(exe)],check=True);direct_result=a.out/'DIRECT-DETERMINANTS.json';subprocess.run([str(exe),str(inp),str(direct_result)],check=True)
    direct=json.loads(direct_result.read_bytes());need(direct['condition_count']==15098 and direct['all_rank_60'],'direct original60by60 projections all invertible')
    V=matrix(90);wr=gzip.decompress((a.author/'output/ADD-WORD.json.gz').read_bytes());payload=json.loads(wr);word=payload['ADD'];need(len(word)==167325 and sha256(wr).hexdigest()==author['V90_ADD_word_uncompressed_sha256'],'V90 literal word pin')
    need(apply(word,[1<<j for j in range(630)])==binary(V),'independent630-column V90 word')
    physical=physical_orders();causal=replay_causal(V,first_C,word,physical)
    uniform_raw=gzip.decompress((a.author/'output/FULL-H-ADD-WORD.json.gz').read_bytes());uniform=json.loads(uniform_raw);fullword=uniform['ADD'];need(apply(fullword,[1<<j for j in range(315)])==binary(matrix(45)),'commonF128 full-H word315 independent columns')
    need(min(cross_cost)==author['C_crosswave_ADD_per_stripe_min']and max(cross_cost)==author['C_crosswave_ADD_per_stripe_max'],'all crosswave ADD invoices')
    exact_perm=6*len(physical['early_ADD'])+sum(len(z['ADD'])for z in physical['late'])
    exact_costs=[12*len(word)+exact_perm+6*c+3780 for c in cross_cost]
    conservative=[12*(len(word)+1869)+6*c+3780 for c in cross_cost]
    need(sum(conservative)==author['full_ADD_count_all_227_H_including_permutation_bound'],'complete charged conservative ADD count')
    out={'status':'PASS_INDEPENDENT_PUNCTURED_ARRAY_AND_PHYSICAL_CAUSAL_REVIEW','layout_uncompressed_sha256':LH,'author_proof_sha256':sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'author_result_sha256':sha256(author_raw).hexdigest(),'coefficients_sha256':sha256(cr).hexdigest(),'direct_condition_count':native_conditions,'direct_60_by_60_determinants_sha256':sha256(direct_result.read_bytes()).hexdigest(),'coefficient_trials_histogram':dict(sorted(counters.items())),'independent_field_arithmetic':'carryless polynomial product and long reduction','V90_word_columns':630,'V90_word_ADD':len(word),'causal_physical_replay':causal,'early_physical_field_swaps':physical['early_field_swap_count'],'late_physical_field_swaps':physical['late_field_swap_counts'],'exact_permutation_ADD_per_H':exact_perm,'exact_ADD_per_H_min':min(exact_costs),'exact_ADD_per_H_max':max(exact_costs),'exact_ADD_all227_H':sum(exact_costs),'conservative_author_ADD_all227_H':sum(conservative),'cache_INIT_copyADD_dirtyCLEAR_each_per_H':3780,'cache_INIT_and_CLEAR_each_all227_H':227*3780,'extra_MOVE':0,'common_F128_full_H_word_columns':315,'common_F128_full_H_word_ADD':len(fullword),'all_source_quotients_globally_compatible':False,'later_transport_constructed':False,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'PHYSICAL-PERMUTATIONS.json').write_text(json.dumps(physical,separators=(',',':'))+'\n');print(out['status'],native_conditions,'full matrices',sum(exact_costs),'exact ADD all227',flush=True)

if __name__=='__main__':main()
