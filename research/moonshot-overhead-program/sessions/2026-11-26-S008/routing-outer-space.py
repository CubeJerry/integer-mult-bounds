"""Check the numerical coefficients of the cumulative visited-cell argument."""

from fractions import Fraction
import json


def check():
    native_ordinary = 1024 * (16 + 9)
    native_stacks = 2 * (2 * (3 * 2**12 + 2) + 1)
    native_direct = 17 * (102 + 1)
    native_abi = 128 * (2 + 5)
    assert native_ordinary + native_stacks + native_direct + native_abi < 2**18

    assert 62 * (18 + 5) < 2**12
    assert 160 * (8 + 5) < 2**16
    one_family = 9 * 2**18 + 2**12 + 2**16
    assert one_family < 5 * 2**19
    assert 128 * Fraction(16, 7) < 293
    walsh_payload = 64 * (2 + 5) + 2 * (293 + 2) + 128 * (2 + 5) + 64
    assert walsh_payload < 2**12

    route_heads = 1024 + 2 + 17 + 128 + 62 + 160 + 256
    walsh_heads = 64 + 2 + 128 + 32 + 11 + 6 + 64 + 128
    assert route_heads < 2048 and walsh_heads < 512
    assert 2 * route_heads + walsh_heads + 512 < 2**13

    outside = 2 * 2**16 + 2**12 * 100 + 2**14 + 3 + 1 + 1 + 8
    assert outside < 2**22
    all_arenas = 5 * 2**19 * (1024 + 100) + 2**22
    assert all_arenas == 2_950_692_864 < 2**32
    return {
        "native_uniform_envelope": 2**18,
        "routing_family": one_family,
        "routing_heads_upper_accounted": route_heads,
        "ordinary_walsh_heads_upper_accounted": walsh_heads,
        "all_arenas_per_Nk": all_arenas,
        "convenient_fast_space_per_input_bit": 2**36,
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
