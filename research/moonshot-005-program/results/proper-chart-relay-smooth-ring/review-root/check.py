#!/usr/bin/env python3
"""Independent exact scalar-ring source-fact composition, no author imports."""
from pathlib import Path
import argparse,hashlib,json
BASE=Path(__file__).resolve().parents[2]
def need(v,s):
    if not v:raise ValueError(s)
def factors(n):
    out={};q=2
    while q*q<=n:
        while n%q==0:out[q]=out.get(q,0)+1;n//=q
        q+=1
    if n>1:out[n]=out.get(n,0)+1
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--receipt',type=Path,default=BASE/'worker-c/proper-chart-relay-review/RESULT.json');ap.add_argument('--contract',type=Path,default=BASE/'worker-b/native-repartition/dependencies/independent.py');ap.add_argument('--output',type=Path,default=Path(__file__).with_name('RESULT.json'));args=ap.parse_args()
    rp=args.receipt;cp=args.contract
    need(hashlib.sha256(rp.read_bytes()).hexdigest()=='160594db2c8c3ba92a799aa645c7eb534bae7573f0793ade16dfa07c64993fd1','independent literal replay receipt')
    need(hashlib.sha256(cp.read_bytes()).hexdigest()=='21f46a8340331abb1486b50bd4e04453f1968b0a5950d86ff7780dd368590874','retained contract')
    src=cp.read_text();need('for prime in (2,3,5):'in src and "smooth(coeff.denominator) and (op!='SCALE' or smooth(abs(coeff.numerator)))"in src,'actual scalar guard')
    out=[]
    for v in json.loads(rp.read_text())['variants']:
        fs=factors(int(v['remaining_D_determinant_up_to_permutation_sign']));bad=set(fs)-{2,3,5}
        controls={x['prime']:x for x in v['coefficient_ring']['prime_controls']};minimum=max((controls[p]['deficit']for p in bad),default=0)
        need(minimum==(2 if v['size']==20 else 0),'sharp residue lower bound')
        for p in bad:
            z=controls[p];need(z['with_seven_relay_modes_rank']==96,'bank smooth-ring sufficiency')
            need(v['coefficient_ring']['abstract_minimal_retention']['ranks_at_all_odd_determinant_factors'][str(p)]==96,'two actual rows remove every nonunit prime')
        out.append({'restored':v['size'],'factorization':fs,'nonunit_primes':sorted(bad),'minimum_arithmetic_records':minimum})
    result={'status':'PASS_INDEPENDENT_RING_SCOPE_REVIEW','variants':out,'source_receipt_sha256':hashlib.sha256(rp.read_bytes()).hexdigest(),'scope':'Universal residue and localized-integer module proof reviewed; finite kernels inherited from C independent replay. No claim of a further independent literal replay, physical decoder or new kappa.'}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');print('PASS: smooth-ring obstruction20 and unit boundary44')
if __name__=='__main__':main()
