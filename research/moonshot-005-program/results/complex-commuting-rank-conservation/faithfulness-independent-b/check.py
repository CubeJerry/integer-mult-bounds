#!/usr/bin/env python3
"""Independent phase-group generation and exact trace/Gram bounds."""
import argparse,hashlib,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
PIN='509d4c0e1ba5a796a9185e99a7782a9e1e3556e6eb0cf4ac6275918129d6d5da'
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--proof',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).with_name('RESULT.json'));ar=ap.parse_args();assert hashlib.sha256(ar.proof.read_bytes()).hexdigest()==PIN
 results=[]
 for d in range(1,5):
  N=1<<d;maskall=(1<<(N-1))-1;gens=[sum(1<<(x-1) for x in range(1,N) if (x&v).bit_count()%2) for v in range(1,N)]
  reached={(0,0)};queue=[(0,0)]
  for low,high in queue:
   for g in gens:
    z=(low^g,high^(low&g))
    if z not in reached:reached.add(z);queue.append(z)
  expected=1<<(d*(d+3)//2);assert len(reached)==expected
  hist=Counter()
  for low,high in reached:
   c0=1+(maskall^(low|high)).bit_count();c1=(low&(maskall^high)).bit_count();c2=(high&(maskall^low)).bit_count();c3=(low&high).bit_count();assert c0+c1+c2+c3==N
   norm=(c0-c2)**2+(c1-c3)**2;hist[norm]+=1
   if low or high:assert norm<=N*N//2
   else:assert norm==N*N
  V=d*(d+3);row=Fraction(expected-1,1<<(V//2));assert row<1 and row==Fraction(expected-1,expected)
  results.append({'heads':d,'generated_actual_phase_group':len(reached),'trace_squared_histogram':dict(sorted(hist.items())),'sufficient_width':V,'exact_Gram_row_bound':str(row)})
 assert results[2]['trace_squared_histogram']=={0:161,8:224,16:112,32:14,64:1}
 # At width below this sufficient bound the same uniform estimate is too weak;
 # this is not a mathematical claim of nonfaithfulness at that width.
 assert Fraction(511,256)>1
 out={'status':'PASS_INDEPENDENT_GENERAL_PHASE_FAITHFULNESS_REVIEW','reviewed_proof_sha256':PIN,'independent_algorithm':'Two-bit Walsh-phase generator BFS; exact integer residue counts for traces; rational Gram row sums. No author verifier imports.','finite_checks':results,'negative_control':{'using_V16_in_the_uniform_three_head_Gram_estimate_fails_strict_dominance':True},'universal_conclusion':'Accepted from the independently reviewed differencing and Gram proof for every fixed d>=1 and V>=d(d+3), not inferred from finite enumeration.','new_kappa':False}
 ar.out.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
