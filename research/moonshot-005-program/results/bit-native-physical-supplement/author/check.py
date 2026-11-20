#!/usr/bin/env python3
"""Reproduce the bilateral precursor, separate final star/profile words, and the frozen-interface obstruction."""
from argparse import ArgumentParser
from hashlib import sha256
import json,subprocess,sys,tempfile
from pathlib import Path
import numpy as np

SELECT=('bilateral','stars','profile','frozen')
def run(*args):subprocess.run(list(map(str,args)),check=True)
def py(file,vals,*args):run(sys.executable,'-B',file,*[v for k,val in vals.items()for v in ('--'+k,val)],*args)
def read(q):return json.loads(q.read_bytes())
def equal(a,b,m):
    if a!=b:raise ValueError('native replay mismatch: '+m)
def main(a):
    repo=a.repo.resolve();d=repo/'research/moonshot-005-program/results';w=a.work.resolve();w.mkdir(exist_ok=True,parents=True);a.out.mkdir(exist_ok=True,parents=True);sel=set(a.select or SELECT);total={}
    prior=d/'bit-native-physical-replay/author';rs=d/'bit-spread-rs-physical-word/author';raw=d/'bit-global-facet-shared-coordinates';early=d/'bit-global-two-sided-facet-slices';bil=d/'bit-global-source-facet-row-column';star=d/'bit-global-two-star-target';profile=d/'bit-global-bilateral-profile';frozen=d/'bit-global-frozen-boundary-obstruction';nc=d/'bit-nonlinear-middle-gauge-obstruction/author';packed=d/'bit-spread-packed-h-facet-fibres/review'
    predecessor=a.prior_work.resolve() if a.prior_work else w/'previous';cache=predecessor/'physical-cache';gauges=predecessor/'gauges'
    if not all((cache/f'{k}{i}.npy').is_file()for i in range(111)for k in ('E','B'))or not all((gauges/f'F{i}.npz').is_file()for i in range(111)):
        py(prior/'check.py',{'repo':repo,'work':predecessor,'out':w/'previous-receipt'},'--select','two-sided')
    lib=w/'native.so';rk=w/'rank.so';run('cc','-O3','-march=native','-shared','-fPIC','-I',nc,raw/'review/certify.c',rs/'gf64_matmul.c','-o',lib)
    run('cc','-O3','-march=native','-shared','-fPIC','-fopenmp','-I',nc,raw/'review/block_rank.c','-o',rk)
    F=w/'early.npz';late=w/'late';taps=w/'taps';agg=w/'aggregate';rim=w/'complete-rim.npy';ct={'repo':repo,'library':lib,'arithmetic':raw/'review/field.py','previous':early/'review/check.py'}
    config={'flat-config':raw/'author/output/PARAMETERS.json','input-config':early/'author/output/PARAMETERS.json','output-config':bil/'author/output/PARAMETERS.json'}
    py(early/'review/check.py',{'repo':repo,'parameters':config['input-config'],'previous-parameters':config['flat-config'],'cache':cache,'gauges':gauges,'field-code':ct['arithmetic'],'library':lib,'save-functionals':F,'out':w/'early'})
    py(bil/'review/late.py',{'repo':repo,'physical':packed/'physical.py','library':lib,'gauges':gauges,'cache':late,'out':w/'late-receipt'})
    shared={**ct,**config,'cache':cache,'gauges':gauges,'late':late,'functional':F}
    if 'bilateral' in sel:
        bo=w/'bilateral';cfg=config.copy();cfg['config']=cfg.pop('output-config');cfg['target-config']=cfg.pop('input-config')
        py(bil/'review/check.py',{**ct,**cfg,'cache':cache,'gauges':gauges,'late':late,'functional':F,'out':bo,'rim-file':rim})
        py(bil/'review/target_sections.py',{**ct,'input-config':config['input-config'],'output-config':config['output-config'],'out':bo})
        py(bil/'review/rim_rank.py',{'repo':repo,'rank-code':raw/'review/exact_rank.py','library':rk,'matrix':rim,'receipt':bo/'RESULT.json','out':bo,'threads':a.threads})
        if a.full_rim:py(bil/'review/rim_rank.py',{'repo':repo,'rank-code':raw/'review/exact_rank.py','library':rk,'matrix':rim,'receipt':bo/'RESULT.json','out':bo,'threads':a.threads},'--full')
        for name in ['RESULT','TARGET-PANELS','DISJOINT-RIM']+(['RIM-RANK']if a.full_rim else []):equal(read(bo/(name+'.json')),read(bil/'review/output'/(name+'.json')),name)
        x=read(bo/'RESULT.json');total['bilateral']={k:x[k]for k in ('all_native_proper_invertible_blocks','actual_extra_source_binary_ADD','original_input_directions_across_pairs','original_output_functions_across_pairs')};total['bilateral']['disjoint_endpoint_invariant_lower']=read(bo/'DISJOINT-RIM.json')['whole_return_lower_after_any_facet_bijection']
    if {'stars','profile'}&sel:
        more={'aggregate':agg,'out':w/'aggregate-receipt','taps':taps};optional=[]
        if 'profile' in sel:more['profile']=profile/'author/output/PROFILE.json'
        else:optional=['--taps-only']
        # The source taps are independently reconstructed from genuine released visits at all 111 donors.
        py(profile/'review/aggregate.py',{**shared,**more},*optional)
    if 'stars' in sel:
        so=w/'stars';py(star/'review/check.py',{**shared,'taps':taps,'out':so},'--complete-census');py(star/'review/full_sections.py',{**ct,'config':config['output-config'],'out':so})
        for name in ('RESULT','WORDS','FULL-ROLE-TARGET-SECTIONS','COMPLETE-CENSUS'):equal(read(so/(name+'.json')),read(star/'review/output'/(name+'.json')),name)
        ops=read(star/'author/output/SOURCE-PINS.json');author_cache=w/'author-taps';author_cache.mkdir(exist_ok=True)
        for j in range(111):
            z=np.load(taps/f'T{j}.npz');h=sha256();h.update(z['rim']);h.update(z['central']);parts={'rim':z['rim'],'central':z['central']}
            keys=sorted(tuple(map(int,k[2:].split('-')))for k in z if k.startswith('H-'))
            for g,e in keys:
                k=f'{g}-{e}';h.update(bytes([g,e]))
                for tag in ('H','G'):
                    mat=z[f'{tag}-{k}'];h.update(mat);parts[f'{tag}{g}_{e}']=mat
            equal(h.hexdigest(),ops[str(j)],'independent source '+str(j));np.savez(author_cache/f'{j:03}.npz',**parts)
        py(star/'author/check.py',{'repo':repo,'cache-dir':cache,'late-cache':late,'source-cache':author_cache,'out':w/'star-author'})
        equal(read(w/'star-author/RESULT.json'),read(star/'author/output/RESULT.json'),'authoritative second star word')
        v=read(so/'RESULT.json');total['stars']={k:v[k]for k in ('full_original_native_blocks','nonflat_full_proper_original_targets','additional_full_identity_blocks','net_extra_source_forward_ADD','net_extra_receiver_forward_ADD','net_extra_inverse_ADD')};total['stars']['whole_return_upper']=read(so/'FULL-ROLE-TARGET-SECTIONS.json')['native_fitting_upper']
    if 'profile' in sel:
        po=w/'profile';py(profile/'review/check.py',{**ct,**config,'profile':profile/'author/output/PROFILE.json','aggregate':agg,'prices':profile/'author/output/WORD-PRICES.json','out':po})
        for name in ('RESULT','PRICES'):equal(read(po/(name+'.json')),read(profile/'review/output'/(name+'.json')),name)
        equal(read(w/'aggregate-receipt/AGGREGATES.json'),read(profile/'review/output/AGGREGATES.json'),'all physical aggregate arrows')
        v=read(po/'RESULT.json');total['profile']={k:v[k]for k in ('physical_common_kernel','disjoint_prior_target_kernel','whole_native_return_upper','forward_binary_ADD')}
    if 'frozen' in sel:
        fo=w/'frozen';py(frozen/'review/check.py',{**ct,'flat-config':config['flat-config'],'output-config':config['output-config'],'rank-code':raw/'review/exact_rank.py','rank-library':rk,'cache':cache,'gauges':gauges,'late':late,'out':fo})
        v=read(fo/'RESULT.json');equal(v,read(frozen/'review/output/RESULT.json'),'all actual frozen-boundary residuals');total['frozen']={k:v[k]for k in ('native_edges','actual_nonflat_edges','minimum_error_rank_lower','maximum_error_rank_lower')}
    total['new_complete_kappa']=False;(a.out/'RESULT.json').write_text(json.dumps(total,sort_keys=True,indent=2)+'\n');print('Verified',','.join(sorted(sel)),flush=True)
if __name__=='__main__':
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--work',type=Path);p.add_argument('--prior-work',type=Path);p.add_argument('--select',nargs='+',choices=SELECT);p.add_argument('--full-rim',action='store_true');p.add_argument('--threads',type=int,default=3);a=p.parse_args()
    if a.work:main(a)
    else:
        with tempfile.TemporaryDirectory(prefix='native-physical-supplement-')as tmp:a.work=Path(tmp);main(a)
