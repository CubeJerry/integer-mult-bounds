# Two genuine proper births remove empty rank-two descents

**Status: proved formal-source construction. Same41 endpoints; no new complete κ.**

The endpoint-reduced predecessor `b18c138efaf2d771197c46ef3ae2a5fc312c322694ef020e41cace70d7662e11` creates P6 and P7 atHub even though dead-code removal has left both packets identically zero until their first proper-chart reads. Their first three uses are exactly:

    INIT P6 Hub; MOVE P6 Extra6; ADD EXTRA_AFF P6,
    INIT P7 Hub; MOVE P7 D3_21; ADD AFF0 P7.

Extra6 andD3_21 have real rank6, whileHub has rank8. Neither packet is read, modified, retained, or otherwise used between its birth and that first MOVE. Initialize P6 directly atExtra6 andP7 directly atD3_21, and delete just those two empty MOVEs. All other operations and their order remain unchanged.

## General zero-birth lemma

If an owned whole record is born zero atC, its only uses before its first ADD are legal nested MOVEs toD, and no earlier operation reads it, then it can instead be born zero atD. Delete those prefix MOVEs. At the first ADD, both words have identical coefficient values and locations for every live record. Their suffixes are then identical. The INIT and final CLEAR remain charged, owner names remain unique, and the actual birth chart is explicitly changed. The lemma does not move nonzero information for free.

This proof holds for every input assignment, every characteristic-two field and every positive whole-record width. In the current two instances each zero prefix is one rank-two MOVE. The exact all222-column replay checks the hypotheses and the entire resulting word. Two negative controls replace the proper birth by an inaccessible ground birth; each fails the first actual cocharted read.

The resulting word is `6c76a836322483cc11888ae214379a27adbb8f638ac3a049584f75953c5185a9`. It has118 INIT,798 ADD,450 MOVE,118 dirty CLEAR and the same41 restored-input endpoints. Its full movement histogram is

    125[1]+66[2]+61[3]+9[4]+73[5]+24[6]+92[7].

The exact saving is2[2]. At exponent199/200, independent exact integer-root arithmetic gives

    saving = 3.98616105131147133691592897415…,
    Q = 1616.84697975268954209642330769582…,
    necessary limiting room = 4.90390045846281314982284267117… .

All ordinary operations, proper owner births, erasure applicability, precision, compilation and complete recursive costs remain obligations. This is a concrete change of source architecture from eight Hub-born principals to six Hub-born principals and two proper-born principals; it is not an assumption that every counted incoming lifetime starts atHub.

## Source interface and further zero states

The source remains an endpoint-only variant. Earlier source-cut, history, common-code and fixed-closure certificates are not inherited from the discarded stage metadata. A fresh inventory/closure audit is needed before reusing an intermediate value. The two removed states were zero, but the preceding endpoint reduction had already removed substantive unused histories.

An exact scan of every owned MOVE in the reduced predecessor found only the two zero-valued movements above. There are no further identically zero reset-to-MOVE intervals in that word to replace by retirement/rebirth epochs. Such a transformation would require fresh owner names and explicit INIT/CLEAR costs; no nonzero state may be relocated by renaming an owner.

Reproduction:

```bash
python build.py --repo /path/to/programme \
  --base /path/to/reduced41/WORD.json \
  --engine /path/to/leaf-capacity-gate/check.py \
  --price-engine /path/to/review36/check.py \
  --out /tmp/proper-birth41
```

This construction was developed by `/root/delivery_audit` from the root's endpoint reduction, with substantial OpenAI assistance, in @CubeJerry's continuing programme. The native source and all prior builders retain their attribution. Independent root review is separate. Complete all111 delivery, strict suppliers and all five foundations remain open.
