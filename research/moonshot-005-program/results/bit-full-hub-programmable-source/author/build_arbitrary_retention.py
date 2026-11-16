"""Six fully programmable first retentions, with all displaced readers paid."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json

def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def trace(w):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)}
 at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};states=[]
 for o in w['operations']:
  states.append((v.copy(),at.copy()));op,n,*q=o
  if op=='INIT':v[n]=0;at[n]=q[0]
  elif op=='MOVE':at[n]=q[0]
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='CLEAR':del v[n],at[n]
 states.append((v,at));return states

FIELDS=['KEEP_C0','KEEP_C1','KEEP_C2','ZFIRST3','ZFIRST4','ZFIRST5']
READERS=[[3,21],[76,64],[80,65],[4],[74],[78]]

def build(base,desired):
 """For any six binary111 rows, preserve46 endpoints and realize the rows."""
 assert len(desired)==6 and all(0<=c<1<<111 for c in desired)
 states=trace(base);ops=base['operations'];before={};after={};data=[]
 for j,(field,readers,c)in enumerate(zip(FIELDS,READERS,desired)):
  p=f'P{j}';start=next(k for k,o in enumerate(ops)if o[0]=='ADD'and o[2]==p and states[k][1][p]=='Hub')
  cap=ops.index(['ADD',p,field]);r=states[cap][0][p];u=r^c
  assert all(states[start][0][f'X{i}']==1<<i and states[start][1][f'X{i}']=='Hub'for i in range(111))
  donors=[f'X{i}'for i in range(111)if u>>i&1]
  before.setdefault(start,[]).extend(['ADD',n,p]for n in donors)
  owners=[]
  for i in readers:
   n=f'ARBITRARY_P{j}_REPAIR{i}';owners.append(n)
   before[start].extend([['INIT',n,'Hub']]+[['ADD',x,n]for x in donors]+[['MOVE',n,f'F{i}']])
   ix=ops.index(['MOVE',f'Y{i}',f'F{i}']);after.setdefault(ix,[]).append(['ADD',n,f'Y{i}'])
  data.append({'packet':p,'field':field,'chart':states[cap][1][p],'old_row_hex':hex(r),'new_row_hex':hex(c),'mask_hex':hex(u),'donors':donors,'readers':readers,'owners':owners})
 new=[]
 for k,o in enumerate(ops):new.extend(before.get(k,[]));new.append(o);new.extend(after.get(k,[]))
 new.extend(['CLEAR',n]for d in data for n in d['owners'])
 w=copy.deepcopy(base);w.update(operations=new,schema='arbitrary-six-first-retention-v1',arbitrary_first_retentions=data,scope='Any six binary111 rows are actual first retentions in the stated M0/M1 fields with all46 old endpoints and all originals restored. All9 receiver repairs are paid. Source family only, no complete supplier.')
 return w,data

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--base',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 P=a.repo/'research/moonshot-005-program';e=load(P/'results/bit-leaf-capacity-quotient/author/check.py','arbitrary_engine')
 base=json.loads(a.base.read_text());R=json.loads((a.repo/base['source_path']).read_text())['native_roots'];C,H,br=e.replay(base,R)
 canonical=[(1<<i)^sum(1<<j for j in range(111)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(111)]
 chosen=[];desired=[]
 for i in range(111):
  if i not in base['targets'] and not e.fits(desired,canonical[i]):chosen.append(i);desired.append(canonical[i])
  if len(desired)==6:break
 w,data=build(base,desired);_,_,report=e.replay(w,R);states=trace(w);li=next(k for k,o in enumerate(w['operations'])if o[0]=='CLEAR');live,at=states[li]
 assert all(live[f]==c for f,c in zip(FIELDS,desired))
 extra=sum((1+len(d['readers']))*len(d['donors'])+len(d['readers'])for d in data)
 assert report['counts']=={k:z+{'INIT':9,'ADD':extra,'MOVE':9,'CLEAR':9}[k]for k,z in br['counts'].items()}
 prof=br['movement_profile'].copy();prof[1]+=9;assert report['movement_profile']==prof
 tests=[]
 for label,rows in [('all_zero',[0]*6),('all_ones',[(1<<111)-1]*6),('held_raw',[1<<i for i in [21,64,65,6,75,79]]),('equal_unfinished',[1<<5]*6)]:
  tw,_=build(base,rows);e.replay(tw,R);ts=trace(tw);ti=next(k for k,o in enumerate(tw['operations'])if o[0]=='CLEAR');assert all(ts[ti][0][f]==c for f,c in zip(FIELDS,rows));tests.append(label)
 controls=[]
 for d in data:
  n=d['owners'][0];i=d['readers'][0]
  for op in [['MOVE',n,f'F{i}'],['ADD',n,f'Y{i}'],['CLEAR',n]]:
   bad=copy.deepcopy(w);bad['operations'].remove(op)
   try:e.replay(bad,R)
   except(AssertionError,KeyError):controls.append({'omitted':op,'rejected':True})
   else:raise AssertionError(('accepted omission',op))
  if d['donors']:
   bad=copy.deepcopy(w);bad['operations'].remove(['ADD',d['donors'][0],n])
   try:e.replay(bad,R)
   except(AssertionError,KeyError):controls.append({'omitted':['ADD',d['donors'][0],n],'rejected':True})
   else:raise AssertionError('accepted incomplete repair recipe')
 a.out.mkdir(parents=True,exist_ok=True);raw=(json.dumps(w,indent=2)+'\n').encode();(a.out/'WORD.json').write_bytes(raw)
 result={'status':'PASS_ARBITRARY_SIX_FIRST_RETENTIONS','word_sha256':hashlib.sha256(raw).hexdigest(),'base_sha256':hashlib.sha256(a.base.read_bytes()).hexdigest(),'representative_canonical_roots':chosen,'canonical_rank':len(e.bb(desired)),'before':br,'after':report,'family_dimension_bits':666,'new_owners':9,'new_MOVEs':9,'new_ADDs':extra,'family_ADD_upper_bound':1674,'retentions':data,'boundary_controls':tests,'omission_controls':controls,'claim_scope':w['scope']}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','word_sha256','representative_canonical_roots','after','new_ADDs']}))
if __name__=='__main__':main()
