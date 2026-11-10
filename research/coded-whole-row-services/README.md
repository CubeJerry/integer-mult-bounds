# Complete coded-row services for the actual recursive Controller

**Publication withheld after overlap review.** This branch is preserved as a
validation/control variant and is excluded from the session's proposed research
contribution links. The earlier
[compiled-row-stock-dispatch](https://github.com/CubeJerry/integer-mult-bounds/tree/5c59d247d51c6e1fca0dead3ed2139b6802b3a15/research/compiled-row-stock-dispatch)
already implements the same Controller callbacks, including a stronger
23-value descriptor and actual geometry/cutoff interface. The original bounded
audit missed its nested vendor export. No foundational-assumption progress is
claimed by this variant. See [the exact overlap review](overlap-review/REVIEW.md).

This package supplies the actual seven-symbol Controller's `is_leaf`,
`prepare`, `install` and `collect` callbacks for a fixed productive width
w>=2 and homogeneous row counts R=w^d. The new local tables check and
preserve complete signed-component rows, stage their real zero-row format
through the existing child header, distribute rows into every productive
field, and collect every returned field before the unchanged occupied-owner
ascent. The mathematical statement is source-relative and proved for all
sizes in this domain. **No new kappa.** All five selected assumptions remain.

The implementation and proof bind the byte-identical Controller retained by
[CrocSwap/integer-mult-bounds#6999](https://github.com/CrocSwap/integer-mult-bounds/pull/6999),
the actual [#5356 Stack](https://github.com/CrocSwap/integer-mult-bounds/pull/5356),
and [#6968 exact scalar tables](https://github.com/CrocSwap/integer-mult-bounds/pull/6968)
for the executable numerical leaves. Base:
`e54523517d0f03e58352e647c403a5af3e525a57`. The accepted certificate at this
base has conditional kappa 0.00363005817; this package changes no certificate.

## What is supplied and what is now physical

One specific protected, nondata payload index g stores a format guide G.
It contains a canonical zero row: virtual bit0 encoded000, and each
component delimiter encoded010. Numerical rows allow000/001 at bit positions
and require010 at exactly the same delimiters. Checking just the physical
length would miss a different same-length component layout. Writing B
literal zeros would destroy the row format; that failure is an explicit control.

The initial guide is supplied, with its production cost F_format(B) retained.
It is not a production e/f/K/rho descriptor. `prepare` physically copies it
to the existing `child_header`; the actual Stack parks G with all other
payload roles; `install` copies it into the current child G. No new tape is
allocated at descent. In the executable binding, g=w and q=w+3: the w
productive fields, G, and two actual scalar work roles.

The graph uses only local reads, writes, unit moves, halt and reject. It has
exactly 273w+125 states, independent of runtime B,R,depth and values. Rows are
striped in the order input row tw+j -> field j, local row t. Collection is
the inverse ordering on all returned fields. Classifying one actual complete
row distinguishes R=1 from R>1 without reading a host depth or row count.
Collection checks component layout and equal row counts across fields; it has
no independent expected returned count. Uniform extra rows in all fields pass
this variant and fail the predecessor's descriptor-count check. Conversely,
this variant rejects some same-length malformed component layouts accepted by
the predecessor's raw-bit router outside its admitted numerical-format domain.
The retained comparison receipt records both directions; neither is a claim
that the predecessor's stated theorem is false.

## Exact costs and scope

For L=RB at a nonleaf boundary, one graph instruction costs one transition:

| Callback | Exact transitions |
| --- | ---: |
| is_leaf |8B+9|
| prepare |9B+8|
| install |13L+4R+R/w+9B+3w+12|
| collect |13L+4R+R/w+4w+4|

Adding every unchanged Controller administrative term gives

    4S+5C+57L+8R+2R/w+31B+38q+27b+7w+136,

where S,C are the actual parent/child occupied payload sums, q the fixed
payload count and b the saved-PC width. This includes classification and
the three callbacks. Numerical child work, literal Controller dispatch,
RET parent tests, root cleanup and input/format/table production remain
separately paid. The proof bounds row-induced historical visits and keeps
all numerical/control/PC backing obligations separate.

Installation/collection individually support any positive row multiple of w.
Complete recursive termination under this stopping rule uses R=w^d. The
selected variable-rank geometry, remainders/padding, changing precision,
production descriptors, semantic native kernels, physical tariff conversion
and full multiplication theorem remain open. Failure can leave partial
output and displaced heads; successful-call correctness is not rollback.

## Reproduce

With Python 3.12 and the standard library, from the repository root:

```sh
python3 -B scripts/research_package.py --package research/coded-whole-row-services
```

Direct scientific checks also work in a Git-free package copy:

```sh
python3 -I -B research/coded-whole-row-services/verify.py
python3 -I -O -B research/coded-whole-row-services/verify.py
```

Expected each time:

    PASS_CODED_WHOLE_ROW_SERVICES 64 7 4160 16

The64 service domains and 16 additional one-row classifiers check exact
counts, complete stripes, inverse gathering, translated prefixes and warm
blank tails. Seven unchanged Controller/Stack runs execute actual SCALE(-1)
leaves on common-width complex pairs, covering57 ordinary boundaries. An
independent complete-word predicate checks all 4160 guide/data pairs of
physical lengths 3 and 6. Sixteen controls cover missing fields, malformed
format, aliases and meaningful graph/cost mutations. A failed collection
explicitly retains54 copied cells, demonstrating the failure-scope limit.

`--write-result` is an explicit receipt-regeneration mode. Default commands
are read-only and compare the frozen typed receipt. Retained sources are
authenticated and executed directly from those bytes, without importing pyc.

The full proof is in [PROOF.md](PROOF.md), source pins in
[DEPENDENCIES.json](DEPENDENCIES.json), and novelty/remaining obligations in
[OVERLAP.md](OVERLAP.md). [NOTICE.md](NOTICE.md) preserves predecessor credit.
The historical WIP checkpoint is retained for recovery and marked as superseded
once the author package is frozen; it is not a second scientific claim.

## Open next questions

1. Bind the actual production descriptor/precision source to G and prove its
   reached stopping domain, with F_format and all metadata transport charged.
2. Extend a named actual variable-rank or remainder/padding call while retaining
   complete component layout and all spectators. Recheck the full budget first.
3. Compose the complete numerical provider registry and graph-clock/pass tariff
   conversion. This row transport theorem supplies neither semantic admission
   nor a new asymptotic multiplication bound.

## Independent lead review

The separate target-only interpreter and mathematical review are under
independent-review/. Normal and optimized replay checks90 domains,10 widths
and4 controls, including changed numerical returns before collection. The
review derives the state count and exact invoices without the author oracle.
This is model-assisted source/mathematical review, not human or kernel acceptance.
