#!/usr/bin/env python3
"""Independent native, parameter, custody and access review of A's five-mask source."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
PIN='14503b00ad6f9d1e4d85ec09769a51c14eca36d61edabe19d9ae2907608c7501'
BASE='27dc6c36eec067acd2fe4679a81c95ea9db8fd6377784a0bbfc060ca52a121fd'
PROOF='0f5eea5890e04fd58c746a504da318d27aed3b8cbc401724a3ec634c66ea748c'
PLAN=[['P0','KEEP_C0',35,'D3_21',[3,21]],['P1','KEEP_C1',110,'D76_64',[76,64]],['P2','KEEP_C2',93,'D80_65',[80,65]],['P3','ZFIRST3',96,'F4',[4]],['P5','ZFIRST5',97,'F78',[78]]]
J=[5,35,93,96,97,109,110]
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();require(hashlib.sha256((a.work/'A/SHARED-PROPER-MASKS-PROOF.md').read_bytes()).hexdigest()==PROOF,'qualified universal proof pin');bp=a.repo/'research/moonshot-005-program/results/bit-canonical-mask-source/author/early-paid46/WORD.json';wp=a.work/'A/shared-proper-five46/WORD.json'
 br,wr=bp.read_bytes(),wp.read_bytes();require(hashlib.sha256(br).hexdigest()==BASE and hashlib.sha256(wr).hexdigest()==PIN,'literal pins');b,w=json.loads(br),json.loads(wr)
 sr=(a.repo/w['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==w['source_sha256']==b['source_sha256'],'native pin');R=json.loads(sr)['native_roots']
 C={n:chart(z)for n,z in w['charts'].items()};memo={}
 def sub(h,k):
  key=(h,k)
  if key not in memo:memo[key]=len(C[h])<=len(C[k])and len(rref(C[h]+C[k])[0])==len(C[k])
  return memo[key]
 for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'native charts')
 require(w['charts']==b['charts'],'unchanged chart definitions');bs,bt,_=replay(b,collect=True);stats,tr,_=replay(w,collect=True)
 meta=w['shared_proper_masks'];require(meta['plan']==PLAN and meta['bits']==[1]*5 and meta['prelude_end']==20,'five-input plan')
 ops=w['operations'];cut=w['carrier_interface_before_operation'];v,at=tr[cut];require(cut==1364 and meta['continuation_before_operation']==cut,'cut1364')
 D={z[2]for z in PLAN};dm=sum(1<<i for i in D);xs={f'X{i}'for i in D};fields={z[1]for z in PLAN};affectedY={f'Y{i}'for z in PLAN for i in z[4]}
 require(D.isdisjoint(w['targets'])and w['targets']==b['targets']and len(w['targets'])==46,'same46 targets, released5 unfinished')
 require(not any(o[0]=='ADD'and o[2]in xs for o in b['operations']),'immutable originals')
 require(not any(o[0]=='ADD'and o[1].startswith('Y')for o in b['operations']),'no output-repair propagation')
 cells=[];param_events={};extra=set(meta['source_add_indices']+meta['correction_add_indices'])
 for j,(p,f,i,h,ys)in enumerate(PLAN):
  raw=f'SHARED_PROPER_RAW_{i}'
  require(ops[4*j:4*j+4]==[['MOVE',f'X{i}',h],['INIT',raw,h],['ADD',f'X{i}',raw],['MOVE',f'X{i}','Hub']],'native cache acquisition before Hub')
  require(sub(f'L{i}',h)and all(sub(h,f'F{k}')for k in ys),'shared correction containment')
  require(not any(o[0]=='MOVE'and o[1]==raw for o in ops),'stationary new cache')
  require(v[raw]==1<<i and at[raw]==h,'actual raw correction source')
  events=[(k,o)for k,o in enumerate(ops)if o[0]=='ADD'and o[1]==f'X{i}'];require([o[2]for k,o in events]==[raw,p],'only actual capture and Hub read remain')
  source=events[1][0];require(source==meta['source_add_indices'][j]and tr[source][1][p]==tr[source][1][f'X{i}']=='Hub','raw Hub chronology')
  cap=ops.index(['ADD',p,f]);reset=ops.index(['ADD',f,p]);require(source<cap<reset,'load capture reset order')
  require([o for o in ops[source:reset]if o[0]=='ADD'and o[1]==p]==[['ADD',p,f]],'only changed packet observer is retention')
  require([o[2]for o in ops if o[0]=='ADD'and o[1]==f]==[p]+[f'Y{k}'for k in ys],'complete retained reader closure')
  require(tr[reset+1][0][p]==0,'true packet reset')
  oldreset=b['operations'].index(['ADD',f,p]);require(v[f]==(bt[oldreset][0][f]&~dm)^(1<<i),'projected-plus-mask retention')
  correction=[]
  for k in ys:
   y=f'Y{k}';read=ops.index(['ADD',f,y]);repair=ops.index(['ADD',raw,y]);require(read<repair and tr[repair][1][y]==h,'actual correction after retention')
   require(repair in meta['correction_add_indices'],'advertised correction');correction.append(repair)
   if h!=f'F{k}':
    require(ops[repair-1]==['MOVE',y,h]and ops[repair+1]==['MOVE',y,f'F{k}'],'nested actual output route');extra.add(repair-1)
   else:require(ops[repair-1]==['MOVE',y,h],'real receiver facet arrival')
   param_events[repair]=j
  param_events[source]=j;cells.append({'packet':p,'retention':f,'raw_input':i,'proper_cache':raw,'chart':h,'rank':len(C[h]),'load':source,'capture':cap,'reset':reset,'corrections':correction})
 for i in range(N):
  require(v[f'X{i}']==1<<i and at[f'X{i}']=='Hub','raw Hub originals')
  require(v[f'Y{i}']==(1<<(N+i))^((1<<i)if i in w['targets']else 0),'arbitrary Y columns and offsets')
  require(at[f'Y{i}']==(f'F{i}'if i in w['targets']else 'zero'),'actual receiver cut charts')
 originals={f'{p}{i}'for p in ['X','Y']for i in range(N)};owned={n:z for n,z in v.items()if n not in originals};require(len(owned)==132 and all(z>>N==0 for z in owned.values()),'132 pure-X owners')
 # Align every surviving predecessor instruction without the author's mapping.
 pos=20;comp=0;resets={p:b['operations'].index(['ADD',f,p])for p,f,i,h,ys in PLAN}
 for k,o in enumerate(b['operations']):
  if o[0]=='CLEAR'or(o[0]=='MOVE'and o[1].startswith('Y')and int(o[1][1:])not in b['targets'])or(o[0]in{'MOVE','ADD'}and o[1]in xs):continue
  while pos in extra:pos+=1
  require(ops[pos]==o,('literal old instruction',k,pos));pos+=1
  old,oldat=bt[k+1];new,newat=tr[pos]
  for n,z in old.items():
   if n in xs|fields|affectedY or(n in resets and k<resets[n])or(n.startswith('Y')and int(n[1:])not in b['targets']):continue
   require(n in new and new[n]==z&~dm and C[newat[n]]==C[oldat[n]],('projected old-state covariance',k,n));comp+=1
 require(pos==cut,'whole retained old core accounted for')
 # Formal monomials theta_j*x_d parameterize only Hub loads and cache repairs.
 # Fixed raw cache acquisitions stay unscaled, as in the actual family.
 fv={f'X{i}':1<<i for i in range(N)};fv.update({f'Y{i}':1<<(N+i)for i in range(N)});fc=None
 for k,o in enumerate(ops):
  if k==cut:fc=fv.copy()
  op,n,*q=o
  if op=='INIT':fv[n]=0
  elif op=='ADD':
   if k in param_events:
    j=param_events[k];require(fv[n]==1<<PLAN[j][2],'parameter reads actual raw source');fv[q[0]]^=1<<(2*N+j)
   else:fv[q[0]]^=fv[n]
  elif op=='CLEAR':del fv[n]
 for i in range(N):require(fv[f'X{i}']==1<<i and fv[f'Y{i}']==(1<<(N+i))^((1<<i)if i in w['targets']else 0),'formal five-parameter endpoint identity')
 for j,(p,f,i,h,ys)in enumerate(PLAN):
  oldreset=b['operations'].index(['ADD',f,p]);require(fc[f]==(bt[oldreset][0][f]&~dm)^(1<<(2*N+j)),'formal retained rows for all32 choices')
 def owned_profile(ww,tt):
  names={o[1]for o in ww['operations']if o[0]=='INIT'};profile={}
  for k,o in enumerate(ww['operations']):
   if o[0]=='MOVE'and o[1]in names:
    d=len(C[tt[k][1][o[1]]])-len(C[o[2]]);profile[d]=profile.get(d,0)+1
  return profile
 opb,opw=owned_profile(b,bt),owned_profile(w,tr);require(opb==opw,'entire owned MOVE profile unchanged')
 jm=sum(1<<i for i in J);nonlocal_rows={};Jfields={}
 for n,z in v.items():
  if not z&jm:continue
  local=sum(1<<i for i in J if sub(f'L{i}',at[n]));row=z&jm&~local
  if n in owned and row:nonlocal_rows[n]={'chart':at[n],'support':[i for i in J if row>>i&1]}
  Jfields[n]={'chart':at[n],'support':[i for i in J if z>>i&1],'accessible_clique_targets':[i for i in J if sub(at[n],f'F{i}')]}
 expected={'KEEP_C0':[35],'KEEP_C1':[110],'KEEP_C2':[93],'ZFIRST3':[96,109],'ZFIRST5':[97,109]}
 require({n:z['support']for n,z in nonlocal_rows.items()}==expected,'exact five nonlocal retained classes')
 require(len(binary_basis(sum(1<<i for i in z['support'])for z in nonlocal_rows.values()))==5,'five independent classes')
 require(all(not z['accessible_clique_targets']for z in Jfields.values()),'no J-dependent cut field below any J facet')
 require(sub('L5','C0')and sub('L5','M1')and all(not sub('L5',f'F{i}')for i in J),'common blocker L5 at both retained charts')
 # Exact access includes ALL live originals and owners, not merely nonlocal rows.
 U=sorted(set(range(N))-set(w['targets']));um=sum(1<<i for i in U);access={i:0 for i in U};evidence={i:{}for i in U}
 for n,z in v.items():
  if not z&um:continue
  for i in U:
   if sub(at[n],f'F{i}'):
    access[i]|=z&um
    for j in U:
     if z>>j&1:evidence[i].setdefault(j,n)
 ar={i:[j for j in U if access[i]>>j&1]for i in U};special=[18,26,61,67,68,71,72,81,84,85]
 require(ar=={i:([5,15]if i in special else [])for i in U},'exact twenty-arc access graph')
 W=[i for i in U if i not in {5,15}];require(len(W)==63 and all(not(access[i]>>j&1)for i in W for j in W),'zero-access witness63')
 remaining=set(U);decoded=[]
 while remaining:
  ready=sorted(i for i in remaining if not any(j in remaining for j in ar[i]));require(bool(ready),'acyclic access graph');decoded+=ready;remaining-=set(ready)
 suffix=ops[cut:];require(len(suffix)==197 and all(o[0]=='MOVE'and o[1].startswith('Y')for o in suffix[:65])and all(o[0]=='CLEAR'for o in suffix[65:]),'suffix65 original MOVEs and132 CLEARs')
 require(stats['counts']=={'MOVE':485,'INIT':132,'ADD':812,'CLEAR':132}and stats['movement_profile']=={1:195,2:34,3:60,4:9,5:70,6:24,7:93},'complete native invoice')
 controls=[]
 tests=[(f'omit real cache capture {i}',['ADD',f'X{i}',f'SHARED_PROPER_RAW_{i}'])for p,f,i,h,ys in PLAN]+[(f'omit actual Hub mask {i}',['ADD',f'X{i}',p])for p,f,i,h,ys in PLAN]+[(f'omit old-reader repair Y{k}',['ADD',f'SHARED_PROPER_RAW_{i}',f'Y{k}'])for p,f,i,h,ys in PLAN for k in ys]
 for label,event in tests:
  bad=copy.deepcopy(w);bad['operations'].remove(event)
  try:replay(bad)
  except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':True,'reason':str(e)})
  else:raise ValueError(('accepted semantic omission',label))
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6);q=moment(stats['movement_profile']);qb=moment(bs['movement_profile'])
 result={'status':'PASS_INDEPENDENT_FIVE_MASK_SOURCE_WITH_ZERO_CLIQUE_ACCESS','word_sha256':PIN,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'stats':stats,'cut':cut,'cells':cells,'unaffected_projected_state_comparisons':comp,'actual_live_pure_X_owners':len(owned),'actual_owner_X_rank':len(binary_basis(owned.values())),'complete_owned_MOVE_profile':opw,'owned_MOVE_increment':0,'formal_parameter_count':5,'formal_all32_endpoint_identity':True,'nonlocal_clique':J,'nonlocal_retained_classes':nonlocal_rows,'nonlocal_projection_rank':5,'all_clique_dependent_fields_and_access':Jfields,'common_blocking_native_line':5,'unfinished_roles':U,'actual_free_access_rows':ar,'actual_access_coordinate_witnesses':evidence,'zero_access_witness63':W,'acyclic_decode_order65':decoded,'whole_moment':record(q),'moment_increment':record((q[0]-qb[1],q[1]-qb[0])),'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'controls':controls,'scope':'Valid actual source change and full222-column binary identities. Five new nonlocal classes have no upward-only access to the seven specified receiver facets. The entire unfinished access graph is acyclic. All five global foundations remain open; no full supplier or kappa.'}
 result['proof_sha256']=PROOF
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','stats','cut','actual_owner_X_rank','nonlocal_projection_rank','whole_moment']},indent=2))
if __name__=='__main__':main()
