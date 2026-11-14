#!/usr/bin/env python3
"""Exact source census and characteristic-zero minors for C2 mixed histories.

Author checker. Modular nonzero determinants certify rational independence;
all source rows, relations and classifications are checked over Fraction.
"""
from __future__ import annotations
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import numpy as np

PRIME=1000003
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc'
FOUR='20a5c2c3eccd000b757f65e2cd6bed7f8a9ec39f0b8f88a66716e4b818a2521f'

def need(test,message):
    if not test:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path,pin):
    b=path.read_bytes();need(sha(b)==pin,str(path)+' pin');return json.loads(gzip.decompress(b))
def add(a,b,c=F(1)):
    a=dict(a)
    for j,v in b.items():
        a[j]=a.get(j,F(0))+c*v
        if not a[j]:del a[j]
    return a
def scale(a,c):return {j:c*v for j,v in a.items() if c*v}
def span(frame):
    s={0}
    for x in frame:s|={v^x for v in tuple(s)}
    return s
class Basis:
    def __init__(self):self.rows={}
    def reduce(self,row):
        row=dict(row)
        for j,v in self.rows.items():
            if j in row:row=add(row,v,-row[j])
        return row
    def add(self,row):
        row=self.reduce(row)
        if row:
            p=min(row);self.rows[p]=scale(row,1/row[p]);return True
        return False

def replay(word,ops,callback=None):
    rows={j:{j:F(1)} for j in range(400)};loc=dict(enumerate(word['initial']));spaces=[span(f) for f in word['frames']];bill=Counter();counts=Counter();peak=0;life=0
    if callback:callback(-1,None,rows,loc)
    for t,o in enumerate(ops):
        ty,d=o[:2];counts[ty]+=1
        if ty=='INIT':
            need(d>=400 and d not in loc,'INIT');rows[d]={};loc[d]=o[2];life+=1
        elif ty=='CLEAR':
            need(d>=400 and loc.get(d)==o[2],'CLEAR');del rows[d];del loc[d]
        elif ty=='MOVE':
            a,b,owned=o[2:];need(loc.get(d)==a and owned==(d>=400),'MOVE source/ownership');need(spaces[a]<spaces[b] or owned and spaces[b]<spaces[a],'nested MOVE');loc[d]=b;bill[abs(len(word['frames'][a])-len(word['frames'][b]))]+=1
        elif ty in ('ADD','COPY'):
            s,c,at=o[2:];need(d!=s and loc.get(d)==loc.get(s)==at,'cochart ADD/COPY');need(ty!='COPY' or not rows[d],'zero COPY');rows[d]=add(rows[d],rows[s],F(c))
        elif ty=='SCALE':
            c,at=o[2:];need(F(c)!=0 and loc.get(d)==at,'SCALE');rows[d]=scale(rows[d],F(c))
        else:raise ValueError(ty)
        peak=max(peak,len(loc)-400)
        if callback:callback(t,o,rows,loc)
    need(len(loc)==400,'all owned records retired')
    return rows,loc,{'instructions':len(ops),'counts':dict(counts),'moves':dict(bill),'peak':peak,'lifetimes':life}

def modrow(row,columns):
    return np.array([(row.get(j,F(0)).numerator*pow(row.get(j,F(0)).denominator,-1,PRIME))%PRIME for j in columns],dtype=np.int64)
def select(rows):
    A=np.array(rows,dtype=np.int64)%PRIME;piv=[];rowlabels=list(range(len(A)));chosen=[];rank=0
    for col in range(A.shape[1]):
        k=next((k for k in range(rank,len(A)) if A[k,col]),None)
        if k is None:continue
        A[[rank,k]]=A[[k,rank]];rowlabels[rank],rowlabels[k]=rowlabels[k],rowlabels[rank]
        chosen.append(rowlabels[rank]);piv.append(col)
        A[rank]=A[rank]*pow(int(A[rank,col]),-1,PRIME)%PRIME
        if rank+1<len(A):A[rank+1:]=(A[rank+1:]-A[rank+1:,col,None]*A[None,rank,:])%PRIME
        rank+=1
        if rank==len(A):break
    return chosen,piv

def determinant(matrix):
    A=np.array(matrix,dtype=np.int64)%PRIME;n=len(A);need(A.shape==(n,n),'square minor');ans=1
    for j in range(n):
        k=next((k for k in range(j,n) if A[k,j]),None)
        if k is None:return 0
        if k!=j:A[[k,j]]=A[[j,k]];ans=-ans
        z=int(A[j,j]);ans=ans*z%PRIME;A[j]=A[j]*pow(z,-1,PRIME)%PRIME
        if j+1<n:A[j+1:,j:]=(A[j+1:,j:]-A[j+1:,j,None]*A[None,j,j:])%PRIME
    return ans%PRIME

def exact_rank(rows):
    b=Basis()
    for row in rows:b.add(row)
    return len(b.rows)

def main(a):
    native=load(a.native,NATIVE);parent=load(a.parent,PARENT);word=parent
    ops=parent['program'][:parent['consumer']['begin']]
    if a.variant=='four':
        word=load(a.four,FOUR)
        ops=[o for o,i in zip(word['program'],word['parent_event_of_output']) if i is None or i<parent['consumer']['begin']]
    need(word['public']==400 and word['frames']==parent['frames'],'same 400-input chart interface')
    roles={int(k):v for k,v in parent['source_role_map'].items()}
    host=sorted((native['live'][k],roles[b],roles[d]) for k,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2']))
    ds=[d for _,_,d in host];D=set(ds);ports=[h for h,_,_ in host]
    final,floc,bill=replay(word,ops);hub=[i for i in range(400) if floc[i]==127]
    H=Basis()
    for i in hub:H.add(final[i])
    need(len(hub)==len(H.rows)==200,'complete actual Hub rank200')
    need(all(H.reduce({d:F(1)})=={d:F(1)} for d in ds),'D coordinates survive quotient unchanged')
    for h,b,d in host:
        need(final[b].get(b,F(0))==1 and set(final[b])<={b}|D,'actual B endpoint is b plus pure D')
        need(final[d]=={d:F(1)},'actual D endpoint unchanged')
    E=[H.reduce(add({b:F(1),d:F(-1)},final[b],F(-1))) for h,b,d in host]
    need(exact_rank(E)==82,'actual stripped reverse residual82')
    def root(h):
        n=native['frames'][native['initial'][h]][0];ones=[i for i in range(9) if n>>i&1]
        if len(ones)==3:return [2 if i in ones else -1 for i in range(9)]
        zeros=[i for i in range(9) if i not in ones];need(len(zeros)==2,'native normal weight3 or7')
        return [3*(int(i==zeros[0])-int(i==zeros[1])) for i in range(9)]
    roots={h:root(h) for h in ports};frame=[5,56,65,69,77,96,100,103]
    G=[{d:F(sum(x*y for x,y in zip(roots[h],roots[k])),18) for k,_,d in host if sum(x*y for x,y in zip(roots[h],roots[k]))} for h in frame]
    need(exact_rank(G)==8,'orthogonal frame Gram rank8')
    for i,h in enumerate(frame):
        for j,k in enumerate(frame):need(G[i].get(host[ports.index(k)][2],F(0))==F(i==j),'genuine orthonormal frame')
    triples=np.array([(x,y,x^y) for x in range(1,512) for y in range(x+1,512) if y<(x^y)],dtype=np.int16)
    need(len(triples)==43435,'all C2 charts counted once')
    spaces=[span(f) for f in word['frames']];eligibility={}
    def eligible(x,y):
        key=(x,y)
        if key in eligibility:return eligibility[key]
        X,Y=spaces[x],spaces[y]
        if len(X)>len(Y):X,Y=Y,X
        if not X<=Y or len(X)>4 or len(Y)<4:ans=[]
        else:
            mem=np.array([z in Y for z in range(512)]);ok=mem[triples[:,0]]&mem[triples[:,1]]
            if len(X)==4:
                p,q,r=sorted(X-{0});ok&=(triples[:,0]==p)&(triples[:,1]==q)
            elif len(X)==2:
                z=next(z for z in X if z);ok&=np.any(triples==z,axis=1)
            ans=np.flatnonzero(ok).tolist()
        eligibility[key]=ans;return ans
    pool=[set() for _ in triples];table=[];keys={};events=[]
    def add_row(t,role,row,charts):
        if not charts:return
        r=H.reduce(row)
        if not r:return
        r=scale(r,1/r[min(r)]);key=tuple(sorted(r.items()))
        if key not in keys:keys[key]=len(table);table.append(r)
        idx=keys[key]
        for c in charts:pool[c].add(idx)
        events.append({'event':t,'role':role,'row':idx,'eligible_charts':len(charts)})
    hub_history_checks=0
    def capture(t,o,rows,loc):
        nonlocal hub_history_checks
        for role in (list(loc) if o is None else [] if o[0]=='CLEAR' else [o[1]]):
            if loc[role]==127:
                need(not H.reduce(rows[role]),'every actual historical Hub row is in the final Hub span')
                hub_history_checks+=1
        if o is None:
            for r,c in loc.items():
                if len(word['frames'][c])==2:add_row(t,r,rows[r],eligible(c,c))
        elif o[0]=='MOVE':add_row(t,o[1],rows[o[1]],eligible(o[2],o[3]))
        elif o[0]!='CLEAR' and len(word['frames'][loc[o[1]]])==2:
            c=loc[o[1]];add_row(t,o[1],rows[o[1]],eligible(c,c))
    replay(word,ops,capture)
    kinds=[];units={};nuisance={}
    for i,r in enumerate(table):
        nonD=set(r)-D
        if nonD:
            need(len(nonD)==1 and len(r)==1,'nuisance rows are pure distinct original Y')
            j=next(iter(nonD));need(j not in nuisance,'no duplicate nuisance direction');nuisance[j]=i;kinds.append('Y')
        elif len(r)==1:units[i]=next(iter(r));kinds.append('D')
        else:kinds.append('M')
    need(len(nuisance)==104,'all104 irrelevant original-Y directions distinguished')
    cache={};certificates=[];distribution=Counter();maxclean=0;rawranks=Counter()
    for c,ids in enumerate(pool):
        known=tuple(sorted(units[i] for i in ids if kinds[i]=='D'));mixed=tuple(sorted(i for i in ids if kinds[i]=='M'));maxclean=max(maxclean,len(known));distribution[len(mixed)]+=1
        need(len(known)<=35,'clean D support cap')
        if not mixed:continue
        key=(known,mixed)
        if key in cache:continue
        keep=[d for d in ds if d not in known]
        M=[{d:v for d,v in table[i].items() if d in keep} for i in mixed]
        # An exact upper rank witness, not a modular-rank upper bound.
        exact=Basis();chosen=[]
        for j,r in enumerate(M):
            if exact.add(r):chosen.append(j)
        r=len(chosen);rawranks[len(mixed),r]+=1
        mr=[M[j] for j in chosen];gr=[{d:v for d,v in row.items() if d in keep} for row in G]
        mat=[modrow(row,keep) for row in mr+gr]
        _,columns=select(mat);need(len(columns)==r+8,'Gram and mixed spaces disjoint after deleting clean coordinates')
        det=determinant(np.array(mat)[:,columns]);need(det!=0,'exact nonzero rational minor')
        entry={'chart':triples[c].tolist(),'known_D_roles':list(known),'mixed_rows':list(mixed),'exact_mixed_rank':r,'chosen_mixed_indices':chosen,'minor_original_columns':[keep[j] for j in columns],'minor_mod_prime':det}
        cache[key]=len(certificates);certificates.append(entry)
    need(maxclean==35,'sharp inherited clean envelope')
    # The no-mixed cases are certified directly as well, independently of
    # invoking the inherited minimum-distance theorem. One rational 8-minor
    # per distinct clean-coordinate set is retained by its deterministic hash.
    clean_cache={}
    for ids in pool:
        if any(kinds[i]=='M' for i in ids):continue
        known=tuple(sorted(units[i] for i in ids if kinds[i]=='D'))
        if known in clean_cache:continue
        keep=[d for d in ds if d not in known];mat=[modrow(row,keep) for row in G];_,columns=select(mat);need(len(columns)==8,'pure-coordinate chart disjoint from Gram');det=determinant(np.array(mat)[:,columns]);need(det,'pure-coordinate rational minor')
        clean_cache[known]={'known_D_roles':list(known),'minor_original_columns':[keep[j] for j in columns],'minor_mod_prime':det}
    need(sum(distribution.values())==43435,'complete chart census')
    reduced_rows=[{str(j):str(v) for j,v in sorted(r.items())} for r in table]
    canonical_pools=[sorted(s) for s in pool]
    controls={}
    # The true demand must be eight-dimensional; adding an exact Gram row
    # as one free local record is an explicit positive escape control.
    B=Basis()
    B.add(G[0]);local_rank=len(B.rows)
    for r in G:B.add(r)
    controls['free_Gram_row_creates_intersection']=local_rank+8-len(B.rows)==1
    need(controls['free_Gram_row_creates_intersection'],'positive synthetic control')
    augmented=np.array([modrow(row,ds) for row in [G[0]]+G]);_,piv=select(augmented)
    need(len(piv)==8<9,'a free Gram observation must invalidate the zero-intersection minor')
    controls['free_Gram_row_breaks_augmented_independence']=True
    dirty_hub=next((row for row in H.rows.values() if any(j in D for j in row)),None)
    need(dirty_hub is not None and H.reduce(dirty_hub)=={},'raw D coefficients alone falsely credit a known Hub row')
    controls['raw_D_credit_without_Hub_conditioning_rejected']=True
    wrong=modrow(G[0],ds);wrong_minor=determinant(np.array([wrong]*8)[:,list(range(8))]);need(wrong_minor==0,'duplicate-row rejection');controls['duplicate_Gram_minor_rejected']=True
    result={'status':'PASS_C2_PASSIVE_HISTORY_ZERO_GRAM_INTERSECTION','variant':a.variant,'native_sha256':NATIVE,'parent_sha256':PARENT,'word_sha256':PARENT if a.variant=='parent' else FOUR,'stripped_program_operations':len(ops),'actual_Hub_rank':len(H.rows),'historical_Hub_rows_checked':hub_history_checks,'all_Hub_history_contained_in_final_Hub':True,'actual_reverse_residual_rank':82,'target_Gram_rank':8,'total_C2_charts':43435,'nonempty_pools':sum(bool(x) for x in pool),'distinct_reduced_rows':len(table),'row_types':dict(Counter(kinds)),'mixed_population_distribution':dict(distribution),'mixed_exact_rank_distribution':{str(k):v for k,v in rawranks.items()},'maximum_clean_D_positions':maxclean,'mixed_minors':len(certificates),'clean_minors':len(clean_cache),'prime':PRIME,'all_effective_local_Gram_intersections_zero':True,'source_bill':bill,'negative_controls':controls,'scope':'Exact source histories and arbitrary C2 refinements of original MOVEs, with immortal local caches and all mutually incompatible refinements jointly granted. No changed source mixing or arbitrary gauges are included. Characteristic-zero consequence follows from exact rational dependencies and nonzero modular minors. Actual source remains rank82, incomplete, and not a supplier.'}
    a.output.mkdir(parents=True,exist_ok=True)
    for name,obj in [('RESULT.json',result),('ROWS.json',reduced_rows),('POOLS.json',canonical_pools),('EVENTS.json',events),('MIXED-MINORS.json',certificates),('CLEAN-MINORS.json',list(clean_cache.values()))]:
        raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode();(a.output/(name+'.gz')).write_bytes(gzip.compress(raw,mtime=0))
    (a.output/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--four',type=Path);p.add_argument('--variant',choices=['parent','four'],default='parent');p.add_argument('--output',type=Path,required=True);main(p.parse_args())
