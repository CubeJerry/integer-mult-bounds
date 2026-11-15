# Exact block capacity of the fixed cohort/run source interface

**Algebraic capacity theorem; independent review pending. No new κ.**
The source's actual movement pattern permits a strict block advantage:

    max dim(D intersection W^(V)) = 9V+floor(V/2).

Here D ranges over arbitrary linear cohort-local run-carrier spaces with
the same full-record capacity per run. The scalar9-dimensional case has a
literal ADD/MOVE source in this package. The stronger block optimum still
requires its separately stated physical lane-compilation contract; it is
not promoted to a complete source or supplier by the algebraic theorem.

## 1. Precisely quantified capacity class

Let k be any field of characteristic two and V>=1. Let W^(V)=W tensor k^V
be the fixed15V-dimensional native h9 fitting code. The authenticated111
input roles are partitioned into the22 actual source cohorts S. A cohort
has r_S cyclic source runs, and all r_S original run carriers have width V.
Before leaving their common starting chart, their independent values span
some D_S contained in k^(S times V), with dim D_S<=r_S V. Define

    D = direct sum_S D_S.

This is the declared algebraic capacity class. It permits arbitrary linear
mixing between coordinates within a cohort. It forbids mixing different
cohorts before acquisition, additional run carriers, wider moving records
and free source imports. No scalar restriction is imposed on block matrices.
The fixed80-cache read-incidence matrix has binary rank40, equal to the
number of actual runs. Thus, when each D_S has full capacity and is physically
realized, the actual packet cache differences span this direct sum. The
matrix and all40 column identities are included in CAPACITY.json.

The h9 class of each cohort is constant. Accordingly W=W0 direct sum W1,
where dim W0=7 and dim W1=8, and D decomposes over the same two classes.
We maximize their acquired dimensions independently.

## 2. The class-one bound is exactly4V

The class-one cohorts beginning at roles52 and22 each have one run. The
projection of W1 onto their union has rank6, as checked from the actual
binary source rows. Its kernel has dimension2. Consequently, for any
U1 contained in D intersection W1^(V),

    dim U1 <= dim ker(projection) + dim projection(U1)
            <= 2V + V + V = 4V.

The old source's class-one carrier spans attain4V by tensoring their scalar
forms with I_V. Neither their exact basis nor their old donor ordering is
needed; only their span matters. A systematic basis realizes the same span
with fewer local ADDs.

## 3. The class-zero bound is floor(11V/2)

The only nontrivial class-zero capacity restrictions come from four
rank-three local projections with two runs each. Their actual first roles
are81,66,46,30. The other class-zero cohorts have four runs and projection
rank at most three, or are singleton axes with one run.

Choose the seven-dimensional W0 basis in CAPACITY.json. Its local dual
projection subspaces A_i have dimension3. The exact binary subspaces for
i=81,66,46 have zero triple intersection. These identities persist over
every characteristic-two field and after tensoring by k^V.

Let U0 be any acquired subspace of W0^(V), and set T=U0^perp in the
7V-dimensional coefficient dual. Since each relevant local projection of
U0 has rank at most2V, dual restriction gives

    dim(T intersection (A_i tensor k^V)) >= V.

Put X_i equal to those intersections for i=81,66,46, and t=dim T. Their
triple intersection is zero. In the ambient space T, codimensions are
subadditive for intersection, so

    t <= sum_i codim_T X_i = 3t-sum_i dim X_i.

Hence `3V<=sum_i dim X_i<=2t`, giving

    dim U0 = 7V-t <= 7V-ceil(3V/2) = floor(11V/2).

This argument allows arbitrary block subspaces, nonsymmetric choices and
noncommuting local maps. It is not an extrapolation from a scalar search.

## 4. Attainment and the strict block advantage

There is a common three-dimensional coefficient space

    H=span(24,32,64)

in the pinned seven-bit dual coordinates. Every one of the four A_i meets
H in dimension2. For even V=2s, decompose the coordinate dual into two
s-dimensional summands and put

    T=H tensor k^s

inside only the first coordinate summand. Then dim T=3s, and each local
intersection with A_i tensor k^(2s) has dimension2s=V. Therefore U0=T^perp
has dimension11s and each constrained cohort projection has dimension
6s-2s=4s=2V, exactly its two-run capacity. The other cohorts satisfy their
capacity inequalities automatically. This attains the bound at every even V.

For V=1, the plane L=span(24,32) meets all four A_i nontrivially. Its
annihilator is a5-dimensional admissible U0. For V=2s+1, take the direct
sum of the even construction and this scalar construction. Its dimension
is11s+5=floor(11V/2), so every positive width is covered.

For each cohort, extend the indicated U0/U1 projection to a subspace D_S
of dimension r_S V; r_S<=|S| ensures this is possible. Their direct sum
contains the desired U0 direct sum U1. Combining the two upper bounds and
this construction proves

    max dim(D intersection W^(V))
      = floor(11V/2)+4V = 9V+floor(V/2).

The remaining W acquisition demand is exactly

    15V-(9V+floor(V/2)) = ceil(11V/2)

under this fixed run-capacity interface. This is a capacity statement, not
a theorem that every global code, terminal choice or decoder can exploit
the fractional slack. W15 remains a retained sufficient target, not a
universal necessity for all architectures.

## 5. Physical realization obligations

The even construction is not a coordinatewise direct sum of two scalar
sources with two carriers per coordinate. In the first half, a constrained
cohort projection has rank1 per coordinate; in the second half it has rank3.
Their total is2V and must be packed across the same two width-V physical
carriers. That cross-coordinate packing is the actual new mechanism.

At V=2, one can choose a fixed basis for each cohort's projected subspace,
complete its r_S*2 rows to an invertible2|S|-coordinate binary matrix, and
apply that local matrix at the common cohort chart. Its inverse at Hub
restores every original. At V=2s this fixed two-lane circuit tensored with
I_s uses O(V) local work and unchanged whole-record carrier paths. Odd V
adds the scalar circuit. These are finite algebraic circuits, but the exact
permitted upper-source operations, local selectors/permutations, transient
ownership and ordinary charges must be exhibited and checked before a
physical block source is admitted.

The scalar word separately uses only the existing full-record ADD opcode.
It therefore supplies physical evidence independent of this unresolved
block compilation. The broad arbitrary-block model used in earlier lower
bounds is not treated as automatic authorization to omit upper-bound costs.

## 6. Exact evidence and provenance

Run `capacity.py` on the emitted scalar word. CAPACITY.json records the
native source pin, both W bases, all local projection ranks, four actual
local dual spaces, the zero triple intersection, H and its intersections,
the scalar plane, class-one rank-six pair, the40-run/80-cache read matrix,
and every systematic scalar carrier form. These finite binary identities
support the all-field proof above; they are not themselves a finite-width
search for every block code.

The seven scalar hitting planes found during exploration are not used as
a claimed universal block classification. In fact the theorem proves a
strict block advantage whenever V>=2. The source geometry and cohort/run
pattern are inherited programme results; the projection-capacity reduction,
optimal9V+floor(V/2) theorem and lane-packing mechanism are new in this
package. Credit @CubeJerry and the source predecessors, with OpenAI assistance.
