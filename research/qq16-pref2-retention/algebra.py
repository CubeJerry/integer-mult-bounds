"""Exact ordered and rational checks for the pre-F2 retention interface.

New material: @CubeJerry with substantial OpenAI Codex assistance, Apache-2.0.
QQ16 local maps: Ali Romman. Recorded-cut decoder: commdata2338 / PR2174.
"""

from fractions import Fraction as Q


def need(condition, message):
    if not condition:
        raise ValueError(message)


def add(*terms):
    """Linear combination of equally shaped rational matrices."""
    first = terms[0][1]
    out = [[Q(0) for _ in row] for row in first]
    for coefficient, matrix in terms:
        need(len(matrix) == len(out), "matrix row shape")
        for i, row in enumerate(matrix):
            need(len(row) == len(out[i]), "matrix column shape")
            for j, value in enumerate(row):
                if value:
                    out[i][j] += coefficient * value
    return out


def mul(a, b):
    need(bool(a) and bool(b) and len(a[0]) == len(b), "product shape")
    out = [[Q(0)] * len(b[0]) for _ in a]
    for i, row in enumerate(a):
        for k, coefficient in enumerate(row):
            if coefficient:
                for j, value in enumerate(b[k]):
                    if value:
                        out[i][j] += coefficient * value
    return out


def eye(n):
    return [[Q(i == j) for j in range(n)] for i in range(n)]


def inverse(matrix):
    n = len(matrix)
    work = [list(row) + unit for row, unit in zip(matrix, eye(n))]
    for j in range(n):
        pivot = next((i for i in range(j, n) if work[i][j]), None)
        need(pivot is not None, "invertible selected section")
        work[j], work[pivot] = work[pivot], work[j]
        divisor = work[j][j]
        work[j] = [v / divisor for v in work[j]]
        for i in range(n):
            if i != j and work[i][j]:
                c = work[i][j]
                work[i] = [v - c * u for v, u in zip(work[i], work[j])]
    return [row[n:] for row in work]


def zero(rows, columns):
    return [[Q(0)] * columns for _ in range(rows)]


def shear_matrix(q, seed):
    a = eye(q)
    if q > 1:
        i, j = seed % q, (seed + 1) % q
        a[i][j] += Q(1 + seed % 3)
        # Alternating directions prevent simultaneous commutative fixtures.
        b = eye(q)
        b[j][i] -= Q(1 + seed % 2)
        a = mul(a, b)
    return a


def models(q):
    """Nine exact local contracts; ordinary dimension 3q and B_s K_s=12I."""
    charts = []
    for s in range(9):
        left = shear_matrix(q, 2 * s + 1)
        a, t = shear_matrix(q, 3 * s + 2), shear_matrix(q, 5 * s + 3)
        blocks = [left] + [
            [[Q(((i + 2) * (j + 1) + s * k) % 5 - 2)
              for j in range(q)] for i in range(q)] for k in (1, 2)]
        b = [sum((block[i] for block in blocks), []) for i in range(q)]
        k = add((12, inverse(left))) + zero(2 * q, q)
        charts.append(dict(B=b, K=k, LA=a, LT=t, PA=inverse(a), PT=inverse(t)))
        need(mul(b, k) == add((12, eye(q))), "ordinary response 12I")
    if q > 1:
        need(mul(charts[0]['LA'], charts[2]['LT']) !=
             mul(charts[2]['LT'], charts[0]['LA']), "noncommuting model")
    return charts


def query(chart, x):
    u, a, t = x
    return add((1, mul(chart['B'], u)), (1, mul(chart['LA'], a)),
               (1, mul(chart['LT'], t)))


def forward(chart, x, y):
    f = query(chart, x)
    xx = [add((1, x[0]), (-1, mul(chart['K'], f))),
          mul(chart['PA'], mul(chart['LT'], x[2])), mul(chart['PT'], f)]
    yy = [add((1, y[0]), (1, xx[0]))] + [
        add((1, x[j]), (1, y[j]), (-1, xx[j])) for j in (1, 2)]
    return xx, yy, f


def backward(current, future, x, y):
    """Literal E / exchange / H factorization, not the decoder formula."""
    u = [y[0], add((1, y[1]), (1, mul(future['PA'],
         add((1, mul(future['B'], y[0])), (1, mul(future['LT'], y[2])))))), y[2]]
    a, b = mul(current['LT'], x[2]), query(current, u)
    v = [u[0], u[1], add((1, u[2]), (1, mul(current['PT'], add((1, a), (-1, b)))))]
    rv = query(current, v)
    yy = [add((1, v[0]), (1, mul(current['K'], rv))), v[1],
          add((1, v[2]), (-12, mul(current['PT'], rv)))]
    xx = [add((1, x[0]), (-1, y[0]))] + [
        add((1, x[j]), (1, y[j]), (-1, yy[j])) for j in (1, 2)]
    need(rv == a, "exchange current query")
    need(xx[2] == mul(current['PT'], add((1, b), (12, a))), "B T record")
    return xx, yy


def adapter_word():
    # Registers: X_A, X_T, Y_A, Y_T, borrowed query scratch.
    # A += H T; T -= H^-1 A; A += H T, preserving each X+Y sum.
    return [('H', 0, 1, 1), ('H', 2, 1, -1),
            ('J', 1, 0, -1), ('J', 3, 0, 1),
            ('H', 0, 1, 1), ('H', 2, 1, -1)]


def factor_word(word=None):
    """Every compound ADD is a four-child dirty echo; scratch always restores."""
    out = []
    for name, target, source, sign in adapter_word() if word is None else word:
        left, right = ('PA', 'LT') if name == 'H' else ('PT', 'LA')
        out.extend([(right, 4, source, 1), (left, target, 4, sign),
                    (right, 4, source, -1), (left, target, 4, -sign)])
    return out


def run_word(rows, word, maps):
    rows = [[list(row) for row in block] for block in rows]
    for op, target, source, sign in word:
        need(target != source, "disjoint ADD ports")
        rows[target] = add((1, rows[target]), (sign, mul(maps[op], rows[source])))
    return rows


def rotate(chart, x, y, fault=None):
    h, j = mul(chart['PA'], chart['LT']), mul(chart['PT'], chart['LA'])
    rows = [x[1], x[2], y[1], y[2]]
    word = adapter_word()
    if fault == 'missing_y_correction':
        word = word[:-1]
    if fault == 'wrong_middle_sign':
        word[2] = ('J', 1, 0, 1)
    out = run_word(rows, word, {'H': h, 'J': j})
    return [x[0], out[0], out[1]], [y[0], out[2], out[3]]


def basis_banks(q):
    n = 40 * q  # four pairs, two sides, (3q ordinary + q A + q T)
    full, banks, offset = eye(n), [], 0
    for _ in range(4):
        sides = []
        for _ in range(2):
            sides.append([full[offset:offset + 3*q], full[offset + 3*q:offset + 4*q],
                          full[offset + 4*q:offset + 5*q]])
            offset += 5*q
        banks.append(sides)
    return banks


def simulate(charts, recipe, fault=None):
    q = len(charts[0]['PA'])
    initial = basis_banks(q)
    banks = [[list(side) for side in pair] for pair in initial]
    histories, cut = {}, None
    for event in recipe:
        kind = event['kind']
        if kind == 'local':
            s, bank = event['stage'], event['pair']
            x, y = banks[bank]
            if s == 2 and fault != 'omit_adapter':
                x, y = rotate(charts[0 if fault == 'wrong_chart' else 2], x, y, fault)
            if event['reverse']:
                x, y = backward(charts[s], charts[s+1], x, y)
            else:
                x, y, f = forward(charts[s], x, y)
                histories[s] = f
            banks[bank] = [x, y]
            if s == 1:
                cut = [list(x), list(y)]
        elif kind == 'bridge':
            i, j, c = event['src'], event['dst'], event['coefficient']
            banks[j][0][0] = add((1, banks[j][0][0]), (c, banks[i][0][0]))
            banks[i][1][0] = add((1, banks[i][1][0]), (-c, banks[j][1][0]))
        else:
            need(kind == 'terminal' and event['pairs'] == 4, "terminal")
            banks = [[y, [add((-1, block)) for block in x]] for x, y in banks]
    need(cut is not None, "B1 cut exists")
    return initial, banks, histories, cut


def observe(charts, initial, final, histories):
    """The complete observation boundary; no transient cut or f2 history."""
    xf, yf = final[0]
    return {'q0': mul(charts[0]['B'], initial[0][0][0]),
            'q2': mul(charts[2]['B'], initial[0][0][0]), 'f0': histories[0],
            'C': yf[0], 'XA': xf[1], 'XT': xf[2], 'YA': yf[1], 'YT': yf[2]}


def decode(charts, observations, fault=None):
    c0, c2 = charts[0], charts[2]
    o = observations
    need(set(o) == {'q0', 'q2', 'f0', 'C', 'XA', 'XT', 'YA', 'YT'}, 'observation whitelist')
    pa = add((1, o['XA']), (-1, o['YA']))
    pt = add((1, o['XT']), (-1, o['YT']))
    da = add((1, pa), (-1, o['YA']))
    if fault == 'terminal_sign':
        da = add((1, pa), (1, o['YA']))
    f0 = o['f0']
    f2 = add((-1 if fault != 'f2_terminal_sign' else 1, mul(c2['LT'], o['YT'])))
    q0, q2 = o['q0'], o['q2']
    if fault == 'omit_q0':
        q0 = zero(len(q0), len(q0[0]))
    if fault == 'omit_q2':
        q2 = zero(len(q2), len(q2[0]))
    completed = o['C']
    middle = add((1, mul(c2['B'], completed)), (1, q2),
                 (-12 if fault != 'omit_f2' else 0, f2),
                 (-1, mul(c2['B'], mul(c0['K'], f0))),
                 (1, mul(c2['LT'], add((1, pt), (-1, mul(c0['PT'], f0))))))
    t = add((1, pa), (-1, da), (1, mul(c2['PA'], middle)))
    xt = mul(c0['PT'], mul(c0['LA'], t))
    xa = mul(c0['PA'], add((1, f0), (-1, q0), (-1, mul(c0['LT'], xt))))
    return [xa, xt, add((1, pa), (-1, xa)), add((1, pt), (-1, xt))]


def expected_selected(initial):
    x, y = initial[0]
    return [x[1], x[2], y[1], y[2]]


def decoder_program():
    """An out-of-place decoder with explicitly owned outputs and temporaries.

    C is an ordinary block. All other observations and m,v are query blocks;
    u is an ordinary temporary. A clear is paid and may discard owned dirt.
    """
    return [
        ('clear', 'm'), ('add', 'm', 'C', 'B2', 1), ('add', 'm', 'q2', 'I', 1),
        ('clear', 'u'), ('add', 'u', 'f0', 'K0', 1), ('add', 'm', 'u', 'B2', -1),
        ('clear', 'u'), ('clear', 'v'), ('add', 'v', 'f0', 'PT0', 1),
        ('add', 'v', 'XT', 'I', -1), ('add', 'v', 'YT', 'I', -11),
        ('add', 'm', 'v', 'LT2', -1), ('clear', 'v'), ('add', 'v', 'YA', 'I', 1),
        ('add', 'v', 'm', 'PA2', 1), ('clear', 'm'), ('add', 'm', 'v', 'LA0', 1),
        ('clear', 'out_XT'), ('add', 'out_XT', 'm', 'PT0', 1), ('clear', 'v'),
        ('add', 'v', 'f0', 'I', 1), ('add', 'v', 'q0', 'I', -1),
        ('add', 'v', 'out_XT', 'LT0', -1), ('clear', 'out_XA'),
        ('add', 'out_XA', 'v', 'PA0', 1), ('clear', 'out_YA'),
        ('add', 'out_YA', 'XA', 'I', 1), ('add', 'out_YA', 'YA', 'I', -1),
        ('add', 'out_YA', 'out_XA', 'I', -1), ('clear', 'out_YT'),
        ('add', 'out_YT', 'XT', 'I', 1), ('add', 'out_YT', 'YT', 'I', -1),
        ('add', 'out_YT', 'out_XT', 'I', -1), ('clear', 'm'), ('clear', 'v')]


def run_decoder_program(charts, observations, program=None):
    """Check arbitrary initial owned dirt as extra independent basis columns."""
    q, ordinary = len(charts[0]['LA']), len(charts[0]['K'])
    columns = len(observations['f0'][0])
    dirty_columns = ordinary + 6*q
    rows = {name: [list(row) + [Q(0)] * dirty_columns for row in block]
            for name, block in observations.items()}
    sizes = dict(m=q, u=ordinary, v=q, out_XA=q, out_XT=q, out_YA=q, out_YT=q)
    offset = columns
    for name, size in sizes.items():
        rows[name] = [[Q(j == offset+i) for j in range(columns + dirty_columns)] for i in range(size)]
        offset += size
    need(offset == columns + dirty_columns, 'owned decoder storage inventory')
    maps = {'I': eye(q), 'B2': charts[2]['B'], 'K0': charts[0]['K']}
    maps.update({name+str(stage): charts[stage][name]
                 for stage in (0, 2) for name in ('PA', 'PT', 'LA', 'LT')})
    for event in decoder_program() if program is None else program:
        kind, target = event[:2]
        need(target in sizes, 'observations are immutable')
        if kind == 'clear':
            rows[target] = zero(sizes[target], columns + dirty_columns)
        else:
            need(kind == 'add', 'decoder alphabet')
            _, _, source, op, sign = event
            rows[target] = add((1, rows[target]), (sign, mul(maps[op], rows[source])))
    output = [rows['out_' + name] for name in ('XA', 'XT', 'YA', 'YT')]
    scratch = [rows[name] for name in ('m', 'u', 'v')]
    return output, scratch, dirty_columns


def linear(*terms):
    out = {}
    for coefficient, expr in terms:
        for word, value in expr.items():
            out[word] = out.get(word, 0) + coefficient * value
    return {word: value for word, value in out.items() if value}


def symbol(name):
    return {(name,): Q(1)}


def operate(operator, expr):
    """Free ordered words, reducing only selected inverse pairs and B2 K2."""
    out = {}
    for word, value in expr.items():
        word = (operator,) + word
        changed = True
        while changed:
            changed = False
            for i in range(len(word)-1):
                a, b = word[i:i+2]
                if (a, b) == ('B2', 'K2'):
                    value *= 12
                elif not (len(a) == len(b) == 3 and a[1:] == b[1:] and
                          {a[0], b[0]} == {'P', 'L'}):
                    continue
                word = word[:i] + word[i+2:]
                changed = True
                break
        out[word] = out.get(word, 0) + value
    return {word: value for word, value in out.items() if value}


def ordered_identity():
    z, w, a, c, pa, pt, f2 = [symbol(s) for s in ('z', 'w', 'a', 'c', 'pa', 'pt', 'f2')]
    op = operate
    f0 = linear((1, op('B0', z)), (1, op('LA0', a)), (1, op('LT0', c)))
    t = op('PA0', op('LT0', c))
    yu = linear((1, w), (1, z), (-1, op('K0', f0)))
    yt = linear((1, pt), (-1, op('PT0', f0)))
    da = linear((1, pa), (-1, t), (1, op('PA2', linear((1, op('B2', yu)), (1, op('LT2', yt))))))
    xa = linear((1, pa), (-1, da))
    new_t = linear((-1, op('PT2', op('LA2', xa))))
    f2_a = op('PA2', op('LT2', new_t))
    final_y_a = linear((-1, f2_a))
    need(final_y_a == xa, "ordered retention identity")
    recovered_da = linear((1, pa), (-1, final_y_a))
    final_y_t = linear((-1, op('PT2', f2)))
    recovered_f2 = linear((-1, op('LT2', final_y_t)))
    need(recovered_f2 == f2, 'f2 from final selected output, no history')
    completed = linear((1, w), (1, op('K2', f2)))
    recovered_t = linear((1, pa), (-1, recovered_da), (1, op('PA2', linear(
        (1, op('B2', completed)), (1, op('B2', z)), (-12, recovered_f2),
        (-1, op('B2', op('K0', f0))), (1, op('LT2', yt))))))
    recovered_c = op('PT0', op('LA0', recovered_t))
    recovered_a = op('PA0', linear((1, f0), (-1, op('B0', z)), (-1, op('LT0', recovered_c))))
    residuals = [linear((1, recovered_da), (-1, da)),
                 linear((1, recovered_t), (-1, t)),
                 linear((1, recovered_c), (-1, c)),
                 linear((1, recovered_a), (-1, a))]
    need(not any(residuals), "ordered decoder residuals")
    return {'retention_identity': True, 'zero_decoder_residuals': len(residuals),
            'rules': 'selected two-sided inverses; B2 K2 = 12 I only'}
