# A sharp sum bound for proper decoder and payload directions

**Author proof awaiting independent review.** For one paid copy at exactly
nine receiver-downset records, let p count nonzero destination lines and
q count payload blocks whose U-projected native-root support has real rank
seven. Then p+q<=11 for every positive width and characteristic-two field,
including noncommuting vertex gauges. Ground arrivals are permitted. This
is not a formation tariff or a scaled b>1 bound.

## Finite incidence certificate

Use the25 proper directions P from the independently reviewed induced95
support certificate, SHA256
`012018d59ce8227282749100b26eef2d3a4013dbb04d48d0bca030f3c036c963`.
For an independent subset D=(lambda_1,...,lambda_k) of P, evaluate
E_D(mu)=(lambda_i dot mu)_i. Let s(D) count coordinate unit vectors
appearing among evaluations of P, and let r(D) be the binary rank of
proper vectors with evaluation zero.

A dual basis to a basis extending D has at most s(D)+r(D) proper members:
nonzero evaluations must be distinct coordinate units; the other proper
members are independent in the common kernel. This bound is attainable:
choose one proper representative for each available unit evaluation, any
representative for each missing unit, an independent proper kernel basis,
and extend that to the full kernel. These nine rows are independent by
evaluation, and their dual basis extends D.

Exact enumeration gives:

| k | All subsets | Independent subsets | max(s+r) |
|---|---:|---:|---:|
|3|2300|2300|7|
|4|12650|12545|7|
|5|53130|50925|6|
|6|177100|154864|5|

The checker derives every evaluation and rank by binary arithmetic and
constructs completed dual-basis witnesses. The separate C++ discovery
census for k=0,...,9 is not a proof dependency.

For a pair of dual bases let p* and q count proper directions on the two
sides. The property is symmetric under exchanging the bases. If their sum
were at least12, the smaller count would be at least3. Counts3,4,5 would
require the larger to be at least9,8,7, contrary to the table. If both
counts are at least6, any six proper directions on one side force at most
five on the other. Thus p*+q<=11. An explicit completion with four proper
decoder directions and seven proper payload directions proves sharpness.

## Whole records and arbitrary vertex gauges

At nine width-V cuts, the fitting has rank9V and factors

    A_i=U_i (xi_i^T tensor I_V) S,
    C_j=S^-1 (xi_j tensor I_V) U_j^-1.

Every U_i and S is invertible. A decoder event block with proper support
lies in its unique shortening lambda tensor k^V, lambda in P. Its V
independent columns have factor lambda tensor G with G invertible.
The proper scalar directions are independent, or those whole blocks
would be dependent. Similarly, a proper payload event has factor
mu tensor H with H invertible and independent scalar directions.

Inverse products between row event e and column event f give

    (mu_e dot lambda_f) H_e G_f = delta_(e,f) I_V.

Invertibility makes the scalar evaluation zero unless the event indices
coincide, when it is one. Proper row directions therefore have distinct
unit evaluations or lie in the common kernel. The finite table applies
without commuting matrices. Exchanging S and S^-T proves the symmetric
sum bound for proper block counts. These are whole block supports, not
freely selected coordinate lanes.

Every nonzero physical destination has a proper decoder support by the
equality-destination theorem. A ground event may also have proper support,
so physical p is at most the proper decoder count p*. Thus p+q<=11.
Ground destinations plus full-support payload blocks consequently number
at least7, counting possible overlap between those two categories.

## Scope and attribution

Sharp algebraic witnesses are not chronological source words. They do not
establish formation locations, source access, price or attainable delivery.
For b>1 event factors inside a bV shortening are rectangular, so this
argument gives no scaled bound. More than nine events changes the premise.
Credit C's induced95 geometry, root's finite evaluation and block proof,
the independently reviewed all-line coupling, retained source/rigidity
authors, @CubeJerry and substantial OpenAI assistance. No complete supplier,
new kappa or foundational discharge.
