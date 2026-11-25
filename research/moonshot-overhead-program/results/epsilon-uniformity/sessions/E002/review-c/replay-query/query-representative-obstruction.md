# Why an auxiliary-only middle map does not align distinct Fourier labels

Status: **proved scoped algebraic obstruction; independent review requested**.
This tests a concrete attempt to remove the numerical pencil's per-query
address permutations. It does not lower-bound their actual tape time,
their number after a new sharing construction, or a multiplication bound.

Source: OpenAI math 3344da59991ed94f9ba711217b29c1d760badfa6,
Fourier kernel.tex, “The endpoint Fourier transforms,” specialized to
ell=2. The scalar numerical data are rational; the coordinate geometry
is the source's nondegenerate bilinear space over F2.

## 1. The proposed simplification and its exact contract

In a free rectangle I x J, put
\[
 H=\operatorname{span}\{d_w:w\in J\}.
\]
For every source v in I, \(H\subseteq d_v^\perp\). The shared first
endpoint transform is along H in each half of the address and hence
uses auxiliary axes only. Its remaining spatial coordinates are
cosets of H. The source subsequently changes those coset representatives
to one common layout, applies the small row maps, and accumulates.

A possible improvement would replace every such middle representative
permutation by phases and permutations of auxiliary coordinates alone,
keeping the physical distinguished query slot unchanged. That would
let the endpoint preparations absorb all expensive coordinate movement
independently of the query j.

The theorem below rules out this exact replacement whenever the
rectangle contains two distinct source directions. It does not exclude
one larger shared transform, a different kernel, simultaneous query
routing, or a coordinate change that also touches the query slots.

## 2. The distinguished coordinate is an intrinsic functional

Let D be a finite-dimensional nondegenerate bilinear space over a field,
let \(d_v\) have \(\langle d_v,d_v\rangle=1\), and let
\(H\subseteq d_v^\perp\) for all v in I. In the physical endpoint basis,
an input column has the unique form
\[
 x=t_v d_v+b_v,\qquad b_v\in d_v^\perp.
\]
Thus
\[
 t_v=\langle d_v,x\rangle.
                                                               \tag{QR1}
\]
Because d_v is orthogonal to H, QR1 defines a well-defined linear
functional \(\ell_v\) on D/H. Transforming along H does not alter this
coset label. Phases do not move a record to a different coset.

**Lemma QR1.** Suppose a common post-endpoint coset layout has one
distinguished coordinate tau, and every source's conversion into it
keeps that source's physical query-slot value unchanged. Then every
source direction d_v is equal.

**Proof.** The contract says
\(\tau(x+H)=\ell_v(x+H)=\langle d_v,x\rangle\) for every x and every
source v. Thus for v,v' in I,
\[
 \langle d_v-d_{v'},x\rangle=0\quad\text{for every }x\in D.
\]
Nondegeneracy gives \(d_v=d_{v'}\). This argument does not need tau
to be chosen in advance, nor does it assume a particular auxiliary
basis. It is valid even if the permitted auxiliary permutations are
not linear. Their inability to change the distinguished coordinate
is the only property used. ∎

The weaker condition \(d_v-d_{v'}\in H\) does not suffice.
It identifies their vector classes in D/H, but their pairing
functionals on D/H can still differ. Confusing those two statements
would miss the surviving query-slot shear.

## 3. The source label directions are distinct

For binary Fourier routing the labels are \([q]^L\), with Gram matrix
\[
 \Gamma(v,w)=1-\Delta(v,w)\pmod2,
\]
where Delta is Hamming distance. The d_v are the generator images in
the quotient by the radical of this Gram form.

**Lemma QR2.** For q>=3, distinct labels give distinct d_v in the
actual quotient, for every positive L.

**Proof.** Choose a coordinate i with v_i!=v'_i. At every differing
coordinate choose a probe letter different from both labels, possible
because q>=3. At equal coordinates choose either common letter.
Call the resulting probe z. Both labels have the same parity of
distance to z. Change only z_i to v_i, giving z'. The distance from v
decreases by one while the distance from v' does not change. Hence
\[
 \Gamma(v,z')-\Gamma(v',z')=1.
                                                               \tag{QR2}
\]
Their Gram rows differ, so their generator images cannot coincide
in the radical quotient. ∎

This condition applies to the numerical construction's q=2^t>=4.
For q=2 it is false in general: the Gram row depends only on the
parity of the binary word. That excluded case is a useful falsifier.

## 4. A canonical rectangle already witnesses the failure

For any q=2^t>=4 and L>=2, fix every coordinate after the first to zero.
Use the first-differing-bit rectangle
\[
 I=\{(0,0,\ldots,0),(1,0,\ldots,0)\},\qquad
 J=\{(2,0,\ldots,0),(3,0,\ldots,0)\}.                \tag{QR3}
\]
For t>2 use the common leading zero prefix. Every cross pair has
distance one, so Gamma vanishes there: this is an actual canonical
free rectangle of the source. Its two source directions are distinct
by QR2. Lemma QR1 therefore forbids the proposed auxiliary-only
common-layout conversion for this rectangle.

More concretely, set x to the first source direction. Its physical
query coordinate is one at that source and zero at the other, since
the two source labels also have distance one. Both values are
well-defined on x+H, because the cross pairings with J vanish.
No common distinguished coset coordinate can equal both values while
leaving each source's query slot unchanged.

## 5. What this says about the numerical invoice

The new variable-arity bound pays polynomial-m ordinary work for the
middle monomial maps, including their packed-XOR/interchange routing.
To lower that coefficient, it is tempting to move all their physical
cost into the once-per-incidence endpoint transforms. QR1--QR3 show
that phases and auxiliary-only reindexing cannot accomplish this in
the retained canonical common-layout schedule.

This is not proof that polynomially many costly maps are necessary.
Several query-dependent maps might share physical passes; their scalar
coefficients might admit a new representation; a different rectangle
family or a different completed kernel could alter the requirement.
Even an unavoidable nontrivial permutation has no quantitative tape
lower bound in this argument.

The useful next gate is therefore explicit: supply a batched executor
for the actual query-slot-dependent coset maps, or replace the common
layout architecture. Merely selecting different complements and calling
the remaining changes “phases” does not remove them.

Credits: @CubeJerry; the pinned Fourier endpoint factorization;
substantial ChatGPT multi-agent assistance. No physical lower bound,
full execution, or formal certificate is claimed.

## 6. A volume count in the literal separated-query executor

The obstruction is present on a positive normalized volume, not just
one isolated source pair. Fix one of the L word positions. Partition
its q letters into consecutive blocks
\(\{4b,4b+1,4b+2,4b+3\}\). For each fixed choice of the other
L-1 letters, retain both canonical rectangles
\[
 \{4b,4b+1\}\times\{4b+2,4b+3\},
 \quad
 \{4b+2,4b+3\}\times\{4b,4b+1\}.
                                                               \tag{QR4}
\]
These are first-differing-bit parts at the penultimate bit with the
higher prefix fixed. They lie at distance one and have nonzero
source rectangle weight \(-p(1)\), since every factor
\(1-1/(2r)\) defining p(1) is nonzero.

There are exactly \(N/2\) such rectangles, each with two source labels,
and their source sides partition all N labels. At each rectangle and
each query, at least one of its two source conversions must alter the
distinguished query coordinate, by QR1. If one source-label stream has
volume V/N, the sum of volumes of these nontrivial conversions is at
least V/2 per query, and at least mV/2 per pencil stage.

The rational Newton predictor has D_pred=Theta(sqrt m) stages. Its
coefficient of every query is nonzero at every stage:
\(\pm1/(2h)\) in Newton step h. Thus the source executor that carries
out each rectangle/query middle conversion separately exposes total
nontrivial representative-conversion volume
\[
 \Omega(m^{3/2}V)                                   \tag{QR5}
\]
already in one predictor evaluation. Finite repair contains that
evaluation at its root and cannot erase this count by a smaller
normalized leaf contribution.

QR5 counts applications of a specified family of nontrivial coordinate
maps. If the chosen compiler bills at least one full-volume f-field
primitive for every such map, it also lower-bounds that compiler's
primitive-volume invoice. It does not prove that each map costs
\(\sqrt f\), that two maps cannot share one pass, or that all algorithms
must explicitly evaluate these rectangle terms. Narrow f may instead
use direct bit operations. A new batched map executor lies outside
the separated-query counting contract and is exactly the remaining
opportunity.

This shows why merely improving Gaussian elimination of each individual
matrix cannot close the normalized \(\sqrt m\)-scale address-invoice
gate in numerical-address-invoice-gate.md. The retained separated-query
schedule already has \(m^{3/2}\) map volume before its D-dimensional
matrix factorization is priced.
