"""Bounded source-algebra feasibility only; no new tape implementation.
Prepared for @CubeJerry with substantial OpenAI assistance. Apache-2.0.
"""
from pathlib import Path
import json
import sys
import types

REFERENCE = Path(__file__).resolve().parents[1]/'wave4/research/selected-owned-lifetime-protocol/inputs/move/reference'


def load(relative, name):
    path = REFERENCE/relative
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module


def main():
    n = load('source/native_verify.py','_feasible_source137')
    c = load('source/clifford_exact.py','_feasible_clifford137')
    linear = load('linear/linear.py','_feasible_linear137')
    rows = (3,4,8,17,32,64,128,1,256)
    q = (128,0,0,128,0,0,0,9,0)
    word = linear.cnot_word(rows)
    inverse = n.inverse(rows)
    source = n.frame([137],9)
    canonical = (('D',q,(0,)*9),('P',inverse),('C',1,1),('P',rows),('D',q,(0,)*9))
    other_source = c.canonical_frame(9,[137])
    for x in range(512):
        actual,exponent = n.state(source,x)
        sign = -1 if (x & 9).bit_count()%2 else 1
        closed = {x:(1,1),x^137:(sign,-sign)}
        if exponent != 1 or actual != closed:
            raise ValueError('direct source Pauli kernel mismatch')
        if n.state(canonical,x) != (actual,exponent):
            raise ValueError('canonical five-factor mismatch')
        values,power = other_source.zero_state(x)
        if power != exponent or {y:v for y,v in enumerate(values) if v != (0,0)} != actual:
            raise ValueError('independent dense source mismatch')
        at = x
        for target,control in word:
            at ^= ((at>>control)&1)<<target
        if at != n.mul(rows,x):
            raise ValueError('literal CNOT word matrix mismatch')
        for target,control in reversed(word):
            at ^= ((at>>control)&1)<<target
        if at != x:
            raise ValueError('reversed word inverse mismatch')
    print(json.dumps({'status':'PASS_137_SOURCE_FEASIBILITY','all512_dense_sparse_and_closed_columns':True,
                      'source_event':['MOVE',1349,3,601,False], 'event_index':28039,
                      'paired_native_xor':137,'native_sign_mask':9,
                      'fixed_cnot_word_length':len(word),'both_map_words_total':2*len(word),
                      'no_tape_implementation':True},indent=2))


if __name__ == '__main__':main()
