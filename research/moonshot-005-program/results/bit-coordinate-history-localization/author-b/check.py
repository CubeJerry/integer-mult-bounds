#!/usr/bin/env python3
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def rank(rows):
    b={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p in b:
                x^=b[p]
            else:
                b[p]=x
                break
    return len(b)


def main(a):
    raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes()
    pin='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
    need(hashlib.sha256(raw).hexdigest()==pin,'native pin')
    w=json.loads(gzip.decompress(raw))
    roots=[]
    for i in range(111):
        r=[F(x) for x in w['frames'][str(w['start'][i])]['B'][0]]
        n=sum(x*x for x in r)
        need(n in (1,4),'normalization')
        roots.append([x*(2 if n==1 else 1) for x in r])
    dot=lambda x,y:sum(p*q for p,q in zip(x,y))
    supports=[sum(1<<k for k,x in enumerate(r) if x) for r in roots]
    need(supports[:8]==[1<<k for k in range(8)],'coordinate index convention')
    part=(a.workspace/'root-work/orthogonal-class-fitting/RESULT.json').read_bytes()
    need(hashlib.sha256(part).hexdigest()=='7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117','partition pin')
    groups=json.loads(part)['groups']
    U=[sum(1<<i for i in g) for g in groups]
    need(groups[0]==list(range(8)),'coordinate class')
    K=[sum(1<<j for j in range(111) if i==j or dot(roots[i],roots[j])==0) for i in range(111)]
    need(K[0]&U[0]==U[0],'K0 coordinate class all ones')
    full=[c for c,g in enumerate(groups) if len(g)==8 and c!=0]
    short=[c for c,g in enumerate(groups) if len(g)<8]
    need(len(full)==8 and len(short)==6,'class counts')
    halves={}
    for c in full+short:
        halves[c]=[]
        for bit in (0,1):
            selected=[i for i in groups[c] if ((K[0]>>i)&1)^bit]
            masks={supports[i] for i in selected}
            need(selected and len(masks)==1,'nonempty single-support half')
            mask=next(iter(masks))
            need(mask.bit_count()==4,'four-coordinate support')
            if c in full:
                need(len(selected)==4 and all(dot(roots[i],roots[j])==0 for i,j in itertools.combinations(selected,2)), 'full half spans coordinate4plane')
            halves[c].append({'class_bit':bit,'indices':selected,'coordinate_mask':mask})
        need(halves[c][0]['coordinate_mask']^halves[c][1]['coordinate_mask']==255,'complementary supports')
    patterns=[]
    proper=[]
    for choice in range(256):
        union=0
        for k,c in enumerate(full):
            union|=halves[c][(choice>>k)&1]['coordinate_mask']
        patterns.append({'choice':choice,'union_coordinate_mask':union})
        if union!=255:
            missing=[p for p in range(8) if not (union>>p)&1]
            need(len(missing)==1,'only one missing coordinate')
            p=missing[0]
            row=K[0]^U[0]
            bits={0:1}
            for k,c in enumerate(full):
                bit=(choice>>k)&1
                bits[c]=bit
                if bit:row^=U[c]
            for c in short:
                allowed=[b for b in (0,1) if not ((halves[c][b]['coordinate_mask']>>p)&1)]
                need(len(allowed)==1,'unique short-class completion')
                bit=allowed[0]
                bits[c]=bit
                if bit:row^=U[c]
            need(row==K[p]^U[0],'exact li identity')
            need(all(not ((supports[i]>>p)&1) for i in range(111) if (row>>i)&1),'support at coordinate facet')
            facet=w['frames'][str(w['final'][111+p])]
            need(facet['dim']==7 and all(dot(roots[p],[F(x) for x in r])==0 for r in facet['B']),'actual coordinate facet')
            proper.append({'coordinate':p,'full_choice':choice,'class_bits':[bits[c] for c in range(15)],'row_hex':hex(row),'weight':row.bit_count(),'span_dimension':7})
    need(len(proper)==8 and {x['coordinate'] for x in proper}==set(range(8)),'exact eight proper patterns')
    L=[K[i]^U[0] for i in range(8)]
    T=[U[c] for c in short]
    need((rank(T),rank(L),rank(T+L),rank(U+[K[0]]))==(6,4,10,16),'binary ranks')
    proper.sort(key=lambda x:x['coordinate'])
    need([x['weight'] for x in proper]==[49,53,53,51,51,51,51,53],'exact support weights')
    result={'status':'PASS_EXACT_COORDINATE_W0_NONCLASS_PROPER_SHORTENING','native_sha256':pin,
            'full_noncoordinate_class_order':full,'short_class_order':short,
            'halves':halves,'all256_full_patterns':patterns,'proper_nonclass_rows':proper,
            'full_pattern_count':256,'proper_full_pattern_count':8,
            'T_short_rank':6,'local_rows_rank':4,'joined_rank':10,'W0_rank':16,
            'W0_mod_Tshort_plus_local_dimension':6,'any_proper_real_chart_scope':True,
            'physical_availability_claimed':False,'source_or_supplier_claimed':False}
    (a.output/'CERTIFICATE.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ['status','proper_full_pattern_count','T_short_rank','local_rows_rank','joined_rank']}))


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O')
    p=argparse.ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--workspace',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    main(p.parse_args())
