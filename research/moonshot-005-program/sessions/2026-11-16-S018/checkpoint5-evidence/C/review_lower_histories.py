#!/usr/bin/env python3
"""Independent physical review of A's paid lower-history57/59 words."""
import argparse,copy,hashlib,itertools,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
PINS={57:'dba6b8219052642d2f4940714ea2f9bda1271b8216df263126e79afed914a4c1',59:'dd60233b57be5fdef83b86a2d2b816e665e3d939850da94b680838d1d6d178ce'}
BASE='bd7fd31ba6cfe1bc92d26619e513184e6ce5864653cf58be7e9b68668be0d987'
FRAMES=[[16,18],[23,71,81],[22,68,85]];PRIMARY=[21,64,65]

def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();br=(a.work/'A/d4-cohort-paid46/WORD.json').read_bytes();require(hashlib.sha256(br).hexdigest()==BASE,'D4 paid52 pin');b=json.loads(br)
 sr=(a.repo/b['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==b['source_sha256'],'native pin');R=json.loads(sr)['native_roots']
 bs,bt,_=replay(b,collect=True);originals={f'{p}{i}'for p in ['X','Y']for i in range(N)}
 mutable={f'X{i}'for i in PRIMARY};immutable={f'X{i}'for g in FRAMES for i in g}
 require(not any(o[0]=='ADD'and o[2]in immutable for o in b['operations']),'immutable projected lower donors')
 require(not any(o[0]=='ADD'and o[1].startswith('Y')for o in b['operations']),'old output rows have no readers')
 caps={f'P{j}':b['operations'].index(['ADD',f'P{j}',f'KEEP_C{j}'])for j in range(3)}
 for k,o in enumerate(b['operations']):
  if o[0]=='ADD'and o[1]in mutable:require(o[2]in caps and k<caps[o[2]],'mutable old reads only in replaced source loads')
 results={};words={};traces={}
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6)
 def owned_profile(w,tr,C):
  own={o[1]for o in w['operations']if o[0]=='INIT'};p={}
  for k,o in enumerate(w['operations']):
   if o[0]=='MOVE'and o[1]in own:
    d=len(C[tr[k][1][o[1]]])-len(C[o[2]]);p[d]=p.get(d,0)+1
  return p
 for count in [57,59]:
  raw=(a.work/f'A/lower-history{count}-paid/WORD.json').read_bytes();require(hashlib.sha256(raw).hexdigest()==PINS[count],'word pin');w=json.loads(raw);words[count]=w
  require(w['source_sha256']==b['source_sha256'],'same native source');C={n:chart(z)for n,z in w['charts'].items()}
  for i in range(N):
   require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'native charts')
  stats,tr,_=replay(w,collect=True);traces[count]=tr;meta=w['lower_history'];cut=w['carrier_interface_before_operation'];v,at=tr[cut]
  require(meta['primaries']==PRIMARY and meta['frames']==FRAMES,'actual lower partition');require(len(w['targets'])==count,'target count')
  for i in range(N):
   require(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub','all cut originals rawHub')
   if i in w['targets']:require(v[f'Y{i}']==(1<<(N+i))^(1<<i)and at[f'Y{i}']==f'F{i}','completed native receiver')
   else:require(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero','raw unfinished ground receiver')
  cells=[];cache_names=[];pre=meta['prelude_end'];pv,pa=tr[pre]
  for j,(aa,frame)in enumerate(zip(PRIMARY,FRAMES)):
   code=sum(1<<i for i in frame);common=meta['common_charts'][j];Z=C[common];lower=meta['lower_fields'][j];upper=meta['upper_fields'][j];packet=f'P{j}';snap=f'LOWER_INITIAL_Y{j}'
   require(len(Z)==3 and len(rref(Z+C[f'J{frame[0]}'])[0])==4,'actual rank3 common below rank4J')
   require(all(sum(x*y for x,y in zip(R[i],R[k]))==0 for i,k in itertools.combinations([aa]+frame,2)),'actual orthogonal primary and lower clique')
   require(pv[snap]==1<<(N+aa)and pa[snap]=='M0','real original-Y snapshot')
   require(pv[f'Y{aa}']==(1<<(N+aa))^code and pa[f'Y{aa}']==f'F{aa}','real primary local acquisition')
   for idx,i in enumerate(frame):
    require(pv[f'X{i}']==1<<i and pa[f'X{i}']=='Hub','lower source acquired at Hub')
    for k in range(1,len(frame)):
     interval=[frame[(idx+h)%len(frame)]for h in range(k)];flag=f'LOWER_FLAG_{j}_{i}_{k}';name=f'LOWER_RAW_{j}_{i}_{k}';cache_names.append(name)
     require(C[flag]==rref(Z+tuple(tuple(R[h])for h in interval))[0],'actual cyclic cache flag')
     require(pv[name]==1<<i and pa[name]==flag,'real stationary raw cache')
     require(not any(o[0]=='MOVE'and o[1]==name for o in w['operations']),'cache truly stationary')
   cell=meta['feedback_cells'][j]['before_operation'];require(w['operations'][cell:cell+2]==[['ADD',packet,f'Y{aa}'],['ADD',f'Y{aa}',packet]],'actual feedback order')
   require(tr[cell][0][packet]==(1<<aa)^code and tr[cell][0][f'Y{aa}']==(1<<(N+aa))^code,'actual feedback operands')
   require(tr[cell+2][0][packet]==(1<<(N+aa))^code and tr[cell+2][0][f'Y{aa}']==(1<<(N+aa))^(1<<aa),'primary completion and packet change')
   pur=w['operations'].index(['ADD',snap,packet]);ucap=w['operations'].index(['ADD',packet,upper]);lcap=w['operations'].index(['ADD',packet,lower]);reset=w['operations'].index(['ADD',lower,packet]);down=w['operations'].index(['MOVE',lower,common])
   require(cell+2<=pur<ucap<lcap<reset<down,'real two-stage history chronology')
   require(tr[ucap][0][packet]==tr[lcap][0][packet]==code and tr[reset+1][0][packet]==0,'same pure code carried through paid M0-to-J route then truly reset')
   require(not any(o[0]=='ADD'and o[2]==packet for o in w['operations'][ucap+1:lcap]),'no hidden replacement load or early reset')
   require(v[upper]==v[lower]==code and C[at[upper]]==C['M0']and at[lower]==common,'actual two retained code fields')
   cells.append({'packet':packet,'primary':aa,'code':frame,'feedback':cell,'purification':pur,'upper_capture':ucap,'lower_capture':lcap,'lower_reset':reset,'new_descent':down})
  require(len(cache_names)==14,'fourteen real lower caches')
  pair_checks=[]
  if count==59:
   plan=w['local_pair_extension']['plan'];require(plan==[['P1','J23','L11','KEEP_M23',38,54],['P2','J22','L12','KEEP_M22',39,53]],'actual third-stage pair plan')
   projected={38,39,53,54};old=words[57]
   require(not any(o[0]=='ADD'and o[2]in{f'X{i}'for i in projected}for o in old['operations']),'four projected pair originals immutable')
   require(not any(o[0]=='ADD'and o[1]in{f'Y{i}'for i in projected}for o in old['operations']),'rebuilt old pair Ys have no source readers')
   for i in projected:
    require([o[2]for o in w['operations']if o[0]=='ADD'and o[1]==f'X{i}']==[f'LOCAL_PAIR_RAW_{i}',f'LOCAL_PAIR_SOURCE_{i}'],'every old original read removed except two actual replacement captures')
   ppv,ppa=tr[w['local_pair_extension']['prelude_end']]
   for packet,J,line,field,i,j in plan:
    require(sum(x*y for x,y in zip(R[i],R[j]))==0,'orthogonal third-stage pair')
    for d in [i,j]:
     flag=f'LOCAL_PAIR_FLAG_{d}';rawname=f'LOCAL_PAIR_RAW_{d}';src=f'LOCAL_PAIR_SOURCE_{d}'
     require(C[flag]==rref(C[line]+C[f'L{d}'])[0]and len(C[flag])==2,'real local pair flag')
     require(ppv[rawname]==ppv[src]==1<<d and ppa[rawname]==flag and ppa[src]==J,'two actual raw caches')
     require(ppv[f'X{d}']==1<<d and ppa[f'X{d}']=='Hub','actual pair original at Hub')
     require(not any(o[0]=='MOVE'and o[1]in{rawname,src}for o in w['operations']),'both new pair caches stationary')
    load=w['operations'].index(['ADD',f'LOCAL_PAIR_SOURCE_{i}',packet]);cap=w['operations'].index(['ADD',packet,field]);reset=w['operations'].index(['ADD',field,packet])
    require(tr[load][0][packet]==0 and tr[load][1][packet]==J,'third stage starts from real zero at proper J')
    require(w['operations'][load:load+2]==[['ADD',f'LOCAL_PAIR_SOURCE_{i}',packet],['ADD',f'LOCAL_PAIR_SOURCE_{j}',packet]],'actual local pair programming')
    require(tr[cap][0][packet]==(1<<i)^(1<<j)and tr[cap][1][packet]==line,'actual pair transported on existing descent')
    require(tr[reset+1][0][packet]==0 and v[field]==(1<<i)^(1<<j)and at[field]==line,'actual pair retention and reset')
    pair_checks.append({'packet':packet,'pair':[i,j],'source_chart':J,'load':load,'capture':cap,'reset':reset,'common_line':line})
  owned={n:z for n,z in v.items()if n not in originals};require(all(z>>N==0 for z in owned.values()),'all cut owners pureX')
  support=0
  for z in owned.values():support|=z
  for i in range(N):support|=v[f'Y{i}']^(1<<(N+i))
  require(support==(1<<N)-1,'full actual cut support111')
  ground={n:z for n,z in owned.items()if z and len(C[at[n]])==0}
  require(len(ground)==len(binary_basis(ground.values()))==25,'actual ground25 fields and rank')
  for f,frame in zip(w['retained_d4_cohort']['fields'],w['retained_d4_cohort']['frames']):require(v[f]==sum(1<<i for i in frame)and at[f]==w['retained_d4_cohort']['meet'],'D4 fields individually retained')
  op=owned_profile(w,tr,C)
  if count==57:
   bp=owned_profile(b,bt,C);bp[1]=bp.get(1,0)+3;require(op==bp,'exactly three new owned unit descents')
  else:require(op==results[57]['owned_MOVE_profile'],'third stage adds no owned MOVE')
  controls=[]
  def full_interface(ww):
   _,tt,_=replay(ww,collect=True);vv,aa=tt[ww['carrier_interface_before_operation']]
   require(vv==v and all(C[aa[n]]==C[at[n]]for n in v),'full declared cut source interface')
  def rejection(label,event,insert=False):
   bad=copy.deepcopy(w)
   if insert:
    k=w['operations'].index(['ADD','P1','KEEP_C1'])+1;bad['operations'].insert(k,event);bad['carrier_interface_before_operation']=cut+1
   else:
    k=bad['operations'].index(event);bad['operations'].pop(k);bad['carrier_interface_before_operation']=cut-(k<cut)
   try:full_interface(bad)
   except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
   else:raise ValueError(('accepted lower-history mutation',label))
  for label,event in [
   ('omit true lower cache capture',['ADD','X71','LOWER_RAW_1_71_1']),
   ('omit actual upper source input',['ADD','X71','P1']),
   ('omit original-Y purifier',['ADD','LOWER_INITIAL_Y1','P1']),
   ('omit lower reset',['ADD','TRIAD23','P1']),
   ('omit new unit descent',['MOVE','TRIAD23','LOWER_COMMON_1']),
   ('omit raw-cache retirement',['CLEAR','LOWER_RAW_1_71_1'])]:rejection(label,event)
  rejection('restore obsolete early M0 reset',['ADD','KEEP_C1','P1'],True)
  if count==59:
   for label,event in [
    ('omit actual proper pair source capture',['ADD','X54','LOCAL_PAIR_SOURCE_54']),
    ('omit actual pair raw decoder cache',['ADD','X38','LOCAL_PAIR_RAW_38']),
    ('omit real third-stage programming',['ADD','LOCAL_PAIR_SOURCE_54','P1']),
    ('omit third-stage packet reset',['ADD','KEEP_M23','P1'])]:rejection(label,event)
  q=moment(stats['movement_profile']);prevq=moment(bs['movement_profile']if count==57 else results[57]['stats']['movement_profile'])
  results[count]={'status':'PASS_INDEPENDENT_PAID_LOWER_HISTORY','targets':count,'word_sha256':PINS[count],
   'native_source_sha256':w['source_sha256'],'stats':stats,'cut':cut,'lower_cells':cells,'stationary_lower_caches':cache_names,
   'third_stage_pairs':pair_checks,'owned_MOVE_profile':op,'actual_live_owner_count':len(owned),
   'actual_owner_X_rank':len(binary_basis(owned.values())),'actual_owner_Y_rank':0,'actual_coordinate_support':111,
   'ground25_names':sorted(ground),'ground_rank':25,'all_X_raw_Hub':True,'unfinished_Y_raw_ground':N-count,
   'new_targets':sorted(set(w['targets'])-set(b['targets']if count==57 else words[57]['targets'])),
   'whole_moment':record(q),'moment_increment':record((q[0]-prevq[1],q[1]-prevq[0])),
   'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'controls':controls,
   'scope':'Independent literal native/all222-column replay, actual changing histories, cache and source chronology, cut source and complete price. Formal checks do not discharge any of five global foundations. No all111 or kappa.'}
  a.out.mkdir(parents=True,exist_ok=True);(a.out/f'PAID{count}-RESULT.json').write_text(json.dumps(results[count],indent=2)+'\n')
  print(json.dumps({k:results[count][k]for k in ['status','targets','stats','cut','whole_moment']},indent=2))
if __name__=='__main__':main()
