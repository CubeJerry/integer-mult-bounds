# Nonlinear17/2 broadcast bound and nine-transfer consequence

**Proved for the exact54-unknown native-neighbour interface.** All records
have a common finite alphabet A, |A|>=2. Inputs are independent and uniform;
the code is deterministic and zero-error. Receiver i knows x_j precisely
when its native real root is orthogonal to root j and seeks x_i. The other57
inputs and initial Y values may be revealed. Every such broadcast Z obeys

    H(Z) >= (17/2) log|A|.

Consequently at least9 whole-record messages are required. Arbitrary
nonlinear operations and every positive block length are allowed. No9m
vector-rank bound or9 distinct owned-lifetime bound is claimed.

Reveal unknowns outside the14 roles
(18,55,56,105,109,66,69,70,89,93,15,14,31,35).
Exact native dot products show that14,31,35 are isolated in this induced
side-information graph. Their three values I are decoded from Z alone, so
H(Z)=3log|A|+H(Z|I). For each fixed I, the first eleven roles remain
independent and uniformly distributed with the same induced graph.

On those eleven roles V define g(S)=H(Z|X_(V minus S))/log|A|.
Determinism gives g(empty)=0. Independent uniform inputs imply
0<=g(S+i)-g(S)<=1. Conditional mutual-information nonnegativity gives
g(S+i)+g(S+j)>=g(S)+g(S+i+j). If S contains no neighbour of i, the
conditioning gives the decoder all its side information, so
g(S+i)-g(S)=1. These statements apply for missing indices as appropriate.

CERTIFICATE.json is an exact106-term rational linear combination of these
constraints:27 monotonicity inequalities,43 submodularity inequalities,
35 decoding equalities and one deterministic-empty equality. Its left
side reduces to g(V); its right side is11/2. All inequality multipliers
have the required sign. The standard-library checker reconstructs the
native graph and each constraint, validates signs and decoding premises,
and checks every coefficient by exact Fraction cancellation. Numerical
LP discovery is not part of the proof. Thus H(Z|I)>=11/2 log|A| in each
conditional slice, establishing17/2. A transcript of s records has at
most |A|^s possible values, hence s>=9.

For an actual fixed-schedule physical continuation, grant the chronological
value of every future strict owned downward transfer to every receiver.
Suppose every initial field inside F_i's downset depends on unknowns only
through i's native neighbours. Receiver i can simulate that downset from
its initial side information and the transcript: an ascending original
cannot enter from outside, owned inward arrivals are in the transcript,
and local arithmetic/zero births add no external information. Therefore
the transcript is a valid broadcast code and requires at least9 transfers.
Several transfers can belong to one lifetime. Input-dependent schedules,
wider payloads, infinite-alphabet nonlinear maps and changed source data
are outside this statement.

Independent full-field audits establish the premise separately for the
392-field masked-Hub cut1129 and408-field all54-held cut1269. The latter
has full source/endpoint/cost review elsewhere. Its original net ascents
cannot be cheaper than the direct suffix at exponent199/200, so its
necessary completed movement is at least1597.494093397153336907...+9.
This1606.494093... floor is below allowance1621.750880211152355246...;
the construction remains open. The canonical characteristic-two rank9
code makes the integral static count exactly9, without establishing the
fractional optimum or physical deliverability.

Run `python -B check.py --repo REPO --out OUT`. Controls reject a wrong
multiplier sign, omitted term, larger bound, changed graph and wrong isolate.
The independent review rederives all106 inequalities with native-role sets
and a separate orientation, and audits both source cuts without importing
this verifier. It also rejects a planted nonlocal initial field.

Credit the native/canonical and initial-chart-transcript predecessors,
Worker C's14-role linear obstruction and independent review, and @CubeJerry.
Standard Shannon inequalities supply the method; this exact certificate
and source application were developed with substantial OpenAI assistance.
No complete supplier, foundation discharge or new kappa is claimed.

Method reference: Anna Blasiak, Robert Kleinberg and Eyal Lubetzky,
[Index coding via linear programming](https://arxiv.org/abs/1004.1379v2).
The source-specific17/2 certificate is derived here; the general LP/entropy
method is prior work.
