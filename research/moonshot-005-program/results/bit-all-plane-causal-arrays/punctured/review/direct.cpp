#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using namespace std;
unsigned char table128[128][128], inverse128[128];
int mul_poly(int a,int b){
    int q=0;for(int k=0;k<7;k++)if((b>>k)&1)q^=a<<k;
    for(int k=12;k>=7;k--)if((q>>k)&1)q^=131<<(k-7);
    return q;
}
uint32_t read32(ifstream&in){unsigned char p[4];in.read((char*)p,4);if(!in)throw runtime_error("truncated review input");return uint32_t(p[0])|(uint32_t(p[1])<<8)|(uint32_t(p[2])<<16)|(uint32_t(p[3])<<24);}
pair<int,int> rankdet(array<array<unsigned char,60>,60> a){
    int rank=0,det=1;
    for(int col=0;col<60&&rank<60;col++){
        int p=rank;while(p<60&&!a[p][col])p++;
        if(p==60)continue;
        swap(a[p],a[rank]);int pivot=a[rank][col];det=table128[det][pivot];int iv=inverse128[pivot];
        for(int c=col;c<60;c++)a[rank][c]=table128[a[rank][c]][iv];
        for(int r=rank+1;r<60;r++)if(a[r][col]){
            const auto* mult=table128[a[r][col]];
            for(int c=col;c<60;c++)a[r][c]^=mult[a[rank][c]];
        }
        rank++;
    }
    return {rank,rank==60?det:0};
}
int main(int argc,char**argv){
    if(argc!=3)throw runtime_error("usage direct INPUT OUTPUT");
    for(int a=0;a<128;a++)for(int b=0;b<128;b++)table128[a][b]=mul_poly(a,b);
    for(int a=1;a<128;a++){
        for(int b=1;b<128;b++)if(table128[a][b]==1){inverse128[a]=b;break;}
        if(!inverse128[a])throw runtime_error("not a field");
    }
    array<array<unsigned char,90>,90> V;
    for(int r=0;r<90;r++){V[r][0]=1;for(int c=1;c<90;c++)V[r][c]=table128[V[r][c-1]][r+1];}
    ifstream in(argv[1],ios::binary);ofstream out(argv[2]);if(!in||!out)throw runtime_error("review IO");
    uint32_t planes=read32(in);int conditions=0;map<int,int>ranks;bool negative=false;out<<"{\"schema\":\"direct-60-by-60-source-projections-v1\",\"conditions\":[";bool first=true;
    for(uint32_t z=0;z<planes;z++){
        auto h=read32(in),receivers=read32(in);array<array<unsigned char,90>,90>C;
        in.read((char*)C.data(),8100);if(!in)throw runtime_error("truncated coefficients");
        for(uint32_t t=0;t<receivers;t++){
            auto receiver=read32(in);array<unsigned char,30>S;in.read((char*)S.data(),30);if(!in)throw runtime_error("truncated subset");
            for(int donor=0;donor<2;donor++){
                array<array<unsigned char,60>,60> M{};
                for(int r=0;r<30;r++){
                    int p=S[r];if(p>=90)throw runtime_error("bad row");
                    for(int c=0;c<45;c++){M[r][c]=V[p][45*donor+c];M[30+r][c]=C[p][45*donor+c];}
                    for(int c=0;c<15;c++)M[30+r][45+c]=V[p][15*donor+c];
                }
                auto[rank,det]=rankdet(M);if(rank!=60)throw runtime_error("direct full projection singular");ranks[rank]++;conditions++;
                if(!first)out<<",";first=false;out<<"["<<h<<","<<receiver<<","<<donor<<","<<det<<"]";
                if(!negative){
                    for(int r=30;r<60;r++)for(int c=0;c<45;c++)M[r][c]=0;
                    auto[bad_rank,bad_det]=rankdet(M);if(bad_rank!=45||bad_det)throw runtime_error("zero-crosswave control");negative=true;
                }
            }
        }
    }
    if(in.peek()!=EOF)throw runtime_error("trailing review bytes");
    out<<"],\"plane_count\":"<<planes<<",\"condition_count\":"<<conditions<<",\"all_rank_60\":true,\"zero_crosswave_control_rank\":45}\n";
    cout<<"PASS_DIRECT_ALL_60_BY_60_PROJECTIONS "<<planes<<" planes "<<conditions<<" conditions\n";
}
