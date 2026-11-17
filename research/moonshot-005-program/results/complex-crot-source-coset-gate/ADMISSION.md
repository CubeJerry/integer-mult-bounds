# A source-coset frame excludes rotation interfaces even with a matrix prefix

**Proved scoped exclusion for arbitrary ordinary Q and actual independent
endpoint units/inverses.** Retain Crot=[[T,0,-N],[0,I,0],[N,0,T]], N=I-T,
with nonzero ordinary idempotent T and ordinary backward transports
a^-1 T a,a^-2 T a^2. Ordinary coefficients have a fixed finite collective
tail catalogue; arbitrary matrices on a fixed finite prefix are allowed.
Faithful separation of that finite tail catalogue is retained. No augmentation,
half-rank or involution-sign premise is used.

Ordinary-class cancellation in L Crot U Q L forces q21=q22=0. Invertibility
makes q20 a unit. The complete coefficient of the Gaussian-one left coset
represented by a in input column zero is

    K=(0,-N q20+T H,T q20+N H)^T,
    H=ordinary_part(a q01 a^-1).

The ordinary row(0,-q20^-1 N,q20^-1 T) retracts K to the identity. Actual
endpoint factorization therefore makes im(K) the entire Gaussian-one encoder
image. The last Gaussian-one column(0,T a p,N a p), p=q02, is transverse to
that image and must vanish, giving p=0. Gaussian-three cancellation then gives
T2 z=0. Q's last column is(0,z,0), incompatible with invertibility and T2 nonzero.

Left-coset separation, not merely source count, excludes the omitted terms.
There are genuine Gaussian-one return words with more source occurrences;
they lie in different left cosets. A fixed matrix prefix does not change this
tail distinction. This proof survives the distinguished-column plus unit,
but does not cover Klein or C_T first interfaces.

[Author proof](../../sessions/2026-11-17-S020/checkpoint4-evidence/B/crot-source-coset-gate/PROOF.md) and root's
[independent derivation](../../sessions/2026-11-17-S020/checkpoint4-evidence/R/crot-coset-review/REVIEW.md)
check every block term, encoder inference, transversality and rank contradiction.
Separate exact sparse arithmetic verifies both signed rotations, source products,
Gaussian support/modulus, noncommuting q and H controls, and sharp return-coset
examples. The universal theorem rests on the written argument and retained
tail separation, not a finite search.
Credit @CubeJerry, source/tensor-separation and rotation predecessors, B and
root; substantial OpenAI assistance. No new complete κ. The selected conditional bound remains .00363005817. Both strict suppliers, the outer assembly and all five foundations remain open. This is ongoing research and is not PR-ready.
