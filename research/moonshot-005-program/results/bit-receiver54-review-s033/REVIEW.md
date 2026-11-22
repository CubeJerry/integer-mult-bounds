# Independent receiver-54 screen and literal candidate review

**Receiver 54 survives the parent projection necessary conditions. The seed-22
candidate has a common injective actual readout on the forced two-space, but
fails whole-proper isolation at eight donors.** No physical compilation or
complete fifth-receiver claim is justified by this candidate.

This review uses a separate GF(64) implementation and reconstructs physical
maps from source-pinned H words, phase frames and owner records. It imports
neither the construction's screen nor its candidate checker. It checks the
receiver-54 portion of the general screen, not all seven alternative targets.

## Native donors and complete parent outputs

The D1509 chart independently gives all eleven native donors:
0,32,35,38,45,61,62,68,69,90,100. For each donor and each of its four D parents,
the reviewer reconstructs the full 30-input H sections at receivers 9 and 48.
All 88 sections are invertible and satisfy the literal whole-interface identity

\[
 B_{jh,r} F_{jh} L_r S_{jr}=E_{jh,r},
\]

where E is the insertion of the two actual D1509 input flags from that parent.

For each donor the review uses all 112 actual receiver-54 outputs outside
D1509 from those parents. Their matrix C_j on [L9,L48] has exactly the same
row space as the construction's sixteen marked equations. Thus no omitted
parent output strengthens this projection test.

| Donors | Rank C_j | Kernel dimension | Projection ranks to 9,48 | Required ranks |
|---|---:|---:|---:|---:|
| 0 | 8 | 8 | 6,6 | 2,2 |
| 38,45,61,62 | 10 | 6 | 4,4 | 2,2 |
| 32,35,68,69,90,100 | 12 | 4 | 2,2 | 2,2 |

The joint projection has the listed kernel dimension and requires rank two.
Every one of these necessary tests passes. This is not an existence proof:
the two block images must also arise from compatible shared D sections.

For the six tight donors, each block C_j,9 and C_j,48 has rank six, their
joint rank is twelve, and therefore

\[
 \ker C_j=\ker C_{j,9}\oplus\ker C_{j,48},
 \qquad \dim\ker C_{j,r}=2.
\]

Their isolation conditions separate into vanishing of both block responses.
This gives exact conditions for further construction work without excluding
receiver 54 in general.

## The same two-space is forced by three H anchors

The three nonzero screen witnesses at donors 0,61,62 have the same column
space K, of dimension two. With L=[L6,L9,L48,L73],

\[
 K=L_9W_9+L_{48}W_{48},\qquad
 \operatorname{rank}W_9=\operatorname{rank}W_{48}=2.
\]

For each anchor, every one of its sixteen quotients visible at receiver 54
has an independently reconstructed decomposition of K using native H
observations alone. Explicit H-only coefficients are saved in the certificate.
The retained D observations used in the original screen are unnecessary for
these decompositions. Noncentral H observation values are checked to vanish
on all thirty source tuple entries.

Under fixed H words/owners and **literal H interface actions**, these
observations force the old source tuples on K independently of D. The reviewer
checks all 472 actual physical off-D1509 outputs vanish at each old anchor,
and its D ingress on K has rank two. Thus the common entire-fibre condition
would have to include this K. Changing physical H readout actions while
preserving only H spaces is outside this argument, as in the receiver-95
full-source review.

## Literal seed-22 candidate

The pinned candidate is
`bit-coupled-fifth-s033/other-receivers/target54/PENCIL-CANDIDATE.json.gz`.
This review applies its stated six-row protected source deltas to the old
full source maps and directly propagates K through the physical H words.
It makes no assumption that this canonical source extension satisfies all
full-bank source validity conditions.

The actual D output indices at receiver 54, reconstructed from the dual-H
flags and checked against retained-receiver controls, are

\[
 O_{54}=[0,3,7,16,19,22,27,32].
\]

The literal physical ingress images have donor-contrast rank 16 and augmented
rank 18. The actual eight D output rows annihilate every contrast and give
one common response of rank two. The claimed forced-space readout is valid.

Isolation fails:

| Donors | All 472 off54 rows | Parent 112 rows | Nonparent 360 rows |
|---|---:|---:|---:|
| 0,61,62 | rank 0 | rank 0 | rank 0 |
| 32,35,38,45,68,69,90,100 | rank 2 | rank 2 | rank 2 |

For every donor, the independently calculated parent response agrees exactly
with the section-only identity

\[
 C_j\begin{bmatrix}
 S_{j9}(S'_{j9})^{-1}W_9\\
 S_{j48}(S'_{j48})^{-1}W_{48}
 \end{bmatrix}.
\]

Invertibility of the full H sections forces this identity for arbitrary
replacement 480-to-30 linear source maps that retain these D spaces and
literal readouts. Consequently source extension or complement changes cannot
repair the displayed candidate's parent leakage with its D sections and
readouts held fixed. Changing the D word, its admitted readout matrices, the
retained spaces, or surrounding H interfaces is a separate question.

The certificate includes actual parent labels, full parent matrices, kernel
bases, native H anchor decompositions, physical ingress values and candidate
parent leakage matrices. Full source validity, all whole-fibre equalities and
physical cost compilation are not claimed here. No new kappa.

## Reproduction

From the repository root:

```sh
python3 -B research/moonshot-005-program/results/bit-receiver54-review-s033/check.py \
  --repo . --out /tmp/s033-receiver54-review \
  --candidate research/moonshot-005-program/results/bit-coupled-fifth-s033/other-receivers/target54/PENCIL-CANDIDATE.json.gz
```

Expected status: `PASS_INDEPENDENT_RECEIVER54_NECESSARY_SCREEN`. PASS denotes
the review and exact readout checks; the saved isolation result is negative.
The checker can also run the screen alone by omitting `--candidate`.

## Open next questions

Solve the simultaneous section-dependent parent isolation equations before
compiling another readout-only candidate. For the six tight donors both block
responses must vanish separately. A successful candidate would then need all
nonparent isolation equations, common entire-fibre equality, full source
validity and physical costs. The necessary projection screen alone cannot
supply those conclusions.

Credit @CubeJerry, S031/S032 H/source contributors, the S033 construction
worker's receiver screen and seed-22 candidate, the adversarial reviewers,
and the root's isolation-gate formulation. Substantial OpenAI assistance.
Apache-2.0; independent agent review, not formal or human certification.
