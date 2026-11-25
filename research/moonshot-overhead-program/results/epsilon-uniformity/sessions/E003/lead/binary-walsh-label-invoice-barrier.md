# Exact binary-Walsh ranks and a local invoice barrier

Status: **proved scoped local-invoice theorem; independent review pending**.
This concerns the binary Fourier/Walsh labels in the source `kernel.tex`,
with its canonical first-difference free rectangles and charged Newton
rectangles. It does not lower-bound arbitrary Walsh algorithms, actual
tape runtime, or integer multiplication.

Source: OpenAI `math@3344da59991ed94f9ba711217b29c1d760badfa6`, Fourier
`build/kernel.tex`, read in full by the lead. The compact rational Newton
predictor retains this geometry. All logarithms are binary; the label
alphabet q is unrelated to the interchanger's address radix.

## 1. Exact geometric rank

Let q=2^t, t>=1, L>=2, and labels v in [q]^L. Over F2 the Gram matrix is

    Gamma(v,w)=1-Delta(v,w)=1+L+sum_i 1_(v_i=w_i).

**Lemma BW1.** Its exact rank, hence the source quotient dimension, is

    D=2+L(q-2).                                         (BW1)

Proof. Let E_i be functions of w_i whose q values sum to zero in F2.
It has dimension q-1 and contains constants since q is even. A sum of
single-coordinate functions vanishes only if each is constant, as follows
by varying one coordinate. Thus U=sum_i E_i has dimension 1+L(q-2).
Row differences changing only v_i span E_i, so U is in the row space
and every row is one fixed row plus U. The fixed row is outside U:
otherwise each `1_(w_i=0)+f_i(w_i)`, f_i in E_i, would be constant.
Its q-value sum is one, while any constant has q-value sum zero. Hence
rank=dim(U)+1. In particular D>=q.

## 2. Free incidence and a nonzero charged term

Put s=floor(L/2), p(k)=product_(h=1)^s(1-k/(2h)). Every odd distance
has nonzero rational weight -p(k). A fixed alphabet letter has exactly
t incidences in the first-difference partition on each specified side:
one per differing-bit position, with prefix/orientation determined by
the letter. Equal coordinates have one choice. Thus every label has

    lambda_free=sum_(j odd) binom(L,j)t^j
               =((1+t)^L-(1-t)^L)/2                  (BW2)

free incidences, with no zero-weight term. For L>=2,t>=1,

    lambda_free >= (1+t)^(L-1).                       (BW3)

For even L factor `(t+1)^L-(t-1)^L`; after division by two its first
term gives BW3. For odd L the sum is at least `(t+1)^L/2`.

Each canonical rectangle has equally sized sides: binary prefix halves
have equal cardinalities, preserved by products. If its source partial
transform uses 2r axes per incident row, its destination uses 2(D-r).
Its literal endpoint-axis invoice is therefore 2D times the common side
size, irrespective of r. Both endpoints must be accounted for.

In `p(k)=sum_(j=0)^s alpha_j binom(L-k,j)`, the leading coefficients
`(-1)^s/(2^s s!)` and `(-1)^s/s!` give

    alpha_s=2^-s !=0.                                 (BW4)

Its canonical list has binom(L,s)q^s common-subword rectangles, each
separately charged for every query. Dividing by q^L labels gives at least

    m binom(L,s) q^(-ceil(L/2))                        (BW5)

in the positive normalized invoice. Combining terms or sharing those
kernels is a different execution outside this literal-list statement.

## 3. Uniform lower bound over both parameters

Define

    J(m,L,t)=D[1+lambda_free
                +m binom(L,s)2^(-t ceil(L/2))].        (BW6)

**Theorem BW.** For m>=2^16, L>=2, t>=1,

    log2 J(m,L,t) >= sqrt((log2 m) log2 log2 m).        (BW7)

Thus local logarithmic loss is at least a fixed multiple of
Psi(log m), Psi(z)=sqrt(z log2(z+2)), uniformly in L,t.

Proof. Write x=log2 m, b=log2 J, u=L-1. The preceding bounds give

    b >= t+u log2(t+1),
    b >= x-(ceil(L/2)-1)t >= x-u t/2.                 (BW8)

If b>=x/2, use x>=16 and x>=4 log2 x. Otherwise u t>x, giving
`b>=t+(x/t)log2(t+1)`. If t<=sqrt(x), monotonic decrease of
log2(t+1)/t gives b>=sqrt(x)log2(sqrt(x)+1)>=sqrt(x)log2(x)/2,
which is at least sqrt(x log2 x). If t>=sqrt(x), arithmetic-geometric
mean gives b>=t+x log2(x)/(2t)>=sqrt(2x log2 x). This proves BW7.

The optimized retained upper invoice has matching O(Psi(log m))
logarithmic scale. Exact rank and incidence therefore do not by
themselves remove this local loss.

## 4. Meaning and limits

For the retained rational predictor the stage count is Theta(sqrt m).
Under A=Theta(m), normalizing its declared complete call invoice by
sqrt(A) leaves J up to absolute factors; finite repair adds nonnegative
terms. This supplies a local-loss premise for the separate nonstationary
numerical-invoice theorem.

This does not show every implementation must pay J. Joint partitions,
cancellations, endpoint sharing, different Gram geometry or repair can
change the invoice. A positive polynomial-arity routing toll is a separate
premise; BW7 does not establish it. Even with improved exact interchange,
numerical Walsh has this separate Psi loss, whose global effect depends
on that toll and the arity schedule.

Finite checks support the proof; there is no formal-kernel, complete
multiplier execution or literature-priority claim.

Credits: @CubeJerry; pinned OpenAI geometry and endpoint-sharing proofs;
the programme's rational Newton/repair processors; substantial AI-assisted
exact rank, incidence and local-invoice derivation.
