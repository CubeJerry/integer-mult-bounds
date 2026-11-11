import argparse,json,hashlib
from pathlib import Path
D=10**15
PIN='b8adae359984f27f140db1fb3cf7e37f1f96a25bdb1cc586de6dca6b47534248'
def need(b,s):
 if not b:raise ValueError(s)
def root(n):
 a=0;b=1<<((n.bit_length()+199)//200)
 while b-a>1:
  m=(a+b)//2
  if m**200<=n:a=m
  else:b=m
 need(a**200<=n<(a+1)**200,'directed root');return a
def run(path):
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'invoice pin');z=json.loads(raw);T={int(k):v for k,v in z['T4'].items()};P={int(k):v for k,v in z['P4'].items()};O={1:20,2:9,3:2,4:13,5:2,6:1};S={1:6,2:4,3:1,4:1,5:1,6:1};F={2:3,5:1};q={r:root(r**199*D**200) for r in set(T)|set(P)|set(O)}
 def moment(h):return [sum(v*q[r] for r,v in h.items()),sum(v*(q[r]+1) for r,v in h.items())]
 for r,v in O.items():P[r]=P.get(r,0)+18*(v-S.get(r,0))
 tl,th=moment(T);pl,ph=moment(P);lo,hi=tl-ph,th-pl;fl,fh=moment(F)
 need(18*18*D<lo<hi<19*18*D,'18 extra rank-one ceiling')
 return {'status':'PASS_CONDITIONAL_FOURTEEN_OWNED_SKIP_PROFILE','invoice_sha256':PIN,'exponent':'199/200','denominator':str(D),'saved_per_native':S,'four_additional_savings':F,'additional_saved_moment_numerator_bounds':[str(fl),str(fh)],'new_T':T,'new_P':P,'paid_count':sum(P.values()),'targets':sum(T.values()),'rank_surplus':sum(r*v for r,v in T.items())-sum(r*v for r,v in P.items()),'raw_margin_numerator_bounds':[str(lo),str(hi)],'additional_per_native_headroom':{'numerator_bounds':[str(lo),str(hi)],'denominator':str(18*D),'floor_rank_one_allowance':18},'scope':'Conditional invoice only: all14 delta skips need actual source-safe physical observations, accumulators, retirement and complete native/caller tariffs. No new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--invoice',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.invoice);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
