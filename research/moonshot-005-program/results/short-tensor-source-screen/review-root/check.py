#!/usr/bin/env python3
"""Root independent geometry and full-source price review. No author imports."""
import argparse,gzip,json,hashlib,itertools
from pathlib import Path
from fractions import Fraction as F
from intervals import need,add,moment
PAIRS=((117,107),(114,106),(111,108),(104,110),(115,109),(112,119),(105,118),(116,113))
def brank(vs):
 piv={}
 for v in vs:
  while v:
   b=v&-v
   if b in piv:v^=piv[b]
   else:piv[b]=v;break
 return len(piv)
def qrank(A):
 A=[list(map(F,x))for x in A];rank=0
 for j in range(len(A[0])):
  p=next((i for i in range(rank,len(A))if A[i][j]),None)
  if p is None:continue
  A[rank],A[p]=A[p],A[rank];pivot=A[rank][j]
  for i in range(rank+1,len(A)):
   c=A[i][j]/pivot
   if c:A[i]=[x-c*y for x,y in zip(A[i],A[rank])]
  rank+=1
  if rank==len(A):break
 return rank
def pair(u,v):return(u&v).bit_count()%2
def hist(b,a,price=0):
 h=add((2,{1+2*a*b:1}),*[(4,{1+j*b:1})for j in range(1,a+1)],(-4,{1:1}),*[(-4,{j*b:1})for j in range(1,a)],(-8*a,{b:1}))
 return add((1,h),(-F(32*a,208),{price:1}))if price else h
def expr(*xs):return moment(add(*xs))
def record(x):return dict(exact=list(map(str,x)),decimal=float(x[0]))
def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 freeze=json.loads((a.author/'FREEZE.json').read_text())
 for f,h in freeze.items():need(hashlib.sha256((a.author/f).read_bytes()).hexdigest()==h,'frozen bytes '+f)
 data=json.loads((a.author/'source/lines120.json').read_text());q=data['labels'];G=data['gram']
 need(len(q)==len(set(q))==120,'120 unique roots');need(all(pair(x,x)==1 for x in q),'all odd labels')
 need(all(pair(q[i],q[j])==(G[i][j]+1)%2 and G[i][j]==G[j][i]for i in range(120)for j in range(120)),'14400 full Gram/label identities')
 need(hashlib.sha256(a.native.read_bytes()).hexdigest()=='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883','actual native pin')
 native=json.loads(gzip.decompress(a.native.read_bytes()));actual=[native['frames'][native['initial'][v]][0]for v in native['live']]
 need(set(actual)==set(q[:104])and len(set(actual))==104,'actual native domain, not presumed ordering')
 W=[];U=[];geometry=[]
 for d,e in PAIRS:
  w=[G[i][d]for i in range(104)];u=[F(G[i][e],2*G[d][e])for i in range(104)];W.append(w);U.append(u)
  D=[i for i,x in enumerate(w)if x];S=[i for i,x in enumerate(u)if x]
  db=[q[i]for i in D];sb=[q[i]for i in S];D2=db+[x<<9 for x in db];S2=sb+[x<<9 for x in sb]
  pairing=brank(sum(pair(x,y)<<j for j,y in enumerate(sb))for x in db)
  need((len(D),len(S),brank(db),brank(sb),pairing)==(52,52,8,8,7),'asymmetric row geometry')
  need(all(not pair(q[d],x)for x in db)and all(not pair(q[e],x)for x in sb),'correct distinct hyperplanes')
  need(brank(D2)==brank(S2)==16 and brank(db+sb)==9,'actual tensor support dimensions')
  need(brank(sum(pair(x,y)<<j for j,y in enumerate(D2))for x in D2)==16,'same-support price16 control')
  need(brank(sum(pair(x,y)<<j for j,y in enumerate(S2))for x in D2)==14,'direct tensor pairing rank14')
  geometry.append(dict(D=D,S=S,D2=D2,S2=S2))
 need(all(sum(W[k][i]*U[k][j]for k in range(8))==F(G[i][j],2)for i in range(104)for j in range(104)),'10816 exact decoder entries')
 need(qrank(list(zip(*W)))==qrank(list(zip(*U)))==8,'both factors rank8')
 for i,j in itertools.combinations(range(8),2):
  need(brank(geometry[i]['D2']+geometry[j]['D2'])==brank(geometry[i]['S2']+geometry[j]['S2'])==18,'all56 distinct-row full spans')
 need(any(sum(W[k][i]*U[k][j]*(2 if k==0 else 1)for k in range(8))!=F(G[i][j],2)for i in range(104)for j in range(104)),'incorrect dual coefficient rejected')
 budgets={}
 for a0 in range(1,7):budgets[str(2*a0)]={str(price):record(moment(hist(17,a0,price)))for price in(14,16)}
 need(expr((1,hist(17,4,14)),(-1,hist(17,3,14)))[0]>0 and expr((1,hist(17,5,14)),(-1,hist(17,4,14)))[1]<0,'rank14 total optimum adjacent signs')
 need(expr((F(1,6),hist(17,3,14)),(-F(1,4),hist(17,2,14)))[0]>0 and expr((F(1,8),hist(17,4,14)),(-F(1,6),hist(17,3,14)))[1]<0,'rank14 pernative optimum adjacent signs')
 need(expr((1,hist(17,2,16)),(-1,hist(17,1,16)))[0]>0 and expr((1,hist(17,3,16)),(-1,hist(17,2,16)))[1]<0 and moment(hist(17,2,16))[1]<0,'rank16 global concavity maximum negative')
 station=add((1,{8:1,9:1}),(-1,{17:1}));two=expr((F(1,6),hist(17,3,14)),(-2,station));need(two[1]<0,'two full station cohorts fail')
 one6=expr((1,hist(17,3,14)),(-6,station));one8=expr((1,hist(17,4,14)),(-8,station));need(one6[0]>0 and one8[1]<0,'onecohort scope control passes6 butfails8')
 proper={}
 for c in(16,17,18):
  f=expr((1,{c-2:1}),(104,{c-1:1,18-c:1}),(-104,{17:1}),(-1,{16:1}))if c<18 else(F(0),F(0))
  if c<18:need(f[0]>0,'proper cochart does not underprice Hub row')
  proper[str(c)]=record(f)
 # Root independently checks C's all-arm h9 extension using the actual complete receipt.
 full=json.loads((a.author/'source/retained-FULL-RESULT.json').read_text());net=add((1,full['native']['paid']),(-1,full['native']['helpers']))
 def W(a0):return add((1,hist(8,a0)),(8*a0,{8:1}))
 need(expr((5,W(6)),(-6,W(5)))[0]>0 and expr((6,W(7)),(-7,W(6)))[1]<0,'h9 unique pernative globalmax a6')
 allowed=add((F(104,12),W(6)));conversion=add((1,net),(16,{1:1,8:1}));gap=expr((1,allowed),(-1,conversion));free=expr((1,allowed),(-1,net),(-16,{8:1}));need(gap[1]<0 and free[1]<0,'allarm fixednative conversion fails evenfreequeries')
 out=dict(status='PASS_ROOT_DIRECT_TENSOR_SOURCE_AND_H9_TARIFF_REVIEW',author_proof_sha256=freeze['PROOF.md'],freeze_files=len(freeze),native_labels=104,gram_entries=14400,decoder_entries=10816,tensor_support_dimensions=[16,16],tensor_pairing_rank=14,distinct_row_span_checks=56,budgets=budgets,two_station_cohorts=record(two),one_cohort_control={'six':record(one6),'eight':record(one8)},proper_cochart_excess=proper,h9_all_arm={'pernative_allowance':record(moment(allowed)),'paid_gap':record(gap),'free_queries_gap':record(free)},scope='Direct-original separate-row source and stated nonnegative-helper-net contract; encoded/shared histories and other caller interfaces remain open. Universal route and concavity arguments are independently read, not inferred from finite checks.')
 a.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'])
if __name__=='__main__':main()
