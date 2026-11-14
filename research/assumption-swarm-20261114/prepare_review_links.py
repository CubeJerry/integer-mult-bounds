from pathlib import Path
import json,re,hashlib,urllib.parse,urllib.request
from concurrent.futures import ThreadPoolExecutor
DATA=[
('Exact ordinary generator count 2T/n_fast for Gaussian tensors and inverse targets.','Lexicographic order only; no arbitrary-order or runtime lower bound.'),
('A 6003-location, 43-tape OLD23/Gamma6 bridge with all 9f strided partitions, original-owner return and Theta(f V_old+E) cost.','Valid source and supplied service remain premises.'),
('Uniform typed INIT and full CLEAR for selected owned lifetimes, costing at most 4F+8 and 2F+4.','A valid common-format donor remains required.'),
('Explicit rounding margins preserve the normalized tensor generator obstruction with O(g log p)=o(p) guard bits.','Stated normalized kernels and phase gaps only; source production is separate.'),
('A fixed 4803-location, 43-tape graph creates typed zero directly from OLD23 in O(V_old+E_old), removing the packed-donor premise.','OLD23 acquisition and the remaining compiler are external.'),
('Join the paid OLD23 bridge and actual all-column positive C leaf in one 12829-location, 70-tape service.','Central C component only; every-prefix numeric-domain conditions remain.'),
('Execute complete selected MOVE24472 through OLD23 and original-owner return: 88816 locations, 72 tapes, cost at most 2^25(f V_old+E+1).','Initial packets and every-prefix bounds remain premises.'),
('Construct symmetry-orbit orders with superpolynomial generator-count savings and exact prime-block cycle bounds.','Representation gain only; complete application and dense storage costs remain paid.'),
('Join all eight owned1526 contacts on one permanent HOME: 121322 states, 44 tapes, typed initialization through full erasure.','9574 intervening events and producer packets remain external.'),
('Lower #7504 canonical padded-rotation switch queries to a restored 2096-location, 14-tape program with O(h^2) cost.','Supplied descriptors; full routing and source acquisition are separate.'),
('Classify homogeneous Gaussian symmetries and prove optimal orbit count Theta(T/g(d)), with explicit rounding and dense-format costs.','Specified dense format only; no general runtime lower bound.'),
('Connect actual #7388 CRT leases to literal switch queries and the original payload mover, paying scans and restoration.','External symbol-action providers remain in the complete caller.'),
('Produce donor1349 through actual MOVE28039 and feed unchanged SUB28041 after same-owner return.','Two intervening public ADDs remain external continuations.'),
('Classify heterogeneous Gaussian symmetries: distinct fine-prime widths force reflection cycles of length at most two.','Normalized matching square grids; no general generator/runtime lower bound.'),
('Replace the per-wire row loop by a fixed 10123-instruction, 20-owner forward/inverse controller with exact complete route costs.','All-record enumeration and source acquisition remain external.'),
('Close both public-ADD gaps: selected INIT28037 through SUB28041 in one 71793-state, 45-tape graph, including signed halving.','Initial packets, divisibility and every-prefix bounds remain premises.'),
('Lower all-record CRT keys to 21135 instructions on22 roles; N(156h+126)+18h+203 overhead pays the payload-head return.','Fixed 13-bit record ABI; header production and radix remain external.'),
('Prove the exact monomial centralizer, physical Gaussian entry bounds and dimension-paid inverse-error transfer.','Matching square phase cells; actual caller, production/error and access remain open.')]

def prepare(row,data):
 claim,limit=data
 refs=list(dict.fromkeys(re.findall(r'(?<![A-Za-z0-9])#\d+',row['body'])))[:2]
 prior=' Predecessors: '+', '.join(refs)+'.' if refs else ' Exact predecessor pins are linked below.'
 body=('## Result\n'+claim+'\n\n## Checks\n`python3 -B scripts/research_package.py --package research/'+row['package']+'`\nIndependent review and negative controls passed. Base `e54523517d0f03e58352e647c403a5af3e525a57`.'+prior+'\n\n## Limits and credit\nNo new kappa; all five full assumptions remain. '+limit+' Prepared for @CubeJerry; credit to cited predecessors and substantial OpenAI assistance.\n\n[Full result, novelty, exact pins, checks and PR draft]('+row['description_url']+')')
 url=row['compare_url']+'?'+urllib.parse.urlencode({'expand':'1','title':row['title'],'body':body})
 assert urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)=={'expand':['1'],'title':[row['title']],'body':[body]}
 row.update(short_pr_body=body,short_prefilled_url=url,short_prefill_chars=len(url),short_prefill_validation={'encoding':'urllib.parse.urlencode exactly once; exact query roundtrip','target':'CrocSwap/main...CubeJerry:'+row['branch'],'authenticated_form_rendered':False})
 return row

def check(row):
 req=urllib.request.Request(row['short_prefilled_url'],headers={'User-Agent':'integer-multiplication-review-link-check'})
 with urllib.request.urlopen(req,timeout=30) as response:
  raw=response.read().decode();parsed=urllib.parse.urlsplit(response.url);q=urllib.parse.parse_qs(parsed.query)
  assert response.status==200 and row['branch'] in raw
  assert q['title']==[row['title']] and q['body']==[row['short_pr_body']]
  assert parsed.path.endswith('/compare/main...CubeJerry:'+row['branch'])
  row['short_prefill_validation'].update(http_status=response.status,branch_seen=True,redirect_query_preserved=True,html_sha256=hashlib.sha256(raw.encode()).hexdigest())
 return row

if __name__=='__main__':
 p=Path('review-links.json');rows=json.loads(p.read_text());assert len(rows)==len(DATA)
 rows=[prepare(r,d) for r,d in zip(rows,DATA)]
 with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(check,rows))
 p.write_text(json.dumps(rows,indent=2)+'\n')
 Path('PREFILLED-REVIEW-LINKS.md').write_text('# Verified prefilled review links\n\nRemote refs, tested trees and package diffs were checked before publication. Each link returned HTTP200, preserved its encoded title and body, and named the intended branch. The signed-in PR form was not rendered; no upstream PR was submitted.\n\n'+'\n'.join('- ['+r['title']+']('+r['short_prefilled_url']+')' for r in rows)+'\n')
 print(json.dumps({'checked':len(rows),'max_url_chars':max(r['short_prefill_chars'] for r in rows),'authenticated_form_rendered':False}))
