# Optional exact extension to Hilbert-valued radial functions

**Proved within the same135-Lagrangian permutation representation; separate from the main signed-cut review. No general group-potential impossibility is asserted.** This strengthens the excluded candidate class from nonnegative signed-cut combinations to any H-invariant Hilbert-valued orbit function with squared displacement. Squared displacement need not itself be subadditive, so this is only a calibration obstruction, not a construction of an admissible cost potential.

Let Omega be the135 Lagrangian three-spaces in the six-dimensional symplectic vector space over F2. Fix L0=span(e1,e2,e3) and its full stabilizer H. The four H orbits have distance d=3−dim(L intersect L0), with sizes1,14,56,64. Let w_r exchange e_i and f_i for i=1,...,r. An H-invariant function f:Omega→Hcal, where Hcal is any real or complex Hilbert space, is specified by four vectors v0,v1,v2,v3.

Define

    q_r(f)=(1/2) sum_L ||f(L)−f(w_r L)||².

For an indicator function of a radial cut, this is exactly half its symmetric difference, the main cut-table normalization. The independently enumerated orbit intersection matrices are

    N1 = [[0,1,0,0], [1,1,12,0], [0,12,12,32], [0,0,32,32]],
    N2 = [[0,0,1,0], [0,3,3,8], [1,3,28,24], [0,8,24,32]].

Entry N_r(d,e) counts L with distance d and w_r L with distance e. Both matrices are symmetric and have row sums1,14,56,64. Expanding q_r through these matrices yields the exact identity

    3q_1−2q_2
      = ||v0−3v1+2v2||² + 8||v1−3v2+2v3||².

Consequently q_2 <= (3/2)q_1. The bound is sharp: scalar orbit values(7,3,1,0) give q_1=96 and q_2=144. Thus no function with nonzero displacement can satisfy q_2>=2q_1. The obstruction includes arbitrary nonnegative sums of squared radial displacements by taking a Hilbert direct sum with square-root weights. The signed-cut cone has the stronger bound q_2<=q_1, as its complete table shows.

There is also a small geometric proof excluding equality q_2=2q_1 without using the complete intersection table. Let s1,s2 be the commuting individual coordinate swaps, so the prefix representative w2=s1s2. H invariance makes their individual squared displacements equal. Decomposing f into their joint ± eigenspaces gives

    q(s1s2)=2q(s1)−4||P_{--} f||²,

where the norm is the total Hilbert norm on functions on Omega. Equality forces (I−s1)(I−s2)f=0. Evaluate this equation at the following three isotropic spaces:

- span(e1,e2,e3), whose distance tuple under1,s1,s2,s1s2 is(0,1,1,2);
- span(e1,e2,f3), whose tuple is(1,2,2,3);
- span(e1+e2,e3,f1+f2), whose tuple is(1,2,2,1).

The resulting equations are v0−2v1+v2=0, v1−2v2+v3=0 and2(v1−v2)=0. Over the real or complex value Hilbert space they force all four vectors equal, hence zero displacement. This is independent of the finite rank calculation.

The exact enumeration and algebraic identity are checked in `enumerate.py` and `TABLE.json`. The statements concern functions on this particular Lagrangian representation that are invariant under the full ordinary parabolic. They do not exclude another representation, nonradial covariant state, marked-factor potential, a non-Hilbert construction, or a full native-query conservation theorem obtained by another method.

Derived by Worker C while independently reviewing Worker B's signed-cut attempt; credit the symplectic/parabolic source and programme predecessors, with OpenAI assistance. No new κ.
