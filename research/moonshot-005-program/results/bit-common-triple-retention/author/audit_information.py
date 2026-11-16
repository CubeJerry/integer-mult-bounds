"""Exact actual-stock/history/point-feedback information audit for the new terminal source."""
from pathlib import Path
import argparse,hashlib,json
from source_loader import load
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();root=a.repo/'research/moonshot-005-program/results';e=load(root/'bit-composed-coded-source/author/retained/source_history_engine.py','e');raw=(a.out/'WORD.json').read_bytes();w=json.loads(raw);R=json.loads((a.repo/w['source_path']).read_text())['native_roots'];S=[int(x,16)for x in w['seed_rows_hex']];run=e.replay(w,R,S,15,False);v=run['cuts']['seed']['values'];at=run['cuts']['seed']['charts'];C=run['C'];mask=(1<<111)-1;rank=lambda rr:len(e.basis(rr));obs=run['snapshots'];rows=[]
dot=lambda i,j:sum(x*y for x,y in zip(R[i],R[j]))
for i in range(111):
 F=C[f'F{i}'];rr=[z for n,z in v.items()if not(z&~mask)and e.contained(C[at[n]],F)]
 rr +=[int(s['row_hex'],16)for s in obs if e.contained(C[s['chart']],F)]
 rr +=[1<<j for j in range(111)if not dot(i,j)]
 rows.append(rr)
known=set();waves=[]
while True:
 nxt={i for i,rr in enumerate(rows)if e.solve(rr+[1<<j for j in known],1<<i)is not None};assert known<=nxt
 if nxt==known:break
 waves.append(sorted(nxt-known));known=nxt
duals=[]
for i,rr in enumerate(rows):
 if i in known:continue
 rr=rr+[1<<j for j in known];eq=rr+[1<<i];cols=[sum(((z>>j)&1)<<k for k,z in enumerate(eq))for j in range(111)];d=e.solve(cols,1<<len(rr));assert d is not None and d>>i&1 and all((d&z).bit_count()%2==0 for z in rr);duals.append({'receiver':i,'dual_hex':hex(d)})
ground=[z for n,z in v.items()if at[n]=='zero'and not(z&~mask)];local={ch:sum(1<<j for j in range(111)if e.contained(C[f'L{j}'],C[ch]))for ch in set(at.values())};nn=[n for n,z in v.items()if at[n]not in ['zero','Hub']and not(z&~mask)and z&~local[at[n]]];norm=ground+[v[n]for n in nn]
assert rank(norm+[v[f'Y{i}']for i in range(111)])==rank(norm)+111
out={'status':'PASS_ACTUAL_FROZEN_INFORMATION_AUDIT','word_sha256':hashlib.sha256(raw).hexdigest(),'actual_targets':w['targets'],'common_rank':rank(ground),'proper_nonlocal_fields':[{'name':n,'chart':at[n],'row_hex':hex(v[n])}for n in nn],'normalized_rank':rank(norm),'all_Y_nuisance_independent':True,'principal_history_count':len(obs),'principal_history_rank':rank(int(s['row_hex'],16)for s in obs),'optimistic_closure':sorted(known),'feedback_waves':waves,'outsider_duals':duals,'scope':'Frozen word measurements plus optimistic raw geometric locals and free decoded-point feedback. New acquisition/recoding, paid communication, or terminal changes are outside the gate.'};(a.out/'CLOSURE.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],'closure',len(known),'newly admitted information',[i for i in known if i not in w['targets']],'duals',len(duals),'common',rank(ground))
