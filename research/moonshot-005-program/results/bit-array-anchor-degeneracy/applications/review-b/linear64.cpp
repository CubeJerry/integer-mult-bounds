#include <algorithm>
#include <cstdint>
#include <cstring>
#include <vector>
static uint8_t table[64][64], inverse_table[64];
static bool initialized = false;
static void initialize() {
  if (initialized) return;
  for (int a=0;a<64;++a) for (int b=0;b<64;++b) {
    int x=a,y=b,product=0;
    while (y) {if(y&1)product^=x;y>>=1;x<<=1;if(x&64)x^=0x43;}
    table[a][b]=uint8_t(product);
    if(product==1)inverse_table[a]=uint8_t(b);
  }
  initialized=true;
}
extern "C" int gf_product_review(int a,int b) {initialize();return table[a][b];}

// Column basis with the last nonzero row as pivot; no author row reducer.
extern "C" int column_rank_review(const uint8_t *input,int rows,int cols) {
  initialize();std::vector<std::vector<uint8_t>> basis(rows);int rank=0;
  for(int c=0;c<cols;++c) {
    std::vector<uint8_t> v(rows);
    for(int r=0;r<rows;++r)v[r]=input[r*cols+c];
    for(int p=rows-1;p>=0;--p) {
      if(!v[p])continue;
      if(basis[p].empty()) {
        uint8_t scale=inverse_table[v[p]];
        for(int r=0;r<=p;++r)v[r]=table[scale][v[r]];
        basis[p]=std::move(v);++rank;break;
      }
      uint8_t scale=v[p];
      for(int r=0;r<=p;++r)v[r]^=table[scale][basis[p][r]];
    }
    if(rank==rows)break;
  }
  return rank;
}

// RREF visits variable columns in reverse order. Free coordinates, in
// increasing order, are the identity block of the returned null basis.
extern "C" int reverse_null_review(const uint8_t *input,int rows,int cols,
                                  uint8_t *output,int expected_nullity) {
  initialize();std::vector<uint8_t>a(input,input+rows*cols);
  std::vector<int>pivots;int rank=0;
  for(int c=cols-1;c>=0&&rank<rows;--c) {
    int pivot=-1;
    for(int r=rows-1;r>=rank;--r)if(a[r*cols+c]){pivot=r;break;}
    if(pivot<0)continue;
    for(int d=0;d<cols;++d)std::swap(a[rank*cols+d],a[pivot*cols+d]);
    uint8_t scale=inverse_table[a[rank*cols+c]];
    for(int d=0;d<cols;++d)a[rank*cols+d]=table[scale][a[rank*cols+d]];
    for(int r=0;r<rows;++r) {
      if(r==rank||!a[r*cols+c])continue;scale=a[r*cols+c];
      for(int d=0;d<cols;++d)a[r*cols+d]^=table[scale][a[rank*cols+d]];
    }
    pivots.push_back(c);++rank;
  }
  if(cols-rank!=expected_nullity)return -1000-rank;
  std::vector<int>free;
  for(int c=0;c<cols;++c)
    if(std::find(pivots.begin(),pivots.end(),c)==pivots.end())free.push_back(c);
  std::memset(output,0,cols*expected_nullity);
  for(int c=0;c<expected_nullity;++c) {
    output[free[c]*expected_nullity+c]=1;
    for(int r=0;r<rank;++r)output[pivots[r]*expected_nullity+c]=a[r*cols+free[c]];
  }
  return rank;
}

extern "C" void product_review(const uint8_t *a,const uint8_t *b,uint8_t *c,
                               int rows,int inner,int cols) {
  initialize();std::memset(c,0,rows*cols);
  for(int r=0;r<rows;++r)for(int k=0;k<inner;++k) {
    uint8_t scale=a[r*inner+k];if(!scale)continue;
    for(int s=0;s<cols;++s)c[r*cols+s]^=table[scale][b[k*cols+s]];
  }
}
