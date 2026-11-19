# Pinned full-output mask audit of the overlapping native tiles

## Exact scope

This is an independent algebraic response audit of Worker A's literal D12/D99 words. It imports no author module and runs no author verifier. It complements the separate physical-owner review: it does not replace checks of every operand's chart, public route and original-owner lifecycle.

The preferred word uses early masks to complete the joint native source basis, late source values w/0 at the six shared donors, and four combined F80 caches. The control uses the same early basis and the same four F80 caches but the unnecessary late values w+v/v. Both use the same full pure-Y transformation. Their pinned decompressed SHA-256 values are:

| Artifact | SHA-256 |
| --- | --- |
| Preferred word | `6096382d0542028f812130d707dbd299de23bbc52a800283ef219f9f9ab45ae7` |
| Preferred certificate | `431033a6d94e43531b2991deb2c4a16c4dada66fd126fa68a3610cf0e8e558aa` |
| Late-mask control word | `9f0cd288c783a55417405e7e78ce97800863e9f8cbda59d9e516f71e5890fd24` |
| Late-mask control certificate | `eed91a2185ba221a5afb81589fbfbe58e53cde5a0a80c14d23dc1c983d7dc198` |

The six shared donors are 5,7,42,43,44,45. Each mask consists of its original field coordinates 476 through 479. These are twenty-four independent original fields, or 120 binary columns. They are not free helper values and their rows are included in the joint early source basis.

## Full response, not a selected receiver test

The separate replay represents every touched original public binary input by its own basis vector. It checks restored original X columns and identity original-Y coefficients, then extracts the proper matrix B on all output coordinates. Untouched public columns and rows are exact identities or zeros by the literal word syntax. Every nonzero five-by-five proper coefficient block is separately checked to be multiplication by an element of GF(32), so the reported field ranks are justified by exact binary expansion.

The preferred word has zero coefficient on all twenty-four mask coordinates at **every final Y output**. In the control, the full mask coefficient matrix has field rank 24, while both displayed receiver projections annihilate it. The complete difference between the two proper maps is supported on exactly these mask input columns and has rank 24. Thus removing the late masks eliminates this response globally; the result is not inferred from equal selected target values.

A source-interface intervention initializes the 96 designated early source fields independently immediately after the native source stage, sets the independent late parities to zero, and replays the common downstream word. Its full response is supported on only the four intended F80 field rows and has rank four. For every active donor, the full and selected early maps have the same rank four and hence the same kernel. The four independent early mask directions at each shared donor therefore satisfy the zero-leakage criterion.

A separate late intervention places 96 independent parity values on their distinct genuine Y injection owners and replays only the subsequent pure-Y gates. It has rank 96 at the full output. This intervention includes twenty-four optional zero parities omitted from the preferred literal word; it describes the larger source interface, with their extra source costs retained if activated. It does not count them as free operations in the preferred invoice. Its image is disjoint from the four clean F80 output coordinates. The combined early/late source transfer consequently has field rank 100.

These interventions explain the observed difference structurally: invertible pure-Y transport cannot erase a nonzero independent native mask injection. No argument about selected-row cancellation can override that full rank.

## Exact proper and return ranks

The preferred proper matrix has rank 76 and 84 nonzero output fields. The control has rank 100 and 100 nonzero output fields. The output support count alone gives only a lower bound on the return rank; the audit computes the relevant principal block exactly.

For any square B, let R contain every row index on which B is nonzero. After ordering R before its complement,

    I+B = [ I_R+B_RR    B_R,Rc ]
          [     0         I_Rc ].

Therefore rank(I+B)=n-|R|+rank(I_R+B_RR). No assumption about the input support or nilpotence of B is needed. The audit applies this identity directly over F2 on the actual compiled bit coordinates.

For the preferred word the 420-by-420 binary principal block is invertible. For the control the 500-by-500 principal block is invertible. Both complete returns therefore have rank **266,400 binary coordinates**, equivalently **53,280 GF(32) field coordinates**, the full original X-bank dimension.

This exact statement is stronger than the earlier support-only lower bounds. Removing the unnecessary late masks leaves the return rank unchanged in this example. A reduced mask response, lower proper rank or cheaper cache invoice does not itself improve rank(I+B).

## Literal operation counts and negative control

Direct word counts and live-cache replay give:

| Word | ADD | INIT | Dirty CLEAR | Extra binary peak |
| --- | ---: | ---: | ---: | ---: |
| Preferred | 47,278 | 380 | 380 | 380 |
| Late-mask control | 49,878 | 500 | 500 | 500 |

Deleting the second tile's contribution from each combined early F80 cache produces a rank-four field mask response. This fault leaves the original-X inverse and original-Y baseline intact, so it specifically tests the required early cancellation rather than triggering an unrelated lifecycle failure.

The preferred finite word still prescribes only four field rows at each of two receivers, on eighteen active donors. Its other responses and full-rank return keep it far from a complete low-return supplier. All five foundational assumptions and the full programme accounting remain unchanged.

## Reproduction

```sh
python3 -B check.py --out OUT
python3 -B native_check.py --author OVERLAP_AUTHOR --out OUT
```

Expected markers are `PASS_EXACT_MASKED_SOURCE_OUTPUT_CRITERION` and `PASS_INDEPENDENT_NATIVE_MASK_CANCELLATION_AUDIT`. `RESULT.json` records the finite algebra domains; `NATIVE-RESULT.json` records the immutable native pins, interventions, operation counts and ranks. The general proof is in `PROOF.md`; source words remain credited to Worker A and their retained native predecessors.
