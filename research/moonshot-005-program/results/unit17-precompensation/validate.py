"""Semantic negative controls; this is the author's checker, not independent review."""
import argparse,gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from build import Machine,expected_common,need

def main(a):
 w=json.loads(gzip.decompress(a.source.read_bytes()));blob=a.word.read_bytes();p=json.loads(gzip.decompress(blob));q={int(k):v for k,v in p['difference_role_map'].items()};E=expected_common(w)
 E.update({r:{r:F(1)} for r in q.values()})
 for x in p['completed_second_shear_donors']:E[q[x+112]]={q[x]:F(1),q[x+112]:F(1)}
 def check(program):
  m=Machine(p['initial'],w['frames'],1880+p['owned_fields'])
  for e in program:m.run(e)
  return [j for j in range(1880) if m.rows[j]!=E[j]]
 tests=[]
 # A source gain2 is not a literal overwrite.
 z=[list(e) for e in p['program']];i=next(i for i,(e,k) in enumerate(zip(z,p['marks'])) if k=='encoder_add_v' and F(e[3]) not in (0,1));z[i][3]='1';bad=check(z);need(bad,'wrong normalized gain rejected');tests.append({'control':'replace normalized gain by1','mismatched_rows':len(bad),'first_mismatch':bad[0]})
 # All initial snapshots must follow every common input pre-correction.
 pairs=[]
 for i,k in enumerate(p['marks']):
  if k=='initial_history_snapshot':pairs.extend([i-1,i])
 take=set(pairs);z=[p['program'][i] for i in pairs]+[e for i,e in enumerate(p['program']) if i not in take];bad=check(z);need(bad,'early snapshots rejected');tests.append({'control':'take initial history before common pre-correction','mismatched_rows':len(bad),'first_mismatch':bad[0]})
 # The source cache must hold actual v, not the independent difference q.
 z=[list(e) for e in p['program']];i=next(i for i,k in enumerate(p['marks']) if k=='form_actual_q');need(p['marks'][i-1]=='cache_actual_v' and z[i-1][0]=='ADD','cache ordering');z[i-1],z[i]=z[i],z[i-1];bad=check(z);need(bad,'q substituted for v rejected');tests.append({'control':'cache q instead of actual v','mismatched_rows':len(bad),'first_mismatch':bad[0]})
 out={'status':'PASS_THREE_SEMANTIC_NEGATIVE_CONTROLS','word_compressed_sha256':hashlib.sha256(blob).hexdigest(),'controls':tests,'independent_review':False};a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
