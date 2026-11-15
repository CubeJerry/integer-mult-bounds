from pathlib import Path
import json,hashlib,argparse
import sympy as s

def basis(rows):
 piv={};out=[]
 for row in rows:
  x=row
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k]
   else:piv[k]=x;out.append(row);break
 return out
def rank(rows):return len(basis(rows))
def system(rows):
 piv={};null=[]
 for j,row in enumerate(rows):
  x=row;c=1<<j
  while x:
   k=x.bit_length()-1
   if k in piv:x^=piv[k][0];c^=piv[k][1]
   else:piv[k]=(x,c);break
  if not x:null.append(c)
 return piv,null
def solve(piv,x):
 c=0
 while x:
  k=x.bit_length()-1
  if k not in piv:return None
  x^=piv[k][0];c^=piv[k][1]
 return c
def transcript(word):
 v={**{f'X{i}':1<<i for i in range(111)},**{f'Y{i}':1<<(111+i) for i in range(111)}}
 ch={**{f'X{i}':f'L{i}' for i in range(111)},**{f'Y{i}':'zero' for i in range(111)}};hist=[]
 for op in word['operations']:
  if op[0]=='INIT':v[op[1]]=0;ch[op[1]]=op[2]
  elif op[0]=='ADD':v[op[2]]^=v[op[1]]
  elif op[0]=='MOVE':ch[op[1]]=op[2]
  elif op[0]=='CLEAR':del v[op[1]];del ch[op[1]]
  else:raise ValueError(op)
  name=op[2] if op[0]=='ADD' else op[1]
  if name.startswith('P') and name[1:].isdigit() and name in v and ch[name]!='Hub':hist.append(v[name])
 assert all(v[f'X{i}']==1<<i for i in range(111))
 return basis(hist),[v[f'P{i}'] for i in range(8)]
def fits(B,masks):return [i for i,m in enumerate(masks) if solve(system([r&m for r in B])[0],1<<i) is not None]
def quotient(B,extra,desired,masks):
 b=basis(B);H=basis(b+extra);n=len(b);piv,_=system(H);qs=[solve(piv,r)>>n for r in desired]
 ambiguity=[basis([x>>n for x in system([r&m for r in H])[1]]) for m in masks]
 F=[];steps=[]
 while True:
  fp,_=system(F)
  j=next((i for i in range(111) if all(solve(fp,x) is not None for x in ambiguity[i]) and solve(fp,qs[i]) is None),None)
  if j is None:break
  steps.append({'receiver':j,'class':qs[j],'local_ambiguity':ambiguity[j]});F.append(qs[j])
 assert rank(F)==len(H)-n
 return {'quotient_dimension':len(H)-n,'forced_dimension':rank(F),'forcing_steps':steps}
def rank107(rows):
 a=[[x%107 for x in row] for row in rows];r=0
 for c in range(8):
  k=next((j for j in range(r,len(a)) if a[j][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];z=pow(a[r][c],-1,107);a[r]=[(x*z)%107 for x in a[r]]
  for j in range(r+1,len(a)):
   z=a[j][c]
   if z:a[j]=[(x-z*y)%107 for x,y in zip(a[j],a[r])]
  r+=1
 return r
repo=next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
root=repo/'research/moonshot-005-program'
parser=argparse.ArgumentParser()
parser.add_argument('--eight-word',type=Path,default=root/'results/bit-cyclic-three-receiver/author/eight-output/WORD.json')
parser.add_argument('--full-word',type=Path,default=root/'results/bit-full-singular-history/author/full-history-output/WORD.json')
args=parser.parse_args()
source=root/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json'
assert hashlib.sha256(source.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e'
roots=json.loads(source.read_text())['native_roots'];dot=lambda a,b:sum(x*y for x,y in zip(a,b))
b=[0,0,1,1,0,0,1,-1];h=[((dot(roots[72],r)+dot(b,r))//2)%2 for r in roots];hm=sum(x<<i for i,x in enumerate(h));full=(1<<111)-1
C=[sum(int(i==j or dot(r,t)==0)<<j for j,t in enumerate(roots)) for i,r in enumerate(roots)];W=[c&(hm if h[i] else full^hm) for i,c in enumerate(C)]
masks=[sum(int(dot(r,t)!=0)<<j for j,t in enumerate(roots)) for r in roots]
G,T=transcript(json.loads(args.eight_word.read_text()))
assert (rank(G),rank(T),rank(G)+rank(W)-rank(G+W),rank(G)+rank(C)-rank(G+C),rank(T)+rank(C)-rank(T+C))==(18,8,11,7,4)
gf,tf=fits(G,masks),fits(T,masks);assert len(gf)==38 and len(tf)==14
dual=int('5001200000000020000100',16)
assert dual&(1<<8) and dual&masks[8]==dual and all((r&dual).bit_count()%2==0 for r in G)
quotients={'G_plus_W':quotient(G,W,W,masks),'G_plus_C':quotient(G,C,C,masks),'T_plus_C':quotient(T,C,C,masks)}
assert [x['quotient_dimension'] for x in quotients.values()]==[4,2,5]
cb=basis(C);assert len(cb)==9
proper=[];words=[0]
for row in cb:words += [x^row for x in words]
for row in words[1:]:
 support=[roots[i] for i in range(111) if row>>i&1]
 if rank107(support)<8:
  assert s.Matrix(support).rank()==7;proper.append(hex(row))
assert len(proper)==9
G2,T2=transcript(json.loads(args.full_word.read_text()))
assert rank(G2)==29 and rank(G2+W)==29 and rank(T2)==8
fullfits=fits(T2,masks);assert fullfits==[17,59]
out={'status':'PASS_INDEPENDENT_HISTORICAL_TERMINAL_QUOTIENTS','engine':'root symbolic222-column replay and separate binary elimination; no author/reviewer imports','old_history_rank':18,'old_terminal_rank':8,'historical_fit_receivers':gf,'terminal_fit_receivers':tf,'exact_completion_quotients':quotients,'canonical_nonzero_words_checked':511,'proper_canonical_word_count':9,'proper_canonical_words':proper,'full_source_history_rank':29,'full_source_contains_W15':True,'full_source_terminal_fit_receivers':fullfits,'scope':'information and source algebra only; geometry/ownership rely on separate word review; history is not universally available','no_new_kappa':True}
Path(__file__).with_name('RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
