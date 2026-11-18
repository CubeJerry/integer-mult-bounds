/* Enumerate the rank <=5 flats of the 95 real-root roles by an outer bound
   over F_3. Every Q-dependent set is dependent mod 3. A spanning basis of
   size <=5 over F_3 can be extended to size five using these 95 roles. */
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
    const std::array<int,6> masks={7,19,42,129,410,466};
    std::array<Mask,6> words{};
    std::array<int,6> maximal{};
    for(int j=0;j<n;++j)for(int h=0;h<6;++h)if(std::popcount(unsigned(xi[j]&masks[h]))%2)words[h].set(j);
    std::array<std::array<long long,96>,6> histogram{};
    auto enumerate=[&](auto&& recurse,int k,int after,const std::vector<int>& space,Mask mask)->void{
        histogram[k][mask.size()]++;
        if(k==5)return;
        for(int i=after;i<n;++i){
            if(mask.has(i))continue;
            if(k<4){auto next=extend(space,i);Mask m=closure(next);if(gives_lex_basis(mask,m,i))recurse(recurse,k+1,i+1,next,m);}
            else{
                Mask m=mask;for(int v:space){int j=root_index[add[i][v]];if(j>=0)m.set(j);}
                if(!gives_lex_basis(mask,m,i))continue;
                histogram[5][m.size()]++;
                for(int h=0;h<6;++h)maximal[h]=std::max(maximal[h],std::popcount(m.lo&words[h].lo)+std::popcount(m.hi&words[h].hi));
            }
        }
    };
    enumerate(enumerate,0,0,std::vector<int>{0},{});
    for(int k=1;k<=5;++k){std::cout<<"F "<<k;for(int j=0;j<=n;++j)if(histogram[k][j])std::cout<<" "<<j<<":"<<histogram[k][j];std::cout<<"\n";}
    for(int h=0;h<6;++h)std::cout<<"W "<<masks[h]<<" "<<words[h].size()<<" "<<maximal[h]<<"\n";
}
