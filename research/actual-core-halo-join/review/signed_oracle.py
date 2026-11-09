"""Independent numerical observer for the actual Core/halo format boundary.

Host integers/Fractions occur only in this observer, never as a production
payload service. Prepared for @CubeJerry with substantial OpenAI assistance.
Apache-2.0. The retained #6880 splice theorem is not a new claim here.
"""
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def binary(word):
    require(type(word) in (str, tuple, list), 'a finite observer word')
    answer = tuple(int(x) for x in word)
    require(all(x in (0, 1) for x in answer), 'binary observer word')
    if type(word) is str:
        require(all(x in '01' for x in word), 'literal binary text')
    return answer


def signmag_decode(word):
    word = binary(word)
    require(len(word) >= 2, 'sign plus magnitude')
    magnitude = sum(bit * 2 ** (len(word) - 1 - i)
                    for i, bit in enumerate(word[1:], 1))
    require(not (word[0] and magnitude == 0), 'canonical positive zero')
    return -magnitude if word[0] else magnitude


def signmag_encode(value, width):
    require(type(value) is int and type(width) is int and width >= 2,
            'signed-magnitude integer domain')
    require(abs(value) < 2 ** (width - 1), 'signed-magnitude range')
    return (int(value < 0),) + tuple(
        abs(value) // 2 ** i % 2 for i in range(width - 2, -1, -1))


def twos_decode(word):
    word = binary(word)
    require(len(word) >= 2, 'two-complement word width')
    unsigned = sum(bit * 2 ** i for i, bit in enumerate(word))
    return unsigned - word[-1] * 2 ** len(word)


def twos_encode(value, width):
    require(type(value) is int and type(width) is int and width >= 2,
            'two-complement integer domain')
    require(-(2 ** (width - 1)) <= value < 2 ** (width - 1),
            'two-complement signed range')
    residue = value % 2 ** width
    return tuple(residue // 2 ** i % 2 for i in range(width))


def toward_zero(numerator, shift):
    require(type(numerator) is int and type(shift) is int and shift >= 0,
            'nonnegative dyadic division shift')
    magnitude = abs(numerator) // 2 ** shift
    return -magnitude if numerator < 0 else magnitude


def expected_lift(word, q, precision, width):
    require(type(q) is int and type(precision) is int and 0 <= q <= precision,
            'exact refinement of the input grid')
    return twos_encode(signmag_decode(word) * 2 ** (precision - q), width)


def expected_return(word, shift, width):
    return signmag_encode(toward_zero(twos_decode(word), shift), width)


def transport_encode(pairs, width):
    return ''.join(''.join(map(str, signmag_encode(real, width)
                                  + signmag_encode(imaginary, width))) + '#'
                   for real, imaginary in pairs)


def transport_decode(body, width):
    require(type(body) is str and type(width) is int and width >= 2,
            'transport observer schema')
    if not body:
        return ()
    require(body.endswith('#'), 'complete final complex record')
    records = body[:-1].split('#')
    require(all(len(row) == 2 * width for row in records),
            'uniform complete complex records')
    return tuple((signmag_decode(row[:width]), signmag_decode(row[width:]))
                 for row in records)


def core_encode(pairs, width):
    return tuple(bit for real, imaginary in pairs
                 for value in (real, imaginary) for bit in twos_encode(value, width))


def core_decode(body, width):
    body = binary(body)
    require(len(body) % (2 * width) == 0, 'complete Core complex records')
    return tuple((twos_decode(body[i:i + width]),
                  twos_decode(body[i + width:i + 2 * width]))
                 for i in range(0, len(body), 2 * width))


def dyadic_radius(records, component_radius):
    """Least nonnegative-power dyadic satisfying R0^2 >= T R_in^2."""
    require(type(records) is int and records > 0, 'complete record count')
    component_radius = Fraction(component_radius)
    require(component_radius > 0, 'positive component radius')
    squared = records * component_radius ** 2
    result = 1
    while result * result < squared:
        result *= 2
    return result


def error_allowance(euclidean_error, shifts, output_bits):
    require(all(type(u) is int and u >= 0 for u in shifts), 'normalizer shifts')
    require(type(output_bits) is int and output_bits >= 0, 'output grid')
    normalizer = 2 ** sum(shifts)
    return (2 * Fraction(euclidean_error) / normalizer
            + Fraction(2, 2 ** output_bits))


def inverse(matrix):
    """Independent full Gaussian elimination; no Schur or window supplier."""
    size = len(matrix)
    require(size > 0 and all(len(row) == size for row in matrix), 'square matrix')
    work = [[Fraction(x) for x in row]
            + [Fraction(int(i == j)) for j in range(size)]
            for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if work[row][column]), None)
        require(pivot is not None, 'invertible original matrix')
        work[column], work[pivot] = work[pivot], work[column]
        divisor = work[column][column]
        work[column] = [x / divisor for x in work[column]]
        for row in range(size):
            if row == column:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [x - coefficient * y
                             for x, y in zip(work[row], work[column])]
    answer = [row[size:] for row in work]
    require(all(sum(Fraction(matrix[i][k]) * answer[k][j] for k in range(size))
                == int(i == j) for i in range(size) for j in range(size)),
            'independent full inverse residual')
    return answer


def principal_window_inverse(matrix, side):
    size = len(matrix)
    require(type(side) is int and side > 0 and size % side == 0,
            'complete equal ordinary windows')
    result = [[Fraction(0) for _ in range(size)] for _ in range(size)]
    for first in range(0, size, side):
        part = inverse([row[first:first + side]
                        for row in matrix[first:first + side]])
        for i in range(side):
            for j in range(side):
                result[first + i][first + j] = part[i][j]
    return result


def apply_msf_tensor(matrices, pairs, spectator_count=1):
    """Direct original-axis tensor action at spectator||axis0||... addresses."""
    periods = tuple(len(matrix) for matrix in matrices)
    volume = 1
    for size in periods:
        volume *= size
    require(len(pairs) == spectator_count * volume, 'whole original field')
    current = tuple(tuple(Fraction(x) for x in pair) for pair in pairs)
    stride = volume
    for matrix, size in zip(matrices, periods):
        require(all(len(row) == size for row in matrix), 'square axis operator')
        stride //= size
        following = []
        for address in range(len(current)):
            row = address // stride % size
            base = address - row * stride
            following.append(tuple(sum(Fraction(matrix[row][column])
                                       * current[base + column * stride][part]
                                       for column in range(size))
                                   for part in (0, 1)))
        current = tuple(following)
    return current


def component_error(actual, exact):
    require(len(actual) == len(exact), 'same original extent')
    return max((sum(abs(Fraction(x) - Fraction(y)) for x, y in zip(a, b))
                for a, b in zip(actual, exact)), default=Fraction(0))
