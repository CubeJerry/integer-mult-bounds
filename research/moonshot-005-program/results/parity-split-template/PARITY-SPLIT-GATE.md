# Complementary odd-population charts and one-arrival rigidity

**Status:** exact finite source geometry and a necessary template for a
restricted monotone carrier code. The tentative claim that every final
facet requires two X-carrier arrivals is false. This result explains its
countermechanism and does not exclude a larger coded construction.

The source pin is
`2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`.
Let L_j be each active first-X binary line vector and let
ell(z)=sum(z_k) over F_2. Every one of the104 L_j is odd: ell(L_j)=1.
The final first-Y facet is F_i=ker(L_i·−), of dimension8. Its48 foreign
Gram-correction donors are precisely the active lines contained in F_i.

## The parity identity

Let C=F_i∩ker(f) be any hyperplane of F_i. On odd vectors, f=1 is
equivalent to f+ell=0. Hence every active donor outside C lies in

\[
C'=F_i\cap\ker(f+\ell).
\]

Unless C is the even hyperplane F_i∩ker(ell), C' is another dimension7
hyperplane. The two charts partition the odd donor population; their
intersection contains only even vectors. Thus the outside population
usually spans a proper7-space, not the whole facet.

The complete source check is stronger: for all104 receivers and all255
distinct hyperplanes of each F_i, the outside support spans **exactly** C'
in all254 non-even cases. In the one even case it spans all F_i. The
histogram is26,416 rank7 cases and104 rank8 cases. The result remains
identical after removing the parent's seven already paid correction terms.
Those corrections are authenticated against parent compressed word
`1536c714dd3500709c7717b8687b53f98d7a30f482aa5b09e5c25a4a23cf8153`;
the checker verifies their exact source coefficients before removing them.

For the dependent triple i=0,j=1,k=98, the binary line vectors satisfy
L_i+L_j+L_k=ell (identified with bit vector511). Restricted to F_i, the
forms L_j+ell and L_k agree, because their difference is L_i. Therefore

\[
F_i\cap F_j\quad\text{and}\quad F_i\cap F_k
\]

are exactly a parity-complementary pair. Each contains24 of receiver i's
foreign donors. This is the source geometry used by the actual cyclic
dependent-triple construction.

## Rigidity below a hyperplane

If C≤F_i has dimension at most6, choose two distinct non-even hyperplanes
H_1,H_2 containing C. Such a pair exists: the annihilator of C inside the
dual of F_i has dimension at least2, giving at least3 nonzero hyperplane
forms, of which at most one is ell. Their parity complements H'_1,H'_2
are distinct7-spaces. Since N_i\C contains both N_i\H_1 and N_i\H_2,
where N_i is the residual donor support, the exact source spans give

\[
\operatorname{span}(N_i\setminus C)
\supseteq H'_1+H'_2=F_i.
\]

Thus **every** last receiver chart of dimension at most6 leaves a residual
outside support spanning dimension8. This follows for all lower subspaces
from the exact hyperplane certificate; it is not a sample of lower charts.

## Scoped consequence for one X arrival

Consider a code using monotone first-X carriers, one Y accumulator for
this receiver, and stationary local caches, subject to the following
**explicit source-support premise**. After accounting for one fixed global
Gram-packet contribution to the receiver, every further acquired correction
at chart C, and every X-carrier value used for that correction, has
original-X support only on initial lines contained in C. Stationary caches
must have local producers satisfying that same premise. No other receiver
relays or new transported common/owned records are supplied.

The premise follows for X-only cochart recoding of original X carriers and
stationary caches of those values, because monotone movement only enlarges
the containing chart. It does **not** follow merely from monotonicity if an
X carrier or cache can read the receiver's globally decoded Y payload or
another packet-bearing record. Such two-way X/Y feedback, recycling of the
global Gram contribution, or source support introduced by a retained
global record is outside this template unless the displayed invariant is
proved separately. Independence of the own-Y seed alone is not used to
assert that invariant. The exact binary support calculations above do not
require this additional coding premise; only the one-arrival consequence
and forced-decoder consequence below do.

Suppose exactly one X carrier arrives at F_i. Let C<F_i be the Y
accumulator's last proper chart, and D<F_i the X carrier's last proper
chart before that arrival. All residual donor coefficients outside C must
be supplied by the arriving X value, whose original-X support is contained
in D. The outside support span must therefore fit inside D.

The rank identities above imply that C cannot have dimension at most6 and
cannot be the even hyperplane. It must be a non-even dimension7 chart.
Its outside support spans its exact parity complement C', so D must equal
C'. Therefore a one-arrival solution, if it exists, has the forced template

\[
Y:\ C\longrightarrow F_i,
\qquad X:\ C'\longrightarrow F_i,
\qquad C'=F_i\cap\ker(f+\ell).
\]

This is a support necessity. It does not assert that either accumulator
can actually form the required source row, that their schedules compose
globally, or that donors can be restored for later source observations.
The dependent triple supplies one actual compatible instance.

### Why changing the global packet coefficient does not silently evade it

Within the same interface, allow arbitrary initial combinations of the
eight global Gram packets. Write that contribution as w·Vq_X. All later
local corrections at F_i have support only on initial lines in F_i. For
sources outside F_i other than i, the required coefficient is zero; for
the own source i it is the specified nonzero target coefficient c_i.

The checker establishes that the roots of the forbidden foreign sources
span the7-space perpendicular to v_i, and that v_i has norm squared8.
Hence w is forced to c_i v_i/8. This recovers the ordinary decoder when
c_i=1 and the coupled forward decoder when c_i=1/2. Arbitrary packet
coefficient cancellation is not a free way to remove the48 foreign duties
under the stated local-information interface. Other shared records or a
changed raw/common code can change this premise and remain outside scope.

## Multilayer template

For independent forms ell,f_1,...,f_m on F_i, the odd population is
partitioned by the affine bits b∈F_2^m into linear acquisition charts

\[
C_b=F_i\cap\bigcap_{j=1}^m\ker(f_j+b_j\ell),
\qquad\dim C_b=8-m.
\]

Each chart's odd part is the affine slice ell=1,f_j=b_j. Different slices
are disjoint, while all charts share the even subspace
F_i∩ker(ell)∩⋂ker(f_j), of dimension7-m. Dropping the last form gives a
nested parent chart. This gives the correct binary split geometry for
multilayer accumulation: a receiver may follow one nested branch, while
actual pivot carriers can bring other branch aggregates to its parent.

The formula supplies geometry only. At every split, the current aggregate
rows, pivots, preserved input dimensions, source observations, ownership
lifetimes and all route prices still need a coherent physical proof.
In particular, incompatible branch acquisitions cannot be added as if the
same raw carrier restarted independently at its initial line each time.

## Reproduction

```bash
python -B parity_split_gate.py --source /path/to/programme-checkout/research/shared-wire-split-composition/data/final.json.gz --output PARITY-SPLIT-GATE.json
```

The script checks all26,520 hyperplane cases, repeats the ranks with all
seven inherited cancellations granted, verifies the104 forced packet
decoders, and retains an exact24-donor counterexample to the rejected
universal rank8 claim. The complete deterministic case table is hashed
in the receipt and regenerated from the pinned source by the checker.
No asymptotic impossibility or new multiplication bound is asserted.
