#!/usr/bin/env python3
"""Independent literal review of a D1509 source/phase-matrix interface.

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

def full_review(package,base,component,three,donors,planes,charts,adj,visible,quota,routes,out):
    source,_=read_json(package/'output/SOURCES.json.gz');early,_=read_json(package/'output/EARLY.json.gz');physical,_=read_json(package/'output/H-PHYSICAL.json.gz');dword,_=read_json(package/'output/D-WORD.json.gz');pair,_=read_json(base/'bit-shared-h-s031-construction/port-aligned-complement/SOURCE-COEFFICIENTS.json.gz');old,_=read_json(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/COEFFICIENTS.json.gz')
    maps={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in source['maps'].items()};twelve={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in pair['maps'].items()};frames={tuple(map(int,s.split('/'))):np.array(M,dtype=np.uint8)for s,M in source['frames'].items()};LF=np.array(source['selected_original_space'],dtype=np.uint8);expected=np.zeros((480,8),dtype=np.uint8);expected[:48,:4]=component['source']['L'];expected[240:288,4:]=component['source']['L'];need(np.array_equal(LF,expected)and rank(LF)==8,'entire selected full-width paired space')
    key=lambda r:(r[1],r[2]);HX={};HY={};Xj={};Yj={}
    for r in routes:
        if r[3]is None:continue
        (HX if r[0]=='X'else HY).setdefault(r[3],[]).append(r)
        if r[0]=='X':Xj.setdefault((r[1],r[3]),[]).append(r)
        elif r[6]is not None:Yj.setdefault((r[6],r[3]),[]).append(r)
    for table in [HX,HY,Xj,Yj]:
        for k in table:table[k].sort(key=key)
    sourcecuts=[];earlyrecords=[];parity_count=0;projection_records=[]
    for j in donors:
        rows=[];labels=[];Ephysical=np.zeros((480,480),dtype=np.uint8);inverses={}
        for h,F in sorted(maps[j].items()):
            need(np.array_equal(F,block_diag([three[j][h],twelve[j][h]])),'exact full15 source direct sum');Q=frames[j,h];need(Q.shape==(30,30)and rank(Q)==30,'invertible full paired source frame');cp=[0,1,2,15,16,17];cq=[q for q in range(30)if q not in cp];T3=np.array(component['source_frames'][f'{j}/{h}'],dtype=np.uint8)
            need(np.array_equal(Q[np.ix_(cp,cp)],T3)and not np.any(Q[np.ix_(cp,cq)])and not np.any(Q[np.ix_(cq,cp)]),'literal protected frame embedding');R=mm(Q,block_diag([F,F]));q=quota[j,h];need(len(Xj[j,h])==q and len(Yj.get((j,h),[]))==30-q,'actual early/late source visit counts')
            for t,r in enumerate(Xj[j,h]):Ephysical[r[2]]=R[t];labels.append([h,r[2]])
            rows.extend(R[:q]);late=np.array(source['late_parities'][str(j)][str(h)],dtype=np.uint8).reshape(30-q,480);need(np.array_equal(late,R[q:]),'all bound original-field late parities');parity_count+=30-q
        E=np.array(rows,dtype=np.uint8);need(np.array_equal(E,early[str(j)]['matrix'])and np.array_equal(Ephysical,early[str(j)]['physical_matrix'])and labels==early[str(j)]['row_owners'],'both literal full480 early orderings');need(sorted(x[1]for x in labels)==list(range(480)),'all genuine source owners once');_,ps,det=echelon(Ephysical);need(len(ps)==480,'full physical early480 determinant');earlyrecords.append({'donor':j,'determinant':det})
        for ii in sorted(adj[j]):
            hs=visible[j,ii];_,ps,det=echelon(np.vstack([maps[j][h]for h in hs]));need(len(ps)==240,'fresh full240 source cut');sourcecuts.append({'donor':j,'receiver':ii,'native':ii<111,'determinant':det});inverses[ii]=inverse(np.vstack([three[j][h]for h in hs]))
        pairranks=[]
        for h in maps[j]:
            for r in maps[j]:
                if h==r:continue
                cols=[inverses[ii][:,3*visible[j,ii].index(h):3*visible[j,ii].index(h)+3]for ii in sorted(adj[j])if h in visible[j,ii]and r in visible[j,ii]];Z=np.hstack(cols);rk=rank(Z);need(rk<=42 and not np.any(mm(three[j][r],Z)),'every protected propagation pair strictly nonsaturating');pairranks.append([h,r,rk])
        projection_records.append({'donor':j,'maximum':max(t[2]for t in pairranks),'pairs':pairranks});print('FULL_SOURCE',j,max(t[2]for t in pairranks),flush=True)
    need(parity_count==1800,'all five actual source parity caches')
    owners=sorted([r for r in routes if r[4]==1509 and r[0]=='X'],key=key)+sorted([r for r in routes if r[4]==1509 and r[0]=='Y'],key=key);need(owners==dword['owners'],'all35 D owner records unchanged');dindex={(r[0],r[1],r[2]):q for q,r in enumerate(owners)};ingress=np.zeros((35,40),dtype=np.uint8);sections=[];cacheH=[]
    actual_hs=set(h for row in maps.values()for h in row)|{h for h,P in enumerate(planes)if P<=charts[1509]};need(set(map(int,physical))==actual_hs and len(actual_hs)==136,'all134 source H planes and two additional D parents')
    for h in sorted(actual_hs):
        data=physical[str(h)];xs=HX[h];ys=HY.get(h,[]);need(data['X_owners']==xs and data['Y_owners']==ys,'all actual early and late H owners');need(data['ports']==[d for d,Q in enumerate(charts)if planes[h]<=Q],'all45 true H ports');ne,nl=len(xs),len(ys);E=np.array(data['early'],dtype=np.uint8).reshape(ne,ne);B=np.array(data['late'],dtype=np.uint8).reshape(nl,nl);G=np.array(data['cross'],dtype=np.uint8).reshape(nl,ne)
        need(rank(E)==ne-(2 if h==642 else 0)and rank(B)==nl,'full physical phase ranks');need((ne,nl)in [(90,0),(45,45)],'actual H phase counts')
        if h in [263,642]:need(np.array_equal(E,old['H'][str(h)]['physical']['word']),'unchanged actual owner-bound H263/H642 word')
        if np.any(G):cacheH.append({'H':h,'fields':ne,'cross_rank':rank(G)})
        xi={(r[1],r[2]):q for q,r in enumerate(xs)};yi={(r[1],r[2]):q for q,r in enumerate(ys)}
        for j in sorted(planes[h]):
            if j not in donors:continue
            Q=frames[j,h];XE=np.zeros((ne,30),dtype=np.uint8);YL=np.zeros((nl,30),dtype=np.uint8);q=quota[j,h]
            for t,r in enumerate(Xj[j,h]):XE[xi[r[1],r[2]]]=Q[t]
            for t,r in enumerate(Yj.get((j,h),[])):YL[yi[r[1],r[2]]]=Q[q+t]
            RX=mm(E,XE);RY=mm(G,XE)^mm(B,YL)
            for ii in range(120):
                if not planes[h]<=adj[ii]:continue
                xx=[q for q,r in enumerate(xs)if charts[r[4]]<=adj[ii]];yy=[q for q,r in enumerate(ys)if charts[r[4]]<=adj[ii]];A=np.vstack([RX[xx],RY[yy]]);_,ps,det=echelon(A);need(A.shape==(30,30)and len(ps)==30,'full actual donor/H section');sections.append({'donor':j,'H':h,'receiver':ii,'determinant':det})
            if planes[h]<=adj[6]:
                state=mm(block_diag([maps[j][h],maps[j][h]]),LF)
                for phase,rs,values in [('X',xs,mm(RX,state)),('Y',ys,mm(RY,state))]:
                    for q,r in enumerate(rs):
                        if r[4]==1509:ingress[dindex[phase,r[1],r[2]],8*donors.index(j):8*donors.index(j)+8]=values[q]
                        elif charts[r[4]]<=adj[6]:need(not np.any(values[q]),'all full-width wrong-D packets vanish')
    need(len(sections)==5040 and np.array_equal(ingress,dword['ingress'])and np.array_equal(ingress,component['D_data']),'all5040 sections and exact owner-bound full-width D ingress');need(len(cacheH)==22 and sum(r['fields']for r in cacheH)==990,'explicit H cache allocation')
    oldfibres,_=read_json(base/'bit-shared-h-s031-construction/d-aligned-full45-pair/output/FIBRES.json.gz');common_count=0
    for h in [263,642]:
        W=np.array(old['H'][str(h)]['word'],dtype=np.uint8);ps=old['H'][str(h)]['ports']
        for ii,data in oldfibres[str(h)].items():
            ii=int(ii);K=np.array(data['kernel'],dtype=np.uint8);rr=[q for q,d in enumerate(ps)if charts[d]<=adj[ii]];reads=[]
            for s,j in enumerate(sorted(planes[h])):
                X=np.vstack([maps[j][a]for a in visible[j,ii]if a!=h]);need(not np.any(mm(X,K)),'retained full15 common inverse fibre');reads.append(mm(W[np.ix_(rr,range(15*s,15*s+15))],mm(maps[j][h],K)))
            need(rank(reads[0])==15 and all(np.array_equal(reads[0],R)for R in reads[1:]),'retained full15 actual readout');common_count+=1
    need(common_count==72,'all retained full common H views')
    def binary(A):
        A=np.asarray(A,dtype=np.uint8);n,m=A.shape;images=MUL[A[:,:,None],(1<<np.arange(6))[None,None,:]];return((images[:,:,None,:]>>np.arange(6)[None,None,:,None])&1).transpose(0,2,1,3).reshape(6*n,6*m).astype(np.uint8)
    T=np.array(dword['matrix'],dtype=np.uint8);compiler=dword['compiler'];eo=compiler['early_elimination_ADDs'];bo=compiler['late_elimination_ADDs'];go=compiler['late_cross_from_cache_ADDs'];need(len(eo)==6543 and len(bo)==4721 and len(go)==4354,'exact D ADD list lengths')
    expected_labels=[f'D1509-X-cache/{r[1]}/{r[2]}/{bit}'for r in owners[:19]for bit in range(6)];need(compiler['cache_labels']==expected_labels and len(set(expected_labels))==114,'all114 stationary D holder bits bound to incoming original X owners')
    early_state=[1<<q for q in range(114)];cache=[0]*114
    for q in range(114):cache[q]^=early_state[q]
    for target,src in reversed(eo):need(0<=target<114 and 0<=src<114 and target!=src,'early ADD reads only present early owners');early_state[target]^=early_state[src]
    departed=list(early_state);early_state=None
    late_state=[1<<(114+q)for q in range(96)]
    for target,src in reversed(bo):need(0<=target<96 and 0<=src<96 and target!=src,'late phase ADD reads only present late owners');late_state[target]^=late_state[src]
    cross=np.zeros((96,114),dtype=np.uint8)
    for target,src in go:need(0<=target<96 and 0<=src<114,'cross ADD reads only stationary cache and late owners');late_state[target]^=cache[src];cross[target,src]^=1
    need(np.array_equal(cross,binary(T[19:,:19])),'entire late cross list equals G');expected_binary=binary(T);expected_rows=[int.from_bytes(np.packbits(row,bitorder='little').tobytes(),'little')for row in expected_binary];need(departed+late_state==expected_rows,'chronological full D word on all210 arbitrary input columns')
    for q in range(114):cache[q]=0
    need(not any(cache),'every stationary D holder cleared after last use')
    for n,ops,A in [(114,eo,T[:19,:19]),(96,bo,T[19:,19:])]:
        state=[1<<q for q in range(n)]
        for t,s in reversed(ops):state[t]^=state[s]
        expectedA=[int.from_bytes(np.packbits(row,bitorder='little').tobytes(),'little')for row in binary(A)];need(state==expectedA,'pure phase forward map')
        for t,s in ops:state[t]^=state[s]
        need(state==[1<<q for q in range(n)],'pure phase inverse restores originals')
    counts={'INIT':114,'cache_copy_ADDs':114,'dirty_CLEAR':114,'forward_ADDs':len(eo)+len(bo)+len(go)+114,'including_pure_inverse_ADDs':2*(len(eo)+len(bo))+len(go)+114,'extra_MOVE':0}
    need(all(compiler[k]==v for k,v in counts.items()),'all exact D operation counts')
    result={'status':'PASS_INDEPENDENT_FULL_WIDTH_D1509_CACHE_INTERFACE','full_source_geometric_cuts':len(sourcecuts),'full_source_native_cuts':sum(x['native']for x in sourcecuts),'early_bases':earlyrecords,'whole_common_H_readouts':common_count,'physical_H_modules':len(physical),'full_donor_H_sections':len(sections),'protected_propagation_maxima':{str(r['donor']):r['maximum']for r in projection_records},'full_source_bounds':{str(r['donor']):r['maximum']+180 for r in projection_records},'source_parity_fields':parity_count,'H_early_cache_fields':sum(r['fields']for r in cacheH),'D_counts':counts,'D_arbitrary_binary_input_columns':210,'chronological_D_cache_access':True,'full_global_return_replayed':False,'complete_supplier_invoice':False}
    (out/'FULL-RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(out/'FULL-SOURCE-DETERMINANTS.json').write_text(json.dumps(sourcecuts,sort_keys=True,indent=2)+'\n');(out/'H-SECTION-DETERMINANTS.json').write_text(json.dumps(sections,sort_keys=True,indent=2)+'\n');payload=(json.dumps(projection_records,sort_keys=True,separators=(',',':'))+'\n').encode();(out/'PROPAGATION.json.gz').write_bytes(gzip.compress(payload,mtime=0));print(result['status'],315,291,72,136,5040,19,15732,26996,flush=True)
    return result

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--literal',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--package',type=Path,required=True);args=ap.parse_args();repo=args.repo.resolve();base=repo/'research/moonshot-005-program/results';lit,raw=read_json(args.literal)
    for name,digest in json.loads((Path(__file__).resolve().parent/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'frozen source pin '+name)
    source=lit['source'];D=source['D'];i=source['receiver'];need((D,i)==(1509,6),'actual D1509 receiver6 interface');L=np.array(source['L'],dtype=np.uint8);need(L.shape==(48,4)and rank(L)==4,'four-dimensional target space');LL=block_diag([L,L])
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json');roots=root_coordinates(layout,basis);planes=[set(x)for x in layout['A2']];charts=[set(x)for x in layout['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    alloc,_=read_json(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');marked=set(alloc['selected_D']);routes=[json.loads(line)for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()];quota=Counter((r[1],r[3])for r in routes if r[0]=='X'and r[3]is not None)
    maps={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in source['maps'].items()};donors=sorted(maps);need(donors==[0,45,61,62,100],'five supplied complete sources');stars={j:[h for h,P in enumerate(planes)if j in P]for j in donors};visible={};cuts=[]
    for j in donors:
        need(set(maps[j])==set(stars[j])and all(F.shape==(3,48)for F in maps[j].values()),'whole28-plane width3 source')
        for ii in sorted(adj[j]):
            hs=[h for h in stars[j]if planes[h]<=adj[ii]];visible[j,ii]=hs;need(len(hs)==16,'geometric source view');_,p,det=echelon(np.vstack([maps[j][h]for h in hs]));need(len(p)==48 and det,'full48 source determinant');cuts.append({'donor':j,'receiver':ii,'native':ii<111,'determinant':det})
    frames={tuple(map(int,key.split('/'))):np.array(M,dtype=np.uint8)for key,M in lit['source_frames'].items()};early=[]
    for j in donors:
        rows=[]
        for h in stars[j]:
            T=frames[j,h];need(T.shape==(6,6)and rank(T)==6,'full local six-coordinate frame');q=quota[j,h]//5;need(q in [3,6]and quota[j,h]==5*q,'actual protected early quota');rows.append(mm(T[:q],block_diag([maps[j][h],maps[j][h]])))
        E=np.vstack(rows);need(E.shape==(96,96)and np.array_equal(E,lit['early'][str(j)]),'literal early96 matrix');_,p,det=echelon(E);need(len(p)==96 and det,'genuine invertible early96 basis');early.append({'donor':j,'determinant':det,'seed':lit['early_seeds'][str(j)]})
    providers={int(h):row for h,row in lit['providers'].items()};need(set(providers)==set(h for row in maps.values()for h in row),'all H providers on all five source stars');left={j:{}for j in donors};provider_stats=[]
    moving,_=read_json(base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz');rankone,_=read_json(base/'bit-shared-h-s031-construction/rank-one-overlap/SOURCE-COEFFICIENTS.json.gz')
    for h,pv in providers.items():
        ds=sorted(j for j in planes[h]if j<111);ps=[d for d,Q in enumerate(charts)if planes[h]<=Q and d in marked];need(pv['donors']==ds and pv['ports']==ps and len(ps)==9,'native H donors and current physical ports');E=np.array(pv['early'],dtype=np.uint8);need(E.shape==(9,9),'nine early H fields')
        if h in [263,642]:need(np.array_equal(E,moving['Hwords']['263']if h==263 else rankone['Bword']),'unchanged accepted H provider')
        if pv['kind']=='double':
            need(len(ds)==3 and all(quota[j,h]==30 for j in ds),'actual all-double H quotas')
            for s,j in enumerate(ds):
                if j in maps:M=mm(E[:,3*s:3*s+3],maps[j][h]);left[j][h]={'X':block_diag([M,M]),'Y':np.zeros((0,96),dtype=np.uint8)}
        else:
            B=np.array(pv['late'],dtype=np.uint8);G=np.array(pv['cross'],dtype=np.uint8);need(B.shape==G.shape==(9,9)and rank(E)==rank(B)==9,'invertible early and late H blocks')
            if pv['kind']=='single':
                need(len(ds)==3 and all(quota[j,h]==15 for j in ds)and not np.any(G),'actual all-single H quotas')
                for s,j in enumerate(ds):
                    if j not in maps:continue
                    S=mm(frames[j,h],block_diag([maps[j][h],maps[j][h]]));left[j][h]={'X':mm(E[:,3*s:3*s+3],S[:3]),'Y':mm(B[:,3*s:3*s+3],S[3:])}
            else:
                need(pv['kind']=='partial'and len(ds)==2,'one partial H branch');large,small=pv['large'],pv['small'];need(set([large,small])==set(ds)and quota[large,h]==30 and quota[small,h]==15 and not np.any(G[:,6:]),'actual partial H quotas/cross block')
                for j in ds:
                    if j not in maps:continue
                    S=mm(frames[j,h],block_diag([maps[j][h],maps[j][h]]));left[j][h]={'X':mm(E[:,:6],S)if j==large else mm(E[:,6:],S[:3]),'Y':mm(G[:,:6],S)if j==large else mm(B[:,:3],S[3:])}
        provider_stats.append({'H':h,'kind':pv['kind'],'early_rank':rank(E),'nonzero_cross':pv['kind']!='double'and bool(np.any(pv['cross']))})
    prefix=[]
    for j in donors:
        for ii in sorted(adj[j]):
            rows=[]
            for h in visible[j,ii]:
                pv=providers[h];pos=[q for q,d in enumerate(pv['ports'])if charts[d]<=adj[ii]];need(len(pos)==3,'actual three visible protected D ports')
                if pv['kind']=='double':rows.extend(left[j][h]['X'][pos+[q+9 for q in pos]])
                else:rows.extend(left[j][h]['X'][pos]);rows.extend(left[j][h]['Y'][pos])
            M=np.array(rows,dtype=np.uint8);_,ps,det=echelon(M);need(M.shape==(96,96)and len(ps)==96,'complete actual six-per-H source prefix');prefix.append({'donor':j,'receiver':ii,'native':ii<111,'determinant':det})
        print('PREFIX',j,63,flush=True)
    Hrecords=[]
    for h in [263,642]:
        ds=sorted(planes[h]);word=np.array(providers[h]['early'],dtype=np.uint8);ps=providers[h]['ports'];views=[ii for ii in range(120)if planes[h]<=adj[ii]];cores=[]
        for ii in views:
            K=null(np.vstack([maps[ds[0]][a]for a in visible[ds[0],ii]if a!=h]));need(K.shape==(48,3),'whole H inverse fibre');pos=[q for q,d in enumerate(ps)if charts[d]<=adj[ii]];reads=[]
            for s,j in enumerate(ds):
                need(not np.any(mm(np.vstack([maps[j][a]for a in visible[j,ii]if a!=h]),K)),'retained whole common fibre');reads.append(mm(word[np.ix_(pos,range(3*s,3*s+3))],mm(maps[j][h],K)))
            need(rank(reads[0])==3 and all(np.array_equal(reads[0],R)for R in reads[1:]),'retained complete H readout');cores.append(K)
        Hrecords.append({'H':h,'geometric_views':len(views),'native_views':sum(ii<111 for ii in views),'core_rank':rank(np.hstack(cores))})
    owners=sorted([r for r in routes if r[4]==D and r[0]=='X'],key=lambda r:(r[1],r[2]))+sorted([r for r in routes if r[4]==D and r[0]=='Y'],key=lambda r:(r[1],r[2]));need(owners==lit['D_owners']and len(owners)==35 and sum(r[0]=='X'for r in owners)==19,'all actual35 D owners in chronological phase order')
    Hinside=[h for h,P in enumerate(planes)if P<=charts[D]];need(len(Hinside)==16,'all16 actual in-D H planes');indices={}
    for h in Hinside:
        ids=[q for q,r in enumerate(owners)if r[3]==h];need(len(ids)==2,'actual two packets from each H');indices[h]=ids
    need(sum(r[3]is None for r in owners)==3,'three additional Hub-route owners retained')
    M=np.zeros((35,8*len(donors)),dtype=np.uint8);line={int(h):np.array(v,dtype=np.uint8)for h,v in source['lines'].items()};dual={int(j):{int(h):np.array(v,dtype=np.uint8)for h,v in row.items()}for j,row in source['dual_rows'].items()}
    for t,j in enumerate(donors):
        inside=[h for h in stars[j]if planes[h]<=charts[D]];need(inside==source['inside'][str(j)]and len(inside)==4,'four true in-D source planes');W=np.column_stack([line[h]for h in inside]);R=np.vstack([dual[j][h]for h in inside]);need(np.array_equal(mm(W,R),np.eye(4,dtype=np.uint8)),'literal four-line source coordinate basis')
        for h in inside:
            pv=providers[h];q=pv['ports'].index(D)
            pieces=[left[j][h]['X'][q:q+1],left[j][h]['X'][q+9:q+10]]if pv['kind']=='double'else[left[j][h]['X'][q:q+1],left[j][h]['Y'][q:q+1]]
            for copy,A in enumerate(pieces):
                value=mm(A,LL);expected=np.zeros((1,8),dtype=np.uint8);expected[0,4*copy:4*copy+4]=dual[j][h];need(np.array_equal(value,expected),'actual phase packet is the intended D dual row');M[indices[h][copy],8*t:8*t+8]=value[0]
        for h in visible[j,i]:
            pv=providers[h];pos=[q for q,d in enumerate(pv['ports'])if d!=D and charts[d]<=adj[i]]
            for phase,A in left[j][h].items():
                use=pos+[q+9 for q in pos]if phase=='X'and pv['kind']=='double'else pos if len(A)else[];need(not np.any(mm(A[use],LL)),'every other actual H packet vanishes on both target copies')
    need(np.array_equal(M,lit['D_data']),'literal35-owner ingress matrix')
    T=np.array(lit['D_word'],dtype=np.uint8);Ti=np.array(lit['D_inverse'],dtype=np.uint8);need(T.shape==Ti.shape==(35,35)and np.array_equal(mm(T,Ti),np.eye(35,dtype=np.uint8)),'full D matrix and inverse');need(not np.any(T[:19,19:])and rank(T[:19,:19])==19 and rank(T[19:,19:])==16,'causal block support and invertible diagonal blocks')
    input_sections={j:sorted(q for h in Hinside if j in planes[h]for q in indices[h])for j in sorted(charts[D])};audience=[ii for ii in range(120)if charts[D]<=adj[ii]];output_sections={ii:[q for q,r in enumerate(owners)if r[5]is not None and ii in planes[r[5]]]for ii in audience}
    need(len(input_sections)==len(output_sections)==12 and all(len(s)==8 for s in list(input_sections.values())+list(output_sections.values())),'twelve geometric8-field input and output sections');need({str(j):s for j,s in input_sections.items()}==lit['all_D_input_indices']and {str(j):s for j,s in output_sections.items()}==lit['all_D_output_indices'],'literal actual D sections')
    minors=[]
    for j,inn in input_sections.items():
        for ii,out in output_sections.items():
            A=T[np.ix_(out,inn)];_,ps,det=echelon(A);need(len(ps)==8 and det,'all sectional8-by8 minors');minors.append({'donor':j,'receiver':ii,'native':j<111 and ii<111,'determinant':det})
    target=output_sections[i];need(target==lit['D_output_indices']and len([q for q in target if q<19])==4,'four early and four late target outputs');need(np.array_equal(mm(T[target],M),np.tile(np.eye(8,dtype=np.uint8),(1,5))),'exact common eight-coordinate target sum')
    args.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_INDEPENDENT_D1509_LOCAL_SOURCE_MATRIX_INTERFACE','source_geometric_cuts':len(cuts),'source_native_cuts':sum(x['native']for x in cuts),'left_prefix_geometric_cuts':len(prefix),'left_prefix_native_cuts':sum(x['native']for x in prefix),'early_bases':early,'retained_H':Hrecords,'D_actual_owners':35,'D_early_owners':19,'D_late_owners':16,'D_sectional_geometric_minors':len(minors),'D_sectional_native_minors':sum(x['native']for x in minors),'D_cross_rank':rank(T[19:,:19]),'target_receiver':i,'target_dimension':8,'supplied_source_donors':donors,'missing_native_D_donors':sorted(j for j in charts[D]if j<111 and j not in donors),'H_provider_counts':dict(Counter(x['kind']for x in provider_stats)),'H_nonzero_cross_blocks':sum(x['nonzero_cross']for x in provider_stats),'literal_payload_sha256':hashlib.sha256(raw).hexdigest(),'author_executable_imports':False,'chronological_cache_compiler_reviewed':False,'complete_H_common_readouts_beyond_two':False,'full45_component_assembled':False,'complete_return':False,'complete_invoice':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(args.out/'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps(cuts,sort_keys=True,indent=2)+'\n');(args.out/'PREFIX-DETERMINANTS.json').write_text(json.dumps(prefix,sort_keys=True,indent=2)+'\n');(args.out/'D-SECTION-MINORS.json').write_text(json.dumps(minors,sort_keys=True,indent=2)+'\n');print(result['status'],315,291,72,67,35,19,16,144,121,8,flush=True)
    if args.package:full_review(args.package,base,lit,maps,donors,planes,charts,adj,visible,quota,routes,args.out)

if __name__=='__main__':main()
