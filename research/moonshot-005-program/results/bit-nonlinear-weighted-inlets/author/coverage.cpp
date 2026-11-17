// Enumerate native real flats of rank at most four by least ordered bases.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>

constexpr int dimension = 8, role_count = 95, witness_count = 838, prime = 257;
using Row = std::array<int, dimension>;
using Rows = std::array<Row, role_count>;
using Closure = std::array<bool, role_count>;
using Hits = std::array<std::uint64_t, (witness_count + 63) / 64>;

struct Census {
    std::array<int, prime> inverse{};
    std::array<Hits, role_count> incidence{};
    std::array<int, witness_count> weight{};
    std::array<int, 5> flats{}, max_weight{}, max_roles{};
    std::array<std::array<int, dimension>, 5> axis_max{};
    Rows roots{};

    void measure(const Closure& contained, int rank) {
        ++flats[rank];
        Hits hit{};
        int size = 0, mass = 0;
        std::array<int, dimension> on_axis{};
        for (int i = 0; i < role_count; ++i) {
            if (!contained[i]) continue;
            ++size;
            for (int j = 0; j < dimension; ++j) on_axis[j] += roots[i][j] == 0;
            for (std::size_t j = 0; j < hit.size(); ++j) hit[j] |= incidence[i][j];
        }
        for (std::size_t j = 0; j < hit.size(); ++j) {
            auto mask = hit[j];
            while (mask) {
                mass += weight[64 * j + std::countr_zero(mask)];
                mask &= mask - 1;
            }
        }
        max_weight[rank] = std::max(mass, max_weight[rank]);
        max_roles[rank] = std::max(size, max_roles[rank]);
        for (int j = 0; j < dimension; ++j) axis_max[rank][j] = std::max(axis_max[rank][j], on_axis[j]);
    }

    void visit(const Rows& residues, const Closure& contained, int first, int rank) {
        measure(contained, rank);
        if (rank == 4) return;
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
        for (int j = 0; j < witness_count; ++j) {
            if (!(std::cin >> weight[j]) || weight[j] < 0 || weight[j] > 1000000) throw std::runtime_error("invalid weight");
            Closure seen{};
            for (int k = 0; k < 14; ++k) {
                int role;
                if (!(std::cin >> role) || role < 0 || role >= role_count || seen[role]) throw std::runtime_error("invalid witness");
                incidence[role][j / 64] |= std::uint64_t{1} << (j % 64);
                seen[role] = true;
            }
        }
        for (int x = 1; x < prime; ++x)
            for (int i = 1; i < prime; ++i)
                if (x * i % prime == 1) inverse[x] = i;
        visit(roots, {}, 0, 0);
        for (int r = 0; r <= 4; ++r) {
            std::cout << r << ' ' << flats[r] << ' ' << max_roles[r] << ' ' << max_weight[r];
            for (int n : axis_max[r]) std::cout << ' ' << n;
            std::cout << '\n';
        }
    }
};

int main() { Census data; data.run(); }
