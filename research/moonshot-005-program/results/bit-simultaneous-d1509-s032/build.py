"""Materialize a simultaneous four-receiver source change on the actual owners.

S031 source/H/D construction and S032 constrained-gauge lemma. @CubeJerry,
with substantial OpenAI assistance. Apache-2.0. No complete supplier claim.
"""
from pathlib import Path
import argparse,importlib.util,json,gzip,hashlib,shutil
import numpy as np

here=Path(__file__).parent
sp=importlib.util.spec_from_file_location('s032_frames',here/'explore.py')
ex=importlib.util.module_from_spec(sp);sp.loader.exec_module(ex)

def save(p,obj):
 raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode()
 p.write_bytes(gzip.compress(raw,mtime=0));return hashlib.sha256(raw).hexdigest()

def main(repo,out):
 g,a,oldsrc,ph,dw=ex.load(repo)
 old=repo/'research/moonshot-005-program/results/bit-shared-h-s031-construction/native-d1509-all-native/output'
 gg=ex.read(here/'output/CONSTRAINED-GAUGES.json.gz')
 oldearly=ex.read(old/'EARLY.json.gz');fr=ex.read(here/'output/FRAMES.json.gz')
 R=gg['receivers'];L=np.array(gg['common_frames'],dtype=np.uint8)
 assert R==[6,9,48,73] and L.shape==(96,32) and a.rank(L)==32
 prot=list(range(48))+list(range(240,288));LF=np.zeros((480,32),dtype=np.uint8);LF[prot]=L
 assert np.array_equal(LF[:,:8],np.array(oldsrc['selected_original_space'],dtype=np.uint8))
 maps={};late={};early={};checks=[]
 for j0,GM in gg['gauges'].items():
  j=int(j0);G=np.array(GM,dtype=np.uint8);assert a.rank(G)==96
  C=np.array(gg['fixed_subspaces'][j0],dtype=np.uint8)
  U=np.hstack([np.array(fr[j0][str(i)],dtype=np.uint8)for i in R])
  assert np.array_equal(a.mm(G,C),C) and np.array_equal(a.mm(G,L),U)
  GG=np.eye(480,dtype=np.uint8);GG[np.ix_(prot,prot)]=G
  maps[j0]={h:a.mm(np.array(M,dtype=np.uint8),GG).tolist()for h,M in oldsrc['paired_maps'][j0].items()}
  late[j0]={h:a.mm(np.array(M,dtype=np.uint8).reshape(-1,480),GG).tolist()for h,M in oldsrc['late_parities'][j0].items()}
  early[j0]={'matrix':a.mm(np.array(oldearly[j0]['matrix'],dtype=np.uint8),GG).tolist(),
             'physical_matrix':a.mm(np.array(oldearly[j0]['physical_matrix'],dtype=np.uint8),GG).tolist(),
             'row_owners':oldearly[j0]['row_owners']}
  # Exact factorizations preserve all complete views, phase frames and pure
  # inverse dimensions, rather than replacing a whole-view check by a section.
  for h,M in maps[j0].items():
   Q=np.array(oldsrc['frames'][f'{j}/{h}'],dtype=np.uint8)
   P=a.mm(Q,np.array(M,dtype=np.uint8))
   quota=sum(x[0]==int(h)for x in early[j0]['row_owners'])
   for row,(hh,owner) in enumerate(early[j0]['row_owners']):
    if hh==int(h):
     within=sum(t[0]==hh for t in early[j0]['row_owners'][:row])
     assert np.array_equal(np.array(early[j0]['physical_matrix'][owner],dtype=np.uint8),P[within])
   assert np.array_equal(P[quota:],np.array(late[j0][h],dtype=np.uint8).reshape(-1,480))
  checks.append({'donor':j,'gauge_rank':96,'fixed_H_and_old_receiver_space':C.shape[1],
                 'simultaneous_receiver_rank':32,'source_views_by_factorization':63})
  print('COMPOSED_SOURCE',j,flush=True)
 # The real H and D words, owners, cache lists and phase inverses are unchanged.
 out.mkdir(parents=True,exist_ok=True)
 source={'paired_maps':maps,'frames':oldsrc['frames'],'late_parities':late,
         'selected_original_space':oldsrc['selected_original_space'],
         'simultaneous_receivers':R,'simultaneous_original_space':LF.tolist()}
 save(out/'SOURCES.json.gz',source);save(out/'EARLY.json.gz',early)
 for name in ['H-PHYSICAL.json.gz','D-WORD.json.gz']:
  shutil.copyfile(old/name,out/name)
 result={'status':'PASS_FOUR_RECEIVER_D1509_CONSTRAINED_SOURCE_COMPOSITION',
         'receivers':R,'donors':sorted(map(int,maps)),'paired_source_bank':480,
         'common_entire_fibre_dimension_per_receiver':8,'joint_common_frame_rank':32,
         'bank_repeats':8,'full_bank_fibre_dimension_per_receiver':64,
         'retained_common_H':[263,642],'physical_H_modules':280,'D_word_unchanged':True,
         'source_checks':checks,'geometric_source_views':693,'native_source_views':639,
         'full_actual_early_bases':11,'source_propagation_bounds_unchanged':True,
         'full_global_supplier':False,'all_D_receivers':False,'new_complete_kappa':False}
 (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(result['status'],4,11,8,32,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'))
 p.add_argument('--out',type=Path,default=here/'output');q=p.parse_args()
 main(q.repo.resolve(),q.out.resolve())
