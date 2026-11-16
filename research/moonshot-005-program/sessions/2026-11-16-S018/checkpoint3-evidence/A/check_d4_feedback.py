"""Actual-y omission controls and complete prices for the feedback variants."""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('/workspace/scratch/b421dd0c4c1e/integer-mult-bounds'));p.add_argument('--word',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();raw=a.word.read_bytes();w=json.loads(raw);source=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(source).hexdigest()==w['source_sha256'];R=json.loads(source)['native_roots']
 e=load(a.repo/'research/moonshot-005-program/results/bit-leaf-capacity-quotient/author/check.py','feedback_check');price=load(Path(__file__).with_name('price_d4_cohort.py'),'feedback_price');_,_,report=e.replay(w,R);ops=w['operations'];f=w['cohort_feedback'];cases=[]
 cases += [('initial_y_precoat',k)for k in f['precoat_operations']]
 cases += [('primary_local_source',k)for k,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('X')and o[2]in{f'Y{i}'for i in f['primaries']}]
 cases += [('feedback_cell',k)for cell in f['feedback_cells']for k in range(cell['before_operation'],cell['after_operation'])]
 cases += [('raw_flag_capture',k)for k,o in enumerate(ops)if o[0]=='ADD'and o[2].startswith('D4_FB_RAW_')]
 cases += [('principal_reset',k)for k,o in enumerate(ops)if o[0]=='ADD'and o[1]in w['cohort']['fields']and o[2]in{'P3','P4','P5'}]
 cases += [('shared_field_descent',k)for k,o in enumerate(ops)if o[0]=='MOVE'and o[1]in w['cohort']['fields']and o[2]==w['cohort']['meet']]
 cases += [('source_quartet_term',k)for k,o in enumerate(ops)if o[0]=='ADD'and o[1].startswith('X')and int(o[1][1:])in w['cohort']['targets']and o[2]in{'P3','P4','P5'}]
 assert len(cases)==60;rejected=[]
 for kind,k in cases:
  z=copy.deepcopy(w);del z['operations'][k]
  try:e.replay(z,R)
  except(AssertionError,KeyError)as ex:rejected.append({'kind':kind,'index':k,'operation':ops[k],'failure':str(ex)[:160]or'222-column endpoint identity'})
  else:raise AssertionError(('accepted omission',kind,k))
 for cell in f['feedback_cells']:
  k=cell['before_operation'];z=copy.deepcopy(w);z['operations'][k:k+2]=z['operations'][k:k+2][::-1]
  try:e.replay(z,R)
  except(AssertionError,KeyError):rejected.append({'kind':'reversed_feedback_cell','index':k})
  else:raise AssertionError(('accepted reversed feedback',k))
 a.out.mkdir(parents=True,exist_ok=True);(a.out/'CONTROLS.json').write_text(json.dumps({'status':'PASS_63_CHANGING_HISTORY_SEMANTIC_CONTROLS','word_sha256':hashlib.sha256(raw).hexdigest(),'baseline':report,'rejected':rejected,'scope':'Author controls with credited retained native interpreter; all222 input columns, including independent original y.'},indent=2)+'\n')
 author=json.loads((a.word.parent/'RESULT.json').read_text());old=author['before']['movement_profile'];new=report['movement_profile'];new={str(k):v for k,v in new.items()};delta={int(k):new.get(k,0)-old.get(k,0)for k in old|new};delta={k:v for k,v in delta.items()if v};g={127:37,64:74,1:-74}
 for j in range(1,9):g[1+7*j]=g.get(1+7*j,0)+74;g[7*j]=g.get(7*j,0)-74
 lim=tuple(z/6 for z in price.moment(g));q=price.moment(new);S=author['full_cut_nonidentity_X_support'];result={'status':'PASS_CHANGING_HISTORY_D4_MOVEMENT','word_sha256':author['word_sha256'],'moment':price.record(q),'change':price.record(price.moment(delta)),'signed_profile_change':delta,'signed_rank_volume_change':sum(d*c for d,c in delta.items()),'limiting_room':price.record((lim[0]-q[1],lim[1]-q[0])),'direct_full_cut_support_baseline':{'completed_count':len(S),'completed_targets':S,'moment':price.record(price.moment({7:222,1:len(S)}))},'scope':'Full cut includes completed-Y X offsets. Future reset of mixed-Y owners requires the actual homogeneous map checked; pure-owner support alone is insufficient.'};(a.out/'PRICE.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS',author['word_sha256'],len(rejected),result['moment']['decimal'][0])
if __name__=='__main__':main()
