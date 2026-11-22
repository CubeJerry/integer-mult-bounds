"""Certify the first tangent direction as a rational one-parameter lift."""
from pathlib import Path
import runpy,json,numpy as np,gzip
here=Path(__file__).parent;v=runpy.run_path(str(here/'tangent.py'));g,a,T,ci,R,J,I,O,systems=[v[k]for k in ['g','a','T','ci','R','J','I','O','systems']];cand=v['candidate'];d=np.array(cand['delta_D'],dtype=np.uint8);assert a.rank(d)==1;blocks=[];allzero=True
for j in J:
 for t,r in enumerate(R):assert a.rank(np.vstack([s['receiver_ingress_to_quotient_maps'][t]for (jj,h),s in systems.items()if jj==j]))==8
for (j,h),s in systems.items():
 c=s['H_observation_core'].shape[1];NN=s['relation_kernel'];groups={}
 for t,r in enumerate(R):
  D=d[np.ix_(O[r],I[j])];B=a.mm(ci[j,r],D);alpha=int(np.bitwise_xor.reduce(np.diag(B)));V=a.mm(a.mm(a.mm(s['receiver_ingress_to_quotient_maps'][t],B),ci[j,r]),NN[c+8*t:c+8*t+8]);groups.setdefault(alpha,np.zeros_like(V));groups[alpha]^=V
 ok=all(not np.any(M)for M in groups.values());allzero&=ok;blocks.append({'donor':j,'H':h,'groups':{alpha:M.tolist()for alpha,M in groups.items()},'all_groups_zero':ok})
oldowners=v['read'](v['four']/'output/D-WORD.json.gz')['owners'];geomJ=sorted(a.charts[1509]);geomR=[r for r in range(120)if a.charts[1509]<=a.adj[r]];poles=set();all144=0
for j in geomJ:
 ij=[q for q,x in enumerate(oldowners)if x[3]is not None and j in a.planes[x[3]]]
 for r in geomR:
  oo=[q for q,x in enumerate(oldowners)if x[5]is not None and r in a.planes[x[5]]];C=T[np.ix_(oo,ij)];D=d[np.ix_(oo,ij)];B=a.mm(g.inverse(C,a),D);alpha=int(np.bitwise_xor.reduce(np.diag(B)))
  if alpha:poles.add(int(g.inverse(np.array([[alpha]],dtype=np.uint8),a)[0,0]))
  all144+=int(a.rank(C^D)==8)
phase_poles=set()
for sl in [slice(0,19),slice(19,35)]:
 C=T[sl,sl];D=d[sl,sl];B=a.mm(g.inverse(C,a),D);alpha=int(np.bitwise_xor.reduce(np.diag(B)))
 if alpha:phase_poles.add(int(g.inverse(np.array([[alpha]],dtype=np.uint8),a)[0,0]))
result={'status':'EXACT_RANK_ONE_PARAMETER_LIFT'if allzero else'TANGENT_WITH_UNRESOLVED_RATIONAL_RESIDUAL','changed_D_coefficients':[[int(i),int(j),int(d[i,j])]for i,j in zip(*np.nonzero(d))],'rank_one_denominator_groups_zero_all44':bool(allzero),'stacked_parent_ingress_maps_rank8_all44':True,'geometric_sections_at_t1':all144,'geometric_sections_total':len(geomJ)*len(geomR),'all_geometric_section_poles':sorted(poles),'phase_poles':sorted(phase_poles),'nonzero_parameters_preserving_all_D_sections_and_phases':[t for t in range(1,64)if t not in poles|phase_poles],'t1_source_quotients_changed':[key for key,D in cand['source_protected_delta'].items()if np.any(D)],'full_source_rank_checks':False,'new_complete_kappa':False};(here/'LIFT-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(here/'LIFT-CERTIFICATE.json.gz').write_bytes(gzip.compress((json.dumps({'grouped_relation_coefficients':blocks},sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0));print(json.dumps(result),flush=True)
