# Independent review of the rotation source-coset obstruction

**Accepted with the author's exact source, endpoint and finite-tail hypotheses.**
The proof covers a fixed finite matrix prefix, so it remains relevant after
the positive distinguished-column same-plus construction. It does not close
the Klein or C_T first interfaces. No new supplier or kappa follows.

## Independent derivation

Writing a for the source, direct noncommutative multiplication gives

    L Crot U = [[a T a,-a T a^2,-a N],
                [T a,N a^2,-N],
                [N a,-N a^2,T]],  N=I-T.

The last input column has ordinary part (0,-N q22,T q22), forcing q22=0.
In the first input column the lower ordinary part is
(T K0-N q21,N K0+T q21), where K0 is the ordinary part of a q00 a.
The projector rotation on these two terms is invertible, forcing both
K0 and q21 to vanish. A term a^2 g a cannot be ordinary: otherwise
a^2 g would be an ordinary multiple of a^-1, equating Gaussian ranks two
and one on the unbounded tail. This argument permits arbitrary coefficients
on the fixed prefix. Thus Q's third row is (q20,0,0); a right inverse of
Q makes q20 right invertible, hence a unit in the finite coefficient algebra.

Project the first input column onto the left ordinary source coset represented
by a. Let H be the ordinary part of a q01 a^-1. The full coefficient is

    K=(0,-N q20+T H,T q20+N H).

Every discarded term is justified separately. Terms a g a and a^2 g a
cannot belong to this left coset, because canceling their final a leaves
a g or a^2 g ordinary. Pure a^2 and a^3 terms have different Gaussian ranks.
The top one-source term contains q21=0. Pure source-rank counting alone
would be insufficient: exact ordinary-return controls a g a and Gaussian-one
return controls a^2 g a exist, but the latter is in a different left coset.

The row D=(0,-q20^-1 N,q20^-1 T) satisfies D K=I without any commutativity
assumption on q20,H,T. Expansion of the actual endpoint factorization shows
im(K) lies in the actual Gaussian-one encoder image. Both are entire free
banks. At each sufficiently large faithful physical width, inclusion and
equal dimension make their images equal. This is an endpoint conclusion,
not extraction of a convenient physical projector rank.

The last input column has Gaussian-one part (0,T a p,N a p), p=q02.
It is transverse to im(K): if Kx has its second entry in im(T) and third in
im(N), applying N and T respectively gives N q20 x=T q20 x=0, hence x=0.
Therefore the entire part vanishes and p=0. The remaining Gaussian-three
part is (-a^3 T2 z,0,0), z=q12, forcing T2 z=0. Q's last column is now
(0,z,0), so its invertibility requires z injective on a whole bank. This
contradicts nonzero T2. Faithful tail separation, nonzero T and ordinary
backward transports are essential hypotheses, retained explicitly.

## Exact independent controls

The checker imports only C's earlier pinned sparse Q(i) arithmetic, not B's
arithmetic, checker or result. It reconstructs the phase-sensitive source,
checks every column's Gaussian support and modulus for a through a^4,
recomputes both signed projector rotations and inverses, and verifies the
literal source block product. Its frame tests use q and H each noncommuting
with T; the wrong sign and omitted q inverse fail. Return examples preserve
the distinction between Gaussian rank and a specific ordinary left coset.
Universal status comes from the argument above and retained tail separation,
not these finite controls alone.

Credit B's source-coset construction and theorem, C's separate exact arithmetic,
the retained source/tensor-separation predecessors, @CubeJerry and OpenAI
assistance. All five foundational assumptions remain open.
