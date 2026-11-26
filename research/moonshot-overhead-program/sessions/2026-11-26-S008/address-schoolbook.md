# Exact worst-case time of the raw 19-state multiplier

For the [fixed five-tape program](schoolbook.py), let $x,y$ be the immutable raw $n$-bit operands. Define $c_j=1$ when $x(y\bmod 2^{j+1})\ge 2^{n+j}$, and zero otherwise. The full external-interface transition count is
$$
T(n,x,y)=10n+8+(4n+4)\operatorname{popcount}(y)+\sum_{j=0}^{n-1}c_j.
$$
Consequently its sharp worst case is $4n^2+15n+7$, attained at $x=y=2^n-1$, and the exact cumulative visited space on every input is $8n+9$. These counts concern the raw program; a surrounding dispatcher has its independent charge.

Initialization takes $4n+5$ transitions. These comprise the start, two $n+1$-transition operand copies, a $2n+1$-transition return to the accumulator left delimiter, and setting the low mark. At multiplier step $j$, its accumulator value is $x(y\bmod 2^j)<2^{n+j}$. The written $n$-bit window ends exactly below position $n+j$, whose pre-step digit is zero. Thus an outgoing carry either occurs once, setting this digit in one transition, or costs no propagation transition. Its occurrence is precisely $c_j=1$.

A zero multiplier digit takes three transitions. For a one digit, the initial branch takes one, the two-bit tests take $2n$, the multiplicand left delimiter takes one, any outward carry costs $c_j$, returning to the accumulator mark costs $n+1$, and restoring the multiplicand costs $n+2$. Shifting and reaffirming the mark take two more. Each one digit therefore costs $4n+7+c_j$. The closing scan from the final mark and the raw high-to-low output consume $3n+3$. This sums to the displayed identity. Since $c_0=0$, the upper bound follows. On all-one operands each $j\ge1$ has $(2^n-1)(2^{j+1}-1)-2^{n+j}=2^{n+j}-2^n-2^{j+1}+1\ge1$, proving attainment.

The raw input head visits $2n+2$ cells, each operand-copy head $n+2$, the accumulator $2n+2$, and the output head $2n+1$ including its final position. The [independent table interpreter](address-schoolbook.py) verified the formula, physical space and full product for all two-operand inputs through six bits and selected wider inputs.

Prepared for Jerry Chen (@CubeJerry) with substantial ChatGPT research assistance.
