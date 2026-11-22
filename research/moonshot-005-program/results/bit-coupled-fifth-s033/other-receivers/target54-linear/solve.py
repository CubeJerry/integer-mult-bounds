"""Exact linear necessary isolation constraints for target54; no whole fibre claim."""
from pathlib import Path
import argparse,importlib.util,json,hashlib,itertools
import numpy as np
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('s033_screen',HERE.parent/'screen.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
mm,rank,inverse,solve,read,save,need,null=s.mm,s.rank,s.inverse,s.solve,s.read,s.save,s.need,s.null
P=s.a.P;BASE=s.BASE

def main(repo,out):
 for p,h in read(HERE/'SOURCE-PINS.json').items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'source pin '+p)
 z=read(repo/BASE/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');dw=read(repo/BASE/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz');old=np.array(dw['matrix'],dtype=np.uint8);R=z['retained_receivers'];I={int(j):v for j,v in z['D_inputs'].items()};O={int(j):v for j,v in z['D_outputs'].items()};records=read(HERE.parent/'output/CERTIFICATE.json.gz');v=next(v for v in records if v['target']==54);W=np.array(v['L_coordinates'],dtype=np.uint8)
 fixed={(q,p)for q in set(sum(O.values(),[]))for p in[4,5,7,8]};free=[(q,p)for q in range(35)for p in range(35)if(q>=19 or p<19)and(q,p)not in fixed];findex={qp:k for k,qp in enumerate(free)};need(len(free)==833,'affine free count')
 equations=[];rhs=[];details=[];tight=[]
 for gate in v['donor_gates']:
  j=gate['donor'];M=np.array(gate['off_matrix'],dtype=np.uint8);blocks=[]
  for b,r in enumerate([9,48]):
   U=null(M[:,8*b:8*b+8]);wr=W[8*R.index(r):8*R.index(r)+8];need(U.shape[1]==rank(wr)==2,'two dimensional separate kernel');V=mm(inverse(old[np.ix_(O[r],I[j])]),U);A=null(wr.T).T;const=mm(mm(A,old[np.ix_(O[r],I[j])]),V)
   eq=np.zeros((12,833),dtype=np.uint8)
   for a in range(6):
    for b0 in range(2):
     for q,row in enumerate(O[r]):
      for p,col in enumerate(I[j]):
       k=findex.get((row,col))
       if k is not None:eq[2*a+b0,k]^=P[A[a,q],V[p,b0]]
   blocks.append({'receiver':r,'kernel':U.tolist(),'old_input_kernel':V.tolist(),'ann_W':A.tolist(),'equations':eq.tolist(),'rhs':const.reshape(-1).tolist()});equations.append(eq);rhs.append(const.reshape(-1))
  is_tight=gate['kernel_dimension']==4
  if is_tight:tight.extend([len(equations)-2,len(equations)-1])
  details.append({'donor':j,'joint_kernel_dimension':gate['kernel_dimension'],'separate_isolation_necessary':is_tight,'blocks':blocks})
 out.mkdir(parents=True,exist_ok=True);save(out/'LINEAR-EQUATIONS.json.gz',{'free_entries':free,'donors':details})
 results={}
 for name,idx in [('six_tight_necessary',tight),('all_eleven_separate_sufficient',list(range(len(equations))))]:
  A=np.vstack([equations[k]for k in idx]);b=np.hstack([rhs[k]for k in idx])[:,None];rr,piv=s.rref(np.hstack([A,b]));rk=rank(A);aug=rank(np.hstack([A,b]));results[name]={'equations':len(A),'rank':rk,'augmented_rank':aug,'dimension_if_consistent':833-rk if aug==rk else None,'consistent':aug==rk};print(name,results[name],flush=True)
  save(out/(name+'.json.gz'),{'matrix':A.tolist(),'rhs':b.tolist(),'rref':rr.tolist(),'pivots':piv})
  if aug==rk:
   xp=solve(A,b)[:,0];K=null(A);save(out/(name+'-PARAMETERS.json.gz'),{'particular':xp.tolist(),'homogeneous_kernel':K.tolist()})
 A=np.vstack([equations[k]for k in tight]);b=np.hstack([rhs[k]for k in tight])[:,None];late_rows=[q for q in O[9]if q>=19];E=np.zeros((833,len(late_rows)),dtype=np.uint8)
 for k,q in enumerate(late_rows):E[findex[q,22],k]=1
 multipliers=solve(A.T,E);need(np.array_equal(mm(A.T,multipliers),E),'four exact equation combinations');forced=mm(b.T,multipliers)[0];need(np.array_equal(forced,old[late_rows,22]),'literal section column forced zero');need(22 in I[0]and rank(old[np.ix_(O[9],I[0])])==8,'old valid section positive control')
 need(np.any(b),'old point violates new isolation equations');corrupt=multipliers.copy();corrupt[0,0]^=1;need(not np.array_equal(mm(A.T,corrupt),E),'elimination certificate corruption rejected')
 save(out/'FORCED-ZERO-COLUMN.json.gz',{'donor':0,'receiver':9,'input_coordinates':I[0],'output_rows':O[9],'zero_global_column':22,'local_kernel_coordinate':I[0].index(22),'late_output_rows':late_rows,'equation_combination_multipliers':multipliers.tolist(),'free_coordinate_targets':E.tolist(),'forced_delta_values':forced.tolist(),'old_column_values':old[late_rows,22].tolist()})
 results['universal_obstruction']={'status':'ALL_LITERAL_FOUR_READOUT_ISOLATING_D_POINTS_HAVE_SINGULAR_RETAINED_SECTION','donor':0,'receiver':9,'zero_global_column':22,'local_kernel_coordinate':I[0].index(22),'separate_full11_implied_by_necessary_tight6':True,'four_readout_rebasing_covered':False,'no_valid_D_in_this_affine_isolation_family':True,'new_complete_kappa':False}
 save(out/'RESULT.json',results)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
