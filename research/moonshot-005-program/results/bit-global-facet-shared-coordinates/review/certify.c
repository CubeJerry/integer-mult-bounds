/* Reversible field reduction: the table labels GF(64), the costs are six-bit ADD counts. */
#include "finite_rank.c"
uint64_t cert_reduce(uint8_t *a,int h,int w,int total,int all,int *piv,const uint8_t *prod,const uint8_t *inv,const int *weight,const int *scale,int *out_rank) {
    int t=0;uint64_t cost=0;
    for(int c=0;c<w && t<h;c++){
        int q=t;while(q<h && !a[q*total+c])q++;
        if(q==h)continue;
        if(q!=t){
            for(int z=0;z<total;z++){uint8_t v=a[q*total+z];a[q*total+z]=a[t*total+z];a[t*total+z]=v;}
            cost+=18;
        }
        uint8_t *v=a+t*total;uint8_t alpha=inv[v[c]];
        if(alpha!=1){for(int z=c;z<total;z++)v[z]=prod[64*alpha+v[z]];cost+=scale[alpha];}
        for(int q=all?0:t+1;q<h;q++)if(q!=t){
            uint8_t *u=a+q*total;int z=u[c];
            if(z){addmul(u+c,v+c,prod+64*z,total-c);cost+=weight[z];}
        }
        piv[t++]=c;
    }
    *out_rank=t;return cost;
}
