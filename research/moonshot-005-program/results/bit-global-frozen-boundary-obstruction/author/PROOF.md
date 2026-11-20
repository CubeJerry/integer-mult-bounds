# Exact obstruction for the fixed native early and late interfaces

Freeze the RS source's pure lanes and early physical visits, all H, D and K words, and the previously chosen pure-Y output basis at the facet. Permit arbitrary GF64-linear maps from the genuine early visits into each facet's output and from each donor's original input into its genuine late-released visits, including arbitrary cross-copy coefficients. Even allowing independent coefficients on each foreign pair, these two classes of changes together cannot realize the full S028 original-coordinate target on **any of its 6,347 flat foreign blocks**.

For a native 480-field copy write \(E\) for the physical early observation, \(L\) for the true late-source response visible in the final facet coordinates, and \(B\) for the unmodified pure-basis mixed response. The possible whole physical blocks have the form

    I₈ ⊗ B + S (I₈ ⊗ E) + (I₈ ⊗ L) R.

The actual late releases occur strictly after the early visits, so a late programming change creates no additional early input for the new facet map. On the original eight copies of \(\ker E\), the term containing \(S\) vanishes. Passing to the quotient by the eight copies of \(\operatorname{im} L\) also kills the entire term containing \(R\). The remaining error relative to the true identity block is the eightfold sum of the maps \(w\mapsto (B-I)w\bmod\operatorname{im} L\) on \(\ker E\). This map has native rank exactly

    rank [L | (B−I)·basis(ker E)] − rank L.

Explicit computation on the physical coefficient arrays gives native quotient rank at least 240 on every applicable edge. Each full target error therefore has rank at least 1,920. At receiver 0 and donor 5, the native early kernel has dimension 300, the late image has rank 180, and the quotient map is injective on the whole native early kernel. The full target error then has rank at least 2,400, even if the programmer can vary the boundary maps separately at every donor and receiver. An exact input subspace here can have dimension at most 1,440. The complete rank census and the raw-order SHA256 are in `output/RESULT.json`.

This obstruction fixes the indicated pure source and output bases and the native routing layers. It permits the boundary changes used in the preceding simultaneous source/facet constructions. Changing the pure output basis, as in the separate full-bank normalization, changes this quotient and falls outside its scope. The argument gives no lower bound for words that may reprogram the frozen layers, or for the unrestricted multiplication exponent.

    python -B PATH/author/check.py --repo REPOSITORY --out FRESH

The verifier accepts the same native early/late caches as the bilateral author. Credit @CubeJerry and the authors of the preceding RS and native layer atlases. Substantial OpenAI assistance.
