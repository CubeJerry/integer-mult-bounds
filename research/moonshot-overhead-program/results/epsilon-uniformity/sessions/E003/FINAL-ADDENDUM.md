# E003 closing analytic refinements

This supplements the independently reviewed `FINAL-REPORT.md` without
changing its scientific snapshot. The complete multiplication envelope
and verification limits remain as stated there. All spanning-tree
formulas use local ell,t>=2; q=2 has the separate four-call free schedule
and its retained charged cost.

## Exact local tree optimization

`route-b/STATE-TREE-MOMENT-PROFILE.md` evaluates the tree's geometric
moment through ordered set partitions `F_ell=sum r! S(ell,r)`.
The exact weight is M=q kappa_ell-E, with E>=0,
kappa_ell=F_ell-1 for even ell and 2F_ell-1 for odd ell. For t>=8ell,
q kappa_ell/2<=M<=q kappa_ell, so

    log2 F_tree=t+ell log2 ell+O(ell).

An exact integer all-arity profile preserves the full charged-list
reserve at most 1/8 and label count N<=m^5. The eventual dimension
guard is still checked explicitly. Lead and A independently accepted
the complete moment and parameter proof.

The further theorem in `route-b/STATE-TREE-OPTIMAL-LOCAL-INVOICE.md`
optimizes the specified positive tree-plus-charged invoice. If u=log2 m,

    inf log2 J=2 sqrt(u[log2 u-log2 log2 u+O(1)]).

The lower argument uses the actual two-sided moment after showing that
every competitive invoice eventually has t>=8ell. The integer profile
matches it from above. Lead and C independently checked the proof.
This refines a local second logarithm; it neither improves the displayed
complete multiplication envelope nor lower-bounds other endpoint executors.

## Charged rank with a fixed number of gauge channels

`route-c/ONE-GAUGE-CHARGED-RANK.md` allows arbitrary signed or asymmetric
free weights and a changed charged matrix. For one fixed input/output
partial gauge per label, every F supported on individually monomial
routes leaves

    rank(I-F)>=ceil(N/2).

C assigns distinct scalar keys to the finitely many gauge subspaces.
The resulting diagonal A,B satisfy BF=FA and have B-A invertible, so
`B-A=B(I-F)-(I-F)A` has rank at most twice rank(I-F). A field extension
can supply enough distinct scalars without changing rank. An orthogonal
perfect matching attains equality for the native labels.

The lead supplied a finite-channel extension. If F is a sum of g such
channel matrices, commuting diagonal displacement operators give

    rank(I-F)>=ceil(N/2^g).

Their product kills every free-channel summand. At I its value is
invertible, while its expansion has at most 2^g left/right diagonal
multiples of I-F. The factor is sharp in an abstract orthonormal-label
model; native sharpness for g>1 is not claimed. Only under the retained
2D-per-charged-rectangle routine does this imply a charged-call invoice
at least 2Dm/2^g.

C and the lead checked the algebra. A fixed-channel representation is
a hypothesis, not a consequence of arbitrary route composition. State
walks and trees change gauges with their states and are not subject to
the g=1 conclusion. Residual transforms, multi-path synthesis and other
charged executors remain outside the claim. No runtime lower bound or
new full multiplier is asserted.


## Concurrent comparison at closing

The lead also read S004's complete FIFTH-WAVE-ADMISSION.md after
reconciliation. It records an alternative source-copying tree and an
independent-input destination-accumulation tree, with smaller finite
counts in some displayed cases. Those detailed new supplier proofs were
not all independently reaudited by E003 before closing. They are useful
parallel constructions, and reinforce that the exact E003 MST optimum
and its optimized invoice are restricted to the specified state-walk
representation. No optimum over every endpoint-sharing method is claimed.
S004's own admission keeps the same complete asymptotic envelope and
its actual routing, storage and precision contracts explicit.
