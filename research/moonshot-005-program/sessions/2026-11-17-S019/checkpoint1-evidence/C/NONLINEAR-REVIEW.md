# Independent review of the Petersen nonlinear transcript gate

**Accept the exact nonlinear nine-descent lower bound in its fixed-prefix,
fixed-schedule, finite-whole-record-alphabet scope.** This strengthens the
linear block-star proof in `REVIEW.md`. No new multiplication exponent or
physical nine-descent decoder is established.

Reviewed root input: `PETERSEN-SHORT-DUAL.json`, SHA256
`7c0e1e96f41d44a3c989906ad9c08eaa96252799a33a065746048a078e23527d`.
The independent script `review_nonlinear.py` does not import the root verifier.
It expands each of the 21 terms under all 120 permutations directly in the
1024 original subset coordinates. The resulting 2520 elementary inequalities
telescope exactly, with rational arithmetic, to minus the empty-set variable
bounded above by minus5. No LP solution tolerance or canonical-orbit lookup
is used by this independent check.

Prepared for @CubeJerry, with credit to root's exact entropy certificate,
Worker A's native star discovery, the retained initial-chart transcript
framework, source authors and the classical Petersen index-coding result.
Substantial OpenAI assistance. This is an agent mathematical review rather
than independent human or formal-kernel acceptance.

## 1. Meaning of every elementary inequality

Let ten independent uniform inputs X_0,...,X_9 take values in a common finite
alphabet A of size at least2. Write h=log|A|. Let T be an arbitrary deterministic
zero-error broadcast permitting every Petersen receiver to recover its own
input from T and its neighbors' raw inputs. No linearity is assumed.

For every subset S of the ten roles, define

f(S)=H(T,X_S)/h.

The certificate uses only the following universally valid inequalities:

- Initialization: -f(all ten)<=-10, from independent uniform inputs.
- Unit slope: f(S+i)-f(S)<=1, because H(X_i)<=h.
- Monotonicity: f(S)-f(S+i)<=0.
- Decoding: f(S+i)-f(S)<=0 when S contains every neighbor of i, since X_i is
  a deterministic function of T and those neighbors. Monotonicity supplies
  the reverse inequality, so the increment is exactly zero.
- Submodularity: f(S)+f(S+i+j)-f(S+i)-f(S+j)<=0 for distinct i,j outside S.

Petersen vertices are the ten two-element subsets of five labels; two vertices
are adjacent exactly when their pairs are disjoint. Every permutation of the
five labels preserves this graph. Applying the corresponding inequality after
every such permutation and averaging is legitimate for an arbitrary code;
the code need not itself be symmetric.

The independent expansion verifies every graph automorphism, every decoder
neighbor premise and every positive rational multiplier. Summing all expanded
inequalities yields

-H(T)/h <= -5.

Therefore every such Petersen code has H(T)>=5h. The statement includes
arbitrary nonlinear encoders and decoders. It is an entropy theorem for all
finite alphabet sizes, rather than an enumeration of possible encodings.

## 2. Four isolated demands add four symbols

The actual14-role source graph is Petersen on
{31,32,55,56,57,58,96,97,109,110}, together with the four isolated vertices
I={5,35,90,93}. Its exact pair labels and every actual neighbor set are recorded
in `audit/NONLINEAR-REVIEW-RESULT.json`.

Each isolated input is recoverable from T alone; jointly H(X_I|T)=0. Thus

H(T)=H(X_I)+H(T|X_I)=4h+H(T|X_I).

Conditional on any value of X_I, the ten Petersen inputs remain independent
and uniform. The same transcript is a valid Petersen code, with that fixed
isolate value granted if desired. Section1 therefore gives
H(T|X_I)>=5h. Consequently H(T)>=9h.

The conditional argument does not assume additivity of an unspecified graph
parameter. It proves the required additivity directly for isolated demands.

## 3. The graph is the actual physical source cut

The independent native interpreter replays the complete local-canonical9 word
on all222 symbolic original columns and validates its movement directions,
co-chart ADDs, final restoration and owned lifetimes. Its word SHA256 is
`3643c6db33ce5ed1ea61724b126a8a3cad28be0c728376193b1f11fbf0457565`;
its source cut is before operation783.

Set all inputs outside the14 witness roles, including every original Y input,
to fixed constants. For each witness receiver i, collect the supports on the
14 inputs of **every actual live cut field** whose real chart lies below F_i.
The result is exactly the indicated graph, including empty side information
for the four isolated roles. This includes the original records, completed
Y records, native caches, known ground fields and all nine canonical code
fields. It does not merely inspect native root pairs or assume the code is
unavailable. The M1 field locations are included explicitly.

Now replace each future downward whole-record output by its value in a common
transcript T and grant that whole transcript to every receiver. Every other
operation moves information only to a containing chart or processes it at its
present chart. By induction along the fixed chronology, a final receiver can
be simulated from T and the initial fields below its final facet. Each such
initial field is a function only of the raw side coordinates just enumerated.
Granting those raw coordinates permits the claimed Petersen+isolates decoder.
This is a deliberately stronger access model than physical receiver chains.

If k downward transfers occur and each carries one value in A, then
H(T)<=kh, even with feedback, dependencies between transcript entries or
nonlinear operations. The lower bound9h gives k>=9.

## 4. Required scope and excluded side channels

The asserted result uses a fixed input-independent schedule and finite common
whole-record alphabet. Any choice of charts, operation locations, record
names, message boundaries or variable-length schedule that depends on data
would itself need to be included and charged as information. The present
argument does not grant such a side channel free of cost.

Arbitrary nonlinear same-chart processing, copying and erasure may be granted;
all possible downward payloads are already included in T. Ascending original
carriers and chronological feedback are allowed. All input-dependent initial
source values have been counted through their actual chart locations.

The statement is cleanest for deterministic zero-error continuations. A
randomized zero-error version can be obtained under input-independent coins
and a worst-case bound on the number and size of messages: condition on a
valid random tape (or on public randomness). For finite inputs, a measure-one
set of tapes is correct on every input, so a fixed-tape argument applies.
This is **not** a statement about bounded-error protocols, expected message
cost, data-dependent schedules, infinite alphabets with unbounded information
per record, or uncharged enlarged auxiliary alphabets.

## 5. Movement implication and publication treatment

The frozen local9 source has moment
Q=1613.25738301456890700441222598059... . Its remaining original ascents are
direct necessary closures. Every additional strict descent costs at least1,
and concavity ensures that refining an already charged direct original ascent
cannot refund its movement charge. Hence Q+9 exceeds the necessary target
allowance by the strictly positive interval in `audit/RESULT.json`:

[0.506502803416551758166075613595474795,
 0.506502803416551758166075613595475241834].

The source acquisition remains valid. The stronger bound closes only the
specified appended-continuation route; it is a later S019 result and should
not overwrite the historically correct S018 eight-descent calculation.
Changing earlier acquisition, initial source charts, known coordinates or
interleaved delivery changes the theorem's hypotheses and requires a fresh
cut audit. All five global foundations remain open.

## 6. Exact whole-graph relaxation

The same14-role graph is induced in the full native111 raw-local index-coding
instance and in its U63 puncture. Fixing all other inputs makes the same lower
bound apply to both broadcast relaxations. Thus each needs at least nine
whole-record symbols for every fixed finite common alphabet, even nonlinearly.

For alphabets consisting of a finite characteristic-two field's V-dimensional
vectors, the retained canonical nine-row fitting supplies nine linear symbols:
each receiver forms its canonical row and cancels its actual raw orthogonal
side inputs. This is an **abstract broadcast** upper bound; it does not provide
nine legal physical chart descents, source acquisition or output delivery.
The exact nine-symbol relaxation should be credited separately from the new
source-bound physical stop, and its canonical attainment relies on the pinned
rank-nine proof rather than on the entropy certificate alone.

## Reproduction and controls

```
python -B review_nonlinear.py --dual ROOT/PETERSEN-SHORT-DUAL.json --repo RECOVERED_S018_CHECKOUT --published CLEAN_PROGRAMME_CHECKOUT --out audit
```

Expected status: `PASS_INDEPENDENT_EXPANDED_NONLINEAR_PETERSEN_GATE`.
The negative controls independently reject a negative conic multiplier,
an invalid decoder premise, a changed initialization bound, and a deleted
term that breaks the full-coordinate telescope.
