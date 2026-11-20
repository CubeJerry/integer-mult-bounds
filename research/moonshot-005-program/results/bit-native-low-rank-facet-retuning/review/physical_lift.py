import argparse,ctypes,json,hashlib,sys,importlib.util,subprocess,tempfile
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser(description='Lift all 384 physical small kernel modes')
for name in ('repo','matrix','out'):p.add_argument('--'+name,type=Path,required=True)
p.add_argument('--emit-kernel',action='store_true');a=p.parse_args();repo=a.repo.resolve();here=Path(__file__).resolve().parent;root=repo/'research/moonshot-005-program/results';a.out.mkdir(parents=True,exist_ok=True)
temporary=tempfile.TemporaryDirectory(prefix='small-source-lifts-');tmp=Path(temporary.name);shared=tmp/'solve.so';libmath=tmp/'field.so'
subprocess.run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared','-I',str(root/'bit-native-rs-return-distance/author'),str(here/'solve_many.c'),'-o',str(shared)],check=True)
subprocess.run(['cc','-O3','-march=native','-std=c11','-fPIC','-shared',str(root/'bit-spread-rs-physical-word/author/gf64_matmul.c'),'-o',str(libmath)],check=True)
subprocess.run([sys.executable,'-I','-B',str(here.parent/'verify.py'),'--repo',str(repo),'--out',str(tmp/'gauges'),'--emit-gauges'],check=True)
sys.path.insert(0,str((root/'bit-spread-rs-physical-word/author').resolve()));from transfer import TABLE,INV,Arithmetic
ops=Arithmetic(libmath);w=96;n=111*w;d=2*w;anchors=4*w
orig=np.memmap(a.matrix,dtype=np.uint8,mode='r',shape=(n,n));X=np.load(tmp/'gauges/SMALL-GAUGES.npz');M=X['kernel'];gauge=X['Winv'];A=orig[anchors:,anchors:];B=orig[anchors:,:anchors];fields=[]
assert hashlib.sha256(memoryview(orig)).hexdigest()=='8b6eccaf6c6e371b85473a48c89a6a5c1f14968b2687ff3f56f76a56e4e4d3c9'
for rep in range(2):fields.append(np.vstack([M[j*d+rep*w:j*d+(rep+1)*w]for j in range(4)]))
RR=ops.matmul(B,np.hstack(fields));n0=len(A);R=RR.shape[1];concat=np.ascontiguousarray(np.hstack([A,RR]));solution=np.empty((n0,R),np.uint8);rows=np.empty(n0,np.uint32);cols=np.empty(n0,np.uint32);diag=np.empty(n0,np.uint8)
lib=ctypes.CDLL(str(shared)).solve_many;ptr=ctypes.c_void_p;lib.argtypes=[ptr,ctypes.c_size_t,ctypes.c_size_t,ptr,ptr,ptr,ptr,ptr,ptr];lib.restype=ctypes.c_int
assert lib(concat.ctypes.data,n0,R,TABLE.ctypes.data,INV.ctypes.data,rows.ctypes.data,cols.ctypes.data,diag.ctypes.data,solution.ctypes.data)==0
whole=[np.vstack([fields[r],solution[:,r*4*w:(r+1)*4*w]]) for r in range(2)];out0=[ops.matmul(orig,v)for v in whole];E=np.eye(d,dtype=np.uint8)
for i in range(4):
 stock=np.vstack([v[i*w:(i+1)*w] for v in whole]);change=ops.matmul(gauge[i]^E,stock)
 for rep in range(2):out0[rep][i*w:(i+1)*w]^=change[rep*w:(rep+1)*w]
assert not any(z.any()for z in out0)
if a.emit_kernel:np.savez_compressed(a.out/'FULL-SMALL-KERNEL.npz',one=whole[0],two=whole[1])
info={'native_donor_coordinates_per_replica_pair':2*n,'independent_full_kernel_columns':4*w,'all_physical_output_residuals':0,'kernel_hashes':[hashlib.sha256(z.tobytes()).hexdigest()for z in whole]};(a.out/'FULL-SMALL-KERNEL.json').write_text(json.dumps(info,indent=2)+'\n');print(info)
