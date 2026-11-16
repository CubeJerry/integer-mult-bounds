"""Exact optimistic point-feedback closure with dual nondecodability witnesses."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def witness(rows,i,allowed):
 piv={}
 for row,rhs in[(z&allowed,0)for z in rows]+[(1<<i,1)]:
  while row:
   b=(row&-row).bit_length()-1
   if b in piv:r,h=piv[b];row^=r;rhs^=h
   else:piv[b]=(row,rhs);break
  else:assert rhs==0
 z=0
 for b in sorted(piv,reverse=True):
  row,rhs=piv[b]
  if rhs^((row&z).bit_count()%2):z^=1<<b
 assert z&~allowed==0 and z>>i&1 and all((r&z).bit_count()%2==0 for r in rows);return z
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));a=ap.parse_args();raw=a.word.read_bytes();w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','static_ascending_engine');t=load(Path(__file__).with_name('build_d4_cohort.py'),'static_ascending_trace');e.replay(w,R);v,_=t.trace(w['operations'])[w['carrier_interface_before_operation']];local=[sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)];fields=['KEEP_C0','KEEP_C1','KEEP_C2','ZFIRST3','ZFIRST4','ZFIRST5'];cases={'three_modes':fields[3:],'six_first_retentions':fields,'all_source_and_groups':fields+[n for n in v if n.startswith('ASC_GROUP_')]};out={};allmask=(1<<111)-1
 for name,names in cases.items():
  known=set(w['targets']);waves=[];rows=[v[n]for n in names];assert all(z>>111==0 for z in rows)
  while True:
   km=sum(1<<i for i in known);nxt=[i for i in range(111)if i not in known and e.fits([z&~(km|local[i])for z in rows],1<<i)]
   if not nxt:break
   known.update(nxt);waves.append(nxt)
  km=sum(1<<i for i in known);missing=sorted(set(range(111))-known);certs=[]
  for i in missing:
   allowed=allmask&~(km|local[i]);z=witness(rows,i,allowed);certs.append({'receiver':i,'indistinguishable_input_delta_hex':hex(z),'support':[j for j in range(111)if z>>j&1]})
  out[name]={'fields':names,'waves':waves,'closure_count':len(known),'closure':sorted(known),'missing':missing,'dual_witnesses':certs}
 result={'status':'PASS_EXACT_OPTIMISTIC_STATIC_CLOSURES_AND_DUALS','word_sha256':hashlib.sha256(raw).hexdigest(),'grant':'Listed actual retained rows globally; all completed raw coordinates globally; every geometrically local raw input separately at each receiver; all newly decoded raw coordinates fed back globally for free. This is stronger than physical chain access.','cases':out,'scope':'Fixed source-code static closure only. Does not exclude changed earlier histories, added source rows, or dynamic source transformations.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({n:{'count':z['closure_count'],'waves':z['waves'],'dual_count':len(z['dual_witnesses'])}for n,z in out.items()}))
if __name__=='__main__':main()
