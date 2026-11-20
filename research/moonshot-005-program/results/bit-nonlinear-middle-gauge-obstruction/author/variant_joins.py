#!/usr/bin/env python3
"""Exact mixed-D original-fibre join certificates for additional frozen physical source words."""
from argparse import ArgumentParser
from collections import Counter
import gzip
from hashlib import sha256
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import random
import numpy as np
BASE_REGULAR={49:3,97:1,53:1,77:7,93:1,8:1,82:3,58:2,106:1,31:1,105:1}
VARIANTS=('ordinary','H263','retuned_D120','D120_36','D120_132','packed_23','packed_24','packed_30','packed_31')
def require(ok,why):
    if not ok:raise ValueError(why)
def load_mod(path,name):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
def load_json(path,pin=None,compressed=False,pin_raw=False):
    raw=path.read_bytes()
    if pin and not pin_raw:require(sha256(raw).hexdigest()==pin,'literal '+path.name)
    if compressed:raw=gzip.decompress(raw)
    if pin and pin_raw:require(sha256(raw).hexdigest()==pin,'coefficient '+path.name)
    return json.loads(raw)
def packed_frames(r,n,f,compiler,par,repairs,label):
    if label in ('packed_23','packed_24'):
        cfg=par['native_all_views_packing' if label=='packed_23' else 'extended_ordinary_packing']
        pairs=[par['pair']]
        single=[(h,next(p for p in par['one_centre'] if p['H']==h and p['k']==3)) for h in cfg if h not in pairs[0]['centres']]
    else:
        cfg=par['singleton_free_30' if label=='packed_30' else 'complete_31'];lookup={tuple(z['centres']):z for z in par['pairs']}
        pairs=[lookup[h,q] for h,q,_ in cfg['pairs']];single=[(h,par['one_centre']['3'])for h in cfg['singles']]
    groups=[]
    for p in pairs:
        charts=[r.Chart(n,z,3) for z in p['centres']];groups.append((charts,r.paired(charts,p['3']),p['3']['early']))
    for h,p in single:
        c=r.Chart(n,h,3);groups.append(([c],c.single(p),p['early']))
    table={}
    for charts,maps,seeds in groups:
        centres={c.h for c in charts}
        for j,source in maps.items():
            c=next(c for c in charts if j in c.donors)
            for h,F in source.items():
                q=n.early[j,h]//15
                if q==3:
                    repair=repairs[c.h,j,3];require(h==repair['singleton'],'genuine literal singleton');B=np.asarray(repair['S'],dtype=np.uint8)
                else:
                    B=np.kron(np.eye(2,dtype=np.uint8),F)
                    if q==1:
                        E=np.eye(6,dtype=np.uint8)[:3] if h in centres else r.pseudo(f'early/{c.h}/3/{j}/{h}/{seeds[str(j)]}',3,6)
                        C=np.eye(6,dtype=np.uint8)[compiler.late_indices(E,f)];B=f.matmul(np.vstack([E,C]),B)
                require((j,h) not in table,'one true donor star');table[j,h]=B
    return table
def add_tables(n,table):
    regular=n.frame;n.c.donors=[]
    def frame(j,h,t,q,half):return table[j,h] if (j,h) in table else regular(j,h,t,q,half)
    n.frame=frame
    return sorted({j for j,h in table})
def variant_inputs(label,a,root,r,f,middle,compiler):
    coeff=load_json(root/'bit-spread-h263-source/author/output/COEFFICIENTS.json.gz','66fe6820e16e2a1a221cc59656b6356087f92b685ff121ef174a67c7c4890a0e',True,True)
    words={'frames':[],'gauges':[]}
    if label=='retuned_D120':
        words=load_json(root/'bit-spread-isolated-middle-cut/author/output/WORDS.json.gz','f185c1d220f258b88159f50bcafe47c1b0fde53439320eb5d9313d06e74bc970',True,True)
    n=middle.NativeLeft(a.repo,r,f,coeff,words,BASE_REGULAR)
    if label=='ordinary':n.c.donors=[];return n,[0,61,62]
    if label=='H263':return n,list(n.c.donors)
    if label=='retuned_D120':return n,sorted(set(n.c.donors)|set(n.gauges))
    if label.startswith('packed_'):
        if label in ('packed_23','packed_24'):
            par=load_json(root/'bit-spread-overlap-source/author/output/PARAMETERS.json')
            entries=load_json(root/'bit-spread-singleton-fibre-repair/author/output/SINGLETON-COEFFICIENTS.json.gz','976d9558f33122618cc0001a8f92623893497f2e1d548000b2c8f801c2b32413',True)
        else:
            p=root/'bit-spread-two-centre-packing/author/output'
            par=load_json(p/'PARAMETERS.json','972939d6c9937d1c18cf90f69399112bf2c9c95eab1b194186b164a2331f5d6c')
            entries=load_json(p/'SINGLETONS.json.gz','107eb64f87489ee31b2fae02f3f93d512bd5a5cf2485d78181dd825d35d21526',True)
        repairs={(v['h'],v['donor'],v['k']):v for v in entries};table=packed_frames(r,n.n,f,compiler,par,repairs,label)
    else:
        name,pin=(('TABLES.json.gz','688380f3b2e65521d6abff2e9267b6460039325bfc60c5b05a4c5cffa052c5d8') if label=='D120_36' else ('ALL-RECEIVERS.json.gz','3d2fbd7fc6eb74e006d6910f812d6d1a7487cf47c59d75844e08b69c8dd98747'))
        spec=load_json((a.facet_tables or root/'bit-spread-d120-facet-fibres/author/output')/name,pin,True);table={}
        for js,v in spec['stars'].items():
            for hs,F in v['F'].items():
                h,j=int(hs),int(js);B=f.matmul(np.asarray(v['P'][hs],dtype=np.uint8),np.kron(np.eye(2,dtype=np.uint8),np.asarray(F,dtype=np.uint8)))
                if n.n.early[j,h]==45:B=np.vstack([B,np.asarray(v['Q'][hs],dtype=np.uint8)])
                table[j,h]=B
    return n,sorted(set(add_tables(n,table))|{0,61,62})
def physical_fibres(n,j,ops):
    source=n.rows(j);stars=[d for d in n.n.marked if j in n.n.D[d]];tables={}
    for d in stars:
        rows=[source[t] for t in n.mid[d] if t in source];require(len(rows)==8,'actual eight marked carriers');tables[d]=np.stack(rows)
    ans={};count=0
    for i in sorted((n.n.adj[j]&set(range(111)))-{80}):
        ds=sorted(d for d in stars if n.n.D[d]<=n.n.adj[i]);require(len(ds)==12,'actual native edge')
        A=np.vstack([tables[d] for d in ds]);rank,X=ops.reduce(A,True);require(rank==96,'complete frozen physical marked cut')
        if count%29==0:require(np.array_equal(n.f.matmul(A,X),np.eye(96,dtype=np.uint8)),'complete native inverse columns')
        count+=1
        for t,d in enumerate(ds):ans[d,i]=X[:,8*t:8*t+8].T.copy()
    return ans,count
def witness(fib,j,k,ops,candidate,discover):
    A,B=fib[j],fib[k];common=sorted(A.keys()&B.keys())
    def ranks(labels):return (ops.reduce(np.vstack([A[t] for t in labels])),ops.reduce(np.vstack([B[t] for t in labels])))
    if candidate:
        labels=[tuple(v) for v in candidate[4]];require(len(set(labels))==len(labels)==12 and set(labels)<=set(common),'actual common native labels');a,b=ranks(labels)
        if discover and a!=b:return [j,k,a,b,labels]
        if not discover:
            require([a,b]==candidate[2:4] and a!=b,'literal original-join discrepancy');return [j,k,a,b,labels]
    require(discover,'missing exact clique certificate');rng=random.Random(811920+j*111+k)
    for _ in range(4096):
        ix=sorted(rng.sample(range(len(common)),12));labels=[common[t]for t in ix];a,b=ranks(labels)
        if a!=b:return [j,k,a,b,labels]
    return None
def resolved(path,base_dir,visited=None):
    info=load_json(path,compressed=True)
    if isinstance(info,list):return info
    visited=set() if visited is None else visited
    require(path not in visited,'acyclic finite variant inheritance');visited.add(path)
    parent=info['inherits']
    earlier=(base_dir/'PAIR-WITNESSES.json.gz') if parent=='base' else path.parent/(parent+'.json.gz')
    data={tuple(v[:2]):v for v in resolved(earlier,base_dir,visited)}
    changed=set()
    for row in info['changes']:
        key=tuple(row[:2]);require(key not in changed,'unique changed pair');changed.add(key);data[key]=row
    return [data[k] for k in sorted(data)]

def main():
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--fibres',type=Path,required=True);p.add_argument('--library',type=Path);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--variant',choices=VARIANTS,required=True);p.add_argument('--canonical',action='store_true',help='test the separate canonical contact target, including donor 10');p.add_argument('--discover',action='store_true');p.add_argument('--facet-tables',type=Path);p.add_argument('--witness-dir',type=Path);p.add_argument('--base-witness-dir',type=Path)
    a=p.parse_args();root=a.repo/'research/moonshot-005-program/results';here=Path(__file__).parent
    f=load_mod(root/'bit-spread-h263-source/review/check.py','field');r=load_mod(root/'bit-spread-overlap-source/review/check.py','geometry');m=load_mod(root/'bit-spread-isolated-middle-cut/review/check.py','left')
    compiler=load_mod(root/'bit-spread-packed-source-owner-compiler/author/compile_pack.py','physical_source')
    ranks=load_mod(here/'census.py','rank_engine');ops=ranks.Elim(f,a.library);n,changed=variant_inputs(a.variant,a,root,r,f,m,compiler)
    data=np.load(a.fibres);fib={};digest=sha256()
    for key,Q in zip(data['indices'],data['matrices']):
        d,j,i=map(int,key);fib.setdefault(j,{})[d,i]=Q;digest.update(key.astype('>i2').tobytes());digest.update(Q.tobytes())
    require(digest.hexdigest()=='c87f3ff6cd51c57af1fe3dd1a444f864631bd146363a92aad17409afe3acb47f','native ordinary inventory')
    counts={}
    for j in sorted(set(changed)|({10} if a.canonical else set())):
        if a.canonical or j!=10:fib[j],counts[j]=physical_fibres(n,j,ops)
    donors=sorted(set(range(111))-(set() if a.canonical else {10}));require(sorted(fib)==donors,'every native identity-active donor')
    wdir=a.witness_dir or here/'variants';name=('canonical-' if a.canonical else '')+a.variant;fixture=wdir/(name+'.json.gz')
    inp=fixture if not a.discover else (wdir/(a.variant+'.json.gz') if a.canonical else (a.base_witness_dir or here)/'PAIR-WITNESSES.json.gz')
    records=resolved(inp,a.base_witness_dir or here);previous={(row[0],row[1]):row for row in records}
    out=[];miss=[];hist=Counter();aggregate=sha256()
    for j,sub in sorted(fib.items()):
        for (d,i),U in sorted(sub.items()):
            aggregate.update(np.array([j,d,i],dtype='>i2').tobytes());aggregate.update(U.tobytes())
    for j,k in combinations(donors,2):
        got=witness(fib,j,k,ops,previous.get((j,k)),a.discover)
        if got is None:miss.append([j,k]);continue
        out.append(got);hist[','.join(map(str,sorted(got[2:4])))]+=1
    if a.discover:
        wdir.mkdir(parents=True,exist_ok=True)
        emitted={'inherits':a.variant,'changes':[q for q in out if previous.get(tuple(q[:2]))!=json.loads(json.dumps(q))]} if a.canonical else out
        fixture.write_bytes(gzip.compress(json.dumps(emitted,separators=(',',':')).encode(),mtime=0))
    else:require(len(records)==len(previous)==len(out),'every literal witness accounted for')
    a.out.mkdir(parents=True,exist_ok=True);sz=sum(len(q) for q in fib.values())
    result={'source_variant':a.variant,'donors':len(donors),'identity_receivers_excluded':[80],'modified_input_excluded':[] if a.canonical else [10],
            'native_cut_count':sz//12,'native_fibres':sz,'full_fibre_inventory_sha256':aggregate.hexdigest(),'directly_recomputed_native_cuts':counts,
            'exact_pairwise_rank_mismatches':len(out),'all_unverified_pairs':miss,'rank_pairs':dict(hist),
            'literal_pair_witness_sha256':sha256(json.dumps(out,separators=(',',':')).encode()).hexdigest(),
            'necessary_changed_left_star_maps':(len(donors)-1) if not miss else None,'new_complete_kappa':False}
    (a.out/(name+'.json')).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(a.variant,len(out),len(miss),sum(counts.values()),flush=True)
    require(not miss,'incomplete variant certificate')
if __name__=='__main__':main()
