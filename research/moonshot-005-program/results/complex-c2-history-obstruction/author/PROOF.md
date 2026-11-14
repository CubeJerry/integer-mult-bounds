# A preterminal history obstruction for eight dimension-two Gram returns

**Author theorem and exact source certificate; independent review pending. No new kappa.**

This closes a specific continuation of the complex source. It does not prohibit genuinely recoding the source, retaining another target code, changing the communication model, or charging a different complete invoice.

## 1. Precise source and question

Let Q be the actual standalone 400-input complex rail, with the 31 terminal coordinate returns deleted at the exact `consumer.begin` boundary of the pinned parent. It has 4,779 instructions. Its original-input hosted reverse residual has rank 82, not eight. Q4 is the literal eight-ferry/four-pair source with exactly those same old returns removed; it has 5,851 instructions and also residual rank 82. The frozen words, native source and complete caller are pinned in `check.py` and `price.py`.

The current question was whether passive preterminal observations from these old histories can realize the previously hypothetical eight rank-seven returns born at dimension-two charts. The answer below is negative for the **canonical hosted Gram demand** under the declared source-history model, even if an arbitrary global initial B preload is granted for free to create that demand. This is not a claim that rank 82 equals eight or that a free preload is physically available.

The 400 independent original inputs consist of the first-X/first-Y bank and 96 hosted B,D pairs. Let H be the row space of all 200 actual final Hub records of Q or Q4, after stripping. Exact replay establishes:

1. H has dimension 200;
2. every original D coordinate survives reduction modulo H unchanged;
3. **every actual historical Hub row, including owned rows before their retirement, already belongs to H**;
4. the desired hosted corrections modulo H have dimension 82.

Point 3 is essential. The argument does not silently discard a useful earlier Hub observation. It grants all of H globally and from the beginning of the computation, a stronger interface than chronological access to those Hub rows.

Let G be the normalized Gram matrix on the 96 actual hosted E8 roots, and let W = row(G), embedded in the D coordinates of the 400-input space. Its rank is eight. The source frame `(5,56,65,69,77,96,100,103)` is exactly orthonormal and supplies an eight-row basis. H intersects W trivially because D coordinates survive the chosen quotient unchanged.

## 2. The generously relaxed local history spaces

For each two-dimensional binary chart C in F_2^9, define L_C in the quotient by H using the following generators.

* Include every actual record value at C at any point in the old source, including every local update of a public or owned record.
* For every actual MOVE A to B, include its current payload at C whenever C lies between A and B by subspace inclusion. This permits inserting C as a stop inside that MOVE.
* Grant immortal local copies and arbitrary linear combinations of every such historical value at the same C. Grant their birth, storage, arithmetic and cleanup free.
* Grant **all** such virtual refinements together, even if different choices would require incompatible retimings or different routes for the same record.

An inserted stop changes no payload unless additional source recoding is supplied. This is a relaxation of passive copying, not permission to create new local information or to alter the payloads of other old MOVEs arbitrarily.

There are exactly

    ((2^9-1)(2^9-2))/((2^2-1)(2^2-2)) = 43,435

two-dimensional charts. The enumeration `(a,b,a xor b)` with `0<a<b<a xor b<512` lists each once.

**Source-history lemma.** For Q and, separately, Q4,

    L_C intersect W = {0}

for every one of these 43,435 charts. The claim holds over every characteristic-zero field and, after tensoring, at every positive whole-field volume V, including arbitrary within-field linear combinations of the retained scalar source histories.

### Exact certificate establishing the finite source facts

The interpreter is written in this package and does not import the predecessor source interpreter or its endpoint receipts. It replays every original input coefficient using `Fraction`, and checks actual charts, nested MOVEs, COPY guards and owned lifetimes. It builds H from actual final rows, checks every historical Hub row, and reduces each eligible historical payload by H. Projective normalization uses exact rational arithmetic.

The two sources each produce the same counts:

| Quantity | Exact value |
| --- | ---: |
| Distinct nonzero reduced rows with some eligible C2 | 298 |
| Pure independent first-Y nuisance directions | 104 |
| Pure original D coordinate rows | 96 |
| Other pure-D rows | 98 |
| Charts with nonempty relaxed pools | 43,180 |
| Maximum pure D coordinates at one C2 | 35 |
| Charts with no other pure-D row | 41,373 |
| Charts with one other pure-D row | 1,824 |
| Charts with two other pure-D rows | 237 |
| Charts with four other pure-D rows | 1 |

The 104 nuisance rows are distinct original-Y coordinate vectors, and cannot participate in a nonzero pure-D combination. They can therefore be dropped when testing W.

For each remaining local pool, first delete its known pure-D coordinate columns. A nonzero W intersection before that deletion is equivalent to a nonzero intersection of the projected W with the projected other-D rows, provided W itself remains injective after deletion. This injectivity is verified directly, not merely inferred from the predecessor distance theorem.

The 40,963 distinct pure-coordinate cases have an exact nonzero eight-column minor of the projected Gram basis. The 2,062 other cases have at most two independent projected extra rows. The sole four-row case has exact rational rank two. For each case the checker first obtains the extra-row rank **over Q**, proving the upper bound; it then exhibits an `(8+r)`-column nonzero minor after appending the eight projected Gram rows.

The minor is computed modulo the prime 1,000,003 after clearing rational denominators by field inversion. Denominators are checked nonzero modulo that prime. A nonzero modular determinant proves the corresponding rational determinant is nonzero. We never use a modular rank as an upper bound on rational rank. Exact rational dependencies supply the necessary upper bound on the local extra rows. Therefore the projected spaces are disjoint over Q and every characteristic-zero extension.

These are finite source-geometry certificates, not an extrapolation from a random search. The universal width assertion follows because the scalar source histories give `L_C tensor F^V`, the demand is `W tensor F^V`, and scalar zero-intersection extends to those tensor spaces. All block coefficients may mix coordinates arbitrarily within that fixed tensor history space.

## 3. Why an initial B preload does not open this interface

Write the stripped source's final hosted Hub rows as

    z = b + R d.

This identity is checked on all original coordinates. Give the construction, at zero cost, any initial replacement

    b <- b + L d.

Let S_L be the invertible matrix on original input columns implementing this replacement; other input coordinates are unchanged. Every old current row r becomes `r S_L`, and H becomes `H S_L`. Every pure-D row w is fixed: `w S_L = w`. Thus

    (L_C + H) intersect (W + H) = H

is equivalent, after right multiplication by S_L, to the corresponding zero effective W intersection for the preloaded source. This is a source transformation, not an uncharged extra original-b copy.

Choosing `L=G-I-R` would make the actual final Hub rows of the preloaded source equal

    z = b + (G-I)d,

so the desired `b-d` correction is exactly `-Gd`, with demand W. We deliberately grant this algebraic preload without claiming it has a legal physical realization. Even this favorable grant does **not** turn the old dimension-two histories into innovative Gram observations.

The same statement applies to block-valued B-from-D preloads at every V, because S is invertible and fixes the entire pure-D subspace. Consistent coordinate conjugation of both source and demand also preserves the statement. An arbitrary changed target gauge without the corresponding source transformation is not covered.

The actual Q4 census separately confirms the conclusion for its real compensated ferry word, including its new packet routes. No generic ferry sufficiency is inferred from a boundary formula.

## 4. Rank-tight streaming with an evolving Hub

The argument permits actual temporal consumption. Suppose new observations `m_1,...,m_q`, each at most V coordinates, are acquired at dimension-two charts and returned to the Hub. Their local formation may use:

* the retained old local history space at the chosen C;
* all H, granted globally from time zero;
* every earlier returned observation, also granted globally for free.

The old source may receive changes caused by Hub processing of those known quantities. Under the fixed old linear source operations, those changes remain linear combinations of H and earlier observations. This includes source rows perturbed by an earlier Hub correction. It does not include an independently redesigned local source transformation carrying new information on an old paid route.

Modulo H, every actual observation therefore has the causal form

    m_t = l_t + sum_(s<t) A_(t,s) m_s,   l_t in L_(C_t) tensor F^V.

This uses actual earlier messages; it does not replace an evolving Hub by a hypothetical future graph. Passing to the granted final-Hub quotient only enlarges the available side information. The relation is justified by linear induction on the literal old operations and the declared additional Hub/return operations.

Assume the observations recover the 8V-dimensional demand `W tensor F^V`. If q is at most eight, the full message span has dimension at most 8V and must equal that demand. Every observation row is then in `W tensor F^V`. The first observation has no earlier message term, so it lies in the zero intersection from Section 2 and is zero. Inductively each later message is zero as well. This contradicts recovery of W.

**Theorem.** In this fixed-history/passive-copy continuation, including the free B preload above and arbitrary causal Hub consumption, at least **nine whole-field C2 returns** are necessary for the canonical hosted Gram demand.

This is a bootstrap obstruction: a tight family of eight messages cannot spend a dimension outside the eventual demand in order to acquire its first useful demand direction. It is not a theorem that every physical return must always be a pure Gram row; that conclusion is used only under the saturated eight-field dimension budget.

## 5. Complete retained tariff

Use the exact complete caller T,P, native paid profile N and helper-target profile H_c from the predecessor fixed-m assembly. For the stripped Q profile, the limiting per-rail allowance at `t=199/200` is

    R_infinity = ((T-P)/18 + N - H_c - Q_paid)_t
               = 57.096340268441956... .

For every fixed integer `m>=2`, the remaining allowance is `R_infinity-d/(m-1)`, where `d=31.5397783670854135...>0`. A multiplicity depending on input size is not admitted.

Nine C2-to-Hub rank-seven returns cost

    9 * 7^(199/200) = 62.390010576575875...,

leaving a strictly negative limiting margin

    -5.293670308133917... .

The real four-ferry debit makes that limiting margin `-5.538129186916182...`. Every finite m is worse. The checker uses exact rational 200th-root intervals and a positive finite-m penalty. It also confirms that eight hypothetical returns retain the predecessor's positive limiting envelope; the failure is caused by the new source-history requirement, not a changed price convention.

This price conclusion is conditional on one paid rank-seven ascent per acquired C2 whole-field observation and the retained complete caller. Relayed acquisitions with new information before their first Hub arrival, changed source fields, a different target code, a different physical interface, or different complete invoices require fresh analysis. All remaining forward work, ordinary work, storage, precision, erasure and compiler services were granted free for this necessary comparison, so charging them cannot rescue this particular family.

## 6. What remains open

* Construct a source transformation that changes a useful local history space, rather than covariantly changing both its mixed rows and the Hub boundary.
* Produce a different low-rank target code and an actual paid observation schedule, including its coupled duties and all source restoration.
* Use extra local transport or a genuinely new relay to create an initial innovative row, and price that transport within the complete invoice.
* Establish a compatible strict uniform complex supplier after complete endpoints; complete BIT admission and the five foundational assumptions remain separate.

The package does not supply a new complete source, a uniform supplier, or a kappa increase. The exact partial rank-82 sources, previous rank-54 source with its paid returns, and old terminal/fresh-source obstructions retain their distinct scopes.

## Credit

Prepared for @CubeJerry with substantial OpenAI research-agent assistance. The retained native construction, shared-wire source and complete caller, the S010 standalone extraction and compensated ferries, the prior mixed-observation conditioning lemma, the E8 source/Gram results, and the fixed-m accounting theorem remain credited predecessors. The new contribution is the complete preterminal C2-history census, its initial-preload covariance extension, and its rank-tight causal return gate. Independent research-agent review must be recorded separately; no human or formal-kernel acceptance is claimed.
