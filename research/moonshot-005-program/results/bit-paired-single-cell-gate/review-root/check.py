#!/usr/bin/env python3
import argparse,hashlib,itertools,json
from pathlib import Path
import sympy as sp
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def main():
 a=argparse.ArgumentParser();a.add_argument('--repo',type=Path,required=True);a.add_argument('--source',type=Path,required=True);a.add_argument('--out',type=Path,required=True);p=a.parse_args();base=p.repo/'research/moonshot-005-program';raw=(base/'sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];word=(base/'results/bit-paired-flag-source/author/output/WORD.json').read_bytes();assert hashlib.sha256(word).hexdigest()=='3aaabaf76bbfabccce40fe2dc56c2dfaf7242061de698d19098d64ef8821a8e5';charts=json.loads(word)['charts'];scan=json.loads((p.source/'SCAN.json').read_text());out={}
 for name,x in scan.items():
  z=x['puncture'];c=charts[name];m=sp.Matrix(c['rows']);basis=m if c['kind']=='span'else sp.Matrix.hstack(*m.nullspace()).T;dim=basis.rank();E=[j for j,r in enumerate(R)if basis.col_join(sp.Matrix([r])).rank()==dim];assert E==z['deleted'];f=z['star']['frame'];assert len(set(f))==8 and not set(E)&set(f);assert all(dot(R[i],R[j])for i,j in itertools.combinations(f,2));edges=z['star']['edges'];assert len({e['role']for e in edges})==len(edges);degrees=[0]*8
  for e in edges:
   i=e['role'];pair=[a for a,j in enumerate(f)if dot(R[i],R[j])==0];assert pair==e['pair']and len(pair)==2 and i not in E and i not in f
   for a in pair:degrees[a]+=1
  assert min(degrees)>=4 and degrees==z['star']['degrees']
  for e,h in itertools.combinations(edges,2):
   if set(e['pair'])&set(h['pair']):assert dot(R[e['role']],R[h['role']])!=0
  out[name]={'rational_chart_rank':dim,'deleted':E,'points':f,'edges':len(edges),'minimum_degree':min(degrees),'all_field_rank_floor_per_width':9}
 assert len(out)==12
 # Independently reject altered source-locality and contact certificates.
 def premise(E,frame,edge):
  assert not set(E)&set(frame)
  assert edge['pair']==[a for a,j in enumerate(frame)if dot(R[edge['role']],R[j])==0]and len(edge['pair'])==2
 z=scan['A3']['puncture'];e=json.loads(json.dumps(z['star']['edges'][0]));f=z['star']['frame']
 failures=[]
 for label,E,edge in [('false local puncture',z['deleted']+[f[0]],e),('wrong edge contact',z['deleted'],dict(e,pair=[0,1,2]))]:
  try:premise(E,f,edge)
  except AssertionError:failures.append(label)
  else:raise AssertionError('mutated certificate accepted')
 assert len(failures)==2
 p.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_INDEPENDENT_TWELVE_PUNCTURES','cases':out,'negative_controls':failures,'universal_argument':'Eight-field punctured factorization versus all-field star rank9V; arbitrary two-packet through maps and nonlocal preloads constrained as stated.','new_complete_kappa':False};(p.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
