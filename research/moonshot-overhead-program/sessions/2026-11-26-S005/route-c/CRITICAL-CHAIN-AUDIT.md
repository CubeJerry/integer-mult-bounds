# S005 independent AQ audit and discrete formal components

Status: **partial independent critical-chain audit; no contradiction found in
the examined chain. Three discrete supporting components are kernel-checked.
No full multiplier formalization or new overhead bound is claimed.**

Programme pin: 62d9d8e917379cb2edc17c9761e12e2345bc01f4.
OpenAI manuscript/formalization pin:
3344da59991ed94f9ba711217b29c1d760badfa6.

## 1. Audited claim and binding costs

AQ claims one fixed deterministic finite-alphabet multitape machine, exact
full product, and an absolute linear bound on all cells ever visited, with

$$
T(n)=O(n\sqrt{L(n)}\,2^{O(F(\log_2L(n)))}),\qquad
F(x)=(x^2\log_2(x+2))^{1/3},\quad L(n)=1+\log_2n.
$$

The first explicit scale-limiting interchange cost is
$\log_2(D_g(1+\lambda))=O(F(\log_2m))$. The numerical caller also pays a
polynomial-$m$ ordinary-work toll multiplying the actual interchange cost.
Its slower numerical arity is necessary for the stated argument. The new
formal components remove neither cost and establish no priority claim.

## 2. Independent recurrence reconstruction

AI fixes $\delta=1/R>0$, chooses odd $m(e)\asymp e^\delta$, and sets
$f(e)=\lfloor(e-\ell)/(m+2a)\rfloor$. Its compiler degree $K$ is fixed
before $R$, with $\delta K\le1/8$. Guards give $f\le e/m\le e/2$ and
geometric contraction of $y=\log_2e$.

The executed bill
$$
T(e)\le cm^K+\Lambda(e)T(f),\qquad
\Lambda(e)\le\sqrt m\,2^{CF(\log_2m)}
$$
has normalized local toll at most $ce^{-3/8}$ and child multiplier at most
$2^{CF(y)}$. For fixed $q<1$ and $y_{i+1}\le qy_i$,
$$
F(q^iy)\le q^{2i/3}F(y),\qquad
\sum_iF(y_i)\le F(y_0)/(1-q^{2/3}).
$$
Reading the positive-width chain backwards bounds $\sum_i e_i^{-3/8}$.
Finite expansion yields $T(e)=O(\sqrt e\,2^{O(F(\log_2e))})$ without
substituting growing parameters into a fixed-parameter asymptotic theorem.

B2's hyperbolic-completion inverse, complement projection, disjoint star
pivots and reserve-only elementary transitions were examined. Its same-side
Gram premise was checked against the characteristic-two label proof: the
first differing inner coordinate fixes an ordered letter pair, leaving only
$d-1$ variable coordinates on either side. Same-side words therefore cannot
be at distance $d$. Arbitrary all-unequal rectangles without that anchoring
would not automatically satisfy this premise.

## 3. Absolute payload and reserve ownership

UP stores $mr$ rank vectors, together at most one parent volume because
$mr\le N$. Unscaled sums survive rank gathering, so scalar-row-map
invertibility is not assumed. Positive deliveries reconstruct
$P_{:J}P_{IJ}^{-1}P_{I:}=P$; disjoint rectangle correction leaves the diagonal.

FP is bijective on all binary coordinates with completed map $I\otimes Q$.
It uses no zero embedding or coordinate projection. Short coordinate packing
uses $O(\log h)$ digit moves and a fixed number of reused arrays, without
transposing the exponential module index.

SR tags only one coarse role. With $32B$ raw roles and $B\ge2m+1$, its
$O(m)$-bit keys fit within an absolute number of parent volumes. Tags are
removed before paid converter calls, retaining raw $1/16$ child masses.

The global space argument requires both:

1. A child with a parked parent frame has at most half the parent's raw volume.
2. A full-volume reserve descent releases payload and reuses the same marked
   interval, rather than allocating a fresh interval farther along the tape.

[ArenaSchedule.lean](formal/ArenaSchedule.lean) proves the corresponding
abstract interval bound $\operatorname{span}\le2CV$, including arbitrary
sequential siblings and non-growing released reserve calls. Any number of
those reserve calls preserves exactly the same span. A failure control proves
three parked full-volume frames exceed the cap when $CV>0$.

The actual AQ allocator still needs an execution refinement into this
schedule. A live-space bound alone does not prove visited space.

## 4. Numerical recurrence and spectator product

NW chooses $x=\lceil\log_2(a+2)\rceil$,
$y=\lceil(x^2\lceil\log_2(x+2)\rceil)^{1/3}\rceil$, $m=2^y-1$, and largest
even $f\le a/A_m$, where $2m\le A_m\le4m$. Above a fixed base,
$y\asymp F(x)=o(x)$ and the logarithmic-width decrement is at least $y/2$.

Integration of $F'$ over $[x-d,x]$, $y/2\le d\le2y=o(x)$, gives
$$
F(x)-F(x-d)\ge c\,yx^{-1/3}(\log_2(x+2))^{1/3}
 \ge c'\sqrt{y\log_2(y+2)}.
$$
This pays the normalized recursive multiplier. After division by $\sqrt a$,
the local $m^KJ(a)$ toll has logarithm at most $(C_I+2K+O(1))F(x)$.
Choosing the final potential constant after $C_I,K$ pays that toll as well.

The exact integer path statement is: if $A_if_i\le a_i$ and
$W_i=2^{w_i}\le A_i^K$ with one fixed $K$, then
$\prod_iW_i\le a_0^K$. If $2^S\ge a_0^K$, the whole batch product and
each prefix divide the root spectator range $2^S$.

[BatchPath.lean](formal/BatchPath.lean) kernel-checks the product bound and
both divisibility claims. It does not formalize logarithmic rounding or a
physical numerical implementation satisfying its premises.

## 5. Precision, caller and coverage

Rational coefficient heights are polynomial in local $m$. Bounded-remainder
division produces $p$ fractional bits in $O(B^2+pB)$ steps for a $B$-bit
divisor. NW gives $B\le m^K=k^{o(1)}$, fitting its stated per-record invoice.
Its path amplification logarithm
$\sum_i m_i^K\le(1+\log k)2^{O(F(\log_2k))}=k^{o(1)}$
is compatible with one absolute $O(k)$ precision format. Exact permutations
create no numerical faults. Completed normalized children are unitary; local
unfinished maps retain separate norm majorants.

The actual integer caller has $Nk=\Theta(n)$, $k=\Theta(\log n)$, tested
short-axis shapes, $O(\log k)$ synchronized layers and selected Walsh width
$O(k/\log k)$. Its search and coefficient tables have polynomial degree
independent of AQ's arities. The examined formulas permit the stated
substitution without a growing proportional space coefficient.

Read: AQ, AI, NW, UP, FP, B2, compact interchange, spectral repair and compact
rational Walsh; actual source permutation and integer caller; relevant formal
interfaces. This audit has **not** rebuilt or re-refereed every inherited
finite cyclic-factor/predictor identity or every transitive source dependency.
The supporting formal lemmas do not close that gap.

The third file, [CopiedCountFormula.lean](formal/CopiedCountFormula.lean),
checks the literal copied Boolean-formula syntax rather than a shared
circuit. It proves the local adder truth identity, that the previous carry
appears once, degree at most $2^k$ for bit $k$, and size at most $m^5$ for
the balanced tree on $m=2^r$ unit-size leaves and $k\le r$. These are
formula-size and degree claims, not a complete cyclic-factor or tape proof.
Whole-word Boolean count semantics is not included in that first-wave file.

## 6. Formal source and new checks

Pinned OAI/Computability/NearSquareRoot/Main.lean has an actual proof through
a native interchange family, selected CRT/permutation/Walsh procedures and
a worst-case equivalence. The independent challenge's admitted statement
stubs are not the solution. The comparator permits propext, Quot.sound and
Classical.choice.

UniformWorstCaseSpec measures actual fixed-machine worst-case halting and
all visited tape/address pairs, but gives only a vanishing excess.
InterchangeROMBinary.RectPhysical uses fixed $\rho$ and a header/record mass.
Neither already states AQ's explicit envelope.

The source requires Lean 4.34.1. A matching compiled Mathlib/OAI closure was
unavailable for a source build. The pure-Std files were compiled with the
available Lean 4.35.0 release, commit
eb6cafb7290e8bd5f2937522d8d804f58f02bafc.
Commands, outputs and hashes are in formal/verification.json. The files
contain no admitted proof, new axiom or unsafe declaration.
No source build, comparator run or full-multiplier kernel check is claimed.

## 7. Open next questions

- Refine actual UP/SR/reserve tape addresses into fixed ArenaSchedule fences,
  then apply the source visitsAtMost_of_tape_fences theorem.
- Establish a physical interchange contract for general monotone envelope $J$,
  retaining machine and visited-cell specifications. Fixed-$\rho$ statements
  alone cannot formally certify a variable envelope.
- Change physical geometry or polynomial-arity numerical work for a new rate.
- Independently examine the unbounded cyclic-factor/predictor chain before
  describing this partial work as a full theorem audit.

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT assistance.
OpenAI's pinned sources, S002 finite constructions and S003 A/B/C suppliers
retain their credit. This review is separate from author admission records.
