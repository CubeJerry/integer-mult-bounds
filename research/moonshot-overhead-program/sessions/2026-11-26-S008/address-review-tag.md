# Exact physical count and signed decoding of comparison tags

For $p,t,g,s,h\ge1$ the [compiled tag machine](node-tapes.py) takes $q=pt^2gs$ independent records of $h$ bits. Write $V=qh$, $W=q(h+2)$, $D=(t,g,s,h)$, and let $b(n)$ and $w(n)$ be the length and popcount of a positive binary numeral. In either tag direction its exact cost and number of distinct visited cells are

$$
\begin{aligned}
T={}&\sum_{n\in D} C(n)+q(4h+10)
  +p(6gt^2+6gt+t^2+8t+2)+2\sum_{n\in D}n+22,\\
C(n)={}&11n-6w(n)+12b(n)+3,\\
S={}&V+W+\sum_{n\in D}(b(n)+n)+\max D+22 .
\end{aligned}
$$

The sums count the four descriptor slots with multiplicity. Consequently **$T\le147V$ and $S\le35V$**, with equality in both bounds for the one-bit input $p=t=g=s=h=1$. The short physical count applies to either sign, independent of the payload.

## Recount from the instruction table

The [independent interpreter's original unary recount](recount-node.md) gives $C(n)$ for materializing a canonical binary descriptor, $2h+3$ for the complete copied run and $3s+3$ for a loop of length $s$ beyond its bodies. The tag program then writes the high trit bit followed by the low bit in two transitions. One later-coordinate position consumes $s(2h+8)+3$ steps for its records. The position test and advance add two more. The final blank dispatch and the threshold tape rewind give a complete later-coordinate fibre of
\[
 t s(2h+8)+6t+3 .
\]
The loop over $g$, its $g$ fibre calls and the earlier-position dispatch cost $gts(2h+8)+6gt+6g+4$ per earlier position before the marker update.

At position $x<t-1$, search $x$ cells to the marker, move it one cell right and return to the first position. This uses $2x+5$ steps. At $x=t-1$ the machine instead detects the terminal blank, rewinds, and writes the initial marker for the next prefix. This takes $2t+4$ steps, one more than the ordinary formula at the last position. Across a complete prefix the threshold updates thus use $t^2+4t+1$. The per-prefix test, and its final terminal test after all $p$ prefixes, close the data loop. The input and output rewinds cost $V+W+4$. Erasing four unary descriptors costs $2\sum D+12$. Opening and closing the markers, initial marker installation and the terminal prefix test account for the remaining six constant steps in the displayed total.

All 11 heads touch the temporary marker at $-1$. The input and output reach their terminal blanks. The four binary descriptors and four unary descriptors reach their respective right ends. The common conversion work tape reaches the maximum completed numeral in $D$, since every intermediate binary prefix is no larger than its final value. This proves the exact space formula for the sum of all head intervals. For $n\ge1$, $C(n)\le22n$ by $b(1)=1$, $b(n)\le n/2+1$ for $n\ge2$, and $w(n)\ge1$. If $V\ge2$, each member of $D$ is at most $V$, $q(4h+10)\le14V$, the remaining prefix terms cost at most $23V$, and $22\le11V$. These estimates give $T\le144V$ and $S\le24V$ in this range. For $V=1$ the exact formulas give 147 and 35.

## Joining successive comparisons to the finite repair

On pass $j$, regard all dimensions before the earlier chosen coordinate as its prefix, all intervening dimensions as $g$, and all dimensions beyond the later coordinate as $s$ **scalar records**. The field-coordinate and existing tag bits belong to the $h$-bit record. If raw field width is $b$, then $h=b+2(j-1)$, independently of how many earlier and later main fields have been crossed. Within a record the output is its unmodified input followed by the two-bit unsigned code for $0,1,2$ at equality, earlier less than later, and earlier greater than later, respectively. The inverse-direction table negates the trit modulo three once. Thus error and predictor formulas can decode each tag pair as twice its first bit plus its second. The raw scalar prefix retains the caller's existing field encoding.

For a selected role with $Q$ raw records and $m$ comparison pairs, the $m$ tag executions cost at most $147Qm(b+m-1)$ transitions. This is the sum of the actual growing input volumes. The shapes of the two positions change at every pass. Two raw banks can alternate as argument/result. On reusing an older result as destination, the new word is strictly longer than its predecessor and overwrites the entire old range. The input is retained by each pass. Prefix, comparison and suffix extents in canonical binary are required at the routine entry. The enclosing operation also supplies an empty or shorter initial destination, returns or clears the last tagged role and charges the spectral table on each decoded record. The [finite spectral coefficient program](compiler-spectral.md) specifies that calculation.

The [composition replay](address-review-tag.py) used the independent interpreter of the prior role/direct recount and the original compiled tag table. It matched every final cell and the exact halt transition. It included 298 single-array executions and 16 signed, two- or three-coordinate compositions with occupied intervening indices, unequal raw scalar widths, unit axes and reused output buffers. The 6,732 full resulting keys matched a coordinate oracle and every tested ternary shift sum on 598,248 transitions. The signs were also mixed across passes to make a mistaken second negation observable. These finite executions and the general instructions above check the tag-to-spectral-record dependency. The actual field arithmetic and the full native node have their own separate clocks.

Run `python3 -B address-review-tag.py` in this session directory. The review used a separately derived exact clock and the [independent table evaluator](recount-node.py); the original tag builder and finite-field caller retain their own attribution.
