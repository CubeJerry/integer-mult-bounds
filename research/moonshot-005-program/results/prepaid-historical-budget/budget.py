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
 raw=path.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'invoice pin');z=json.loads(raw);T={int(k):v for k,v in z['T4'].items()};P={int(k):v for k,v in z['P4'].items()};O={1:20,2:9,3:2,4:13,5:2,6:1};S={1:6,2:4,3:1,4:1,5:1,6:1};F={2:3,5:1};A={3:3,6:1};q={r:root(r**199*D**200) for r in set(T)|set(P)|set(O)}
 def moment(h):return [sum(v*q[r] for r,v in h.items()),sum(v*(q[r]+1) for r,v in h.items())]
 for r,v in O.items():P[r]=P.get(r,0)+18*(v-S.get(r,0))
 for r,v in A.items():P[r]=P.get(r,0)+18*v
 tl,th=moment(T);pl,ph=moment(P);lo,hi=tl-ph,th-pl;fl,fh=moment(F);al,ah=moment(A);losslo,losshi=al-fh,ah-fl
 need(3*18*D<lo<hi<4*18*D,'three extra rank-one ceiling');need(losslo>0,'prepayment costs more than the four additional saved routes')
 return {'status':'PASS_CONDITIONAL_PREPAID_FOURTEEN_OWNED_PROFILE','prepaid_routes':A,'prepaid_moment_numerator_bounds':[str(al),str(ah)],'net_cost_versus_ten_free_helper_profile_numerator_bounds':[str(losslo),str(losshi)],'invoice_sha256':PIN,'exponent':'199/200','denominator':str(D),'saved_per_native':S,'four_additional_savings':F,'additional_saved_moment_numerator_bounds':[str(fl),str(fh)],'new_T':T,'new_P':P,'paid_count':sum(P.values()),'targets':sum(T.values()),'rank_surplus':sum(r*v for r,v in T.items())-sum(r*v for r,v in P.items()),'raw_margin_numerator_bounds':[str(lo),str(hi)],'additional_per_native_headroom':{'numerator_bounds':[str(lo),str(hi)],'denominator':str(18*D),'floor_rank_one_allowance':3},'scope':'Conditional invoice only: Four historical helper combinations are precomputed from actual cochart entry q inputs and their four transports are included. The ten earlier pointwise decoders and all complete native/caller tariffs remain conditional. No new kappa.'}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--invoice',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=run(a.invoice);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps(r,indent=2,sort_keys=True))
