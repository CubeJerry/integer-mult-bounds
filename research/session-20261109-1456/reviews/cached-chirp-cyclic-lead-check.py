"""Independent exact arithmetic checks of the frozen analytic join.

Does not import the contribution's oracle, phase, FFT, or cyclic implementation.
The saved physical receipt is evidence of execution, not a universal proof.
Prepared for @CubeJerry with substantial OpenAI assistance.
"""
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path('/workspace/scratch/a365d332d434/worker-analytic-wave8')
PKG = ROOT / 'research/cached-chirp-cyclic-join'
receipt = json.loads((PKG / 'evidence/REPLAY.json').read_text())['final_registered']['receipt']
raw = [(400,0),(-256,64),(100,-50),(141,211),(-88,-241),(300,1),(-100,17),(11,-301)]
x = [(F(a,1024), F(b,1024)) for a,b in raw]
def plus(a,b): return a[0]+b[0], a[1]+b[1]
def minus(a,b): return a[0]-b[0], a[1]-b[1]
def div(a,d): return a[0]/d, a[1]/d
def fft4(z):
    even0, even1 = plus(z[0],z[2]), minus(z[0],z[2])
    odd0 = plus(z[1],z[3])
    d = minus(z[1],z[3]); odd1 = d[1], -d[0]
    return [div(plus(even0,odd0),4),div(plus(even1,odd1),4),
            div(minus(even0,odd0),4),div(minus(even1,odd1),4)]
left,right = fft4(x[:4]), fft4(x[4:])
ideal = [div(plus(a,b),2) for a,b in zip(left,right)] + [div(minus(a,b),2) for a,b in zip(left,right)]
got = [(F(a,1024),F(b,1024)) for a,b in receipt['output']]
error = max(abs(a-c)+abs(b-d) for (a,b),(c,d) in zip(got,ideal))
assert error == F(11,8192) < F(receipt['universal_bound']) < F(1,128)
assert all(a*a+b*b <= F(1,4) for a,b in x)
assert all(a*a+b*b < F(501,1000)**2 for a,b in got)
phase_cases = 0
for t in (2,4,8,16,32):
    for slope in range(1,t,2):
        for j in range(t):
            for k in range(t):
                lhs = slope*(j*j-((j-k)%t)**2+k*k)
                assert (lhs-2*slope*j*k) % (2*t) == 0
                assert (-2*((-slope*j)%t)*k-lhs) % (2*t) == 0
                phase_cases += 1
allocation_cases = 0
for D in range(2,35):
    for ell in range(2,12):
        A = (D-1)*(ell-1)
        C = 8*(1<<A)+9*D+18
        for chi in (0,7,31,100):
            q=chi+2
            f=max(q,16,A+13,chi+1+(C-1).bit_length(),(6*D-1).bit_length())
            assert f>ell and f-A>=13
            assert F(C,1<<f)+F(2,1<<q) <= F(1,1<<chi)
            allocation_cases += 1
helper = Path('/workspace/scratch/a365d332d434/query-optimum/scripts')
sys.path.insert(0,str(helper))
spec=importlib.util.spec_from_file_location('review_gate',helper/'check_research_commit.py')
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
gate.check(ROOT,'research/cached-chirp-cyclic-join','HEAD',False,True)
result = {
 'local_commit':'306f8c2f91e549de8a3d759467d5ac3edc47c469',
 'proof_sha256':hashlib.sha256((PKG/'PROOF.md').read_bytes()).hexdigest(),
 'independent_exact_two_stage_DFT_error':str(error),
 'phase_and_frequency_congruence_cases':phase_cases,
 'allocation_inequality_cases':allocation_cases,
 'source_byte_gate':True,
 'reviewed_obligations':['same cached payload in all three uses','actual M restoration','one final grid drop','right-to-left LSB flag ordering','half-disk admission','full f+A Fourier precision and setup costs'],
 'limitations':['lead did not repeat the 63-second numerical execution','finite q2 provider only; no production GL64/O73 execution','broad expansion and global outer recovery remain open','no new kappa']
}
out=Path(__file__).with_name('cached-chirp-cyclic-lead-review.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,sort_keys=True))
