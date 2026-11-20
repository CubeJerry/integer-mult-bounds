# Reduced proper transfer of the all-RS spread word

For donor j and receiver i, take the sixty actual D with j in D and
i in D-perpendicular, in increasing D ID. Enumerate the eight left and
eight right relevant *real owners* at each D in their actual early/late
order followed by owner ID. Let L be the full map from the native donor
to these left rows, A_d the actual 8-square D response, and R the full map
from the right rows to the native facet. The one-body matrix is exactly

    B_ij = R diag_d(A_d) L.

Every proper path with these endpoints uses these D, by nested-chart
incidence. The code constructs L from the actual source and V/Hermite H
factors. For R it applies the field transpose of the actual F and K factors
in reverse algebraic order solely to compute matrix columns. The independent
forward K routine instead takes all actually delivered D fields, applies
each V^T and genuine retained-early addition, and returns physical early and
late F rows separately. Passing them through the actual F coefficient
matrices reproduces the same B on the checked pairs. The proper calculation
fixes original Y=0 to isolate the X response; the separate pure-Y invertibility
and actual-owner counts remain mandatory.

The eight-copy reduction is exact for the all-RS spread word. At both raw
endpoints the canonical coordinate index enumerates component (n=9,36), base
copy e=0,...,7, channel c=0,...,2n/3-1, polynomial power t=0,...,15 in this
order. Simultaneously reordering both endpoints to (e,n,c,t) keeps the
identity term unchanged. At each H, actual owner-label groups list whole
eight-copy packets in increasing copy order. Both single-phase 16-field
stripes partition into two physical 8-copy sets. Within every component
degree, source_slot assigns copy e to copy e, with identical field
coefficients for each e. Every H transformation and each D word is repeated
on these real copy groups. K is a repeated base chart, and its k_row terminal
assignment likewise sends copy e to the same raw facet coordinate group with
the same coefficients. Thus the full global proper response is a common
permutation conjugate of eight identical one-body matrices; in particular
rank(I+B) is eight times the one-body value. This assertion depends on
the specified all-RS source, spread K and the corresponding RS facet.
Other source couplings or raw terminal bases require a fresh argument.

`transfer.py` exports an Atlas with methods `factors(i,j)`, `block(i,j)`,
`terminal_inputs(i,j)` and `facet(i)`. The terminal input method returns the
physical early IDs, E, late IDs and Y. A result for fixed F does not immediately
apply to arbitrary terminal retuning. `check_transfer.py` executes all eight
copies directly on genuine source/H, D/K and F holder labels for full-vector
and isolated-lane controls including two double-singleton pairs. The result
matches the collapsed matrix after the declared canonical permutation.

Both scripts accept the repository, K author output and D CHARTS.json.gz
paths. NumPy with its portable field-table path suffices. The optional
row-major field multiplier may be compiled by
`cc -O3 -march=native -shared -fPIC gf64_matmul.c -o /tmp/gf64-matmul.so`
and supplied with `--library /tmp/gf64-matmul.so`. The optimized path uses
the same six-bit field coefficients. The scripts pin the physical D selector
and K word payloads. Matrix files can be regenerated with repeated `--block i,j`
options to transfer.py. No numerical inverse, probabilistic rank estimate
or off-field interpretation is involved. Independent source and transfer
review remain distinct from this author replay.
