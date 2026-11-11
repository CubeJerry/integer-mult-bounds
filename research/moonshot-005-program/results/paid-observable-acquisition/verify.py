#!/usr/bin/env python3
"""Actual1880-input two-observable acquisition; no oracle and no common read."""
import argparse,collections,gzip,hashlib,json
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(x,m):
 if not x:raise ValueError(m)
def add(a,b,c):
 z=a.copy()
 for i,v in b.items():
  t=z.get(i,F(0))+c*v
  if t:z[i]=t
  else:z.pop(i,None)
 return z
def span(a):
 S={0}
 for x in a:S.update(z^x for z in tuple(S))
 return frozenset(S)
def targets(w,M):
 rows=[{i:F(1)} if i in M else {} for i in range(w['public']+w['owned_fields'])];chart=dict(enumerate(w['initial']))
 for e in w['program'][:30824]:
  tag,r=e[:2]
  if tag=='INIT':rows[r]={};chart[r]=e[2]
  elif tag=='CLEAR':rows[r]={};chart.pop(r,None)
  elif tag=='MOVE':chart[r]=e[3]
  elif tag=='SCALE':rows[r]={i:F(e[2])*v for i,v in rows[r].items()}
  elif tag in ('ADD','COPY'):rows[r]=add(rows[r],rows[e[2]],F(e[3]))
 need(chart[1481]==chart[130]==541,'actual target frame at cut30824');T=[rows[1481],rows[130]];need(list(map(len,T))==[59,26],'actual source row supports');return T

def build(w):
 M=sorted(set(w['live'])|{i+112 for i in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']));need(len(M)==400 and w['public']==1480,'native dimensions');qm={i:1480+j for j,i in enumerate(M)};T=targets(w,set(M));C=list(map(span,w['frames']));empty=C[3];top=C[127];need(len(top)==512 and len(C[541])==128,'target lattice ranks');N=[i for i in M if C[w['initial'][i]]!=empty];need(len(N)==200 and all(w['final'][i]==127 for i in N),'all200 nonentry endpoints127');D=sorted({i for row in T for i in row if C[w['initial'][i]]!=empty});need(len(D)==52 and all(i in N for i in D),'52 required nonentry carriers');first=1880+w['owned_fields'];outs=[first,first+1];tmp=first+2;ops=[];marks=[];reservations=[]
 def app(e,label):marks.append({'physical_event':len(ops),'label':label});ops.append(e)
 for i in M:app(['ADD',qm[i],i,'-1',w['initial'][i]],'actual_input_difference')
 for out,row in zip(outs,T):
  app(['INIT',out,3],'entry_accumulator_init')
  for i,c in sorted(row.items()):
   if C[w['initial'][i]]==empty:need(w['initial'][i]==3,'literal entry chart');app(['ADD',out,qm[i],str(c),3],'entry_row_term')
  app(['MOVE',out,3,541,True],'paid_rank7_entry_arrival')
 for k,e in enumerate(w['program']):
  if e[0]=='MOVE' and e[1] in D:
   need(e[4] is False,'reserved public main route');reservations.append({'source_event':k,'physical_event':len(ops),'logical_main':e[1],'physical_main':qm[e[1]],'source_chart':e[2],'target_chart':e[3],'rank':len(w['frames'][e[3]])-len(w['frames'][e[2]])});app(['MOVE',qm[e[1]],e[2],e[3],False],'reserved_raw_main_MOVE')
 for out,row in zip(outs,T):
  app(['INIT',tmp,127],'nonentry_accumulator_init')
  for i,c in sorted(row.items()):
   if C[w['initial'][i]]!=empty:app(['ADD',tmp,qm[i],str(c),127],'nonentry_row_term')
  app(['MOVE',tmp,127,541,True],'paid_rank2_nonentry_arrival');app(['ADD',out,tmp,'1',541],'combine_entry_and_nonentry');app(['CLEAR',tmp,541],'retire_duplicate_nonentry_sum')
 meta={'status':'ACTUAL_TWO_OBSERVABLE_ACQUISITION_PREFIX','source_sha256':PIN,'public':1880,'owned_labels_declared':w['owned_fields']+3,'common_owned_labels_reserved':w['owned_fields'],'initial':w['initial']+[w['initial'][i] for i in M],'program':ops,'marks':marks,'difference_role_map':{str(i):r for i,r in qm.items()},'output_roles':{'r_delta1481':outs[0],'Mnew_delta130':outs[1]},'output_chart':541,'output_rows':[{str(i):str(c) for i,c in sorted(row.items())} for row in T],'nonentry_donors':D,'reserved_raw_main_routes':reservations,'unexecuted_reserved_main_MOVEs':sum(e[0]=='MOVE' and e[1] in qm for e in w['program'])-len(reservations),'remaining_obligations':['Retimed raw carriers are at127; original intermediate q duties need a new proof.','Consume/replace both outputs and all affected receiver obligations.','Retire both live owned outputs with charged operations.','Complete remaining routes without reusing consumed reservation credit.','Complete supplier, precision, recursive accounting and foundations remain open.']}
 return meta,T,qm

def replay(w,meta,ops):
 pub=1880;C=list(map(span,w['frames']));rows={i:{i:F(1)} for i in range(pub)};chart=dict(enumerate(meta['initial']));bill=collections.Counter();hist=collections.Counter();peak=life=0;used=set()
 for e in ops:
  tag,r=e[:2];need(0<=r<pub+meta['owned_labels_declared'],'role range');bill[tag]+=1
  if tag=='INIT':need(r>=pub and r not in chart,'fresh owned INIT');chart[r]=e[2];rows[r]={};life+=1;used.add(r)
  elif tag=='CLEAR':need(r>=pub and chart.get(r)==e[2],'owned CLEAR');chart.pop(r);rows.pop(r)
  elif tag=='MOVE':
   a,b,own=e[2:];need(chart.get(r)==a and type(own) is bool and own==(r>=pub),'typed MOVE');need(C[a]<C[b] or own and C[b]<C[a],'proper nested MOVE');chart[r]=b;hist[abs(len(w['frames'][a])-len(w['frames'][b]))]+=1
  elif tag=='ADD':need(r!=e[2] and chart.get(r)==chart.get(e[2])==e[4],'actual cochart ADD');need(F(e[3])!=0,'nonzero coefficient');rows[r]=add(rows[r],rows[e[2]],F(e[3]))
  else:raise ValueError('unimplemented operation')
  peak=max(peak,len(chart)-pub)
 return rows,chart,{'counts':dict(bill),'MOVE_histogram':{str(k):v for k,v in sorted(hist.items())},'owned_lifetimes':life,'owned_labels_used':len(used),'peak_owned':peak,'live_owned_outputs':len(chart)-pub}

def run(source,packet,write=False):
 raw=source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));meta,T,qm=build(w);text=json.dumps(meta,indent=2,sort_keys=True)+'\n';path=packet/'ACQUISITION-PREFIX.json'
 if write:path.write_text(text)
 else:need(path.read_text()==text,'entire typed prefix reconstructed')
 out,chart,bill=replay(w,meta,meta['program']);need(all(out[i]=={i:F(1)} and chart[i]==w['initial'][i] for i in range(1480)),'all1480 arbitrary common values/charts unchanged');need(all(out[qm[i]]=={qm[i]:F(1),i:F(-1)} for i in qm),'all400 actual differences preserved');outputs=list(meta['output_roles'].values());expected={}
 for field,row in zip(outputs,T):
  ex={}
  for i,c in row.items():ex=add(ex,{qm[i]:F(1),i:F(-1)},c)
  need(out[field]==ex and chart[field]==541,'full1880-column target observable');expected[field]=ex
 need(set(chart)-set(range(1880))==set(outputs),'exact two owned outputs');need(all(chart[qm[i]]==127 for i in meta['nonentry_donors']),'used raw-main itineraries completed');need(bill['counts']['ADD']==487 and bill['owned_lifetimes']==4 and bill['owned_labels_used']==3 and bill['peak_owned']==3,'exact scalar/storage costs');need(bill['counts']['INIT']==4 and bill['counts']['CLEAR']==2,'charged lifecycle');res=meta['reserved_raw_main_routes'];need(len(res)==len({r['source_event'] for r in res}),'no duplicate reservation');need(bill['counts']['MOVE']==len(res)+4,'exact funded/new split');paid=[e for m,e in zip(meta['marks'],meta['program']) if m['label'].startswith('paid_')];need(collections.Counter(abs(len(w['frames'][e[2]])-len(w['frames'][e[3]])) for e in paid)=={7:2,2:2},'paid profile two7/two2')
 r,s=T;de=r.get(129,F(0))*s.get(130,F(0))-r.get(130,F(0))*s.get(129,F(0));dn=r.get(2,F(0))*s.get(4,F(0))-r.get(4,F(0))*s.get(2,F(0));need(de==F(1,8) and dn==F(-1,8),'two independent hub contribution minors')
 negatives=[]
 for name,label,change in [('wrong_entry_coefficient','entry_row_term','coefficient'),('wrong_nonentry_coefficient','nonentry_row_term','coefficient'),('missing_input_difference','actual_input_difference','omit'),('missing_funded_route','reserved_raw_main_MOVE','omit'),('false_public_descent','paid_rank2_nonentry_arrival','flag'),('omit_row_combination','combine_entry_and_nonentry','omit')]:
  k=next(m['physical_event'] for m in meta['marks'] if m['label']==label);bad=[e.copy() for e in meta['program']]
  if change=='omit':bad.pop(k)
  elif change=='flag':bad[k][4]=False
  else:bad[k][3]=str(F(bad[k][3])+1)
  try:
   z,c,b=replay(w,meta,bad);need(all(z[i]==ex for i,ex in expected.items()) and all(z[qm[i]]=={qm[i]:F(1),i:F(-1)} for i in qm),'mutated exact observable/input interface')
  except ValueError as exc:negatives.append({'mutation':name,'rejection':str(exc)})
  else:raise ValueError('accepted mutant '+name)
 return {'status':'PASS_ACTUAL_TWO_OBSERVABLE_ACQUISITION','source_sha256':PIN,'prefix_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'independent_physical_input_directions':1880,'arbitrary_common_roles_preserved':1480,'actual_differences_formed_and_preserved':400,'target_source_cut_before_event':30824,'target_roles':[1481,130],'target_supports':list(map(len,T)),'entry_terms':[sum(w['initial'][i]==3 for i in row) for row in T],'nonentry_terms':[sum(w['initial'][i]!=3 for i in row) for row in T],'all_nonentry_main_carriers_end_at127':200,'nonentry_donors_hoisted':len(meta['nonentry_donors']),'reserved_main_MOVEs_used':len(res),'reserved_main_MOVEs_unexecuted':meta['unexecuted_reserved_main_MOVEs'],'new_paid_MOVE_profile':{'7':2,'2':2},'exact_new_paid_moment_at_kappa_1_over_200':'2*7^(199/200)+2*2^(199/200)','entry_contribution_minor':'1/8','nonentry_contribution_minor':'-1/8','prefix_instructions':len(meta['program']),'typed_bill':bill,'additional_row_and_assembly_ADDs_beyond400_input_differences':87,'owned_output_retirements_outstanding':2,'source_row_l1_norms':[str(sum(map(abs,row.values()),F(0))) for row in T],'negative_controls':negatives,'scope':'Actual1880-input acquisition prefix, two live owned outputs at541; common data unchanged. Consumes exact raw-main reservations and changes chronology. No complete joint native, receiver continuation, uniform supplier, or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path);p.add_argument('--write-prefix',action='store_true');a=p.parse_args();r=run(a.source,a.packet,a.write_prefix);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
