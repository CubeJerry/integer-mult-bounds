# Incidence required by every zero-Gram-side rectangle cover

Status: **new proved scoped geometric incidence theorem; independent review
requested**. This extends the canonical-partition count to arbitrary
rectangle covers satisfying the source within-side Gram condition. It
still does not prove a physical runtime lower bound: incidences may share
work. The current multiplier theorem does not depend on this result.

## 1. Family and exact scope

Retain the characteristic-two geometry with d a power of two, d>=2,
`h=2d-1`, `q=2^t>=2`, `U=[q]^h`, and outer labels `V=U^h`.
For outer labels v,w let k(v,w) count coordinates whose inner words have
Hamming distance d. Let F(v) consist of the off-diagonal neighbors used
by P*: exactly d outer coordinates change, at inner distance d in each.
Put

    C=binom(h,d), C0=2^(h-1),
    M=sum_(j=0)^(d/2-1) binom(h,j).

Consider any family of directed rectangles (L_a,K_a) that covers every
ordered pair (v,w) with w in F(v), and satisfies

    k(w,w')=0 for all w,w' in K_a,
    k(v,v')=0 for all v,v' in L_a.                    (NC1)

The cover need not be disjoint, canonical, uniform, or unweighted. A
weighted rectangle identity with a nonzero coefficient on every required
edge also supplies such a cover after zero coefficients are omitted.
Allowing extra covered pairs and cancellations does not weaken the proof.
Only the within-side condition (NC1) and required edge coverage are used.

Write rho_v for the number of rectangles with v in their source side.
The corresponding destination count obeys the same bounds by symmetry.

**Theorem NC.** For every outer label v,

    rho_v >= C (C/M)^d,                              (NC2)
    rho_v >= C [C(q-1)^d/(C0 q^(d-1))]^d.            (NC3)

In particular,

    log2 rho_v >= (d^2+d t)/32.                      (NC4)

Under the retained sufficient rank guard
`2^(t d^2)>=2^(2d^2-2) m`, this implies

    log2 rho_v >= (log2 m)^(2/3)/32.                 (NC5)

The constants are deliberately conservative. The power 2/3 restriction
in this geometric class does not retain the canonical partition's
additional `(log log m)^(1/3)` factor.

## 2. A binary constant-weight independent-set bound

Let A be a collection of d-subsets of an h=2d-1 element set, with no
pair at symmetric-difference size d. Equivalently, distinct members never
have intersection size d/2. Then

    |A| <= M.                                       (NC6)

To prove this, put e=d/2, also a power of two. Over F2 use

    B_e(z_1,...,z_h)=sum_(j=0)^(e-1) e_j(z_1,...,z_h).

When c input coordinates equal one, this equals one exactly when e
divides c; the low-bit binomial argument is the same elementary identity
used in the retained characteristic-two label construction. For d-subsets
A,B, evaluate at `z_i=1_(i in A)1_(i in B)`. Their intersection has size
at least one because h=2d-1. Distinct members have intersection at most
d-1, and the only multiple of e in that interval is e itself. It is
excluded by assumption. The diagonal intersection size d=2e is allowed.
Thus the evaluation matrix on the family is the identity.

The displayed polynomial has only monomials indexed by subsets of size
less than e. Each evaluated monomial is a rank-one matrix, factoring into
its incidence at A and at B. Its matrix rank is therefore at most M,
which proves (NC6). This argument depends on the power-of-two choice;
it is not a claim for an arbitrary distance parameter.

## 3. Bounding one rectangle side near a fixed label

Fix an outer label v. For each of its h^2 individual letters, choose one
alternative letter. Restrict to the binary subcube using only those
original/alternative choices. Its neighbors of the prescribed outer type
number `C^(d+1)`: choose d changed outer coordinates, and a d-subset of
changed binary positions at each selected inner coordinate.

Let K satisfy its half of (NC1). Among these neighbors, all members of K
must have exactly the same set S of changed outer coordinates. Indeed,
if two change different sets, one outer coordinate equals v there and
the other is at inner distance d from v there. Their mutual k is then
positive, contradicting (NC1).

For each of the d coordinates in S, the projection of K consists of
binary d-subsets with no pair at distance d. Section 2 bounds each
projection by M. Therefore K contains at most M^d of the restricted
neighbors. Every required neighbor must be covered by a rectangle with
v in its source, proving `rho_v M^d>=C^(d+1)` and (NC2).

For the unrestricted q-ary neighbor family the same argument forces one
changed-coordinate set S. A projection in a changed coordinate is a set
of inner words with no pair at distance d. Restrict the retained binary
scalar matrix P0 (equal or distance d) to this projection. It is an
identity matrix, so the projection has size at most rank(P0), hence at
most `C0 q^(d-1)` by its explicit degree-(d-1) tensor factorization.
There are `C (q-1)^d` far inner neighbors. The full outer family thus has
size `C [C(q-1)^d]^d`, whereas one K contains at most
`[C0 q^(d-1)]^d` of them. This proves (NC3). Source-side symmetry proves
the destination-incidence version. No disjointness or sign assumption
entered either counting argument.

## 4. Uniform explicit growth

First, `C/M>=2^(d/8)` for every power of two d>=2. For d=2,4,8,16 this
is a finite binomial inequality, verifiable exactly as `C^8>=2^d M^8`.
For d>=32, write n=2d-1. The elementary binomial-tail bound gives

    M <= 2^(n H_2(1/4)) <= 2^(5n/6),
    C >= 2^n/(n+1).

The first inequality follows by weighting the lower tail with 3^(-j):
its unweighted sum is at most `3^(n/4)(4/3)^n`. For the second entropy
comparison, `H_2(1/4)=2-(3/4)log2 3<=5/6`, since `3^9>=2^14`.
The central binomial coefficient C is a maximum among n+1 coefficients.
Consequently

    log2(C/M) >= (2d-1)/6-log2(2d) >= d/8.

The last inequality holds at d=32 and increases when d is doubled:
its slack increases by `5d/24-1>0`. Together with the four finite cases,
(NC2) now yields `log2 rho_v>=d^2/8`.

If q>=2d, Bernoulli's inequality gives `(1-1/q)^d>=1/2`.
Also `C0<=d C`, because C0 sums d binomial terms, each at most C.
Thus (NC3) implies

    log2 rho_v >= d(t-log2(2d)).

When `t>=2 log2(2d)`, this is at least dt/2. Otherwise,
`dt<=2d log2(2d)<=2d^2`, using `log2(2d)<=d` for d>=2.
The binary bound then gives `log2 rho_v>=dt/16`. Hence in all cases
log2 rho_v is at least both d^2/8 and dt/16. Adding these inequalities
and dividing by two proves the conservative (NC4).

Put z=log2 m. The rank guard implies `t d^2>=z`, so
`d^2+dt>=d^2+z/d>=z^(2/3)`: if d>=z^(1/3), use the first term;
otherwise use the second. This proves (NC5).

## 5. Consequence for a specifically charged certificate

Suppose a variable-arity certificate charges a fixed positive power of
the incidence count at each stage, with nonnegative normalized log
charges, and its arity logarithms z_i satisfy
`sum z_i>=cY` and `1<=z_i<=CY`. The same ratio argument as the lead's
variable invoice theorem gives

    sum z_i^(2/3) >= c' Y^(2/3).

Thus any such certificate using the retained sufficient rank guard and
zero-Gram-side rectangle delivery has log overhead at least order Y^(2/3),
even when the canonical rectangle partition is replaced completely.
This applies only when incidences are actually assigned those positive
charges. An upper invoice, by itself, is not a runtime lower bound.

The remaining gap is meaningful. C's exact canonical count and the lead's
literal-invoice analysis force the additional `(log Y)^(1/3)` factor for
that partition. The present noncanonical theorem does not. A better
partition could in principle remove that factor. Beating the 2/3 power
within a positively incidence-charged certificate would require changing
at least the Gram-side condition, the label/rank family or its sufficient
rank guard. Sharing physical work across incidences escapes the charged
certificate premise and is not ruled out.

This proof does not assert optimality of any graph partition, a lower
bound on the exact rank requirement, or a time lower bound for tape
interchange or multiplication. The rank guard is a sufficient premise,
not a necessary statement about every algorithm.

Source dependencies: the pinned OpenAI tape label/endpoint construction;
the retained characteristic-two B_d and rank factorization in
`routes/B/characteristic-two-label-geometry.md`; C's exact canonical count
motivated removing the canonical assumption. The constant-weight rank
argument, its application to arbitrary source-compatible rectangle covers,
and the explicit combined incidence bound are derived here.

Credits: @CubeJerry, source authors and prior programme, E002 team, and
substantial ChatGPT multi-agent assistance. This is a written proof,
not formal verification or a full tape implementation.
