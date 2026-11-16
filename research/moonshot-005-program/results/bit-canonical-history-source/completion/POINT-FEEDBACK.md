# The changed code's 24-point set is closed under raw feedback

**Proved for this fixed code and local-information interface. No new kappa.**
This is separate from the four-direction completion theorem. A dimension
bound on new broadcasts alone would not exclude a free feedback cascade.

Let U8, E6 and T24 be exactly those in SOURCE.json. For a set T of freely
available raw coordinates, define

    Phi_U(T) = {i : e_i lies in U8 + span{e_j:j in T} + L_i},

where L_i contains every geometrically permitted foreign raw coordinate.
Exact native rank computations, with explicit witnesses, give

    Phi_U(E6)=T24,     Phi_U(T24)=T24.

Thus repeatedly adding only the raw outputs that can already be completed
from this information stops at T24. It does not reach all 111 receivers,
even if each newly completed raw coordinate is sent everywhere at zero cost
and every receiver has all of its permitted raw side information.

For each of the 87 outsiders, POINT-CLOSURE.json contains a binary vector
lambda_i with own coefficient one that annihilates U8, every T24 point row,
and L_i. The all-zero input and the input lambda_i produce identical available
measurements but different desired outputs. This proves the impossibility
for exact nonlinear decoders as well as linear ones. The same witness works
over every characteristic-two extension field, and at arbitrary positive
record width by varying a single coordinate. Induction on the feedback rounds
then proves the closure statement for any order of output announcements.

The new code can physically complete 15 outputs in the current word. This
closure result generously grants the other nine compatible raw outputs and
their global transmission, so it does not rely on the present delivery gap.
The result does not cover a changed ground code, new nonpoint coded messages,
new nonlocal receiver information, or a changed chronological interface.

```sh
python3 check_point_closure.py --repo REPO --source SOURCE.json --out output
```

Expected status: `PASS_CHANGED_U8_POINT_FEEDBACK_CLOSURE`. The checker verifies
every outsider dual and rejects all 87 own-coordinate corruptions. It does
not infer a universal impossibility from failed search. The finite native
system is fully certified; the stated field and width quantifiers follow
from the dual argument. **No new kappa.**
