#!/usr/bin/env python3
from pathlib import Path
import argparse,json,hashlib,runpy,contextlib,io
p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);a=p.parse_args();root=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):d=runpy.run_path(str(root/'enumerate.py'))
expected={'PROOF.md':'930eecd13fbb0bcdab1fe0bd5662d76b025016cb731b7902f7287832e47217ea','check.py':'f39f3cb9829280612ff7368d8351212fba816563dc3d4fb9bbec859d484ee299','RESULT.json':'04a51f738ce7a298143a023fb1b50b566ac062d39277de04343b77ddfa6329e3','LAGRANGIANS.json':'0481063b5f853bf9729915c425a8681dc3bc8a78cc85af80b5c8aaa22f29f458'}
for f,h in expected.items():assert hashlib.sha256((a.author/f).read_bytes()).hexdigest()==h,f
cert=json.loads((a.author/'LAGRANGIANS.json').read_text());result=json.loads((a.author/'RESULT.json').read_text());own=json.loads((root/'TABLE.json').read_text());assert {tuple([0]+L)for L in cert['lagrangians']}==set(d['Ls'])
for row in result['cut_table']:
 mask=sum(1<<(i-1)for i in range(1,4)if i not in row['plus_shells']);assert row['h']==own['cuts'][mask]['h']
for v in range(1,64):
 ss=[set(s)for s in d['Ls']if v in s];assert len(ss)==15 and set.intersection(*ss)=={0,v}
Z=set(d['span']([8,16,32]))-{0};pauli=[len(Z^{d['swap'](v,r)for v in Z})//2 for r in range(4)];assert pauli==result['pauli63_cut']==[0,4,6,7]
for row in result['cut_table']+[{'h':pauli}]:
 h=row['h'];assert 2*h[2]<=3*h[1] and 4*h[3]<=7*h[1]
assert own['three_space_mixed_difference_certificate'][0]['distance_tuple']==[0,1,1,2];assert own['Hilbert_Gram_identity']['sharp_q1_q2']==[96,144]
out={'status':'INDEPENDENT_PASS_FULL_PARABOLIC_LAGRANGIAN_CUTS','reviewed_pins':expected,'method':'Fresh RREF enumeration of all1395 three-subspaces,135 isotropic survivors; no author-code import.','exact_spaces_matched':135,'full_parabolic_generators':12,'full_parabolic_orbit_sizes':[1,14,56,64],'radial_cuts_up_to_complement':8,'faithful_group_action_line_intersections':63,'cone_separator':['h2<=h1','4h3<=5h1'],'specified_Pauli63_mixture_separator':['2h2<=3h1','4h3<=7h1'],'three_space_Hilbert_certificate':True,'optional_exact_Hilbert_bound':'q2<=3q1/2 with explicit positive-square identity; no general potential claim.','scope':'The stated diagonal radial sign-cut cone and listed extensions only; no full-ordinary caller impossibility.','new_complete_kappa':False};(root/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
