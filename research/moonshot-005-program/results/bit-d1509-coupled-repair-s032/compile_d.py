"""Actual chronological binary compiler for the changed 35-owner D word."""
from pathlib import Path
import importlib.util,json,gzip,hashlib,numpy as np
repo=Path.cwd();base=repo/'research/moonshot-005-program/results';here=Path(__file__).parent;four=base/'bit-simultaneous-d1509-s032'
s=importlib.util.spec_from_file_location('dc',base/'bit-shared-h-s031-construction/native-d1509-all-native/compile_prefix.py');c=importlib.util.module_from_spec(s);s.loader.exec_module(c)
w=json.loads((here/'ALL-DONOR-VECTOR.json').read_text())['witness'];T=np.array(w['matrix'],dtype=np.uint8);old=json.loads(gzip.decompress((four/'output/D-WORD.json.gz').read_bytes()));prior=json.loads((four/'output/COMPILER-RESULT.json').read_text())
def eliminate(A):
 rows=c.binary_rows(A);n=len(rows);ops=[]
 def add(t,s):rows[t]^=rows[s];ops.append([t,s])
 for q in range(n):
  bit=1<<q
  if not rows[q]&bit:
   p=next(r for r in range(q+1,n)if rows[r]&bit);add(q,p);add(p,q);add(q,p)
  for r in range(n):
   if r!=q and rows[r]&bit:add(r,q)
 assert rows==[1<<q for q in range(n)];return ops
E=eliminate(T[:19,:19]);B=eliminate(T[19:,19:]);crossrows=c.binary_rows(T[19:,:19]);X=[1<<q for q in range(114)];Y=[1<<(114+q)for q in range(96)];cache=X.copy();cross=[]
for t,s in reversed(E):X[t]^=X[s]
for t,s in reversed(B):Y[t]^=Y[s]
for t,row in enumerate(crossrows):
 for s in range(114):
  if row>>s&1:Y[t]^=cache[s];cross.append([t,s])
assert X+Y==c.binary_rows(T)
for n,ops in [(114,E),(96,B)]:
 state=[1<<q for q in range(n)]
 for t,s in reversed(ops):state[t]^=state[s]
 for t,s in ops:state[t]^=state[s]
 assert state==[1<<q for q in range(n)]
new=2*(len(E)+len(B))+114+len(cross);previous=old['compiler']['including_pure_inverse_ADDs'];result={'status':'PASS_CHANGED_D1509_CHRONOLOGICAL_BINARY_WORD','early_ADD_per_direction':len(E),'late_ADD_per_direction':len(B),'cache_copy_ADD':114,'cross_ADD':len(cross),'including_pure_inverse_ADD':new,'old_D_including_pure_inverse_ADD':previous,'fullbank_ADD_delta':8*(new-previous),'new_fullbank_source_H_D_ADD':prior['fullbank_ADD_including_phase_inverses']+8*(new-previous),'fullbank_INIT_unchanged':prior['fullbank_INIT'],'fullbank_CLEAR_unchanged':prior['fullbank_dirty_CLEAR'],'fullbank_extra_field_exports_unchanged':16,'added_MOVEs':0,'all210_original_columns_checked':True,'full_global_supplier_invoice':False,'new_complete_kappa':False};(here/'COMPILER-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');payload={'owners':old['owners'],'matrix':T.tolist(),'inverse':w['inverse'],'early_elimination_ADD':E,'late_elimination_ADD':B,'late_cross_from_original_early_cache_ADD':cross,'cache_labels':old['compiler']['cache_labels']};(here/'D-WORD.json.gz').write_bytes(gzip.compress((json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0));print(result,flush=True)
