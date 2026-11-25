# Independent A review of streamed Lagrange repair

Status: **accepted algebraic and stated low-storage component**, retaining
its explicit physical qualification. It is optional, and is not a new
premise of the admitted P or V construction.

Reviewed root note SHA256
`3ad812fc74befa07eb286129e0aa221a22151d3d07a3d0805d8249ddbba4b33e`;
checker SHA256
`838ea6c9ac9a01c8786e9dc7357d6cdce87bcda6969e155335fea04de79bf6fa`.
Pins and spectral conventions are those of E002's root repair.

## 1. Coefficient and repair identities

Put ell=|J|<=s<q-1. Each L_j has degree at most ell-1<=s-1<q-2.
For 0<=i,r<s, r-i lies strictly between -(q-1) and q-1. Therefore
sum_(t in E*) t^(r-i) is zero unless r=i. When r=i it equals q-1,
which is one in characteristic two. Because t^(q-1)=1, SL1 extracts
[T^i]L_j with the stated minus-i exponent. A plus-i exponent instead
extracts a different character. The strict degree bound prevents a
T^(q-1) term from aliasing into the constant coefficient.

All displayed node denominators are nonzero. A product accumulator and
repeated membership tests evaluate L_j(t); no inverse matrix is stored.
Inversion and exponentiation cost polynomial(log q) bit work. The loop
count is polynomial(B+q), with constant field registers and logarithmic
control state. This does not make spectral membership tests free.

For the ell-by-ell Vandermonde V, interpolation gives
(V^-1)_(j,i)=[T^i]L_j. Check discrepancy is delta=H(P-zI)X, so
`e=V^-1 delta` has e_j=g_j X_j. SL2 is exactly
`y=V^-T diag(g_j^2) V^-1 delta`, padded by zero check coordinates.
Thus (H^T y)_j=g_j^3 X_j on J. Nonzero gaps in F4 have cube one;
zero gaps require zero correction. Outside J, p_j=z. This proves
PX+PZ+zZ=zX for arbitrary occupied E data. The transposed inverse is
in the correct position and no gap is inverted. Empty J is correct.

## 2. Physical qualification and isolated replay

Source comparison runs can compute one shifted count in m passes with
O(log m) bits per spatial location. Recompute this for each required shift
and coefficient. Its work is polynomial m, and a constant number of count
or coefficient streams has width comparable to a fixed field symbol.
Input/output roles still need actual aligned coordinate moves or serial
scans. No spectral conversion or mask-location obligation is removed.
At fixed m, q<=4B=O(m), so all SL1--SL2 loops are polynomial m.
Metadata and temporary streams are removed before paid children.

A much larger common root field must not be enumerated at every small
child. The note warns of exactly this issue. A separate explicit subfield
construction is recorded in `EMBEDDED-SUBFIELD-ENUMERATION.md`; it can
supply the smaller field when the root degree is a power of two. It is
an additional algorithmic lemma, not something assumed free in SL1.

I copied the inspected checker to `replay-lagrange/` and ran it in
isolation. It passed 2,384 coefficient cases, 4,449 basis repairs, 606
occupied extension-field vectors and 375 zero-gap containing sets. It
rejected 1,332 wrong-exponent cases and the degree-alias negative control.
These are exact finite identities only, not a physical tape simulation or
an asymptotic verification. The receipt is alongside the copied checker.

The accepted grouped-role matrix method remains sufficient for P and V.
This optional supplier offers a different storage/time tradeoff and does
not strengthen their global envelope by itself.

Credits: standard multiplicative character orthogonality and interpolation;
Jerry Chen (@CubeJerry), the E002 root repair, and AI-assisted independent
review. No formal or human verification is claimed.
