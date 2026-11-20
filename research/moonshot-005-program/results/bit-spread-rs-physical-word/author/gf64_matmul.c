#include <stddef.h>
#include <stdint.h>
#include <string.h>
#ifdef __AVX2__
#include <immintrin.h>
#endif

/* Dense row-major GF(64), z^6+z+1. Call with a validated 64x64 product table. */
void gf64_gemm(const uint8_t *a, const uint8_t *b, uint8_t *out, const uint8_t *tab,
               size_t m, size_t k, size_t n) {
    memset(out,0,m*n);
    for (size_t i=0;i<m;i++) {
        uint8_t *o=out+i*n;
        for (size_t t=0;t<k;t++) {
            uint8_t coeff=a[i*k+t];
            if (!coeff) continue;
            const uint8_t *s=b+t*n,*p=tab+64*coeff;
            size_t j=0;
#ifdef __AVX2__
            __m128i low=_mm_loadu_si128((const __m128i*)p);
            uint8_t high_data[16]={0,p[16],p[32],p[48]};
            __m128i high=_mm_loadu_si128((const __m128i*)high_data);
            __m256i lo=_mm256_broadcastsi128_si256(low),hi=_mm256_broadcastsi128_si256(high);
            __m256i mask=_mm256_set1_epi8(15);
            for(;j+32<=n;j+=32) {
                __m256i input=_mm256_loadu_si256((const __m256i*)(s+j));
                __m256i v=_mm256_xor_si256(_mm256_shuffle_epi8(lo,_mm256_and_si256(input,mask)),
                     _mm256_shuffle_epi8(hi,_mm256_and_si256(_mm256_srli_epi16(input,4),mask)));
                _mm256_storeu_si256((__m256i*)(o+j),_mm256_xor_si256(v,_mm256_loadu_si256((const __m256i*)(o+j))));
            }
#endif
            for(;j<n;j++) o[j]^=p[s[j]];
        }
    }
}
