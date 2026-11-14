# Wave2 recovery checkpoint: OLD23 to a typed owned zero HOME

Status: **unverified implementation in progress**, 2026-11-14.
Base: `e54523517d0f03e58352e647c403a5af3e525a57`. No new kappa.

Produce the six-Gamma typed zero directly from one valid old coded field and
its immutable23-code context, without a preexisting Gamma6 donor. Reuse the
exact frozen codec Builder from the concurrent selected-move-packed-codec
package (`machine.py` SHA256
`119b69594a2a33550eec9b6e083db8f496c3fb3d9c1214b6703d687a0a662eba`).

Read the entire old context, infer b from its first complete component,
recover r by exact record-size division, check complete row geometry and
every later component/old frontier, and emit
`^ Gamma(f,r,P,S,b,cutoff) 0^V | $` on a distinct inactive owned HOME.
Here `P=outer*rows*2^u`, `S=2^(a-u-9f)`, `V=outer*rows*2^a*2rb`.
The output may be newly allocated from a blank window or overwrite an
already allocated inactive body of exactly the inferred F bits. It must
never overwrite the old-format source in place or receive productive credit.

Zero has the same value under every complete coordinate permutation and
linear frame. Therefore no9f data transport is needed. Target the complete
uniform bound O(V_old+E_old), paying context, source validation, unary
guides, output/header allocation, zeroing, markers, all head returns and
private retirement. Export full-capacity CLEAR for the produced owned bank.

The fixed OLD23 source geometry and source field access are supplied; a
full root producer, source dispatcher, owner grant and chronological caller
remain external. Exact B1 marker/head binding and extent checks are required;
an old-format HOME cannot be silently relabelled as a shorter packed HOME.
Keep wave1 selected-owned-gamma-init frozen.
