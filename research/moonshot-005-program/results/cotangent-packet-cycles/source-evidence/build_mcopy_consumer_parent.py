#!/usr/bin/env python3
"""Explicit extension of pinned root m-copy builder for the B7+24 consumer rail.

Root builder SHA256 c1126456f16c748e9405450dabbd54824b80b2768c9f8072698484b09b881c73.
This separately named builder pins the newly composed Q; no root constant is changed.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import gzip, hashlib, importlib.util, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rail_exact',HERE/'source-evidence/extract_rail.py')
engine=importlib.util.module_from_spec(spec);spec.loader.exec_module(engine)
SOURCE_PIN=engine.SOURCE_PIN
RAIL_PIN='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc'
FULL_PIN='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
RAW={1:990,2:360,3:105,4:112,5:133,6:8,7:2}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def integer_root(a,n):
    lo,hi=0,1<<((a.bit_length()+n-1)//n)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**n<=a:lo=mid
        else:hi=mid
    need(lo**n<=a<(lo+1)**n,'Exact root enclosure');return lo
DEN=10**30
BOUNDS={}
def moment(profile):
    lo=hi=F(0)
    for rank,count in profile.items():
        r=int(rank)
        if r not in BOUNDS:
            q=integer_root(r**199*DEN**200,200);BOUNDS[r]=(F(q,DEN),F(q+1,DEN))
        a,b=BOUNDS[r]
        lo+=count*(a if count>=0 else b);hi+=count*(b if count>=0 else a)
    return lo,hi
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [clean(v) for v in x]
    return x
def remap(op,mapping,start,old_public):
    def role(r):return mapping[r] if r<old_public else start+r-old_public
    out=list(op);out[1]=role(out[1])
    if op[0] in ('ADD','COPY'):out[2]=role(out[2])
    return out
def main(a):
    need(a.copies>=2,'At least two copies')
    sb=(a.repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes()
    rb=(a.rail/'rail-consumer.json.gz').read_bytes()
    fb=(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json').read_bytes()
    need(sha(sb)==SOURCE_PIN and sha(rb)==RAIL_PIN and sha(fb)==FULL_PIN,'Pinned inputs')
    s,q=[json.loads(gzip.decompress(b)) for b in (sb,rb)];full=json.loads(fb)
    m=a.copies;p=1480+400*(m-1)
    roles={int(k):v for k,v in q['source_role_map'].items()};rev={v:k for k,v in roles.items()}
    need(len(roles)==400 and set(rev)==set(range(400)),'Full main domain')
    need(q['initial']==[s['initial'][rev[i]] for i in range(400)],'Initial chart interface')
    need(q['frames'][:len(s['frames'])]==s['frames'],'Shared chart identifiers')
    spaces=list(map(engine.span,q['frames']));owned=max(q['owned_fields'],s['owned_fields'])
    initial=s['initial']+q['initial']*(m-1);ops=[];blocks=[]
    for j in range(m-1):
        bank={i:1480+400*j+i for i in range(400)};start=len(ops)
        ops += [['ADD',bank[i],rev[i],'-1',q['initial'][i]] for i in range(400)]
        ops += [remap(o,bank,p,400) for o in q['program']]
        blocks.append({'copy':j+1,'start':start,'stop':len(ops)})
    start=len(ops)
    ops += [remap(o,{i:i for i in range(1480)},p,1480) for o in s['program']]
    stop=len(ops)
    for j in range(m-1):
        ops += [['ADD',1480+400*j+i,rev[i],'1',s['final'][rev[i]]] for i in range(400)]
    word={'public':p,'owned_fields':owned,'initial':initial,'frames':q['frames'],'program':ops,
          'source_sha256':sha(sb),'rail_sha256':sha(rb),'copies':m,'private_blocks':blocks,
          'common_block':[start,stop],'source_role_map':roles,
          'scope':'Exact fixed-m B7+24-consumer partial endpoint lift; not a complete native supplier.'}
    print('Running full shared word',m,p,len(ops),flush=True)
    actual,loc,bill=engine.run(ops,initial,p,owned,spaces,{i:{i:F(1)} for i in range(p)})
    print('Computing separately composed endpoint',flush=True)
    common,cloc,cbill=engine.run(s['program'],s['initial'],1480,s['owned_fields'],spaces,{i:{i:F(1)} for i in range(1480)})
    private,ploc,pbill=engine.run(q['program'],q['initial'],400,q['owned_fields'],spaces,{i:{i:F(1)} for i in range(400)})
    need(all(actual[i]==common[i] and loc[i]==cloc[i] for i in range(1480)),'Every common endpoint')
    for j in range(m-1):
        for i in range(400):
            target=dict(common[rev[i]])
            for k,c in private[i].items():target=engine.plus(target,{1480+400*j+k:c,rev[k]:-c})
            need(actual[1480+400*j+i]==target,'Every arbitrary-input private coefficient')
            need(loc[1480+400*j+i]==ploc[i]==s['final'][rev[i]],'Every final chart')
    need(bill['instructions']==cbill['instructions']+(m-1)*(pbill['instructions']+800),'All operations counted')
    expected=Counter(cbill['counts'])
    for typ,n in pbill['counts'].items():expected[typ]+=(m-1)*n
    expected['ADD']+=800*(m-1)
    need(bill['counts']==expected,'Ordinary histogram')
    need(bill['peak']==max(cbill['peak'],pbill['peak']),'Serial owned peak')
    need(bill['lifetimes']==cbill['lifetimes']+(m-1)*pbill['lifetimes'],'All lifetimes charged')
    T={int(k):v for k,v in full['invoice']['T'].items()};P={int(k):v for k,v in full['invoice']['P'].items()}
    H={int(k):v for k,v in full['native']['helpers'].items()};N={int(k):v for k,v in full['native']['paid'].items()}
    Q=pbill['moves'];G={r:N.get(r,0)-RAW.get(r,0) for r in set(N)|set(RAW)}
    tm={r:m*T.get(r,0)-18*(m-1)*H.get(r,0) for r in set(T)|set(H)}
    pm={r:m*P.get(r,0)-18*(m-1)*G.get(r,0)+18*(m-1)*(Q.get(r,0)-RAW.get(r,0)) for r in set(P)|set(G)|set(Q)|set(RAW)}
    need(all(v>=0 for v in tm.values()) and all(v>=0 for v in pm.values()),'Nonnegative complete profiles')
    alt={r:m*(P.get(r,0)-18*N.get(r,0))+18*bill['moves'].get(r,0) for r in set(P)|set(N)|set(bill['moves'])}
    need(all(pm.get(r,0)==alt.get(r,0) for r in set(pm)|set(alt)),'Independent full caller formula')
    signed={r:tm.get(r,0)-pm.get(r,0) for r in set(tm)|set(pm)};margin=moment(signed)
    perrail=[x/(18*(m-1)) for x in margin]
    payload=(json.dumps(word,sort_keys=True,separators=(',',':'))+'\n').encode();blob=gzip.compress(payload,mtime=0)
    a.output.mkdir(parents=True,exist_ok=True);(a.output/'WORD.json.gz').write_bytes(blob)
    result={'status':'PASS_EXACT_FIXED_MULTIPLICITY_PARTIAL_LIFT','copies':m,'input_directions':p,
      'ordinary_bill':bill,'T':tm,'P':pm,'productive_count':sum(tm.values()),'paid_count':sum(pm.values()),
      'rank_surplus':sum(r*c for r,c in signed.items()),'moment_bounds':margin,'per_rail_moment_bounds':perrail,
      'per_rail_moment_decimal':float(perrail[0]),'source_sha256':sha(sb),'rail_sha256':sha(rb),'full_caller_pin':sha(fb),
      'word_sha256':sha(blob),'word_payload_sha256':sha(payload),'complete_endpoint':False,'independent_review':'pending',
      'scope':'All arbitrary scalar inputs and formal full caller profiles; physical and uniform compiler, both strict suppliers and all foundations remain.'}
    (a.output/'RESULT.json').write_text(json.dumps(clean(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps(clean({k:result[k] for k in ['status','copies','ordinary_bill','per_rail_moment_decimal','word_payload_sha256']}),indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--rail',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--copies',type=int,required=True);main(ap.parse_args())
