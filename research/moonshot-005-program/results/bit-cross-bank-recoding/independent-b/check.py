#!/usr/bin/env python3
"""Independent full-column exact replay of the three-ADD P7/P0 coupling."""
from pathlib import Path
from sympy import Matrix
from collections import Counter
from functools import lru_cache
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(a.base)=='46e299557269f8f78aedd9e049a2db020b22e64c6e7df59101a8c61cca05224e';assert sha(a.word)=='f17fb4bb7cc9dbe2c3a1725f1b24586b0e97262b98c7e2cff07e25df35ad35a5'
w0=json.loads(a.base.read_text());w=json.loads(a.word.read_text());src=a.repo/w['source_path'];assert sha(src)==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(src.read_text())['native_roots']
@lru_cache(None)
def rowbasis(rows):
 m=Matrix(rows)if rows else Matrix.zeros(0,8);r,p=m.rref();return tuple(tuple(r[i,j]for j in range(8))for i in range(len(p)))
def chart(s):
 rows=tuple(tuple(r)for r in s['rows'])
 if s['kind']=='span':return rowbasis(rows)
 assert s['kind']=='ann';ns=Matrix(rows).nullspace();return rowbasis(tuple(tuple(v)for v in ns))
@lru_cache(None)
def sub(A,B):return len(rowbasis(A+B))==len(B)
def replay(z,metadata=True):
 C={n:chart(s)for n,s in z['charts'].items()};v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};own=set();born=set();counts=Counter();moves=Counter();dirty=0;peak=0;cuts={};p7=[];newreads=[];xevents=[]
 for step,o in enumerate(z['operations'],1):
  counts[o[0]]+=1
  if o[0]=='INIT':
   _,n,c=o;assert n not in v and n not in born;v[n]=0;at[n]=c;own.add(n);born.add(n)
  elif o[0]=='ADD':
   _,s,t=o;assert C[at[s]]==C[at[t]],(step,o,'colocation')
   if t=='P7':p7.append((s,v[s],at[s]))
   if s=='HKEEP_D7'and t in ['P0','Y3','Y21']:newreads.append((step,t,v[s],at[s],at[t]))
   v[t]^=v[s]
  elif o[0]=='MOVE':
   _,n,c=o;old=at[n];assert sub(C[c],C[old])if n in own else sub(C[old],C[c]),(step,o,'direction');dist=abs(len(C[c])-len(C[old]));assert dist>0;moves[dist]+=1;at[n]=c
  elif o[0]=='CLEAR':
   _,n=o;assert n in own;dirty+=bool(v[n]);own.remove(n);del v[n];del at[n]
  else:raise AssertionError(o)
  peak=max(peak,len(own))
  if (o[0]=='MOVE'and o[1].startswith('X'))or(o[0]=='ADD'and o[2].startswith('X')):xevents.append((tuple(o),tuple((n,v[n],at[n])for n in o[1:]if n.startswith('X'))))
  if metadata and step in[z['milestones']['source_cut'],z['milestones']['seed8_before_Y']]:cuts['source'if step==z['milestones']['source_cut']else'seed']=(v.copy(),at.copy())
 for i in range(111):
  assert v[f'X{i}']==1<<i and at[f'X{i}']=='Hub'
  assert v[f'Y{i}']==((1<<(111+i))^((1<<i)if i in z['targets']else 0))and at[f'Y{i}']==f'F{i}'
 assert not own and len(v)==222
 return {'cuts':cuts,'p7':p7,'newreads':newreads,'xevents':xevents,'counts':dict(counts),'moves':dict(sorted(moves.items())),'dirty':dirty,'peak':peak}
b=replay(w0);n=replay(w);g=int(w['cross_bank_coupling']['transported_row_hex'],16)
extra=[['ADD','HKEEP_D7',t]for t in ['P0','Y3','Y21']]
assert Counter(map(tuple,w['operations']))==Counter(map(tuple,w0['operations']))+Counter(map(tuple,extra))
keep_step=w['operations'].index(['ADD','P7','HKEEP_D7'])+1
assert keep_step<n['newreads'][0][0]
assert n['p7']==b['p7']and n['xevents']==b['xevents']and n['cuts']['source']==b['cuts']['source'];assert n['moves']==b['moves']and n['dirty']==b['dirty']
assert n['peak']==b['peak']==114
assert[o[2]for o in w['operations']if o[:2]==['ADD','KEEP_C0']]==['P0','Y3','Y21']
assert n['counts']=={k:v+(3 if k=='ADD'else 0)for k,v in b['counts'].items()}
sv,sp=n['cuts']['seed'];bv,bp=b['cuts']['seed'];assert set(sv)==set(bv)and sp==bp;diff={name:sv[name]^bv[name]for name in sv if sv[name]!=bv[name]};assert diff=={'KEEP_C0':g}
assert sv['HKEEP_D7']==g and sp['HKEEP_D7']=='D3_21';assert len(n['newreads'])==3 and [x[1]for x in n['newreads']]==['P0','Y3','Y21'];assert all(x[2]==g and x[3]==x[4]=='D3_21'for x in n['newreads'])
assert all(sv[f'P{i}']==bv[f'P{i}']for i in range(8));assert all(sv[name]==bv[name]for name in sv if sp[name]=='zero')
assert (g>>42&1)==(g>>69&1)and(g>>24&1)==0
negative=[]
for target in ['P0','Y3','Y21']:
 z=dict(w);z['operations']=list(w['operations']);z['operations'].remove(['ADD','HKEEP_D7',target])
 try:replay(z,False)
 except AssertionError:negative.append(target)
 else:raise AssertionError(('deletion accepted',target))
z=dict(w0);z['operations']=[]
for o in w0['operations']:
 z['operations'].append(o)
 if o in [['MOVE',t,'D3_21']for t in ['P0','Y3','Y21']]:z['operations'].append(['ADD','HKEEP_D7',o[1]])
try:replay(z,False)
except AssertionError:negative.append('three_reads_without_P7_retiming')
else:raise AssertionError('unretimed word accepted')
result={'status':'PASS_INDEPENDENT_FULL222_CROSS_BANK_COUPLING','base_word_sha256':sha(a.base),'word_sha256':sha(a.word),'native_source_sha256':sha(src),'all_columns':222,'endpoints_preserved':w['targets'],'counts':n['counts'],'movement_profile':n['moves'],'dirty_clear':n['dirty'],'extra_ADD':3,'extra_MOVE':0,'new_owners':0,'P7_source_observations_unchanged':True,'all_original_X_trajectories_and_values_unchanged':True,'source_cut_identical':True,'seed_change_only_KEEP_C0_hex':hex(g),'seed_locations_identical':True,'ground_and_other_retentions_identical':True,'three_actual_reads':n['newreads'],'deletion_controls_fail':negative,'coarse42_69_dual_still_annihilates_g':True,'scope':'Actual arbitrary-input source coupling and full-column chronology; no new endpoints, canonical completion, supplier, or kappa. No author replay imported.','new_kappa':False};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in['status','counts','movement_profile','extra_ADD','extra_MOVE','seed_change_only_KEEP_C0_hex','deletion_controls_fail']}))
