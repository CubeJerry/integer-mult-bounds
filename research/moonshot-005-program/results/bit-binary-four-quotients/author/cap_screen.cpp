#ifdef NDEBUG
#error Assertions must remain enabled
#endif
#include <algorithm>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using U=__uint128_t;
struct Hash { size_t operator()(const U& a) const { uint64_t x=(uint64_t)a, y=(uint64_t)(a>>64); x^=y+0x9e3779b97f4a7c15ULL+(x<<6)+(x>>2); x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;return x^(x>>31); }};
struct Row {U v,one,two;int gain;};
int pc(U x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
int main(int argc,char**argv){assert(argc==2);std::ifstream f(argv[1]);int n;f>>n;assert(n==18034);std::vector<Row> r(n);std::vector<int> top;
 for(int i=0;i<n;++i){uint64_t h,l,oh,ol,th,tl;int g;f>>h>>l>>oh>>ol>>th>>tl>>g;assert(f.good());r[i]={((U)h<<64)|l,((U)oh<<64)|ol,((U)th<<64)|tl,g};assert(g>=14&&g<=17);assert(pc(r[i].one)+2*pc(r[i].two)==g);if(g>=16)top.push_back(i);}
 assert(top.size()==1134);using Pair=std::pair<uint16_t,uint16_t>;std::unordered_map<U,std::vector<Pair>,Hash> map;map.reserve(700000);
 for(size_t a=0;a<top.size();++a)for(size_t b=a+1;b<top.size();++b){int i=top[a],j=top[b];map[r[i].v^r[j].v].push_back({i,j});}
 std::cerr<<"top pair keys "<<map.size()<<"\n";std::unordered_set<uint64_t> seen;uint64_t raw=0;int best=-1;std::vector<int> bestids;std::unordered_map<int,uint64_t> hist;
 for(int i=0;i<n;++i)for(int j=i+1;j<n;++j){if(r[i].gain+r[j].gain<30)continue;auto it=map.find(r[i].v^r[j].v);if(it==map.end())continue;
  for(auto p:it->second){if(p.first==i||p.first==j||p.second==i||p.second==j)continue;int potential=r[i].gain+r[j].gain+r[p.first].gain+r[p.second].gain;if(potential<64)continue;++raw;
   std::vector<int> ids={i,j,p.first,p.second};std::sort(ids.begin(),ids.end());uint64_t key=0;for(int x:ids)key=(key<<16)|x;if(!seen.insert(key).second)continue;
   U one=0,two=0,check=0;for(int x:ids){one|=r[x].one;two|=r[x].two;check^=r[x].v;}assert(check==0);int gain=2*pc(two)+pc(one&~two);++hist[gain];if(gain>best){best=gain;bestids=ids;}
  }
 }
 std::cout<<"{\"status\":\"PASS_EXACT_DANGEROUS_BINARY_CAP_SCREEN\",\"high_catalog_size\":"<<n<<",\"top_catalog_size\":"<<top.size()<<",\"top_pair_keys\":"<<map.size()<<",\"candidate_cap_occurrences\":"<<raw<<",\"unique_caps_potential_ge64\":"<<seen.size()<<",\"max_disjoint_row_saving_for_four_high\":"<<best<<",\"example_indices\":[";
 for(size_t i=0;i<bestids.size();++i){if(i)std::cout<<",";std::cout<<bestids[i];}std::cout<<"],\"gain_histogram\":{";bool first=true;std::vector<std::pair<int,uint64_t>> hh(hist.begin(),hist.end());std::sort(hh.begin(),hh.end());for(auto p:hh){if(!first)std::cout<<",";first=false;std::cout<<"\""<<p.first<<"\":"<<p.second;}std::cout<<"}}\n";
}
