"""Exact checks of the sparse block formula and its global fibre ranks."""
from itertools import combinations

def verify(f):
    qvalues=[f.q6(v) for v in range(64)]
    f.need(set(qvalues)=={0,1},'the base-field trace quadratic is binary valued')
    Q=tuple(v for v in range(64) if not qvalues[v])
    f.need(len(Q)==28,'twenty-eight singular field nodes')
    Qpoly=f.polynomial(Q);expected=[0]*29
    for degree in (1,10,28):expected[degree]=1
    f.need(Qpoly==tuple(expected),'exact sparse polynomial of all twenty-eight nodes')
    polar_rows=[sum(f.b6(1<<i,1<<j)<<j for j in range(6)) for i in range(6)]
    f.need(f.binary_rank(polar_rows)==6,'nondegenerate minus quadratic polar form')
    for a in range(64):
        for bit in range(6):
            for b in range(64):
                f.need(f.b6(a^(1<<bit),b)==f.b6(a,b)^f.b6(1<<bit,b),'polar form is binary bilinear')
    blocks={};polynomials={};nonzero_determinants=[]
    for v in range(1,64):
        block=tuple(a for a in Q if f.b6(v,a)==(qvalues[v]^1))
        f.need(len(block)==16,'every nonzero receiver parameter has sixteen distinct nodes')
        p=f.polynomial(block)
        f.need(p==f.block_formula(v),'sparse formula equals exact product of its sixteen linear factors')
        f.need(all((f.evaluate(p,a)==0)==(a in block) for a in range(64)),'complete base-field root set of the block polynomial')
        determinant=1
        for a,b in combinations(block,2):determinant=f.MUL[determinant][a^b]
        f.need(determinant!=0,'full-rank sixteen-node Vandermonde source view')
        blocks[v]=block;polynomials[v]=p;nonzero_determinants.append(determinant)
    f.need(f.rank(polynomials.values())==7,'global block-polynomial span has dimension seven')
    fibres={};centres=[]
    for c in Q:
        vv=[v for v in range(1,64) if c in blocks[v]]
        f.need(len(vv)==36 and f.binary_rank(vv)==6,'all thirty-six fixed-centre receiver parameters span the six-space')
        for v in vv:
            p=f.divide(polynomials[v],c)
            f.need(tuple(f.MUL[f.power(v,2)][a] for a in p)==f.U(v,c),'normalized fibre equals the linearized field family')
            fibres[c,v]=p
        f.need(f.rank(fibres[c,v] for v in vv)==6,'exact full fixed-centre fibre rank')
        basis=[f.U(1<<i,c) for i in range(6)]
        f.need(f.rank(basis)==6,'six independent field-linear coefficient directions')
        for v in range(64):
            predicted=[f.xor(basis[i][d] for i in range(6) if v>>i&1) for d in range(16)]
            f.need(tuple(predicted)==f.U(v,c),'normalized fibre family is binary linear in v')
        centres.append({'node':c,'receiver_count':36,'fibre_span_rank':6})
    pairs=[]
    for c,d in combinations(Q,2):
        vv=[v for v in range(1,64) if c in blocks[v] and d in blocks[v]]
        f.need(len(vv)==20 and f.binary_rank(vv)==5,'twenty common-node parameters span a binary five-space')
        f.need(all(not f.b6(v,c^d) for v in vv),'common-node parameters lie in the polar hyperplane')
        f.need(f.rank(fibres[c,v] for v in vv)==5,'exact common-two-node fibre rank')
        pairs.append({'nodes':[c,d],'receiver_count':20,'fibre_span_rank':5})
    fault=list(polynomials[1]);fault[0]^=1
    f.need(f.evaluate(fault,blocks[1][0])!=0,'a polynomial coefficient fault destroys a declared root')
    return Q,blocks,polynomials,{'status':'PASS_INDEPENDENT_GEOMETRIC_RS_FIELD_IDENTITY',
        'field_modulus':0x43,'node_polynomial_nonzero_degrees':[1,10,28],
        'nodes':list(Q),'block_count':63,'global_block_span_rank':7,
        'fixed_centre_checks':centres,'all_common_node_pair_checks':pairs,
        'all_source_Vandermonde_determinants_nonzero':True,'coefficient_fault_rejected':True}
