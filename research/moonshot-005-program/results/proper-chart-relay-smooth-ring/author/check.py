#!/usr/bin/env python3
"""Exact pinned composition checks for the smooth-ring corollary."""
import argparse,hashlib,json
from pathlib import Path

def need(v,s):
    if not v:raise ValueError(s)

BASE=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--receipt',type=Path,default=BASE/'worker-c/proper-chart-relay-review/RESULT.json');p.add_argument('--contract',type=Path,default=BASE/'worker-b/native-repartition/dependencies/independent.py');p.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));a=p.parse_args()
    rp='160594db2c8c3ba92a799aa645c7eb534bae7573f0793ade16dfa07c64993fd1';cp='21f46a8340331abb1486b50bd4e04453f1968b0a5950d86ff7780dd368590874'
    need(hashlib.sha256(a.receipt.read_bytes()).hexdigest()==rp,'frozen independent relay receipt')
    need(hashlib.sha256(a.contract.read_bytes()).hexdigest()==cp,'retained exact scalar contract')
    text=a.contract.read_text();need('for prime in (2,3,5):'in text and "assert smooth(coeff.denominator) and (op!='SCALE' or smooth(abs(coeff.numerator)))"in text,'actual denominator/numerator guard')
    d=json.loads(a.receipt.read_text());out=[]
    for r in d['variants']:
        n=r['size'];det=int(r['remaining_D_determinant_up_to_permutation_sign']);factors={2:3,3:3,7:1,127:2}if n==20 else{2:8,3:1,5:4};v=1
        for q,e in factors.items():v*=q**e
        need(v==det,'exact complete determinant factorization')
        controls=r['coefficient_ring']['prime_controls'];remaining=[z for z in controls if z['prime']not in[2,3,5]]
        if n==20:
            need([(z['prime'],z['full_public_rank'])for z in remaining]==[(7,399),(127,398)],'actual non-inverted residue deficiencies')
            need(all(len(z['full_input_kernel_basis'])==z['deficit']for z in remaining),'explicit kernel witness counts')
            need(max(z['deficit']for z in remaining)==2,'two scalar records necessary')
            need(all(z['with_seven_relay_modes_rank']==96 for z in remaining),'retained seven-bank rows suffice over smooth ring')
            ret=r['coefficient_ring']['abstract_minimal_retention'];need(ret['rows']==['q1','q4']and all(ret['ranks_at_all_odd_determinant_factors'][str(z['prime'])]==96 for z in remaining),'two original Gram records suffice')
        else:need(not remaining and set(factors)<={2,3,5},'fortyfour determinant is a unit, no smooth-ring obstruction')
        out.append({'restored':n,'determinant':det,'factorization':factors,'noninverted_bad_primes':[z['prime']for z in remaining],'minimum_additional_records_for_global_smooth_ring_recovery':2 if n==20 else 0,'unit_boundary_control':n==44})
    result={'status':'PASS_PINNED_SMOOTH_RING_COROLLARY','independent_receipt_sha256':rp,'retained_scalar_contract_sha256':cp,'ring':'Z[1/30,i]','variants':out,'classification':'Universal residue/module proof with inherited independently verified finite source evidence. No physical decoder or new kappa.'}
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('PASS:20 smooth-ring obstruction and sharp2-record arithmetic control;44 unit boundary')
if __name__=='__main__':main()
