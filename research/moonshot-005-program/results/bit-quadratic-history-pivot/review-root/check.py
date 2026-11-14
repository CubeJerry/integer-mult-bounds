#!/usr/bin/env python3
"""Independent pivot replay, using the root reviewer's separate source engine."""
import argparse,gzip,hashlib,importlib.util,json
from pathlib import Path
PIN='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78'
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--package',type=Path,required=True);p.add_argument('--engine',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 spec=importlib.util.spec_from_file_location('independent_root_bit_replay',a.engine);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 raw=(a.repo/'research/paired-query-only-bit/retained/inputs/BIT-NATIVE-WORD.json.gz').read_bytes();v.need(hashlib.sha256(raw).hexdigest()==PIN,'native pin');native=json.loads(gzip.decompress(raw))
 pp=a.package/'output/PREFIX.json.gz';cp=a.package/'output/CLOSED-PARTIAL.json.gz';word=v.load(pp);closed=v.load(cp)
 for k,f in native['frames'].items():v.need(word['frames'][k]==f,'unchanged native frame')
 for k,f in word['frames'].items():
  if k not in native['frames']:v.need(v.qr(f['B'])==f['dim']and v.qr(f['A'])==8-f['dim']and all(v.dot(x,y)==0 for x in f['B']for y in f['A']),'exact new frame')
 v.need(word['start']==native['start'][:222]and word['public']==222,'original interface')
 R=[native['frames'][str(native['start'][i])]['B'][0]for i in range(111)];K=[sum(int(i==j or v.dot(r,s)==0)<<j for j,s in enumerate(R))for i,r in enumerate(R)]
 rows,loc,bill=v.replay(word);rr,ll,cbill=v.replay(closed)
 v.need(rows[334]==K[92]&K[54]and loc[334]==0,'ground quadratic');v.need(rows[333]==(1<<203)^K[92]^(1<<92),'actual dirty proper cache')
 C=word['frames'][str(loc[333])];v.need(C['dim']==6 and all(v.dot(b,R[i])==0 for b in C['B']for i in(92,54)),'proper cache chart')
 for i in range(111):
  y=(1<<(111+i))^((1<<i)if i==92 else 0)
  v.need(rows[i]==1<<i and loc[i]==native['final'][i]and rows[222+i]==1<<i and loc[222+i]==native['start'][i],'originals and copies')
  v.need(rows[111+i]==y and loc[111+i]==(native['final'][111+i]if i==92 else 0),'actual Y state')
  v.need(rr[i]==1<<i and rr[111+i]==y and ll[i]==native['final'][i]and ll[111+i]==native['final'][111+i],'complete partial222column endpoint')
 v.need(cbill['moves']=={1:28,2:32,5:32,6:27,7:164}and cbill['dirty_clears']==113,'paid closure')
 def cut(S):
  O=[r for j,r in rows.items()if any(all(v.dot(b,R[t])==0 for b in word['frames'][str(loc[j])]['B'])for t in S)];T=[(1<<t)|(1<<(111+t))for t in S];return len(v.basis(O)),len(v.basis(O+T))
 screen=cut((2,8,14,21,46,48,81,84));v.need(screen==(214,222),'actual all-column eight-cut')
 r={'status':'PASS_INDEPENDENT_ACTUAL_QUADRATIC_PIVOT','native_sha256':PIN,'prefix_sha256':hashlib.sha256(pp.read_bytes()).hexdigest(),'closure_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),'independent_engine_sha256':hashlib.sha256(a.engine.read_bytes()).hexdigest(),'prefix':bill,'closure':cbill,'cut_ranks':screen,'completed_targets':1,'input_columns':222,'no_new_kappa':True}
 a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
