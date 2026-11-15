#!/usr/bin/env python3
"""Source-bound exact linear certificate; no imports from source author code."""
import argparse,hashlib,json,copy
from pathlib import Path
from linear import basis,rank,reduce,xor,intersection,subset
NATIVE='research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
NATIVE_SHA='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
WORD_SHA='aa9d17693c1f976625ee420e1367680e86cfec0195259d609f7eddc258eda01e'
M=(1<<222)-1

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def emb(x,b):return sum(1<<(2*i+b) for i in range(111) if x>>i&1)
def certify(D,W,A,B,local):
 assert subset(B,D)
 duties=[]
 for ports in [[1],[8,11],[22,23]]:
  delta=[xor(1<<(2*i+b) for i in ports) for b in range(2)]
  for i in ports:assert subset(intersection(A,[1<<j for j in range(222) if local[i]>>j&1]),D)
  for b in range(2):assert reduce(xor(W[i][b] for i in ports),basis(D))==0
  L=xor([])
  for i in ports:L|=local[i]
  side=list(basis(B+[1<<j for j in range(222) if L>>j&1]).values())
  assert rank(side+delta)-rank(side)==2
  J=intersection(D,side+delta)
  assert rank(J+side)-rank(side)==2
  duties.append({'ports':ports,'demand_rows_hex':[hex(x) for x in delta],'side_rows_hex':[hex(x) for x in side],'J_rows_hex':[hex(x) for x in J],'side_dimension':rank(side),'J_dimension':rank(J)})
 J=[list(map(lambda x:int(x,16),d['J_rows_hex'])) for d in duties];side=[list(map(lambda x:int(x,16),d['side_rows_hex'])) for d in duties]
 I12=intersection(J[0],J[1]);I3=intersection(J[2],J[0]+J[1]);assert subset(I12,side[0]);assert subset(I3,side[2])
 return {'duties':duties,'first_pair_intersection_dimension':rank(I12),'first_two_J_sum_dimension':rank(J[0]+J[1]),'third_intersection_dimension':rank(I3),'first_pair_intersection_rows_hex':[hex(x) for x in I12],'third_intersection_rows_hex':[hex(x) for x in I3],'required_D_slack_per_whole_record_width':6}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,default=Path(__file__).parent/'CERTIFICATE.json');a=ap.parse_args()
 ns=a.repo/NATIVE;assert sha(ns)==NATIVE_SHA and sha(a.source)==WORD_SHA
 roots=json.loads(ns.read_text())['native_roots'];w=json.loads(a.source.read_text());assert not w['closed']
 val={f'X{i}_b{b}':1<<(2*i+b) for i in range(111) for b in range(2)};val.update({f'Y{i}_b{b}':1<<(222+2*i+b) for i in range(111) for b in range(2)});k0={}
 for op in w['operations']:
  if op[0]=='INIT':assert op[1] not in val;val[op[1]]=0
  elif op[0]=='ADD':assert op[1]!=op[2];val[op[2]]^=val[op[1]]
  elif op[0]=='MOVE':
   if op[1] in ['P0_b0','P0_b1'] and op[2]=='A15':k0[op[1]]=val[op[1]]
  else:raise AssertionError(op)
 assert all(val[n]==row for n,(chart,row) in w['expected'].items())
 D=list(basis([val[n] for n in sorted(val) if n.startswith('C')]).values())
 K0=[(1<<i)^sum(1<<j for j in range(111) if j!=i and sum(a*b for a,b in zip(roots[i],roots[j]))==0) for i in range(111)];h=K0[0]^K0[4]
 W0=[K0[i]&sum(1<<j for j in range(111) if ((h>>i)^(h>>j))&1==0) for i in range(111)];W=[[emb(z,b) for b in range(2)] for z in W0];Wall=[z for rows in W for z in rows];A=list(basis(D+Wall).values());assert[rank(D),rank(Wall),rank(A)]==[80,30,91]
 local=[sum(3<<(2*j) for j in range(111) if sum(a*b for a,b in zip(roots[i],roots[j]))==0) for i in range(111)]
 cases=[]
 for depth in [1,2,3]:
  z=[0,0];n=[0,0]
  for name,row in val.items():
   if name.startswith('C7_'):
    _,ell,color,bank=name.split('_');b=int(bank[1:])
    if color=='0':z[b]^=row
    if color=='1' and int(ell)>=depth:n[b]^=row
  B=list(basis([val['P0_b0'],val['P0_b1'],k0['P0_b0'],k0['P0_b1']]+n+[z[b]^(1<<(14+b)) for b in range(2)]).values());assert rank(B)==8
  c=certify(D,W,A,B,local);c.update({'query':7,'depth':depth,'B_rows_hex':[hex(x) for x in B],'B_rank':8});cases.append(c)
 # Positive relaxation: enough W information supplies every native fitting.
 for i in range(111):
  loc=[1<<j for j in range(222) if local[i]>>j&1]
  for b in range(2):assert reduce(1<<(2*i+b),basis(Wall+loc))==0
 # Rejection controls directly challenge the logical matrix conditions.
 controls=[]
 for label,Bextra in [('free_receiver1',[1<<2,1<<3]),('free_pair8_11',[(1<<16)^(1<<22),(1<<17)^(1<<23)]),('free_pair22_23',[(1<<44)^(1<<46),(1<<45)^(1<<47)])]:
  B=[int(x,16) for x in cases[0]['B_rows_hex']]+Bextra
  try:certify(D,W,A,B,local)
  except AssertionError:controls.append({'name':label,'gate_rejects_changed_hypothesis':True})
  else:raise AssertionError(('relaxation-not-detected',label))
 out={'status':'PASS_SOURCE_BOUND_THREE_DUTY_SIX_SLACK_GATE','source_sha256':WORD_SHA,'native_sha256':NATIVE_SHA,'D_rank':80,'W_rank':30,'A_rank':91,'W_quotient_dimension':11,'D_rows_hex':[hex(x) for x in D],'W_rows_hex':[[hex(x) for x in row] for row in W],'cases':cases,'negative_controls':controls,'scope':'q7 class-zero delayed feedback at depths1,2,3; fixed actual D; free seed subspace inside D+W; arbitrary characteristic-two field and tensor width; no full source/decoder claim'}
 a.out.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cases':[{k:c[k] for k in ['query','depth','required_D_slack_per_whole_record_width','first_pair_intersection_dimension','first_two_J_sum_dimension','third_intersection_dimension']} for c in cases],'controls':len(controls)},indent=2))
if __name__=='__main__':main()
