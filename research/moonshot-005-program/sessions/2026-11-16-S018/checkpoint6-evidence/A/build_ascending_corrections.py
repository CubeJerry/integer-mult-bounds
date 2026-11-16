"""Six restored original carriers fan out three actual shared correction groups."""
import argparse,copy,hashlib,importlib.util,json
from collections import defaultdict
from pathlib import Path
PIN='c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245'
PRIMARIES=[4,74,78]
ASSIGN=[(0,(4,74),4),(2,(4,74),74),(7,(4,78),4),(28,(4,78),78),(44,(74,78),74),(50,(74,78),78)]
BACKUP={0:'ZRAW0',2:'COMMON_RAW2',7:'P0',28:'ZRAW28',44:'ZRAW44',50:'ADDED_RAW50'}
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def write(p,obj):
 raw=(json.dumps(obj,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def lab(group):return 'ASC_GROUP_'+'_'.join(map(str,group))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--word',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/work-S018/A/pruned78/WORD.json'));ap.add_argument('--out',type=Path,required=True);ap.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));ap.add_argument('--mask',default=None);a=ap.parse_args();raw=a.word.read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;w=json.loads(raw);sr=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(sr).hexdigest()==w['source_sha256'];R=json.loads(sr)['native_roots'];e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','ascending_engine');t=load(Path(__file__).with_name('build_d4_cohort.py'),'ascending_trace');pr=load(Path(__file__).with_name('price_d4_cohort.py'),'ascending_price');C,_,before=e.replay(w,R);bt=t.trace(w['operations']);oldcut=w['carrier_interface_before_operation'];charts=copy.deepcopy(w['charts']);U=set(w['released_carriers'])-set(w['targets']);assert len(U)==63;groups=defaultdict(list)
 for i in sorted(U):groups[tuple(k for k in PRIMARIES if sum(x*y for x,y in zip(R[k],R[i]))==0)].append(i)
 donor=set(i for g,v in groups.items()if g for i in v);assert len(donor)==57;dm=sum(1<<i for i in donor);chosen=dm if a.mask is None else int(a.mask,0);assert chosen&~dm==0;donor_names={f'X{i}'for i in donor};carriers={x[0]for x in ASSIGN};carrier_names={f'X{i}'for i in carriers};assert not any(o[0]=='ADD'and(o[1]in donor_names or o[2]in donor_names|carrier_names)for o in w['operations']);protected={}
 for i in carriers:
  reads=[k for k,o in enumerate(w['operations'])if o[0]=='ADD'and o[1]==f'X{i}'];assert len(reads)==1;protected[i]=reads[0];assert bt[reads[0]][0][f'X{i}']==1<<i
 packets=['P3','P4','P5'];fields=['ZFIRST3','ZFIRST4','ZFIRST5'];resets={p:w['operations'].index(['ADD',f,p])for p,f in zip(packets,fields)}
 for p,f,aa in zip(packets,fields,PRIMARIES):
  assert[o for o in w['operations'][:resets[p]]if o[0]=='ADD'and o[1]==p]==[['ADD',p,f]]
  assert[o[2]for o in w['operations']if o[0]=='ADD'and o[1]==f and o[2]!=p]==[f'Y{aa}']
 ops=[];owners=[];captures=[]
 def add(*rows):ops.extend([list(o)for o in rows])
 for g,inputs in sorted(groups.items()):
  if not g:continue
  name=lab(g);charts[name]={'kind':'ann','rows':[R[k]for k in g]};Z=e.chart(charts[name]);assert len(Z)==8-len(g);assert e.sub(C['M1'],Z);owners.append(name);add(('INIT',name,name))
  for i in inputs:
   assert e.sub(C[f'L{i}'],Z);add(('MOVE',f'X{i}',name))
   if chosen>>i&1:captures.append(len(ops));add(('ADD',f'X{i}',name))
   add(('MOVE',f'X{i}','Hub'))
 prelude=len(ops);mapping={};cut=None;loads=[];precoats=[];carrier_reads=[];restores=[];couplings=[];pending_y=[]
 for k,o in enumerate(w['operations']):
  if k==oldcut:cut=len(ops)
  typ,n,*q=o
  if typ=='MOVE'and n.startswith('Y')and int(n[1:])not in w['targets']:pending_y.append(o);mapping[k]=len(ops);continue
  if typ=='MOVE'and n in donor_names|carrier_names:mapping[k]=len(ops);continue
  if typ=='MOVE'and n in{f'Y{i}'for i in PRIMARIES}and bt[k][1][n]=='zero':
   aa=int(n[1:])
   for c,g,b in ASSIGN:
    if b==aa:
     assert bt[k][0][BACKUP[c]]==1<<c and len(C[bt[k][1][BACKUP[c]]])==0;precoats.append(len(ops));add(('ADD',BACKUP[c],n))
  if typ=='MOVE'and n in packets and bt[k][1][n]=='Hub':
   aa=PRIMARIES[packets.index(n)]
   for g,inputs in groups.items():
    if aa in g:
     for i in inputs:
      if chosen>>i&1:loads.append(len(ops));add(('ADD',f'X{i}',n))
  add(o)
  for c,g,aa in ASSIGN:
   if k==protected[c]:
    name=lab(g);assert e.sub(C[f'L{c}'],e.chart(charts[name]));add(('MOVE',f'X{c}',name));couplings.append(len(ops));add(('ADD',name,f'X{c}'),('MOVE',f'X{c}',f'F{aa}'))
  if typ=='MOVE'and n in{f'Y{i}'for i in PRIMARIES}and q[0]=='M1':add(('ADD',lab(tuple(PRIMARIES)),n))
  if typ=='MOVE'and n in{f'Y{i}'for i in PRIMARIES}and q[0]==f'F{n[1:]}':
   aa=int(n[1:]);add(('ADD',lab((aa,)),n))
   for c,g,b in ASSIGN:
    if b==aa:
     carrier_reads.append(len(ops));add(('ADD',f'X{c}',n),('MOVE',f'X{c}','Hub'))
     for i in groups[g]:
      if chosen>>i&1:restores.append(len(ops));add(('ADD',f'X{i}',f'X{c}'))
  mapping[k]=len(ops)
 assert cut is not None;add(*pending_y,*[('CLEAR',n)for n in owners]);nw=copy.deepcopy(w);nw.update(schema='ascending-original-shared-correction-canonical-quotient-v1',base_word_sha256=PIN,charts=charts,operations=ops,carrier_interface_before_operation=cut,released_carriers=sorted(set(w['released_carriers'])-donor-carriers),ascending_corrections={'primaries':PRIMARIES,'assignment':[list(x[:1])+[list(x[1]),x[2]]for x in ASSIGN],'ground_backups':BACKUP,'groups':{'_'.join(map(str,g)):v for g,v in groups.items()},'allowed_mask_hex':hex(dm),'chosen_mask_hex':hex(chosen),'parameter_count':len(donor),'prelude_end':prelude,'raw_group_capture_indices':captures,'packet_load_indices':loads,'ground_precoat_indices':precoats,'carrier_coupling_indices':couplings,'carrier_reader_indices':carrier_reads,'carrier_restore_indices':restores,'continuation_before_operation':cut},scope='Same46 outputs; three dense canonical unknown-coordinate projections are retained at M1. Six backed original records ascend actual shared pair corrections to three receiver facets, with ground nuisance cancellation and explicit final Hub restoration. No added owned MOVE. Binary57-parameter weighted-column family; canonical quotient statement is for the all-one mask. No all111 supplier or kappa.')
 CC,_,after=e.replay(nw,R);nt=t.trace(ops);v,at=nt[cut];ov,oa=bt[oldcut];S=set(w['targets'])|{61,67};sm=sum(1<<i for i in S);unknown_mask=((1<<111)-1)^sm;mode_records=[]
 for aa,f in zip(PRIMARIES,fields):
  K=(1<<aa)^sum(1<<i for i in range(111)if sum(x*y for x,y in zip(R[aa],R[i]))==0);u=K&chosen;assert v[f]==ov[f]^u and CC[at[f]]==CC['M1'];assert ov[f]&unknown_mask==0
  if chosen==dm:assert (v[f]^K)&unknown_mask==0
  mode_records.append({'primary':aa,'field':f,'chart':at[f],'canonical_row_hex':hex(K),'known_old_offset_hex':hex(ov[f]),'actual_row_hex':hex(v[f]),'unknown_projection_hex':hex(v[f]&unknown_mask)})
 for c,g,aa in ASSIGN:
  u=sum(1<<i for i in groups[g]if chosen>>i&1);assert v[f'X{c}']==1<<c and at[f'X{c}']=='Hub'
  read=next(k for k in carrier_reads if ops[k][1]==f'X{c}');vv,loc=nt[read];assert vv[f'X{c}']==(1<<c)^u and loc[f'X{c}']==f'F{aa}'
 for i in range(111):
  assert v[f'X{i}']==1<<i
  if i in nw['released_carriers']:assert at[f'X{i}']==f'L{i}'
  if i not in w['targets']:assert v[f'Y{i}']==1<<(111+i)and at[f'Y{i}']=='zero'
 for g,inputs in groups.items():
  if g:assert v[lab(g)]==sum(1<<i for i in inputs if chosen>>i&1)
 comp=0
 for k,o in enumerate(w['operations']):
  if k>=oldcut:break
  oldv,oldat=bt[k+1];vv,aa=nt[mapping[k]]
  for n,z in oldv.items():
   if n in carrier_names or n in fields or n in{f'Y{i}'for i in PRIMARIES}or(n in packets and k<=resets[n]):continue
   assert n in vv and vv[n]==z,(k,o,n,hex(vv.get(n,0)),hex(z))
   if n not in donor_names and not(n.startswith('Y')and int(n[1:])not in w['targets']):assert CC[aa[n]]==C[oldat[n]],(k,n,'chart')
   comp+=1
 born={o[1]for o in ops if o[0]=='INIT'};oldborn={o[1]for o in w['operations']if o[0]=='INIT'};owned={n:z for n,z in v.items()if n in born};assert all(z>>111==0 for z in owned.values());support=0
 for z in owned.values():support|=z
 for i in range(111):support|=v[f'Y{i}']^(1<<(111+i))
 support_list=[i for i in range(111)if support>>i&1];owned_move_delta=sum(o[0]=='MOVE'and o[1]in born for o in ops)-sum(o[0]=='MOVE'and o[1]in oldborn for o in w['operations']);assert owned_move_delta==0;gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 lim=tuple(x/6 for x in pr.moment(gate));q=pr.moment(after['movement_profile']);qo=pr.moment(before['movement_profile']);a.out.mkdir(parents=True,exist_ok=True);sha=write(a.out/'WORD.json',nw);res={'status':'PASS_ACTUAL_ASCENDING_SHARED_CORRECTION_CARRIERS','word_sha256':sha,'base_word_sha256':PIN,'before':before,'after':after,'interface':cut,'all_targets':nw['targets'],'native_original_count':len(nw['released_carriers']),'native_originals':nw['released_carriers'],'remaining_ground_Y_count':65,'known_support':sorted(S),'canonical_mode_records':mode_records,'mode_rank_mod_known48':len(e.bb(v[f]&unknown_mask for f in fields)),'full_cut_nonidentity_X_support':support_list,'full_cut_nonidentity_X_support_count':len(support_list),'owned_X_rank':len(e.bb(owned.values())),'owned_Y_rank':0,'unaffected_old_state_comparisons':comp,'owned_MOVE_increment':owned_move_delta,'whole_moment':pr.record(q),'moment_increment':pr.record((q[0]-qo[1],q[1]-qo[0])),'necessary_limiting_room':pr.record((lim[0]-q[1],lim[1]-q[0])),'scope':nw['scope']};write(a.out/'RESULT.json',res);print(json.dumps({k:res[k]for k in['status','word_sha256','after','native_original_count','mode_rank_mod_known48','full_cut_nonidentity_X_support_count','whole_moment','necessary_limiting_room']}))
if __name__=='__main__':main()
