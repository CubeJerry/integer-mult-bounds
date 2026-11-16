from pathlib import Path
import json,copy,importlib.util,hashlib
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
repo=args.repo;P=repo/'research/moonshot-005-program';out=args.out;out.mkdir(parents=True,exist_ok=True)
def load(path,name):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
e=load(P/'results/bit-leaf-capacity-quotient/author/check.py','engine')
base=P/'results/bit-canonical-mask-source/author/early-paid46/WORD.json';w=json.loads(base.read_text());ops=w['operations'];R=json.loads((repo/w['source_path']).read_text())['native_roots'];C,_,before=e.replay(w,R)
def trace(operations):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(i+111)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};out=[]
 for o in operations:
  out.append((v.copy(),at.copy()));op,n,*q=o
  if op=='INIT':v[n]=0;at[n]=q[0]
  elif op=='MOVE':at[n]=q[0]
  elif op=='ADD':v[q[0]]^=v[n]
  elif op=='CLEAR':del v[n],at[n]
 out.append((v,at));return out
states=trace(ops)
cut=next(i for i,o in enumerate(ops)if o[0]=='ADD' and o[2]=='P0')
v,at=states[cut];held={f'X{i}':at[f'X{i}']for i in range(111)if C[at[f'X{i}']]!=C['Hub'] or v[f'X{i}']!=1<<i}
assert all((o[0]=='MOVE'and o[2]=='Hub')or o[0]!='MOVE' for o in ops[cut:]if o[1] in held)
retime=[(k,o)for k,o in enumerate(ops)if k>=cut and ((o[0]=='MOVE'and o[1]in held)or(o[0]=='ADD'and o[2].startswith('X')))]
assert all(o[2]in held for k,o in retime if o[0]=='ADD'),(cut,held,retime)
needed={o[1] for k,o in enumerate(ops) if k>=cut and k not in {j for j,_ in retime} and o[0]=='ADD' and o[1] in held and (C[states[k][1][o[1]]]!=C['Hub'] or states[k][0][o[1]]!=(1<<int(o[1][1:]))) }
snapshot={n:ch for n,ch in held.items() if n in needed}
seq=[]
for n,ch in snapshot.items():seq.extend([['INIT','RELEASE_'+n,ch],['ADD',n,'RELEASE_'+n]])
seq.extend(o for _,o in retime if o[0]=='MOVE');seq.extend(o for _,o in retime if o[0]=='ADD')
ss=trace(ops[:cut]+seq)[-1]
assert all(ss[0][f'X{i}']==1<<i and ss[1][f'X{i}']=='Hub'for i in range(111))
removed={k for k,o in retime};newops=ops[:cut]+seq;redirect=[]
for k in range(cut,len(ops)):
 if k in removed:continue
 o=ops[k].copy()
 if o[0]=='ADD' and o[1]in held and (C[states[k][1][o[1]]]!=C['Hub'] or states[k][0][o[1]]!=(1<<int(o[1][1:]))):
  assert states[k][0][o[1]]==v[o[1]]
  redirect.append({'old_index':k,'old_operation':o.copy(),'snapshot':'RELEASE_'+o[1]});o[1]='RELEASE_'+o[1]
 newops.append(o)
newops.extend(['CLEAR','RELEASE_'+n]for n in snapshot)
nw=copy.deepcopy(w);nw.update(operations=newops,schema='stationary-snapshot-complete-Hub-release-v1',base_word_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),early_release={'cut':cut,'held':held,'redirected_readers':redirect,'all_Hub_loads_raw111':True},scope='Source scheduling changes actual Hub availability to all111 raw originals before every principal P0-P5 load; same46 endpoints, unchanged MOVE multiset, paid stationary snapshots. Partial source, no complete supplier.')
C,H,after=e.replay(nw,R)
ns=trace(newops);cuts=[]
for packet in ['P0','P1','P2','P3','P4','P5']:
 ix=next(i for i,o in enumerate(newops)if o[0]=='ADD' and o[2]==packet and ns[i][1][packet]=='Hub');vv,aa=ns[ix]
 assert all(vv[f'X{i}']==1<<i and aa[f'X{i}']=='Hub'for i in range(111));cuts.append({'packet':packet,'actual_index':ix,'raw_rank':111})
assert before['movement_profile']==after['movement_profile']
assert after['counts']=={k:z+{'INIT':len(snapshot),'ADD':len(snapshot),'MOVE':0,'CLEAR':len(snapshot)}[k]for k,z in before['counts'].items()}
blob=(json.dumps(nw,indent=2)+'\n').encode();(out/'WORD.json').write_bytes(blob)
result={'status':'PASS_LITERAL_FULL111_HUB_SOURCE_RELEASE','base_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),'word_sha256':hashlib.sha256(blob).hexdigest(),'before':before,'after':after,'old_cut':cut,'held':held,'snapshots':snapshot,'retimed_operations':retime,'redirected_readers':redirect,'actual_Hub_cuts':cuts,'claim_scope':nw['scope']};(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','word_sha256','after','actual_Hub_cuts']}))
