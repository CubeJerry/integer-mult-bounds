"""Independent rational and typed interpreter for feedback-star review."""
from fractions import Fraction as Q
from collections import Counter
import gzip,hashlib,json

def need(ok,why):
 if not ok:raise ValueError(why)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):
 b=p.read_bytes();return json.loads(gzip.decompress(b) if p.suffix=='.gz' else b)
def space(frame):
 s={0}
 for v in frame:s|={x^v for x in tuple(s)}
 return frozenset(s)
def add(x,y,c=Q(1)):
 z=x.copy()
 for k,v in y.items():
  w=z.get(k,Q(0))+c*v
  if w:z[k]=w
  else:z.pop(k,None)
 return z
def root9(v):
 S={i for i in range(9) if v>>i&1}
 if len(S)==3:return [Q(int(i in S))-Q(1,3) for i in range(9)]
 need(len(S)==7,'root weight');a,b=sorted(set(range(9))-S)
 return [Q(int(i==a)-int(i==b)) for i in range(9)]
def rank(A):
 B=[list(map(Q,r)) for r in A];k=0
 for j in range(len(B[0]) if B else 0):
  pivot=next((i for i in range(k,len(B)) if B[i][j]),None)
  if pivot is None:continue
  B[k],B[pivot]=B[pivot],B[k];v=B[k][j];B[k]=[x/v for x in B[k]]
  for i in range(k+1,len(B)):
   v=B[i][j]
   if v:B[i]=[x-v*y for x,y in zip(B[i],B[k])]
  k+=1
  if k==len(B):break
 return k

def interpret(s,w,full=False):
 frames=s['frames']+[r['frame'] for r in w.get('additional_charts',[])];spaces=list(map(space,frames));R={i:{i:Q(1)} for i in range(1880)};L=dict(enumerate(w['initial']));ops=Counter();moves=Counter();raw=Counter();rs=set(w['private_role_map'].values());life=peak=0
 program=w['program'] if full else w['program'][:w['marks']['common_starts']]
 for t,o in enumerate(program):
  op,r=o[:2];ops[op]+=1;need(0<=r<1880+w['owned_fields'],'declared role')
  if op=='INIT':need(r>=1880 and r not in L,'init');R[r]={};L[r]=o[2];life+=1
  elif op=='CLEAR':need(r>=1880 and L.get(r)==o[2],'clear');R.pop(r,None);del L[r]
  elif op=='MOVE':
   a,b,owned=o[2:];need(L.get(r)==a and type(owned)is bool and owned==(r>=1880),'owned route');need(spaces[a]<spaces[b] or owned and spaces[b]<spaces[a],'nested route');L[r]=b;k=abs(len(frames[a])-len(frames[b]));moves[k]+=1;raw[k]+=int(r in rs)
  elif op=='SCALE':
   need(Q(o[2]) and L.get(r)==o[3],'scale')
   if not full:R[r]={j:Q(o[2])*v for j,v in R[r].items()}
  else:
   need(op in ('ADD','COPY'),'known opcode');j,c,C=o[2:];need(r!=j and L.get(r)==L.get(j)==C,'cochart '+str(t))
   if not full:need(op!='COPY' or not R[r],'copy zero');R[r]=add(R[r],R[j],Q(c))
  peak=max(peak,len(L)-1880)
 if full:
  need(set(L)==set(range(1880)),'all owners retired')
  return {'instructions':sum(ops.values()),'opcode_counts':dict(ops),'move_rank_histogram':dict(moves),'raw_histogram':{k:v for k,v in raw.items() if v},'owned_lifetimes':life,'peak_owned':peak,'final_owned':0},L
 return R,L

def powers(r):
 D=2**120;N=r**199*D**200;lo=0;hi=r*D+1
 while hi-lo>1:
  m=(lo+hi)//2
  if m**200<=N:lo=m
  else:hi=m
 need(lo**200<=N<hi**200,'integer-power bracket');return Q(lo,D),Q(lo if lo**200==N else hi,D)
def interval(counts):
 lo=hi=Q(0)
 for r,c in counts.items():
  a,b=powers(r);lo+=c*(a if c>=0 else b);hi+=c*(b if c>=0 else a)
 return lo,hi
