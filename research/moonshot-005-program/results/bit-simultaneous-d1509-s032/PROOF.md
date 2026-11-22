# Four simultaneous D1509 receivers and a sharp input-change boundary

**Constructive local source/H/D result. Independent review is recorded separately. No complete supplier, canonical return or new κ.**

At programme baseline `2626a0707b56697774c5a9989a095b38458411ee`, S031 supplies one complete D1509 cut at receiver 6 on eleven native donors. This package replaces the eleven source maps by explicit invertible input changes and obtains **four simultaneous native receivers 6, 9, 48 and 73**, on the same H and D words. The entire inverse fibre at each receiver has dimension 8 in each 480-field source bank, with the same identity readout from all eleven donors. All whole H263/H642 interfaces remain exactly unchanged.

This is optimal within the following class: independent invertible linear changes of each source bank, with the original source-quotient and H-output diagram fixed up to those changes. Every five-element subset of the eleven native receivers has unequal joined-fibre dimensions at two donors. The obstruction permits arbitrary whole-bank coordinate mixing and invertible readout basis changes. It does not exclude changing the source quotient tuple or H communication maps.

## 1. Exact inherited interface

Arithmetic is GF(64), represented by GF(2)[x]/(x^6+x+1). The native donors are 0,32,35,38,45,61,62,68,69,90,100. D1509 has twelve geometric receivers 6,9,48,52,54,73,74,85,87,95,98,117. Receiver 117 is geometric only, so the optimality census uses the first eleven. No owner is created there or at geometric donor 113.

A base source bank has 480 fields. Protected coordinates 0..47 and 240..287 form a 96-dimensional direct summand; the remaining 384 coordinates stay fixed. Each source quotient is a genuine paired 30-by-480 map. The input changes may mix both protected copies, so the new maps are not presented as two independent 15-by-240 systems.

For donor j and receiver r, A[j,r] is the complete 96-by-96 protected restriction from original source coordinates to all visible marked proper D input records. It uses actual owner labels, source phase frames and full H phase words. The predecessor source-view and donor-section results make it invertible; this package directly checks all 132 donor/receiver pairs.

Let I[j,r] insert the eight D1509 ingress coordinates into that actual proper-record ordering. Let C[j,r] be the corresponding invertible 8-by-8 section of the unchanged physical D word. Define the oriented preimage

    U[j,r] = A[j,r]^{-1} I[j,r] C[j,r]^{-1}.

Then A[j,r] U[j,r] vanishes on every other visible marked D record, and the D1509 readout is I8. Source/H maps keep the complementary 384 coordinates separate. Because the full 480-dimensional proper left restriction is invertible, this rank-eight preimage is the **entire** isolated D1509 inverse fibre, not a chosen subspace of a larger kernel.

`FRAMES.json.gz`, `PROPER.json.gz` and `READOUTS.json.gz` record exact matrices and owner bindings. The separate independent review reconstructs them from the atlas.

## 2. Constrained simultaneous input-change lemma

Let V be n-dimensional over any field. For donor j, let Cj be a full-column-rank matrix whose image must remain fixed pointwise, and let Uj collect several source preimages in one common parameter ordering. For a proposed common frame L, an invertible Gj satisfying

    Gj Cj = Cj,       Gj L = Uj

exists if and only if

    ker [Cj L] = ker [Cj Uj].

Necessity follows by left multiplication. For sufficiency, send `[Cj L] v` to `[Cj Uj] v`. Equality of kernels makes this a well-defined isomorphism between their images. Extend bases of those two subspaces to bases of V and map the added basis vectors bijectively.

Individual ranks or pairwise intersection dimensions do not establish this condition: [1 0] and [0 1] have equal rank and different kernels. The construction computes the nullspace of `[Cj Uj]`; its parameter projections Pj impose `L Pj = Uj Pj`. Combined equations force part of L. A deterministic completion is accepted only after the full kernel condition passes at every donor. No general-position assumption is used.

## 3. Preserved H cores and a literal four-receiver completion

The protected paired H263 and H642 fibre cores have dimensions 44 and 36. Their union at donor 61 spans dimension 60. Let Cj span the relevant H cores and the old receiver-6 frame. Its dimension is 50 at donors 0/62, 42 at 45/100, 64 at 61, and 8 at each of the other six donors.

For R=(6,9,48,73), each concatenation Uj has rank 32. Combined forced parameter constraints have rank 20 and augmented rank 20. Deterministic seed 0 gives a rank-32 matrix L and eleven invertible 96-by-96 matrices Gj satisfying both equations of Section 2. These are the literal certificate `CONSTRAINED-GAUGES.json.gz`.

The first eight columns of L equal the earlier receiver-6 frame. Each Gj fixes Cj, hence fixes every retained protected H inverse-fibre column pointwise. Extending Gj by identity on the other 384 coordinates also fixes every complete paired H263/H642 fibre, including its width-12 component.

Replace each actual quotient F[j,h] by F[j,h] Gj. Apply the same right composition to the actual early source matrix and every actual late parity. All source phase frames, owner assignments, 280 physical H modules and the physical 35-owner D1509 word remain unchanged.

For common frame Lr, the new proper restriction is `A[j,r] Gj Lr = A[j,r] U[j,r]`. All other visible proper D records vanish and the actual D readout gives the eight parameters. The common space has dimension 8, hence is the whole inverse fibre. This holds simultaneously for arbitrary independent source inputs, at all eleven donors and all four receivers.

Eight existing lane repetitions give four common 64-dimensional fibres at bank 3840. Their joined common frame has dimension 256. These are one source/H/D architecture, not four separately chosen source words.

## 4. Source, H and phase contracts

A common invertible right composition preserves every full source-view rank and every propagation-span dimension. Thus 693 geometric/639 native source views remain invertible, as do all eleven actual 480-dimensional early source matrices. Literal row/owner bindings and changed matrices are provided.

The five earlier structured sources retain paired propagation bound 444<450; the six geometric sources retain 150<450. At bank 3840 these become 3552 and 1200, both below 3600. This invariance does not require the new maps to remain a literal four-edit geometric family.

Since each relevant Gj fixes every entire old paired H fibre, all off-H annihilation and central-H readout equalities remain literal. The 72 geometric/67 native whole H interfaces are preserved. The 11088 other donor/H section ranks survive, but still do not establish common whole fibres at other H centres.

Source changes are real operations: they are included in the actual early matrices and late parities, compiled and charged. No coordinate change, phase restoration or owner permutation is free.

## 5. Exact local costs

The unchanged chronological D word retains its 19 original early caches, late cross block, arbitrary late baselines, actual owners and phase dimensions 19/16. H642 still exports 16 field symbols at gap 6 after eight lane repetitions.

Recompiling the changed source matrices and late parities gives the following eight-lane **gross local replacement** counts, including the verified pure phase inverse words:

| Operation | Four-receiver source | S031 predecessor |
| --- | ---: | ---: |
| Binary ADD | 453,937,608 | 444,189,456 |
| Binary INIT | 279,648 | 279,648 |
| Dirty binary CLEAR | 279,648 | 279,648 |
| Extra gap-6 field exports | 16 | 16 |
| Extra binary MOVE records | 96 | 96 |

ADD increases by 9,748,152. No new communication route or holder is introduced. `PHASE-COMPILER-RECEIPTS.json.gz` binds actual source/H words and counts. The author uses the pinned predecessor compiler on changed physical matrices; this reuse is not independent verification. Separate compiler review is recorded independently.

Pure phase inverses still require global restoration/preload placement. This is neither a complete supplier invoice nor a net saving. At bank 3840 and multiplicity 870, the retained necessary return cap remains 34675 with 16 paid exports, versus abstract floor 34560. No actual global return is supplied.

## 6. Sharp four-receiver boundary

For receiver set R, let Sj(R) be the span of entire inverse fibres at donor j. Every independent invertible source-bank change preserves its dimension. If all donors have identical whole fibres at every receiver in R, these dimensions must agree.

Every five-element subset of the eleven native receivers is checked: choose(11,5)=462. Each has unequal joined ranks among donors 0,32,45,61. In the author's comparison order, 231 subsets are witnessed by 0/45, 168 by 0/32 and 63 by 0/61. The independent certificate uses a different comparison order and the same exact inequalities. Therefore no five receivers can be aligned by independent invertible input changes. With the positive four-receiver construction, the maximum is exactly four in this class.

For example, adding receiver 52 to the constructed four gives joined rank 38 at donor 0 and 40 at donor 32. All eleven native receivers together have dimensions 74 at 0/62, 64 at the six new donors, 80 at 45/100 and 66 at 61.

This gate does not assume preservation of H cores or of the protected block: arbitrary invertible maps on all 480 coordinates preserve the dimensions. Invertible receiver/D-section readout changes alter frames but not inverse-fibre spaces. Field extensions preserve ranks. Under k-fold repetitions all dimensions multiply by k, so arbitrary invertible copy mixing cannot remove a mismatch.

Excluded neither by this theorem nor by the finite census are nonlinear input bijections, cross-donor recoding, genuinely changed source quotient tuples, changed H-output diagrams, extra informative channels or changed isolation requirements. The theorem is a finite diagram obstruction with explicitly proved extensions, not a universal supplier impossibility.

## 7. Open next questions

The next source/H construction must change the incompatible joined-fibre dimensions. Additional input gauges or invertible D readout retuning cannot supply a fifth receiver in this class.

A concrete attempt is an off-D quotient edit on directions invisible to its earlier receiver constraints but visible to a new receiver. It must preserve actual whole H fibres and the four receiver cuts, then pass all source-view, early-rank and nonsaturation checks afresh. Whether coupled changes can complete all donor arrangements remains open.

Other D1509 receivers, other D charts, one hundred remaining native source stars, whole-H compatibility outside H263/H642, K/facet transport, global inverse placement, actual return, both strict suppliers and the full caller remain unproved. All five foundations remain: native_all_columns, owned_erasure, compiler, precision_tape, analytic_recovery. No new complete κ.

Credit @CubeJerry; S031 source/H/D authors and independent reviewers; inherited quadric, Desarguesian allocation, balanced-atlas and compiler contributors. Substantial OpenAI assistance. Apache-2.0. No human or proof-kernel review is asserted.
