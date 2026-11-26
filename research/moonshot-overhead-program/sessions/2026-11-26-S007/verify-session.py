"""Reproduce the numerical certificates in this directory with Python's standard library."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
CASES = (
    ('check-radix-rank.py','radix-rank-receipt.json'),
    ('verify-top-monomial-split.py','top-monomial-receipt.json'),
    ('verify-grouped-words.py','grouped-words-receipt.json'),
    ('verify-trace-shears.py','trace-shears-receipt.json'),
    ('verify-fourier-batches.py','fourier-batch-receipt.json'),
    ('verify-fibre-join.py','fibre-join-cases.json'),
    ('verify-packed-chirp.py','packed-chirp-receipt.json'),
    ('verify-trace-rader.py','trace-rader-cases.json'),
    ('verify-chirp-volume.py','chirp-volume-cases.json'),
    ('verify-factor-directory.py','factor-directory-receipt.json'),
    ('verify-plane-directory.py','plane-directory-receipt.json'),
    ('verify-plane-directory.py','plane-directory-b15.json','--nonterminal-prefix'),
    ('verify-plane-independent.py','plane-independent-receipt.json'),
    ('verify-padded-convolution.py','padded-convolution-receipt.json'),
    ('verify-lane-packed-convolution.py','lane-packed-convolution-receipt.json'),
    ('check-compiler-masks.py','compiler-mask-receipt.json'),
    ('verify-marked-directory.py','marked-directory-cases.json'),
    ('verify-structured-orbit-directory.py','structured-orbit-directory-receipt.json'),
    ('verify-ordinary-binary-product.py','ordinary-binary-product-cases.json'),
    ('verify-mod-four-word.py','mod-four-word-receipt.json'),
    ('check-mod-four-jets.py','mod-four-jets-receipt.json'),
    ('check-first-witt-carry.py','first-witt-carry-receipt.json'),
    ('verify-half-square-converse.py','half-square-converse-cases.json'),
    ('verify-macro-triadic-product.py','macro-triadic-product-receipt.json'),
    ('check-fixed-witt-precision.py','fixed-witt-precision-receipt.json'),
    ('verify-fixed-witt-independent.py','fixed-witt-independent-cases.json'),
    ('verify-macro-ck-independent.py','macro-ck-independent-cases.json'),
    ('verify-precision-striped-pascal.py','precision-striped-pascal-receipt.json'),
)

def main():
    for name, receipt, *options in CASES:
        completed = subprocess.run([sys.executable, str(HERE/name), *options],
                                   cwd=HERE, check=True, stdout=subprocess.PIPE)
        expected = (HERE/receipt).read_bytes()
        if json.loads(completed.stdout) != json.loads(expected):
            raise SystemExit(f'Certificate mismatch in {receipt}')
        print(f'{receipt} {hashlib.sha256(expected).hexdigest()}', flush=True)
    print(f'Passed {len(CASES)} numerical certificate replays.', flush=True)

if __name__=='__main__':
    main()
