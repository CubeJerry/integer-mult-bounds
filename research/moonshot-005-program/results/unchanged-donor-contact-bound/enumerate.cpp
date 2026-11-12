// Exact RREF enumeration of every binary subspace of F_2^9.
// Source populations are discovery data; the analytic contact bound does not
// depend on this enumeration. @CubeJerry, OpenAI assistance, Apache-2.0.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <utility>
#include <vector>
using namespace std;
array<int,512> active{};
array<uint64_t,10> counts{};
array<map<pair<int,int>,uint64_t>,10> profiles;
array<map<pair<int,int>,vector<int>>,10> witnesses;
int population(const vector<int>& basis) {
    array<int,512> a{}; int n=1, total=0;
    for(int b:basis) { for(int i=0;i<n;i++) a[n+i]=a[i]^b; n*=2; }
    for(int i=0;i<n;i++) total+=active[a[i]];
    return total;
}
void evaluate(const vector<int>& piv, const vector<int>& basis) {
    int d=piv.size(); vector<int> other;
    int mask=0;for(int p:piv)mask|=1<<p;
    for(int col=0;col<9;col++)if(!(mask&(1<<col))) {
        int v=1<<col;
        for(int i=0;i<d;i++)if(basis[i]&(1<<col))v|=1<<piv[i];
        other.push_back(v);
    }
    int a=population(basis),b=population(other);
    auto key=make_pair(a,b); profiles[d][key]++; counts[d]++;
    if(!witnesses[d].count(key))witnesses[d][key]=basis;
}
void enumerate_pivots(const vector<int>& piv) {
    int d=piv.size(),mask=0;vector<int> basis;vector<pair<int,int>> free;
    for(int p:piv) {mask|=1<<p;basis.push_back(1<<p);}
    for(int i=0;i<d;i++)for(int col=piv[i]+1;col<9;col++)if(!(mask&(1<<col)))free.emplace_back(i,col);
    uint64_t total=uint64_t(1)<<free.size(),previous=0;
    for(uint64_t index=0;index<total;index++) {
        uint64_t gray=index^(index>>1);
        if(index) {
            int change=__builtin_ctzll(gray^previous);
            basis[free[change].first]^=1<<free[change].second;
        }
        evaluate(piv,basis);previous=gray;
    }
}
void select(int d,int next,vector<int>& piv) {
    if(int(piv.size())==d) {enumerate_pivots(piv);return;}
    for(int p=next;p<=9-(d-int(piv.size()));p++) {
        piv.push_back(p);select(d,p+1,piv);piv.pop_back();
    }
}
int main(int argc,char**argv) {
    if(argc!=2)return 2;
    ifstream input(argv[1]);int v,n=0;
    while(input>>v) {if(v<=0||v>=512||active[v]||!(__builtin_popcount(unsigned(v))&1))return 3;active[v]=1;n++;}
    if(n!=104)return 4;
    vector<int> piv;
    for(int d=0;d<=9;d++) {select(d,0,piv);cerr<<"dimension "<<d<<" subspaces "<<counts[d]<<"\n";}
    cout<<"{\"ambient\":9,\"source_ports\":104,\"dimensions\":[";
    for(int d=0;d<=9;d++) {
        if(d)cout<<',';
        cout<<"{\"dimension\":"<<d<<",\"subspaces\":"<<counts[d]<<",\"profiles\":[";
        bool first=true;
        for(auto [key,count]:profiles[d]) {
            if(!first)cout<<',';
            first=false;
            cout<<"{\"donors\":"<<key.first<<",\"receivers\":"<<key.second<<",\"count\":"<<count<<",\"witness\":[";
            auto row=witnesses[d][key];for(size_t j=0;j<row.size();j++){if(j)cout<<',';cout<<row[j];}cout<<"]}";
        }
        cout<<"]}";
    }
    cout<<"]}\n";
}
