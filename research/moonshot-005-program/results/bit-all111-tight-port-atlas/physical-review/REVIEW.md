# Independent arbitrary-input audit of the all-111 base port schedule

The SHA-256 `b6ab5630c5b90f1be4ab07cb1a9ac2f09c13524c0aea6e70028a8023b68f2bef` binary stream realizes the published partial all-111 map on all **319,680** input columns. The normalized movement uses 1,440 genuine binary native copies. The required foreign rank is 240 over GF64 at each of 6,470 ordered pairs, while 40 transfer blocks are zero and the largest has rank 23. No complete supplier or new κ follows.

## Independent oracle and geometric checks

The review consumes only the original 111 root tuples, the frozen decompressed atlas `9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72`, and the raw little-endian binary operations. The author emitter regenerates the frozen bytes. The subsequent target oracle and interpreter use separate implementations and import no author geometry, eliminator or simulation.

For each original receiver $i$, stripe $t$, and coordinate $p=0,\ldots,15$, the independently predicted output over $\mathbf F_{64}=\mathbf F_2[x]/(x^6+x+1)$ is

\[
Y_{i,t,p}+\sum_{j:\,j=i\text{ or }R_i\perp R_j} X_{j,t,p}
 +\sum_{(j,s,\alpha,t,\beta)\to i}\beta^p\sum_{q=0}^{15}\alpha^q X_{j,s,q}.
\]

The last sum comes from pure X routes ending at the receiver, a Y reading the source evaluation at its initial native line, or a Y beginning in the middle directly from ground and reading its actual predecessor's X snapshot at that $D_4$. A route lacking all three supplies no term. For the middle handoff, both routes must share the same $D_4$ and the predecessor must terminate its middle sequence there. There are exactly 2,880 such symbol reads, hence 17,280 binary handoffs. The two Vandermonde vector families for each ordered $(i,j)$ are separately independent because within each stripe all associated nodes are distinct and number at most 16. Distinct stripes lie in disjoint summands. Thus its rectangular transfer has rank equal to the number of its terms. The sum of individual ranks is 42,840. The complete histogram is in `GEOMETRY.json`. This sum counts individual ranks only.

The geometric checker uses rational elimination on the supplied root bases and checks double orthogonality for every three-root $A_2$ and twelve-root $D_4$ set. It checks ranks two, four, six and seven for the primal and dual sites, verifies every dual middle assignment and reconstructs each path by strict containment of complete root sets. Every indexed incoming and outgoing $A_2$–$D_4$ port occurs once on its respective side. A separate opcode reader validates each actual MOVE against the 112,189 allowed arcs including the canonical descent, the live co-location of both ADD operands, chronological owner births, final retirements and every original's charts. There are 799,200 rank-one, 650,160 rank-two, 34,560 rank-four and 12,960 rank-eight movements.

## Exhaustive linear comparison

`replay.cpp` interprets every actual ADD. For each of the 111 X-source roles it propagates all 1,440 independent original coordinates at once as bitsets and compares every terminal field against the oracle. A prior full-stream provenance audit proves that no operation merges Y data from two different roles. A simultaneous 1,440-coordinate Y basis comparison for each disjoint role therefore covers all 159,840 independent Y columns. The checker compares all public fields with their raw arbitrary inputs when X is restored at Hub and checks all 12,960 canonical binary records on their complete original-column bases. Every one of 714,960 CLEARs retires a symbol nonzero on at least one original input basis vector. Omitting the first actual prepositioned-X binary read at $D_4$ leaves a co-located legal word whose endpoint disagrees in 40 rows on its witnessing full source-role basis.

The fixed schedule lifts by tensoring its coefficient rows with the identity on any allowed common record volume. This finite coefficient audit leaves the full 240-rank foreign target, the recursive supplier and the physical foundations open. The tested six-bit GF64 word uses 1,440 binary copies.

## Reproduction

```sh
python3 -B "$PHYSICAL_AUTHOR/physical.py" --native "$NATIVE" --layout "$LAYOUT" --out "$TMP/author" --word "$TMP/native.bin"
sha256sum "$TMP/native.bin"
python3 -B geometry.py --native "$NATIVE" --layout "$LAYOUT" --out "$TMP/tables"
c++ -O3 -std=c++17 replay.cpp -o "$TMP/independent-replay"
"$TMP/independent-replay" "$TMP/native.bin" "$TMP/tables" -1 111
```

The raw stream is generated from the pinned original-root file and compressed base atlas. It occupies 397,166,688 bytes. Expected receipts are `GEOMETRY.json` and `ARBITRARY-INPUT.json`. This independent audit was developed by S022 Worker C with OpenAI assistance for @CubeJerry and credits the physical and atlas authors for the construction.
