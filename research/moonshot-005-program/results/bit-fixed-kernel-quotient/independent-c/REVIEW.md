# Independent review of the fixed-kernel quotient corollary

**Accepted as the stated sharp algebraic identity and conditional source
calculation. No new κ.**

The reviewed root proof is `root/delayed-feedback/FIXED-KERNEL-QUOTIENT.md`.
It is a valid reduction to the previously independently reviewed sharp
terminal-seed theorem. The fixed-grant hypothesis G subset D is essential;
the proof does not count an unacquired kernel as a freely chosen source seed.

Write g=dim G, a=dim(N intersect G), and S=T+G. Every admissible T gives
N+G subset S and dim S<=q+g-a. Conversely, for every S satisfying those
conditions, choose a complement U to G in S containing a complement of
N intersect G in N. Then T=N+U has T+G=S,

    dim T=dim S-g+a<=q,

and W subset D+T follows from W subset D+S because G subset D. Thus the
two feasible classes correspond exactly for the objective dim(S intersect E).
Applying the prior sharp lemma with mandatory space N+G and budget q+g-a
cancels the added g-a in the slack term. It gives precisely

    min(dim E, dim((N+G) intersect E)+z+q-n-r).

Feasibility remains q>=n+r. The arbitrary-field proof also applies to
tensor-scaled fixed spaces and arbitrary operator-valued terminal subspaces;
it makes no commutation or scalar-tensor assumption on T itself.

The independent finite control enumerates all16 subspaces of F2^3 and every
valid D,N,G,W,E,q instance with N,G subset D and q in0..3:471,040 cases.
It directly enumerates each feasible T, without invoking the author's
formula as an optimizer. Two negative controls show that adding dim G as
free seed slack is wrong and omitting its actual mandatory intersection is
also wrong. These tests are controls; the complement argument is the proof.

The source-specific premises were recomputed from the80 actual frozen cache
coefficient rows, without author rank code or donor-offset assumptions:

    dim D=40, dim W=15, dim C=9,
    dim(D intersect W)=8, dim(D intersect C)=5,
    dim((D+W) intersect C)=8.

Thus r=7 and z=3. For depth4, the actual proposed fixed rows g=e0+R0 and
the class-one suffix N are independent, lie in D, and their span intersects
C trivially. With q8 and n1 the exact canonical cap is3. For depths5..7,
N is zero, so the actual freely chosen terminal capacity is q7,n0; the cap
remains3. The checker records all seven depth cases to expose this change
of mandatory terminal dimension rather than silently assigning a free
eighth field to a zero record.

This review accepts those coefficient-space premises and the conditional
sharp bound. It does not independently admit a delayed-source word, prove
a physical decoder, bound every vertex gauge of the canonical fitting, or
exclude alternative source increments and target codes. The existing
rank/arrival theorem separately rejects any complete target construction
with only one width-V kernel. A later multi-kernel architecture must retain
the true dimension and acquisition constraints when this corollary is used.

```sh
python3 -B check.py --repo /absolute/path/to/integer-mult-bounds \
  --word /absolute/path/to/colored-eight-source/output/COUPLED-WORD.json \
  --out /absolute/path/to/RESULT.json
```

Expected status: `PASS_INDEPENDENT_FIXED_KERNEL_QUOTIENT`.
Exact proof/source/reviewer pins are in `MANIFEST.json`.
Credit the prior sharp quotient authors and reviewers, root's fixed-grant
reduction, Worker A's colored-source proposal, and Worker C's independent
review. Prepared for @CubeJerry with substantial OpenAI assistance.
