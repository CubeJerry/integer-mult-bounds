#!/usr/bin/env python3
"""Compile the seven-source code through three genuine D4 ports per plane."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json
import build as direct

N=direct.N
RANK=direct.RANK
DEGREE=direct.DEGREE
DONORS=direct.DONORS
RECEIVERS=direct.RECEIVERS
PHI=direct.PHI
need=direct.need
mul=direct.mul
inv=direct.inv
dot=direct.dot
names=direct.names

def solve2(a,b,target):
    determinant=mul(a[0],b[1])^mul(a[1],b[0]);q=inv(determinant)
    x=mul(q,mul(target[0],b[1])^mul(target[1],b[0]))
    y=mul(q,mul(a[0],target[1])^mul(a[1],target[0]))
    need([mul(x,a[c])^mul(y,b[c])for c in range(2)]==target,'two-message decoder')
    return x,y

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
    certificate=[];plane_add=0;copy_add=0;receiver_add=0
    for j,k in combinations(range(N),2):
        h=planes[j,k];visible=[i for i in range(N)if i not in(j,k)];a,b,c,d,e=visible
        lifts={i:direct.lift(i,j,k)for i in visible}
        rows={i:[inv(dot(PHI[k],lifts[i])),inv(dot(PHI[j],lifts[i]))]for i in visible}
        decoder={i:solve2(rows[a],rows[b],rows[i])for i in[d,e]}
        candidates=[z for z,D in enumerate(Ds)if A[h]<=D]
        histogram=Counter(len(seen_by_D[z])for z in candidates)
        need(len(candidates)==45 and max(histogram)==3,'native D4 visibility cap three')
        triple_counts={tuple(S):sum(seen_by_D[z]==set(S)for z in candidates)for S in combinations(visible,3)}
        need(all(v==2 for v in triple_counts.values()),'every receiver triple has two actual D4 flats')
        triples=[(a,d,e),(b,d,e),(a,b,c)]
        mids=[next(z for z in candidates if seen_by_D[z]==set(S))for S in triples]
        branches=[(a,mids[0],[(a,1),(d,decoder[d][0]),(e,decoder[e][0])]),(b,mids[1],[(b,1),(d,decoder[d][1]),(e,decoder[e][1])]),(c,mids[2],[(c,1)])]
        record={'pair':[j,k],'H':h,'visible_receivers':visible,'all_D4_visibility_histogram':dict(sorted(histogram.items())),'branches':[]}
        for branch,(pivot,mid,outputs)in enumerate(branches):
            q=f'Q{j}{k}_{branch}_';init(q,H(j,k));t=len(events)
            add(q,f'E{j}_{k}_',rows[pivot][0]);add(q,f'E{k}_{j}_',rows[pivot][1]);plane_add+=len(events)-t
            move(q,'D'+str(mid))
            for u,(i,coefficient)in enumerate(outputs):
                need(coefficient,'every delivered coordinate is used')
                if u+1==len(outputs):z=q
                else:
                    z=f'C{j}{k}_{branch}_{i}_';init(z,'D'+str(mid));t=len(events);add(z,q,1);copy_add+=len(events)-t
                move(z,'F'+str(RECEIVERS[i]));t=len(events)
                for column in range(RANK):add(f'Y{i}_{column}_',z,mul(coefficient,lifts[i][column]))
                receiver_add+=len(events)-t;clear(z)
            record['branches'].append({'message_target_receiver':pivot,'D4':mid,'D4_sees':sorted(seen_by_D[mid]),'plane_coefficients':rows[pivot],'outputs':[{'receiver':i,'coefficient':coef,'lift':lifts[i]}for i,coef in outputs]})
        clear(f'E{j}_{k}_');clear(f'E{k}_{j}_');certificate.append(record)
    return {'schema':'literal-binary-record-seven-source-F8-three-D4-ports-v1','native_donors':DONORS,'native_receivers':RECEIVERS,'plane_indices':[[j,k,h]for(j,k),h in sorted(planes.items())],'field_polynomial':direct.POLYNOMIAL,'field_degree':DEGREE,'bank_field_dimension':RANK,'parameters':direct.PARAMETERS,'source_forms':PHI,'shared_D4_certificates':certificate,'ordinary_ADD_partition':{'source':source_add,'plane':plane_add,'D4_copy':copy_add,'receiver':receiver_add},'events':events}

def replay(w,word):
    A=[set(h)for h in w['A2']];Ds=[set(d)for d in w['D4']];R=w['root_table'];fields={};original={};order=[]
    for prefix,roles in [('X',DONORS),('Y',RECEIVERS)]:
        for j,role in enumerate(roles):
            for c in range(RANK):
                for name in names(f'{prefix}{j}_{c}_'):
                    n=len(order);order.append(name);original[name]=1<<n;fields[name]=[1<<n,('L'+str(role))if prefix=='X'else'G',False]
    def chart_rank(chart):return 0 if chart=='G'else 8 if chart=='Hub'else 1 if chart[0]=='L'else 2 if chart[0]=='H'else 4 if chart[0]=='D'else 7
    def nested(a,b):
        if a=='G' or b=='Hub':return chart_rank(a)<chart_rank(b)
        if a[0]=='L'and b[0]=='H':return int(a[1:])in A[int(b[1:])]
        if a[0]=='H'and b[0]=='D':return A[int(a[1:])]<=Ds[int(b[1:])]
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
            _,name,chart=event;need(name in fields,'live move');old=fields[name][1];need(nested(old,chart),f'strict genuine inclusion {old}->{chart}');gap=chart_rank(chart)-chart_rank(old);profile[gap]+=1
            if fields[name][2]:owned_profile[gap]+=1
            fields[name][1]=chart
        elif op=='CLEAR':
            _,name=event;need(name in owned,'owned clear');dirty+=bool(fields[name][0]);owned.remove(name);del fields[name]
        else:raise ValueError(op)
    need(not owned and set(fields)==set(original),'helper closure')
    for j in range(N):
        for c in range(RANK):
            for bit,name in enumerate(names(f'X{j}_{c}_')):need(fields[name]==[original[name],'Hub',False],'X restoration')
    for i in range(N):
        for c in range(RANK):
            for bit,name in enumerate(names(f'Y{i}_{c}_')):
                wanted=original[name]
                for j in range(N):
                    if j!=i:wanted^=original[names(f'X{j}_{c}_')[bit]]
                need(fields[name]==[wanted,'F'+str(RECEIVERS[i]),False],'all-column receiver sum')
    return {'counts':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),'owned_upward_profile':dict(sorted(owned_profile.items())),'dirty_CLEAR':dirty,'peak_owned_binary_records':peak,'original_binary_columns':len(original),'all_original_X_restored':True,'all_arbitrary_Y_baselines_preserved':True,'all_42_foreign_blocks_identity':True,'final_rows':{name:fields[name][0]for name in order}}

def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();raw=gzip.decompress(args.layout.read_bytes());need(sha256(raw).hexdigest()==direct.LAYOUT_HASH,'pinned layout');w=json.loads(raw)
    word=build(w);res=replay(w,word);need(res['movement_profile']=={1:126,2:189,3:441,7:210},'paid shared-port invoice')
    args.out.mkdir(parents=True,exist_ok=True);wr=json.dumps(word,separators=(',',':')).encode()+b'\n';(args.out/'WORD.json').write_bytes(wr)
    out={'status':'PASS_PAID_NATIVE_SEVEN_SOURCE_THREE_D4_PORT_GADGET','layout_uncompressed_sha256':direct.LAYOUT_HASH,'word_sha256':sha256(wr).hexdigest(),'invoice':res,'ordinary_ADD_partition':word['ordinary_ADD_partition'],'field_source_ports':42,'field_H_to_D4_ports':63,'field_D4_to_F_deliveries':147,'all_pair_plane_H_D_port_count':3,'all_pair_plane_D_F_delivery_count':7,'full_balanced_source_constructed':False,'shared_existing_balanced_path_word_used':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],res['counts'],res['movement_profile'],'dirty',res['dirty_CLEAR'],'peak',res['peak_owned_binary_records'])

if __name__=='__main__':main()
