# Wave 3: bounded feasibility map for an encoded balanced CRT inverse

Status: **candidate allocation only; no inverse physical implementation or
new theorem claimed**. Prepared for CubeJerry with substantial OpenAI
assistance. Canonical base remains
`e54523517d0f03e58352e647c403a5af3e525a57`, per the root's wave transition.
The prior scale audit remains superseded; current #7267 Gaussian accuracy
work is not part of this candidate.

## Exact missing implication

At the same #5353 padded source encoding as the newly completed forward
endpoint, construct a one-invocation inverse address-state evaluator using
only encoded topology and actual current coordinates. The intended theorem
would be equality, on the entire admitted padded rectangle, with

    research/unconditional-batched-crt/check_batched_crt.py:
    balanced(values, moduli, reverse=True, compiled=False).

The actual pinned function is retained locally only as a host-level oracle.
Its source SHA256 is
`681e2e3d71fa74c8b9b326f3860104fd9d89590a222e26ae6ee718d1fd40ff2e`,
Git blob `1cf78abccd5e06beecc3ed21ba55f7c03b65fdbc`, at canonical base.
It reverses tree levels, visits nodes at increasing starts, reconstructs
the actual current left child, and negates each right offset before its
padded rotation. CRT.md section 1 explicitly states this inverse factorization.
Those algebraic facts are existing results, not proposed new mathematics.

The new implication would be physical encoded realization on the existing
owned-source interface, paying every current-state read, numerical result,
staging copy, head restoration, write and retirement. It must preserve all
source metadata and historical backing. No host `reversed(range(...))`,
decoded axis count or saved input-size list of prior node calls is allowed.

## Overlap and source distinctions

| Existing work | Established scope | What it does not supply for this candidate |
| --- | --- | --- |
| #4100, canonical `balanced(reverse=True)` and CRT.md §1 | All-padded inverse algebra; host loop over descending levels | Encoded reverse topology and physical node/source lifecycle |
| #4195, `crt-mixed-width-caller` | Logical synchronized forward/inverse tree, declared widths and padded intermediates | Physical uniform source producer/consumer |
| #7152, exact head `66adbede4bd4ab603ba3e0a7f6708403905b753c` | Physical whole-tree forward/reverse micro-row state execution, changing precision, 127 stable roles | Its level/row/node schedule remains compiled geometry |
| #7154, exact head `cc35ecedce6f208d5056fab6d17c58555affc73c` | Encoded forward numerical-node iterator on 78 roles | Reverse level selection and subtractive whole-node values |
| New forward endpoint, local code SHA `c24ae2c90d175d276120438809e7c7401b8a8c04dec139f1b7345e9778984ced` | Uniform forward whole-node source commits, 79 roles | Reverse iterator and inverse numerical producer; root is publishing exact reviewed source |
| #5053, `encoded-current-crt/producer.py` | Actual current-left reconstruction, positive offsets and forward whole-node values | Its updated field uses addition; no direction argument |
| #4169, `crt-arbitrary-source-repair` | Inverse of the raw compact macro S on dirty `(u,t,y)` states, evaluated at actual epochs | This is a different inverse from the complete balanced CRT map |
| #4795/#4982 and later complete repair refinements | Actual finite key service, including raw inverse/ideal switch, at fixed geometry | Uniform balanced-tree inverse on the #5353 axis source |
| #4024, `crt-address-streams`, and #5095 physical sandwich | Bidirectional triangular payload Converter, actual encoded Counts, paid full router and two padding passes | Different source format, traversal and routing premises; not this balanced address-vector interface |

Canonical #4024 must retain its priority as an actual encoded bidirectional
CRT implementation. The candidate must never be advertised as the first
encoded CRT inverse. It also cannot be substituted for #4169's `S^-1` in
`T(S^-1(q))`: that raw macro can modify dirty compact controls and guard
bits, whereas a whole balanced CRT inverse operates on a different state.

The #5095 sandwich actually invokes #4024's inverse Converter after recovery,
but it expects complete payload movement with the Converter's source/frame
contract. A single-vector balanced inverse cannot replace that call. Both
maps agree with coefficient inversion on valid addresses; their padded
extensions need not be identical on arbitrary dirty invalid payloads.

Narrow all-state PR queries for `CRT inverse`, `inverse CRT`, `reverse CRT`,
`subtractive`, `encoded reverse`, `bidirectional CRT`, `CRT converter` and
`balanced inverse` found the listed predecessor chains and no exact new
encoded balanced-source inverse. The search is bounded and does not cover
unpublished work. `SOURCE-PINS.json` authenticates the four main distinction
sources; source/oracle bytes and exact witness pins are in WITNESSES.json.

## Two independent implementation obligations

### A. Encoded reverse-level control

Use the existing physical axis-count/depth manufacture. After #7154's
validated setup, its half-size tape contains one and its depth tape contains
k=log2(d) tokens. A paid pass over all but the first depth token can invoke
the existing physical doubling routine to prepare H=d/2, then restore the
depth head. This costs O(d) local actions and needs no additional role.

Process nodes of this size in increasing encoded start order. At the last
node of a level, consume one depth token and halve H through the existing
temporary counter role by pairing unary tokens. Do not halve after the
final H=1 level. Each level's nodes are disjoint, so increasing starts is
compatible with inverse composition; only the level order must reverse.
The full doubling/halving work sums to O(d). Source and half/cursor returns
must retain their actual predecessor head conventions.

This is an implementation plan, not an established reverse iterator. It
requires a fresh proof of startup, parity/divisibility, current cursor,
termination, final-node cleanup and decreasing-precision reentry. A source
diff must explicitly identify changed methods; existing frontend byte pins
must not silently be reused for modified control.

### B. Subtractive whole-node numerical production

At a node let k_A and c_i be the existing #5053 actual-current-left result.
The inverse target value is

    y_i = (x_i-c_i) mod s_i,  x_i<s_i;
    y_i = x_i,               x_i>=s_i.

If any left coordinate is invalid, k_A=0 and all offsets are zero as before.
The existing `Arithmetic.subtract` already implements modular subtraction
on the admitted `0<=x_i,c_i<s_i<2^(P_G-1)` domain, preserving the high-bit
margin. Replacing the final forward addition with that routine appears
sufficient. Every new source and the changed line need explicit pins and
credit, with its simultaneous-word census and retirement rechecked.

The forward endpoint's projection/retire/commit code can then be reused
unchanged: both inverse branches still return a value below 2^h_i, so its
high-bit validation and source-shape preservation remain applicable. The
inverse numeric contract and reverse schedule are distinct obligations;
neither one by itself establishes the complete inverse source endpoint.

## Optimistic complete budget before allocation

Let A=sum h_i, M=2+3A+4d and P_G=1+sum_(i in G)h_i. The candidate target is

    T_inv <= C_inv(M+2)^2 + 4096
       + sum_G [2^21(P_G+2)^4 + 2^16(P_G+2)^2 + 4096].

The deliberately doubled numerical coefficient is an optimistic safe target
pending the subtractive provider's loop/ownership audit, not a new proved
tariff. Setup and halving add O(d); per-node source staging, update and
retirement add O(M+n_G(P_G+2)); summing those terms remains O(A^2).
Near-equal widths retain the geometric sum O(A^4) for the numerical work.
Thus O(A^4) complete source time is feasible without dropping helpers.

Expected owned roles are the same 78 frontend/numerical roles plus one
staging role. The candidate retained-backing envelope is the forward one:

    K_source + B_num + 8(P*+2) + 6(d+2) + (A+2) + M,
    P*=A+1,
    B_num=(P*+1)+2(2A+2d+2)+57(P*+2)+3[d(P*+2)+2].

Counting the staging role's visited span uses M+1. Other roles retain the
source model's explicit backing convention. These bounds are for **one
inverse invocation**. Constructing a fresh forward evaluator and a fresh
inverse evaluator for a round-trip test retains two sets of 79 histories;
it does not prove same-bank restart or a 79-role bidirectional lifecycle.

This helper budget does not improve the full selected multiplication bound.
Applying the available O(A^4) helper independently to every payload record
would not fit the desired fast conversion bill. Full payload movement,
exception-key composition and all selected hypotheses remain uncharged
until an actual compatible caller is supplied. No ROM/micro-row cost can
be removed merely because the complete address inverse is computable.

## Bounded discriminators already established

Using only the frozen host caller, the search visited 65 of the 1,024
padded tuples for moduli (2,3,5,7), widths (2,2,3,3), stopping at the first
wrong-level-order witness:

    input                   (0,1,0,0)
    actual forward          (0,1,2,1)
    correct inverse         (0,1,0,0)
    subtract in forward order (0,1,0,1).

A second witness prevents a global-invalid identity shortcut:

    balanced inverse of (1,3,1,1) is (1,3,1,5).

The invalid coordinate disables its own relevant node but does not make
the entire padded rectangle pointwise fixed. No untouched search region
is reported as covered. These are source-bound controls, not a universal
proof of a new program. Reproduce with

```sh
python -I -W error -B verify_witnesses.py
```

from this directory. Expected:

`PASS_INVERSE_CRT_FEASIBILITY_WITNESSES visited=65 domain=1024 controls=2`.

## Allocation and stopping gates

Recommendation: feasible **narrow enabling follow-up**, below an uncovered
selected-caller obligation in priority. Its novelty is specific to the new
balanced source interface, so do not expand it merely to obtain another PR.

Before implementation, root should confirm this exact scope is still
unclaimed and pin the newly published forward endpoint. Stop or redirect if
a predecessor already supplies an encoded reverse iterator on the same
source, if a broad claim would merely repeat #4024, or if a supposed actual
caller needs raw compact S^-1 rather than balanced CRT inversion.

If allocated, first execute one four-axis reverse path with actual numerical
subtraction and observed decreasing precision. Then prove the full encoded
loop/lifecycle and independently test both inverse compositions over a
bounded padded family, with actual source histories counted. Stop on any
host geometry decode, stale left-state reuse, hidden fresh owner allocation,
unpriced source conversion or numeric-width expansion. Retain all inherited
compiler/native/precision/analytic assumptions and claim no new kappa.
