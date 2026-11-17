#include <array>
#include <bitset>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>

// A pair (x,y) of absent donors forces r absent if (r,x) and (r,y)
// are active nonorthogonal edges on two different real two-planes.
using Mask = std::bitset<111>;
using Root = std::array<int,8>;
int main() {
    std::array<Root,111> roots{};
    for (auto &s: roots) for (int &x:s) if (!(std::cin>>x)) return 2;
    int dot[111][111]{};
    for(int i=0;i<111;++i)for(int j=0;j<111;++j)
        for(int a=0;a<8;++a)dot[i][j]+=roots[i][a]*roots[j][a];
    std::map<int,int> rounds, degrees;
    long long seed_count=0, singleton_count=0;
    for(int i=0;i<111;++i) {
        std::vector<int> roles;
        for(int j=0;j<111;++j) if(dot[i][j]==0)roles.push_back(j);
        int n=roles.size(); ++degrees[n];
        Mask full; for(int j=0;j<n;++j) full.set(j);
        Mask implications[63][63];
        for(int x=0;x<n;++x)for(int y=x+1;y<n;++y)
            for(int r=0;r<n;++r)if(r!=x && r!=y) {
                int u=dot[roles[r]][roles[x]],v=dot[roles[r]][roles[y]],
                    w=dot[roles[x]][roles[y]];
                // det of the 3x3 Gram matrix, valid because all squared lengths equal 4.
                int det=64+2*u*v*w-4*(u*u+v*v+w*w);
                if(u!=0 && v!=0 && det>0) implications[x][y].set(r);
            }
        for(int x=0;x<n;++x) {
            ++singleton_count;
            if(implications[x][x].any()) return 3;
            for(int y=x+1;y<n;++y) {
                ++seed_count;
                Mask closure; closure.set(x); closure.set(y);
                std::vector<int> active{x,y}; size_t processed=0; int depth=0;
                while(closure!=full) {
                    Mask next=closure;
                    for(size_t v=processed;v<active.size();++v)
                        for(size_t u=0;u<v;++u) {
                            int a=active[u], b=active[v];
                            next|=a<b?implications[a][b]:implications[b][a];
                        }
                    ++depth;
                    if(next==closure) throw std::runtime_error("nontrivial stopping set");
                    processed=active.size();
                    for(int z=0;z<n;++z)if(next[z]&&!closure[z])active.push_back(z);
                    closure=next;
                }
                ++rounds[depth];
            }
        }
    }
    std::cout<<seed_count<<" "<<singleton_count<<"\n";
    for(auto entry:degrees)std::cout<<entry.first<<" "<<entry.second<<" "; std::cout<<"\n";
    for(auto entry:rounds)std::cout<<entry.first<<" "<<entry.second<<" "; std::cout<<"\n";
}
