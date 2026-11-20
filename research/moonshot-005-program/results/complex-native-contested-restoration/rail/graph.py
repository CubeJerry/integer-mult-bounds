"""Read the pinned paid rational word and its complete caller receipt."""
from collections import Counter, defaultdict
from fractions import Fraction
from functools import cache
from hashlib import sha256
from pathlib import Path
import gzip
import json

ROOT = Path(__file__).resolve().parent
WORD = '7660985e0b618cdbee13e4190a4c6d5f91fbdf01a8f7a5186fdde8b980c19b48'
APPLICATION = '1b2d87e93ae023f5ffd464546af53281b6cb4963dfd76ae4742e0a5540b752fa'


def require(condition, label):
    if not condition:
        raise ValueError(label)


def read(name, digest):
    data = gzip.decompress((ROOT/'sources'/name).read_bytes())
    require(sha256(data).hexdigest() == digest, 'pinned source '+name)
    return json.loads(data)


@cache
def rational(literal):
    return Fraction(literal)


def get_histogram(raw):
    return Counter({int(r):n for r,n in raw.items()})


class Graph:
    def __init__(self):
        data = read('DOUBLE-CANDIDATE.json.gz', WORD)
        self.receipt = read('DOUBLE-APPLICATION.json.gz', APPLICATION)
        require(self.receipt['word_sha256'] == WORD, 'receipt binds word')
        self.moves = {e:(a,b) for e,a,b in data['moves']}
        self.forms = {}
        for f,terms in data['forms']:
            row = {e:rational(q) for e,q in terms if rational(q)}
            require(len(row) == len(terms), 'zero or duplicate incidence')
            self.forms[f] = row
        self.schedule = data['schedule']
        self.initial = data['initial']
        self.final = data['final']
        self.first_output = data['first_output']
        self.frames = data['frames']
        self.dimension = [len(basis) for basis in self.frames]
        self.incoming = defaultdict(list)
        self.outgoing = defaultdict(list)
        for j,b in enumerate(self.initial):
            self.incoming[b].append(~j)
        for j,b in enumerate(self.final):
            self.outgoing[b].append(self.first_output+j)
        for e,(a,b) in self.moves.items():
            self.outgoing[a].append(e)
            self.incoming[b].append(e)
        require(set(self.schedule) == set(self.forms) and len(self.schedule)==len(self.forms), 'complete schedule')
        require(len(self.initial)==len(self.final)==1289 and len(self.moves)==5707, 'source shape')
        ready = {~j for j in range(len(self.initial))}
        for e in self.schedule:
            send = self.moves[e][0] if e in self.moves else self.final[e-self.first_output]
            require(set(self.forms[e]) <= set(self.incoming[send]) & ready, 'stock ownership or causality')
            ready.add(e)
        spans = []
        for basis in self.frames:
            sector = {0}
            for x in basis:
                sector |= {v^x for v in sector}
            require(len(sector) == 2**len(basis), 'frame basis')
            spans.append(sector)
        self.rank = {}
        self.sign = {}
        for e,(a,b) in self.moves.items():
            nested = (spans[a] < spans[b]) or (spans[b] < spans[a])
            require(nested, 'non-positive or nonnested paid move')
            self.rank[e] = abs(self.dimension[b]-self.dimension[a])
            self.sign[e] = 1 if self.dimension[b]>self.dimension[a] else -1
        self.native = get_histogram(self.receipt['native']['paid_native_ranks'])
        require(Counter(self.rank.values()) == self.native, 'source native invoice')
        self.helpers = get_histogram(self.receipt['native']['positive_helper_ranks'])
        census = self.receipt['caller_census']
        self.calls = census['calls']
        self.fixed_paid = get_histogram(census['fixed_caller_paid'])
        self.fixed_root = get_histogram(census['fixed_root_targets'])
        require(self.calls==48, 'whole caller count')
