"""Read-only finite setup-cost census, not a physical runtime substitute.

Mirror the unchanged rational serializer and prepare_pages control order.
Count every exact rational reduction, product/division operand-bit rectangle,
binary-division digit traversal and sequential matrix record visit. These are
source-derived comparison metrics, not measured Tape actions or a new tariff.
No resulting page is supplied to a physical execution.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys

PACKAGE=Path(__file__).resolve().parent
ROOT=PACKAGE.parents[1]
sys.path.insert(0,str(PACKAGE))
from halo_core_sources import core_sources,load,need


def bits(x):return max(1,abs(x).bit_length())


class Bill:
    def __init__(self):self.c=Counter();self.stage='';self.rows=[]
    def product(self,x,y):
        self.c['products']+=1
        self.c['product_bit_rectangles']+=bits(x)*bits(y)
        self.c['maximum_operand_bits']=max(self.c['maximum_operand_bits'],bits(x),bits(y))
        return x*y
    def divide(self,x,y,kind):
        need(x>=0 and y>0,'positive source division')
        self.c['divisions']+=1;self.c[kind+'_divisions']+=1
        rect=bits(x)*bits(y)
        self.c['division_bit_rectangles']+=rect
        self.c[kind+'_division_bit_rectangles']+=rect
        q=r=0;visits=0
        for i in range(bits(x)-1,-1,-1):
            visits+=bits(q)+bits(r)
            q*=2;r=r*2+((x>>i)&1)
            visits+=max(bits(r),bits(y))
            if r>=y:
                visits+=max(bits(r),bits(y))+bits(q)
                r-=y;q+=1
        self.c['division_digit_visits']+=visits
        self.c[kind+'_division_digit_visits']+=visits
        need((q,r)==divmod(x,y),'binary division trace')
        return q,r
    def reduce(self,n,d):
        self.c['rational_reductions']+=1
        a,b=abs(n),d
        while b:
            _,r=self.divide(a,b,'gcd');a,b=b,r
        nn,rr=self.divide(abs(n),a,'exact_quotient');need(rr==0,'exact reduced numerator')
        dd,rr=self.divide(d,a,'exact_quotient');need(rr==0,'exact reduced denominator')
        return (-nn if n<0 else nn),dd
    def record(self,label,before):
        self.rows.append(dict(label=label,**{k:self.c[k]-before.get(k,0) for k in self.c
                                           if k!='maximum_operand_bits'}))


class Rational:
    def __init__(self,bill,n,d=1,reduce=False):
        need(d>0,'positive source denominator');self.bill=bill
        self.n,self.d=bill.reduce(n,d) if reduce else (n,d)
    @classmethod
    def from_q(cls,bill,q,reduce=False):return cls(bill,q.numerator,q.denominator,reduce)
    def copy(self):return Rational(self.bill,self.n,self.d)
    def value(self):return Q(self.n,self.d)
    def size(self):return 1+bits(self.n)+1+bits(self.d)+1
    def over(self,b):
        need(b.n!=0,'nonzero exact pivot');c=self.bill
        return Rational(c,c.product(abs(self.n),b.d)*(-1 if (self.n<0)!=(b.n<0) else 1),
                        c.product(self.d,abs(b.n)),True)
    def times(self,b):
        c=self.bill;return Rational(c,c.product(self.n,b.n),c.product(self.d,b.d),True)
    def minus(self,b):
        c=self.bill;x=c.product(self.n,b.d);y=c.product(b.n,self.d)
        c.c['signed_additions']+=1;c.c['signed_addition_width_sum']+=max(bits(x),bits(y))
        return Rational(c,x-y,c.product(self.d,b.d),True)
    def rounded(self,P):
        c=self.bill;c.c['roundings']+=1;c.c['shift_written_bits']+=bits(self.n)+P
        q,r=c.divide(abs(self.n)<<P,self.d,'rounding')
        return (-q if self.n<0 else q)


class Matrix:
    def __init__(self,bill,n,m,entry):
        self.bill=bill;self.n=n;self.m=m
        self.values=[entry(i,j).copy() for i in range(n) for j in range(m)]
        bill.c['matrix_record_written_cells']+=sum(x.size() for x in self.values)
    def get(self,i,j):
        need(0<=i<self.n and 0<=j<self.m,'source matrix index')
        at=i*self.m+j;self.bill.c['matrix_gets']+=1
        self.bill.c['matrix_scan_cells']+=2*sum(x.size() for x in self.values[:at+1])
        self.bill.c['matrix_record_written_cells']+=self.values[at].size()
        return self.values[at].copy()
    def set(self,i,j,value):
        at=i*self.m+j;old=sum(x.size() for x in self.values)
        self.values[at]=value.copy();new=sum(x.size() for x in self.values)
        self.bill.c['matrix_sets']+=1
        self.bill.c['matrix_scan_cells']+=2*old+new
        self.bill.c['matrix_record_written_cells']+=new
    def close(self):self.bill.c['matrix_cleared_cells']+=sum(x.size() for x in self.values)


def inverse(matrix):
    c=matrix.bill;n=matrix.n;need(n==matrix.m,'square source block')
    augmented=Matrix(c,n,2*n,lambda i,j:matrix.get(i,j) if j<n else Rational(c,int(i==j-n)))
    for k in range(n):
        pivot=augmented.get(k,k);need(pivot.n>0,'positive admitted source pivot')
        for j in range(2*n):
            previous=augmented.get(k,j)
            if previous.n:augmented.set(k,j,previous.over(pivot))
        for i in range(n):
            if i==k:continue
            factor=augmented.get(i,k)
            if not factor.n:continue
            for j in range(2*n):
                source=augmented.get(k,j)
                if not source.n:continue
                previous=augmented.get(i,j)
                augmented.set(i,j,previous.minus(factor.times(source)))
    result=Matrix(c,n,n,lambda i,j:augmented.get(i,j+n));augmented.close()
    original=[[matrix.values[i*n+j].value() for j in range(n)] for i in range(n)]
    output=[[result.values[i*n+j].value() for j in range(n)] for i in range(n)]
    need(all(sum(original[i][k]*output[k][j] for k in range(n))==int(i==j)
             for i in range(n) for j in range(n)),'independent exact inverse residual')
    return result


def pages(bill,data,block,P,label):
    n=len(data);before=bill.c.copy()
    source=Matrix(bill,n,n,lambda i,j:Rational.from_q(bill,data[i][j],True))
    bill.record(label+':serialize',before)
    padded=((n+block-1)//block)*block
    def entry(i,j):
        if label.endswith('upper'):i,j=padded-1-i,padded-1-j
        if i>=n or j>=n:return Rational(bill,int(i==j))
        return source.get(i,j)
    before=bill.c.copy()
    for i in range(padded):
        for j in range(padded):
            ib,jb=i//block,j//block
            if jb>ib or ib>jb+1:need(entry(i,j).n==0,'adjacent-block support admission')
    bill.record(label+':support',before)
    for index in range(padded//block):
        before=bill.c.copy();start=index*block
        matrix=Matrix(bill,block,block,lambda i,j:entry(start+i,start+j))
        result=inverse(matrix)
        bill.c['diagonal_inverse_blocks']+=1
        for i in range(block):
            for j in range(block):result.get(i,j).rounded(P)
        matrix.close();result.close()
        if index:
            for i in range(start,start+block):
                for j in range(start-block,start):entry(i,j).rounded(P)
        bill.record(label+':block:'+str(index),before)
    source.close()


def main():
    source=core_sources();results=[]
    with source.numerical() as runtime:
        from admitted_context import AdmittedPartition
        from prepared_join import build_numeric
        from core_layout import Layout
        forward=load('cost_forward_pages',source.FORWARD/'pages.py')
        for entry_bits in (64,40):
            ref=runtime.reference.Reference(runtime.raw,15,1,2,1,3,entry_bits)
            layout=Layout((4,),(0,),3)
            family=[[AdmittedPartition(runtime,ref,'narrow',layout.core_starts(c)[0],8,1,((7,),))]
                    for c in range(2)]
            programs,windows,actions,blocks,plan=build_numeric(runtime,family,
                target=2,initial_radius_bits=2,incoming=28)
            bill=Bill()
            for c in range(2):
                window=windows[c][0]
                for name in ('shear_lower','shear_upper','f_lower','f_upper'):
                    pages(bill,getattr(window,name),window.block,plan['P'],f'c{c}:{name}')
                for suffix,data in zip(('lower','upper'),forward.factors(actions[c][0],blocks[c][0],plan['P'])):
                    pages(bill,data,blocks[c][0],plan['P'],f'c{c}:forward_{suffix}')
            results.append(dict(entry_bits=entry_bits,reference_sha256=ref.description_hash,
                allocation=plan,total=dict(bill.c),parts=bill.rows))
    a,b=results
    ratios={key:str(Q(b['total'][key],a['total'][key])) for key in a['total'] if a['total'][key]}
    report=dict(status='EXACT_SOURCE_OPERATION_CENSUS_ONLY',
        scope='All source coefficient reductions, complete inverse diagonal blocks and coupling roundings are represented. Operand-bit and serialized-cell metrics are comparison proxies, not measured Tape actions, complete wall time, or a new physical tariff.',
        source_pins={str(path.relative_to(ROOT)):sha256(path.read_bytes()).hexdigest() for path in
                    [ROOT/'research/physical-boundary-pages/boundary_pages.py',
                     ROOT/'research/physical-gaussian-core/gaussian_matrix.py',
                     ROOT/'research/physical-gaussian-core/gaussian_rationals.py',
                     source.INVERSE/'source_window.py',source.FORWARD/'pages.py']},
        ledger_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),results=results,
        entry40_over_entry64_ratios=ratios)
    print(json.dumps(report,indent=2,sort_keys=True))


if __name__=='__main__':main()
