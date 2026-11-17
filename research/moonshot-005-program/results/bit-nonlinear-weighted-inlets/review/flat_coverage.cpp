/* Enumerate the rank <=4 flats of the 95 real-root roles by an outer bound
   over F_3. Every Q-dependent set is dependent mod 3. A spanning basis of
   size <=4 over F_3 can be extended to size four using these 95 roles. */
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using U = std::uint64_t;
struct Mask {
    U lo=0, hi=0;
    void set(int i) { if(i<64) lo |= U(1)<<i; else hi |= U(1)<<(i-64); }
    bool has(int i) const {return i<64 ? (lo>>i&1) : (hi>>(i-64)&1);}
    int size() const {return std::popcount(lo)+std::popcount(hi);}
    bool operator==(const Mask&)const=default;
};
constexpr int n=95, q8=6561;
int add[n][q8], code[n], root_index[q8];
std::array<int,8> digits(int a){std::array<int,8> d;for(auto &z:d){z=a%3;a/=3;}return d;}
int from_digits(const std::array<int,8>&d){int a=0;for(int j=7;j>=0;--j)a=3*a+(d[j]+3)%3;return a;}
Mask closure(const std::vector<int>& words) {
    Mask result; for(int z:words){int r=root_index[z]; if(r>=0)result.set(r);} return result;
}
std::vector<int> extend(const std::vector<int>& vs,int d){
    std::vector<int> more=vs; more.reserve(3*vs.size());
    for(int v:vs){int v1=add[d][v];more.push_back(v1);more.push_back(add[d][v1]);}
    return more;
}
bool gives_lex_basis(Mask prior,Mask after,int d){
    for(int j=0;j<d;++j)if(after.has(j)&&!prior.has(j))return false;
    return true;
}
int main(){
    std::fill(root_index,root_index+q8,-1);std::array<int,n> ids{},xi{};
    for(int i=0;i<n;++i){
        std::array<int,8> r; if(!(std::cin>>ids[i]>>xi[i]))throw std::runtime_error("missing role");
        for(auto &x:r) std::cin>>x;
        code[i]=from_digits(r);
        if(code[i]==0 || root_index[code[i]]>=0)throw std::runtime_error("duplicate mod-3 projective root");
        root_index[code[i]]=i;auto neg=r;for(int &x:neg)x=-x;root_index[from_digits(neg)]=i;
        for(int v=0;v<q8;++v){auto z=digits(v);for(int j=0;j<8;++j)z[j]+=r[j];add[i][v]=from_digits(z);}
    }
    std::array<std::array<uint64_t,14>,n> witness_membership{};
    std::array<int,840> weights{};
    for(int w=0;w<838;++w) {
        if(!(std::cin>>weights[w]) || weights[w]<0) throw std::runtime_error("invalid witness weight");
        for(int j=0;j<14;++j) {
            int role; if(!(std::cin>>role)|| role<0 || role>=n) throw std::runtime_error("bad witness role");
            witness_membership[role][w/64] |= U(1)<<(w%64);
        }
    }
    std::array<std::array<int,256>,105> table{};
    for(int p=0;p<105;++p) for(int m=1;m<256;++m)
        table[p][m]=table[p][m&(m-1)] + weights[8*p+std::countr_zero(unsigned(m))];
    std::array<int,6> max_mass{}, max_unweighted{};
    auto score=[&](int rank,Mask roots){
        std::array<U,14> covered{};
        for(int part=0;part<2;++part) {
            U z=part ? roots.hi:roots.lo;
            while(z) {
                int j=64*part+std::countr_zero(z); z&=z-1;
                for(int k=0;k<14;++k)covered[k]|=witness_membership[j][k];
            }
        }
        int mass=0;
        for(int p=0;p<105;++p)mass+=table[p][(covered[p/8]>>(8*(p%8)))&255];
        max_mass[rank]=std::max(max_mass[rank],mass);
        int nc=0;for(U v:covered)nc+=std::popcount(v);max_unweighted[rank]=std::max(max_unweighted[rank],nc);
    };
    std::array<std::array<long long,96>,6> histogram{};
    auto enumerate=[&](auto&& recurse,int k,int after,const std::vector<int>& space,Mask mask)->void{
        histogram[k][mask.size()]++;score(k,mask);
        if(k==5)return;
        for(int i=after;i<n;++i){
            if(mask.has(i))continue;
            if(k<4){auto next=extend(space,i);Mask m=closure(next);if(gives_lex_basis(mask,m,i))recurse(recurse,k+1,i+1,next,m);}
            else{
                Mask m=mask;for(int v:space){int j=root_index[add[i][v]];if(j>=0)m.set(j);}
                if(!gives_lex_basis(mask,m,i))continue;
                histogram[5][m.size()]++;score(5,m);
            }
        }
    };
    enumerate(enumerate,0,0,std::vector<int>{0},{});
    for(int k=1;k<=5;++k) {
        long long total=0;for(auto count:histogram[k])total+=count;
        std::cout<<k<<" "<<total<<" "<<max_mass[k]<<" "<<max_unweighted[k]<<"\n";
    }
}
