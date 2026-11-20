#include <cstdint>
#include <algorithm>
#include <vector>
#include <cstring>
#if defined(__PCLMUL__) || defined(__VPCLMULQDQ__)
#include <immintrin.h>
#endif
using U=uint32_t;using V=uint64_t;constexpr U mask=0xffffff, f=0x1b00001, mu=0x1c71c70;
inline V cl(V a,V b){
#ifdef __PCLMUL__
    return _mm_cvtsi128_si64(_mm_clmulepi64_si128(_mm_cvtsi64_si128(a),_mm_cvtsi64_si128(b),0));
#else
    V value=0;
    while(b){if(b&1)value^=a;a<<=1;b>>=1;}
    return value;
#endif
}
inline U mul(U a,U b){V p=cl(a,b),q=cl(p>>23,mu)>>25;U r=(p^cl(q,f))&0x1ffffff;return r^((0u-(r>>24))&f);}
inline U inv(U x){U z=1;for(int i=0;i<24;i++){if(i)z=mul(z,x);x=mul(x,x);}return z;}
#if defined(__AVX512F__) && defined(__AVX512BW__) && defined(__VPCLMULQDQ__) && defined(__AVX2__)
inline __m512i cl8(__m512i a,__m512i b){
    __m512i even=_mm512_clmulepi64_epi128(a,b,0),odd=_mm512_clmulepi64_epi128(a,b,0x11);
    return _mm512_mask_blend_epi64(0xaa,even,_mm512_bslli_epi128(odd,8));
}
inline __m256i mul8(__m256i a,U b){
    __m512i p=cl8(_mm512_cvtepu32_epi64(a),_mm512_set1_epi64(b));
    __m512i q=_mm512_srli_epi64(cl8(_mm512_srli_epi64(p,23),_mm512_set1_epi64(mu)),25);
    __m512i r=_mm512_and_si512(_mm512_xor_si512(p,cl8(q,_mm512_set1_epi64(f))),_mm512_set1_epi64(0x1ffffff));
    __m512i high=_mm512_sub_epi64(_mm512_setzero_si512(),_mm512_srli_epi64(r,24));
    return _mm512_cvtepi64_epi32(_mm512_xor_si512(r,_mm512_and_si512(high,_mm512_set1_epi64(f))));
}
#endif
void ax(U*d,const U*s,size_t n,U b,bool add){
    size_t j=0;
#if defined(__AVX512F__) && defined(__AVX512BW__) && defined(__VPCLMULQDQ__) && defined(__AVX2__)
    for(;j+8<=n;j+=8){__m256i x=mul8(_mm256_loadu_si256((const __m256i*)(s+j)),b);
       if(add)x=_mm256_xor_si256(x,_mm256_loadu_si256((const __m256i*)(d+j)));
       _mm256_storeu_si256((__m256i*)(d+j),x);}
#endif
    for(;j<n;j++){U x=mul(s[j],b);d[j]=add?(d[j]^x):x;}
}
extern "C" U verify_mul(U a,U b){return mul(a,b);}
extern "C" size_t detrec(U*a,size_t h,size_t w,U*det){
    size_t k=0;U product=1;
    for(size_t t=0;t<w&&k<h;t++){
       size_t c=w-1-t,hit=k;while(hit<h && !a[hit*w+c])++hit;if(hit==h)continue;
       if(hit!=k)std::swap_ranges(a+k*w,a+(k+1)*w,a+hit*w);
       U*p=a+k*w;product=mul(product,p[c]);U iv=inv(p[c]);
       for(size_t r=k+1;r<h;r++){U*d=a+r*w;U z=mul(d[c],iv);if(z)ax(d,p,c+1,z,true);}
       k++;
    }
    *det=(h==w&&k==h)?product:0;return k;
}
inline U change(U x,const U*t){return t[x&255]^t[256+((x>>8)&255)]^t[512+(x>>16)];}
extern "C" void weightall(uint16_t*out,const U*rec2std,const U*std2limb,const uint8_t*wt){
   for(U x=0;x<=mask;x++){
      U z=change(x,rec2std);unsigned cost=0;
      for(int t=0;t<4;t++){
          U b=change(z,std2limb);cost+=wt[b&63]+wt[(b>>6)&63]+wt[(b>>12)&63]+wt[b>>18];
          z=((z<<1)&mask)^((0u-(z>>23))&27u);
      }
      out[x]=cost;
   }
}
inline unsigned scale(U s,const U*base,const U*rec2limb){
   U rows[24]={};unsigned count=0;
   for(int j=0;j<24;j++){
       U v=change(mul(s,base[j]),rec2limb);for(int k=0;k<24;k++)if((v>>k)&1)rows[k]^=1u<<j;
   }
   for(int j=0;j<24;j++){
       if(!((rows[j]>>j)&1)){int t=j+1;while(t<24 && !((rows[t]>>j)&1))t++;if(t==24)return UINT32_MAX;std::swap(rows[t],rows[j]);count+=3;}
       for(int t=0;t<24;t++)if(t!=j&&((rows[t]>>j)&1)){rows[t]^=rows[j];++count;}
   }
   return count;
}
extern "C" V price(U*A,size_t w,const uint16_t*cost,const U*base,const U*rec2limb){
   V total=0;
   for(size_t k=0;k<w;k++){
       size_t q=k;while(q<w&&!A[q*w+k])q++;if(q==w)return UINT64_MAX;
       if(q!=k){std::swap_ranges(A+k*w,A+(k+1)*w,A+q*w);total+=72;}
       U*p=A+k*w;U iv=inv(p[k]);if(iv!=1){total+=scale(iv,base,rec2limb);ax(p+k,p+k,w-k,iv,false);}
       for(size_t r=0;r<w;r++)if(r!=k){U*d=A+r*w;U v=d[k];if(v){total+=cost[v];ax(d+k,p+k,w-k,v,true);}}
   }
   return total;
}
