#!/usr/bin/env python3
"""Source-bound anisotropic Gram relay; separate arithmetic-lattice evidence.
@CubeJerry with OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,copy,gzip,hashlib,json,math

OLD='0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c'

def need(c,m):
 if not c: raise ValueError(m)
def root(v):
 on=[i for i in range(9)if v>>i&1]
 if len(on)==3:return [2 if i in on else -1 for i in range(9)]
 off=[i for i in range(9)if i not in on];need(len(off)==2,'root type')
 return [3*(int(i==off[0])-int(i==off[1]))for i in range(9)]
def dot(x,y):return sum(a*b for a,b in zip(x,y))
def plus(a,b,c=F(1)):
 out=dict(a)
 for k,v in b.items():
  z=out.get(k,F(0))+c*v
  if z:out[k]=z
  else:out.pop(k,None)
 return out
def mult(a,c):return {k:v*c for k,v in a.items()if v*c}
def combine(coeff,rows):
 out={}
 for c,row in zip(coeff,rows):out=plus(out,row,F(c))
 return out
def span(vs):
 out={0}
 for v in vs:out|={x^v for x in tuple(out)}
 return frozenset(out)
def mm(A,B):return [[sum(a*b for a,b in zip(row,col))for col in zip(*B)]for row in A]
def trans(A):return list(map(list,zip(*A)))
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def determinant(A):
 a=[list(map(F,row))for row in A];d=F(1)
 for j in range(len(a)):
  k=next((i for i in range(j,len(a))if a[i][j]),None)
  if k is None:return F(0)
  if k!=j:a[k],a[j]=a[j],a[k];d=-d
  p=a[j][j];d*=p;a[j]=[x/p for x in a[j]]
  for i in range(j+1,len(a)):
   c=a[i][j];a[i]=[x-c*y for x,y in zip(a[i],a[j])]
 return d
def inverse(A):
 n=len(A);a=[list(map(F,row))+eye(n)[j]for j,row in enumerate(A)]
 for j in range(n):
  k=next(i for i in range(j,n)if a[i][j]);a[j],a[k]=a[k],a[j];p=a[j][j];a[j]=[x/p for x in a[j]]
  for i in range(n):
   if i!=j:
    c=a[i][j];a[i]=[x-c*y for x,y in zip(a[i],a[j])]
 return [row[n:]for row in a]
def ff_rank(A,p):
 a=[[int(F(x).numerator)*pow(int(F(x).denominator),-1,p)%p for x in row]for row in A];r=0
 for j in range(len(a[0])):
  k=next((i for i in range(r,len(a))if a[i][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];c=pow(a[r][j],-1,p);a[r]=[x*c%p for x in a[r]]
  for i in range(len(a)):
   if i!=r:
    c=a[i][j];a[i]=[(x-c*y)%p for x,y in zip(a[i],a[r])]
  r+=1
 return r

def replay(w,mutation=None):
 n=w['public'];rows={i:{i:F(1)}for i in range(n)};loc=dict(enumerate(w['initial']));spaces=[span(f)for f in w['frames']];bills={False:Counter(),True:Counter()};ct=Counter();maxodd=1;peak=0;hist=[];odd_witness=None;max_binary_height=0;max_l1=F(1)
 for k,orig in enumerate(w['program']):
  e=list(orig)
  if mutation and k==mutation[0]:e=mutation[1]
  op,r=e[:2];ct[op]+=1
  if op=='INIT':need(r not in rows and r>=n,'owned init');rows[r]={};loc[r]=e[2];peak=max(peak,len(rows)-n)
  elif op=='CLEAR':need(r in rows and r>=n and loc[r]==e[2],'owned retirement');hist.append((r,bool(rows[r])));del rows[r];del loc[r]
  elif op=='MOVE':
   _,r,a,b,owned=e;need(loc[r]==a and owned==(r>=n),'actual move entrance');need(spaces[a]<spaces[b]or owned and spaces[b]<spaces[a],'nested movement');bills[owned][abs(len(w['frames'][a])-len(w['frames'][b]))]+=1;loc[r]=b
  elif op=='SCALE':
   need(loc[r]==e[-1],'cochart scale');rows[r]=mult(rows[r],F(e[2]))
  else:
   need(op in('ADD','COPY')and loc[r]==loc[e[2]]==e[-1],'cochart additive gate')
   rows[r]=plus(rows[r]if op=='ADD'else{},rows[e[2]],F(e[3]))
  if op in('ADD','COPY','SCALE'):
   c=F(e[2]if op=='SCALE'else e[3]);need(c and abs(c)+1<2**16,'bounded scalar')
   def smooth(z):
    for p in(2,3,5):
     while z%p==0:z//=p
    return z==1
   need(smooth(c.denominator)and(op!='SCALE'or smooth(abs(c.numerator))),'original smooth scalar grammar')
   for v in rows[r].values():
    d=v.denominator
    while d%2==0:d//=2
    maxodd=math.lcm(maxodd,d);max_binary_height=max(max_binary_height,v.denominator.bit_length()-d.bit_length())
    if d>1 and odd_witness is None:odd_witness={'step':k,'register':r,'coefficient':str(v)}
   max_l1=max(max_l1,sum(abs(v)for v in rows[r].values()))
 need(set(rows)==set(range(n)),'all owned ended')
 return rows,loc,{'instructions':sum(ct.values()),'counts':dict(ct),'public_moves':dict(sorted(bills[False].items())),'owned_moves':dict(sorted(bills[True].items())),'lifetimes':len(hist),'dirty_retirements':sum(x[1]for x in hist),'peak_owned':peak,'odd_prefix_lcm':maxodd,'first_nondyadic_coefficient':odd_witness,'maximum_binary_denominator_exponent':max_binary_height,'maximum_scalar_row_l1':str(max_l1)}

def prepare(w):
 rm={int(k):v for k,v in w['source_role_map'].items()};T=w['relay']['restored_ports'];S=w['relay']['unrestored_ports'];H=sorted(T+S);live=sorted(k for k in rm if k<112);U=sorted(set(live)-set(H));r={h:root(w['frames'][w['initial'][rm[h]]][0])for h in live};fr=list(map(root,w['relay']['ground_Gram_frame']));g={h:[F(dot(r[h],f),18)for f in fr]for h in live};need(len(H)==96 and len(live)==104 and len(T)==20,'literal ports');need(all(x in(F(0),F(1,2),F(-1,2))for gh in g.values()for x in gh),'dyadic original Gram coefficients')
 L=[[F(i==j,4)for j in range(8)]for i in range(8)]
 for a,b in[(0,2),(1,3)]:L[a][a]+=F(1,24);L[b][b]+=F(1,24);L[a][b]-=F(1,24);L[b][a]-=F(1,24)
 B={h:208+k for k,h in enumerate(H)};D={h:304+k for k,h in enumerate(H)};need(all(w['initial'][B[h]]==w['initial'][rm[h]]and w['initial'][D[h]]==3 for h in H),'actual B/D starting charts');return rm,T,S,H,live,U,g,L,B,D

def expected(w):
 rm,T,S,H,live,U,g,L,B,D=prepare(w);perm={int(k):v for k,v in w['relay']['permutation'].items()};q=[{D[h]:g[h][i]for h in H if g[h][i]}for i in range(8)];z=[combine(row,q)for row in L];rr={h:plus({D[h]:F(-1)}if h in H else{},combine(g[h],z))for h in live};want={i:{i:F(1)}for i in range(400)}
 for h in U:want[rm[h]]=plus(want[rm[h]],want[rm[h+112]],F(-1))
 for h in H:want[B[h]]=plus(want[B[h]],rr[h]);want[D[h]]={D[h]:F(1)}if h in T else rr[perm[h]]
 return want

def make_patch(w):
 C=3;ops=[]
 for i,j in[(400,402),(401,403)]:ops += [['ADD',i,j,'1',C],['SCALE',j,'-2',C],['ADD',j,i,'1',C],['SCALE',i,'1/4',C],['SCALE',j,'1/3',C],['ADD',i,j,'1',C],['SCALE',i,'1/2',C],['SCALE',j,'-1',C],['ADD',j,i,'1',C]]
 ops += [['SCALE',i,'1/4',C]for i in range(404,408)]
 return ops

def main():
 pa=argparse.ArgumentParser();pa.add_argument('--source',type=Path,required=True);pa.add_argument('--out',type=Path,default=Path(__file__).parent);a=pa.parse_args();raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==OLD,'exact old relay source pin');old=json.loads(gzip.decompress(raw));w=copy.deepcopy(old);ins=432;ops=make_patch(w);need(len(ops)==22 and old['program'][ins]==['SCALE',304,'-1',3],'actual pre-D preload boundary');need(all(e[0]=='ADD'and 400<=e[1]<=407 for e in old['program'][386:432]),'last Gram capture completed');w['program'][ins:ins]=ops;w['schema']='moonshot-anisotropic-Gram-relay-source-v1';w['source_pins']['original_relay_word']=OLD
 for k,t in w['relay']['markers'].items():
  if t>=ins:w['relay']['markers'][k]=t+len(ops)
 for key,events in w['relay']['events'].items():
  if isinstance(events,list):
   for event in events:
    if isinstance(event,dict)and 'step'in event and event['step']>=ins:event['step']+=len(ops)
 w['anisotropic']={'insertion_index':ins,'new_scalar_events':len(ops),'Lambda':[[str(x)for x in row]for row in prepare(w)[7]],'complete_source':False,'unrestored_D':76,'forward_outputs_completed':0}
 w['relay']['preload']='r_h=-d_h+g_h Lambda q; q=sum g_j d_j; symmetric anisotropic Lambda retained explicitly'
 rows,loc,bill=replay(w);need(rows==expected(w),'all400 arbitrary-input endpoint rows');oldrows,oldloc,oldbill=replay(old);need(loc==oldloc,'all400 unchanged physical endpoints');need(bill['public_moves']==oldbill['public_moves']and bill['owned_moves']==oldbill['owned_moves'],'exact unchanged movement bill');need(bill['lifetimes']==oldbill['lifetimes']and bill['peak_owned']==oldbill['peak_owned'],'no new owner lifetime or peak');need(bill['odd_prefix_lcm']==3,'exact new odd prefix denominator3')
 rm,T,S,H,live,U,g,L,B,D=prepare(w);gs=[g[h]for h in S];C=mm(trans(gs),gs);A=[[F(i==j)-x for j,x in enumerate(row)]for i,row in enumerate(mm(L,C))];need(determinant(A)==F(3375,128),'smooth residual determinant');oldA=[[F(i==j)-C[i][j]for j in range(8)]for i in range(8)];need(determinant(oldA)==24387048,'independent reconstruction old determinant');Ai=inverse(A);need(all(all(p in(2,3,5)for p in prime_factors(x.denominator))for row in Ai for x in row),'all inverse denominators smooth');ranks={str(p):ff_rank(A,p)for p in(7,11,13,31,127)};need(all(r==8 for r in ranks.values()),'old bad-prime controls repaired')
 # Source mutation: restore the first changed difference eigenvalue to1/4;
 # independently reject both full intended map and the claimed S-unit determinant.
 mutant=(ins+4,['SCALE',402,'1/4',3]);mutrows,_,_=replay(w,mutation=mutant);need(mutrows!=rows,'changed eigenvalue detected by whole-source endpoint replay')
 late=copy.deepcopy(old);late['program'][912:912]=ops;late_rows,_,_=replay(late);need(any(late_rows[D[h]]!={D[h]:F(1)}for h in T),'late mixing must fail actual restoration')
 iso=[[F(i==j,4)for j in range(8)]for i in range(8)];isoA=[[F(i==j)-x for j,x in enumerate(row)]for i,row in enumerate(mm(iso,C))];need(determinant(isoA)==F(324135,32768)and ff_rank(isoA,7)==6,'isotropic quarter control still has two7 defects')
 a.out.mkdir(parents=True,exist_ok=True);word=a.out/'WORD.json.gz';payload=json.dumps(w,sort_keys=True,separators=(',',':')).encode();word.write_bytes(gzip.compress(payload,mtime=0));result={'status':'PASS_SOURCE_BOUND_ANISOTROPIC_RELAY','source_sha256':OLD,'word_sha256':hashlib.sha256(word.read_bytes()).hexdigest(),'word_payload_sha256':hashlib.sha256(payload).hexdigest(),'source_endpoint_columns':400,'remaining_D':76,'forward_completed':0,'new_scalar_events':22,'bill':bill,'old_bill':oldbill,'small_schur_det':str(determinant(A)),'old_small_schur_det':str(determinant(oldA)),'small_inverse_lcm_denominator':math.lcm(*(x.denominator for row in Ai for x in row)),'residue_ranks':ranks,'scalar_mutation_rejected':True,'late_insertion_rejected':True,'isotropic_quarter_control':{'determinant':str(determinant(isoA)),'rank_mod7':ff_rank(isoA,7)},'no_new_movement_or_owned_record':True,'classification':'Actual partial400-input source and arithmetic-unit repair; physical completion, uniform supplier and all foundations remain open. No new kappa.'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))
def prime_factors(n):
 out=[];p=2
 while p*p<=n:
  if n%p==0:
   out.append(p)
   while n%p==0:n//=p
  p+=1
 if n>1:out.append(n)
 return out
if __name__=='__main__':main()
