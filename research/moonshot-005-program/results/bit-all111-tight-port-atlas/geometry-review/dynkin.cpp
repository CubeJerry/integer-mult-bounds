// Enumerate parent D4 root sets from all simply-laced Dynkin stars.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
using Root=std::array<int,8>;
using Chart=std::array<int,12>;
Root positive(Root x) {
    auto p=std::find_if(x.begin(),x.end(),[](int y){return y!=0;});
    if(p==x.end()) throw std::logic_error("zero root");
    if(*p<0) for(int& a:x) a=-a;
    return x;
}
int main() {
    std::array<Root,120> roots;
    std::map<Root,int> ids;
    for(int i=0;i<120;i++) {
        for(int& x:roots[i]) if(!(std::cin>>x)) throw std::runtime_error("invalid root file");
        ids.emplace(positive(roots[i]),i);
    }
    int dot[120][120]{};
    for(int i=0;i<120;i++) for(int j=0;j<120;j++)
        for(int k=0;k<8;k++) dot[i][j]+=roots[i][k]*roots[j][k];
    std::set<Chart> flats;
    int total=0;
    for(int c=0;c<120;c++) for(int a=0;a<120;a++) if(std::abs(dot[c][a])==2)
        for(int b=a+1;b<120;b++) if(std::abs(dot[c][b])==2 && dot[a][b]==0)
            for(int d=b+1;d<120;d++) if(std::abs(dot[c][d])==2 && dot[a][d]==0 && dot[b][d]==0) {
                Chart list{c,a,b,d};
                std::array<int,3> outer{a,b,d};
                int n=4;
                for(int mask=1;mask<=7;mask++) {
                    Root x=roots[c];
                    for(int z=0;z<3;z++) if((mask>>z)&1)
                        for(int k=0;k<8;k++) x[k]-=dot[c][outer[z]]/2*roots[outer[z]][k];
                    list[n++]=ids.at(positive(x));
                    if(mask==7) {
                        for(int k=0;k<8;k++) x[k]+=roots[c][k];
                        list[n++]=ids.at(positive(x));
                    }
                }
                std::sort(list.begin(),list.end());
                if(std::adjacent_find(list.begin(),list.end())!=list.end()) throw std::logic_error("non-D4");
                ++total;flats.insert(list);
            }
    std::cout<<total<<" "<<flats.size()<<"\n";
    for(const auto& chart:flats) {
        for(int x:chart) std::cout<<x<<" ";
        std::cout<<"\n";
    }
}
