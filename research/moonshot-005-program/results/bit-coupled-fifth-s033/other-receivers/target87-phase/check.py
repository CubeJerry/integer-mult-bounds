"""Exact receiver87 phase requirement; no global feasibility claim."""
from pathlib import Path
import argparse,importlib.util,hashlib,json
import numpy as np
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('s033_screen',HERE.parent/'screen.py');s=importlib.util.module_from_spec(sp);sp.loader.exec_module(s)
def main(repo,out):
 for p,h in s.read(HERE/'SOURCE-PINS.json').items():s.need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'source pin '+p)
 z=s.read(repo/s.BASE/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');I={int(k):v for k,v in z['D_inputs'].items()};O={int(k):v for k,v in z['D_outputs'].items()};T=np.array(s.read(repo/s.BASE/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz')['matrix'],dtype=np.uint8);v=next(v for v in s.read(HERE.parent/'two-frame-column-gates/output/CERTIFICATE.json.gz')['target_gates']if v['target']==87);E=[4,5];counts={j:[sum(p<19 for p in ii),sum(p>=19 for p in ii)]for j,ii in I.items()if set(E)<=set(ii)};s.need(counts=={0:[5,3],61:[6,2],62:[5,3]},'actual containing-profile phase counts');records=[]
 for r in[9,73]:
  B=np.array(next(x['forced_input_span']for x in v['input_union_gates']if x['receiver']==r),dtype=np.uint8);e=np.eye(35,dtype=np.uint8)[:,27:28];c=s.solve(B,e);early=[k for k,q in enumerate(O[r])if q<19];late=[k for k,q in enumerate(O[r])if q>=19];s.need(len(early)==len(late)==4,'actual row phase split');s.need(s.rank(T[np.ix_(O[r],E)][early])==2,'old literal profile early rank two');records.append({'receiver':r,'output_rows':O[r],'union_column27_coefficients':c.tolist(),'native_sections_containing27':[j for j,ii in I.items()if 27 in ii],'literal_profile_early_rank':2,'required_rebased_profile_early_rank':1})
 S=np.zeros((8,8),dtype=np.uint8)
 for col,row in enumerate([1,2,0,4,3,5,6,7]):S[row,col]=1
 s.need(s.rank(S)==8 and not np.any(S[:4,5:])and s.rank(S[:4,[2,3]])==1,'single-section sharp phase counterexample')
 out.mkdir(parents=True,exist_ok=True);s.save(out/'CERTIFICATE.json.gz',{'profile_columns':E,'native_input_phase_counts':counts,'records':records,'single_section_rank_eight_phase_example':S.tolist(),'single_section_global_input_order':I[0]});s.save(out/'RESULT.json',{'status':'EXACT_REBASED_RECEIVER87_PROFILE_MUST_HAVE_EARLY_RANK_ONE','native_donor0_phase_split':[5,3],'retained_output_phase_split':[4,4],'literal_readout_family_excluded':True,'rebased_family_excluded_by_this_test':False,'global_D_or_source_feasibility_claimed':False,'new_complete_kappa':False})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);q=p.parse_args();main(q.repo.resolve(),q.out.resolve())
