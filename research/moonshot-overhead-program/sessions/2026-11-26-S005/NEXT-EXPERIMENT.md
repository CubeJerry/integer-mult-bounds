# Next experiment: compressed Frobenius-equivariant CRT circuits

Status: **open research handoff, not an admitted fast supplier or rate**.
This is a concrete continuation of UC/FL. It does not change the frozen
report, the carry contracts or the unconditional frontier.

## A discriminating circuit relation

Let K=F_(2^b), q=2^b, and let S square each coordinate of K^q. Its fixed
space is F_2^q. For an invertible K-linear partial evaluation circuit C_j,
the states reachable from arbitrary binary input form exactly

    C_j(F_2^q)=Fix(J_j),  J_j=C_j S C_j^(-1).

This space has q independent bits, even though its expanded description
has q field coordinates. The full evaluation map is invertible on
polynomials of degree below q; its terminal semilinear symmetry combines
S with the Frobenius permutation of the evaluation points. Define its
orientation by J_final=E S E^(-1), rather than choosing a permutation
convention implicitly.

Seek a factorization C_(j+1)=L_j C_j such that the conjugated symmetry
has a *monomial* description J_j=M_j S at every stage. The exact local
condition is

    L_j M_j = M_(j+1) L_j^(2),

where L_j^(2) squares its matrix entries. It follows by writing
L_j J_j=J_(j+1) L_j. Here M_0=I. The question is whether useful
non-invariant butterfly blocks can satisfy this relation with an efficient
executor on compressed cycle words. Cycles may merge or split; no single
globally invariant binary flag is assumed.

Since J_j^b=I, a permutation cycle in a monomial M_j has length d
dividing b. Its fixed-coordinate equations include a twisted scalar
normalization. Once normalized, the parameter belongs to F_(2^d) and
has d bits. Existence follows from the conjugacy and fixed-space
dimension; efficient construction of all normalizations, their
directories and the actual chosen coordinate maps must be proved and
charged. A monomial formula by itself is not a tape algorithm.

For odd b, a single two-coordinate update cannot create a two-cycle
from M_0=I while retaining this monomial symmetry, because 2 does not
divide b. This suggests testing larger blocks or an explicitly
nonmonomial compressed class rather than assuming ordinary binary
layers will close.

## Costs that decide whether the experiment is useful

The target for the binary transform is q sqrt(b) times at most a fixed
polylog(b), with O(q) actual working payload under the stated supplier
contract. The endpoint needs the sharper q sqrt(b) bound; a retained
polylog(b) corresponds to a polynomial log-log overhead at the integer
root, provided all higher carry contracts also fit. Both forward and
inverse transforms are required.

Charge stage construction, scalar normalization, cycle regrouping,
physical movement, local field arithmetic and data-dependent coordinate
conversion. Materializing q full field words uses qb physical bits,
even when their values are constrained.
Keeping multiple conjugate flags does not automatically remove that
expansion. FS's q b polylog(b) factor preparation was affordable once
at the integer root; repeating an O(qb) conversion at every binary leaf
would exceed the binary target. A shared larger root directory needs
an explicit revised space and access-time contract.

This experiment concerns the binary transform. Ordinary squaring is not
a ring homomorphism modulo four. FL's separately charged first-carry
transport remains necessary, and its shared root setup cannot be
repeated for free at every binary leaf.

## Why the simplest invariant-flag shortcut is insufficient

In a normal basis, Frobenius is a cyclic b-shift with characteristic
polynomial T^b-1. A complete invariant flag with one-dimensional steps
over F_2 makes it triangular with every diagonal entry one, forcing
T^b-1=(T-1)^b. This occurs exactly when b is a power of two; conversely
the resulting single unipotent block has such a flag. This observation
concerns that specific flag construction, not arbitrary compressed
evaluation circuits.

UC needs q=2^b comparable to its actual polynomial length. Rounding b
to the next power of two can increase q toward the square of that
length. The padding cannot be omitted from the global invoice. The
semilinear relation above is intended to test a route beyond this
restricted flag choice, not to relabel its cost.

## First test and continuation gate

For an explicit additive-evaluation block, solve the local relation
for monomial M_(j+1), check the full binary fixed space, and construct
the actual compressed forward and inverse operations. Record exact
cycle payload and movement costs. If monomial closure fails, preserve
the first counterexample and ask whether a slightly larger, explicitly
compressed class changes the complete invoice. Do not infer a global
lower bound from failure of the monomial class.

The lead and Route A derived this handoff during final discussion.
It has not been admitted as a complete construction or independently
kernel-checked. Standard finite-field and linear-algebra facts retain
their provenance; substantial ChatGPT assistance.
