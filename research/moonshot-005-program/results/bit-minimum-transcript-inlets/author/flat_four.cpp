/* Exact outer bound on the native lines in any real rank <=4 subspace.
 * A real-rank-four integer matrix has rank <=4 modulo 3 by its minors.
 * Enumerate every native projective basis of ranks <=4 modulo 3. */
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

using Point = std::array<int, 8>;
constexpr int count = 95;
constexpr int universe = 6561;
int plus_table[count][universe];
int point_index[universe];
Point roots[count];
int number[count], opposite[count];

int encode(const Point& coordinates) {
    int n=0;
    for (int j=7; j>=0; --j) n=3*n+(coordinates[j]%3+3)%3;
    return n;
}
int addition(int role, int n) {
    Point p{};
    for (int j=0; j<8; ++j) { p[j]=roots[role][j]+n%3; n/=3; }
    return encode(p);
}
int main() {
    std::fill(point_index, point_index+universe, -1);
    for (int i=0; i<count; ++i) {
        Point neg{};
        for (int j=0; j<8; ++j) {
            if (!(std::cin>>roots[i][j])) throw std::runtime_error("missing role coordinate");
            neg[j]=-roots[i][j];
        }
        number[i]=encode(roots[i]); opposite[i]=encode(neg);
        if (!number[i] || point_index[number[i]]>=0) throw std::runtime_error("duplicate projective point");
        point_index[number[i]]=point_index[opposite[i]]=i;
        for (int n=0; n<universe; ++n) plus_table[i][n]=addition(i,n);
    }
    std::array<int,5> maximum{0,1,0,0,0};
    std::array<int,8> axis_four{};
    std::array<long long,5> independent{1,count,0,0,0};
    // Repeated bases of a flat are intentional. Each reported maximum
    // only needs exhaustive coverage of all bases, not flat deduplication.
    for (int i=0; i<count; ++i) for (int j=i+1; j<count; ++j) {
        int line[3]={0,number[i],opposite[i]};
        int plane[9], p=0;
        for(int x:line){
            plane[p++]=x;plane[p++]=plus_table[j][x];
            plane[p++]=plus_table[j][plus_table[j][x]];
        }
        int nplane=0;for(int x:plane) nplane+=point_index[x]>=0;
        maximum[2]=std::max(maximum[2],nplane/2);++independent[2];
        for (int k=j+1; k<count; ++k) {
            if (std::find(plane,plane+9,number[k])!=plane+9) continue;
            ++independent[3];
            int three[27], t=0;
            for (int x:plane) {
                three[t++]=x;three[t++]=plus_table[k][x];
                three[t++]=plus_table[k][plus_table[k][x]];
            }
            int nth=0;
            for(int x:three) nth+=point_index[x]>=0;
            nth/=2;maximum[3]=std::max(maximum[3],nth);
            for(int l=k+1;l<count;++l) {
                if (std::find(three,three+27,number[l])!=three+27) continue;
                ++independent[4];
                int nf=nth;
                for(int x:three) nf+=point_index[plus_table[l][x]]>=0;
                maximum[4]=std::max(maximum[4],nf);
                if(nf<11) continue;
                // ± roles in the old subspace are counted in both signs.
                // The new coset l+three contributes each new line once.
                for(int a=0;a<8;++a) {
                    int nzero=0;
                    for(int x:three) {
                        int id=point_index[x];
                        if(id>=0 && roots[id][a]==0) ++nzero;
                    }
                    nzero/=2;
                    for(int x:three) {
                        int id=point_index[plus_table[l][x]];
                        if(id>=0 && roots[id][a]==0) ++nzero;
                    }
                    axis_four[a]=std::max(axis_four[a],nzero);
                }
            }
        }
    }
    for(int r=1;r<=4;++r)std::cout<<maximum[r]<<(r<4?' ':'\n');
    for(int a=0;a<8;++a)std::cout<<axis_four[a]<<(a<7?' ':'\n');
    for(int r=1;r<=4;++r)std::cout<<independent[r]<<(r<4?' ':'\n');
}
