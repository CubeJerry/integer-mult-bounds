"""A's independent native/source/invoice review of C's canonical3 reset words."""
from pathlib import Path
import argparse, copy, hashlib, json, importlib.util
from collections import Counter
from build_d4_cohort import trace
from price_d4_cohort import moment, record
parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--work',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);args=parser.parse_args();REPO=args.repo.resolve();WORK=args.work.resolve();A=WORK/'A';CWORK=WORK/'C'
def key(p):
 p=p.resolve()
 try:return 'evidence/'+str(p.relative_to(WORK))
 except ValueError:return 'repo/'+str(p.relative_to(REPO))
def load(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def out(path,z):path.write_text(json.dumps(z,indent=2)+'\n')
ep=REPO/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py'
sp=importlib.util.spec_from_file_location('independent_native',ep);e=importlib.util.module_from_spec(sp);sp.loader.exec_module(e)
PINS={
 'liberated':(CWORK/'canonical3-reset-source/LIBERATED-CACHED48-WORD.json','dda004b1c3cae1c0d0cfb0d698c101963842db12d542fed842a82dbffc14ee44'),
 'matched':(CWORK/'canonical3-reset-source/MATCHED-CUT-WORD.json','60c6f8820eefe232ee6c8f5b348be21bd86bb42c13532054fc2548b784cd2da7'),
 'old_control':(CWORK/'canonical3-reset-control/OLD-CONTROL-WORD.json','7b3bb9579a8991bedfa5c9df1bcc08827b2bff055072924d170a48d04f9d279e'),
 'reset_control':(CWORK/'canonical3-reset-control/RESET-CONTROL-WORD.json','314efd9a2d01c4dc6b20c6dc76eb5cd12630c8a67accc3841063b8ebe9a973e2'),
 'ascending':(A/'ascending-canonical3/WORD.json','cc505aaf4aee5e1995b4db22f9b53609856d3ecdc3ea1eb0797f2584e375dfee')}
words={};cuts={};stats={};charts={};traces={}
for label,(p,pin) in PINS.items():
 assert sha(p)==pin,(label,'word pin');w=load(p);words[label]=w
 src=REPO/w['source_path'];assert sha(src)==w['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
 R=load(src)['native_roots'];ch,hi,st=e.replay(w,R);charts[label]=ch;stats[label]=st;traces[label]=trace(w['operations']);cuts[label]=traces[label][w['carrier_interface_before_operation']]
 stats[label]['moment']=record(moment(st['movement_profile']));stats[label]['word_sha256']=pin
S=sorted(set(words['ascending']['targets'])|{61,67});U=sorted(set(range(111))-set(S));sm=sum(1<<i for i in S);um=sum(1<<i for i in U)
assert len(S)==48 and len(U)==63
primary=[4,74,78];fields=['ZFIRST3','ZFIRST4','ZFIRST5'];groups={}
for i in U:
 g=tuple(a for a in primary if sum(x*y for x,y in zip(R[i],R[a]))==0);groups.setdefault(g,[]).append(i)
donors=sorted(i for g,ds in groups.items() if g for i in ds);assert len(donors)==57
originals={f'{p}{i}'for p in 'XY'for i in range(111)};source_reports={};source_controls=[]
for label in ['liberated','matched']:
 w=words[label];v,at=cuts[label];ch=charts[label];ops=w['operations'];cut=w['carrier_interface_before_operation'];tr=traces[label]
 assert w['targets']==S
 for i in S:
  name=f'CANONICAL_RESET_RAW_{i}';capture=ops.index(['ADD',f'X{i}',name]);assert tr[capture][0][f'X{i}']==1<<i and tr[capture][1][f'X{i}']==f'L{i}'
  assert ops[capture-1]==['INIT',name,f'L{i}'] and ops[capture+1]==['MOVE',name,'zero']
  assert v[name]==1<<i and at[name]=='zero'
 for i in donors:
  name=f'CANONICAL_NATIVE_RAW_{i}';capture=ops.index(['ADD',f'X{i}',name]);assert tr[capture][0][f'X{i}']==1<<i and tr[capture][1][f'X{i}']==f'L{i}'
  assert v[name]==1<<i and at[name]==f'L{i}' and not any(z[0]=='MOVE' and z[1]==name for z in ops)
 for g,ds in groups.items():
  if not g:continue
  name='ASC_GROUP_'+'_'.join(map(str,g));assert v[name]==sum(1<<i for i in ds)
  expect=e.chart({'kind':'ann','rows':[R[a]for a in g]});assert ch[at[name]]==expect
 for a,f in zip(primary,fields):
  expect=sum(1<<i for i in U if sum(x*y for x,y in zip(R[i],R[a]))==0)
  assert v[f]==expect and at[f]=='M1'
  k=ops.index(['MOVE',f,'M1']);assert tr[k][1][f]=='Hub' and len(ch['Hub'])-len(ch['M1'])==3
  for z in ops[:k]:
   if z[0]=='ADD' and z[2]==f:
    j=ops.index(z);assert tr[j][1][z[1]]=='Hub' and tr[j][0][z[1]]==1<<int(z[1][1:])
 assert len(e.bb(v[f]for f in fields))==3
 for i in range(111):assert v[f'X{i}']==1<<i
 native=[i for i in range(111)if at[f'X{i}']==f'L{i}'];assert native==w['released_carriers'];assert len(native)==(54 if label=='liberated'else 15)
 for i in range(111):
  assert v[f'Y{i}']==(1<<(111+i))^((1<<i)if i in S else 0)
  expected=f'F{i}'if i in (S if label=='liberated'else words['ascending']['targets'])else'zero';assert at[f'Y{i}']==expected
 owned=[z for n,z in v.items()if n not in originals];assert all(z>>111==0 for z in owned) and len(e.bb(owned))==105
 assert stats[label]['movement_profile']=={1:67,2:37,3:4,4:1,5:37,6:19,7:165}
 assert stats[label]['counts']=={'INIT':115 if label=='liberated'else 206,'ADD':306,'MOVE':330,'CLEAR':115 if label=='liberated'else 206}
 assert stats[label]['dirty_CLEAR']==115
 source_reports[label]={'cut':cut,'raw_native_originals':native,'pure_owned_rank':105,'actual_known_ground_captures':48,'actual_native_unknown_captures':57,'proper_group_count':7,'common_mode_count':3,'complete_targets_at_cut':48 if label=='liberated'else 46}
ov,oa=cuts['ascending'];mv,ma=cuts['matched'];ch=charts['matched'];checked=0
for n,z in ov.items():assert n in mv and (mv[n]^z)&~sm==0 and ch[ma[n]]==ch[oa[n]];checked+=1
assert checked==323
# Six independent source/lifetime omissions. Four preserve the partial endpoints
# and are rejected specifically because their actual cut-source contract changes.
lw=words['liberated'];lc=lw['carrier_interface_before_operation'];lv,la=cuts['liberated']
for label,event in [
 ('native_capture',['ADD','X5','CANONICAL_NATIVE_RAW_5']),
 ('group_input',['ADD','X5','ASC_GROUP_4_74_78']),
 ('Hub_mode_input',['ADD','X5','ZFIRST3']),
 ('common_descent',['MOVE','ZFIRST3','M1']),
 ('known_acquisition',['ADD','X0','CANONICAL_RESET_RAW_0']),
 ('owned_retirement',['CLEAR','ZFIRST3'])]:
 b=copy.deepcopy(lw);k=b['operations'].index(event);del b['operations'][k];bc=lc-(k<lc)
 try:e.replay(b,R)
 except(AssertionError,KeyError)as err:reason='native endpoint/ownership replay rejects'
 else:
  bv,ba=trace(b['operations'])[bc];assert bv!=lv or any(ch[ba[n]]!=ch[la[n]]for n in lv);reason='endpoints pass, actual cut-source identity rejects'
 source_controls.append({'omission':label,'outcome':reason})
# Audit the literal continuation without relying on C's reported block.
old=words['old_control'];new=words['reset_control'];oc=old['carrier_interface_before_operation'];nc=new['carrier_interface_before_operation']
extra_old=[['CLEAR',f'CANONICAL_RESET_RAW_{i}']for i in [0,61,67]];assert old['operations'][-3:]==extra_old
fixed=old['operations'][oc:-3];assert new['operations'][nc:nc+len(fixed)]==fixed
inverse_index=nc+len(fixed);assert new['operations'][inverse_index]==['ADD','X6','X27']
assert fixed[:6]==[['MOVE','X27','F4'],['ADD','ASC_GROUP_4','X27'],['ADD','H4_1','X27'],['MOVE','X27','Hub'],['ADD','ZRAW0','Y13'],['ADD','CANONICAL_RESET_RAW_0','Y13']]
assert fixed[-6:]==[['ADD',f'X{i}','X27']for i in [24,25,26,47,51,6]]
for i in [0,61,67]:
 n=f'CANONICAL_RESET_RAW_{i}';k=old['operations'].index(['ADD',f'X{i}',n]);assert old['operations'][k-1]==['INIT',n,f'L{i}']and old['operations'][k+1]==['MOVE',n,'zero'];assert traces['old_control'][k][0][f'X{i}']==1<<i
ov,oa=cuts['old_control'];nv,na=cuts['reset_control']
for n,z in ov.items():assert n in nv and (nv[n]^z)&~sm==0 and ch[na[n]]==ch[oa[n]]
assert ov['H4_1']==1<<6 and nv['H4_1']==0
assert ov['ASC_GROUP_4']==nv['ASC_GROUP_4']==sum(1<<i for i in [24,25,26,47,51])
bv,ba=traces['reset_control'][inverse_index];assert bv['X27']==(1<<27)^(1<<6) and ba['X27']==ba['X6']=='Hub'and bv['X6']==1<<6
preload=['ADD','CANONICAL_RESET_RAW_0','Y13'];pi=new['operations'].index(preload);assert pi==new['operations'].index(['MOVE','CANONICAL_RESET_RAW_0','zero'])+1 and pi<nc
control_reports=[]
for label,k,record_name,residual in [('ground_Y_preload',pi,'Y13',1<<0),('Hub_X_inverse',inverse_index,'X27',1<<6)]:
 bad=copy.deepcopy(new);del bad['operations'][k];v,at=trace(bad['operations'])[-1];errs={}
 for i in range(111):
  for name,expected in [(f'X{i}',1<<i),(f'Y{i}',(1<<(111+i))^((1<<i)if i in S else 0))]:
   if v[name]!=expected:errs[name]=v[name]^expected
 assert errs=={record_name:residual}
 try:e.replay(bad,R)
 except AssertionError:pass
 else:raise AssertionError('omitted repair accepted')
 control_reports.append({'omitted':label,'exact_isolated_residual':{record_name:hex(residual)}})
assert stats['old_control']['counts']=={'INIT':104,'ADD':652,'MOVE':429,'CLEAR':104}
assert stats['reset_control']['counts']=={'INIT':206,'ADD':318,'MOVE':331,'CLEAR':206}
gate={127:37,64:74,1:-74}
for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
lim=tuple(x/6 for x in moment(gate));q=moment(stats['liberated']['movement_profile']);direct=moment({7:222,1:48})
result={'status':'PASS_INDEPENDENT_CANONICAL3_RESET_SOURCE_AND_FIXED_CONTINUATION','native_source_sha256':sha(src),'independent_interpreter_sha256':sha(ep),'known_coordinates':S,'unknown_donors':donors,'source_reports':source_reports,'matched_old_named_records_checked':checked,'source_semantic_controls':source_controls,'fixed_literal_continuation_operations':len(fixed),'isolated_repair_controls':control_reports,'all_222_replays':stats,'complete_source_moment':record(q),'necessary_limiting_room':record((lim[0]-q[1],lim[1]-q[0])),'added_movement_over_raw48_direct':record((q[0]-direct[1],q[1]-direct[0])),'scope':'Two distinct actual source prefixes. Matched cut preserves every old named unknown-X/Y column and chart, requiring ground-known corrections and an actual invertible-X Hub inverse for a fixed continuation. Liberated source completes48 and holds54 originals native. No actual63-output decoder extension, no global foundation, no all111 supplier, no kappa.'}
DEST=args.out;DEST.mkdir(parents=True,exist_ok=True);out(DEST/'RESULT.json',result)
manifest={key(p):sha(p)for p,_ in PINS.values()};manifest.update({key(ep):sha(ep),key(src):sha(src),key(Path(__file__)):sha(Path(__file__)),key(CWORK/'CANONICAL3-RESET-SOURCE.md'):sha(CWORK/'CANONICAL3-RESET-SOURCE.md')});
for p in [A/'CANONICAL3-RESET-REVIEW.md',A/'build_d4_cohort.py',A/'price_d4_cohort.py',CWORK/'build_canonical3_reset_source.py',CWORK/'build_canonical3_reset_control.py']:manifest[key(p)]=sha(p)
manifest['evidence/A/canonical3-reset-review/RESULT.json']=sha(DEST/'RESULT.json');out(DEST/'MANIFEST.json',manifest)
print(result['status']);print('source moment',result['complete_source_moment']['decimal'][0]);print('matched named records',checked,'source controls',len(source_controls),'repair controls',len(control_reports))
