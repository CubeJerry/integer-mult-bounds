# Generic selected MOVE coverage: bounded preflight

## Decision

The selected source family has no central-rank blocker for a generic positive
rank engine: every one of the 6,310 authenticated MOVE events lowers to
`M_left C_r M_right` with positive `C_r`, and `1 <= r <= 8`. A repeated
first-slot positive-C leaf plus fixed slot swaps can therefore cover the
central factor for every observed rank, subject to a numerical prefix
promise. The exact rank census and aggregate monomial census are in
[`CENSUS.json`](CENSUS.json); regenerate it with
[`build_census.py`](build_census.py).

This result is a bounded source gate. #7000 already proves the all-column
algebra for the selected caller, and #6978 already supplies rank-scaled
positive children in a different coded ABI. Thus rank algebra and coded-child
coverage are prior work. The new literal Gamma6/HOME central lifecycle is covered by the companion
`worker-a/research/generic-positive-native-join-gate` package (freeze
SHA-256 `5735c401ba981a7af4d3a146eb047d04fa0c87dbf7ed49bd82dc57df8d6cb2ef`).
Its scope is fixed positive rank 1 through 9 with supplied prefix promises.
This census independently shows the selected archive only needs ranks 1 through
8; it does not audit or re-prove that implementation. The remaining source-specific scope here is
the monomial join for the complete recipe set and its event/owner bindings.
The census adds no full all-MOVE literal program and no `native_all_columns`
admission. Continue only if a source-bound monomial/ABI join is the intended
remaining contribution.

## Authenticated scope and census

The independent root span-set census at `root-work/native-generic-census/NESTED-GEOMETRY.json` (SHA-256 `303463d8c5e87a2af402df05d582d98e487dc6de3d95825ef7934662797ba0b9`) confirms all 6,310 selected pairs are nested and its dimension-difference histogram matches this exact rank histogram. This is corroboration of the finite geometry only, not a compiler, physical, or tariff theorem.

The input is the canonical e545 archive at
`research/shared-wire-split-composition/data/final.json.gz`, Git blob
`74563a7867d9d762b6588f65362369668841bb3e`, 350,722 bytes, SHA-256
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Its full 64-hex-character canonical decompressed word SHA-256 is
`91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097`. This is also the byte-identical
archive authenticated by the published rank-1 and rank-2 binders. The exact
rank-1 event 24472 and rank-2 event 28141 were independently rebound from the
whole archive; both recipes also match a fresh run of the copied exact
compiler. The archive has 6,263 non-private and 47 private MOVE events; the
private marker is ownership metadata, not an orientation bit.

The census loads all 71,261 events and 1,095 frames, extracts all 6,310 MOVE
events, and compiles each of the 2,971 distinct ordered frame pairs once. The
source recipe orientation is `canonical_frame(start).adjoint().then(
canonical_frame(end))`, matching both published binders. For each pair the
compiler returns `U=M_left (C_1^(tensor r) tensor I) M_right`, with positive
central C. For fixed `f`, tensorization preserves this order across the
complete columns; the central factor is `C_r^(tensor f)` and each absolute
monomial phase `i^a` becomes `i^(a*f)`. The private marker never reverses the
transform.

| Positive central rank `r` | MOVE events | Distinct ordered frame pairs |
|---:|---:|---:|
| 1 | 4,075 | 1,824 |
| 2 | 828 | 406 |
| 3 | 811 | 524 |
| 4 | 241 | 130 |
| 5 | 320 | 67 |
| 6 | 17 | 10 |
| 7 | 12 | 6 |
| 8 | 6 | 4 |
| **Total** | **6,310** | **2,971** |

There are no rank-zero, rank-nine, or inverse-oriented central factors in
this source archive. The two existing literal samples land in the census:
event 24472 is rank one (`[MOVE,415,3,99,false]`), and event 28141 is rank two
(`[MOVE,1526,601,470,true]`).

Across the 12,620 left/right monomial factors, the census finds:

| Recipe property | Count |
|---|---:|
| Nonzero affine translations | 5,241 factors |
| Translation support size 1 through 9 | 2,037; 1,033; 840; 584; 383; 173; 162; 23; 6 |
| Nonzero absolute phase | 3,884 factors |
| Absolute phase residues 0, 1, 2, 3 | 8,736; 2,319; 466; 1,099 factors |
| Distinct nonidentity binary matrices | 3,449 |
| CZ quadratic edges, total across factors | 34,039 |
| Single-coordinate phase gates: `S`, `S†`, `Z` | 6,390; 11,891; 16,774 |

All nine-bit translation support occurs, including six full-support factor
occurrences.
Every factor's binary matrix is nonidentity. The polynomial phase records
have dimension nine and contain only the expected Clifford gate classes:
linear `S`/`S†`/`Z`, quadratic `CZ`, and a constant `i^a`. The exact compiler
also records every matrix, offset, linear/quadratic coefficient and constant
in a deterministic full-payload digest in `CENSUS.json`.

## What the existing proofs already supply

The #7000 application review at e545 proves for each selected MOVE that the
exact frame quotient factors as

`U = M_left (C_1^(tensor r) tensor I) M_right`.

Tensoring this fixed identity over `f` columns yields the exact `f`-column
service. The monomial phase becomes `i^(a*f)`, while exterior rational
coefficients remain outside the tensor power. This settles the algebraic
all-`f` lift for the selected source under its stated contracts; it does not
compile or price a literal tape MOVE.

The direct predecessor #6978 at head
`12e58dfdad9371a26f9978c814779da344fd80b4` already supplies a rank-scaled
positive child for `1 <= r <= 8` in its 23-field coded ABI, with child width
`r*f` and the corresponding cutoff check. It covers the earlier selected
#6030 word (3,453 MOVEs and 2,886 distinct chart pairs), not this exact 6,310
event archive. Its proof also leaves the supplier-free monomial join and the
whole MOVE lifecycle obligations explicit. The selected rank-1 and rank-2
literal packages bind only their individual events 24472 and 28141 in a
Gamma6/HOME interface; those are fixed specializations, not a generic
all-recipe dispatcher.

Accordingly, this finite census is not itself new all-column mathematics.
It identifies the additional source-specific literal scope: handle all
2,971 ordered frame-pair recipes, then bind their 6,310 event owners and
chronology to the complete caller interface.

## Literal operations and ABI still needed

The published rank-2 MOVE body hardcodes one pair of binary matrices and
phase polynomials, rejects nonzero offsets, and uses two first-slot C passes
with the six CNOTs of the `0`/`1` slot swaps. Its `compile_word` primitive
accepts a fixed CNOT word, its rank-2 linear source has generic fixed 9-by-9
Gaussian elimination, and its phase compiler accepts fixed 9-coordinate
linear/quadratic recipes. Those modules expose useful building blocks, but
the compiled MOVE remains tied to event 28141.

A source-complete generic extension must add or bind the following recipe-wide joins and caller connections (the fixed-r positive central lifecycle itself is now supplied by the companion package):

1. **All-rank center.** For each `r <= 8`, apply the first-slot positive C
   service `r` times, bringing each selected coordinate to slot zero with a
   fixed three-CNOT swap and swapping back afterward. This is the central
   part reviewed separately by the generic HOME task. Rank guard must be
   `r*f <= cutoff`; checking only `f <= cutoff` is insufficient.
2. **Every affine offset.** The rank-2 compiler currently rejects `b != 0`.
   The rank-1 sample handles only its selected axis-zero reversal. The full
   census requires arbitrary fixed nine-bit `b`, including all-nine-axis
   support. For `|x> -> i^q(x)|Gx xor b>`, bit `b_i` addresses output/native coordinate slot `i` after `G`. For any fixed `b_i=1`, the conjugated sequence `S_0i X_0 S_0i` realizes `X_i`, where `S_0i` is the fixed three-CNOT swap of slots 0 and i and `X_0` is the first-slot reversal. Thus arbitrary fixed `b` has a finite construction-time expansion; each slot swap/reversal still needs its own time, history, and payload bill in the source ABI, in the correct order relative to `G` and the diagonal phase.
3. **Recipe-wide monomial binding.** Generate a fixed CNOT word for each
   authenticated `G`; load the matching `linear_Z4`, symmetric
   `quadratic_rows`, and `phase` into the literal phase body; and bind the
   offset vector. There is no runtime matrix loader in the existing rank-2
   service. Constants repeat by `f`, not once per call.
4. **Event and owner ABI.** Bind each source index, ordered frame pair,
   owner, private/lifetime flag, and chronological input/output role. Preserve
   the complete six-Gamma header, payload, coefficients, spectators, heads,
   private owners and opaque exterior. The rank-2 HOME adapter proves one
   already-reserved owner 1526 packet; it does not synthesize typed INIT,
   locate all 6,310 jobs, transport their packet layouts, or charge the
   enclosing bank.
5. **Numerical admission.** Every central intermediate must be integral and
   fit signed `w` bits; every monomial phase negation must also fit. One simple
   sufficient promise for a rank-`r`, `f`-column direct call is that all
   post-right-monomial real/imaginary numerators are divisible by `2^(r*f)`,
   bounded by `M` in absolute value, and
   `2^(r*f)*M <= 2^(w-1)-1`. Each of the `r*f` positive C axes spends one
   power of two and increases the component bound by at most two; monomial
   permutations and Gaussian-unit phases preserve divisibility and magnitude.
   The symmetric bound also avoids the most-negative signed value. The
   selected caller has not been shown to supply this promise.

The rank-1 and rank-2 packages give complete direct-leaf bills for their own
fixed recipes, including staging, returns, and retained history. This preflight
does not sum a complete generic MOVE bill or a 6,310-event caller invoice.
Even if each fixed recipe gets a uniform direct `O(f*V + E)` implementation,
that rate is still a leaf rate. No faster recursive supplier, full ownership
closure, precision composition, or kappa change follows.

## Exact reproduction

From the workspace root, with the canonical repository object store available:

```sh
python3 -I -B worker-c/research/selected-native-generic-preflight/build_census.py /workspace/scratch/92c9920affc2/repo --write
python3 -I -B -W error publication/native-endpoint/research/literal-selected-move-join/bind_source.py --source-repo /workspace/scratch/92c9920affc2/repo
python3 -I -B -W error publication/rank2-home/research/literal-owned-rank-two-move/implementation/bind_source.py --source-repo /workspace/scratch/92c9920affc2/repo
```

`build_census.py` authenticates the Git blob and canonical word hash before
compiling all distinct pairs. It refuses `-O` because the pinned source
compiler uses assertions as internal exactness checks. The two published
binders each re-extract and authenticate the same entire source archive and
the selected sample event. No full checkout was cloned or downloaded for this
preflight.

## Scope boundary

This preflight supports a generic fixed-recipe literal implementation under
the explicit numerical premise above. It does not implement that full
compiler/dispatcher, verify every emitted tape graph, establish that the
selected caller meets the numerical premise, establish `native_all_columns`
independently of the retained proof, or discharge any of the other four
selected assumptions. The next proof-worthy claim is a complete source-bound
Gamma6/HOME wrapper joining arbitrary compiled `M_left`, positive `C_r`, and
`M_right` for the exact finite recipe set, with all owners, event chronology,
costs, rejection behavior and historical backing accounted for.
