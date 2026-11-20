#!/usr/bin/env python3
"""Check the price, independent source geometry, and exact rational relay obstruction."""
from pathlib import Path
import argparse
import json
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from graph import APPLICATION,WORD,Graph,require
from packed import Field,PRIME,coefficient,unit
from price import compiler,price,real_power,GRID
from rows import bank_ranks,nullspace,triangle_test
from fractions import Fraction as Q


def controls():
    # Deliberately dependent demand pair; mixed A,D obstruction differs from diagonal rank(C).
    require(nullspace([[1,1]],2,False)==[[-1,1]],'exact nullspace control')
    require(len(nullspace([[PRIME]],1,False))==0 and len(nullspace([[0]],1,True))==1,'bad-prime direction')
    a=Field(4)
    raw=[0,PRIME,PRIME**2+45,2048*(PRIME-1)**2]
    z=a.reduce(sum(x*unit(j)for j,x in enumerate(raw)),3)
    require([coefficient(z,j)for j in range(4)]==[x%PRIME for x in raw],'packed overflow control')
    require(real_power(81,Q(1,2))==(9*GRID,9*GRID),'exact dyadic power')
    require(70+64<18*8 and 70+16>18*4 and 70+256>18*16,'interior chord control')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output')
    args=parser.parse_args()
    controls()
    g=Graph()
    result,paid,targets=price(g)
    receipt={'status':'PASS_P104_PATH_PRICES_AND_EXACT_GROUPED_RELAY_INTERFACE',
             'source':{'canonical_main':'e54523517d0f03e58352e647c403a5af3e525a57',
                       'source_pr':7830,'p104_head':'14c74c6a67108f675ac1196a5f2415ead0920e71',
                       'grade_pr':7828,'grade_head':'03b572b3b9ab72c6ba67762e85e1630cda1daad5',
                       'word_sha256':WORD,'application_sha256':APPLICATION},
             'native_banks':{'forward':bank_ranks(g),'adjoint':bank_ranks(g,True)},
             'grouped_relay':triangle_test(g),'path_price':result,
             'conditional_complex_compiler':compiler(paid,targets),
             'negative_controls':['remove final contested join','use a common rank supplier without full paid chord',
                    'take a deficient modular rank as a rational upper bound','packed product above one field digit',
                    'count one fixed funded homogeneous grade as O(N^9)'],
             'complete_kappa_claimed':False}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(receipt['status'])
    print('rational triples',receipt['grouped_relay']['triples'],'private joins',result['private_joins'],
          'contested lower and witness',result['necessary_contested_per_identical_copy'],result['witness_contested_joins'])


if __name__=='__main__':
    main()
