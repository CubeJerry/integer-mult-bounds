#include "field_rank.c"
#include <stdlib.h>
#include <string.h>
size_t right_kernel(uint8_t *A,size_t m,size_t n,const uint8_t *prod,const uint8_t *inv,uint8_t *out) {
    uint32_t *rows=malloc(m*sizeof(*rows)),*cols=malloc((n+1)*sizeof(*cols));uint8_t *diag=malloc(n+1),*pivot=calloc(n,1);
    if (!rows||!cols||!diag||!pivot) return n+1;
    size_t rank=exact_rank(A,m,n,prod,inv,rows,cols,diag),d=n-rank;memset(out,0,n*d);
    for(size_t i=0;i<rank;i++)pivot[cols[i]]=1;
    size_t s=0;for(size_t j=0;j<n;j++)if(!pivot[j])out[j*d+s++]=1;
    for(size_t k=rank;k>0;k--) {
        size_t i=k-1,p=cols[i];uint8_t *q=out+p*d;const uint8_t *r=A+(size_t)rows[i]*n;
        for(size_t j=p+1;j<n;j++)if(r[j])add_multiple(q,out+j*d,d,prod+64*r[j]);
        const uint8_t *scale=prod+64*inv[diag[i]];for(size_t j=0;j<d;j++)q[j]=scale[q[j]];
    }
    free(rows);free(cols);free(diag);free(pivot);return d;
}
