# Actual frame contract and rank-one interface geometry

The exact #7481 word has gzip SHA256
`acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`.
The pinned retained constructor is `worker-a/selected/frozen/clifford_exact.py`,
SHA256 `2982ead07721e83358dc67c6f49c2b4c16a236a6bebdfd72f58221be1f5d0962`.
Authenticated #7481 verify_native.py calls inherited vendor/frozen/clifford_exact.py
on canonical_frame(a).adjoint().then(canonical_frame(b)), checking signed Pauli
action and absolute phase. Its retained independent native checker requires
strictly nested public upward MOVEs and strictly nested owned MOVEs in either
direction. Both primary files are copied under inputs/. Direct archive byte
crossbinding was not repeated: the nested #7334 archive is unavailable locally;
no archive was fetched. The algebra below concerns the explicitly pinned code.

## Algebraic geometry of the actual constructor

Over F2, let U be an n-by-r ordered independent basis and extend its columns
to G. For 0<r<n the constructor sets Q=I+G^{-T}G^{-1}, forms the monomial
K=diag(Q)perm(G), and returns F_U=K F_E K^{-1}, where E selects the first r
Fourier axes. The actual unsigned symplectic blocks give
B_U=G E G^T=UU^T and D_U=I+Q B_U. Also U^T(Q+I)U=I_r.

For Z input (0,z), the output is x=UU^Tz, z'=(I+QUU^T)z. Therefore
U^T(z'+x)=U^Tz+U^T(Q+I)U U^Tz=0. Both sides have dimension n, proving

\[
F_U Z_0=L(U)=\{(u,u+w):u\in U,\ w\in U^\perp\}.
\]

The empty/full constructor cases give the same identity directly. No
nondegeneracy of the restricted dot product on U is required. The partial
Fourier unsigned symplectic matrix is an involution, so each F_U is an
unsigned symplectic involution; signed phases need not square to identity.

For the physical interface M=F_V F_U^{-1}, B-rank is n minus the dimension
of Z0 intersect M Z0. Applying F_V^{-1} and using the involutions gives
n-dim(L(V) intersect L(U)). The intersection has independent parameters
u in U intersect V and w in (U+V)-perp. Hence

\[
\operatorname{rank} B(M)=\dim U+\dim V-2\dim(U\cap V).
\]

This is a proof for every ordered independent basis accepted by the pinned
constructor, not an extrapolation from finite tests. Rank1 forces nesting
and dimension difference1, including fresh noncatalog canonical frames.
For monomial L,R, B( L M R )=A_L B(M) D_R; invertible A_L,D_R preserve rank.
Consequently ordinary monomial adapters cannot turn a nonnested rank>=2
interface into a one-child LC1R factorization. Nonmonomial Fourier work
is not declared ordinary/free by this statement.

## Finite source audit

All1096 actual frames pass the L(U) identity and unsigned-involution checks.
Every actual interface to115 matches the formula. There are370 available
prefix frames before firstuse33814, with no earlier770 touch. Their actual
B-rank census is {0:1,1:6,3:4,4:37,5:75,6:191,7:56}. The available rank1 IDs
are554,555,556,557,822,823. The entire table adds only824,825. No nonnested
rank1 case exists. RESULT.json contains every exact record. Runtime1.06s.

Combined with the algebraic identity, wave34's31 lower and15 upper spaces
exhaust canonical rank1 imports. A new basis of a listed span adds no new
normalized history class; an unused span has no original history absent
another incoming job. Thus wave34's negative gate also excludes the broader
one-child canonical-frame import under unchanged-history/no-other-new-job
conditions, subject to binding the constructor provenance above. Wave34
itself remains frozen in its original declared scope.

## Same span does not imply literal physical equality

Rank0 means equal spans and gives an ordinary monomial adapter. The only
source alias1091/1092 has DIFFERENT signed tableaux. Its exact rank0 adapter
has nontrivial affine/quadratic terms and decomposition phase2. lower_child
verifies the adapter's tableau and absolute global phase. A basis-change
control at115 also has different operators with a nonidentity rank0 adapter.
The full recipes are in RESULT.json.

Negative history pooling by span is a safe overgrant of free normalization;
it does not require equal operators or equal phases. Positive physical
sources must emit and invoice the actual ordinary monomial adapter and
preserve phase. The native MOVE grammar requires strict nesting and positive
rank; a zero-rank alias is not automatically a legal native MOVE shortcut.

Replay:

```sh
python3 -I -B worker-a/cache-frame-contract/audit.py
```

Source inputs are unchanged. No physical supplier or kappa is claimed.
