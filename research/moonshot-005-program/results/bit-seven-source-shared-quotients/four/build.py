#!/usr/bin/env python3
"""A paid F4 donor-dependent quotient gadget on actual native chart labels."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import gzip,json

LAYOUT_HASH='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
DONORS=[0,14,15,30]
RECEIVERS=[33,48,50,1]
V=[(1,0),(0,1),(1,1),(1,2)]
PHI=[(0,1),(1,0),(1,1),(2,1)]

def need(value,message):
    if not value:raise ValueError(message)
def mul(a,b):
    z=0
    while b:
        if b&1:z^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return z
def inv(a):
    need(a!=0,'nonzero denominator');return next(b for b in range(1,4)if mul(a,b)==1)
def dot(a,b):return mul(a[0],b[0])^mul(a[1],b[1])
def field_names(prefix):return [prefix+'b0',prefix+'b1']

def build(w):
    A=[set(h)for h in w['A2']]
    planes={(j,k):next(h for h,H in enumerate(A)if{DONORS[j],DONORS[k]}<=H)for j,k in combinations(range(4),2)}
    def H(j,k):return 'H'+str(planes[tuple(sorted((j,k)))])
    events=[]
    def put(*a):events.append(list(a))
    def init(p,chart):
        for x in field_names(p):put('INIT',x,chart)
    def move(p,chart):
        for x in field_names(p):put('MOVE',x,chart)
    def clear(p):
        for x in field_names(p):put('CLEAR',x)
    def add(dst,src,c):
        for k in range(2):
            v=mul(c,1<<k)
            for r in range(2):
                if v>>r&1:put('ADD',field_names(dst)[r],field_names(src)[k])
    for j in range(4):
        for k in range(4):
            if k==j:continue
            e=f'E{j}_{k}_';init(e,'L'+str(DONORS[j]))
            for c in range(2):add(e,f'X{j}_{c}_',PHI[k][c])
            move(e,H(j,k))
    for j in range(4):
        for c in range(2):move(f'X{j}_{c}_','Hub')
    for i in range(4):
        for c in range(2):move(f'Y{i}_{c}_','F'+str(RECEIVERS[i]))
    formula=[]
    for j,k in combinations(range(4),2):
        for i in range(4):
            if i in(j,k):continue
            l=next(n for n in range(4)if n not in(i,j,k))
            coefficients=[inv(dot(PHI[k],V[l])),inv(dot(PHI[j],V[l]))]
            z=f'Z{j}{k}_{i}_';init(z,H(j,k))
            add(z,f'E{j}_{k}_',coefficients[0]);add(z,f'E{k}_{j}_',coefficients[1])
            move(z,'F'+str(RECEIVERS[i]))
            for c in range(2):add(f'Y{i}_{c}_',z,V[l][c])
            clear(z)
            formula.append({'plane':[j,k],'receiver':i,'line':l,'plane_coefficients':coefficients,'decode_vector':V[l]})
        clear(f'E{j}_{k}_');clear(f'E{k}_{j}_')
    return {'schema':'literal-binary-record-tetrahedral-F4-v1','native_donors':DONORS,'native_receivers':RECEIVERS,'plane_indices':[[j,k,h]for(j,k),h in sorted(planes.items())],'field_polynomial':7,'line_vectors':V,'source_forms':PHI,'plane_formulas':formula,'events':events}

def replay(w,word,semantic=True):
    A=[set(h)for h in w['A2']];R=w['root_table'];fields={};original={};names=[]
    for prefix,roles in [('X',DONORS),('Y',RECEIVERS)]:
        for j,role in enumerate(roles):
            for c in range(2):
                for name in field_names(f'{prefix}{j}_{c}_'):
                    n=len(names);names.append(name);original[name]=1<<n
                    fields[name]=[1<<n,('L'+str(role))if prefix=='X'else'G',False]
    def rank(chart):return 0 if chart=='G'else 8 if chart=='Hub'else 1 if chart[0]=='L'else 2 if chart[0]=='H'else 7
    def nested(a,b):
        if a=='G' or b=='Hub':return rank(a)<rank(b)
        if a[0]=='L'and b[0]=='H':return int(a[1:])in A[int(b[1:])]
        if a[0]=='H'and b[0]=='F':return all(sum(x*y for x,y in zip(R[j],R[int(b[1:])]))==0 for j in A[int(a[1:])])
        return False
    counts=Counter();profile=Counter();owned_profile=Counter();dirty=0;peak=0;owned=set();seen=set(fields)
    for t,event in enumerate(word['events']):
        op=event[0];counts[op]+=1
        if op=='INIT':
            _,name,chart=event;need(name not in seen,'fresh auxiliary name');seen.add(name);fields[name]=[0,chart,True];owned.add(name);peak=max(peak,len(owned))
        elif op=='ADD':
            _,dst,src=event;need(dst!=src and dst in fields and src in fields,'live distinct operands');need(fields[dst][1]==fields[src][1],f'ADD same chart at{t}');fields[dst][0]^=fields[src][0]
        elif op=='MOVE':
            _,name,chart=event;need(name in fields,'live move');old=fields[name][1];need(nested(old,chart),f'strict genuine inclusion {old}->{chart}');gap=rank(chart)-rank(old);profile[gap]+=1
            if fields[name][2]:owned_profile[gap]+=1
            fields[name][1]=chart
        elif op=='CLEAR':
            _,name=event;need(name in owned,'owned clear');dirty+=bool(fields[name][0]);owned.remove(name);del fields[name]
        else:raise ValueError(op)
    need(not owned and set(fields)==set(original),'all helpers retired and originals retained')
    failures=[]
    for j in range(4):
        for c in range(2):
            for bit,name in enumerate(field_names(f'X{j}_{c}_')):
                if fields[name][0]!=original[name]or fields[name][1]!='Hub':failures.append(name)
    for i in range(4):
        for c in range(2):
            for bit,name in enumerate(field_names(f'Y{i}_{c}_')):
                wanted=original[name]
                for j in range(4):
                    if j!=i:wanted^=original[field_names(f'X{j}_{c}_')[bit]]
                if fields[name][0]!=wanted or fields[name][1]!='F'+str(RECEIVERS[i]):failures.append(name)
    if semantic:need(not failures,'all-column receiver/source identity: '+repr(failures))
    return {'counts':dict(sorted(counts.items())),'movement_profile':dict(sorted(profile.items())),'owned_upward_profile':dict(sorted(owned_profile.items())),'dirty_CLEAR':dirty,'peak_owned_binary_records':peak,'original_binary_columns':len(original),'final_rows':{name:fields[name][0]for name in names},'semantic_failures':failures}

def main():
    ap=ArgumentParser();ap.add_argument('--layout',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();raw=gzip.decompress(a.layout.read_bytes());need(sha256(raw).hexdigest()==LAYOUT_HASH,'pinned native layout');w=json.loads(raw)
    need(all(mul(a,b)==mul(b,a)for a in range(4)for b in range(4)),'field multiplication')
    need(all(dot(PHI[j],V[j])==0 for j in range(4)),'source kernels')
    need(all(dot(PHI[j],V[k])!=0 for j in range(4)for k in range(4)if j!=k),'four distinct projective lines')
    R=w['root_table'];geometry=[]
    for i,r in enumerate(RECEIVERS):
        dots=[sum(a*b for a,b in zip(R[r],R[j]))for j in DONORS];need([d==0 for d in dots]==[j!=i for j in range(4)],'native tetrahedral foreign visibility');geometry.append(dots)
    word=build(w);res=replay(w,word);need(res['movement_profile']=={1:24,5:24,7:32},'all private ports and public movements charged')
    controls={}
    for j,k in combinations(range(4),2):
        rows=[p['plane_coefficients']for p in word['plane_formulas']if p['plane']==[j,k]]
        determinant=mul(rows[0][0],rows[1][1])^mul(rows[0][1],rows[1][0]);need(determinant,'two genuinely distinct private plane outputs')
    mutant=json.loads(json.dumps(word));idx=next(t for t,e in enumerate(mutant['events'])if e[0]=='ADD'and e[1].startswith('Y'))
    mutant['events'].pop(idx);controls['omitted_receiver_ADD_failing_rows']=replay(w,mutant,False)['semantic_failures'];need(controls['omitted_receiver_ADD_failing_rows'],'coefficient omission detected')
    mutant=json.loads(json.dumps(word));idx=next(t for t,e in enumerate(mutant['events'])if e[0]=='MOVE'and e[1].startswith('E'))
    mutant['events'].pop(idx)
    try:replay(w,mutant);raise RuntimeError('missing source MOVE accepted')
    except ValueError as exc:controls['omitted_source_MOVE']=str(exc)
    controls['Y_baseline_columns']=sum(bool(row & (1<<n))for n,(name,row)in enumerate(res['final_rows'].items())if name.startswith('Y'))
    need(controls['Y_baseline_columns']==16,'all independent Y baseline columns present')
    a.out.mkdir(parents=True,exist_ok=True);wr=json.dumps(word,separators=(',',':')).encode()+b'\n';(a.out/'WORD.json').write_bytes(wr)
    out={'status':'PASS_PAID_NATIVE_TETRAHEDRAL_DONOR_KERNEL_GADGET','layout_uncompressed_sha256':LAYOUT_HASH,'word_sha256':sha256(wr).hexdigest(),'native_foreign_dots':geometry,'invoice':res,'negative_controls':controls,'field_inputs_per_donor':2,'field_outputs_per_receiver':2,'field_source_ports':12,'field_private_plane_ports':12,'full_balanced_source_constructed':False,'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],res['counts'],res['movement_profile'],'dirty',res['dirty_CLEAR'],'peak',res['peak_owned_binary_records'])
if __name__=='__main__':main()
