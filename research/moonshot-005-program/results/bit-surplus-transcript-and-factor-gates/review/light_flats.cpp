// Enumerate native real flats of rank at most five by least ordered bases.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>

constexpr int dimension = 8, role_count = 95, prime = 257;
using Row = std::array<int, dimension>;
using Rows = std::array<Row, role_count>;
using Closure = std::array<bool, role_count>;
constexpr int light_count=6;
struct Census {
    std::array<int,prime> inverse{};
    Rows roots{};
    std::array<int,role_count> membership{};
    std::array<int,6> counts{},occupancy{};
    std::array<int,light_count> max_light{};
    void measure(const Closure& contained,int rank) {
        ++counts[rank];
        int size=0;
        std::array<int,light_count> part{};
        for(int j=0;j<role_count;j++) if(contained[j]) {
            ++size;
            for(int k=0;k<light_count;k++) part[k]+=(membership[j]>>k)&1;
        }
        occupancy[rank]=std::max(occupancy[rank],size);
        if(rank==5) for(int k=0;k<light_count;k++) max_light[k]=std::max(max_light[k],part[k]);
    }

    void visit(const Rows& residues, const Closure& contained, int first, int rank) {
        measure(contained, rank);
        if (rank == 5) return;
        for (int p = first; p < role_count; ++p) {
            if (contained[p]) continue;
            Row pivot = residues[p];
            auto it = std::find_if(pivot.begin(), pivot.end(), [](int x) { return x != 0; });
            if (it == pivot.end()) throw std::logic_error("invalid closure");
            int c = static_cast<int>(it - pivot.begin());
            int scale = inverse[*it];
            for (int& x : pivot) x = x * scale % prime;
            Rows next;
            Closure closure{};
            bool least_basis = true;
            for (int i = 0; i < role_count; ++i) {
                bool zero = true;
                for (int j = 0; j < dimension; ++j) {
                    next[i][j] = (residues[i][j] + prime * prime - residues[i][c] * pivot[j]) % prime;
                    if (next[i][j]) zero = false;
                }
                closure[i] = zero;
                if (i < p && zero && !contained[i]) { least_basis = false; break; }
            }
            if (least_basis) visit(next, closure, p + 1, rank + 1);
        }
    }

    void run() {
        for (auto& row : roots) {
            int norm = 0;
            for (int& x : row) {
                if (!(std::cin >> x) || x < -2 || x > 2) throw std::runtime_error("invalid root");
                norm += x * x;
                x = (x + prime) % prime;
            }
            if (norm != 4) throw std::runtime_error("unexpected squared norm");
        }
        for(int& mask:membership) if(!(std::cin>>mask) || mask<0 || mask>=64) throw std::logic_error("invalid membership");
        for (int x = 1; x < prime; ++x)
            for (int i = 1; i < prime; ++i)
                if (x * i % prime == 1) inverse[x] = i;
        visit(roots, {}, 0, 0);
        for(int r=0;r<=5;r++) std::cout<<r<<" "<<counts[r]<<" "<<occupancy[r]<<"\n";
        for(int amount:max_light) std::cout<<amount<<" ";
        std::cout<<"\n";
    }
};

int main() { Census data; data.run(); }
