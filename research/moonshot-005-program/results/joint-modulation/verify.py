#!/usr/bin/env python3
"""Exact joint-rank criterion and five-input illustrative typed word."""
import argparse,collections,hashlib,json
from fractions import Fraction as F
from pathlib import Path
def need(x,m):
 if not x:raise ValueError(m)
def rank(rows):
 a=[[F(v) for v in r] for r in rows];h=0
 for j in range(len(a[0]) if a else 0):
  p=next((i for i in range(h,len(a)) if a[i][j]),None)
  if p is None:continue
  a[h],a[p]=a[p],a[h];z=a[h][j];a[h]=[v/z for v in a[h]]
  for i in range(len(a)):
   if i!=h and a[i][j]:z=a[i][j];a[i]=[x-z*y for x,y in zip(a[i],a[h])]
  h+=1
 return h
def multiply(a,b):return [[sum((F(x)*F(b[k][j]) for k,x in enumerate(row)),F(0)) for j in range(len(b[0]))] for row in a]
def add(a,b,c):
 z=a.copy()
 for i,v in b.items():
  t=z.get(i,F(0))+c*v
  if t:z[i]=t
  else:z.pop(i,None)
 return z
def show(a):return {str(i):str(v) for i,v in sorted(a.items())}
def word():
 return [['INIT',5,0],['ADD',5,0,'1',0],['MOVE',5,0,2,True],['ADD',4,0,'-1',0],['ADD',0,3,'1',0],['MOVE',3,0,2,False],['ADD',5,3,'1',2],['MOVE',0,0,1,False],['MOVE',4,0,1,False],['ADD',4,0,'1',1],['MOVE',1,0,1,False],['ADD',1,0,'1',1],['MOVE',0,1,2,False],['MOVE',5,2,1,True],['ADD',1,5,'-1',1],['CLEAR',5,1],['MOVE',2,0,2,False],['ADD',0,3,'-1',2]]
def source_word():
 return [['INIT',5,0],['ADD',5,0,'1',0],['MOVE',5,0,2,True],['MOVE',0,0,1,False],['MOVE',1,0,1,False],['ADD',1,0,'1',1],['MOVE',0,1,2,False],['MOVE',5,2,1,True],['ADD',1,5,'-1',1],['CLEAR',5,1],['MOVE',2,0,2,False]]
def replay(P):
 r={i:{i:F(1)} for i in range(5)};chart={i:0 for i in range(5)};bill=collections.Counter();life=peak=0
 for e in P:
  op,j=e[:2];bill[op]+=1
  if op=='INIT':need(j==5 and j not in chart,'owned INIT');r[j]={};chart[j]=e[2];life+=1
  elif op=='CLEAR':need(j==5 and chart[j]==e[2],'owned CLEAR');r.pop(j);chart.pop(j)
  elif op=='MOVE':
   a,b,o=e[2:];need(chart[j]==a and type(o)is bool and o==(j==5),'typed route');need(a<b or o and b<a,'proper nested toy route');chart[j]=b
  elif op=='ADD':need(j!=e[2] and chart[j]==chart[e[2]]==e[4],'cochart ADD');r[j]=add(r[j],r[e[2]],F(e[3]))
  else:raise ValueError('unknown op')
  peak=max(peak,len(chart)-5)
 return r,chart,{'instructions':len(P),'counts':dict(sorted(bill.items())),'owned_lifetimes':life,'peak_owned':peak,'final_owned':len(chart)-5}
def run(packet,write):
 A=[[1,-1]];B=[[0,0],[1,0]];F0=[[1,0,0],[1,0,0]];K=[[1],[1]];Z=[[-1,1]];block=[A[0]+[0,0,0]]+[b+f for b,f in zip(B,F0)];M=multiply(multiply(Z,B),K)
 need(multiply(A,K)==[[0]] and multiply(Z,F0)==[[0,0,0]],'exact kernel/left-null bases');need(M==[[1]] and rank(block)-rank(A)-rank(F0)==rank(M)==1,'joint exact rank excess')
 individual=[]
 for j in range(2):
  a=[[A[0][j]]];b=[[row[j]] for row in B];g=[a[0]+[0,0,0]]+[x+y for x,y in zip(b,F0)];ex=rank(g)-rank(a)-rank(F0);need(ex==0,'individual neutral pulse must fail');individual.append(ex)
 P=word();source=source_word();need([P[i] for i in [0,1,2,7,10,11,12,13,14,15,16]]==source,'all original common instructions kept in order');need(P[5]==['MOVE',3,0,2,False] and P[8]==['MOVE',4,0,1,False] and source[10]==['MOVE',2,0,2,False] and source[4]==['MOVE',1,0,1,False],'exact two raw reservation lineages')
 r,c,bill=replay(P);wanted={0:{0:F(1)},1:{1:F(1)},2:{2:F(1)},3:{3:F(1)},4:{4:F(1),3:F(1)}};need(r==wanted and c=={0:2,1:1,2:2,3:2,4:1},'full five-input endpoint/charts');need(bill=={'instructions':18,'counts':{'ADD':8,'CLEAR':1,'INIT':1,'MOVE':8},'owned_lifetimes':1,'peak_owned':1,'final_owned':0},'complete tariff')
 sr,sc,sbill=replay(source);need(all(sr[i]=={i:F(1)} for i in range(5)) and sbill['instructions']==11,'unmodified toy common baseline')
 controls=[]
 for name,k,outfield in [('omit_second_pulse',6,1),('omit_initial_noise_observation',3,4),('omit_terminal_restoration',17,0)]:
  bad=P[:k]+P[k+1:];rr,_,_=replay(bad);err=add(rr[outfield],wanted[outfield],F(-1));need(bool(err),'must reject '+name);controls.append({'mutation':name,'field':outfield,'exact_error':show(err)})
 need(multiply([[0,1]],F0)!=[[0,0,0]],'noisy decoder rejected');controls.append({'mutation':'use_only_later_helper_read','rejection':'dF0 is nonzero'})
 result={'status':'PASS_JOINT_MODULATION_CRITERION_AND_TYPED_TOY','scope':'Universal matrix criterion and explicit illustrative network; no frozen-native crossing or new kappa.','A':A,'B':B,'F0':F0,'K':K,'Z':Z,'ZBK':[[str(v) for v in row] for row in M],'block_rank':rank(block),'rank_A':rank(A),'rank_F0':rank(F0),'rank_excess':1,'individual_control_excesses':individual,'toy_word':P,'toy_common_source':source,'endpoint_rows':{str(i):show(v) for i,v in r.items()},'tariff':bill,'baseline_native_instructions':11,'baseline_raw_MOVEs':2,'additional_ADDs':5,'additional_MOVEs':0,'additional_owned_lifetimes':0,'negative_controls':controls,'new_complete_kappa':None};text=json.dumps(result,indent=2,sort_keys=True)+'\n';path=packet/'CERTIFICATE.json'
 if write:path.write_text(text)
 else:need(path.read_text()==text,'certificate reconstruction')
 return {'status':result['status'],'certificate_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'rank_excess':1,'toy_instructions':18,'symbolic_input_directions':5,'negative_controls':4,'new_complete_kappa':None}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--write-certificate',action='store_true');p.add_argument('--output',type=Path);a=p.parse_args();r=run(a.packet,a.write_certificate);s=json.dumps(r,indent=2,sort_keys=True)+'\n'
 if a.output:a.output.write_text(s)
 print(s,end='')
