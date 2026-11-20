#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <vector>
#if defined(__PCLMUL__) || (defined(__AVX512F__) && defined(__AVX512BW__) && defined(__VPCLMULQDQ__))
#include <immintrin.h>
#endif
#if defined(__AVX512F__) && defined(__AVX512BW__) && defined(__VPCLMULQDQ__)
#define NATIVE_PACKED_E24 1
#endif
using W=std::uint32_t;
constexpr std::uint64_t mask=(1u<<24)-1;
static inline std::uint64_t lowpoly(std::uint64_t a) {return a^(a<<1)^(a<<3)^(a<<4);}
static inline W mul(W a,W b) {
#if defined(__PCLMUL__)
    __m128i aa=_mm_cvtsi64_si128(a),bb=_mm_cvtsi64_si128(b);
    std::uint64_t p=_mm_cvtsi128_si64(_mm_clmulepi64_si128(aa,bb,0));
#else
    std::uint64_t p=0, term=a;
    while (b) {
        if (b&1u) p^=term;
        term<<=1;
        b>>=1;
    }
#endif
    std::uint64_t z=(p&mask)^lowpoly(p>>24);
    return static_cast<W>((z&mask)^lowpoly(z>>24));
}
static inline W inverse(W a) {
    W n=0xfffffe,result=1;
    while(n) {if(n&1)result=mul(result,a);a=mul(a,a);n>>=1;}
    return result;
}
#if defined(NATIVE_PACKED_E24)
static inline __m512i lowvec(__m512i a) {
    __m512i r=_mm512_ternarylogic_epi64(a,_mm512_slli_epi64(a,1),_mm512_slli_epi64(a,3),0x96);
    return _mm512_xor_si512(r,_mm512_slli_epi64(a,4));
}
static inline __m256i vmul(__m256i s,W coef) {
    auto a=_mm512_cvtepu32_epi64(s),b=_mm512_set1_epi64(coef),maskv=_mm512_set1_epi64(mask);
    auto even=_mm512_clmulepi64_epi128(a,b,0x00),odd=_mm512_clmulepi64_epi128(a,b,0x11);
    auto pp=_mm512_mask_blend_epi64(0xaa,even,_mm512_bslli_epi128(odd,8));
    auto z=_mm512_xor_si512(_mm512_and_si512(pp,maskv),lowvec(_mm512_srli_epi64(pp,24)));
    z=_mm512_xor_si512(_mm512_and_si512(z,maskv),lowvec(_mm512_srli_epi64(z,24)));
    return _mm512_cvtepi64_epi32(z);
}
#endif
static inline void update(W* dest,const W* source,std::size_t n,W k,bool add=true) {
    std::size_t i=0;
#if defined(NATIVE_PACKED_E24)
    for(;i+8<=n;i+=8) {
        auto x=vmul(_mm256_loadu_si256((const __m256i*)(source+i)),k);
        if(add)x=_mm256_xor_si256(x,_mm256_loadu_si256((const __m256i*)(dest+i)));
        _mm256_storeu_si256((__m256i*)(dest+i),x);
    }
#endif
    for(;i<n;++i) {W z=mul(source[i],k);dest[i]=add?(dest[i]^z):z;}
}
extern "C" void mm24(const W* a,const W* b,W* dst,std::size_t rows,std::size_t common,std::size_t cols) {
    std::fill(dst,dst+rows*cols,0);
    for(std::size_t i=0;i<rows;++i)for(std::size_t k=0;k<common;++k){W coef=a[i*common+k];if(coef)update(dst+i*cols,b+k*cols,cols,coef);}
}
extern "C" std::size_t rank24(W* a,std::size_t rows,std::size_t cols,W* row_ids,W* pivots) {
    for(std::size_t i=0;i<rows;++i)row_ids[i]=i;
    std::size_t r=0;
    for(std::size_t c=0;c<cols && r<rows;++c) {
        std::size_t u=r;while(u<rows && a[row_ids[u]*cols+c]==0)++u;
        if(u==rows)continue;
        std::swap(row_ids[u],row_ids[r]);W* src=a+row_ids[r]*cols;W k=inverse(src[c]);
        pivots[r]=src[c];
        for(std::size_t i=r+1;i<rows;++i) {W* dst=a+row_ids[i]*cols;W coef=mul(dst[c],k);if(coef)update(dst+c,src+c,cols-c,coef);}
        ++r;
    }
    return r;
}
extern "C" int solve24(W* aug,std::size_t n,std::size_t cols) {
    std::size_t w=n+cols;
    for(std::size_t c=0;c<n;++c) {
        std::size_t u=c;while(u<n && aug[u*w+c]==0)++u;
        if(u==n)return 1;
        if(u!=c)std::swap_ranges(aug+u*w,aug+(u+1)*w,aug+c*w);
        W* src=aug+c*w;W k=inverse(src[c]);if(k!=1)update(src+c,src+c,w-c,k,false);
        for(std::size_t i=0;i<n;++i)if(i!=c) {W* dst=aug+i*w;W coef=dst[c];if(coef)update(dst+c,src+c,w-c,coef);}
    }
    return 0;
}
extern "C" void all_prices(const W* transforms,std::uint16_t* charge) {
    for(W a=0;a<(1u<<24);++a) {
        unsigned total=0;
        for(unsigned j=0;j<24;++j) {
            const W* lut=transforms+768*j;
            W bits=lut[a&255]^lut[256+((a>>8)&255)]^lut[512+(a>>16)];
            total+=__builtin_popcount(bits);
        }
        charge[a]=total;
    }
}
static inline W to_native(W p,const W* inverse_lut) {
    return inverse_lut[p&255]^inverse_lut[256+((p>>8)&255)]^inverse_lut[512+(p>>16)];
}
static unsigned scale_price(W s,const W* basis,const W* inverse_lut) {
    W rr[24]={};unsigned count=0;
    for(unsigned c=0;c<24;++c) {
        W out=to_native(mul(s,basis[c]),inverse_lut);
        for(unsigned r=0;r<24;++r)if ((out>>r)&1)rr[r]|=1u<<c;
    }
    for(unsigned c=0;c<24;++c) {
        if(((rr[c]>>c)&1)==0) {
            unsigned r=c+1;while (r<24 && (((rr[r]>>c)&1)==0))++r;
            if(r==24)return UINT32_MAX;std::swap(rr[r],rr[c]);count+=3;
        }
        for(unsigned r=0;r<24;++r)if(r!=c && ((rr[r]>>c)&1)){rr[r]^=rr[c];++count;}
    }
    return count;
}
extern "C" std::uint64_t price24(W *a,std::size_t n,const std::uint16_t* charge,const W* basis,const W* inverse_lut,std::uint64_t* stats) {
    std::uint64_t total=0;
    for(std::size_t c=0;c<n;++c) {
        std::size_t u=c;while(u<n && a[u*n+c]==0)++u;if(u==n)return UINT64_MAX;
        if(u!=c){std::swap_ranges(a+c*n,a+(c+1)*n,a+u*n);total+=72;++stats[0];}
        W* src=a+c*n;W k=inverse(src[c]);
        if(k!=1){unsigned p=scale_price(k,basis,inverse_lut);if(p==UINT32_MAX)return UINT64_MAX;total+=p;update(src+c,src+c,n-c,k,false);++stats[1];}
        for(std::size_t r=0;r<n;++r)if(r!=c) {
            W* dst=a+r*n;W coeff=dst[c];if(coeff){total+=charge[coeff];update(dst+c,src+c,n-c,coeff);++stats[2];}
        }
    }
    return total;
}
