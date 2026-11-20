#!/usr/bin/env python3
"""Construct the four invertible facet gauges from a frozen physical Schur map."""
import argparse
import ctypes
import hashlib
import importlib.util
import json
from pathlib import Path
import numpy as np


def require(ok, message):
    if not ok:
        raise ValueError(message)


def doubled(matrix):
    zero = np.zeros_like(matrix)
    return np.block([[matrix, zero], [zero, matrix]])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('engine', 'lib', 'data', 'out'):
        p.add_argument('--' + name, type=Path, required=True)
    p.add_argument('--four', action='store_true', help='input is the four-role Schur matrix')
    args = p.parse_args()
    spec = importlib.util.spec_from_file_location('native_stream', args.engine / 'check.py')
    pkg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pkg)
    engine = pkg.Engine(args.lib)
    multiply = engine.mm
    inverse_call = engine.lib.inverse_direct
    inverse_call.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p]
    inverse_call.restype = ctypes.c_int

    def inverse(matrix):
        source = np.ascontiguousarray(matrix)
        require(source.shape == (len(source), len(source)), 'square inverse')
        result = np.empty_like(source)
        require(inverse_call(source.ctypes.data, len(source), result.ctypes.data), 'singular Schur pivot')
        return result

    with np.load(args.data) as raw:
        if args.four:
            schur = np.array(raw['matrix'], copy=True)
        else:
            require(list(raw['roles']) == [0, 1, 2, 3], 'ordered original roles')
            schur = multiply(inverse(raw['qe']), raw['qa'])
    width = len(schur) // 4
    require(schur.shape == (4*width, 4*width), 'four native receiver dimensions')

    def block(i, j):
        return schur[i*width:(i+1)*width, j*width:(j+1)*width]

    # The letters follow the displayed four-row derivation in PROOF.md.
    A = multiply(inverse(block(1, 3)), block(1, 0))
    B = multiply(inverse(block(1, 3)), block(1, 2))
    C = multiply(inverse(block(0, 3)), block(0, 1))
    D = multiply(inverse(block(0, 3)), block(0, 2))
    E = block(2, 0) ^ multiply(block(2, 3), A)
    F = multiply(block(2, 3), B)
    G = block(2, 1) ^ multiply(block(2, 3), C)
    H = multiply(block(2, 3), D)

    def fractional(numerator, first, denominator, shift, constant):
        first_inverse = inverse(first)
        top = multiply(numerator, first_inverse)
        bottom = multiply(denominator, first_inverse)
        return np.block([[top, multiply(top, shift) ^ block(3, 2)],
                         [bottom, multiply(bottom, shift) ^ constant]])

    left = fractional(block(3, 0), E, A, F, B)
    right = fractional(block(3, 1), G, C, H, D)
    transition = multiply(inverse(right), left)
    eye = np.eye(width, dtype=np.uint8)
    zero = np.zeros_like(eye)
    top = np.block([[eye, zero], [transition[:width, :width], transition[:width, width:]]])
    bottom = np.block([[zero, eye], [transition[width:, :width], transition[width:, width:]]])
    Z = multiply(top, inverse(bottom))
    P = multiply(inverse(Z ^ doubled(F)), doubled(E))
    Q = multiply(inverse(Z ^ doubled(H)), doubled(G))
    R = doubled(A) ^ multiply(doubled(B), P)
    S = doubled(C) ^ multiply(doubled(D), Q)
    diagonal = [multiply(doubled(block(0, 2)), P) ^ multiply(doubled(block(0, 3)), R),
                multiply(doubled(block(1, 2)), Q) ^ multiply(doubled(block(1, 3)), S),
                Z, multiply(doubled(block(3, 0)) ^ multiply(doubled(block(3, 2)), P), inverse(R))]
    identity = np.eye(2*width, dtype=np.uint8)
    empty = np.zeros_like(identity)
    modes = np.block([[identity, empty], [empty, identity], [P, Q], [R, S]])
    inverse_gauges = np.stack([y ^ identity ^ doubled(block(i, i)) for i, y in enumerate(diagonal)])
    gauges = np.stack([inverse(x) for x in inverse_gauges])
    args.out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.out / 'GAUGES.npz', actual=inverse_gauges, W=gauges,
                        X_local=modes, K_reduced=schur)
    print('constructed the four native paired gauges at width', width, flush=True)


if __name__ == '__main__':
    main()
