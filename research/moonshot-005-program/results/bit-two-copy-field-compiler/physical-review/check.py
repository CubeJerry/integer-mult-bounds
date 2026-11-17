#!/usr/bin/env python3
"""Fresh b=2 source audit for the separately frozen general-b cut theorem."""
from pathlib import Path
import hashlib,importlib.util,json,argparse
from fractions import Fraction

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/programme'))
 p.add_argument('--word',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/workers/A/two-copy-f4/output/WORD.json'))
 p.add_argument('--theorem-checker',type=Path,default=Path('/workspace/scratch/abe0e83e3d3b/workers/C/pair-source-audit/check.py'))
 p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'output');a=p.parse_args()
 pin='9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550'
 assert hashlib.sha256(a.word.read_bytes()).hexdigest()==pin
 spec=importlib.util.spec_from_file_location('frozen_general_b_cut',a.theorem_checker);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 g=m.mod(a.repo/m.GEOMETRY,'b2_independent_fraction_geometry')
 assert m.digest(a.repo/m.NATIVE)==m.PINS['native'] and m.digest(a.repo/m.GEOMETRY)==m.PINS['geometry']
 R=json.loads((a.repo/m.NATIVE).read_bytes())['native_roots'];w=json.loads(a.word.read_bytes())
 C,V,P,stats,regions,audits=m.audit_source(w,2,R,g)
 assert w['carrier_interface_before_operation']==4010 and len(V)==812
 assert stats['counts']=={'INIT':368,'ADD':2872,'MOVE':992,'CLEAR':368}
 assert stats['movement_profile']=={1:326,2:238,4:206,7:222}and stats['owned_downward']=={1:72}and not stats['owned_upward']
 frames=m.check_frames(m.FRAMES,R,set(range(8,111))-m.TARGETS)
 h=m.mod(a.repo/m.ENTROPY,'b2_exact_dual');dual=json.loads((a.repo/m.DUAL).read_bytes());h.CORE=dual['roles'];h.ISO=dual['isolates'];ent=h.review_dual(dual,R)
 gate={127:37,64:74,1:-74}
 for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
 cap=tuple(v/6 for v in g.moment(gate));q=tuple(v/2 for v in g.moment(stats['movement_profile']));lin=(cap[0]-q[1]-17,cap[1]-q[0]-17);nonlin=(cap[0]-q[1]-Fraction(33,2),cap[1]-q[0]-Fraction(33,2))
 # For b=2: 8b + ceil(17b/2) = 16+17 =33, not34.
 result={'status':'PASS_INDEPENDENT_TWO_COPY_F4_CURRENT_CUT','word_sha256':pin,'general_b_checker_sha256':m.digest(a.theorem_checker),
 'copies':2,'cut':4010,'all_original_columns':444,'all_live_fields':812,'source_stats':stats,
 'all103_current_facet_audits':audits,'private_regions':regions,'private_arrival_floor':16,
 'remaining95_linear_downward_floor':18,'remaining95_nonlinear_downward_floor':17,
 'total_extra_linear_MOVE_floor':34,'total_extra_nonlinear_MOVE_floor':33,
 'normalized_source_moment':m.interval_record(q),'normalized_room_after_linear_floor':m.interval_record(lin),'normalized_room_after_nonlinear_floor':m.interval_record(nonlin),
 'nine_frame_witness_rechecked':frames,'Shannon_witness_terms':ent['terms'],
 'scope':'Fresh two-copy source premises for separately stated general-b private-region and95-role transcript theorem. Linear34 vs nonlinear33 MOVEs. No complete caller or supplier.'}
 a.out.mkdir(parents=True,exist_ok=True);m.save(a.out/'CERTIFICATE.json',result);m.save(a.out/'INDEPENDENT-CUT.json',[{'name':n,'chart':P[n],'rank':len(C[P[n]]),'row_hex':hex(v)}for n,v in sorted(V.items())])
 print(result['status'],'444columns812fields','linear34 nonlinear33','room',result['normalized_room_after_linear_floor']['decimal'][0])
if __name__=='__main__':main()
