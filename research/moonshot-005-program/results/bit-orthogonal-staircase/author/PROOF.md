# Masked orthogonal staircases: a complete logical source and its scope limit

**Proved symbolic construction; author-verified finite native instance.
Independent implementation review pending. No new kappa.**

This package constructs the entire222-input BIT logical map with15 descending
packets, one per retained orthogonal class. It is a concrete correctness
scaffold and a sharp isolated-packet mechanism, not a target-feasible source.
The retained complete target invoice excludes even14 such packets. All native
physical/compiler, ownership/erasure, precision and outer-recursion obligations
remain separate. No previously selected certificate is changed.

## 1. General orthogonal-class construction

Let r_1,...,r_s be nonzero pairwise orthogonal real vectors in R^d, where
1<=s<=d. Let F_i=r_i^perp and C_i=intersection_(j<=i) F_j, with C_0=R^d.
Thus dim(C_i)=d-i. Independent original records x_i begin on span(r_i) and
must finish at Hub; independent y_i begin at zero and must finish at F_i
with value y_i+x_i. Values lie in any characteristic-two field, at any
positive whole-record width V. Every operation below is ADD with coefficient
I_V, a nested physical MOVE, zero INIT or explicitly charged owned CLEAR.

At zero, replace the Y values successively by prefix sums: for i=2,...,s,
perform Y_i+=Y_(i-1). The result is Y_i=sum_(j<=i)y_j. Move each Y_i to C_i.
For i<s, move X_i to C_(i-1); this is legal because r_i is orthogonal to all
earlier roots. Use X_s as a borrowed ascending tail accumulator. It starts at
C_(s-1), containing its own line. At C_i, descending i=s-1,...,1 in the
algorithm's loop, its value is T_i=sum_(j>i)x_j. Let Y_i read this value.
Then move the accumulator to C_(i-1); if i>1 add the waiting original X_i,
which subsequently continues unchanged to Hub. At i=1 simply finish the
accumulator's ascent to Hub. Original X_1 is already there. No X_1 addition
into the borrowed accumulator is needed.

At Hub subtract, equivalently add, X_2,...,X_(s-1) from the accumulator.
This restores X_s. Every other original X is unchanged at Hub. The local
preloads are exactly

    Y_i = sum_(j<=i)y_j + sum_(j>i)x_j  at C_i.

All chart reads occurred at the actual common C_i. There is no assumed
coincidence of information merely because its algebraic support is local.
For multiple disjoint classes, perform all such ascending acquisitions before
any packet birth, so ALL original X are restored at Hub first.

Initialize one owned packet at Hub and load P=sum_(j=1..s)x_j from actual
restored originals. Descend through C_1,...,C_s. Before stage i, its value is

    P = sum_(j<i)y_j + sum_(j>=i)x_j.

At C_i perform Y_i+=P and then P+=Y_i. Since characteristic is two,

    Y_i becomes y_i+x_i,
    P becomes sum_(j<=i)y_j + sum_(j>i)x_j.

The latter is the required invariant for the next stage. This two-ADD map
sends (Y,P) to (Y+P,Y), is invertible and has zero packet-through coefficient.
The completed original Y_i ascends from C_i to F_i. After the last stage,
P=sum_j y_j. Descend the remaining distance to zero and CLEAR this explicitly
nonzero arbitrary-input record. Original X and Y endpoints are all correct.

The algorithm is causal even though the tail-acquisition loop runs through
indices in reverse order: the accumulator moves monotonically upward through
nested C_i, while the later packet moves monotonically downward. No original
path restarts and no extra ascending owned carrier is used. The arbitrary
original Y masks are restored in the completed outputs, not assumed zero.

## 2. Accounting and native instance

For s>=2, the ADD counts are: s-1 Y-prefix updates, s-1 tail reads, s-2 tail
aggregations, s-2 restorations, s packet acquisitions and2s exchanges. Total
7s-6. The one-element case instead uses one acquisition and one output ADD,
or the same two-ADD exchange when retaining its historical pattern; it is not
included in the7s-6 formula. All actual native classes have size at least5.

Each original X and Y traverses d-1 ranks. The packet traverses d. With unit
rank steps the class MOVE count is2s(d-1)+d. Zero-rank moves are omitted.
The native partition has111 ports in15 mutually orthogonal classes, of sizes

    8,7,7,8,7,8,8,8,7,8,8,5,8,8,6.

Running the construction on all classes gives the full logical map

    X_j -> X_j;  Y_j -> Y_j+X_j,  every0<=j<111,

with222 original input columns,1674 unit MOVEs,687 ADDs,15 INIT/CLEAR and peak
one live owned record. All111 X are restored before any descending packet.
Every nonzero CLEAR is paid and retains the owned-erasure premise. The words
use exact rational real charts, including newly generated nested flags.

The source native is pinned at SHA256
51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78;
the retained partition receipt is
7c725fc39b03e00244d31860ce76a79f0011f90b15b22bb2f7e97f8d5af64117.
The builder checks every class, every operation, the complete map, every path
and the invoice while emitting the literal word. This author check is not
independent verification. The finite scalar construction and its componentwise
identity lift do not establish a uniform native compiler or multiplier.

## 3. Why independent one-packet modules cannot reach the target

Consider an isolated module in the same physical route model, with only one
descending packet, original X inputs on their actual root lines, original Y
and zero-born records initially carrying no X information, and otherwise only
ascending paths or stationary records. Original Y feedback is unrestricted.
Assume it completes two distinct targets i,j. If their roots are nonorthogonal,
neither input line span(r_i),span(r_j) belongs to the downset

    D={C:C subset F_i or C subset F_j}.

An ascending carrier starting outside a downset cannot enter. Initial inside
records have zero coefficients on the two independent x inputs. One descending
whole-V packet can first enter D at most once and inject at most V dimensions
of those inputs. Yet the two final Y records inside D require2V independent
coordinates. This contradiction proves that every pair of targets completed
by an isolated one-packet module must be orthogonal. At most d such nonzero
roots exist in R^d. The staircase attains this maximum on an orthogonal d-set.

Therefore a source that partitions111 target duties among mutually isolated
one-packet modules needs at least ceil(111/8)=14 packets. The programme's
complete monotone packet-cap theorem excludes q>=11 at k>=1/200 in the retained
caller, even with arbitrary monotone rank jumps. Hence no such isolated-module
architecture can reach the target. This is NOT a lower bound on arbitrary
joint q8/9/10 sources: multiple packets may seed one another's receiver regions,
and initial intermediate states may already contain prior packet information.
Those are precisely the kinds of joint histories the active programme seeks.

## 4. Provenance and next use

The two-ADD mixed exchange and physical receiver-downset principle were already
admitted in this programme. The new construction combines ground Y-prefix
masks, one actual restored tail accumulator and a nested descending staircase
to finish all members of each orthogonal class with a single packet. Credit
@CubeJerry, original BIT/E8 and class/history authors, the lead construction
and Worker C's preliminary independent algebra/count review. Substantial
OpenAI assistance; no human or formal-kernel verification is claimed.

Use the full word as a correctness/chronology scaffold and the isolated-module
gate to avoid pursuing mere repetition of locally successful blocks. The
target needs coordinated packet histories or a changed fully costed interface.
No movement exponent, covered BIT supplier, completed supplier or new kappa
is asserted.
