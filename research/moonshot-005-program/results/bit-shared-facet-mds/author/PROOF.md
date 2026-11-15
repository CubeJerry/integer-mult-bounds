# Shared-facet MDS correction across independently paid copies

**Proved local algebraic/physical construction with exact source geometry. No new κ.** A four-chart correction is implemented by an ordinary-record word on four independent binary copies of the pinned111-port unit. Its paid completion control completes one native receiver. A28-chart/16-channel construction is proved parametrically with GF32 coefficient certificates. The simultaneous all-receiver source and chronology remain open.

## 1. Source and computational model

The authenticated111 native integer norm-four roots are in `research/moonshot-005-program/sessions/2026-11-14-S013/cloud/SOURCE-RECOVERY.json`, SHA256 `8cd5303821f7cb529ab756e1c6d6697672023a9d63193a676fd0b7c62308ab4e`. Let L_j=span(r_j), F_i=r_i-perp in real dimension8, S_i={j≠i:r_i·r_j=0}, M_i=Σ_(j∈S_i)x_j, and K_i=x_i+M_i. Geometry is real/rational; payload arithmetic is characteristic two. All physical records have the same original width s. Copies are separate records, with every MOVE, ADD, INIT and dirty CLEAR charged. Fixed binary CNOT identities below work coordinatewise for every s≥1 over every characteristic-two field.

Multiple original Y banks ending at the same F_i can exchange information there. The earlier scalar arrival-to-proper-cover injection does not automatically duplicate across these banks. This package constructs that shared-facet behavior explicitly. It does not reinstate the withdrawn two-copy comparison of intrinsic cover218 with scalar cap194 in the facet-collector scope correction.

## 2. A rank-sensitive local lower bound

**Proposition1.** Let S be a finite set of source lines in a real facet F, not covered by any two proper real linear subspaces of F. Let b,s≥1. Independent inputs x_j∈k^(bs) are corrected by n width-s channels on proper charts C_a⊂F. Suppose linear maps L_aj:k^(bs)→k^s vanish when L_j is not contained in C_a, and decoders D_a:k^s→k^(bs) satisfy Σ_a D_a L_aj=I_(bs) for every j. Then n≥b+2, over every field k and with arbitrary block maps.

For any two distinct channels p,q, choose j outside C_p∪C_q. Their contributions vanish; the remaining n−2 width-s channels factor a rank-bs identity, so bs≤(n−2)s. The cases n≤1 fail because S is not contained in one proper chart. Repeated charts are allowed. The proposition requires source-local channels and is not a lower bound on arbitrary interacting global source protocols.

`NO-TWO-COVER.json` independently certifies the premise at all111 pinned ports. Delete one coordinate where r_i is nonzero, identifying F_i with R^7. The28 quadratic monomials on the foreign roots have rank28 modulo101, hence over Q and R. Two proper-subspace covers would yield two nonzero linear forms whose nonzero product vanishes on all roots, contradicting this rank. The certificate lists28 witness source roles for each port. This independently rechecks the no-two-cover fact used in the programme's canonical proper-cover results.

Thus the local bound is b+2, not the scalar cover3 multiplied by b. For b2 the four-chart GF4 construction below attains it.

## 3. MDS factorization and ordinary-record implementation

**Proposition2.** Suppose n proper charts C_a⊂F cover every source line in S at least b times. Over E=GF(2^d), take a b×n matrix D with every b columns independent. For each j choose b containing charts J_j and set u_j=D_(J_j)^(-1)x_j. Assign coordinate u_j,t to its selected chart, and let z_a be the sum of assigned coordinates. Then Dz=Σ_jx_j, since each source contributes D_(J_j)D_(J_j)^(-1)x_j.

Expand each field element into d separately paid binary banks. Every invertible E matrix becomes an invertible binary matrix. Gaussian elimination realizes it by ordinary inter-bank ADDs, with a swap represented by three ADDs. Reversing an elimination sequence applies the matrix; the forward sequence restores it. These binary identities remain true over every characteristic-two extension and every original width s. No uncharged operation selects halves of a single wide record.

A literal source-local schedule uses only original upward-moving records:

1. Choose b anchor charts A. Preencode the b original Y field banks by D_A^(-1) at zero; move each anchor to its chart.
2. At each L_j, preencode its b cocharted original X field banks by D_(J_j)^(-1); route each coordinate to its chosen chart.
3. At an anchor chart, ADD each arriving source coordinate directly into its original Y anchor, then move that source record to Hub. At a nonanchor chart choose one arriving original X coordinate as pivot, sum the other contributors into it, retain it, and send the others to Hub. These n−b pivots are distinct physical coordinates.
4. Move all Y anchors to F and postencode by D_A. Then move each nonanchor original-X pivot up to F, add its D-column contribution to Y, and move it to Hub.
5. At Hub undo nonanchor aggregations using the unchanged encoded contributors, then invert every source preencoding. All X originals are restored; Y has become y+Σ_jx_j.

Every route is a nested upward inclusion. No owned record moves upward. All cocharted operations are explicit ordinary ADDs. Arbitrary formal Y inputs are preserved. An independently valid preload may be used, but this schedule does not establish when a global canonical K_i preload can be formed.

For dimension6 charts inside a dimension7 F, each contributing original source bank pays rank5 to its chart. Every nonanchor pivot then pays two rank1 ascents; all other contributors pay rank2 to Hub. Each Y anchor pays rank6 then rank1. Unused original X/Y banks pay their rank7 routes. Encoding, aggregation, decoding and restoration ADDs are all charged.

## 4. Exact geometry:28 charts with incidence16

`search.py` starts from the native roots and closes projective lines under x↦x−(x·q/2)q. Every dot product used is even, every resulting vector has norm4, and the set stabilizes at120 projective lines. These are explicit rational vectors; the conclusion does not require a root-system classification theorem.

For every native i,63 full roots are orthogonal to r_i. The charts F_i∩q-perp, for q in the120-root set with r_i·q≠0 and q not parallel to r_i, have28 distinct restrictions to F_i. Each has dimension6 and contains36 of those63 roots. Each full foreign root lies in exactly16 charts, hence every actual native foreign root does too. `GEOMETRY.json` lists every normal and native support mask for all111 ports. Extra normals are legal charts, not fictitious source records.

This gives b16,n28 in Proposition2. Over GF32=F2[t]/(t^5+t^2+1), set D_ra=α_a^r for r=0,...,15 and28 distinct field elements α_a=0,...,27. Every16-column minor is a nonzero Vandermonde determinant. `MDS-CERTIFICATE.json` verifies inverses for all31 nonzero field elements and all selected matrices for receiver3's58 sources. Each binary matrix has an explicit finite Gaussian ADD synthesis. All28 chart channels have contributors here; a zero channel in the general construction may simply be omitted.

For receiver3 the direct-anchor algorithm on80 paid binary copies has379927 ADD and22540 MOVE, no owned records, and profile200[1]+4580[2]+4640[5]+80[6]+13040[7], where [r]=r^(199/200). ADD subtotals are364980 source encoding/restoration,3800 nonanchor aggregation/restoration,6060 Y anchor pre/postencoding,2407 nonanchor decoding and2680 direct anchor reads. These are exact synthesis counts for the proved parametric algorithm. No enormous80-copy literal word is emitted or claimed independently replayed.

An optional finite search checks scalar binary b2 five-channel color patterns in this28-chart atlas. Its negative result is limited to five distinct atlas charts. Sixteen native receivers admit a five-channel binary witness if a chart is repeated. These observations do not imply an arbitrary-block obstruction and are not premises of the MDS construction.

## 5. Four-chart literal source and paid one-receiver completion

For receiver3, charts F3∩F76,F3∩F81,F3∩F91,F3∩F96 double-cover all58 actual foreign roots. In GF4=F2[t]/(t^2+t+1), take D=[[1,1,1,1],[0,1,t,t+1]]. Every two columns are independent. Two field coordinates and two binary banks per field give four separately paid ordinary copies, with888 independent X/Y columns.

`four-chart-word/WORD.json` uses the first two charts as original-Y anchors. It has1050 ADD,1128 MOVE,no INIT/CLEAR, and profile12[1]+228[2]+232[5]+4[6]+652[7]. All X finish restored at Hub, all Y at their own native facets, and only Y3 changes: y3+M3 independently in each copy. Its two nonanchor pivots are actual source coordinates of roles1 and2. `check_word.py` checks rational geometry, all888 columns, every operation, endpoints and counts.

`COMPLETED-CONTROL-WORD.json` appends four late owned records initialized at Hub after X restoration. Each reads K3's59 actual original sources, descends Hub→F3, adds to its Y3, and is dirty-cleared. This completes y3+x3 in all four copies, at full cost4 INIT,1290 ADD,1132 MOVE,4 dirty CLEAR, profile16[1]+228[2]+232[5]+4[6]+652[7]. It is a paid one-receiver completion, not a free global code supply.

Five semantic negative controls remove source encoding, nonanchor aggregation, chart delivery, a pivot Hub return, or the late-K3 route. Each rejects. The predecessor using four X pivots is preserved in `four-chart-word-v1/` with generator/checker; it used1188 ADD and the same movement. The current direct-anchor schedule needs only two original-X pivots.

## 6. Conditional whole-system movement envelope

For b16,n28,d5 there are80 paid productive binary copies. Suppose a future global construction simultaneously forms every receiver's channels using one chart visit per original X coordinate, supplies compatible source/pivot assignments, restores all inputs, and makes canonical preloads available chronologically. These are substantive unproved hypotheses, and the strict one-hop independent-source model is subject to a separate cohort-filtration obstruction; the envelope does not assert feasibility of that model.

An optimistic allocation has8880 Y banks each paying[6]+[1];6660 X pivots each paying[5]+2[1];2220 other X banks each paying[5]+[2]; and720 actual canonical fields (rank9 per productive copy) each paying[8]. The physical profile is22200[1]+2220[2]+8880[5]+8880[6]+720[8]. Dividing every productive body and caller term by the same80 copies gives

Q_opt=(555/2)[1]+(111/4)[2]+111[5]+111[6]+9[8].

Exact integer200th-root directed intervals in `OPTIMISTIC-BUDGET.json` give Q_opt=1614.6750836050235274... and limiting room7.0757966061288278... under the retained caller invoice. The first positive tested even caller m is4. This is only a conditional optimistic movement allocation. It does not supply simultaneous acquisition, solve preload/restoration chronology, or omit the cost of a repair. All INIT/CLEAR/ADD, ordinary supplier, uniform complex supplier, finite compilation, precision, structural and foundational obligations remain.

The local word makes the chronology issue explicit: when chart aggregates exist,192 X coordinates remain encoded and some remain below Hub. At correction completion all X reach Hub but192 remain encoded; only the inverse restores them. A free ground canonical preload cannot simply be inserted earlier. The late-K3 control resolves the chronology for one receiver by a paid proper-facet import, without establishing global affordability.

## 7. Status, reproduction, and credit

Proved: local n≥b+2, exact native28/16 incidence, MDS local correction, characteristic-two ordinary-bank implementation, four-copy literal local word and paid one-receiver completion. Computationally checked: stated finite geometries, coefficient matrices, literal words and negative controls. Conditional arithmetic: the full optimistic allocation. Open: simultaneous global acquisition/decoding with canonical chronology and every existing supplier/caller obligation.

From this directory run `python search.py --repo REPO`, `python certify_cover.py --repo REPO`, `python certify_mds.py`, `python build.py --repo REPO`, and `python check_word.py --repo REPO`. The manifest pins all proofs, sources and certificates. Author replay is not independent review; a separate review is requested.

The next task is a compatible simultaneous acquisition/canonical-code interface, or a scoped obstruction to a proposed implementation. A local MDS correction does not establish a new multiplication exponent.

Credit: @CubeJerry and the persistent programme; root for the shared-facet mechanism,28/16 suggestion, rank-sensitive question, original-pivot routing and cohort caution; Worker C for independent native geometry, proofs, ordinary-bank construction, controls and exact certificates. Existing canonical proper-cover, finite-unit and bank-expansion results retain their original credit. Developed with OpenAI assistance.
