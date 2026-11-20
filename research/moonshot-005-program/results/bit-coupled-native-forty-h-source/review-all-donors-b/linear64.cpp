// Independent exact GF64 elimination and literal source-word price replay.
#include <algorithm>
#include <cstdint>
#include <cstring>
#include <vector>
namespace {
uint8_t mult[64][64], inverse[64];
bool initialized = false;
uint8_t polynomial_product(unsigned a, unsigned b) {
    unsigned x = 0;
    for (unsigned i = 0; i < 6; ++i) if ((a >> i) & 1) x ^= b << i;
    for (int i = 10; i >= 6; --i) if ((x >> i) & 1) x ^= 0x43U << (i - 6);
    return uint8_t(x);
}
void initialize() {
    if (initialized) return;
    for (unsigned a = 0; a < 64; ++a) for (unsigned b = 0; b < 64; ++b)
        mult[a][b] = polynomial_product(a,b);
    for (unsigned a = 1; a < 64; ++a) for (unsigned b = 1; b < 64; ++b)
        if (mult[a][b] == 1) inverse[a] = uint8_t(b);
    initialized = true;
}
}
extern "C" int gf_product(int a, int b) { initialize(); return mult[a][b]; }
// Last available row is pivot; all arithmetic uses polynomial multiplication.
extern "C" int reduce64(uint8_t *a, int rows, int columns, int width,
                         int *pivots, int full) {
    initialize();
    int rank = 0;
    for (int col = 0; col < columns && rank < rows; ++col) {
        int p = rows - 1;
        while (p >= rank && !a[p*width+col]) --p;
        if (p < rank) continue;
        if (p != rank) for (int c = 0; c < width; ++c)
            std::swap(a[p*width+c], a[rank*width+c]);
        uint8_t scale = inverse[a[rank*width+col]];
        for (int c = col; c < width; ++c) a[rank*width+c] = mult[scale][a[rank*width+c]];
        for (int i = full ? 0 : rank+1; i < rows; ++i) {
            if (i == rank) continue;
            uint8_t q = a[i*width+col];
            if (!q) continue;
            for (int c = col; c < width; ++c) a[i*width+c] ^= mult[q][a[rank*width+c]];
        }
        pivots[rank++] = col;
    }
    return rank;
}
extern "C" void matmul64(const uint8_t *a, const uint8_t *b, uint8_t *out,
                           int rows, int middle, int columns) {
    initialize(); std::memset(out,0,size_t(rows)*columns);
    for (int i=0;i<rows;++i) for (int k=0;k<middle;++k) {
        uint8_t q=a[i*middle+k]; if (!q) continue;
        for (int j=0;j<columns;++j) out[i*columns+j] ^= mult[q][b[k*columns+j]];
    }
}
// Exact deterministic field-reduction stream: opcode,dst u16,src u16,scalar.
extern "C" int compile64(uint8_t *a, int n, uint8_t *stream,
                          uint64_t capacity, const uint64_t *weight,
                          const uint64_t *scale_price, uint64_t *price) {
    initialize(); uint64_t length=0, cost=0;
    auto emit = [&](uint8_t op,int d,int s,uint8_t q) {
        if (length+6>capacity) return false;
        stream[length++]=op;stream[length++]=uint8_t(d);stream[length++]=uint8_t(d>>8);
        stream[length++]=uint8_t(s);stream[length++]=uint8_t(s>>8);stream[length++]=q;
        return true;
    };
    for (int col=0;col<n;++col) {
        int p=col; while (p<n && !a[p*n+col]) ++p;
        if (p==n) return -1;
        if (p!=col) {
            for (int j=0;j<n;++j) std::swap(a[p*n+j],a[col*n+j]);
            if (!emit(2,col,p,0)) return -2; cost+=18;
        }
        if (a[col*n+col]!=1) {
            uint8_t q=inverse[a[col*n+col]];
            if (!emit(1,col,0,q)) return -2; cost+=scale_price[q];
            for (int j=0;j<n;++j) a[col*n+j]=mult[q][a[col*n+j]];
        }
        for (int i=0;i<n;++i) if (i!=col && a[i*n+col]) {
            uint8_t q=a[i*n+col];
            if (!emit(0,i,col,q)) return -2; cost+=weight[q];
            for (int j=0;j<n;++j) a[i*n+j]^=mult[q][a[col*n+j]];
        }
    }
    for (int i=0;i<n;++i) for (int j=0;j<n;++j)
        if (a[i*n+j] != uint8_t(i==j)) return -3;
    *price=cost; return int(length);
}
