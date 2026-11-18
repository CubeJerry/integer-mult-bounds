#include <algorithm>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <vector>
struct Edge{int to,back,cap;};
struct Net{
 std::vector<std::vector<Edge>> g;std::vector<int> level,iter;
 Net(int n):g(n),level(n),iter(n){}
 void add(int u,int v,int c){int x=g[u].size(),y=g[v].size();g[u].push_back({v,y,c});g[v].push_back({u,x,0});}
 bool layer(){fill(level.begin(),level.end(),-1);std::queue<int>Q;level[0]=0;Q.push(0);
 while(!Q.empty()){int u=Q.front();Q.pop();for(auto&e:g[u])if(e.cap&&level[e.to]<0){level[e.to]=level[u]+1;Q.push(e.to);}}return level[1]>=0;}
 int step(int u,int c){if(u==1)return c;for(int &k=iter[u];k<(int)g[u].size();++k){Edge&e=g[u][k];if(e.cap&&level[e.to]==level[u]+1){int f=step(e.to,std::min(c,e.cap));if(f){e.cap-=f;g[e.to][e.back].cap+=f;return f;}}}return 0;}
 int solve(){int t=0;while(layer()){fill(iter.begin(),iter.end(),0);while(int f=step(0,1000000))t+=f;}return t;}
};
int main(){int j,n,m,k;while(std::cin>>j>>n>>m>>k){Net g(n);std::vector<std::vector<int>>es;
 for(int u,v,c,z=0;z<m;++z){std::cin>>u>>v>>c;es.push_back({u,v,c,(int)g.g[u].size()});g.add(u,v,c);}
 int f=g.solve();std::vector<int>balance(n);for(auto&e:es){int a=e[2]-g.g[e[0]][e[3]].cap;if(a<0||a>e[2])return 2;balance[e[0]]+=a;balance[e[1]]-=a;}
 if(balance[0]!=f||balance[1]!=-f)return 3;for(int u=2;u<n;++u)if(balance[u])return 4;
 std::cout<<j<<" "<<k<<" "<<f<<"\n";}}
