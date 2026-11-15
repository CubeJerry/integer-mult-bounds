"""Finite source-specific canonical basis choice; every row is a valid code row."""
def choose_basis(K,scalar_basis,dual,X,held):
 ids={n:i for i,n in enumerate(X)};hm=sum(1<<ids[n]for n in held);orig=[];cur=[]
 for i in scalar_basis:
  oo=[];cc=[]
  for k in range(4):
   row=sum(1<<(4*j+k)for j in range(111)if K[i]>>j&1);oo.append(row);cc.append(sum(((row&dual[n]).bit_count()%2)<<t for t,n in enumerate(X)))
  orig.append(oo);cur.append(cc)
 dp_o=[[0]*4];dp_c=[[0]*4];candidates=[]
 for mask in range(1,512):
  z=(mask&-mask).bit_length()-1;old=mask^(1<<z);oo=[dp_o[old][k]^orig[z][k]for k in range(4)];cc=[dp_c[old][k]^cur[z][k]for k in range(4)];dp_o.append(oo);dp_c.append(cc)
  for b in range(1,16):
   row=coeff=cm=0
   for k in range(4):
    if b>>k&1:
     row^=oo[k];coeff^=cc[k]
     for q in range(9):
      if mask>>q&1:cm|=1<<(4*q+k)
   proj=sum(((coeff>>ids[n])&1)<<t for t,n in enumerate(held));cost=(coeff&~hm).bit_count();candidates.append((cost,cm,row,proj))
 candidates.sort();direct=[next(x for x in candidates if x[3]==1<<q)for q in range(len(held))];B={};H=[]
 for x in candidates:
  if x[3]:continue
  v=x[1]
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;H.append(x);break
  if len(H)==36-len(held):break
 assert len(H)==36-len(held)
 out=direct+H
 return [x[2]for x in out],[x[3]for x in out],{'candidate_family':'511 nonzero scalar canonical rows times15 nonzero binary bank vectors','candidate_count':len(candidates),'zero_projection_candidates':sum(x[3]==0 for x in candidates),'Hub_basis_dimension':len(H),'completed_Hub_seed_ADD_sum':sum(x[0]for x in out),'scope':'Greedy minimal-weight Hub basis within this finite candidate family; no universal source optimality claim.'}
