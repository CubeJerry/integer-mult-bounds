#include "field.c"
size_t screen_deltas(const uint8_t *mat,size_t count,size_t h,size_t w,const uint8_t *table,const uint8_t *inv,size_t group,size_t groups,uint64_t *hist){
 uint8_t *a=malloc(h*w);uint32_t *rows=malloc(h*sizeof(uint32_t)),*cols=malloc(w*sizeof(uint32_t));size_t n=0;
 for(size_t i=group;i<count;i+=groups)for(size_t j=0;j<i;j++){
   const uint8_t *x=mat+i*h*w,*y=mat+j*h*w;for(size_t k=0;k<h*w;k++)a[k]=x[k]^y[k];size_t r=ordered_rank(a,h,w,table,inv,rows,cols);hist[r]++;n++;
 }free(a);free(rows);free(cols);return n;
}
