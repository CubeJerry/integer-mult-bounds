#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
import json,numpy as np
P=Path(__file__).resolve().parent
s=json.loads((P/'SPECTRAL-SCREEN.json').read_text());d=json.loads((P/'PHASE-CLOSURE.json').read_text())
R=np.array([[int(2*F(x))for x in row]for row in s['R0']],dtype=object);I=np.eye(8,dtype=object);ph=[(1,0),(0,1),(-1,0),(0,-1)]
def square(bits):
    real=np.zeros((8,8),dtype=object);imag=real.copy()
    for i in range(8):
        a,b=(1,0)if bits[i]%2==0 else(0,1)
        for j in range(8):
            c,e=ph[(-bits[j])%4];real[i,j]=R[i,j]*(a*c-b*e);imag[i,j]=R[i,j]*(a*e+b*c)
    rr=real@real-imag@imag;ii=real@imag+imag@real
    return np.array_equal(rr,4*I)and not any(ii.flat)
passed=0
for r in d['results']:
    p=r['phase'];actual=square(p);expected=len({x//2 for x in p})==1
    if actual!=expected:raise ValueError('commutator criterion mismatch')
    passed+=actual
one=[(q&2).bit_count()%2 for q in s['labels']];two=[2*x for x in one]
if not square(one)or square(two)or passed!=32:raise ValueError('normalizer boundary control')
receipt={'status':'PASS_ROOT_EXACT_OLD_NORMALIZER_CRITERION','phase_count':len(d['results']),'pass':passed,'fail':len(d['results'])-passed,'width_one_control':{'frequency':2,'phase':one,'square_identity':True},'width_two_counterexample':{'frequencies':[2,2],'phase':two,'square_identity':False},'scope':'Independent exact normalized matrix check, separate from the literal physical caller and from arbitrary new normalizers.'}
(P/'NORMALIZER-RESULT.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print('PASS:32 positive,2016 negative; actual width1 and width2 controls')
