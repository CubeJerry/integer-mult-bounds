"""Source-contract replay, portable inventories, and semantic destructive controls.

This is author-side verification; the independent C implementation is separate.
"""
from pathlib import Path
import argparse,collections,copy,hashlib,importlib.util,json

def rank(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)

def span_has(rows,x):return rank(rows+[x])==rank(rows)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);w=json.loads(a.word.read_text());raw=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==w['source_sha256'];R=json.loads(raw)['native_roots'];ep=a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py';sp=importlib.util.spec_from_file_location('interleaved_author_control',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e);C={h:e.chart(z)for h,z in w['charts'].items()};_,_,stats=e.replay(w,R);T=w['targets'];P=w['construction'];code={int(i):j for i,j in P['code_carrier'].items()};common=P['common_roles'];commonrow=sum(1<<j for j in common);held=set(code.values());dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));K=[(1<<i)^sum(1<<j for j in range(111)if dot(i,j)==0)for i in range(111)];basis=[K[i]for i in P['canonical_basis_roles']]
 def trace(word,marks):
  v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};out={}
  for k in range(len(word['operations'])+1):
   if k in marks:out[k]=(v.copy(),at.copy())
   if k==len(word['operations']):break
   typ,n,*q=word['operations'][k]
   if typ=='INIT':v[n]=0;at[n]=q[0]
   elif typ=='ADD':v[q[0]]^=v[n]
   elif typ=='MOVE':at[n]=q[0]
   else:del v[n];del at[n]
  return out
 keys=['all_six_Y_waiting_at_facets','only_six_raw_code_originals_held','canonical_ground_while_six_held'];indices=[w['milestones'][k]for k in keys]+[w['carrier_interface_before_operation']]
 def contracts(word,inds):
  snaps=trace(word,set(inds));v,at=snaps[inds[0]];assert all(at[f'Y{i}']==f'F{i}'for i in T);assert not any(n.startswith('CANONICAL_')for n in v),'early Y timing'
  for idx in inds[1:3]:
   v,at=snaps[idx]
   for j in range(111):assert v[f'X{j}']==1<<j and at[f'X{j}']==('COMMON'if j in held else'Hub'),('held source',j)
   for i in T:assert v[f'Y{i}']==(1<<(111+i))^(1<<code[i])^(K[i]^(1<<i)^commonrow),('waiting Y',i)
  v,at=snaps[inds[2]]
  for k,n in enumerate(P['canonical_fields']):assert v[n]==basis[k]and at[n]=='zero',('canonical query',k)
  for i in T:assert v[f'LATE_CODE_{i}']==K[i]^commonrow,('proper code',i)
  v,at=snaps[inds[3]]
  for j in range(111):assert v[f'X{j}']==1<<j and at[f'X{j}']=='Hub'and v[f'NATIVE_RAW_{j}']==1<<j and at[f'NATIVE_RAW_{j}']==f'L{j}',('final raw/native',j)
  for i in range(111):assert v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in T else 0)and at[f'Y{i}']==(f'F{i}'if i in T else'zero'),('final Y',i)
  for i,roles in P['raw_mask_roles'].items():assert v[f'MASK_{i}']==sum(1<<j for j in roles),('mask source',i)
  return snaps
 snaps=contracts(w,indices)
 controls=[]
 for key,choices in w['semantic_operation_indices'].items():
  for idx in choices:
   m=copy.deepcopy(w);del m['operations'][idx];mis=[z-int(idx<z)for z in indices]
   try:e.replay(m,R);contracts(m,mis)
   except (AssertionError,KeyError,ValueError)as ex:controls.append({'class':key,'deleted_index':idx,'operation':w['operations'][idx],'rejected':True,'reason':str(ex)[:240]});break
  else:raise AssertionError(('all omissions passed',key))
 # Exact actual state inventories, and optimistic facet accessibility separated
 # from the one-chain availability needed by a receiver execution.
 for label,idx in [('canonical_ground_cut',indices[2]),('completed_six_cut',indices[3])]:
  v,at=snaps[idx];fields=[{'name':n,'chart':at[n],'chart_rank':len(C[at[n]]),'coefficient_row_hex':hex(x),'has_initial_Y_columns':bool(x>>111)}for n,x in sorted(v.items())];facets=[]
  for i in range(111):
   if i in T:continue
   names=[n for n in v if e.sub(C[at[n]],C[f'F{i}'])];pure=[n for n in names if not(v[n]>>111)];local=[1<<j for j in range(111)if dot(i,j)==0];masknames=[n for n in pure if n.startswith('MASK_')];masks=[v[n]for n in masknames];b=[v[n]for n in pure if not n.startswith('MASK_')]
   facets.append({'receiver':i,'accessible_live_fields':names,'accessible_pure_X_fields':pure,'all_column_rank':rank([v[n]for n in names]),'pure_X_rank':rank([v[n]for n in pure]),'pure_X_rank_without_masks':rank(b),'native_raw_rank':len(local),'mask_fields':masknames,'mask_rank':rank(masks),'masks_in_native_side_information':all(span_has(local,x)for x in masks),'target_in_optimistic_facet_span':span_has([v[n]for n in names],(1<<i)^(1<<(111+i)))})
  inv={'word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'cut_before_operation':idx,'label':label,'fields':fields,'unfinished_facets':facets,'scope':'Actual fields and positions. Facet-containment lists are optimistic accessibility envelopes, not simultaneous custody or legal one-chain decoder grants.'};(a.out/(label+'.json')).write_text(json.dumps(inv,indent=2)+'\n')
 # Exact helper geometry determines what a single upward path can read.
 masks=[f'MASK_{i}'for i in T];helper={'charts':[{'field':n,'chart':at[n],'raw_roles':P['raw_mask_roles'][n[5:]],'native_roles_in_chart':[j for j in range(111)if e.sub(C[f'L{j}'],C[at[n]])]}for n in masks],'proper_containment_pairs':[[p,q]for p in masks for q in masks if p!=q and e.sub(C[at[p]],C[at[q]])]};(a.out/'helper_geometry.json').write_text(json.dumps(helper,indent=2)+'\n')
 result={'status':'PASS_INTERLEAVED_SOURCE_AND_DESTRUCTIVE_CONTROLS','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'source_sha256':w['source_sha256'],'verifier_sha256':hashlib.sha256(ep.read_bytes()).hexdigest(),'stats':stats,'controls':controls,'checked_source_cuts':indices,'unfinished_facets_with_some_mask':sum(bool(z['mask_fields'])for z in facets),'mask_rank_histogram':dict(collections.Counter(z['mask_rank']for z in facets)),'all_mask_local_ranks_unchanged':all(z['pure_X_rank']==z['pure_X_rank_without_masks']for z in facets),'scope':'Author-side exact checks; independent mathematical review is separate.'};(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','word_sha256','checked_source_cuts','unfinished_facets_with_some_mask','mask_rank_histogram','all_mask_local_ranks_unchanged']}))
if __name__=='__main__':main()
