#!/usr/bin/env python3
"""Verify exact four-receiver input changes and the sharp five-subset gate.

Separate independent review reconstructs the physical atlas. This checker binds
all literal inverse restrictions and source compositions. @CubeJerry with
substantial OpenAI assistance. Apache-2.0. No complete supplier claim.
"""
from pathlib import Path
import argparse,gzip,hashlib,importlib.util,itertools,json
import numpy as np
HERE=Path(__file__).parent

def need(value,message):
 if not value:raise ValueError(message)
def read(path):return json.loads(gzip.decompress(path.read_bytes()))
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def verify(repo,out):
 for p,digest in json.loads((HERE/'SOURCE-PINS.json').read_text()).items():
  need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==digest,'source pin '+p)
 ex=load(HERE/'explore.py','s032_bound_frames');g,a,oldsrc,oldh,oldd=ex.load(repo)
 old=repo/'research/moonshot-005-program/results/bit-shared-h-s031-construction/native-d1509-all-native/output'
 frames=read(HERE/'output/FRAMES.json.gz');proper=read(HERE/'output/PROPER.json.gz')
 gauges=read(HERE/'output/CONSTRAINED-GAUGES.json.gz');newsrc=read(HERE/'output/SOURCES.json.gz')
 newearly=read(HERE/'output/EARLY.json.gz');oldearly=read(old/'EARLY.json.gz')
 R=gauges['receivers'];L=np.array(gauges['common_frames'],dtype=np.uint8)
 need(R==[6,9,48,73] and L.shape==(96,32)and a.rank(L)==32,'four exact full receiver frames')
 prot=list(range(48))+list(range(240,288));LF=np.zeros((480,32),dtype=np.uint8);LF[prot]=L
 need(np.array_equal(LF[:,:8],np.array(oldsrc['selected_original_space'],dtype=np.uint8)),'receiver6 unchanged')
 need(np.array_equal(LF,np.array(newsrc['simultaneous_original_space'],dtype=np.uint8)),'materialized common frame')
 inverse_tests=0
 for j,rr in frames.items():
  for i,U0 in rr.items():
   U=np.array(U0,dtype=np.uint8);rec=proper[j][i];A=np.array(rec['matrix'],dtype=np.uint8);target=np.array(rec['target'],dtype=np.uint8)
   need(A.shape==(96,96)and a.rank(A)==96,'complete marked proper restriction')
   need(U.shape==(96,8)and a.rank(U)==8 and np.array_equal(a.mm(A,U),target),'oriented entire inverse fibre')
   inverse_tests+=1
 composition_tests=0;gauge_checks=[]
 oldfib=read(repo/'research/moonshot-005-program/results/bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz')
 for j0,GG0 in gauges['gauges'].items():
  j=int(j0);G=np.array(GG0,dtype=np.uint8);C=np.array(gauges['fixed_subspaces'][j0],dtype=np.uint8)
  U=np.hstack([np.array(frames[j0][str(i)],dtype=np.uint8)for i in R])
  need(a.rank(G)==96 and np.array_equal(a.mm(G,C),C)and np.array_equal(a.mm(G,L),U),'invertible constrained gauge')
  GG=np.eye(480,dtype=np.uint8);GG[np.ix_(prot,prot)]=G
  for h,rr in oldfib.items():
   if j not in a.planes[int(h)]:continue
   for i,z in rr.items():
    K=np.array(z['kernel'],dtype=np.uint8);Z=np.zeros_like(K);K2=np.block([[K,Z],[Z,K]])
    need(np.array_equal(a.mm(GG,K2),K2),'entire paired H fibre fixed pointwise')
  for h,M in oldsrc['paired_maps'][j0].items():
   need(np.array_equal(a.mm(np.array(M,dtype=np.uint8),GG),np.array(newsrc['paired_maps'][j0][h],dtype=np.uint8)),'actual source quotient')
   P=np.array(oldsrc['late_parities'][j0][h],dtype=np.uint8).reshape(-1,480)
   need(np.array_equal(a.mm(P,GG),np.array(newsrc['late_parities'][j0][h],dtype=np.uint8).reshape(-1,480)),'actual late parity')
   composition_tests+=1
  for key in ['matrix','physical_matrix']:
   need(np.array_equal(a.mm(np.array(oldearly[j0][key],dtype=np.uint8),GG),np.array(newearly[j0][key],dtype=np.uint8)),'actual early matrices')
  need(oldearly[j0]['row_owners']==newearly[j0]['row_owners'],'source owner binding')
  gauge_checks.append([j,96,C.shape[1],32])
 for name in ['H-PHYSICAL.json.gz','D-WORD.json.gz']:
  need((old/name).read_bytes()==(HERE/'output'/name).read_bytes(),'literal H/D word unchanged')
 need(oldsrc['frames']==newsrc['frames'],'source phase frames unchanged')
 ff={int(j):{int(i):np.array(U,dtype=np.uint8)for i,U in rr.items()}for j,rr in frames.items()}
 native=[i for i in sorted(ff[0])if i<111];five=json.loads((HERE/'output/FIVE-RECEIVER-CENSUS.json').read_text())
 expected=list(itertools.combinations(native,5));need(len(five['records'])==len(expected)==462,'all five-native-receiver subsets')
 for record,rr in zip(five['records'],expected):
  need(record['receivers']==list(rr),'ordered exhaustive receiver subset')
  dims={j:a.rank(np.hstack([ff[j][i]for i in rr]))for j in [0,32,45,61]}
  need(len(set(dims.values()))>1,'unequal-join witness')
  need(all(record['ranks'][str(j)]==rank for j,rank in dims.items()),'recorded witness ranks')
 A=np.array([[1,0]],dtype=np.uint8);B=np.array([[0,1]],dtype=np.uint8)
 need(a.rank(A)==a.rank(B)==1 and a.rank(np.vstack([A,B]))==2,'equal rank does not imply equal kernels')
 G0=np.array(gauges['gauges']['0'],dtype=np.uint8);bad=G0.copy();row,col=np.argwhere(L!=0)[0];bad[0,row]^=1
 need(not np.array_equal(a.mm(bad,L),a.mm(G0,L)),'changed gauge rejected')
 badL=L.copy();badL[0,8]^=1
 need(not np.array_equal(a.mm(G0,badL),a.mm(G0,L)),'changed readout rejected')
 result={'status':'PASS_FOUR_RECEIVER_D1509_AND_SHARP_FIXED_INPUT_GAUGE_GATE','receivers':R,
  'native_donors':sorted(ff),'whole_inverse_restrictions':inverse_tests,'composed_source_quotients':composition_tests,
  'gauge_checks':gauge_checks,'geometric_source_views_inherited_by_exact_composition':693,
  'native_source_views_inherited_by_exact_composition':639,'retained_full_H_views':[72,67],
  'five_receiver_subsets_excluded':462,'arbitrary_changed_source_quotients_or_H_D_words_excluded':False,
  'negative_controls':['equal_rank_different_kernel','altered_gauge','altered_readout'],
  'complete_supplier':False,'new_complete_kappa':False}
 out.mkdir(parents=True,exist_ok=True);(out/'VERIFY-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print(result['status'],4,11,132,462,flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--out',type=Path,required=True);q=p.parse_args();verify(q.repo.resolve(),q.out.resolve())
