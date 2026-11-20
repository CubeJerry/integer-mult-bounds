#include "field_rank.c"

/* Solve A Z = S over the native field. The mutable augmented array has n by
   (n+b) scalar entries. Reject failure to obtain all n original pivots. */
int solve_many(uint8_t *aug, size_t n, size_t b, const uint8_t *tab,
               const uint8_t *inv, uint32_t *rows, uint32_t *cols, uint8_t *diag,
               uint8_t *out) {
    size_t pitch=n+b;
    size_t rank=exact_rank(aug,n,pitch,tab,inv,rows,cols,diag);
    if(rank!=n) return -1;
    for(size_t i=0;i<n;i++) if(cols[i]!=i) return -2;
    for(size_t ii=n;ii>0;ii--){
        size_t i=ii-1;
        const uint8_t *row=aug+(size_t)rows[i]*pitch;
        uint8_t *dest=out+i*b;
        for(size_t c=0;c<b;c++) dest[c]=row[n+c];
        for(size_t j=i+1;j<n;j++) if(row[j])
            add_multiple(dest,out+j*b,b,tab+64*row[j]);
        const uint8_t *scale=tab+64*inv[diag[i]];
        for(size_t c=0;c<b;c++) dest[c]=scale[dest[c]];
    }
    return 0;
}
