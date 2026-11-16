#!/usr/bin/env python3
"""Paid46 audit and exact comparison of actual observation spans."""
from pathlib import Path
from fractions import Fraction
import argparse,copy,hashlib,importlib.util,json
BASE='9053904c95084269c8d2df3f883a8c32dfadff763a2c0338a5ebf7c45d4d6267'
WORD='a0f0e1b5aa027d9f8faea8a529f47b5757f438f8609e1819af5e2a0f4da3b8fc'
CODED='45479de20faad9d9cd4ace9493057b82fb2c8b6f8baa4ac67134571f2e5cca84'
PROTECTED='de4e5799da70814323cbe233e118c6bb26cbf3ac537bf77d4669db3304f9e460'
POINTS=[8,9,36,37,50]
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def separate(rows,target):
 b={}
 for r,t in [(x,0)for x in rows]+[(target,1)]:
  while r:
   p=r.bit_length()-1
   if p in b:r^=b[p][0];t^=b[p][1]
   else:b[p]=(r,t);break
  assert r or not t
 z=0
 for p,(r,t)in sorted(b.items()):
  if ((r&z).bit_count()%2)^t:z|=1<<p
 assert (target&z).bit_count()%2 and all(not((r&z).bit_count()%2)for r in rows)
 return z
def compare(e,left,right):
 a,b=e.bb(left),e.bb(right);union=e.bb(list(a.values())+list(b.values()))
 def missing(x,y):
  for r in x:
   if not e.fits(y,r):return {'row_hex':hex(r),'separating_dual_hex':hex(separate(y,r))}
  return None
 return {'left_rank':len(a),'right_rank':len(b),'intersection_rank':len(a)+len(b)-len(union),'left_not_in_right':missing(a.values(),list(b.values())),'right_not_in_left':missing(b.values(),list(a.values()))}
def main():
 p=argparse.ArgumentParser()
 for n in ['repo','base','word','author-result','coded-word','protected-coded-word','engine','price-engine','history-engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();assert sha(a.base)==BASE and sha(a.word)==WORD and sha(a.coded_word)==CODED and sha(a.protected_coded_word)==PROTECTED
 old=json.loads(a.base.read_text());w=json.loads(a.word.read_text());assert w['base_word_sha256']==BASE and set(w['targets'])==set(old['targets'])|set(POINTS)and not(set(POINTS)&set(old['targets']))
 src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256']==old['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine,'e');price=load(a.price_engine,'p');hist=load(a.history_engine,'h')
 C0,H0,r0=e.replay(old,R);C,H,r=e.replay(w,R);assert r['counts']=={'INIT':127,'ADD':819,'MOVE':481,'CLEAR':127}and r['dirty_CLEAR']==127
 names={f'ADDED_RAW{i}'for i in POINTS};assert [o for o in w['operations']if not any(n in names for n in o[1:])]==old['operations'];prefix=[]
 for i in POINTS:prefix += [['INIT',f'ADDED_RAW{i}',f'L{i}'],['ADD',f'X{i}',f'ADDED_RAW{i}'],['MOVE',f'ADDED_RAW{i}','zero']]
 assert w['operations'][:15]==prefix
 d={k:r['movement_profile'].get(k,0)-r0['movement_profile'].get(k,0)for k in set(r['movement_profile'])|set(r0['movement_profile'])};d={k:n for k,n in d.items()if n};assert d=={1:5}
 inv=lambda s,C:{n:v for n,v in s[1].items()if n!='P3'and not v>>111 and C[s[2][n]]==C['M1']}
 s0,g0=hist.cut(old);s,g=hist.cut(w);assert inv(s,C)==inv(s0,C0)and len(e.bb(inv(s,C).values()))==11
 for i in [8,9,36]:
  name=f'IMPORT_E{i}';assert s[1][name]==1<<i and s[2][name]=='M1';probe=copy.deepcopy(w);ix=probe['operations'].index(['ADD','CAP46','P3']);probe['operations'][ix:ix]=[['ADD',name,'P3'],['ADD',name,'P3']];e.replay(probe,R)
 controls=[]
 for i in POINTS:
  for op in [['ADD',f'X{i}',f'ADDED_RAW{i}'],['MOVE',f'ADDED_RAW{i}','zero'],['ADD',f'ADDED_RAW{i}',f'Y{i}'],['CLEAR',f'ADDED_RAW{i}']]:
   bad=copy.deepcopy(w);bad['operations'].remove(op)
   try:e.replay(bad,R)
   except (AssertionError,KeyError)as ex:controls.append({'removed':op,'rejected':str(ex)})
   else:raise AssertionError(('essential omission accepted',op))
 B={127:37,64:74,1:-74}
 for j in range(1,9):B[1+7*j]=B.get(1+7*j,0)+74;B[7*j]=B.get(7*j,0)-74
 allowance=tuple(v/6 for v in price.moment(B));Q=price.moment(r['movement_profile']);room=(allowance[0]-Q[1],allowance[1]-Q[0]);author=json.loads(a.author_result.read_text())
 for key,z in [('moment',Q),('limiting_room',room)]:assert Fraction(author['price'][key]['lower_fraction'])<=z[0]<=z[1]<=Fraction(author['price'][key]['upper_fraction'])
 variants={'paid_raw46':(w,C,H,r,s,g,WORD)}
 for label,path,pin in [('coded46',a.coded_word,CODED),('protected_coded46',a.protected_coded_word,PROTECTED)]:
  ww=json.loads(path.read_text());assert ww['targets']==w['targets']and ww['source_sha256']==w['source_sha256'];CC,HH,rr=e.replay(ww,R);ss,gg=hist.cut(ww);variants[label]=(ww,CC,HH,rr,ss,gg,pin)
 mask=(1<<111)-1;data={};spaces={}
 for label,(ww,CC,HH,rr,ss,gg,pin)in variants.items():
  stock=[(n,gg[2][n],v)for n,v in gg[1].items()if not v>>111];common=[v for n,c,v in stock if c=='zero'];observed=[];current=[];own_fail=[];quotient_fail=[];targets=set(ww['targets'])
  for i in range(111):
   current.append([v for n,c,v in stock if e.sub(CC[c],CC[f'F{i}'])]);rows=[v&mask for _,_,c,v in HH if e.sub(CC[c],CC[f'F{i}'])];observed.append(rows)
   if i not in targets:
    if any(v>>i&1 for v in rows):own_fail.append(i)
    local={j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0};keep=mask^sum(1<<j for j in targets|local);rank=len(e.bb(v&keep for v in rows))
    if rank:quotient_fail.append([i,rank])
  known=targets.copy();waves=[]
  while True:
   nxt={i for i,rows in enumerate(observed)if e.fits(rows+[1<<j for j in known],1<<i)};assert known<=nxt
   if nxt==known:break
   waves.append(sorted(nxt-known));known=nxt
  duals=[{'receiver':i,'dual_hex':hex(price.outsider_dual(rows+[1<<j for j in known],i))}for i,rows in enumerate(observed)if i not in known]
  outside_mask=mask^sum(1<<j for j in targets);owned={o[1]for o in ww['operations']if o[0]=='INIT'};owned_rows=[v&outside_mask for n,c,v in stock if n in owned]
  data[label]={'word_sha256':pin,'replay':rr,'moment':price.display(price.moment(rr['movement_profile'])),'actual_M1_inventory':{n:hex(v)for n,v in inv(ss,CC).items()},'actual_M1_rank':len(e.bb(inv(ss,CC).values())),'actual_M1_outsider_quotient_rank':len(e.bb(v&outside_mask for v in inv(ss,CC).values())),'actual_common_rank':len(e.bb(common)),'all_current_owned_outsider_quotient_rank':len(e.bb(owned_rows)),'fresh_all_history_feedback_closure':sorted(known),'feedback_waves':waves,'outsider_duals':duals,'outsider_own_coordinate_nonzero_failures':own_fail,'outsider_history_mod_rawlocals_and_targets_nonzero_ranks':quotient_fail,'common_rows_hex':[hex(v)for v in common]};spaces[label]=(current,observed,common)
 comparisons={}
 for label in ['coded46','protected_coded46']:
  left,lh,lc=spaces[label];right,rh,rc=spaces['paid_raw46'];cur=[{'receiver':i,**compare(e,left[i],right[i])}for i in range(111)];history=[{'receiver':i,**compare(e,lh[i],rh[i])}for i in range(111)]
  pd={k:variants[label][3]['movement_profile'].get(k,0)-r['movement_profile'].get(k,0)for k in set(variants[label][3]['movement_profile'])|set(r['movement_profile'])}
  comparisons[label]={'orientation':'left=coded variant; right=paid_raw46','common':compare(e,lc,rc),'current_stock_native_receivers':cur,'all_history_native_receivers':history,'coded_current_not_contained_in_paid_count':sum(c['left_not_in_right']is not None for c in cur),'paid_current_not_contained_in_coded_count':sum(c['right_not_in_left']is not None for c in cur),'coded_history_not_contained_in_paid_count':sum(c['left_not_in_right']is not None for c in history),'paid_history_not_contained_in_coded_count':sum(c['right_not_in_left']is not None for c in history),'coded_price_minus_paid':price.display(price.moment(pd))}
 out={'status':'PASS_INDEPENDENT_PAID_RAW46_WITH_NONDOMINATING_SPAN_COMPARISON','word_sha256':WORD,'base_word_sha256':BASE,'source_sha256':w['source_sha256'],'replay':r,'all_parent_operations_retained_in_order':True,'added_points':POINTS,'exact_movement_increment':d,'price':{'moment':price.display(Q),'limiting_room':price.display(room)},'actual_M1_inventory_unchanged':True,'three_actual_import_access_probes_pass':True,'semantic_controls':controls,'variants':data,'span_comparisons':comparisons,'scope':'Cheaper identical endpoints do not imply dominance of actual common or receiver observation spans. Source custody and simultaneous historical observation envelopes remain distinct.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'status':out['status'],'price':out['price'],'variants':{k:{z:v[z]for z in ['actual_M1_rank','actual_M1_outsider_quotient_rank','actual_common_rank','all_current_owned_outsider_quotient_rank','outsider_own_coordinate_nonzero_failures','outsider_history_mod_rawlocals_and_targets_nonzero_ranks']}for k,v in data.items()},'comparisons':{k:{z:v[z]for z in ['common','coded_current_not_contained_in_paid_count','paid_current_not_contained_in_coded_count','coded_history_not_contained_in_paid_count','paid_history_not_contained_in_coded_count','coded_price_minus_paid']}for k,v in comparisons.items()}}))
if __name__=='__main__':main()
