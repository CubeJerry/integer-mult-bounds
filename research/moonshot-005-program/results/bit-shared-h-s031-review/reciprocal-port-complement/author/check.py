#!/usr/bin/env python3
"""Exact literal replay of a reciprocal width12 pair and its local D modules.

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

def local_modules(maps,donors,planes,charts,adj,visible,ports,words,direction_data):
    records=[];inverses={}
    for key,directions in sorted(direction_data.items()):
        d,i=map(int,key.split('/'));V=np.column_stack([directions[str(h)]for h in [263,642]]).astype(np.uint8);obs=[];operators=[]
        for j in donors:
            hs=visible[j,i]
            if (j,i)not in inverses:inverses[j,i]=inverse(np.vstack([maps[j][h]for h in hs]))
            Mi=inverses[j,i]
            for q,h in enumerate(hs):
                F=maps[j][h]
                if not planes[h]<=charts[d]:obs.append(F);continue
                T=mm(F,V)
                if rank(T):obs.append(mm(null(T.T).T,F))
                operators.append((j,h,Mi[:,12*q:12*q+12],F))
        for h in [263,642]:
            pos=[q for q,x in enumerate(ports[h])if x!=d and charts[x]<=adj[i]]
            for s,j in enumerate(sorted(planes[h])):obs.append(mm(words[h][np.ix_(pos,range(12*s,12*s+12))],maps[j][h]))
        E=null(np.vstack(obs));need(not np.any(mm(np.vstack(obs),V)),'the two old directions lie in the linear envelope')
        for seed in range(32):
            u=mm(E,coefficients(f'D4module/{i}/{d}/{seed}',(E.shape[1],1)));M=np.hstack([V,u]);U=M[:,echelon(M)[1]]
            for iteration in range(8):
                M=np.hstack([U]+[mm(K,mm(F,U))for j,h,K,F in operators]);N=M[:,echelon(M)[1]]
                if N.shape[1]==U.shape[1]:break
                U=N
                if U.shape[1]>4:break
            if U.shape[1]!=4:continue
            if any(rank(mm(F,U))!=1 for j,h,K,F in operators):continue
            lines={};ok=True
            for j,h,K,F in operators:
                M=mm(K,mm(F,U));need(rank(np.hstack([U,M]))==4,'four-space invariant under every source coordinate projection');p=echelon(M)[1];need(len(p)==1,'one-dimensional source contribution');v=M[:,p]
                if h in lines and rank(np.hstack([lines[h],v]))!=1:ok=False;break
                lines[h]=v
            if ok:break
        else:raise AssertionError('no four-space with all shared projection lines')
        need(rank(np.hstack([V,U]))==4 and not np.any(mm(np.vstack(obs),U)),'common four-space contains both H directions and kills all known outside observations')
        need(len(lines)==14,'all fourteen H lines touched by the five supplied sources')
        for j in donors:
            hs=[h for h in visible[j,i]if planes[h]<=charts[d]];need(len(hs)==4 and rank(np.hstack([lines[h]for h in hs]))==4,'each supplied donor has a basis of four H lines')
        partial=[]
        for j in sorted(charts[d]):
            hs=[h for h,P in enumerate(planes)if j in P and P<=charts[d]];known=[h for h in hs if h in lines];r=rank(np.hstack([lines[h]for h in known]))if known else 0;need(r==len(known),'independent known partial star at every geometric D donor');partial.append({'donor':j,'known_lines':len(known),'rank':r})
        records.append({'D':d,'receiver':i,'native':i<111,'envelope_dimension':E.shape[1],'seed':seed,'space':U.tolist(),'H_lines':{str(h):v[:,0].tolist()for h,v in lines.items()},'partial_other_stars':partial})
    need(len(records)==48 and sum(r['native']for r in records)==46,'all common geometric and native cuts')
    print('LOCAL_D_FOUR_SPACES',len(records),sum(r['native']for r in records),flush=True)
    return records

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--literal',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    repo=args.repo.resolve();base=repo/'research/moonshot-005-program/results';literal,raw=read_json(args.literal)
    need(hashlib.sha256(raw).hexdigest()=='e907a50baf567d498b4ea4c3d1628eab865a0ae5f576aaa15bc5d06f2fc8aae7','frozen literal payload')
    for name,digest in json.loads((Path(__file__).resolve().parent/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'review input pin '+name)
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json')
    roots=root_coordinates(layout,basis);planes=[set(x)for x in layout['A2']];charts=[set(x)for x in layout['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    allocation,_=read_json(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');marked=set(allocation['selected_D'])
    maps={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in literal['maps'].items()};donors=sorted(maps)
    need(donors==[0,45,61,62,100]and planes[263]&planes[642]=={61},'one shared donor and five literal sources')
    ports={h:[d for d,D in enumerate(charts)if planes[h]<=D and d not in marked]for h in [263,642]}
    words={h:np.array(literal['H'][str(h)]['word'],dtype=np.uint8)for h in [263,642]}
    for h in ports:
        need(ports[h]==literal['H'][str(h)]['ports']and len(ports[h])==36,'current unmarked36 physical ports')
        need(np.array_equal(words[h],np.array([[power(t+1,k)for k in range(36)]for t in range(36)],dtype=np.uint8))and rank(words[h])==36,'full literal Vandermonde provider')
    common=sorted(set(ports[263])&set(ports[642]));need(common==[296,733,825,1852],'four actual unmarked shared D flags')
    rel=np.array(literal['relations'],dtype=np.uint8);lift=np.array(literal['lift'],dtype=np.uint8)
    need(rel.shape==(8,144)and rank(rel)==8 and lift.shape==(144,136)and rank(lift)==136 and not np.any(mm(rel,lift)),'exact eight cross equations and136-dimensional kernel')
    for side,h in enumerate([263,642]):
        s=sorted(planes[h]).index(61);selector=words[h][np.ix_([ports[h].index(d)for d in common],range(12*s,12*s+12))]
        need(np.array_equal(selector,literal['selectors'][side])and rank(selector)==4,'actual same-D contribution selector')
        C=np.zeros((12,144),dtype=np.uint8);C[:,72*side+12*s:72*side+12*s+12]=np.eye(12,dtype=np.uint8)
        need(np.array_equal(maps[61][h],np.hstack([mm(C,lift),np.zeros((12,56),dtype=np.uint8)])),'central control on the common source bank')
    cuts=[];visible={};stars={j:[a for a,P in enumerate(planes)if j in P]for j in donors}
    for j in donors:
        need(set(maps[j])==set(stars[j])and all(M.shape==(12,192)for M in maps[j].values()),'complete28-plane source tuple')
        for i in sorted(adj[j]):
            hs=[a for a in stars[j]if planes[a]<=adj[i]];visible[j,i]=hs;need(len(hs)==16,'actual16-plane cut')
            M=np.vstack([maps[j][a]for a in hs]);_,ps,det=echelon(M);need(len(ps)==192 and det!=0,'complete192-dimensional source view')
            cuts.append({'donor':j,'receiver':i,'native':i<111,'determinant':det})
        print('REVIEWED_ALIGNED_SOURCE',j,63,flush=True)
    fibres={};core_ranks={};Hreceipts=[]
    for h in [263,642]:
        ds=sorted(planes[h]);views=[i for i in range(120)if planes[h]<=adj[i]];fibres[h]={}
        for i in views:
            off=[a for a in visible[ds[0],i]if a!=h];K=null(np.vstack([maps[ds[0]][a]for a in off]));need(K.shape==(192,12),'whole12-dimensional off-H fibre')
            positions=[q for q,d in enumerate(ports[h])if charts[d]<=adj[i]];need(len(positions)==12,'actual12 visible component ports');reads=[]
            for s,j in enumerate(ds):
                X=np.vstack([maps[j][a]for a in visible[j,i]if a!=h]);need(not np.any(mm(X,K)),'same entire fibre for all donors')
                R=mm(words[h][np.ix_(positions,range(12*s,12*s+12))],mm(maps[j][h],K));reads.append(R)
            need(rank(reads[0])==12 and all(np.array_equal(reads[0],R)for R in reads[1:]),'full common physical readout')
            fibres[h][i]=(K,reads[0],[ports[h][q]for q in positions])
        core_ranks[h]=rank(np.hstack([v[0]for v in fibres[h].values()]));Hreceipts.append({'H':h,'geometric_receivers':len(views),'native_receivers':sum(i<111 for i in views),'core_rank':core_ranks[h]})
        print('REVIEWED_ALIGNED_H',h,len(views),core_ranks[h],flush=True)
    quota=Counter()
    for row in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,owner,_,plane,_,_,source,_=json.loads(row)
        if phase=='X'and plane is not None:need(owner==source,'actual original early owner');quota[owner,plane]+=1
    need(Counter(quota.values())=={15:2675,30:422,45:11},'raw early quotas')
    early=[]
    for j in donors:
        chart=263 if j in [0,61,62]else 642;seed=literal['early_seeds'][str(j)];rows=[]
        for plane in stars[j]:
            F=maps[j][plane];count=quota[j,plane]//15;need(count in [1,2],'ordinary source quota')
            if count==2:rows.append(kron(np.eye(2,dtype=np.uint8),F))
            elif plane in [263,642]:rows.append(np.hstack([F,np.zeros_like(F)]))
            else:
                A=coefficients(f'early/{chart}/12/{j}/{plane}/{seed}',(12,24));need(rank(A)==12,'local early frame')
                rows.append(np.hstack([mm(A[:,:12],F),mm(A[:,12:],F)]))
        M=np.vstack(rows);_,ps,det=echelon(M);need(M.shape==(384,384)and len(ps)==384 and det!=0,'single full actual384-dimensional early basis')
        early.append({'donor':j,'seed':seed,'determinant':det,'rank':384})
    cross=[];direction_data={}
    for d in common:
        for i in range(120):
            if not charts[d]<=adj[i]:continue
            V={}
            for h in [263,642]:
                K,R,ps=fibres[h][i];q=ps.index(d);V[h]=mm(K,inverse(R)[:,q:q+1])
            need(rank(np.hstack([V[263],V[642]]))==2,'two independent target contributions at shared D')
            ramp=next(x for x in literal['ramps']if x['D']==d)
            for h,other,name in [(263,642,'beta'),(642,263,'gamma')]:
                ds=sorted(planes[h])
                for t,s in enumerate([0,2]):
                    value=int(mm(words[h][ports[h].index(d):ports[h].index(d)+1,12*s:12*s+12],mm(maps[ds[s]][h],V[other]))[0,0]);need(value==ramp[name][t],'literal reciprocal cross-amplitude')
            need(all(MUL[b,g]==1 for b,g in zip(ramp['beta'],ramp['gamma'])),'both reciprocal identities')
            for ha in [263,642]:
                hb=905-ha;others=[q for q,D in enumerate(ports[hb])if D!=d and charts[D]<=adj[i]]
                for s,j in enumerate(sorted(planes[hb])):
                    need(not np.any(mm(words[hb][np.ix_(others,range(12*s,12*s+12))],mm(maps[j][hb],V[ha]))),'all wrong-D packets vanish in both directions')
                for j in donors:
                    outside=[a for a in visible[j,i]if not planes[a]<=charts[d]];need(len(outside)==12,'twelve source planes outside D')
                    need(not np.any(mm(np.vstack([maps[j][a]for a in outside]),V[ha])),'all outside-D source quotients vanish at every donor')
            cross.append({'D':d,'receiver':i,'native':i<111,'direction_rank':2,'wrong_D_values_zero':True,'outside_D_values_zero':True})
            direction_data[f'{d}/{i}']={str(h):v[:,0].tolist()for h,v in V.items()}
    old,_=read_json(base/'bit-shared-h-s031-review/full45-two-h-pair/author/PAIR-TWELVE.json.gz');oldmaps={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in old['maps'].items()}
    K=null(np.vstack([oldmaps[0][a]for a in visible[0,4]if a!=263]));ps=[q for q,d in enumerate(ports[263])if charts[d]<=adj[4]]
    R=mm(words[263][np.ix_(ps,range(12))],mm(oldmaps[0][263],K));q=[ports[263][t]for t in ps].index(733);v=mm(K,inverse(R)[:,q:q+1]);row=words[642][ports[642].index(825):ports[642].index(825)+1,:12]
    oldvalue=int(mm(row,mm(oldmaps[45][642],v))[0,0]);need(oldvalue==20,'negative control: old coordinate-selector gluing fails actual D733->D825')
    need(len(cross)==48 and sum(x['native']for x in cross)==46,'all48 geometric and46 native unmarked shared-D cuts')
    module_records=local_modules(maps,donors,planes,charts,adj,visible,ports,words,direction_data)
    whole=[]
    for h,j,k in [(116,0,45),(643,62,100)]:
        for i in range(120):
            if not planes[h]<=adj[i]:continue
            K=[null(np.vstack([maps[t][a]for a in visible[t,i]if a!=h]))for t in [j,k]];r=rank(np.hstack(K));need(r>12,'unbuilt whole-H fibre condition remains unsatisfied');whole.append({'H':h,'receiver':i,'joint_rank':r})
    args.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_RECIPROCAL_PORT_WIDTH12_LOCAL_MODULES','source_geometric_cuts':len(cuts),'source_native_cuts':sum(x['native']for x in cuts),'H':Hreceipts,
      'actual_early_bases':early,'shared_D':common,'geometric_shared_D_checks':48,'native_shared_D_checks':46,
      'both_direction_wrong_D_annihilation':True,'all_five_donor_outside_D_annihilation':True,'old_pair_negative_value':oldvalue,'common_four_space_count':len(module_records),'unbuilt_whole_H_fibre_ranks':whole,
      'literal_payload_sha256':hashlib.sha256(raw).hexdigest(),'author_executable_imports':False,'complete_D_word':False,
      'protected_component_repaired':False,'full45_repaired_pair':False,'global_continuation':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    (args.out/'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps(cuts,sort_keys=True,indent=2)+'\n')
    payload=(json.dumps({'cross_checks':cross,'directions':direction_data,'four_spaces':module_records},sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/'CROSS-CERTIFICATES.json.gz').write_bytes(gzip.compress(payload,mtime=0))
    print(result['status'],315,291,72,67,48,46,oldvalue,flush=True)

if __name__=='__main__':main()
