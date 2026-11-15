# Three native duties require six residual directions in the packed two-copy source

**Proved scoped obstruction, conditional only on the declared linear interface; no new κ.**
The actual paid two-copy source has D of dimension80, W of dimension30 and A=D+W of dimension91. Replacing a second query by the specified class-zero delayed feedback does not make a complete decoder possible merely by adding one, two, three or four ordinary principal fields whose free seeds stay in A. This includes the prospective19-field construction that would have normalized q=19/2. The construction remains a valid partial source; the result identifies the next interface that must change.

## 1. Pinned interface and quantifiers

Use the frozen ordinary scalar word `two-copy-packed-source/output/WORD.json`, SHA256 `aa9d17693c1f976625ee420e1367680e86cfec0195259d609f7eddc258eda01e`, and native geometry SHA256 `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`. There are222 independent X coordinates indexed by native role i in0..110 and physical copy a in{0,1}. Let E be their coefficient space over any characteristic-two field k. The coefficient matrices are binary; the exact ranks and inclusions below are unchanged over every extension of the binary field.

Let D be the span of the160 actual scalar cache values at handoff, W the direct-sum h9 fitting space, and A=D+W. All these values are obtained by literal symbolic replay of the pinned source, not by treating hypothetical increments as acquired. Their dimensions are80,30,91, respectively, and dim(D∩W)=19. Let L_i be the span of both-copy coordinates x_(j,a) with root j orthogonal to root i. These are generously granted freely to receiver i.

Retain the actual P0 delayed feedback at depth4. Grant its two terminal rows and two proper-cell kernel rows globally. For query7 choose one of depths d=1,2,3, and grant the two class-zero delayed kernel rows k_(7,a)=e_(7,a)+sum of all query7 class-zero cache rows in copy a, and the two terminal rows N_(7,a,d)=sum of query7 class-one cache rows at depth at least d. These eight granted rows span B_d, with dim B_d=8 and B_d contained in D. The concrete second feedback need not yet be built: this is a favorable information grant, so excluding it excludes an actual decoder with no additional information.

For every positive integer s, tensor these fixed coefficient spaces by k^s. Permit arbitrary linear mixing of the s whole-record columns in the decoder and arbitrary free seed subspace S contained in A tensor k^s. Require actual historical W acquisition:

    W tensor k^s is contained in (D tensor k^s)+S.

If there are p separately paid principal physical fields, each an ordinary full Hub-to-ground lifetime in this interface, four are the two-copy mandatory feedback fields, leaving dim S at most(p−4)s. No restriction requires S itself to lie in W: arbitrary D offsets are allowed. No outside-A seed is admitted in this particular proposition.

Suppose every native receiver in both copies fits from B_d tensor k^s, S and L_i tensor k^s. Then

    dim(S intersect (D tensor k^s)) >= 6s,

and consequently p>=21.

## 2. Reduction to three virtual duties

Write T=S∩(D tensor k^s). Since W projects onto the entire11-dimensional quotient A/D, the history condition makes S surject onto (A/D) tensor k^s. Therefore

    dim T = dim S−11s <= (p−15)s.

For each of the five native roles1,8,11,22,23, exact source-bound elimination proves

    A intersect L_i is contained in D.

Every fitting row in A for role i differs from its fixed W_i row by an element of A∩L_i, so its class modulo D is exactly W_i modulo D. The same elimination proves W_1 contained in D, W_8+W_11 contained in D, and W_22+W_23 contained in D, copy by copy. Hence fitting all those receivers forces three virtual duties supplied by T+B:

1. the two coordinate demands of receiver1, with side space L_1;
2. the two sums e_(8,a)+e_(11,a), with side space L_8+L_11;
3. the two sums e_(22,a)+e_(23,a), with side space L_22+L_23.

The pair sums cancel the unique W quotient classes. This is a necessary consequence of individual fitting, not a claim that the virtual pair is a physical decoder operation.

For duty t, denote its two-dimensional demand space by Delta_t, let C_t=B_d+its side space, and put

    J_t = D intersect (C_t+Delta_t).

For all three duties the exact certificate gives dim((C_t+Delta_t)/C_t)=2 and J_t surjects onto that quotient. Any decoder must therefore supply a2s-dimensional subspace F_t contained in T∩(J_t tensor k^s) whose map to the demanded quotient is injective. In particular F_t intersects C_t tensor k^s trivially. This follows by selecting preimages of a basis of the demanded quotient; arbitrary block mixing changes neither the rank nor this section argument.

## 3. The direct-sum obstruction

The exact binary matrix certificate proves

    J_1 intersect J_2 is contained in C_1,
    J_3 intersect (J_1+J_2) is contained in C_3.

These inclusions persist after scalar extension and tensoring by k^s. Thus F_1∩F_2=0. Also F_3∩(F_1+F_2)=0, because any such vector lies in J_3∩(J_1+J_2), hence in C_3, whereas F_3 injects modulo C_3. Therefore T contains the direct sum F_1+F_2+F_3, of dimension6s. Combining with dim T<=(p−15)s gives p>=21.

The certificate dimensions are:

| Query7 depth | dim J1 | dim J2 | dim J3 | dim(J1∩J2) | dim(J1+J2) | dim(J3∩(J1+J2)) |
|---|---:|---:|---:|---:|---:|---:|
|1|54|58|54|42|70|46|
|2|54|58|54|42|70|46|
|3|52|56|52|40|68|44|

These dimensions are finite exact certificates for fixed matrices. The quantified conclusion for all fields and all s follows from the preceding linear-algebra proof, not extrapolation from a finite width test.

## 4. Consequence for the actual budget and escape scope

The current source has16 principal physical fields. Nineteen fields leave four residual D directions;20 leave five. Both fail this six-direction requirement. At least21 would add five actual rank8 principal lifetimes. Even before additional second-feedback receiver fragmentation, that expense exceeds the current necessary movement room: five times8^(199/200)>39.5, while the independently verified whole two-copy room is less than30.414. The inequality8^(199/200)>79/10 can be checked exactly by (79/10)^200<8^199. This is a real physical field count, not a fractional-record accounting convention. Adding21 fields is only necessary for this information interface; it is not asserted sufficient.

The result does not exclude source recoding that changes D, different cache-selector feedback kernels that change B, additional paid nonlocal information, or seeds outside A. It also does not exclude another correct low-cost decoder architecture. Those are the consequential remaining directions. The source's acquisition gain, paid-bank translation, actual Y0 outputs and historical W30 witnesses remain valid.

## 5. Reproduction and adversarial controls

```sh
python3 -B check.py --repo /path/to/programme \
  --source /path/to/two-copy-packed-source/output/WORD.json
```

Expected status `PASS_SOURCE_BOUND_THREE_DUTY_SIX_SLACK_GATE`. The checker authenticates the actual source and geometry, replays its values, reconstructs W from the native roots, checks all quotient uniqueness conditions and matrix inclusions, and emits explicit bases for D, B, every J/C space and both decisive intersections. `CERTIFICATE.json` contains the complete finite data. Three changed-information controls add the demanded fields and invalidate the gate; freely supplying all W rows positively fits every native demand. The formal literal-word geometry/ownership audit is separate in `../review-two-copy-packed/`.

Credit @CubeJerry, the native/cohort/source and retained-history predecessors, Worker C's packed source, root's paid-bank representation and19-bank question, and Worker A's three-duty proof and exact certificate. OpenAI assistance. All five foundational assumptions remain; **No new κ**.
