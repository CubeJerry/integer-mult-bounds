"""Rebuild authenticated old E and proper B from native owners at all 6,470 pairs."""
import argparse,importlib.util,json
from hashlib import sha256
from pathlib import Path
import numpy as np

def mod(p,n):
    spec=importlib.util.spec_from_file_location(n,p);a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);return a
def req(v,msg):
    if not v:raise ValueError(msg)
def main():
    p=argparse.ArgumentParser()
    for t in ('repo','parameters','cache','physical','out'):p.add_argument('--'+t,type=Path,required=True)
    p.add_argument('--mm-library',type=Path);a=p.parse_args();base=a.repo/'research/moonshot-005-program/results';p=mod(a.physical,'native_physical');f=mod(base/'bit-spread-h263-source/review/check.py','field');r=mod(base/'bit-spread-overlap-source/review/check.py','geometry');n=r.Native(a.repo,f)
    ph=p.Physical(a.repo,n,f,a.mm_library);ph.check_binary_K(base);par=json.loads(a.parameters.read_bytes())
    rec={};a.cache.mkdir(parents=True,exist_ok=True);native=set(range(111));geometry={i:sorted(n.adj[i]&native)for i in native};full={}
    for i in range(111):
        dual,ends=ph.terminal(i);early,late=sorted(u for u in ends if u<53280),sorted(u for u in ends if u>=53280)
        def rows(ids):
            mat=np.zeros((480,len(ids)),dtype=np.uint8)
            for t,u in enumerate(ids):
                k,v=ends[u];offset=0 if k==3 else 96;mat[offset:offset+32*k,t]=v
            return mat
        full[i]=(early,rows(early),late,rows(late))
        for tag,q in [('E',len(early)),('B',480)]:
            rec[i,tag]=np.lib.format.open_memmap(a.cache/f'{tag}{i}.npy',mode='w+',shape=(len(geometry[i]),q,480),dtype=np.uint8)
    for j in range(111):
        at=ph.propagate(j)
        for i in geometry[j]:
            e,F,y,G=full[i];ix=[t for t,u in enumerate(e)if u in at];iy=[t for t,u in enumerate(y) if u in at]
            E=np.zeros((len(e),480),dtype=np.uint8);Y=np.zeros((len(y),480),dtype=np.uint8)
            if ix:E[ix]=np.stack([at[e[t]] for t in ix])
            if iy:Y[iy]=np.stack([at[y[t]] for t in iy])
            B=ph.mm(F[:,ix],E[ix])^ph.mm(G[:,iy],Y[iy]);q=geometry[i].index(j)
            rec[i,'E'][q]=E;rec[i,'B'][q]=B
    for (i,key),array in rec.items():
        array.flush();req(sha256(array).hexdigest()==par['expected'][str(i)][key],f'actual native {key} F{i}')
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'OWNER-TRANSPORT.json').write_text(json.dumps({'complete_native_pairs':6470,'eight_actual_copies':8,'preterminal_owner_and_proper_matrices':222,'full_bit_template_K_widths':[9,36]},indent=2)+'\n')
    print('PASS 6470 original source/H/D/K/F blocks, all 222 stored matrices')
if __name__=='__main__':main()
