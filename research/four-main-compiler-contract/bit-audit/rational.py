"""Lead independent rational logarithm / alternating exponential bounds.
@CubeJerry, OpenAI assistance, Apache-2.0. No source price imports.
"""
from fractions import Fraction as F

def need(ok, message):
    if not ok:
        raise ValueError(message)

def log_unit(x):
    z = (x - 1) / (x + 1)
    need(0 <= z <= F(1, 3), 'log range')
    terms = 48
    total = 2 * sum((z ** (2*j+1) / (2*j+1) for j in range(terms)), F(0))
    tail = 2 * z ** (2*terms+1) / ((2*terms+1) * (1-z*z))
    return total, total + tail

def log_bounds(n):
    need(type(n) is int and n >= 1, 'positive rank')
    s = n.bit_length()-1
    a,b = log_unit(F(n, 2**s))
    c,d = log_unit(F(2))
    return a+s*c, b+s*d

def exponential_partial(t, terms):
    need(0 <= t < 1, 'alternating exponential domain')
    value = current = F(1)
    for j in range(1, terms+1):
        current *= -t / j
        value += current
    return value

def exp_interval(a,b):
    # exp(-t) decreases in t; odd/even partial sums bracket exp(-t).
    need(0 <= a <= b < 1, 'exponential interval')
    return exponential_partial(b,35), exponential_partial(a,36)

def signed_moment(signed, saving, logs):
    low = high = F(0)
    for rank, coefficient in signed.items():
        a,b = logs[rank]
        l,u = exp_interval(saving*a,saving*b)
        l *= rank; u *= rank
        low += coefficient*(l if coefficient >= 0 else u)
        high += coefficient*(u if coefficient >= 0 else l)
    return low,high
