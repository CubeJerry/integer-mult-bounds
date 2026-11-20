#include <array>
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <numeric>
#include <vector>

using Byte = std::uint8_t;

static Byte product(Byte x, Byte y) {
    unsigned u = x, v = y, z = 0;
    while (v) {
        if (v & 1) z ^= u;
        u <<= 1;
        if (u & 64) u ^= 0x43;
        v >>= 1;
    }
    return static_cast<Byte>(z);
}

// Row space dimension over GF(64), with all pivot multiples cached.
// Column order is reversed to provide a separate pivot convention.
extern "C" std::size_t dimension(Byte *a, std::size_t nr, std::size_t nc) {
    std::array<std::array<Byte,64>,64> table{};
    std::array<Byte,64> reciprocal{};
    for (unsigned i=0; i<64; ++i) for (unsigned j=0; j<64; ++j) {
        table[i][j]=product(i,j);
        if (table[i][j]==1) reciprocal[i]=j;
    }
    std::vector<std::size_t> order(nr);
    std::iota(order.begin(),order.end(),0);
    std::vector<Byte> multiples(64*nc);
    std::size_t rank=0;
    for (std::size_t width=nc; width>0 && rank<nr; --width) {
        std::size_t c=width-1, pivot=rank;
        while (pivot<nr && a[order[pivot]*nc+c]==0) ++pivot;
        if (pivot==nr) continue;
        std::swap(order[pivot],order[rank]);
        const Byte* basis=a+order[rank]*nc;
        for (unsigned q=1; q<64; ++q) {
            Byte factor=table[q][reciprocal[basis[c]]];
            Byte* values=multiples.data()+q*nc;
            for (std::size_t x=0; x<width; ++x) values[x]=table[factor][basis[x]];
        }
        for (std::size_t i=rank+1; i<nr; ++i) {
            Byte* row=a+order[i]*nc;
            const Byte factor=row[c];
            if (factor==0) continue;
            const Byte* values=multiples.data()+factor*nc;
            for (std::size_t x=0; x<width; ++x) row[x]^=values[x];
        }
        ++rank;
    }
    return rank;
}
