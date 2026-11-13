# Independent integer-power certification of the carrier943 charged budget

At kappa=19/5000, the verified interval is

    M+17(f(8)-f(1)-f(4))
      in [-8.955077952063432905843994,
          -8.955077952063432905794371] <0.

The existing budget_price.py supplies endpoint proposals only, frozen at
denominator DEN=10^24. The callable verifier imports no price engine and
performs no logarithm, exponential, binary search or endpoint-adjustment loop.
For all25 required invoice/delta ranks it directly checks

    lower^5000 <= r^4981*DEN^5000 <= upper^5000.

The positive5000th-power function is increasing, so these integer inequalities
prove the rational price brackets. Decimal is used only to display already
certified rational values. The exact f(1)=1 uses a point bracket.

CURRENT-PRICE.json is pinned by SHA256
86f71ccbc923db5d7a6753aa971c3a9c8a572680534498ed17be072cfa2aae6b,
with native payload
64fca675b91298868e12f09423b47e0c2327cba7095e35c8919c1953b4ed68b8.
The exact caller SHA256 is
255d89f38cd45e38e5770f559bc43dc217e989032359768cdc7e8cdfd64b47bc.
The executed receipt supplies that caller and directly counts its17 J events
and stages. Pinned joint invoice verification commit
509baf4514966e4202cfdde379d7adf3085b1cc7 verifies the complete invoice;
it is not source or supplier admission of unselected #7481.

M is freshly recomputed from after.T minus after.P. The task's exact native
delta is {8:+1,1:-1,4:-1}. Both the combined signed profile and the looser
separated M+17*delta interval have strictly negative upper bounds, and the
combined interval is contained in the separated one.

    M in [-59.241933884374900242189582,
          -59.241933884374900242139925]

    delta in [2.958050348959498078608562,
              2.958050348959498078608564]

Two executed mutations call the actual bracket validator. Raising rank4's
lower endpoint by one DEN unit fails its lower-power inequality; lowering
the upper endpoint fails its upper-power inequality. Neither control uses
a remembered floating value or a hard-coded numerical sign.

## Portable callable interface

`verify.verify(invoice_path, caller_path=None)` returns a deterministic
JSON-serializable receipt and writes or prints nothing. Supplying the caller
authenticates its bytes and independently counts17 invocations. Omitting it
explicitly labels that count inherited from the pinned joint invoice
verification; this optional integration mode does not claim a fresh count.

```sh
python3 -I -B research/p104-carrier943-transport-bound/independent_budget.py research/p104-carrier943-transport-bound/inputs/CURRENT-PRICE.json --caller research/p104-carrier943-transport-bound/inputs/CALLER.json
python3 -I -O -B research/p104-carrier943-transport-bound/independent_budget.py research/p104-carrier943-transport-bound/inputs/CURRENT-PRICE.json --caller research/p104-carrier943-transport-bound/inputs/CALLER.json
```

The self-contained module is bundled as independent_budget.py in this package. Static
SEEDS carry proposal provenance; PROPOSALS.json is not a runtime dependency.
Normal and optimized receipts match exactly. Callable tests with Path writes
forbidden and a copied Git-free invocation also pass.

This settles only the numerical-method/sign gate for the pinned invoice and
specified charge. Carrier delta applicability, all actual source/supplier
admission, physical return/stock, all-column behavior and other foundational
obligations remain open. No physical construction, new kappa or publication
is claimed. Prepared for Jerry Chen / CubeJerry with substantial OpenAI
assistance.

The frozen independent implementation SHA256 is `ca2811c0a20d62c37b146cc7c5a3311507589651db49adcbfc2d5c6fa6346c90`. The bundled deterministic receipt SHA256 is `7beefdf62bfb40f8ce8ae900aee0534d9d013929e893dc29e3c0a9d4cfb408ee`. This note is adapted only to use the packaged reproduction paths.
