#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <utility>
#include <vector>
using namespace std;
struct Spec {int rank=0; uint32_t offset=0,count=0; vector<int> piv; vector<pair<int,int>> cells;};
struct Layer {int cut,rank; uint64_t lo,hi;};
struct Best {uint64_t value=0; uint32_t low=0,high=0;};
static uint32_t packer[512][9][512];
void need(bool b,const char* m){if(!b)throw runtime_error(m);}
int main(int argc,char**argv){
 need(argc==3,"usage: check INPUT.txt RESULT.json");ifstream in(argv[1]);need(bool(in),"input open");int nc,nb;uint64_t objective;in>>nc>>nb>>objective;need(nb>0&&nb<=16&&nc<=64*nb,"mask dimensions");vector<uint64_t> coeff(nc);for(auto&v:coeff)in>>v;
 array<Spec,512> sp;uint32_t total=0;vector<int> order;
 for(int d=0;d<=9;d++)for(int pm=0;pm<512;pm++)if(popcount((unsigned)pm)==d){auto&s=sp[pm];s.rank=d;s.offset=total;for(int p=0;p<9;p++)if(pm>>p&1){s.piv.push_back(p);for(int q=p+1;q<9;q++)if(!(pm>>q&1))s.cells.emplace_back(p,q);}s.count=1u<<s.cells.size();total+=s.count;order.push_back(pm);for(int p:s.piv)for(int v=0;v<512;v++){uint32_t z=0;for(size_t k=0;k<s.cells.size();k++)if(s.cells[k].first==p&&(v>>s.cells[k].second&1))z|=1u<<k;packer[pm][p][v]=z;}}
 need(total==8283458,"all binary subspaces counted");vector<uint64_t> masks((size_t)total*nb,0),phi(total,0);array<vector<Layer>,10> layers;int nlayer;in>>nlayer;for(int i=0;i<nlayer;i++){Layer l;in>>l.cut>>l.rank>>l.lo>>l.hi;need(l.rank>=1&&l.rank<=9&&l.cut<nc,"layer spec");layers[l.rank].push_back(l);}
 int ngen;in>>ngen;for(int i=0;i<ngen;i++){uint32_t id;int cut;in>>id>>cut;need(id<total&&cut<nc,"generator index");masks[(size_t)id*nb+cut/64]|=1ull<<(cut%64);}
 int nex;in>>nex;vector<uint32_t> expected_id(nex);vector<uint64_t> expected((size_t)nex*nb);for(int i=0;i<nex;i++){in>>expected_id[i];for(int b=0;b<nb;b++)in>>expected[(size_t)i*nb+b];}
 int nports;in>>nports;vector<int> ports(nports);for(auto&v:ports)in>>v;need(bool(in)&&nports<=128,"complete input");array<array<uint64_t,2>,512> ortho{};for(int v=0;v<512;v++)for(int j=0;j<nports;j++)if(!(popcount((unsigned)(v&ports[j]))&1))ortho[v][j/64]|=1ull<<(j%64);
 array<Best,10> best{};uint64_t total_edges=0;auto start=chrono::steady_clock::now();int prior_rank=0;
 for(int pm:order){const auto&s=sp[pm];int d=s.rank;if(d!=prior_rank){cerr<<"finished dimension "<<prior_rank<<" best "<<best[prior_rank].value<<" elapsed "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";prior_rank=d;}
  for(uint32_t ix=0;ix<s.count;ix++){uint32_t id=s.offset+ix;array<int,9> row{};for(int p:s.piv)row[p]=1<<p;for(size_t k=0;k<s.cells.size();k++)if(ix>>k&1)row[s.cells[k].first]|=1<<s.cells[k].second;array<uint64_t,16> accum{};for(int b=0;b<nb;b++)accum[b]=masks[(size_t)id*nb+b];
   if(!layers[d].empty()){uint64_t lo=~0ull,hi=~0ull;for(int p:s.piv){lo&=ortho[row[p]][0];hi&=ortho[row[p]][1];}for(const auto&l:layers[d])if(!(lo&l.lo)&&!(hi&l.hi))accum[l.cut/64]|=1ull<<(l.cut%64);}
   uint64_t least=numeric_limits<uint64_t>::max();uint32_t least_id=0;
   for(int j=0;j<d;j++){int drop=s.piv[j],qm=pm^(1<<drop);const auto&t=sp[qm];uint32_t base=0;array<uint32_t,9> delta{};for(int i=0;i<d;i++)if(i!=j)base|=packer[qm][s.piv[i]][row[s.piv[i]]];for(int i=0;i<j;i++)delta[i]=packer[qm][s.piv[i]][row[drop]];uint32_t z=base;
    for(uint32_t a=0;a<(1u<<j);a++){if(a)z^=delta[countr_zero(a)];uint32_t hid=t.offset+z;need(hid<id,"hyperplane precedes parent");for(int b=0;b<nb;b++)accum[b]|=masks[(size_t)hid*nb+b];if(phi[hid]<least){least=phi[hid];least_id=hid;}total_edges++;}}
   uint64_t val=0;for(int b=0;b<nb;b++){masks[(size_t)id*nb+b]=accum[b];uint64_t z=accum[b];while(z){int k=countr_zero(z);need(64*b+k<nc,"mask tail");val+=coeff[64*b+k];z&=z-1;}}phi[id]=val;if(d){need(val>=least,"monotone potential");if(val-least>best[d].value)best[d]={val-least,least_id,id};}
  }
 }
 for(int i=0;i<nex;i++)for(int b=0;b<nb;b++)need(masks[(size_t)expected_id[i]*nb+b]==expected[(size_t)i*nb+b],"source-chart membership mismatch");
 auto decode=[&](uint32_t id){vector<int> ans;for(int pm:order){const auto&s=sp[pm];if(id<s.offset||id>=s.offset+s.count)continue;uint32_t ix=id-s.offset;array<int,9> row{};for(int p:s.piv)row[p]=1<<p;for(size_t k=0;k<s.cells.size();k++)if(ix>>k&1)row[s.cells[k].first]|=1<<s.cells[k].second;for(int p:s.piv)ans.push_back(row[p]);return ans;}throw runtime_error("decode ID");};
 uint64_t maximum=0;for(int d=1;d<=9;d++)maximum=max(maximum,best[d].value);ofstream out(argv[2]);out<<"{\n\"status\":\"EXACT_ALL_SUBSPACE_UNIT_EDGE_SCREEN\",\n\"subspaces\":"<<total<<",\n\"unit_edges\":"<<total_edges<<",\n\"cuts\":"<<nc<<",\n\"objective_numerator\":"<<objective<<",\n\"maximum_unit_increment_numerator\":"<<maximum<<",\n\"source_chart_memberships_match\":true,\n\"by_upper_dimension\":[\n";
 for(int d=1;d<=9;d++){out<<(d>1?",\n":"")<<"{\"dimension\":"<<d<<",\"increment_numerator\":"<<best[d].value<<",\"from_frame\":[";auto a=decode(best[d].low);for(size_t i=0;i<a.size();i++)out<<(i?",":"")<<a[i];out<<"],\"to_frame\":[";a=decode(best[d].high);for(size_t i=0;i<a.size();i++)out<<(i?",":"")<<a[i];out<<"]}";}out<<"\n]}\n";cerr<<"DONE unit edges "<<total_edges<<" max "<<maximum<<" elapsed "<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"\n";
}
