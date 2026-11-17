# Independent review of the two-copy whole-record F4 compiler

**PASS: exact local compiler and literal partial source, not a complete
supplier.** This review composes two independent checks: root reconstructs
the field algebra and whole-record implementation, and C reconstructs the
complete chronological source, its geometry and its current cut.

The reviewed word has SHA256
`9cda39e27c2416a4eac6dbb714bc53239f1cb1c83ba4423ee50a704fc14df550`.
The two copies are separately paid collections of original records. They
are not masked coordinates within one original record.

## Algebra and compiler

Root's checker defines F4 independently as F2[x]/(x^2+x+1), reconstructs
all twelve edge-dependent two-by-two field matrices, and expands their
action into four-by-four binary matrices. It checks each actual ADD list
against that matrix and its reverse list against the inverse. All 72
forward-ADD omission controls change the required local map. The complete
forward network uses 72 ADDs, the inverse another 72, and actual native
seeding uses 16 ADDs. These are whole-record ADDs on the two paid copies.

The checker independently derives the entire eight-by-eight F4 payload
matrix. Each output has the other three same-frame native roles with
identity coefficient, plus three nonzero cross-frame native roles. Every
coefficient is compiled into binary whole-record operations. No field
scalar primitive or lane selection is assumed. Since the resulting
identities are binary matrix identities, they hold over every
characteristic-two field and after tensoring with an identity at every
positive record width. The tensor coefficient algebra need not remain a
field for this conclusion.

Root then reconstructs all 444 original columns through both exact parent
prefixes, seeding, forward compiler and ground inverse. The resulting 812
current fields match C's separately reconstructed physical cut. In
particular all arbitrary original Y baselines are restored, rather than
being checked only on zero initial Y values.

## Physical chronology and invoice

C's separate checker replays the literal word without importing A's builder
or interpreter. It checks every cochart ADD, every nested MOVE, every
public upward direction, each zero birth and retirement, and the final raw
X endpoints. Its source-specific audit is retained alongside this review.

The full source has 368 INIT, 2872 ADD, 992 MOVE and 368 CLEAR, with moment
profile 326[1]+238[2]+206[4]+222[7]. At cut 4010 there are 812 fields, 206
ground public Ys and 16 public Ys at rank six. Only the 16 coordinate
outputs are complete. The eight geometric frame roles per copy have a
partial native payload; their diagonal corrections are not supplied.

The normalized movement equals the three-copy source's movement, while
ordinary ADDs per copy decrease. The payload coefficients differ, so this
is not an unconditional dominance claim about every possible continuation.

## Scope and reproduction

Run root's `check.py` with explicit `--repo`, `--word`, `--cut` and `--out`;
the `--cut` input must be C's independently generated current inventory.
C's physical audit takes explicit `--repo`, `--word`, `--theorem-checker`
and `--out`. The checkpoint reproduction runner provides portable paths.

This establishes the stated finite source and a uniform binary compiler.
It does not supply the complete batched caller, terminal delivery,
precision, ownership, recursive accounting or a new complete kappa. The
separate private-region theorem imposes further source-specific duties.

Credit A's source construction, C's complete physical audit, root's
independent algebraic review, the retained source and geometry authors,
@CubeJerry, and substantial OpenAI research assistance. This is a research
agent review, not human or proof-kernel certification.
