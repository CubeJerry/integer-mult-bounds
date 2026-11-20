/* Finite GF(64) matrix operations and reversible binary invoices. */
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#ifdef __AVX2__
#include <immintrin.h>
#endif

static void row_add(uint8_t *dest,const uint8_t *source,size_t length,const uint8_t *times){
    size_t j=0;
#ifdef __AVX2__
    const uint8_t high_values[16]={0,times[16],times[32],times[48]};
    __m256i low=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i*)times));
    __m256i high=_mm256_broadcastsi128_si256(_mm_loadu_si128((const __m128i*)high_values));
    __m256i mask=_mm256_set1_epi8(15);
    for(;j+32<=length;j+=32){
        __m256i x=_mm256_loadu_si256((const __m256i*)(source+j));
        __m256i v=_mm256_xor_si256(_mm256_shuffle_epi8(low,_mm256_and_si256(x,mask)),
                                    _mm256_shuffle_epi8(high,_mm256_and_si256(_mm256_srli_epi16(x,4),mask)));
        _mm256_storeu_si256((__m256i*)(dest+j),_mm256_xor_si256(v,_mm256_loadu_si256((const __m256i*)(dest+j))));
    }
#endif
    for(;j<length;j++)dest[j]^=times[source[j]];
}

size_t ordered_rank(uint8_t *matrix,size_t height,size_t width,const uint8_t *field,const uint8_t *inverse,
                    uint32_t *row_order,uint32_t *columns){
    for(size_t i=0;i<height;i++)row_order[i]=(uint32_t)i;
    size_t rank=0;
    for(size_t col=0;col<width && rank<height;col++){
        size_t chosen=rank;
        while(chosen<height && !matrix[row_order[chosen]*width+col])chosen++;
        if(chosen==height)continue;
        uint32_t tmp=row_order[chosen];row_order[chosen]=row_order[rank];row_order[rank]=tmp;
        uint8_t *pivot=matrix+row_order[rank]*width;uint8_t scale=inverse[pivot[col]];
        columns[rank]=(uint32_t)col;
        for(size_t i=rank+1;i<height;i++){
            uint8_t *dest=matrix+row_order[i]*width;uint8_t q=field[64*scale+dest[col]];
            if(q)row_add(dest+col,pivot+col,width-col,field+64*q);
        }
        rank++;
    }
    return rank;
}

static unsigned scalar_cost(unsigned coefficient,const uint8_t *field){
    unsigned rows[6]={0},total=0;
    for(unsigned c=0;c<6;c++)for(unsigned r=0;r<6;r++)
        if(field[64*coefficient+(1u<<c)]&(1u<<r))rows[r]|=1u<<c;
    for(unsigned c=0;c<6;c++){
        unsigned s=c;while(s<6 && !(rows[s]&(1u<<c)))s++;
        if(s==6)return 9999;
        if(s!=c){unsigned v=rows[c];rows[c]=rows[s];rows[s]=v;total+=3;}
        for(unsigned r=0;r<6;r++)if(r!=c && (rows[r]&(1u<<c))){rows[r]^=rows[c];total++;}
    }
    return total;
}

/* The input is [A|I]. Gauss-Jordan also gives a finite reversible invoice for A and its inverse. */
uint64_t invert_and_price(uint8_t *matrix,size_t n,const uint8_t *field,const uint8_t *inverse,uint8_t *output){
    size_t *rows=malloc(n*sizeof(*rows));if(!rows)return UINT64_MAX;
    unsigned weight[64],scale[64];
    for(unsigned q=0;q<64;q++){
        weight[q]=0;for(unsigned t=0;t<6;t++)weight[q]+=(unsigned)__builtin_popcount(field[64*q+(1u<<t)]);
        scale[q]=q?scalar_cost(q,field):0;
    }
    uint64_t total=0;
    for(size_t i=0;i<n;i++)rows[i]=i;
    for(size_t c=0;c<n;c++){
        size_t p=c;while(p<n && !matrix[rows[p]*2*n+c])p++;
        if(p==n){free(rows);return UINT64_MAX;}
        if(p!=c){size_t v=rows[c];rows[c]=rows[p];rows[p]=v;total+=18;}
        uint8_t *pivot=matrix+rows[c]*2*n;uint8_t q=inverse[pivot[c]];
        if(q!=1){for(size_t k=c;k<2*n;k++)pivot[k]=field[64*q+pivot[k]];total+=scale[q];}
        for(size_t i=0;i<n;i++)if(i!=c){
            uint8_t *dest=matrix+rows[i]*2*n;uint8_t factor=dest[c];
            if(factor){row_add(dest+c,pivot+c,2*n-c,field+64*factor);total+=weight[factor];}
        }
    }
    for(size_t i=0;i<n;i++){
        uint8_t *row=matrix+rows[i]*2*n;
        for(size_t j=0;j<n;j++)if(row[j]!=(uint8_t)(i==j)){free(rows);return UINT64_MAX;}
        memcpy(output+i*n,row+n,n);
    }
    free(rows);return total;
}
