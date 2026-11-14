# An ambient ceiling for the entire hypothetical even-stage invoice family

**Proved arithmetic consequence under the same declared invoice and helper
interfaces; independent review requested. No new κ.** This does not assert
that any of the unconstructed short callers exists.

Let `f_a(b)` be the free-decoder upper surplus per port in the author proof,
at `t=199/200`, with `b=h−1` and even stage count `2a`, a>=1. The author's
concavity argument shows successive differences decrease with a, and its
geometry argument shows `f_1` strictly decreases with b>0. Direct subtraction
gives the particularly simple first difference

    D(b)=f_2(b)-f_1(b)
        =2(1+4b)^t+2(1+2b)^t-12b^t.

For every 0<t<1 and b>0,

    D'(b)
      =8t(1+4b)^(t-1)+4t(1+2b)^(t-1)-12t*b^(t-1)
      <t*b^(t-1)[2*4^t+2*2^t-12] <0.

The independent integer-root check certifies both `f_1(135)<0` and
`D(135)<0`. Hence for every real b>=135, the first term is negative and
the first successive difference is negative. Decreasing successive
differences imply `f_a(b)<0` for every positive integer a.

Therefore **every integer h>=136 fails even with a free decoder at every
positive even stage count in this invoice family**. At h=135, the
two-stage free-decoder surplus is strictly positive, so136 is the exact
adjacent integer onset of this optimistic all-stage exclusion. This does
not certify a native source, a two-stage caller or enough room for a real
decoder at h=135.

The author's monotonicity of `f_a(b)/b^t` in t transfers the negative result
to every `0<t<=199/200`, equivalently target saving at least1/200 within
that positive-exponent domain. Public endpoint movement and mandatory QUERY
charges remain included. The paired stage family, helper endpoint-credit
grammar, and distinction between native dimension and productive rank are
unchanged. Arbitrary callers and representations remain outside the result.

Author: programme orchestrator for @CubeJerry with OpenAI assistance.
Dependency: Worker A's tensor-native-preflight proof and exact caller pins.
Evidence: independent `check.py` and `RESULT.json` beside this note.
