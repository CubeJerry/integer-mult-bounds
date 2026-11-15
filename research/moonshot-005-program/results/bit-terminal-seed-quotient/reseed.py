#!/usr/bin/env python3
"""Reseed fixed serial template; no complete decoder claimed."""
import argparse,copy,hashlib,json
from pathlib import Path
def basis(rows):
 b={}
 for x in rows:
  while x:
   k=(x&-x).bit_length()-1
   if k in b:x^=b[k]
   else:b[k]=x;break
 return list(b.values())
def rank(rows):return len(basis(rows))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def replay(w):
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};H=[];T={};counts={}
 for step,o in enumerate(w['operations']):
  k,a,*rest=o;counts[k]=counts.get(k,0)+1
  if k=='INIT':assert a not in v;v[a]=0;loc[a]=rest[0]
  elif k=='ADD':
   b=rest[0];assert loc[a]==loc[b];v[b]^=v[a]
   if a.startswith('X')and b.startswith('P')and b[1:].isdigit():assert loc[a]=='Hub'and v[a]==1<<int(a[1:])
  elif k=='MOVE':loc[a]=rest[0]
  elif k=='CLEAR':assert not(a.startswith('X')or(a.startswith('Y')and a[1:].isdigit()));del v[a];del loc[a]
  for p in [f'P{i}'for i in range(8)]:
   if p in v and loc[p]!='Hub':H.append((p,v[p]))
  if step+1==w['markers']['handoff']:T={p:v[p]for p in[f'P{i}'for i in range(8)]}
 for i in range(111):
  assert v[f'X{i}']==1<<i and loc[f'X{i}']=='Hub'
  assert v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in w['completed_targets']else 0)
 return H,T,counts

def change(w,targets):
 w=copy.deepcopy(w);modes=[int(x,16)for x in w['proper_mode_rows_hex']]+[0];seeds=[int(x,16)for x in w['initial_seed_rows_hex']];free=[i for i in range(8)if i!=4]
 for i in free:seeds[i]=targets[i]^modes[i]
 old=w['operations'];new=[];mp={};i=0
 while i<len(old):
  mp[i]=len(new);o=old[i]
  if o[0]=='INIT'and o[1]in[f'P{j}'for j in free]:
   name=o[1];j=int(name[1:]);new.append(o);i+=1
   while i<len(old)and old[i][0]=='ADD'and old[i][2]==name and old[i][1].startswith('X'):mp[i]=len(new);i+=1
   for k in range(111):
    if seeds[j]>>k&1:new.append(['ADD',f'X{k}',name])
   continue
  new.append(o);i+=1
 mp[len(old)]=len(new);w['operations']=new;w['markers']={k:mp[v]for k,v in w['markers'].items()};w['exchange']={k:(mp[v]if k.endswith('_index')and v is not None else v)for k,v in w['exchange'].items()};w['initial_seed_rows_hex']=[hex(x)for x in seeds];w['initial_seed_fitting_roles']=[None]*8
 for i,t in enumerate(targets):w['expected_owned_at_handoff'][f'P{i}']['value_hex']=hex(t)
 w['schema']='canonical-aligned-serial-point-source-v1';w['reseed_scope']='Same movements/chronology, seven changed Hub seed rows, W15 history retained.'
 return w
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(exist_ok=True,parents=True)
 raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';roots=json.loads(raw)['native_roots'];h=[(dot(roots[72],x)//2+dot([0,0,1,1,0,0,1,-1],x)//2)%2 for x in roots];hm=sum(x<<i for i,x in enumerate(h));allx=(1<<111)-1
 C=[sum((i==j or dot(x,y)==0)<<j for j,y in enumerate(roots))for i,x in enumerate(roots)];W=[x&(hm if h[i]else allx^hm)for i,x in enumerate(C)]
 src=json.loads((a.source/'WORD.json').read_text());hist,oldterminal,_=replay(src);D=basis([v^(oldterminal[p]if p!='P4'else 0)for p,v in hist]);N=[oldterminal['P4']];assert N==[1<<9]and rank(D+N)==len(D)
 chosen=[];B=list(D)
 for i,c in enumerate(C):
  if h[i]==0 and rank(B+[c])>len(B):B=basis(B+[c]);chosen.append(('canonical',i,c))
 assert len(chosen)==5
 for i,w in enumerate(W):
  if rank(B+[w])>len(B):B=basis(B+[w]);chosen.append(('W',i,w))
 assert len(chosen)==7 and rank(B+W)==len(B)
 it=iter(chosen);targets=[N[0]if i==4 else next(it)[2]for i in range(8)]
 report={'status':'PASS_ROOT_CANONICAL_ALIGNED_SEED_SPACE','source_sha256':{f:hashlib.sha256((a.source/f).read_bytes()).hexdigest()for f in['WORD.json','CLOSED-WORD.json']},'new_complete_kappa':False,'D_basis_hex':[hex(x)for x in D],'D_rank':len(D),'D_intersection_W':len(D)+15-rank(D+W),'D_intersection_C':len(D)+9-rank(D+C),'D_plus_C_intersection_W':rank(D+C)+15-rank(D+C+W),'N_intersection_C':rank(N)+9-rank(N+C),'chosen_terminals':[{'kind':k,'role':i,'row_hex':hex(v)}for k,i,v in chosen],'variants':{}}
 for name in ['WORD.json','CLOSED-WORD.json']:
  old=json.loads((a.source/name).read_text());w=change(old,targets);hh,tt,counts=replay(w);T=list(tt.values());H=[v for _,v in hh]
  assert rank(T)==8 and rank(T)+9-rank(T+C)==5 and rank(H+W)==rank(H)
  assert [o for o in old['operations']if o[0]!='ADD']==[o for o in w['operations']if o[0]!='ADD']
  assert rank(D+T)==rank(H)==rank(D+T+H)
  fits=[]
  for i,r in enumerate(roots):
   outside=sum((dot(r,s)!=0)<<j for j,s in enumerate(roots))
   if rank([v&outside for v in T]+[1<<i])==rank([v&outside for v in T]):fits.append(i)
  (a.out/name).write_text(json.dumps(w,indent=2,sort_keys=True)+'\n')
  report['variants'][name]={'counts':counts,'history_rank':rank(H),'W_intersection':rank(H)+15-rank(H+W),'terminal_rank':rank(T),'terminal_C_intersection':5,'terminal_W_intersection':rank(T)+15-rank(T+W),'canonical_extension_dimension':4,'terminal_fitting_roles_under_free_local_corrections':fits,'nonADD_operations_unchanged':True,'actual_completed_targets':w['completed_targets']}
 (a.out/'RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='D_basis_hex'},sort_keys=True))
if __name__=='__main__':main()
