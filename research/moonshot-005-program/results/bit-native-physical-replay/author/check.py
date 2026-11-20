#!/usr/bin/env python3
"""Reproduce selected native physical words, original row checks and exact nonlinear obstructions."""
from argparse import ArgumentParser
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile

SELECT=('nonlinear','d120','packed','global','two-sided')
VARIANTS=('ordinary','H263','retuned_D120','D120_36','D120_132','packed_23','packed_24','packed_30','packed_31')
def run(*args):subprocess.run([str(v) for v in args],check=True)
def py(path,*args):run(sys.executable,'-B',path,*args)
def data(p):return json.loads(p.read_bytes())
def equal(x,y,what):
    if x!=y:raise ValueError('native replay mismatch '+str(what))
def main(a):
    repo=a.repo.resolve();results=repo/'research/moonshot-005-program/results';w=a.work.resolve();out=a.out.resolve();w.mkdir(exist_ok=True,parents=True);out.mkdir(exist_ok=True,parents=True)
    def get(stem,side='author'):return results/stem/side
    rs=get('bit-spread-rs-physical-word');gd=get('bit-global-facet-shared-coordinates');gr=get('bit-global-facet-shared-coordinates','review');tw=get('bit-global-two-sided-facet-slices');tr=get('bit-global-two-sided-facet-slices','review')
    pa=get('bit-spread-packed-h-facet-fibres');pr=get('bit-spread-packed-h-facet-fibres','review');na=get('bit-nonlinear-middle-gauge-obstruction');fa=get('bit-spread-d120-facet-fibres');fr=get('bit-spread-d120-facet-fibres','review')
    src=get('bit-spread-source-owner-compiler')/'compile_source.py';field=get('bit-spread-h263-source','review')/'check.py';geom=get('bit-spread-overlap-source','review')/'check.py';pars=get('bit-spread-two-centre-packing')/'output/PARAMETERS.json'
    selected=set(a.select or SELECT);summ={};tier=w/'field.so';rank=w/'rank.so';brank=w/'block-rank.so';invert=w/'inverse.so'
    run('cc','-O3','-march=native','-shared','-fPIC','-I',na,gr/'certify.c',rs/'gf64_matmul.c','-o',tier)
    run('cc','-O3','-march=native','-shared','-fPIC',na/'finite_rank.c','-o',rank)
    if 'nonlinear' in selected:
        d=w/'nonlinear';fib=w/'native-fibres.npz'
        py(na/'check.py','--native-review',get('bit-spread-isolated-middle-cut','review')/'output/RESULT.json','--out',d)
        py(na/'census.py','--repo',repo,'--library',rank,'--degree',0,'--save-fibres',fib,'--out',d)
        py(na/'all_joins.py','--repo',repo,'--library',rank,'--fibres',fib,'--out',d)
        py(na/'cross_joins.py','--repo',repo,'--library',rank,'--fibres',fib,'--out',d)
        small=data(d/'CROSS-JOINS.json');equal(small,data(na/'output/CROSS-JOINS.json'),'ordinary 107-clique')
        joins={}
        for v in VARIANTS:
            py(na/'variant_joins.py','--repo',repo,'--variant',v,'--fibres',fib,'--library',rank,'--out',d/'variants')
            res=data(d/'variants'/(v+'.json'));equal(res,data(na/'output/variants'/(v+'.json')),v)
            joins[v]=[res['native_cut_count'],res['exact_pairwise_rank_mismatches'],res['necessary_changed_left_star_maps']]
        summ['nine_separate_nonlinear_source_obstructions']={'earlier_ordinary_mismatches':small['complete_pairwise_incompatibility_count'],'variants':joins}
    if a.canonical:
        if 'nonlinear' not in selected:raise ValueError('the canonical certificate uses --select nonlinear')
        more={}
        for v in VARIANTS:
            py(na/'variant_joins.py','--repo',repo,'--variant',v,'--canonical','--fibres',fib,'--library',rank,'--out',d/'variants')
            p=d/'variants'/('canonical-'+v+'.json');current=data(p);equal(current,data(na/'output/variants'/p.name),'canonical '+v)
            more[v]=[current['native_cut_count'],current['exact_pairwise_rank_mismatches'],current['necessary_changed_left_star_maps']]
        summ['separate_canonical_summand_obstructions']=more
    if 'd120' in selected:
        d=w/'d120';py(fa/'check.py','--repo',repo,'--out',d/'author');py(fr/'check.py','--repo',repo,'--tables',fa/'output','--out',d/'review')
        A=data(d/'author/RESULT.json');B=data(d/'review/RESULT.json');equal(A,data(fa/'output/RESULT.json'),'D120 author');equal(B,data(fr/'output/RESULT.json'),'D120 review')
        summ['two_separate_D120_words']={name:{'native_fibres':q['designated_original_subspace_fibres'],'original_fields':q['field_dimension_on_full_true_bank'],'native_D_minors':q['local_D_native_sections']} for name,q in sorted(B.items())}
    if 'packed' in selected:
        d=w/'packed';p=get('bit-native-complete-middle-charts');support=p if (p/'slices.py').is_file() else pa/'support'
        run('cc','-O3','-march=native','-shared','-fPIC',support/'invert.c','-o',invert)
        py(pa/'check.py','--repo',repo,'--h-author',rs,'--isolated-author',get('bit-spread-isolated-middle-cut'),'--middle-author',support,'--k-words',get('bit-gf64-actual-k-atlas')/'output','--d-charts',get('bit-minimum-cache-d-atlas')/'output/CHARTS.json.gz','--packing-review',geom,'--field-review',field,'--parameters',pars,'--compiler',src,'--library',tier,'--inverse-library',invert,'--out',d/'author')
        py(pr/'check.py','--repo',repo,'--rank-library',rank,'--mm-library',tier,'--price-code',gr/'field.py','--price-library',tier,'--author-result',pa/'output/RESULT.json','--out',d/'review')
        A=data(d/'author/RESULT.json');B=data(d/'review/RESULT.json');equal(A,data(pa/'output/RESULT.json'),'all packed author matrices');equal(B,data(pr/'output/RESULT.json'),'physical packed graphs')
        summ['packed_31_native_word']={'native_H_receiver_sections':B['native_H_receiver_sections'],'donor_receiver_H':B['native_donor_H_receiver_sections'],'distinct_pairs':A['distinct_native_ordered_donor_receiver_pairs'],'total_field_directions':A['total_native_original_field_directions'],'terminal_each_direction_ADD':B['exact_endpoint_ADD_each_direction']}
    if {'global','two-sided'}&selected:
        d=w/'shared';cache=w/'physical-cache';gauges=w/'gauges'
        py(gr/'rebuild.py','--repo',repo,'--parameters',gd/'output/PARAMETERS.json','--physical',pr/'physical.py','--mm-library',tier,'--cache',cache,'--out',d/'review')
        py(gd/'check.py','--repo',repo,'--cache-dir',cache,'--out',d/'author')
        py(gr/'check.py','--repo',repo,'--parameters',gd/'output/PARAMETERS.json','--cache',cache,'--library',tier,'--minor-roles',24,'--emit-gauges',gauges,'--out',d/'review')
        A=data(d/'author/RESULT.json');B=data(d/'review/RESULT.json');equal(A,data(gd/'output/RESULT.json'),'shared global author');equal(B,data(gr/'output/RESULT.json'),'cross-checked global word')
        summ['whole_native_shared_coordinate_word']={k:B[k] for k in ('all_foreign_invertible','native_exact_input_columns_over_edges','guaranteed_global_kernel','native_return_rank_lower','native_return_rank_upper','additional_forward_and_inverse_ADD')}
    if 'two-sided' in selected:
        d=w/'two-sided';ranges=w/'S028-RANGES.npz'
        py(tw/'check.py','--repo',repo,'--cache-dir',cache,'--previous-author',gd,'--out',d/'author')
        py(tr/'check.py','--repo',repo,'--parameters',tw/'output/PARAMETERS.json','--previous-parameters',gd/'output/PARAMETERS.json','--cache',cache,'--gauges',gauges,'--field-code',gr/'field.py','--library',tier,'--save-ranges',ranges,'--out',d/'review')
        A=data(d/'author/RESULT.json');B=data(d/'review/RESULT.json');equal(A,data(tw/'output/RESULT.json'),'two-sided author');equal(B,data(tr/'output/RESULT.json'),'all true two-sided input directions')
        summ['two_sided_target_on_original_points_at_every_proper_pair']=B
    if a.exact:
        if 'two-sided' not in selected:raise ValueError('the exact complete-rank extension needs --select two-sided')
        run('cc','-O3','-march=native','-shared','-fPIC','-fopenmp','-I',na,gr/'block_rank.c','-o',brank)
        py(gr/'exact_rank.py','--repo',repo,'--library',brank,'--controls-only')
        py(tr/'exact_augmentation.py','--repo',repo,'--parameters',gd/'output/PARAMETERS.json','--prior',gr/'output/FULL-ASSEMBLY.json','--ranges',ranges,'--gauges',gauges,'--cache',cache,'--field-code',gr/'field.py','--library',tier,'--rank-library',brank,'--threads',a.threads,'--out',d/'review')
        exact=data(d/'review/EXACT-NATIVE-RETURN.json');equal(exact,data(tr/'output/EXACT-NATIVE-RETURN.json'),'exact complete physical return')
        summ['exact_global_fittings']=exact
    summ['new_complete_kappa']=False
    (out/'RESULT.json').write_text(json.dumps(summ,sort_keys=True,indent=2)+'\n')
    print('Verified',','.join(sorted(selected)),flush=True)
if __name__=='__main__':
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--work',type=Path);ap.add_argument('--select',nargs='+',choices=SELECT);ap.add_argument('--exact',action='store_true');ap.add_argument('--canonical',action='store_true');ap.add_argument('--threads',type=int,default=3)
    args=ap.parse_args()
    if args.work:main(args)
    else:
        with tempfile.TemporaryDirectory(prefix='native-physical-replay-')as temp:
            args.work=Path(temp);main(args)
