# Active helper loans with an exact common-state shadow

**Status:** proved algebraic primitive; two full 1,880-input source instances exactly verified; scoped candidate census computationally reproduced. **No new κ.** The source is `research/shared-wire-split-composition/data/final.json.gz`, SHA256 `2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883`. All event numbers are zero based.

## 1. General immediate-closure lemma

Work over a characteristic-zero coefficient field, coordinatewise on arbitrary V-field values. Let common helper H and difference donor Q be cochart at A, with values h and q. Suppose an original legal H MOVE takes A→B. Suppose Q subsequently follows an already accounted route sequence to B, without any intervening operation requiring its original q payload. Until that reunion, H has no further MOVE, INIT or CLEAR, but it may undergo arbitrary common scalar reads and writes. The rest of the common word can run normally.

Track a scalar coefficient α_r for each virtual common field. Initially α_H=1 and every other α_r=0. Propagate α through precisely the source's linear instructions: ADD coefficients add, SCALE multiplies, INIT/CLEAR resets the owned role. A COPY destination is allowed in this construction only if its outstanding α is zero; the source's required zero destination is then also physically zero. At the reunion require every live field r≠H with α_r≠0 to be cochart at B. These are sufficient conditions for this particular one-escrow construction, not necessary conditions for all loans.

Perform the opening signed swap

    H+=Q; Q−=H; H+=Q.

The states become H=q and Q=−h. Execute the original H MOVE, and INIT one owned zero shadow Z at B. Throughout the window, rename every common scalar operand or destination H to Z. Other common instructions keep their original roles, charts and routes. The invariant is

    virtual common H = physical Z + α_H h,
    virtual common r = physical r + α_r h  (r≠H),
    physical H = q, physical Q = −h.

It follows by induction on each scalar and lifecycle instruction. A legal MOVE changes the representation of the whole field linearly; the same abstract linear error coefficient propagates. The coefficients are compiled from the fixed source word; they do not require additional run-time V-field storage. The symbolic h is not read remotely. It only describes the missing term, whose physical value remains escrowed on Q. A receiver cochart at B may add the actual physical H=q during the window; the receiver's own availability and future obligations remain separate conditions.

When Q arrives at B, perform

    H−=Q; Q+=H; H−=Q.

This restores H=h and Q=q. Correct each other nonzero debt by r+=α_r H. If α_H≠0, scale H by α_H (omit when it is1), then add Z. This restores H to its current virtual common value. If α_H=0, use the signed swap on H,Z instead: H becomes Z and owned Z contains−h. CLEAR Z after the assembly. The latter branch avoids an uncharged destructive public overwrite. All owned retirement still uses the admitted owned-erasure interface.

The result restores every live common field at the reunion, not merely its endpoints. Hence the unmodified common suffix is correct. A source read is represented by the exact virtual update; its physical destination may carry a tracked debt until closure. H need not be literally decoded at that time. This changes the common representation and lies outside a fixed actual-read decoding contract.

For d q-delivery ADDs and k non-H debts at closure, the nonzero-α_H construction adds 7+d+k ADDs, at most one SCALE, one INIT and one CLEAR. It adds no Gaussian MOVE. It uses one additional owned V-field lifetime. The zero-α_H branch replaces the final one-ADD assembly by a three-ADD swap. These are complete local counts, including the opening and closing swaps.

## 2. Two literal full-input instances

The literal word uses all 1,480 arbitrary common inputs, including the 1,080 dirty helpers, and 400 independent second-main inputs. It includes400 entry ADDs forming q=v−u, all 1,710 raw difference-main MOVEs, and 400 exit recombinations. Its baseline is one entire common native plus that raw difference bank; it is not a full difference native.

| Instance | Opening H MOVE | Donor arrival | Delivered q | Common debts at closure |
|---|---|---|---|---|
| Read/write active | H3:3→424 at 29097 | Q178 at 33597 | q67+=q178 after 32151 | α_3=1/2, α_67=1 |
| Read-active early delivery | H1340:3→597 at 36070 | Q122 at 37333 | q883+=q122 after 36071 | α_1340=1, α_1512=−1 |

The first window includes the actual H read at 33544 and writes at 33545 and 33582. The second includes a common H read at 36071, and receiver883 departs597 at 36168, before donor122 arrives at 37333. The delivery is thus physically earlier than that donor reunion. It is not claimed to add a missing target endpoint coefficient; these initial entry coordinates admit other reach routes.

Every common role and live common owner is restored at each closure:1,480 public plus 28 owned roles at 33597, and 1,480 public plus 41 owned roles at 37333. The final difference map is exactly I+e_67 e_178^T+e_883 e_122^T. Exit recombination gives the corresponding explicitly stated partial physical two-copy map. The source's complete difference endpoint E(q) is still absent.

The common/raw baseline has 73,771 instructions. The two loans have73,794, adding18 ADDs,1 SCALE,2 INITs and 2 CLEARs, and changing no MOVE or MOVE rank. Both include all 800 boundary ADDs. The full word has 52 owned labels,56 lifetimes, peak43 live owned fields and zero live owned fields at exit. Every one of the 1,880 independent physical input columns is checked exactly.

## 3. Candidate census and its boundary

The separately reproducible `census.py` considers one constant raw-main donor and one nonmain role between its opening MOVE and next MOVE/INIT/CLEAR, permits intervening scalar operations, disallows debt-bearing COPY destinations and requires all non-H debt fields to be cochart at the donor's arrival. On this source it finds80 scalar-active candidates,34 passing debt closures at 19 distinct starts, plus the 354 quiet windows already known.

Even granting all 34 candidate edges simultaneously, with unlimited q payload capacity and local history, leaves the same 102 missing endpoint coefficients as the main/all-owned/all-quiet graph. The inherited46-by46 endpoint witness also survives: all2,116 source/sink exclusions remain, and its diagonal determinant is1/8. Thus the existing endpoint-only46-field lower-bound proof applies to this enlarged information graph as well. `ENDPOINT-WITNESS.json` preserves the exact predecessor certificate and its pin. This is a source-specific diagnostic for the defined class; simultaneous physical compatibility is not asserted. Intermediate correction, re-encoding, extra routes, multiple escrows and paused common calendars are outside the census.

Simply omitting common helper151's old value at 30773 and continuing the original common word creates nonzero final debts in 425 roles:373 at 127 and 52 other endpoints. Meeting the escrow only at 127 cannot automatically discharge those other debts. The separate paid paused-common loan avoids this propagation by pausing before the offending common reads and restoring the full common cut before resumption. Its two new rank 2 calls are explicit, and its larger q continuation remains open.

## 4. Physical and numerical limits

All new scalar coefficients in the two instances are ±1 or1/2. Their encodings are fixed and their arithmetic is O(V). Each shadow is a real owned V-field with explicit lifecycle. No free helper or previous input is reread at another chart. The native's legal complete-field Gaussian and owned-retirement premises remain in force.

Exact rational identity does not establish finite-precision implementation by itself. New scalar gates have bounded operator norms, while the full-word error bound must compose their local errors with the inherited transport and suffix norms. No scalar cancellation removes a precision charge. This packet supplies neither a new uniform supplier nor a complete recursive price.

## 5. Reproduction and credit

`verify.py` reconstructs the complete literal word, checks typed frame legality and COPY-zero obligations, compares every physical endpoint and every common cut row, and rejects five mutants: omitted common correction, omitted shadow assembly, wrong helper scale, wrong restoration chart and wrong q delivery. Normal and optimized Python runs produce identical receipts. `census.py` independently re-enumerates the stated candidate class and its reachability diagnostic; it is not independent mathematical review of the author.

Credit: existing source authors and @CubeJerry's persistent programme; S002 quiet-loan predecessors; S003 root for proposing active-read retiming; S003 adversarial worker for the shadow lemma, literal lowering and census. AI assistance disclosed. No new κ.
