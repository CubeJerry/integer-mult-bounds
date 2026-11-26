"""Rational and binary checks for the explicit C=53 input-length threshold."""
from fractions import Fraction as F
from math import factorial

J, start = 11500, 11510
E, U, M = F(167, 500), F(8001, 1000), F(1447, 200)
B = F(36169, 5000)


def main():
    assert 3*16+6 <= 2**(16-5)
    assert 500*(14+9) == J and J+2 <= 2**14
    assert (1+F(1, 500))/3 == E
    assert 8+F(32, 3*J) < U
    assert sum(F(21,10)**i/factorial(i) for i in range(8)) > U
    assert 7 + E*F(21, 10)/3 == B
    assert B+F(20, 4**10) < M
    assert 4*M-(M+3*(U-1)+E*F(21,10)) == F(3, 5000)
    assert F(4497,100)**3-240*M**3 == F(50622783,1000000)
    q = 3*start + (3*start+2).bit_length() + 2
    v0 = 240*(q*2**(3*start)+2)
    assert q == 34548 and (4*v0)**2 < 1 << 69110
    assert ((4*v0)**2).bit_length() == 69110
    assert F(1)+F(2,4096) < F(1001,1000)
    g = F(4497,100)+8*F(1001,1000)
    assert g == F(26489,500)
    assert 10*(v0+3) <= (g-48)*4*v0
    assert 4096*31 <= 2**30 and 2**30+2 <= 2**31
    assert F(53)-g-F(1,64) == F(51,8000)
    assert (F(53)-g-F(1,64))*2**20 > 182+2*g+1
    print("C=53 tail: first band", start, "Q", q, "history threshold ceiling-log", 69110)
    print("upper ratios: native 44.97, Walsh 52.978; outer spare 51/8000 with one bit reserved")


if __name__ == "__main__":
    main()
