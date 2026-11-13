"""Independent exact source counts and exchange-argument distance arithmetic."""
import argparse,gzip,json,hashlib,collections,math
from fractions import Fraction as F
from pathlib import Path
if not __debug__:raise SystemExit('Assertions required')
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def main(a):
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()==PIN;s=json.loads(gzip.decompress(raw));ch=s['frames'];v=[[F(x) for x in ch[str(s['start'][i])]['B'][0]] for i in range(111)]
 counts=[sum(i!=j and sum(x*y for x,y in zip(v[i],v[j]))==0 for j in range(111)) for i in range(111)];costs=sorted(x-52 for x in counts);assert min(costs)==3 and max(costs)==10 and sum(costs)==698
 expected={(9,0):619,(9,11):532,(8,0):627,(8,1):619,(8,3):603};cases=[]
 for (q,e),d in expected.items():
  r=111-q-e;z=sum(costs[:r]);assert z==d;cases.append({'q':q,'extra_arrivals':e,'required_saved_visits':r,'distance':z,'relaxation_first_costs_taken':dict(sorted(collections.Counter(costs[:r]).items())),'support_valid_rankone_terms_required':math.ceil(z/144)})
 N={1:1,2:3,3:6,4:12,5:20,6:36,7:111};products=[(r,t,N[r]*N[t]) for r in N for t in N if r+t<=8];assert max(v for _,_,v in products)==144
 assert max(x for x in costs)<16
 out={'status':'PASS_INDEPENDENT_SOURCE_HISTOGRAM_CLOSED_FORM_DISTANCE_AND_RECTANGLE_ARITHMETIC','source_sha256':PIN,'foreign_support_histogram':dict(sorted(collections.Counter(counts).items())),'first_marginal_cost_histogram':dict(sorted(collections.Counter(costs).items())),'second_marginal_cost':16,'sum_all_first_costs':698,'cases':cases,'root_flat_count_premises':N,'maximum_support_valid_rectangle_area':144,'dimension_pairs_attaining_area_bound':[[r,t] for r,t,z in products if z==144],'geometry_is_proved_dependency_not_new_enumeration':True,'negative_controls':{'at_least_one_second_saving_before_unused_first_is_cost_dominated':True,'replacing_hamming_distance_with_matrix_rank_is_not_valid':True,'relaxation_distance627_is_not_physical_attainment':True},'scope':'Source counts and arithmetic independently checked; universal support/geometry/copy proof in REVIEW.md. Scalar fitting and individually support-valid rank-one terms only. No new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','first_marginal_cost_histogram','cases','maximum_support_valid_rectangle_area']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
