# The correction is a full-rank operator, despite eight broadcast coordinates

For the actual 104 source rows, the independent checker establishes the exact
identity A^T A=104I. Hence G=AA^T has G^2=104G. On im(A), G acts by 104; on
ker(A^T), it acts by 0. These spaces have dimensions 8 and 96 and form a direct
sum. The off-diagonal correction operator C=G/8-I therefore has eigenvalues
12 and -1 respectively, so rank(C)=104 and C^-1=G/96-I. The finite exact
checker also multiplies the displayed inverse literally.

This prevents treating all correction aggregates as an eight-dimensional
family merely because the broadcast Gram matrix has rank 8. It is not a
104-call lower bound in the presence of local side information. The inverse
has a factor 3 in its denominator and is not proposed as a dyadic physical
implementation; the original conditional decoder remains dyadic.

A second independently checked source property is that each receiver's 55
odd other-port vectors span the full seven-dimensional hyperplane a_i-perp.
If its known data consist only of individual even coordinates, removing
any one of its 48 even coordinates adds a nonorthogonal root to the unknown
set, making that set span all eight packet dimensions, including a_i.
Therefore that receiver can no longer decode from the fixed eight packets.
An explicit ambiguity is recorded in MINIMAL-COORDINATES.json.

This coordinate-set minimality does not require 48 physical packets: the
correct single aggregate can substitute for them, and supplying odd
coordinates changes the premise. No new kappa is established.
