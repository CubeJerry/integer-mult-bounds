# The exact common-preload rank of a single masked staircase

**Author theorem; independent review pending. Proved algebraic interface and exact native applications, not a new supplier or a new kappa.**

This result follows a network-coding construction attempt. It rules out replacing many independent staircases by one final mutable staircase supplied with a few earlier common broadcasts. It does not rule out genuinely interleaved staircases, ascending nonlocal relays, arbitrary later Y-to-Y coding, changed source interfaces, or nonlinear algorithms.

## 1. The physical and algebraic interface

Let r_1,...,r_s be nonzero real source vectors, in a fixed order, and F_i=r_i^perp. Set C_0=R^d and C_i=intersection_(k<=i) F_k. Repeated charts are allowed; they do not create zero-cost nontrivial movement. Independent values x_i,y_i lie in K^V, where K is any characteristic-two field and V>=1.

A final main record P starts at Hub carrying an arbitrary V-row linear function Hx of the selected x inputs. It descends through C_1,...,C_s. At stage i the actual original receiver Y_i is at C_i, and the final interaction is exactly

    Y_i <- Y_i+P;  P <- P+Y_i.                         (1)

Thus (Y,P) maps to (Y+P,Y). Receiver i is correct after this interaction and then may ascend to F_i. No subsequent nonlocal contribution to that receiver is granted.

Before (1), Y_i may have arbitrary original-Y precoding and an X preload from

    E + L_i,                                         (2)

where E is ONE fixed common linear code in K^(sV), and L_i is the space of rows supported on selected source lines contained in C_i. The entire code E is generously made available at every required receiver; actual acquisition, dissemination, storage and price are separate. Every local form in L_i is also generously granted. This is therefore a relaxation of an actual chronology of common broadcasts and local ascending acquisitions.

Other independent original inputs may be present: project all coefficient rows to the selected x columns. The rank below is the rank of that projected common code; the full common code has at least this rank. Arbitrary noncommuting V-by-V blocks are permitted in every preload. No scalar-tensor or commuting assumption is made.

Define a **bad position** j in {2,...,s} by

    r_j is nonorthogonal to at least one r_k with k<j.

Let b be the number of bad positions.

## 2. Exact theorem

**Fixed-order theorem.** The least possible dimension of the common preload code E for the algebraic interface above is exactly bV.

In particular, r full-width common broadcasts require r>=b, even if they are jointly coded by arbitrary operators. A collection of r earlier broadcasts plus this final main staircase therefore needs at least b+1 full-width channels in this interface. This is a channel-dimension consequence, not a physical-price theorem. Funded observations must be charged according to their actual contract, not relabelled as fresh full Hub routes.

**Order-optimized theorem.** Let omega be the maximum size of a pairwise-orthogonal subset of the selected real source lines. Minimizing over all target orders gives

    min_order min_dim(E) = (s-omega)V.                 (3)

The optimum statement concerns this single-final-staircase interface. It is not the optimum number of packets in the full physical source problem.

## 3. Proof of the forced tail equations

Restrict to selected X coefficients. Let A_i be the V-row X coefficient matrix of Y_i immediately before (1). Correctness requires A_1+H=J_1, where J_i denotes the identity V-block at selected input i and zeros elsewhere. Since the post-stage packet is the old Y_i, induction gives

    A_i = H + J_1+...+J_i.                            (4)

No claim about the Y nuisance variables was used to derive this necessary equation. Since no selected source line is contained in C_s (each has nonzero inner product with its own normal), L_s=0. Thus (2),(4) imply

    H+J_1+...+J_s belongs to E.                        (5)

Subtract (5) from (4). For every i, the tail matrix

    T_i=J_(i+1)+...+J_s

belongs rowwise to E+L_i. There are therefore local matrices B_i, supported in C_i, such that every row of

    R_i=T_i+B_i                                       (6)

lies in E. This removes the arbitrary starting main code H without assuming that it was the full sum originally.

## 4. A universal block-triangular rank certificate

List the bad positions j_1<...<j_b. For each j_a use the V rows R_(j_a-1) and the V input columns of x_(j_a).

The diagonal block is I_V. Indeed T_(j_a-1) has that block I_V, and x_(j_a) is not local to C_(j_a-1): a prior normal is nonorthogonal to its source line, by the bad-position definition.

Every block strictly below this diagonal is zero. If a'>a, the earlier input j_a belongs to the first j_(a')-1 normals. Its block in the tail T_(j_(a')-1) is zero, and its own nonzero norm forbids its source line from lying in C_(j_(a')-1), so the local correction also has zero block there.

The selected bV-square submatrix is block upper triangular with identity diagonal. Its determinant is one over every field. Hence the stack of the R_i has rank at least bV. Its row space is contained in E, proving

    dim E >= bV.                                     (7)

This proof covers singular and noncommuting preload blocks, every V, arbitrary characteristic-two extension fields, and repeated/dependent real normals. It is an exact minor argument, not a finite search or an assumed rounding to full widths.

## 5. Sharpness and the best order

Call the first position and every non-bad position good. A good source r_j is orthogonal to all earlier source vectors. Choose

    E=span{all V coordinate rows of x_j: j is bad}.

For each i, the tail T_i modulo E is the sum of the future good inputs. Every such source r_j, j>i, is orthogonal to all the first i normals, so this remainder is local to C_i. Thus all conditions (6) hold with dim E=bV.

Set the main initial packet to sum_j x_j. Precode original Y values at ground by ordinary prefix sums. Give Y_i its X tail T_i using the displayed common and local decomposition. Then its incoming value is

    Y_i = sum_(j<=i)y_j + sum_(j>i)x_j.

The existing orthogonal-staircase feedback identity (1) completes Y_i=y_i+x_i successively and leaves P=sum_j y_j after the last stage. This is an algebraic realization in the relaxed acquisition interface; it does not make the local tails available physically or free of charge.

All good positions form a pairwise-orthogonal set, so their number is at most omega and b>=s-omega. Conversely, place a largest orthogonal set first. Those omega positions are good. Every remaining source is nonorthogonal to at least one member of that set; otherwise it could be added to it. Thus every remaining position is bad and equality holds, proving (3).

The sharp scheme is informative: it simply broadcasts each bad coordinate independently and reserves the final staircase for the orthogonal structure. Arbitrary common coding cannot improve the rank of this particular interface.

## 6. Actual native applications

The native BIT source is pinned at SHA256 `51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78`. Its 111 distinct real lines lie in R^8 and include the eight coordinate lines. Therefore omega=8 exactly. A single final masked staircase serving all 111 targets needs at least 103V dimensions of common preloads, plus its own V-wide main packet. This is vastly outside the current q8/q9/q10 design range and closes that proposed serialization route. It does not exclude a coordinated family of several final buses whose live states interact.

For the previously certified native pentagon (92,36,54,38,55), the orthogonality graph is C5 and omega=2. A final staircase serving all five targets needs at least 3V common preload dimensions. Thus one common seed followed by one standard full staircase is impossible, and even two common seeds are insufficient. Three isolated orthogonal-class packets already suffice for the five targets, whereas this interface needs four channels in its most optimistic dimension accounting.

The universal lower bound is the written theorem. The verifier checks the exact native graph, all 120 pentagon orders, and every scalar local completion in those orders; it also checks arbitrary block completions and illegal-locality mutations. These checks validate the fixed source and examples, not the all-field proof by extrapolation.

## 7. What remains open

A two-packet pentagon, or a larger joint source with fewer packets than its isolated orthogonal cover, must use a different chronology. In particular, several active packet states, nonlocal ascending Y/X histories, or a changed final interaction may permit capabilities excluded by (1),(2). Existing independent-channel odd-cycle obstructions and the present common-preload theorem have different hypotheses; neither is silently promoted to a general two-packet impossibility.

The retained native source, all required original restorations, actual acquisition of every preload, cochart operations, movement jumps, owned lifetimes and erasures, precision, compiler, uniformity, BIT completion and compatible complex supplier remain to be proved for a successful new word. No foundation is discharged and no complete kappa is claimed.

## Literature bridge and credit

Forney's minimal-realization/shortest-basis perspective motivates looking for an exact state-dimension invariant rather than optimizing numerical tariffs: G. D. Forney Jr., *Minimal Realizations of Linear Systems: The Shortest Basis Approach*, arXiv:0910.4336v3, https://arxiv.org/abs/0910.4336 . Blasiak and Kleinberg's serializability work emphasizes that algebraic endpoint and cut feasibility alone does not supply a chronology: *The Serializability of Network Codes*, arXiv:1001.1373, https://arxiv.org/abs/1001.1373 . Neither paper is asserted to prove this source-specific staircase theorem.

Credit @CubeJerry and the persistent programme; the original E8/BIT source and its retained scalar code; the existing complete orthogonal staircase, mixed-Y feedback, and native odd-cycle packages. This exact common-preload rank theorem and construction attempt were developed by the S013 construction worker with substantial OpenAI assistance. Independent review is a separate pending gate.
