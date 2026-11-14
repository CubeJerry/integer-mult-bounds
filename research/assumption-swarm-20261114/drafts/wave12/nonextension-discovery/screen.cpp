#include <algorithm>
#include <array>
#include <iostream>
#include <vector>
using I=long long;
constexpr I P=1000003;
I power(I a,I n){I r=1;for(;n;n>>=1,a=a*a%P)if(n&1)r=r*a%P;return r;}
int rank8(std::array<std::array<I,8>,8> a){
  int r=0;for(int c=0;c<8&&r<8;c++){
    int k=r;while(k<8&&!a[k][c])k++;if(k==8)continue;
    std::swap(a[k],a[r]);I z=power(a[r][c],P-2);
    for(int j=c;j<8;j++)a[r][j]=a[r][j]*z%P;
    for(int i=r+1;i<8;i++){I f=a[i][c];for(int j=c;j<8;j++)a[i][j]=(a[i][j]-f*a[r][j]%P+P)%P;}
    r++;
  }return r;
}
int main(){
  std::cout<<"{\"scope\":\"g3, all40320 orders, C=[[1,1],[w,1]] tensor cubed; finite-field evidence only\",\"prime\":"<<P<<",\"runs\":[";
  bool first=true;
  for(I w:{I(2),I(3),power(4096,P-2)}){
    std::array<std::array<I,8>,8> h;for(int i=0;i<8;i++)for(int j=0;j<8;j++)h[i][j]=power(w,__builtin_popcount(unsigned(i&(~j)&7)));
    std::array<int,8> order{0,1,2,3,4,5,6,7};std::array<int,9> hist{};std::vector<std::array<int,8>> bad;
    do{
      std::array<std::array<I,8>,8> e;
      for(int i=0;i<8;i++)for(int j=0;j<8;j++)e[i][j]=(h[order[i]][order[j]]-(i&&j?h[order[i-1]][order[j-1]]:0)+P)%P;
      int r=rank8(e);hist[r]++;if(r<8&&bad.size()<8)bad.push_back(order);
    }while(std::next_permutation(order.begin(),order.end()));
    if(!first)std::cout<<",";first=false;std::cout<<"{\"w_mod_p\":"<<w<<",\"rank_histogram\":[";
    for(int i=0;i<9;i++){if(i)std::cout<<",";std::cout<<hist[i];}std::cout<<"],\"first_failures\":[";
    for(size_t k=0;k<bad.size();k++){if(k)std::cout<<",";std::cout<<"[";for(int j=0;j<8;j++){if(j)std::cout<<",";std::cout<<bad[k][j];}std::cout<<"]";}std::cout<<"]}";
  }
  std::cout<<"]}\n";
}
