# Selected boundary scales and the existing exact scalar tables

**Decision: stop a new scalar-algorithm task as covered.** Existing #6968
already supplies literal exact SCALE for every fixed nonzero rational,
including 1125 and 1/1125. Restricting rounded ADD to divisible inputs or
factoring 1125 supplies no new scalar theorem. This is a bounded source/ABI
audit and an unclaimed next-wave integration proposal. No new kappa.

## Sources and overlap

Canonical base: `e54523517d0f03e58352e647c403a5af3e525a57`.

- [#6968](https://github.com/CrocSwap/integer-mult-bounds/pull/6968), exact
  head `13193a22b1070a74a8580c5d3ea27470443f815a`, provides
  `research/current-scalar-flat-tables/{PROOF.md,tables.py}`. Its constructor
  remains byte-identical in main: SHA256
  `654e9734ef80a9394807ca508543b1bc164afb5768d23d0e5a88c790d2f13bac`,
  Git blob `1cc22f75fbe53d48b84be42782e581c04820cd49`.
- [#6990](https://github.com/CrocSwap/integer-mult-bounds/pull/6990), exact
  head `38cd824c60f2bb5c6f2603f848a9487cb3a57965`, provides compact rounded
  ADD. Main's constructor SHA256 is
  `fe8a28fd523ebb7ec78dce4ba0855b3070a6cbff470602cd62f8d3ff445e0f0a`.
- [#7268](https://github.com/CrocSwap/integer-mult-bounds/pull/7268), head
  `618ff7af4ac85c63ee2c39acc69bf763ed35b60a`, reduces the signed-residue
  graph to linear size. Its executable still limits odd denominators to
  125 and coefficient lengths to 24; it does not install unscale-1125.
- Selected application review, main's
  `docs/research/pr-intake-evidence/pr7000-application/PROOF-REVIEW.md`,
  SHA256 `4501502c2ceb9759b20372435fe4beb51082c5a5e2910c1fd5dbe6edca415055`,
  §§4--6 gives S=1125, 53,280 boundary conversions, common fractional
  width F=p+D, signed width W=p+h+2D+3 and temporary width W+26.

These proofs, constructors, source binder and newer residue PR were read.
The targeted PR search was bounded and is not exhaustive novelty evidence.

## Permitted arithmetic and exact success

For reduced q=a/b, b=2^d o, o<=125, #6990 computes
`x+floor((a*y+floor(b/2))/b)`. If b divides a*y, its result is exactly
x+a*y/b, because `0<=floor(b/2)<b`. This is an immediate specialization
of the existing theorem, not a new divisibility result for selected inputs.
It is binary ADD on distinct target/source fields, and 1/1125 is outside
its executable odd-denominator domain. It is not a unary SCALE provider.

#6968's `compile_scalar('SCALE',q)` already accepts every fixed nonzero
rational, without that odd-denominator restriction. Its finite carry tests
exact divisibility and final signed fit directly, without an overflowing
same-width intermediate product. Both q=1125 and q=1/1125 have d=0 and
the published carry bound 1126. The graph is fixed before input widths vary.

The selected exact common-grid/range induction supplies the numerical
success conditions at its scalar cuts: entry scaling is integral and the
completed unscale is exactly divisible by 1125 on the retained grid. No new
scalar numerical assumption is needed. Actual native returns, common-format
presentation and physical ownership remain the selected inherited premises.

## Representation, owners and complete cost

The exact ABI is a nonempty complete complex field with a positive even
component count, positive component widths, signed little-endian two's-
complement components, virtual delimiter 2, canonical three-bit physical
codes and an actual physical blank frontier. SCALE has one public target
and two distinct owned work roles (staged output and rewind guide). Public,
work and contexts start at their origins. Protected LEFT markers, ancestor
separation, and contiguous old raw-binary work prefixes without hidden
nonblank cells beyond their frontier are explicit premises.

Whole-field staging precedes any target write. Success installs on the
original owner with unchanged delimiters/extent, restores heads through the
unchanged executor and physically retires work through the primitive wrapper.
Failure preserves public contents but may leave work/heads dirty. No failure
rollback follows. These are inherited theorems, not replayed here.

Let B be data-bit count, R component count, L=B+R and V=3L the coded
physical extent. With blank work, #6968 charges
`1024(d+2)(L+1)` physical cell actions plus executed rows. For both required
scales this is **2048(L+1)**. Add positive entry retirement of dirty work,
borrowed-context/head costs, source authentication and finite table setup.
All 53,280 conversions need the sum over their actual extents/dirt/contexts.
Historical output/guide capacities remain separately retained maxima, with
current extents V and V+3; public, context, ancestor and controller backing
remain charged.

For uniform W and R>=2, the core `2048(R(W+1)+1)` lies below the selected
`2^20 R(W+26)` arithmetic allowance. This comparison does not pay omitted
codecs, source/owner dispatch, dirty prefixes, contexts, or a different
machine-cost convention. No old invoice cap is automatically transferred.
The new outer phase/egress uses raw MSB-first common-width components and a
Gamma header; this scalar service uses coded LSB-first delimited fields.
Equal numerical values do not supply an executable format conversion.

## Exact remaining join and unclaimed proposal

The #6968 installed source binder covers the older #6030-derived caller:
366,842 scalar sites and 42 operation/coefficient pairs. `source_literal`
recognizes only authenticated `local`, `boundary-left`, `boundary-right`,
`outer`, and `query-add` origins after named wrappers. It explicitly bounds
outer/boundary columns by 104. It is not an installation of selected #7000's
native entrance-scale and exit-unscale events. The selected review describes
and counts those operations; it does not turn the old binder into a current
emitted wrapper registry.

**Proposed bounded lemma, not started or reserved:** for one exact selected
native-call interface, emit and bind each entrance scale and exit unscale
with its pinned source, actual call occurrence, direction and public port.
Use the existing SCALE tables on the actual physical owner. Prove exact
chronological bracketing, owner preservation, common-format and grid/range
admission, and the summed setup/lifecycle/codec bill. Extension across the
finite selected catalogue must recount 53,280 genuine boundary operations.
No scalar algorithm should be replaced or re-proved. First compare against
the lead's active actual compiler-word work and obtain the real emitted call
tuple; invented tokens or a numerical histogram are insufficient.

The correct present conclusion is that scalar arithmetic is already
available, while selected occurrence/owner/format installation remains a
separate source-bound join. A package containing only the divisible-input
observation or factoring 1125 would repeat settled work.

This audit stops here. No worktree edit, new kernel, table catalogue,
physical replay, selected cold replay or upstream PR was made. All five
selected assumptions and kappa 0.00363005817 retain their status. The
integration proposal is unclaimed pending overlap allocation.

Prepared for @CubeJerry with substantial OpenAI assistance. Credit #6968,
#6990, #7268, the retained lifecycle/scalar predecessors and selected #7000
authors. This audit records a reduction and remaining interface, not their
theorems as a new contribution.
