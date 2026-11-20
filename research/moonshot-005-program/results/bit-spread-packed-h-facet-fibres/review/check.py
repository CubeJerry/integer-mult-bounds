#!/usr/bin/env python3
"""Independent endpoint replay for 31 true two-centre stars."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import gzip,importlib.util,json
from pathlib import Path
import numpy as np
from physical import Physical,check
def mod(p,n):
    s=importlib.util.spec_from_file_location(n,p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);return v

def roster(r,n,p):
    d={};lookup={tuple(v['centres']):v for v in p['pairs']}
    spec=p['complete_31']
    for h,q,shared in spec['pairs']:
        for k in (3,12):
            cs=[r.Chart(n,z,k) for z in (h,q)];source=r.paired(cs,lookup[h,q][str(k)])
            for c in cs:d[c.h,k]=(c,source,cs)
    for h in spec['singles']:
        for k in (3,12):
            c=r.Chart(n,h,k);d[h,k]=(c,c.single(p['one_centre'][str(k)]),[c])
    return d

def run(a):
    b=a.repo/'research/moonshot-005-program/results';r=mod(b/'bit-spread-overlap-source/review/check.py','geom');f=mod(b/'bit-spread-h263-source/review/check.py','gf');rank=mod(a.rank_code or b/'bit-nonlinear-middle-gauge-obstruction/author/census.py','rank').Elim(f,a.rank_library)
    ar=None
    if a.price_code:
        h=mod(b/'bit-spread-source-owner-compiler/author/compile_source.py','physical_price')
        ar=mod(a.price_code,'independent_price').Arithmetic(a.price_library,f,h)
    auth=json.loads(a.author_result.read_bytes()) if a.author_result else None
    allprice=0
    n=r.Native(a.repo,f);p=Physical(a.repo,n,f,a.mm_library);p.check_binary_K(b);spec=b/'bit-spread-two-centre-packing/author/output'
    pars=(spec/'PARAMETERS.json').read_bytes();sing=(spec/'SINGLETONS.json.gz').read_bytes();check(sha256(pars).hexdigest()=='972939d6c9937d1c18cf90f69399112bf2c9c95eab1b194186b164a2331f5d6c' and sha256(sing).hexdigest()=='107eb64f87489ee31b2fae02f3f93d512bd5a5cf2485d78181dd825d35d21526','actual packed 31 source')
    repairs={(x['h'],x['donor'],x['k']):(x['singleton'],np.asarray(x['S'],dtype=np.uint8)) for x in json.loads(gzip.decompress(sing))}
    d=roster(r,n,json.loads(pars));hs=sorted({h for h,k in d});P=np.load(a.panels) if a.panels else None;seen=set();recs={};phases=Counter();repair=Counter();donorcheck=0;all_coeff=0;checkpoint=sha256()
    for i in range(111):
        hh=[h for h in hs if n.H[h]<=n.adj[i]]
        if not hh:continue
        right,_=p.terminal(i);recs[i]={}
        for k in (3,12):
            src=[];dst=[]
            for h in hh:
                c,maps,cs=d[h,k];nodes=[t for t,z in enumerate(c.ports)if n.D[z]<=n.adj[i]];ds=[c.ports[t] for t in nodes];check(len(ds)==k,'actual H-to-D outbound labels')
                j=c.donors[-1];order=sorted(set(n.views[j,i])-{h});goal=np.zeros((16*k,k),dtype=np.uint8);goal[:k]=np.eye(k,dtype=np.uint8)
                M=p.mm(c.V[nodes,2*k:3*k],maps[j][h]);stack=np.vstack([M]+[maps[j][z] for z in order]);rr,inverse=rank.reduce(stack,True);check(rr==16*k,'independent unique H-side inverse')
                L=inverse[:,:k];ll=np.kron(np.eye(2,dtype=np.uint8),L)
                for j in c.donors:
                    row=c.ix[j];core=p.mm(c.V[nodes,row*k:(row+1)*k],maps[j][h]);check(np.array_equal(p.mm(core,L),np.eye(k,dtype=np.uint8)),'exact ordinary source-to-visible-H labels')
                    primary=next(x.h for x in cs if j in x.donors)
                    for z in set(n.views[j,i])-{h}:
                        if n.early[j,z]==45:
                            q,S=repairs[primary,j,k];check(q==z,'actual patched singleton')
                            ns=[g for g,dj in enumerate(p.fans[z][k])if n.D[dj]<=n.adj[i]]
                            jet=np.vstack([p.waves[k][ns],p.jet[k][ns]])
                            check(not p.mm(jet,p.mm(S,ll)).any(),'physical singleton 3k source derivative')
                            repair[k]+=1
                        else:check(not p.mm(maps[j][z],L).any(),'other native H outputs vanish before propagation')
                    donorcheck+=1
                early=sum(n.early[j,h] for j in c.donors)//45;phases[h,early]+=1
                seq=[('X',t) for t in range(early)]+[('Y',t)for t in range(2-early)]
                cols=[]
                for phase,stripe in seq:
                    for z in ds:
                        rid=p.flags[h,z,phase][stripe];owners=p.middle[z];positions=[t for t,u in enumerate(owners) if u in right]
                        check(len(positions)==8,'eight actual D exit owners reaching the native facet')
                        Q=np.vstack([right[owners[t]]for t in positions]).T;v=p.dword(z)[positions,owners.index(rid),None]
                        cols.append(p.mm(Q,v)[:,0])
                zz=np.stack(cols).T
                if P:
                    for tag,actual in [('L',ll),('Z',zz)]:
                        name=f'{tag}-{i}-{h}-{k}';seen.add(name);check(np.array_equal(P[name],actual),'every physical original-to-facet panel coefficient '+name)
                all_coeff+=ll.size+zz.size;checkpoint.update(ll.tobytes());checkpoint.update(zz.tobytes())
                src.append(ll);dst.append(zz)
            domain=np.hstack(src);image=np.hstack(dst);wanted=2*k*len(hh)
            check(rank.reduce(domain)==rank.reduce(image)==wanted,'joint raw original and downstream column independence')
            if ar:
                def complete(M):
                    used=ar.reduce(M.T)
                    reqs=sorted(set(range(len(M)))-set(used))
                    return np.hstack([M,np.eye(len(M),dtype=np.uint8)[:,reqs]])
                O=p.mm(complete(domain),ar.reduce(complete(image),True)[0])
                Oinv,price=ar.reduce(O,True)
                check(np.array_equal(p.mm(O,image),domain) and np.array_equal(p.mm(O,Oinv),np.eye(32*k,dtype=np.uint8)),'every raw native original and invertible facet matrix')
                pin=sha256(O.tobytes()).hexdigest();allprice+=8*price
                if auth:check(pin==auth['terminal_gauges'][f'{i}/{k}']['matrix_sha256'],'literal actual facet word')
            recs[i][k]={'charts':len(hh),'full_columns':wanted,'input_sha256':sha256(domain.tobytes()).hexdigest(),'terminal_sha256':sha256(image.tobytes()).hexdigest()}
    check(len(hs)==31 and len(recs)==110 and donorcheck==6246 and (P is None or set(P.files)==seen),'complete native roster and both components')
    ordinals={}
    for k,off in [(3,0),(12,768)]:
        for e in range(8):
            for l in range(2):
                for s in range(16*k):
                    ordinals[off+16*s+8*l+e]=off+32*k*e+16*k*l+s
    check(set(ordinals)==set(ordinals.values())==set(range(3840)),'actual full original vs physical F bank permutation')
    visited=set();cycles=Counter()
    for t in ordinals:
        if t in visited:continue
        s=t;steps=0
        while s not in visited:visited.add(s);s=ordinals[s];steps+=1
        check(s==t,'valid actual owner cycle');cycles[steps]+=1
    if ar:
        allprice+=len(recs)*18*(3840-sum(cycles.values()))
        if auth:check(allprice==auth['terminal_ADD_forward']==auth['ground_preload_inverse_ADD'],'exact field operations and true permutations charged')
    result={'exact_endpoint_ADD_each_direction':allprice if ar else None,'actual_native_chart_count':31,'constrained_facets':110,'max_charts_per_facet':max(v[3]['charts']for v in recs.values()),'native_H_receiver_sections':donorcheck//6,
            'native_donor_H_receiver_sections':donorcheck//2,'original_fields_per_section':240,'source_and_terminal_panel_field_coefficients':all_coeff,
            'paired_panel_sha256':checkpoint.hexdigest(),'physical_singleton_jet_replays':repair,'all_early_charts':len({h for h,e in phases if e==2}),
            'early_late_charts':len({h for h,e in phases if e==1}),'raw_to_packed_cycles':cycles,'true_output_swaps_all_field_owners':3840-sum(cycles.values()),
            'per_facet':recs,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print(result['native_donor_H_receiver_sections'],result['source_and_terminal_panel_field_coefficients'],repair,cycles)
if __name__=='__main__':
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--panels',type=Path);p.add_argument('--price-code',type=Path);p.add_argument('--price-library',type=Path);p.add_argument('--author-result',type=Path);p.add_argument('--rank-code',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--mm-library',type=Path);p.add_argument('--rank-library',type=Path);run(p.parse_args())
