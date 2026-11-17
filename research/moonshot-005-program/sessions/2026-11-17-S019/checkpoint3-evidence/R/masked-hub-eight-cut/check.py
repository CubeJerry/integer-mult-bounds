from pathlib import Path
import argparse,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();P=a.repo.resolve();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()=='f21de38f4a8adc1a55920c16b684285f62607829fe512a0088fe5ecb217fcfdd';w=json.loads(raw);src=(P/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots']
geom=P/'research/moonshot-005-program/sessions/2026-11-17-S019/checkpoint1-evidence/R/check_petersen_gate.py';sp=importlib.util.spec_from_file_location('root_fraction_geometry',geom);g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g);charts={k:g.chart(v)for k,v in w['charts'].items()};I=[52,82,98,101,106,107,57,85];mask=sum(1<<i for i in I);cut=w['carrier_interface_before_operation'];assert cut==1129
v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};original=set(v)
for op,n,*z in w['operations'][:cut]:
 if op=='INIT':assert n not in v;v[n]=0;at[n]=z[0]
 elif op=='ADD':assert n!=z[0]and charts[at[n]]==charts[at[z[0]]];v[z[0]]^=v[n]
 elif op=='MOVE':
  old,new=charts[at[n]],charts[z[0]];assert len(old)!=len(new)
  assert g.subset(old,new)if n in original else g.subset(new,old)
  at[n]=z[0]
 else:assert op=='CLEAR'and n not in original;del v[n],at[n]
assert all(sum(a*b for a,b in zip(roots[i],roots[j]))!=0 for i in I for j in I)
inside=[];outside=[]
for n,x in v.items():
 dest=[i for i in I if g.subset(charts[at[n]],charts[f'F{i}'])]
 if dest:assert not(x&mask),(n,dest);inside.append(n)
 elif x&mask:outside.append({'field':n,'chart':at[n],'chart_rank':len(charts[at[n]]),'projection_roles':[i for i in I if x>>i&1]})
assert len(v)==392 and len(inside)==254 and len(outside)==33
assert all(v[f'Y{i}']==1<<(111+i)and charts[at[f'Y{i}']]==[]for i in I)
def rank(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)
observations=[v[n]&mask for n in inside];demands=[1<<i for i in I];assert rank(observations+demands)-rank(observations)==8;altered=observations+[1<<I[0]];assert rank(altered+demands)-rank(altered)==7
report={'status':'PASS_MASKED_HUB_EIGHT_FRAME_CUT_PREMISES','word_sha256':hashlib.sha256(raw).hexdigest(),'native_source_sha256':w['source_sha256'],'geometry_sha256':hashlib.sha256(geom.read_bytes()).hexdigest(),'cut':cut,'frame':I,'ordered_nonorthogonal_pairs':64,'actual_live_fields':len(v),'inside_fields_count':len(inside),'inside_fields':inside,'all_inside_frame_projections_zero':True,'outside_fields_with_frame_information':outside,'conditional_linear_deficit':8,'scope_control_one_raw_frame_grant_deficit':7,'scope':'Fresh source application of existing downset theorem: >=8 distinct inward lifetimes for all-field linear or finite-alphabet nonlinear fixed schedules, not8 full Hub-to-ground tariffs.'}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'])
