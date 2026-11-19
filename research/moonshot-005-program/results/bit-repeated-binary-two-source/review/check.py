#!/usr/bin/env python3
"""Separate Worker-B review of the repeated binary two-dimensional gate.

Does not import or execute the author's implementation. Inherited color caps
are authenticated and matched, not reclassified as new searches.
"""
from argparse import ArgumentParser
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import gzip
import json


def check(condition, reason):
    if not condition:
        raise AssertionError(reason)


def rank(vectors):
    rows = {}
    for vector in vectors:
        while vector:
            index = vector.bit_length()-1
            if index not in rows:
                rows[index] = vector
                break
            vector ^= rows[index]
    return len(rows)


def graph_spaces(m):
    # Enumerate ambient binary planes from pairs, rather than parameterizing
    # matrices in GL2 as the author's checker does.
    ambient = {tuple(sorted((u, v, u ^ v)))
               for u, v in combinations(range(1, 1 << (2*m)), 2)}
    graphs = [frozenset(plane) for plane in sorted(ambient)
              if all({(v >> (2*j)) & 3 for v in plane} == {1,2,3}
                     for j in range(m))]
    check(len(graphs) == 6**(m-1), "independent graph-plane census")
    triples = 0
    for a, b, c in combinations(graphs, 3):
        if a & b and a & c and b & c:
            triples += 1
            check(bool(a & b & c), "every pairwise-intersecting triple has a common line")
    # Any larger counterexample contains a triple: fix two distinct planes
    # and add one which misses their intersection line.
    line_families = {}
    for vector in range(1, 1 << (2*m)):
        family = [plane for plane in graphs if vector in plane]
        if family:
            span_rank = rank(v for plane in family for v in plane)
            check(span_rank <= m+1, "full binary graph star spans at most m+1")
            line_families[vector] = (len(family), span_rank)
    return graphs, {"donors":m,"ambient_planes":len(ambient),"graph_planes":len(graphs),
                    "intersecting_triples":triples,
                    "nonempty_line_stars":len(line_families),
                    "star_size_rank_histogram":{str(k):v for k,v in sorted(Counter(line_families.values()).items())}}


def evaluate(rows, value):
    return sum(((row & value).bit_count() & 1) << i for i, row in enumerate(rows))


def common_functions(graphs):
    cases, count_hist = 0, Counter()
    for a in graphs:
        ar = list(a)[:2]
        for b in graphs:
            br = list(b)[:2]
            successes = 0
            # Every Boolean function of the first graph target is included;
            # this checks genuinely nonlinear functions as well as linear ones.
            for truth in range(16):
                fibres = defaultdict(set)
                for x in range(16):
                    fibres[evaluate(br,x)].add((truth >> evaluate(ar,x)) & 1)
                if all(len(values) == 1 for values in fibres.values()):
                    successes += 1
            dimension = rank(list(a & b))
            check(successes == 2**(2**dimension), "all common Boolean functions factor through intersection")
            cases += 1
            count_hist[dimension, successes] += 1
    # Marginal fullness alone is insufficient. The tuple(x0,x0) has two
    # individually surjective ports but only two joint outputs for four targets.
    outputs = {(x & 1, x & 1) for x in range(4)}
    check(len({v[0] for v in outputs}) == len({v[1] for v in outputs}) == 2
          and len(outputs) == 2, "correlated-port negative control")
    return {"ordered_graph_pairs":cases,"all_Boolean_functions_per_pair":16,
            "intersection_dimension_and_function_count_histogram":{str(k):v for k,v in sorted(count_hist.items())},
            "marginal_only_saturation_rejected":True}


def gf4_mul(a,b):
    # Independent two-bit formula: omega^2=omega+1.
    a0,a1=a&1,a>>1
    b0,b1=b&1,b>>1
    return (a0*b0 ^ a1*b1) | ((a0*b1 ^ a1*b0 ^ a1*b1) << 1)


def scope_controls(graphs):
    # Three hyperplanes of one 3-space, in graph coordinates. This differs
    # from the author's explicit GF4 fixture.
    matrices = [[[1,0],[0,1]], [[1,1],[0,1]], [[1,0],[0,3]]]
    spaces = []
    for matrix in matrices:
        space = {(a,b,gf4_mul(a,matrix[0][0])^gf4_mul(b,matrix[1][0]),
                      gf4_mul(a,matrix[0][1])^gf4_mul(b,matrix[1][1]))
                 for a,b in product(range(4),repeat=2)}
        check(len(space) == 16 and len({point[2:] for point in space}) == 16,
              "GF4 graph maps invertible")
        spaces.append(space)
    check([len(a & b) for a,b in combinations(spaces,2)] == [4,4,4]
          and len(set.intersection(*spaces)) == 1, "GF4 counterexample to common line")
    a,b=next((a,b) for a,b in combinations(graphs,2) if not a&b)
    # First summands agree, second summands do not intersect. A nonzero
    # direct-sum intersection does not enforce every varying base summand.
    ua=list(a)[:2]+[v<<4 for v in list(a)[:2]]
    vb=list(a)[:2]+[v<<4 for v in list(b)[:2]]
    dim=rank(ua)+rank(vb)-rank(ua+vb)
    check(dim == 2 and not a&b, "varying-copy scope control")
    return {"GF4_matrices":matrices,"GF4_pair_cardinalities":[4,4,4],
            "GF4_common_cardinality":1,"varying_copy_total_intersection_dimension":dim,
            "varying_copy_second_summand_intersection_dimension":0}


def main():
    parser=ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--author',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    pg=args.repo/'research/moonshot-005-program'
    layout_raw=gzip.decompress((pg/'results/bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes())
    old_raw=gzip.decompress((pg/'results/bit-stripe-varying-port-cut/review/output/RESULT.json.gz').read_bytes())
    check(sha256(layout_raw).hexdigest()=='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72','layout pin')
    check(sha256(old_raw).hexdigest()=='55062cf00045a9d8888fbea8cd613d9c8db65ef570381c282aa004e73d8aa0ae','inherited independent color certificate pin')
    layout=json.loads(layout_raw); old=json.loads(old_raw)
    roots=layout['root_table']; planes=[set(x) for x in layout['A2']]
    middle=[set(x) for x in layout['D4']]
    orth=[{j for j,v in enumerate(roots) if sum(a*b for a,b in zip(u,v))==0}
          for u in roots[:111]]
    visible=[{i for i,o in enumerate(orth) if h<=o} for h in planes]
    middle_receivers=[{i for i,o in enumerate(orth) if d<=o} for d in middle]
    native=set(range(111))
    canonical=[sum(1<<j for j in ((o&native)^{i})) for i,o in enumerate(orth)]
    check(rank(canonical)==9,'native canonical rank')
    full=(1<<111)-1
    for i,o in enumerate(orth):
        mask=full^sum(1<<j for j in o&native)
        check(rank([row&mask for row in canonical])==9,'canonical outside restriction')
    singletons={next(iter(h&native)):index for index,h in enumerate(planes) if len(h&native)==1}
    check(len(singletons)==11,'singleton count')
    records={item['plane']:item for item in old['records']}
    author=json.loads((args.author/'output/RESULT.json').read_bytes())
    author_incidence=json.loads(gzip.decompress((args.author/'output/NATIVE-INCIDENCE.json.gz').read_bytes()))
    author_by_plane={item['H']:item for item in author_incidence}
    hist=Counter(); pair_hist=Counter(); uncovered=0; covered=0; count=0
    for h_index,h in enumerate(planes):
        donors=sorted(h&native)
        if len(donors)<2:
            continue
        receivers=sorted(i for i in visible[h_index]
                         if all(j not in singletons or i not in visible[singletons[j]] for j in donors))
        ds=[index for index,d in enumerate(middle) if h<=d]
        check(len(ds)==45,'45 real exits per ordinary plane')
        ports={i:{d for d in ds if i in middle_receivers[d]} for i in receivers}
        check(all(len(p)==15 for p in ports.values()),'every target sees15 ports')
        intersections=Counter(len(ports[i]&ports[j]) for i,j in combinations(receivers,2))
        check(set(intersections)<={3,6},'all distinct target pairs share3 or6 exits')
        pair_hist.update(intersections)
        neighbourhoods=[sum(1<<index for index,i in enumerate(receivers) if i in middle_receivers[d]) for d in ds]
        missing=sum(mask==0 for mask in neighbourhoods)
        prior=records[h_index]
        check(prior['native_donors']==donors and prior['joint_tight_receivers']==receivers,'same exact inherited color instance')
        check(prior['port_neighborhoods']==sorted(set(neighbourhoods)-{0}) and prior['uncovered_ports']==missing,'same complete port incidence')
        alpha=prior['rank_cap']
        check(1<=alpha<=len(donors),'inherited alpha range')
        fresh=author_by_plane[h_index]
        check(fresh['joint_tight_receivers']==receivers and fresh['native_donors']==donors
              and fresh['inherited_alpha']==alpha and fresh['uncovered_ports']==missing
              and fresh['shared_port_pair_histogram']=={str(k):v for k,v in intersections.items()},'all author finite incidences matched')
        hist[len(donors),alpha]+=1;uncovered+=missing;covered+=alpha+1;count+=1
    check(hist=={(2,1):204,(2,2):23,(3,1):630,(3,2):249,(3,3):2},'complete color cap histogram')
    information=covered+Fraction(2*uncovered,15)+33
    check(count==1108 and covered==2492 and uncovered==1436,'whole native census')
    check(information==Fraction(40747,15) and 3264-information==Fraction(8213,15),'exact total information deficit')
    check(author['information_capacity_per_replication']==str(information),'author total')
    g2,c2=graph_spaces(2);g3,c3=graph_spaces(3)
    result={'status':'PASS_INDEPENDENT_REPEATED_BINARY_TWO_REVIEW',
            'author_PROOF_sha256':sha256((args.author/'PROOF.md').read_bytes()).hexdigest(),
            'author_check_sha256':sha256((args.author/'check.py').read_bytes()).hexdigest(),
            'author_RESULT_sha256':sha256((args.author/'output/RESULT.json').read_bytes()).hexdigest(),
            'ordinary_planes':count,'shared_port_pair_histogram':dict(pair_hist),
            'covered_capacity_per_repetition':covered,'uncovered_ports':uncovered,
            'total_capacity':str(information),'required':3264,'deficit':str(3264-information),
            'base_balanced_deficit':int(180*(3264-information)),
            'independent_graph_plane_controls':[c2,c3],
            'nonlinear_common_function_controls':common_functions(g2),
            'scope_controls':scope_controls(g2),
            'author_code_imported_or_executed':False,
            'inherited_color_caps_reproved':False,
            'repair_channel_or_changed_canonical_transfer':False,
            'new_complete_kappa':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(result['status'])
    print('Independent graph planes, all native incidences, nonlinear factor controls; deficit98556 at r180.')


if __name__=='__main__':
    main()
