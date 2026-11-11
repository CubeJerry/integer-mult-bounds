#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
using U=uint64_t;
constexpr U P=1000000007, HALF=500000004;
struct Op {int t,d,s;U q;int c,n,k,m,dim,event;};
struct Result {int a=0,b=0,h=0,first=-1;U got=0,want=0;};
int pattern(int scheme,const Op&e,int role,int total){
 switch(scheme){
 case 0:return 0;case 1:return 1;case 2:return e.c&1;
 case 3:return e.c==0;case 4:return e.c==e.n-1;
 case 5:return 2*e.c>=e.n;case 6:return e.k&1;
 case 7:return e.k==0;case 8:return e.k==e.m-1;
 case 9:return 2*e.k>=e.m;case 10:return e.dim&1;
 case 11:return 2*e.event>=total;case 12:return role&1;
 case 13:return e.c%3==0;
 }
 return 0;
}
std::array<U,2> weights(int style,int bit){
 U sign=bit?P-1:1;
 switch(style){
 case 0:return bit?std::array<U,2>{0,1}:std::array<U,2>{1,0};
 case 1:return {1,sign};
 case 2:return {HALF,sign*HALF%P};
 case 3:return {sign,1};
 case 4:return {sign*HALF%P,HALF};
 }
 return {0,0};
}
int main(int argc,char**argv){
 if(argc!=3){std::cerr<<"usage: screen input output-prefix\n";return 2;}
 std::ifstream f(argv[1]);int N,C,H,E,T;f>>N>>C>>H>>E>>T;
 std::vector<U>A(N),B(N),U0(C),EA(N),EB(N);
 for(auto* x:{&A,&B,&U0,&EA,&EB})for(auto&v:*x)f>>v;
 std::vector<Op> ops(E);for(auto&e:ops)f>>e.t>>e.d>>e.s>>e.q>>e.c>>e.n>>e.k>>e.m>>e.dim>>e.event;
 if(!f){std::cerr<<"input parse failed\n";return 2;}
 auto run=[&](int lp,int rp,int ls,int rs,int lf,int rf){
  auto a=A,b=B,u=U0;
  for(const auto&e:ops){
   switch(e.t){
   case 0:u[e.d]=(u[e.d]+e.q*u[e.s])%P;break;
   case 1:a[e.d]=(a[e.d]+e.q*a[e.s])%P;b[e.d]=(b[e.d]+e.q*b[e.s])%P;break;
   case 2:{auto w=weights(ls,pattern(lp,e,e.s,T)^lf);U x=(w[0]*a[e.s]+w[1]*b[e.s])%P;u[e.d]=(u[e.d]+e.q*x)%P;break;}
   case 3:{auto v=weights(rs,pattern(rp,e,e.d,T)^rf);U x=e.q*u[e.s]%P;a[e.d]=(a[e.d]+v[0]*x)%P;b[e.d]=(b[e.d]+v[1]*x)%P;break;}
   case 4:u[e.d]=u[e.d]*e.q%P;break;
   case 5:a[e.d]=a[e.d]*e.q%P;b[e.d]=b[e.d]*e.q%P;break;
   case 6:u[e.d]=0;break;
   default:throw std::runtime_error("unknown opcode");
   }
  }
  Result r;
  auto bad=[&](int field,U got,U want,int&n){if(got!=want){++n;if(r.first<0){r.first=field;r.got=got;r.want=want;}}};
  for(int i=0;i<N;++i){bad(i,a[i],EA[i],r.a);bad(N+i,b[i],EB[i],r.b);}
  for(int i=0;i<H;++i)bad(2*N+i,u[i],U0[i],r.h);
  for(int i=H;i<C;++i)if(u[i]!=0)throw std::runtime_error("owned final dirt not cleared");
  return r;
 };
 auto control=run(0,0,0,1,0,0);
 if(control.a||control.h||control.b!=286){std::cerr<<"fixed-selector control failed "<<control.a<<" "<<control.b<<" "<<control.h<<"\n";return 3;}
 std::string prefix=argv[2];std::ofstream rejects(prefix+".tsv"),survivors(prefix+"-survivors.tsv");
 rejects<<"load_pattern\tread_pattern\tload_style\tread_style\tload_flip\tread_flip\tbad_A\tbad_B\tbad_helpers\tfirst_field\tgot\texpected\n";
 auto start=std::chrono::steady_clock::now();int checked=0,alive=0,helper_clean=0,best=100000;
 std::array<int,6> bestp{};Result bestr;bool stopped=false;
 for(int lp=0;lp<14&&!stopped;++lp)for(int rp=0;rp<14&&!stopped;++rp)for(int ls=0;ls<5&&!stopped;++ls)for(int rs=0;rs<5&&!stopped;++rs)for(int lf=0;lf<2&&!stopped;++lf)for(int rf=0;rf<2&&!stopped;++rf){
  auto r=run(lp,rp,ls,rs,lf,rf);++checked;if(!r.h)++helper_clean;
  int score=r.a+r.b+r.h;if(score<best){best=score;bestp={lp,rp,ls,rs,lf,rf};bestr=r;}
  auto&out=score?rejects:survivors;
  out<<lp<<'\t'<<rp<<'\t'<<ls<<'\t'<<rs<<'\t'<<lf<<'\t'<<rf<<'\t'<<r.a<<'\t'<<r.b<<'\t'<<r.h<<'\t'<<r.first<<'\t'<<r.got<<'\t'<<r.want<<'\n';
  if(!score)++alive;
  if(checked%1000==0){double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();std::cout<<"PROGRESS "<<checked<<" seconds "<<sec<<" survivors "<<alive<<std::endl;if(sec>600)stopped=true;}
 }
 double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
 std::ofstream summary(prefix+"-summary.json");
 summary<<"{\n\"checked\":"<<checked<<",\"declared_family\":19600,\"complete\":"<<(checked==19600?"true":"false")<<",\"survivors\":"<<alive<<",\"helper_clean\":"<<helper_clean<<",\"best_total_bad\":"<<best<<",\"best_parameters\":[";
 for(int i=0;i<6;++i)summary<<(i?",":"")<<bestp[i];
 summary<<"],\"best_bad_A\":"<<bestr.a<<",\"best_bad_B\":"<<bestr.b<<",\"best_bad_helpers\":"<<bestr.h<<",\"seconds\":"<<sec<<",\"scope\":\"Finite modular rejection screen only. No general obstruction or construction certificate.\"}\n";
 std::cout<<"COMPLETE checked "<<checked<<" survivors "<<alive<<" helper_clean "<<helper_clean<<" best "<<best<<" seconds "<<sec<<std::endl;
}
