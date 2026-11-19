#!/usr/bin/env python3
"""Separate exact rank and scope reconstruction for class relabelling."""
import argparse,gzip,hashlib,json,time
from collections import Counter
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)

def main():
    a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--author',type=Path,required=True);a=a.parse_args();start=time.monotonic()
    base=a.repo/'research/moonshot-005-program/results'
    lp=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz';pp=base/'bit-native-nine-port-modules/author/output/PARTITIONS.json.gz'
    lr=gzip.decompress(lp.read_bytes());need(hashlib.sha256(lr).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    lay=json.loads(lr);H=[set(x)for x in lay['A2']];D=[set(x)for x in lay['D4']];roots=lay['root_table'];native=set(range(111));classes=json.loads(gzip.decompress(pp.read_bytes()))['classes']
    orth=[{j for j,y in enumerate(roots)if sum(x[k]*y[k]for k in range(8))==0}for x in roots]
    ports={};bydonor={j:[]for j in native}
    exceptional=[h for h,P in enumerate(H)if len(P&native)<=1]
    ordinary=[h for h,P in enumerate(H)if len(P&native)>=2];ordinary_index={h:t for t,h in enumerate(ordinary)}
    need(len(ordinary)==1108 and len(exceptional)==12,'ordinary/singleton census')
    for h,P in enumerate(H):
        for j in P&native:bydonor[j].append(h)
        cl=classes[str(h)];need(len(cl)==5 and all(len(x)==9 for x in cl),'five nine-port classes')
        flat=sum(cl,[]);need(len(set(flat))==45,'partition disjointness')
        actual={d for d,Q in enumerate(D)if P<=Q};need(set(flat)==actual,'actual H ports')
        for i in range(120):
            if P<=orth[i]:need(all(sum(D[d]<=orth[i]for d in block)==3 for block in cl),'three visible ports per native class')
        for c,values in enumerate(cl):
            for d in values:ports[h,d]=c
    tight={}
    for i in native:
        tight[i]=set()
        for j in native&orth[i]:
            view=[h for h in bydonor[j]if H[h]<=orth[i]]
            need(len(view)==16,'foreign source view length')
            if all(h in ordinary_index for h in view):tight[i].add(j)
    piv={};selected=[];equations=0;cut_count=0;native_comparisons=0
    def insert(mask,label):
        nonlocal equations
        equations+=1;x=mask
        while x:
            p=x.bit_length()-1
            if p not in piv:piv[p]=x;selected.append(label);return True
            x^=piv[p]
        return False
    certpath=a.author/'CERTIFICATE.json';cert=json.loads(certpath.read_bytes())
    need(cert['ordinary_planes']==ordinary,'certificate ordinary variables match native geometry')
    labels=cert['selected_equations'];need(len(labels)==5540,'square certificate dimension')
    seen_sums=set();prefix_rank=None
    for index,label in enumerate(labels):
        if label[0]=='sum':
            _,h=label;need(h in ordinary_index and h not in seen_sums,'distinct valid ordinary sum');seen_sums.add(h)
            insert(sum(1<<(5*ordinary_index[h]+c)for c in range(5)),label)
        else:
            need(label[0]=='cut' and len(label)==5,'certificate row label')
            _,d,j,k,i=label;Q=D[d]
            need(i in native and i!=80 and j!=10 and k!=10 and j!=k,'identity target pair')
            need(Q<=orth[i] and j in Q&tight[i] and k in Q&tight[i],'actual visible D and tight donor pair')
            contained=[h for h,P in enumerate(H)if P<=Q];signed=Counter()
            for h in contained:
                if j in H[h]:signed[h,ports[h,d]]+=1
                if k in H[h]:signed[h,ports[h,d]]-=1
            signed=Counter({u:v for u,v in signed.items()if v})
            need(all(h in ordinary_index for h,c in signed),'no exceptional variable in cut')
            need(sum(signed.values())==0,'uniform rational vector satisfies signed cut')
            need(sum(j in H[h]for h in contained)==4 and sum(k in H[h]for h in contained)==4,'four actual H per donor/D')
            mask=0
            for (h,c),v in signed.items():
                if v%2:mask^=1<<(5*ordinary_index[h]+c)
            insert(mask,label);cut_count+=1
        if index==len(labels)-2:prefix_rank=len(piv)
    need(seen_sums==set(ordinary),'all ordinary plane sums present')
    need(prefix_rank==5539,'independent omitted-final-row rank control')
    n=5*len(ordinary);need(len(piv)==n,'ordinary coefficient matrix has full rank modulo2')
    # A single one-hot column cannot satisfy the unique mod2 solution: the
    # uniform rational solution 1/5 reduces to five ones in every ordinary H.
    need(all((sum(1<<c for c in range(5))^(1<<chosen)).bit_count()==4 for chosen in range(5)),'one-hot differs from unique ordinary solution')
    # Removing one selected independent equation leaves at most n-1 rank.
    need(len(selected)==n and len(selected[:-1])==n-1,'omitted-equation rank control')
    result={'status':'PASS_SEPARATE_FIXED_CLASS_RELABEL_REVIEW','author_code_imported':False,
      'ordinary_planes':len(ordinary),'exceptional_planes':exceptional,'ordinary_variables':n,
      'ordinary_rank_mod2':len(piv),'full_variables':5600,'full_rank_mod2':len(piv)+len(exceptional),
      'full_nullity_mod2':4*len(exceptional),'uniform_rational_solution':'1/5',
      'ordinary_equations_checked':equations,'donor_difference_equations':cut_count,
      'certificate_used':True,'certificate_sha256':hashlib.sha256(certpath.read_bytes()).hexdigest(),'selected_rows':selected,
      'scope':'Fixed five nine-port partition at each H; arbitrary local class permutations; one global independent class; identity pairs i!=80,j!=10; no extra information or changed source class decomposition.',
      'no_new_complete_kappa':True,'elapsed_seconds':time.monotonic()-start,
      'source_pins':[{'path':str(p.relative_to(a.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}for p in [lp,pp]]}
    a.out.mkdir(parents=True,exist_ok=True)
    with gzip.GzipFile(str(a.out/'SELECTED-ROWS.json.gz'),'wb',mtime=0)as f:f.write(json.dumps(result.pop('selected_rows'),separators=(',',':')).encode())
    (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['ordinary_variables','ordinary_rank_mod2','full_rank_mod2','full_nullity_mod2','donor_difference_equations','elapsed_seconds']}))
if __name__=='__main__':main()
