# A nonunitary support bound for a paid correction layer

**Proved for the stated exact linear circuit model. No new κ.** A single rank-one query layer cannot implement the actual normalizer N, or the two-stage correction C, with sublinear ordinary row-branching. The argument allows nonunitary arithmetic, zero workspace and arbitrary coordinate monomials. It is a Gaussian-depth bound, not an aggregate paid-moment bound.

## 1. The circuit model and support potential

For a finite matrix M over any field, write s(M) for the maximum number of nonzero entries in one row. Zero rows contribute zero. For composable matrices A,B,

    s(AB) <= s(A) s(B).

Indeed, a row of AB is a linear combination of at most s(A) rows of B. Their supports have a union of size at most s(A)s(B); cancellations only reduce it. This remains valid for rectangular matrices and singular maps. Coordinate monomials, zero initialization, coordinate selection and a COPY into new coordinates have row degree at most one. No invertibility or bound on coefficients is required.

Let V be the column multiplicity. A rank-r Gaussian child on one field, in either orientation, has row degree 2^(rV). Any disjoint parallel layer of such children has row degree at most 2^(r_max V). Ordinary monomial adapters do not change this bound. A literal nonself query Y <- Y + G X for a rank-r Gaussian G has row degree at most 1+2^(rV), including the unchanged destination baseline. A disjoint bank of such queries obeys the same bound, rather than multiplying the degrees of its distinct ports.

Write an entire circuit as a product of ordinary factors and paid layers. Let

    L_V = sum over ordinary factors O of log2(max(1,s(O))).

Let direct Gaussian layers have maximum ranks r_1,...,r_a and query layers have maximum ranks u_1,...,u_b. All ordinary additions, port mixtures, preprocessing, output adapters, workspace operations and their actual occurrences are included in L_V. Then

    log2 s(F_V) <= L_V + V sum_i r_i
                        + sum_j log2(1+2^(u_j V)).                 (1)

In particular, if all paid layers are rank one, with total layer count d_V,

    log2 s(F_V) <= L_V + d_V V + b.                            (2)

For a fixed finite layer template, L_V=o(V) gives an asymptotic support slope at most the sum of the layers' maximum ranks. Arbitrary coordinate permutations, including port-dependent spatial route changes, are permitted as degree-one factors. The result does not impose a common Fourier fibre or a unitary intermediate-state condition.

The final map is measured only on independent original main inputs. Initially zero ancillary columns can be deleted; doing so cannot increase row degree. Restoring zero ancillas or discarding workspace does not defeat (1). A free initial dense encoding of the original inputs is not allowed: its ordinary factors or paid layers must be included. This is a straight-line exact linear statement; nonlinear operations or approximate algorithms require another argument.

## 2. Actual normalizer and two-stage correction

The already admitted actual112-port normalizer is N=Q^-1 R0 Q. Every row has precisely 4^(V+1)=2^(2V+2) nonzeros. This is proved by the four nonzero R0 neighbors and the four distinct translations in each one-column block C_qh^-1 C_qj, with the scalar R0 coefficient applied once outside the tensor power.

Consequently an implementation with one direct rank-one layer must satisfy L_V>=V+2. With one rank-one QUERY layer it must satisfy

    L_V >= 2V+2-log2(1+2^V)
        = V+2-log2(1+2^-V) > V+1.                            (3)

Thus L_V=o(V) excludes either one-layer implementation, even with arbitrary nonunitary ordinary factors. The exact direct circuit Q, R0, Q^-1 is a sharp depth control: its two Gaussian layers have total rank depth2, its ordinary R0 factor has degree4, and its row count meets (1) with equality. This does not assert that two additive queries suffice, nor that depth2 is an optimal paid moment.

The separately admitted actual two-stage correction C has at least one row with 16*4^V nonzeros for every V>=2. Its source-bound proof is stronger: at least a fraction 1-24*2^(-3V)>0 of spatial rows has this support, after checking all affine collision systems. Therefore a one-query implementation of C requires

    L_V >= 2V+4-log2(1+2^V) > V+3.                            (4)

The N and C premises are pinned dependencies. The present proof extends the fixed-ordinary support observation to a paid layer with arbitrary nonunitary interleavings; it does not rebrand the earlier source-support theorem as new.

## 3. Postprocessing a coded output

Suppose a complete already-paid source has matrix E_V with

    s(E_V) <= c_V 2^(rho V),     log2 c_V=o(V).

If a subsequent correction has ordinary allowance L_V=o(V) and a fixed collection of paid layers of total maximum-rank depth d, then (1) gives

    log2 s(F_V E_V) <= (rho+d)V+o(V).

A desired whole Gaussian job of rank R has exactly 2^(RV) nonzeros in each of its rows, up to coordinate monomials. Hence a necessary condition is R<=rho+d. More generally the same conclusion holds when an endpoint's support slope is established directly. This proves a necessary correction-depth condition without requiring any intermediate operator to be unitary.

For example, an authenticated two-bank coded output with global row bound c 2^(23V) cannot yield even one independent rank25 Gaussian output using one rank-one query layer and sublinear ordinary branching. It needs depth at least2. Mixing the two banks is already permitted: one must use the global maximum23, not claim a stronger bound from the smaller support of only one bank. This numerical example is conditional until its actual source-rank premise is separately admitted.

An aggregate price follows only for a separately specified query template. If the only permitted repair operations are complete112-port rank-one query banks, each such layer costs112. Two layers then cost224. A lower bound on depth alone does **not** imply that arbitrary partial-port circuits cost224, nor that a higher-rank sparse layer or a redesigned interleaved source is excluded. Every such alternative needs its own paid profile.

## 4. Necessary scope controls

The ordinary assumption cannot be removed. Repeated sparse additions or port mixing can increase L_V linearly in V and build exponentially supported matrices without Gaussian children. The previously admitted clean-ancilla construction implements Q one column at a time with linear ordinary mixing; it lies outside L_V=o(V). Conversely, arbitrarily large scalar coefficients cannot defeat this theorem: they do not create a nonzero at a new matrix position.

The bound uses the actual layer schedule. Calls on disjoint banks may form one parallel layer, while a later call consuming an earlier output is a new layer even if the total number of calls is small. The theorem supplies no general rank-mass bound. It complements the earlier entropy theorem: entropy gives stronger price consequences in an explicitly unitary circuit class, while the present support argument tolerates nonunitary factors and arbitrary coordinate monomials but only constrains depth and ordinary branching.

The all-width proof is the elementary row-union inequality. Exact finite checks authenticate the actual N support, reproduce the source collision premise for C from its pinned receipt, and exercise nonunitary and cancellation controls. They are not used to extrapolate an asymptotic claim. No strict complex supplier, compatible BIT supplier, foundational assumption discharge or new complete κ follows.

Credit the earlier actual112 source, physical-interface, unitary-normalizer and two-stage-elimination authors for their pinned source facts. Root developed this paid-layer extension and its nonunitary scope for @CubeJerry with OpenAI assistance.
