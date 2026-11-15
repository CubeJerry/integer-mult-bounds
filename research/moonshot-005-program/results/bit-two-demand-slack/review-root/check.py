#!/usr/bin/env python3
"""Independent rank-identity validation of all49 virtual-demand certificates."""
import argparse,hashlib,json,re
from pathlib import Path

def rank(rows):
 b={}
 for x in rows:
  while x:
   p=x.bit_length()-1
   if p in b:x^=b[p]
   else:b[p]=x;break
 return len(b)
def xor(rows):
 x=0
 for z in rows:x^=z
 return x
def contained(a,b):return rank(b+a)==rank(b)
def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--certificate',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();nf=a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json';assert hashlib.sha256(nf.read_bytes()).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';assert hashlib.sha256(a.source.read_bytes()).hexdigest()=='8939d815b7e1b1dfa89e3e0a6812e5b427f98ddf3020a3300c6232aaa803db52';roots=json.loads(nf.read_text())['native_roots'];w=json.loads(a.source.read_text());c=json.loads(a.certificate.read_text())
 v={f'X{i}':1<<i for i in range(111)}|{f'Y{i}':1<<(111+i)for i in range(111)};k0=None
 for op in w['operations']:
  if op[0]=='INIT':v[op[1]]=0
  elif op[0]=='ADD':
   if op[1:]==['P0','Y0']:assert k0 is None;k0=v['P0']
   v[op[2]]^=v[op[1]]
  else:assert op[0]=='MOVE'
 assert all(v[f'X{i}']==1<<i for i in range(111));assert v['Y0']==(1<<111)^1
 D=[z for n,z in v.items()if re.fullmatch(r'C\d+_\d+_[01]',n)or n.startswith('EXTRA')];L=[sum(1<<j for j in range(111)if sum(x*y for x,y in zip(roots[i],roots[j]))==0)for i in range(111)];K=[(1<<i)|L[i]for i in range(111)];h=K[0]^K[4];W=[K[i]&sum(1<<j for j in range(111)if(h>>j&1)==(h>>i&1))for i in range(111)];A=D+W;assert (rank(D),rank(W),rank(A))==(42,15,48)
 assert {(x['query'],x['depth'])for x in c['cases']}=={(q,d)for q in range(1,8)for d in range(1,8)}and len(c['cases'])==49;out=[]
 for case in c['cases']:
  q,d=case['query'],case['depth'];R0=xor(z for n,z in v.items()if n.startswith(f'C{q}_')and n.endswith('_0'));N=xor(z for n,z in v.items()if n.startswith(f'C{q}_')and n.endswith('_1')and int(n.split('_')[1])>=d);B=[v['P0'],k0,(1<<q)^R0,N];assert contained(B,D);Js=[];sides=[]
  for obj in case['obligations']:
   i,j=obj['receivers'];delta=(1<<i)^(1<<j);assert contained([W[i]^W[j]],D)
   for t in [i,j]:assert rank(A)-rank([x&~L[t]for x in A])==rank(D)-rank([x&~L[t]for x in D])
   side=B+[1<<t for t in range(111)if(L[i]|L[j])>>t&1];assert not contained([delta],side);J=[int(x,16)for x in obj['J_rows_hex']];assert contained(J,D)and contained(J,side+[delta]);assert rank(J)==rank(D)+rank(side+[delta])-rank(D+side+[delta]);assert rank(J)==obj['J_dimension'];assert not contained(J,side);Js.append(J);sides.append(side)
  assert len(Js)==2;I=[int(x,16)for x in case['intersection_rows_hex']];assert contained(I,Js[0])and contained(I,Js[1]);assert rank(I)==rank(Js[0])+rank(Js[1])-rank(Js[0]+Js[1]);lost=[t for t in range(2)if contained(I,sides[t])];assert lost
  out.append({'query':q,'depth':d,'J_ranks':[rank(x)for x in Js],'I_rank':rank(I),'lost':lost})
 assert all(contained([1<<i],W+[1<<j for j in range(111)if L[i]>>j&1])for i in range(111))
 result={'status':'PASS_ROOT_ALL49_TWO_V_SLACK_CERTIFICATES','cases':out,'universal_conclusion':'dim(T)>=2V for every characteristic-two field and positive block width in the fixed D42 two-feedback scope','independent_method':'actual source replay and rank-dimensional completeness of supplied intersection bases; no author code imported','positive_controls':'each single virtual demand has a scalar slack witness; all W15 globally fits','new_complete_kappa':False};a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'cases':len(out)}))
if __name__=='__main__':main()
