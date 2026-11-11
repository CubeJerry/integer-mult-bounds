import argparse,copy,gzip,hashlib,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def req(x,m):
 if not x:raise ValueError(m)
def add(a,b,c):
 a=dict(a)
 for k,v in b.items():
  a[k]=a.get(k,F(0))+c*v
  if not a[k]:del a[k]
 return a
def span(b):
 s={0}
 for v in b:s|={x^v for x in tuple(s)}
 return s
def adj(w,role,main):
 a={role:F(1)}
 for e in reversed(w['program'][:30824]):
  op=e[0]
  if op=='ADD':
   v=a.get(e[1],F(0))*F(e[3])
   if v:
    a[e[2]]=a.get(e[2],F(0))+v
    if not a[e[2]]:del a[e[2]]
  elif op=='SCALE':
   if e[1] in a:a[e[1]]*=F(e[2])
  elif op=='COPY':
   v=a.pop(e[1],F(0))
   if v:
    a[e[2]]=a.get(e[2],F(0))+v
    if not a[e[2]]:del a[e[2]]
  elif op=='INIT':a.pop(e[1],None)
  elif op=='CLEAR':req(e[1] not in a,'future read after CLEAR')
  else:req(op=='MOVE','source opcode')
 return {k:v for k,v in a.items() if k in main and v}
def check(p,w,main,rows,selected,newprofile):
 mp={q:1480+i for i,q in enumerate(sorted(main))};dims=list(map(len,w['frames']));sp=list(map(span,w['frames']))
 req(p['difference_role_map']=={str(q):r for q,r in mp.items()},'raw role map')
 req((p['public'],p['common_owned_labels_reserved'],p['owned_labels_declared'])==(1880,51,54),'physical declarations')
 req(p['initial']==w['initial']+[w['initial'][q] for q in sorted(main)],'initial charts')
 val={i:{i:F(1)} for i in range(1880)};loc=dict(enumerate(p['initial']));own=set();labels=set();peak=birth=0;cnt=Counter();mh=Counter();nh=Counter();rawmoves=[]
 for i,e in enumerate(p['program']):
  op=e[0];cnt[op]+=1
  if op=='INIT':
   _,r,f=e;req(r in range(1931,1934) and r not in val and 0<=f<len(sp),'fresh INIT/reserved labels');val[r]={};loc[r]=f;own.add(r);labels.add(r);birth+=1;peak=max(peak,len(own))
  elif op=='CLEAR':
   _,r,f=e;req(r in own and loc[r]==f,'owned CLEAR');del val[r];del loc[r];own.remove(r)
  elif op=='ADD':
   _,d,s,c,f=e;req(d in val and s in val and loc[d]==loc[s]==f,'cochart ADD');req(F(c)!=0,'nonzero coefficient');val[d]=add(val[d],val[s],F(c))
  elif op=='MOVE':
   _,r,s,t,flag=e;req(r in val and loc[r]==s and s!=t,'MOVE endpoint');req(flag==(r in own),'MOVE ownership');req(sp[s]<sp[t] or (r in own and sp[t]<sp[s]),'nested/public ascent');rank=abs(dims[s]-dims[t]);mh[rank]+=1
   if r in own:nh[rank]+=1
   else:rawmoves.append(i)
   loc[r]=t
  else:raise ValueError('prefix opcode '+op)
 req(own=={1931,1932} and loc[1931]==loc[1932]==541,'two live owned outputs')
 for r in range(1480):req(val[r]=={r:F(1)} and loc[r]==w['initial'][r],'arbitrary common preserved')
 for q,r in mp.items():
  req(val[r]=={r:F(1),q:F(-1)},'all actual q preserved');req(loc[r]==(w['final'][q] if q in selected else w['initial'][q]),'raw endpoint chart')
 for name,row in rows.items():
  target={}
  for q,c in row.items():target=add(target,{mp[q]:F(1),q:F(-1)},c)
  r=1931 if name=='r_delta1481' else 1932;req(val[r]==target,'exact1880-input observable '+name);req(p['output_rows'][0 if name=='r_delta1481' else 1]=={str(k):str(v) for k,v in sorted(row.items())},'logical output row')
 req(p['output_roles']=={'r_delta1481':1931,'Mnew_delta130':1932} and p['output_chart']==541,'output labels')
 se=[i for i,e in enumerate(w['program']) if e[0]=='MOVE' and e[1] in selected];rs=p['reserved_raw_main_routes'];req([r['physical_event'] for r in rs]==rawmoves,'all raw MOVEs reserved');req([r['source_event'] for r in rs]==se and len(set(se))==len(rs),'all selected routes once in source order')
 for r in rs:
  e=w['program'][r['source_event']];req(e==['MOVE',r['logical_main'],r['source_chart'],r['target_chart'],False],'original source occurrence');req(p['program'][r['physical_event']]==['MOVE',mp[e[1]],e[2],e[3],False],'renamed source occurrence');req(r['physical_main']==mp[e[1]] and r['rank']==abs(dims[e[2]]-dims[e[3]]),'reservation rank')
 total=sum(e[0]=='MOVE' and e[1] in main for e in w['program']);req(p['unexecuted_reserved_main_MOVEs']==total-len(rs),'unexecuted reservations');req(nh==Counter(newprofile),'new paid profile');req(labels=={1931,1932,1933} and peak==3,'fresh labels and peak')
 return {'counts':dict(cnt),'MOVE_histogram':dict(mh),'new_paid_MOVE_profile':dict(nh),'instructions':len(p['program']),'owned_lifetimes':birth,'peak_owned':peak,'fresh_owned_labels':3,'live_owned_outputs':2,'common_rows_preserved':1480,'raw_q_rows_preserved':400,'independent_inputs':1880,'unique_source_routes_used':len(rs),'source_routes_unexecuted':total-len(rs)}
def run(repo,pkg):
 raw=(repo/'research/shared-wire-split-composition/data/final.json.gz').read_bytes();req(hashlib.sha256(raw).hexdigest()==PIN,'source pin');w=json.loads(gzip.decompress(raw));main=set(w['live'])|{q+112 for q in w['live']}|set(w['hosted']['X2'])|set(w['hosted']['Y2']);rows={'r_delta1481':adj(w,1481,main),'Mnew_delta130':adj(w,130,main)};support=set().union(*map(set,rows.values()));entry={q for q in support if w['initial'][q]==3};non=support-entry;req((len(rows['r_delta1481']),len(rows['Mnew_delta130']),len(support),len(entry),len(non))==(59,26,60,8,52),'adjoint support partition');out={};pins={}
 for name,file,receipt,selected,profile,expected in [('direct','ACQUISITION-PREFIX.json','RESULT.json',non,{7:2,2:2},(730,233,4)),('lifted','LIFTED-PREFIX.json','LIFTED-RESULT.json',support,{1:8,2:2},(783,262,10))]:
  b=(pkg/file).read_bytes();p=json.loads(b);a=json.loads((pkg/receipt).read_text());req(p['source_sha256']==PIN and hashlib.sha256(b).hexdigest()==a['prefix_sha256'],'author prefix pin');r=check(p,w,main,rows,selected,profile);req((r['instructions'],r['unique_source_routes_used'],r['owned_lifetimes'])==expected,'independent census');req(r['counts']==a['typed_bill']['counts'] and r['MOVE_histogram']=={int(k):v for k,v in a['typed_bill']['MOVE_histogram'].items()},'author billing');controls=[]
  for mutation in ['wrong_owned_output','wrong_input_difference','broken_reserved_route','false_public_descent','erase_live_output']:
   bad=copy.deepcopy(p)
   if mutation=='wrong_owned_output':
    i=next(i for i,e in enumerate(bad['program']) if e[0]=='ADD' and e[1]==1931);bad['program'][i][3]=str(F(bad['program'][i][3])+1)
   elif mutation=='wrong_input_difference':bad['program'][0][3]='1'
   elif mutation=='broken_reserved_route':bad['program'][bad['reserved_raw_main_routes'][0]['physical_event']][2]=3
   elif mutation=='false_public_descent':
    i=next(i for i,e in enumerate(bad['program']) if e[0]=='MOVE' and e[1]>=1931 and len(w['frames'][e[2]])>len(w['frames'][e[3]]));bad['program'][i][4]=False
   else:bad['program'].append(['CLEAR',1931,541])
   try:check(bad,w,main,rows,selected,profile)
   except ValueError as err:controls.append({'mutation':mutation,'rejection':str(err)})
   else:raise ValueError('negative control survived')
  r['negative_controls']=controls;out[name]=r;pins[file]=hashlib.sha256(b).hexdigest();pins[receipt]=hashlib.sha256((pkg/receipt).read_bytes()).hexdigest()
 return {'status':'PASS_INDEPENDENT_BOTH_1880_INPUT_ACQUISITION_PREFIXES','source_sha256':PIN,'reviewed_artifact_pins':pins,'source_rows':{n:{str(k):str(v) for k,v in sorted(row.items())} for n,row in rows.items()},'source_row_method':'Fresh reverse adjoints before source30824 with zero initial helper differences.','variants':out,'scope':'Exact finite1880-input acquisition prefixes, all1480 arbitrary common fields and400 raw differences preserved, two live owned outputs at541. No native source-clock state, S8 composition, output retirement, continuation, precision admission, or new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repository',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.repository,a.package);a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(r['status'])
