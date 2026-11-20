#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>
#ifdef __AVX512VBMI__
#include <immintrin.h>
#endif
static int rankq(uint8_t a[134][192],const uint8_t*m,const uint8_t*iv){
 int r=0;
 for(int c=0;c<130;c++){int p=r;while(p<134&&!a[p][c])p++;if(p==134)continue;
 if(p!=r){for(int q=0;q<192;q++){uint8_t t=a[p][q];a[p][q]=a[r][q];a[r][q]=t;}}
 for(int i=r+1;i<134;i++){uint8_t v=m[64*a[i][c]+iv[a[r][c]]];if(!v)continue;const uint8_t*tab=m+64*v;
#ifdef __AVX512VBMI__
 __m512i t=_mm512_loadu_si512(tab);for(int z=c/64;z<3;z++){__m512i x=_mm512_loadu_si512(a[r]+64*z),y=_mm512_loadu_si512(a[i]+64*z);_mm512_storeu_si512(a[i]+64*z,_mm512_xor_si512(y,_mm512_permutexvar_epi8(x,t)));}
#else
 for(int z=c;z<130;z++)a[i][z]^=tab[a[r][z]];
#endif
 }r++;}return r;}
void allpair(const uint8_t*M,const uint8_t*m,const uint8_t*v,int n,int threads,uint64_t*h){
 omp_set_num_threads(threads);
 #pragma omp parallel
 {uint8_t a[134][192];uint64_t local[131]={0};
 #pragma omp for schedule(dynamic,8)
 for(int i=0;i<n;i++)for(int j=0;j<i;j++){
 const uint8_t*x=M+(size_t)i*134*130,*y=M+(size_t)j*134*130;for(int r=0;r<134;r++){for(int t=0;t<130;t++)a[r][t]=x[130*r+t]^y[130*r+t];memset(a[r]+130,0,62);}local[rankq(a,m,v)]++;}
 #pragma omp critical
 {for(int r=0;r<=130;r++)h[r]+=local[r];}}}
