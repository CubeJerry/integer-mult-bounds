#!/usr/bin/env python3
"""Independent exact rational replay, source cuts and movement account.
@CubeJerry with OpenAI assistance. Apache-2.0. No author engine imported.
"""
import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(x,s):
    if not x:raise ValueError(s)

def span(frame):
    s={0}
    for v in frame:
        need(v not in s,'independent chart basis')
        s|={w^v for w in tuple(s)}
    return frozenset(s)

def plus(a,b,c):
    r=dict(a)
    for i,x in b.items():
        z=r.get(i,F(0))+c*x
        if z:r[i]=z
        else:r.pop(i,None)
    return r

def replay(w,mode='seed',controls=False):
    spaces=[span(f) for f in w['frames']]
    public=w['public'];rows={i:{i:F(1)}for i in range(public)};loc=dict(enumerate(w['initial']))
    raw=Counter();owned=Counter();counts=Counter();peak=0;lifetimes=0;trace={};retire=[]
    marks=w.get('echo',{}).get('markers',{})
    relays=w.get('echo',{}).get('relay_fields',[])
    entry=None
    for t,o in enumerate(w['program']):
        code=o[0];counts[code]+=1
        if code=='INIT':
            _,i,c=o;need(i>=public and i not in rows,'fresh owner');rows[i]={};loc[i]=c;lifetimes+=1
        elif code=='CLEAR':
            _,i,c=o;need(i>=public and loc[i]==c,'owned clear chart');retire.append((t,i,c,dict(rows[i])))
            if i in relays and mode not in ['dirty_echo','zero_erasure']:
                need(not rows[i],'declared clean relay not zero')
                C=w['echo']['C'];D=w['echo']['D']
                want=C if mode=='zero_roundtrip' and i==relays[0] else D
                need(c==want,'declared clean relay retirement chart')
            del rows[i];del loc[i]
        elif code=='MOVE':
            _,i,c,d,isowned=o;need(i in rows and loc[i]==c,'actual departure chart')
            need((spaces[c]<spaces[d] or spaces[d]<spaces[c]),'strict nested move')
            need(isowned==(i>=public),'owner classification')
            rank=abs(len(w['frames'][c])-len(w['frames'][d]));(owned if isowned else raw)[rank]+=1
            if mode=='dirty_echo' and i in relays and d==127:
                trace['borrowed_Hub_'+str(i)]=dict(rows[i])
            if mode=='seed' and i in [400,401] and d==127:
                trace['borrowed_Hub_'+str(i)]=dict(rows[i])
            loc[i]=d
        elif code=='ADD':
            _,i,j,c,f=o;need(loc.get(i)==f and loc.get(j)==f,'cocharted read')
            rows[i]=plus(rows[i],dict(rows[j]),F(c))
        elif code=='SCALE':
            _,i,c,f=o;need(loc.get(i)==f,'cocharted scale');rows[i]={j:F(c)*x for j,x in rows[i].items() if F(c)*x}
        else:raise ValueError('unrecognized instruction '+code)
        peak=max(peak,len(rows)-public)
        if t+1==marks.get('relay_entry'):entry={i:dict(rows[i])for i in relays}
        if t+1==marks.get('relay_restoration'):
            need(entry is not None,'real relay entry captured')
            need(all(rows[i]==entry[i]for i in relays),'restored exact dirty relay values')
            trace['relay_restoration']=True
    need(set(rows)==set(range(public)),'all owners retired')
    return rows,loc,dict(raw),dict(owned),dict(counts),peak,lifetimes,trace,retire

def main():
    z=argparse.ArgumentParser()
    z.add_argument('--package',type=Path,required=True)
    z.add_argument('--seed',type=Path,required=True)
    z.add_argument('--output',type=Path,required=True)
    a=z.parse_args()
    seed_bytes=a.seed.read_bytes()
    need(hashlib.sha256(seed_bytes).hexdigest()=='6281068be019f5f17ee9b64dd4f08323b00d1d3003b7ff3ccda6597ebe6265fc','seed source')
    seed=json.loads(gzip.decompress(seed_bytes));parent=replay(seed)
    native_raw=(a.package/'dependencies/native.json.gz').read_bytes()
    need(hashlib.sha256(native_raw).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','native source')
    native=json.loads(gzip.decompress(native_raw))
    role={int(k):v for k,v in seed['source_role_map'].items()}
    live=native['live']
    pairs={live[i]:(role[b],role[d])for i,b,d in zip(native['hosted']['Dports'],native['hosted']['X2'],native['hosted']['Y2'])}
    J=[32,48,85,98];T=[0,7,87,92]
    P=[F(1,2),F(-1,2),F(1,2),F(1,2)];Q=[-1,1,-1,1]
    def root(h):
        b=native['frames'][native['initial'][h]][0];on=[i for i in range(9)if b>>i&1]
        if len(on)==3:return [2 if i in on else -1 for i in range(9)]
        off=[i for i in range(9)if not(b>>i&1)]
        return [3*(int(i==off[0])-int(i==off[1]))for i in range(9)]
    need(all(Q[i]*P[j]==-F(sum(x*y for x,y in zip(root(h),root(k))),18)for i,h in enumerate(T)for j,k in enumerate(J)),'true Gram rectangle')
    expected=copy.deepcopy(parent[0])
    for i,h in enumerate(T):
        for j,k in enumerate(J):
            expected[role[h+112]]=plus(expected[role[h+112]],{role[k]:F(1)},Q[i]*P[j])
            expected[pairs[k][0]]=plus(expected[pairs[k][0]],{pairs[h][1]:F(1)},-Q[i]*P[j])
    results=[]
    for mode in ['dirty_echo','zero_roundtrip','zero_output_cleanup','zero_erasure','zero_echo']:
        folder=a.package/mode.replace('_','-')
        raw=(folder/'WORD.json.gz').read_bytes()
        w=json.loads(gzip.decompress(raw));r=replay(w,mode)
        need(r[0]==expected and r[1]==parent[1],'all400 public rows and endpoint charts')
        if mode=='dirty_echo':
            need(all(r[7]['borrowed_Hub_'+str(i)]==parent[7]['borrowed_Hub_'+str(i)]for i in [400,401]),'genuine borrowed Gram rows preserved')
        author=json.loads((folder/'RESULT.json').read_text())
        need({str(k):v for k,v in r[2].items()}==author['raw_histogram'],'raw invoice')
        need({str(k):v for k,v in r[3].items()}==author['owned_histogram'],'owned invoice')
        need(r[4]==author['source_bill']['counts'] and r[5]==author['source_bill']['peak'] and r[6]==author['source_bill']['lifetimes'],'ordinary and lifetime counts')
        controls=[]
        if mode=='zero_output_cleanup':
            b=copy.deepcopy(w);relay=b['echo']['relay_fields'][0]
            cache=b['echo']['cache_fields'][str(T[0])]
            idx=next(i for i,o in enumerate(b['program'])if o[0]=='ADD' and o[1:3]==[relay,cache])
            b['program'][idx][3]='0'
            try:replay(b,mode);rejected=False
            except ValueError as e:rejected='clean relay not zero' in str(e) or 'restored exact dirty' in str(e)
            need(rejected,'cleanup omission cannot pass clean-owner claim')
            controls.append('public-preserving-dirty-owner mutation rejected')
        if mode=='dirty_echo':
            b=copy.deepcopy(w);idx=b['echo']['markers']['A_inverse_end']-1
            need(b['program'][idx][0]=='ADD','inverse-stage witness')
            b['program'][idx][3]='0'
            try:bad=replay(b,mode);rejected=bad[0]!=expected
            except ValueError:rejected=True
            need(rejected,'inverse paired feedback required')
            controls.append('inverse-feedback mutation rejected')
        results.append(dict(mode=mode,word_sha256=hashlib.sha256(raw).hexdigest(),all400_rows=True,final_locations=True,raw=r[2],owned=r[3],ordinary_counts=r[4],peak=r[5],lifetimes=r[6],controls=controls))
    out=dict(status='PASS_INDEPENDENT_PAIRED_ECHO_SOURCE_REPLAY',seed_sha256=hashlib.sha256(seed_bytes).hexdigest(),proof_sha256=hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest(),variants=results,scope='Exact400-column rational replay and binary chart chronology. Introduced phases reproduced separately with retained engine; no all-column foundation discharge.')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(out['status'],len(results),'variants')
if __name__=='__main__':main()
