# Exact-sum Gaussian rounding with optimal bilateral slack (1/\sqrt2)

This package gives an explicit global bijection on pairs of Gaussian
integers. Relative to the ideal #6509 operator
\(C_+(u,v)=((s+id)/2,(s-id)/2)\), the map has combined Euclidean error at
most one, preserves the complex sum \(s=u+v\) exactly, is covariant under
global multiplication by \(i\) and wire swap, and has an inverse related by
complex conjugation. Its bilateral pair-radial supremum is exactly
\(1/\sqrt2\).

The upper bound is proved for the explicit map in [proof/PROOF.md](proof/PROOF.md).
The lower bound applies to every exact-sum integer-output map with error at
most one; it does not assume bijectivity. Thus \(1/\sqrt2\) is optimal under
the exact-sum constraint. Because conjugation preserves norms and gives
the inverse, every inward radial change is paired with an outward change
of the same size. The forward outward supremum is also exactly
\(1/\sqrt2\), optimal among exact-sum error-one bijections with this
conjugation-as-inverse identity; see the root audit for this corollary. The
map does not satisfy an \(F^4\) identity.

## Construction

Write real coordinates \(s=u+v\), \(d=u-v\),
\(H(a,b)=(a+b,a-b)\), \(T=H/2\), and \(J(a,b)=(-b,a)\). If the
coordinates of \(s\) have the same parity, output difference \(d'=Jd\).
Otherwise let \(p=\Re(s)\bmod2\), \(t=TJd\), and apply the phase-swapped
two-axis half-grid involution \(M_p\) defined in the proof. Put
\(d'=HM_p(t)\) and return \(((s+d')/2,(s-d')/2)\).

The exact inverse, parity classes, phase covariance, wire-swap covariance,
error bound and radial estimate are proved algebraically. The sharp lower
bound uses the fixed-sum family \(s=(1,0)\), \(d=(2a+1,0)\), where every
legal error-one exact-sum output has one of two radial gaps tending to
\(1/\sqrt2\).

## Evidence and reproduction

The frozen integer checker and result are copied unchanged under `proof/`.
Root's separate exact `Fraction` implementation and result are copied under
`review/root/`. `verify.py` loads source bytes directly, cross-checks both
implementations, repeats their bounded exact cases, and checks concrete
failure controls for a wrong phase assignment and for \(F^4\). It also checks
the `n=1` witness for the pinned #6778 same-map row/column obstruction.

From the repository root, using Python 3.12 and the standard library:

```sh
python3 -I -B -W error research/conserved-phase-optimal-gaussian-rounding/verify.py
python3 -I -O -B -W error research/conserved-phase-optimal-gaussian-rounding/verify.py
python3 -I -B -W error research/conserved-phase-optimal-gaussian-rounding/proof/check.py
python3 -I -O -B -W error research/conserved-phase-optimal-gaussian-rounding/proof/check.py
python3 -I -B -W error research/conserved-phase-optimal-gaussian-rounding/review/root/check_candidate.py
python3 -I -O -B -W error research/conserved-phase-optimal-gaussian-rounding/review/root/check_candidate.py
```

The cross-check covers the integer cube \([-4,4]^4\), 60 deterministic large
integers through 400 decimal digits, and 20 power-of-two cases through
\(2^{512}\). These finite checks corroborate and challenge the written proof;
the all-input result follows from the proof, not enumeration. All replay
commands are read-only. Source pins and role boundaries are in
[SOURCES.json](SOURCES.json) and [ROLE-BOUNDARIES.md](ROLE-BOUNDARIES.md).
`sha256sum -c CHECKSUMS.sha256` verifies the packaged artifacts;
`FREEZE.json` inventories those files and records the checksum-list hash.

## Related work and limits

Ali Romman's #6509 supplies the conserved Gaussian pair operator and exact
sum-rounding lineage. Nick Petalas's #6619 frames the outward-slack
optimization question. CubeJerry's #6778 theorem at its pinned head proves
that no globally Gaussian-unit-covariant map exact on all integral ideal
images can commute with itself across row and column applications. This
candidate satisfies both hypotheses for the `n=1` native transform, so that
same-map tensor commutation is impossible here; an exact `n=1` rank-one
witness is included in `verify.py`. The current global-half branch at commit
`26226aa52337e6e94bc0cdf3cf6b89d16bb42f5f` gives a different, less
constrained global construction with bilateral slack \(1/2\); it does not
establish this exact-sum, global-\(i\)-covariant, inverse-by-conjugation
contract. Exact references and blob/hash pins are in `SOURCES.json` and the
copied proof's source notice.

This package proves an unbounded-integer arithmetic theorem only. The same
stateless map cannot be used as a commuting row/column rounder under #6778's
hypotheses. The theorem does not rule out ordered execution, different maps,
or an enlarged state/representation, and no selected caller contract is
supplied. There is no fixed-width implementation, native supplier, precision
recurrence, physical tariff, or new \(\kappa\). All five selected framework
assumptions remain. The fourth-power counterexample also shows that this map cannot square
to wire swap.

## Open next questions

1. **Can an actual caller use this map through ordered execution, different
   per-axis maps, or enlarged state?** #6778 rules out commutation of the same
   stateless map across row and column applications because this map is
   globally unit-covariant and exact on integral ideal images. First pin the
   caller and determine whether it permits a different representation or
   execution order. No caller admission is included here.
2. **Can the map be implemented with a complete fixed-width or tape budget?**
   This matters for precision and storage assumptions. First choose one
   signed format and account for every temporary, return and recursive child.
   No physical implementation or tariff is supplied.
3. **What is the best tradeoff if exact-sum conservation is relaxed?**
   The global-half branch has a smaller bilateral constant under a different
   interface. First compare the full identity constraints and prove a lower
   bound for a precisely stated intermediate class. This package only proves
   optimality within exact-sum maps.

## Credit

Prepared for @CubeJerry with substantial OpenAI Codex assistance. The root
provided the candidate phase-pairing formula and wrote the separate
`Fraction` checker. The proof/integer-check role formalized and tested that
same formula. These are distinct implementations of a shared proposed map,
not a blind or human review; no formal proof assistant was used. Full role
boundaries are recorded in `ROLE-BOUNDARIES.md`.
