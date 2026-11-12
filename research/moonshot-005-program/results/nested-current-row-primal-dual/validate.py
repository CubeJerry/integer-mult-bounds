#!/usr/bin/env python3
"""Author's second exact replay with explicit intermediate row gates.

No generator imports. This is supplementary validation by the construction
author, not an independent-agent mathematical review.
"""
import argparse,copy,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
SOURCE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153'
def need(v,m):
 if not v:raise ValueError(m)
def span(vs):
 S={0}
 for v in vs:S|={u^v for u in tuple(S)}
 return frozenset(S)
def addto(r,s,c):
 for k,v in s.items():
  x=r.get(k,F(0))+c*v
  if x:r[k]=x
  else:r.pop(k,None)
def root(v):
 bits=[j for j in range(9) if v>>j&1]
 if len(bits)==3:return [2*int(j in bits) for j in range(8)] if 8 in bits else [1 if j in bits else -1 for j in range(8)]
 need(len(bits)==7,'source root type');i,j=[k for k in range(9) if k not in bits]
 return [1 if k==i else -1 for k in range(8)] if j==8 else [2*(int(k==i)-int(k==j)) for k in range(8)]
def run(s,w,gate=True):
 frames=s['frames']+[d['frame'] for d in w.get('additional_charts',[])];spaces=list(map(span,frames));raw={int(k):v for k,v in w['private_role_map'].items()};rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(w['initial']));q={r:{p:F(1),r:F(-1)} for r,p in raw.items()};joins={r['before_primal']:r for r in w.get('nested_acquisition',{}).get('records',[]) if 'before_primal' in r};checks=[]
 def qrow(serial):
  row={}
  for r,c in serial:addto(row,q[r],F(c))
  return row
 for t,o in enumerate(w['program'][:w['marks']['common_starts']]):
  if gate and t in joins:
   r=joins[t]
   for bank,fields,expected in [('primal',r['four_current_carriers'],r['incoming_current_rows']),('dual',r['four_current_dual_carriers'],r['incoming_dual_rows'])]:
    for field,e in zip(fields,expected):need(loc[raw[field]]==r['chart'] and rows[raw[field]]==qrow(e),'actual '+bank+' nested input row at event '+str(t))
   checks.append({'event':t,'chart':r['chart'],'primal_current_row_supports':[len(x) for x in r['incoming_current_rows']],'dual_current_row_supports':[len(x) for x in r['incoming_dual_rows']]})
  op,d=o[:2]
  if op=='INIT':need(d>=1880 and d not in rows and d<1880+w['owned_fields'],'fresh declared owned lifetime');rows[d]={};loc[d]=o[2]
  elif op=='CLEAR':need(d>=1880 and loc.get(d)==o[2],'owned clear');del rows[d];del loc[d]
  elif op=='MOVE':
   c0,c1,owned=o[2:];need(d in rows and loc[d]==c0 and type(owned)is bool and owned==(d>=1880),'actual MOVE source and ownership')
   need(spaces[c0]<spaces[c1] or owned and spaces[c1]<spaces[c0],'strict nested MOVE');loc[d]=c1
  elif op=='SCALE':need(d in rows and loc[d]==o[3] and F(o[2]),'cochart nonzero scale');rows[d]={k:F(o[2])*v for k,v in rows[d].items()}
  elif op in ('ADD','COPY'):
   src,c,C=o[2:];need(d!=src and d in rows and src in rows and loc[d]==loc[src]==C,'actual cochart ADD at '+str(t));need(op!='COPY' or not rows[d],'actual zero COPY target');addto(rows[d],rows[src],F(c))
  else:raise ValueError('unknown opcode')
  if t+1==w['marks'].get('all_active_donors_restored'):
   need(all(rows[raw[x]]==q[x] and loc[raw[x]]==127 for x in s['live']),'all104 original first donors restored')
 return rows,loc,checks
def main(a):
 sb=a.source.read_bytes();pb=a.parent.read_bytes();wb=a.word.read_bytes();need(hashlib.sha256(sb).hexdigest()==SOURCE and hashlib.sha256(pb).hexdigest()==PARENT,'immutable source and parent pins')
 s=json.loads(gzip.decompress(sb));p=json.loads(gzip.decompress(pb));w=json.loads(gzip.decompress(wb));raw={int(k):v for k,v in w['private_role_map'].items()};q={r:{v:F(1),r:F(-1)} for r,v in raw.items()};roots={x:root(s['frames'][s['initial'][x]][0]) for x in s['live']};hosted={s['live'][i]:(x,y) for i,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])}
 selected=[0,1,2,98,99,103];oldY=[112,113,210];newY=[114,211,215]
 need(all(roots[c]==[u-v for u,v in zip(roots[a0],roots[b0])] for a0,b0,c in [(0,1,98),(0,2,99),(1,2,103)]),'exact A3 source root identities')
 W={x+112:{d:-F(sum(c*v for c,v in zip(roots[x],roots[d])),8) for d in s['live'] if d!=x and sum(c*v for c,v in zip(roots[x],roots[d]))} for x in selected}
 signatures={d:tuple(y for y in sorted(W) if d in W[y]) for d in s['live']};newstars={114:(112,113,114),211:(112,210,211),215:(113,210,215)};last=(114,211,215)
 forward={y:W[y].copy() for y in oldY}
 for y in newY:forward[y]={d:W[y][d] for d,g in signatures.items() if g==newstars[y] or y==114 and g==last}
 reverse={}
 for y,r in forward.items():
  for d,c in r.items():
   if d in hosted:reverse.setdefault(hosted[d][0],{})[hosted[y-112][1]]=-c
 declared=w['nested_acquisition'];need({int(y):{d:F(c) for d,c in r} for y,r in declared['forward_correction_rows'].items()}==forward,'forward metadata derived freshly from source')
 need({int(y):{d:F(c) for d,c in r} for y,r in declared['reverse_correction_rows'].items()}==reverse,'reverse metadata is actual hosted transpose')
 original,original_loc,_=run(s,p);wanted={r:row.copy() for r,row in original.items()}
 for table in [forward,reverse]:
  for r,coeff in table.items():
   for d,c in coeff.items():addto(wanted[raw[r]],q[d],c)
 def check(candidate,gate=True):
  rows,loc,checks=run(s,candidate,gate);need(rows==wanted and loc==original_loc,'complete1880 prefix matrix and locations');return checks
 checks=check(w);need(len(checks)==3,'three actual four-carrier interface gates')
 need(w['program'][w['marks']['common_starts']:]==p['program'][p['marks']['common_starts']:],'unchanged literal common suffix')
 for r in set(forward)|set(reverse)|{hosted[x][1] for x in selected}:
  uses=[o for o in w['program'][w['marks']['common_starts']:] if o[1]==raw[r] or o[0] in ('ADD','COPY') and o[2]==raw[r]];need(uses==[['ADD',raw[r],r,'1',s['final'][r]]],'no continuation feedback beyond recoupling')
 controls=[]
 def reject(name,bad):
  try:check(bad)
  except ValueError as e:controls.append({'mutation':name,'rejection':str(e)})
  else:raise ValueError('accepted mutant '+name)
 first=next(r for r in declared['records'] if 'before_primal' in r)
 bad=copy.deepcopy(w);entry=next(r for r in bad['nested_acquisition']['records'] if 'before_primal' in r);entry['incoming_current_rows'][0]=[[entry['four_current_carriers'][0],'1']];reject('pretend_original_donor_instead_of_current_encoded_row',bad)
 D=hosted[2][1];t=next(i for i,o in enumerate(w['program']) if o[0]=='MOVE' and o[1]==raw[D] and o[2]==3);bad=copy.deepcopy(w);bad['program'][t]=['SCALE',raw[D],'1',3];reject('omit_preterminal_reverse_source_route',bad)
 t=first['dual_encoder']['begin']+2*len(first['dual_encoder']['roles']);bad=copy.deepcopy(w);need(bad['program'][t][0]=='ADD','dual mutation event');bad['program'][t][3]=str(-F(bad['program'][t][3]));reject('wrong_nested_dual_recombination_sign',bad)
 controlsU={d for r in declared['records'] for d in r.get('coupled_controls',[])};t=next(i for i,o in enumerate(w['program']) if declared['begin']<i<declared['restored'] and o[0]=='ADD' and o[2] in {raw[d] for d in controlsU} and o[4]==127);bad=copy.deepcopy(w);bad['program'][t]=['SCALE',bad['program'][t][1],'1',127];reject('omit_coupled_control_restoration',bad)
 owners={c['owner'] for c in declared['cache_declarations'] if c['receiver']==114};t=next(i for i,o in enumerate(w['program']) if o[0]=='ADD' and o[1]==raw[114] and o[2] in owners);bad=copy.deepcopy(w);bad['program'][t]=['SCALE',raw[114],'1',bad['program'][t][4]];reject('omit_new_forward_partial_read',bad)
 bad=copy.deepcopy(w);bad['additional_charts'][0]['frame'].pop();reject('wrong_acquisition_subspace',bad)
 result={'status':'PASS_NESTED_INTERMEDIATE_ROWS_AND_SIX_REJECTING_CONTROLS','word_sha256':hashlib.sha256(wb).hexdigest(),'word_payload_sha256':hashlib.sha256(gzip.decompress(wb)).hexdigest(),'source_sha256':SOURCE,'parent_sha256':PARENT,'gate_receipts':checks,'all1880_prefix_rows_checked':True,'new_forward_rows_from_source':{str(y):len(r) for y,r in forward.items()},'new_reverse_coefficients':sum(map(len,reverse.values())),'negative_controls':controls,'independence':'Supplementary second implementation by the construction author; no generator imports. Separate independent-agent reviews must be recorded separately.','scope':'Exact finite normalized prefix and suffix-composition validation; no complete global target map, physical supplier or new kappa.'}
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'gates':checks,'controls':len(controls)},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['source','parent','word','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
