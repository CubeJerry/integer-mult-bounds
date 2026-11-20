/* In-place blocked exact forward elimination over the supplied 64-element field. */
#include "finite_rank.c"
#include <stdio.h>
#ifdef _OPENMP
#include <omp.h>
#endif

#if defined(__AVX512VBMI__)
/* Four independent destination rows keep four 64-byte column segments in registers. */
static inline void update_four(uint8_t *base,const uint8_t *factors,int cols,int panel,
        int top,int first,int from,int count,const uint8_t *product) {
    __m512i sum[4][4];
    for(int r=0;r<4;r++)
        for(int t=0;t<4;t++)sum[r][t]=_mm512_loadu_si512(base+(size_t)(first+r)*cols+from+64*t);
    for(int k=0;k<count;k++){
        __m512i tab[4];
        for(int r=0;r<4;r++)tab[r]=_mm512_loadu_si512(product+64*factors[(size_t)(first+r)*panel+k]);
        for(int t=0;t<4;t++){
            __m512i v=_mm512_loadu_si512(base+(size_t)(top+k)*cols+from+64*t);
            for(int r=0;r<4;r++)
                sum[r][t]=_mm512_xor_si512(sum[r][t],_mm512_permutexvar_epi8(v,tab[r]));
        }
    }
    for(int r=0;r<4;r++)
        for(int t=0;t<4;t++)_mm512_storeu_si512(base+(size_t)(first+r)*cols+from+64*t,sum[r][t]);
}
#endif

int native_augmented_rank(uint8_t *A,int rows,int cols,int limit,const uint8_t *mul,const uint8_t *inverse,int panel,int threads) {
    if(panel<1||threads<1)return -1;
    uint8_t *L=malloc((size_t)rows*panel);
    if(!L)return -1;
    int rank=0;
    #ifdef _OPENMP
    omp_set_num_threads(threads);
    #endif
    for(int start=0;start<limit && rank<rows;start+=panel){
        if(getenv("NATIVE_RANK_PROGRESS") && start%(20*panel)==0){fprintf(stderr,"native rank panel %d/%d\n",start,limit);fflush(stderr);}
        int stop=start+panel<limit?start+panel:limit,top=rank;
        memset(L+(size_t)rank*panel,0,(size_t)(rows-rank)*panel);
        for(int c=start;c<stop&&rank<rows;c++){
            int p=rank;while(p<rows && A[(size_t)p*cols+c]==0)p++;
            if(p==rows)continue;
            uint8_t *pivot=A+(size_t)rank*cols;
            uint8_t *factors=L+(size_t)rank*panel;
            if(p!=rank){
                uint8_t *other=A+(size_t)p*cols;
                for(int t=start;t<cols;t++){uint8_t x=pivot[t];pivot[t]=other[t];other[t]=x;}
                other=L+(size_t)p*panel;
                for(int t=0;t<rank-top;t++){uint8_t x=factors[t];factors[t]=other[t];other[t]=x;}
            }
            for(int k=0;k<rank-top;k++)if(factors[k]){
                const uint8_t *basis=A+(size_t)(top+k)*cols;
                addmul(pivot+stop,basis+stop,mul+64*factors[k],cols-stop);
            }
            uint8_t inv=inverse[pivot[c]];const uint8_t *scale=mul+64*inv;
            if(inv!=1)for(int t=c;t<cols;t++)pivot[t]=scale[pivot[t]];
            for(int i=rank+1;i<rows;i++){
                uint8_t *tgt=A+(size_t)i*cols;uint8_t w=tgt[c];
                if(w){L[(size_t)i*panel+rank-top]=w;addmul(tgt+c,pivot+c,mul+64*w,stop-c);}
            }
            rank++;
        }
        int pivots=rank-top;
        if(!pivots || stop==cols)continue;
        /* A tile holds a segment of all pivot rows and output rows under one L2 working set. */
        int tile=256;
        #pragma omp parallel for schedule(static) collapse(2)
        for(int blockrow=0;blockrow<(rows-rank+47)/48;blockrow++){
            for(int blockcol=0;blockcol<(cols-stop+tile-1)/tile;blockcol++){
                int from=stop+tile*blockcol,nn=cols-from;
                if(nn>tile)nn=tile;
                int first=rank+48*blockrow,last=first+48;
                if(last>rows)last=rows;
                int i=first;
                #if defined(__AVX512VBMI__)
                if(nn==256)for(;i+4<=last;i+=4)update_four(A,L,cols,panel,top,i,from,pivots,mul);
                #endif
                for(;i<last;i++){
                    uint8_t *dst=A+(size_t)i*cols+from;
                    const uint8_t *l=L+(size_t)i*panel;
                    for(int k=0;k<pivots;k++)if(l[k])
                        addmul(dst,A+(size_t)(top+k)*cols+from,mul+64*l[k],nn);
                }
            }
        }
    }
    free(L);return rank;
}

int native_block_rank(uint8_t *A,int n,int m,const uint8_t *table,const uint8_t *inv,int b,int threads) {
    return native_augmented_rank(A,n,m,m,table,inv,b,threads);
}
