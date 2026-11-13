"""Root review: independent dense source, integer Gram minor, rational invoice."""
import argparse, gzip, hashlib, json
from pathlib import Path
from fractions import Fraction as F
from dense_engine import run, span
from source_review import rank
if not __debug__: raise SystemExit('Assertions required')
NATIVE='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
PARENT='a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc'
FULL='d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7'
def read(p,pin,compressed=False):
 raw=p.read_bytes();assert hashlib.sha256(raw).hexdigest()==pin
 return json.loads(gzip.decompress(raw) if compressed else raw)
def root3(n):
 support=[j for j in range(9) if n>>j&1]
 if len(support)==3:return [3*int(j in support)-1 for j in range(9)]
 assert len(support)==7
 missing=[j for j in range(9) if j not in support]
 return [3*(int(j==missing[0])-int(j==missing[1])) for j in range(9)]
def interval(profile):
 scale=10**24;out=[F(0),F(0)]
 for r,c in profile.items():
  assert r>=1
  target=r**199*scale**200
  lo,hi=0,r*scale+1
  while hi-lo>1:
   mid=(lo+hi)//2
   if mid**200<=target:lo=mid
   else:hi=mid
  assert lo**200<=target<(lo+1)**200
  bounds=[F(lo,scale),F(lo+1,scale)]
  if c<0:bounds.reverse()
  out=[x+c*y for x,y in zip(out,bounds)]
 return out

def main(a):
 manifest=read(a.bundle/'MANIFEST.json',a.manifest_sha)
 for row in manifest['files']:
  assert hashlib.sha256((a.bundle/row['path']).read_bytes()).hexdigest()==row['sha256']
 s=read(a.repo/'research/shared-wire-split-composition/data/final.json.gz',NATIVE,True)
 q=read(a.bundle/'source-evidence/rail-consumer.json.gz',PARENT,True)
 full=read(a.repo/'research/shared-wire-split-composition/FULL-RESULT.json',FULL)
 rows,den,loc,bill,_=run(q,list(map(span,q['frames'])))
 roles={int(k):v for k,v in q['source_role_map'].items()}
 host={s['live'][k]:(roles[b],roles[d]) for k,b,d in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};H=list(host)
 M=[[rows[b][host[j][1]]+den*int(i==j) for j in H] for i,(b,d) in host.items()]
 J=set(q['consumer']['selected_return_ports']);C={h for h,r in zip(H,M) if not any(r)}
 assert len(J)==31 and len(C)==24 and C<=J and rank(M)==58
 Bids={b for b,d in host.values()};pure=[]
 for h,(b,d) in host.items():
  assert all(rows[i][b]==den*int(i==b) for i in range(400))
  assert rows[d]==[den*int(j==d) for j in range(400)]
  assert all(rows[i][d]==0 for i in range(400) if i not in Bids and i!=d)
  writes=[(t,o) for t,o in enumerate(q['program']) if o[1]==d]
  assert all(o[0]=='MOVE' for t,o in writes)
  reads=[o for o in q['program'] if o[0] in ['ADD','COPY'] and o[2]==d]
  if len(writes)==1:
   assert writes[0][1][2:4]==[3,loc[d]] and all(o[4]==loc[d] for o in reads);pure.append(h)
 assert len(pure)==74
 normals={h:s['frames'][s['initial'][h]][0] for h in H}
 r3={h:root3(normals[h]) for h in H}
 allowed=lambda h,k:h!=k and (normals[h]&normals[k]).bit_count()%2==0
 optimum=[[sum(x*y for x,y in zip(r3[h],r3[k])) if h not in C and k not in J else 0 for k in H] for h in H]
 assert rank(optimum)==8
 for i,h in enumerate(H):
  assert M[i][i]==den*int(h not in J)
  for j,k in enumerate(H):
   assert allowed(h,k) or optimum[i][j]*den==18*M[i][j]
   assert (normals[h] in span(q['frames'][loc[host[k][1]]])) == ((normals[h]&normals[k]).bit_count()%2==0)
 frame=[0,7,20,27,36,46,57,111]
 assert set(frame)<=set(H)-J
 for h in frame:
  for k in frame:
   assert M[H.index(h)][H.index(k)]==den*int(h==k)
   assert not allowed(h,k)
 unreturned=[h for h in H if M[H.index(h)][H.index(h)]!=0];assert len(unreturned)==65
 get=lambda x:{int(k):F(v) for k,v in x.items()}
 T=get(full['invoice']['T']);P=get(full['invoice']['P']);native=get(full['native']['paid']);helpers=get(full['native']['helpers']);Q=bill['moves']
 keys=set(T)|set(P)|set(native)|set(helpers)|set(Q)
 limit={r:(T.get(r,0)-P.get(r,0))/18+native.get(r,0)-helpers.get(r,0)-Q.get(r,0) for r in keys}
 price=interval(limit);after=limit.copy();after[1]=after.get(1,0)-65;floor=interval(after)
 slope=interval({r:(T.get(r,0)-P.get(r,0))/18 for r in set(T)|set(P)})
 assert price[0]>26 and price[1]<F(261,10) and floor[1]<F(-389,10) and slope[1]<0
 negative={'allowing_own_diagonal_is_outside_ferry_class':not allowed(frame[0],frame[0]),'free_rank8_still_has65_nonzero_columns':sum(any(row[j] for row in optimum) for j in range(96))==65}
 assert all(negative.values())
 result={'status':'PASS_ROOT_GENERAL_FERRY_SOURCE_AND_TERMINAL_INVOICE_REVIEW','author_manifest_sha256':a.manifest_sha,'all400_source_inputs':True,'all96_B_columns_identity':True,'D_effects_only_at_own_D_and_B_bank':True,'pure_D_donors':pure,'parent_reverse_rank':58,'free_optimum_rank':8,'fixed_I8_frame':frame,'fixed_nonzero_diagonal_columns':65,'limiting_allowance_bounds':list(map(str,price)),'limiting_terminal_margin_bounds':list(map(str,floor)),'finite_m_slope_bounds':list(map(str,slope)),'negative_controls':negative,'method':'Dense common-denominator interpreter and fraction-free integer rank reused from independently authored root/B review; direct integer-scaled E8 roots and fresh 24-digit exact integer-root price enclosure. No author checker or author rank routine imported.','proof_scope':'Initial-line compensated ferries only; arbitrary free allowed L is algebraic. Terminal floor requires original D facets and no D-bearing retained record outside Hub and those facets. Full suffix transfer (not only B projection) required for any intermediate handoff. No source completion or new kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','free_optimum_rank','fixed_nonzero_diagonal_columns','limiting_terminal_margin_bounds','negative_controls']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--manifest-sha',required=True);main(p.parse_args())
