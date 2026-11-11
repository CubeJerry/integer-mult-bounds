#!/usr/bin/env python3
"""Exact source certificate for the terminal-chart export obstruction.

No author or predecessor verifier is imported. The already proved prefixes
are replayed only on the necessary 52-input subspace; full-prefix correctness
is an inherited theorem, not claimed anew here.
"""
import argparse,collections,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PREFIXES={'direct':('ACQUISITION-PREFIX.json','f918a319b8133a2fe7ae59da97d47c2a811ee899e0b8253c61bde20c66faa98d'),'facet':('LIFTED-PREFIX.json','e87e4bfcb9772b232e6c443cf2d8ee79a7de356d381eda3aa42040e5e37003c0')}
BUDGET='b5c4a118bb7e72a31d7ba90a8cd4b72884f9fa6470710850119d709ad3f21f40'
EIGHT_PAYLOAD='a0a0dd9264f9703d7052ac1038128b04fffd165d06330c606ab1ab787053f913'
def need(x,m):
 if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def span(b):
 s={0}
 for x in b:s|={z^x for z in tuple(s)}
 return frozenset(s)
def add(a,b,c):
 z=a.copy()
 for k,v in b.items():
  t=z.get(k,F(0))+c*v
  if t:z[k]=t
  else:z.pop(k,None)
 return z
def rank(rows):
 B={}
 for orig in rows:
  a=orig.copy()
  while a:
   k=min(a)
   if k in B:a=add(a,B[k],-a[k])
   else:
    v=a[k];B[k]={j:t/v for j,t in a.items()};break
 return len(B)
def adjoint(program,out,K):
 a={out:F(1)}
 for e in reversed(program):
  op,d=e[:2];v=a.get(d,F(0))
  if not v:continue
  if op in ('INIT','CLEAR'):a.pop(d,None)
  elif op=='SCALE':
   z=v*F(e[2])
   if z:a[d]=z
   else:a.pop(d,None)
  elif op in ('ADD','COPY'):
   s=e[2];need(s!=d,'distinct source/destination');z=a.get(s,F(0))+v*F(e[3])
   if z:a[s]=z
   else:a.pop(s,None)
   if op=='COPY':a.pop(d,None)
 return {j:v for j,v in a.items() if j in K and v}
def no_exit(program,C,hub):
 out=[(k,e) for k,e in enumerate(program) if e[0]=='MOVE' and C[e[2]]==hub]
 need(not out,'an original MOVE leaves the terminal chart')
 return len([e for e in program if e[0]=='MOVE'])
def prefix_state(p,C,K):
 chart={i:f for i,f in enumerate(p['initial'])};rows={i:{} for i in chart};live=set();raw={int(k):v for k,v in p['difference_role_map'].items()}
 for q in K:rows[raw[q]]={q:F(1)}
 count=collections.Counter()
 for e in p['program']:
  op,d=e[:2];count[op]+=1
  if op=='INIT':need(d>=p['public'] and d not in chart,'fresh owned');chart[d]=e[2];rows[d]={};live.add(d)
  elif op=='CLEAR':need(d in live and chart[d]==e[2],'owned CLEAR');live.remove(d);del chart[d];del rows[d]
  elif op=='ADD':need(d in chart and e[2] in chart and C[chart[d]]==C[chart[e[2]]]==C[e[4]],'cochart ADD');rows[d]=add(rows[d],rows[e[2]],F(e[3]))
  elif op=='MOVE':
   s,t,own=e[2:];need(d in chart and chart[d]==s,'MOVE source');need(bool(own)==(d>=p['public']),'ownership flag');need((C[s]<C[t] or (own and C[t]<C[s])),'proper nested MOVE');chart[d]=t
  else:raise ValueError('unexpected prefix instruction')
 return chart,rows,live,raw,count

def run(a):
 root=a.repository;P=root/'research/moonshot-005-program/results';raw=(root/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();need(sha(raw)==NATIVE,'native pin');w=json.loads(gzip.decompress(raw));C=list(map(span,w['frames']));hub=C[127]
 source_moves=no_exit(w['program'],C,hub);need(source_moves==6310,'all original route census');owned=[e for e in w['program'] if e[0]=='MOVE' and e[4]];need(len(owned)==47,'all owned over-grant')
 budgetraw=(P/'relay-acquisition-budget/RESULT.json').read_bytes();need(sha(budgetraw)==BUDGET,'complete budget pin');budget=json.loads(budgetraw)
 eight_raw=gzip.decompress((P/'lifetime-elimination/eight.json.gz').read_bytes());need(sha(eight_raw)==EIGHT_PAYLOAD,'S8 literal pin');eight=json.loads(eight_raw);retained=sum(e[0]=='MOVE' and e[4] for e in eight['program']);need(retained==33,'retained second-owned calls')
 facetraw=(P/'paid-observable-acquisition/LIFTED-PREFIX.json').read_bytes();p=json.loads(facetraw);K=p['nonentry_donors'];need(len(K)==len(set(K))==52,'52 distinct terminal inputs');KK=set(K)
 M=set(w['live'])|{q+112 for q in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);need(KK<=M,'actual main inputs')
 endpoints=[];det=F(1)
 for q in K:
  y=q+112;need(y in M and C[w['final'][y]]!=hub and len(w['frames'][w['final'][y]])==8,'actual off-hub main endpoint');row=adjoint(w['program'],y,KK);need(set(row)=={q} and row[q] in (F(1),F(1,2)),'diagonal source endpoint witness');det*=row[q];endpoints.append({'input':q,'output':y,'final_chart':w['final'][y],'coefficient':str(row[q])})
 need(det==F(1,128),'52-endpoint determinant');need(sum(x['coefficient']=='1' for x in endpoints)==45,'45 whole coefficients')
 cases={};outside_rows=None
 for name,(file,pin) in PREFIXES.items():
  b=(P/'paid-observable-acquisition'/file).read_bytes();need(sha(b)==pin,'prefix pin '+name);p=json.loads(b);need(p['nonentry_donors']==K,'same52 donor set');chart,rows,live,rawmap,count=prefix_state(p,C,KK)
  need(all(chart[rawmap[q]]==127 and rows[rawmap[q]]=={q:F(1)} for q in K),'all52 independent raws at terminal hub')
  out={d:z for d,z in rows.items() if C[chart[d]]!=hub and z};need(set(out)=={1931,1932} and live=={1931,1932} and rank(list(out.values()))==2,'exact two-mode outside state')
  r,s=out[1931],out[1932];minor=r.get(2,F(0))*s.get(4,F(0))-r.get(4,F(0))*s.get(2,F(0));need(minor==F(-1,8),'outside source-mode rank certificate')
  if outside_rows is None:outside_rows=[r,s]
  else:need(outside_rows==[r,s],'same actual external information')
  bp=budget['variants']['four_aggregates' if name=='direct' else 'eight_facet_copies'];hi=F(bp['remaining_paid_moment_per_native_interval'][1]);ceil=int(hi);need(ceil==(2 if name=='direct' else 8),'optimistic additional-call ceiling')
  cases[name]={'prefix_sha256':pin,'nonzero_outside_physical_roles':[1931,1932],'outside_projection_rank':2,'outside_minor_columns':[2,4],'outside_minor':str(minor),'new_export_field_unit_lower_bound':50,'remaining_paid_moment_upper':str(hi),'optimistic_additional_call_ceiling':ceil,'minimum_additional_offhub_prefix_mode_rank_to_fit':50-ceil,'new_field_lower_bound_after_granting_all33_retargeted_difference_owned_calls':17,'exclusion_even_after33_free_retargeted_calls':17>hi}
  need(F(50)>hi and F(17)>hi,'both fixed-profile exclusions')
 # Controls check premises and the dimension mechanism, rather than only pins.
 controls=[]
 bad=copy.deepcopy(endpoints);bad[0]['coefficient']='3'
 try:
  need(all(adjoint(w['program'],x['output'],KK)=={x['input']:F(x['coefficient'])} for x in bad),'mutated endpoint coefficient')
 except ValueError as e:controls.append({'mutation':'wrong_endpoint_coefficient','result':str(e)})
 else:raise ValueError('wrong endpoint mutant accepted')
 altered=w['program']+[['MOVE',w['public'],127,endpoints[0]['final_chart'],True]]
 try:no_exit(altered,C,hub)
 except ValueError as e:controls.append({'mutation':'grant_new_terminal_exit_as_old_route','result':str(e)})
 else:raise ValueError('terminal-exit premise mutant accepted')
 independent=outside_rows+[{q:F(1)} for q in K if q not in (2,4)];need(rank(independent)==52,'50 globally supplied coordinate complements suffice for cut rank')
 need(rank(outside_rows*26)==2,'duplicate fields do not create52 modes');need(rank(outside_rows+[{2:F(1)}])==3,'one new mode reduces deficit only one')
 controls += [{'grant':'50 independent global coordinate modes K except2,4','outside_rank':52,'remaining_cut_deficit':0,'scope':'Sharpness of this global-information relaxation only, not a legal50-route construction.'},{'grant':'52 copies of the two existing aggregate fields','outside_rank':2,'remaining_cut_deficit':50},{'grant':'one additional independent outside coordinate','outside_rank':3,'remaining_cut_deficit':49},{'grant':'free global original-input reread of all52 coordinates','outside_rank':52,'remaining_cut_deficit':0,'scope':'Excluded source-access interface change.'}]
 cert={'source_sha256':NATIVE,'canonical_hub_basis':w['frames'][127],'all_original_MOVEs':source_moves,'original_MOVEs_leaving_canonical_hub':0,'original_owned_moves':47,'owned_source_dimension_histogram':dict(sorted(collections.Counter(len(w['frames'][e[2]]) for e in owned).items())),'retained_second_owned_moves':retained,'terminal_input_roles':K,'selected_offhub_endpoints':endpoints,'selected_endpoint_rank':52,'selected_endpoint_determinant':str(det),'outside_rows_on_K':[{str(q):str(v) for q,v in sorted(z.items())} for z in outside_rows],'cases':cases,'negative_controls':controls}
 ctext=json.dumps(cert,indent=2,sort_keys=True)+'\n';cp=a.package/'CERTIFICATE.json'
 if a.write_certificate:cp.write_text(ctext)
 else:need(cp.read_text()==ctext,'exact certificate reproduction')
 return {'status':'PASS_TERMINAL_HUB_EXPORT_50_FIELD_OBSTRUCTION','source_sha256':NATIVE,'certificate_sha256':sha(cp.read_bytes()),'target_rank':52,'initial_outside_rank':2,'minimum_new_export_volume_in_full_field_units':50,'after33_free_retargeted_difference_owned_exports':17,'additional_offhub_mode_rank_required_for_facet_eight_call_budget':42,'cases':cases,'controls':len(controls),'scope':'Every characteristic-zero linear continuation of either exact prefix, under the retained cochart/complete-field model and fixed original route geometry, needs50 further outbound field units. Arbitrary ordering, repetition and helper recoding on original edges are granted. Changed prefix information, unpriced source rereads, nonlinearity, or changed geometry/cost profiles are outside. No global multiplication lower bound or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--package',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--write-certificate',action='store_true');p.add_argument('--output',type=Path,required=True);a=p.parse_args();v=run(a);a.output.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n');print(v['status'])
