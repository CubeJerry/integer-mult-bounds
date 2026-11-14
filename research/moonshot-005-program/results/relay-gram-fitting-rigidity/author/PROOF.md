# The native contact pattern rigidly determines the Gram metric

**Proved source-specific compatibility theorem; independent review pending.
No new kappa.**

The anisotropic relay repairs an arithmetic defect. It also changes the
forward fitting equations. This companion identifies that change exactly and
proves that preserving all old contact zeros permits no anisotropic modal
preload at all, even with arbitrary whole-field operator blocks. The argument
uses a real orthogonal frame and seven equality witnesses from only seventeen
actual native ports. It does not infer a physical impossibility from a failed
search.

## 1. Source, notation and exact scope

The source is `proper-chart-relay/author/20/WORD.json.gz`, SHA256
`0edf81ca8f6a7e60e5a01d4acdcaefdb74882180b8d12c408513bc91cd625b1c`.
All labels below are historical native port labels, decoded through its
`source_role_map`. Let H be its 96 hosted ports and P its full 104 ports.
The actual binary normal at h is v_h, its initial line is L_h, and its final
Y/D facet is F_h = v_h^perp. Let g_h be the unit real root row in the recorded
omitted orthogonal frame, with the predecessor's normalization.

For distinct i,j in P the source identities are

    g_i g_j^T = 0  iff  v_i dot v_j = 1 over F_2.

The right side says L_i is not contained in F_j. Also g_h g_h^T = 1 and
L_h is not contained in F_h. Thus the matrix G-I has exactly the required
zero entries at forbidden direct contacts, including its diagonal.

Here a "preserved fitting" means preserving these algebraic zero equations.
They are necessary for an unchanged direct-original-X forward scheme whose
public carriers only ascend to their prescribed facets. An imported mixed
payload, changed chronology, additional chart movement or different caller
may escape this restricted scheme. This theorem does not prohibit those
mechanisms.

## 2. Orthogonal-frame rigidity, including operator blocks

Let k be any field of characteristic zero, V >= 1, and let Lambda be an
8-by-8 block matrix whose entries are arbitrary k-linear endomorphisms of
k^V. Scalars g_hi act centrally on these operators. Suppose

    sum_ab g_ia Lambda_ab g_jb = 0                         (1)

for every distinct hosted i,j with v_i dot v_j = 1.

**Theorem 1.** There is a single operator T on k^V such that

    Lambda_ab = delta_ab T.                              (2)

If in addition the diagonal of -I_(96V) + (g_H tensor I_V) Lambda
(g_H^T tensor I_V) vanishes, then T=I_V and Lambda=I_(8V).

**Proof.** The eight actual hosted ports

    B = [0,7,20,27,36,46,57,111]

form an orthonormal root frame. Their binary normals are respectively

    [11,21,161,38,146,140,56,191].

Let F be the matrix with these g rows. Exact root multiplication gives
FF^T=I_8. Every distinct ordered pair of these frame ports is forbidden,
so (1) says F Lambda F^T is block diagonal. Write its diagonal blocks
T_0,...,T_7. This step requires no symmetry of Lambda.

For a port h let f_h=g_h F^T be its coordinates in this frame. The following
seven forbidden pairs have coordinatewise products supported at just two
places. The table lists 4(f_i * f_j), where * denotes coordinatewise product.

| Actual ports i,j | Product vector | Consequence |
|---|---|---|
| 1,12 | e_0-e_4 | T_0=T_4 |
| 1,8 | e_1-e_4 | T_1=T_4 |
| 1,10 | e_1-e_5 | T_1=T_5 |
| 2,10 | e_2-e_5 | T_2=T_5 |
| 2,13 | e_0-e_3 | T_0=T_3 |
| 4,9 | -e_4+e_6 | T_4=T_6 |
| 5,9 | e_6-e_7 | T_6=T_7 |

Equation (1) turns each row into the displayed operator equality. These
seven edges connect all eight indices, hence every T_a is one operator T.
Conjugating back by the scalar orthogonal F proves (2). Since every g_h has
unit norm, each diagonal Gram block is T. Zero diagonal of the residual
therefore requires T=I_V. QED.

This is a universal linear identity argument. The finite certificate checks
its source-specific hypotheses. It does not promote a finite search over
matrices or field widths into a universal theorem. The dyadic proof also
works over any coefficient ring in which 2 is a unit, with appropriate free
modules, because it uses only central scalar identities.

## 3. Consequences for arithmetic repair

For scalar whole-field gates, equation (2) leaves Lambda=lambda I_8. The
companion `relay-sunit-family` theorem excludes every nonzero lambda in
S=Z[1/30] as a smooth-ring repair of this terminal twenty-target source.
Requiring the full old fitting, including zero diagonal, leaves only lambda=1,
whose old bad-prime obstruction is already independently established.

There is a useful stronger qualification for operator preloads. Assume
Lambda=I_8 tensor T with T in Mat_V(S), and assume the remaining D map is
invertible over S. Let C=g_S0^T g_S0 for the 76 unrestored ports S0. The
literal source gives

    rank_(F_127)(C-I_8) = 6.                              (3)

By the determinant lemma, the remaining D map is invertible only if
I_(8V)-C tensor T is invertible. If T-I_V had a kernel vector b modulo 127,
choose a nonzero a in ker(C-I_8). Then a tensor b would be a nonzero kernel
vector of I_(8V)-C tensor T, contradiction. Therefore

    T-I_V is invertible modulo 127,                       (4)

and in particular has rank V in characteristic zero. Every hosted diagonal
contact defect then has full whole-field rank. Operator repair preserving
off-diagonal zeros cannot hide its diagonal defect in a few coordinates.
This is an algebraic statement; it is not a bound on the cost of a new
multicast or mixed-history physical decoder.

The need to retain the diagonal qualification is real. For two external
channels, take N=[[0,1],[0,0]], so N^2=0. Then

    A=-I+G_S0 tensor N,
    A^-1=-I-G_S0 tensor N.

This is a formal smooth-ring repair with the old off-diagonal zero pattern,
but every diagonal defect is -I_2+N, of determinant 1. Implementing this
operator as an actual native whole-field service, and completing its forward
interface, are separate obligations. It is a boundary counterexample to an
unqualified operator version of the scalar S-unit obstruction, not an admitted
physical construction.

## 4. Exact debt of the anisotropic source

For the companion actual scalar matrix

    Lambda=(1/4)I_8+(1/24)diag(J,0_4),
    J=[[1,0,-1,0],[0,1,0,-1],[-1,0,1,0],[0,-1,0,1]],

the checker finds the following, in the same native port convention.

| Domain | Old forbidden off-diagonal ordered pairs | Newly nonzero forbidden pairs | Nonzero diagonal defects |
|---|---:|---:|---:|
| Hosted 96 | 4866 | 1612 | 96 |
| Full 104 | 5720 | 1948 | 104 |

On hosted ports the new forbidden coefficients are -1/48 (844 occurrences),
1/48 (752), -1/24 (12) and 1/24 (4). The Gram diagonal is 1/4 at 23 ports,
13/48 at 54, 7/24 at 17 and 1/3 at 2; none equals the required unit value.
The full 104 row extension is a mathematical fitting calculation; the
companion word does not execute all 104 forward corrections.

The smooth determinant 3375/128 and these debts are simultaneous exact facts.
Thus the construction is a source-level arithmetic repair with a changed
forward interface. It does not become an admitted supplier merely by
retaining the old MOVE histogram.

## 5. Physical budget and next obligation

The old 46.508011523... limiting room describes the same incomplete MOVE
profile under the retained price template. The 22 added scalar instructions
and entrance scale 3 require their own work and grid accounting. The old
finite-m correction and old forward cancellation credit cannot be transferred
to a new caller without proving its compatibility.

At minimum, a useful continuation must physically restore the remaining
76 D outputs, supply the changed forward service, and complete the compatible
rank-eight residual cancellation. Independent one-target relay service would
already require roughly two new owned rank-one moves per added target, far
beyond that room. This is a limitation of that service mechanism, not a
universal physical lower bound. A competitive continuation must share work
between targets or replace existing paid movement and must explicitly handle
the newly forbidden forward contacts.

The next constructive question is whether acquired mode information can be
used on preterminal public histories to implement both duties jointly. There
is no free access to the eight algebraic inverse aggregates.

## 6. Verification and attribution

Run `check.py --source /path/to/WORD.json.gz --output RESULT.json` with the
pinned predecessor word. Python standard library only. Expected status:
`PASS_EXACT_FRAME_RIGIDITY_WITNESS`.

The checker authenticates the literal source, reconstructs all roots and
contacts, verifies the eight-frame identities and seven exact table rows,
checks the violation counts, the bad-prime rank and the anisotropic unit
determinant. Boundary controls retain scalar-quarter off-diagonal fitting,
show anisotropic fitting loss, remove each tree edge, and check the square-zero
operator example. Universal quantifiers are justified in the proof, not by
finite checking.

Credit the predecessor native geometry, proper-chart relay and independent
ring audits, the scalar S-unit companion, @CubeJerry, and substantial OpenAI
assistance. No foundation is discharged and no complete kappa changes.
