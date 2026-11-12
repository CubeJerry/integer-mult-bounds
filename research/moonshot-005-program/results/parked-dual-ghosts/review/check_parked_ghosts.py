#!/usr/bin/env python3
"""Independent parked-original/late-zero audit; imports no author generator."""
import argparse,copy,gzip,json
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
from cohort_geometry import SOURCE_PIN,root,rank,space,require
from check_cohort_word import load,sha,inverse,rowadd,combine,typed,prefix_execute,moment,INVOICE_PIN

PINS={
 'one':('3d7ada763346a5658ef481f84bf895b668005a558e999be431d2257e16fbd101','2e0853ba95763f5182d675fbf08317871ca4b5df7328066230e446ef959f782a','1ddafe5fb71345cb6f4225959716213de6f24d8e9c287aa7bad09b09046102fb'),
 'eight':('bd5c598c9ac30bffdcdd85a4cb059376ceb83846144fa9cfa28a347a9ea2ef17','bd00e7e4f8e9f12f48694dedd1886ef2a4b0677f0333a613fec5bb361c34514a','28eb67043a72a60697771c1a62634fe89c9b7bf8b99146daffc4b3b7864afbb6')}
S=[0,7,20,27,36,46,57,111];B=[5,56,65,69,77,96,100,103]
def operands(o):return o[1:3] if o[0] in ('ADD','COPY') else o[1:2]
def clean(c):return {r:n for r,n in c.items() if n}
def audit(source,parent,word,variant,report,invoice,literal=True):
 xs=sorted(source['live']);host={xs[p]:(source['hosted']['X2'][j],source['hosted']['Y2'][j]) for j,p in enumerate(source['hosted']['Dports'])};hs=sorted(host)
 raw={int(r):v for r,v in word['private_role_map'].items()};q={r:{raw[r]:F(1),r:F(-1)} for r in raw};frames=source['frames']+[x['frame'] for x in word.get('additional_charts',[])];spaces=list(map(space,frames))
 roots={x:root(source['frames'][source['initial'][x]][0]) for x in xs};gram=lambda i,j:F(sum(a*b for a,b in zip(roots[i],roots[j])),8)
 selected=[56] if variant=='one' else S;complete=[] if variant=='one' else B
 decoder=[] if variant=='one' else [[gram(s,b) for s in S] for b in B]
 if variant=='eight':
  require([[sum(decoder[i][k]*decoder[j][k] for k in range(8)) for j in range(8)] for i in range(8)]==[[F(i==j) for j in range(8)] for i in range(8)],'source-derived exact orthogonal decoder')
 oldcut=parent['marks']['common_starts'];records=[];byfirst={};ghosts=[]
 for k,x in enumerate(selected):
  br,dr=host[x];j=raw[br];uses=[(e,o) for e,o in enumerate(parent['program'][400:oldcut],400) if j in operands(o)];require(uses,'real first use')
  e,o=uses[0];require(o[0]=='MOVE' and o[2]==source['initial'][br] and o[4] is False and len(frames[o[3]])==6,'unread authentic line to dimension6 first ascent')
  g=1880+parent['owned_fields']+k;ghosts.append(g);byfirst[e]=(j,g,o[3]);records.append(dict(first_X=x,hosted_B=br,raw_B=j,ghost=g,first_parent_event=e,activation_chart=o[3]))
 out=[];active={};chron={};birth={}
 for e,o in enumerate(parent['program'][:oldcut]):
  chron[e]=len(out)
  if e in byfirst:
   j,g,c=byfirst[e];out.append(['MOVE',j,o[2],127,False]);birth[g]=len(out);out.append(['INIT',g,c]);active[j]=g
  else:
   n=list(o)
   for p in ([1,2] if o[0] in ('ADD','COPY') else [1]):n[p]=active.get(n[p],n[p])
   if n[0]=='MOVE' and n[1] in ghosts:n[4]=True
   out.append(n)
 observation=len(out)
 for r in records:out.append(['ADD',r['raw_B'],r['ghost'],'1',127])
 for i,b in enumerate(complete):
  for k,g in enumerate(ghosts):
   if decoder[i][k]:out.append(['ADD',raw[host[b][0]],g,str(-decoder[i][k]),127])
 for g in ghosts:out.append(['CLEAR',g,127])
 cut=len(out);out+=parent['program'][oldcut:]
 if literal:require(out==word['program'],'independently re-emitted complete literal word')
 require(word['marks']['common_starts']==cut and word['parked_dual_ghosts']['observation_boundary']==observation,'actual observation and common boundaries')
 for name,e in parent['marks'].items():
  mapped=chron[e] if e<oldcut else e+cut-oldcut
  require(word['marks'][name]==mapped,'chronological mark '+name)
 require(word['additional_charts']==parent['additional_charts'],'inherited chart identities unchanged')
 entry,_=prefix_execute(parent,400)
 for x in selected:require(entry[raw[host[x][0]]]==q[host[x][0]],'original qB at entry')
 pr,pl=prefix_execute(parent,oldcut);obs,ol=prefix_execute(word,observation);after,al=prefix_execute(word,cut)
 require(set(obs)==set(pr)|set(ghosts) and set(after)==set(pr) and al==pl,'complete live interfaces and final chart preservation')
 bslots=[raw[host[x][0]] for x in hs];droles=[host[x][1] for x in hs]
 def dcoeff(row):
  coeff=[row.get(raw[d],F(0)) for d in droles];require(combine(coeff,[q[d] for d in droles])==row,'pure original D row on all1880 inputs');return coeff
 R=[]
 for x in hs:R.append(dcoeff(rowadd(pr[raw[host[x][0]]],q[host[x][0]],F(-1))))
 for r in records:
  j=r['raw_B'];g=r['ghost'];br=r['hosted_B'];expected=rowadd(pr[j],q[br],F(-1))
  require(obs[j]==q[br] and ol[j]==127,'real parked original at hub');require(obs[g]==expected and ol[g]==127,'actual retained pure-D ghost at hub')
  r['D_coefficients']=[[d,str(c)] for d,c in zip(droles,dcoeff(obs[g])) if c]
  require(all(spaces[r['activation_chart']]<=spaces[source['final'][d]] for d,c in zip(droles,dcoeff(obs[g])) if c),'actual partial ghost support respects birth chart')
  for j2 in pr:
   if j2!=j:require(pr[j2].get(j,F(0))==0,'all other endpoints independent of parked original')
 for j in pr:
  expected=pr[j]
  if j in [r['raw_B'] for r in records]:expected=q[next(r['hosted_B'] for r in records if r['raw_B']==j)]
  require(obs[j]==expected,'all1880 original columns at retained observation')
  delta={}
  for b in complete:
   if j==raw[host[b][0]]:delta=rowadd({},q[host[b][1]],F(-1))
  require(after[j]==rowadd(pr[j],delta),'all1880 original columns at common entry')
 # The changed fields are isolated until authentic final common recoupling.
 for b in complete:
  j=raw[host[b][0]];touch=[o for o in word['program'][cut:] if j in operands(o)]
  require(touch==[['ADD',j,host[b][0],'1',source['final'][host[b][0]]]],'changed private endpoint has no suffix feedback')
 require(word['program'][cut:]==parent['program'][oldcut:],'complete literal common/final suffix')
 # Independent 400-input inverse, using the real post-prefix rows.
 for x in xs:require(after[raw[x]]==q[x],'first-X original preserved')
 for x in hs:require(after[raw[host[x][1]]]==q[host[x][1]],'original D preserved')
 for x in xs:
  y=x+112;row=after[raw[y]];cy=row.get(raw[y],F(0));require(cy in (F(1),F(1,2)),'nonzero known own-Y coefficient')
  rest=rowadd(row,combine([cy]+[row.get(raw[z],F(0)) for z in xs],[q[y]]+[q[z] for z in xs]),F(-1));require(all(i<1480 for i in rest),'Y has only restored X, own input and known common inputs')
 actualR=[dcoeff(rowadd(after[raw[host[x][0]]],q[host[x][0]],F(-1))) for x in hs]
 require(word['hosted_reverse_output_corrections']=={str(host[x][0]):[[d,str(c)] for d,c in zip(droles,actualR[i]) if c] for i,x in enumerate(hs)},'all96 actual correction metadata rows match interpreted inputs')
 residual=[[actualR[i][j]+F(i==j) for j in range(96)] for i in range(96)]
 zero=[hs[i] for i,row in enumerate(residual) if not any(row)];require(zero==complete,'exact individual reverse completion set')
 rr=rank(residual);require(rr==88,'exact residual rank88')
 nonzero_cols=sum(any(row[j] for row in residual) for j in range(96));require(nonzero_cols==96,'all96 residual columns still nonzero')
 if variant=='eight':
  remaining=[i for i,x in enumerate(hs) if x not in B];require([[residual[i][j] for j in remaining] for i in remaining]==[[F(i==j) for j in range(88)] for i in range(88)],'explicit88x88 identity lower-rank minor')
 # Add independent phantom coordinates at each zero birth; do not import the
 # author's phantom calculation or infer it from the actual zero evaluation.
 def inject(e,state,loc,o):
  for k,g in enumerate(ghosts):
   if e==birth[g]+1:state[g]=rowadd(state[g],{1880+k:F(1)})
 phantom,_=prefix_execute(word,observation,inject)
 N=[[phantom[j].get(v,F(0)) for v in bslots]+[phantom[j].get(1880+k,F(0)) for k in range(len(ghosts))] for j in bslots+ghosts]
 require([row[:96] for row in N[:96]]==[[F(i==j) for j in range(96)] for i in range(96)] and not any(c for row in N[96:] for c in row[:96]),'actual phantom block [[I,K],[0,L]]')
 L=[row[96:] for row in N[96:]];Li=inverse(L);require(Li is not None,'actual phantom ghost block invertible')
 normalized=[combine(row,[obs[g] for g in ghosts]) for row in Li]
 for r,row in zip(records,normalized):require(all(spaces[r['activation_chart']]<=spaces[source['final'][d]] for d,c in zip(droles,dcoeff(row)) if c),'normalized actual ghost causal support')
 bill=typed(source,word);pb=typed(source,parent);require(bill['final']==pb['final'] and bill['peak']==43,'whole-word final charts/ownership/peak')
 gh=Counter(abs(len(frames[o[3]])-len(frames[o[2]])) for o in word['program'] if o[0]=='MOVE' and o[1] in ghosts)
 delta=bill['ranks'].copy();delta.subtract(pb['ranks']);require(clean(delta)=={8:len(ghosts),5:-len(ghosts)},'complete transport delta includes raw parking and every owned tail')
 require(sum(r*n for r,n in bill['rawranks'].items())==3200 and sum(r*n for r,n in gh.items())==3*len(ghosts),'raw and new owned rank mass')
 logical=set(raw);oldraw=Counter(abs(len(source['frames'][o[3]])-len(source['frames'][o[2]])) for o in source['program'] if o[0]=='MOVE' and o[1] in logical)
 native=Counter(abs(len(source['frames'][o[3]])-len(source['frames'][o[2]])) for o in source['program'] if o[0]=='MOVE');extra=bill['ranks'].copy();extra.subtract(native);extra.subtract(bill['rawranks']);extra.subtract(gh);require(clean(extra)=={9:8},'all and only8 inherited E8 packet transports beyond native/raw/ghost')
 T={int(r):n for r,n in invoice['T4'].items()};P={int(r):n for r,n in invoice['P4'].items()};paid={r:P.get(r,0)+18*(bill['rawranks'][r]-oldraw[r]+gh[r])+144*(r==9) for r in P.keys()|oldraw.keys()|bill['rawranks'].keys()|gh.keys()|{9}};paid=clean(paid)
 require(paid=={int(r):n for r,n in report['conditional_caller']['P_partial'].items()},'independent full H4 caller invoice')
 margin=tuple(v/18 for v in moment({r:T.get(r,0)-paid.get(r,0) for r in T.keys()|paid.keys()}))
 bounds=[report['conditional_caller']['remaining_moment_per_native_lower'],report['conditional_caller']['remaining_moment_per_native_upper']];require(F(bounds[0])<=margin[0]<=margin[1]<=F(bounds[1]),'independent exact integer-power moment bracket')
 return dict(instructions=len(out),counts=dict(bill['counts']),raw_profile=dict(bill['rawranks']),raw_calls=sum(bill['rawranks'].values()),raw_rank_mass=3200,owned_ghost_profile=dict(gh),owned_peak=43,observation_boundary=observation,common_boundary=cut,ghost_records=records,normalized_phantom_L=[[str(x) for x in row] for row in L],ghost_rank=rank([dcoeff(obs[g]) for g in ghosts]),completed_reverse_first_X=complete,reverse_residual_rank=rr,nonzero_reverse_residual_columns=nonzero_cols,terminal_separated_source_first_departure_floor=96,full_input_columns=1880,private_triangular_inverse_rows=400,literal_suffix_instructions=len(word['program'])-cut,paid_profile=paid,target_profile=T,paid_positions=sum(paid.values()),target_positions=sum(T.values()),rank_surplus=sum(r*(T.get(r,0)-paid.get(r,0)) for r in T.keys()|paid.keys()),remaining_moment_exact=list(map(str,margin)),remaining_moment_approx=float(margin[0]))

def main(a):
 source=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',True,pin=SOURCE_PIN);invoice=load(a.repo/'research/moonshot-005-program/results/eight-packet-seven-corrections-fused/INPUT-INVOICE.json',pin=INVOICE_PIN);results={};controls={}
 for v in ('one','eight'):
  path=a.one_parent if v=='one' else a.eight_parent;pin,payload,wp=PINS[v];parent=load(path,True,pin=pin,payload=payload);word=load(a.package/v/'WORD.json.gz',True,payload=wp);report=load(a.package/v/'RESULT.json')
  result=audit(source,parent,word,v,report,invoice);result.update(word_payload_sha256=wp,word_sha256=sha((a.package/v/'WORD.json.gz').read_bytes()),parent_sha256=pin,parent_payload_sha256=payload,author_result_sha256=sha((a.package/v/'RESULT.json').read_bytes()));results[v]=result
  maps=load(a.package/v/'CHART-MAPS.json');pairs=lambda w:{(o[2],o[3]) for o in w['program'] if o[0]=='MOVE'};introduced=pairs(word)-pairs(parent);recipes=maps['introduced_maps'];frames=source['frames']+[c['frame'] for c in word['additional_charts']]
  require({(r['source'],r['target']) for r in recipes}==introduced,'exact introduced parking-map coverage')
  for r in recipes:require(r['recipe']['rank']==len(frames[r['target']])-len(frames[r['source']])==8,'complete parking map rank8')
  require(maps['word_sha256']==result['word_sha256'] and maps['parent_word_sha256']==pin and maps['wrong_global_phase_rejected'],'map artifact word pins and phase control')
  for name,epin in maps['engine_pins'].items():require(sha((a.repo/'research/shared-wire-split-composition/frozen'/name).read_bytes())==epin,'retained exact chart engine pin')
  result.update(introduced_map_coverage=len(introduced),map_receipt_sha256=sha((a.package/v/'CHART-MAPS.json').read_bytes()),chart_engine_scope='Existing exact Clifford and independent signed-Pauli engines credited; fresh map coverage/rank/pin checks here, not a third phase engine.')
  # Literal reconstruction rejects actual source mutations independently of
  # the author's AUDIT receipts; semantic controls below also bypass pins.
  g=word['parked_dual_ghosts'];mutations={}
  init=g['records'][0]['activate_event'];restore=g['records'][0]['public_restore_event'];tail=next(i for i,o in enumerate(word['program']) if o[0]=='MOVE' and o[1]==g['records'][0]['ghost'])
  for name,e,p,val in [('wrong_birth_chart',init,2,3),('unpaid_owned_tail',tail,4,False),('missing_public_restoration',restore,3,'0')]:
   bad=copy.deepcopy(word);bad['program'][e][p]=val
   try:audit(source,parent,bad,v,report,invoice,literal=False)
   except (ValueError,AssertionError,KeyError):mutations[name]='REJECTED'
   else:raise ValueError('negative control accepted '+name)
  # Omitted ghost transport changes the independently reconstructed invoice.
  badreport=copy.deepcopy(report);r=next(iter(result['owned_ghost_profile']));badreport['conditional_caller']['P_partial'][str(r)]-=18
  try:audit(source,parent,word,v,badreport,invoice)
  except (ValueError,AssertionError,KeyError):mutations['omit_owned_tail_from_invoice']='REJECTED'
  else:raise ValueError('unpaid ghost control accepted')
  if v=='eight':
   bad=copy.deepcopy(word);e=g['completion_events'][0]['event'];bad['program'][e][3]=str(-F(bad['program'][e][3]))
   try:audit(source,parent,bad,v,report,invoice,literal=False)
   except (ValueError,AssertionError,KeyError):mutations['wrong_actual_ghost_decoder']='REJECTED'
   else:raise ValueError('wrong decoder control accepted')
  bad=copy.deepcopy(word);g0=g['records'][0];e=next(e for e,o in enumerate(bad['program']) if e>g0['activate_event'] and o[0]=='ADD' and o[2]==g0['ghost']);bad['program'][e][2]=g0['physical_B']
  try:audit(source,parent,bad,v,report,invoice,literal=False)
  except (ValueError,AssertionError,KeyError):mutations['free_parked_original_replaces_encoded_ghost']='REJECTED'
  else:raise ValueError('free original oracle control accepted')
  controls[v]=mutations
 out=dict(status='PASS_INDEPENDENT_PARKED_DUAL_GHOSTS',source_sha256=SOURCE_PIN,checker_sha256=sha(Path(__file__).read_bytes()),results=results,negative_controls=controls,scope='Finite exact source words. Actual late-zero observations and eight individual reverse completions; no full global adjoint or new kappa. All96 terminal residual columns remain nonzero.')
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({v:{k:x[k] for k in ('instructions','ghost_rank','reverse_residual_rank','completed_reverse_first_X','remaining_moment_approx')} for v,x in results.items()},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--one-parent',type=Path,required=True);p.add_argument('--eight-parent',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
