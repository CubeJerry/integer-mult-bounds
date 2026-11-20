#!/usr/bin/env python3
"""Verify the actual 220 complete proper blocks, all canonical endpoint slices, and all local costs."""
from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util,json
from pathlib import Path
import numpy as np
from blocks import Proper,Target,req

def mod(p,n):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main(a):
    root=a.repo/'research/moonshot-005-program/results';f=mod(root/'bit-spread-h263-source/review/check.py','gf');geo=mod(root/'bit-spread-overlap-source/review/check.py','native').Native(a.repo,f);helper=mod(root/'bit-spread-source-owner-compiler/author/compile_source.py','price')
    ar=mod(a.arithmetic,'field').Arithmetic(a.library,f,helper);pr=mod(a.previous,'previous');mm=ar.mm;_,body,lane=pr.coords();terms=pr.target_blocks(root);flat,first,last=[json.loads(p.read_bytes())for p in (a.flat_config,a.input_config,a.output_config)]
    ti=first['dimensions'];zo=last['output_dimensions'];adj=[sorted(geo.adj[i]&set(range(111)))for i in range(111)];jcore=set(adj[80]);icore=set(adj[10]);req(10 not in jcore and 80 not in icore and len(jcore)==62 and len(icore)==61,'native unmatched source10 and facet80')
    req(set(terms)=={(80,j)for j in jcore}|{(i,10)for i in icore},'all and only 123 S028 nonflat pairs form the two stars')
    raw=np.load(a.functional);fun={k:raw[k]for k in raw};E=[np.load(a.cache/f'E{i}.npy',mmap_mode='r')for i in range(111)];B=[np.load(a.cache/f'B{i}.npy',mmap_mode='r')for i in range(111)];VS=[np.load(a.gauges/f'F{i}.npz')for i in range(111)];Taps=[np.load(a.taps/f'T{j}.npz')for j in range(111)];L=[np.load(a.late/f'L{j}.npy',mmap_mode='r')for j in range(111)]
    for i,entry in enumerate(flat['expected'][str(i)]for i in range(111)):
        for k,Z in [('E',E[i]),('B',B[i]),('V',VS[i]['V']),('S',VS[i]['S'])]:req(sha256(Z).hexdigest()==entry[k],'actual early and pure gauges')
        req(sha256(L[i]).hexdigest()==last['donors'][str(i)]['late_transfer_sha256'],'actual native late observations')
    inputs,outputs={},{};native={};price={};both=set(terms);leaf=[]
    def no(w):return [(k,i,j,not inv)for k,i,j,inv in reversed(w)]
    for j in jcore:inputs[j]=[('T',80,j,False),('B',80,j,True)]
    for i in icore:outputs[i]=[('B',i,10,True),('T',i,10,False)]
    inputs[10]=[];outputs[80]=[]
    import bridge
    allowed=bridge.attachments(icore,zo,terms,lane) if a.bridge else {i for i in icore if zo[i]==7}
    for j in sorted(set(range(111))-set(inputs)):
        i=min(i for i in adj[j] if i in allowed);inputs[j]=no(outputs[i])+[('B',i,j,True)];both.add((i,j));leaf.append([i,j,'source'])
    for i in sorted(set(range(111))-set(outputs)):
        j=min(j for j in adj[i] if j in jcore and ti[j]==7);outputs[i]=[('B',i,j,True)]+no(inputs[j]);both.add((i,j));leaf.append([i,j,'facet'])
    req(len(both)==220 and len(leaf)==97 and set(inputs)==set(outputs)==set(range(111)),'220 distinct complete native proper blocks in the same word')
    if a.bridge:bridge_pair=bridge.connect(inputs,outputs,both,leaf,allowed,jcore,icore,adj,no)
    @lru_cache(maxsize=12)
    def op(k,i,j):
        if k=='T':Z=Target(ar,body,lane,*terms[i,j]);price[k,i,j]=int(Z.price);return Z
        q=adj[i].index(j);ee=E[i][q];l=L[j][adj[j].index(i)];bb=mm(VS[i]['V'],B[i][q]^mm(VS[i]['S'],ee));phase={}
        if f'A-{i}'in fun:
            amp=fun[f'A-{i}'];oi=fun[f'ids-{i}']
            for e in range(8):
                key=f'Q-{i}-{e}'
                if key not in fun:continue
                y=mm(fun[key],ee)
                for g in set(lane[oi]):
                    use=lane[oi]==g;x=np.zeros((480,amp.shape[1]),dtype=np.uint8);x[body[oi[use]]]=amp[use];phase[int(g),e]=[(x,y)]
        Z=Proper(ar,ee,bb,l,Taps[j],phase);price[k,i,j]=int(Z.price);native[i,j]=Z.sha;return Z
    def apply(word,x,transpose=False):
        for k,i,j,inv in (reversed(word) if transpose else word):x=op(k,i,j).apply(x,inv,transpose)
        return x
    def reduced(word):
        s=[]
        for v in word:
            if s and v[:3]==s[-1][:3] and v[-1]!=s[-1][-1]:s.pop()
            else:s.append(v)
        return s
    U=pr.rand(flat['U8_SHAKE_tag'],(480,8));P=pr.rand('globally shared native output rows 0',(8,480));base=np.eye(8,dtype=np.uint8)[:,1:]
    actual=pr.rand('independent complete original 220 star samples',(3840,3));W=np.kron(base,U[:,:5]);P7=np.kron(base,P[:7].T)
    per={};s2={};h2={};hist=Counter();a.out.mkdir(parents=True,exist_ok=True)
    if a.bridge:
        inputs={k:reduced(w)for k,w in inputs.items()};outputs={k:reduced(w)for k,w in outputs.items()};P7=np.kron(np.eye(8,dtype=np.uint8)[:,[2,3,4,6,7]],P[:7].T)
    for j,w in sorted(inputs.items()):
        req(np.array_equal(apply(w,W),W) and np.array_equal(apply(w,P7,True),P7),'native complete donor word fixes genuine 35 inputs and 49 covectors')
        s2[j]=sum(price[k,i,o]for k,i,o,v in w)
    for i,w in sorted(outputs.items()):
        chosen=bridge.probes(i,icore,terms,lane) if a.bridge else list(range(1,8));obs=np.kron(np.eye(8,dtype=np.uint8)[:,chosen],P[:zo[i]].T)
        req(np.array_equal(apply(w,W),W) and np.array_equal(apply(w,obs,True),obs),'native complete facet fixes genuine 35 inputs and selected original covectors')
        h2[i]=sum(price[k,i0,j]for k,i0,j,v in w)
    for idx,(i,j)in enumerate(sorted(both)):
        w=inputs[j]+[('B',i,j,False)]+outputs[i];expected=[('T',i,j,False)]if (i,j)in terms else []
        req(reduced(w)==expected,'complete cancellation of physical invertible factors on all 3840 true originals')
        req(np.array_equal(apply(w,actual),apply(expected,actual)),'direct genuine source/active facet numerical composition control')
        if idx%40==0:print('native star',idx,i,j,flush=True)
    for i,js in enumerate(adj):
        for j in js:
            if (i,j) not in terms:hist[(len(bridge.probes(i,icore,terms,lane)) if a.bridge else 7)*zo[i]]+=1
    req(len(native)==len(both),'authenticated native bilateral arrows at every prescribed anchor')
    res={'full_original_native_blocks':len(both),'nonflat_full_proper_original_targets':len(terms),'additional_full_identity_blocks':len(leaf),'complete_native_matrix_entries':len(both)*3840**2,'other_flat_native_pairs':6470-len(both),'all_compiled_ordinary_original_inputs_per_pair':35,'flat_original_covector_dimension_counts':hist,'net_extra_source_forward_ADD':sum(s2.values()),'net_extra_receiver_forward_ADD':sum(h2.values()),'net_extra_forward_ADD':sum(s2.values())+sum(h2.values()),'net_extra_inverse_ADD':sum(s2.values())+sum(h2.values()),'new_INIT_CLEAR_MOVE':0,'new_complete_kappa':False}
    prefix='BRIDGE-' if a.bridge else ''
    if a.bridge:res.update({'additional_native_bridge':list(bridge_pair),'reselected_aperture_cover':sorted(allowed),'source_pure_original_inverse_is_paid_at_Hub':True,'both_complete_groups_connected':True})
    if a.complete_census:
        from census import complete
        matches,cert=complete((ar,pr,inputs,outputs,apply,adj,terms,body,lane,fun,E,B,VS,Taps,L));req(matches==both,'all 6250 other genuine proper blocks differ on a literal original full-bank input');(a.out/(prefix+'COMPLETE-CENSUS.json')).write_text(json.dumps(cert,sort_keys=True,indent=2)+'\n')
    (a.out/(prefix+'RESULT.json')).write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');(a.out/(prefix+'WORDS.json')).write_text(json.dumps({'additional_anchors':leaf,'native_block_sha256':{f'{i},{j}':v for (i,j),v in sorted(native.items())},'local_source_amounts':s2,'local_facet_amounts':h2,'primitive_blocks':{f'{k}/{i}/{j}':v for (k,i,j),v in sorted(price.items())}},indent=2,sort_keys=True)+'\n');print(res,flush=True)
if __name__=='__main__':
    p=ArgumentParser()
    for k in ('repo','arithmetic','library','previous','flat-config','input-config','output-config','functional','cache','gauges','taps','late','out'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--complete-census',action='store_true');p.add_argument('--bridge',action='store_true');main(p.parse_args())
