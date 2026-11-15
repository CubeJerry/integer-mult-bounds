def basis(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return b

def rank(rows):return len(basis(rows))
def reduce(x,b):
 for p in sorted(b,reverse=True):
  if x>>p&1:x^=b[p]
 return x

def xor(xs):
 z=0
 for x in xs:z^=x
 return z

def intersection(X,Y):
 X=list(basis(X).values());by=basis(Y);columns={}
 for a,x in enumerate(X):
  z=reduce(x,by)
  while z:
   bit=z&-z;p=bit.bit_length()-1;columns[p]=columns.get(p,0)^(1<<a);z^=bit
 equations=basis(columns.values());free=[i for i in range(len(X)) if i not in equations];out=[]
 for f in free:
  c=1<<f
  for p in sorted(equations):
   if (equations[p]&c).bit_count()%2:c^=1<<p
  out.append(xor(X[j] for j in range(len(X)) if c>>j&1))
 assert rank(out)==len(out)
 return out

def subset(X,Y):
 by=basis(Y)
 return all(reduce(x,by)==0 for x in X)
