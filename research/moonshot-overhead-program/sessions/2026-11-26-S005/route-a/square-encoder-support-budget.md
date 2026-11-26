# Support uncertainty fixes the square-encoder child budget

Status: **proved scoped invoice obstruction; independent review pending**.
This elementary support-uncertainty argument tests the Bell endpoint
budget. It is not a lower bound for integer multiplication, Walsh
transforms, all basis changes, or the full-rate source row program.
Dependency: `paired-column-bell-executor.md` (BE1--BE3 and BE0).

## 1. The gate being tested

Bell uses one half-width Walsh at entry and one at exit. Grouping more
columns might suggest a quarter-width encoder with critical child mass
2 sqrt(1/4)=1. The following proof rules out that saving for square
encoders built from full-volume partial Walsh calls and monomial maps.

Let N=2^a and H_a be normalized Walsh. Write s(v) for support size.
A monomial matrix permutes coordinates and multiplies them by nonzero
scalars.

## 2. Support uncertainty and monomialized bases

**SU1.** Every nonzero real or complex v satisfies s(v)s(H_a v)>=N.

**Proof.** Flat entries give

    ||H_a v||_infinity <= N^(-1/2)||v||_1
                       <= sqrt(s(v)/N)||v||_2.

Output support gives ||H_a v||_2^2<=s(H_a v)s(v)||v||_2^2/N.
Unitarity cancels the nonzero norm. QED.

**SU2.** If E is invertible square and H_a E=E M for monomial M,
then on each permutation cycle C of M,

    (1/|C|) sum_(j in C) log2 s(E e_j) >= a/2.        (SU2)

In particular some column has support at least 2^(a/2). If all
columns have support at most 2^s, then s>=a/2.

**Proof.** H_a sends each E-column to a nonzero scalar times the
next on its cycle. Multiply SU1 around the cycle. Each support
appears twice, so product s(E e_j)^2>=N^|C|. QED.

E need not be orthogonal. Nonuniform supports still obey the cycle
average, although the implementation consequence uses a uniform
support-generating word.

## 3. Full-volume partial-Walsh invoice

Suppose E is a word of monomial maps and partial Walsh calls of widths
s_1,...,s_r, each on the complete N-coordinate array. A width-s call
multiplies support by at most 2^s, so every E-column has support at
most 2^(sum_i s_i). SU2 forces

    sum_i s_i>=a/2.                                  (SU3)

Executing E and its inverse by these full-volume calls gives
square-root-normalized child mass

    2 sum_i sqrt(s_i/a)
      >=2 sqrt((sum_i s_i)/a)>=sqrt(2).              (SU4)

This is a recurrence-invoice inequality, not a time lower bound for
a child Walsh call. Bell's single s_1=a/2 call attains both equalities.
If every s_i<=a/A, then sqrt(s_i)>=s_i/sqrt(a/A), strengthening the
mass bound to sqrt(A). Making every encoder call a high-arity child
therefore does not achieve bounded normalized mass in this class.

## 4. Recursive consequence and exact scope

A conjugation node has total child width 2 sum_i s_i>=a. In a positive
invoice tree using only this construction until fixed positive base
widths at most b, total leaf width is at least a. Thus it has at least
a/b full-volume base-call occurrences. The direct linear-in-a invoice
is not just an unfortunate equal-halves choice.

This assumes separately billed full-volume occurrences and no entry/exit
cancellation with neighboring computations. It does not apply to
rectangular encoders, variable-volume check rows, initialized/discarded
row expansions, arithmetic cancellations between encoded branches,
actual shared endpoint work, or new encoder operations beyond this
monomial/partial-Walsh word. Those escapes need their own full-rate
and physical accounting.

Stop optimizing the Bell pairing constant. Its common-layout algebra
is retained; improvement must change the endpoint-volume model or
supply a different converter mechanism.
