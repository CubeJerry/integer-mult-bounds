from pathlib import Path
from collections import Counter
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--word',type=Path,required=True);p.add_argument('--root-source',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sp=importlib.util.spec_from_file_location('own_geometry',a.root_source);g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
w=json.loads(a.word.read_text());assert hashlib.sha256(a.word.read_bytes()).hexdigest()=='f5acfcb454d6d50dfdb7d66acd2c33980e4aed17826afafbb67fbeb2168f58c1';src=(a.repo/w['source_path']).read_bytes();assert hashlib.sha256(src).hexdigest()==w['source_sha256'];roots=json.loads(src)['native_roots'];charts={n:g.chart(c)for n,c in w['charts'].items()}
v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};loc={f'X{i}':f'L{i}'for i in range(111)}|{f'Y{i}':'zero'for i in range(111)};profile=Counter();cv=cl=None
for ix,(op,n,*z)in enumerate(w['operations']):
 if ix==w['carrier_interface_before_operation']:cv=v.copy();cl=loc.copy()
 if op=='INIT':assert n not in v;v[n]=0;loc[n]=z[0]
 elif op=='ADD':assert charts[loc[n]]==charts[loc[z[0]]];v[z[0]]^=v[n]
 elif op=='MOVE':profile[abs(len(charts[loc[n]])-len(charts[z[0]]))]+=1;loc[n]=z[0]
 else:assert op=='CLEAR';del v[n],loc[n]
assert all(v[f'X{i}']==1<<i for i in range(111));T=set(w['targets']);U=set(range(111))-T
assert all(v[f'Y{i}']==((1<<(111+i))^(1<<i if i in T else 0))for i in range(111))
assert all(cv[f'X{i}']==1<<i and cl[f'X{i}']=='Hub'for i in range(111));assert all(cv[f'Y{i}']==1<<(111+i)and charts[cl[f'Y{i}']]==[]for i in U)
code=[cv[f'CANONICAL_{j}']for j in range(9)];assert all(charts[cl[f'CANONICAL_{j}']]==[]for j in range(9));words=[0]
for z in code:words+= [x^z for x in words]
assert len(set(words))==512
N=[sum(1<<j for j,r in enumerate(roots)if sum(x*y for x,y in zip(q,r))==0)for q in roots];allmask=(1<<111)-1
outside_min=[]
for i in U:
 k=N[i]^(1<<i);assert k in words
 assert all(not z or z&~N[i]for z in words)
 gap=min((z&~N[i]).bit_count()for z in words if z and z!=k);assert gap>=18;outside_min.append(gap)
proper=[n for n in cv if not n.startswith(('X','Y')) and 1<len(charts[cl[n]])<8];assert len(proper)==20
for i in U:assert not any(g.subset(charts[cl[n]],charts[f'F{i}'])for n in proper)
assert (N[0]|N[2]|N[4]|N[5])==allmask
claim=json.loads(a.author.read_text());ws=claim['all111_independent_functional_collision_witnesses'];assert len(ws)==111
for r in ws:
 j,i=r['native_site'],r['receiver'];h=sum(1<<k for k in r['collision_difference_support']);assert h>>j&1 and h>>i&1
 assert not h&(N[i]^(1<<j));assert all((h&z).bit_count()%2==0 for z in code)
assert min((N[j]&sum(1<<i for i in U)).bit_count()for j in range(111))==49
assert len(cv)==362 and all(cv[f'NATIVE_RAW_{j}']==1<<j and charts[cl[f'NATIVE_RAW_{j}']]==charts[f'L{j}']for j in range(111))
def power(n):
 N=n**199<<(128*200);lo=0;hi=1<<((N.bit_length()+199)//200)
 while hi-lo>1:
  mid=(lo+hi)//2
  if mid**200<=N:lo=mid
  else:hi=mid
 return F(lo,1<<128),F(hi,1<<128)
def moment(c):
 lo=hi=F(0)
 for d,k in c.items():
  x,y=power(d);lo+=k*(x if k>=0 else y);hi+=k*(y if k>=0 else x)
 return lo,hi
price=moment(profile);delta=moment({1:1,6:1,7:-1});gate={127:37,64:74,1:-74}
for j in range(1,9):gate[1+7*j]=gate.get(1+7*j,0)+74;gate[7*j]=gate.get(7*j,0)-74
allow=tuple(x/6 for x in moment(gate));room=(allow[0]-price[1],allow[1]-price[0]);floor=(6+105*delta[0],6+105*delta[1]);remain=(room[0]-floor[1],room[1]-floor[0]);assert 0<delta[0]<delta[1]<1 and remain[0]>0
assert 7+104*delta[1]<room[0] and 8+103*delta[0]>room[1]
from decimal import Decimal,localcontext
def dec(x):
 with localcontext()as c:c.prec=55;return str(Decimal(x.numerator)/Decimal(x.denominator))
result={'status':'PASS_INDEPENDENT_FANOUT_RESIDUAL_GATE','method':'Own binary full-column replay with root geometry, all512 actual codewords,111 explicit functional collisions and independent128-bit integer-root intervals. No construction-author or C verifier imported.','actual_source_fields':len(cv),'actual_code_rank':9,'all105_code_neighbor_intersections_zero':True,'minimum_other_support_outside_neighbors':min(outside_min),'checked_functional_collisions':111,'required_native_sites':111,'available_Y_visitors':105,'native_only_added_floor':list(map(dec,floor)),'remaining_movement_after_floor':list(map(dec,remain)),'surviving_native_only_port_counts':[6,7],'scope':'Pinned source, fixed schedule, arbitrary nonlinear local processing; quantitative floor additionally assumes every downward departure is a native line.'}
a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
