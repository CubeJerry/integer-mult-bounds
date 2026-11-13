# Past-only arbitrary helper-relation gate

This wave grants owned private source erasure, preparation, cleanup, cache
storage and ordinary work free. It imposes only the strictly earlier
coframed destination-B history condition. No later-A or zero-cleanup
condition is imposed. The earlier wave26 files remain frozen as a
zero-cleanup result and supply no future constraint here.

The exact #7481 native gzip SHA256 is
`acee323696b18914bd863d55341f92112b48d3d1dc1443c276efb6c396fcc0a9`.
The canonical payload and complete invoice pins are in SUBSETS.json.
All native event positions are zero-based.

For an event E, let P_E be its pooled strictly earlier destination-B
history, x_E its native row and H the helper-coordinate space. Because
x_E is outside P_E, an arbitrary single helper-only relation u enables a
provider precisely when u belongs to
L_E=(P_E+span(x_E)) intersect H and u is outside P_E. A subset uses the
intersection L of its L_E spaces. A generic vector in L can avoid every
old P_E simultaneously iff L is not contained in any of them. Over Q a
finite union of proper linear subspaces cannot cover L. A demoted
coordinate h can also be chosen nonzero whenever it appears in L's basis
support; its cheapest optimistic debit is min f(R_h) over that support.
Actual preparation, cleanup, simultaneous availability and storage are
additional obligations, granted free in this upper bound.

The code checks that its fourteen events are exactly the past-main
survivors in the pinned projected temporal receipt. It binds complete
rational target rows, owned MOVE literals, paid ranks and nonzero main
support to the actual word. Every selected history uses equal binary
frame subspaces and strictly earlier clocks. It rebuilds independent
rational bases from B's retained chronological generators and checks
history ranks against the independent root replay. Helper-extension
kernels retain full-row lifts. Their dimensions are checked by separate
projected-rank calculations. Intersections are checked for inclusion and
against dim(U intersect V)=dim(U)+dim(V)-dim(U+V). Synthetic nonzero
intersection and helper-extension controls pass.

All 16,383 nonempty subsets were covered. Exactly 16,366 intersections
are zero. The seventeen eligible spaces are the fourteen singletons and
three pairs; there are no eligible larger subsets. All zero masks and
all nonzero bases/supports are retained in SUBSETS.json. Empty parent
intersections propagate exactly. The full run completed in 0.55 seconds.

| Enabled sites | Lost target rank | Native gain at .0038 |
| --- | ---: | ---: |
| 30581 | 3 | -0.99276291300029566991811085473190172 |
| 30593 | 4 | -2.9789837303114766470001366428127908 |
| 35152 | 3 | -0.99276291300029566991811085473190172 |
| 35448 | 3 | -0.99276291300029566991811085473190172 |
| 35452 | 4 | -2.9789837303114766470001366428127908 |
| 35448, 35452 | 4 | -0.98424471722944524443052953506699821 |
| 36346 | 2 | 0 |
| 36358 | 4 | -2.9789837303114766470001366428127908 |
| 39875 | 6 | -0.98977264480647242158854040174750308 |
| 39884 | 2 | -0.99473901308203140256960710774579257 |
| 39875, 39884 | 6 | 0.010227355193527578411459598252496918 |
| 41646 | 4 | 1.9803029133026523874931293289617982 |
| 42487 | 4 | 0 |
| 42500 | 4 | -0.99148180422914957451241868033509649 |
| 44253 | 2 | -0.99473901308203140256960710774579257 |
| 45656 | 4 | -2.9789837303114766470001366428127908 |
| 35152, 45656 | 4 | -0.98424471722944524443052953506699821 |

The best candidate is event41646, granting one rank6 cache deletion and
debiting the rank4 target of coordinate770. Its optimistic native gain
f(6)-f(4) is 1.98030291330265238749... . The complete invoice has17 calls,
a baseline .0038 moment -59.24193388437490024..., and a required native
saving3.48481964025734707... . The best optimistic full moment remains
-25.57678435822980965... . All signs use the parent's directed rational
price bounds, with actual native payload binding and exact invoice pin.

Thus no profile here clears the complete .0038 deficit. This does not
exclude a smaller complete improvement: singleton41646 has positive
native gain, and {39875,39884} also has a small positive native gain.
Their physical construction and complete invoices remain unproved.

The scope is one homogeneous helper-only relation independent of arbitrary
mains, with unchanged native histories/frames/operations outside removed
owned MOVEs, one fully debited original helper target, and no extra zero-
MOVE credits. Proportional directions with additional zero-MOVE credits
are B's separate scope. Changed producer histories and frame routes are
not covered. No physical supplier or kappa is claimed.

Replay from the existing workspace:

```sh
python3 -I -B worker-a/past-constraint/subsets.py
```

Inputs are the pinned native word, root projected and full temporal
receipts, B's history and single-helper receipts, and the parent's budget
routine and pinned invoice. The script mutates no source word.
