# An actual dyadic transferred-kernel second interface

**Proved ordinary isometric column, unit, inverse and source identities at
all positive widths.** Put s1=SWAP_ad and s2=SWAP_ab. Let h conditionally apply
Y_c when a=d, including its phase i^((1-2c)1[a=d]). It is an ordinary
involution, commutes with s1,t1 and has ordinary A²-backward transport. Define

    N0=(I-s1)(I+h)/4, R2=(I-s2)(I-t2)/4.

An explicit signed ordinary monomial G conjugates s1 to s2 and h to s2t2.
Consequently G N0 G^-1=R2. For V=G N0, V*V=N0 and VV*=R2. Projectors are
formed after the collective tensor lift. The exact signed table and all phases
are in the proof; removing phases fails the intended identities.

The coupled-column support projector N satisfies N<=N0, so this construction
resolves the previous irreducible capacity comparison positively. The actual
column (I-N0,V,0) is isometric and satisfies the necessary coset equation.
Three coefficient shears and an input-bank swap produce

    Qcolumn=[[0,-V*,I-N0],[0,I-R2,V],[I,0,0]].

Each direction uses 15 ADD,27 SCALE,24 MONO and prefix bound11. A further
explicit completion Qhighlow uses 30 ADD,53 SCALE,43 MONO; its inverse uses
30 ADD,55 SCALE,43 MONO, with prefix bounds79/109. All three banks begin
arbitrary, temporary source changes are restored, and all full-field monomial
passes are charged. Neither completion supplies independent Gaussian jobs.

- C's [proof](../../sessions/2026-11-17-S020/checkpoint3-evidence/C/klein-transferred-kernel/PROOF.md), [actual words](../../sessions/2026-11-17-S020/checkpoint3-evidence/C/klein-transferred-kernel/output/WORDS.json), [receipts](../../sessions/2026-11-17-S020/checkpoint3-evidence/C/klein-transferred-kernel/output/RESULT.json).
- B's [independent review](../../sessions/2026-11-17-S020/checkpoint3-evidence/B/klein-transfer-independent-review/REVIEW.md) uses separate exact Q(i) arithmetic and no C checker imports, replays all four words, both inverse products, phase controls and eight omitted-ADD controls.

A subsequent independently reviewed endpoint theorem excludes the entire
completion family with this fixed last column from the desired (4,2,1) caller.
It does not invalidate the positive column/unit identity. Changed left action
or first interface remains outside that exclusion. Credit @CubeJerry, source,
Klein and ordinary-capacity predecessors, C and B; OpenAI assistance. No new complete κ. The selected conditional bound remains κ=.00363005817. Both strict suppliers, the complete outer assembly and all five foundations remain open. This is ongoing research and is not PR-ready.
