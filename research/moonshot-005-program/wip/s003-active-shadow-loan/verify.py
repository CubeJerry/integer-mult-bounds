#!/usr/bin/env python3
"""Exact active-shadow-loan source instance, with all 1880 independent inputs."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
CASES=(dict(name='read_write',start=29097,close=33597,helper=3,donor=178,receiver=67,deliver=32151,target=424,pending={67:Q(1)},helper_alpha=Q(1,2)),dict(name='read_before_receiver_departure',start=36070,close=37333,helper=1340,donor=122,receiver=883,deliver=36071,target=597,pending={1512:Q(-1)},helper_alpha=Q(1)))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def add(a,b,c):
 z=a.copy()
 for i,v in b.items():
  x=z.get(i,Q(0))+c*v
  if x:z[i]=x
  else:z.pop(i,None)
 return z
def space(a):
 S={0}
 for x in a:S.update(y^x for y in tuple(S))
 return frozenset(S)
def replay(w,ops,checkpoints=()):
 pub=w['public'];owners=w['owned_fields'];S=list(map(space,w['frames']));rows={i:{i:Q(1)} for i in range(pub)};chart=dict(enumerate(w['initial']));bill=collections.Counter();hist=collections.Counter();life=peak=0;captures={};labels=set();checks=set(checkpoints)
 for k,e in enumerate(ops):
  tag,r=e[:2];need(0<=r<pub+owners,'role range');bill[tag]+=1
  if tag=='INIT':
   need(r>=pub and r not in chart,'INIT requires dead owned role');chart[r]=e[2];rows[r]={};life+=1;labels.add(r)
  elif tag=='CLEAR':
   need(r>=pub and chart.get(r)==e[2],'CLEAR requires live owned role');chart.pop(r);rows.pop(r)
  elif tag=='MOVE':
   a,b,owned=e[2:];need(chart.get(r)==a and type(owned) is bool and owned==(r>=pub),'typed MOVE source and owner flag');need(S[a]<S[b] or owned and S[b]<S[a],'proper nested MOVE');hist[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1;chart[r]=b
  elif tag in ('ADD','COPY'):
   s,c,f=e[2:];need(r!=s and chart.get(r)==chart.get(s)==f and r in chart and s in chart,'live cochart scalar');c=Q(c);need(c!=0,'nonzero ADD coefficient')
   if tag=='COPY':need(not rows[r],'COPY destination exactly zero on all inputs')
   rows[r]=add(rows[r],rows[s],c)
  elif tag=='SCALE':
   c,f=Q(e[2]),e[3];need(c!=0 and chart.get(r)==f,'nonzero live cochart SCALE');rows[r]={i:c*v for i,v in rows[r].items()}
  else:raise ValueError('unknown opcode')
  peak=max(peak,len(chart)-pub)
  if k in checks:captures[k]=({i:r.copy() for i,r in rows.items()},chart.copy())
 need(all(chart.get(i)==f for i,f in enumerate(w['final'])),'all public final charts');need(len(chart)==pub,'all owned roles cleared')
 return rows,{'counts':dict(bill),'move_histogram':{str(k):v for k,v in sorted(hist.items())},'owned_lifetimes':life,'peak_owned':peak,'owned_labels_used':len(labels),'final_owned':len(chart)-pub},captures

def build(w):
 M=sorted(set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));need(w['public']==1480 and len(M)==400,'pinned native dimensions');qm={r:1480+j for j,r in enumerate(M)};old=lambda r:r if r<1480 else r+400;shadow=1880+w['owned_fields'];base=[['ADD',qm[i],i,'-1',w['initial'][i]] for i in M];ops=[e.copy() for e in base];mark=[];active=None;alpha={};before={c['start']:c for c in CASES};after={c['close']:c for c in CASES};delivery={c['deliver']:c for c in CASES};closures=[]
 def app(e,label):mark.append({'physical_event':len(ops),'label':label});ops.append(e)
 for k,e in enumerate(w['program']):
  if k in before:
   c=before[k];need(active is None,'disjoint loans');active=c;h=c['helper'];q=qm[c['donor']];a=e[2];need(e==['MOVE',h,a,c['target'],False],'helper public start MOVE');alpha={h:Q(1)}
   for op in (['ADD',h,q,'1',a],['ADD',q,h,'-1',a],['ADD',h,q,'1',a]):app(op,c['name']+':opening_swap')
  b=e.copy();b[1]=old(e[1]);
  if e[0] in ('ADD','COPY'):b[2]=old(e[2])
  base.append(b)
  x=b.copy()
  if active and k>active['start'] and k<=active['close']:
   h=active['helper'];tag,r=e[:2];need(not(r==h and tag in ('MOVE','INIT','CLEAR')),'borrowed helper has no later route/lifecycle')
   if tag in ('INIT','CLEAR'):alpha.pop(r,None)
   elif tag=='SCALE':
    if r in alpha:alpha[r]*=Q(e[2])
   elif tag in ('ADD','COPY'):
    if tag=='COPY':need(not alpha.get(r),'no COPY with outstanding destination debt')
    z=alpha.get(r,Q(0))+Q(e[3])*alpha.get(e[2],Q(0))
    if z:alpha[r]=z
    else:alpha.pop(r,None)
   if x[1]==h:x[1]=shadow
   if tag in ('ADD','COPY') and x[2]==h:x[2]=shadow
  ops.append(x)
  if e[0]=='MOVE' and e[1] in qm:
   qmove=['MOVE',qm[e[1]],e[2],e[3],False];base.append(qmove);ops.append(qmove)
  if k in before:app(['INIT',shadow,before[k]['target']],before[k]['name']+':shadow_init')
  if k in delivery:
   c=delivery[k];app(['ADD',qm[c['receiver']],c['helper'],'1',c['target']],c['name']+':early_q_delivery')
  if k in after:
   c=after[k];h=c['helper'];q=qm[c['donor']];f=c['target'];expect={h:c['helper_alpha'],**c['pending']};need(alpha==expect,'exact full-common debt coefficients')
   for op in (['ADD',h,q,'-1',f],['ADD',q,h,'1',f],['ADD',h,q,'-1',f]):app(op,c['name']+':closing_swap')
   for r,a in sorted(c['pending'].items()):app(['ADD',old(r),h,str(a),f],c['name']+':common_debt_correction')
   if c['helper_alpha']!=1:app(['SCALE',h,str(c['helper_alpha']),f],c['name']+':helper_debt_scale')
   app(['ADD',h,shadow,'1',f],c['name']+':helper_shadow_assembly');app(['CLEAR',shadow,f],c['name']+':shadow_clear');closures.append({'name':c['name'],'source_event':k,'baseline_physical_event':len(base)-1,'loan_physical_event':len(ops)-1});active=None;alpha={}
 for i in M:
  b=['ADD',qm[i],i,'1',w['final'][i]];base.append(b);ops.append(b)
 meta={'public':1880,'owned_fields':w['owned_fields']+1,'frames':w['frames'],'initial':w['initial']+[w['initial'][i] for i in M],'final':w['final']+[w['final'][i] for i in M],'program':ops,'difference_role_map':{str(i):j for i,j in qm.items()},'loan_marks':mark,'restoration_checkpoints':closures,'source_sha256':PIN,'status':'EXACT_1880_INPUT_COMMON_REFERENCE_PLUS_TWO_DIFFERENCE_SHEARS'}
 return meta,base,qm,old

def run(source,packet,write=False,controls=True):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));meta,base,qm,old=build(w);payload=(json.dumps(meta,separators=(',',':'),sort_keys=True)+'\n').encode();path=packet/'active-shadow-word.json.gz'
 if write:path.write_bytes(gzip.compress(payload,mtime=0))
 else:need(gzip.decompress(path.read_bytes())==payload,'complete reconstructed literal word')
 cps=meta['restoration_checkpoints'];baseline,bb,bc=replay(meta,base,[x['baseline_physical_event'] for x in cps]);out,bill,oc=replay(meta,meta['program'],[x['loan_physical_event'] for x in cps]);expected={i:r.copy() for i,r in baseline.items()}
 for c in CASES:expected[qm[c['receiver']]]=add(expected[qm[c['receiver']]],{qm[c['donor']]:Q(1),c['donor']:Q(-1)},Q(1))
 need(out==expected,'all1880 output rows match reference common map and declared q shears')
 restore=[]
 for c in cps:
  br,bf=bc[c['baseline_physical_event']];rr,rf=oc[c['loan_physical_event']];common=[r for r in br if r<1480 or r>=1880];need(all(rr[r]==br[r] and rf[r]==bf[r] for r in common),'entire current common state restored');restore.append({'name':c['name'],'source_event':c['source_event'],'common_public_rows':1480,'live_common_owned_rows':len(common)-1480,'all_common_rows_restored':True})
 delta=collections.Counter(bill['counts']);delta.subtract(bb['counts']);need({k:v for k,v in delta.items() if v}=={'ADD':18,'SCALE':1,'INIT':2,'CLEAR':2},'literal operation delta');need(bill['move_histogram']==bb['move_histogram'],'no Gaussian MOVE added, removed, or reranked')
 negatives=[]
 if controls:
  for name,label,mut in [('omit_common_debt','read_write:common_debt_correction','omit'),('omit_helper_shadow','read_write:helper_shadow_assembly','omit'),('wrong_helper_half','read_write:helper_debt_scale','scale'),('restore_before_donor_arrival','read_write:closing_swap','wrong_chart'),('wrong_q_delivery','read_before_receiver_departure:early_q_delivery','coefficient')]:
   at=next(t['physical_event'] for t in meta['loan_marks'] if t['label']==label);bad=[e[:] for e in meta['program']]
   if mut=='omit':bad.pop(at)
   elif mut=='scale':bad[at][2]='1'
   elif mut=='wrong_chart':bad[at][-1]=3
   else:bad[at][3]='-1'
   try:
    got,_,_=replay(meta,bad);need(got==expected,'mutant violates full1880-column output map')
   except ValueError as exc:negatives.append({'mutation':name,'rejected':str(exc)})
   else:raise ValueError('accepted negative control '+name)
 result={'status':'PASS_EXACT_ACTIVE_SHADOW_LOANS','source_sha256':PIN,'word_payload_sha256':hashlib.sha256(payload).hexdigest(),'word_gzip_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'independent_input_directions':1880,'common_input_directions':1480,'difference_input_directions':400,'boundary_ADDs_included':800,'physical_public_outputs':1880,'source_instructions':len(w['program']),'baseline_instructions':len(base),'loan_instructions':len(meta['program']),'baseline_bill':bb,'loan_bill':bill,'operation_delta':{k:v for k,v in delta.items() if v},'additional_Gaussian_MOVEs':0,'restorations':restore,'difference_shears':[{'source_logical':c['donor'],'target_logical':c['receiver'],'coefficient':'1','delivery_after_source_event':c['deliver'],'closure_after_source_event':c['close']} for c in CASES],'negative_controls':negatives,'scope':'Two exact scalar-word primitives with400 input differences and400 output recombinations, one full common native, and a raw400-main difference transport bank. This is not the complete difference native, supplier, price admission, or a new kappa. The34 immediate-closure candidates add no currently missing endpoint reach even under simultaneous granting.'}
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path);p.add_argument('--write-word',action='store_true');p.add_argument('--skip-negative-controls',action='store_true');a=p.parse_args();r=run(a.source,a.packet,a.write_word,not a.skip_negative_controls);s=json.dumps(r,indent=2,sort_keys=True)+'\n';
 if a.output:a.output.write_text(s)
 print(s,end='')
