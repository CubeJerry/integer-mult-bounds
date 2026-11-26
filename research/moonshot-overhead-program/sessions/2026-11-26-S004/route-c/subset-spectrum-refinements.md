# Sharper physical matching and the exposed ratio subgroup

Status: **proved refinements, independent audit pending**. This addendum
extends `subset-spectrum-blocking.md` without changing SB1–SB8. The
original 5/256 physical construction remains valid.

## 1. Full physical matching improves 5/256 to 5/16

For the actual order-five gate, put p_i=1/q_i in [0,1/2]. Its local
target-exponent distribution is

    mu_p = p delta_0 + (1-p)(delta_1+delta_(-1))/2.

Each mass in the four-fold convolution is multiaffine in the four p_i.
Minimizing one affine coordinate at a time shows that its minimum over
[0,1/2]^4 is attained at a vertex. There are 16 vertices. Convolution
commutes, so their masses depend only on the number h of p_i=1/2.
The complete list, with numerators over denominator 256, is:

| h | Number of vertices | Masses at exponents 0,1,2,3,4 |
|---|---|---|
| 0 | 1 | 96, 16, 64, 64, 16 |
| 1 | 4 | 48, 56, 48, 48, 56 |
| 2 | 6 | 56, 52, 48, 48, 52 |
| 3 | 4 | 60, 54, 44, 44, 54 |
| 4 | 1 | 70, 57, 36, 36, 57 |

Every target-root eigenspace has dimension at least D_group/16. Let g
be the minimum of the five integer dimensions. Choose g distinct
original joint eigenvectors from each target eigenspace and match them
into g disjoint five-element sets, one vector of each root per set.
Each span is a regular cyclic piece. Every original one-coordinate
query preserves it because the query is diagonal on those joint
eigenvectors. All remaining eigenvectors are singleton pieces. Hence

    theta_j=5g/D_group >=5/16.                             (SB9)

This is a basis choice for a rank comparison, not a physical matching
algorithm. It retains unequal q_i and all actual multiplicities. For
order three, the analogous two-fold vertex minima are 1/4,1/4,5/16,
giving theta_j>=3/4. The simple selected-word SB8 remains an independent
proof of a positive uniform fraction.

## 2. General finite ratio-subgroup corollary

The lead requested this formulation to distinguish the target root
order from the subgroup exposed by its subset. Let S be a fixed finite
nonzero spectrum, a in S, and G=<S/a> of finite order d. In the cyclic
root setting G=mu_d. Assume every value of S has actual dimension
fraction at least p_*>0 in each original coordinate. Multiplicities may
vary. If d=1 the target is scalar and the sharp error is zero.

For d>=2, put T=S/a. It contains 1 and generates G. The sets T^j of
products of exactly j elements increase with j. If T^(j+1)=T^j, then
multiplication by each t in T preserves that finite set; bijectivity
also gives preservation under t^-1. Thus the set is G-invariant and
contains 1, so it equals G. Until this occurs its size grows by at
least one. Starting from T^0={1}, we obtain

    T^(d-1)=G.                                            (SB10)

Choose one length-(d-1) word for each group element, padding with 1.
Group d-1 original coordinates. Each selected spectral word has actual
fraction at least p_*^(d-1), and the d target products are distinct.
Match equal multiplicities among those selected joint eigenspaces and
leave other eigenvectors as singletons. The regular fraction is at least

    theta_* = d p_*^(d-1)>0.                             (SB11)

Apply the blocking theorem with r replaced by d. The target product
lies in the fixed coset a^m G, and the exceptional mass decays
exponentially. The sharp limiting error constant for support degree
o(sqrt(m)) or active volume o(W sqrt(m)) is

    1-1/d.                                                (SB12)

The inverse-query, arbitrary-port and rational-fraction variants remain
valid. This proves an invariant decomposition of the actual payload;
distributional balance alone would not suffice for the rank theorem.

For {zeta,zeta^-1} with zeta of order r, the ratio subgroup has order
d=r/gcd(r,2). Odd r gives d=r; even r gives sharp constant 1-2/r.
Products then occupy a coset of the smaller subgroup, and constant
prediction contradicts a claimed sharp 1-1/r limit. A larger alphabet
can expose a larger subgroup, but a vanishing dimension fraction must
not replace fixed p_*. The physical odd-order proof above handles
vanishing equal-field fractions without making that substitution.

No model exclusion or complete multiplication bound changes here.

## 3. Exact controls

The self-contained `verify_subset_spectrum_refinements.py` passes all
16 order-five vertices individually, not only their five symmetry
classes, together with four order-three vertices and 92 individual root
mass inequalities. It also checks 256 unequal physical multiplicity
matchings and exhausts all 4,094 normalized cyclic subsets through
ambient order 12. The latter yields 44,597 explicit distinct-product
witness words, with strict cardinality growth checked at all 10,078
steps before subgroup completion. The saved JSON records these counts.

An order-four two-root pair gives a degree-zero constant predictor with
error exactly 1/2, rejecting the invalid ambient-order constant 3/4.
Finite subgroup checks support the implementation of the word selection;
the general statement follows from the complete set-growth proof above.
