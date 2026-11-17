// Test all two-seed closures on the native receiver neighbourhoods.
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

struct Bits {
    std::uint64_t lo{}, hi{};
    bool has(int i) const { return (i < 64 ? lo >> i : hi >> (i-64)) & 1; }
    void add(int i) { if (i < 64) lo |= std::uint64_t{1} << i; else hi |= std::uint64_t{1} << (i-64); }
    int size() const { return std::popcount(lo)+std::popcount(hi); }
    friend Bits operator&(Bits a,Bits b) { return {a.lo & b.lo,a.hi & b.hi}; }
};

int main() {
    constexpr int n=111;
    std::array<std::array<int,8>,n> root;
    for (auto& v:root) for (auto& x:v) if (!(std::cin>>x)) throw std::runtime_error("bad native input");
    std::array<std::array<int,n>,n> dot{};
    std::array<Bits,n> nonorth{}, neighbours{};
    for (int j=0;j<n;j++) for (int k=0;k<n;k++) {
        for (int c=0;c<8;c++) dot[j][k]+=root[j][c]*root[k][c];
        if (dot[j][k]==0) neighbours[j].add(k);
        if (dot[j][k]==2 || dot[j][k]==-2) nonorth[j].add(k);
    }
    // The other two role lines of an A2 through j determine each other.
    std::array<std::array<int,n>,n> mate{};
    for (int j=0;j<n;j++) for (int k=0;k<n;k++) {
        mate[j][k]=-1;
        if (!nonorth[j].has(k)) continue;
        for (int r=0;r<n;r++) {
            if (r==j || r==k) continue;
            bool plus=true,minus=true;
            for (int c=0;c<8;c++) {
                int v=root[j][c]-(dot[j][k]/2)*root[k][c];
                plus=plus && (v==root[r][c]);
                minus=minus && (-v==root[r][c]);
            }
            if (plus || minus) mate[j][k]=r;
        }
    }
    int pair_count=0, min_closed=n, max_round=0, failures=0;
    for (int i=0;i<n;i++) {
        std::vector<int> near;
        for (int j=0;j<n;j++) if (neighbours[i].has(j)) near.push_back(j);
        int worst=0,mind=n,bad=0;
        for (int j:near) for (int k:near) if (k>j) {
            ++pair_count;
            Bits seeds;
            seeds.add(j); seeds.add(k);
            int rounds=0;
            while (true) {
                Bits next=seeds;
                for (int h:near) {
                    if (seeds.has(h)) continue;
                    Bits hits=seeds & nonorth[h];
                    int count=hits.size();
                    if (count<2) continue;
                    if (count==2) {
                        int a=hits.lo?std::countr_zero(hits.lo):64+std::countr_zero(hits.hi);
                        int other=mate[h][a];
                        if (other>=0 && hits.has(other)) continue;
                    }
                    next.add(h);
                }
                if (next.size()==seeds.size()) break;
                ++rounds; seeds=next;
            }
            if (seeds.size()!=int(near.size())) ++bad;
            if (mind>seeds.size()) mind=seeds.size();
            if (worst<rounds) worst=rounds;
        }
        if (min_closed>mind) min_closed=mind;
        if (max_round<worst) max_round=worst;
        failures+=bad;
        std::cout<<i<<" "<<near.size()<<" "<<mind<<" "<<worst<<" "<<bad<<"\n";
    }
    std::cerr<<pair_count<<" pairs, "<<failures<<" failures, min closure "<<min_closed<<", max rounds "<<max_round<<"\n";
}
