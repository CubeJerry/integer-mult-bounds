/* Streaming GF(64) column elimination. Incoming columns are converted to
   the reciprocal polynomial basis before reduction. */
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>
#if defined(__GFNI__) && defined(__AVX512BW__)
#include <immintrin.h>
#endif

typedef struct {
    uint8_t m[64][64], inv[64];
    uint64_t binary[64];
} Field;

typedef struct {
    size_t width, rank, seen;
    uint32_t *selected;
    uint8_t **basis, determinant;
} Echelon;

static Field direct, reciprocal;
static uint8_t encode[64], decode[64];

static uint8_t mult(uint8_t a, uint8_t b, unsigned poly) {
    unsigned x=a, y=b, z=0;
    while(y) {
        if(y&1u) z^=x;
        x<<=1;
        if(x&64u) x^=poly;
        y>>=1;
    }
    return (uint8_t)z;
}

static void make_field(Field *f,unsigned poly) {
    for(unsigned x=0;x<64;x++) {
        for(unsigned y=0;y<64;y++) {
            f->m[x][y]=mult(x,y,poly);
            if(f->m[x][y]==1) f->inv[x]=(uint8_t)y;
        }
        uint64_t bin=0;
        for(unsigned b=0;b<6;b++)
            for(unsigned k=0;k<6;k++)
                if(f->m[x][1u<<b]&(1u<<k))
                    bin |= (uint64_t)1 << (8*(7-k)+b);
        f->binary[x]=bin;
    }
}

static inline void add_multiple(const Field *f,uint8_t *dst,const uint8_t *src,size_t len,uint8_t q) {
    size_t j=0;
#if defined(__GFNI__) && defined(__AVX512BW__)
    const __m512i op=_mm512_set1_epi64((long long)f->binary[q]);
    for(;j+64<=len;j+=64) {
        __m512i val=_mm512_loadu_si512(src+j);
        val=_mm512_gf2p8affine_epi64_epi8(val,op,0);
        _mm512_storeu_si512(dst+j,_mm512_xor_si512(val,_mm512_loadu_si512(dst+j)));
    }
#endif
    const uint8_t *tab=f->m[q];
    for(;j<len;j++) dst[j]^=tab[src[j]];
}

int init_field(void) {
    make_field(&direct,0x43);make_field(&reciprocal,0x61);
    uint8_t reciprocal_generator=reciprocal.inv[2];
    for(unsigned v=0;v<64;v++) {
        uint8_t z=0;
        for(int k=5;k>=0;k--)
            z=reciprocal.m[z][reciprocal_generator]^((v>>k)&1u);
        encode[v]=z;decode[z]=(uint8_t)v;
    }
    uint8_t src[64],dst[64];
    for(unsigned x=0;x<64;x++)src[x]=(uint8_t)x;
    for(unsigned x=0;x<64;x++) {
        if(decode[encode[x]]!=x) return 0;
        memset(dst,0,64);add_multiple(&direct,dst,src,64,(uint8_t)x);
        for(unsigned y=0;y<64;y++)
            if(dst[y]!=direct.m[x][y]||encode[direct.m[x][y]]!=reciprocal.m[encode[x]][encode[y]]) return 0;
        memset(dst,0,64);add_multiple(&reciprocal,dst,src,64,(uint8_t)x);
        for(unsigned y=0;y<64;y++) if(dst[y]!=reciprocal.m[x][y])return 0;
    }
    return 1;
}

void multiply_direct(const uint8_t *a,const uint8_t *b,uint8_t *out,size_t h,size_t inner,size_t w) {
    memset(out,0,h*w);
    for(size_t r=0;r<h;r++)
        for(size_t k=0;k<inner;k++) {
            uint8_t z=a[r*inner+k];
            if(z)add_multiple(&direct,out+r*w,b+k*w,w,z);
        }
}

Echelon *begin(size_t n) {
    Echelon *s=calloc(1,sizeof(*s));
    if(!s)return NULL;
    s->width=n;s->determinant=1;s->basis=calloc(n,sizeof(*s->basis));s->selected=calloc(n,sizeof(*s->selected));
    if(!s->basis||!s->selected){free(s->basis);free(s->selected);free(s);return NULL;}
    return s;
}

/* One independent input column is one row in the transposed linear system.
   Batching keeps each resident pivot hot across several new columns. */
int consume(Echelon *s,const uint8_t *rows,size_t count) {
    size_t n=s->width;
    uint8_t *work=malloc(count*n), *alive=malloc(count);
    if(!work||!alive){free(work);free(alive);return 0;}
    memset(alive,1,count);
    for(size_t j=0;j<count*n;j++) work[j]=encode[rows[j]];
    for(size_t p=0;p<n;p++) {
        uint8_t *v=s->basis[p];
        if(!v) {
            size_t t=0;
            while(t<count && (!alive[t]||!work[t*n+p]))t++;
            if(t==count)continue;
            uint8_t *r=work+t*n, z=r[p];
            v=malloc(n-p);
            if(!v){free(work);free(alive);return 0;}
            for(size_t j=p;j<n;j++)v[j-p]=reciprocal.m[reciprocal.inv[z]][r[j]];
            s->selected[s->rank]=(uint32_t)(s->seen+t);
            s->basis[p]=v;s->rank++;
            s->determinant=reciprocal.m[s->determinant][z];alive[t]=0;
        }
        for(size_t t=0;t<count;t++) {
            if(!alive[t])continue;
            uint8_t *r=work+t*n+p;
            if(*r)add_multiple(&reciprocal,r,v,n-p,*r);
        }
    }
    s->seen+=count;free(work);free(alive);return 1;
}

size_t present_rank(const Echelon *s) {return s->rank;}
uint8_t determinant(const Echelon *s) {return s->rank==s->width?decode[s->determinant]:0;}
void pivot_columns(const Echelon *s,uint32_t *out) {memcpy(out,s->selected,s->rank*sizeof(*out));}
void finish(Echelon *s) {
    for(size_t i=0;i<s->width;i++)free(s->basis[i]);
    free(s->basis);free(s->selected);free(s);
}

void scale_add_direct(uint8_t *dst,const uint8_t *src,size_t len,uint8_t coefficient) {
    add_multiple(&direct,dst,src,len,coefficient);
}

/* Binary ADD invoice for the finite word reducing a GF(64) local matrix
   to identity and applying the final scalar. Axes within each field use
   the six polynomial-basis bits. */
static unsigned binary_scalar(uint8_t q) {
    if(!q)return 0;
    uint8_t a[6]={0,0,0,0,0,0};
    for(unsigned c=0;c<6;c++) for(unsigned r=0;r<6;r++)
        if(direct.m[q][1u<<c]&(1u<<r))a[r]|=1u<<c;
    unsigned cost=0;
    for(unsigned c=0;c<6;c++) {
        unsigned s=c;
        while(s<6 && !(a[s]&(1u<<c)))s++;
        if(s==6)return 9999;
        if(s!=c){uint8_t z=a[s];a[s]=a[c];a[c]=z;cost+=3;}
        for(unsigned r=0;r<6;r++)if(r!=c && (a[r]&(1u<<c))){a[r]^=a[c];cost++;}
    }
    return cost;
}

uint64_t gauge_invoice(const uint8_t *input,size_t n,uint8_t scalar) {
    uint8_t *a=malloc(n*n);
    if(!a)return UINT64_MAX;
    memcpy(a,input,n*n);
    unsigned weight[64],scale[64];
    for(unsigned q=0;q<64;q++) {
        scale[q]=binary_scalar((uint8_t)q);weight[q]=0;
        for(unsigned k=0;k<6;k++)weight[q]+=(unsigned)__builtin_popcount(direct.m[q][1u<<k]);
    }
    uint64_t total=n*scale[scalar];
    for(size_t j=0;j<n;j++) {
        size_t s=j;
        while(s<n && !a[s*n+j])s++;
        if(s==n){free(a);return UINT64_MAX;}
        if(s!=j){
            for(size_t c=0;c<n;c++){uint8_t z=a[s*n+c];a[s*n+c]=a[j*n+c];a[j*n+c]=z;}
            total+=18;
        }
        uint8_t *row=a+j*n, z=direct.inv[row[j]];
        if(z!=1){for(size_t c=j;c<n;c++)row[c]=direct.m[z][row[c]];total+=scale[z];}
        for(size_t r=0;r<n;r++)if(r!=j) {
            uint8_t *cur=a+r*n,q=cur[j];
            if(q){add_multiple(&direct,cur+j,row+j,n-j,q);total+=weight[q];}
        }
    }
    for(size_t row=0;row<n;row++)for(size_t col=0;col<n;col++)
        if(a[row*n+col]!=(row==col)){free(a);return UINT64_MAX;}
    free(a);return total;
}

int quotient(Echelon *s,const uint8_t *rows,size_t count,uint8_t *out) {
    size_t w=s->width, free_width=w-s->rank;
    uint8_t *work=malloc(w*count);
    if(!work)return 0;
    for(size_t i=0;i<w*count;i++)work[i]=encode[rows[i]];
    size_t pos=0;
    for(size_t p=0;p<w;p++) {
        const uint8_t *basis=s->basis[p];
        if(basis){
            for(size_t r=0;r<count;r++)if(work[r*w+p])
                add_multiple(&reciprocal,work+r*w+p,basis,w-p,work[r*w+p]);
        }else{
            for(size_t r=0;r<count;r++)out[r*free_width+pos]=decode[work[r*w+p]];
            pos++;
        }
    }
    free(work);return pos==free_width;
}

int inverse_direct(const uint8_t *src,size_t n,uint8_t *inv) {
    size_t w=2*n;uint8_t *a=calloc(n,w);
    if(!a)return 0;
    for(size_t i=0;i<n;i++){memcpy(a+i*w,src+i*n,n);a[i*w+n+i]=1;}
    for(size_t c=0;c<n;c++) {
        size_t r=c;
        while(r<n && !a[r*w+c])r++;
        if(r==n){free(a);return 0;}
        if(r!=c)for(size_t j=c;j<w;j++){uint8_t x=a[r*w+j];a[r*w+j]=a[c*w+j];a[c*w+j]=x;}
        uint8_t *pivot=a+c*w;uint8_t q=direct.inv[pivot[c]];
        if(q!=1)for(size_t j=c;j<w;j++)pivot[j]=direct.m[q][pivot[j]];
        for(size_t i=0;i<n;i++)if(i!=c && a[i*w+c])add_multiple(&direct,a+i*w+c,pivot+c,w-c,a[i*w+c]);
    }
    for(size_t i=0;i<n;i++)memcpy(inv+i*n,a+i*w+n,n);
    free(a);return 1;
}
