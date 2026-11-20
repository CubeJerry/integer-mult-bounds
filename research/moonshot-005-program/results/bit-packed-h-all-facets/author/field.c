#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#ifdef __AVX2__
#include <immintrin.h>
#endif
static void sax(uint8_t *dst, const uint8_t *src, size_t n, const uint8_t *lut, int add) {
  size_t t=0;
#ifdef __AVX2__
  __m256i lo=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i*)lut));
  uint8_t hh[16]={0,lut[16],lut[32],lut[48]};
  __m256i hi=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i*)hh));__m256i mask=_mm256_set1_epi8(15);
  for(;t+32<=n;t+=32){
    __m256i x=_mm256_loadu_si256((const __m256i*)(src+t));
    __m256i z=_mm256_xor_si256(_mm256_shuffle_epi8(lo,_mm256_and_si256(x,mask)),_mm256_shuffle_epi8(hi,_mm256_and_si256(_mm256_srli_epi16(x,4),mask)));
    if(add)z=_mm256_xor_si256(z,_mm256_loadu_si256((const __m256i*)(dst+t)));
    _mm256_storeu_si256((__m256i*)(dst+t),z);
  }
#endif
  for(;t<n;t++){uint8_t z=lut[src[t]];if(add)dst[t]^=z;else dst[t]=z;}
}
int invert(uint8_t *m,size_t n, const uint8_t *t,const uint8_t *inv) {
  const size_t w=2*n;
  for(size_t c=0;c<n;c++){
    size_t p=c;
    while(p<n && !m[p*w+c])p++;
    if(p==n)return 0;
    if(p!=c)for(size_t x=c;x<w;x++){uint8_t a=m[p*w+x];m[p*w+x]=m[c*w+x];m[c*w+x]=a;}
    uint8_t *pivot=m+c*w;
    if(pivot[c]!=1)sax(pivot+c,pivot+c,w-c,t+64*inv[pivot[c]],0);
    for(size_t r=0;r<n;r++)if(r!=c && m[r*w+c])sax(m+r*w+c,pivot+c,w-c,t+64*m[r*w+c],1);
  }
  return 1;
}
int field_rank(uint8_t*m,int h,int w,const uint8_t*tab,const uint8_t*inv){
 int k=0;
 for(int c=0;c<w&&k<h;c++){
   int q=k;while(q<h&&!m[q*w+c])q++;
   if(q==h)continue;
   if(q!=k)for(int u=c;u<w;u++){uint8_t t=m[q*w+u];m[q*w+u]=m[k*w+u];m[k*w+u]=t;}
   uint8_t*s=m+k*w;uint8_t v=inv[s[c]];
   for(int r=k+1;r<h;r++)if(m[r*w+c])sax(m+r*w+c,s+c,w-c,tab+64*tab[v*64+m[r*w+c]],1);
   ++k;
 }
 return k;
}

int field_pivots(uint8_t*m,int h,int w,const uint8_t*tab,const uint8_t*inv,int*out){
 int k=0;
 for(int c=0;c<w&&k<h;c++){
   int q=k;while(q<h&&!m[q*w+c])q++;
   if(q==h)continue;
   if(q!=k)for(int u=c;u<w;u++){uint8_t t=m[q*w+u];m[q*w+u]=m[k*w+u];m[k*w+u]=t;}
   uint8_t*s=m+k*w;uint8_t v=inv[s[c]];
   for(int r=k+1;r<h;r++)if(m[r*w+c])sax(m+r*w+c,s+c,w-c,tab+64*tab[v*64+m[r*w+c]],1);
   out[k]=c;++k;
 }
 return k;
}
