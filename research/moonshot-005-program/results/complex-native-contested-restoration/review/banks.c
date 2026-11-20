#include <stdint.h>
#include <stdlib.h>
#include <stddef.h>
#define P 65537u
static uint32_t inv(uint32_t x) {
    uint32_t v=1;
    for(unsigned e=P-2;e;e>>=1){if(e&1)v=(uint64_t)v*x%P;x=(uint64_t)x*x%P;}
    return v;
}
size_t rank_mod(uint32_t *a,size_t n,size_t m) {
    size_t r=0;
    for(size_t c=0;c<m && r<n;c++){
        size_t k=r;while(k<n && !a[k*m+c])k++;
        if(k==n)continue;
        for(size_t j=c;j<m;j++){uint32_t v=a[r*m+j];a[r*m+j]=a[k*m+j];a[k*m+j]=v;}
        uint32_t *v=a+r*m,iv=inv(v[c]);
        for(size_t i=r+1;i<n;i++){
            uint32_t *u=a+i*m,q=(uint64_t)iv*u[c]%P;
            if(!q)continue;
            for(size_t j=c;j<m;j++)u[j]=(u[j]+(uint64_t)(P-q)*v[j])%P;
        }
        r++;
    }
    return r;
}
