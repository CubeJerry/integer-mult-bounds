# Receiver54 isolation linearization and normalized relaxation

This package derives the necessary parent-isolation equations, solves their exact affine family, and certifies that the literal-readout family contains no admissible D. The sibling two-frame-column-gates package and independent review strengthen the obstruction to arbitrary common invertible readout rebasing.

For each donor j let M_j=[M9 M48] be the old parent off54 map on the two supported retained frames. Every individual block has a two dimensional kernel U_jr. For the six tight donors32,35,68,69,90,100 the joint kernel has dimension4 and is exactly the direct sum of these two block kernels. Thus isolation necessarily requires

im(S_old,jr S_new,jr^(-1) W_r) = U_jr.

The two sides have dimension2. Under section invertibility this is equivalent to

Ann(W_r) S_new,jr S_old,jr^(-1) U_jr = 0.

These are linear equations in D. With the fixed88 rectangle and phase zeros, the six tight donors give144 scalar equations of rank76 on833 variables. The affine dimension is757. Requiring each block to vanish separately at all eleven donors gives264 equations but the same rank76 and the same affine solution space. At donors whose joint kernel has dimension6 or8 this separate-block condition was initially a sufficient strengthening; the exact elimination proves it is already implied by the necessary tight-donor equations in this affine family.

Every solution forces global D column22 to vanish on all eight receiver9 output rows. The early four entries vanish by the physical phase zeros. FORCED-ZERO-COLUMN.json.gz supplies four exact linear combinations of the144 necessary equations proving the late four entries vanish. Donor0's input set contains column22, so its receiver9 section has a nonzero right kernel and cannot be invertible. The old section has rank8; its failure to satisfy the new isolation equations is a positive control. A corrupted elimination multiplier is rejected.

No conclusion is based on random samples. UNIVERSAL-KERNELS.json.gz is an earlier diagnostic for other retained sections. The four elimination combinations are the compact decisive certificate.

## Arbitrary readout normalization

For each r separately write A_r=Q_r^(-1) T'[O_r,:], allowing an arbitrary common invertible Q_r. Fixed native H images imply A_r[:,{4,5,7,8}]=T_old[O_r,{4,5,7,8}]. Dropping every phase constraint and every shared physical row constraint leaves248 entries per receiver. The necessary six-donor linear equations have rank48, hence dimension200, for each of r9 and48.

The normalized affine family has no fixed nonzero donor0 right kernel common to all its points. This does not establish determinant feasibility. Its section is still always singular by a varying column dependence: donor32 forces A_r[:,22] into im W_r, and this plane equals span(A_r[:,4],A_r[:,5]). Donor0 contains all three columns. The sibling column-gate package provides this stronger algebraic certificate and the H-only normalization witnesses. Arbitrary common Q_r therefore does not evade the receiver54 obstruction under the fixed H actions and retained frame spaces.

## Replay

```sh
python research/moonshot-005-program/results/bit-coupled-fifth-s033/other-receivers/target54-linear/solve.py --repo . --out /tmp/s033-linear54
python research/moonshot-005-program/results/bit-coupled-fifth-s033/other-receivers/target54-linear/normalized.py --repo . --out /tmp/s033-normalized54
```

SOURCE-PINS.json and NORMALIZED-SOURCE-PINS.json authenticate inputs. The output contains exact matrices, right hand sides, reduced forms, particular solutions and full nullspace parameterizations. No new kappa, whole fifth receiver, or compiler cost is claimed.

Authorship: @CubeJerry, with substantial OpenAI assistance. Apache-2.0.
