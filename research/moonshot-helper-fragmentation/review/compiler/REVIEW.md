# Fresh independent compiler arithmetic review

**PASS as a sufficient arithmetic specification, conditional on unbuilt
native and BIT suppliers. No new κ.** The canonical invoice is pinned to
main `e54523517d0f03e58352e647c403a5af3e525a57`, SHA256
`d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`.
The reconstructed independent engine and receipts were rerun after recovery;
their bytes are new and not identified with earlier historical hashes.

## Accounting implication

The hypothetical repeated1,276-extra native replaces, rather than duplicates,
the old helper credits. Its complete profiles have46,360 targets and117,612
paid calls, masses321,364 and319,844. An actual word exposing arbitrary
independent targets is still required.

For product power v, specialize every target below L to an owned zero input,
execute the entire product word including every paid child, and erase only
its zero complete output. All lost target moment is debited. This uses an
all-column independent-output contract; intermediate values need not vanish.
There are D removed positions and2D additional initialization/erasure events.
For positive offsets u,w with u>=C, product paid splitting and target loss
are bounded by

`P_t^v + 2 J^-u P_(t+u)^v + L^w T_(t-w)^v`,

where t=1-C. With J=c^v,L=b^v this is strictly below T_t^v if
`alpha^v+2 gamma^v+lambda^v<1`. The ratios include every paid job and removed
target. Positive separated moment also gives positive rank surplus because
retained ranks are at least L and paid ranks at most J, with L>J.

## Independent exact checks

At C=.00500007, v=1920,c=11,b=12,u=w=1/7, the independently recomputed ratios
satisfy

| Ratio | Proved rational upper bound |
|---|---:|
| alpha=P_t/T_t |12499990009/12500000000|
| gamma=P_(t+u)/(11^u T_t)|19/20|
| lambda=12^w T_(t-w)/T_t|977/1000|

The exact Bernoulli/geometric bound is below999/1000. The actual ambient is
153^1920, even though the largest single target is145. Using theta=28/29,
the independent logarithmic inequalities prove p=1377, while p1376 fails.
The integer threshold H=5839800000000 satisfies
`(H+1)^1377 < 2^58398`; the preceding10^8-spaced grid point fails.
The uniform loss1e-8 leaves .00500006. These numbers are a conditional
compiler specification, not an admitted provider or assembled theorem.

The independent arithmetic uses60-digit fixed-point integers,100 positive
atanh-series terms plus a rational tail for log, and100 Taylor terms plus a
rational geometric tail for exp. Every rounding is outward. Author numerical
code is not imported. Normal/-O results are byte-identical.

Controls show the unchanged original invoice fails, the named old-completion
bound exceeds one, p1362 computed with false ambient145 fails with153, the
previous p/H fail, and a separate toy changes surplus sign when lost targets
are correctly debited. The u<C control rejects an invalid splitting bound.

## Reproduction and remaining obligations

```sh
python3 -I -B independent.py --source /path/to/FULL-RESULT.json
python3 -I -O -B independent.py --source /path/to/FULL-RESULT.json
```

Expected marker: `PASS_INDEPENDENT_COMPILER_SPECIFICATION_REVIEW`.
`arithmetic.py` is the reviewer's independent arithmetic module.

A physical repeated1,276-extra native and compatible covered BIT saving
.0050001 are unbuilt. The product needs actual new target/paid/field/operation
counts, owned banks for every specialized input, and paid copying, routing,
erasure and precision. No old ordinary constant may be reused automatically.
Raw occurrence count is `sum(i=0..v-1) B^(v-1-i) p0^i`; paid splitting does
not remove its work. The inherited source-grid and compiler contracts must
apply to the new word and every unbounded input size. All five foundational
assumptions remain. These checks neither prove the native nor bypass BIT,
source access, tape, precision or the final outer theorem.

Prepared by a separate OpenAI Codex reviewer. The target-restriction method
and canonical source authors retain their predecessor credit. Fresh authored
specification byte signoff follows below after reading its restored text.

## Fresh authored-byte signoff

The restored specification and checker were read in full. Author normal/-O
replays passed with identical output. The raw-margin and logarithmic-margin
decimal lower claims also pass independent rational comparisons. Reviewed:

- COMPILER-SPECIFICATION.md `7b6630be0a48438de543b8295ff52af15f8dc9968673d30cd712705ec17abb3f`
- compiler_certificate.py `7cd3d3be42e1121ace82b1fd9222cf8a0719bb815f77b1c7d2871dc7135393fc`
- COMPILER-RESULT.json `19b227e2f81befa0a9688b8fa5d06e6d3dc668152e4d6e90eaa66f775b63356c`

The separate two-stage BIT and54+4 outer-row claim is explicitly bound to
published commit `a169504af5d7a394424bb19b10d58f1d1b5d1fce`, package
`research/bit-target-bootstrap`. Its proof was read: covered BIT .0050001,
ordinary B=.00500007, complex U=.00500006 and outer g=1e-8 match this
specification exactly. That package supplies the separately verified outer
gate evidence; this review's local arithmetic script does not claim to rerun
those58 rows. There is no numerical addition of κ gains or change of model
in the join. Both physical suppliers remain unbuilt.
