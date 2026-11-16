#!/usr/bin/env python3
"""Physical known-source reset control, with independent predecessor replay."""
import argparse,copy,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['repo','word','source-result','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();P=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(P/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from price import invoice
PIN='c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245'
assert hashlib.sha256(a.word.read_bytes()).hexdigest()==PIN
base=json.loads(a.word.read_bytes());br=json.loads(a.source_result.read_bytes());independent_replay(base)
cut=br['interface_index'];states,_=trace(base);v,at=states[cut]
is_original=lambda n:len(n)>1 and n[0]in'XY'and n[1:].isdigit()
owners={n:z for n,z in v.items()if not is_original(n)}
assert all(v[f'X{i}']==1<<i for i in range(111))
Sbits=0
for z in owners.values():Sbits|=z
for i in range(111):Sbits|=v[f'Y{i}']^(1<<(111+i))
assert Sbits>>111==0
S=[i for i in range(111)if Sbits>>i&1]
assert set(S)==set(base['targets'])|{61,67}and len(S)==48
prefix=copy.deepcopy(base['operations'][:cut]);prefix.remove(['MOVE','Y13','F13'])
assert [o for o in base['operations']if 'Y13'in o]==[['MOVE','Y13','F13']]
start_at=at.copy();start_at['Y13']='zero'
assert owners['CAP2942']==(1<<29)^(1<<42)and at['CAP2942']=='M1'
assert owners['P0']==1<<7 and at['P0']=='zero'
future=[['MOVE','X5','M1'],['ADD','CAP2942','X5'],['MOVE','X5','Hub']]
for i in range(111):
 if i!=5 and at[f'X{i}']!='Hub':future.append(['MOVE',f'X{i}','Hub'])
future += [['ADD','X29','X5'],['ADD','X42','X5'],['ADD','P0','Y13'],['MOVE','Y13','F13'],['INIT','S018_NEW','Hub'],['ADD','X13','S018_NEW'],['ADD','X7','S018_NEW'],['MOVE','S018_NEW','F13'],['ADD','S018_NEW','Y13'],['CLEAR','S018_NEW']]
future += [['CLEAR',n]for n in owners]
def word(ops,targets,kind):
 return {'schema':'known-source-cut-reset-control-v1','source_path':base['source_path'],'source_sha256':base['source_sha256'],'charts':base['charts'],'targets':targets,'operations':ops,'source_word_sha256':PIN,'kind':kind,'scope':'Physical proof control for cut reset; not a best endpoint-count frontier or complete supplier.'}
targets=sorted(base['targets']+[13]);old=word(prefix+future,targets,'old-source-continuation')
oldstats=independent_replay(old)
def run(vv,aa,ops):
 vv=vv.copy();aa=aa.copy()
 for op,n,*q in ops:
  if op=='INIT':assert n not in vv;vv[n]=0;aa[n]=q[0]
  elif op=='ADD':vv[q[0]]^=vv[n]
  elif op=='MOVE':aa[n]=q[0]
  elif op=='CLEAR':del vv[n],aa[n]
 return vv,aa
ov,oa=run(v,start_at,future)
zv={n:(z if n.startswith('X')and n[1:].isdigit()else (1<<(111+int(n[1:])))if n.startswith('Y')and n[1:].isdigit()else 0)for n,z in v.items()}
zf,za=run(zv,start_at,future)
D={i:zf[f'Y{i}']^ov[f'Y{i}']for i in range(111)}
assert all(d&~Sbits==0 for d in D.values())
M=[zf[f'X{i}']for i in range(111)];assert all(r>>111==0 for r in M)
assert M==[(1<<i)^((1<<29)^(1<<42)if i==5 else 0)for i in range(111)]
def inverse_ops(rows):
 rows=list(rows);ops=[]
 for j in range(len(rows)):
  pivot=next((k for k in range(j,len(rows))if rows[k]>>j&1),None)
  if pivot is None:raise ValueError('singular reset original map')
  if pivot!=j:
   for x,y in [(pivot,j),(j,pivot),(pivot,j)]:rows[y]^=rows[x];ops.append(['ADD',f'X{x}',f'X{y}'])
  for k in range(len(rows)):
   if k!=j and rows[k]>>j&1:rows[k]^=rows[j];ops.append(['ADD',f'X{j}',f'X{k}'])
 assert rows==[1<<i for i in range(len(rows))]
 return ops
inverse=inverse_ops(M);assert len(inverse)==2
init=[]
for s in S:init += [['INIT',f'RESET_RAW{s}',f'L{s}'],['ADD',f'X{s}',f'RESET_RAW{s}'],['MOVE',f'RESET_RAW{s}','zero']]
for i,d in D.items():
 for s in S:
  if d>>s&1:init.append(['ADD',f'RESET_RAW{s}',f'Y{i}'])
init += [['CLEAR',f'RESET_RAW{s}']for s in S]
for i in range(111):
 if at[f'X{i}']!=f'L{i}':init.append(['MOVE',f'X{i}',at[f'X{i}']])
for i in range(111):
 if start_at[f'Y{i}']!='zero':init.append(['MOVE',f'Y{i}',start_at[f'Y{i}']])
init += [['INIT',n,at[n]]for n in owners]
new=word(init+future+inverse,targets,'reset-source-continuation')
newstats=independent_replay(new)
controls=[]
for op in [['ADD','RESET_RAW7','Y13'],['ADD','X7','RESET_RAW7'],inverse[-1]]:
 bad=copy.deepcopy(new)
 if op in inverse:bad['operations']=bad['operations'][:-1]
 else:bad['operations'].remove(op)
 try:independent_replay(bad)
 except(AssertionError,KeyError,ValueError)as e:controls.append({'omitted':op,'rejected':True,'reason':str(e)})
 else:raise AssertionError(('accepted mutant',op))
# Separate actual singular-map fixture: old Hub owner restores a lost original.
sp=[['MOVE',f'X{i}','Hub']for i in range(111)]+[['MOVE',f'Y{i}',f'F{i}']for i in range(111)]+[['INIT','OLD_B','Hub'],['ADD','X0','OLD_B']]
sf=[['INIT','NEW_C','Hub'],['ADD','X0','NEW_C'],['ADD','NEW_C','X0'],['ADD','OLD_B','X0'],['CLEAR','NEW_C'],['CLEAR','OLD_B']]
sold=word(sp+sf,[],'singular-control-old');independent_replay(sold)
snew=word(sp[:-1]+sf,[],'singular-control-zero-source')
_,se=trace(snew);sm=[se[0][f'X{i}']for i in range(111)]
assert sm==[0]+[1<<i for i in range(1,111)]
try:inverse_ops(sm)
except ValueError:controls.append({'singular_original_map_rejected':True,'kernel_hex':'0x1','rank':110})
else:raise AssertionError('accepted singular original map')
try:independent_replay(snew)
except AssertionError:controls.append({'forced_singular_word_endpoint_rejected':True})
else:raise AssertionError('accepted singular physical endpoint')
a.out.mkdir(parents=True,exist_ok=True)
hashes={}
for name,w in [('OLD-WORD.json',old),('RESET-WORD.json',new)]:
 data=(json.dumps(w,indent=2)+'\n').encode();(a.out/name).write_bytes(data);hashes[name]=hashlib.sha256(data).hexdigest()
result={'status':'PASS_ACTUAL_KNOWN_SOURCE_CUT_RESET_CONTROL','source_word_sha256':PIN,'source_cut':cut,'known_coordinates':S,'known_count':len(S),'old_owned_count':len(owners),'raw_native_carriers':len(base['released_carriers']),'all_cut_owned_and_Y_offsets_supported_on_S':True,'owned_source_support_rows':{n:hex(z)for n,z in owners.items()},'preloads':{str(i):hex(d)for i,d in D.items()if d},'reset_original_matrix_rows_hex':[hex(r)for r in M],'actual_Hub_inverse':inverse,'old_stats':oldstats,'reset_stats':newstats,'old_price':invoice(oldstats['movement_profile']),'reset_price':invoice(newstats['movement_profile']),'direct48_reference_price':invoice({7:222,1:48}),'words':hashes,'negative_controls':controls,'scope':'Actual47-output proof controls and source audit. General reduction rests on the written proof, not enumeration. All222 columns and actual geometry/lifetimes/prices checked; no all111 supplier or exponent.'}
(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status']);print(json.dumps({'old_stats':oldstats,'reset_stats':newstats,'inverse':inverse,'words':hashes,'reset_Q':result['reset_price']['moment']['lower']},indent=2))
