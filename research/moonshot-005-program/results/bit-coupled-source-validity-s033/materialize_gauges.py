"""Convert a full source-gauge certificate into literal protected source edits."""
from pathlib import Path
import argparse,importlib.util,gzip,json,numpy as np

def run(repo,gauges,out):
 p=Path(__file__).parent/'check.py';sp=importlib.util.spec_from_file_location('materialize_gauge',p);b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b);g,a,old,*_=b.load(repo);data=b.read(gauges);delta={}
 for j,G0 in data['source_right_gauges'].items():
  G=np.array(G0,dtype=np.uint8)
  if G.shape!=(96,96)or a.rank(G)!=96:raise ValueError('invertible96-dimensional gauge')
  for h,F0 in old['paired_maps'][j].items():
   F=np.array(F0,dtype=np.uint8)[np.ix_(b.PROWS,b.PROT)];delta[f'{j}/{h}']=(a.mm(F,G)^F).tolist()
 obj={'D_matrix':data['D_matrix'],'source_protected_delta':delta,'kind':'global_source_gauge'};raw=(json.dumps(obj,sort_keys=True,separators=(',',':'))+'\n').encode();out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(gzip.compress(raw,mtime=0)if out.suffix=='.gz'else raw);print('PASS_MATERIALIZED_GLOBAL_SOURCE_GAUGES',len(delta),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path('.'));p.add_argument('--gauges',type=Path,required=True);p.add_argument('--out',type=Path,required=True);q=p.parse_args();run(q.repo.resolve(),q.gauges.resolve(),q.out.resolve())
