#!/usr/bin/env python3
"""Independent exact carry/Lucas check, including unfolded prefix formulas."""
import itertools
import json
import math
from pathlib import Path


def fmul(a, b):
    out = 0
    while b:
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return out


def omega(exponent):
    return (1, 2, 3)[exponent % 3]


def bits(value, width):
    return [(value >> k) & 1 for k in range(width)]


def add_bits(x, y, omit_generate=False):
    carry, out = 0, []
    for a, b in zip(x, y):
        out.append(a ^ b ^ carry)
        carry = (0 if omit_generate else a * b) ^ ((a ^ b) * carry)
    return out


def value(word):
    return sum(x << k for k, x in enumerate(word))


def binomial(n, h):
    return (math.comb(n, h) if h <= n else 0) if n >= 0 else (-1)**h * math.comb(h-n-1, h)


def const(x):
    return ('c', x)


def formula_add(x, y):
    carry, out = const(0), []
    for a, b in zip(x, y):
        out.append(('+', ('+', a, b), carry))
        carry = ('+', ('*', a, b), ('*', ('+', a, b), carry))
    return out


def count_formula(length, width):
    words = [[('v', (j,k)) if k < 2 else const(0) for k in range(width)] for j in range(length)]
    size = 1 << (length - 1).bit_length()
    words += [[const(0)] * width for _ in range(size-length)]
    while len(words) > 1:
        words = [formula_add(words[j], words[j+1]) for j in range(0,len(words),2)]
    return words[0]


def serialize(tree):
    # Every occurrence is copied. There are no pointer/reuse instructions.
    if tree[0] in ('c', 'v'):
        return [tree], int(tree[0] == 'v')
    left, dl = serialize(tree[1])
    right, dr = serialize(tree[2])
    return [(tree[0],)] + left + right, max(dl,dr) if tree[0] == '+' else dl+dr


def evaluate(program, variables):
    stack = []
    for item in reversed(program):
        if item[0] == 'c':
            stack.append(item[1])
        elif item[0] == 'v':
            stack.append(variables[item[1]])
        else:
            a,b = stack.pop(),stack.pop()
            stack.append(a ^ b if item[0] == '+' else fmul(a,b))
    assert len(stack) == 1
    return stack[0]


def run():
    addition_cases = 0
    for width in range(1,7):
        for x in range(1 << width):
            for y in range(1 << width):
                assert value(add_bits(bits(x,width),bits(y,width))) == (x+y) % (1 << width)
                addition_cases += 1
    assert value(add_bits(bits(1,2),bits(1,2),True)) != 2

    lucas_cases = 0
    for width in range(1,7):
        for count in range(33):
            for offset in range(-16,17):
                shifted = add_bits(bits(count,width),bits(-offset,width))
                assert value(shifted) == (count-offset) % (1 << width)
                for h in range(1 << width):
                    coefficient = math.prod(shifted[k] for k in range(width) if (h >> k) & 1)
                    assert coefficient == binomial(count-offset,h) % 2
                    lucas_cases += 1

    formula_cases, largest_tree = 0, 0
    for length in (1,2,3,4):
        trees = formula_add(count_formula(length,4), [const(x) for x in bits(-3,4)])
        programs = []
        for k,tree in enumerate(trees):
            program,degree = serialize(tree)
            assert degree <= 1 << k
            programs.append(program)
            largest_tree = max(largest_tree,len(program))
        for digits in itertools.product(range(3),repeat=length):
            variables = {(j,k):(digit >> k) & 1 for j,digit in enumerate(digits) for k in (0,1)}
            assert value([evaluate(program,variables) for program in programs]) == (sum(digits)-3) % 16
            formula_cases += 1

    stats_cases = 0
    sizes,degrees = [1]*25,[1,1]+[0]*23
    for level in range(21):
        for k in range(25):
            assert sizes[k] <= 8**level * math.comb(level+k,k)
            assert degrees[k] <= 1 << k
            stats_cases += 1
        next_sizes,next_degrees,carry_size,carry_degree = [],[],1,0
        for k in range(25):
            next_sizes.append(2*sizes[k]+carry_size+2)
            next_degrees.append(max(degrees[k],carry_degree))
            carry_size += 4*sizes[k]+4
            carry_degree = max(2*degrees[k],degrees[k]+carry_degree)
        sizes,degrees = next_sizes,next_degrees

    predictor_cases, phase_control = 0,False
    for length in (1,2,3):
        for exponent in itertools.product(range(3),repeat=length):
            for shift in itertools.product(range(3),repeat=length):
                count = sum((x+y) % 3 for x,y in zip(exponent,shift))
                for offset in range(-2,5):
                    for degree in range(8):
                        width = (degree+1).bit_length()
                        shifted,total = bits(count-offset,width),0
                        for h in range(degree+1):
                            coefficient = math.prod(shifted[k] for k in range(width) if (h >> k) & 1)
                            total ^= fmul(omega(2*h),coefficient)
                        result = fmul(omega(offset-sum(shift)),total)
                        if offset <= count <= offset+degree:
                            target = omega(sum(exponent))
                            assert result == target
                            phase_control |= total != target
                        assert 0 <= result < 4
                        predictor_cases += 1
    assert phase_control
    return dict(status='passed',addition_truth_cases=addition_cases,
                shifted_lucas_cases=lucas_cases,unfolded_formula_cases=formula_cases,
                largest_serialized_bit_formula_nodes=largest_tree,
                size_degree_recurrence_cases=stats_cases,f4_predictor_cases=predictor_cases,
                negative_controls=dict(missing_carry_generate=True,omitted_scalar_phase=True),
                asymptotic_tape_compiler_checked=False)


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('characteristic-two-carry-formula-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
