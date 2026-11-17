#!/usr/bin/env python3
"""Exact source audit and corroboration of the enumeration-free block proof."""
import argparse
from hashlib import sha256
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
PINS={
 'native':'8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e',
 'cut':'9c3b5745e015eb14926e6ecb0ff8f1df877116eddd9799e448650c61d8866aac',
 'cases':'20b665b916f86fdc10a3577f09e9043389deb8677b5b6f8653bfb75495df8802'}
ROLES=[14,17,19,20,96,99,101,102]

def read(path,pin):
    raw=path.read_bytes();assert sha256(raw).hexdigest()==pin
    return json.loads(raw)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--native',type=Path,default=HERE.parent/'native.json')
    ap.add_argument('--cut',type=Path,default=HERE.parent/'full-half-reservoir-review/output/INDEPENDENT-CUT.json')
    ap.add_argument('--cases',type=Path,default=HERE.parents[1]/'A/complementary-frame-search/output/RESULT.json')
    ap.add_argument('--out',type=Path,default=HERE/'CERTIFICATE.json')
    args=ap.parse_args()
    native=read(args.native,PINS['native']);roots=native['native_roots']
    assert all(sum(x*x for x in roots[i])>0 for i in ROLES)
    assert all(sum(x*y for x,y in zip(roots[i],roots[j]))==0 for i,j in itertools.combinations(ROLES,2))
    fields={x['name']:x for x in read(args.cut,PINS['cut'])}
    mask=sum(1<<r for r in ROLES)
    for r in ROLES:
        assert fields[f'NATIVE_{r}']['chart']==f'L{r}'
        assert int(fields[f'NATIVE_{r}']['row_hex'],16)==1<<r
        assert fields[f'Y{r}']['chart']=='zero'
        row=int(fields[f'Y{r}']['row_hex'],16)
        assert row>>111==1<<r and row&mask==0
    supplied=read(args.cases,PINS['cases']);cases=supplied['cases']
    assert len(cases)==192
    pairs_checked=0
    for case in cases:
        seed=case['seed_permutation'];assert sorted(seed)==list(range(8))
        blocks=[(1<<seed[i])|(1<<seed[4+i]) for i in range(4)]
        history=blocks+blocks
        p2,p3=case['round2'],case['round3']
        for i,j in enumerate(p2):history[i]=history[4+j]=blocks[i]|blocks[j]
        omitted=[]
        for i,j in enumerate(p3):
            u,v=history[i],history[4+j]
            final=u|v;own=(1<<i)|(1<<(4+j))
            assert final==255^own and final.bit_count()==6
            missing=255^final
            assert missing in blocks
            omitted.append(blocks.index(missing))
        assert sorted(omitted)==list(range(4))
        assert all((p&15).bit_count()==(p>>4).bit_count()==1 for p in blocks)
        for i,j in enumerate(p3):
            u,v=history[i],history[4+j]
            assert all((p&15).bit_count()<=2 and (p>>4).bit_count()<=2 for p in (u,v))
            need_a=15^(1<<i);need_b=(15^(1<<j))<<4
            assert all([need_a&~u,need_a&~v,need_b&~u,need_b&~v])
            pairs_checked+=1
    out={'status':'PASS_ENUMERATION_FREE_BLOCK_PROOF_REVIEW','physical_roles':ROLES,
         'pins':PINS,'source_lines_form_an_orthogonal_basis':True,
         'initial_target_X_support_avoids_all_eight_inputs':True,
         'corroborating_cases_checked':len(cases),'final_pairs_checked':pairs_checked,
         'universal_proof':'REVIEW.md, Sections 2-4; does not rely on completeness of the supplied finite case list',
         'scope':'Three actual cochart cross-frame perfect-match rounds; one native-unit seed per Y; eight records only; invertible scalar binary pair maps; no later information arrivals',
         'no_general_supplier_exclusion':True}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'cases':len(cases),'pairs':pairs_checked,'out':str(args.out)}))
if __name__=='__main__':main()
