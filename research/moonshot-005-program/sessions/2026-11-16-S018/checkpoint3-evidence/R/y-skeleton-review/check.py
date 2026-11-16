#!/usr/bin/env python3
"""Independent root all-column/interface review of homogeneous-Y reset."""
import argparse,hashlib,json,copy,sys
from pathlib import Path
p=argparse.ArgumentParser()
for n in ['repo','work','out']:p.add_argument('--'+n,type=Path,required=True)
a=p.parse_args();P=a.repo/'research/moonshot-005-program';sys.path.insert(0,str(P/'sessions/2026-11-16-S018/root-review'))
from optimize_word import independent_replay
from review_source_families import trace
from review_leaf_capacity import chart_basis,echelon
from price import invoice
paths={'base':'A/d4-feedback-pruned78/WORD.json','old':'C/y-skeleton-control/OLD-WORD.json','reset':'C/y-skeleton-control/RESET-WORD.json','unprepared':'C/y-skeleton-control/UNPREPARED-WORD.json','late':'C/y-skeleton-control/LATE-PRELOAD-NEGATIVE.json'}
raw={k:(a.work/v).read_bytes()for k,v in paths.items()};ws={k:json.loads(v)for k,v in raw.items()};b=ws['base'];old=ws['old'];new=ws['reset'];u=ws['unprepared'];late=ws['late']
assert hashlib.sha256(raw['base']).hexdigest()=='c7e48e002da3ce642707b25d74dc15d0915945f319053eb97f2016045afe4615'
assert hashlib.sha256(raw['old']).hexdigest()=='8ccbe6b77cccd404e529a86eb073eada9094fe647db4909a30a2ef29235975be'
assert hashlib.sha256(raw['reset']).hexdigest()=='82753e515ed84953f3807cb3614e4ed29d583d852e4fb7ba223f68cc56a52c7a'
src=(a.repo/b['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==b['source_sha256']=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
R=json.loads(src)['native_roots'];charts={n:chart_basis(v)for n,v in b['charts'].items()}
for i,r in enumerate(R):
 assert len(charts[f'L{i}'])==1 and len(echelon(charts[f'L{i}']+[r])[0])==1
 assert len(charts[f'F{i}'])==7 and all(sum(x*y for x,y in zip(row,r))==0 for row in charts[f'F{i}'])
for w in ws.values():assert w['charts']==b['charts']and w['source_sha256']==b['source_sha256']
stats={k:independent_replay(ws[k])for k in ['base','old','reset']};tr={k:trace(w)for k,w in ws.items()}
N=111;xm=(1<<N)-1;S=set(b['targets'])|{61,67};sm=sum(1<<i for i in S);assert len(S)==54
bc=b['cohort_feedback']['continuation_before_operation'];oc=old['continuation_before_operation'];nc=new['continuation_before_operation'];bv,ba=tr['base'][0][bc];ov,oa=tr['old'][0][oc];nv,na=tr['reset'][0][nc]
assert bc==oc==793 and nc==423 and old['operations'][:oc]==b['operations'][:bc]
meta=new['skeleton'];length=meta['literal_continuation_length'];F=old['operations'][oc:];assert length==len(F)==251 and new['operations'][nc:nc+length]==F
originals={f'{z}{i}'for z in 'XY'for i in range(N)};owners=set(bv)-originals
assert len(owners)==112 and{n:bv[n]>>N for n in owners if bv[n]>>N}=={'ZFIRST3':1<<4,'ZFIRST4':1<<74,'ZFIRST5':1<<78}
for n in bv:
 assert charts[ba[n]]==charts[na[n]] and (bv[n]^nv[n])>>N==0
 assert (bv[n]^nv[n])&xm&~sm==0
for i in S:
 n=f'SKELETON_RAW_{i}';assert nv[n]==1<<i and na[n]=='zero'
 assert new['operations'].count(['INIT',n,f'L{i}'])==1 and new['operations'].count(['ADD',f'X{i}',n])==1 and new['operations'].count(['MOVE',n,'zero'])==1
 assert new['operations'].count(['CLEAR',n])==1
ps,pe=meta['initial_preload_range'];assert pe-ps==52 and pe<new['operations'].index(['ADD','Y4','ZFIRST3'])
for op in new['operations'][ps:pe]:
 assert op[0]=='ADD'and op[1].startswith('SKELETON_RAW_')and op[2].startswith('Y')
 k=new['operations'].index(op);vv,aa=tr['reset'][0][k];assert aa[op[1]]==aa[op[2]]=='zero'
ufinal=tr['unprepared'][1][0];M=[ufinal[f'X{i}']for i in range(N)];frame=[3,4,47,51];offset=sum(1<<j for j in frame)
assert M==[(1<<i)^(offset if i==0 else 0)for i in range(N)]
assert all(ufinal[f'Y{i}']>>N==1<<i for i in range(N))
corrections=[ufinal[f'Y{i}']^(1<<(N+i))^((1<<i)if i in b['targets']else 0)for i in range(N)];assert all(z&~sm==0 for z in corrections)
pre_end=nc+length;before_inv,at_inv=tr['reset'][0][pre_end];assert all(before_inv[f'X{i}']==M[i]and at_inv[f'X{i}']=='Hub'for i in range(N))
assert meta['Hub_inverse']==[['ADD',f'X{i}','X0']for i in frame]
assert new['operations'][pre_end:pre_end+4]==meta['Hub_inverse']
old_transient=tr['old'][0][oc+2][0]['X0'];assert old_transient==(1<<0)^(1<<(N+4))^sum(1<<i for i in [3,47,51])
controls=[]
for op in [['ADD','Y4','ZFIRST3'],['ADD','SKELETON_RAW_3','Y3'],['ADD','X47','X0']]:
 bad=copy.deepcopy(new);bad['operations'].remove(op)
 try:independent_replay(bad)
 except(AssertionError,KeyError):controls.append({'omitted':op,'rejected':True})
 else:raise AssertionError('mutation survived')
lfinal=tr['late'][1][0];assert lfinal['X0']==(1<<0)^(1<<4)
assert all(lfinal[f'Y{i}']==(1<<(N+i))^((1<<i)if i in b['targets']else 0)for i in range(N))
try:independent_replay(late)
except AssertionError:pass
else:raise AssertionError('late counterexample passed')
# Adding exactly the residual Hub correction makes it pass, confirming legal
# geometry/lifetimes and isolating the intended error from a malformed route.
repaired=copy.deepcopy(late);repaired['operations'].append(['ADD','X4','X0']);independent_replay(repaired)
proof=a.work/'C/HOMOGENEOUS-SIGNATURE-RESET.md'
r={'status':'PASS_ROOT_HOMOGENEOUS_SIGNATURE_RESET_REVIEW','proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),'word_hashes':{k:hashlib.sha256(v).hexdigest()for k,v in raw.items()},'source_count':54,'source_coordinates':sorted(S),'old_cut':oc,'new_cut':nc,'literal_continuation_length':length,'all_named_cut_y_columns_equal':True,'all_named_cut_unknown_x_columns_equal':True,'actual_initial_preloads':52,'actual_owned_Y_signature':{'ZFIRST3':4,'ZFIRST4':74,'ZFIRST5':78},'transient_arbitrary_Y_in_original_X0':hex(old_transient),'nontrivial_original_matrix':'I plus row0 entries3,4,47,51; invertible involution','actual_Hub_inverse':meta['Hub_inverse'],'stats':stats,'reset_price':invoice(stats['reset']['movement_profile']),'direct_skeleton_reference':invoice({1:54,3:3,4:3,7:219}),'independent_controls':controls,'late_preload_control':{'all_Y_endpoints_correct':True,'X0_error':'x4','actual_geometry_and_lifetimes_confirmed':True,'one_extra_Hub_ADD_repairs_control':True},'scope':'Universal H-column argument reviewed separately. No C/A execution code imported; independently implemented predecessor exact geometry/all222 engine disclosed. Actual mixed-Y owner usage, paid source54, preload timing and nonidentity Hub repair checked. All five global foundations and suppliers remain open.'}
a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
