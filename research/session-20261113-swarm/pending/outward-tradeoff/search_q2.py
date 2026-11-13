"""Bounded complete-ball injection search, not a global rounding construction."""
from collections import deque
from itertools import product
import json
import sys

H = ((1,1,1,1),(1,-1,1,-1),(1,1,-1,-1),(1,-1,-1,1))


def need(ok, why):
    if not ok:
        raise ValueError(why)


def norm2(x):
    return sum(t*t for t in x)


def allowed_growth(a, b):
    # Exact sqrt(a)-sqrt(b) <= sqrt(10)-3. For positive growth,
    # two legal squarings reduce this to A+B sqrt(10) <= 0.
    if a <= b:
        return True
    d = a-b
    aa = (d-19)**2+360-76*b
    bb = 12*(a+b-19)
    if bb == 0:
        return aa <= 0
    if bb > 0:
        return aa < 0 and aa*aa >= 10*bb*bb
    return aa <= 0 or aa*aa <= 10*bb*bb


def candidates(x):
    z = tuple(sum(a*b for a,b in zip(r,x)) for r in H)
    if z[0] % 2:
        ys = product(*((a//2, a//2+1) for a in z))
    else:
        base = tuple(a//2 for a in z)
        ys = [base] + [tuple(a+(delta if i==j else 0) for i,a in enumerate(base))
                       for j in range(4) for delta in (-1,1)]
    out = []
    for y in ys:
        need(sum((2*a-b)**2 for a,b in zip(y,z)) <= 4, 'error enumeration')
        if allowed_growth(norm2(y), norm2(x)):
            out.append(y)
    return out


def matching(xs, edges):
    # Iterative augmenting BFS. Every operation is finite on the declared graph.
    target_owner = {}
    chosen = {}
    failure = None
    for root in xs:
        queue = deque([root])
        parent = {root: None}
        via = {}
        seen_y = set()
        end = None
        while queue and end is None:
            x = queue.popleft()
            for y in edges[x]:
                if y in seen_y:
                    continue
                seen_y.add(y)
                if y not in target_owner:
                    end = (x,y)
                    break
                other = target_owner[y]
                if other not in parent:
                    parent[other] = x
                    via[other] = y
                    queue.append(other)
        if end is None:
            failure = {'input_set': list(parent), 'output_neighbors': list(seen_y)}
            need(len(seen_y) < len(parent), 'Hall separator sizes')
            break
        x,y = end
        while True:
            target_owner[y] = x
            chosen[x] = y
            if parent[x] is None:
                break
            y,x = via[x],parent[x]
    return chosen, failure


def main():
    radius = int(sys.argv[1]) if len(sys.argv)>1 else 3
    need(1 <= radius <= 6, 'declared preflight radius cap')
    xs = [x for x in product(range(-radius,radius+1),repeat=4) if norm2(x)<=radius*radius]
    edges = {x:candidates(x) for x in xs}
    chosen, failure = matching(xs, edges)
    need(len(set(chosen.values())) == len(chosen), 'injection')
    for x,y in chosen.items():
        need(y in edges[x], 'chosen edge')
    receipt = dict(radius=radius, inputs=len(xs), edges=sum(map(len,edges.values())),
                   matched=len(chosen), complete=len(chosen)==len(xs),
                   error_bound_squared=1, outward_threshold='sqrt(10)-3',
                   scope='complete finite S_radius only; no global map or asymptotic claim',
                   matching=[[list(x),list(y)] for x,y in chosen.items()], hall=failure)
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':
    main()
