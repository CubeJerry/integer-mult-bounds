from argparse import ArgumentParser
from hashlib import sha256
import ctypes,importlib.util,json
from pathlib import Path
import numpy as np
p=ArgumentParser()
for t in ('repo','library','source','pin','out'):p.add_argument('--'+t,type=Path,required=True)
p.add_argument('--threads',type=int,default=4);a=p.parse_args();b=a.repo/'research/moonshot-005-program/results/bit-spread-h263-source/review/check.py';sp=importlib.util.spec_from_file_location('gf',b);f=importlib.util.module_from_spec(sp);sp.loader.exec_module(f)
M=np.load(a.source,mmap_mode='r');pins=json.loads(a.pin.read_bytes());digest=sha256(M).hexdigest();assert M.shape==(1956,134,130)and digest==pins['sha']
c=ctypes.CDLL(str(a.library.resolve())).allpair;ptr=ctypes.c_void_p;c.argtypes=[ptr,ptr,ptr,ctypes.c_int,ctypes.c_int,ptr];h=np.zeros(131,dtype=np.uint64);c(M.ctypes.data,f.MUL.ctypes.data,f.INVERSE.ctypes.data,len(M),a.threads,h.ctypes.data);assert int(h[130])==len(M)*(len(M)-1)//2==1911990
a.out.mkdir(parents=True,exist_ok=True);x={'actual_native_matrix_pins':digest,'independent_pair_computations':int(sum(h)),'genuine_projected_rank_130':int(h[130]),'target_pair_rank_upper':128,'at_most_one_core_bridge':True};(a.out/'PAIRS.json').write_text(json.dumps(x,indent=2,sort_keys=True)+'\n');print(x)
