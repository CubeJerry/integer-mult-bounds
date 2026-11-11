#!/usr/bin/env python3
"""Exact selective paused-common helper loan, with all1880 independent physical inputs."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
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
 M=sorted(set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));need(w['public']==1480 and len(M)==400,'native dimensions');qm={i:1480+j for j,i in enumerate(M)};old=lambda r:r if r<1480 else r+400;K=1880+w['owned_fields'];P=w['program'];start=30773;stop=43452;hoisted={30832,30848,42670,43452};H=151;Qd=qm[101];Yr=qm[213];B=541;top=127
 base=[['ADD',qm[i],i,'-1',w['initial'][i]] for i in M];ops=[e.copy() for e in base];marks=[];check=None;borrowed=[];retimed=[]
 def app(e,label):marks.append({'physical_event':len(ops),'label':label});ops.append(e)
 for k,e in enumerate(P):
  if k==start:
   need(e==['MOVE',H,327,B,False],'pinned helper bridge')
   for x in (['ADD',H,Qd,'1',327],['ADD',Qd,H,'-1',327],['ADD',H,Qd,'1',327]):app(x,'opening_swap')
  x=e.copy();x[1]=old(e[1])
  if e[0] in ('ADD','COPY'):x[2]=old(e[2])
  base.append(x);ops.append(x)
  if e[0]=='MOVE' and e[1] in qm:
   qmove=['MOVE',qm[e[1]],e[2],e[3],False];base.append(qmove)
   if k not in hoisted:ops.append(qmove)
  if k==start:
   baseline_cut=len(base)-1;app(['INIT',K,B],'early_carrier_init');app(['ADD',K,H,'1',B],'early_carrier_load')
   for j in range(start+1,stop+1):
    z=P[j]
    if j in hoisted:
     need(z[0]=='MOVE' and z[1] in (101,213),'only donor and receiver routes hoisted')
     retimed.append({'source_event':j,'physical_event':len(ops),'logical_main':z[1]});ops.append(['MOVE',qm[z[1]],z[2],z[3],False])
    if j in (30824,30826,30830):
     need(z[0]=='MOVE' and z[1]==1481 and z[4] is True,'reserved second-owned1481 slot');borrowed.append({'source_event':j,'source':z[2],'target':z[3],'rank':abs(len(w['frames'][z[2]])-len(w['frames'][z[3]]))});app(['MOVE',K,z[2],z[3],True],'funded_second_owned_1481')
    if j==30832:
     need(z==['MOVE',213,3,594,False],'receiver594 arrival');app(['ADD',Yr,K,'1',594],'desired_q101_to_q213');app(['CLEAR',K,594],'early_carrier_clear')
   need(P[stop]==['MOVE',101,233,top,False],'donor top arrival');app(['INIT',K,top],'repair_init');app(['ADD',K,Qd,'1',top],'repair_copy_minus_h');app(['MOVE',K,top,B,True],'paid_descent_rank2')
   for z in (['ADD',H,K,'-1',B],['ADD',K,H,'1',B],['ADD',H,K,'-1',B],['ADD',K,H,'1',B]):app(z,'restore_helper_and_encode_return')
   app(['MOVE',K,B,top,True],'paid_ascent_rank2');app(['ADD',Qd,K,'1',top],'restore_raw_donor_q101');app(['CLEAR',K,top],'repair_clear');check={'baseline_physical_event':baseline_cut,'loan_physical_event':len(ops)-1,'source_common_cut_after':start,'donor_calendar_advanced_through':stop,'hoisted_main_source_events':sorted(hoisted)}
 for i in M:
  z=['ADD',qm[i],i,'1',w['final'][i]];base.append(z);ops.append(z)
 meta={'public':1880,'owned_fields':w['owned_fields']+1,'frames':w['frames'],'initial':w['initial']+[w['initial'][i] for i in M],'final':w['final']+[w['final'][i] for i in M],'program':ops,'difference_role_map':{str(i):j for i,j in qm.items()},'loan_marks':marks,'restoration_checkpoint':check,'funded_second_owned_slots':borrowed,'retimed_main_MOVEs':retimed,'source_sha256':PIN,'status':'EXACT_SELECTED_ENDPOINT_WITH_ONLY_FOUR_RAW_ROUTES_HOISTED'}
 return meta,base,qm

def run(source,packet,write=False,controls=True):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));meta,base,qm=build(w);payload=(json.dumps(meta,separators=(',',':'),sort_keys=True)+'\n').encode();path=packet/'selective-paused-word.json.gz'
 if write:path.write_bytes(gzip.compress(payload,mtime=0))
 else:need(gzip.decompress(path.read_bytes())==payload,'entire literal word matches source lowering')
 cp=meta['restoration_checkpoint'];baseline,bb,bc=replay(meta,base,[cp['baseline_physical_event']]);out,bill,oc=replay(meta,meta['program'],[cp['loan_physical_event']]);expected={i:r.copy() for i,r in baseline.items()};expected[qm[213]]=add(expected[qm[213]],{qm[101]:Q(1),101:Q(-1)},Q(1));need(out==expected,'all1880 physical output rows')
 need(out[213]=={213:Q(1),101:Q(1)} and out[qm[213]]=={qm[213]:Q(1),qm[101]:Q(1)},'both copies of selected Y213 endpoint exactly correct')
 br,bf=bc[cp['baseline_physical_event']];rr,rf=oc[cp['loan_physical_event']];common=[i for i in br if i<1480 or i>=1880];need(all(rr[i]==br[i] and rf[i]==bf[i] for i in common),'every live common row restored before suffix resumes');need(rr[qm[101]]=={qm[101]:Q(1),101:Q(-1)},'raw q101 donor restored at127')
 need([x['source_event'] for x in meta['retimed_main_MOVEs']]==[30832,30848,42670,43452],'exact four hoisted source occurrences')
 for i,r in qm.items():
  row={r:Q(1),i:Q(-1)}
  if i==213:row=add(row,{qm[101]:Q(1),101:Q(-1)},Q(1))
  need(rr[r]==row,'all400 difference fields at resume cut')
  f=127 if i==101 else 594 if i==213 else bf[r]
  need(rf[r]==f,'all400 difference charts at selective resume cut')
 delta=collections.Counter(bill['counts']);delta.subtract(bb['counts']);need({k:v for k,v in delta.items() if v}=={'ADD':11,'MOVE':5,'INIT':2,'CLEAR':2},'exact ordinary and owned operation delta');hd=collections.Counter({int(k):v for k,v in bill['move_histogram'].items()});hd.subtract({int(k):v for k,v in bb['move_histogram'].items()});need({k:v for k,v in hd.items() if v}=={1:2,2:2,4:1},'funded1,1,4 and paid2,2 rank histograms')
 need(len([x for x in meta['loan_marks'] if x['label']=='funded_second_owned_1481'])==3,'three reserved slots');need(meta['funded_second_owned_slots']==[{'source_event':30824,'source':541,'target':534,'rank':1},{'source_event':30826,'source':534,'target':117,'rank':1},{'source_event':30830,'source':117,'target':594,'rank':4}],'exact source-funded route pins')
 negatives=[]
 if controls:
  for name,label,change in [('omit_donor_restoration','restore_raw_donor_q101','omit'),('omit_common_repair_step','restore_helper_and_encode_return','omit'),('false_public_descent','paid_descent_rank2','public'),('omit_middle_funded_leg','funded_second_owned_1481','middle'),('wrong_endpoint_shear','desired_q101_to_q213','coefficient')]:
   ats=[x['physical_event'] for x in meta['loan_marks'] if x['label']==label];at=ats[1] if change=='middle' else ats[0];bad=[x.copy() for x in meta['program']]
   if change in ('omit','middle'):bad.pop(at)
   elif change=='public':bad[at][4]=False
   else:bad[at][3]='-1'
   try:
    got,_,_=replay(meta,bad);need(got==expected,'mutant violates full1880-column endpoint map')
   except ValueError as exc:negatives.append({'mutation':name,'rejection':str(exc)})
   else:raise ValueError('accepted mutant '+name)
 return {'status':'PASS_EXACT_SELECTIVE_PAUSED_COMMON_ENDPOINT_LOAN','source_sha256':PIN,'word_payload_sha256':hashlib.sha256(payload).hexdigest(),'word_gzip_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'independent_physical_inputs':1880,'common_input_directions':1480,'second_main_input_directions':400,'boundary_ADDs_included':800,'source_instructions':len(w['program']),'baseline_instructions':len(base),'loan_instructions':len(meta['program']),'baseline_bill':bb,'loan_bill':bill,'operation_delta':{k:v for k,v in delta.items() if v},'funded_second_owned_slots':meta['funded_second_owned_slots'],'new_paid_MOVE_ranks':[2,2],'exact_new_weighted_Gaussian_cost_at_kappa_1_over_200':'2 * 2^(199/200)','common_state_at_cut30773_restored':{'public_rows':1480,'live_owned_rows':len(common)-1480},'retimed_main_MOVE_count':len(meta['retimed_main_MOVEs']),'retimed_main_source_events':[x['source_event'] for x in meta['retimed_main_MOVEs']],'all400_difference_states_and_charts_at_resume_checked':True,'completed_selected_second_endpoint':{'logical_output':213,'physical_output':qm[213],'exact_physical_input_rows':{str(qm[213]):'1',str(qm[101]):'1'}},'negative_controls':negatives,'scope':'One exact missing q101→q213 endpoint shear with dirty common native preserved; only raw101 three routes and raw213 one arrival are hoisted, all other raw routes retain source-clock interleaving. Three second-owned1481 routes carry this chosen q101 instead of their generally required delta1481; all other difference-native duties remain open. The two new rank2 complete-field routes and all ordinary/owned/boundary operations are charged. No complete supplier, target admission, or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path);p.add_argument('--write-word',action='store_true');p.add_argument('--skip-negative-controls',action='store_true');a=p.parse_args();r=run(a.source,a.packet,a.write_word,not a.skip_negative_controls);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
