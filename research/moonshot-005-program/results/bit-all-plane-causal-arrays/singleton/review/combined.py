#!/usr/bin/env python3
"""Combine independently reviewed local interfaces in the common field F128."""
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import gzip,json
from check import M,need

def main():
    p=ArgumentParser();p.add_argument('--full-review',type=Path,required=True);p.add_argument('--punctured-review',type=Path,required=True);p.add_argument('--singleton-review',type=Path,required=True);p.add_argument('--common-word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    full=json.loads((a.full_review/'RESULT.json').read_bytes());two=json.loads((a.punctured_review/'RESULT.json').read_bytes());single=json.loads((a.singleton_review/'RESULT.json').read_bytes());holder=json.loads((a.full_review/'HOLDER-PERMUTATIONS.json').read_bytes());raw=gzip.decompress(a.common_word.read_bytes());word=json.loads(raw)['ADD']
    need(full['full_native_planes']==881 and two['direct_condition_count']==15098 and single['singleton_planes']==11,'three complete reviewed families')
    V=[]
    for alpha in range(1,46):
        row=[1]
        for _ in range(44):row.append(M[row[-1]][alpha])
        V.append(row)
    prefix_total=0
    for pattern in holder['patterns']:
        state=[1<<j for j in range(315)];prefix=[]
        for p,q in pattern['field_swaps']:
            for bit in range(7):
                x,y=7*p+bit,7*q+bit;prefix.extend([[x,y],[y,x],[x,y]])
        for x,y in prefix+word:state[x]^=state[y]
        expected=[];order=pattern['input_column_order_by_physical_port']
        for row in V:
            for bit in range(7):
                value=0
                for c,v in enumerate(row):
                    for k in range(7):
                        if M[v][1<<k]>>bit&1:value^=1<<(7*order[c]+k)
                expected.append(value)
        need(state==expected,'all actual full-plane holder permutations in commonF128')
        prefix_total+=8*len(prefix)
    need(prefix_total==20832 and len(word)==42522,'exact common-field full-plane local cost')
    full_count=881*(24*len(word)+prefix_total);two_count=two['exact_ADD_all227_H'];single_count=single['ADD_all11_H'];total=full_count+two_count+single_count
    need(total==1666493220,'exact combined1119-plane ordinary invoice')
    out={'status':'PASS_ALL_1119_NONEMPTY_LOCAL_INTERFACES_COMMON_F128','field_modulus':131,'field_degree':7,'plane_counts':{'three_native_donors':881,'two_native_donors':227,'one_native_donor':11},'full_H_physical_permutation_patterns_replayed':3,'full_H_binary_columns_each':315,'full_H_ADD_with_exact_permutations':full_count,'two_donor_H_ADD_with_exact_permutations':two_count,'singleton_H_ADD':single_count,'all1119_local_ADD':total,'all_stationary_cache_INIT_and_dirty_CLEAR_each':two['cache_INIT_and_CLEAR_each_all227_H']+single['INIT_and_dirtyCLEAR_each_all11_H'],'extra_MOVE_at_H':0,'common_full_H_word_uncompressed_sha256':sha256(raw).hexdigest(),'review_receipt_pins':{'full':sha256((a.full_review/'RESULT.json').read_bytes()).hexdigest(),'punctured':sha256((a.punctured_review/'RESULT.json').read_bytes()).hexdigest(),'singleton':sha256((a.singleton_review/'RESULT.json').read_bytes()).hexdigest()},'global_source_quotients_compatible':False,'later_transport_constructed':False,'complete_supplier_or_new_kappa':False}
    a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],total,'ADD',out['all_stationary_cache_INIT_and_dirty_CLEAR_each'],'cache owners',flush=True)

if __name__=='__main__':main()
