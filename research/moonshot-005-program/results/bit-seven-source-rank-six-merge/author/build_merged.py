#!/usr/bin/env python3
"""Seven-source word with genuine D4-to-K6 merging and in-place F8 maps."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json
import build as direct
from build_shared import solve2

N=direct.N;RANK=direct.RANK;DEGREE=direct.DEGREE
DONORS=direct.DONORS;RECEIVERS=direct.RECEIVERS;PHI=direct.PHI
need=direct.need;mul=direct.mul;inv=direct.inv;dot=direct.dot;names=direct.names

def binary_rows(matrix):
    rows=[]
    for row in matrix:
        for bit in range(DEGREE):
            value=0
            for column,coefficient in enumerate(row):
                for k in range(DEGREE):
                    if mul(coefficient,1<<k)>>bit&1:value|=1<<(DEGREE*column+k)
            rows.append(value)
    return rows

def compile_inplace(matrix):
    target=binary_rows(matrix);work=target[:];ops=[];n=len(work)
    def add(a,b):work[a]^=work[b];ops.append([a,b])
    for c in range(n):
        p=next(p for p in range(c,n)if work[p]>>c&1)
        if p!=c:add(c,p);add(p,c);add(c,p)
        for p in range(n):
            if p!=c and work[p]>>c&1:add(p,c)
    need(work==[1<<p for p in range(n)],'invertible in-place binary matrix')
    word=ops[::-1];state=[1<<p for p in range(n)]
    for a,b in word:state[a]^=state[b]
    need(state==target,'all columns of in-place matrix')
    return word

def build(w):
    A=[set(h)for h in w['A2']];Ds=[set(d)for d in w['D4']];roots=w['root_table']
    planes={(j,k):next(h for h,H in enumerate(A)if{DONORS[j],DONORS[k]}<=H)for j,k in combinations(range(N),2)}
    seen_by_D=[{i for i,r in enumerate(RECEIVERS)if all(sum(a*b for a,b in zip(roots[r],roots[t]))==0 for t in D)}for D in Ds]
    def H(j,k):return 'H'+str(planes[tuple(sorted((j,k)))])
    events=[]
    def put(*a):events.append(list(a))
    def init(p,chart):
        for x in names(p):put('INIT',x,chart)
    def move(p,chart):
        for x in names(p):put('MOVE',x,chart)
    def clear(p):
        for x in names(p):put('CLEAR',x)
    def add(dst,src,c):
        for k in range(DEGREE):
            v=mul(c,1<<k)
            for r in range(DEGREE):
                if v>>r&1:put('ADD',names(dst)[r],names(src)[k])
    def inplace(p,q,matrix):
        coordinates=names(p)+names(q);word=compile_inplace(matrix)
        for a,b in word:put('ADD',coordinates[a],coordinates[b])
        return word
    for j in range(N):
        for k in range(N):
            if k==j:continue
            e=f'E{j}_{k}_';init(e,'L'+str(DONORS[j]))
            for c in range(RANK):add(e,f'X{j}_{c}_',PHI[k][c])
            move(e,H(j,k))
    source_add=sum(e[0]=='ADD'for e in events)
    for j in range(N):
        for c in range(RANK):move(f'X{j}_{c}_','Hub')
    for i in range(N):
        for c in range(RANK):move(f'Y{i}_{c}_','F'+str(RECEIVERS[i]))
    certificates=[];plane_form_add=0;plane_inplace_add=0;D_copy_add=0;K_inplace_add=0;receiver_add=0
    def decode_and_clear(q,i,v):
        nonlocal receiver_add
        t=len(events)
        for column in range(RANK):add(f'Y{i}_{column}_',q,v[column])
        receiver_add+=len(events)-t;clear(q)
    for j,k in combinations(range(N),2):
        h=planes[j,k];visible=[i for i in range(N)if i not in(j,k)];a,b,c,d,e=visible
        lifts={i:direct.lift(i,j,k)for i in visible}
        rows={i:[inv(dot(PHI[k],lifts[i])),inv(dot(PHI[j],lifts[i]))]for i in visible}
        candidates=[z for z,D in enumerate(Ds)if A[h]<=D]
        triples=[(a,d,e),(b,d,e),(a,b,c)]
        mids=[next(z for z in candidates if seen_by_D[z]==set(S))for S in triples]
        K=next(p for p,P in enumerate(A)if {RECEIVERS[d],RECEIVERS[e]}<=P)
        need(all(sum(x*y for x,y in zip(roots[u],roots[v]))==0 for mid in mids[:2]for u in Ds[mid]for v in A[K]),'both D4 flats lie in actual rank-six K')
        first=f'E{j}_{k}_';second=f'E{k}_{j}_'
        # Pay the third scalar output before overwriting the two owned queries.
        qc=f'Q{j}{k}_c_';init(qc,H(j,k));t=len(events)
        add(qc,first,rows[c][0]);add(qc,second,rows[c][1]);plane_form_add+=len(events)-t
        move(qc,'D'+str(mids[2]));move(qc,'F'+str(RECEIVERS[c]));decode_and_clear(qc,c,lifts[c])
        # Reuse the two owned source query records for the two shared messages.
        Hmatrix=[rows[a],rows[b]];Hword=inplace(first,second,Hmatrix);plane_inplace_add+=len(Hword)
        copies=[]
        for index,(query,pivot,mid)in enumerate([(first,a,mids[0]),(second,b,mids[1])]):
            move(query,'D'+str(mid));copy=f'M{j}{k}_{index}_';init(copy,'D'+str(mid));t=len(events);add(copy,query,1);D_copy_add+=len(events)-t
            move(copy,'K'+str(K));copies.append(copy)
            move(query,'F'+str(RECEIVERS[pivot]));decode_and_clear(query,pivot,lifts[pivot])
        Kmatrix=[list(solve2(rows[a],rows[b],rows[i]))for i in[d,e]]
        Kword=inplace(copies[0],copies[1],Kmatrix);K_inplace_add+=len(Kword)
        for query,i in zip(copies,[d,e]):move(query,'F'+str(RECEIVERS[i]));decode_and_clear(query,i,lifts[i])
        certificates.append({'pair':[j,k],'H':h,'receiver_order':[a,b,c,d,e],'D4_for_a_b_c':mids,'K6_dual_A2':K,'K6_receiver_roots':sorted(A[K]),'H_inplace_matrix':Hmatrix,'H_binary_ADD':Hword,'K_inplace_matrix':Kmatrix,'K_binary_ADD':Kword,'output_rows':{str(i):rows[i]for i in visible},'output_lifts':{str(i):lifts[i]for i in visible}})
    return {'schema':'literal-binary-record-seven-source-F8-D4-K6-merge-v1','native_donors':DONORS,'native_receivers':RECEIVERS,'plane_indices':[[j,k,h]for(j,k),h in sorted(planes.items())],'field_polynomial':direct.POLYNOMIAL,'field_degree':DEGREE,'bank_field_dimension':RANK,'source_forms':PHI,'merge_certificates':certificates,'ordinary_ADD_partition':{'source':source_add,'H_third_output':plane_form_add,'H_inplace_two_queries':plane_inplace_add,'D4_copy':D_copy_add,'K6_inplace_decoder':K_inplace_add,'receiver':receiver_add},'events':events}

def replay(w,word,semantic=True):
    A=[set(h)for h in w['A2']];Ds=[set(d)for d in w['D4']];R=w['root_table'];fields={};original={};order=[]
    for prefix,roles in [('X',DONORS),('Y',RECEIVERS)]:
        for j,role in enumerate(roles):
            for c in range(RANK):
                for name in names(f'{prefix}{j}_{c}_'):
                    n=len(order);order.append(name);original[name]=1<<n;fields[name]=[1<<n,('L'+str(role))if prefix=='X'else'G',False]
    def chart_rank(chart):return 0 if chart=='G'else 8 if chart=='Hub'else {'L':1,'H':2,'D':4,'K':6,'F':7}[chart[0]]
    def nested(a,b):
        if a=='G' or b=='Hub':return chart_rank(a)<chart_rank(b)
        if a[0]=='L'and b[0]=='H':return int(a[1:])in A[int(b[1:])]
        if a[0]=='H'and b[0]=='D':return A[int(a[1:])]<=Ds[int(b[1:])]
        if a[0]=='D'and b[0]=='K':return all(sum(x*y for x,y in zip(R[u],R[v]))==0 for u in Ds[int(a[1:])]for v in A[int(b[1:])])
        if a[0]=='K'and b[0]=='F':return int(b[1:])in A[int(a[1:])]
        if a[0]=='D'and b[0]=='F':return all(sum(x*y for x,y in zip(R[j],R[int(b[1:])]))==0 for j in Ds[int(a[1:])])
        return False
    counts=Counter();profile=Counter();owned_profile=Counter();dirty=0;peak=0;owned=set();seen=set(fields)
    for t,event in enumerate(word['events']):
        op=event[0];counts[op]+=1
        if op=='INIT':
            _,name,chart=event;need(name not in seen,'fresh auxiliary');seen.add(name);fields[name]=[0,chart,True];owned.add(name);peak=max(peak,len(owned))
        elif op=='ADD':
            _,dst,src=event;need(dst!=src and dst in fields and src in fields,'live distinct operands');need(fields[dst][1]==fields[src][1],f'ADD same chart at {t}');fields[dst][0]^=fields[src][0]
        elif op=='MOVE':
            _,name,chart=event;need(name in fields,'live move');old=fields[name][1];need(nested(old,chart),f'strict actual inclusion {old}->{chart}');gap=chart_rank(chart)-chart_rank(old);profile[gap]+=1
            if fields[name][2]:owned_profile[gap]+=1
            fields[name][1]=chart
        elif op=='CLEAR':
            _,name=event;need(name in owned,'owned clear');dirty+=bool(fields[name][0]);owned.remove(name);del fields[name]
        else:raise ValueError(op)
    need(not owned and set(fields)==set(original),'owned closure, originals retained');failures=[]
    for j in range(N):
        for c in range(RANK):
            for bit,name in enumerate(names(f'X{j}_{c}_')):
                if fields[name]!=[original[name],'Hub',False]:failures.append(name)
    for i in range(N):
        for c in range(RANK):
            for bit,name in enumerate(names(f'Y{i}_{c}_')):
                wanted=original[name]
                for j in range(N):
                    if j!=i:wanted^=original[names(f'X{j}_{c}_')[bit]]
                if fields[name]!=[wanted,'F'+str(RECEIVERS[i]),False]:failures.append(name)
    if semantic:need(not failures,'all-column source and receiver identity')
    return {'counts':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),'owned_upward_profile':dict(sorted(owned_profile.items())),'dirty_CLEAR':dirty,'peak_owned_binary_records':peak,'original_binary_columns':len(original),'semantic_failures':failures,'all_original_X_restored':not any(s.startswith('X')for s in failures),'all_arbitrary_Y_baselines_preserved':not failures,'all_42_foreign_blocks_identity':not failures,'final_rows':{name:fields[name][0]for name in order}}

def main():
    p=ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==direct.LAYOUT_HASH,'layout pin');w=json.loads(raw)
    word=build(w);res=replay(w,word);need(res['movement_profile']=={1:252,2:315,3:189,7:210},'complete paid K-merge movement profile')
    need(res['counts']['INIT']==res['counts']['CLEAR']==315 and res['peak_owned_binary_records']==129,'actual owned-query reuse invoice')
    mutant=json.loads(json.dumps(word));pos=next(p for p,e in enumerate(mutant['events'])if e[0]=='ADD'and e[1].startswith('M')and e[2].startswith('M'));mutant['events'].pop(pos)
    failed=replay(w,mutant,False)['semantic_failures'];need(failed,'omitted K decoder ADD detected')
    mutant=json.loads(json.dumps(word));pos=next(p for p,e in enumerate(mutant['events'])if e[0]=='MOVE'and e[2].startswith('K'));mutant['events'].pop(pos)
    try:replay(w,mutant);raise RuntimeError('missing K movement accepted')
    except ValueError as exc:badmove=str(exc)
    a.out.mkdir(parents=True,exist_ok=True);wr=json.dumps(word,separators=(',',':')).encode()+b'\n';(a.out/'WORD.json').write_bytes(wr)
    out={'status':'PASS_PAID_NATIVE_SEVEN_SOURCE_D4_K6_MERGE','layout_uncompressed_sha256':direct.LAYOUT_HASH,'word_sha256':sha256(wr).hexdigest(),'invoice':res,'ordinary_ADD_partition':word['ordinary_ADD_partition'],'field_source_queries':42,'field_H_to_D4_ports':63,'field_D4_to_K6_ports':42,'field_K6_to_F_deliveries':42,'field_direct_D4_to_F_deliveries':63,'inplace_H_and_K_matrices':42,'negative_controls':{'omitted_K_decoder_ADD_failures':failed,'omitted_K_MOVE':badmove},'full_balanced_source_constructed':False,'fixed_balanced_route_word_used':False,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],res['counts'],res['movement_profile'],'peak',res['peak_owned_binary_records'],word['ordinary_ADD_partition'])

if __name__=='__main__':main()
