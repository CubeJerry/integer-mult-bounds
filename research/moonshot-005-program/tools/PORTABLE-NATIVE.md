# Portable access to the pinned native

S005 lost its shell environment at approximately 2026-11-11 15:13 UTC.
The GitHub connection and JavaScript execution tool remained available.
These small CommonJS modules permit exact source loading without shell,
network calls from JavaScript, or filesystem access inside that tool.
They are recovery infrastructure, not a new mathematical theorem.

Fetch the native using the connected GitHub file reader with base64 encoding
at a verified programme commit. Decode with base64Bytes, check compressed
SHA256, inflate using the vendored tiny-inflate export through gunzipPinned,
and parse asciiText of the returned bytes. The pinned native JSON is ASCII.
The gzip wrapper checks the header, exact length and CRC32; its output-size
limit is 100 MB. Only the already authenticated native is used as input.

Pinned native compressed SHA256:
2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883
Git blob:74563a7867d9d762b6588f65362369668841bb3e
Compressed bytes:350722; decompressed bytes:1857439.
The recovered word has1480 public inputs,71261 instructions and1095 frame
labels (1094 distinct chart spaces, as separately established).

The SHA256 implementation was checked against the empty-string and abc test
vectors and the existing independently authenticated native digest. The
recovered word was parsed and its source counts checked. No source identity
was admitted merely by loading it.

Third-party decompressor: foliojs/tiny-inflate, index.js Git blob
44d1151b21f9a2a70dbc261dc7df6f2d14bc06d5, fetched from its official repository.
The source is vendored unchanged, with its MIT license and credit to Devon
Govett. The license Git blob is6291454829be6a266438f11110e7656581683f0c.
Native compressed bytes are not duplicated here.
