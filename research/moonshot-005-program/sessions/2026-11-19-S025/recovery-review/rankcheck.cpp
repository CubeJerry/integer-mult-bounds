#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

// Fresh reviewer implementation. Input is a sequence of full matrices,
// not author kernel reductions or determinant claims.
using Matrix=std::vector<std::vector<unsigned>>;
std::array<std::array<unsigned,128>,128> times;
std::array<unsigned,128> inverse;
unsigned read32(std::ifstream& in){
  unsigned char q[4]; in.read(reinterpret_cast<char*>(q),4);
  if(!in) throw std::runtime_error("truncated input");
  return q[0]|unsigned(q[1])<<8|unsigned(q[2])<<16|unsigned(q[3])<<24;
}
unsigned field_product(unsigned x,unsigned y){
  unsigned p=0;
  for(unsigned i=0;i<7;++i) if(y&(1u<<i)) p^=x<<i;
  for(int i=12;i>=7;--i) if(p&(1u<<i)) p^=131u<<(i-7);
  return p;
}
unsigned rank(Matrix a){
  unsigned r=0,n=a.size(),m=a[0].size();
  for(unsigned c=0;c<m && r<n;++c){
    unsigned pivot=r; while(pivot<n && !a[pivot][c]) ++pivot;
    if(pivot==n) continue;
    std::swap(a[pivot],a[r]); unsigned scale=inverse[a[r][c]];
    for(unsigned k=c;k<m;++k) a[r][k]=times[scale][a[r][k]];
    for(unsigned j=r+1;j<n;++j) if(a[j][c]){
      unsigned z=a[j][c]; for(unsigned k=c;k<m;++k) a[j][k]^=times[z][a[r][k]];
    }
    ++r;
  }
  return r;
}
int main(int argc,char**argv){
  if(argc!=3) throw std::runtime_error("rankcheck INPUT OUTPUT");
  for(unsigned x=0;x<128;++x) for(unsigned y=0;y<128;++y) times[x][y]=field_product(x,y);
  for(unsigned x=1;x<128;++x){
    for(unsigned y=1;y<128;++y) if(times[x][y]==1) inverse[x]=y;
    if(!inverse[x]) throw std::runtime_error("not a field");
  }
  std::ifstream in(argv[1],std::ios::binary);
  unsigned count=read32(in),passed=0,negative=0;
  std::array<unsigned,4> families{};
  for(unsigned z=0;z<count;++z){
    unsigned family=read32(in),n=read32(in),m=read32(in),expected=read32(in);
    if(family>3 || !n || !m || n>90 || m>90) throw std::runtime_error("matrix metadata");
    Matrix a(n,std::vector<unsigned>(m));
    for(auto&row:a) for(auto&x:row){int value=in.get();if(value<0||value>=128) throw std::runtime_error("matrix byte"); x=value;}
    if(rank(a)!=expected) throw std::runtime_error("independent original-matrix rank mismatch at "+std::to_string(z));
    ++families[family]; ++passed; if(expected<n) ++negative;
  }
  if(in.peek()!=EOF) throw std::runtime_error("trailing data");
  std::ofstream out(argv[2]);
  out<<"{\"status\":\"PASS_FRESH_FULL_MATRIX_RANK_REVIEW\",\"cases\":"<<passed<<",\"families\":[";
  for(unsigned i=0;i<4;++i) out<<(i?",":"")<<families[i];
  out<<"],\"rank_deficient_controls\":"<<negative<<"}\n";
  std::cout<<"PASS_FRESH_FULL_MATRIX_RANK_REVIEW "<<passed<<" cases\n";
}
