import argparse,ctypes,importlib.util,sys,json
from pathlib import Path
import numpy as np
p=argparse.ArgumentParser()
for n in ('replay','engine','repo','h-words','d-words','k-words','stream-lib','out'):p.add_argument('--'+n,type=Path,required=True)
p.add_argument('--sector',required=True,choices=('small','large'));p.add_argument('--roles',default='0,1,2,3,4,5,6,7')
a=p.parse_args();spec=importlib.util.spec_from_file_location('stream',a.engine/'check.py');eg=importlib.util.module_from_spec(spec);spec.loader.exec_module(eg)
alg=eg.load_replay(a.replay);engine=eg.Engine(a.stream_lib);alg.mm=engine.mm;nat=alg.Native(a);cs=eg.Cascade(nat,alg,engine,a.sector=='small')
w=cs.width;n=111*w;roles=list(map(int,a.roles.split(',')));r=len(roles);state=engine.lib.begin(n);lib=engine.lib
lib.quotient.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p];lib.quotient.restype=ctypes.c_int
try:
 for j in range(111):
  if j in roles:continue
  pkt=cs.columns(j)
  for t in range(0,w,64):
   b=pkt[t:t+64];alg.need(lib.consume(state,b.ctypes.data,len(b)),'quotient donor')
  if j%15==0:print('donor',j,flush=True)
 remaining=n-lib.present_rank(state);alg.need(remaining==r*w,'actual anchored quotient dimension')
 Ac=[];Ec=[]
 for j in roles:
  arr=cs.columns(j);emb=np.zeros_like(arr);emb[:,j*w:(j+1)*w]=np.eye(w,dtype=np.uint8)
  for pkt,lst in [(arr,Ac),(emb,Ec)]:
   quot=np.empty((w,remaining),dtype=np.uint8)
   for t in range(0,w,64):
    b=pkt[t:t+64];alg.need(lib.quotient(state,b.ctypes.data,len(b),quot[t:].ctypes.data),'quotient projection')
   lst.append(quot)
 qa=np.vstack(Ac).T.copy();qe=np.vstack(Ec).T.copy()
 a.out.mkdir(parents=True,exist_ok=True);np.savez_compressed(a.out/(a.sector.upper()+'.npz'),qa=qa,qe=qe,roles=roles)
finally:lib.finish(state)
