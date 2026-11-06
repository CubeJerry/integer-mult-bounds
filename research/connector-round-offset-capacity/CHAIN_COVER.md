# Symmetric-chain covers reduce the round budget

This addendum retains the interface and boundary-correction proof of `PROOF.md`. It replaces the allocation of one round to each nonempty group subset with one round to each chain in a classical symmetric-chain decomposition. It does not modify the earlier proof or introduce a new physical operation. **No new κ.**

For a group of b sources, define

    W_b = binom(b,floor(b/2)).

The exact minimum number of permutation-prefix chains covering every nonempty subset of that group is W_b. Consequently D groups need exactly D W_b rounds within the literal group-subset prefix-cover model specified below. If `D W_b≤c` and `D+1≤c`, the same correction yields a depth-(D+1) block on `k=Db` sources and

    N(c)≥Db floor(c/(D+1)).                              (1)

In particular, for every integer c≥16,

    N(c)≥c log₂c − (1/2)c log₂log₂c − 4c.                (2)

This improves a lower-order term in the capacity guarantee; the already proved leading asymptotic `N(c)~c log₂c` and the selected multiplication exponent remain unchanged.

## 1. Exact cover size and an explicit decomposition

A permutation-prefix chain contains one subset at each cardinality. It therefore covers at most one subset of rank ceil(b/2). That rank is nonempty for b≥1 and contains W_b subsets, proving the lower bound W_b even when the empty subset need not be covered.

For the matching upper bound, partition the Boolean lattice into saturated symmetric chains. A chain at dimension b has the form

    S_a ⊂ S_(a+1) ⊂ ... ⊂ S_(b−a),   |S_j|=j.

Start at b=0 with the chain containing the empty set. Given such a chain and a new label x, replace its two copies in dimension b+1 by

    S_a ⊂ ... ⊂ S_(b−a) ⊂ (S_(b−a)∪{x}),

and, when nonempty,

    (S_a∪{x}) ⊂ ... ⊂ (S_(b−a−1)∪{x}).

The first chain starts at rank a and ends at rank b+1−a. The second starts at rank a+1 and ends at rank b−a. Both are saturated and symmetric in dimension b+1. They partition the two copies of the old chain: every set not containing x lies in the first chain; the top set containing x also lies there; all remaining sets containing x lie in the second. Since the old chains partitioned the old cube, this construction partitions the new cube. This proves existence and gives a deterministic recursive algorithm for every b.

Every symmetric chain crosses rank ceil(b/2) exactly once. Because those rank sets are partitioned, there are exactly W_b chains. Extend each chain to a full permutation-prefix chain: first list the elements of its smallest set in any fixed order, then list the unique element added at each chain step, then list the remaining elements. Every original chain set appears at its own cardinality prefix. Thus W_b permutations cover all subsets.

For D disjoint groups, perform the same construction within each group. In a round assigned to a group chain, place that group's extended permutation first, followed by all labels outside the group. Every set in that chain is consequently an actual global prefix set. Exactly D W_b rounds suffice; arbitrary permutations fill the remaining c−D W_b rounds.

## 2. Scope of the round-budget optimum

The model for the exact minimum is this: **every nonempty group subset must occur literally as the initial set of a round, and its productive read uses that prefix**. Every round is a permutation of all k=Db labels. The boundary correction is retained separately. Under this rule the family consisting of all ceil(b/2)-element subsets in all D groups is an antichain of size D W_b: different groups are disjoint, so two such nonempty sets are incomparable. One global permutation-prefix chain contains at most one member of this family. Hence at least D W_b rounds are necessary, matching the construction.

This is an optimum for the stated cover rule. It is not a lower bound for all depth-(D+1) connector blocks, all representations with several productive prefixes per group, or all constructions that exploit cancellations between different group representations. It does not determine exact finite N(c).

## 3. Why the inherited correction remains sufficient

A group subset S is assigned to its chain's round r(S). Distinct subsets in the same chain may share a round, but a target mask has only one subset from each group. Different groups have disjoint assigned round sets. In any case the correction needs only the identity

    q_(r(S)k+|S|)=r(S)·1+1_S.

The nonempty group parts of a target mask are disjoint. Summing their productive prefixes and adding the boundary `r₀k`, where `r₀=−Σr(S) mod c`, yields the target mask modulo c with at most D+1 reads. Shared rounds between different target masks pose no conflict: outputs can read at different positions in the same source round and do not change the connector. Source counts, chronological scheduling, dirty cancellation, padding, and disjoint-source concatenation are exactly those already proved in `PROOF.md`. Therefore (1) follows without a new model assumption.

## 4. An elementary binomial estimate

For every integer b≥1,

    W_b ≤ 2^b/sqrt(b).                                  (3)

Here is a direct proof, so no asymptotic approximation or floating-point bound is needed. Put `u_m=binom(2m,m)/4^m`. Then u₀=1 and

    u_(m+1)/u_m=(2m+1)/(2m+2).

Induction gives `u_m≤1/sqrt(3m+1)`: the required step is

    (2m+1)^2/(2m+2)^2 ≤ (3m+1)/(3m+4),

whose cross-multiplied right side minus left side is m≥0. For b=2m≥2, this implies (3) because 3m+1≥2m. For b=2m+1, `W_b/2^b=((2m+1)/(2m+2))u_m≤u_m≤1/sqrt(3m+1)≤1/sqrt(b)`. This also covers b=1.

For context, a matching constant-factor lower estimate is `W_b≥2^b/(4sqrt(b))`. Indeed `u_m≥1/(2sqrt(m))` for m≥1 follows by induction from u₁=1/2 and

    (2m+1)^2/(2m+2)^2 ≥ m/(m+1).

For odd b use `(2m+1)/(2m+2)≥1/2`, and check b=1 separately. Thus `W_b=Θ(2^b/sqrt(b))` with uniform constants. The maximal feasible b for a round allowance x therefore satisfies `b=log₂x+(1/2)log₂log₂x+O(1)` as x tends to infinity. To justify inversion, maximality gives `W_b≤x<W_(b+1)≤2W_b`; hence `log₂x=b−(1/2)log₂b+O(1)`, first implying b=Θ(log x), then the displayed expansion. For fixed D this additionally gives block size

    k=D log₂c+(D/2)log₂log₂c+O_D(1).

The exact estimate (2) below uses only the upper bound (3), not this asymptotic inversion.

## 5. Explicit lower-order capacity bound

Let c≥16, L=log₂c, and choose

    D=floor(L),
    b=floor(L−(1/2)log₂L−1).

Then `D+1≤c`, `1≤b≤L`, and `b≥L−(1/2)log₂L−2≥L/4`. The final inequality holds at L=4 and remains true because the derivative of `(3/4)L−(1/2)log₂L−2` is positive for L≥4. Also `2^b≤c/(2sqrt(L))`. By (3),

    D W_b ≤ L·2^b/sqrt(b)
          ≤ L·c/(2sqrt(L))·2/sqrt(L)
          = c.

The chain construction is therefore feasible. Applying (1), with the same floor accounting as in `PROOF.md`,

    N(c)≥cb−cb/(D+1)−Db
        ≥cL−(1/2)c log₂L−2c−c−L²
        ≥cL−(1/2)c log₂L−4c,

since b≤L<D+1, D≤L, and L²≤c for c≥16. This proves (2) over every integer characteristic c≥16. A constructor may instead take the largest b satisfying the exact integer test `D*binom(b,floor(b/2))≤c`; it can only increase the constructed source count for that D. The logarithmic choice above is an analytic witness, not a required numerical computation.

## 6. Provenance, reproduction, and limits

Symmetric-chain decomposition is classical, not a new theorem of this contribution: N. G. de Bruijn, C. van Ebbenhorst Tengbergen, and D. Kruyswijk, *On the set of divisors of a number*, Nieuw Archief voor Wiskunde, series 2, 23 (1951), 191–193. The publication details and version-of-record location were checked against the authors' institutional record: https://research.tue.nl/en/publications/on-the-set-of-divisors-of-a-number/ . The published scan is linked there at https://research.tue.nl/files/4373475/597494.pdf . The self-contained induction above supplies the precise Boolean-lattice case used here.

The new connection is to the explicit round-boundary correction in this package: one permutation round supports all members of a group chain, reducing the exact cover budget from `D(2^b−1)` to `D W_b` and improving the guaranteed lower-order capacity term. The inherited interface, concatenation and counting background remain CrocSwap/integer-mult-bounds#4231, CrocSwap/integer-mult-bounds#4248, CrocSwap/integer-mult-bounds#6071 and CrocSwap/integer-mult-bounds#6107 as pinned in `SOURCES.json`. Base: `7c49fe32c55de02c2c873655c804b16e4c3fef0a`.

A reproducible constructor follows the displayed induction exactly, extends each chain to a group permutation, assigns consecutive round numbers, and uses the unchanged boundary-correction rule. It should check that the chains partition all b-subsets, are saturated and symmetric, comprise exactly W_b chains, and reproduce each set as a permutation prefix. Literal prefix and dirty-call verification belongs to the package's separate executed checks; this proof note does not claim tests that have not been run. Finite tests corroborate the identities but do not establish the universal theorem.

The source word and output schedule remain explicit, with no probabilistic search. The complete abstract call count is unchanged for the chosen number of sources: cn source calls and c(2^n−1) output calls. Exponentially many outputs, physical input access, helper/frame work, decoder, address, layout, routing, precision, restoration and outer costs remain. The chain optimum concerns only the stated literal-prefix cover class. Exact finite capacity, the optimal lower-order term for unrestricted N(c), and a favorable physical consumer remain open. No selected-frontier assumption is discharged.

Prepared for @CubeJerry with OpenAI Codex assistance in derivation and independent review. Classical chain-cover credit is retained above; no human or proof-kernel acceptance is claimed. Apache-2.0.
