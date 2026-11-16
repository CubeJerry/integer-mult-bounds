"""Independent physical load-cut inventory and protected decoder controls."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json,sys
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();sys.path.insert(0,str(a.engine));from check import replay,rr,null,rank
w=json.loads(a.word.read_text());old=json.loads(a.base.read_text());R=json.loads((a.repo/w['source_path']).read_text())['native_roots'];C={n:rr(c['rows'])if c['kind']=='span'else null(c['rows'])for n,c in w['charts'].items()};assert hashlib.sha256(a.word.read_bytes()).hexdigest()=='204e38b8c56f17cc3e88a475d4c75e5613ed4215e29c6ede33e55a3e614a82b1'
v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};inventory=None
for step,o in enumerate(w['operations'],1):
 op,n,*q=o
 if op=='INIT':v[n]=0;at[n]=q[0]
 elif op=='MOVE':at[n]=q[0]
 elif op=='ADD':
  if o==['ADD','BACK2','P3']:
   assert v['BACK2']==v['P3']==sum(1<<i for i in [0,2,28,29]);assert C[at['BACK2']]==C['M1'];inventory={s:hex(z)for s,z in v.items()if s!='P3'and not(z>>111)and C[at[s]]==C['M1']};load_step=step
  v[q[0]]^=v[n]
 elif op=='CLEAR':del v[n];del at[n]
assert inventory and rank([int(x,16)for x in inventory.values()])==9
assert not any(o[0]=='ADD'and o[1]=='ZKEEP2'and o[2].startswith('Y')for o in w['operations'])
for i in range(111):assert[o for o in w['operations']if o[0]=='MOVE'and o[1]==f'X{i}']==[o for o in old['operations']if o[0]=='MOVE'and o[1]==f'X{i}']
controls=[]
for op in [['MOVE','BACK2','Jnew2'],['ADD','BACK2','Y2'],['MOVE','ZRAW0','zero']]:
 z=deepcopy(w);z['operations'].remove(op)
 try:replay(z,R,False)
 except (ValueError,AssertionError)as e:controls.append({'removed':op,'rejected':str(e)})
 else:raise AssertionError(('accepted invalid custody',op))
for op in [['ADD','BACK2','P3'],['ADD','Q1','P3']]:
 z=deepcopy(w);z['operations'].remove(op);replay(z,R,False);controls.append({'removed':op,'old_endpoints_preserved':True,'meaning':'Different payload; does not invalidate protected-decoder theorem.'})
out={'status':'PASS_INDEPENDENT_PORT41_LOAD_CUT_AND_PROTECTED_DECODER','word_sha256':hashlib.sha256(a.word.read_bytes()).hexdigest(),'load_cut_step':load_step,'actual_available_records':inventory,'actual_available_rank':9,'all_X_routes_unchanged':True,'old_Y_readers_of_new_payload':0,'controls':controls,'scope':'Universal binary-recipe theorem is the accompanying two-reset/copy proof, not an extrapolation from controls.'};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(controls),'controls')
