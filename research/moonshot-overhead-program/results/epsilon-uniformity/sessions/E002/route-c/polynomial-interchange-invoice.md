# Polynomial local execution for the structured characteristic-two interchanger

Status: complete written component composition, independent review pending.
This is a theorem about the interchanger. A whole integer-multiplication
bound additionally needs the numerical Walsh, outer permutations, integer
assembly and uniform common-space selector.

Pins: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, tape
`build/interchange.tex`; programme predecessor
`0607d044d1d09489580da0e5828588820e1a6775`. Sources within that programme:
B's `characteristic-two-label-geometry.md`,
`characteristic-two-order-three-interchange.md`,
`structured-shift-check-refinement.md`; A's power-two count formulas,
rational-height ledger and fixed-field parameter inequalities Q2--Q7.

The E002 suppliers are C's `succinct-cyclic-executor.md` and
`small-radix-batching.md`; A's `HEIGHT-PRICED-AFFINE-STREAMS.md` and
`SUCCINCT-ROW-EXECUTION.md`; and the lead's
`on-demand-spectral-repair.md`. Their independent reviews are recorded
separately. No expanded exponential instruction list is interpreted per
input symbol.

## 1. Finite family and polynomial compact data

For a sufficiently large odd m, use the retained power-of-two-distance
label geometry, with `N<=m^5` labels and rational address dimension
`D_I<=m`. Its complete address maps have polynomial count and polynomial
bit height, as in the predecessor height proof. Complete the list of
required units before choosing the small compatible odd radix by R1.
Then b is polynomial in m and all layouts are valid modulo every b^f.

Take B pairwise-independent ternary shifts, `2m+1<=B<6m+3`, with window
half-width `b_win=5 ceil(sqrt m)`. Let T be the next power of two at least
`2b_win+1`, D_pred=T-1, and u=m-floor(D_pred/2). For m>=4096,

    D_pred <= 24 sqrt(m),     D_pred<=m.                         (I1)

The canonical copied bit-formula and all addition budgets are identical
for every shift beta; no beta-dependent zeros are pruned. Their affine
coefficients alone change. Formula size S and `log w` are polynomial in m,
where w is the completely occupied power-of-two module width. The
polynomial list of path evaluators and their coordinate translations is
constructed without listing w rows.

Use `E=F_(4^e)`, `e=ceil(log_4 B)`, for shift checks. A degree-e irreducible
can be found by the predecessor bounded enumeration in polynomial B time.
One symbol has 2e binary coordinates. Field operations and every compact
row/index coefficient description have polynomial-m cost. The same field
encoding is retained at every spatial and finite-repair recursion depth.

The source's label matrices and endpoint instruction lists have polynomial
size. Even enumerating all directed label pairs, endpoint bases and finite
control combinations costs a fixed polynomial in m. Large optional
frequency verification tables may be generated separately as additive
certificates; no runtime operation consults them.

## 2. Local scalar work without changing spatial calls

Fix a pencil stage. Its coefficient matrix on each shift/module block is
a sum of polynomially many input masks followed by coordinate translations
(C3). C4--C5 apply it in polynomial m work per encoded input volume. Shift
seeds and polynomially many label roles can be serialized by role scans.
Each source shared-pencil operation keeps its prescribed common layout.

The order-three identity

    C_j=Q_j+1_(H_j>N_j),   C_j^2=Q_j+1_(H_j<N_j)

decomposes the affine query stage into one shared-swap pencil plus ordinary
comparison masks in the original physical layout. The coefficient matrices
are applied to the streams already supplied by that shared routing. We do
not execute Q_j separately for each monomial path. The exact number of
spatial interchange calls is therefore the predecessor's number.

Apply the small-shift Vandermonde checks as `H0 tensor I_(32w)`. The
lead's spectral component computes each required small coefficient block
in polynomial m work from m comparison labels. All seed/check dimensions
are O(m), the module coordinate is unchanged, and actual E arithmetic is
charged. Serial small-role scans give polynomial m work per volume.

Comparison labels, sort keys, role tags, path evaluator workspace and
other metadata are **temporary nonrecursive work**. Strip them before
launching every paid spatial or converter child, and regenerate them
when needed after return. Each child receives the original fixed-width
E-symbol payload and its separately charged descriptor. Keeping tags in
child payloads would enlarge the recursive invoice and is not this
implementation.

A's height-priced affine stream theorem implements each triangular
address operation in polynomial m work per volume. General address changes
retain exactly the source's field-permutation calls, with their triangular
parts now polynomially priced. Pointwise comparisons, copied sums, matrix
scans, field arithmetic and head returns all have the same polynomial
nonrecursive bound. Identical field-permutation calls on module rows can be grouped into
one call with that module index as an ordinary prefix spectator. Keep
such a group within a single physical label and one source/target layout.
This replaces several equal-width calls by one call on the sum of their
volumes; their volume-weighted invoice is exactly unchanged. A group
occupies at most one label's fraction of its parent batch, at most 2/N
after leading padding. Since N>=3, this is at most 2/3. It is not correct
to retain the sharper 2/W single-row space ratio after this grouping.

Since only polynomially many label/control types
exist, overcounting all combinations by polynomial m scans is legitimate;
overcounting the recursive calls is not.

## 3. Exact finite-contraction regrouping

Let the predictor row count be

    R = 32 B w,        S=R/32=Bw,

and let `s0=floor(B/32)`. The genuine check rows number `32 s0 w`; append
`(B-32s0)w` internal zero rows to get exactly S. Their coordinates can
be indexed by a check type in [B] and a module coordinate in [w]. The
spectral map ignores padded inputs and returns zero in padded outputs.
Each conversion phase has 2S=R/16 rows.

At finite unrolling height h, parent copies number 16^h. Preserve the
label index. For each group of 16 parent copies, the conversion input
has index tuple

    (copy16, half2, checkB, module_w).

Combine the first two indices into a 32-valued duplicate coordinate:
`dup32=2*copy16+half2`. Permute these finite control fields to the child's
canonical `(shiftB,dup32,module_w)` order. This gives exactly R arbitrary
child rows and hence the next level has 16^(h-1) copies. No module row
is dropped, identified or treated as initialized input. Reverse the same
finite control map after return.

Only the B, 32 and 16^h control ranges are rearranged; the w-coordinate
is an unchanged whole payload. At

    h=ceil(log2(m)/4),    16^h<=16m,                            (I2)

all those ranges are polynomial in m. Serial extraction of every control
type or whole-block radix sorting therefore gives polynomial m work per
volume on a fixed number of tapes. Even an implementation that moves the
module field explicitly can use its polynomial `log w` bit width; no
width-many scans are needed. The direct finite leaves have m ordinary
swaps and polynomial comparison work per row.

There are four child phases, each with 1/16 of the parent payload. They
run sequentially, with scratch intervals reused. Their total mass is 1/4,
and their parked arrays sum geometrically. The final three-transform word
also runs sequentially and reuses its workspace. At most
`4^h<=4 sqrt(m)` finite internal nodes lie at any frontier; the complete
unrolling contains polynomially many control-node types. Thus its full
nonrecursive work and space coefficients remain polynomial in m.

## 4. The recursive-call coefficient, with the new window paid

Write `R_pencil` for the source calls per independent row in one shared
pencil. Under the exact rank-fraction guard, the preceding source invoice
is

    R_pencil <=64 D_I(1+lambda).

The finite full-rate closure, applied to D_pred rather than silently using
the old smaller window, has

    sigma_Q/W <=8 D_pred R_pencil +3m 4^(-h)
              <=2^14 sqrt(m) D_I(1+lambda).                    (I3)

Here W=N R 16^h is the completed row count before optional binary basis
expansion. For I3, I1 bounds the first term by 12,288 times the displayed
quantity, I2 makes the leaf term at most `3 sqrt m`, and `D_I>=2`.
The conservative 2^14 absorbs both terms. In particular
`log W=poly(m)`, although W itself may be exponential in a polynomial.

Use the multidigit split at eta=1: `ell=ceil(log_b W)`. Its padding is at
most two. With `a=D_I-2`, the actual spatial recurrence is

    T_m(e) <= C_m + Lambda_m T_m(f),
    f=floor((e-ell)/(m+2a))<=e/m,
    Lambda_m=2 sigma_Q/W+2a
             <=2^17 sqrt(m) D_I(1+lambda),                     (I4)

for e above the explicit base range. The extra slack in 2^17 is harmless.
Below `ell+m+2a`, direct digit moves cost polynomial m per symbol because
b, ell and a are polynomial in m. The scalar work, fixed-tape dispatch,
metadata removal, finite-control regrouping, and all triangular address
work proved above give `C_m<=m^K` for one absolute K, after increasing a
fixed initial cutoff. Descriptor setup may be kept separately as a fixed
polynomial in m and log of node volume; this is absorbed by the same
polynomial-m volume bound exactly as in the elementary-stream proof.

No step in I4 pays W work per input symbol. The row processor takes the
compact formula and endpoint lists directly. It neither scans an expanded
W-by-W matrix nor uses W physical tapes.

## 5. Uniform parameter margin and all-width interchanger

For inverse exponent slack J>=4 take the retained geometric parameters
`d` a power of two in `[100J,200J)`, `rho_J=1/2+1/(2J)`, and the least
accepted m of the predecessor discrete form. Its exact inequalities are

    log2[D_I(1+lambda)]
        <=3x/d+10d^2 log2(4x),      x=log2 m.

Choose, for example, `x>=2^42 J^3 log2 J`. The proof of predecessor
Q4--Q7 then yields, with its same decreasing log(x)/x comparison,

    Lambda_m <=m^rho_J/2,    log2 m=O(J^3 log2 J).               (I5)

The larger absolute threshold absorbs I4's factor 2^17 and the larger
power-of-two window. All choices and strict margins can be checked by
integer inequalities in the terminating constructor; no real optimizer
or advice is needed. The label guards and the polynomial count of their
exact rational maps are retained.

Divide I4 by e^rho_J. Its recursive contribution contracts by at most
1/2. The base width, base cost and C_m are polynomial m. It follows that
one fixed finite-alphabet multitape processor, given the compact parameter
plan and binary input stream, interchanges two radix-b fields of any
positive width e in

    m^K V max(1,e^rho_J) actual transitions,
    m^K V +poly(m,log(2V)) cells ever visited,                 (I6)

for a larger absolute K. Constants do not depend on the arbitrary prefix,
gap or suffix ranges. Finite exceptional parameter values use the explicit
direct processor.

For binary address fields of u bits, pad each range to the least b^e
above 2^u and then discard the padding at the end. Inflation is `<b^2`,
which is polynomial m. Also e<=u+1. All leading/spare coordinates are
restored by the source partition proof. Thus I6 gives

    time <=m^K V max(1,u^rho_J),
    visited cells <=m^K V,                                   (I7)

after the ordinary fixed-degree descriptor bound and one final absolute
polynomial enlargement. Bits may be embedded once into the fixed E
coordinate encoding, paying its polynomial-m factor; internal recursive
calls retain that same encoding and do not extend it again.

For visited space, finite-repair children shrink by 1/16. Spatial main
children grouped by label shrink by at most 2/N<=2/3. Park their other live arrays at marked
ends and reuse sibling intervals. Before a full-volume reserve call, merge
and clear the main arrays, leaving only its descriptor. The source's
geometric parked-payload proof then gives the polynomial-m coefficient in
I7; the union of visited intervals, not only simultaneously live storage,
is bounded. Counter and descriptor degrees are absolute.

## 6. What has changed and what remains

The preceding expanded compiler gave an exponential-in-polynomial-m local
coefficient. This construction has a polynomial-m local interchanger
coefficient because its row maps, spectral selection, address arithmetic
and radix preparation now use their actual compact structure. Its finite
algebraic identities and recursive-call rate are inherited and explicitly
rechecked, not assumed to become cheaper in the call metric.

The whole multiplication theorem still needs the distinct rational Walsh
processor, precision and outer integer assembly. In particular one cannot
replace its numerical coefficients by characteristic-two coefficients.
Any full-envelope transfer must charge its preparation, invoke a common
visited-space cap, and prove candidate selection and fallback at every
input length. I7 alone does not establish an endpoint or an upper bound
for multiplication.

Credits: Jerry Chen (@CubeJerry); the pinned OpenAI source and earlier
programme finite constructions; E002 Routes A/C and the lead's separate
physical and algebraic suppliers; substantial AI-assisted derivation and
review. No human refereeing, full tape implementation or Lean build is
claimed.
