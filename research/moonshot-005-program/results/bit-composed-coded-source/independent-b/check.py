from pathlib import Path
import argparse,json,hashlib
from collections import Counter
from own_engine import replay,chart
p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'output');a=p.parse_args();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(a.base)=='204e38b8c56f17cc3e88a475d4c75e5613ed4215e29c6ede33e55a3e614a82b1'
b=json.loads(a.base.read_text());w=json.loads(a.word.read_text());br=replay(b);wr=replay(w);g=int(w['cross_bank_coupling']['transported_row_hex'],16)
assert wr['p7']==br['p7']and wr['xevents']==br['xevents'];assert wr['moves']==br['moves']and wr['dirty']==br['dirty']
assert wr['counts']=={k:v+(3 if k=='ADD'else 0)for k,v in br['counts'].items()};assert wr['counts']=={'INIT':115,'ADD':908,'MOVE':436,'CLEAR':115};assert wr['peak']==br['peak']==115
bv,bp=br['cuts']['seed'];wv,wp=wr['cuts']['seed'];assert set(bv)==set(wv)and bp==wp;assert {n:wv[n]^bv[n]for n in wv if wv[n]!=bv[n]}=={'KEEP_C0':g};assert wr['cuts']['source']==br['cuts']['source']
assert Counter(map(tuple,w['operations']))==Counter(map(tuple,b['operations']))+Counter({('ADD','HKEEP_D7','P0'):1,('ADD','HKEEP_D7','Y3'):1,('ADD','HKEEP_D7','Y21'):1})
def inventory(z):
 C={n:chart(s)for n,s in z['charts'].items()};v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};at={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)}
 for o in z['operations']:
  if o[0]=='INIT':v[o[1]]=0;at[o[1]]=o[2]
  elif o[0]=='MOVE':at[o[1]]=o[2]
  elif o[0]=='CLEAR':del v[o[1]];del at[o[1]]
  else:
   assert o[0]=='ADD';v[o[2]]^=v[o[1]]
   if o==['ADD','BACK2','P3']:
    assert v['P3']==0;return {n:hex(r)for n,r in v.items()if n!='P3'and r>>111==0 and C[at[n]]==C['M1']}
 raise AssertionError('no source reset')
ib,iw=inventory(b),inventory(w);assert ib==iw and 'Q1'in iw and 'BACK2'in iw
assert wv['ZKEEP2']==int(iw['Q1'],16)and wp['ZKEEP2']=='L41';assert wp['ZRAW0']=='zero'and wv['ZRAW0']==1
assert int(iw['BACK2'],16)==(1<<0)^(1<<2)^(1<<28)^(1<<29)
assert(g>>24&1)==0 and(g>>42&1)==(g>>69&1)
r={'status':'PASS_INDEPENDENT_COMPOSED_FULL222_AND_M1_INVENTORY','base_port41_word_sha256':sha(a.base),'composed_word_sha256':sha(a.word),'counts':wr['counts'],'profile':wr['moves'],'peak_owned':wr['peak'],'dirty_CLEAR':wr['dirty'],'all_columns':222,'same34targets':w['targets'],'sourcecut_unchanged_from_port41':True,'P7_observations_and_original_X_mutations_unchanged':True,'seed_only_KEEP_C0_change_hex':hex(g),'same_actual_M1_recipe_inventory':iw,'ZKEEP2_is_actual_Q1_at_L41':True,'BACK2_is_old_h_at_Jnew2':wp['BACK2']=='Jnew2','ground_helper_is_paid_raw_X0':True,'coarse_duals_not_removed':True,'no_new_kappa':True};a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k]for k in['status','composed_word_sha256','counts','profile','same_actual_M1_recipe_inventory']}))
