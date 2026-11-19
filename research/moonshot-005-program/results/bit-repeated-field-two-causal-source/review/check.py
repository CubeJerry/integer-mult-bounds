#!/usr/bin/env python3
"""Independent field-two causal-gate review; no author code is executed."""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import product
from pathlib import Path
import gzip,json


def need(value,why):
    if not value:raise AssertionError(why)


def rank(rows):
    basis={}
    for v in rows:
        while v:
            p=v.bit_length()-1
            if p not in basis:basis[p]=v;break
            v^=basis[p]
    return len(basis)


def nonlinear_controls():
    # A different3-space from the author's fixture, still with rank2 at each
    # donor: T=(x0+x2, x1+x4, x3+x5).
    rows=[(1<<0)|(1<<2),(1<<1)|(1<<4),(1<<3)|(1<<5)]
    need(rank(rows)==3 and all(rank([row&(3<<(2*j)) for row in rows])==2 for j in range(3)),
         'independent top fixture projections')
    tvalue=[sum(((row&x).bit_count()&1)<<k for k,row in enumerate(rows)) for x in range(64)]
    need(Counter(tvalue)=={k:8 for k in range(8)},'top uniformly distributed')
    cases=sharp_mi=sharp_common=0
    common_hist=Counter()
    for functions in product(range(16),repeat=3):
        evalue=[sum(((functions[j]>>((x>>(2*j))&3))&1)<<j for j in range(3)) for x in range(64)]
        joint=Counter(zip(tvalue,evalue));emass=Counter(evalue)
        product_e=1;product_joint=1
        for mass in emass.values():product_e*=mass**mass
        for mass in joint.values():product_joint*=mass**mass
        # H(T|E)>=1 iff product_e >= 2^64*product_joint. H(T)=3,
        # hence this is the stronger direct check I(T;E)<=2.
        need(product_e >= (1<<64)*product_joint,'exact mutual-information upper bound')
        sharp_mi+=int(product_e==(1<<64)*product_joint)
        neighbours=defaultdict(set)
        for t,e in joint:
            neighbours[t].add(8+e);neighbours[8+e].add(t)
        seen=set();masses=[]
        for start in range(8):
            if start in seen:continue
            queue=[start];seen.add(start);target_count=0
            while queue:
                node=queue.pop();target_count+=node<8
                for nxt in neighbours[node]:
                    if nxt not in seen:seen.add(nxt);queue.append(nxt)
            masses.append(8*target_count)
        product_common=1
        for mass in masses:product_common*=mass**mass
        # H(common)<=I(T;E), compared with exact integer products.
        need(product_common*product_joint >= (1<<192)*product_e,
             'maximal deterministic common function does not exceed mutual information')
        need(product_common >= (1<<256),'common entropy at most two bits')
        sharp_common+=int(product_common==(1<<256))
        common_hist[tuple(sorted(masses))]+=1;cases+=1
    need(cases==4096,'full nonlinear domain')
    # Future-dependent output cannot be counted as an early common function.
    fixed_early=lambda x:(x&1,(x>>2)&1,(x>>4)&1)
    need(fixed_early(0)==fixed_early(2) and tvalue[0]!=tvalue[2],'future-read negative control')
    return {'Boolean_encoder_triples':cases,'direct_mutual_information_checks':cases,
            'common_function_data_processing_checks':cases,'sharp_MI_cases':sharp_mi,
            'sharp_common_entropy_cases':sharp_common,
            'component_mass_histogram':[[list(k),v] for k,v in sorted(common_hist.items())],
            'future_read_control_rejected':True}


def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--author',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();pg=a.repo/'research/moonshot-005-program'
    paths={
        'layout':pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',
        'factor':pg/'results/bit-all111-balanced-causal-atlas/author/output/BALANCED-FACTOR.json',
        'caps':pg/'results/bit-stripe-varying-port-cut/review/output/RESULT.json.gz',
        'balanced_proof':pg/'results/bit-all111-balanced-causal-atlas/author/BALANCED-PROOF.md'}
    pins={'layout':'9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72',
          'factor':'346e7604b000ba057e49e8dcae639eaf1b8d82aeb1466f8b959a84390971dfa7',
          'caps':'55062cf00045a9d8888fbea8cd613d9c8db65ef570381c282aa004e73d8aa0ae',
          'balanced_proof':'9e37ccf5b73614d4bec7fb9b02cfc0516d5c4690b3f215db31325904bd2002fa'}
    raw={key:(gzip.decompress(path.read_bytes()) if path.suffix=='.gz' else path.read_bytes()) for key,path in paths.items()}
    for key,data in raw.items():need(sha256(data).hexdigest()==pins[key],key+' source pin')
    layout=json.loads(raw['layout']);factor=dict(json.loads(raw['factor'])['factors']);caps=json.loads(raw['caps'])
    roots=layout['root_table'];planes=[set(z) for z in layout['A2']];mids=[set(z) for z in layout['D4']]
    native=set(range(111));orth=[{j for j,v in enumerate(roots) if sum(x*y for x,y in zip(u,v))==0} for u in roots[:111]]
    visible=[{i for i,o in enumerate(orth) if h<=o} for h in planes]
    dvis=[{i for i,o in enumerate(orth) if d<=o} for d in mids]
    singletons={next(iter(h&native)):index for index,h in enumerate(planes) if len(h&native)==1}
    x={index:12//len(h&native)+factor.get(index,0) for index,h in enumerate(planes) if h&native}
    need(all(45*sum(x[index] for index,h in enumerate(planes) if j in h)==5760 for j in native),
         'all111 actual early source-bank sizes')
    previous={z['plane']:z for z in caps['records']}
    author_result=json.loads((a.author/'output/RESULT.json').read_bytes())
    author_census=json.loads(gzip.decompress((a.author/'output/CAUSAL-CENSUS.json.gz').read_bytes()))
    author_by_h={z['H']:z for z in author_census}
    margins=Counter();hist=Counter();uncovered=covered=0
    for hi,h in enumerate(planes):
        donors=sorted(h&native);m=len(donors)
        if m<2:continue
        targets=sorted(i for i in visible[hi] if all(j not in singletons or i not in visible[singletons[j]] for j in donors))
        ds=[d for d,z in enumerate(mids) if h<=z]
        masks=[sum(1<<n for n,i in enumerate(targets) if i in dvis[d]) for d in ds]
        u=masks.count(0)
        old=previous[hi]
        need(len(ds)==45 and old['native_donors']==donors and old['joint_tight_receivers']==targets,
             'identical native plane and exact target set')
        need(sorted(set(masks)-{0})==old['port_neighborhoods'] and u==old['uncovered_ports'],
             'same entire port incidence as admitted color instance')
        early=x[hi];alpha=old['rank_cap']
        gap=45*(m-1)*early-u*m*early-180
        need(gap>0,'causal top excluded at every native plane')
        beta=alpha+1 if alpha<m else 2*m
        got=author_by_h[hi]
        need(got=={'H':hi,'m':m,'x':early,'u':u,'top_early_deficit_at_r180':gap,
                   'alpha':alpha,'field_star_capacity_per_r':beta},'every new author causal entry')
        margins[gap]+=1;hist[m,alpha,beta]+=1;covered+=beta;uncovered+=u
    capacity=Fraction(covered+33)+Fraction(2*uncovered,15)
    need(sum(margins.values())==1108 and min(margins)==30,'complete strict causal census')
    need(covered==2519 and uncovered==1436 and capacity==Fraction(41152,15),'correct arbitrary-field star budget')
    need(author_result['r180']=={'capacity':493824,'required':587520,'deficit':93696},'author global result')
    result={'status':'PASS_INDEPENDENT_REPEATED_FIELD_TWO_CAUSAL_REVIEW',
            'author_PROOF_sha256':sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),
            'author_check_sha256':sha256((a.author/'check.py').read_bytes()).hexdigest(),
            'author_RESULT_sha256':sha256((a.author/'output/RESULT.json').read_bytes()).hexdigest(),
            'source_pins':pins,'strict_native_planes':1108,'early_top_gap_histogram':dict(sorted(margins.items())),
            'minimum_early_top_gap_r180':30,'larger_field_cap_histogram':{str(k):v for k,v in sorted(hist.items())},
            'covered_dimension':covered,'uncovered_ports':uncovered,'capacity_per_r':str(capacity),
            'required_per_r':3264,'deficit_r180':93696,'entropy_controls':nonlinear_controls(),
            'early_word_scope':'No additional H escape route; original X restored before later Y.',
            'author_code_imported_or_executed':False,'inherited_color_decisions_reproved':False,
            'extra_repair_or_replacement_bank_transfer':False,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status']);print('1108 causal gaps;4096 exact nonlinear MI/data-processing controls;93696 deficit.')


if __name__=='__main__':main()
