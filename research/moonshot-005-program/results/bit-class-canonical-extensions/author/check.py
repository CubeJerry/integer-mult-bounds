#!/usr/bin/env python3
"""Exact finite canonical/class cosets and literal facet-local differences."""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from pathlib import Path

SOURCE='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
AUTHOR='407ecc76c7a4a3b8dd4d88cc4743b63df51be244842f268b7c42f3a27d38d864'


def pivots(rows):
    basis={}
    for value in rows:
        while value:
            p=(value & -value).bit_length()-1
            if p in basis:value^=basis[p]
            else:basis[p]=value;break
    return basis


def reduce(value,basis):
    for p,b in sorted(basis.items()):
        if value>>p&1:value^=b
    return value


def words(basis):
    rows=list(basis)
    return {sum(1<<i for i in range(len(rows)) if bits>>i&1):
            xor([row for i,row in enumerate(rows) if bits>>i&1])
            for bits in range(1<<len(rows))}


def xor(rows):
    result=0
    for row in rows:result^=row
    return result


def rational_rank(rows):
    basis={}
    for raw in rows:
        row=list(raw)
        for p,b in sorted(basis.items()):
            if row[p]:
                scale=row[p];row=[x-scale*y for x,y in zip(row,b)]
        p=next((j for j,x in enumerate(row) if x),None)
        if p is not None:
            scale=row[p];basis[p]=[x/scale for x in row]
    return len(basis)


def main(args):
    raw=(args.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SOURCE
    source=json.loads(gzip.decompress(raw))
    manifest=(args.author/'MANIFEST.json').read_bytes();assert hashlib.sha256(manifest).hexdigest()==AUTHOR
    for name,pin in json.loads(manifest)['artifacts'].items():
        assert hashlib.sha256((args.author/name).read_bytes()).hexdigest()==pin
    author=json.loads((args.author/'RESULT.json').read_text());groups=author['groups']
    roots=[]
    for i in range(111):
        assert source['frames'][str(source['start'][i])]['dim']==1
        r=[F(x) for x in source['frames'][str(source['start'][i])]['B'][0]]
        norm=sum(x*x for x in r);assert norm in (1,4)
        r=[x*(2 if norm==1 else 1) for x in r]
        if next(x for x in r if x)<0:r=[-x for x in r]
        assert all(x.denominator==1 for x in r);roots.append(tuple(map(int,r)))
    dot=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))
    K=[sum(1<<j for j in range(111) if i==j or dot(i,j)==0) for i in range(111)]
    U=[sum(1<<i for i in g) for g in groups]
    assert len(pivots(K))==9 and len(pivots(U))==15
    cb=list(pivots(K).values());code=list(words(cb).values())
    intersection=[r for r in code if all((r&u) in (0,u) for u in U)]
    ib=list(pivots(intersection).values());assert len(ib)==5
    ip=pivots(ib);iwords={value:bits for bits,value in words(ib).items()}
    remainder=[reduce(r,ip) for r in K]
    qb=list(pivots(remainder).values());assert len(qb)==4
    qwords={value:bits for bits,value in words(qb).items()}
    class_of={i:c for c,g in enumerate(groups) for i in g}
    cosets=[qwords[r] for r in remainder]
    assert all(len({cosets[i] for i in g})==1 for g in groups)
    class_cosets=[cosets[g[0]] for g in groups]
    assert set(class_cosets)==set(range(1,16))
    facets={i:[[F(x) for x in r] for r in source['frames'][str(source['final'][111+i])]['B']]
            for i in range(111)}
    for i in range(111):
        assert len(facets[i])==rational_rank(facets[i])==7
        assert all(sum(x*y for x,y in zip(roots[i],r))==0 for r in facets[i])
    table=[]
    for i in range(111):
        c=class_of[i];local=K[i]^U[c]
        assert not (local>>i&1)
        support=[j for j in range(111) if local>>j&1]
        assert all(dot(i,j)==0 for j in support)
        iw=K[i]^remainder[i];assert iw in iwords
        assert K[i]==qwords_inverse(qb,cosets[i])^qwords_inverse(ib,iwords[iw])
        table.append({'port':i,'class':c,'class_coset_4bits':format(cosets[i],'04b'),
                      'canonical_row_hex':hex(K[i]),'quotient_remainder_hex':hex(remainder[i]),
                      'intersection_coordinates_5bits':format(iwords[iw],'05b'),
                      'local_difference_hex':hex(local),'local_support':support,
                      'local_support_size':len(support),'own_entry_zero':True,
                      'actual_receiver_facet':source['final'][111+i],
                      'all_local_support_lines_in_actual_facet':True})
    classes=[]
    for c,g in enumerate(groups):
        representative=g[0]
        assert len(pivots(U+[K[representative]]))==16
        assert all(reduce(K[i]^K[representative],ip)==0 for i in g)
        assert all(len(pivots(U+[K[representative],K[j]]))==17
                   for d,h in enumerate(groups) if d!=c for j in h[:1])
        classes.append({'class':c,'ports':g,'coset_4bits':format(class_cosets[c],'04b'),
                        'canonical_representative_port':representative,
                        'W_dimension':16,'same_W_for_all_class_members':True})
    result={'status':'PASS_EXACT_CLASS_CANONICAL_COSETS_AND_LITERAL_LOCAL_DIFFERENCES',
            'source_sha256':SOURCE,'class_manifest_sha256':AUTHOR,
            'method':'Direct rational source roots and actual facets; low-pivot binary elimination; exhaustive512 canonical words and exact reconstruction coordinates. No author checker imported.',
            'canonical_dimension':9,'U_dimension':15,'intersection_dimension':5,
            'canonical_quotient_dimension':4,'all15_nonzero_cosets_exactly_once':True,
            'intersection_basis_hex':[hex(x) for x in ib],
            'quotient_remainder_basis_hex':[hex(x) for x in qb],
            'classes':classes,'all111_rows':table,
            'own_line_negative_control':{'port':0,'own_square_norm':4,'own_line_in_facet':False},
            'scope':'Candidate16-dimensional W_c=U+<K_i> depends only on class c;15 distinct such spaces. Every l_i=K_i+u_c is literally facet-supported. No actual local current row, global W encoder, chronological packet/source access, q8 realization or completed supplier is provided.'}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','canonical_dimension','U_dimension',
        'intersection_dimension','canonical_quotient_dimension','all15_nonzero_cosets_exactly_once']},indent=2))


def qwords_inverse(basis,bits):
    return xor([r for i,r in enumerate(basis) if bits>>i&1])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    main(p.parse_args())
