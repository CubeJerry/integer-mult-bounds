from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
from collections import defaultdict
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def trace(w):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};ans=[]
 for o in w['operations']:
  ans.append((v.copy(),at.copy()));op,n,*q=o
  if op=='INIT':v[n]=0;at[n]=q[0]
  elif op=='MOVE':at[n]=q[0]
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='CLEAR':del v[n],at[n]
 ans.append((v,at));return ans
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();P=a.repo/'research/moonshot-005-program'
 e=load(P/'results/bit-leaf-capacity-quotient/author/check.py','prune_engine');assert hashlib.sha256(a.base.read_bytes()).hexdigest()=='075896b6aafe6d0bbb6d406a2cca367c644357f57e01a7888cdfde843f61bd4b';w=json.loads(a.base.read_text());assert hashlib.sha256((a.repo/w['source_path']).read_bytes()).hexdigest()==w['source_sha256'];R=json.loads((a.repo/w['source_path']).read_text())['native_roots'];C,H,before=e.replay(w,R);st=trace(w);ops=w['operations'];cut=w['carrier_interface_before_operation']
 owned={o[1]for o in ops if o[0]=='INIT'}
 keep_ground=[n for n,z in st[cut][0].items()if n in owned and z and C[st[cut][1][n]]==C['zero']]
 live={f'{q}{i}'for q in ['X','Y']for i in range(111)};keep=set();needed=set();removed_zero=0
 for k in reversed(range(len(ops))):
  if k==cut-1:live.update(keep_ground)
  op,n,*q=ops[k]
  if op=='ADD':
   if q[0]in live and st[k][0][n]:keep.add(k);live.add(n)
   elif not st[k][0][n]:removed_zero+=1
  elif op=='MOVE':
   if n in live:keep.add(k)
  elif op=='INIT':
   if n in live:keep.add(k);needed.add(n);live.remove(n)
 for k,o in enumerate(ops):
  if o[0]=='CLEAR'and o[1]in needed:keep.add(k)
 required=defaultdict(list)
 for k in sorted(keep):
  op,n,*q=ops[k]
  if op=='ADD':
   required[n].append((k,st[k][1][n]));required[q[0]].append((k,st[k][1][q[0]]))
 for n in keep_ground:required[n].append((cut,st[cut][1][n]))
 for q in ['X','Y']:
  for i in range(111):n=f'{q}{i}';required[n].append((len(ops),st[-1][1][n]))
 newkeep={k for k in keep if ops[k][0]!='MOVE'};birth_changes={};fusions=[]
 for n,req in required.items():
  req=sorted(req);moves=[k for k in sorted(keep)if ops[k][0]=='MOVE'and ops[k][1]==n]
  if n in owned:
   bi=next(k for k in keep if ops[k][0]=='INIT'and ops[k][1]==n);birth_changes[bi]=req[0][1];prev_index=bi;prev_chart=req[0][1]
  else:prev_index=-1;prev_chart=f'L{n[1:]}'if n.startswith('X')else'zero'
  for k,ch in req:
   if C[ch]!=C[prev_chart]:
    avail=[z for z in moves if prev_index<z<k and C[ops[z][2]]==C[ch]]
    assert avail,(n,prev_index,k,prev_chart,ch)
    newkeep.add(avail[-1]);fusions.append({'name':n,'new_move':ops[avail[-1]],'old_index':avail[-1]})
   prev_index=k;prev_chart=ch
 newops=[];newcut=None
 for k,o in enumerate(ops):
  if k==cut:newcut=len(newops)
  if k not in newkeep:continue
  if o[0]=='INIT':o=['INIT',o[1],birth_changes[k]]
  newops.append(o)
 nw={k:copy.deepcopy(z)for k,z in w.items()};nw.update(operations=newops,carrier_interface_before_operation=newcut,schema='endpoint-and-common-source-pruned-projection-v1',base_word_sha256=hashlib.sha256(a.base.read_bytes()).hexdigest(),preserved_common_fields=keep_ground,scope='Pruned release78 source preserves46 endpoints, every public original and each listed actual common field at the interface. All78 released originals remain raw at their native lines until the interface. Higher-chart rows/history not inherited. No completed111 supplier or new kappa.')
 CC,HH,after=e.replay(nw,R);nst=trace(nw);assert all(nst[newcut][0][n]==st[cut][0][n]and CC[nst[newcut][1][n]]==C['zero']for n in keep_ground)
 for i in w['released_carriers']:assert nst[newcut][0][f'X{i}']==1<<i and nst[newcut][1][f'X{i}']==f'L{i}'
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(nw,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw)
 report={'status':'PASS_PRUNED_RELEASE78_COMMON_INTERFACE','word_sha256':hashlib.sha256(raw).hexdigest(),'base_sha256':hashlib.sha256(a.base.read_bytes()).hexdigest(),'before':before,'after':after,'interface_index':newcut,'preserved_common_fields':keep_ground,'preserved_common_rank':len(e.bb(st[cut][0][n]for n in keep_ground)),'kept_owner_count':len(needed),'removed_zero_ADDs':removed_zero,'proper_births':{str(k):ch for k,ch in birth_changes.items()if ch!=ops[k][2]},'scope':nw['scope']};(a.out/'RESULT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
