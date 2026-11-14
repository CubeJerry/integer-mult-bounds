#!/usr/bin/env python3
"""Actual native sharp-potential and repeated-public-visit source controls."""
import argparse,copy,gzip,hashlib,importlib.util,json
from pathlib import Path
def module(p):
 z=importlib.util.spec_from_file_location('root_all_route_engine',p);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
def main(a):
 e=module(a.engine);need=e.need
 need(e.digest(a.native)=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin');n=e.read(a.native)
 ids=set(n['start'][:222]+n['final'][:222]);frames={str(k):n['frames'][str(k)] for k in ids};need(0 in ids and 1 in ids,'actual ground andHub')
 def template(prog,scope):return dict(schema='native-BIT-public-route-control-v1',public=222,owned_fields=0,hub=1,start=n['start'][:222],final=n['final'][:222],frames=frames,program=prog,end_owned=[],scope=scope)
 Xup=[['MOVE',i,n['start'][i],1] for i in range(111)];Yup=[['MOVE',111+i,0,n['final'][111+i]] for i in range(111)]
 wx=template([['MOVE',0,n['start'][0],0],['ADD',111,0,0],['MOVE',0,0,1]]+Xup[1:]+Yup,'OnlyY0 is complete; X0 uses a sharp downward excursion. No complete supplier.')
 wy=template(Xup+[['MOVE',111,0,1],['ADD',111,0,1],['MOVE',111,1,n['final'][111]]]+Yup[1:],'OnlyY0 is complete; its final own-facet arrival is downward. No complete supplier.')
 roots=[e.rref(n['frames'][str(c)]['B']) for c in n['start'][:111]]
 j=next(j for j in range(111) if all(not e.contained(roots[i],e.rref(n['frames'][str(n['final'][111+j])]['B'])) for i in [0,1]))
 f=n['final'][111+j];visit=[['MOVE',0,1,f],['MOVE',0,f,1]];swap=[['ADD',0,1,1],['ADD',1,0,1],['ADD',0,1,1]]
 wr=template(Xup+visit+swap+visit+swap+Yup,'All public values unchanged; one public X visits the same foreign facet with two independent values. No complete supplier.')
 words={'sharp_X_public_descent':wx,'sharp_Y_public_descent':wy,'same_public_record_repeated_facet':wr};receipts={};a.output.mkdir(parents=True,exist_ok=True)
 for name,w in words.items():
  re=e.replay(w,n);norm,G=e.normalize(w,n,re);expected={i:1<<i for i in range(222)}
  if name!='same_public_record_repeated_facet':expected[111]^=1
  need(re['val']==expected and re['loc']==dict(enumerate(n['final'][:222])),'all222 actual endpoints and values')
  need(norm['owned_moves']==0 and re['peak']==0,'no hidden owned record')
  target_rank=2 if name=='same_public_record_repeated_facet' else 1
  need(norm['historical_x_rank']==target_rank and norm['public_downward_moves']==target_rank,'actual independent public histories')
  need(dict(re['moves'])==({7:222,1:4} if target_rank==2 else {1:1,8:1,7:221}),'complete source tariff')
  if name=='sharp_Y_public_descent':
   need(not any(o[0]=='MOVE' and o[1]==111 and o[3]==n['final'][111] and len(re['frames'][o[2]])<7 for o in w['program']),'no own-facet upward anchor')
  blob=gzip.compress((json.dumps(w,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0);(a.output/(name+'.json.gz')).write_bytes(blob)
  receipts[name]=dict(word_sha256=hashlib.sha256(blob).hexdigest(),counts=dict(re['counts']),profile=dict(re['moves']),normalization=norm,all222_columns_and_endpoint_charts=True)
 # In the repeated-visit control, neither source line0 nor1 lies in the visited
 # facet. Collapsing its actual two arrival values to one loses a necessary
 # original-X history even if every originalY and localX is freely granted.
 facet=e.rref(n['frames'][str(f)]['B']);local=[1<<i for i in range(111) if e.contained(roots[i],facet)]
 need(not e.in_span(1,e.basis([2]+local+[1<<i for i in range(111,222)])),'last-visit-only normalization rejected')
 need(not e.in_span(2,e.basis([1]+local+[1<<i for i in range(111,222)])),'first-visit-only normalization rejected')
 out=dict(status='PASS_ACTUAL_NATIVE_PUBLIC_ROUTE_SHARPNESS_AND_REVISITS',native_sha256=e.digest(a.native),engine_sha256=e.digest(a.engine),receipts=receipts,repeated_facet_native_index=j,negative_controls=['collapse repeated physical record to its first arrival','collapse repeated physical record to its last arrival','assume every finalY has an upward own-facet anchor'],sharp_excursion='Each single-descent word has Q=222*7^t+(1+8^t-7^t), attaining the potential lower bound exactly.',classification='Three actual finite native partial words with scalar characteristic-two tensor identity lift; no complete111-target source.',new_kappa=None)
 (a.output/'RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(dict(status=out['status'],words=len(words),repeated_facet=j)))
if __name__=='__main__':
 p=argparse.ArgumentParser()
 for k in ['native','engine','output']:p.add_argument('--'+k,type=Path,required=True)
 main(p.parse_args())
