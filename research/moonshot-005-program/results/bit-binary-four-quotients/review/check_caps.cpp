#ifdef NDEBUG
#error Exact assertions must remain enabled
#endif
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using B=__uint128_t;
struct H {size_t operator()(B v)const{uint64_t a=(uint64_t)v,b=(uint64_t)(v>>64);a^=(b<<23)|(b>>41);a*=0x9e3779b185ebca87ULL;a^=a>>29;return a;}};
struct Row {B v,one,two;int gain;};
int pc(B x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
int main(int argc,char**argv){
 assert(argc==2);std::ifstream f(argv[1]);size_t n;f>>n;assert(n==38324);std::vector<Row> r(n);std::unordered_map<B,int,H> index;index.reserve(131072);std::vector<int> high,top,seventeen,fifteen;
 for(size_t i=0;i<n;i++){uint64_t h,l,a,b,c,d;int g;f>>h>>l>>a>>b>>c>>d>>g;assert(f.good());r[i]={((B)h<<64)|l,((B)a<<64)|b,((B)c<<64)|d,g};assert(pc(r[i].v)>=4&&pc(r[i].v)<=8);assert(!(r[i].one&r[i].two));assert(pc(r[i].one)+2*pc(r[i].two)==g);assert(g>=13&&g<=17);assert(index.emplace(r[i].v,(int)i).second);if(g>=14)high.push_back(i);if(g>=16)top.push_back(i);if(g==17)seventeen.push_back(i);if(g==15)fifteen.push_back(i);}
 assert(high.size()==18034&&top.size()==1134&&seventeen.size()==12&&fifteen.size()==6912);
 uint64_t pairtests=0;
 for(size_t a=0;a<high.size();a++)for(size_t b=a+1;b<high.size();b++){++pairtests;assert(index.find(r[high[a]].v^r[high[b]].v)==index.end());}
 int overlap=111;for(size_t a=0;a<seventeen.size();a++)for(size_t b=a+1;b<seventeen.size();b++)overlap=std::min(overlap,pc(r[seventeen[a]].one&r[seventeen[b]].one));assert(overlap==5);
 std::unordered_set<uint64_t> caps;std::map<int,int> histogram;int best=0;uint64_t triples=0,rare=0;std::vector<int> example;
 auto accept=[&](int a,int b,int c,int d){
  std::vector<int> v={a,b,c,d};std::sort(v.begin(),v.end());if(std::adjacent_find(v.begin(),v.end())!=v.end())return;int potential=0;B sum=0,one=0,two=0;uint64_t key=0;
  for(int i:v){assert(r[i].gain>=14);potential+=r[i].gain;sum^=r[i].v;one|=r[i].one;two|=r[i].two;key=(key<<16)|(uint16_t)i;}
  if(potential<64)return;assert(sum==0);if(!caps.insert(key).second)return;int saved=pc(one|two)+pc(two);++histogram[saved];if(saved>best){best=saved;example=v;}
 };
 // DIFFERENT cap coverage: either >=3 top-gain classes, or exactly2 top,
 // which must BOTH have gain17 and leave two gain15 classes.
 for(size_t a=0;a<top.size();a++)for(size_t b=a+1;b<top.size();b++)for(size_t c=b+1;c<top.size();c++){
  ++triples;int i=top[a],j=top[b],k=top[c];auto p=index.find(r[i].v^r[j].v^r[k].v);if(p!=index.end()&&r[p->second].gain>=14)accept(i,j,k,p->second);
 }
 for(size_t a=0;a<seventeen.size();a++)for(size_t b=a+1;b<seventeen.size();b++)for(int c:fifteen){
  ++rare;int i=seventeen[a],j=seventeen[b];auto p=index.find(r[i].v^r[j].v^r[c].v);if(p!=index.end()&&r[p->second].gain==15&&c<p->second)accept(i,j,c,p->second);
 }
 assert(caps.size()==3989&&best==46);assert((histogram==std::map<int,int>({{32,3935},{41,12},{42,14},{43,4},{44,3},{45,18},{46,3}})));
 std::cout<<"{\"status\":\"PASS_DISTINCT_TOP_TRIPLE_AND_TWO17_CAP_AUDIT\",\"all_catalog\":"<<n<<",\"high_pair_tests\":"<<pairtests<<",\"top_triples_tested\":"<<triples<<",\"two17_plus15_tests\":"<<rare<<",\"no_high_pair_sum_in_catalog\":true,\"minimum17_overlap\":"<<overlap<<",\"dangerous_caps\":"<<caps.size()<<",\"maximum_disjoint_row_saving\":"<<best<<",\"histogram\":{";
 bool first=true;for(auto x:histogram){if(!first)std::cout<<",";first=false;std::cout<<"\""<<x.first<<"\":"<<x.second;}std::cout<<"},\"example_all_catalog_indices\":[";for(size_t i=0;i<example.size();i++){if(i)std::cout<<",";std::cout<<example[i];}std::cout<<"]}\n";
}
