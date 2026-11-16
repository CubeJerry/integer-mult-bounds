#!/usr/bin/env python3
"""Independent physical/source review of A's mode-preserving48 and50 words."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
BASE='14503b00ad6f9d1e4d85ec09769a51c14eca36d61edabe19d9ae2907608c7501'
PINS={48:'28f6825bf0c35f0e76d856c269b1602caa91aefa9bb8b6db2b64f7d6659ec3dc',50:'58d5e8fa834cec59fa8019d686ff7a2e08fe43deb95d95c969ea8951ed03b662'}
FRAME=[74,80,90,92];OTHER=[80,90,92];J=[5,35,93,96,97,109,110]
PAIRS=[['P1','J23','L11','KEEP_M23',38,54],['P2','J22','L12','KEEP_M22',39,53]]
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();br=(a.work/'A/shared-proper-five46/WORD.json').read_bytes();require(hashlib.sha256(br).hexdigest()==BASE,'base pin');b=json.loads(br);bs,bt,_=replay(b,collect=True);bv,ba=bt[b['carrier_interface_before_operation']]
 sr=(a.repo/b['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==b['source_sha256'],'native pin');R=json.loads(sr)['native_roots'];originals={f'{p}{i}'for p in ['X','Y']for i in range(N)};reports={}
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6)
 def ownmoves(w,C,tr):
  names={o[1]for o in w['operations']if o[0]=='INIT'};ans={}
  for k,o in enumerate(w['operations']):
   if o[0]=='MOVE'and o[1]in names:
    d=len(C[tr[k][1][o[1]]])-len(C[o[2]]);ans[d]=ans.get(d,0)+1
  return ans
 for count in [48,50]:
  wr=(a.work/f'A/mode-preserving{count}/WORD.json').read_bytes();require(hashlib.sha256(wr).hexdigest()==PINS[count],'new word pin');w=json.loads(wr);C={n:chart(z)for n,z in w['charts'].items()};memo={}
  def sub(h,k):
   key=(h,k)
   if key not in memo:memo[key]=len(C[h])<=len(C[k])and len(rref(C[h]+C[k])[0])==len(C[k])
   return memo[key]
  for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'actual native charts')
  stats,tr,_=replay(w,collect=True);ops=w['operations'];cut=w['carrier_interface_before_operation'];v,at=tr[cut];meta=w['mode_preserving_d4'];require(meta['frame']==FRAME and meta['other']==OTHER and meta['primary']==74,'literal selected quartet')
  common=meta['common'];require(C[common]==chart({'kind':'ann','rows':[R[i]for i in FRAME]})and len(C[common])==4 and sub(common,'M1'),'actual common rank4 chart')
  require(all(sum(x*y for x,y in zip(R[i],R[j]))==0 for i in FRAME for j in FRAME if i!=j),'actual orthogonal quartet')
  pre=meta['prelude_end'];pv,pa=tr[pre];sigma=sum(1<<i for i in OTHER);snap='MODE_INITIAL_Y74'
  require(pv[snap]==1<<(N+74)and pa[snap]=='M1'and pv['Y74']==(1<<(N+74))^sigma and pa['Y74']=='F74','real arbitrary-Y snapshot and primary local accumulation')
  for i in FRAME:require(pv[f'X{i}']==1<<i and pa[f'X{i}']=='Hub','actual raw quartet at Hub before loading')
  caches=[]
  for idx,i in enumerate(OTHER):
   for size in [1,2]:
    interval=[OTHER[(idx+h)%3]for h in range(size)];flag=f'MODE_D4_FLAG_{i}_{size}';n=f'MODE_D4_RAW_{i}_{size}';caches.append(n)
    require(C[flag]==rref(C[common]+tuple(tuple(R[k])for k in interval))[0]and len(C[flag])==4+size,'exact cyclic source flag')
    require(pv[n]==1<<i and pa[n]==flag and not any(o[0]=='MOVE'and o[1]==n for o in ops),'actual stationary cyclic raw cache')
  k=meta['feedback_cell']['before_operation'];require(ops[k:k+2]==[['ADD','P4','Y74'],['ADD','Y74','P4']],'literal changing primary cell')
  require(tr[k][0]['P4']==sum(1<<i for i in FRAME)and tr[k][0]['Y74']==(1<<(N+74))^sigma and tr[k][1]['P4']==tr[k][1]['Y74']=='F74','actual feedback operands')
  require(tr[k+2][0]['Y74']==(1<<(N+74))^(1<<74)and tr[k+2][0]['P4']==(1<<(N+74))^sigma,'completed primary and dirty packet')
  pur=ops.index(['ADD',snap,'P4']);cap=ops.index(['ADD','P4','ZFIRST4']);reset=ops.index(['ADD','ZFIRST4','P4']);down=ops.index(['MOVE','ZFIRST4',common]);clear=ops.index(['CLEAR',snap])
  require(k+2<=pur<cap<reset<clear<down and tr[cap][0]['P4']==sigma and tr[reset+1][0]['P4']==0,'actual purification capture reset clear descent')
  require(v['ZFIRST4']==sigma and at['ZFIRST4']==common and snap not in v,'pure triple code and finished snapshot lifetime')
  for idx,i in enumerate(OTHER):
   reads=[o[1]for o in ops if o[0]=='ADD'and o[2]==f'Y{i}'];want=['ZFIRST4']+[f'MODE_D4_RAW_{OTHER[(idx-size)%3]}_{size}'for size in [1,2]];require(reads==want,'exact common-code then cyclic-local decoder')
  D=set(FRAME);changed={'ZFIRST4'};paircells=[]
  require(not any(o[0]=='ADD'and o[2]in{f'X{i}'for i in FRAME}for o in b['operations']),'projected quartet originals immutable')
  if count==50:
   require(w['local_pair_extension']['plan']==PAIRS,'actual third-stage pairs');pairD={38,39,53,54};D|=pairD;changed|={'KEEP_M23','KEEP_M22'}
   require(not any(o[0]=='ADD'and o[2]in{f'X{i}'for i in pairD}for o in reference48['operations']),'projected pair originals immutable')
   ppv,ppa=tr[w['local_pair_extension']['prelude_end']]
   for p,top,line,f,i,j in PAIRS:
    for d in [i,j]:
     flag=f'LOCAL_PAIR_FLAG_{d}';raw=f'LOCAL_PAIR_RAW_{d}';src=f'LOCAL_PAIR_SOURCE_{d}'
     require(C[flag]==rref(C[line]+C[f'L{d}'])[0]and len(C[flag])==2 and sub(flag,top),'actual pair source flag below proper J')
     require(ppv[raw]==ppv[src]==1<<d and ppa[raw]==flag and ppa[src]==top,'actual two stationary pair caches')
     require(not any(o[0]=='MOVE'and o[1]in{raw,src}for o in ops),'pair caches have no MOVE')
     require([o[2]for o in ops if o[0]=='ADD'and o[1]==f'X{d}']==[raw,src],'all old pair-coordinate reads projected away')
    load=ops.index(['ADD',f'LOCAL_PAIR_SOURCE_{i}',p]);capture=ops.index(['ADD',p,f]);resetpair=ops.index(['ADD',f,p]);require(ops[load:load+2]==[['ADD',f'LOCAL_PAIR_SOURCE_{i}',p],['ADD',f'LOCAL_PAIR_SOURCE_{j}',p]],'real pair programming')
    require(tr[load][0][p]==0 and tr[load][1][p]==top and tr[capture][0][p]==(1<<i)^(1<<j)and tr[capture][1][p]==line,'real zero proper source and descending pair payload')
    require(tr[resetpair+1][0][p]==0 and v[f]==(1<<i)^(1<<j)and at[f]==line,'actual pair retention/reset')
    paircells.append({'packet':p,'pair':[i,j],'proper_chart':top,'load':load,'capture':capture,'reset':resetpair,'common_line':line})
  else:reference48=w
  dm=sum(1<<i for i in D);checked=[]
  for n,z in bv.items():
   if n in originals or n in changed:continue
   require(n in v and v[n]==z&~dm and C[at[n]]==C[ba[n]],('complete old cut source projection',n));checked.append(n)
  for i in range(N):
   require(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub','all raw Hub originals at cut')
   require(v[f'Y{i}']==(1<<(N+i))^((1<<i)if i in w['targets']else 0)and at[f'Y{i}']==(f'F{i}'if i in w['targets']else 'zero'),'all exact completed/unfinished receiver interfaces')
  require(len(w['targets'])==count and set(w['targets'])==set(b['targets'])|{90,92}|({53,54}if count==50 else set()),'exact added outputs')
  owned={n:z for n,z in v.items()if n not in originals};require(all(z>>N==0 for z in owned.values()),'all cut owners pureX');jm=sum(1<<i for i in J);nonlocal_rows={}
  for n,z in owned.items():
   local=sum(1<<i for i in J if sub(f'L{i}',at[n]));row=z&jm&~local
   if row:nonlocal_rows[n]=[i for i in J if row>>i&1]
  expected={'KEEP_C0':[35],'KEEP_C1':[110],'KEEP_C2':[93],'ZFIRST3':[96,109],'ZFIRST5':[97,109]};require(nonlocal_rows==expected,'all five exact nonlocal classes retained')
  for n in expected:require(v[n]&jm==bv[n]&jm,'every named retained J payload unchanged')
  own=ownmoves(w,C,tr);oldown=ownmoves(b,C,bt);oldown[1]+=1;require(own==oldown,'exactly one additional owned unit descent overall')
  U=sorted(set(range(N))-set(w['targets']));um=sum(1<<i for i in U);ar={i:0 for i in U}
  for n,z in v.items():
   if not z&um:continue
   for i in U:
    if sub(at[n],f'F{i}'):ar[i]|=z&um
  rows={i:[j for j in U if ar[i]>>j&1]for i in U};special={18,26,61,67,68,71,72,81,84,85}
  require(rows=={i:([5,15]if i in special else [])for i in U},'actual unfinished access remains twenty-arc DAG')
  remaining=set(U);order=[]
  while remaining:
   ready=sorted(i for i in remaining if not(set(rows[i])&remaining));require(bool(ready),'whole unfinished graph acyclic');order+=ready;remaining-=set(ready)
  tail=ops[cut:];require(all(o[0]in{'MOVE','CLEAR'}for o in tail)and all(o[1].startswith('Y')and o[2]==f'F{o[1][1:]}'for o in tail if o[0]=='MOVE'),'no future source acquisition in frozen suffix')
  require(sum(o[0]=='MOVE'for o in tail)==len(U),'direct original-Y closure suffix')
  controls=[]
  events=[('missing actual local raw cache',['ADD','X90','MODE_D4_RAW_90_1']),('missing primary raw accumulation',['ADD','X90','Y74']),('missing actual quartet Hub input',['ADD','X90','P4']),('missing arbitrary-Y purifier',['ADD','MODE_INITIAL_Y74','P4']),('missing packet reset',['ADD','ZFIRST4','P4']),('missing common descent',['MOVE','ZFIRST4',common])]
  if count==50:events += [('missing actual proper pair capture',['ADD','X54','LOCAL_PAIR_SOURCE_54']),('missing actual pair source program',['ADD','LOCAL_PAIR_SOURCE_54','P1']),('missing paired local observation',['ADD','LOCAL_PAIR_RAW_38','Y54']),('missing third-stage reset',['ADD','KEEP_M23','P1'])]
  for label,event in events:
   bad=copy.deepcopy(w);bad['operations'].remove(event)
   try:replay(bad)
   except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':str(e)})
   else:raise ValueError(('accepted semantic omission',label))
  q=moment(stats['movement_profile']);floor=(q[0]+len(U),q[1]+len(U));require(floor[0]>limit[1],'fixed-cut DAG floor exceeds necessary allowance')
  reports[count]={'status':'PASS_MODE_PRESERVING_WORD_WITH_ACYCLIC_REMAINING_CUT','word_sha256':PINS[count],'base_word_sha256':BASE,'stats':stats,'targets':w['targets'],'cut':cut,'quartet_primary':74,'quartet_other':OTHER,'quartet_raw_caches':caches,'quartet_chronology':{'feedback':k,'purification':pur,'capture':cap,'reset':reset,'snapshot_retirement':clear,'unit_descent':down},'third_stage_pairs':paircells,'old_named_source_rows_projected_exactly':checked,'live_owner_count':len(owned),'live_owner_X_rank':len(binary_basis(owned.values())),'exact_nonlocal_J_classes':nonlocal_rows,'complete_owned_MOVE_profile':own,'actual_initial_chart_access':rows,'all_unfinished_acyclic_order':order,'necessary_future_owned_descents':len(U),'whole_moment':record(q),'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'fixed_cut_completion_movement_floor':record(floor),'controls':controls,'scope':'Actual new endpoints preserve five nonlocal rows, but the exact final cut still requires one future whole-field descent per unfinished receiver by the independently reviewed initial-chart theorem. Earlier source changes remain open. No global foundation or kappa claim.'}
  a.out.mkdir(parents=True,exist_ok=True);(a.out/f'RESULT{count}.json').write_text(json.dumps(reports[count],indent=2)+'\n');print(json.dumps({k:reports[count][k]for k in ['status','cut','stats','necessary_future_owned_descents','whole_moment']},indent=2))
if __name__=='__main__':main()
