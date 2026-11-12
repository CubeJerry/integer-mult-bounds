#!/usr/bin/env python3
"""S008 fresh reconstruction, exact prefix proof, physical word and invoice.

No S007 missing-helper hash is bypassed. The original generators are lost;
this generator and its outputs carry new provenance. @CubeJerry, OpenAI aid.
"""
from common import *
import argparse
import eight, small

def interpret_prefix(s,w):
 frames=s['frames']+[d['frame'] for d in w.get('additional_charts',[])];spaces=list(map(space,frames));rows={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(w['initial']))
 for t,e in enumerate(w['program'][:w['marks']['common_starts']]):
  op,r=e[:2]
  if op=='INIT':need(r>=1880 and r not in rows,'fresh prefix lifetime');rows[r]={};loc[r]=e[2]
  elif op=='CLEAR':need(r>=1880 and loc.get(r)==e[2],'prefix retirement');del rows[r];del loc[r]
  elif op=='MOVE':
   a,b,owned=e[2:];need(loc.get(r)==a and owned==(r>=1880),'prefix route source/ownership');need(spaces[a]<spaces[b] or owned and spaces[b]<spaces[a],'prefix nested route');loc[r]=b
  elif op=='SCALE':need(loc.get(r)==e[3] and F(e[2]),'prefix scale');rows[r]={j:F(e[2])*c for j,c in rows[r].items()}
  elif op in ('ADD','COPY'):
   j,c,at=e[2:];need(r!=j and loc.get(r)==loc.get(j)==at,'prefix cochart '+str(t));need(op!='COPY' or not rows[r],'prefix copy guard');rows[r]=add(rows[r],rows[j],F(c))
  else:raise ValueError(op)
  if t+1==w['marks'].get('all_active_donors_restored'):
   raw={int(x):r for x,r in w['private_role_map'].items()};need(all(rows[raw[x]]=={raw[x]:F(1),x:F(-1)} and loc[raw[x]]==127 for x in s['live']),'all104 original donors restored')
 return rows,loc

def typed(s,w):
 frames=s['frames']+[d['frame'] for d in w.get('additional_charts',[])];spaces=list(map(space,frames));loc=dict(enumerate(w['initial']));counts=Counter();ranks=Counter();rawranks=Counter();raw=set(w['private_role_map'].values());life=peak=0
 for t,e in enumerate(w['program']):
  op,r=e[:2];counts[op]+=1;need(0<=r<1880+w['owned_fields'],'declared physical role')
  if op=='INIT':need(r>=1880 and r not in loc,'fresh lifetime');loc[r]=e[2];life+=1
  elif op=='CLEAR':need(r>=1880 and loc.get(r)==e[2],'retirement');del loc[r]
  elif op=='MOVE':
   a,b,owned=e[2:];need(loc.get(r)==a and type(owned)is bool and owned==(r>=1880),'actual MOVE source/ownership');need(spaces[a]<spaces[b] or owned and spaces[b]<spaces[a],'nested actual MOVE');k=abs(len(frames[a])-len(frames[b]));ranks[k]+=1;rawranks[k]+=int(r in raw);loc[r]=b
  elif op=='SCALE':need(loc.get(r)==e[3] and F(e[2]),'actual nonzero scale')
  elif op in ('ADD','COPY'):j,c,at=e[2:];need(r!=j and loc.get(r)==loc.get(j)==at,'actual cochart '+str(t))
  else:raise ValueError(op)
  peak=max(peak,len(loc)-1880)
 need(set(loc)==set(range(1880)),'all owned retired')
 return {'instructions':len(w['program']),'opcode_counts':dict(sorted(counts.items())),'move_rank_histogram':dict(sorted(ranks.items())),'raw_histogram':dict(sorted((r,n) for r,n in rawranks.items() if n)),'owned_lifetimes':life,'peak_owned':peak,'final_owned':0,'final_locations':loc}

def pow_bounds(r,den=10**30):
 if not r:return F(0),F(0)
 target=r**199*den**200;lo,hi=0,r*den+1
 while hi-lo>1:
  mid=(hi+lo)//2
  if mid**200<=target:lo=mid
  else:hi=mid
 need(lo**200<=target<(lo+1)**200,'directed root bracket');return F(lo,den),F(lo if lo**200==target else lo+1,den)
def interval(cs):
 lo=hi=F(0)
 for r,c in cs.items():a,b=pow_bounds(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi

def verify(s,p,w,invoice):
 old,oldloc=interpret_prefix(s,p);new,newloc=interpret_prefix(s,w);raw={int(x):r for x,r in w['private_role_map'].items()};ys=w['newly_completed_firstY_receivers'];q={x:{r:F(1),x:F(-1)} for x,r in raw.items()};need(set(old)==set(new) and oldloc==newloc,'same prefix live fields/charts')
 for r,row in old.items():
  want=row
  for y in ys:
   if r==raw[y]:
    for d,c in w['corrections'][str(y)]:want=add(want,q[d],F(c))
  need(new[r]==want,'1880-coordinate prefix delta only selected receivers')
 oldtail=p['program'][p['marks']['common_starts']:];tail=w['program'][w['marks']['common_starts']:];need(tail==oldtail,'literal identical common suffix')
 for y in ys:
  need(new[raw[y]]==add(q[y],q[y-112]),'completed ordinary receiver');uses=[e for e in tail if e[1]==raw[y] or e[0] in ('ADD','COPY') and e[2]==raw[y]];need(uses==[['ADD',raw[y],y,'1',s['final'][y]]],'no later receiver feedback except recoupling')
 bill=typed(s,w);pbill=typed(s,p);need(bill.pop('final_locations')==pbill.pop('final_locations'),'final charts unchanged');profile=Counter(bill['raw_histogram']);oldraw=Counter(abs(len(s['frames'][o[3]])-len(s['frames'][o[2]])) for o in s['program'] if o[0]=='MOVE' and o[1] in raw);target=Counter({int(k):v for k,v in invoice['T4'].items()});paid=Counter({int(k):v for k,v in invoice['P4'].items()})
 for r in profile.keys()|oldraw.keys():paid[r]+=18*(profile[r]-oldraw[r])
 paid[9]+=18*8;need(all(n>=0 for n in paid.values()),'nonnegative paid profile');lo,hi=interval({r:target[r]-paid[r] for r in target.keys()|paid.keys()});delta={k:bill['opcode_counts'].get(k,0)-pbill['opcode_counts'].get(k,0) for k in bill['opcode_counts'].keys()|pbill['opcode_counts'].keys()}
 return {'status':'PASS_FRESH_SOURCE_WORD_PREFIX_COMPOSITION_AND_TYPES','source_sha256':SPIN,'parent_sha256':PPIN,'parent_payload_sha256':PPAY,'bill':bill,'increment_over_fused_parent':delta,'newly_completed_firstY_receivers':ys,'remaining_residual_terms':4985-48*len(ys),'exact_input_coordinates':1880,'all_original_donors_restored_before_E8':True,'same_literal_common_suffix':True,'common_restoration_scope':'Inherited from independently reviewed parent via exact1880-coordinate prefix comparison and identical noninterfering suffix.','additional_charts':w['additional_charts'],'conditional_caller':{'T4':dict(sorted(target.items())),'P_partial':dict(sorted(paid.items())),'target_positions':sum(target.values()),'paid_positions':sum(paid.values()),'rank_surplus':sum(r*(target[r]-paid[r]) for r in target.keys()|paid.keys()),'remaining_moment_per_native_lower':str(lo/18),'remaining_moment_per_native_upper':str(hi/18),'remaining_moment_per_native_decimal':float(lo/18),'added_paid_per_native':{9:8}},'scope':'Finite exact source construction. All residuals, reverse duties, suppliers and foundations remain. No new complete kappa.'}

def main(args):
 s,p,invoice=load_inputs(args.repo)
 for name in list(SELECT) if args.variant=='all' else [args.variant]:
  w=eight.build(s,p) if name=='eight' else small.build(s,p,name);r=verify(s,p,w,invoice);out=args.output/name;out.mkdir(parents=True,exist_ok=True);payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();blob=gzip.compress(payload,mtime=0,compresslevel=9);(out/'WORD.json.gz').write_bytes(blob);r['word_sha256']=sha(blob);r['word_payload_sha256']=sha(payload);r['generator_sha256']={x.name:sha(x.read_bytes()) for x in Path(__file__).parent.glob('*.py')};(out/'RESULT.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({'variant':name,'operations':len(w['program']),'raw_calls':sum(r['bill']['raw_histogram'].values()),'remaining':r['remaining_residual_terms'],'moment':r['conditional_caller']['remaining_moment_per_native_decimal'],'payload':r['word_payload_sha256']},sort_keys=True),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--variant',choices=['all']+list(SELECT),default='all');main(ap.parse_args())
