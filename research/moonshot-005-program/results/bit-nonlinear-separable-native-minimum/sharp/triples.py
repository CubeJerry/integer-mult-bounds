"""Create and independently replay the anchored-three-donor certificate on native roots."""
import argparse
from collections import Counter
from copy import deepcopy
import gzip
from hashlib import sha256
import json
from pathlib import Path

N = 111
LAYOUT_SHA = '9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'


def need(value, message):
    if not value:
        raise ValueError(message)


def vertices(mask):
    while mask:
        unit = mask & -mask
        yield unit.bit_length() - 1
        mask ^= unit


def support(layout):
    raw = gzip.decompress(layout.read_bytes())
    need(sha256(raw).hexdigest() == LAYOUT_SHA, 'published root table')
    roots = json.loads(raw)['root_table'][:N]
    return [sum(1 << j for j, b in enumerate(roots) if sum(x*y for x,y in zip(a,b)) == 0) for a in roots]


def allowed(mask, r, s, anchors):
    need(0 <= r < s < N and len(anchors) == len(set(anchors)) == 8, 'distinct two rows and eight anchors')
    need(all(0 <= c < N for c in anchors) and r not in anchors and s not in anchors, 'exterior anchors')
    anchor_mask = sum(1 << c for c in anchors)
    need(all(not (mask[c] & anchor_mask) for c in anchors), 'eight independent true own terms')
    donors = mask[r] & mask[s] & ~(anchor_mask | 1 << r | 1 << s)
    for c in anchors:
        if (mask[r] | mask[s]) & (1 << c):
            donors &= ~mask[c]
    return donors


class Components:
    def __init__(self):
        self.rep = list(range(N))

    def root(self, v):
        while self.rep[v] != v:
            self.rep[v] = self.rep[self.rep[v]]
            v = self.rep[v]
        return v

    def join(self, r, s):
        self.rep[self.root(r)] = self.root(s)


def tree_state(mask, tree):
    need(len(tree) == len(set(tuple(e) for e in tree)) == 2*N-1, '221 distinct tree edges')
    incidence = [set() for _ in range(2*N)]
    known = [0]*N
    for r, d in tree:
        need(0 <= r < N and 0 <= d < N and mask[r] & (1 << d), 'native tree edge')
        incidence[r].add(N+d); incidence[N+d].add(r)
        known[r] |= 1 << d
    stack = [0]; seen = {0}
    while stack:
        new = incidence[stack.pop()] - seen
        stack.extend(new); seen.update(new)
    need(len(seen) == 2*N, 'native bipartite tree spans')
    return known


def construct(mask, tree, charts):
    known = tree_state(mask, tree); comp = Components(); steps = []
    for r,s,anchors in charts:
        d = allowed(mask,r,s,anchors)
        first,second = d & known[r], d & known[s]
        common = first & second
        if not common:
            continue
        pivot = next(vertices(common)); pexider = []
        if comp.root(r) != comp.root(s):
            start,available = (r,first) if first.bit_count() >= second.bit_count() else (s,second)
            if available.bit_count() < 3:
                continue
            q,t,*_ = vertices(available ^ (1 << pivot))
            pexider = [start,pivot,q,t]
            comp.join(r,s)
        elif first == second:
            continue
        steps.append([r,s,list(anchors),pivot,pexider])
        known[r] |= second; known[s] |= first
    need(known == mask, 'all native edges certified by the constructed transcript')
    return {'tree':tree,'charts':steps}


def gf2_rank(rows):
    basis = {}
    for v in rows:
        while v:
            h = v.bit_length()-1
            if h in basis:
                v ^= basis[h]
            else:
                basis[h] = v
                break
    return len(basis)


def defect(mask,tree):
    tree = set(tuple(e) for e in tree)
    r,j = next((r,j) for r in range(N) for j in vertices(mask[r]) if (r,j) not in tree)
    canonical = [z | 1 << i for i,z in enumerate(mask)]
    checks = {}
    for bits in [1,2,3,6]:
        rows = [sum(1 << (bits*k+u) for k in vertices(M)) for M in canonical for u in range(bits)]
        original = gf2_rank(rows)
        rows[bits*r] ^= 1 << (bits*j + int(bits>1))
        changed = gf2_rank(rows)
        need((original,changed) == (9*bits,9*bits+1), 'native one-rank global endpoint')
        checks[bits] = [original,changed]
    return {'perturbed_edge':[r,j],'canonical_and_changed_binary_ranks':checks,'all_proper_functions_bijective_if_bits_at_least_2':True}


def replay(mask,cert):
    known = tree_state(mask,cert['tree']); comp = Components(); joined = 0
    growth = Counter(); widths = Counter()
    for r,s,anchors,pivot,pex in cert['charts']:
        domain = allowed(mask,r,s,anchors)
        raw_r,raw_s = domain & known[r], domain & known[s]
        need(0 <= pivot < N and (raw_r & raw_s) & 1 << pivot, 'identified two-bijection graph')
        if pex:
            start,p,q,t = pex
            need(p == pivot and start in (r,s) and len({p,q,t}) == 3, 'three distinct exterior donor graphs')
            good = domain & known[start]
            need(all(0 <= a < N and good & 1 << a for a in (p,q,t)), 'three known bijections in a common first projection')
            need(comp.root(r) != comp.root(s), 'a new additive row link')
            comp.join(r,s); joined += 1
        need(comp.root(r) == comp.root(s), 'additive transition proved before subgroup propagation')
        growth[(raw_r ^ raw_s).bit_count()] += 1; widths[domain.bit_count()] += 1
        known[r] |= raw_s; known[s] |= raw_r
    need(known == mask and joined == N-1 and len({comp.root(i) for i in range(N)}) == 1, 'full native support and single additive row component')
    return {'transcript_charts':len(cert['charts']),'pexider_additive_joins':joined,'subgroup_only_charts':len(cert['charts'])-joined,'native_tree_edges':len(cert['tree']),'all_proper_edges':sum(v.bit_count() for v in known),'per_chart_new_edge_histogram':dict(growth),'native_donor_width_histogram':dict(widths)}


def main():
    p = argparse.ArgumentParser();p.add_argument('--layout',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--seeds',type=Path,help='optional old CLOSURE and WEIGHTED charts used only to seek a compact transcript');a=p.parse_args()
    mask=support(a.layout);a.out.mkdir(parents=True,exist_ok=True);cp=a.out/'THREE-COLUMNS.json.gz'
    if a.seeds:
        z=json.loads((a.seeds/'CLOSURE.json').read_bytes());w=json.loads((a.seeds/'WEIGHTED.json').read_bytes())
        charts={}
        for _,r,s,p,q,anchors,*_ in z['forced']+w['closure']:
            r,s=sorted((r,s));anchors=tuple(sorted(anchors));key=(r,s,anchors)
            if key not in charts:charts[key]=allowed(mask,r,s,anchors)
            need(all(charts[key] & 1 << c for c in (p,q)), 'actual native supplied square')
        cert=construct(mask,z['tree'],charts.keys())
        raw=(json.dumps(cert,separators=(',',':'))+'\n').encode();cp.write_bytes(gzip.compress(raw,mtime=0))
    raw=gzip.decompress(cp.read_bytes());cert=json.loads(raw);stats=replay(mask,cert)
    faults={}
    for label,mutate in [
        ('anchor_endpoint',lambda c: c['charts'][0][2].__setitem__(0,c['charts'][0][0])),
        ('three_donor_collision',lambda c:c['charts'][0][4].__setitem__(2,c['charts'][0][4][1])),
        ('unproved_additivity',lambda c:c['charts'][0].__setitem__(4,[])),
        ('substituted_pivot',lambda c:c['charts'][0].__setitem__(3,c['charts'][0][0]))
    ]:
        bad=deepcopy(cert);mutate(bad)
        try:replay(mask,bad)
        except ValueError as exc:faults[label]=str(exc)
    need(len(faults)==4,'effective targeted negative controls')
    out={'layout_uncompressed_sha256':LAYOUT_SHA,'transcript_uncompressed_sha256':sha256(raw).hexdigest(),'positive':stats,'strict_factor_two_endpoint':defect(mask,cert['tree']),'negative_controls':faults}
    (a.out/'TRIPLE-RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n');print(stats,out['strict_factor_two_endpoint'],faults)


if __name__=='__main__':main()
