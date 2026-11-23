# Read-only cross-review of existing binary owner capacity

**Accepted within the existing successful-call, one-bank scope. No new
custody or capacity blocker was found.** This is a complementary review of
concurrent work already carrying separate census, capacity and application
reviews. It is not a new theorem, a replacement author package, or a claim
of priority for its construction. No file in that concurrent workspace was
modified. Prepared for Jerry Chen with substantial OpenAI assistance;
this is model-assisted review, not human or proof-kernel certification.

## Exact provenance and publication status

The existing publication manifest is
`/tmp/research-20261123-5ec7193af3d0-cache/publication-manifests/storage-final/meta.json`,
SHA256 `dd801459cb89b032d06d4c8c4086168117bd413440dcd21833ccc11e684e3637`.
It declares local head `4795bc7d967e0fa60c136d8f7845d4cacafe153a` and full
tree `94232376e370feeefd6295852a38f4ab6cf3d33e`, based on public #8091 head
`9b8a622686654e7a77ff2598fea7ff6db81c1ed0`, tree
`5399ef7377a7eaf529f6df470da4d6d8f440c777`.
The API still reported that predecessor head when checked at approximately
10:55 UTC. Local acceptance is not being relabelled as observed publication.

**Subsequent publication observation.** The coordinating reviewer has now
verified public head `b500f72bbcf9c03a7f7fd40b366eedd6d1dd285b`, parent
`9b8a622686654e7a77ff2598fea7ff6db81c1ed0`, with final tree
`02ba12cfeaa324b9b002806f0bbcb3103e3a5808`. The published census proof,
capacity corollary and storage application exactly match the reviewed
scientific texts. The final metadata tree differs from the earlier
manifest's `94232376...` tree; this review makes no full-tree equality
claim between those snapshots. Its scientific hash bindings are unchanged.

The original scientific files were subsequently located at
`/workspace/scratch/5ec7193af3d0/work-binary-owner-census/PROOF.md` and
`COROLLARY.md`; their independent reviews are in the sibling
`work-binary-owner-review/` and `work-binary-capacity-review/` directories.
All four file hashes independently match the fragments listed below.

Its files are serialized as JSON string fragments. The relevant paths and
verified hashes are:

| Existing package file | Fragment | SHA256 |
|---|---:|---|
| binary-census/PROOF.md | 14 | `672289a9a52ffdc710b4ff037c03c7149097fb99a9083ba9da62021edc77c97f` |
| binary-census/COROLLARY.md | 9 | `0170a085fb126ae4e2ab556cd41a446241e42bf9f602aac5418ae5b6a87d16f3` |
| binary-census/review/CROSS-REVIEW.md | 31 | `a9c1a7116946e388e6cf43afe1c6ea20cc25f9f9dc2cd666fa65f736aceea47a` |
| binary-census/capacity-review/CROSS-REVIEW.md | 19 | `f7f2d76d68800637f2ec3e8e638b81d8b6861fcd55b9a3e3eaf1ff857a84d400` |

All four were read in full. The separate application review and final
assumption map were also read. Source construction and interpreters remain
credited to Ali Romman's #8042 at
`dfd25d553a843a946ca0b94130a5ff8943e98fdd`; the existing census authors,
numerical proof and separate reviewers retain their attribution.

## Literal allocations and origin custody

The six inspected resolved files are raw_binary.py, strong_binary.py,
binary_receiver.py, raw_binary_stage.py, receiver.py and transport.py.
Their bytes and lengths match the concurrent SOURCE-BINDINGS manifest.
The compressed graph and caller were independently authenticated by both
Git blob identity and SHA256, decoded, and compared with the manifest's
canonical decoded JSON. No author checker was imported.

The literal Job.select helper was also read in periodic.py, SHA256
`6233e1806d29bd386ce39fab398fee4f6b73b11d4bdc1e3608bcccde15d71b19`.
It returns Job(self.owner, selected_axes), preserving the owner identity.
This matches the additional binding in the existing application review.

An independent register scan reproduces 18,906 target bindings, 104,904
paid resumes, 3,433 simultaneous private registers and the owner coefficient
18,906+max(3,433,1)=22,339. Private INIT and CLEAR are balanced, every
referenced register is live, and the final set is the original public set.
The private peak occurs at instruction 35,534, after the last MOVE at 29,029.
Counting only paid cuts would report 2,803 and would be insufficient.

The source allocation cases agree with the proof:

- Initial productive fields contribute B owners throughout Plan.run.
- Each decoder input binding creates at most one zero owner. Borrowed
  pending jobs and external selected rows alias existing owners.
- An inner INIT creates one private owner; CLEAR retires that owner.
  MOVE selects an existing register owner. Routes, ADD and SWAP use
  work tapes and modify existing owners.
- An outer QUERY owns at most one clone at a time. Its clone is retired
  after the yielded loan returns and before the next port. QUERY and
  LOCAL are serial branches, so their extra-owner bounds take a maximum.
- Machine.leaf uses only banks.start and banks.install on this allocator.
  The issued-leaf output is a separately charged named page. There is no
  additional replacement OwnerBanks slot hidden in paid execution.

The actual decoder call surface consists of zero, native, leaf and
retire_zero. Selected loans retain their allocation-origin charge even
when forwarded through several contexts. The proof does not equate
registration in the live dictionary with physical lifetime.

In particular, opening zeros are allocated before live[ident] is inserted.
Closing removes the context from that dictionary before resuming its
native tail and retiring the input zeros. The inclusive origin interval
[birth,birth+q*delay] includes both transients and the late private peak.
Its count is at most count[e]*(q*delay[e]+1) per band. This is the correct
quantity C_* for the bound, including between paid events.

## Return ordering, recursion and capacity

The source only accepts descending-delay links. Delays are powers of one
base D0>=q, hence q*D_child<=D_parent. A child born on the issue tick closes
before the parent's next resume. Closing rows precede paid/open rows; in
the equality case, ascending-band closes place the smaller-band child
before its parent. Descending-band paid/open processing collects a newly
issued loan on the same tick. Induction over the finite descending bands
covers forwarded ancestor owners, including the final paid loan.

Local leaf recursion may create other bank instances. It receives stream
and page arguments, not the outer private OwnerBanks object. Those other
banks and suspended ancestors require the existing composition theorem;
the reviewed census does not discard their storage or include them in
the count for this one allocator.

The free-first allocation argument is correct at completed allocator
calls. It is also correctly qualified at intermediate statements:
capacity increments before live.add, and live.remove precedes the free
list append. The proof charges the prospective/departing owner to its
current origin context, rather than asserting a false partition at every
statement. A fresh logical bank does not reset a reused physical head's
historical reservation; the stated max(K0,V_field*capacity) boundary remains.

## Production arithmetic and exact limits

The existing corollary imports the accepted numerical enclosure at the
same transport.py hash. With N=2^h, B=N^92 and the literal binary parameters,
it obtains sum(count)<2N^6. Independently recomputing the exact integer
comparison verifies 6^76>2^19*5^76. The source level invariant therefore
gives delay<N^76, and the inclusive q*delay+1 term is below N^77 for
h>=1024. Thus C_*<2N^83. Since 22,339<2^15 and 2^16<N^9 already at the
least Recipe height, B+22,339*C_*<2B. Actual binary dispatch requires
h>=3000, so this application stays within the arithmetic domain.

The pre-existing independent capacity review supplies the fuller literal
production-grade and inherited ambient bindings. This cross-review does
not claim to re-extract every nested dependency archive or to provide a
new numerical enclosure oracle. Its additional exact checks are recorded
in EVIDENCE.json.

The acceptance retains successful source execution, custody, valid
funding, source return and zero/erasure semantics. It concerns one fresh
bank's owner capacity. The existing application and composition proofs
must still account for field byte volume, recursive banks and warm
physical histories. Header/control representation, other physical roles,
outer allocation, movement, source admission and caller-specific analytic
recovery remain separately scoped. No canonical assumption or kappa is
changed by this review.

The proposed new coarse binary-count branch is superseded by this exact,
already reviewed concurrent result. Preserve and credit the existing
package rather than publishing another census with duplicate novelty.
