#!/usr/bin/env python3
"""Independent physical/formal57-column review of six ascending original correctors."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require,rref
from price_projection import moment,record
PIN='cc505aaf4aee5e1995b4db22f9b53609856d3ecdc3ea1eb0797f2584e375dfee'
BASE='c7cf9a565d5dd6613342274979a9aa5de1bbb209cc3704a2a19e60eecb034245'
PRIMARY=[4,74,78];FIELDS=['ZFIRST3','ZFIRST4','ZFIRST5']
ASSIGN=[(0,(4,74),4),(2,(4,74),74),(7,(4,78),4),(28,(4,78),78),(44,(74,78),74),(50,(74,78),78)]
BACKUP={0:'ZRAW0',2:'COMMON_RAW2',7:'P0',28:'ZRAW28',44:'ZRAW44',50:'ADDED_RAW50'}
def groupname(g):return 'ASC_GROUP_'+'_'.join(map(str,g))
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();br=(a.work/'A/pruned78/WORD.json').read_bytes();wr=(a.work/'A/ascending-canonical3/WORD.json').read_bytes();require(hashlib.sha256(br).hexdigest()==BASE and hashlib.sha256(wr).hexdigest()==PIN,'word pins');b,w=json.loads(br),json.loads(wr)
 sr=(a.repo/w['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==w['source_sha256']==b['source_sha256'],'native source pin');R=json.loads(sr)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()};memo={}
 def sub(h,k):
  key=(h,k)
  if key not in memo:memo[key]=len(C[h])<=len(C[k])and len(rref(C[h]+C[k])[0])==len(C[k])
  return memo[key]
 for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'native charts')
 bs,bt,_=replay(b,collect=True);stats,tr,_=replay(w,collect=True);bc=b['carrier_interface_before_operation'];bv,ba=bt[bc];meta=w['ascending_corrections'];ops=w['operations'];cut=w['carrier_interface_before_operation'];v,at=tr[cut];require(cut==1083 and meta['continuation_before_operation']==cut,'actual cut1083')
 S=sorted(set(b['targets'])|{61,67});U=sorted(set(range(N))-set(S));sm=sum(1<<i for i in S);um=sum(1<<i for i in U);groups={}
 for i in U:
  g=tuple(k for k in PRIMARY if sum(x*y for x,y in zip(R[k],R[i]))==0);groups.setdefault(g,[]).append(i)
 donors=sorted(i for g,ds in groups.items()if g for i in ds);require(len(donors)==57 and len(U)==63,'actual57 of63 unknown donors')
 require(meta['groups']=={'_'.join(map(str,g)):ds for g,ds in groups.items()}and int(meta['chosen_mask_hex'],16)==sum(1<<i for i in donors),'exact full mask partition')
 require(not any(o[0]=='ADD'and(o[1]in{f'X{i}'for i in donors}or o[2]in{f'X{i}'for i in donors+[z[0]for z in ASSIGN]})for o in b['operations']),'previously detached unknowns and immutable protected carriers')
 pv,pa=tr[meta['prelude_end']];group_report={}
 for g,ds in groups.items():
  if not g:continue
  name=groupname(g);require(C[name]==chart({'kind':'ann','rows':[R[k]for k in g]})and len(C[name])==8-len(g)and sub('M1',name),'actual group intersection above M1')
  require(pv[name]==sum(1<<i for i in ds)and pa[name]==name,'actual grouped raw acquisition')
  require(not any(o[0]=='MOVE'and o[1]==name for o in ops),'all seven new owners stationary')
  for i in ds:require(sub(f'L{i}',name)and pv[f'X{i}']==1<<i and pa[f'X{i}']=='Hub','donor really passes correction chart then reaches Hub')
  group_report['_'.join(map(str,g))]={'inputs':ds,'chart':name,'rank':len(C[name]),'field_row_hex':hex(v[name])}
 carrier_report=[]
 for c,g,aa in ASSIGN:
  x=f'X{c}';name=groupname(g);u=sum(1<<i for i in groups[g]);oldreads=[o for o in b['operations']if o[0]=='ADD'and o[1]==x];require(len(oldreads)==1,'exact old protected carrier read')
  oldread=ops.index(oldreads[0]);couple=ops.index(['ADD',name,x]);read=ops.index(['ADD',x,f'Y{aa}']);coat=ops.index(['ADD',BACKUP[c],f'Y{aa}']);restores=[k for k,o in enumerate(ops)if o[0]=='ADD'and o[2]==x and o[1].startswith('X')]
  require(oldread<couple<read and coat<read and tr[coat][0][BACKUP[c]]==1<<c and len(C[tr[coat][1][BACKUP[c]]])==len(C[tr[coat][1][f'Y{aa}']])==0,'real protected raw use and ground nuisance cancellation')
  require(sub(f'L{c}',name)and sub(name,f'F{aa}')and tr[couple][1][x]==name and tr[couple][0][x]==1<<c,'actual ascending group acquisition')
  require(tr[read][0][x]==(1<<c)^u and tr[read][1][x]==f'F{aa}','real mixed original at receiving facet')
  require([ops[k][1]for k in restores]==[f'X{i}'for i in groups[g]]and all(k>read and tr[k][1][x]=='Hub'and tr[k][0][ops[k][1]]==1<<int(ops[k][1][1:])for k in restores),'actual raw-Hub restoration without cyclic donors')
  require(v[x]==1<<c and at[x]=='Hub','every corrected original actually restored')
  carrier_report.append({'carrier':c,'group':list(g),'receiver':aa,'old_protected_read':oldread,'ground_precoat':coat,'coupling':couple,'receiver_read':read,'actual_restore_operations':restores})
 modes=[]
 for aa,p,f in zip(PRIMARY,['P3','P4','P5'],FIELDS):
  cap=ops.index(['ADD',p,f]);reset=ops.index(['ADD',f,p]);require(tr[reset+1][0][p]==0,'changed first retention really resets packet')
  require([o for o in ops[:reset]if o[0]=='ADD'and o[1]==p]==[['ADD',p,f]],'no unhandled packet observer')
  require([o[2]for o in ops if o[0]=='ADD'and o[1]==f]==[p,f'Y{aa}'],'exact retained reader closure')
  expected=(1<<aa)^sum(1<<i for i in range(N)if sum(x*y for x,y in zip(R[aa],R[i]))==0);u=expected&um
  require(bv[f]&um==0 and v[f]==bv[f]^u and at[f]=='M1','actual canonical unknown projection at M1')
  require(ops.count(['ADD',groupname((aa,)),f'Y{aa}'])==1 and ops.count(['ADD',groupname(tuple(PRIMARY)),f'Y{aa}'])==1,'actual singleton and triple group observations')
  modes.append({'primary':aa,'field':f,'canonical_row_hex':hex(expected),'old_known_offset_hex':hex(bv[f]),'actual_row_hex':hex(v[f]),'unknown_projection_hex':hex(u),'capture':cap,'reset':reset})
 require(len(binary_basis(v[f]&um for f in FIELDS))==3,'three independent canonical quotient modes')
 originals={f'{p}{i}'for p in ['X','Y']for i in range(N)};owned={n:z for n,z in v.items()if n not in originals}
 for n,z in bv.items():
  if n in originals or n in FIELDS:continue
  require(v[n]==z and C[at[n]]==C[ba[n]],('every other old cut owner unchanged',n))
 require(w['targets']==b['targets']and len(w['targets'])==46,'same46 endpoints')
 for i in range(N):
  require(v[f'X{i}']==1<<i,'all cut originals raw')
  if i in w['released_carriers']:require(at[f'X{i}']==f'L{i}','retained native original')
  if i not in w['targets']:require(v[f'Y{i}']==1<<(N+i)and at[f'Y{i}']=='zero','all65 arbitrary unfinished Y inputs stay ground')
 require(len(w['released_carriers'])==15 and len(owned)==101 and all(z>>N==0 for z in owned.values()),'actual15 native and101 pureX owners')
 support=0
 for z in owned.values():support|=z
 for i in w['targets']:support|=1<<i
 require(support==sm|sum(1<<i for i in donors)and support.bit_count()==105,'full source support105')
 # Every parameter-bearing instruction reads an immutable raw original.
 events={};read_counts={i:0 for i in donors};donor_index={i:j for j,i in enumerate(donors)}
 for k,o in enumerate(ops):
  if o[0]=='ADD'and o[1].startswith('X')and int(o[1][1:])in donor_index:
   i=int(o[1][1:]);events[k]=donor_index[i];read_counts[i]+=1
 require(not any(o[0]=='ADD'and o[2]in{f'X{i}'for i in donors}for o in ops),'all parameter donors remain immutable')
 for g,ds in groups.items():
  for i in ds:
   if g:require(read_counts[i]==1+len(g)+(2 if len(g)==2 else 0),'each parameter occurs in actual capture, packet loads and needed carrier restores')
 fv={f'X{i}':1<<i for i in range(N)};fv.update({f'Y{i}':1<<(N+i)for i in range(N)});fc=None
 for k,o in enumerate(ops):
  if k==cut:fc=fv.copy()
  op,n,*q=o
  if op=='INIT':fv[n]=0
  elif op=='ADD':
   if k in events:
    j=events[k];require(fv[n]==1<<donors[j],'formal parameter source remains actual raw');fv[q[0]]^=1<<(2*N+j)
   else:fv[q[0]]^=fv[n]
  elif op=='CLEAR':del fv[n]
 for i in range(N):require(fv[f'X{i}']==1<<i and fv[f'Y{i}']==(1<<(N+i))^((1<<i)if i in w['targets']else 0),'formal57-parameter all222 endpoint identity')
 for g,ds in groups.items():
  if g:require(fc[groupname(g)]==sum(1<<(2*N+donor_index[i])for i in ds),'formal actual proper group masks')
 for aa,f in zip(PRIMARY,FIELDS):require(fc[f]==bv[f]^sum(1<<(2*N+donor_index[i])for g,ds in groups.items()if aa in g for i in ds),'formal proper three-mode source')
 def ownprofile(ww,tt):
  names={o[1]for o in ww['operations']if o[0]=='INIT'};ans={}
  for k,o in enumerate(ww['operations']):
   if o[0]=='MOVE'and o[1]in names:
    d=len(C[tt[k][1][o[1]]])-len(C[o[2]]);ans[d]=ans.get(d,0)+1
  return ans
 opb,opw=ownprofile(b,bt),ownprofile(w,tr);require(opb==opw,'complete owned movement profile unchanged')
 controls=[];d=groups[(4,74)][0]
 tests=[('omit actual group capture',['ADD',f'X{d}',groupname((4,74))]),('omit actual packet mask',['ADD',f'X{d}','P3']),('omit actual ground nuisance correction',['ADD','ZRAW0','Y4']),('omit real group-to-original coupling',['ADD',groupname((4,74)),'X0']),('omit actual original delivery',['ADD','X0','Y4']),('omit real original restoration',['ADD',f'X{d}','X0']),('omit singleton correction',['ADD',groupname((4,)),'Y4']),('omit triple correction',['ADD',groupname(tuple(PRIMARY)),'Y4']),('omit changed-packet reset',['ADD','ZFIRST3','P3']),('omit source lifetime end',['CLEAR',groupname((4,74))])]
 for label,event in tests:
  bad=copy.deepcopy(w);bad['operations'].remove(event)
  try:replay(bad)
  except(ValueError,KeyError)as e:controls.append({'control':label,'rejected':str(e)})
  else:raise ValueError(('accepted source/correction omission',label))
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);limit=(gl/6,gh/6);q=moment(stats['movement_profile']);qb=moment(bs['movement_profile'])
 result={'status':'PASS_INDEPENDENT_ACTUAL_ASCENDING_CORRECTIONS_AND_FORMAL57_FAMILY','word_sha256':PIN,'base_word_sha256':BASE,'native_source_sha256':w['source_sha256'],'stats':stats,'cut':cut,'actual_groups':group_report,'carrier_chronology':carrier_report,'canonical_modes':modes,'comparison_coordinate_set_S48':S,'S48_is_not_a_raw48_ground_grant':True,'actual_raw_ground_backups_used':BACKUP,'parameter_count':57,'formal_parameter_read_events':len(events),'all_parameter_endpoint_and_source_identities':True,'canonical_claim_scope':'Only the all-one mask has the displayed canonical quotient rows; arbitrary binary parameters preserve endpoints and the weighted unknown-column source.','source_support_count':105,'actual_owner_X_rank':len(binary_basis(owned.values())),'actual_owner_Y_rank':0,'native_originals':w['released_carriers'],'complete_owned_MOVE_profile':opw,'whole_moment':record(q),'moment_increment':record((q[0]-qb[1],q[1]-qb[0])),'necessary_limiting_room':record((limit[0]-q[1],limit[1]-q[0])),'controls':controls,'scope':'Actual shared raw corrections ascend in six original carriers with real ground nuisance cancellation and explicit independent raw-donor Hub restoration. Pure canonical quotient source at M1, no additional owned MOVE. All five global foundations remain open; no new output or kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','stats','cut','formal_parameter_read_events','whole_moment']},indent=2))
if __name__=='__main__':main()
