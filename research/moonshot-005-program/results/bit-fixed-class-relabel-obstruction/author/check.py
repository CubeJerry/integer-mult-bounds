#!/usr/bin/env python3
"""Authenticate the ordinary-class rational-uniqueness certificate."""
import argparse,gzip,hashlib,json
from pathlib import Path
def need(x,s):
    if not x:raise ValueError(s)
def rank(rows):
    piv={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in piv:piv[p]=x;break
            x^=piv[p]
    return len(piv)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    pp=base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    lr,pr=gzip.decompress(lp.read_bytes()),gzip.decompress(pp.read_bytes())
    need(hashlib.sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    lay=json.loads(lr);classes=json.loads(pr)['classes'];H=list(map(set,lay['A2']));D=list(map(set,lay['D4']));roots=lay['root_table'];native=set(range(111))
    ordinary=sorted(h for h,P in enumerate(H)if len(P&native)>=2)
    cp=Path(__file__).with_name('CERTIFICATE.json');cert=json.loads(cp.read_text())
    need(cert['ordinary_planes']==ordinary and len(ordinary)==1108,'ordinary variables')
    ix={(h,c):5*z+c for z,h in enumerate(ordinary)for c in range(5)}
    adj=[{j for j,y in enumerate(roots)if sum(u*v for u,v in zip(x,y))==0}for x in roots]
    class_at={};partition_tests=0
    for h in ordinary:
        ports=[d for d,M in enumerate(D)if H[h]<=M]
        cs=classes[str(h)];need(len(cs)==5 and all(len(c)==9 for c in cs),'five nine-port classes')
        need(sorted(sum(cs,[]))==ports,'complete actual partition')
        for i in range(120):
            if H[h]<=adj[i]:
                need(all(sum(D[d]<=adj[i]for d in c)==3 for c in cs),'actual class visibility');partition_tests+=1
        for c,ds in enumerate(cs):
            for d in ds:class_at[h,d]=c
    rows=[];sumrows=set();cut_count=0;cached={}
    for label in cert['selected_equations']:
        if label[0]=='sum':
            _,h=label;need(h in ordinary and h not in sumrows,'one ordinary sum row')
            sumrows.add(h);rows.append(sum(1<<ix[h,c]for c in range(5)));continue
        need(label[0]=='cut','equation type');_,d,j,k,i=label
        need(i in native and j in native and k in native and j!=k and i!=80 and j!=10 and k!=10,'unaltered identity pair')
        need(j in D[d]and k in D[d]and D[d]<=adj[i],'actual visible middle')
        for donor in [j,k]:
            key=i,donor
            if key not in cached:
                view=[h for h,P in enumerate(H)if donor in P and P<=adj[i]]
                need(len(view)==16 and all(h in ordinary for h in view),'tight ordinary source view');cached[key]=view
        hj=[h for h in cached[i,j]if H[h]<=D[d]]
        hk=[h for h in cached[i,k]if H[h]<=D[d]]
        need(len(hj)==len(hk)==4,'uniform rational witness has equal signed counts')
        need(all((h,d)in class_at for h in hj+hk),'actual local labels')
        row=0
        for h in set(hj)^set(hk):row^=1<<ix[h,class_at[h,d]]
        rows.append(row);cut_count+=1
    need(sumrows==set(ordinary)and len(rows)==5540,'square equation coverage')
    r=rank(rows);need(r==5540,'integer determinant odd via full binary rank')
    need(rank(rows[:-1])==5539,'missing equation control')
    result={'status':'PASS_FIXED_CLASS_RELABEL_RATIONAL_UNIQUENESS',
        'variables':5540,'equations':len(rows),'rank_mod2':r,'ordinary_planes':len(ordinary),
        'sum_equations':len(sumrows),'actual_D_cut_equations':cut_count,
        'tight_view_checks':len(cached),'actual_partition_receiver_checks':partition_tests,
        'unique_rational_value':'1/5','one_hot_possible':False,
        'negative_control_deleted_equation_rank':5539,
        'scope':'fixed nine-port partitions and common five class source decomposition; current target identity pairs only',
        'changed_partitions_and_mixed_ports':'not excluded','new_complete_kappa':False,
        'source_pins':[{'path':str(p.relative_to(a.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,pp,base/'bit-class-separated-middle-gate/author/PROOF.md']],
        'partition_payload_sha256':hashlib.sha256(pr).hexdigest(),'certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest()}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['variables','equations','rank_mod2','actual_D_cut_equations']}))
if __name__=='__main__':main()
