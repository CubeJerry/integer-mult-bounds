import json,hashlib,argparse,types
from pathlib import Path

def basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return b

def contains(rows,x):
 b=basis(rows)
 while x:
  p=x.bit_length()-1
  if p not in b:return False
  x^=b[p]
 return True

def xor(xs):
 z=0
 for x in xs:z^=x
 return z
m=types.SimpleNamespace(basis=basis,rank=lambda rows:len(basis(rows)),contains=contains,xor=xor)
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'CERTIFICATE.json');args=p.parse_args()
assert hashlib.sha256(args.source.read_bytes()).hexdigest()=='4cea047c9f28a17c3379d3073a88b3a5d00e6e749214661c9d330a289824d060'
native=args.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
assert hashlib.sha256(native.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
w=json.loads(args.source.read_text());rr=json.loads(native.read_text())['native_roots'];M=(1<<111)-1;W=[int(z,16) for z in w['W_rows_hex']];D=list(m.basis([v for n,(c,v) in w['expected'].items() if n.startswith('C')]).values());A=D+W;loc=[sum(1<<j for j in range(111) if sum(a*b for a,b in zip(rr[i],rr[j]))==0) for i in range(111)];R=[m.xor(v for n,(c,v) in w['expected'].items() if n.startswith('C'+str(q)+'_')) for q in range(8)];B=[w['expected']['P0'][1],int(w['kernel_x_hex'],16),255]+R

assert len(D)==40 and m.rank(A)==47 and m.rank(B)==11
val={f'X{i}':1<<i for i in range(111)};val.update({f'Y{i}':1<<(111+i) for i in range(111)})
for op in w['operations']:
 if op[0]=='INIT':val[op[1]]=0
 elif op[0]=='ADD':val[op[2]]^=val[op[1]]
 elif op[0]=='CLEAR':raise AssertionError('requires live word')
assert all(val[n]==v for n,(c,v) in w['expected'].items())
K=[(1<<i)|loc[i] for i in range(111)];h=K[0]^K[4]
assert W==[K[i]&sum(1<<j for j in range(111) if ((h>>i)^(h>>j))&1==0) for i in range(111)]
assert m.rank(W)==15 and all(m.contains(D,b) for b in B)

def red(x,b):
 for p in sorted(b,reverse=True):
  if x>>p&1:x^=b[p]
 return x
results=[]
for i,j in [(8,11),(22,23)]:
 non=M^(loc[i]|loc[j]);bb=m.basis([b&non for b in B]);target=((1<<i)^(1<<j))&non;rem=red(target,bb);assert rem
 t=(rem&-rem).bit_length()-1;z=1<<t
 for p in sorted(bb):
  if (bb[p]&z).bit_count()%2:z^=1<<p
 assert not z&(loc[i]|loc[j]);assert all((z&b).bit_count()%2==0 for b in B);assert(z&target).bit_count()%2==1
 assert m.contains(D,W[i]^W[j]);assert m.rank(A)-m.rank([a&(M^loc[i]) for a in A])==len(D)-m.rank([a&(M^loc[i]) for a in D]);assert m.rank(A)-m.rank([a&(M^loc[j]) for a in A])==len(D)-m.rank([a&(M^loc[j]) for a in D])
 results.append({'pair':[i,j],'dual_hex':hex(z),'dual_support':[q for q in range(111) if z>>q&1],'W_difference_hex':hex(W[i]^W[j]),'ambient_local_dimensions':[m.rank(A)-m.rank([a&(M^loc[t]) for a in A]) for t in [i,j]]})
assert all(m.contains([z&(M^loc[i]) for z in W+B],1<<i) for i in range(111))
for i,j in [(8,11),(22,23)]:assert not ((1<<i)&(loc[i]|loc[j]))
def verify_dual(i,j,z,grant):
 assert not z&(loc[i]|loc[j])
 assert all((z&b).bit_count()%2==0 for b in grant)
 assert ((z>>i)^(z>>j))&1
controls=[]
for name,i,j,z,grant in [('erase_demand_bit',8,11,(1<<37)|(1<<78),B),('add_unpriced_point',8,11,(1<<8)|(1<<37)|(1<<78),B+[1<<8]),('second_erased_demand',22,23,(1<<33)|(1<<61),B)]:
 try:verify_dual(i,j,z,grant)
 except AssertionError:controls.append({'name':name,'rejected':True})
 else:raise AssertionError(name)
out={'status':'PASS_ARBITRARY_LIFT_RAW_QUERY_GATE','source_word_sha256':hashlib.sha256(args.source.read_bytes()).hexdigest(),'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'rank_D':len(D),'rank_A':m.rank(A),'rank_B':m.rank(B),'B_rows_hex':[hex(b) for b in B],'pairs':results,'negative_controls':controls,'positive_control_full_W_grant_fits_all':True,'positive_control_extra_demand_point_breaks_dual':True};args.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
