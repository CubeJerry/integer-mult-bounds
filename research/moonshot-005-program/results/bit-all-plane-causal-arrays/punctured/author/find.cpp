#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <vector>
using Row=std::vector<int>;using Mat=std::vector<Row>;
static int mul[128][128],inv[128];
static void need(bool b,const char*s){if(!b)throw std::runtime_error(s);}
static int product(int a,int b){int c=0;while(b){if(b&1)c^=a;b>>=1;a<<=1;if(a&128)a^=131;}return c;}
static int power(int a,int n){int r=1;while(n){if(n&1)r=mul[r][a];a=mul[a][a];n>>=1;}return r;}
static Mat multiply(const Mat&a,const Mat&b){need(!a.empty()&&!b.empty()&&a[0].size()==b.size(),"matrix dimensions");Mat c(a.size(),Row(b[0].size()));for(size_t i=0;i<a.size();++i)for(size_t k=0;k<b.size();++k)if(a[i][k])for(size_t j=0;j<b[0].size();++j)c[i][j]^=mul[a[i][k]][b[k][j]];return c;}
static Mat transpose(const Mat&a){Mat b(a[0].size(),Row(a.size()));for(size_t i=0;i<a.size();++i)for(size_t j=0;j<a[0].size();++j)b[j][i]=a[i][j];return b;}
// Return a matrix whose rows are a canonical basis of the right nullspace.
static Mat nullrows(Mat a){int n=a.size(),m=a[0].size(),r=0;std::vector<int>p;for(int j=0;j<m&&r<n;++j){int z=r;while(z<n&&!a[z][j])++z;if(z==n)continue;std::swap(a[z],a[r]);int v=inv[a[r][j]];for(int k=j;k<m;++k)a[r][k]=mul[a[r][k]][v];for(int i=0;i<n;++i)if(i!=r&&a[i][j]){v=a[i][j];for(int k=j;k<m;++k)a[i][k]^=mul[v][a[r][k]];}p.push_back(j);++r;}Mat out;for(int j=0;j<m;++j)if(std::find(p.begin(),p.end(),j)==p.end()){Row z(m);z[j]=1;for(int i=0;i<r;++i)z[p[i]]=a[i][j];out.push_back(z);}return out;}
static int determinant(Mat a){int n=a.size();need(a[0].size()==a.size(),"square determinant");int det=1;for(int j=0;j<n;++j){int p=j;while(p<n&&!a[p][j])++p;if(p==n)return 0;std::swap(a[p],a[j]);int v=a[j][j];det=mul[det][v];v=inv[v];for(int k=j;k<n;++k)a[j][k]=mul[a[j][k]][v];for(int i=j+1;i<n;++i)if(a[i][j]){v=a[i][j];for(int k=j;k<n;++k)a[i][k]^=mul[v][a[j][k]];}}return det;}
static uint64_t next64(uint64_t&x){x^=x<<13;x^=x>>7;x^=x<<17;return x;}
struct Condition{int receiver,donor;Row rows;Mat right,left;};
int main(int argc,char**argv){try{need(argc==3,"usage: find INSTANCE.txt COEFFICIENTS.json");for(int a=0;a<128;++a)for(int b=0;b<128;++b)mul[a][b]=product(a,b);for(int a=1;a<128;++a){inv[a]=power(a,126);need(mul[a][inv[a]]==1,"field inverses");}Mat V(90,Row(90));for(int i=0;i<90;++i)for(int j=0;j<90;++j)V[i][j]=power(i+1,j);need(determinant(V)!=0,"V90 invertible");std::ifstream in(argv[1]);std::ofstream out(argv[2]);need(bool(in)&&bool(out),"input/output files");int count;in>>count;out<<"{\"schema\":\"F128-punctured-H-explicit-causal-array-v1\",\"field_modulus\":131,\"planes\":[";long long total_conditions=0,total_trials=0;for(int p=0;p<count;++p){int h,nr;in>>h>>nr;std::vector<Condition>cs;for(int t=0;t<nr;++t){int receiver;in>>receiver;Row rows(30);for(int&z:rows)in>>z;for(int donor=0;donor<2;++donor){Mat A(30,Row(45)),B(30,Row(15));for(int i=0;i<30;++i){need(rows[i]>=0&&rows[i]<90,"actual port row");for(int j=0;j<45;++j)A[i][j]=V[rows[i]][45*donor+j];for(int j=0;j<15;++j)B[i][j]=V[rows[i]][15*donor+j];}Mat N=nullrows(A),L=nullrows(transpose(B));need(N.size()==15&&L.size()==15,"Vandermonde source ranks");need(multiply(A,transpose(N))==Mat(30,Row(15)),"right kernel");need(multiply(L,B)==Mat(15,Row(15)),"left kernel");cs.push_back({receiver,donor,rows,transpose(N),L});}}Mat C;std::vector<int>dets;uint64_t selected_seed=0;int trials=0;for(;;){++trials;need(trials<10000,"bounded materialization search");uint64_t state=0x9e3779b97f4a7c15ULL^(uint64_t(h+1)*0x100000001b3ULL)^(uint64_t(trials)*0xd1342543de82ef95ULL);selected_seed=state;C=Mat(90,Row(90));for(auto&row:C)for(int&z:row)z=int(next64(state)&127);dets.clear();bool good=true;for(const auto&c:cs){Mat Q(30,Row(45));for(int i=0;i<30;++i)for(int j=0;j<45;++j)Q[i][j]=C[c.rows[i]][45*c.donor+j];int d=determinant(multiply(c.left,multiply(Q,c.right)));if(!d){good=false;break;}dets.push_back(d);}if(good)break;}total_conditions+=cs.size();total_trials+=trials;if(p)out<<',';out<<"{\"H\":"<<h<<",\"trial\":"<<trials<<",\"xorshift_seed_decimal\":\""<<selected_seed<<"\",\"C_hex_rows\":[";for(int i=0;i<90;++i){if(i)out<<',';out<<'\"';for(int x:C[i])out<<std::hex<<std::setw(2)<<std::setfill('0')<<x;out<<std::dec<<'\"';}out<<"],\"conditions\":[";for(size_t t=0;t<cs.size();++t){if(t)out<<',';out<<'['<<cs[t].receiver<<','<<cs[t].donor<<','<<dets[t]<<']';}out<<"]}";}
out<<"],\"total_conditions\":"<<total_conditions<<",\"total_trials\":"<<total_trials<<"}\n";std::cout<<"PASS "<<count<<" planes "<<total_conditions<<" conditions "<<total_trials<<" trials\n";
}catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
