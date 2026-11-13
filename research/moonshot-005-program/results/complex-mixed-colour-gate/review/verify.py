"""Independent rational source-column audit of the colour theorem."""
import argparse,collections,copy,hashlib,gzip,itertools,json,math
from pathlib import Path
from fractions import Fraction as F
from dense_engine import run,span
if not __debug__:raise SystemExit("Exact checks require Python without -O")
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p,pin):
 b=p.read_bytes();assert sha(b)==pin,(str(p),sha(b));return json.loads(gzip.decompress(b))
def rank(rows):
 basis={}
 for row in rows:
  d={i:F(v) for i,v in enumerate(row) if v}
  while d:
   p=min(d)
   if p not in basis:
    c=d[p];basis[p]={i:v/c for i,v in d.items()};break
   c=d[p]
   for i,v in basis[p].items():
    w=d.get(i,F(0))-c*v
    if w:d[i]=w
    elif i in d:del d[i]
 return len(basis)
def main(a):
 q=load(a.bundle/'source-evidence/rail-consumer.json.gz','a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc');w=load(a.bundle/'output/rail-exchange.json.gz','cb77301a8f402fcc0f8dc069faefa0f0b3c6dfaedb6122a5a7d65b04802e2514');s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz','2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883')
 rootproof=a.root_proof.read_bytes();assert sha(rootproof)=='f97c93f356c7afb998c236a38bdf9aab637fb2b1f4269a517139d9db7db74a4a'
 roles={int(k):v for k,v in q['source_role_map'].items()};host={s['live'][k]:(b,d) for k,b,d in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};ports=sorted(host)
 old,den,loc,bill,_=run(q,list(map(span,q['frames'])));new,dnew,ln,bn,_=run(w,list(map(span,w['frames'])))
 # Reverse receiver ordering relative to the root certificate.
 receivers=[roles[d] for j,(b,d) in sorted(host.items(),reverse=True)]+[roles[j+112] for j in reversed(s['live'])];assert len(set(receivers))==200
 for j,(b,d) in host.items():
  assert q['initial'][roles[j]]==q['initial'][roles[b]] and loc[roles[j]]==loc[roles[b]]==127
  assert q['initial'][roles[j+112]]==q['initial'][roles[d]]==3 and loc[roles[j+112]]==loc[roles[d]]
  assert all(old[r][roles[b]]==0 for r in receivers)
 gram=[];effective=[];events=[]
 for k,e in enumerate(q['program']):
  if e!=['MOVE',451,127,3,True]:continue
  end=next(t for t in range(k+1,len(q['program'])) if q['program'][t]==['CLEAR',451,3]);raw=collections.defaultdict(F)
  for z in q['program'][k+1:end]:assert z[0]=='ADD' and z[2]==451 and z[4]==3;raw[z[1]]+=F(z[3])
  beta=[raw[r] for r in receivers]
  # Exact derivative propagation checks every later operation and owner reuse.
  active=set(range(400))
  for z in q['program'][:k+1]:
   if z[0]=='INIT':active.add(z[1])
   elif z[0]=='CLEAR':active.remove(z[1])
  delta={r:F(0) for r in active};delta[451]=F(1)
  for z in q['program'][k+1:]:
   op,r=z[:2]
   if op=='INIT':delta[r]=F(0)
   elif op=='CLEAR':del delta[r]
   elif op=='MOVE':pass
   elif op=='SCALE':delta[r]*=F(z[2])
   elif op in ('ADD','COPY'):
    if op=='COPY':assert delta[r]==0
    delta[r]+=F(z[3])*delta[z[2]]
   else:raise AssertionError(op)
  actual=[delta[r] for r in receivers];assert actual==beta
  gram.append(beta);effective.append(actual);events.append(k)
 assert len(gram)==8 and rank(gram)==8
 H={j:[old[r][roles[j]] for r in receivers] for j in s['live']};hostcols=[H[j] for j in ports]
 assert rank(hostcols)==20 and rank(list(H.values()))==20 and rank(gram+hostcols)==28
 # H intersect W=0, so pair independence in H is equivalent to modulo-W independence.
 primitive={};pairw=[]
 for j in ports:
  v=H[j];g=math.gcd(*v);assert g;v=tuple(x//g for x in v)
  if next(x for x in v if x)<0:v=tuple(-x for x in v)
  assert v not in primitive;primitive[v]=j
 for i,j in itertools.combinations(ports,2):
  v,t=H[i],H[j];r=next(k for k,x in enumerate(v) if x);c=next(k for k in range(200) if v[r]*t[k]!=v[k]*t[r]);det=v[r]*t[c]-v[c]*t[r];assert det;pairw.append([i,j,receivers[r],receivers[c],det])
 assert len(pairw)==4560
 actualbad=[]
 for j,(b,d) in host.items():
  cols=[[new[r][roles[j]] for r in receivers],[new[r][roles[b]] for r in receivers]]
  if rank(cols)>1:actualbad.append(j)
 assert sorted(actualbad)==[1,106] and rank(gram+[H[1],H[106]])==10
 e=[[int(i==j) for j in range(6)] for i in range(6)];z=[0]*6;U1=[e[2],e[3]];U2=[e[4],e[5]];G=[e[2],z]
 assert rank(U1+G)==2 and rank(U2+G)==3
 assert rank(U1+[e[0],z])==rank(U2+[e[0],z])==3
 assert rank(U1+U1)==2 # one supported port or parallel projected columns permit this
 assert rank(U1+[z,z])==2
 controls={'rank_deficient_decoder_detected_on_second_port':True,'nonzero_decoder_inside_W_increases_pair_rank':True,'one_support_or_parallel_source_columns_can_evade':True,'zero_net_B_after_extra_cancellation_not_excluded':True,'new_direction_count_not_packet_count':True}
 # Full required original source-to-receiver rank104, independent of colour choice.
 target=[]
 for j in s['live']:
  v=[F(0)]*200;v[receivers.index(roles[j+112])]=F(1) if j in host else F(1,2);target.append(v)
 assert rank(target)==104
 out={'status':'PASS_INDEPENDENT_SOURCE_COLOUR_RANKS_AND_PROOF_PREMISES','root_proof_sha256':sha(rootproof),'parent_word_sha256':'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','exchange_word_sha256':'cb77301a8f402fcc0f8dc069faefa0f0b3c6dfaedb6122a5a7d65b04802e2514','method':'Full dense400 original-input replay shared with our source review; exact rational sparse elimination; reversed receiver ordering; original-coordinate pair minors, not root basis coordinates. No root matrix/rank routines imported.','receivers':receivers,'old_hosted_source_X_rank':20,'old_all104_source_X_rank':20,'old_source_B_receiver_columns_zero':True,'W_effective_rank':8,'raw_decoders_equal_effective_final_decoders_all8':True,'packet_down_events':events,'combined_rank':28,'H_intersect_W_dimension':0,'all96_hosted_nonzero_nonproportional':True,'all4560_pair_witnesses':pairw,'pair_witness_sha256':sha(json.dumps(pairw,separators=(',',':')).encode()),'actual_exchange_rank2_hosted_pairs':sorted(actualbad),'ports1_106_rank_mod_W':2,'complete_source_receiver_rank':104,'fixed_interface_new_receiver_directions_lower':76,'controls':controls,'scope':'Exact source premises for root allV one-mode and scalar k-mode proof. h_j are nonzero scalars, fixed old source quotient preserved. Net B cancellations/new acquisitions and changed earlier source require separate analysis;76 directions are not76 packets/calls.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','old_hosted_source_X_rank','old_all104_source_X_rank','W_effective_rank','raw_decoders_equal_effective_final_decoders_all8','combined_rank','actual_exchange_rank2_hosted_pairs','fixed_interface_new_receiver_directions_lower']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--bundle',type=Path,required=True);p.add_argument('--root-proof',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
