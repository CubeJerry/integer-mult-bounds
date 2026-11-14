#!/usr/bin/env python3
"""Independent exact scope controls, not an implementation of the theorem."""
from pathlib import Path
import hashlib,json

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(2))%2 for j in range(2)] for i in range(2)]
A=[[0,1],[0,0]];T=[[0,0],[1,0]]
AT=mul(A,T);TA=mul(T,A)
if AT==TA:raise ValueError('noncommuting control accidentally commutes')
# First entry at Fi, legal coupled addition, then first entry at Fj.
first=[1,0];second_channel=[0,1];later=[a^b for a,b in zip(first,second_channel)]
cross=first[1]*later[0];diagonal=first[0]*later[1]
if cross==diagonal:raise ValueError('coupled-history control fails to break reciprocity')
# Exhaust all F2 weights: no assignment satisfies alternation on the 5-cycle.
accepted=[]
for mask in range(32):
    bits=[(mask>>i)&1 for i in range(5)]
    if all(bits[i]^bits[(i+1)%5]==1 for i in range(5)):accepted.append(mask)
if accepted:raise ValueError('odd-cycle alternating weights found')
p=Path('worker-c/commutative-two-channel/PROOF.md');raw=p.read_bytes()
section=raw.split(b'## 5.')[0]
out={'status':'PASS_INDEPENDENT_MATHEMATICAL_REVIEW_AND_SCOPE_CONTROLS',
     'reviewed_author_file_sha256':hashlib.sha256(raw).hexdigest(),
     'reviewed_sections_1_through_4_sha256':hashlib.sha256(section).hexdigest(),
     'reviewed_scope':'Universal argument in Sections1-4 only; any appended native-specific or finite-search sections are not covered.',
     'noncommuting_control':{'A':A,'T':T,'AT':AT,'TA':TA},
     'coupled_control':{'first':first,'injected_other_channel':second_channel,'later':later,'cross_product':cross,'diagonal_product':diagonal},
     'F2_odd_cycle_assignments_checked':32,'accepted_assignments':accepted,
     'universal_proof_comes_from':'Independent algebraic review in REVIEW.md, not this finite enumeration.'}
Path('worker-a/review-two-channel/RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'author_section_sha256':out['reviewed_sections_1_through_4_sha256']}))
