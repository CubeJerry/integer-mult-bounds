// Find every minimum-dimensional real span of native roots meeting all 838 witnesses.
// Rank over F_257 agrees with rational rank on these roots by the minor bound in PROOF.md.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <unordered_set>
#include <vector>

constexpr int dimension = 8;
constexpr int roles_count = 95;
constexpr int prime = 257;
constexpr int depth_limit = 6;
using Row = std::array<int, dimension>;
using Rows = std::array<Row, roles_count>;

struct Mask {
    std::uint64_t low = 0, high = 0;
    bool operator==(const Mask&) const = default;
    void add(int i) {
        if (i < 64) low |= std::uint64_t{1} << i;
        else high |= std::uint64_t{1} << (i - 64);
    }
    bool meets(Mask other) const { return (low & other.low) || (high & other.high); }
};

struct MaskHash {
    std::size_t operator()(Mask m) const { return m.low ^ (m.high * 0x9e3779b185ebca87ULL); }
};

struct Witness {
    std::array<int, 14> indices;
    Mask mask;
};

class Search {
    std::array<int, roles_count> roles{};
    std::array<int, prime> inverse{};
    std::vector<Witness> witnesses;
    std::array<std::unordered_set<Mask, MaskHash>, depth_limit + 1> seen;
    std::array<std::size_t, depth_limit + 1> hit_count{};
    std::vector<int> basis;

    void visit(const Rows& residues, Mask closure, int rank) {
        if (!seen[rank].insert(closure).second) return;
        auto missed = std::find_if(witnesses.begin(), witnesses.end(),
            [&](const Witness& w) { return !closure.meets(w.mask); });
        if (missed == witnesses.end()) {
            ++hit_count[rank];
            std::cout << "basis";
            for (int i : basis) std::cout << ' ' << roles[i];
            std::cout << '\n';
            return;
        }
        if (rank == depth_limit) return;
        // Every hitting extension contains at least one root of this unhit witness.
        for (int id : missed->indices) {
            Row pivot = residues[id];
            auto lead = std::find_if(pivot.begin(), pivot.end(), [](int v) { return v != 0; });
            if (lead == pivot.end()) throw std::logic_error("witness hit before extension");
            int column = static_cast<int>(lead - pivot.begin());
            int scale = inverse[*lead];
            for (int& value : pivot) value = value * scale % prime;
            Rows next{};
            Mask next_closure;
            for (int i = 0; i < roles_count; ++i) {
                bool is_zero = true;
                for (int j = 0; j < dimension; ++j) {
                    next[i][j] = (residues[i][j] + prime * prime - residues[i][column] * pivot[j]) % prime;
                    if (next[i][j]) is_zero = false;
                }
                if (is_zero) next_closure.add(i);
            }
            basis.push_back(id);
            visit(next, next_closure, rank + 1);
            basis.pop_back();
        }
    }

public:
    void run(std::istream& input) {
        Rows roots{};
        std::array<int, 111> position;
        position.fill(-1);
        for (int i = 0; i < roles_count; ++i) {
            if (!(input >> roles[i]) || roles[i] < 0 || roles[i] >= 111 || position[roles[i]] != -1)
                throw std::runtime_error("invalid role table");
            position[roles[i]] = i;
        }
        for (auto& row : roots) {
            int norm = 0;
            for (int& value : row) {
                if (!(input >> value) || value < -2 || value > 2) throw std::runtime_error("invalid root");
                norm += value * value;
                value = (value + prime) % prime;
            }
            if (norm != 4) throw std::runtime_error("root norm");
        }
        int count;
        if (!(input >> count) || count != 838) throw std::runtime_error("witness count");
        for (int n = 0; n < count; ++n) {
            Witness w{};
            std::set<int> distinct;
            for (int& id : w.indices) {
                int role;
                if (!(input >> role) || role < 0 || role >= 111 || position[role] == -1 || !distinct.insert(role).second)
                    throw std::runtime_error("witness contains invalid or duplicate role");
                id = position[role];
                w.mask.add(id);
            }
            witnesses.push_back(w);
        }
        for (int x = 1; x < prime; ++x)
            for (int y = 1; y < prime; ++y)
                if (x * y % prime == 1) inverse[x] = y;
        visit(roots, {}, 0);
        std::cout << "visited";
        for (const auto& group : seen) std::cout << ' ' << group.size();
        std::cout << "\nhitting";
        for (auto n : hit_count) std::cout << ' ' << n;
        std::cout << '\n';
        if (hit_count != decltype(hit_count){0, 0, 0, 0, 0, 0, 194}) throw std::runtime_error("unexpected hitting census");
    }
};

int main(int argc, char** argv) {
    if (argc != 2) return 2;
    std::ifstream input(argv[1]);
    Search search;
    search.run(input);
}
