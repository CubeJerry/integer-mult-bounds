# Packet admission for initial correction and historical receiver gain

Status: **proved conditional linear-interface reduction**. This is an exact criterion for the specified interface, not a source construction and not a new kappa. All vector spaces are over a fixed characteristic-zero coefficient field, with unrestricted independent input vectors. It makes no integer residue-decoding or bit-complexity lower-bound claim.

## Data and chronological contracts

Let the pinned native common word have endpoint map F, split into terminal hub and off-hub maps F_h,F_o. Let u be its original common inputs and q an independent m-vector of donor differences. A family of s actual chronological controls has baseline payload rows H, strictly lower triangular earlier-control response L, and nonzero normalizing gains g_i. At control i the literal instruction adds g_i times (b_i minus the current payload), where the physically retained local target is b_i=H_i u+D_i q. This is not a pure overwrite unless g_i=1. Cached b_i is formed before initial correction and remains at its literal encoder chart. Set T=diag(1/g_i)+L; T is invertible by chronology.

Let Z_o,Z_h be the off-hub and hub endpoint responses to the additive increments. Let specified physically implementable historical decoders have baseline A u and control response B. Initial snapshots are taken **after** initial correction; each later observation is copied at its actual source time and chart, with a paid owned lifetime until use. No formal history coordinate is a free physical record.

Let V be a fixed linear right inverse on the required off-hub debt space: F_o V y=y there. V's output is supported on common inputs physically at the packet-receiving initial chart. Require H V=0 on that space. The source chart-3 right inverse uses same-role inputs, coefficient two on eight coupled first-Y coordinates and one on the other admissible coordinates. This applies only to 451 admissible off-hub roles; the other seven roles must have zero debt.

Desired receiver additions are A u+R q. Their baseline raw values, predetermined scaling, and receiver fields used for initial correction must already be at the initial chart. Funded raw receiver routes must visit every stored decoder record they consume. Original donor q values remain physically at the terminal hub until all hub correction and other consumers finish.

## Exact stacked criterion

Define

    J = Z_o T^{-1} D,
    K = -V J,
    E = R - B T^{-1}D + A V J,
    M = [ J ; E ].

The semicolon denotes vertical stacking. Send linear packets Cq to the initial chart. The prescribed initial common correction Kq and raw receiver correction Eq can both be implemented from these packets, without additional donor information there, **if and only if row(M) is contained in row(C)**. The minimum scalar packet count for this fixed V, controls and decoder family is rank(M). An r-packet interface exists exactly when rank(M)<=r. If A V=0, this simplifies to

    rank([ Z_o T^{-1}D ; R-B T^{-1}D ]) <= r.

Unit-donor decoders have A supported on initial donor coordinates, so A V=0 for chart-3 correction. Dropping A V J for an arbitrary decoder is invalid.

Proof. Initial correction gives H K=0. Actual increments satisfy T Delta=Dq, hence Delta=T^{-1}Dq. Off-hub error is F_o Kq+Z_o Delta=-Jq+Jq=0. The historical decoder gives A(u+Kq)+B Delta; adding Eq yields A u+R q.

Since F_o V is identity on the debt image, row(K)=row(J): each is a linear function of the other, using V and F_o. Thus row([K;E])=row(M). Recoverability from Cq is equivalent to ker(C) contained in ker([K;E]), equivalently the stated row containment. Necessity holds even for a nonlinear local decoder if its only q-dependent observations are Cq and the domain is the full field vector space: q and q+d are indistinguishable for d in ker C. Independent local original data do not repair that ambiguity. Sufficiency uses linear combinations; choosing a row basis of M attains rank(M). This is an algebraic minimum inside this interface, not a minimum over all communication algorithms.

## Guards, terminal restoration and physical lowering

The packet-rank condition alone is insufficient. Let G_0 be the COPY-destination response to initial perturbations and G_1 its response to selected increments, with one row for every chronological COPY guard. The unchanged source COPY instructions are valid only if

    G_0 K + G_1 T^{-1}D = 0.

Final endpoint neutrality does not imply this guard identity. Locations, live owned labels and every ADD/SCALE cochart requirement must also match the literal word.

Hub error is (F_h K+Z_h T^{-1}D)q. All original q remain physically at the hub, so subtracting this known linear combination restores every hub common field. This requires actual cochart operations and scalar services. History records are not substituted for q. All common outputs then equal F u.

An r-row basis C can be streamed as r real owned packets: form C_i q at the hub, MOVE once to the initial chart, apply its coefficients to initial common and raw receiver fields, then CLEAR. This uses r new packet MOVEs and no additional receiver-distribution MOVE: corrected receiver payloads use their already funded original routes. The source word waits until all corrections finish. Raw donor routes may be hoisted only once and retain every reservation charge. Streaming does not remove separate encoder-target caches or historical caches.

For a literal implementation factor J=J_C C and E=E_C C. Initial corrections use -V J_C and E_C; ADD counts are their nonzero coefficient counts, plus packet formation and ownership instructions. Scalar denominators, precision, bit growth and storage depend on the factors. Packet rank bounds neither these ordinary costs nor owned peak. Donor raw fields must finally regain their required second-copy endpoint values through an authenticated local recovery or paid transport. Coupled reverse outputs and hosted Y2-to-X2 outputs remain obligations until an actual word establishes them. This lemma assigns them no free restoration.

## Whole-system scope

The optimization variables are physically admitted controls, normalization, actual historical decoders and a compatible V. Their rows cannot be chosen merely to fit a desired low-rank matrix. The next source problem is to construct data for every required row with rank(M)<=r, all guards zero, full 1880-input restoration and the complete budget satisfied. The fixed E8 Gram column is separately excluded for donor77 in its original five-chart additive control class; other admitted low-rank matrices, access or processing remain open.

The independently replayed unit17 construction instantiates this interface with 17 rank-one packets, real caches and full common restoration. It handles 17 ordinary shear outputs, without improving their Gaussian price. The theorem retains the programme's uniform complex supplier, covered/completed BIT supplier, compiler, decoder, precision, ownership/erasure, source-access and complete recursive obligations, together with every foundational assumption. No rank inequality alone proves kappa=1/200.
