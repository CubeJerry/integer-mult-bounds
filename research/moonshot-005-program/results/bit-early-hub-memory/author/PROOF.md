# An exact chronology obstruction to an X-only early-Hub split

**Proved under the stated interface. No new κ.** This closes a naive early-Hub repair of the shared-facet construction, while leaving retained stationary caches, earlier X-to-Y copies, feedback and further global formation open.

## 1. Precise interface and statement

Let nonzero real source lines L_j=span(r_j) and target facets F_j=r_j-perp lie in a positive-definite real space. Inputs consist of b independently valued width-V original X banks at each L_j and b independently valued original Y banks whose X-dependent parts are initially zero. The payload field k is arbitrary.

Before a cut τ, the only X-dependent state is in the original X banks. They undergo arbitrary invertible linear transformations among cocharted groups, with arbitrary noncommuting block coefficients, and move only to containing charts. This gives an invertible current-X matrix P relative to the original independent X inputs. Original Y banks have not received any X-dependent information. Zero or pure-Y auxiliary state is harmless; any retained X-dependent state outside the original X banks is excluded.

At τ, form a fixed global row space H from the original X banks currently at Hub. Grant arbitrary copies and availability of any row in H; this is stronger than limiting H to canonical rank9bV. After τ, no additional X-dependent global information may be formed from later Hub arrivals. All remaining non-global information propagates only by cocharted linear operations and moves to containing charts. In particular a new downward helper carrying fresh X-dependent information is outside the interface.

**Theorem.** If any original X bank remains below Hub at τ, this interface cannot complete all original target maps Y_j↦Y_j+X_j. This holds for every k,b,V and every finite monotone X recoding word, regardless of its cross-root mixing or its number of local ADDs.

The theorem does not assume a rank bound on the fixed global space. It is a causality/source-access obstruction. Its no-side-memory hypothesis is essential and substantially narrower than the actual programme's sources, which use many retained caches and earlier feedback copies.

## 2. Inverse-column geometric locality

Write z=P x for current X values, and W=P^(-1). The block column W_a maps a perturbation of current bank a back to the original X coordinates.

**Lemma.** If original X bank a is currently at chart C_a, every original role j in the support of W_a has L_j⊂C_a.

Initially W=I and the statement is immediate. A monotone MOVE enlarges C_a and preserves the support inclusion. For an elementary ADD a→c with block coefficient A, the inverse update changes column a by the appropriate composition of column c with −A; a and c are cocharted, so their union support remains in that common chart. An arbitrary invertible cocharted transformation similarly replaces the corresponding inverse columns by linear combinations of columns all supported in that chart. No commutativity or scalar coefficient premise is used. Induction proves the lemma.

This is a statement about inverse columns, not just forward payload rows. Confusing the two would miss the causal obstruction.

## 3. Proof of the theorem

Choose a below-Hub bank a at chart C. Give it a nonzero width-V perturbation v, set every other current X perturbation to zero, and let w=W_a v be the resulting original-input perturbation. Since P is invertible, w≠0. By the lemma, every nonzero original block w_j has L_j⊂C.

All τ-Hub X banks have zero perturbation, so every fixed global row in H has zero perturbation. By hypothesis no side memory or Y bank has an X-dependent perturbation at the cut. Thus the only initially nonzero local perturbation is at C. Inductively any post-cut local record that acquires nonzero perturbation lies at a chart containing C: cocharted linear operations preserve this cone, and permitted local moves enlarge it. Globally distributed records have zero perturbation and do not create an exception.

A final Y_j can therefore be perturbed only if C⊂F_j. But required identity completion demands output perturbation w_j for each nonzero original block. For such j, L_j⊂C, whereas L_j is not contained in F_j because r_j·r_j>0. Consequently C cannot be contained in F_j. Every required nonzero target perturbation is forbidden, a contradiction.

## 4. Exact finite control and relationship to the local MDS source

The checker tracks inverse X columns independently through every X-to-X ADD of the actual four-binary-copy shared-facet word, checking support against the real source charts. It does not reuse the word author's state replay. At the chart-aggregate cut,440 independent X banks are at Hub and4 original pivots remain below it. Canonical C has dimension36 and its intersection with the actual Hub row space has dimension32. Each retained pivot's inverse column is explicitly listed and lies in its proper chart; its canonical projection is nonzero.

At local-correction completion all444 original X banks are at Hub, so their encoded row space already contains all36 canonical dimensions even before the inverse restores the original named values. The construction therefore distinguishes arrival at Hub from restoration. Its Y banks have already collected X information before the first cut, so the local word is a positive example **outside** the theorem's premise, not a source rejected by it.

A simple scope control is to allow fresh global formation after the cut: let all original X banks reach Hub, copy all their independent values into paid globals, and descend them to waiting Y records. This can realize the identity but violates the frozen-global premise and has the full source/transport cost. Likewise, pre-cut stationary owned caches or earlier X-to-Y copies can carry the selected inverse-column perturbation outside the single future cone; they require their actual paid source histories and cannot be treated as zero information.

The next positive repair must exploit such retained memory or earlier receiver interaction, or explicitly pay a later global route. No lower bound on the amount of necessary side memory is asserted here, and no unconditional shared-facet or multiplication impossibility follows.

Reproduce `python check.py --repo REPO --source PATH_TO_SHARED_FACET_PACKAGE`. Credit @CubeJerry, the persistent programme and native source predecessors; root's early-Hub interface question and Worker C's inverse-column proof; OpenAI assistance.
