# A kernel-checked whole-word bridge for the binary count formula

Status: **checked in Lean 4.35.0 with no admitted proofs or new axioms**.
This second-wave component imports the unchanged first-wave copied-tree
size/degree proof and now proves the actual ordinary count. It does not
formalize a cyclic matrix factorization, a tape compiler, the OpenAI
source closure, or an improved multiplication bound.

The inherited mathematical dependency is
routes/A/characteristic-two-count-formula.md, used by the S003
succinct-factor and compact-interchange suppliers. Its elementary
balanced-adder construction receives no new priority claim here.

## Exact statement

Let \(m\ge1\), and choose a power-of-two padding size satisfying

\[
 m\le 2^r\le2m.
\]

The file constructs a literal tree of Boolean addition and multiplication
formulas. Leaf \(i<m\) is the independent variable \(z_i\) in its low bit;
all higher bits and all padded leaves \(i\ge m\) are literal false constants.
Addition evaluates as XOR and multiplication as AND.

Let \(C_k\) be output bit \(k\) of the balanced tree. For every Boolean
valuation, the main combined theorem proves

\[
 \sum_{k=0}^{r} 2^k C_k
   =\sum_{i=0}^{m-1}z_i,
 \qquad
 |C_k|\le32m^5,\qquad
 \deg_{\rm syntax}(C_k)\le2^k\quad(0\le k\le r).
\]

The sum is an equality of ordinary natural numbers, not merely equality
modulo two. The same formula in the exact-count conclusion is the formula
in the size and degree conclusions. No semantic assumption about an
unspecified count circuit appears in the theorem.

The source files are:

- formal/CopiedCountFormula.lean, unchanged SHA-256
  7acf9cb4b02b654166b8cd355e73b9c5b18a1ee77034c0439ca57b13a29877f8.
- formal/CountSemantics.lean, SHA-256
  83a7132dbbe2121204c004badbfc6d8345ca7e5eb77f5b24001e6b08dbdabb50.

The closing theorem is
MoonshotS005.BitFormula.paddedBalancedCount_complete_spec.
Its printed axiom dependencies are only propext and Quot.sound.

## What the proof checks

The previous file counts syntax as a tree: a repeated input contributes
its full size at every occurrence. Its carry is

\[
 xy+(x+y)c,
\]

so the previous carry occurs once. The file proves the exact size
identity, per-bit degree induction, repeated-prefix size majorant,
and its bound \(2^{4r+k}\le(2^r)^5\) for \(k\le r\).

The new file first proves ordinary ripple addition with its outgoing
carry retained:

\[
 \operatorname{value}_n(\operatorname{sum})
   +2^n\,\operatorname{carry}_n
  =\operatorname{value}_n(x)+\operatorname{value}_n(y).
\]

It proves every Boolean word is less than \(2^n\), then removes the
carry by reduction modulo \(2^n\). Induction through the actual balanced
tree shows that every finite output prefix equals the leaf total modulo
its word size. The total is at most \(2^r\); therefore \(r+1\) bits
retain it exactly.

A separate range-count induction identifies the recursive leaf total
with the contiguous input variables. Finally, evaluation congruence
shows that literal padded false leaves have exactly the semantics of
zero extension, and proves that their total equals the unpadded count.
The size estimate changes from \((2^r)^5\) to \(32m^5\) using
\(2^r\le2m\).

This removes the specific gap between a correct local adder and a
correct full count. It also prevents a circuit-sharing assumption from
quietly replacing the polynomial copied-formula claim.

## Reproduction and remaining boundary

The four isolated pure-Std files are replayed by formal/verify_formal.py.
From that directory run:

    python3 -I -B verify_formal.py --lean /path/to/lean

The recorded successful runtime is Lean 4.35.0, release commit
eb6cafb7290e8bd5f2937522d8d804f58f02bafc. The script compiles fresh
intermediate modules in a temporary directory, sets its import path
explicitly, treats warnings as errors, checks the printed axiom sets,
and records source hashes, commands and compiler output in
formal/verification.json. The first three source hashes are unchanged.

The OpenAI source pin requires Lean 4.34.1; that full project and its
comparator were not built. The new modules do not establish the
characteristic-two cyclic factorization, its full-rate tensor identity,
the finite spectral predictor, or the machine that realizes those maps
on tapes. Boolean evaluation corresponds to the prime subfield used by
the count formula, but the abstract field embedding has not been added
to this pure-Std development. Those are separate next bridges.

The current supporting formal components are the allocation schedule,
batch-product divisibility, copied syntax/degree/size, and whole-word
count semantics. Their scope is concrete and narrow. They strengthen
confidence in dependencies of the written AQ result while leaving its
complete physical and numerical proof obligations intact.

Prepared for Jerry Chen (@CubeJerry), with substantial ChatGPT assistance.

