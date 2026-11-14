# Exact proper-cover capacity of the full class reservoir

**Root theorem, depending on the independently checked class-reservoir kernel and real native geometry. No new kappa.**

Let k have characteristic two, V>=1, and let E be any subspace of the scalar class-reservoir quotient tensor k^V. All native block fittings under consideration have rows in C tensor k^V plus E. Write q_c for the nonzero quotient of class indicator u_c, and call class c enabled when q_c tensor k^V is contained in E. Let n_c be its size.

The checked kernel identity gives every row in class c the form K_i M+u_c(I+M). If M is nonzero, its support is exactly the canonical support: off-class canonical entries are M and own-class entries are I. Its exact capped proper-cover charge chi is2, as witnessed by the full canonical quadratic span. If M=0, the row is u_c I and c must be enabled. Its n_c-1 foreign lines are mutually orthogonal. For n_c<=7 they lie in one proper facet subspace, so chi=0. For n_c=8 they span the full rank7 facet but can be partitioned between two proper subspaces, so chi=1. In these cases gamma=chi exactly.

Therefore, for fixed E, the exact minimum total chi, and also minimum total gamma, is

    222 - sum_enabled c w_c,
    w_c = 2 n_c for n_c<=7, and w_c=8 for n_c=8.

The lower bound holds rowwise; it is attained algebraically by choosing u_c I on every enabled class and canonical rows elsewhere. No physical availability is granted. If the enabled q_c span rank r, their tensor span has dimension rV, so r<=floor(dim(E)/V). Conversely any subset of quotient rank r is enabled by its full tensor span at cost rV. The exact minimum with quotient budget at most rV is thus obtained from the weighted subset census.

| Quotient rank budget r | Minimum chi and gamma |
|---|---|
|0|222|
|1|208|
|2|194|
|3|180|
|4|166|
|5|154|
|6|142|
|7|128|
|8|120|
|9|104|
|10|72|

The independent native checker enumerates all32768 class subsets and their quotient ranks, giving this table. Worker C separately recomputed the weighted table and reviewed the rowwise argument; this arithmetic cross-check is distinguished from root's independent native-source reconstruction. The two-rank boundary uses classes1 and2, both of size7. It gives charge194 at quotient dimension2V, but its scalar fitting rank is11; it is not a legal source or a supplier certificate.

For every dim(E)<2V the table gives chi>=208. This is a source-specific family theorem even for arbitrary entangled subspaces E and noncommuting fitting blocks. It does not exclude other scalar envelopes or different global codes. Exact roots and real geometry remain separate from the characteristic-two value field.

Dependencies: the frozen class proof SHA256850b4fd5792f9afb21499fd0886c758416f003f0b043d292ca5b975ca0ca981c, native SHA25651203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78, and the admitted geometric-facet incidence proof. Credit Worker C, root, @CubeJerry and OpenAI assistance.
