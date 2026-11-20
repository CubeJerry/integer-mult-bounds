#include <stdint.h>
#include <stddef.h>
#ifdef __AVX2__
#include <immintrin.h>
#endif
/* Exact polynomial-basis GF(64) elimination. The caller supplies field tables. */
static inline void add_multiple(uint8_t *d,const uint8_t *s,size_t n,const uint8_t *p) {
    size_t j=0;
#ifdef __AVX2__
    const __m256i lo=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i *)p));
    const uint8_t h[16]={0,p[16],p[32],p[48]};
    const __m256i hi=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i *)h));
    const __m256i mask=_mm256_set1_epi8(15);
    for(;j+32<=n;j+=32) {
        __m256i x=_mm256_loadu_si256((const __m256i *)(s+j));
        __m256i y=_mm256_xor_si256(_mm256_shuffle_epi8(lo,_mm256_and_si256(x,mask)),
                      _mm256_shuffle_epi8(hi,_mm256_and_si256(_mm256_srli_epi16(x,4),mask)));
        _mm256_storeu_si256((__m256i *)(d+j),_mm256_xor_si256(y,_mm256_loadu_si256((const __m256i *)(d+j))));
    }
#endif
    for(;j<n;j++)d[j]^=p[s[j]];
}
size_t exact_rank(uint8_t *mat,size_t h,size_t w,const uint8_t *tab,const uint8_t *inv,
                  uint32_t *rows,uint32_t *cols,uint8_t *diag) {
    for(size_t i=0;i<h;i++)rows[i]=(uint32_t)i;
    size_t rank=0;
    for(size_t c=0;c<w && rank<h;c++) {
        size_t k=rank;
        while(k<h && mat[(size_t)rows[k]*w+c]==0)k++;
        if(k==h)continue;
        uint32_t tmp=rows[rank];rows[rank]=rows[k];rows[k]=tmp;
        uint8_t *pivot=mat+(size_t)rows[rank]*w;
        uint8_t z=inv[pivot[c]];
        cols[rank]=(uint32_t)c;diag[rank]=pivot[c];
        for(size_t i=rank+1;i<h;i++) {
            uint8_t *dst=mat+(size_t)rows[i]*w;
            uint8_t q=tab[64*z+dst[c]];
            if(q)add_multiple(dst+c,pivot+c,w-c,tab+64*q);
        }
        rank++;
    }
    return rank;
}
