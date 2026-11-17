#include <array>
#include <cstdint>
#include <iostream>
#include <fstream>
#include <limits>
using Rows=std::array<unsigned,8>;
const int cost[6]={0,3,1,1,2,2};
std::pair<unsigned,unsigned> gate(unsigned u,unsigned v,int k){
  switch(k){case 0:return {u,v};case 1:return {v,u};case 2:return {u^v,v};
    case 3:return {u,u^v};case 4:return {u^v,u};default:return {v,u^v};}
}
uint64_t prefixes=0,solutions=0; int best=1000,seedmask=0,bestseed=0;
int partners[3][4]={{1,2,3,0},{2,3,0,1},{3,0,1,2}};
std::array<int,12> choice{},bestchoice{};Rows bestrows{};
void visit(int n,Rows rows,int used){
  if(n<8){int round=n/4,i=n%4,j=partners[round][i];
    for(int k=0;k<6;++k){auto [u,v]=gate(rows[i],rows[4+j],k);auto next=rows;next[i]=u;next[4+j]=v;
      choice[n]=k;visit(n+1,next,used+cost[k]);}return;}
  ++prefixes;unsigned multiplicity=1;auto final=rows;int total=used;
  for(int i=0;i<4;++i){int j=partners[2][i],accepted=0,mincost=100,selected=-1;
    for(int k=0;k<6;++k){auto [u,v]=gate(rows[i],rows[4+j],k);
      unsigned wa=15^(1<<i),wb=(15^(1<<j))<<4;
      unsigned da=(u&15)^wa,db=(v&240)^wb;
      bool good= !(u&(1<<i)) && !(v&(1<<(4+j))) && ((da==0 && (__builtin_popcount(db)==1||__builtin_popcount(db)==2))||(db==0 && (__builtin_popcount(da)==1||__builtin_popcount(da)==2)));
      if(good){++accepted;
        if(cost[k]<mincost){mincost=cost[k];selected=k;final[i]=u;final[4+j]=v;}}}
    if(!accepted)return;multiplicity*=accepted;total+=mincost;choice[8+i]=selected;}
  solutions+=multiplicity;if(total<best){best=total;bestchoice=choice;bestrows=final;bestseed=seedmask;}
}
int main(int argc,char**argv){int count=argc>1?16:1;
  if(argc>2){std::ifstream input(argv[2]);input>>count;
    for(seedmask=0;seedmask<count;++seedmask){for(int i=0;i<4;++i)partners[0][i]=i;
      for(int round=1;round<3;++round)for(int i=0;i<4;++i)input>>partners[round][i];
      Rows r;for(int i=0;i<8;++i){int k;input>>k;r[i]=1<<k;}visit(0,r,0);}
  }else for(seedmask=0;seedmask<count;++seedmask){Rows r;for(int i=0;i<4;++i){int prev=(i+3)%4;
    r[prev]=(seedmask>>i)&1?1<<i:1<<(4+prev);r[4+i]=(seedmask>>i)&1?1<<(4+prev):1<<i;}visit(0,r,0);}
  std::cout<<"{\"seed_permutations\":"<<count<<",\"two_round_prefixes\":"<<prefixes<<",\"full_solutions\":"<<solutions<<",\"minimum_forward_ADD_cost\":"<<best<<",\"best_seed_mask\":"<<bestseed<<",\"gate_choices\":[";
  for(int i=0;i<12;++i)std::cout<<(i?",":"")<<bestchoice[i];std::cout<<"],\"final_rows\":[";
  for(int i=0;i<8;++i)std::cout<<(i?",":"")<<bestrows[i];std::cout<<"]}\n";
}
