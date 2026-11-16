# Independent coherent first-pivot review

**Accepted in the stated interface: R20=0 and an everywhere invertible first pivot R00, with the declared clock and any fixed diagonal second interface. Other first pivots and non-diagonal second interfaces remain open.**

The root review reads the entire proof and relies on the separately reviewed fixed-width tensor-separation and support argument. The new checker imports no author implementation. It checks the actual 16-address source and a separate transport model occupying all sixteen joint quarter-phase sectors, then verifies the block formulas with free noncommutative SymPy coefficients. The second model checks normalization on all sector values; it does not substitute for the native source or prove the obstruction by sampling.

Let the first column be (s_b,t_b,0), with s nonzero in all four scalar sectors. For G_b=[[s_b,0,0],[t_b,s_b,0],[0,0,I]], the literal relation a s_b=s_a a and its t analogue give

    G_a^-1 L G_b = [[a,0,0],[s_a^-1 s_b,a,0],[0,0,I]].

The two t terms cancel in their actual order. This is a symbolic identity for every permitted s and t. The new cross coefficient w=s_a^-1 s_b is a diagonal ordinary unit and generally differs from I; the independent all-sector control detects that difference. For a leading lower shear with s=1, the entire t parameter is just an ordinary output gauge. Neither normalization declares that gauge free.

After normalization, the first interface has the displayed shape [[I,bh,c],[0,dh,e],[0,fh,g]]. Exact multiplication gives the three pre-Q rows and the q11 equation in the proof. Because b,d are quarter-control coefficients, a b h a and a d h a have the same at-most-two support bound as the earlier clock terms. The term w b h a also has at most two support per one-column row. Therefore all competing terms in the critical second-row equation have at most four support after the final a, while -w a^2 q11 a has eight. Since w is a unit, separation forces q11=0. The first-row equations already give q01=q12=0 and q00 a=a q11, so q00=0 as well.

The same block-triangular argument forces q02,q10,q21 to be units. The ordinary part of the third-row first entry is g q21, so g=0. The normalized first matrix's lower two-by-two block remains invertible; after g=0, a column permutation makes it triangular with diagonal e,f, hence both are units. These arguments use finite-dimensional square blocks and do not require a commutative determinant shortcut.

The rank-two component now has a minor [[A,a^2 q02],[f h a q10 a,0]], where A need not vanish. Both off-diagonal blocks are invertible. The first is pure rank two. Every term of the second has four-support; absence of non-Gaussian endpoint components places the entire second block in rank two. A block matrix with invertible off-diagonal entries and zero lower-right entry is invertible regardless of A, so this component has rank at least 2D, contradicting the required D. This is the all-width support/separation/rank proof, not a conclusion from a search failure.

The independent control with conditional sector matrices (identity, active swap, identity, identity) has invertible full routing in every sector but first-pivot values (1,0,1,1). It violates exactly the unit-pivot premise while preserving R20=0. Thus the theorem cannot be extended to conditional pivot changes merely by citing invertibility of R. A first column entering the idle bank, a different clock placement, or a second interface with physical address permutations are also outside the theorem.

All native calls, ordinary output gauges, clocks, scalar-sector recipes, inverses, body services, tapes and precision charges remain. This result directs construction away from a redundant parameter family; it supplies neither a profitable endpoint nor a strict complex supplier. Both suppliers and all five foundations remain required. No new complete kappa.

Author: Worker B. Independent normalization and proof review: root. Credit @CubeJerry and the preserved source, tensor-separation and ordinary-compiler contributors, with substantial OpenAI assistance.
