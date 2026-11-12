#!/usr/bin/env python3
"""Independent rational audit; reuses root's separately written exact engine.
No author/modular checker imports. @CubeJerry, OpenAI assistance, Apache-2.0.
"""
import argparse,gzip,hashlib,importlib.util,json
from pathlib import Path
from fractions import Fraction as F

def main(a):
 spec=importlib.util.spec_from_file_location('root_engine',a.engine);e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
 raw=a.source.read_bytes();e.need(hashlib.sha256(raw).hexdigest()==e.PIN,'source pin');w=json.loads(gzip.decompress(raw));xs=sorted(w['live'])
 roots=[];facets=[];vectors=[]
 for i,x2,y2 in zip(w['hosted']['Dports'],w['hosted']['X2'],w['hosted']['Y2']):
  x=xs[i];basis=w['frames'][w['initial'][x]];e.need(len(basis)==1,'first-X line');v=basis[0]
  vectors.append(v);roots.append(e.root(v));facet=e.span(w['frames'][w['final'][y2]])
  e.need(len(facet)==256 and facet==frozenset(z for z in range(512) if (v&z).bit_count()%2==0),'actual Y2 facet dual')
  e.need(e.span(w['frames'][w['initial'][y2]])==frozenset({0}),'actual Y2 zero start')
  e.need(e.span(w['frames'][w['initial'][x2]])==frozenset({0,v}),'actual X2 line');facets.append(facet)
 e.need(len(vectors)==len(set(vectors))==96 and e.matrix_rank(roots)==8,'hosted domain')
 missing={z for z in range(1,512) if z.bit_count() in (3,7)}-set(vectors);e.need(len(missing)==24,'missing24 roots')
 cases=[];directions={}
 for z in range(1,512):
  blocked=[j for j,c in enumerate(facets) if z not in c];r=e.matrix_rank([roots[j] for j in blocked]);e.need(r==(7 if z in missing else 8),'fresh rational rank classification')
  if r==7:
   direction=e.root(z);e.need(all(sum(u*v for u,v in zip(direction,roots[j]))==0 for j in blocked),'exact null upper certificate');directions[z]=direction
  cases.append({'line':z,'blocked_count':len(blocked),'rational_rank':r})
 pairs=0
 for z in directions:
  for t in directions:
   if z<t:e.need(e.matrix_rank([directions[z],directions[t]])==2,'distinct exceptional directions');pairs+=1
 e.need(pairs==276,'all exceptional pairs')
 author=json.loads(a.author.read_text());indexed={c['line']:c for c in author['certificates']};e.need(set(indexed)==set(range(1,512)),'author511 coverage')
 e.need(author['source_sha256']==e.PIN,'author source pin')
 for c in cases:
  other=indexed[c['line']];e.need(c['rational_rank']==other['rational_rank'] and c['blocked_count']==other['unavailable_hosted_count'],'independent receipt agreement')
 D=10**40;z=8**199*D**200;lo=e.root_floor(z,200);hi=lo if lo**200==z else lo+1;price=[F(8*lo,D),F(8*hi,D)]
 envelope=json.loads(a.envelope.read_text());budget=[F(x) for x in envelope['cases']['direct_baseline']['moment_per_native_exact_bounds']]
 e.need(price[0]>F(63338026,10**6) and price[1]<F(63338027,10**6),'exact price interval')
 e.need(price[0]>budget[1] and budget[1]<48,'failure even under direct-raw optimum')
 out={'status':'PASS_INDEPENDENT_RATIONAL_REVERSE_PACKET_GATE','source_sha256':e.PIN,'author_receipt_sha256':hashlib.sha256(a.author.read_bytes()).hexdigest(),
      'reviewer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'independent_engine_sha256':hashlib.sha256(a.engine.read_bytes()).hexdigest(),
      'method':'Fresh rational elimination and actual Y2/X2 source charts; independent root engine, no author/modular imports',
      'line_cases':cases,'rank8_lines':487,'rank7_lines':24,'exceptional_lines':sorted(directions),'exceptional_pair_ranks_checked':276,
      'max_nonzero_Gram_acquisition_dimension':1,'separate_eight_packet_price_exact_bounds':list(map(str,price)),
      'best_fixed_H4_raw_budget_exact_bounds':list(map(str,budget)),'optimistic_gap_at_least':str(price[0]-budget[1]),
      'envelope_receipt_sha256':hashlib.sha256(a.envelope.read_bytes()).hexdigest(),
      'scope':'Complete Gram packets assembled from unchanged original hosted Y2 at legal charts and carried on separately paid returns. Partial factors, changed payloads, shared funded routes and common coding excluded. No new kappa.'}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({k:out[k] for k in ['status','rank8_lines','rank7_lines','optimistic_gap_at_least']}))

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['source','author','envelope','engine','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
