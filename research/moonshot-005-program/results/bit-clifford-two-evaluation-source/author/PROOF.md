# Two Clifford evaluations give compatible source quotas and a pure early phase

**Source-interface existence theorem, with exact native certificates. No
complete proper map, supplier or new kappa.** The construction below changes
the one-vector source class. It supplies a structured family in which all
foreign source views and the actual native early phase can be chosen
simultaneously. Shared H decoding, D/K compression and low return rank remain
separate requirements.

## 1. Finite field, native geometry and two fixed vectors

Use the authenticated 120-root quadratic space V over F2 and its explicit
sixteen-dimensional Clifford module S from the one-evaluation gate. All
native lines are nonsingular vectors j with q(j)=1. Each source plane H
through j is an anisotropic binary two-space: its three nonzero vectors
have q=1. There are 28 such H through each line. A foreign receiver i sees
exactly the sixteen H contained in i-perp. These statements concern the
actual frozen root table and source-plane labels.

Let F0=GF(16)=F2[t]/(t^4+t+1), with integer labels in the polynomial basis.
The following two vectors in S=F0^16 are used for every donor and every H:

    v=(9,6,7,2,10,6,15,1,6,14,5,5,5,10,13,13),
    w=(13,15,11,8,1,13,3,12,7,2,11,10,12,8,2,11).

Put E_H=C(H)v+C(H)w, where C(H) is the four-dimensional unital local
Clifford algebra. The certificate establishes:

1. Every E_H has dimension eight (all 1120 H).
2. For a fixed native donor, two distinct E_H spaces span dimension twelve,
   except for eleven listed donor/plane-pairs of dimension eleven. At any
   donor the graph of exceptional pairs has maximum degree one. All 41958
   donor/plane-pairs are checked. Thus any three distinct planes through
   a donor contain a pair spanning dimension twelve.
3. For every native foreign (i,j), the sixteen visible E_H span S. All
   6470 ordered foreign pairs have dimension sixteen.

These exact finite certificates imply the same ranks over every extension
of F0. The visibility statement has a separate review using actual H words
and binary field expansion, rather than the author's vectorized field
elimination. The proofs below use all three facts, not visibility alone.

## 2. Counting source planes inside binary subspaces

If a d-dimensional binary subspace L contains j and contains a source
plane through j, beta(j,-) is nonzero on L. Such planes correspond to
vectors k in L with q(k)=beta(j,k)=1, modulo k~k+j. Hence there are at most
2^(d-2) source planes in L. In particular dimensions at most five contain
at most eight planes.

For sharper bounds put G_L=sum_(x in L)(-1)^q(x). Translation by j, with
q(j)=1, changes the sign of this Gauss sum after multiplication by
(-1)^beta(j,x). Character expansion therefore gives the exact plane count

    n_j(L)=2^(d-3)-G_L/4.                         (1)

Let R be the polar radical of L. Expanding the square of the sum gives

    G_L^2=|L| sum_(z in R)(-1)^q(z).

On R, q is linear. The sum is zero if q|R is nonzero and is |R| otherwise.
Since V is nondegenerate of dimension eight, dim R<=8-d. Thus |G_L|<=16
for d=6 or7. Formula(1) gives at most twelve source planes in a six-space
and at most twenty in a hyperplane. If beta(j,-) vanishes on L there are
no source planes, so the same upper bounds hold. The checker additionally
enumerates all 2667 six-spaces and 127 hyperplanes through donor77 as
native controls. These finite counts support the general argument and
are not used to infer it.

For any collection of planes through j, let L be their binary span. Since
C(H)=span{I,gamma(j),gamma(k),gamma(j)gamma(k)}, their total algebra word
space is exactly gamma(L)+gamma(j)gamma(L). Consequently their total
evaluation space depends only on L. This equality is valid over F0 and
its extensions even though L and the source labels are binary.

## 3. Every sixteen-plane receiver view satisfies the source Hall test

Fix a foreign pair (i,j) and any subset A of its sixteen visible planes.
We claim dim(sum_(H in A)E_H)>=|A|. For nonempty |A|<=8, one E_H has
dimension eight. For 9<=|A|<=12, a nonexceptional plane pair gives dimension
twelve. For |A|>=13, the counting bound forces the binary span to have
dimension at least seven. It lies in the seven-space i-perp, so it equals
i-perp. Its evaluation space therefore equals the full sixteen-plane
evaluation space, which is S by the certificate. The empty case is trivial.

For X in End(S), let Q_H be the row space of the observation X|E_H.
Then Q_H is naturally S* tensor E_H, has dimension 128, and

    dim(sum_(H in A)Q_H)=16 dim(sum_(H in A)E_H)>=16|A|.       (2)

The independent-representatives lemma applied with sixteen slots per H
therefore allows a 16-row quotient F_(j,H) of X|E_H such that the stack
over any specified receiver view is invertible on the 256 original matrix
coordinates. Simultaneous selection for all receivers is handled below;
separate receiver-specific choices would not suffice.

## 4. The actual native early phase satisfies its own Hall test

The bank-480 atlas gives each donor 28 source planes. Their early/late
field quotas are (15,15), (30,0) or (45,0), and the early quotas sum to
480. Normalizing by 15 and then multiplying by eight gives a bank-256
interface with early quotas e_H in {8,16,24}. Write e_H=8(1+t_H);
t_H is 0,1 or2 and sum t_H=4. The late quotas are eight when e_H=8,
and zero otherwise. The checker reconstructs these facts from every
actual original-owner route, not from a new schedule.

At e_H=8, designate eight early and eight late rows for the 16-row source
quotient. At e_H=16, all quotient rows are early. At e_H=24, sixteen rows
are the quotient and eight additional early rows remain genuine original
owner values. These extra rows are explicitly retained, not set to zero
or removed from the later decoder contract.

We can choose all 256 early rows independently in their respective Q_H
spaces. For a plane subset A of size m the necessary grouped row count is

    sum_(H in A)e_H <= 8(m+4).                      (3)

For m<=8, dim sum Q_H>=16*8=128>=8(m+4). For 9<=m<=20, a nonexceptional
pair gives dim sum Q_H>=16*12=192>=8(m+4). If m>=21, the planes cannot
lie in any proper binary hyperplane, so their span is V. Their evaluation
space is consequently the same as that of all planes through j, namely S:
it already contains any one full native receiver view. Hence dim sum Q_H
is 256, at least the total of all early quotas. These inequalities also
imply every partial-slot inequality. The independent-representatives
lemma therefore supplies an invertible 256-row early source map.

The information and early conditions must be satisfied by the same rows.
Introduce independent coefficient variables for every selected row in
Q_H, including additional early rows. Every receiver-view determinant is
a nonzero polynomial by (2). The native early determinant is nonzero by
(3). Their product, over all 111 donors and all relevant receivers, is
nonzero in the common polynomial ring. A coefficient variable occurs in
at most 36 native receiver determinants, since at most 36 native receivers
are perpendicular to one H, and in at most one native early determinant.
Its individual degree is therefore at most 37.

Over any field with more than 37 elements, a nonzero polynomial with each
individual degree at most 37 cannot vanish everywhere. Use the field
F=GF(256) containing F0. For example one can construct it as
F0[s]/(s^2+s+t^3); t^3 has trace one to F2. Thus simultaneous source
quotients and invertible early maps exist over one fixed eight-bit field.
Lexicographic enumeration of the finite coefficient arrays, checking the
listed determinants exactly, is a terminating uniform selector. This
proof does not claim that the coefficient arrays have been computed or
that the selection algorithm has a practical complexity bound.

**Optional shared-plane specialization, source-only.** The same 16-row quotient F_H can be used
by every native donor lying in H. Indeed Q_H depends only on H, because
v,w and the original matrix coordinates are common to all donors. Identify
the quotient-row variables across those donors, keeping any extra early
rows donor-specific. Each individual receiver or early determinant stays
nonzero: within one determinant no distinct rows or distinct H variables
have been identified. Their product is therefore still nonzero. A quotient
coefficient occurs in at most 3*36 receiver determinants and three early
determinants, so its individual degree is at most 111. GF(256) still
suffices. This shared-plane property does not identify receiver-specific
inverse decoders or prove common H transport.
In fact, the programme's existing identical-plane-kernel odd-witness gate
excludes this specialization for the original canonical endpoint. The
main candidate retains donor-specific F_(j,H), with degree at most 37.
The optional specialization is not adopted as a downstream construction.

## 5. Genuine source words and an explicit finite invoice

For r independent matrix-module copies the bank is b=256r. The source
maps can be repeated on those copies; all copied field symbols are paid.
To use the literal bank-480 atlas, take r=15a, so b=3840a and replicate
that atlas 8a times. This is the smallest common bank at a=1. Native
quotient widths are 16r; all actual extra early owners remain present.

At native donor j, before its early departures, compute every required
late parity into a stationary initialized cache. Apply the selected
invertible early map to its actual original X owners. When the genuine
late Y owners later visit that native line, add the cached parities into
their designated values and charge dirty CLEAR for each cache. The early
inverse is applied to restored original X owners at Hub, as part of the
whole pure-early inverse if further stages are composed. Cache values are
never recovered by reading an X owner after its departure. Late cache
injections preserve arbitrary original Y baselines.

The literal atlas has 2675 donor-plane incidences of type (15,15), 422
of type (30,0) and 11 of type (45,0). Thus all donors together need
21400r late field caches and carry 88r extra early field values beyond
the 16-row quotient interface. There are no additional source MOVEs.

Expand F in its eight-bit basis. Put M=8b=2048r and let L_j be the
number of late binary cache records at donor j. Their sum is
L_total=8*21400r=171200r. An invertible binary M-by-M map and its inverse
cost at most 2(M^2+3M) ADDs. Direct computation of the L_j parities uses
at most M L_j ADDs, and injection into genuine Y uses L_j further ADDs.
Therefore the source contribution has the explicit bounds

    ADD <= 222(M^2+3M) + M L_total + L_total,
    INIT = charged dirty CLEAR = L_total,
    extra stationary ownership peak <= L_total,
    additional MOVE = 0.

These are finite upper bounds on the source module, not an invoice for
H/D/K/F transport or the return bank. A fixed finite coefficient search
is a separate setup constant; it has not been measured or optimized.
The physical compiler and erasure foundations are retained. Tensoring
with any positive whole-record body width gives the same identities and
operation counts in whole-record units.

## 6. What this resolves and what it does not

The one-vector evaluation gate is bypassed within a concrete, restricted
two-evaluation source family. The construction simultaneously provides
all native sixteen-plane source quotients and an invertible pure early
source phase on the actual source-port quotas, with paid genuine late
taps. Donor-specific quotients are retained; the optional degree-111
source specialization has a known canonical downstream obstruction.
The main theorem is more than a visibility test. It is still
an existence proof with a terminating selector, not an emitted global
coefficient file or a completed literal source/H/D/K/F word.

Nothing here proves that the source quotients have common H lifts, that
the induced D demands satisfy the shared-message intersections, that the
K contributions fit their causal channels, or that rank(I+B) is small.
Those conditions must be solved jointly inside this family or with a
further representation change. The irreducible target is compatible with
the field and bank arithmetic but is not thereby physically realized.
Strict BIT and complex suppliers, complete recursion and all five
foundational assumptions remain open.

The search log records a bounded discovery experiment. `check.py` verifies
the fixed finite witness, source geometry and exact rank conditions; the
Gauss-sum, Hall and determinant arguments establish the stated general
implications. Credit @CubeJerry, Worker C's Clifford geometry and
one-evaluation gate, native/atlas and source-compiler authors, and the
S027 orchestrator with substantial OpenAI assistance. No new kappa.
