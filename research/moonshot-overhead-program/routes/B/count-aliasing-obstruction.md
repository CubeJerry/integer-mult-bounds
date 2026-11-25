# Small-characteristic aliasing of a scalar count predictor

Status: **proved scoped obstruction, pending independent review**.
This concerns predictors that see an ordinary count only modulo an odd
characteristic. It is not a lower bound for Fourier transforms, tape
interchange, multivariate query polynomials or integer multiplication.

It explains a concrete incompatibility in transferring the compact
rational Newton route into the source's small-characteristic interchange
construction. Adjoining a finite field extension does not remove it.

**Cross-route refinement.** Route C independently proved a stronger
theta-series tail estimate in `../C/INTERCHANGE-COUNT-OBSTRUCTION.md` and
combined it with an exact lower bound on the published rational Gram
dimension. Its result excludes uniform defect at most `1/4` for every
parameter choice satisfying the source contraction. The present note
retains the independently derived simpler estimate and its own exact
checks for provenance; it is not the programme's strongest obstruction.

## 1. Exact central-window collision

Let `p` be odd, let `K` be any field of characteristic `p`, and let a
predictor depend only on the count scalar `c*1_K`. If an interval of
consecutive integer counts has width at least `p`, it contains `c,c+p`.
The two scalar inputs in `K` are equal, while

    (-1)^(c+p) = -(-1)^c.

The target values are distinct in odd characteristic. No function of
that scalar, in particular no polynomial of any degree, can be correct
at every count in the interval. A field extension does not change the
equality of the two input scalars.

Thus a central-window polynomial in the *ordinary count* cannot simply
replace the source's multivariate, integral-binomial predictor when its
window width is at least `p`. The source avoids this scalar-count
collapse by using query-polynomial representations of the integer
binomial coefficients, not by dividing the count polynomial by `h!`
inside a small-characteristic field.

## 2. A distributional obstruction independent of the shift family

Fix `m>=1` and odd `p`. Let `C~Bin(m,1/2)`. Among all functions
`f:F_p -> K`, the maximum probability that

    f(C mod p) = (-1)^C

is at most

    1/2 + (sqrt(p)/2) cos(pi/(2p))^m.             (A)

The bound can be capped at 1 when its right side exceeds 1. It applies
to all functions, so allowing a higher-degree polynomial cannot evade it.

### Proof

Write `P_r=Pr[C=r mod 2p]`, with subscripts read modulo `2p`. For a fixed
residue modulo `p`, the two possibilities modulo `2p` have opposite
parity because `p` is odd. A function can choose the better sign there;
any value other than `+1,-1` performs no better. Hence the exact optimum is

    sum_(r=0)^(p-1) max(P_r,P_(r+p))
      = 1/2 + (1/2) sum_(r=0)^(p-1) |P_r-P_(r+p)|.    (B)

Let `zeta=exp(pi i/p)` and `lambda_h=(1+zeta^h)/2`. Fourier inversion for
the sum of `m` independent Bernoulli increments on `Z/(2p)` gives

    P_r-P_(r+p) = (1/p) sum_(h odd) lambda_h^m zeta^(-hr).

Apply Parseval on all `2p` residues. The difference changes sign on
translation by `p`, so

    sum_(r=0)^(p-1) |P_r-P_(r+p)|^2
        = (1/p) sum_(h odd) |lambda_h|^(2m)
        <= cos(pi/(2p))^(2m).

There are `p` odd frequencies, and their largest modulus is
`cos(pi/(2p))`. Cauchy--Schwarz in (B) proves (A). QED.

The elementary inequality `cos(x)<=exp(-x^2/2)` for
`0<=x<pi/2` follows by differentiating `log cos(x)+x^2/2`, whose
derivative is `x-tan(x)<=0`. Therefore (A) also yields

    success <= 1/2 + (sqrt(p)/2) exp(-pi^2 m/(8p^2)).   (A-exp)

## 3. Arbitrary deterministic rows and shifts

Give row `i` any fixed binary shift `beta_i` and any field-valued
function `f_i` of its shifted count modulo `p`; allow the functions to
differ between rows and allow any positive row weights summing to 1.
At a spectral tuple `k`, that row predicts the target sign using

    (-1)^|beta_i| f_i(|k xor beta_i| mod p).

Choose `k` uniformly from the full binary cube only for this proof.
For each fixed row, the shifted count has distribution `Bin(m,1/2)`.
The desired sign is `(-1)^|beta_i| (-1)^|k xor beta_i|`. By (A), the
average success of that row is bounded by its right side. Averaging
over rows shows that some fixed tuple `k` has success no larger than
that same bound. Consequently every scheme with a uniform exceptional
fraction at most `delta<1/2` must satisfy

    1-2 delta <= sqrt(p) cos(pi/(2p))^m,
    m <= (8p^2/pi^2)[(log p)/2 - log(1-2 delta)].       (N)

This applies to arbitrary shift-family size, repetition and row-specific
polynomials. The ordinary count loses the same information in every row.
It also applies over any extension of `F_p`.

The source binary Fourier kernel realizes every sign tuple `k`: set the
auxiliary spectral coordinates to zero, choose one distinguished
coordinate in each pair equal to one, and put its partner equal to
`k_j`. Thus the hard tuple is not an artificial unused spectral case
for that kernel. The same independent sign patterns are available in
products of disjoint swap involutions on their two-point orbits.

For fixed `p`, the lower bound on the necessary exceptional fraction
tends to `1/2`. In particular, a uniform `1/16` exceptional fraction is
impossible once the explicit bound (N) fails. The obstruction does not
rule out a characteristic growing with `m`, additional count digits,
multivariate query representations, or another repair mechanism.

## 4. Consequence for this programme

The rational predictor has a small batch and controlled inverse gaps.
Its transfer to the existing tape interchange construction needs a real
new bridge. Removing a `1/h` instruction by changing arithmetic syntax
is insufficient: any replacement that remains merely a function of the
scalar count modulo `p` fails (N).

The next noncircular question is whether additional count information
can be represented with a small full-rate module and routed using the
same data characteristic, without reinstating the generic Clifford
dimension. This obstruction gives a falsifier for that next search.

The exact finite verifier computes (B) by integer binomial sums and
checks a rational relaxation of (A). No finite check is used in place
of the all-`m` proof above. Credit: the source predictor distinction is
from the pinned OpenAI Fourier manuscript; this scoped aliasing argument
was developed with substantial AI assistance for @CubeJerry.
