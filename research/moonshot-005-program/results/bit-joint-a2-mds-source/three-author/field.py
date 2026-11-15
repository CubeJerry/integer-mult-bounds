"""Finite binary extension arithmetic and explicit reversible ADD synthesis."""
def mul(a,b,d,mod):
 z=0
 while b:
  if b&1:z^=a
  b>>=1;a<<=1
  if a&(1<<d):a^=mod
 return z
def power(a,n,d,mod):
 z=1
 while n:
  if n&1:z=mul(z,a,d,mod)
  a=mul(a,a,d,mod);n>>=1
 return z
def invert(A,d,mod):
 n=len(A);M=[r[:]+[int(i==j)for j in range(n)]for i,r in enumerate(A)]
 for c in range(n):
  p=next(i for i in range(c,n)if M[i][c]);M[c],M[p]=M[p],M[c];v=power(M[c][c],(1<<d)-2,d,mod);M[c]=[mul(x,v,d,mod)for x in M[c]]
  for i in range(n):
   if i!=c and M[i][c]:
    v=M[i][c];M[i]=[a^mul(v,b,d,mod)for a,b in zip(M[i],M[c])]
 assert all(M[i][:n]==[int(i==j)for j in range(n)]for i in range(n));return[r[n:]for r in M]
def binary_matrix(A,d,mod):
 return[sum(((mul(A[i][j],1<<b,d,mod)>>a)&1)<<(d*j+b)for j in range(len(A[i]))for b in range(d))for i in range(len(A))for a in range(d)]
def restore_adds(matrix):
 M=matrix[:];n=len(M);ops=[]
 def add(a,b):M[b]^=M[a];ops.append((a,b))
 for c in range(n):
  p=next(i for i in range(c,n)if M[i]>>c&1)
  if p!=c:add(p,c);add(c,p);add(p,c)
  for i in range(n):
   if i!=c and M[i]>>c&1:add(c,i)
 assert M==[1<<i for i in range(n)];return ops
