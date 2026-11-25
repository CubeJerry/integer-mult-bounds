# Independent review of the noncanonical incidence theorem

Reviewer: E002 independent reviewer A, distinct from the original Route A
author. Status: **PASS for the stated geometric count and charged-certificate
consequence**. No actual tape-runtime or multiplication lower bound follows.

Reviewed complete `NONCANONICAL-RECTANGLE-INCIDENCE-BARRIER.md`, SHA-256
`35143ce234fee2acd20c23dbaf53987972e705d92b4839c77449b5952c8cd806`.
Reviewed and independently replayed checker SHA-256
`df4dc85c787ed83eb5bd4e4eb3588c30acc417e018853afbedd9c5a6a498289c`.
The source interface was checked against the full retained
`routes/B/characteristic-two-label-geometry.md` at the programme snapshot.

## 1. The constant-weight rank argument

For d a power of two and e=d/2, the binary polynomial
`B_e=sum_(j<e)e_j` evaluates to one exactly when e divides the count of
one inputs. This follows from the low binary digits in the expansion of
(1+T)^c over F2. For two d-subsets of a (2d-1)-set the intersection has
size at least one, so distinct intersections can hit a multiple of e only
at e. The diagonal intersection 2e gives one. Excluding intersection e
therefore makes the restricted evaluation matrix the identity.

Each of the M monomials factors into one function of each subset, hence
has rank at most one. The independent family has size at most M. This
uses the power-of-two hypothesis and the exact 2d-1 ground-set size.
It does not apply unchanged to arbitrary distance parameters.

## 2. From one side to per-label incidence

Fix a source label v. The binary choice at every individual letter
supplies exactly C^(d+1) required far neighbors. For any destination side
satisfying NC1, two such neighbors cannot have different outer supports:
a position used by just one of them creates mutual inner distance d,
contradicting k=0. With outer support fixed, the projection at each of
the d changed positions is an independent family of binary d-subsets,
so the side contains at most M^d neighbors. Coverage alone proves NC2.
Neither disjointness nor regularity is needed.

For q-ary neighbors, the same support argument applies. In each changed
coordinate a projection with no pair at distance d makes the source
scalar matrix P0 restrict to the identity. Its explicit degree-(d-1)
tensor factorization bounds rank by C0 q^(d-1). Counting all required
neighbors and the maximum possible intersection with one side proves
NC3. The source-side conclusion follows symmetrically. Weighted identities
still cover every edge whose target coefficient is nonzero, after zero
weights are removed; cancellation does not invalidate this counting.

This concerns exactly NC1's retained k=0 within-side condition. It does
not establish the same statement for all conceivable endpoint geometries
or for a relaxed Gram-side condition.

## 3. The uniform estimates

The lower-tail calculation is valid because d/2-1<(2d-1)/4. Weighting
terms by 3^(-j) bounds M by 2^((2d-1)H_2(1/4)), and the displayed
integer comparison 3^9>=2^14 gives H_2(1/4)<=5/6. The central binomial
bound gives C>=2^(2d-1)/(2d). At d=32 the resulting inequality has
positive slack; doubling d increases it by 5d/24-1. The four smaller
power-of-two cases are exact finite inequalities. Thus log rho_v>=d^2/8.

For q>=2d, Bernoulli and C0<=dC give the stated
`log rho_v>=d(t-log(2d))`. The split t>=2log(2d) versus its complement
correctly yields log rho_v>=dt/16 in all cases, using the binary bound
in the second case. Averaging the two lower bounds proves the deliberately
weaker (d^2+dt)/32 estimate. The retained sufficient rank guard gives
td^2>=log m. Splitting d at (log m)^(1/3) then proves NC5.

For a separately specified positive-incidence certificate with
1<=z_i<=CY and sum z_i>=cY, one has
`sum z_i^(2/3)>=sum z_i/(CY)^(1/3)>=c'Y^(2/3)`.
This establishes the final analytic consequence precisely when the
certificate actually assigns those nonnegative charges. An algorithmic
upper invoice by itself does not do so.

## 4. Independent finite replay and scope

Copied the reviewed checker into `replay-noncanonical/` and executed it
independently at 2026-11-25T23:23:34.813637+00:00; exit code zero.
The replay receipt and complete log are retained there. It reproduced:

- two binary constant-weight cases, including ranks 1 and 7 and exact
  largest compatible families of sizes 1 and 5;
- two q-ary cases with largest compatible families 1 and 6;
- nine exact binomial inequalities and 60 uniform incidence inequalities;
- 598 checks of differing outer supports and two negative controls on
  the power-of-two/within-side assumptions.

The polynomial identity, rank factorization and geometric coverage proof
establish the infinite family. The finite replay supports the implemented
small cases and arithmetic controls; it is not an asymptotic tape test.

The theorem extends the incidence obstruction beyond the canonical
partition within NC1, but loses the canonical extra logarithmic factor.
It neither proves optimality of a rectangle partition nor a necessary
rank guard. It does not exclude sharing work across incidences, another
label family, another Gram condition or a different algorithm. The
unconditional positive multiplier envelope does not depend on this result.

Credits: @CubeJerry; the pinned source and retained characteristic-two
construction; Route A's new incidence argument; substantial ChatGPT
multi-agent assistance. No formal refinement, full machine execution or
literature-priority claim is made.
