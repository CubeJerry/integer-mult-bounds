from itertools import combinations,product
from pathlib import Path
import json

def span(rows):
 S={0}
 for v in rows:S|={s^v for s in tuple(S)}
 return tuple(sorted(S))
def pairing(u,v):return (((u&7)&(v>>3)).bit_count()+((v&7)&(u>>3)).bit_count())&1
spaces={};allspaces=0
for piv in combinations(range(6),3):
 positions=[(r,c)for r,p in enumerate(piv)for c in range(p+1,6)if c not in piv]
 for mask in range(1<<len(positions)):
  rows=[1<<p for p in piv]
  for k,(r,c)in enumerate(positions):
   if mask>>k&1:rows[r]|=1<<c
  allspaces+=1
  if any(pairing(rows[i],rows[j])for i in range(3)for j in range(i)):continue
  s=span(rows);assert s not in spaces;spaces[s]=rows
assert allspaces==1395 and len(spaces)==135
Ls=sorted(spaces);idx={s:i for i,s in enumerate(Ls)};dist=[3-((sum((v>>3)==0 for v in s)).bit_length()-1)for s in Ls];assert [dist.count(d)for d in range(4)]==[1,14,56,64]
def swap(v,r):
 for j in range(r):
  if ((v>>j)^(v>>(j+3)))&1:v^=(1<<j)|(1<<(j+3))
 return v
perms=[[idx[tuple(sorted(swap(v,r)for v in s))]for s in Ls]for r in range(4)]
table=[]
for mask in range(8):
 S={i for i,d in enumerate(dist)if d and mask>>(d-1)&1};h=[]
 for r in range(4):
  gS={perms[r][i]for i in S};assert len(S^gS)%2==0;h.append(len(S^gS)//2)
 table.append({'cut_mask':mask,'selected_distances':[d for d in range(1,4)if mask>>(d-1)&1],'size':len(S),'h':h,'deficit2':2*h[1]-h[2],'deficit3':3*h[1]-h[3]})
print(json.dumps(table,indent=2))
out={'status':'INDEPENDENT_RREF_ENUMERATION','all_three_subspaces':allspaces,'lagrangians':135,'radial_orbit_sizes':[1,14,56,64],'cuts':table};(Path(__file__).parent/'TABLE.json').write_text(json.dumps(out,indent=2)+'\n')
# Full Siegel parabolic: GL(3,2) elementary transvections and all symmetric shears.
generators=[];labels=[]
for i in range(3):
 for j in range(3):
  if i==j:continue
  def f(v,i=i,j=j):return v ^ (((v>>j)&1)<<i) ^ (((v>>(i+3))&1)<<(j+3))
  generators.append(f);labels.append(f'GL_transvection_{i}_{j}')
for i in range(3):
 for j in range(i,3):
  def f(v,i=i,j=j):
   if i==j:return v ^ (((v>>(i+3))&1)<<i)
   return v ^ (((v>>(j+3))&1)<<i) ^ (((v>>(i+3))&1)<<j)
  generators.append(f);labels.append(f'symmetric_shear_{i}_{j}')
Hperms=[];L0=idx[span([1,2,4])]
for f in generators:
 assert all(pairing(f(u),f(v))==pairing(u,v)for u in range(64)for v in range(64))
 p=[idx[tuple(sorted(f(v)for v in s))]for s in Ls];assert sorted(p)==list(range(135))and p[L0]==L0;Hperms.append(p)
seen=set();orbits=[]
for i in range(135):
 if i in seen:continue
 orb={i};queue=[i]
 for v in queue:
  for p in Hperms:
   z=p[v]
   if z not in orb:orb.add(z);queue.append(z)
 seen|=orb;assert len({dist[x]for x in orb})==1;orbits.append({'distance':dist[i],'size':len(orb)})
assert sorted(orbits,key=lambda z:z['distance'])==[{'distance':d,'size':n}for d,n in enumerate([1,14,56,64])]
for mask in range(8):
 S={i for i,d in enumerate(dist)if d and mask>>(d-1)&1}
 assert all({p[i]for i in S}==S for p in Hperms)
 assert table[mask]['h'][2]<=table[mask]['h'][1]
 assert 4*table[mask]['h'][3]<=5*table[mask]['h'][1]
# Complement symmetry; invalid non-H-invariant singleton away from L0 is rejected as a free potential.
for mask in range(8):
 S={i for i,d in enumerate(dist)if d and mask>>(d-1)&1};T=set(range(135))-S
 assert [len(T^{perms[r][i]for i in T})//2 for r in range(4)]==table[mask]['h']
wrong={next(i for i,d in enumerate(dist)if d==1)};assert any({p[i]for i in wrong}!=wrong for p in Hperms)
out.update({'full_parabolic_generators':labels,'verified_parabolic_orbits':sorted(orbits,key=lambda z:z['distance']),'exact_cone_separator':'h2 <= h1, and4h3 <=5h1 for every nonnegative combination; every nontrivial cut has h1>0.','positive_controls':['complement invariance','all rank0 parabolic generators have zero length'],'negative_control':'A singleton off L0 fails full-parabolic invariance.'});(Path(__file__).parent/'TABLE.json').write_text(json.dumps(out,indent=2)+'\n');print('Full H orbits verified; h2<=h1 cone separator PASS')
# Exact polynomial certificate for arbitrary Hilbert-valued radial functions.
Ns=[]
for r in range(4):
 N=[[0]*4 for _ in range(4)]
 for i in range(135):N[dist[i]][dist[perms[r][i]]]+=1
 assert all(sum(N[d])==[1,14,56,64][d]for d in range(4));assert all(N[d][e]==N[e][d]for d in range(4)for e in range(4));Ns.append(N)
Q=[[[int(i==j)*[1,14,56,64][i]-Ns[r][i][j]for j in range(4)]for i in range(4)]for r in range(4)];A=[1,-3,2,0];B=[0,1,-3,2]
assert all(3*Q[1][i][j]-2*Q[2][i][j]==A[i]*A[j]+8*B[i]*B[j]for i in range(4)for j in range(4));sharp=[7,3,1,0];qs=[sum(sharp[i]*Q[r][i][j]*sharp[j]for i in range(4)for j in range(4))for r in range(4)];assert qs[1:3]==[96,144]
def swap_one(v,j):return v^((1<<j)|(1<<(j+3)))if((v>>j)^(v>>(j+3)))&1 else v
pairs=[]
for rows in[[1,2,4],[1,2,32],[3,4,24]]:
 assert all(pairing(u,v)==0 for u in rows for v in rows);s=span(rows);images=[s,span([swap_one(v,0)for v in rows]),span([swap_one(v,1)for v in rows]),span([swap_one(swap_one(v,0),1)for v in rows])];pairs.append({'basis_vectors':rows,'distance_tuple':[dist[idx[t]]for t in images]})
assert[p['distance_tuple']for p in pairs]==[[0,1,1,2],[1,2,2,3],[1,2,2,1]]
out.update({'orbit_intersection_matrices':Ns,'Hilbert_Gram_identity':{'A':A,'B':B,'formula':'3Q1-2Q2=A*A^T+8B*B^T','sharp_orbit_values':sharp,'sharp_q1_q2':[96,144]},'three_space_mixed_difference_certificate':pairs});(Path(__file__).parent/'TABLE.json').write_text(json.dumps(out,indent=2)+'\n');print('Arbitrary radial Hilbert identity and three-space certificate PASS')
