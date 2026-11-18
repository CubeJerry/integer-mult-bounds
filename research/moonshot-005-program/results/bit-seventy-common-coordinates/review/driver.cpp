// The max-flow engine is copied byte-for-byte from the pinned prior review.
#define main historical_review_main
#include "dinic_engine.cpp"
#undef main
#include <array>
#include <cstdint>
#include <fstream>
#include <string>

uint32_t read32(std::ifstream& in){
 unsigned char b[4];in.read((char*)b,4);if(!in)throw std::runtime_error("truncated graph certificate");
 return uint32_t(b[0])|(uint32_t(b[1])<<8)|(uint32_t(b[2])<<16)|(uint32_t(b[3])<<24);
}
struct Arc{int u,v,c,tag;}; // tag1=early source inlet;tag2=terminal arc.
struct Test{int donor,receiver,k,late,value,target,cut;};

Test run(int donor,int n,const std::vector<Arc>& arcs,int distinguished,int k,bool late,int degree){
 Net net(n);std::vector<std::array<int,4>> originals;originals.reserve(arcs.size());
 for(const Arc&e:arcs){
  int capacity=e.c;
  if(e.tag==1&&late)capacity=0;
  if(e.tag==2)capacity=(e.c==distinguished?(late?0:5760):k);
  int slot=net.g[e.u].size();originals.push_back({e.u,e.v,capacity,slot});net.add(e.u,e.v,capacity);
 }
 int value=net.solve();std::vector<int> balance(n);
 for(const auto&e:originals){
  int used=e[2]-net.g[e[0]][e[3]].cap;
  if(used<0||used>e[2])throw std::runtime_error("directed physical capacity violation");
  balance[e[0]]+=used;balance[e[1]]-=used;
 }
 if(balance[0]!=value||balance[1]!=-value)throw std::runtime_error("source/sink divergence");
 for(int v=2;v<n;v++)if(balance[v])throw std::runtime_error("internal chart conservation");
 std::vector<bool> reachable(n,false);std::queue<int> q;reachable[0]=true;q.push(0);
 while(!q.empty()){
  int u=q.front();q.pop();for(const auto&e:net.g[u])if(e.cap>0&&!reachable[e.to]){reachable[e.to]=true;q.push(e.to);}
 }
 int cut=0;for(const auto&e:originals)if(reachable[e[0]]&&!reachable[e[1]])cut+=e[2];
 if(cut!=value||reachable[1])throw std::runtime_error("exact residual minimum cut mismatch");
 int target=(late?0:5760)+(degree-1)*k;
 return {donor,distinguished,k,int(late),value,target,cut};
}

int main(int argc,char**argv){
 if(argc!=3)throw std::runtime_error("usage driver INPUT OUTPUT");
 std::ifstream in(argv[1],std::ios::binary);std::ofstream out(argv[2]);if(!in||!out)throw std::runtime_error("review IO");
 int graphs=read32(in),mixed=0,latecases=0;bool comma=false;
 out<<"{\"schema\":\"independent-seventy-flow-primal-dual-v1\",\"cases\":[";
 auto write=[&](Test t){if(comma)out<<",";comma=true;out<<"["<<t.donor<<","<<t.receiver<<","<<t.k<<","<<t.late<<","<<t.value<<","<<t.target<<","<<t.cut<<"]";};
 for(int count=0;count<graphs;count++){
  int donor=read32(in),n=read32(in),m=read32(in),degree=read32(in),omitted=read32(in);
  std::vector<int>neighbors(degree);for(int&i:neighbors)i=read32(in);
  std::vector<Arc>arcs(m);for(Arc&e:arcs){e.u=read32(in);e.v=read32(in);e.c=read32(in);e.tag=read32(in);}
  for(int receiver:neighbors){auto t=run(donor,n,arcs,receiver,70,false,degree);if(t.value!=t.target)throw std::runtime_error("mixed70 target missed");write(t);mixed++;}
  auto t=run(donor,n,arcs,omitted,70,true,degree);if(t.value!=t.target)throw std::runtime_error("all-but-one late70 target missed");write(t);latecases++;
  if(donor==80){
   auto bad=run(donor,n,arcs,neighbors.front(),71,false,degree);
   if(bad.value!=10080||bad.target!=10091)throw std::runtime_error("k71 mixed source-cut control");write(bad);
   bad=run(donor,n,arcs,omitted,71,true,degree);
   if(bad.value!=4320||bad.target!=4331)throw std::runtime_error("k71 late source-cut control");write(bad);
  }
  if(count%20==0)std::cerr<<"reviewed donor "<<donor<<", mixed cases "<<mixed<<"\n";
 }
 if(in.peek()!=EOF)throw std::runtime_error("trailing graph data");
 if(mixed!=6470||latecases!=111)throw std::runtime_error("case census");
 out<<"],\"mixed_cases\":"<<mixed<<",\"late_cases\":"<<latecases<<",\"negative_cases\":2,\"every_capacity_conservation_and_residual_cut_checked\":true}\n";
 std::cout<<"PASS_INDEPENDENT_6470_MIXED_AND_111_LATE_FLOWS\n";
}
