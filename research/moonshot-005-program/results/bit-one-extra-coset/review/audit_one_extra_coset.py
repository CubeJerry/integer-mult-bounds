#!/usr/bin/env python3
"""Independent exact BIT-code audit for the one-extra-coset theorem."""
import argparse, collections, gzip, hashlib, itertools, json
from fractions import Fraction
from pathlib import Path

PIN = '51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'

def need(ok, msg):
    if not ok:
        raise AssertionError(msg)

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def rank_low(rows):
    """F2 row rank using low-bit pivots (independent of root's high-pivot code)."""
    pivots={}
    for value in rows:
        z=int(value)
        while z:
            p=(z & -z).bit_length()-1
            if p in pivots:
                z ^= pivots[p]
            else:
                pivots[p]=z
                break
    return len(pivots)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--root-package',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    native_path=args.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz'
    raw=native_path.read_bytes()
    need(hashlib.sha256(raw).hexdigest()==PIN,'native pin mismatch')
    src=json.loads(gzip.decompress(raw))
    charts={int(k):v for k,v in src['frames'].items()}

    roots=[]
    for i in range(111):
        r=[Fraction(x) for x in charts[src['start'][i]]['B'][0]]
        n=dot(r,r)
        need(n in (1,4),f'root norm mismatch {i}')
        scale=2 if n==1 else 1
        v=[scale*x for x in r]
        need(all(x.denominator==1 for x in v) and dot(v,v)==4,f'integral doubled root failed {i}')
        roots.append([int(x) for x in v])

    # Canonical actual contact fit from exact real geometry.
    K=[]
    for i,r in enumerate(roots):
        bits=0
        for j,s in enumerate(roots):
            d=dot(r,s)
            need(d.denominator==1 and int(d)%2==0,f'non-even inner product {i},{j}')
            k=int(i==j or d==0)
            need(k == (1 ^ ((int(d)//2)&1)),f'contact encoding differs at {i},{j}')
            bits |= k<<j
        K.append(bits)
    need(all(((K[i]>>j)&1)==((K[j]>>i)&1) for i in range(111) for j in range(111)),
         'canonical fit is not symmetric')
    need(rank_low(K)==9,'canonical code dimension is not 9')

    # Select original rows with low-pivot elimination and retain coordinates.
    pivots={}
    basis=[]
    basis_ports=[]
    normal=[]
    for row_index,row in enumerate(K):
        z=row
        coeff=0
        while z:
            p=(z & -z).bit_length()-1
            if p in pivots:
                pv,pc=pivots[p]
                z ^= pv
                coeff ^= pc
            else:
                k=len(basis)
                basis.append(row)
                basis_ports.append(row_index)
                pivots[p]=(z,coeff^(1<<k))
                coeff=1<<k
                break
        normal.append(coeff)
    need(len(basis)==9 and all(x for x in normal),'basis/normals construction failed')
    points=[]
    for j in range(111):
        p=0
        for k,row in enumerate(basis):
            p |= ((row>>j)&1)<<k
        points.append(p)
    need(all(((normal[i]&points[j]).bit_count()&1)==((K[i]>>j)&1)
             for i in range(111) for j in range(111)), 'K does not factor through independent basis coordinates')
    need(len(set(normal))==111,'coefficient normals duplicate')
    need(all(normal),'zero coefficient normal')

    # Exact row-basis codeword list and extension-field distance premise.
    code=[0]
    for row in basis:
        code += [x^row for x in code]
    need(len(set(code))==512 and len(code)==512,'codeword enumeration not 2^9')
    dmin=min(x.bit_count() for x in code if x)
    need(dmin==48,'binary code minimum distance changed')

    # Recompute every one- and two-row zero-set rank with a different pivot order.
    zero_masks=[(((1<<111)-1)^K[i]) for i in range(111)]
    single_ranks=[]
    for i,zmask in enumerate(zero_masks):
        single_ranks.append(rank_low([points[j] for j in range(111) if (zmask>>j)&1]))
    need(single_ranks==[8]*111,'one-zero set rank failure')
    pair_ranks=[]
    pair_intersection_hist=collections.Counter()
    pair_witness=None
    for i,j in itertools.combinations(range(111),2):
        zmask=zero_masks[i]&zero_masks[j]
        rr=rank_low([points[k] for k in range(111) if (zmask>>k)&1])
        pair_ranks.append(rr)
        need(rr==7,f'pair zero-set rank not 7 at ({i},{j})')
        closed=(K[i]&K[j]).bit_count()
        pair_intersection_hist[closed]+=1
        if closed==36 and pair_witness is None:
            pair_witness=(i,j)
    need(len(pair_ranks)==6105 and set(pair_ranks)=={7},'pair rank census incomplete')
    need(max(pair_intersection_hist)==36 and pair_witness is not None,'closed-neighborhood cap')

    # Coordinate availability and the sharp noncoordinate h=e_1+e_10 witness over F2.
    outside_masks=[(((1<<111)-1) ^ (K[i] ^ (1<<i))) for i in range(111)]
    code_restrictions=[{word & mask for word in code} for mask in outside_masks]
    coordinate_availability=[]
    for j in range(111):
        h=1<<j
        av=[i for i,mask in enumerate(outside_masks) if (h&mask) in code_restrictions[i]]
        need(sum(1<<i for i in av)==K[j],f'coordinate availability not T_{j}')
        coordinate_availability.append(len(av))
    h=(1<<1)|(1<<10)
    sharp=[i for i,mask in enumerate(outside_masks) if (h&mask) in code_restrictions[i]]
    need(len(sharp)==36,'sharp noncoordinate availability count not36')
    need(h not in code and all((h^(1<<j)) not in code for j in range(111)),
         'binary witness unexpectedly zero or coordinate coset')

    # The rank-two, three-normal exception: all pair conditions hold but no common q.
    aa=[0b01,0b10,0b11]
    qq=[0b00,0b00,0b01]
    def span2(a,b): return {0,a,b,a^b}
    pair_conditions=all((qq[i]^qq[j]) in span2(aa[i],aa[j]) for i,j in itertools.combinations(range(3),2))
    common_q=[q for q in range(4) if all((qq[i]^q) in (0,aa[i]) for i in range(3))]
    need(pair_conditions and not common_q,'rank-two negative control did not exhibit gluing failure')

    # A base-field rank certificate lifts to any extension: every binary minor
    # remains zero/nonzero, so rank_F(M)=rank_F2(M) for each 0/1 matrix M.
    # Hence if a codeword over F had <48 support, its zero-coordinate submatrix
    # would have rank<9 over F, hence over F2, yielding a binary <48 word.
    # Likewise a binary restriction vector lies in the extended rowspace iff it
    # lies in the binary rowspace. This transfers both distance and availability.
    result={
        'status':'PASS_INDEPENDENT_ONE_EXTRA_COSET_SOURCE_AND_EXTENSION_AUDIT',
        'native_sha256':PIN,
        'reconstructed_code_dimension':9,
        'basis_ports': basis_ports,
        'all111_normals_distinct_nonzero':True,
        'single_zero_ranks':{'count':len(single_ranks),'all':8},
        'pair_zero_intersection_ranks':{'count':len(pair_ranks),'all':7},
        'pair_closed_neighborhood_intersection':{'maximum':max(pair_intersection_hist),
            'histogram':dict(sorted(pair_intersection_hist.items()))},
        'binary_codeword_count':len(code),
        'minimum_binary_codeword_weight':dmin,
        'sharp_witness':{'h_support':[1,10],'F2_availability_count':len(sharp),
                         'available_rows':sharp,'not_coordinate_over_any_extension_by_distance_transfer':True},
        'coordinate_availability_is_exact_closed_neighborhood':True,
        'extension_field_transfer':{
            'rank_invariance': 'All source matrices have entries in F2; a nonzero minor remains nonzero and zero minors remain zero under every characteristic-two extension.',
            'distance_argument': 'If an extended codeword had support<48, its >63 zero coordinates give a rank<9 punctured generator matrix; extension rank invariance yields a nonzero binary codeword with the same zero coordinates, contradicting binary distance48.',
            'availability_argument': 'For binary h and each binary restriction matrix, rowspace membership over an extension is equivalent to equality of ranks of binary augmented matrices, hence to base-field membership.',
            'coordinate_coset_negative_control': 'For h=e1+e10, h+c e_l is nonzero with support<=3 for every extension scalar c and every l; it cannot be in the extended code of distance48.'
        },
        'rank2_three_normal_negative_control':{'pair_conditions_hold':pair_conditions,'global_q_exists':False},
        'proof_audit':{
            'gluing_scope':'Pair-difference relations force a global q only when the available binary normals span rank>=3.',
            'dependent_normal_handling':'For any extra normal a, at least two of an independent triple remain independent modulo span(a); intersecting the corresponding spans(a,a_i) therefore leaves only span(a), including when a is a selected normal or a dependent sum.',
            'rank2_exception':'Three distinct nonzero normals 01,10,11 can satisfy all pairwise relations without one global q; this prevents extending the gluing lemma to rank2 by assertion.',
            'main_bound':'For any nonzero noncoordinate coset, availability<=36. A coset with>=37 available normals has rank>=3, glues to a representative supported in the common closed neighborhood; two support coordinates force availability<=36, so only a single-coordinate coset remains.'
        },
        'scope':'Scalar characteristic-two fields, the pinned actual code C+span(h), and its vertex-gauge equivalent only. No arbitrary rank-ten space or entangled operator extension.'
    }
    args.output.mkdir(parents=True,exist_ok=True)
    (args.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','reconstructed_code_dimension','single_zero_ranks','pair_zero_intersection_ranks','pair_closed_neighborhood_intersection','minimum_binary_codeword_weight','sharp_witness','rank2_three_normal_negative_control']},indent=2))

if __name__=='__main__':
    main()
