# Independent review of the free-terminal return restriction

On the original 111 roles, the eight scaffold positions are actual own diagonals with indices 71, 4, 52, 9, 66 before the central rectangle and 13, 54, 88 after it. The center uses output roles 73, 12, 56 and donors 15, 20, 33, 34, 39, 44. Original native root inner products verify the entire strictly lower block support is zero. The eight own diagonals of $I+B$ are invertible regardless of changes to foreign entries, because the forward atlas has no proper coefficient on an own diagonal. Independent nonsingular input and output gauges preserve these zero and invertible facts.

The separate implementation in `transfer.py` forms each selected native H-port covector directly from its ordinary or confluent linear functional on the source's degree-15 coefficients. It obtains phase quotas from true owner records, inherits the paid source coordinate order and builds the relevant $8$-column D restrictions from local Cauchy coordinates. It then reconstructs K rows using the actual early and late stripe owner files and their recorded early-to-late copies. For both K choices all 36 whole physical blocks agree with the author's early and late coefficients, comparing 14,515,200 field entries. The compared arrays contain every arriving original early X and every true late Y at the three recipients.

Write $E$ for all $1{,}080$ early rows on the $2{,}880$ selected donor coordinates and $Y$ for the $1{,}440$ late rows. Every allowed local terminal choice has $W_iY_i+T_iE_i$ with $W_i$ invertible. Modulo the span of all $E$ rows, the image of the lifted late row space is unchanged by these choices. Hence the central rank is at least $\operatorname{rank}([E;Y])-\operatorname{rank}(E)$. This argument even allows arbitrary cross-recipient early row additions, strengthening its applicability to the legitimate local terminal choices. Unrestricted invertible donor gauges preserve the common right-multiplication rank calculation.

`rank.cpp` uses an independent polynomial GF(64) implementation, eliminates from the rightmost column, and caches all nonzero multiples of each pivot vector. For both physical K words the ranks are 1,035 and 2,430, giving a central lower bound of 1,395. Reversing the native field column order preserves the result. Independent eight-copy replication scales these ranks by eight, also with subsequent gauge or terminal mixing across the copies. Upper block triangularity now gives a return rank of at least $8(8\cdot480+1395)=41{,}880$. Excess over nine complete banks is at least 7,320. This restriction is specific to the tested upstream coefficients through K. It does not require keeping any foreign block invertible or keeping the originally proposed F.

Generate the physical preterminal arrays directly in a scratch directory and compare their aggregate hashes with the independent author output. An optional `--compare-arrays` on the first command compares every array entry when a prior producer has supplied the 36 arrays. Run:

```sh
python -B transfer.py --repo REPO --d-words D_OUTPUT --k-words K_OUTPUT --arrays-out ARRAYS --out OUT
python -B check.py --repo REPO --arrays ARRAYS --author-result AUTHOR_OUTPUT/RESULT.json --out OUT
```

Credit the native atlas, spread RS source, minimum D words, both K constructions, and the native return-obstruction author. Independently reviewed with substantial OpenAI assistance.
