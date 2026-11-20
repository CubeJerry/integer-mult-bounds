#!/usr/bin/env python3
"""Independent literal review of the repaired full45 two-H source pair.

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
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();repo=args.repo.resolve();base=repo/'research/moonshot-005-program/results';here=Path(__file__).resolve().parent;author=here.parent
    for name,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'pin '+name)
    lit,raw=read_json(author/'output/COEFFICIENTS.json.gz');need(hashlib.sha256(raw).hexdigest()=='0982dba6a263c27dc650cada82908ae018bceb20f28774502128d4dba607a102','frozen full literal')
    old,_=read_json(base/'bit-shared-h-s031-review/full45-two-h-pair/author/output/COEFFICIENTS.json.gz')
    protected,_=read_json(base/'bit-shared-h-s031-construction/protected-d1509-tail-repair/SOURCE-COEFFICIENTS.json.gz');aligned,_=read_json(base/'bit-shared-h-s031-construction/port-aligned-complement/SOURCE-COEFFICIENTS.json.gz')
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json');roots=root_coordinates(layout,basis)
    planes=[set(x)for x in layout['A2']];charts=[set(x)for x in layout['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    witness,_=read_json(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');marked=set(witness['selected_D'])
    maps={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in lit['source_maps'].items()};donors=sorted(maps);centres=[263,642]
    need(donors==[0,45,61,62,100]and planes[263]&planes[642]=={61},'one shared donor and five whole tuples')
    components={3:{int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in protected['maps'].items()},12:{int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in aligned['maps'].items()}}
    stars={j:[h for h,P in enumerate(planes)if j in P]for j in donors};visible={};cuts=[]
    for j in donors:
        need(set(maps[j])==set(stars[j])and len(stars[j])==28,'complete source star')
        for h,M in maps[j].items():need(M.shape==(15,240)and np.array_equal(M,block_diag([components[3][j][h],components[12][j][h]])),'literal repaired component direct sum')
        for i in sorted(adj[j]):
            hs=[h for h in stars[j]if planes[h]<=adj[i]];visible[j,i]=hs;need(len(hs)==16,'sixteen source observations');M=np.vstack([maps[j][h]for h in hs]);_,ps,det=echelon(M);need(len(ps)==240 and det,'fresh full240 determinant')
            cuts.append({'donor':j,'receiver':i,'native':i<111,'determinant':det})
        print('SOURCE',j,63,flush=True)
    words={h:np.array(lit['H'][str(h)]['word'],dtype=np.uint8)for h in centres};ports={h:[d for d,D in enumerate(charts)if planes[h]<=D]for h in centres};fibres={};hrecords=[]
    for h in centres:
        info=lit['H'][str(h)];need(info['ports']==ports[h]and len(ports[h])==45,'actual45 physical exits');need(info['protected_ports']==[d for d in ports[h]if d in marked]and len(info['protected_ports'])==9,'actual marked split')
        need(info==old['H'][str(h)],'all old H matrices, owners and extensions literally unchanged');need(rank(words[h])==(45 if h==263 else 44),'provider ranks')
        ds=sorted(planes[h]);views=[i for i in range(120)if planes[h]<=adj[i]];fibres[h]={}
        for i in views:
            K=null(np.vstack([maps[ds[0]][a]for a in visible[ds[0],i]if a!=h]));need(K.shape==(240,15),'entire full15 inverse fibre');pos=[q for q,d in enumerate(ports[h])if charts[d]<=adj[i]];need(len(pos)==15,'fifteen visible ports');reads=[]
            for s,j in enumerate(ds):
                X=np.vstack([maps[j][a]for a in visible[j,i]if a!=h]);need(not np.any(mm(X,K)),'full fibre common across donors');D=mm(maps[j][h],K);need(rank(D)==15,'full donor pencil');reads.append(mm(words[h][np.ix_(pos,range(15*s,15*s+15))],D))
            need(rank(reads[0])==15 and all(np.array_equal(reads[0],R)for R in reads[1:]),'common invertible full15 readout');fibres[h][i]=(K,reads[0],[ports[h][q]for q in pos])
        core=rank(np.hstack([t[0]for t in fibres[h].values()]));need(core==(214 if h==263 else 210),'full core rank');hrecords.append({'H':h,'geometric':len(views),'native':sum(i<111 for i in views),'word_rank':rank(words[h]),'core_rank':core});print('H',h,core,flush=True)
    earlylit,_=read_json(author/'output/EARLY.json.gz');quota=Counter();owners={j:{}for j in donors}
    for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,owner,coordinate,h,_,_,source,_=json.loads(line)
        if phase=='X'and h is not None:
            need(owner==source,'genuine original owner');quota[owner,h]+=1
            if owner in owners:owners[owner].setdefault(h,[]).append(coordinate)
    early=[];bindings=[]
    for j in donors:
        need(sorted(v for xs in owners[j].values()for v in xs)==list(range(480)),'each actual source owner exactly once');chart=263 if j in [0,61,62]else 642;rows=[];labels=[]
        for h in stars[j]:
            F=maps[j][h];count=quota[j,h]//15;need(count in [1,2],'ordinary source quotas')
            if count==2:R=kron(np.eye(2,dtype=np.uint8),F)
            else:
                need(h not in centres,'both selected centres have complete doubled quotient');left=[];right=[]
                for k in [3,12]:
                    A=coefficients(f'early/{chart}/{k}/{j}/{h}/0',(k,2*k));need(rank(A)==k,'full local frame');left.append(A[:,:k]);right.append(A[:,k:])
                R=np.hstack([mm(block_diag(left),F),mm(block_diag(right),F)])
            rows.append(R);labels.extend([[h,x]for x in sorted(owners[j][h])])
        M=np.vstack(rows);given=earlylit['full'][str(j)];need(np.array_equal(M,given['matrix'])and labels==given['row_owners'],'exact full480 early literal and owner order');_,ps,det=echelon(M);need(M.shape==(480,480)and len(ps)==480,'independent early480 determinant')
        early.append({'donor':j,'determinant':det,'seed3':0,'seed12':0})
        for h in centres:
            if j not in planes[h]:continue
            loc=[q for q,(a,x)in enumerate(labels)if a==h];need(len(loc)==30 and np.array_equal(M[loc],kron(np.eye(2,dtype=np.uint8),maps[j][h])),'actual early two-copy H binding')
            physicalowners=[o for o in lit['H'][str(h)]['physical']['input_owners']if o[0]==j];need(physicalowners==[[j,labels[q][1]]for q in loc],'same original H input owners');bindings.append({'donor':j,'H':h,'count':30})
        print('EARLY',j,det,flush=True)
    need([x['determinant']for x in early]==[15,20,52,54,42],'reported exact early determinants');need(len(bindings)==6,'six bound source-to-H interfaces')
    common=sorted(set(ports[263])&set(ports[642]));need(common==[296,733,825,1509,1852],'actual five common D charts');drecords=[]
    for d in common:
        audience=[i for i in range(111)if charts[d]<=adj[i]]
        for i in audience:
            vectors=[]
            for h in centres:
                K,R,ps=fibres[h][i];q=ps.index(d);vectors.append(mm(K,inverse(R)[:,q:q+1]))
            V=np.hstack(vectors);need(rank(V)==2,'two independent isolated H directions');obs=[]
            for j in donors:
                outside=[h for h in visible[j,i]if not planes[h]<=charts[d]];need(len(outside)==12,'twelve actual outside-D source planes');X=np.vstack([maps[j][h]for h in outside]);need(not np.any(mm(X,V)),'both directions kill every outside-D source observation');obs.append(X)
            for h in centres:
                pos=[q for q,x in enumerate(ports[h])if x!=d and charts[x]<=adj[i]];need(len(pos)==14,'all fourteen other visible H packets')
                for s,j in enumerate(sorted(planes[h])):
                    X=mm(words[h][np.ix_(pos,range(15*s,15*s+15))],maps[j][h]);need(not np.any(mm(X,V)),'both directions kill every wrong-D H contribution');obs.append(X)
            dimension=240-rank(np.vstack(obs));need(dimension in [18,20,22],'partial known D dimension');drecords.append({'D':d,'receiver':i,'dimension':dimension,'directions':V.tolist()})
        print('D',d,len(audience),flush=True)
    need(len(drecords)==57,'all native shared-D cuts');compiler,_=read_json(author/'output/COMPILER.json.gz');oldcompiler,_=read_json(base/'bit-shared-h-s031-review/full45-two-h-pair/author/output/COMPILER.json.gz');need(compiler==oldcompiler,'unchanged literal binary ADD words')
    # The old pair provides a nonzero negative control in each component.
    oldfibres,_=read_json(base/'bit-shared-h-s031-review/full45-two-h-pair/author/output/FIBRES.json.gz');controls=[]
    for i,d,e,expected in [(4,733,825,20),(6,1509,302,30)]:
        K,R,ps=fibres[263][i];v=mm(K,inverse(R)[:,ps.index(d):ps.index(d)+1]);row=words[642][ports[642].index(e):ports[642].index(e)+1,:15];oldF=np.array(old['source_maps']['45']['642'],dtype=np.uint8)
        oldentry=oldfibres['263'][str(i)];oldK=np.array(oldentry['kernel'],dtype=np.uint8);oldR=np.array(oldentry['readout'],dtype=np.uint8);oldq=oldentry['ports'].index(d);oldv=mm(oldK,inverse(oldR)[:,oldq:oldq+1]);oldvalue=int(mm(row,mm(oldF,oldv))[0,0]);need(oldvalue==expected,'frozen old cross-D negative control');newvalue=int(mm(row,mm(maps[45][642],v))[0,0]);need(newvalue==0,'old physical cross-D packet vanishes after repair');controls.append({'receiver':i,'D':d,'otherD':e,'old_frozen_pair_value':oldvalue,'new':newvalue})
    args.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_INDEPENDENT_D_ALIGNED_FULL45_TWO_H_PAIR','source_geometric_cuts':len(cuts),'source_native_cuts':sum(t['native']for t in cuts),'H':hrecords,'early_bases':early,'early_H_bindings':bindings,'shared_native_D_cuts':len(drecords),'partial_D_dimensions':sorted(set(t['dimension']for t in drecords)),'old_H_data_exactly_equal':True,'old_binary_ADD_lists_exactly_equal':True,'uniform_bounds':{str(j):216 if j in [0,61,62]else 207 for j in donors},'new_control_values':controls,'literal_payload_sha256':hashlib.sha256(raw).hexdigest(),'author_executable_imports':False,'complete_D_word':False,'complete_invoice':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(args.out/'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps(cuts,sort_keys=True,indent=2)+'\n');payload=(json.dumps({'D_records':drecords},sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/'CERTIFICATES.json.gz').write_bytes(gzip.compress(payload,mtime=0));print(result['status'],315,291,72,67,45,44,57,flush=True)

if __name__=='__main__':main()
