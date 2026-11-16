#!/usr/bin/env python3
"""One actual receiver chain and a finite12-cover bounding acyclic witnesses."""
import argparse,copy,hashlib,itertools,json
from pathlib import Path
from release_projection import N,chart,replay,require,rref
from price_projection import moment,record
PIN='dda004b1c3cae1c0d0cfb0d698c101963842db12d542fed842a82dbffc14ee44'
COVER=[[5,15,18,68,71,81,85],[13,17,31,53,84,101,103],[14,25,91,94,96,102],[24,26,66,72,90,92],[32,52,62,87,99,109],[34,58,60,82,97,105],[51,55,59,70,95,100],[33,56,57,63,83],[35,54,86,107],[88,93,106,108],[47,69,89],[98,104,110]]
def save(p,z):
 raw=(json.dumps(z,indent=2)+'\n').encode();p.write_bytes(raw);return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser()
 for n in ['repo','work','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();p=a.work/'C/canonical3-reset-source/LIBERATED-CACHED48-WORD.json';require(hashlib.sha256(p.read_bytes()).hexdigest()==PIN,'frozen source pin');b=json.loads(p.read_text());bs,bt,_=replay(b,collect=True);cut=b['carrier_interface_before_operation'];bv,ba=bt[cut]
 sr=(a.repo/b['source_path']).read_bytes();require(hashlib.sha256(sr).hexdigest()==b['source_sha256'],'native pin');R=json.loads(sr)['native_roots'];C={n:chart(z)for n,z in b['charts'].items()};U=sorted(set(range(N))-set(b['targets']))
 flat=[i for g in COVER for i in g];require(len(flat)==len(set(flat))==63 and sorted(flat)==U,'explicit twelve-group partition of all63 unknowns')
 native_sources={}
 for i in U:
  n=b['source_interface']['actual_native_raw_donor_caches'].get(str(i),f'X{i}');require(bv[n]==1<<i and ba[n]==f'L{i}','actual raw native observation for every unknown');native_sources[i]=n
 for g in COVER:
  for i,j in itertools.combinations(g,2):
   require(sum(x*y for x,y in zip(R[i],R[j]))==0,'exact pairwise orthogonality in each cover group')
   require(len(rref(C[f'L{i}']+C[f'F{j}'])[0])==len(rref(C[f'L{j}']+C[f'F{i}'])[0])==7,'both actual initial-chart access arcs')
 # Any acyclic induced witness contains at most one role from each cover group.
 owner='ASC_GROUP_4_74_78';require(bv[owner]==1<<5 and C[ba[owner]]==C['M1'],'actual retained raw5 at M1')
 w=copy.deepcopy(b);h='CANONICAL_FIRST_UNKNOWN_MEET';w['charts'][h]={'kind':'ann','rows':[R[i]for i in [4,74,78,5]]};H=chart(w['charts'][h]);require(len(H)==4 and len(rref(H+C['M1'])[0])==5 and len(rref(H+C['F5'])[0])==7,'actual rank4 meet below M1 and F5')
 chain=[['MOVE',owner,h],['MOVE','Y5',h],['ADD',owner,'Y5'],['MOVE','Y5','F5']]
 tail=copy.deepcopy(b['operations'][cut:]);require(tail.count(['MOVE','Y5','F5'])==1,'one old closing Y5 move');tail.remove(['MOVE','Y5','F5']);w['operations']=b['operations'][:cut]+chain+tail;nc=cut+4
 w.update(schema='canonical3-first-unknown49-actual-chain-v1',base_word_sha256=PIN,targets=sorted(set(b['targets'])|{5}),carrier_interface_before_operation=nc,scope='Actual first unknown receiver5 via retained raw5, one owned unit descent and a nested rank4 receiver chain. Three canonical modes, seven group values and54 native originals retained; the raw5 group changes chart. No all111 or kappa.')
 w['source_interface'].update(continuation_before_operation=nc,actual_additional_completed_unknowns=[5],remaining_raw_ground_Y_count=62,proper_group_chart_overrides={owner:h},all49_targets_at_native_facets=True)
 stats,tr,_=replay(w,collect=True);v,at=tr[nc];CC={n:chart(z)for n,z in w['charts'].items()}
 for n,z in bv.items():
  if n=='Y5':require(v[n]==z^(1<<5)and at[n]=='F5','actual first unknown completed')
  else:
   require(v[n]==z,'all old source values preserved')
   if n==owner:require(at[n]==h,'actual moved raw5 chart')
   else:require(CC[at[n]]==C[ba[n]],'all other actual source charts preserved')
 require(stats['counts']=={'INIT':115,'ADD':307,'MOVE':332,'CLEAR':115}and stats['dirty_CLEAR']==115,'complete49 invoice')
 require(stats['movement_profile']=={1:68,2:37,3:5,4:2,5:37,6:19,7:164},'complete49 movement profile')
 controls=[]
 for label,event in [('omit actual raw5 descent',chain[0]),('omit actual receiver read',chain[2])]:
  bad=copy.deepcopy(w);bad['operations'].remove(event)
  try:replay(bad)
  except ValueError as e:controls.append({'control':label,'rejected':str(e)})
  else:raise ValueError('invalid first-unknown control accepted')
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 gl,gh=moment(gate);q=moment(stats['movement_profile']);qb=moment(bs['movement_profile']);a.out.mkdir(parents=True,exist_ok=True);pin=save(a.out/'WORD.json',w)
 result={'status':'PASS_ACTUAL_FIRST_UNKNOWN49_AND_NATIVE12_COVER','source_word_sha256':PIN,'word_sha256':pin,'native_source_sha256':b['source_sha256'],'cut':nc,'stats':stats,'actual_receiver_chain':chain,'all_other_source_rows_and_charts_preserved':True,'ground_raw_basis_still48_not49':True,'whole_moment':record(q),'increment':record((q[0]-qb[1],q[1]-qb[0])),'necessary_limiting_room':record((gl/6-q[1],gh/6-q[0])),'native_observation_sources':native_sources,'orthogonal_partition_of_U63':COVER,'maximum_possible_initial_chart_acyclic_witness_upper_bound':12,'upper_bound_proof':'Every pair inside a listed group has two actual initial-chart access arcs, because both raw native observations exist. An acyclic induced set therefore has at most one vertex per group. The12 groups partition all63 unfinished roles of the frozen fresh48 cut. Adding other source-access arcs cannot remove these two-cycles. This is not a bound on stronger information inequalities or a completion construction.','controls':controls,'scope':'One actual chain reaches the static closure ceiling49 for the fixed seven-group source, while its62 terminal static duals still require new measurements or earlier histories. The acyclic-witness method cannot exclude the fresh48 movement margin by a >24 witness, since every such witness has size<=12. All five global foundations and full111 remain open; no kappa.'}
 save(a.out/'RESULT.json',result);print(json.dumps({k:result[k]for k in ['status','word_sha256','stats','whole_moment','necessary_limiting_room','maximum_possible_initial_chart_acyclic_witness_upper_bound']},indent=2))
if __name__=='__main__':main()
