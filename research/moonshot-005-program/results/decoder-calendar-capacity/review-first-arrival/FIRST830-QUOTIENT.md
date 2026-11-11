# The first 830 route has two independent destination demands

This is a source-bound local witness for the capacity discussion. Before source
event 25489, execute the exact first-copy prefix and keep the 400 input
second-minus-first differences in their initial carriers. There have been no
main MOVEs or owned lifetimes. The next original instruction is public helper
830 moving from chart 3 to chart 56.

At chart 56 the complete current physical state consists only of common role
60 and its raw difference carrier. Let S be their row span, c the current
common role830 row, and d its virtual second-minus-first difference. The exact
source gives d=−q172/2. The two input-coordinate functionals

- the entering arbitrary helper830 coordinate, and
- the entering second-main172 coordinate

both annihilate S. On the ordered targets (c,d), they give the diagonal matrix
`diag(−1,−1/2)`. Thus their images in the quotient by S are independent. The
quotient rank of the two targets is exactly two; the ranks of S, S+c and S+c+d
are respectively 2, 3 and 4.

A single scalar-coded complete-field arrival extends the destination row span
by at most one dimension. It therefore cannot make both c and d simultaneously
available from this exact state, regardless of its scalar coefficients or
source encoding. Retaining c's existing route and adding one rank-one d route
is locally sharp for this simultaneous-arrival contract.

This does not forbid delaying d until a later consumer, changing earlier
coding, using another already funded route, or changing which virtual fields
must be current. In particular it does not contradict a demand-only helper
representation or a later quiet-route loan.

`first830_quotient.py` independently replays the authenticated source prefix
and checks the two exact dual coordinates, every destination holder, and the
row identity. It has no author imports. Reproduce with:

```sh
python -B first830_quotient.py --source SOURCE --output FIRST830-QUOTIENT.json
```

The receipt includes the full target rows and their current source versions.
No complete supplier or new κ is established.
