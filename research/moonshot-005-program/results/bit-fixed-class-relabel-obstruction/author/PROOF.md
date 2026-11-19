# Independent relabelling cannot glue the fixed native nine-port classes

**Scoped obstruction pending independent review. No new kappa.** The prior
class-separation theorem left independent per-plane relabelling open. The
present certificate excludes every such relabelling of its fixed partitions.
Changed partitions, mixed components within ports and different targets remain
outside the theorem.

## 1. Exact contract

Use the pinned native geometry and five nine-port classes at every A2 plane H.
There are 1,108 ordinary H with at least two native donors, eleven singleton
H, and one empty H. Let F be finite and rho a positive integer. Every donor
has a common original-input decomposition into five W_c of dimension 48rho.
Its ordinary class-c quotient has 3rho coordinates from W_c only. At each H
choose any permutation sigma_H of the five fixed classes. H processing is
linear and class-preserving with unrestricted within-class coefficients;
the class permutation selects which component every port carries. Each
H-to-D and D-to-K flag has rho fields.

Later processing may be nonlinear, mix classes and use charged storage on
the same routes. No informative bypass, extra return or free source read
is granted. Used proper target blocks are identities: all selected pairs
exclude receiver80 and donor10, so are unchanged by both current two-star
targets. Used foreign source views consist of sixteen ordinary planes.

**Theorem.** No choices of sigma_H, source coefficients and downstream
processing meet all these target equations. This is not a lower bound for
arbitrary rank(I+B), representations or changed proper targets.

## 2. Required equal counts

For a tight receiver i and active donor j, the sixteen class-c quotients
recover 48rho coordinates of W_c, so their square source map is invertible.
Each visible three-port H projection on the donor's quotient is invertible
as well. Consequently those H-port data are independent coordinates.

For a visible D let n_c(j,D) count j's four H planes in D whose port is
labelled c. The class-c inverse-decoder image at D has dimension
rho*n_c(j,D). For two active donors j,k the complete required D image has
dimension at least rho*sum_c max(n_c(j,D),n_c(k,D)). Only four D-to-K flags
can reach i, capacity 4rho. The alphabet bound applies even to nonlinear
downstream encoders. Each count vector sums to four, forcing

    n_c(j,D)=n_c(k,D) for every c.                       (1)

This is the retained class-separation argument, now applied to arbitrary
labels. Each certificate equation has an actual witnessing receiver with
both source cuts tight. No equation uses donor10 or receiver80.

## 3. A rational uniqueness certificate

Fix global component0. Let w_(H,t) be its binary selection indicator for
local class t at ordinary H. Thus sum_t w_(H,t)=1. If c(H,D) is the fixed
local class of the port to D, (1) gives integer equations

    sum_(H subset D,j in H) w_(H,c(H,D))
       - sum_(H subset D,k in H) w_(H,c(H,D)) = 0.       (2)

Every H in a used row is ordinary, because it lies in the active donor's
tight view. There are 1,108*5=5,540 variables. CERTIFICATE.json selects
5,540 actual equations, including every ordinary-plane sum equation.
Exact elimination shows their square integer coefficient matrix has rank
5,540 modulo2. Its integer determinant is therefore odd, so it is also
invertible over Q. Minus signs disappear only in this modular check; the
rational equations retain their signs and right-hand sides.

The rational assignment w_(H,t)=1/5 satisfies every equation: each sum has
five entries, and each side of (2) counts four H, giving 4/5. It is thus the
UNIQUE rational solution. It is not binary one-hot. This contradiction
proves the theorem without a failed search or floating-point rank.

The discovery system used all1,120 H and had rank5,552 of5,600 modulo2.
Its48-dimensional nullspace consisted of four free coordinates at each of
the12 singleton/empty H. The final proof instead checks the square5,540
ordinary-variable system explicitly; it does not infer uniqueness from
the discovery nullity alone.

## 4. Validation and controls

The checker reconstructs each selected equation from integer root products,
actual donor/plane/D membership, receiver visibility, sixteen ordinary
source planes per active donor, and all actual port classes. Every selected
pair is checked to avoid the modified target stars. It checks the full
native partitions and the binary matrix rank rather than trusting stored
coefficients or a claimed rank. Source and certificate hashes are recorded.

Deleting any selected equation gives rank5,539. Uniform1/5 is an exact
positive control for rational relaxation. If all D equations are removed,
one-hot choices exist independently at each H. These controls distinguish
the class constraint and gluing equations; neither relaxed solution is a
physical construction under the full contract.

## 5. Architectural implication and open next questions

The new H divisibility theorem requires larger source components. Five
varying three-matrix components can fit the local H capacity by occupying
the five nine-port classes. This theorem shows that arbitrary relabelling
of these SAME partitions cannot glue that simple class-separated pattern
through D. It does not contradict the local positive H word.

A continuation must change actual partitions, mix component information
inside ports, remove the fixed common five-way decomposition, or change
additional proper target blocks. Each needs its own compatibility proof,
chronology and invoice. Strict BIT/complex suppliers, whole recursion and
all five foundations remain. No new complete kappa.

Credit @CubeJerry; native nine-port partition authors; the S027
class-separated middle theorem; S028 H linearization authors; and the S028
orchestrator's exact rational-uniqueness certificate, with substantial
OpenAI assistance. Separate independent review is recorded with admission.
