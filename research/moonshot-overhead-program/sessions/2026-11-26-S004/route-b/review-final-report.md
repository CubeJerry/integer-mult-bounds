# Route B review of the S004 final report

Reviewed the complete session `FINAL-REPORT.md`, the final FFT supplier
snapshot, and the relevant exact-check receipts. Review time: before
the scheduled 01:01:15 UTC close. This receipt does not claim completion
of the requested interval before the session record is finalized.

**Final verdict: pass.** At 00:57:36 UTC I reread the report and confirmed
that both scope clarifications listed below were incorporated: its
complete FFT bound now chooses a=1 (M=2), and its monotone formula states
both threshold and budget ranges. No algorithmic or proof blocker was
found in the supplier/corrector chain. The following list records the
review corrections and their rationale, not outstanding requests.

1. Before the complete packed FFT time bound, specify a fixed modular
   budget, for example `a=1` and M=2. The supplier's own FFT2 bound is
   valid for every allowed a, but the full modular correction invoice
   is added separately. For arbitrary a growing as log n and alpha<1,
   its loglog term need not be absorbed by the displayed FFT3 term.
   Any fixed a makes the reported complete upper bound valid. The author
   proof already says the added modular cost is smaller when a is small.
2. With the sharp nonnegative bilinear count, explicitly retain
   `0<M<=U^2` and `0<=S<=2h-1`. The linked proof has these hypotheses;
   the threshold is essential, as its zero-candidate negative control
   demonstrates. The report's model exclusions are otherwise correct.

## Supplier and repair chain

The final frozen FFT author file in the repository matches the scratch
file, SHA-256
`fbc0204cb95cd22cfcde5cb508024ee514fc78190d6a45f76fa53c109f31633c`.
It explicitly recovers E through least nonnegative residues modulo M,
using the proved 0<=E<M promise. The scalar mass product is optional.
The centered alternative uses a separate modulus greater than 2(M-1),
at most 2M; it does not use an invalid same-M centered lift at M=2.
The full summed cost and one all-visited space bound are displayed.

The signed sparse, one-sided budgeted, proper-recurrence, precise
tall-Hankel, amplitude and hybrid summaries retain their distinct
promises. The report does not turn sparse or recurrence recovery into
an unrestricted signed product verifier. It correctly separates fast
correction from a fast all-input supplier, and labels the complete FFT
bridge slower than the current project bound. It does not claim that
the finite Python reference implementations execute the multitape
schedule.

## Exact counts

The final supplier receipt reports exactly 217 complete cases, 2,542
coefficient checks, 37,148 complex rounding controls and 2,229 fixed-grid
FFT stages, as the report states. The separate actual-engine integration
receipt reports 34 complete cases, 568 coefficients and 16 all-maximum
digit controls. I also read the lead's isolated integration JSON and
confirmed those counts and both component hashes match.

The actual-swap receipt matches the report's 1,461 boundary columns and
14 exact identity baselines. Its characteristic-two inverse and
strata-mixing port controls are real finite checks. My independent NS
review covers actual multiplicities and the absence of semisimplicity,
without admitting free address masks or physical inversion.

## Scope and attribution

The unconditional/conditional/component distinctions and the explicit
absence of a general multiplication lower bound are appropriate. My
review does not newly audit every complete E002/S003 theorem or Route A
geometry proof; the report points to their separate receipts.

Classical source attribution is accurate for the monotone rectangle
argument, sparse derivative interpolation, recurrence arithmetic and
the cyclotomic/ordinary FFT engines. The FFT note precisely limits the
Cooley--Tukey read scope to the indexed primary p. 297 and supplies its
own numerical and physical proof.

For additional scalar-rank provenance, Filmus's author-hosted
*Smolensky's Lower Bound* (September 2010), Section 5, Theorem 5.2 and
Corollary 5.3, explicitly contain the complement-monomial reduction and
binary binomial-tail bound:
<https://yuvalfilmus.cs.technion.ac.il/Manuscripts/Smolensky.pdf>.
I read that section and its sign-variable convention after the lead's
earlier source pointer. E003 already cites this exposition. S004's
source note disclaims priority for the scalar method; the final report
also makes no incompatible novelty claim. Preserving this exact pointer
would make the attribution record more direct.

No new mathematical gate was started during final reconciliation.

Prepared for @CubeJerry with substantial ChatGPT assistance.
