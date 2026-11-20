#!/usr/bin/env python3
"""Independent literal review of the protected D1509 central-tail repair.

No source-construction or predecessor executable code is imported. The finite
field and exact root-coordinate methods follow the credited independent
Hermite review, with fresh source nullspaces and last available pivot rows.
"""
import argparse
from collections import Counter
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np


def need(value, message):
    if not value:
        raise AssertionError(message)


def xor(values):
    answer = 0
    for value in values:
        answer ^= int(value)
    return answer


def product(x, y):
    result = 0
    while y:
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x & 64:
            x ^= 67
    return result


MUL = np.array([[product(x, y) for y in range(64)] for x in range(64)], dtype=np.uint8)
INV = np.array([0] + [next(y for y in range(1, 64) if MUL[x, y] == 1)
                           for x in range(1, 64)], dtype=np.uint8)


def power(x, exponent):
    answer = 1
    while exponent:
        if exponent & 1:
            answer = int(MUL[answer, x])
        x = int(MUL[x, x])
        exponent >>= 1
    return answer


def mm(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    need(left.ndim == right.ndim == 2 and left.shape[1] == right.shape[0], 'matrix dimensions')
    answer = np.zeros((left.shape[0], right.shape[1]), dtype=np.uint8)
    for col in range(left.shape[1]):
        answer ^= MUL[left[:, col, None], right[col, None, :]]
    return answer


def kron(left, right):
    left, right = np.asarray(left, dtype=np.uint8), np.asarray(right, dtype=np.uint8)
    return MUL[left[:, None, :, None], right[None, :, None, :]].reshape(
        left.shape[0] * right.shape[0], left.shape[1] * right.shape[1])


def echelon(matrix):
    matrix = np.array(matrix, dtype=np.uint8, copy=True)
    pivots = []
    determinant = 1
    for col in range(matrix.shape[1]):
        row = len(pivots)
        choices = np.flatnonzero(matrix[row:, col])
        if not len(choices):
            continue
        chosen = row + int(choices[-1])
        matrix[[row, chosen]] = matrix[[chosen, row]]
        determinant = int(MUL[determinant, matrix[row, col]])
        matrix[row, col:] = MUL[INV[matrix[row, col]], matrix[row, col:]]
        if row + 1 < len(matrix):
            matrix[row + 1:, col:] ^= MUL[matrix[row + 1:, col, None], matrix[row, None, col:]]
        pivots.append(col)
        if len(pivots) == len(matrix):
            break
    return matrix, pivots, determinant


def rank(matrix):
    return len(echelon(matrix)[1])


def null(matrix):
    rows, pivots, _ = echelon(matrix)
    free = [j for j in range(rows.shape[1]) if j not in pivots]
    result = np.zeros((rows.shape[1], len(free)), dtype=np.uint8)
    result[free] = np.eye(len(free), dtype=np.uint8)
    for i in range(len(pivots) - 1, -1, -1):
        result[pivots[i]] = mm(rows[i:i + 1, pivots[i] + 1:], result[pivots[i] + 1:])[0]
    need(not np.any(mm(matrix, result)), 'independent nullspace identity')
    return result


def certificate(matrix):
    _, cols, _ = echelon(matrix)
    _, rows, _ = echelon(matrix[:, cols].T)
    minor = matrix[np.ix_(rows, cols)]
    _, pivots, determinant = echelon(minor)
    kernel = null(matrix)
    need(len(pivots) == len(cols) and determinant != 0, 'nonzero maximal minor')
    need(rank(kernel) == matrix.shape[1] - len(cols), 'independent upper-rank certificate')
    return {'shape': list(matrix.shape), 'rank': len(cols), 'minor_rows': rows,
            'minor_columns': cols, 'minor_determinant': determinant,
            'kernel_columns': kernel.tolist(), 'matrix_sha256': hashlib.sha256(matrix.tobytes()).hexdigest()}


def quadratic(x):
    return ((x & (x >> 1)) & 85).bit_count() & 1


def polar(x, y):
    return (x & (((y & 85) << 1) | ((y & 170) >> 1))).bit_count() & 1


def root_coordinates(layout, basis):
    columns = basis['lattice_basis_columns']
    lattice = [[columns[j][i] for j in range(8)] for i in range(8)]
    hyperbolic = basis['hyperbolic_basis_masks']
    reverse = {xor(hyperbolic[j] for j in range(8) if mask >> j & 1): mask for mask in range(256)}
    need(len(reverse) == 256, 'binary lattice coordinate isomorphism')
    roots = []
    for original in layout['root_table']:
        coordinates = [0] * 8
        for i in range(7, -1, -1):
            coordinates[i], remainder = divmod(original[i] - sum(lattice[i][j] * coordinates[j]
                                                               for j in range(i + 1, 8)), lattice[i][i])
            need(remainder == 0, 'exact integral root coordinates')
        roots.append(reverse[sum((x & 1) << i for i, x in enumerate(coordinates))])
    need(len(set(roots)) == 120 and set(roots) == {x for x in range(256) if quadratic(x)},
         'all actual anisotropic root labels')
    return roots


def u_polynomial(v, centre):
    numerator = np.zeros(17, dtype=np.uint8)
    for degree, coefficient in [(8, v), (16, power(v, 2)), (14, power(v, 4)),
                                (5, power(v, 4)), (1, power(v, 8)),
                                (2, power(v, 16)), (4, power(v, 32))]:
        numerator[degree] ^= coefficient
    numerator[0] = xor(MUL[numerator[d], power(centre, d)] for d in range(1, 17))
    answer = np.zeros(16, dtype=np.uint8)
    answer[15] = numerator[16]
    for d in range(14, -1, -1):
        answer[d] = numerator[d + 1] ^ MUL[centre, answer[d + 1]]
    need(numerator[0] == MUL[centre, answer[0]], 'exact division by z+centre')
    return answer


def root_product(nodes):
    result = np.array([1], dtype=np.uint8)
    for node in sorted(nodes):
        new = np.zeros(len(result) + 1, dtype=np.uint8)
        new[1:] ^= result
        new[:-1] ^= MUL[node, result]
        result = new
    return result


def binary_map(inputs, outputs):
    pairs = dict(zip(inputs, outputs))
    basis, span = [], {0: 0}
    for v in inputs:
        if v not in span:
            basis.append(v)
            span.update({w ^ v: image ^ pairs[v] for w, image in list(span.items())})
    need(len(basis) == 6 and len(span) == len(set(span.values())) == 64,
         'independent full binary parameter isomorphism')
    need(all(span[v] == w for v, w in zip(inputs, outputs)), 'all native parameter images')
    return span, basis


def inverse(A):
    n = len(A)
    R, pivots, _ = echelon(np.hstack((A, np.eye(n, dtype=np.uint8))))
    need(pivots == list(range(n)), 'invertible square matrix')
    for i in range(n - 1, -1, -1):
        R[:i, i:] ^= MUL[R[:i, i, None], R[i, None, i:]]
    answer = R[:, n:]
    need(np.array_equal(mm(A, answer), np.eye(n, dtype=np.uint8)), 'inverse residual')
    return answer


def q(x):
    return power(x, 9) ^ power(x, 18) ^ power(x, 36)


def field_polar(x, y):
    return q(x ^ y) ^ q(x) ^ q(y)


def witt(space, form):
    space, answer = set(space), []
    while len(space) > 1:
        b = lambda x, y: form(x ^ y) ^ form(x) ^ form(y)
        zeros = sorted(x for x in space if x and not form(x))
        if zeros:
            first = zeros[0]
            second = next(x for x in zeros if b(first, x))
        else:
            first = min(space - {0})
            second = min(space - {0, first})
        answer += [first, second]
        space = {x for x in space if not b(x, first) and not b(x, second)}
    return answer


def binary_span(values):
    span = {0}
    for value in values:
        span |= {x ^ value for x in list(span)}
    return span


def read_json(path):
    raw = path.read_bytes()
    if path.suffix == '.gz':
        raw = gzip.decompress(raw)
    return json.loads(raw), raw


def coefficients(tag,shape):
    return np.frombuffer(hashlib.shake_256(tag.encode('ascii')).digest(int(np.prod(shape))),dtype=np.uint8).reshape(shape)&63

def block_diag(matrices):
    answer=np.zeros((sum(len(M)for M in matrices),sum(M.shape[1]for M in matrices)),dtype=np.uint8)
    r=c=0
    for M in matrices:
        answer[r:r+len(M),c:c+M.shape[1]]=M;r+=len(M);c+=M.shape[1]
    return answer

def hermite(node):
    return np.array([[power(node,d-s)if(d&s)==s else 0 for d in range(30)]for s in range(2)],dtype=np.uint8)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--literal',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();repo=args.repo.resolve();base=repo/'research/moonshot-005-program/results'
    lit,raw=read_json(args.literal)
    need(hashlib.sha256(raw).hexdigest()=='61288e29cd19845b514fd8c186ca9e18cd054df43c86b5ca7f74a8d60fe43a05','frozen source literal')
    for name,digest in json.loads((Path(__file__).resolve().parent/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'source pin '+name)
    old,_=read_json(base/'bit-shared-h-s031-construction/rank-one-overlap/SOURCE-COEFFICIENTS.json.gz');moving,_=read_json(base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz')
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json');roots=root_coordinates(layout,basis)
    planes=[set(x)for x in layout['A2']];charts=[set(x)for x in layout['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    allocation,_=read_json(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');marked=set(allocation['selected_D'])
    maps={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in lit['maps'].items()};before={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in old['maps'].items()}
    donors=sorted(maps);need(donors==[0,45,61,62,100],'five complete sources')
    changed=sorted((j,a)for j,row in maps.items()for a,M in row.items()if not np.array_equal(M,before[j][a]));need(changed==[(45,642),(100,642)],'exactly two central tails changed')
    ports={h:[d for d,D in enumerate(charts)if planes[h]<=D and d in marked]for h in [263,642]};need(set(ports[263])&set(ports[642])=={1509},'one actual shared marked D')
    words={263:np.array(moving['Hwords']['263'],dtype=np.uint8),642:np.array(old['Bword'],dtype=np.uint8)};need(rank(words[263])==9 and rank(words[642])==8,'unchanged provider ranks9/8')
    stars={j:[a for a,P in enumerate(planes)if j in P]for j in donors};visible={};cuts=[]
    for j in donors:
        need(set(maps[j])==set(stars[j])and all(M.shape==(3,48)for M in maps[j].values()),'all28 literal quotient matrices')
        for i in sorted(adj[j]):
            hs=[a for a in stars[j]if planes[a]<=adj[i]];visible[j,i]=hs;need(len(hs)==16,'actual sixteen-plane source view')
            M=np.vstack([maps[j][a]for a in hs]);_,ps,det=echelon(M);need(len(ps)==48 and det!=0,'all full source determinants')
            cuts.append({'donor':j,'receiver':i,'native':i<111,'determinant':det})
    fibres={};Hreceipts=[]
    for h in [263,642]:
        ds=sorted(planes[h]);views=[i for i in range(120)if planes[h]<=adj[i]];fibres[h]={}
        for i in views:
            K=null(np.vstack([maps[ds[0]][a]for a in visible[ds[0],i]if a!=h]));need(K.shape==(48,3),'whole inverse-H fibre')
            positions=[q for q,d in enumerate(ports[h])if charts[d]<=adj[i]];reads=[]
            for s,j in enumerate(ds):
                X=np.vstack([maps[j][a]for a in visible[j,i]if a!=h]);need(not np.any(mm(X,K)),'identical whole fibre at all three donors')
                reads.append(mm(words[h][np.ix_(positions,range(3*s,3*s+3))],mm(maps[j][h],K)))
            need(rank(reads[0])==3 and all(np.array_equal(reads[0],R)for R in reads[1:]),'full common actual three-port readout')
            fibres[h][i]=(K,reads[0],[ports[h][q]for q in positions])
        core=np.hstack([row[0]for row in fibres[h].values()]);need(rank(core)==(22 if h==263 else 18),'retained exact fibre-core dimensions')
        Hreceipts.append({'H':h,'geometric_receivers':36,'native_receivers':sum(i<111 for i in views),'core_rank':rank(core)})
        if h==642:Sb=core[:,echelon(core)[1]]
    need(Sb.shape==(48,18),'entire second geometric core')
    for j in [45,100]:need(not np.any(mm(maps[j][642]^before[j][642],Sb)),'changed tails vanish on entire H642 core')
    quota=Counter()
    for row in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,owner,_,plane,_,_,source,_=json.loads(row)
        if phase=='X'and plane is not None:need(owner==source,'actual early owner');quota[owner,plane]+=1
    early=[]
    for j in donors:
        chart=263 if j in [0,61,62]else 642;rows=[]
        for a in stars[j]:
            F=maps[j][a];count=quota[j,a]//15;need(count in [1,2],'ordinary source quotas')
            if count==2:rows.append(kron(np.eye(2,dtype=np.uint8),F))
            elif a in [263,642]:rows.append(np.hstack([F,np.zeros_like(F)]))
            else:
                A=coefficients(f'early/{chart}/3/{j}/{a}/0',(3,6));need(rank(A)==3,'local early frame')
                rows.append(np.hstack([mm(A[:,:3],F),mm(A[:,3:],F)]))
        M=np.vstack(rows);_,ps,det=echelon(M);need(M.shape==(96,96)and len(ps)==96,'one full actual early96 basis')
        early.append({'donor':j,'seed':0,'determinant':det})
    D=1509;views=[i for i in range(111)if charts[D]<=adj[i]];need(len(views)==11,'actual native D1509 audience');spaces={};Drecords=[]
    for i in views:
        obs=[]
        for j in donors:
            outside=[a for a in visible[j,i]if not planes[a]<=charts[D]];need(len(outside)==12,'twelve outside-D quotients');obs.extend(maps[j][a]for a in outside)
        before_A=48-rank(np.vstack(obs));otherA=[q for q,d in enumerate(ports[263])if d!=D and charts[d]<=adj[i]]
        for s,j in enumerate(sorted(planes[263])):obs.append(mm(words[263][np.ix_(otherA,range(3*s,3*s+3))],maps[j][263]))
        before_B=48-rank(np.vstack(obs));otherB=[q for q,d in enumerate(ports[642])if d!=D and charts[d]<=adj[i]]
        obs.append(mm(words[642][np.ix_(otherB,range(3,6))],maps[61][642]));L=null(np.vstack(obs));need((before_A,before_B,L.shape[1])==(12,6,4),'canonical12->6->4 partial-cut dimensions')
        need(np.array_equal(L,lit['spaces'][str(i)]),'independently rebuilt canonical four-space')
        for s,j in enumerate(sorted(planes[642])):obs.append(mm(words[642][np.ix_(otherB,range(3*s,3*s+3))],maps[j][642]))
        X=np.vstack(obs);need(rank(X)==44 and not np.any(mm(X,L)),'exact common known four-dimensional D space')
        V=[]
        for h in [263,642]:
            K,R,ps=fibres[h][i];q=ps.index(D);V.append(mm(K,inverse(R)[:,q:q+1]))
        V=np.hstack(V);need(rank(V)==2 and not np.any(mm(X,V)),'both prior isolated directions retained')
        spaces[i]=L;Drecords.append({'receiver':i,'dimensions':[before_A,before_B,4,48-rank(X)],'space':L.tolist(),'two_directions':V.tolist()})
    systems=[]
    for s,j in enumerate(sorted(planes[642])):
        rows=[];rhs=[];target=mm(before[j][642],Sb)
        for u in range(3):
            for t in range(18):
                row=np.zeros((3,48),dtype=np.uint8);row[u]=Sb[:,t];rows.append(row.reshape(-1));rhs.append(target[u,t])
        for i,L in spaces.items():
            for q,d in enumerate(ports[642]):
                if d==D or not charts[d]<=adj[i]:continue
                for t in range(4):rows.append(MUL[words[642][q,3*s:3*s+3,None],L[:,t][None,:]].reshape(-1));rhs.append(0)
        M=np.array(rows,dtype=np.uint8);y=np.array(rhs,dtype=np.uint8)[:,None]
        need(M.shape==(142,144)and rank(M)==rank(np.hstack([M,y]))==110,'consistent affine tail system rank110')
        need(np.array_equal(mm(M,maps[j][642].reshape(-1,1)),y),'actual new coefficient satisfies every tail equation')
        N=null(M);need(N.shape==(144,34)and rank(N)==34,'complete34-dimensional solution freedom')
        systems.append({'donor':j,'shape':[142,144],'rank':110,'nullity':34})
    expected={0:[116,263],45:[642],61:[263,642],62:[263,643],100:[642]};identity=np.eye(3,dtype=np.uint8)
    for j in donors:
        edits=[]
        for a,F in maps[j].items():
            node=moving['base_nodes'][str(j)][str(a)];G=kron(np.array([[power(node,k)for k in range(16)]],dtype=np.uint8),identity)
            if not np.array_equal(F,G):edits.append(a)
        need(sorted(edits)==expected[j],'same one/two geometric quotient edits')
    K,R,ps=fibres[263][6];q=ps.index(1509);v=mm(K,inverse(R)[:,q:q+1]);packet=words[642][ports[642].index(302):ports[642].index(302)+1,:3]
    negative=int(mm(packet,mm(before[45][642],v))[0,0]);positive=int(mm(packet,mm(maps[45][642],v))[0,0]);need(negative==30 and positive==0,'old protected cross-D failure repaired')
    args.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_INDEPENDENT_PROTECTED_D1509_TAIL_REPAIR','changed_quotients':changed,'source_geometric_cuts':len(cuts),'source_native_cuts':sum(x['native']for x in cuts),
      'H':Hreceipts,'early_bases':early,'native_D1509_views':11,'known_partial_D_dimensions':[4]*11,'affine_systems':systems,
      'old_negative_control':negative,'new_control':positive,'protected_uniform_bounds':{str(j):36 if j in [0,61,62]else 27 for j in donors},
      'literal_payload_sha256':hashlib.sha256(raw).hexdigest(),'author_executable_imports':False,'complete_D_word':False,'full45_pair_assembled':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(args.out/'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps(cuts,sort_keys=True,indent=2)+'\n')
    payload=(json.dumps({'D_spaces':Drecords},sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/'CERTIFICATES.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    print(result['status'],315,291,72,67,11,4,110,negative,positive,flush=True)

if __name__=='__main__':main()
