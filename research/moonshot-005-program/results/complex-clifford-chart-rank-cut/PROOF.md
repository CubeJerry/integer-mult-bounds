# A global Clifford-frame price cut for the P104 scalar incidence graph

The complete 48-call #7830 price allows **9587.4244784095…** native units at saving 1/200. Every assignment of nine-axis Clifford frames to this scalar incidence graph costs at least **9598.81296**, including assignments with arbitrary new frames and any number of zero-rank transfers. The exact minimum of the sum of native Fourier ranks is **9,646**, attained by the original layout. A second price test bounds the full-interval saving of this architecture below **0.004392**. The results hold while its scalar incidence equations and 1,289 public birth and return chart roles are retained. Changes to the scalar graph, productive role list or caller remain open design choices. [#7830 native word and caller](https://github.com/Clear1nsight/integer-mult-bounds/tree/14c74c6a67108f675ac1196a5f2415ead0920e71/research/p104-chart306-chain)

## From literal arithmetic to the chart graph

Every ordinary form f reads its listed donor stocks at f’s sending frame, or at its terminal frame if it is a public output. Introduce a token for each paid or public sender and each paid or public arrival. Identify the sender token of f with the destination token of every literal donor to f. Public arrivals and public outputs carry their actual prescribed chart labels. Union-find gives 1,362 resulting scalar components, including 423 pinned components. The 5,707 original paid jobs connect 4,135 distinct component pairs, with one job for each original occurrence. Any rank-zero local monomial adapter retains its underlying Lagrangian and satisfies the same token equality. Allow independent new Lagrangians at every unpinned component.

Write H=F₂⁹ and Δ={(x,x):x∈H}, the fixed diagonal isotropic space in H⊕H. Under the upstream preimage convention a canonical subspace chart U has Lagrangian `L_U={(u,u+v): u∈U, v∈U^⊥}`. Thus `L_U∩Δ={(u,u):u∈U}`. An arbitrary exact Clifford T has chart L(T)=T⁻¹L₀. A transition has Fourier grade `9−dim(L∩L′)`. Global phase and signed monomials can further constrain realization; this lower bound grants every Lagrangian assignment. [Upstream frame convention](sources/general-clifford-frames.tex)

## Nine binary flags lower-bound every physical grade

Fix a flag 0=F₀<F₁<⋯<F₉=Δ. Give each L its nine bits `b_j(L)=dim(L∩F_j)−dim(L∩F_(j−1))`. Each increment is zero or one. For A⊂B⊂Δ the bit support of A is a subset of the bit support of B, since the quotient F_j/F_(j−1) has dimension one. Put A=L∩Δ, B=L′∩Δ, S=L∩L′ and d=9−dim S. Applying the support inclusion to A∩B bounds the Hamming distance of the two bit vectors by `dim A+dim B−2 dim(A∩B)`.

The last expression is the dimension of the image of A+B in the symplectic quotient S^⊥/S. Indeed A+B⊂S^⊥ and (A+B)∩S=A∩B. This image is isotropic because Δ is isotropic, while the quotient has symplectic dimension 2d. Hence the Hamming distance is at most d. This proof permits L,L′ to be arbitrary Lagrangians, without a nesting or canonical-chart constraint.

For a fixed bit j, every candidate chart assignment gives a cut in the 1,362-component graph with known terminal sides. At unit capacity per paid position, the maximum flows for the basis `(436,252,65,45,19,7,2,9,1)` are the integers in the table. The original chart assignment realizes every minimum cut simultaneously, so summing over bits proves the sharp 9,646 lower bound.

| Flag bit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Unit flow and incumbent cut | 977 | 1059 | 1105 | 1076 | 1122 | 1108 | 1103 | 1085 | 1011 |

## Exact weighted price on the same graph

Use the second flag with basis `(108,145,272,1,42,16,8,4,2)`. Assign nine integer capacities `c_ej` to each undirected component pair e, with scale C=100,000 and multiplicity μ_e. For each k=1,…,9 the verifier checks that the sum of the k largest capacities on e is at most `C μ_e k^(199/200)`. Directed integer-root bounds certify every check. These inequalities cover all bit subsets of size k. If an actual grade-d edge changes h flag bits, then h≤d, and the capacities paid across its changed bits total at most `C μ_e d^(199/200)`. This remains true when d=0. Summing nine independent terminal minimum cuts gives the following lower certificate.

| Bit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Integer flow | 102135024 | 106842633 | 110828532 | 109274903 | 103306376 | 109010703 | 108865849 | 108168584 | 101448692 |

The sum divided by 100,000 is exactly 59992581/6250 = **9598.81296**. Each flow value is checked against the capacity of its final cut and against all pinned sides. The native spending allowance is the positive-helper moment plus the fixed productive-minus-paid caller moment divided by 48, evaluated with exact outward integer intervals. It is smaller than 9587.4244784096. This comparison holds for each native visit independently, even if different callers use different internal frame assignments. [Capacities](author/capacities-best.json.gz) · [Exact flows](author/output/best/FLAG-RESULT.json)

Each single native transition of a fixed incidence graph costs at most 9^(199/200)<9. Therefore altering or removing one paid connection while preserving the existing ordinary equality constraints, and allowing arbitrary new chart labels everywhere, still leaves native cost greater than 9589.81296. This also exceeds the entire-caller allowance. A program that eliminates a paid site and rewrites its readers can change additional ordinary equality constraints and falls outside this one-connection statement.

Two additional diagnostics follow from the sharp volume cut. With z zero-grade positions, concavity on [1,9] gives native price at least `5707−z + ((9^(199/200)−1)/8)(9646−5707+z)`. This first test alone requires at least **827 zero-grade positions** just to meet the target allowance. The weighted certificate then rules out the full fixed graph at any z.

For a stricter architecture ceiling, put κ=549/125000 and t=1−κ. The replay chooses a rational λ and checks `r^t≥(1−λ)r^(199/200)+λr` independently for every grade r=1,…,9 with directed dyadic enclosures. Consequently every assignment's tariff is at least `(1−λ)9598.81296+λ·9646`. This exceeds the upper bound on its complete native allowance at t by more than 0.01318. Any saving κ′≥κ under the full-interval criterion would have to pass at this t and cannot do so. This ceiling concerns the fixed scalar graph and caller contract. [Exact ceiling test](author/output/best/CEILING.json)

## Additional exact result for nested orientations

If endpoint labels stay canonical subspaces and every paid pair remains nested, fixing the original direction of each inclusion yields 207 non-forced variables. Their lattice intervals have 197 two-element domains, eight five-element domains and two sixteen-element domains. Integer min-sum elimination, with exact comparisons of the resulting rank histograms, returns the original native histogram. The accompanying minimizer relocates twenty scalar components at identical price. This supplies an alternate chart labeling with the original incidence and scalar endpoint under the same mathematical chart contracts.

The direction of a single component pair can only reverse strictly if its ends have no other directed path in the old orientation and the lower/upper interval after deleting that relation permits proper reverse inclusion. These tests leave 63 of 4,135 pairs. Every corresponding exact optimum costs strictly more than the original. For two reversals, remove one relation first, test admissibility of reversing the other, and require the two deletion tests symmetrically. Of 8,547,045 unordered pairs, 3,165 survive. They all cost strictly more. Cases forced to equality already obey an orientation with fewer strict reversals. Both tests permit any subspace of F₂⁹, including subspaces absent from the original atlas. [Nested result](author/output/RESULT.json) · [Two-reversal result](author/output/PAIR-RESULT.json)

## Funded donor proposed in the live successor audit

At PR #7833 head `2b3176a88b4c46d4e1dc944843859634baa18b82`, the new right to fund a fifth chart-282 ingress with donor 100187 also withdraws that donor from chart 1098. Its old clock is 1010 and the compensated clock is 1011. Release the four direct readers 100622, 100222, 100610 and 100619, and release every affected downstream send at its existing time and endpoints. At each affected sender, permit every exterior observation with a causally earlier arrival to be carried forward. The resulting generous exterior contains the true physically available input space, by induction through the order of the 1,018 affected operations over 30 charts. It yields 12 distinct terminal exterior sets, covering 208 affected public rows. In each of the 208 cases adding that single required row raises the rational rank by one.

For example the nine exterior observations of terminal 154925 are 100188, 100620, 100739, 100741, 100783, 102118, 102128, 102130 and 102132. Their rank is nine and the target raises it to ten. Set original-axis inputs `x0=207/2, x2=−72, x41=−20, x45=1, x262=9/4, x777=−1` and the remaining axes to zero. This pulse vanishes on each exterior observation and evaluates to one on the target. The fifth ingress is therefore a legal funded send whose displaced donor cannot be restored through those fixed remaining endpoints and clocks. Changing endpoints, times, outside stock or other frozen events changes the premises. [Exact rows, pulse and complete 208-row test](author/output/DONOR100187.json)
