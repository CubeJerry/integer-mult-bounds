#!/usr/bin/env python3
"""Fresh current-stock and full-history audit after endpoint/birth reduction."""
from pathlib import Path
import argparse,hashlib,importlib.util,json
WORD='6c76a836322483cc11888ae214379a27adbb8f638ac3a049584f75953c5185a9'
def load(path):
 s=importlib.util.spec_from_file_location('e',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def representation(rows,target):
 b={}
 for j,x in enumerate(rows):
  c=1<<j
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p][0];c^=b[p][1]
   else:b[p]=(x,c);break
 c=0
 while target:
  p=target.bit_length()-1
  if p not in b:return None
  x,q=b[p];target^=x;c^=q
 return [j for j in range(len(rows))if c>>j&1]
def dual(rows,i):
 b={}
 for x,t in [(r,0)for r in rows]+[(1<<i,1)]:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p][0];t^=b[p][1]
   else:b[p]=(x,t);break
  assert x or not t
 z=0
 for p,(r,t)in sorted(b.items()):
  if ((r&z).bit_count()%2)^t:z|=1<<p
 assert z>>i&1 and all(not((z&r).bit_count()%2)for r in rows)
 return z

def delivery_cut(w):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};born=set()
 for step,o in enumerate(w['operations'],1):
  op,n,*q=o
  if op=='INIT':v[n]=0;at[n]=q[0];born.add(n)
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='MOVE':at[n]=q[0]
  elif op=='CLEAR':del v[n],at[n]
  if all(f'P{i}'in v and at[f'P{i}']=='zero'for i in range(8))and all(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'for i in range(111)):
   return step,v.copy(),at.copy()
 raise AssertionError('No predecoder restored-input cut')

def main():
 p=argparse.ArgumentParser()
 for n in ['repo','word','engine','out']:p.add_argument('--'+n,type=Path,required=True)
 a=p.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()==WORD;w=json.loads(raw);src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];R=json.loads(src)['native_roots'];e=load(a.engine);C,H,rep=e.replay(w,R);step,v,at=delivery_cut(w);xmask=(1<<111)-1;dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]));ground=[r for n,r in v.items()if at[n]=='zero'and not r>>111]
 stock_rows=[];pure_rows=[];all_rows=[];actual=[];raw_stock=[];pure_fit=[];full_fit=[]
 for i in range(111):
  F=C[f'F{i}'];locals_=[1<<j for j in range(111)if dot(i,j)==0];stock=[r for n,r in v.items()if not r>>111 and e.sub(C[at[n]],F)];pure=[r for _,_,c,r in H if not r>>111 and e.sub(C[c],F)];all_=[r&xmask for _,_,c,r in H if e.sub(C[c],F)]
  if representation(stock,1<<i)is not None:actual.append(i)
  if representation(stock+locals_,1<<i)is not None:raw_stock.append(i)
  if representation(pure+locals_,1<<i)is not None:pure_fit.append(i)
  if representation(all_+locals_,1<<i)is not None:full_fit.append(i)
  stock_rows.append(stock+locals_);pure_rows.append(pure+locals_);all_rows.append(all_+locals_)
 def closure(base):
  known=set(w['targets']);waves=[]
  while True:
   nxt={i for i,rows in enumerate(base)if representation(rows+[1<<j for j in known],1<<i)is not None};assert known<=nxt
   if nxt==known:break
   waves.append(sorted(nxt-known));known=nxt
  ds=[{'receiver':i,'dual_hex':hex(dual(rows+[1<<j for j in known],i))}for i,rows in enumerate(base)if i not in known]
  return {'closure':sorted(known),'feedback_waves':waves,'outsider_duals':ds}
 results={'stock_plus_raw':closure(stock_rows),'pure_history_plus_raw':closure(pure_rows),'all_history_Xparts_plus_raw':closure(all_rows)}
 candidates=[]
 for i in sorted(set(results['all_history_Xparts_plus_raw']['closure'])-set(w['targets'])):
  candidates.append({'receiver':i,'currently_retained_stock_fits':i in actual,'stock_plus_raw_fits':i in raw_stock,'pure_history_plus_raw_fits':i in pure_fit,'full_history_plus_raw_fits':i in full_fit})
 out={'status':'PASS_FRESH_PROPER_BIRTH41_INFORMATION_AUDIT','word_sha256':WORD,'native_source_sha256':w['source_sha256'],'replay':rep,'fresh_delivery_cut_step':step,'fresh_common_rank':len(e.bb(ground)),'pure_current_stock_fitting':actual,'current_stock_plus_raw_fitting':raw_stock,'pure_history_plus_raw_fitting':pure_fit,'all_history_Xparts_plus_raw_fitting':full_fit,'models':results,'new_diagnostic_receivers':candidates,'scope':'Fresh word-derived information audit. All-history and raw-local grants are optimistic; no new endpoint is claimed without actual retained custody/nested receiver paths and a full price.'};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'CURRENT-STOCK.json').write_text(json.dumps({'cut_step':step,'fields':[{'field':n,'chart':at[n],'row_hex':hex(r),'pure_X':r>>111==0}for n,r in v.items()]},indent=2)+'\n');(a.out/'ALL-HISTORIES.json').write_text(json.dumps([{'step':s,'field':n,'chart':c,'row_hex':hex(r)}for s,n,c,r in H],indent=2)+'\n');print(json.dumps({'status':out['status'],'cut':step,'commonrank':out['fresh_common_rank'],'actual_count':len(actual),'stock_raw_count':len(raw_stock),'pure_history_count':len(pure_fit),'full_history_count':len(full_fit),'closures':{k:len(v['closure'])for k,v in results.items()},'new_receivers':candidates}))
if __name__=='__main__':main()
