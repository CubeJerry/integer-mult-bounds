#!/usr/bin/env python3
import importlib.util,sys,json
from pathlib import Path
h=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('three_head_base',h/'check.py');m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
i=m.eye(8);X={v:m.monomial([j^v for j in range(8)],[0]*8) for v in [1,2,4,7]}
def q(v):return m.M((i.scale((1,1))+X[v].scale((1,-1))).a,1).norm()
qa,qb,qc=q(1),q(2),q(4);S=m.monomial([0,4,1,5,2,6,3,7],[0]*8);B=qb@S
assert S.power(3)==i and S@qb@S.star()==qa
assert qa.star()@S@qb@S==S.power(2)
assert B.power(3)==qa@qb@qc and B.power(6)==X[7] and B.power(12)==i
assert [m.gaussian_rank(B.power(k)) for k in range(12)]==[0,1,2,3,2,1]*2
checks=[]
for v in [1,2]:
 av,bv,big=qa.tp(v),qb.tp(v),B.tp(v);iv=m.eye(8**v);z=m.zero(8**v)
 source=m.block([[bv,z,z,z],[iv,av,z,z],[z,z,bv,(av@bv).scale((-1,0))],[z,z,z,av]])
 pre=m.diagonal([S.tp(v),S.power(2).tp(v),S.tp(v),S.power(2).tp(v)])
 post=m.diagonal([iv,S.star().tp(v),iv,S.star().tp(v)])
 target=m.block([[big,z,z,z],[iv,big,z,z],[z,z,big,big.power(2).scale((-1,0))],[z,z,z,big]])
 assert post@source@pre==target
 checks.append({'width':v,'independent_inputs':4,'all_columns':True,'head_power_ranks':[m.gaussian_rank(big.power(k)) for k in range(6)]})
# Direct-sum chart dimensions, where a=0,b=1,c=2 and sevenbodyaxes3..9.
charts={'ground_c':{2},'line_ac':{0,2},'facet_b_perp':set(range(10))-{1},'hub':set(range(10))}
ranks=[len(charts['line_ac'])-len(charts['ground_c']),len(charts['facet_b_perp'])-len(charts['line_ac']),len(charts['hub'])-len(charts['line_ac'])]
assert ranks==[1,7,8]
assert charts['ground_c']<charts['line_ac']<charts['facet_b_perp']<charts['hub']
assert B.power(6)!=i # Ordinary translation must not be omitted as a scalar identity.
out={'status':'PASS_EXACT_THREE_HEAD_SPECTATOR_SOURCE','ordinary_cycle':[0,4,1,5,2,6,3,7],'head_rank_pattern_mod6':[0,1,2,3,2,1],'source_move_ranks':ranks,'sixth_power':'X_a X_b X_c, ordinary translation, not identity','twelfth_power_identity':True,'width_checks':checks,'additional_forward_half_ordinary_permutations':3,'array_volume_multiplier':'2^V for both source and targets, retained in physical compilation','scope':'Exact direct-sum source and all-column head gauge only; no completed caller or supplier.','new_kappa':False}
(h/'THREE-HEAD-RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
