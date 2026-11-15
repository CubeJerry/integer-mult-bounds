#!/usr/bin/env python3
import argparse,hashlib,json
from pathlib import Path
from linear import basis,rank,reduce,xor,intersection,subset
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,default=Path(__file__).parent/'CERTIFICATE.json');a=p.parse_args()
native=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(native.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';assert hashlib.sha256(a.source.read_bytes()).hexdigest()=='8939d815b7e1b1dfa89e3e0a6812e5b427f98ddf3020a3300c6232aaa803db52'
r=json.loads(native.read_text())['native_roots'];w=json.loads(a.source.read_text());M=(1<<111)-1
val={f'X{i}':1<<i for i in range(111)};val.update({f'Y{i}':1<<(111+i) for i in range(111)});k0=None
for op in w['operations']:
 if op[0]=='INIT':val[op[1]]=0
 elif op[0]=='ADD':val[op[2]]^=val[op[1]]
 elif op==['MOVE','P0','A15']:k0=val['P0']
 elif op[0]=='CLEAR':raise AssertionError('live word required')
assert all(val[n]==v for n,(c,v) in w['expected'].items())
D=list(basis([v for n,v in val.items() if n.startswith('C') or n.startswith('EXTRA')]).values());local=[sum(1<<j for j in range(111) if sum(x*y for x,y in zip(r[i],r[j]))==0) for i in range(111)];K=[(1<<i)|local[i] for i in range(111)];h=K[0]^K[4];W=[K[i]&sum(1<<j for j in range(111) if ((h>>i)^(h>>j))&1==0) for i in range(111)];A=list(basis(D+W).values());assert [rank(D),rank(W),rank(A)]==[42,15,48]
cases=json.loads((Path(__file__).parent/'CASES.json').read_text());results=[]
for case in cases:
 q,l=case['query'],case['depth'];R0=xor(v for n,v in val.items() if n.startswith('C'+str(q)+'_') and n.endswith('_0'));Nj=xor(v for n,v in val.items() if n.startswith('C'+str(q)+'_') and n.endswith('_1') and int(n.split('_')[1])>=l);B=list(basis([val['P0'],k0,(1<<q)^R0,Nj]).values());assert subset(B,D)
 obligations=[];Js=[];sides=[]
 for i,j in case['pairs']:
  assert subset(intersection(A,[1<<t for t in range(111) if local[i]>>t&1]),D)
  assert subset(intersection(A,[1<<t for t in range(111) if local[j]>>t&1]),D)
  assert subset([W[i]^W[j]],D)
  L=local[i]|local[j];delta=(1<<i)^(1<<j);side=B+[1<<t for t in range(111) if L>>t&1];assert not subset([delta],side)
  J=intersection(D,side+[delta]);assert not subset(J,side)
  obligations.append({'receivers':[i,j],'demand_hex':hex(delta),'local_mask_hex':hex(L),'J_dimension':rank(J),'J_rows_hex':[hex(x) for x in J]});Js.append(J);sides.append(side)
 assert len(Js)==2;I=intersection(*Js);lost=[t for t in range(2) if subset(I,sides[t])];assert lost
 # Each requirement alone admits a scalar slack row, so both are consequential.
 for J,side in zip(Js,sides):assert any(not subset([x],side) for x in J)
 results.append({'query':q,'depth':l,'B_rank':rank(B),'B_rows_hex':[hex(x) for x in B],'obligations':obligations,'intersection_dimension':rank(I),'intersection_rows_hex':[hex(x) for x in I],'lost_demand_indices':lost})
result={'status':'PASS_ALL_FIELD_Q9_ONE_D_SLACK_GATE','source_word_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'D_rank':42,'W_rank':15,'A_rank':48,'cases':results,'controls':{'each_single_virtual_requirement_has_a_scalar_slack_solution':True,'all_W15_global_fields_fit':all(subset([1<<i],W+[1<<j for j in range(111) if local[i]>>j&1]) for i in range(111))}}
a.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':result['status'],'cases':len(results),'q7_examples':[{k:v for k,v in x.items() if k in ['query','depth','B_rank','intersection_dimension','lost_demand_indices']} for x in results if x['query']==7]},indent=2))
