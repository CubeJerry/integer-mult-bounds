import argparse,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
PINS={'research/paired-query-only-bit/EFREE-CALLER.json.gz':'757b3523798f840bdb02028b23708c3416627a99ea09e7a3c4bcdc5cd0c7ce4b','research/paired-query-only-bit/EFREE-RESULT.json':'a46b6c6040f75184cab5467656811ad988c216e3bc8e44d595a5015b6e49620b','research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz':'51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'}
def need(condition,message):
 if not condition:raise ValueError(message)
def read(root,relative):
 raw=(root/relative).read_bytes();need(hashlib.sha256(raw).hexdigest()==PINS[relative],'pin '+relative)
 return json.loads(gzip.decompress(raw) if relative.endswith('.gz') else raw)
def integer_root_200(value):
 x=1<<((value.bit_length()+199)//200)
 while True:
  y=(199*x+value//(x**199))//200
  if y>=x:break
  x=y
 while x**200>value:x-=1
 while (x+1)**200<=value:x+=1
 need(x**200<=value<(x+1)**200,'200th root certificate')
 return x

def run(repository,author):
 caller=read(repository,'research/paired-query-only-bit/EFREE-CALLER.json.gz')
 ledger=read(repository,'research/paired-query-only-bit/EFREE-RESULT.json')
 word=read(repository,'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz')
 receipt=json.loads((author/'RESULT.json').read_text())
 dims={int(k):f['dim'] for k,f in word['frames'].items()}
 native_jobs=[abs(dims[e[2]]-dims[e[3]]) for e in word['program'] if e[0]=='MOVE']
 helper_jobs=[abs(dims[word['final'][i]]-dims[word['start'][i]]) for i in range(2*caller['ports'],word['public'])]
 paid=[];targets=[];query_events=[];event_counts=Counter()
 for t,e in enumerate(caller['events']):
  event_counts[e[0]]+=1
  if e[0]=='LOCAL':paid.extend(native_jobs);targets.extend(helper_jobs)
  elif e[0]=='QUERY':query_events.append(t);paid.extend([1]*caller['ports'])
  elif e[0]=='IDLE_ONE':paid.extend([caller['body_rank']*len(e[2])]*caller['ports'])
 for row in caller['diagonal']:targets.extend([row['q']+caller['body_rank']*len(row['stages'])]*caller['ports'])
 P=Counter(paid);T=Counter(targets)
 need(event_counts['LOCAL']==36 and event_counts['QUERY']==4 and event_counts['IDLE_ONE']==32,'literal caller event census')
 need(query_events==[196,198,201,349] and caller['ports']==111,'query job source census')
 need(caller['events'][349]==['QUERY',19,20],'query349 source occurrence')
 need(P==Counter({int(k):v for k,v in ledger['paid'].items()}),'complete paid source ledger')
 need(T==Counter({int(k):v for k,v in ledger['targets'].items()}),'complete target source ledger')
 need(dict(P)=={int(k):v for k,v in receipt['paid'].items()},'author paid ledger')
 need(dict(T)=={int(k):v for k,v in receipt['targets'].items()},'author target ledger')
 # Independent decimal grid and Newton roots, not author's dyadic bisection.
 D=10**30;power={}
 for rank in sorted(set(P)|set(T)):
  integer=rank**199*D**200;lower=integer_root_200(integer)
  upper=lower if lower**200==integer else lower+1
  power[rank]=(Q(lower,D),Q(upper,D))
 lower=upper=Q(0)
 for rank in set(P)|set(T):
  c=T[rank]-P[rank];lo,hi=power[rank]
  lower+=c*(lo if c>=0 else hi);upper+=c*(hi if c>=0 else lo)
 author_lower,author_upper=map(Q,receipt['margin_intervals_by_free_queries_removed']['0'])
 need(author_lower<=lower<=upper<=author_upper,'independent interval inside author enclosure')
 need(upper+444<0 and lower+445>0,'exact444/445 boundary')
 need(upper+111<0,'one query insufficient')
 need(upper+111+18*18<0 and lower+111+18*19>0,'18/19 net-unit boundary')
 for k in range(5):
  a,b=map(Q,receipt['margin_intervals_by_free_queries_removed'][str(k)])
  need(a<=lower+111*k<=upper+111*k<=b,'all query-count enclosures')
 need(len(query_events)*111==444,'entire query layer exact maximum credit')
 author_files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(author.iterdir()) if p.is_file()}
 return {'status':'PASS_INDEPENDENT_BIT_QUERY_TARGET_REVIEW','source_pins':PINS,'reviewed_author_files':author_files,
   'methods':['literal per-event native expansion','independent decimal-grid integer Newton200th roots','exact signed rational intervals'],
   'literal_query_events':query_events,'literal_event_counts':dict(event_counts),'native_jobs':len(native_jobs),'native_helpers':len(helper_jobs),
   'paid_jobs':len(paid),'target_fields':len(targets),'power_grid':str(D),
   'baseline_margin':[str(lower),str(upper)],'after_all_four_queries':[str(lower+444),str(upper+444)],
   'minimum_total_net_unit_credits':445,'minimum_extra_net_unit_credits_after_query349':334,
   'conditional_uniform_net_unit_credits_per18_changed_calls':19,
   'controls':{'444_credits_fail':True,'445_credits_pass_raw_gate':True,'a_fifth_original_query_does_not_exist':True,
               '18_uniform_credits_fail_after_query349':True,'19_uniform_credits_pass_raw_gate_after_query349':True},
   'scope':'Exact kappa1/200 with the pinned native, IDLE and target profiles fixed; all four QUERY costs granted free. '
           'Changed-provider admission and the metadata claim that PR7177 changes18 calls are outside this numerical review. '
           'The18-call calculation is conditional on that explicit count. No new kappa and no assertion of global monotonicity.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repository,a.author);a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='reviewed_author_files'},sort_keys=True,indent=2))
