# Odd-parity bilateral half-unit sweep

This finite gate studies \(U=H_4/2\) on only odd-total-parity input and
output vectors, with error at most one and absolute radial change at most
\(1/2\). The complete finite odd input balls tested are \(R=5,9,11\).
For even total parity, \(Ux\) is already an integer vector and preserves
even total parity, so this gate focuses on the only rounded coset.

| Radius | Inputs | Parity-preserving corners | Accepted edges | Accepted output points | Quotient adjacencies | Flow / inputs |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 1,656 | 13,248 | 8,160 | 2,168 | 70 | 1,656 / 1,656 |
| 9 | 16,696 | 133,568 | 81,440 | 19,240 | 567 | 16,696 / 16,696 |
| 11 | 36,704 | 293,632 | 177,984 | 41,248 | 1,188 | 36,704 / 36,704 |

All three quotient flows saturate their input capacities. Each positive
orbit-pair flow is saved with the input/output orbit-capacity vectors, and
the exact source-side Hall neighborhood is saved in RESULT.json. The
biregular orbit-flow lift proves existence of a finite injection on each
ball; it does not supply a global assignment.

## Replay

From this directory:

~~~~sh
python3 -I -B sweep.py > /tmp/odd-half-result.json
cmp /tmp/odd-half-result.json RESULT.json
python3 -I -B verify.py
python3 -I -O -B verify.py
~~~~

The filter uses integer arithmetic only. The verifier checks every saved
orbit capacity, positive-flow conservation, sink capacity, complete cut
neighborhood, and two deliberate corruptions. See PROOF.md for the exact
criterion and finite matching lift.

This evidence is restricted to \(R=5,9,11\). It does not establish the
unbounded Hall condition or a global uniform rounder.
