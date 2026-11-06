# Independent audit: chain-cover round-offset refinement

Scope: the proposed symmetric-chain construction and one assigned round per
covering permutation. Reviewer: separately assigned Codex agent for Worker C.
Prepared for @CubeJerry with substantial OpenAI Codex assistance; no human or
proof-kernel acceptance is claimed. Canonical source base:
`7c49fe32c55de02c2c873655c804b16e4c3fef0a`.

**PASS:** no mathematical or literal-execution blocker found within this scope.

## Universal symmetric-chain induction

Suppose a chain in the Boolean lattice on n coordinates has ranks
`a,a+1,...,n-a`, with consecutive members differing by one added bit. Append
the new bit to its final member to obtain a chain of ranks
`a,...,n-a,n+1-a`. These endpoint ranks sum to n+1. The second chain consists
of every original member except the last, each with the new bit adjoined; its
ranks are `a+1,...,n-a`, again with endpoint ranks summing to n+1. It is empty
exactly when the old chain was a singleton.

These two chains partition the old chain and its entire new-bit copy: all
old members lie in the first, its last member's new-bit copy also lies there,
and all other new-bit copies lie in the second. Distinct old chains have
disjoint members and copies, so the operation preserves a partition of the
entire Boolean lattice. Starting from the sole chain `[0]` at n=0 therefore
proves a symmetric-chain decomposition for every n.

Every resulting nonempty chain crosses rank floor(n/2) exactly once. Its count
is consequently `binom(n,floor(n/2))`. Extend a chain by first adding the
initial mask's bits in increasing order, then following its actual one-bit
steps, then adding the remaining missing bits in increasing order. Every bit
is added exactly once, so the result is a genuine permutation, and every
member of the original chain occurs as a prefix. All subsets are covered.

## Exact minimality in the specified representation class

Every permutation has exactly one prefix of any fixed rank r. Covering all
rank-floor(b/2) subsets therefore requires at least `binom(b,floor(b/2))`
permutations for b>=2. For b=1 use rank 1, since the floor central rank is the
empty set; the same numerical minimum is one. This proves exact minimality
for coverage by permutation prefixes, not for unrestricted connector words.

For D pairwise disjoint nonempty groups, one full-source permutation cannot
have nonempty prefixes wholly contained in two different groups: its prefixes
are nested, while nonempty subsets of distinct groups are disjoint. The first
source label determines the only group that can have a productive pure-group
prefix in this round. Each group needs its central-layer number of rounds.
Any scheme demanding one pure-group productive prefix per group subset thus
needs at least `D*binom(b,floor(b/2))` rounds for equal group size b. Assigning
that many separate group-permutation rounds attains the minimum. This does
not exclude mixed-group prefixes, multiple productive reads per group, or
other offset structures.

## Correction identity and threshold

In a source word of c permutations of all k=Db source labels, round r starts
at the exact integer vector `r*1`. Place one group's covering permutation first
in each assigned round, followed by all remaining labels. If S is a prefix
subset of that group permutation, its actual source boundary has count
`r*1+1_S`. For a nonempty target mask choose one such prefix for each nonempty
group part, at most D productive reads. Their offsets sum to an integer R.
Read once more at the start of round `(-R) mod c`; this existing boundary has
count `((-R) mod c)*1`. Their sum is the target mask modulo c.

The assumptions `D,b>=1`, `D*binom(b,floor(b/2))<=c`, and `D+1<=c` suffice.
The last condition is required by this stated padding argument, which uses
up to D+1 reads and pads to exactly c. It is not claimed necessary for all
connector representations. For b=1 the round-capacity inequality alone permits
c=D and does not imply this condition. For b>=2 the covering number is at
least two, so c>=2D already implies c>=D+1.

The correction is a positive read, requires no unassigned round, and may be
before, after, or at the same boundary as another read. Sorting reads is legal
because output calls preserve the connector. Exactly c reads eliminate the
arbitrary initial dirty connector value; exactly c source calls restore it.
Initial outputs are retained additively, sources are immutable, and the order
A_M B_j is unchanged. No prime-characteristic or commutation assumption enters.
Disjoint-source copies concatenate because each copy ends at zero modulo c;
at most `copies*(D+1)<=c` total reads can then be padded at global zero.

## Independent finite evidence

`verify_chains_independent.py` imports only the standard library. It reads the literal
author-generated CHAIN-COVERS.json and CHAIN-FIXTURES.json, and never imports or calls the
symmetric-chain constructor. Each literal permutation, saturated symmetric
chain, partition of the Boolean lattice, chain embedding, central-layer count,
and supplied subset-to-prefix locator is checked for b=1..12.

Across the twelve covers it checks 1,911 permutations and 8,190 located masks.
It executes the actual source word and every padded output read on independent
formal coefficients for each initial output, the dirty connector, and all
composed source terms. This checks arbitrary inputs without assuming A/B
commutation. The five fixtures are:

| D | b | c | copies | sources | nonzero masks | complete calls |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 3 | 3 | 1 | 3 | 7 | 30 |
| 2 | 3 | 6 | 1 | 6 | 63 | 414 |
| 3 | 2 | 6 | 1 | 6 | 63 | 414 |
| 3 | 3 | 9 | 1 | 9 | 511 | 4,680 |
| 2 | 3 | 6 | 2 | 12 | 4,095 | 24,642 |

Total: 4,739 nonzero output masks, 30,180 complete calls and 63,994 formal
output coefficients. All 89 negative controls are rejected. They include
invalid permutations, invalid and valid-but-wrong locators, broken chains,
incorrect cover counts, missing source calls/masks, out-of-range reads,
insufficient characteristic, a shifted actual read with unchanged call count,
and moving zero-prefix padding to a nonzero boundary while retaining c reads.
The last two controls test semantic action, not merely structural guards.

Executed successfully from the scratch root:

```sh
python -I -B -W error chain-cover-refinement/verify_chains_independent.py
python -I -O -B -W error chain-cover-refinement/verify_chains_independent.py
```

Both print `PASS_INDEPENDENT_CHAIN_COVER_REFINEMENT` with identical counts.
Finite verification corroborates the supplied implementation; the induction
and algebra above establish the universal claims. This audit establishes no
physical supplier price, selected-frontier assumption, or new multiplication
exponent.
