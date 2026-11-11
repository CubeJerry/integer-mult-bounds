# Selector lifting: an exact invariant and a repair obstruction

**No new kappa.** This appendix proves the passive-mode identity for a proposed
shared-core lift and a source-specific failure of two restricted repair methods.
It does not construct H4, rule out other sharing constructions, or prove an
architecture-independent bound. Source pins and the favorable complete profile
are in SOURCES.json and REVIEW.md.

## The selector invariant

Work over Q with complete fields of equal volume and exact scalar operations.
Consider a finite word with main fields x and core fields u (arbitrary public
helpers and owned fields initialized to zero). Its admitted normalized endpoint
is (E x, h): public helper inputs h return unchanged, and owned fields clear.
Let M0 be the main-only scalar word obtained by retaining all main-to-main ADDs
and main SCALEs, deleting core couplings, and ignoring normalized-identity MOVEs.
Assume there are no main COPY, INIT, or CLEAR operations; the selected source
satisfies these syntactic conditions.

Make k independent main banks x_c with identical chart schedules, sharing the
core once. Choose a column v and row w with w v=1. Replace a core-from-main
contact q x by q sum_c w_c x_c; replace a main-from-core contact q u by updates
q v_c u to the corresponding main in every bank. Duplicate main-only operations
and main MOVE jobs; retain core-only operations, owned lifetimes and core MOVEs
once. All actual scalar services and movements must still be paid.

Set z=sum_c w_c x_c and d_c=x_c-v_c z. An induction on each source event proves:
(z,u) follows the original word, while every d_c follows its main-only word.
For a core-from-main event the core sees exactly z. For a main-from-core event,
z changes by q u because w v=1, while every d_c is unchanged. Main-only linear
events act identically on z and each d_c; core-only events do not affect d_c.
Duplicated identical chart movements commute with these constant combinations.
Thus, at every prefix, the invariant holds, including the owned zero/clear
conditions inherited through the z execution. At return,

x'_c = v_c E z + M0(x_c-v_c z).

The division-free selector v=(1,...,1), w=(1,0,...,0) works over every field;
it gives x'_1=E x_1 and x'_c=E x_1+M0(x_c-x_1). This is the simplest proposed
source-level lift, not a proof that the desired independent outputs are correct.

For k>=2 the entire lift equals independent copies of E on all inputs exactly
when M0=E. Indeed P=v w is a rank-one projection, and its complementary bank
subspace has positive dimension. The full endpoint is

F = P tensor E + (I-P) tensor M0.

On the complementary subspace F acts by M0, whereas the desired endpoint acts
by E. The shared public helpers nevertheless return correctly because the
active z execution is the original admitted word.

## A literal-chart postrepair cannot fix this source

The selected E is invertible: its shears and eight coupled two-field blocks
all have determinant one. The selected M0 is invertible because all retained
SCALE coefficients are nonzero and every ADD is elementary. Consequently a
linear postrepair of the main outputs is uniquely

R = (I tensor E) F^-1
  = P tensor I + (I-P) tensor C, where C=E M0^-1.

The independent checker selector_witness.py applies inverse operations in
reverse chronological order to e_129. It then applies the selected E row17,
which is e_17-e_129. The inverse column has entries zero at17 and three at129,
so C[17,129]=-3 exactly. Forward replay of M0 returns e_129, independently
checking the computed inverse column. A wrong inverse-order control fails.
This method differs from the author's chronological right-inverse row method.

Field17 has final chart127 of rank9, while field129 has final chart143 of rank8.
For any k>=2 and any selector with w v=1, the corresponding cross-chart block
of R is -3(I-P), which is nonzero. Products of scalar ADD/SCALE operations
confined to each literal final-chart class remain block diagonal by that chart
partition, even if they mix different banks within a class. They cannot realize
R. This excludes only that postrepair class; moving fields, changing charts,
different source words, nonlinear/packed representations and other architectures
are not excluded. No full defect rank is needed or claimed by this check.

## One-way FULL-hub repairs require at least 119 rank-one jobs

This applied obstruction has a deliberately explicit grammar. Consider the
two-bank selector lift after its core has returned. The returned main fields
are arbitrary independent state coordinates because F is invertible; there
is no prepared side information about these coordinates in other fields.
Partition the returned rank8 fields by their original literal final chart,
allowing both banks to mix freely within each class.

Before evaluating FULL-chart outputs, a class may form scalar combinations
only of its own returned fields and export complete fields to FULL. Each
export is one paid rank-one conversion and has the same field volume. Arbitrary
scalar processing in FULL is granted for free. There is no cross-class
preprocessing, feedback, partial-field packing, additional informative input,
or new helper target credit. All non-FULL output completion and return costs
may be granted free *after* FULL evaluation; they cannot feed information
back into that evaluation. These are restrictions of the investigated repair
grammar, not asserted facts about every operation permitted by the whole model.

Let C_FULL,S be the matrix of C with FULL output rows and source columns in
one original rank8 chart class S. The two-bank postrepair block on this cut is
(I-P) tensor C_FULL,S, since the identity term has no FULL-to-rank8 entries.
Over Q its rank is rank(C_FULL,S), because rank(I-P)=1 for two banks.
For field volume V the required dependence has rank rank(C_FULL,S)*V.
Each exported complete field carries at most V independent scalar dimensions,
so the class needs at least rank(C_FULL,S) exports. Different original classes
have disjoint export counts in this grammar; the lower bounds add.

The pinned source has 200 FULL main fields and 200 rank8 main fields, grouped
into 104 literal rank8 charts. Each group has one or two source fields.
The independent hub_witness.py computes all 200 columns of M0^-1 modulo
p=1000000007 by reverse inverse-word execution and checks every column by
forward M0 composition. It applies the selected E to obtain the needed C rows.
It then uses explicit 1x1 and 2x2 minors, with witnesses in HUB-RESULT.json,
rather than the author's row propagation and Gaussian rank calculation.

Primality of p is checked by trial division through floor(sqrt(p))=31622.
All source rational denominators and all main SCALE numerators are units
modulo p; the encountered scalar denominators are 1,2,4,8,16,32. Thus the
matrix reduction is defined, and every nonzero minor modulo p proves a
nonzero rational minor. The rational ranks are at least the modular ranks.

The complete 104-group census gives 16 groups of modular rank2, 87 of rank1,
and one of rank0, for a total lower bound119. The 104 source subspaces are
also independently distinct, each containing 256 vectors. This distinction
alone is not an audit of equivalence under all free ordinary adapters.

Even granting the favorable H4 complete signed moment from REVIEW.md, adding
119 rank-one jobs to each of 18 native calls changes that moment by at most
-18*119=-2142, since 1^(199/200)=1. The exact resulting interval is

[-370816614896575152,-370816614896395384]/10^15 < 0.

This one-way repair therefore cannot meet the kappa=.005 raw-moment gate
with the stated complete target profile and no new helper credits, even
before charging ordinary repair work or non-FULL completion.

## Abstract extension: a communication cut with explicit premises

A broader lemma is valid for a fixed network of chart-equivalence classes
and a fixed finite word of linear operations over a field. Its control
schedule is independent of the input values. Assume: (1) all arrays have equal volume V; (2) initial arrays in a source
class S are independent of all initial data outside S; (3) every operation
that communicates S-dependent information across a class boundary is an
explicit charged full-field transfer carrying at most V dimensions; and
(4) local operations, feedback, relays and newly introduced classes do not
introduce free cross-class transfers or prepared side information.

Fix all other initial inputs. By induction on the transcript, every outside
state depends on the initial S arrays only through messages that have left S.
Incoming feedback is itself determined by earlier outgoing messages and fixed
outside inputs, so it does not increase their total independent information.
For a required linear outside output map of rank q_S*V, at least q_S transfers
must leave S. Summing over source classes counts each departure only once,
according to its origin class. If every such transfer has paid tariff at least
one and creates no additional target credit, the same rank-sum budget bound
holds despite feedback, relays, interleaving and new charts.

This is an abstract sufficient communication model. Applying its 119 numerical
conclusion to the full retained ABI additionally requires proving that its
classes are closed under every allowed free adapter, copy and reencoding.
The present package checks literal charts and distinct subspaces; it does
not discharge that stronger equivalence/operation obligation. The applied
source-specific theorem above remains the explicitly one-way grammar.

## Credit and verification scope

The selector construction and source row/minor obstruction were proposed by
the construction agent in this run; a separate review agent derived the
projector/postrepair identity and checked inverse columns and small minors.
Both are OpenAI-assisted work prepared for @CubeJerry. Existing source
contributors retain the attribution listed in REVIEW.md. None of this is
human review, formal-kernel acceptance, a completed supplier, or a new kappa.
