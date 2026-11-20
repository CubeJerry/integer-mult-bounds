"""Nine terminal-pivot flows certify native chart-change volume for arbitrary Clifford frames."""
from collections import deque
from fractions import Fraction as Q
from hashlib import sha256
from functools import cache
from pathlib import Path
import argparse,gzip,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from check import Model,dim,extend,ZERO,WORD,UNIT,power,need

power=cache(power)

BASIS=[436,252,65,45,19,7,2,9,1]
APPLICATION='1b2d87e93ae023f5ffd464546af53281b6cb4963dfd76ae4742e0a5540b752fa'

class Network:
    def __init__(self,n):
        self.g=[[]for _ in range(n)];self.source=n-2;self.sink=n-1
    def add(self,u,v,cap):
        to=[v,cap,len(self.g[v])];back=[u,0,len(self.g[u])];self.g[u].append(to);self.g[v].append(back)
    def solve(self):
        s,t=self.source,self.sink;flow=0
        while True:
            dist=[-1]*len(self.g);dist[s]=0;q=deque([s]);
            while q:
                u=q.popleft()
                for v,cap,_ in self.g[u]:
                    if cap and dist[v]<0:dist[v]=dist[u]+1;q.append(v)
            if dist[t]<0:return flow,{i for i,x in enumerate(dist)if x>=0}
            cursor=[0]*len(self.g)
            def augment(u,maxcap):
                if u==t:return maxcap
                while cursor[u]<len(self.g[u]):
                    a=self.g[u][cursor[u]];v,cap,rev=a
                    if cap and dist[v]==dist[u]+1:
                        d=augment(v,min(maxcap,cap))
                        if d:a[1]-=d;self.g[v][rev][1]+=d;return d
                    cursor[u]+=1
                return 0
            while more:=augment(s,10**20):flow+=more

def flag_bits(m,basis):
    F=ZERO;last={v:0 for v in m.site};allbits=[]
    for i,x in enumerate(basis,1):
        F=extend(F,x);need(dim(F)==i,'independent flag basis');current={v:dim(F&U)for v,U in m.site.items()};b={v:current[v]-last[v]for v in m.site};need(set(b.values())<={0,1},'one-dimensional increments');allbits.append(b);last=current
    return allbits

def cuts(model,bits,edges,capacities):
    n=len(model.site);out=[];inc=[]
    for j,b in enumerate(bits):
        nw=Network(n+2);inf=sum(row[j]for row in capacities)+1
        for v in model.pinned:
            if b[v]:nw.add(n,v,inf)
            else:nw.add(v,n+1,inf)
        for (u,v),cs in zip(edges,capacities):nw.add(u,v,cs[j]);nw.add(v,u,cs[j])
        value,S=nw.solve();cut=sum(cs[j]for (u,v),cs in zip(edges,capacities)if(u in S)!=(v in S));need(cut==value and all((v in S)==bool(b[v])for v in model.pinned),'primal flow and dual cut');out.append(value)
        inc.append(sum(cs[j]for (u,v),cs in zip(edges,capacities)if b[u]!=b[v]))
    return out,inc

def moment(hist):
    lo=hi=0
    for grade,n in hist.items():
        l,h=power(int(grade));
        if n<0:l,h=h,l
        lo+=l*n;hi+=h*n
    return Q(lo,UNIT),Q(hi,UNIT)

def fmt(x):return str(int(x*10**10)/10**10)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--application',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--capacity',type=Path);a=ap.parse_args();raw=gzip.decompress(a.source.read_bytes());appraw=gzip.decompress(a.application.read_bytes());need(sha256(raw).hexdigest()==WORD and sha256(appraw).hexdigest()==APPLICATION,'pinned physical word and caller');w=json.loads(raw);app=json.loads(appraw);m=Model(w);pairs={tuple(sorted(e)):n for e,n in m.multiplicity.items()};edges=sorted(pairs);bits=flag_bits(m,BASIS);f,g=cuts(m,bits,edges,[[pairs[e]]*9 for e in edges]);volume=sum(f);need(f==g and volume==9646,'sharp original-grade volume equality');inv=app['caller_census'];calls=inv['calls'];T=moment(inv['fixed_root_targets']);P=moment(inv['fixed_caller_paid']);H=moment(app['native']['positive_helper_ranks']);allow=((T[0]-P[1])/calls+H[0],(T[1]-P[0])/calls+H[1]);count=len(w['moves']);alpha=Q(power(9)[0],UNIT)/8-Q(1,8)
    def bound(z):alive=count-z;return alive+alpha*(volume-alive)
    threshold=next(z for z in range(count+1)if bound(z)<allow[1]);need(threshold==827 and bound(threshold-1)>allow[1],'whole-caller minimum zero-grade count');out={'source_sha256':WORD,'independent_paid_events':count,'flag_basis':BASIS,'primal_integer_flows':f,'incumbent_cut_sizes':g,'optimal_cumulative_paid_grade':volume,'positive_only_native_moment_lower_floor_10dp':fmt(bound(0)),'native_moment_limit_floor_10dp':fmt(allow[0]),'mandatory_zero_grade_positions_for_one_over_200':threshold,'lower_price_with_826_zeroes_floor_10dp':fmt(bound(826)),'lower_price_with_827_zeroes_floor_10dp':fmt(bound(827))}
    if a.capacity:
        d=json.loads(gzip.decompress(a.capacity.read_bytes()));scale=d['scale'];need(isinstance(scale,int)and scale>0,'positive exact capacity scale');rows=d['edges'];dem={tuple(sorted((u,v))):c for u,v,c in rows};need(len(rows)==len(edges)and set(dem)==set(edges),'exactly one capacity vector per true edge pair');caps=[]
        for e in edges:
            cs=dem[e];need(len(cs)==9 and all(isinstance(c,int)and c>=0 for c in cs),'capacity domain');ordc=sorted(cs,reverse=True);mu=pairs[e]
            for k in range(1,10):need(sum(ordc[:k])*UNIT<=scale*mu*power(k)[0],'edge capacity majorization')
            caps.append(cs)
        xx,_=cuts(m,flag_bits(m,d['basis']),edges,caps);money=Q(sum(xx),scale);out['weighted_flag_flow']={'basis':d['basis'],'scale':scale,'exact_capacitated_flows':xx,'native_moment_lower':str(money),'strict_obstruction':money>allow[1]}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'FLAG-RESULT.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('PASS_SHARP_NATIVE_CLIFFORD_VOLUME',out)
if __name__=='__main__':main()
