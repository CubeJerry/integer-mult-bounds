# Independent Route B review of the interchange obstruction

Review time: 2026-11-25 13:51 UTC. Reviewer: a separate ChatGPT research
agent assigned to Route B, not the author of Route C's proof. This is
independent AI review, not human refereeing or formal-kernel certification.

Reviewed file:
`../C/INTERCHANGE-COUNT-OBSTRUCTION.md`, SHA-256
`67945049963b8d640d875c326f62857af1cd91c36c4f1a6c23ed44696427ab99`.
Verifier SHA-256:
`94a255467d71d28858682f453ea38326fc1914e6c21e7c34c9d6a851880c2a7b`.

I read the complete proof and checked the corresponding source contraction
in pinned tape `interchange.tex`, including the full-volume reserve calls
and the actual recurrence. No algebraic objection was found.

Checks made independently in the proof:

* The Krawtchouk duality and generating function give the displayed
  nonzero spectrum, with the sign `(-1)^ceil(t/2)` for both parities of t.
* The outer tensor sum has exactly the constant and one-nonconstant-factor
  eigenspaces. The constant eigenvalue of the minus Gram block cannot
  vanish, by reduction modulo the odd prime p.
* Restriction to two letters is a principal-submatrix lower bound for all
  larger alphabets. The resulting rank bound makes `m>p^2` necessary for
  the source's stated sublinear contraction.
* The residue-agreement formula is exact. I independently derived its
  Parseval identity before reading Route C, obtaining a weaker bound.
  Route C's odd-frequency Gaussian-series estimate is correct and
  removes the extraneous square-root-of-p prefactor.
* For `m>=p^2`, the elementary constants used in the note suffice for
  `Delta<1/2`. Thus defect is strictly greater than `1/4`, and the
  combined source-specific incompatibility follows.
* The mixture-of-shifts argument produces a worst frequency, and the
  source simultaneous-swap spectrum realizes every independent sign
  pattern. The result is not inferred from an unrealizable spectrum.

The supplied verifier was run and passed: 10,302 Krawtchouk values,
5,312 character-row checks, a 156-dimensional minus-block modular minor
with the complementary plus block, 672 residue-function cases, and the
recorded contraction checks. The script regenerated its deterministic
JSON in its existing directory; no source edit was made. Future replays
should use an isolated copy to avoid concurrent regeneration.

My separate `count-aliasing-obstruction.md` preserves an independently
derived weaker estimate and exact checker. It explicitly defers to Route
C for the strongest combined conclusion. The next question remains a
small-characteristic evaluator retaining divided-power information, or a
different routing/Gram construction; increasing p in the published
geometry does not fix the scalar-count approach.
