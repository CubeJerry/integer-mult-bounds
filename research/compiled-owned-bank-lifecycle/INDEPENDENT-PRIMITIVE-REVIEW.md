# Independent physical primitive and boundary review

Prepared for @CubeJerry with substantial OpenAI assistance. The reviewing root
agent and the authoring lifecycle agent used separate methods. This is scoped
AI-assisted review, not human or proof-kernel acceptance.

The portable `independent_primitives.py` imports only machine.py as its subject.
Its sparse absolute-coordinate hardware, signed-word encoder, expected sums,
prefix guards and primitive action counter are separate implementations. It
imports no author Tape, fixture, encoder or expected-value function. Portability
changed only the machine path and loading of captured source bytes; the
reviewer's oracle and cases are unchanged.

Both commands executed successfully on the frozen machine SHA256
`ec597bce13275003ff30e4be481c936401826c1d4af642b55eec0c410774d1df`:

```sh
python -B research/compiled-owned-bank-lifecycle/independent_primitives.py
python -O -B research/compiled-owned-bank-lifecycle/independent_primitives.py
```

Both returned `PASS_ROOT_LIFECYCLE_PRIMITIVE_REVIEW`, with 4,095 legal signed
pairs across widths1–6, 1,365 overflow rejections, twelve canonical-zero and
physical-retirement formats, and seven exact scan-bill cases. They also check
coded logical-blank continuity, origin rejection, borrowed source preservation
and protected ancestor prefixes. The signed tests include positive and negative
extremes and compare the actual destination against an independent arithmetic
sum, so an overwrite implementation would not pass.

The root reviewer independently derived the following action counts directly
from the source loops, without using the author's invoice function:

| Operation | Local reads+writes+unit moves |
| --- | ---: |
| Transfer L binary cells | 8L+14 |
| Retire L binary cells | 5L+7 |
| Normalized Stack.push, q payloads, total parent S, PC width b | 2S+10q+7b+11 |
| Normalized Stack.pop | 2S+21q+11b+28 |
| Save / consume PC | 4b+4 / 5b+4 |

Including child retirement, both relays, the staged header and occupied owner
replacement gives

`4S+5C+18L_in+13L_out+5H+38q+27b+103`.

The author controller's formula agrees. These counts require canonical local
heads and contiguous binary bodies, with logical blanks encoded rather than
physical holes. Row service actions and leaf/top tests remain additional.
The reviewer also read the written source/lifecycle proof and found no blocking
issue in its scoped implication. Native numerical/geometry tables, row services
and the imported quantified compiler theorem remain explicit premises.
