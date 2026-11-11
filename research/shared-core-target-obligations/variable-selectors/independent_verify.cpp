#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using U=std::uint64_t;
constexpr U p=1000000007,half=(p+1)/2;
struct Op{int type,d0,d1,s0,s1;U q,mask;};
std::array<U,2> weight(int style,int bit){
 const U sign=bit?p-1:1,sgnhalf=bit?p-half:half;
 if(style==0)return {U(1-bit),U(bit)};
 if(style==1)return {1,sign};
 if(style==2)return {half,sgnhalf};
 if(style==3)return {sign,1};
 if(style==4)return {sgnhalf,half};
 throw std::runtime_error("style");
}
int main(int argc,char**argv){
 if(argc<2)return 2;
 std::ifstream in(argv[1]);int fields,outputs,opcount,cases;
 in>>fields>>outputs>>opcount>>cases;
 if(fields!=1931||outputs!=1880||cases!=19600)return 2;
 std::vector<U> initial(fields),target(fields);
 for(auto &x:initial){in>>x;}
 for(auto &x:target){in>>x;}
 std::vector<Op> ops(opcount);
 for(auto &e:ops)in>>e.type>>e.d0>>e.d1>>e.s0>>e.s1>>e.q>>e.mask;
 int clean=0,best=outputs+1,controls=0;
 for(int which=0;which<cases;++which){
  std::array<U,12> r;for(auto &z:r)in>>z;if(!in)return 2;
  if(argc==3&&which==0&&std::string(argv[2])=="--mutate-witness")r[10]=(r[10]+1)%p;
  auto x=initial;
  const auto w0=weight(r[2],r[4]),w1=weight(r[2],1^r[4]);
  const auto v0=weight(r[3],r[5]),v1=weight(r[3],1^r[5]);
  for(const auto &e:ops){
   switch(e.type){
   case 0:
    x[e.d0]=(x[e.d0]+e.q*x[e.s0])%p;
    if(e.d1>=0)x[e.d1]=(x[e.d1]+e.q*x[e.s1])%p;
    break;
   case 1:{
    const auto &w=((e.mask>>r[0])&1)?w1:w0;
    const U z=(w[0]*x[e.s0]+w[1]*x[e.s1])%p;
    x[e.d0]=(x[e.d0]+e.q*z)%p;break;}
   case 2:{
    const auto &v=((e.mask>>r[1])&1)?v1:v0;
    const U z=e.q*x[e.s0]%p;
    x[e.d0]=(x[e.d0]+v[0]*z)%p;x[e.d1]=(x[e.d1]+v[1]*z)%p;break;}
   case 3:x[e.d0]=x[e.d0]*e.q%p;if(e.d1>=0)x[e.d1]=x[e.d1]*e.q%p;break;
   case 4:x[e.d0]=0;break;
   case 5:if(x[e.d0]!=0)return 4;x[e.d0]=e.q*x[e.s0]%p;break;
   default:return 5;
   }
  }
  std::array<int,3> bad{0,0,0};
  for(int i=0;i<outputs;++i)if(x[i]!=target[i])bad[i<400?0:i<800?1:2]++;
  for(int i=outputs;i<fields;++i)if(x[i]!=0)return 6;
  if(x[r[9]]!=r[10]||target[r[9]]!=r[11]||r[10]==r[11]){
   std::cerr<<"DETECTED_WITNESS_MISMATCH case "<<which<<"\n";return 3;
  }
  if(U(bad[0])!=r[6]||U(bad[1])!=r[7]||U(bad[2])!=r[8])return 7;
  if(!bad[2])clean++;
  const int total=bad[0]+bad[1]+bad[2];if(total<best)best=total;
  if(r[0]==0&&r[1]==0&&r[2]==0&&r[3]==1&&r[4]==0&&r[5]==0){
   if(bad!=std::array<int,3>{0,286,0})return 8;
   controls++;
  }
 }
 if(clean!=296||best!=286||controls!=1)return 9;
 U extra;if(in>>extra)return 10;
 std::cout<<"{\"status\":\"PASS_INDEPENDENT_ALL19600_WITNESSES\",\"cases\":19600,\"helper_clean\":"<<clean<<",\"minimum_mismatches\":"<<best<<",\"all_owned_zero\":true,\"no_new_kappa\":true}\n";
}
