"""Exact GF32 arithmetic and binary ADD compilation."""
def mul(a,b):
 z=0
 while b:
  if b&1:z^=a
  a<<=1;b>>=1
  if a&32:a^=0x25
 return z
T=[[mul(a,b)for b in range(32)]for a in range(32)]
def power(a,n):
 z=1
 while n:
  if n&1:z=T[z][a]
  a=T[a][a];n//=2
 return z
INV=[0]+[power(a,30)for a in range(1,32)]
def reduce(a,invert=False):
 a=[r[:]for r in a];n=len(a);m=len(a[0])if n else 0;p=0
 if invert:a=[r+[int(i==j)for j in range(n)]for i,r in enumerate(a)]
 for c in range(m):
  k=next((k for k in range(p,n)if a[k][c]),None)
  if k is None:continue
  a[p],a[k]=a[k],a[p];tab=T[INV[a[p][c]]];a[p]=[tab[x]for x in a[p]]
  for k in range(n):
   if k!=p and a[k][c]:
    tab=T[a[k][c]];a[k]=[x^tab[y]for x,y in zip(a[k],a[p])]
  p+=1
  if p==n:break
 if invert:
  assert p==n==m
  return [r[m:]for r in a]
 return p
def mm(a,b):
 out=[]
 for row in a:
  v=[0]*len(b[0])
  for k,x in enumerate(row):
   if x:
    tab=T[x]
    for c,y in enumerate(b[k]):v[c]^=tab[y]
  out.append(v)
 return out
def binary_matrix(a):
 out=[]
 for row in a:
  bits=[0]*5
  for c,x in enumerate(row):
   for s in range(5):
    y=T[x][1<<s]
    for r in range(5):
     if y>>r&1:bits[r]|=1<<(5*c+s)
  out+=bits
 return out
def linear_word(matrix,fields):
 rows=binary_matrix(matrix);n=len(rows);ops=[]
 assert all(len(r)==len(matrix)for r in matrix)
 for c in range(n):
  k=next(k for k in range(c,n)if rows[k]>>c&1)
  if k!=c:
   for d,s in [(c,k),(k,c),(c,k)]:rows[d]^=rows[s];ops.append((d,s))
  for k in range(n):
   if k!=c and rows[k]>>c&1:rows[k]^=rows[c];ops.append((k,c))
 assert rows==[1<<k for k in range(n)]
 check=[1<<k for k in range(n)];word=[]
 for d,s in reversed(ops):
  check[d]^=check[s];word.append(['ADD',5*fields[d//5]+d%5,5*fields[s//5]+s%5])
 assert check==binary_matrix(matrix)
 return word
def add_field(d,s):return [['ADD',5*d+b,5*s+b]for b in range(5)]
def swap_field(a,b):return []if a==b else add_field(a,b)+add_field(b,a)+add_field(a,b)
