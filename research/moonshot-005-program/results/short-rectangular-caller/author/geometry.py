#!/usr/bin/env python3
"""Exact prospective HOST2 boundary geometry; not a native source."""
from pathlib import Path
import argparse,gzip,json,hashlib
from collections import Counter
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def dot(x,y):return (x&y).bit_count()%2
def basis(rows):
    piv={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k in piv:x^=piv[k]
            else:piv[k]=x;break
    return list(piv.values())
def ortho(q,h):
    need(dot(q,q)==1,'odd port')
    out=[q];W=basis([(1<<j)^(q if dot(1<<j,q)else 0)for j in range(h)])
    while W:
        characteristic=((1<<h)-1)
        for v in out:characteristic^=v
        candidate=next((w for w in W if dot(w,w)and(len(W)==1 or w!=characteristic)),None)
        if candidate is None:
            odd=next(w for w in W if dot(w,w));even=next(w for w in W if not dot(w,w));candidate=odd^even
        need(dot(candidate,candidate)==1 and(len(W)==1 or candidate!=characteristic),'nonalternating complement')
        out.append(candidate);W=basis([w^(candidate if dot(w,candidate)else 0)for w in W])
    need(len(out)==h and all(dot(x,y)==int(i==j)for i,x in enumerate(out)for j,y in enumerate(out)),'orthonormal basis')
    return out
def terms(vs):return Counter(vs)
def delta(A,B):
    C=A.copy()
    for v,c in B.items():C[v]-=c
    return {v:c for v,c in C.items()if c}
def signed(*pairs):
    C=Counter()
    for v,c in pairs:C[v]+=c
    return {v:c for v,c in C.items()if c}
def phase_translation(rows,h):
    weights=[sum((r>>j)&1 for r in rows)-1 for j in range(h)]
    need(all(w%2==0 for w in weights),'even phase difference')
    need(all(sum(((r>>i)&1)*((r>>j)&1)for r in rows)%2==0 for i in range(h)for j in range(i)),'no quadratic phase difference')
    return sum(((w//2)%2)<<j for j,w in enumerate(weights))
def main(source,caller,out):
    need(hashlib.sha256(source.read_bytes()).hexdigest()==PIN,'native source pin')
    W=json.loads(gzip.decompress(source.read_bytes()));C=json.loads(gzip.decompress(caller.read_bytes()))
    q0=[W['frames'][W['initial'][i]][0]for i in W['live']]
    need(len(q0)==104 and len(set(q0))==104 and len(basis(q0))==9 and all(dot(q,q)for q in q0),'actual live P104 labels')
    qs=[q<<(9*tag)for tag in range(2)for q in q0]
    need(len(set(qs))==208 and len(basis(qs))==18,'two-tag tensor labels')
    need(C['native_dimension']==18 and C['stages']>=2 and C['stages']%2==0 and C['roles']==2*C['stages']+2,'h18 two-chain shape')
    h=18;b=17;s=C['stages'];N=h+b*s;axes=[1<<j for j in range(N)];entries=[];contacts=0
    for q in qs:
        B=ortho(q,h);tr=phase_translation(B,h)
        for st in range(1,s+1):
            common=B[1:]+axes[h:h+(st-1)*b];fresh=axes[h+(st-1)*b:h+st*b]
            x0=terms(common+[q]);y0=terms(common);x1=terms(common+[q]+fresh);y1=terms(common+fresh)
            body=signed(*[(v,1)for v in fresh]);fw=signed((q,-1),*[(v,1)for v in fresh]);rv=signed((q,1),*[(v,1)for v in fresh])
            need(delta(x1,x0)==body and delta(y1,y0)==body,'both diagonal fresh bodies')
            need(delta(y1,x0)==fw and delta(x1,y0)==rv,'both absolute cross phases')
            need(len(basis(common+[q]+fresh))==h+st*b,'orthogonal native/common sum');contacts+=4
        entries.append(dict(label=q,basis=B,phase_translation=tr))
    target=Counter();idles=Counter()
    for ep in C['endpoint']:
        need(len(ep['stages'])==len(set(ep['stages'])) and ep['head_exponent']==-1,'whole target axes')
        target[1+b*len(ep['stages'])]+=len(qs)
    for e in C['events']:
        if e[0]=='IDLE_ONE':
            need(len(e[2])==len(set(e[2])),'whole idle axes');idles[b*len(e[2])]+=len(qs)
    need(all(q<(1<<h)for q in qs)and len(set(axes[h:]))==b*s,'head and all body axes disjoint')
    q=qs[0];B=ortho(q,h);common=B[1:];fresh=axes[h:h+b];old=terms(common)
    need(delta(terms(common+fresh),old)!=signed((q,1),*[(v,1)for v in fresh]),'missing head negative control')
    need(len(basis(common+[q]+fresh[:-1]+fresh[:1]))<h+b,'aliased fresh axis negative control')
    R=dict(status='PASS_SHORT_CALLER_BOUNDARY_GEOMETRY',native_pin=PIN,caller_pin=hashlib.sha256(caller.read_bytes()).hexdigest(),
      ports=208,native_dimension=h,stages=s,ambient=N,absolute_boundary_checks=contacts,
      all_type_A_field_assignments=208*s*4,target_histogram=dict(sorted(target.items())),idle_histogram=dict(sorted(idles.items())),
      control_missing_head_rejected=True,control_aliased_axis_rejected=True,
      scope='Exact prospective HOST2 boundary and whole-job geometry only; no h18 native word, decoder, or helper invoice is supplied.',port_bases=entries)
    raw=json.dumps(R,sort_keys=True,separators=(',',':')).encode();out.mkdir(parents=True,exist_ok=True)
    (out/'GEOMETRY.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    summary={k:v for k,v in R.items()if k!='port_bases'};summary['canonical_sha256']=hashlib.sha256(raw).hexdigest()
    (out/'GEOMETRY-SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('native',type=Path);p.add_argument('caller',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.native,a.caller,a.out)
