#!/usr/bin/env python3
"""Reconstruct both scalar port gates from raw native incidences.

Uses only the retained S030 independent field/root primitives, not either
new feedback-gate executable. Literal duals are authenticated against freshly
formed matrices; ranks and polynomial kernels are reconstructed separately.
"""
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
import gzip
import hashlib
import importlib.util
import itertools
import json
import numpy as np


def need(ok, why):
    if not ok:
        raise ValueError(why)


ap = ArgumentParser()
ap.add_argument('--repo', type=Path, required=True)
ap.add_argument('--out', type=Path, required=True)
args = ap.parse_args()
here = Path(__file__).resolve().parent
base = args.repo/'research/moonshot-005-program/results'
for p, digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
    need(hashlib.sha256((args.repo/p).read_bytes()).hexdigest() == digest, 'source pin '+p)
spec = importlib.util.spec_from_file_location('old_independent', base/'bit-coupled-native-geometric-cycle-source/review-c/check.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
L = json.loads(gzip.decompress((base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz').read_bytes()))
B = json.loads((base/'bit-clifford-one-evaluation-gate/author/BASIS.json').read_text())
roots = g.roots_from_files(L, B)
planes, charts = list(map(set, L['A2'])), list(map(set, L['D4']))
adj = [{j for j,y in enumerate(roots) if i != j and not g.b(x,y)} for i,x in enumerate(roots)]
data = json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
nodes, parameters = data['H_nodes'], data['receiver_parameters']
c, H, D, donors = 49, 263, 110, [0,61,62]
ids = [i for i in range(111) if planes[H] <= adj[i]]
aud = [i for i in ids if charts[D] <= adj[i]]
need(planes[H] == set(donors) and nodes[H] == c and len(ids) == 33 and len(aud) == 12, 'native port identity')
need(10 not in donors and 80 not in ids, 'ordinary identity target')
stars = {j:[p for p,P in enumerate(planes) if j in P] for j in donors}
off = {(j,i):[p for p in stars[j] if p != H and planes[p] <= adj[i]] for j in donors for i in ids}
parameter = lambda j,i: parameters[str(j)][str(i)]


def polynomial(xs):
    out = np.array([1],dtype=np.uint8)
    for a in xs:
        nxt = np.zeros(len(out)+1,dtype=np.uint8)
        nxt[1:] ^= out
        nxt[:-1] ^= g.M[a,out]
        out = nxt
    return out


def evaluate(p,a):
    out = 0
    for t in reversed(p):
        out = int(g.M[out,a]) ^ int(t)
    return out


U, deriv = {}, {}
for j,i in itertools.product(donors,ids):
    v = parameter(j,i)
    need(len(off[j,i]) == 15, 'full off-H source count')
    u = g.M[g.power(v,2),polynomial(nodes[p] for p in off[j,i])]
    numerator = np.zeros(17,dtype=np.uint8)
    numerator[1:] ^= u
    numerator[:-1] ^= g.M[c,u]
    expected = np.zeros(17,dtype=np.uint8)
    for degree,exponent in [(1,8),(2,16),(4,32),(5,4),(8,1),(14,4),(16,2)]:
        expected[degree] = g.power(v,exponent)
    expected[0] = evaluate(expected,c)
    need(np.array_equal(numerator,expected), 'raw-incidence Moore identity')
    d = g.power(v,8) ^ int(g.M[g.power(c,4),g.power(v,4)])
    need(d != 0 and evaluate(u,c) == d, 'actual central derivative')
    U[j,i], deriv[j,i] = u,d

quota,exits = Counter(),{}
for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
    phase,owner,coordinate,p,d,_,source,_ = json.loads(line)
    if p == H:
        need(phase == 'X' and owner == source and owner in donors,'early original ownership')
        quota[owner] += 1
        exits.setdefault(d,set()).update((owner,coordinate,lane) for lane in range(8))
need(quota == {0:30,61:30,62:30} and len(exits) == 45 and set(map(len,exits.values())) == {16}, 'actual positive physical packets')
need(all(sum(len(s) for d,s in exits.items() if charts[d] <= adj[i]) == 240 for i in ids), 'tight receiver owner cut')
frob = [1,2,4,8,16,32]
specifications = [
    ('universal-gap-feedback-port-gate',[1,2,4,32],298,302,303),
    ('involutive-feedback-extension',[0,1,2,4,8,16,32],343,348,349),
]
summary = []
for name,amplitudes,rank0,rank1,rank2 in specifications:
    package = base/'bit-shared-h-s031-review'/name
    literals = json.loads((package/'output/CERTIFICATES.json').read_text())
    cases = {(x['reference'],x['companion']):x for x in literals['cases']}
    E = sorted({(a+b-1)%63+1 for a in frob for b in amplitudes})
    need(len(E) == (18 if len(amplitudes) == 4 else 21),'exact product feature space')
    for ref in donors:
        eta = np.array([[g.power(parameter(ref,i),e) for e in E] for i in ids],dtype=np.uint8)
        need(g.rank(eta) == len(E), 'native feature independence')
        rows = g.echelon(eta.T)[1]
        interpolation = g.invert(eta[rows])
        def coefficients(values):
            coef = g.mm(interpolation,values[rows])
            need(np.array_equal(g.mm(eta,coef),values),'entire feature interpolation')
            return coef.T.reshape(-1)
        def equation(a,t):
            return g.M[np.array([g.power(a,m) for m in range(17)],dtype=np.uint8)[:,None],eta[t][None,:]].reshape(-1)
        for other in donors:
            C0 = np.array([equation(nodes[p],t) for t,i in enumerate(ids) for p in off[other,i]],dtype=np.uint8)
            C = np.vstack([C0,[equation(c,ids.index(i)) for i in aud]])
            rhs = np.array([0]*495+[g.M[g.power(parameter(ref,i),2),deriv[ref,i]] for i in aud],dtype=np.uint8)
            if ref == other:
                values = np.array([np.r_[g.M[g.power(parameter(ref,i),2),U[ref,i]],0] for i in ids],dtype=np.uint8)
                need(np.array_equal(g.mm(C,coefficients(values)[:,None])[:,0],rhs),'same-donor positive control')
                continue
            polynomials = []
            for epsilon,s in itertools.product([0,1],amplitudes):
                values = []
                for i in ids:
                    u = U[other,i]
                    p = np.r_[u,0]
                    if epsilon:
                        p = np.zeros(17,dtype=np.uint8)
                        p[1:] ^= u
                        p[:-1] ^= g.M[c,u]
                    values.append(g.M[g.power(parameter(ref,i),s),p])
                polynomials.append(coefficients(np.array(values,dtype=np.uint8)))
            Z = np.column_stack(polynomials)
            need(g.rank(Z) == 2*len(amplitudes) and not np.any(g.mm(C0,Z)), 'explicit complete off-H polynomial kernel')
            need((g.rank(C0),g.rank(C),g.rank(np.column_stack([C,rhs]))) == (rank0,rank1,rank2), 'independent three ranks')
            literal = cases[ref,other]
            w = np.array(literal['annihilator'],dtype=np.uint8)
            need(w.shape == (507,) and not np.any(g.mm(w[None,:],C)) and g.mm(w[None,:],rhs[:,None])[0,0] == 1,'literal dual on independently built raw matrix')
            bad = w.copy()
            bad[np.flatnonzero(w)[-1]] ^= 1
            need(np.any(g.mm(bad[None,:],C)), 'damaged dual rejected')
            # The exact contradiction is unchanged by an independently chosen
            # reversal of every row, so it is not tied to traversal ordering.
            need(not np.any(g.mm(w[::-1][None,:],C[::-1])),'row-order-independent contradiction')
            summary.append({'family':name,'reference':ref,'companion':other,'off_rank':rank0,'rank':rank1,'augmented_rank':rank2,'kernel_dimension':Z.shape[1]})

# Distinguish large update involution from the tempting smaller condition.
I = np.eye(3,dtype=np.uint8)
big = np.eye(48,dtype=np.uint8)
good = np.zeros((3,48),dtype=np.uint8)
good[0,1],good[2,9] = 1,1
bad = np.zeros((3,48),dtype=np.uint8)
bad[0,1],bad[1,9] = 1,1
kron = lambda A,B: g.M[A[:,None,:,None],B[None,:,None,:]].reshape(A.shape[0]*B.shape[0],A.shape[1]*B.shape[1])
controls = Counter()
for i in sorted(adj[0]):
    visible = [p for p in stars[0] if planes[p] <= adj[i]]
    p = polynomial(nodes[t] for t in visible)
    need(len(p) == 17 and p[-1] == 1,'actual sixteen-root source polynomial')
    cv = p[:16].copy()
    cv[0] ^= 1
    Csmall = kron(cv[:,None],I)
    for label,V in [('large_involution',good),('small_only',bad)]:
        N,S = g.mm(Csmall,V),g.mm(V,Csmall)
        N2 = g.mm(N,N)
        need(not np.any(g.mm(S,S)),'both small matrices square to zero')
        controls[label] += 1
        if label == 'large_involution':
            need(not np.any(N2) and np.any(S) and np.array_equal(g.mm(big^N,big^N),big),'strict enlarged involutive family')
        else:
            need(np.any(N2) and not np.any(g.mm(N,N2)) and np.array_equal(g.mm(big^N,big^N^N2),big),'valid three-term inverse outside hypothesis')
result = {'status':'PASS_ROOT_UNIVERSAL_AND_INVOLUTIVE_PORT_GATES','cases':summary,'raw_native_fibres':99,
          'same_donor_positive_controls':6,'corrupted_dual_controls':12,'actual_H_fields':720,
          'visible_fields':240,'port_fields':16,'source_controls':dict(controls),'general_conditional_feedback_excluded':False,
          'arbitrary_binary_or_nonlinear_bank_gauges_excluded':False,'new_complete_kappa':False}
args.out.mkdir(parents=True,exist_ok=True)
(args.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(result['status'],12,99,720,240,16,flush=True)
