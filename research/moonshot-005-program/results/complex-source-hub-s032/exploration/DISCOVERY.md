# Bounded discovery, separate from proof

The mixed-integer search minimized outgoing message capacity minus an exact
matching representation of the target cross rank. The original target splits
into889 nonsingular singleton and200 nonsingular two-by-two blocks. For these
blocks the maximum matching in the selected nonzero submatrix equals rank.

Three25-second searches found feasible cuts of deficit1. Each run stopped at
its time limit with a large unresolved dual gap. The solver was not used to
prove infeasibility, optimality, completeness or a mathematical lower bound.
Each returned chart set was subsequently rechecked by exact rational target
minors and a complete boundary enumeration; root supplied a separate raw-DAG
audit. The third cut alone rejects all120 retained endpoint pairs.

Optional reproduction, requiring SciPy only for discovery:

    python3 -I -B target_components.py
    OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I -B search_cut.py 25

Run these from this directory. The final proof is in the parent directory
and does not require these commands or search results to be regenerated.

A separate fixed-cut-mask experiment showed that the new third cut by itself
does not replace the earlier exhaustive reclosure screen:17,060 of the27,002
old fixed-cut pairs survive it; all seven old/new fixed cuts leave9,515. Those
counts are exploratory and are not used by the admitted theorem.
