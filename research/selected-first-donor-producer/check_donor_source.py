"""Independently authenticate C5's source witness against the retained full word.

Apache-2.0. Prepared for @CubeJerry with substantial OpenAI assistance.
"""
import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def check(archive, witness):
    raw = archive.read_bytes()
    require(len(raw) == 350722, 'archive byte length')
    require(sha256(raw).hexdigest() == '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883', 'archive digest')
    word = json.loads(gzip.decompress(raw))
    canonical = json.dumps(word, sort_keys=True, separators=(',', ':')).encode()
    require(sha256(canonical).hexdigest() == '91429a6b96729292a8764836e00c87a6f7cd3b76f05159033f4867f69a98d097', 'canonical word digest')
    require(word['public'] == witness['public'] == 1480, 'public owner boundary')
    require({str(i): word['frames'][i] for i in (3, 601)} == witness['frames'], 'actual source frames')
    require(witness['index'] == 28039 and word['program'][28039] == witness['event'], 'actual MOVE')
    require([[i, word['program'][i]] for i in range(28037, 28042)] == witness['first_contacts'], 'five consecutive source contacts')
    live = dict(enumerate(word['initial']))
    require(len(live) == word['public'], 'initial public inventory')
    for i, event in enumerate(word['program'][:28039]):
        opcode, owner = event[:2]
        if opcode == 'INIT':
            require(owner >= word['public'] and owner not in live, 'fresh owned lifetime')
            live[owner] = event[2]
        elif opcode == 'CLEAR':
            require(owner >= word['public'] and live.get(owner) == event[2], 'owned retirement frame')
            del live[owner]
        elif opcode == 'MOVE':
            require(live.get(owner) == event[2], 'current MOVE source frame')
            require(event[4] == (owner >= word['public']), 'MOVE ownership flag')
            live[owner] = event[3]
        elif opcode in ('ADD', 'COPY'):
            require(live.get(owner) == live.get(event[2]) == event[4], 'binary operand current frames')
        elif opcode == 'SCALE':
            require(live.get(owner) == event[3], 'current scalar frame')
        else:
            raise ValueError(('unknown selected opcode', i, opcode))
    require({str(i): live[i] for i in (1349, 1526)} == witness['current_frames_before_MOVE'], 'actual pre-MOVE current frames')
    require(witness['checked_prefix_events'] == 28039, 'prefix length')
    return {'status': 'PASS', 'archive_bytes': len(raw), 'archive_sha256': sha256(raw).hexdigest(),
            'canonical_sha256': sha256(canonical).hexdigest(), 'typed_prefix_events': 28039,
            'actual_contacts': witness['first_contacts'], 'actual_frames': witness['frames'],
            'current_frames_before_MOVE': witness['current_frames_before_MOVE'],
            'scope': 'Exact source authentication and chronological ownership/frame typing; no numerical execution or physical donor acquisition.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--package', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--receipt', type=Path)
    args = parser.parse_args()
    witness = json.loads((args.package/'SOURCE-EVENT.json').read_text())
    result = check(args.archive, witness)
    broken = dict(witness, frames={'3': [], '601': [239]})
    try:
        check(args.archive, broken)
    except ValueError as error:
        require(str(error) == 'actual source frames', 'specific wrong-frame negative control')
    else:
        raise ValueError('mutated source frame passed')
    result['wrong_frame_witness_rejected'] = True
    text = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if args.receipt:
        args.receipt.write_text(text)
    print(json.dumps({'status': result['status'], 'typed_prefix_events': 28039, 'wrong_frame_witness_rejected': True}, sort_keys=True))


if __name__ == '__main__':
    main()
