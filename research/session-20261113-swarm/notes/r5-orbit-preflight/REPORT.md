# R5 Hall-witness orbit preflight

## Result

**Bounded negative result for the proposed symmetry and shell route.** The
1,692-input strict-\(\beta\) Hall witness is valid, but its setwise
stabilizer in the complete signed-permutation symmetry group of the
\(H_4/2\) error/slack graph is trivial. The supplied witness therefore has
no nontrivial orbit compression under that group. A bounded pivot over
squared-norm balls, individual shells, and every union of coordinate-parity
classes also found no positive Hall deficiency.

The witness has not been replaced by a short analytic membership rule. In
particular, this preflight does not turn the 1,692-item input list into a
closed-form set and is not a separate publication claim. The frozen R5
package remains unchanged.

## Exact symmetry calculation

Let \(H=H_4\), and let \(W_4\) be the signed-permutation group on four
coordinates. It has \(4!2^4=384\) elements. A pair
\((A,B)\in W_4\times W_4\) acts on an input/output edge by
\((x,y)\mapsto(Ax,By)\). It preserves both the error
\(\|y-Hx/2\|_2\) and the outward increment
\(\|y\|_2-\|x\|_2\) exactly when

\[
BH=HA.
\]

Since \(HH^T=4I\), for each possible input action \(A\) there is at most one
output action:

\[
B=HAH^T/4.
\]

The checker enumerates all 384 possible \(A\), retains exactly the cases
where this formula gives an integral signed permutation \(B\), checks
\(BH=HA\), and verifies closure under composition. There are exactly 192
graph-automorphism pairs. The diagonal subgroup using the same signed
permutation on input and output, \(A=B\), has order eight.

Using the exact R5 certificate, the input set \(T\) has setwise stabilizer
of order one in those 192 pairs. The declared output set \(N_\beta(T)\) also
has setwise stabilizer of order one. Thus no nontrivial subgroup of these
graph automorphisms preserves the supplied \(T\) for orbit counting. This
rules out the proposed symmetry reduction for this witness; it does not rule
out a different Hall set with more symmetry.

The certificate still passes the current exact verifier's direct
re-enumeration: all 1,692 inputs have exactly 1,691 outputs in their complete
strict-\(\beta\) neighborhood. The deficit remains one.

## Evidence-driven pivot

With the symmetry route closed for this \(T\), the checker tested compact
sets defined by squared norm and coordinate parity, using the same exact
strict-neighbor routine and no new matching search or radius.

- For all 26 nonempty sets \(B_k=\{x\in S_5:\|x\|_2^2\le k\}\),
  \(|B_k|-|N_\beta(B_k)|\le0\). The maximum is zero.
- For each nonempty exact squared-norm shell in \(S_5\), the same difference
  is at most zero. The maximum is zero at the origin shell.
- Every one of the 16 coordinate-parity classes is only partially present in
  \(T\); its certificate count is strictly between zero and the class size.
- All 65,535 nonempty unions of the 16 full coordinate-parity classes were
  checked exactly. None has positive deficiency. The largest difference is
  \(-456\), for the full \(S_5\), whose strict neighborhood has 3,577 points.

These finite counts are evidence against the tested templates, not a theorem
that no short analytic description exists. Membership in \(T\) remains
provided by the pinned input list. Membership in its complete neighborhood
can be generated from \(T\) by exact output enumeration, as `check.py`
demonstrates. Producing \(T\) itself without trusting the list would require
a structural definition or a pinned deterministic Hall-set constructor;
neither was established here.

## Exact reproduction and pins

Run from this directory:

```sh
python3 -B check.py
python3 -O -B check.py
```

The checker reads only the adjacent frozen R5 package. It authenticates the
compressed and expanded certificate and the exact verifier before loading
the latter from authenticated source bytes. It emits the complete counts in
`RESULT.json`; default execution writes no files. The ordinary and optimized
runs produce the same receipt.

Source pins and predecessor credit are recorded in `SOURCES.json`. The
canonical base is `e54523517d0f03e58352e647c403a5af3e525a57`; the expanded R5
certificate is pinned by SHA-256
`b1fe3d866d2184227f46ec73ec2021c546bba056e98077e657e9205d9db5ad8b`; and the
current exact R5 verifier is pinned by SHA-256
`611124563b42ec1c20d4755d190a850d1deac5ed743d6f98094ec97f7d893190`.

Credit: @CubeJerry's R5 candidate workstream and the existing exact verifier;
Nick Petalas's #6619; ywz65's #2589 finite-sphere predecessor, cited by #6619;
and Ali Romman's #6509 ideal Gaussian pair construction. This bounded audit
was prepared with substantial OpenAI Codex assistance.

## Limit

This work answers the proposed orbit-compression route for the supplied
Hall witness and the specified shell/parity pivot only. It neither resolves
the open global outward-slack infimum nor changes the finite R5 theorem,
selected \(\kappa\), or conditional multiplication frontier.
