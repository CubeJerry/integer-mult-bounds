"""Bit-basis replay of the physical H reduction and its exact reverse."""
import struct

def verify(matrix, stream, F, expected_price):
    n=len(matrix); need=lambda ok,msg:None if ok else (_ for _ in ()).throw(ValueError(msg))
    bitrows={a:[sum(((int(F.product[a,1<<s])>>t)&1)<<s for s in range(6)) for t in range(6)] for a in range(64)}
    coefficients={a:[(t,s) for t in range(6) for s in range(6) if bitrows[a][t]>>s&1] for a in range(64)}
    scales={}
    for a in range(1,64):
        rows=bitrows[a][:]; reduce=[]
        def add(d,s):
            rows[d]^=rows[s];reduce.append((d,s))
        for c in range(6):
            p=next(j for j in range(c,6) if rows[j]>>c&1)
            if p!=c:
                add(p,c);add(c,p);add(p,c)
            for j in range(6):
                if j!=c and rows[j]>>c&1:add(j,c)
        need(rows==[1<<j for j in range(6)], 'independent scalar binary row reduction')
        scales[a]=reduce[::-1]
    target=[0]*(6*n)
    for d,row in enumerate(matrix):
        for s,q in enumerate(row):
            if not q:continue
            for t,mask in enumerate(bitrows[int(q)]):
                target[6*d+t]^=mask<<(6*s)
    need(len(stream)%6==0, 'whole field-operation records')
    operations=[]
    for op,d,s,q in struct.iter_unpack('<BHHB',stream):
        need(d<n and s<n, 'original physical holder indices')
        if op==0:
            need(d!=s and q!=0, 'valid scaled ADD')
            operations.extend((6*d+t,6*s+u) for t,u in coefficients[q])
        elif op==1:
            need(q!=0 and s==0, 'valid local field multiplier')
            operations.extend((6*d+t,6*d+u) for t,u in scales[q])
        elif op==2:
            need(d!=s and q==0, 'valid original-holder swap')
            for b in range(6):
                operations.extend([(6*d+b,6*s+b),(6*s+b,6*d+b),(6*d+b,6*s+b)])
        else:raise ValueError('unknown field opcode')
    need(len(operations)==expected_price, 'each literal whole-record ADD counted')
    rows=target[:]
    for d,s in operations:rows[d]^=rows[s]
    identity=[1<<j for j in range(6*n)]
    need(rows==identity, 'actual H binary reduction on all basis vectors')
    for d,s in reversed(operations):rows[d]^=rows[s]
    need(rows==target, 'reverse binary ADD word implements the entire actual H matrix')
    return {'binary_dimension':6*n,'field_operations':len(stream)//6,'whole_record_ADD_each_direction':len(operations),
            'forward_and_inverse_all_basis_vectors':True}
