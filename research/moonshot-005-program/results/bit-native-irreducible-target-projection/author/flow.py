"""Exact integral late-flow construction around the fixed D12 tile."""
from collections import defaultdict,deque
class Dinic:
 def __init__(self,n):self.g=[[]for _ in range(n)];self.original=[]
 def add(self,u,v,c):
  a=[v,c,len(self.g[v])];b=[u,0,len(self.g[u])];self.g[u].append(a);self.g[v].append(b);self.original.append((u,len(self.g[u])-1,c))
 def flow(self,s,t):
  total=0
  while True:
   level=[-1]*len(self.g);level[s]=0;q=deque([s])
   while q:
    u=q.popleft()
    for v,c,r in self.g[u]:
     if c and level[v]<0:level[v]=level[u]+1;q.append(v)
   if level[t]<0:return total
   it=[0]*len(self.g)
   def dfs(u,f):
    if u==t:return f
    while it[u]<len(self.g[u]):
     edge=self.g[u][it[u]];v,c,r=edge
     if c and level[v]==level[u]+1:
      got=dfs(v,min(f,c))
      if got:edge[1]-=got;self.g[v][r][1]+=got;return got
     it[u]+=1
    return 0
   while (v:=dfs(s,10**9)):total+=v
def construct(routes,layout,remaining,tile_yout,tile_dest,amount=8):
 def fid(j,c):return 111*480+j*480+c
 H=list(map(set,layout['A2']));D=list(map(set,layout['D4']));roots=layout['root_table']
 O={j for j,r in enumerate(roots)if sum(a*b for a,b in zip(roots[80],r))==0}
 relevant={d for d,W in enumerate(D)if W<=O and d!=12}
 LH=defaultdict(list);HD=defaultdict(list);DK=defaultdict(list);KF=defaultdict(list)
 reserved=set(tile_dest.values())|set(tile_yout.values())
 for kind,j,c,h,d,k,line,term in routes:
  if kind!='Y':continue
  f=fid(j,c)
  if line in remaining:LH[line,h].append(f)
  if d in relevant:
   if h is not None:HD[h,d].append(f)
   if f not in reserved and 80 in H[k]:DK[d,k].append(f)
  if j==80 and f not in set(tile_dest.values()):KF[k].append(f)
 keys=[('s',),('t',)]+[('j',j)for j in remaining]+[('h',h)for h in sorted({h for h,d in HD})]+[('d',d)for d in sorted(relevant)]+[('k',k)for k in sorted(KF)]
 ids={key:i for i,key in enumerate(keys)};network=Dinic(len(keys));meta=[]
 def add(a,b,c,typ,key):
  if c and a in ids and b in ids:network.add(ids[a],ids[b],c);meta.append((typ,key))
 for j in remaining:add(('s',),('j',j),amount,'source',j)
 for (j,h),owners in sorted(LH.items()):add(('j',j),('h',h),len(owners),'LH',(j,h))
 for (h,d),owners in sorted(HD.items()):add(('h',h),('d',d),len(owners),'HD',(h,d))
 for (d,k),owners in sorted(DK.items()):add(('d',d),('k',k),len(owners),'DK',(d,k))
 for k,owners in sorted(KF.items()):add(('k',k),('t',),len(owners),'KF',k)
 total=network.flow(ids['s',],ids['t',]);print('LATE_FLOW',total,'of',len(remaining)*amount,flush=True)
 assert total==len(remaining)*amount
 used=defaultdict(dict)
 for (u,index,capacity),(typ,key)in zip(network.original,meta):
  e=network.g[u][index];f=capacity-e[1]
  if f:used[u][e[0]]=f
 counts=defaultdict(int);paths=[]
 for j in remaining:
  for t in range(amount):
   nodes=[ids['j',j]]
   while nodes[-1]!=ids['t',]:
    u=nodes[-1];v=next(v for v,f in used[u].items()if f);used[u][v]-=1;nodes.append(v)
   assert [keys[n][0]for n in nodes]==['j','h','d','k','t']
   h,d,k=[keys[n][1]for n in nodes[1:4]];owners=[]
   for label,key,bank in [('LH',(j,h),LH),('HD',(h,d),HD),('DK',(d,k),DK),('KF',k,KF)]:
    index=counts[label,key];owners.append(sorted(bank[key])[index]);counts[label,key]+=1
   paths.append({'donor':j,'coordinate':t,'H':h,'D':d,'K':k,'owners':owners})
 for t in range(4):assert len({p['owners'][t]for p in paths})==len(paths)
 return paths
