# Stable-history gate for a recoverable encoder

This is a derived linear-interface proposition, not a claim of source
feasibility. Let F0 be a complete baseline receiver-history matrix and B
its control-response matrix. Let K span the neutral control kernel, including
all required guards. Assume every zero-baseline history relation annihilates
every neutral control: dF0=0 implies dBK=0. This is the only history
annihilation premise needed; an all-control dB=0 theorem is stronger.

A
row d_s is a stable history decoder if d_s B K=0. Examples are actual
pre-control input observations and final receiver-chart endpoint values
required to be restored. A final endpoint outside the receiver's history
is not such an example without a separate access/response proof.

Let S be the span of baseline rows d_s F0 of certified stable decoders.
Let D=row(E) intersect row(W_T) intersect row(F0) be the locally encodable,
terminal-recoverable and receiver-visible common modes. If D is contained
in S, no recoverable-encoder channel exists for this fixed interface.

Proof. A feasible encoder decoder d would satisfy r=dF0 in D and dBc=1
for a neutral c. Since r belongs to S, choose a stable decoder d_s with
d_s F0=r. Then (d-d_s)F0=0, hence (d-d_s)BK=0 by the history-annihilation
premise. Since c belongs to the image of K, dBc=d_s Bc=0, contradiction. The argument applies
coordinatewise for all admitted field volumes. Arbitrary coordinate-linear
controls do not change the zero adjoints used by the premise.

More precisely the response of any decoder to neutral controls depends only
on its baseline row r. This defines a linear map G:D -> dual(ker A),
G(r)(c)=dBc, independent of the representation dF0=r. The recoverable-encoder
criterion is nonzero precisely when G is nonzero. Since D intersect S lies
in ker G, rank(G) <= dim(D)-dim(D intersect S). Thus a positive quotient
dimension is necessary; it is not sufficient, and does not price a channel.

The first source test should authenticate D and S, including literal
history representations and endpoint stability, before building the larger
neutral-control matrix. Correlated external side information, changed
observation access, or common-dependent interventions beyond the stated
single encoder require a new interface. No new kappa.
