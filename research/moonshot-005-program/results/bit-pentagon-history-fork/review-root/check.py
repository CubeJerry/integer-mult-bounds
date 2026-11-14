#!/usr/bin/env python3
"""Independent set-valued source replay of the two-lifetime pentagon fork."""
import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
IDS=[92,36,54,38,55]
def need(c,m):
    if not c:raise ValueError(m)
def dot(a,b):return sum(F(x)*F(y)for x,y in zip(a,b))
def rank(rows):
    a=[list(map(F,r))for r in rows];n=0
    for j in range(8):
        k=next((k for k in range(n,len(a))if a[k][j]),None)
        if k is None:continue
        a[n],a[k]=a[k],a[n];v=a[n][j];a[n]=[x/v for x in a[n]]
        for k in range(n+1,len(a)):
            v=a[k][j];a[k]=[x-v*y for x,y in zip(a[k],a[n])]
        n+=1
    return n
def replay(w):
    loc=dict(enumerate(w['start']));rows={i:{i}for i in range(222)};ever=set(rows);ops=Counter();moves=Counter();down=[];dirty=peak=0
    for at,e in enumerate(w['program']):
        op,r=e[:2];ops[op]+=1
        if op=='INIT':need(r>=222 and r not in ever,'fresh owner');ever.add(r);rows[r]=set();loc[r]=e[2];peak=max(peak,len(rows)-222)
        elif op=='ADD':
            _,r,s,c=e;need(r!=s and loc[r]==loc[s]==c,'literal cochart');rows[r]^=rows[s]
        elif op=='MOVE':
            _,r,a,b=e;need(loc[r]==a,'current chart');fa,fb=w['frames'][str(a)],w['frames'][str(b)];d=fb['dim']-fa['dim'];need(d and(r>=222 or d>0),'public ascent');sm,lg=(fa,fb)if d>0 else(fb,fa)
            need(all(dot(u,v)==0 for u in sm['B']for v in lg['A']),'actual chart containment');loc[r]=b;moves[abs(d)]+=1
            if d<0:down.append({'owner':r,'from_dimension':fa['dim'],'to_dimension':fb['dim'],'history':sorted(rows[r])})
        elif op=='CLEAR':need(r>=222 and loc[r]==e[2],'owned clear at actual chart');dirty+=bool(rows[r]);del rows[r];del loc[r]
        else:raise ValueError(op)
    return rows,loc,{'operations':dict(ops),'movement':dict(sorted(moves.items())),'downward':down,'dirty_clears':dirty,'peak_owners':peak}
def run(repo,package):
    raw=(repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');n=json.loads(gzip.decompress(raw));paths=[package/'PREFIX.json.gz',package/'CLOSED-PARTIAL.json.gz'];words=[json.loads(gzip.decompress(p.read_bytes()))for p in paths]
    w,c=words;need(c['program'][:len(w['program'])]==w['program'],'literal closure prefix');need(w['start']==n['start'][:222]and w['public']==222,'all original inputs')
    for key,frame in n['frames'].items():need(w['frames'][key]==frame,'native frames unchanged')
    for key,frame in w['frames'].items():
        if key not in n['frames']:need(rank(frame['B'])==frame['dim'] and rank(frame['A'])==8-frame['dim'] and all(dot(a,b)==0 for a in frame['A']for b in frame['B']),'new rational frame')
    r,l,b=replay(w);rr,ll,bb=replay(c)
    for i in range(111):
        target={111+i}^({i}if i in IDS else set())
        need(r[i]==rr[i]=={i}and l[i]==ll[i]==n['final'][i],'all X inputs restored')
        need(r[111+i]==rr[111+i]==target,'exact five targets and all independent Y baselines')
        need(l[111+i]==(n['final'][111+i]if i in IDS else n['start'][111+i]) and ll[111+i]==n['final'][111+i],'original Y charts')
    expected={222:set(IDS),223:{IDS[2],IDS[3]},224:{IDS[2],IDS[3]},225:{IDS[3]},226:{IDS[2]},227:{IDS[1]},228:{IDS[4]}}
    need(all(r[k]==v for k,v in expected.items())and set(r)==set(range(229)),'exact seven retained caches')
    need(set(rr)==set(range(222)) and bb['dirty_clears']==7 and bb['peak_owners']==7,'all actual retirements')
    need(bb['movement']=={1:9,2:2,5:2,6:7,7:215},'complete partial invoice')
    need({d['owner']for d in b['downward']}=={227,228},'exactly two descending lifetimes')
    for owner in(227,228):need([(d['from_dimension'],d['to_dimension'])for d in b['downward']if d['owner']==owner]==[(8,7),(7,6),(6,0)],'continuous whole Hub-to-ground route')
    need(b['operations']=={'INIT':7,'MOVE':129,'ADD':32},'prefix operations')
    def brank(rows):
        out={}
        for S in rows:
            x=sum(1<<i for i in S)
            while x:
                j=x.bit_length()-1
                if j in out:x^=out[j]
                else:out[j]=x;break
        return len(out)
    need(brank([d['history']for d in b['downward']])==4,'historical transfer rank four')
    need(brank([b['downward'][0]['history'],b['downward'][1]['history']])==2,'initial packet rank two')
    bad=json.loads(json.dumps(w));at=next(j for j,e in enumerate(bad['program'])if e[:3]==['ADD',222,228]);del bad['program'][at];rb,_,_=replay(bad);need(rb[111+IDS[3]]!={111+IDS[3],IDS[3]},'retained-history deletion fails branch target')
    return {'status':'PASS_INDEPENDENT_TWO_PACKET_PENTAGON_FORK','source_sha256':PIN,'prefix_sha256':hashlib.sha256(paths[0].read_bytes()).hexdigest(),'closure_sha256':hashlib.sha256(paths[1].read_bytes()).hexdigest(),'all_input_columns':222,'completed_targets':IDS,'initial_packet_rank':2,'downward_history_rank':4,'descending_lifetimes':2,'stationary_caches':5,'prefix':b,'closure':bb,'missing_retained_history_control':True,'complete_source':False,'no_new_kappa':True}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();d=run(a.repo,a.package);a.output.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items()if k not in('prefix','closure')}))
