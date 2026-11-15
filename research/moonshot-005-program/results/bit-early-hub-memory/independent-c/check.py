from pathlib import Path
import json,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--source',type=Path,default=Path(__file__).parent.parent/'shared-facet-coding');a=p.parse_args();raw=(a.repo/'research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e';R=json.loads(raw)['native_roots'];w=json.loads((a.source/'four-chart-word/WORD.json').read_text());dot=lambda a,b:sum(x*y for x,y in zip(a,b))
def rank(rows):
 B={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in B:v^=B[p]
   else:B[p]=v;break
 return len(B)
def xor(rows):
 z=0
 for v in rows:z^=v
 return z
X=[f'X{j}_{k}'for j in range(111)for k in range(4)];Y=[f'Y{j}_{k}'for j in range(111)for k in range(4)];v={n:1<<i for i,n in enumerate(X+Y)};D={n:v[n]for n in X};loc={n:f'L{i//4}'for i,n in enumerate(X)}|{n:'zero'for n in Y}
for o in w['operations'][:w['milestones']['all_chart_aggregates_formed']]:
 if o[0]=='ADD':
  src,dst=o[1:];v[dst]^=v[src]
  if src in D and dst in D:D[src]^=D[dst]
 elif o[0]=='MOVE':loc[o[1]]=o[2]
 else:raise AssertionError(o)
H=[v[n]for n in X if loc[n]=='Hub'];held=[n for n in X if loc[n]!='Hub'];Q=[v[n]for n in held];C=[sum(1<<(4*j+k)for j in range(111)if i==j or dot(R[i],R[j])==0)for i in range(111)for k in range(4)];S=[v[n]&((1<<444)-1)for n in Y];groups={}
for ch in sorted({loc[n]for n in held}):
 ns=[n for n in held if loc[n]==ch];cols=[D[n]for n in ns]
 def restriction(rows):return rank([sum(((u&z).bit_count()%2)<<j for j,z in enumerate(cols))for u in rows])
 groups[ch]={'records':ns,'inverse_columns_hex':[hex(z)for z in cols],'Y_restriction_rank':restriction(S),'plus_two_actual_pivot_copies_rank':restriction(S+[v[n]for n in ns]),'plus_one_copy_rank':restriction(S+[v[ns[0]]])};assert groups[ch]['Y_restriction_rank']==0 and groups[ch]['plus_two_actual_pivot_copies_rank']==2 and groups[ch]['plus_one_copy_rank']==1
proj=[xor(v[n]for n in X if loc[n]=='Hub'and(u&D[n]).bit_count()%2)for u in C]
assert rank(H)==440 and rank(Q)==4 and rank(H+Q)==444 and rank(C)==36;assert rank(H)+rank(C)-rank(H+C)==32;assert rank(Q)+rank(C)-rank(Q+C)==0;assert rank(proj)==36 and rank(proj+Q)==40
r={'status':'PASS_INDEPENDENT_RETAINED_MEMORY_AND_CANONICAL_PROJECTION','groups':groups,'Hub_rank':440,'held_rank':4,'canonical_rank':36,'canonical_intersection_Hub':32,'canonical_intersection_held':0,'actual_Hub_projection_of_canonical_rank':36,'canonical_plus_held_rank':40,'source_word_sha256':hashlib.sha256((a.source/'four-chart-word/WORD.json').read_bytes()).hexdigest()};(Path(__file__).parent/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
