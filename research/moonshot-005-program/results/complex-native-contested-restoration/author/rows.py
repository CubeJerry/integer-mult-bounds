"""Local rational transfer and arbitrary-input bank rank checks."""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import cache
from graph import require
from packed import Field, PRIME, inverse, unit


@cache
def residue(q):
    return q.numerator * inverse(q.denominator % PRIME) % PRIME


def original_values(g, adjoint=False):
    n = len(g.initial)
    field = Field(n)
    forms = g.forms
    scheduler = g.schedule
    moves = g.moves
    initial = g.initial
    if adjoint:
        forms = defaultdict(dict)
        for reader, row in g.forms.items():
            donor = reader if reader in moves else ~(reader-g.first_output)
            for original, q in row.items():
                target = original if original in moves else g.first_output+(~original)
                forms[target][donor] = q
        moves = {e:(b,a) for e,(a,b) in moves.items()}
        scheduler = [e for e in reversed(g.schedule) if e in moves] + list(range(g.first_output,g.first_output+n))
        initial = g.final
    values = {~j:unit(j) for j in range(n)}
    banks = defaultdict(list)
    for j,b in enumerate(initial):
        banks[b].append(~j)
    for node in scheduler:
        row = forms[node]
        require(len(row)<=2048, 'packed sum capacity')
        values[node] = field.reduce(sum(residue(q)*values[e] for e,q in row.items()),3)
        if node in moves:
            banks[moves[node][1]].append(node)
    return values,banks


def bank_ranks(g,adjoint=False):
    values,banks = original_values(g,adjoint)
    field = Field(len(g.initial))
    nullity = sum(len(events)-len(field.basis(values[e] for e in events)) for events in banks.values())
    require(nullity==0,'arbitrary-original bank independence')
    return {'active_charts':len(banks),'scalars':sum(map(len,banks.values())),'rank_deficit':nullity}


def nullspace(rows,n,modular):
    """Column kernel, returning basis vectors with their free coordinates fixed."""
    a = [list(row) for row in rows]
    pivots = []
    for j in range(n):
        i = len(pivots)
        hit = next((u for u in range(i,len(a)) if a[u][j]),None)
        if hit is None:
            continue
        a[i],a[hit] = a[hit],a[i]
        scale = inverse(a[i][j]) if modular else 1/Q(a[i][j])
        a[i] = [scale*x % PRIME if modular else scale*x for x in a[i]]
        for k,row in enumerate(a):
            if k!=i and row[j]:
                h = row[j]
                a[k] = [(x-h*y)%PRIME for x,y in zip(row,a[i])] if modular else [x-h*y for x,y in zip(row,a[i])]
        pivots.append(j)
        if len(pivots)==len(a):
            break
    basis = []
    for free in set(range(n))-set(pivots):
        v = [0]*n
        v[free] = 1
        for i,j in enumerate(pivots):
            v[j] = (-a[i][free])%PRIME if modular else -a[i][free]
        basis.append(v)
    return basis


def triangle_blocks(g):
    for b,inputs in g.incoming.items():
        outputs = g.outgoing[b]
        from_chart = defaultdict(list)
        to_chart = defaultdict(list)
        for e in inputs:
            if e in g.moves:
                from_chart[g.moves[e][0]].append(e)
        for e in outputs:
            if e in g.moves:
                to_chart[g.moves[e][1]].append(e)
        for a,x in from_chart.items():
            for c,y in to_chart.items():
                if (g.dimension[b]-g.dimension[a])*(g.dimension[c]-g.dimension[b])>0:
                    yield a,b,c,x,y, [i for i in inputs if i not in x], [o for o in outputs if o not in y]


def kernel_block(g,rows,columns,modular,transpose=False):
    mat = [[g.forms[o].get(i,0) for i in columns] for o in rows]
    if modular:
        mat = [[residue(q) for q in row] for row in mat]
    if transpose:
        mat = [[mat[i][j] for i in range(len(rows))] for j in range(len(columns))]
    return nullspace(mat,len(rows) if transpose else len(columns),modular)


def triangle_test(g):
    counts = Counter()
    for a,b,c,x,y,z,w in triangle_blocks(g):
        counts['triples'] += 1
        require(not kernel_block(g,w+y,x,True), 'full column boundary')
        require(not kernel_block(g,y,z+x,True,True), 'full row boundary')
        kernel_mod = kernel_block(g,w,x,True)
        if not kernel_mod:
            continue
        counts['incoming_possible_mod_p']+=1
        cokernel_mod = kernel_block(g,y,z,True,True)
        if not cokernel_mod:
            continue
        counts['both_possible_mod_p']+=1
        # A modular vanishing capacity alone would not prove a rational upper bound.
        # Explicit exact nullspaces give the upper bound when both modular screens survive.
        kernel = kernel_block(g,w,x,False)
        cokernel = kernel_block(g,y,z,False,True)
        for u in kernel:
            cu = [sum(g.forms[o].get(i,0)*v for i,v in zip(x,u)) for o in y]
            for v in cokernel:
                require(sum(p*q for p,q in zip(v,cu)) == 0, 'positive rational bypass')
        counts['positive_quotient_ranks'] += 0
    require(counts['triples']==6959 and counts['both_possible_mod_p']==822, 'all triples')
    return dict(counts)
