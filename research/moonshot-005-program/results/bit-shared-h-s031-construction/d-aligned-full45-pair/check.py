#!/usr/bin/env python3
"""D-aligned full45 pair: repaired protected tails and port-aligned width12 sources.

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
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();repo=args.repo.resolve();here=Path(__file__).resolve().parent
    for name,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'pin '+name)
    base=repo/'research/moonshot-005-program/results'
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json')
    roots=root_coordinates(layout,basis);planes,charts=[set(x)for x in layout['A2']],[set(x)for x in layout['D4']]
    adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    witness,_=read_json(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');marked=set(witness['selected_D'])
    pair,pairraw=read_json(base/'bit-shared-h-s031-construction/port-aligned-complement/SOURCE-COEFFICIENTS.json.gz')
    pair['parameters']={'centres':[263,642],'shared_donor':61,'12':{'early':{str(j):0 for j in [0,45,61,62,100]}}}
    protected,_=read_json(base/'bit-shared-h-s031-construction/protected-d1509-tail-repair/SOURCE-COEFFICIENTS.json.gz')
    protected_word,_=read_json(base/'bit-shared-h-s031-construction/rank-one-overlap/SOURCE-COEFFICIENTS.json.gz')
    old,_=read_json(base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz')
    donors=[0,45,61,62,100];centres=[263,642]
    need(planes[263]&planes[642]=={61}and sorted(planes[263]|planes[642])==donors,'actual five-donor overlap')
    need(pair['core_seed']==0 and pair['fill_seed']==1,'exact port-aligned component seeds')
    three={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in protected['maps'].items()}
    twelve={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in pair['maps'].items()}
    stars={j:[a for a,P in enumerate(planes)if j in P]for j in donors}
    maps={j:{a:block_diag([three[j][a],twelve[j][a]])for a in stars[j]}for j in donors}
    word3={263:np.array(old['Hwords']['263'],dtype=np.uint8),642:np.array(protected_word['Bword'],dtype=np.uint8)}
    ports={h:[d for d,D in enumerate(charts)if planes[h]<=D]for h in centres}
    ports3={h:[d for d in ports[h]if d in marked]for h in centres};ports12={h:[d for d in ports[h]if d not in marked]for h in centres}
    word12={h:np.array(pair['H'][str(h)]['word'],dtype=np.uint8)for h in centres};words={}
    for h in centres:
        need(len(ports[h])==45 and len(ports3[h])==9 and len(ports12[h])==36 and pair['H'][str(h)]['ports']==ports12[h],'actual complementary physical ports')
        vandermonde=np.array([[power(q+1,d)for d in range(36)]for q in range(36)],dtype=np.uint8)
        need(np.array_equal(word12[h],vandermonde)and rank(vandermonde)==36,'literal retained width12 provider')
        P=np.zeros((45,45),dtype=np.uint8)
        for p,d in enumerate(ports[h]):
            for s in range(3):
                if d in ports3[h]:P[p,15*s:15*s+3]=word3[h][ports3[h].index(d),3*s:3*s+3]
                else:P[p,15*s+3:15*s+15]=word12[h][ports12[h].index(d),12*s:12*s+12]
        need(rank(P)==(45 if h==263 else 44),'full provider rank45/44');words[h]=P
    visible={(j,i):[a for a in stars[j]if planes[a]<=adj[i]]for j in donors for i in adj[j]}
    cut_records=[]
    for j in donors:
        need(set(three[j])==set(twelve[j])==set(stars[j]),'one complete source tuple per donor')
        need(all(M.shape==(12,192)for M in twelve[j].values()),'literal width12 source dimensions')
        for i in sorted(adj[j]):
            hs=visible[j,i];need(len(hs)==16,'actual16-plane source view')
            M3=np.vstack([three[j][a]for a in hs]);M12=np.vstack([twelve[j][a]for a in hs])
            _,p3,d3=echelon(M3);_,p12,d12=echelon(M12)
            need(len(p3)==48 and len(p12)==192 and d3 and d12,'both full component source cuts')
            M=np.vstack([maps[j][a]for a in hs]);order=[15*p+r for p in range(16)for r in range(3)]+[15*p+r for p in range(16)for r in range(3,15)]
            need(M.shape==(240,240)and np.array_equal(M[order],block_diag([M3,M12])),'literal joint full-source direct sum')
            cut_records.append({'donor':j,'receiver':i,'native':i<111,'determinant3':d3,'determinant12':d12,'determinant':int(MUL[d3,d12])})
        print('VERIFIED_FULL_WIDTH_DONOR',j,63,flush=True)
    fibres={};Hreceipts=[]
    for h in centres:
        ds=sorted(planes[h]);views=[i for i in range(120)if planes[h]<=adj[i]];fibres[str(h)]={};cores={3:[],12:[]}
        need(10 not in ds and 80 not in views,'actual unmodified identity-sum target')
        for i in views:
            off=[a for a in visible[ds[0],i]if a!=h]
            K3=null(np.vstack([three[ds[0]][a]for a in off]));K12=null(np.vstack([twelve[ds[0]][a]for a in off]))
            need(K3.shape==(48,3)and K12.shape==(192,12),'entire two component fibres')
            for k,component,K,word,portlist in [(3,three,K3,word3[h],ports3[h]),(12,twelve,K12,word12[h],ports12[h])]:
                positions=[p for p,d in enumerate(portlist)if charts[d]<=adj[i]];need(len(positions)==k,'all component visible ports');reads=[]
                for s,j in enumerate(ds):
                    X=np.vstack([component[j][a]for a in visible[j,i]if a!=h]);need(not np.any(mm(X,K)),'common entire component fibre')
                    D=mm(component[j][h],K);need(rank(D)==k,'full central component pencil')
                    reads.append(mm(word[np.ix_(positions,range(k*s,k*s+k))],D))
                need(rank(reads[0])==k and all(np.array_equal(reads[0],R)for R in reads[1:]),'actual full component readout');cores[k].append(K)
            K=block_diag([K3,K12]);need(K.shape==(240,15)and rank(K)==15,'entire full-width fibre')
            positions=[p for p,d in enumerate(ports[h])if charts[d]<=adj[i]];need(len(positions)==15,'actual15 visible full-width ports');reads=[]
            for s,j in enumerate(ds):
                X=np.vstack([maps[j][a]for a in visible[j,i]if a!=h]);need(not np.any(mm(X,K)),'full common off-H uncertainty')
                reads.append(mm(words[h][np.ix_(positions,range(15*s,15*s+15))],mm(maps[j][h],K)))
            need(rank(reads[0])==15 and all(np.array_equal(reads[0],R)for R in reads[1:]),'full15 common physical readout')
            fibres[str(h)][str(i)]={'kernel':K.tolist(),'readout':reads[0].tolist(),'ports':[ports[h][p]for p in positions],
                                   'readout_determinant':echelon(reads[0])[2]}
        core3=rank(np.hstack(cores[3]));core12=rank(np.hstack(cores[12]));need(core3==(22 if h==263 else 18),'protected core ranks22/18')
        Hreceipts.append({'H':h,'donors':ds,'physical_ports':ports[h],'geometric_receivers':len(views),'native_receivers':sum(i<111 for i in views),
                          'provider_rank':rank(words[h]),'component_core_ranks':[core3,core12],'full_core_rank':core3+core12})
        print('VERIFIED_FULL_WIDTH_H',h,len(views),rank(words[h]),core3,core12,flush=True)
    need(all(rank(F)==15 for row in maps.values()for F in row.values()),'every full quotient has rank15')
    propagation={j:(216 if j in [0,61,62]else 207)for j in donors}
    need(all(n<225 for n in propagation.values()),'protected all-centre nonsaturation')
    quota=Counter();owners={j:{}for j in donors};Howners={h:[]for h in centres}
    for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,owner,coordinate,plane,d,_,source,_=json.loads(line)
        if phase=='X'and plane is not None:
            need(owner==source,'actual original early owner');quota[owner,plane]+=1
            if owner in owners:owners[owner].setdefault(plane,[]).append(int(coordinate))
            if plane in centres:Howners[plane].append([owner,int(coordinate),d])
    need(Counter(quota.values())=={15:2675,30:422,45:11},'raw early quota census')
    for h in centres:need(len(Howners[h])==90 and set(x[2]for x in Howners[h])==set(ports[h]),'actual90 owners on all45 exits')
    for j in donors:
        need(sorted(x for row in owners[j].values()for x in row)==list(range(480)),'all480 actual donor coordinates owned once')
        need(all(len(owners[j][a])==quota[j,a]for a in stars[j])and max(quota[j,a]for a in stars[j])==30,'ordinary actual source quotas')
    need(not(set(owners[61][263])&set(owners[61][642])),'shared donor centres use disjoint original owners')
    early_matrices={};early_records=[];early_components={}
    for j in donors:
        source_chart=263 if j in [0,61,62]else 642;component_rows={};dets=[];seeds=[]
        for k,component,seed in [(3,three,0),(12,twelve,pair['parameters']['12']['early'][str(j)])]:
            rows={}
            for plane in stars[j]:
                F=component[j][plane];count=quota[j,plane]//15;need(count in [1,2],'ordinary1/2 early quota')
                if count==2:rows[plane]=kron(np.eye(2,dtype=np.uint8),F)
                elif plane in centres:rows[plane]=np.hstack([F,np.zeros_like(F)])
                else:
                    A=coefficients(f'early/{source_chart}/{k}/{j}/{plane}/{seed}',(k,2*k));need(rank(A)==k,'full local early frame')
                    rows[plane]=np.hstack([mm(A[:,:k],F),mm(A[:,k:],F)])
            M=np.vstack([rows[a]for a in stars[j]]);_,ps,det=echelon(M)
            need(M.shape==(32*k,32*k)and len(ps)==32*k,'one complete component early basis')
            component_rows[k]=rows;dets.append(det);seeds.append(seed)
            early_components[f'{j}/{k}']={'seed':seed,'source_chart':source_chart,'determinant':det,'matrix':M.tolist()}
        rows=[];row_owner_labels=[]
        for plane in stars[j]:
            count=quota[j,plane]//15;R=np.zeros((15*count,480),dtype=np.uint8)
            for k,start,bankstart in [(3,0,0),(12,3,48)]:
                M=component_rows[k][plane]
                for copy in range(count):
                    rr=slice(15*copy+start,15*copy+start+k)
                    R[rr,bankstart:bankstart+16*k]=M[k*copy:k*copy+k,:16*k]
                    R[rr,240+bankstart:240+bankstart+16*k]=M[k*copy:k*copy+k,16*k:]
            rows.append(R);row_owner_labels.extend([[plane,x]for x in sorted(owners[j][plane])])
        M=np.vstack(rows);_,ps,det=echelon(M);need(M.shape==(480,480)and len(ps)==480,'one full early480 basis')
        need(det==MUL[dets[0],dets[1]],'full early direct-sum determinant')
        early_matrices[str(j)]={'matrix':M.tolist(),'row_owners':row_owner_labels}
        early_records.append({'donor':j,'rank':480,'determinant':det,'component_seeds':seeds,'component_determinants':dets,'source_chart':source_chart})
        print('VERIFIED_SHARED_SOURCE_EARLY',j,480,det,flush=True)
    physical={};compilers={};physical_receipts=[]
    for h in centres:
        ds=sorted(planes[h]);Hinputs=[(j,x)for j in ds for x in sorted(owners[j][h])]
        need(len(Hinputs)==90 and all(len(owners[j][h])==30 for j in ds),'thirty actual H inputs per donor')
        owner_index={owner:q for q,owner in enumerate(Hinputs)};P=np.zeros((90,90),dtype=np.uint8);output_labels=[]
        for d in ports[h]:
            pair_owners=sorted((j,x)for j,x,p in Howners[h]if p==d);need(len(pair_owners)==2,'two physical owners per D')
            for copy,owner in enumerate(pair_owners):
                row=owner_index[owner];output_labels.append({'owner':list(owner),'D':d,'copy':copy})
                for s in range(3):P[row,30*s+15*copy:30*s+15*copy+15]=words[h][ports[h].index(d),15*s:15*s+15]
        defect=0 if h==263 else 2;paid=np.zeros((defect,90),dtype=np.uint8)
        if defect:paid[0,0]=1;paid[1,15]=1
        augmented=np.vstack([P,paid]);need(rank(P)==90-defect and rank(augmented)==90,'actual owner-bound ranks and sufficient complements')
        if defect:
            _,ps,_=echelon(np.hstack([augmented,np.eye(92,dtype=np.uint8)]));extra=[x-90 for x in ps if x>=90];need(len(extra)==2,'two extension columns')
            T=np.column_stack([augmented,np.eye(92,dtype=np.uint8)[:,extra]])
            need(rank(augmented[:-1])==89,'deleting one complement loses one original field')
        else:T=P
        Ti=inverse(T);need(np.array_equal(mm(Ti,augmented),np.vstack([np.eye(90,dtype=np.uint8),np.zeros((defect,90),dtype=np.uint8)])),'all original owners and zero complements restored')
        n=6*len(T);binary=np.array([[int(MUL[T[r//6,s//6],1<<(s%6)])>>(r%6)&1 for s in range(n)]for r in range(n)],dtype=np.uint8)
        reduced=binary.copy();operations=[]
        def add(target,source):
            need(target!=source,'distinct ADD owner labels');reduced[target]^=reduced[source];operations.append([target,source])
        for col in range(n):
            options=np.flatnonzero(reduced[col:,col]);need(len(options)>0,'full binary extension rank');pivot=col+int(options[0])
            if pivot!=col:add(col,pivot);add(pivot,col);add(col,pivot)
            for row in range(n):
                if row!=col and reduced[row,col]:add(row,col)
        need(np.array_equal(reduced,np.eye(n,dtype=np.uint8)),'physical binary ADD compiler')
        symbolic=[1<<i for i in range(540)]+[0]*(6*defect)
        for target,source in reversed(operations):symbolic[target]^=symbolic[source]
        need(symbolic==[sum(int(binary[r,c])<<c for c in range(540))for r in range(n)],'literal forward physical outputs')
        for target,source in operations:symbolic[target]^=symbolic[source]
        need(symbolic==[1<<i for i in range(540)]+[0]*(6*defect),'all originals and zeros restored by literal inverse')
        physical[str(h)]={'input_owners':[list(x)for x in Hinputs],'output_owners':output_labels,'word':P.tolist(),
                          'complements':paid.tolist(),'extension':T.tolist(),'extension_inverse':Ti.tolist()}
        compilers[str(h)]={'binary_elimination_ADDs':operations,'dimension':n}
        physical_receipts.append({'H':h,'two_copy_inputs':90,'two_copy_rank':90-defect,'binary_dimension':n,
                                  'binary_ADDs_per_direction':len(operations),'eight_lane_forward_inverse_ADDs':16*len(operations),
                                  'paid_field_exports':8*defect,'binary_INIT_MOVE_CLEAR_each':48*defect,'MOVE_gap':6 if defect else None})
        print('VERIFIED_PHYSICAL_H_COMPILER',h,n,len(operations),8*defect,flush=True)
    old_coefficients,_=read_json(base/'bit-shared-h-s031-review/full45-two-h-pair/author/output/COEFFICIENTS.json.gz')
    old_compiler,_=read_json(base/'bit-shared-h-s031-review/full45-two-h-pair/author/output/COMPILER.json.gz')
    binding_records=[]
    for h in centres:
        need(words[h].tolist()==old_coefficients['H'][str(h)]['word'],'exact old logical H word equality')
        need(physical[str(h)]==old_coefficients['H'][str(h)]['physical'],'exact old physical owner matrix and extension equality')
        need(compilers[str(h)]==old_compiler[str(h)],'exact old binary ADD operation list equality')
        for j in sorted(planes[h]):
            E=np.array(early_matrices[str(j)]['matrix'],dtype=np.uint8)
            labels=early_matrices[str(j)]['row_owners'];rows=[r for r,(plane,x)in enumerate(labels)if plane==h]
            need([labels[r][1]for r in rows]==sorted(owners[j][h]),'actual original-owner H input order')
            need(np.array_equal(E[rows],kron(np.eye(2,dtype=np.uint8),maps[j][h])),'new early rows bind exactly to unchanged two-copy H input slots')
            binding_records.append({'H':h,'donor':j,'actual_original_owners':sorted(owners[j][h]),'early_rows':rows,'quotient_copies':2,'bound_fields':30})
    common_ports=sorted(set(ports[263])&set(ports[642]));need(common_ports==[296,733,825,1509,1852],'all five actual shared D charts')
    shared_D=[]
    for d in common_ports:
        for i in range(111):
            if not charts[d]<=adj[i]:continue
            obs=[]
            for j in donors:
                need(j in charts[d],'all five supplied donors lie in shared D')
                hs=[h for h in stars[j]if planes[h]<=adj[i]and not planes[h]<=charts[d]]
                need(len(hs)==12,'all actual outside-D source observations')
                obs.extend(maps[j][h]for h in hs)
            outside_dimension=240-rank(np.vstack(obs));isolated={}
            for h in centres:
                f=fibres[str(h)][str(i)];K=np.array(f['kernel'],dtype=np.uint8);R=np.array(f['readout'],dtype=np.uint8)
                pos=f['ports'].index(d);v=mm(K,inverse(R)[:,pos:pos+1]);isolated[h]=v
                others=[p for p,q in enumerate(ports[h])if q!=d and charts[q]<=adj[i]]
                for t,j in enumerate(sorted(planes[h])):obs.append(mm(words[h][np.ix_(others,range(15*t,15*t+15))],maps[j][h]))
            X=np.vstack(obs);V=np.hstack([isolated[h]for h in centres]);need(rank(V)==2 and not np.any(mm(X,V)),'both isolated fullwidth H directions satisfy every known source and wrong-D H condition')
            shared_D.append({'D':d,'receiver':i,'outside_source_common_dimension':outside_dimension,'known_partial_D_common_dimension':240-rank(X),'isolated_directions':{str(h):v[:,0].tolist()for h,v in isolated.items()}})
    need(len(shared_D)==57,'complete shared native D incidence census')
    print('VERIFIED_SHARED_D_COMPATIBILITY',57,'EXACT_OLD_H_COMPILERS',2,flush=True)
    corrupted=words[642].copy();bad_port=ports12[642][0];corrupted[ports[642].index(bad_port),15]^=1;bad_count=0
    for i,S in fibres['642'].items():
        i=int(i);K=np.array(S['kernel'],dtype=np.uint8);positions=[p for p,d in enumerate(ports[642])if charts[d]<=adj[i]]
        reads=[mm(corrupted[np.ix_(positions,range(15*s,15*s+15))],mm(maps[j][642],K))for s,j in enumerate(sorted(planes[642]))]
        bad_count+=not all(np.array_equal(reads[0],R)for R in reads[1:])
    need(bad_count>0,'changed physical coefficient is detected')
    args.out.mkdir(parents=True,exist_ok=True)
    def save(name,value):
        payload=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/name).write_bytes(gzip.compress(payload,mtime=0));return hashlib.sha256(payload).hexdigest()
    result={'status':'PASS_D_ALIGNED_FULL45_TWO_H_PAIR','centres':centres,'shared_donor':61,'donors':donors,'source_width':15,
            'source_bank_dimension':240,'physical_bank_fields':3840,'source_geometric_cuts':len(cut_records),
            'source_native_cuts':sum(x['native']for x in cut_records),'geometric_receiver_chart_pairs':sum(x['geometric_receivers']for x in Hreceipts),
            'native_receiver_chart_pairs':sum(x['native_receivers']for x in Hreceipts),'common_readout_dimension':15,
            'H_receipts':Hreceipts,'uniform_propagation_upper_by_donor':propagation,'saturation_threshold':225,
            'physical_propagation_upper_by_donor':{j:16*n for j,n in propagation.items()},'physical_saturation_threshold':3600,
            'actual_early_bases':early_records,'physical_H_receipts':physical_receipts,'paid_field_exports':16,
            'binary_INIT_MOVE_CLEAR_each':96,'paid_MOVE_gap':6,'corrupted_port_readout_failures':bad_count,
            'shared_native_D_cuts':57,'both_direction_known_D_failures':0,'known_partial_D_dimensions':sorted({x['known_partial_D_common_dimension']for x in shared_D}),'exact_old_logical_H_words':True,'exact_old_physical_H_matrices_and_extensions':True,'exact_old_binary_ADD_lists':True,'new_early_H_owner_bindings':binding_records,'full45_joint_two_H_sources':True,'all111_sources':False,'complete_D_K_facet_word':False,
            'complete_return':False,'complete_invoice':False,'new_complete_kappa':False}
    coefficient={'field_modulus':67,'centres':centres,'shared_donor':61,'donors':donors,
                 'source_maps':{str(j):{str(a):M.tolist()for a,M in row.items()}for j,row in maps.items()},
                 'H':{str(h):{'donors':sorted(planes[h]),'ports':ports[h],'protected_ports':ports3[h],'complement_ports':ports12[h],
                              'word':words[h].tolist(),'physical':physical[str(h)]}for h in centres}}
    result['coefficient_payload_sha256']=save('COEFFICIENTS.json.gz',coefficient)
    result['fibre_payload_sha256']=save('FIBRES.json.gz',fibres)
    result['early_payload_sha256']=save('EARLY.json.gz',{'full':early_matrices,'components':early_components})
    result['compiler_payload_sha256']=save('COMPILER.json.gz',compilers)
    result['shared_D_payload_sha256']=save('SHARED-D-CHECKS.json.gz',shared_D)
    (args.out/'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps(cut_records,sort_keys=True,indent=2)+'\n')
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],len(cut_records),sum(x['native']for x in cut_records),72,67,45,44,57,16,flush=True)

if __name__=='__main__':main()
