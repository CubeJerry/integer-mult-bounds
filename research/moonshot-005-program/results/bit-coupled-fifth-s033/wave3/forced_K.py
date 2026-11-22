"""The complete old four-space remains forced at donor61 under variableD.
Literal H and four common frames are retained; arbitrary linear source maps.
"""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib
import numpy as np
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('s033_arithmetic',HERE.parent/'check.py');alg=importlib.util.module_from_spec(s);s.loader.exec_module(alg)
mm,rank,solve,read,save,need=[getattr(alg,k)for k in['mm','rank','solve','read','save','need']];BASE=Path('research/moonshot-005-program/results')
def main(repo,out):
 for p,h in read(HERE/'FORCED-K-SOURCE-PINS.json').items():need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==h,'source pin '+p)
 layout=read(repo/BASE/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');roots=np.array(layout['root_table'],dtype=np.int64);adj=[set(np.flatnonzero(v==0))for v in roots@roots.T];planes=[set(v)for v in layout['A2']];charts=[set(v)for v in layout['D4']]
 z=read(repo/BASE/'bit-source-d-interpolation-s032/INTERPOLATION.json.gz');L=np.array(z['common_frames'],dtype=np.uint8);K=mm(L,np.array(z['forced_K_coordinates_in_L'],dtype=np.uint8));need(rank(K)==4,'entire four-space')
 hf=read(repo/BASE/'bit-simultaneous-d1509-s032-independent/output/H-FIBRES.json.gz')['61'];source=read(repo/BASE/'bit-simultaneous-d1509-s032/output/SOURCES.json.gz');prot=list(range(48))+list(range(240,288));R=z['retained_receivers'];records=[]
 for hs,matrix in source['paired_maps']['61'].items():
  h=int(hs)
  if not planes[h]<=adj[95]:continue
  F=np.array(matrix,dtype=np.uint8)[:,prot];need(F.shape==(30,96),'all thirty source rows')
  parent=planes[h]<=charts[1509];parts=[];labels=[]
  for key,frame in sorted(hf.items()):
   center,r=map(int,key.split('/'))
   if r<111 and planes[h]<=adj[r]:
    A=np.array(frame,dtype=np.uint8);parts.append(A);labels.append(['native_H',center,r,A.shape[1]])
  H=np.hstack(parts)if parts else np.zeros((96,0),dtype=np.uint8)
  visible=[]
  if not parent:
   for t,r in enumerate(R):
    if planes[h]<=adj[r]:
     A=L[:,8*t:8*t+8];need(not np.any(mm(F,A)),'nonparent retained frame source image zero');parts.append(A);labels.append(['retained_D_zero',r,8]);visible.append(r)
  X=np.hstack(parts)if parts else np.zeros((96,0),dtype=np.uint8);C=solve(X,K);need(np.array_equal(mm(X,C),K),'whole forced K decomposition')
  records.append({'H':h,'D_parent':parent,'H_span_rank':rank(H),'prescribed_span_rank':rank(X),'retained_D_zero_views':visible,'generator_labels':labels,'K_coefficients':C.tolist(),'old_full_quotient_K_image':mm(F,K).tolist()})
 need(len(records)==16 and sum(v['D_parent']for v in records)==4,'all target-visible quotients')
 noH=[v for v in records if not v['D_parent']and not v['retained_D_zero_views']];need({v['H']for v in noH}=={333,906},'essential native H-only observation controls')
 # Authenticate the old literal proper-isolation conclusion on this wholeK.
 proper=read(repo/BASE/'bit-simultaneous-d1509-s032/output/PROPER.json.gz')['61']['95'];gauges=read(repo/BASE/'bit-simultaneous-d1509-s032/output/CONSTRAINED-GAUGES.json.gz');G=np.array(gauges['gauges']['61'],dtype=np.uint8);A=np.array(proper['matrix'],dtype=np.uint8);labels=[tuple(v)for v in proper['labels']];dw=read(repo/BASE/'bit-simultaneous-d1509-s032/output/D-WORD.json.gz');indices=[labels.index(tuple(dw['owners'][p][:3]))for p in z['D_inputs']['61']];Y=mm(A,mm(G,K));off=[q for q in range(len(labels))if q not in indices];need(not np.any(Y[off])and rank(Y[indices])==4,'old wholeK proper isolation')
 out.mkdir(parents=True,exist_ok=True);save(out/'FORCED-K-CERTIFICATE.json.gz',{'K':K.tolist(),'quotient_decompositions':records,'old_target_ingress':Y[indices].tolist(),'old_off_D_rank':rank(Y[off])})
 result={'status':'PASS_FULL_SOURCE_VARIABLE_D_FORCED_FOUR_SPACE','forced_donor':61,'target_receiver':95,'forced_K_dimension':4,'target_visible_source_quotients':16,'parents_forced_by_H_alone':4,'nonparents_forced_by_H_and_zero_D_images':12,'all_source_quotient_rows_checked':30,'essential_H_only_nonparents':[333,906],'old_off_D_rank':0,'old_ingress_rank':4,'variable_D_allowed':True,'arbitrary_linear_full_source_recodings':True,'fixed_H_words_owners_and_four_literal_frames':True,'new_complete_kappa':False};save(out/'FORCED-K-RESULT.json',result);print(json.dumps(result,sort_keys=True))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path.cwd());p.add_argument('--out',type=Path,required=True);a=p.parse_args();main(a.repo.resolve(),a.out.resolve())
