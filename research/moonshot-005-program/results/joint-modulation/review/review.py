import argparse,collections,copy,hashlib,json
from fractions import Fraction as Q
from pathlib import Path

def check(x,m):
 if not x:raise ValueError(m)
def rank(M):
 if not M:return 0
 B={}
 for col in zip(*M):
  a={i:Q(v) for i,v in enumerate(col) if v}
  while a:
   p=max(a)
   if p not in B:
    z=a[p];B[p]={i:v/z for i,v in a.items()};break
   z=a[p]
   for i,v in B[p].items():
    y=a.get(i,Q(0))-z*v
    if y:a[i]=y
    else:a.pop(i,None)
 return len(B)
def execute(P):
 spaces=[frozenset([0]),frozenset([0,1]),frozenset([0,1,2,3])];state={i:[Q(i==j) for j in range(5)] for i in range(5)};loc={i:0 for i in range(5)};ops=collections.Counter();life=peak=0;trace=[]
 for e in P:
  op,j=e[:2];ops[op]+=1;trace.append({i:r[:] for i,r in state.items()})
  if op=='INIT':check(j==5 and j not in state,'fresh owned INIT');state[j]=[Q(0)]*5;loc[j]=e[2];life+=1
  elif op=='CLEAR':check(j==5 and loc[j]==e[2],'owned CLEAR');del state[j];del loc[j]
  elif op=='MOVE':
   a,b,own=e[2:];check(loc[j]==a and own==(j==5),'physical route/ownership');check(spaces[a]<spaces[b] or own and spaces[b]<spaces[a],'strict nested chart route');loc[j]=b
  elif op=='ADD':
   s,c,f=e[2:];check(j!=s and loc[j]==loc[s]==f,'cochart ADD');state[j]=[a+Q(c)*b for a,b in zip(state[j],state[s])]
  else:raise ValueError('unexpected opcode')
  peak=max(peak,len(state)-5)
 return state,loc,ops,life,peak,trace

def main(args):
 p=args.packet;c=json.loads((p/'CERTIFICATE.json').read_text());P=c['toy_word'];S=c['toy_common_source'];state,loc,ops,life,peak,trace=execute(P);want={i:[Q(i==j) for j in range(5)] for i in range(5)};want[4][3]=Q(1)
 check(state==want,'all five symbolic input columns');check(loc=={0:2,1:1,2:2,3:2,4:1},'all final typed charts');check(dict(ops)=={'INIT':1,'ADD':8,'MOVE':8,'CLEAR':1} and life==peak==1,'complete instruction/lifetime counts')
 at=0;used=[]
 for i,e in enumerate(P):
  if at<len(S) and e==S[at]:used.append(i);at+=1
 check(at==len(S)==11,'native common subsequence');extra=[e for i,e in enumerate(P) if i not in used];check(collections.Counter(e[0] for e in extra)=={'ADD':5,'MOVE':2},'five extra ADDs plus two raw reservations')
 for raw,common in [(3,2),(4,1)]:check([e[2:4] for e in P if e[0]=='MOVE' and e[1]==raw]==[e[2:4] for e in S if e[0]=='MOVE' and e[1]==common],'raw route lineage')
 sr,_,_,_,_,_=execute(S);check(all(sr[i][j]==Q(i==j) for i in range(5) for j in range(5)),'native common baseline')
 A=[];B=[[],[]]
 for enabled in [4,6]:
  toy=copy.deepcopy(P)
  for i in [4,6]:toy[i][3]='1' if i==enabled else '0'
  rr,_,_,_,_,tr=execute(toy);A.append(rr[1][3]);B[0].append(tr[3][0][3]);B[1].append(tr[9][0][3])
 check(A==[Q(1),Q(-1)] and B==[[Q(0),Q(0)],[Q(1),Q(0)]],'source-derived A and B')
 F0=[[1,0,0],[1,0,0]];G=[A+[0,0,0]]+[a+b for a,b in zip(B,F0)];check(rank(G)==3 and rank([A])==1 and rank(F0)==1,'joint rank excess one')
 for j in range(2):
  aa=[[A[j]]];bb=[[r[j]] for r in B];gg=[aa[0]+[0,0,0]]+[a+b for a,b in zip(bb,F0)];check(rank(gg)-rank(aa)-rank(F0)==0,'each individual pulse fails')
 controls=[]
 for name,index,field in [('omit compensation',6,1),('omit noise observation',3,4),('omit restoration',17,0)]:
  rr,_,_,_,_,_=execute(P[:index]+P[index+1:]);error=[a-b for a,b in zip(rr[field],want[field])];check(any(error),'negative endpoint control');controls.append({'mutation':name,'error':[str(v) for v in error]})
 try:execute(P[:5]+P[6:])
 except ValueError as e:controls.append({'mutation':'omit funded raw donor MOVE','rejection':str(e)})
 else:raise ValueError('invalid source access accepted')
 result={'status':'PASS_INDEPENDENT_JOINT_MODULATION_REVIEW','proof_sha256':hashlib.sha256((p/'PROOF.md').read_bytes()).hexdigest(),'certificate_sha256':hashlib.sha256((p/'CERTIFICATE.json').read_bytes()).hexdigest(),'block_rank':3,'rank_A':1,'rank_F0':1,'joint_excess':1,'individual_excesses':[0,0],'toy_instructions':18,'symbolic_inputs':5,'new_ADDs':5,'new_MOVEs':0,'new_owned_lifetimes':0,'negative_controls':controls,'independence':'Fresh dense symbolic replay, explicit nested binary chart sets, independent column-span rank and literal pulse toggles; no author verifier import.'};args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(result['status'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
