#!/usr/bin/env python3
"""Exact independent recovery of the completed rail, both terminal cuts, and the two null star products."""
from collections import Counter,defaultdict
from fractions import Fraction as Q
from functools import reduce
from math import gcd,lcm
from pathlib import Path
import argparse,gzip,hashlib,json


def need(value,message):
    if not value:raise ValueError(message)


def add(u,v,z):
    for i,c in v.items():
        k=u.get(i,0)+z*c
        if k:u[i]=k
        else:u.pop(i,None)


def rank(rows):
    basis={}
    for row in rows:
        if not row:continue
        d=lcm(*(v.denominator for v in row.values()));v={k:int(x*d)for k,x in row.items()if x}
        while v:
            c=max(v)
            if c not in basis:
                basis[c]=v;break
            other=basis[c];g=gcd(v[c],other[c]);a=v[c]//g;b=other[c]//g
            v={k:x*b for k,x in v.items()};add(v,other,-a)
            if v:
                g=reduce(gcd,v.values())
                if g>1:v={k:x//g for k,x in v.items()}
    return len(basis)


def full_target(word,layout,rail):
    source={int(role):i for i,role in enumerate(layout['source_labels'])}
    pos={source[int(role)]:local for role,local in rail['source_role_map'].items()};native=len(word['initial']);first=word['first_output']
    co={f:{e:Q(z)for e,z in cols}for f,cols in word['forms']};v={~j:({j:1},1)for j in range(native)}
    for f in word['schedule']:
        den=lcm(*(r.denominator*v[e][1] for e,r in co[f].items()));row={}
        for e,r in co[f].items():add(row,v[e][0],r.numerator*(den//(v[e][1]*r.denominator)))
        g=reduce(gcd,row.values(),den);v[f]=({j:x//g for j,x in row.items()},den//g)
    target=[None]*400
    for i,l in pos.items():
        z,d=v[first+i];need(z.keys()<=pos.keys(),'an actual helper contributes unexpectedly');target[l]={pos[k]:Q(x,d)for k,x in z.items()}
    need(len(pos)==400 and None not in target,'400 original target labels')
    return target


def physical(word):
    n=word['public'];loc={i:c for i,c in enumerate(word['initial'])};state={i:{i:Q(1)}for i in range(n)};grades=Counter();ops=Counter();peak=0
    spans=[]
    for fr in word['frames']:
        q={0}
        for h in fr:q|={v^h for v in q}
        spans.append(q)
    for op in word['program']:
        typ,r=op[:2];ops[typ]+=1
        if typ=='MOVE':
            _,r,c,d,owned=op;need(loc[r]==c and owned==(r>=n),'MOVE ownership');need(spans[c]<spans[d] or (owned and spans[d]<spans[c]),'genuine comparable charts');grades[abs(len(word['frames'][c])-len(word['frames'][d]))]+=1;loc[r]=d
        elif typ=='ADD':
            _,r,t,x,c=op;need(r!=t and loc[r]==loc[t]==c,'ADD owners');add(state[r],state[t],Q(x))
        elif typ=='SCALE':
            _,r,x,c=op;need(loc[r]==c and Q(x),'SCALE owner');state[r]={i:y*Q(x)for i,y in state[r].items()}
        elif typ=='INIT':
            _,r,c=op;need(r>=n and r not in loc,'fresh INIT');loc[r]=c;state[r]={};peak=max(peak,len(loc)-n)
        elif typ=='CLEAR':
            _,r,c=op;need(loc[r]==c and r>=n,'proper CLEAR');del loc[r];del state[r]
        else:raise ValueError(typ)
    need(len(loc)==n,'all owned packets retired');return [state[i]for i in range(n)],[loc[i]for i in range(n)],grades,ops,peak


def compose(x,y):
    out=[]
    for row in x:
        h={}
        for i,c in row.items():add(h,y[i],c)
        out.append(h)
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();src=a.author/'sources'
    read=lambda d:json.loads(gzip.decompress(d.read_bytes()))
    base=read(src/'rail-base.json.gz');native=read(src/'DOUBLE-CANDIDATE.json.gz');layout=read(src/'LAYOUT.json.gz');complete=a.author/'output/COMPLETE-WORD.json.gz'
    need(hashlib.sha256(gzip.decompress((src/'DOUBLE-CANDIDATE.json.gz').read_bytes())).hexdigest()=='7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48','upstream #7830 source pin')
    target=full_target(native,layout,base);L,sites,basepay,baseops,peak0=physical(base);actual,ends,pay,ops,peak=physical(read(complete));need(actual==target and sites==ends,'all 160000 actual coefficients and final owners')
    corrections=[{int(i):Q(v)for i,v in row.items()}for row in read(src/'base-correction.json.gz')];need(compose(corrections,L)==target and rank(L)==400,'unique rational correction')
    groups=defaultdict(set);birth=defaultdict(set)
    for i,(g,b)in enumerate(zip(sites,base['initial'])):groups[g].add(i);birth[b].add(i)
    core=max(groups,key=lambda s:len(groups[s]));initial=max(birth,key=lambda s:len(birth[s]));need(core==127,'common terminal')
    allids=set(range(400));block=lambda mat,rows,cols:[{j:x for j,x in mat[i].items()if j in cols}for i in sorted(rows)]
    direct=[];send={};recv={};bcut=[];off1=[{}for _ in range(400)];off2=[{}for _ in range(400)]
    for g,idx in groups.items():
        send[g]=rank(block(corrections,allids-idx,idx));recv[g]=rank(block(corrections,idx,allids-idx));
        for i in idx:need({j:x for j,x in corrections[i].items()if j in idx}=={i:1},'terminal local identity')
        for h,jdx in groups.items():
            if g==h:continue
            v=block(corrections,jdx,idx)
            if not any(v):continue
            need(rank(v)==1 and (g==core or h==core),'remote rank-one star block');direct.append([g,h])
            off=off1 if g==core else off2
            for j,row in zip(sorted(jdx),v):off[j].update(row)
        if g!=core:
            forbidden=set().union(*(J for J in birth.values()if not any(set(target[i])&J for i in idx)));bcut.append(rank(block(L,idx,forbidden)))
    need(not any(compose(off1,off2)) and not any(compose(off2,off1)),'both opposite star products zero')
    st=rank(block(target,groups[core],birth[initial]));sl=rank(block(L,groups[core],birth[initial]));birthcut=sum(bcut)+max(0,st-sl)
    out={'native_word_sha256':hashlib.sha256(gzip.decompress(complete.read_bytes())).hexdigest(),'full_endpoint_equal_original_source':True,'independent_main_rows':rank(L),'remote_rank_one_pairs':len(direct),'terminal_outgoing_rank_sum':sum(send.values()),'incoming_rank_sum':sum(recv.values()),'birth_mixing_lower':birthcut,'target_and_rail_at_birth_to_hub':[st,sl],'annihilating_both_products':True,'complete_moves':ops['MOVE'],'complete_instructions':sum(ops.values()),'extra_grade_one':pay[1]-basepay[1],'original_and_complete_max_owned':[peak0,peak],'extra_peak_against_baseline':peak-peak0,'operation_histogram':ops}
    need(tuple(out[k]for k in ('remote_rank_one_pairs','terminal_outgoing_rank_sum','incoming_rank_sum','birth_mixing_lower','complete_moves','complete_instructions','extra_grade_one'))==(192,192,178,170,995,10644,192),'source counts and exact cuts');a.out.mkdir(exist_ok=True,parents=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out)
if __name__=='__main__':main()
