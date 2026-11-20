#!/usr/bin/env python3
"""Price all forty-four-centre source words on literal X/Y holders, including their inverses."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import importlib.util
import json
import gzip
from pathlib import Path


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    p = ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--emit-words', action='store_true')
    a = p.parse_args()
    base = a.repo/'research/moonshot-005-program/results'
    paths = {
        'compiler': base/'bit-spread-packed-source-owner-compiler/author/compile_pack.py',
        'helper': base/'bit-spread-source-owner-compiler/author/compile_source.py',
        'review': base/'bit-spread-overlap-source/review/check.py',
        'field': base/'bit-spread-h263-source/review/check.py',
        'background': base/'bit-spread-rs-physical-word/author/source-output/PER-DONOR-COSTS.json'}
    compiler, helper, review, field = (module(paths[s], 'forty_compile_'+s) for s in ('compiler','helper','review','field'))
    native = review.Native(a.repo, field)
    wires, xcount = compiler.physical_slots(native, a.repo, helper)
    raw = (Path(__file__).parent/'output/PARAMETERS.json').read_bytes()
    parameters = json.loads(raw)
    pairs = parameters["pairs"]
    sr=(Path(__file__).parent/"output/SINGLETONS.json.gz").read_bytes()
    repairs={(v["h"],v["donor"],v["k"]):(v["singleton"],__import__("numpy").asarray(v["S"],dtype="uint8")) for v in json.loads(gzip.decompress(sr))}
    templates = {}
    for k in (3,12):
        for record in pairs:
            charts = [review.Chart(native,h,k) for h in record['centres']]
            maps = review.paired(charts,record[str(k)])
            for donor, rows in maps.items():
                need(k not in templates.setdefault(donor,{}),'one source per donor and component')
                chart = next(c for c in charts if donor in c.donors)
                templates[donor][k] = chart,rows,record[str(k)]['early'][str(donor)],set(record['centres'])
        for h, options in parameters['singles'].items():
            h=int(h); chart=review.Chart(native,h,k); prm=options[str(k)]
            for donor, rows in chart.single(prm).items():
                need(k not in templates.setdefault(donor,{}),'one single-centre source per donor')
                templates[donor][k]=chart,rows,prm['early'][str(donor)],{h}
    singletons = {j for (j,h),n in native.early.items() if n == 45}
    need(set(templates) == set(range(111)), 'all111 true original source stars')
    a.out.mkdir(parents=True,exist_ok=True)
    totals, per_donor, hashes, all_y = Counter(), {}, {}, set()
    for donor, parts in sorted(templates.items()):
        records, placements, costs, digests = {}, {}, Counter(), {}
        for k in (3,12):
            chart,rows,seed,centres=parts[k]
            bill,perm,late,stream=compiler.compile_one(helper,review,chart,donor,rows,seed,centres,wires,xcount,records,repairs.get((chart.h,donor,k)))
            need(not set(placements)&set(perm) and not all_y.intersection(late),'disjoint real source and cache destinations')
            placements.update(perm);all_y.update(late);costs.update(bill)
            digests[str(k)] = sha256(stream).hexdigest()
            if a.emit_words:
                helper.save_compressed(a.out/f'REDUCE-{donor}-{k}.bin.gz',stream)
        need(set(placements)==set(range(3840*donor,3840*(donor+1))),'every original X field accounted')
        swaps=helper.permutation_swaps(placements)
        records[f'{donor}-swaps']=swaps
        costs['permutation_ADD']=18*len(swaps)
        costs['inverse_ADD']=costs['basis_ADD']+costs['permutation_ADD']
        costs['forward_ADD']=costs['inverse_ADD']+costs['write_ADD']+costs['read_ADD']
        costs['total_ADD']=costs['inverse_ADD']+costs['forward_ADD']
        body=json.dumps(records,sort_keys=True,separators=(',',':')).encode()
        digests['holder']=sha256(body).hexdigest()
        if a.emit_words:
            helper.save_compressed(a.out/f'HOLDERS-{donor}.json.gz',body)
        hashes[str(donor)]=digests;per_donor[str(donor)]=dict(costs);totals.update(costs)
    need(6*len(all_y)==totals['INIT'],'all late fields get exactly one paid cache')
    background=json.loads(paths['background'].read_bytes());bg=Counter()
    # Every donor now has its own compiled source; no background row is reused.
    inverse=bg['early_basis_ADD']+bg['source_owner_permutation_ADD']
    cache=bg['snapshot_copy_ADD_INIT_dirty_CLEAR']
    forward=inverse+cache+bg['late_evaluation_ADD']
    combined={'donors':111,'source_forward_ADD':forward+totals['forward_ADD'],
              'source_pure_inverse_ADD':inverse+totals['inverse_ADD'],
              'source_forward_and_inverse_ADD':forward+inverse+totals['total_ADD'],
              'source_INIT':cache+totals['INIT'],'source_dirty_CLEAR':cache+totals['dirty_CLEAR'],
              'source_extra_MOVE':0,'new_complete_kappa':False}
    out={'status':'PASS_PAID_FORTY_FOUR_CENTRE_ALL_DONOR_SOURCE_COMPILER','parameters_sha256':sha256(raw).hexdigest(),
         'source_pins':{str(v.relative_to(a.repo)):sha256(v.read_bytes()).hexdigest()for v in paths.values()},
         'native_chart_count':44,'special_donor_count':111,'regular_donor_count':0, 'singleton_payload_sha256':sha256(gzip.decompress(sr)).hexdigest(),
         'special':dict(totals),'special_donor_costs':per_donor,'all_word_hashes':hashes,
         'background':dict(bg),'combined':combined}
    (a.out/'COST.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(combined,sort_keys=True))

if __name__=='__main__':
    main()
