#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#if defined(__AVX2__)
#include <immintrin.h>
#endif

/* All byte entries are field labels below 64. Arguments are checked by Python. */
static void addmul(uint8_t *out,const uint8_t *in,const uint8_t *table,size_t n){
    size_t k=0;
#if defined(__AVX2__)
    uint8_t tmp[16]={0,table[16],table[32],table[48]};
    const __m256i lo=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i*)table));
    const __m256i hi=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i*)tmp));
    const __m256i mask=_mm256_set1_epi8(15);
    for(;k+32<=n;k+=32){
        __m256i x=_mm256_loadu_si256((const __m256i*)(in+k));
        __m256i a=_mm256_shuffle_epi8(lo,_mm256_and_si256(x,mask));
        __m256i b=_mm256_shuffle_epi8(hi,_mm256_and_si256(_mm256_srli_epi16(x,4),mask));
        __m256i dst=_mm256_loadu_si256((const __m256i*)(out+k));
        _mm256_storeu_si256((__m256i*)(out+k),_mm256_xor_si256(dst,_mm256_xor_si256(a,b)));
    }
#endif
    for(;k<n;k++)out[k]^=table[in[k]];
}

int gf_eliminate(uint8_t *a,int rows,int cols,int width,int both,const uint8_t *prod,const uint8_t *inverse){
    int r=0;
    for(int c=0;c<cols && r<rows;c++){
        int pivot=r;while(pivot<rows && !a[pivot*width+c])pivot++;
        if(pivot==rows)continue;
        uint8_t *v=a+r*width;
        if(pivot!=r){uint8_t *p=a+pivot*width;for(int k=0;k<width;k++){uint8_t t=v[k];v[k]=p[k];p[k]=t;}}
        uint8_t inv=inverse[v[c]];
        if(inv!=1){const uint8_t *tab=prod+64*inv;for(int k=c;k<width;k++)v[k]=tab[v[k]];}
        for(int z=both?0:r+1;z<rows;z++){
            uint8_t *p=a+z*width;const uint8_t t=p[c];
            if(z!=r && t)addmul(p+c,v+c,prod+64*t,width-c);
        }
        r++;
    }
    return r;
}
