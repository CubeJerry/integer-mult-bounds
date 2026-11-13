# Independent review: singular-cell historical fitting

## Verdict and scope

I find the singular-cell theorem's stated algebraic conclusions sound under the
path, source, cache, and no-Y-feedback hypotheses in
`worker-b/scattering-feedback/PROOF.md` and `SCOPE.md`. The review is
independent of B's 2-by-2 checker: I rederived the generalized-inverse
parameterization and the chart induction, then wrote a separate GF(2)
exhaustion for local controls. The finite check is only a negative-control
check; it is not being used as a proof of the all-field theorem.

The result is a historical-information upper bound and, with the admitted
fitting-rigidity premise, a support obstruction. It does not make the
historical coordinates independently selectable or physically available,
and it supplies no transport, lifetime, erasure, or price credit. The fixed
even-m calculation below is a movement-only budget comparison, not a complete
word or a sufficient construction.

## Local singular-cell algebra

At a cell C, take the actual aggregate packet-through map
`D : P_in -> P_out`, and let `nu = dim ker D`. Choose a complement
`P_in = ker D ⊕ S` and a complement of `im D` in the packet-output space.
Define `R` as the inverse from `im D` to `S`, extended by zero on that output
complement. Let `J` inject the kernel and `h` project onto the kernel along
`S`. Then

```
RD = I - J h,  DR is projection onto im D,
DJ = 0, hJ = I, hR = 0.
```

For the *actual* cell values set `W = P_out - C X_in` and `T_C = h P_in`.
The cell equation gives the necessary image compatibility
`(I-DR)W = 0`, and then

```
P_in = R(P_out - C X_in) + J T_C.
```

Substitution into the actual `X_out` and history equations gives the formulas
in B's proof. Conversely, compatibility plus this kernel coordinate
reconstructs the cell input exactly. This does not allow an arbitrary
incompatible `W`, and it does not grant independently realizable `T_C`s.
Each `T_C` is defined from the actual arrival `P_in` in that cell.

My separate GF(2) control enumerated all 16 two-by-two `D` matrices, factored
each kernel projection as `J h`, and checked `hR=0`, `DJ=0`, the reconstruction
identity on all 256 two-by-two `P_in` matrices, and ten singular-image
rejections. It recovered the nullity counts `{0:6, 1:9, 2:1}`. These controls
pin the compatibility and missing-kernel negative cases but do not replace
the dimension-free complement argument.

## Boundary and chart induction

Use `Z_0` equal to the q whole-V packet values at their **first arrival** at
zero, before zero-cell operations. Arrivals can occur at different times;
they are one boundary value per persistent packet path, not a claim of
simultaneous availability. Since all non-Y sources start on positive
dimensional lines, caches start at zero, and Y cannot feed packets or caches,
every zero-chart X/packet/cache history is a linear function of these actual
first-arrival values. This needs no inverse of the zero through map.

This choice is material. A packet can arrive with p, be copied to a
stationary zero cache, and then be updated by `P <- P + cache`, leaving a
later pre-CLEAR packet value zero while the earlier history still contains
p. The terminal packet payload is therefore not a valid replacement for
`Z_0` in the singular case. B's checker includes this countercontrol.

For each visited nonzero proper chart define `T_C=h_C P_in` from the actual
packet arrival, and stack

```
G = ( Z_0, (T_C)_C ).
```

These are actual linear functions of x and may be dependent. Induct by
increasing chart dimension. At C, every ascending X arrival comes from a
lower chart already normalized (or is an original input born at C). Every
descending packet departure `P_out` is the same value arriving at its next
lower chart, already normalized. Apply the exact local formula above; all
terms involving `T_C` go into the global coefficient on G, while the
remaining x-columns stay inside the lower/source charts and therefore inside
C. Compatibility is retained at each cell. This also explains why no
Hub-cell inverse or Hub nullity is needed for the claimed histories at proper
charts: any Hub information that reaches a lower chart is represented by its
actual lower-chart arrival and then by `Z_0` or a lower `T_C`; Hub-only
histories cannot travel to a lower Y facet under the no-copy/no-Y-feedback
interface.

The coordinate-count bound is then immediate:

```
rank(G as a map of x) <= q V + sum_C nu_C
                     <= q V + V sum_C q_C
                     <= 8 q V.
```

Each of q monotone Hub-to-zero packet paths visits at most one chart at each
of dimensions 1 through 7, so `sum_C q_C <= 7q`. Skipped chart dimensions
only reduce the count. The bound does not say any of these coordinates is a
free source or an independently addressable register.

## Fitting and refined facet support

After separating the G part, a local remainder at chart C is supported only
on original source lines contained in C. At a target facet F_i, every
cocharted X input has a proper predecessor chart, and every packet output has
a proper successor chart. The Y_i remainder accumulated before F_i is
supported in its own last proper chart. Other Y paths cannot arrive at F_i:
their distinct seven-dimensional terminal facets are incomparable, and
moving Y copies are excluded. Cochart Y mixing along Y_i's route remains
inside its last proper chart.

Therefore the final residual support is contained in the union of at most
`1 + r_i + s_i` proper subspaces: Y_i's last proper chart, the r_i X
predecessors, and the s_i packet successors at F_i. Under canonical foreign
support, the required contact set has at least 55 root lines. The separately
reviewed universal E7 result says a union of any two proper real subspaces
contains at most 52. Thus `r_i+s_i >= 2` for each of 111 target facets. The
111 X paths plus q=9 packet paths can supply at most 111+9=120 such visits,
versus 222 required. This contradiction rules out canonical foreign support
for the actual historical fitting, regardless of complement/generalized
inverse choices.

The fitting part remains conditional on admitted premises: characteristic
two, actual BIT contact geometry, minrank 9V, and canonical fitting support
for scalars (or the stated all-V invertible-Schur / fixed-decoder premise).
For scalars, rank-nine rigidity plus the support contradiction implies
`rank(A) >= 10` and historical span dimension at least 10. For general V,
the proof correctly leaves the singular-Schur stratum open: either
`rank(A)>9V` or a rank-9V fitting lies in that unresolved stratum. No general
all-V `10V` claim follows.

The direct all-V consequence is sound without fitting rigidity: one packet
has `rank(A) <= 8V < 9V`, so it cannot complete all 111 targets in this
interface. More generally `q V + sum nu_C >= 9V`, hence q>=2. This is a
necessary information bound only; it does not transfer the old fresh-packet
count to historical modes after singular exchanges.

## Fixed-even-m movement comparison

The candidate profile specified for this screen uses q=8 packet paths and
unit-rank moves on all routes:

```
111 X paths: 111*(8-1) = 777 unit moves
111 Y paths: 111*(7-0) = 777 unit moves
  8 packet paths: 8*(8-0) =  64 unit moves
                                      total = 1618
```

At t=199/200 a rank-one MOVE costs exactly one, so this selected all-unit
profile has movement moment 1618. From the pinned fixed-even-m caller,

```
A_m = (N-H)_t + m/(36(m-1)) * (T2-P2)_t
```

is the available Q movement-moment allowance. With
`(T2-P2)_t < 0`, A_m increases with m. My separate 192-bit directed-root
calculation from the pinned histograms gives:

| even m | Q allowance interval (display) | difference from 1618 |
|---:|---:|---:|
| 2 | 1609.4157908658 | -8.5842091342 |
| 4 | 1617.6391837627 | -0.3608162373 |
| 6 | 1619.2838623421 | +1.2838623421 |

Equivalently, writing `E=(N-H)_t-1618` and `D=-(T2-P2)_t>0`, the exact real
threshold is

```
m >= 36 E / (36 E - D),
```

which is bracketed by the receipt at approximately 4.28858525225. Thus m=6
is the first **even** m whose caller has room for this movement-only profile.
This only says the tariff allowance does not reject 1618 MOVE units. Because
`q^(199/200) < q` for q>1, it is not a lower bound for alternative
jump-based schedules; and it says nothing about whether the paths can be
scheduled to realize the needed modes, compatible fittings, source
acquisition/restoration, ADD/INIT operations, caches, or the complete Q
contract. In particular, m=6 is not a full-word or kappa result.

## Pinned artifacts

The reviewed B artifacts are the exact paths and hashes in
`MANIFEST.json`. The parent invertible-through proof SHA is
`5713d1b4e06be85211c3ef0bd8b4312090554dbb6a55f35e2394415a92c14d18`; B's
new proof SHA is `8511f06a30329e7708d8d20f843ca16c426e8870ae03b0e26ffc025a0cb98172`.
The B result is explicitly a local control receipt; it does not itself prove
the all-field induction or the E7 geometry.
