"""Independent finite source geometry check; no Clifford compiler imported."""
from pathlib import Path
import collections
import gzip
import hashlib
import json
import subprocess
import sys

BASE = 'e54523517d0f03e58352e647c403a5af3e525a57'
PATH = 'research/shared-wire-split-composition/data/final.json.gz'
HASH = '2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
EXPECTED = {'1':4075,'2':828,'3':811,'4':241,'5':320,'6':17,'7':12,'8':6}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    repo = Path(sys.argv[1]).resolve()
    raw = subprocess.check_output(['git','-C',str(repo),'show',BASE+':'+PATH])
    require(hashlib.sha256(raw).hexdigest()==HASH,'canonical source bytes')
    word = json.loads(gzip.decompress(raw))
    spans = []
    for frame in word['frames']:
        span = {0}
        for direction in frame:
            require(direction not in span,'independent source frame directions')
            span |= {point ^ direction for point in tuple(span)}
        spans.append(span)
    histogram = collections.Counter()
    pairs = set()
    total = 0
    for event in word['program']:
        if event[0] != 'MOVE':
            continue
        source, target = event[2:4]
        pairs.add((source,target))
        left,right = spans[source],spans[target]
        require(left < right or right < left,'proper nested source subspaces')
        histogram[str(abs(len(left).bit_length()-len(right).bit_length()))] += 1
        total += 1
    require(total==6310 and len(pairs)==2971 and dict(histogram)==EXPECTED,
            'exact source counts and dimension differences')
    print(json.dumps({'status':'PASS_ROOT_SOURCE_NESTED_MOVE_CENSUS','base':BASE,
        'path':PATH,'archive_sha256':HASH,'MOVE_events':total,
        'distinct_ordered_pairs':len(pairs),'nested_events':total,
        'non_nested_events':[], 'dimension_difference_histogram':dict(sorted(histogram.items())),
        'scope':'Independent explicit binary span-set geometry; no Clifford compiler import and no physical or tariff claim.'},indent=2))

if __name__=='__main__':main()
