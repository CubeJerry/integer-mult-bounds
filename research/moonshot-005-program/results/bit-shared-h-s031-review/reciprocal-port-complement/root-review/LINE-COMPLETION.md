# Completing fourteen local H lines to all sixteen

**Accepted after independent worker-C proof and literal-certificate review.** At a fixed shared-D cut,
the accepted reciprocal source supplies fourteen lines in a four-dimensional
GF64 space U. At every geometric donor, the known incident lines are independent.
There are sixteen H parents of D, with each H incident to three donors and each
donor incident to four H parents.

Add one missing H line at a time. For every donor incident to that H, its currently
known incident lines span a proper subspace of U of dimension at most three.
There are only three such forbidden subspaces. Choose a nonzero linear functional
vanishing on each forbidden subspace, in the displayed four-column basis of U.
Its evaluation on the curve

\[
 c(t)=(1,t,t^2,t^3),\qquad t\in\operatorname{GF}(64),
\]

is a nonzero polynomial of degree at most three. It vanishes at no more than
three field elements. The union of the three exceptional sets has size at most
nine, so at least55 choices remain. The vector U c(t) is nonzero and outside
every forbidden donor span. Inserting its line preserves partial-star
independence. Repeat for the second missing H.

The result is sixteen lines such that the four lines at each of the twelve
geometric donors form a basis of U. This argument works for every extension of
GF64 and under direct repetition of the displayed scalar construction. It is
an exact finite-field existence proof, not a random-search extrapolation.

The root checker enumerates t=0,...,63 in the polynomial-basis encoding and
selects the first value passing the actual rank tests. It succeeds at all48
shared-D cuts. The chosen parameters and all sixteen complete line vectors are
retained in output/LINE-COMPLETIONS.json.gz, with the original fourteen unchanged.

These independent per-cut line systems do not choose common source matrices or
one common physical D word across receivers. In particular they do not repair
the recorded whole-H fibre mismatch. They are a more complete local interface
for a subsequent construction, without any new price or kappa claim.
