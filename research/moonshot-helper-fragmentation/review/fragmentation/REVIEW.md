# Fresh independent review after environment recovery

**PASS for the scoped mathematical results. No new κ.** This is a newly
executed verification, not a claim that reconstructed files retain historical
hashes. Canonical base is `e54523517d0f03e58352e647c403a5af3e525a57`.
The source invoice is authenticated by Git blob
`ff3256f0d3ffbfc56b062f9ec0fdbbc7b30e76d5` and SHA256
`d9ba709fa5dcefffe3f3abdcf34600ce188224703cfd743e6db8b58ba4816cb7`.

Original T/P counts are 23,392/117,612 and rank masses 321,364/319,844.
Each of 18 native occurrences has 1,080 original helpers of total rank 7,650;
there are 3,952 fixed root targets. Descendants of an already split selected
helper are not silently recombined into an earlier historical ancestor.

## Independent sharp dual proof

At t=199/200, the positive extra-field price is
`lambda = 3*3^t - 4^t - 5^t`. For all 96 integer partitions p of ranks1..9,
the code proves `sum(s^t)-r^t-lambda*(len(p)-1) <= L_r` by exact integer root
enclosures at denominator10^24. Maximizers are unchanged ranks<=5 and
balanced binary ranks6..9; (3,3,3) ties (4,5) at rank9 symbolically.

Summing gives a bound for **at most q** extra fields, justified by lambda>0.
It is negative at22,953 and positive at22,954, with an explicit attaining
partition. Thus22,954 is the sharp threshold, not a numerical greedy result.
The repeated-native lower bound follows from q=18*1275, while18*1276 is
attained by `{1:13,2:18,3:1808,4:408,5:109}`. Exactly554 rank-nine helpers
become3+3+3, the remaining41 become4+5. Mass and target counts are checked.

## Continuum binary obstruction

Concavity makes balanced binary pieces optimal among at-most-two-piece
integer partitions for0<t<1. Let d be that optimized T minus unchanged P.
The moment is negative at t=199/200. All24 logarithmic tails
`sum(s>=r) d_s log(s)` are strictly positive, proved by exact integer products.
Abel summation then gives `sum d_r log(r) r^t > 0` for every real t>=0.
Hence the moment decreases with C=1-t, excluding C in[.005,1) in this class.
No sampled-exponent extrapolation is used. Direct sums preserve negativity;
products preserve T_t<P_t when each positive-mass factor has that inequality.
Post-product repartitioning is excluded.

## Reproduction, controls and limits

```sh
python3 -I -B independent.py --source source/FULL-RESULT.json
python3 -I -O -B independent.py --source source/FULL-RESULT.json
```

Expected marker: `PASS_INDEPENDENT_DUAL_ABEL_REVIEW`. No author scientific
code is imported. The dual proof differs from resource-allocation sorting.
Explicit exceptions survive optimized Python. Controls expose duplicate old
helper credit, omission of100 paid rank-one jobs and a wrong dual multiplier.

Positive raw moment does not construct independent physical outputs. The
root, paid calls, helper identities and rank mass are fixed. Cross-helper
repartitioning, new unpaid fields, changed interfaces and arbitrary
post-product refinement are outside scope. Ordinary work, ownership,
precision, compilation and BIT compatibility require an actual construction.
All five foundational assumptions remain. No multiplication theorem or
general κ=.005 impossibility is proved. Prepared by a separate OpenAI Codex
reviewer; retained source authors keep their credit.

## Fresh authored-byte signoff

The regenerated author proof was read in full; balanced-partition smoothing,
concave perspective, chain-prefix optimization, strictness and Abel summation
are valid in the stated scope. Author normal/-O replays also passed. Reviewed:

- PROOF.md SHA256 `c45cee8c176e604f00549d83e068d73f45c78bf47b7b04e5b288416fd788ac33`
- verify.py SHA256 `8dd13bccc6837a1193473fc3910356518779db01db0339a6c92adb53011602b6`
- RESULT.json SHA256 `beff900e537159c18c0e1c331aa4d7067e6c9ebd8ab4a89de64f00d533340d7a`

Independent normal/-O receipts are byte-identical. The independent source
is intentionally separately implemented: binary-search roots, a sharp dual
certificate over96 partitions, and exact integer-product tails.
