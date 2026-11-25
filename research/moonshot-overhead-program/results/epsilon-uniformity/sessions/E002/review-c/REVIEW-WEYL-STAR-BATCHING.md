# Independent review of the Weyl-star batching component

Reviewer: E002 conditional review C. Gate: **PASS for the specified local algebra and tape composition, with the declared row-mixing and established address-primitive invoices**.

Reviewed complete note SHA-256
`8472657f7ac8307c1fa99908918a45ba3901048cd31f3a757111ea0c01a4bb02`, and complete checker SHA-256
`4f1b22db3b25ec520fd6e527d1e3eec5c1d6daea7b38a2eb2de4cc81e49c4905`.
I read the pinned tape `permutations.tex` controlled-small-block lemma and its proof, together with E002's active-field/interchanger substitution. This review does not claim applicability to all retained Fourier middle maps.

## 1. Algebra and occupancy

For s nonzero, t is an actual nonzero pivot of s. The map `x -> (u=x+x_t s, epsilon=x_t)` is bijective when the forced zero coordinate u_t is replaced by epsilon. Its inverse is `x=u+epsilon s`. Thus no independently occupied coordinate is discarded or assumed zero. The same invertible map is applied to every query field while s and xi remain unchanged.

The phase splits as `xi dot x=xi dot u+epsilon (xi dot s)`, and translation by s flips epsilon while fixing u. This gives WB3 with the stated order `Z^delta X`. Direct multiplication verifies

`D_delta^(-1) Z^delta X D_delta=i^delta X`,

and hence `G_delta^(-1) Z^delta X G_delta=i^delta Z`. The inverse has its exact factor 1/2. The application order in the note is correct: layout, inverse common basis, pointwise diagonal row sum, common basis, inverse layout. The s=0 branch is already diagonal and correctly omits these changes.

Every B_j acts on row indices at each fixed address and therefore commutes with the address bases. No commutativity between different B_j is required. Expanding Q(i) in its two rational basis components is exact and gives the stated factor-two volume cost; the rational target acts separately on arbitrary input components.

## 2. Controlled-block physical interface

The pivot-dependent cyclic position rotation is realizable without padding f. Binary powers of the f-cycle express the required shift, and each fixed position permutation is a product of two involutions. Each layer consists of disjoint two-bit swaps; its controls are only the unchanged bits of s. Those are valid constant-size block permutations for the source lemma.

After the pivot moves, epsilon is excluded from the target set. The remaining coset shears flip distinct one-bit targets using controls from s and the m epsilon bits. Their total is f+m, which is at most half of a=(m+2)f for f>=2. This provides the fixed free fraction required by the source guard. The f=1 branch has no such shear. The inverse reverses the same transformations and restores all occupied fields.

The source small-block lemma requires a polynomial-time table generator **at each control setting**. The note's table-generation claim is valid in precisely that sense: finding t, selecting a fixed power of the cycle, and reading the needed s bit are polynomial-a computations. It does not require or justify materializing a table for all 2^f settings of s. Reading the claim through its explicitly cited source interface avoids such an exponential table assumption.

There are O(log(f+2)) position layers and one coset-shear layer. Substitution of the completed interchanger into the established controlled-block processor yields the whole-active-width WB6 cost, with fixed logarithmic powers. Controls, guards, exceptional-record handling and all rearrangements are charged. Narrow active widths use the stated direct branch; their extra factor is absorbed by the fixed polylog(k) allowance.

Each one-bit Hadamard or inverse can move the specified address bit to an adjacent-pair position and back by ordinary split/merge passes of full volume O(V). Processing the m bits therefore adds O(mV) ordinary work, not m recursive f-field calls. Dot products can be computed by scanning mf address bits, at most the active O(k)-bit counter/record budget. The declared polynomial-m row-matrix arithmetic remains a separate ordinary invoice. This establishes WB7 under that invoice.

The common layout itself uses only a fixed number of reused full-volume regions. The exact interchanger contributes its established visited-region envelope, and row-mixing buffers retain their own explicit polynomial-m bound. The note does not incorrectly strengthen an arbitrary row-matrix supplier's workspace requirement.

## 3. Precision and reuse

Unnormalized H and its rational inverse need no numerical square root. Intermediate common-basis norm growth has logarithm O(m); phases have unit modulus. Polynomial-m coefficient heights and row arithmetic remain within the declared local precision family. A complete multiplier would still need its global event/path guard, as the note says.

For a sequence with the same W_j family and unchanged parameter fields, the identical C_s and G_delta conjugate every stage. The transformed stage matrices act pointwise on rows; their products may be noncommutative on row indices but still require no intervening address basis change. Entry and exit bases can therefore be paid once for the whole sequence. This is an actual reuse theorem for this operator family.

Different rectangles having individual Weyl representations do not establish a common basis for their sum. Nor may the retained predictor polynomial be distributed over rectangle summands. The note explicitly excludes both invalid inferences. Rebuilding the basis at every Theta(sqrt m) stage retains a positive arity power, so this local theorem alone proves neither NI5 nor RV-W.

## 4. Independent finite replay and decision

The exact checker and note were copied to `e002-review-c/replay-weyl/` and executed independently. Its receipt binds both hashes. The checker uses integer pairs for Gaussian integers and keeps the full inverse-Hadamard power-of-two denominator, so its comparisons do not depend on floating-point tolerances. It tests occupied-layout bijections, phase/conjugacy identities, complete weighted pencils, a two-stage reused basis, and wrong-phase/omitted-layout controls. Row-matrix generality follows from the commuting tensor-factor argument rather than these scalar-weight tests.

I accept the specified positive local component. It demonstrates why separated nontrivial-map application volume is not a physical lower bound. The actual source middle-map classification, the common basis across all relevant contributions, and the global precision/space composition remain distinct unsupplied gates. The admitted unconditional envelope remains V.

Credits: @CubeJerry; the pinned controlled-block processor; E002's physical primitives; standard Weyl/Pauli identities; the batching author; substantial ChatGPT multi-agent assistance. No full-machine execution, formal verification or priority claim is made.
