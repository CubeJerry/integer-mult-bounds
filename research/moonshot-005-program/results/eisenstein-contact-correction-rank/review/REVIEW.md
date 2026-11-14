# Independent review of the correction-rank theorem

The integrator accepts the stated ranks with their separate scopes: every root section requires correction rank at least4V; the pinned canonical section requires at least6V; its correction is uniquely rank8V when restricted to the original eight-coordinate bilinear representation.

A separately written checker rebuilt the canonical coordinates from the pinned nine-coordinate roots, reconstructed all540 dual pencils, computed the six-root determinant with BigInt Bareiss elimination, and verified the homogeneous constraint rank using prime103 rather than the author's prime101. The exact S kernel gives the characteristic-zero upper bound on that constraint rank. The rank63 lower witness therefore proves a one-dimensional kernel over Q(sqrt(-3)) or C.

The universal4V argument is sound: a bad pair's four common complex-orthogonal neighbors are a second pencil, so another bad pair exists among them. The four cross correction blocks are forced zero in every section. The two remaining off-diagonal pairs are invertible scalar multiples of I_V, producing an invertible4V principal block. This does not enumerate all phase sections.

For the canonical six indices, the real Gram entries all vanish off diagonal, so every entry of the correction minor is forced, including its zero diagonal. det(C/4)=9 gives det(-theta C/12)=-1/3 exactly. Tensoring with I_V proves rank at least6V.

The ambient-coordinate theorem applies the scalar520-by64 constraint system to each matrix entry of the unknown V-block coefficients. Its kernel span(S) leaves a single matrix multiplier; one nonzero bad contact forces that multiplier to be -theta I_V/12. This is valid without symmetry, invertibility or commutativity assumptions on the unknown blocks. It is not a theorem about unrestricted correction spaces or every phase section.

Controls check that S+I violates diagonal constraints and a zeroed minor row destroys the determinant. The author's complete checker and three mutations were also reproduced exactly; that is separate from the independent method.

The rescaled-base H/2 plus conjugate(H)/2 construction is a necessary scope control: rank4 added correction is possible when its diagonal and base normalization change, and it recovers the rank8 real Gram operator. No MOVE count, ownership price, complete source or new kappa follows.
