#include <array>
#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;
const array<int,25> proper={31,59,87,91,122,199,206,217,220,234,241,244,248,265,268,274,289,292,319,367,386,400,431,443,508};
array<bool,512> good{};
array<int,9> chosen{},bestBasis{},bestDual{};
array<uint64_t,10> histogram{};
uint64_t combinations=0,bases=0;int best=10;
void leaf(){
 ++combinations;array<int,9> a{};
 for(int i=0;i<9;i++){
  for(int j=0;j<9;j++)a[i]|=((chosen[j]>>i)&1)<<j;
  a[i]|=1<<(9+i);
 }
 for(int j=0;j<9;j++){
  int p=j;while(p<9&&!((a[p]>>j)&1))p++;
  if(p==9)return;swap(a[p],a[j]);
  for(int i=0;i<9;i++)if(i!=j&&((a[i]>>j)&1))a[i]^=a[j];
 }
 ++bases;int score=0;array<int,9> dual{};
 for(int i=0;i<9;i++){dual[i]=a[i]>>9;score+=!good[dual[i]];}
 histogram[score]++;
 if(score<best){best=score;bestBasis=chosen;bestDual=dual;}
}
void rec(int start,int depth){
 if(depth==9){leaf();return;}
 for(int i=start;i<=25-(9-depth);i++){chosen[depth]=proper[i];rec(i+1,depth+1);}
}
int main(){
 for(int v:proper)good[v]=true;rec(0,0);
 cout<<"{\"all_nine_subsets\":"<<combinations<<",\"invertible_bases\":"<<bases<<",\"minimum_full_span_payloads\":"<<best<<",\"histogram\":[";
 for(int i=0;i<10;i++)cout<<(i?",":"")<<histogram[i];
 cout<<"],\"decoder_basis\":[";for(int i=0;i<9;i++)cout<<(i?",":"")<<bestBasis[i];
 cout<<"],\"payload_basis\":[";for(int i=0;i<9;i++)cout<<(i?",":"")<<bestDual[i];cout<<"]}\n";
}
