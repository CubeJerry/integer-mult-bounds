#!/usr/bin/env python3
"""Independent native65 augmentation and fixed-source static dual certificates."""
import argparse,copy,hashlib,json
from pathlib import Path
from release_projection import N,binary_basis,chart,replay,require
from price_projection import moment,record
BASE='cc505aaf4aee5e1995b4db22f9b53609856d3ecdc3ea1eb0797f2584e375dfee'
NATIVE='669dacab51d60878c25bf040d6a32feae85df36d48b4292f2ed6e94c3c8fbbf7'
PROOF='9fb5938a2c01d314ff7c4c369c6c6bec41e13d252b2f3582cb6caf407a0636a3'
STATIC='bfd7dec83ee2afb8aed462864b496c180446e651805efbc05bc3516e6e3a9574'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fits(rows,target):
 b=binary_basis(rows)
 while target:
  p=target.bit_length()-1
  if p not in b:return False
  target^=b[p]
 return True
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();bp=a.work/'A/ascending-canonical3/WORD.json';np=a.work/'A/ascending-canonical3-native65/WORD.json';sp=a.work/'A/ascending-canonical3/OPTIMISTIC-CLOSURE.json';pp=a.work/'A/ASCENDING-CORRECTIONS-PROOF.md'
 require(sha(bp)==BASE and sha(np)==NATIVE and sha(sp)==STATIC and sha(pp)==PROOF,'source/proof/static pins')
 b,w,cert=json.loads(bp.read_text()),json.loads(np.read_text()),json.loads(sp.read_text());sr=(a.repo/b['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==b['source_sha256']==w['source_sha256'],'native pin');R=json.loads(sr)['native_roots'];C={n:chart(z)for n,z in w['charts'].items()}
 for i in range(N):require(C[f'L{i}']==chart({'kind':'span','rows':[R[i]]})and C[f'F{i}']==chart({'kind':'ann','rows':[R[i]]}),'native charts')
 bs,bt,_=replay(b,collect=True);stats,tr,_=replay(w,collect=True);bc=b['carrier_interface_before_operation'];cut=w['carrier_interface_before_operation'];bv,ba=bt[bc];v,at=tr[cut]
 U=sorted(set(range(N))-set(b['targets']));require(len(U)==65 and cut==bc+130==1213 and w['targets']==b['targets'],'actual native65 cut')
 pre=[];names=[]
 for i in U:
  n=f'ASC_NATIVE_RAW_{i}';names.append(n);pre += [['INIT',n,f'L{i}'],['ADD',f'X{i}',n]]
 require(w['operations']==pre+b['operations']+[['CLEAR',n]for n in names],'actual initial snapshots, unchanged old word and retirements')
 for n,z in bv.items():require(v[n]==z and C[at[n]]==C[ba[n]],('old cut row/chart unchanged',n))
 for i,n in zip(U,names):require(v[n]==1<<i and at[n]==f'L{i}','actual native raw snapshot')
 require(stats['movement_profile']==bs['movement_profile']and stats['counts']=={'INIT':166,'ADD':702,'MOVE':425,'CLEAR':166}and stats['dirty_CLEAR']==166,'complete native bank invoice')
 bad=copy.deepcopy(w);bad['operations'].remove(['ADD','X5','ASC_NATIVE_RAW_5']);_,badtr,_=replay(bad,collect=True);require(badtr[cut-1][0]['ASC_NATIVE_RAW_5']==0,'endpoint-pass/source-fail missing native capture')
 local=[sum(1<<j for j in range(N)if sum(x*y for x,y in zip(R[i],R[j]))==0)for i in range(N)];allmask=(1<<N)-1;case_reports={};dual_total=0
 expected_fields=['KEEP_C0','KEEP_C1','KEEP_C2','ZFIRST3','ZFIRST4','ZFIRST5']
 for label,cc in cert['cases'].items():
  fields=cc['fields'];require(fields==(expected_fields[3:]if label=='three_modes'else expected_fields if label=='six_first_retentions'else expected_fields+[n for n in bv if n.startswith('ASC_GROUP_')]),'actual globally granted fields')
  rows=[bv[n]for n in fields];require(all(z>>N==0 for z in rows),'pure-X observations');known=set(b['targets']);waves=[]
  while True:
   km=sum(1<<i for i in known);new=[i for i in range(N)if i not in known and fits([z&~(km|local[i])for z in rows],1<<i)]
   if not new:break
   waves.append(new);known.update(new)
  missing=sorted(set(range(N))-known);require(waves==cc['waves']and sorted(known)==cc['closure']and len(known)==cc['closure_count']and missing==cc['missing'],'exact feedback closure')
  require(len(cc['dual_witnesses'])==len(missing)and[z['receiver']for z in cc['dual_witnesses']]==missing,'one exact dual per missing demand')
  km=sum(1<<i for i in known);duals=[]
  for witness in cc['dual_witnesses']:
   i=witness['receiver'];z=int(witness['indistinguishable_input_delta_hex'],16)
   require(z&~allmask==0 and z>>i&1 and z&(km|local[i])==0,'dual changes demand and no granted raw input')
   require(all((row&z).bit_count()%2==0 for row in rows),'dual annihilates every actual granted row')
   require(witness['support']==[j for j in range(N)if z>>j&1],'literal witness support');duals.append(witness)
  dual_total+=len(duals);case_reports[label]={'fields':fields,'waves':waves,'closure':sorted(known),'closure_count':len(known),'missing_count':len(missing),'verified_dual_count':len(duals),'dual_witnesses':duals}
 require([case_reports[n]['closure_count']for n in ['three_modes','six_first_retentions','all_source_and_groups']]==[46,48,49]and dual_total==190,'exact closure counts and190 duals')
 # The final62 duals also apply to C's real fresh48 source under the same fixed-code grant.
 freshp=a.work/'C/canonical3-reset-source/LIBERATED-CACHED48-WORD.json';fresh=json.loads(freshp.read_text());_,ft,_=replay(fresh,collect=True);fv,fa=ft[fresh['carrier_interface_before_operation']]
 fresh_fields=fresh['source_interface']['proper_group_fields']+fresh['source_interface']['canonical_fields'];freshrows=[fv[n]for n in fresh_fields];known=set(fresh['targets']);freshwaves=[]
 while True:
  km=sum(1<<i for i in known);new=[i for i in range(N)if i not in known and fits([z&~(km|local[i])for z in freshrows],1<<i)]
  if not new:break
  freshwaves.append(new);known.update(new)
 require(freshwaves==[[5]]and len(known)==49,'fresh source fixed global code adds only5')
 for witness in cert['cases']['all_source_and_groups']['dual_witnesses']:
  z=int(witness['indistinguishable_input_delta_hex'],16);require(all((r&z).bit_count()%2==0 for r in freshrows)and z&sum(1<<i for i in known)==0,'same62 duals for fresh actual code rows')
 original={f'{p}{i}'for p in ['X','Y']for i in range(N)}
 result={'status':'PASS_INDEPENDENT_NATIVE65_BANK_AND190_STATIC_DUALS','source_word_sha256':BASE,'native65_word_sha256':NATIVE,'proof_sha256':PROOF,'static_receipt_sha256':STATIC,'native_source_sha256':b['source_sha256'],'native65_stats':stats,'native65_cut':cut,'native65_all_old_cut_rows_charts_unchanged':True,'actual_native_snapshot_roles':U,'native65_owned_rank':len(binary_basis(z for n,z in v.items()if n not in original)),'native65_whole_moment':record(moment(stats['movement_profile'])),'missing_native_capture_passes_endpoints_but_fails_source':True,'static_cases':case_reports,'dual_witness_count':dual_total,'fresh_canonical3_fixed_code_extension':{'word_sha256':sha(freshp),'initial_known_count':48,'globally_granted_actual_fields':fresh_fields,'waves':freshwaves,'closure_count':49,'same_final62_duals_verified':True,'scope':'Fixed globally granted code rows plus all separate native-local raw inputs and free decoded-point feedback. Does not exclude new source acquisition or changed earlier histories.'},'scope':'Native65 is a physical zero-MOVE source augmentation. Exact duals prove nondecodability in the stated fixed observation interface over every characteristic-two field/positive width, including nonlinear decoders. New source rows and paid future deliveries are outside this static claim. All five global foundations remain open; no all111 or kappa.'}
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k]for k in ['status','native65_stats','native65_owned_rank','dual_witness_count','fresh_canonical3_fixed_code_extension']},indent=2))
if __name__=='__main__':main()
