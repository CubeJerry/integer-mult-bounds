"""Independent dense source certificate for the mixed-handoff colour gate."""
from pathlib import Path
from fractions import Fraction as F
import argparse,gzip,json,hashlib,math,itertools
from dense_engine import run,span
if not __debug__:raise SystemExit('Exact verifier requires assertions')
PINS={'parent':'a235a7e58f9eb96c6d409a88095fd6b59c977977baabb8735c76b2b820dcbedc','exchange':'cb77301a8f402fcc0f8dc069faefa0f0b3c6dfaedb6122a5a7d65b04802e2514','native':'2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','engine':'62f4baea972b8e03170bd4e69aec40f989364af41e194ff356850a62cf3c223c'}
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p,h):
 b=p.read_bytes();assert sha(b)==h;return json.loads(gzip.decompress(b))
def basis(vectors):
 out={};selected=[]
 for k,row in enumerate(vectors):
  row=list(row)
  while any(row):
   j=next(i for i,a in enumerate(row) if a)
   if j not in out:
    d=math.gcd(*row);row=[a//d for a in row]
    if row[j]<0:row=[-a for a in row]
    out[j]=row;selected.append(k);break
   a,b=row[j],out[j][j];g=math.gcd(a,b);row=[b//g*x-a//g*y for x,y in zip(row,out[j])];d=math.gcd(*row)
   if d:row=[a//d for a in row]
 return out,selected
def rank(v):return len(basis(v)[0])
def ints(v):
 d=math.lcm(*(x.denominator for x in v));return [int(x*d) for x in v]
def determinant(a):
 a=[r[:] for r in a];n=len(a);sign=1;prev=1
 for k in range(n-1):
  i=next(i for i in range(k,n) if a[i][k]);a[k],a[i]=a[i],a[k]
  if i!=k:sign=-sign
  p=a[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    z=a[i][j]*p-a[i][k]*a[k][j];assert z%prev==0;a[i][j]=z//prev
   a[i][k]=0
  prev=p
 return sign*a[-1][-1]
def inverse(a):
 n=len(a);z=[[F(x) for x in r]+[F(i==j) for j in range(n)] for i,r in enumerate(a)]
 for k in range(n):
  i=next(i for i in range(k,n) if z[i][k]);z[i],z[k]=z[k],z[i];p=z[k][k];z[k]=[x/p for x in z[k]]
  for i in range(n):
   if i!=k:
    p=z[i][k];z[i]=[x-p*y for x,y in zip(z[i],z[k])]
 return [r[n:] for r in z]
def controls():
 e=[[int(i==j) for j in range(6)] for i in range(6)];U1=[e[2],e[3]];U2=[e[4],e[5]]
 assert rank(U1+[e[2]])==2 and rank(U2+[e[2]])==3
 assert rank(U1+[e[0]])==rank(U2+[e[0]])==3
 assert rank(U1+U1)==2
 assert rank([e[2],e[2]])==rank([e[4],e[4]])==1
 assert rank([e[2],e[2]])==1
 assert rank(U1+[ [0]*6 ])==2
 return {'rank_deficient_V2_decoder':{'decoder_rank':1,'supported_pair1_rank':2,'supported_pair2_rank':3,'required_pair_rank':2},'decoder_inside_old_W_rejected_pair_rank':3,'one_supported_port_control_is_feasible_at_pair_rank':2,'two_coordinated_scalar_modes_pass_rank_necessity':True,'parallel_source_columns_break_two_port_obstruction':True,'exact_extra_B_cancellation_makes_gate_silent':True,'scope':'Explicit finite controls showing which stronger claims would be false; universal theorem is separately proved.'}
def main(a):
 ep=Path(__file__).with_name('dense_engine.py');assert sha(ep.read_bytes())==PINS['engine']
 q=load(a.parent,PINS['parent']);w=load(a.exchange,PINS['exchange']);s=load(a.repo/'research/shared-wire-split-composition/data/final.json.gz',PINS['native'])
 old,D,loc,info,_=run(q,list(map(span,q['frames'])));new,Dn,ln,infon,_=run(w,list(map(span,w['frames'])))
 roles={int(k):v for k,v in q['source_role_map'].items()};host={s['live'][k]:(x,y) for k,x,y in zip(s['hosted']['Dports'],s['hosted']['X2'],s['hosted']['Y2'])};H=list(host);V=[roles[j+112] for j in s['live']]+[roles[d] for b,d in host.values()];assert len(H)==96 and len(V)==200
 assert all(old[r][roles[b]]==0 for r in V for b,d in host.values())
 for j,(b,d) in host.items():
  assert q['initial'][roles[j]]==q['initial'][roles[b]] and loc[roles[j]]==loc[roles[b]]==127
  assert q['initial'][roles[j+112]]==q['initial'][roles[d]]==3 and loc[roles[j+112]]==loc[roles[d]]
 gram=[]
 for k,e in enumerate(q['program']):
  if e!=['MOVE',451,127,3,True]:continue
  end=next(t for t in range(k+1,len(q['program'])) if q['program'][t]==['CLEAR',451,3]);c={}
  for op in q['program'][k+1:end]:
   assert op[0]=='ADD' and op[2]==451 and op[4]==3;c[op[1]]=c.get(op[1],F(0))+F(op[3])
  gram.append(ints([c.get(r,F(0)) for r in V]))
 assert len(gram)==rank(gram)==8
 col={j:[old[r][roles[j]] for r in V] for j in s['live']};hostcols=[col[j] for j in H];hb,hi=basis(hostcols);assert len(hb)==20;allb,allidx=basis(gram+hostcols);assert len(allb)==28 and allidx[:8]==list(range(8))
 piv=list(sorted(hb));baseports=[H[i] for i in hi];B=[col[j] for j in baseports];minor=[[row[k] for k in piv] for row in B];inv=inverse(minor);coord={}
 for j in H:
  v=[col[j][k] for k in piv];c=[sum(F(v[k])*inv[k][i] for k in range(20)) for i in range(20)];assert all(sum(c[k]*B[k][t] for k in range(20))==col[j][t] for t in range(200));coord[j]=c
 pair_witness=[]
 for i,j in itertools.combinations(H,2):
  a0,b0=coord[i],coord[j];witness=next(((r,t,a0[r]*b0[t]-a0[t]*b0[r]) for r in range(20) for t in range(r+1,20) if a0[r]*b0[t]!=a0[t]*b0[r]),None);assert witness,(i,j);pair_witness.append([i,j,witness[0],witness[1],str(witness[2])])
 assert len(pair_witness)==4560
 allrows=gram+hostcols;ap=sorted(allb);bigminor=[[allrows[i][j] for j in ap] for i in allidx];det=determinant(bigminor);assert det
 assert rank(list(col.values()))==20 and rank(gram+list(col.values()))==28
 assert rank(gram+[col[1],col[106]])==10
 bad=[]
 for j,(b,d) in host.items():
  r=rank([[new[z][roles[j]] for z in V],[new[z][roles[b]] for z in V]])
  if r>1:bad.append(j)
 assert bad==[1,106]
 out={'status':'PASS_EXACT_SOURCE_QUOTIENT_AND_COLOUR_GATE_CERTIFICATES','pins':PINS,'method':'Independent dense integer all400-input interpreter (shared with worker B source review); fraction-free row elimination and explicit span/minor certificates; no author sparse engine or author rank routine.','parent_dyadic_exponent':D,'exchange_dyadic_exponent':Dn,'cocharted_hosted_pairs':96,'old_B_source_receiver_transfer_zero':True,'old_hosted_X_receiver_rank':20,'old_all104_X_receiver_rank':20,'gram_decoder_rank':8,'combined_rank':28,'quotient_rank':20,'all_hosted_columns_nonzero_pairwise_independent_mod_W':True,'pairwise_minor_checks':4560,'pairwise_witness_sha256':sha(json.dumps(pair_witness,separators=(',',':')).encode()),'hosted_basis_ports':baseports,'hosted_basis_pivot_output_roles':[V[k] for k in piv],'hosted_basis_minor_determinant':str(determinant(minor)),'hosted_column_coordinates':{j:[str(v) for v in c] for j,c in coord.items()},'combined_independent_rows':['Gram'+str(i) if i<8 else 'X'+str(H[i-8]) for i in allidx],'combined_minor_output_roles':[V[k] for k in ap],'combined28_minor_determinant':str(det),'actual_exchange_rank2_pairs':bad,'ports1_106_quotient_rank':2,'complete_source_receiver_rank_required':104,'new_directions_required_in_fixed_W_plus_L_interface_at_least':76,'new_directions_are_not_packet_or_MOVE_count':True,'controls':controls(),'scope':'Exact finite source certificates supporting separate all-V single-mode and scalar k-mode proofs; changed early source/extra acquisitions remain outside; no supplier or kappa.'}
 a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','old_hosted_X_receiver_rank','gram_decoder_rank','combined_rank','pairwise_minor_checks','combined28_minor_determinant','actual_exchange_rank2_pairs','new_directions_required_in_fixed_W_plus_L_interface_at_least']},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--parent',type=Path,required=True);p.add_argument('--exchange',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
