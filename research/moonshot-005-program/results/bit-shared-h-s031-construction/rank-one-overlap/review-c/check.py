#!/usr/bin/env python3
"""Independent rank-one-overlap two-centre component review.

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


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();repo=args.repo.resolve();here=Path(__file__).resolve().parent
    for p,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/p).read_bytes()).hexdigest()==digest,'pin '+p)
    base=repo/'research/moonshot-005-program/results';author=base/'bit-shared-h-s031-construction/rank-one-overlap'
    raw_coeff,raw=read_json(author/'SOURCE-COEFFICIENTS.json.gz');literal,_=read_json(author/'LITERAL-PROVIDER.json')
    old,_=read_json(base/'bit-shared-h-s031-construction/moving-fibres/output/COEFFICIENTS.json.gz')
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz')
    basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json');roots=root_coordinates(layout,basis)
    planes,charts=[set(x)for x in layout['A2']],[set(x)for x in layout['D4']]
    adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    h=642;donors=sorted(planes[h]);views=[i for i in range(120)if planes[h]<=adj[i]]
    need(donors==[45,61,100]and len(views)==36 and len(set(views)&set(range(111)))==34 and 80 not in views,'actual native identity-target chart')
    prm,_=read_json(base/'bit-coupled-native-geometric-cycle-source/component/output/PARAMETERS.json');prm=prm['local']['642']
    u,v=(roots[j]for j in donors[:2]);perp={x for x in range(256)if not polar(x,u)and not polar(x,v)}
    sb,tb=witt(perp,quadratic),witt(range(64),q)
    node={xor(sb[s]for s in range(6)if mask>>s&1):xor(tb[s]for s in range(6)if mask>>s&1)for mask in range(64)}
    need(len(node)==64 and all(quadratic(x)==q(a)for x,a in node.items()),'actual quadratic isometry')
    omega=prm['omega'];coords={xor(prm['F4_basis'][s]for s in range(6)if mask>>s&1):tuple(((mask>>(2*t))&1)^int(MUL[omega,(mask>>(2*t+1))&1])for t in range(3))for mask in range(64)}
    need(len(coords)==64 and power(omega,2)^omega==1 and all(q(a)==xor(power(t,3)for t in r)for a,r in coords.items()),'actual Hermitian coordinates')
    reverse={r:a for a,r in coords.items()};rotation={a:reverse[tuple(int(MUL[omega,t])for t in r)]for a,r in coords.items()}
    radicals={}
    for d,D in enumerate(charts):
        if planes[h]<=D:
            span=binary_span(roots[j]for j in D)
            radical=sorted(x for x in span if all(not polar(x,y)for y in span))
            need(len(span)==16 and len(radical)==4 and set(radical)<=perp,'actual D radical')
            radicals[d]=radical
    ports=[d for d,R in radicals.items()if all(rotation[node[x]]in {node[y]for y in R}for x in R)]
    need(ports==prm['ports']==[302,594,673,1089,1297,1509,1726,2230,3067],'actual selected Desarguesian nine ports')
    E=np.array([[power(t,2)for t in coords[node[radicals[d][1]]]]for d in ports],dtype=np.uint8)
    E2=np.array([[MUL[x,x],MUL[y,y],MUL[z,z],MUL[x,y],MUL[x,z],MUL[y,z]]for x,y,z in E],dtype=np.uint8)
    N=null(E2.T).T
    need(rank(E)==3 and rank(E2)==6 and N.shape==(3,9),'linear and quadratic chart ranks')
    m,n,p=(np.array(literal[x],dtype=np.uint8)for x in ['m','n','p'])
    need(all(m)and all(n)and all(m^n)and not np.any(mm(np.vstack([m,n]),E2)),'three nowhere-zero annihilator weights')
    _,cols,_=echelon(N);Ni=inverse(N[:,cols]);um=mm(m[cols][None,:],Ni)[0];un=mm(n[cols][None,:],Ni)[0]
    def complete(first):
        rows=[first]
        for row in np.eye(3,dtype=np.uint8):
            if rank(np.array(rows+[row],dtype=np.uint8))>len(rows):rows.append(row)
            if len(rows)==3:return np.array(rows,dtype=np.uint8)
        raise AssertionError('basis completion')
    t=MUL[n,INV[m]]
    W=[mm(complete(um^un),MUL[N,INV[t^1]]),mm(complete(um),N),mm(complete(un),MUL[N,INV[t]])]
    need(all(np.array_equal(X[0],m)for X in W)and rank(np.vstack(W))==7,'rank-seven common-row degeneration')
    a=MUL[MUL[m,p],INV[t^1]];b=MUL[MUL[m,p],INV[t]]
    G=np.vstack([m,a,a^b]+[row for X in W for row in X[1:]])
    Q=np.zeros((9,9),dtype=np.uint8);Q[1,[0,3]]=1;Q[2,[0,6]]=1
    for row,col in enumerate([1,2,4,5,7,8],3):Q[row,col]=1
    P=mm(inverse(G),Q)
    need(rank(G)==9 and rank(P)==8 and np.array_equal(P,literal['word'])and np.array_equal(P,raw_coeff['Bword']),'literal rank-eight provider rebuilt')
    need(np.array_equal(t,literal['weights']),'literal coefficient weights')
    maps={int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in raw_coeff['maps'].items()}
    nodes={int(j):{int(a):int(v)for a,v in row.items()}for j,row in old['base_nodes'].items()}
    need(set(maps)==set(nodes)=={0,45,61,62,100},'five complete literal donors')
    stars={j:[p for p,S in enumerate(planes)if j in S]for j in maps}
    I=np.eye(3,dtype=np.uint8);ev=lambda a:kron(np.array([[power(a,d)for d in range(16)]],dtype=np.uint8),I)
    rho=np.array(raw_coeff['r'],dtype=np.uint8)[:,None];lam=np.array(raw_coeff['lambda'],dtype=np.uint8)[None,:]
    need(rho[:,0].tolist()==[32,42,1]and lam[0].tolist()==[17,33,59]and rank(mm(rho,lam))==1,'literal rank-one amplitude')
    expected={0:[116,263],45:[642],61:[263,642],62:[263,643],100:[642]}
    qnodes={a for a in range(64)if not q(a)}
    blockset={frozenset(a for a in qnodes if field_polar(v,a)==(q(v)^1)):v for v in range(1,64)}
    cuts=[];visible={};parameters={}
    for j in sorted(maps):
        need(set(maps[j])==set(nodes[j])==set(stars[j])and set(nodes[j].values())==qnodes,'all actual source planes and nodes')
        need(all(M.shape==(3,48)and np.all(M<64)for M in maps[j].values()),'literal source dimensions')
        edits=[a for a in stars[j]if not np.array_equal(maps[j][a],ev(nodes[j][a]))]
        need(edits==expected[j],'exact one/two edit locations')
        seen=set()
        for i in sorted(adj[j]):
            hs=[a for a in stars[j]if planes[a]<=adj[i]];visible[j,i]=hs
            need(len(hs)==16,'sixteen actual source planes')
            B=frozenset(nodes[j][a]for a in hs);need(B in blockset,'actual geometric source incidence')
            vv=blockset[B];seen.add(vv);parameters[j,i]=vv
            M=np.vstack([maps[j][a]for a in hs]);_,ps,det=echelon(M)
            need(len(ps)==48 and det!=0,'complete source cut')
            cuts.append({'donor':j,'receiver':i,'native':i<111,'planes':hs,'parameter':vv,'determinant':det})
        need(seen==set(range(1,64)),'all63 source blocks once')
    Bfibres={};Aformula={};P0=[];Pb=[];pencil_records={};zero=np.zeros((3,3),dtype=np.uint8)
    for i in views:
        vv=parameters[61,i];Ub=u_polynomial(vv,60)[:,None];Kb=kron(Ub,I);Bfibres[i]=Kb
        r=np.array(coords[node[roots[i]]],dtype=np.uint8)[:,None];s=mm(E,r)[:,0];V=MUL[s[:,None],E]
        D=[mm(W[0],MUL[t[:,None],V]),mm(W[1],MUL[t[:,None],V]),mm(W[2],V)]
        D[0][0]=mm(a[None,:],V)[0];D[1][0]=mm(MUL[m,p][None,:],V)[0];D[2][0]=mm(b[None,:],V)[0]
        need(all(np.array_equal(M,literal['pencils'][str(i)][j])for j,M in enumerate(D)),'all specialised literal pencils')
        need(all(np.array_equal(mm(maps[j][642],Kb),D[z])and rank(D[z])==3 for z,j in enumerate(donors)), 'actual transplanted source pencils')
        A=np.hstack([MUL[t[:,None],V],V]);F=np.block([[D[0],D[0]],[D[1],zero],[zero,D[2]]])
        need(np.array_equal(mm(G,A),mm(Q,F))and np.array_equal(mm(P,F),A),'specialised finite provider identity')
        need(not np.any(mm(D[1][1:],rho)),'fixed right kernel for lower two pencil rows')
        value=mm(D[1],rho);need(value[0,0]!=0 and not np.any(value[1:]),'nonzero first-axis source action')
        pencil_records[str(i)]={'pencil_determinants':[echelon(M)[2]for M in D],'rho_scalar':int(value[0,0])}
        if planes[263]<=adj[i]:
            Ka=kron(u_polynomial(vv,0)[:,None],I);P0.append(Ka);Pb.append(Kb)
            target=np.zeros((3,3),dtype=np.uint8);target[0]=MUL[value[0,0],lam[0]]
            need(np.array_equal(mm(maps[61][642],Ka),target),'entire rank-one overlap prescription')
            correction=kron(Ub,mm(rho,lam));Knew=Ka^correction
            need(rank(correction)==1 and rank(Knew)==3 and not np.any(mm(maps[61][642],Knew)),'explicit rank-one fibre correction')
            Aformula[i]=Knew
    P0=np.hstack(P0);Pb=np.hstack(Pb)
    need(len(Aformula)==20 and rank(P0)==rank(Pb)==15 and rank(np.hstack([P0,Pb]))==30,'two disjoint old propagation spaces')
    Bcore=np.hstack(list(Bfibres.values()))
    need(rank(Bcore)==18 and rank(np.hstack([Bcore,P0]))==30,'full second-core and first-propagation intersection has dimension3')
    need(rank(mm(maps[61][642],P0))==1,'global first-propagation action is exactly rank one')
    for j,companion in [(0,116),(61,642),(62,643)]:
        need(nodes[j][263]==0 and nodes[j][companion]==60,'actual reflected source nodes')
        need(np.array_equal(maps[j][companion],maps[61][642]),'copied companion quotient')
        need(np.array_equal(maps[j][263],np.array(old['maps'][str(j)]['263'],dtype=np.uint8)),'first central quotient retained')
        need(not np.any(mm(maps[j][263],Pb)),'first central quotient annihilates companion propagation')
    ports_by={263:[110,132,720,810,1509,1735,1994,2621,2836],642:ports}
    words={263:np.array(old['Hwords']['263'],dtype=np.uint8),642:P}
    witness,_=read_json(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');selected=set(witness['selected_D'])
    fibres={};Hreceipts=[];moved=[];omitted=[]
    for centre in [263,642]:
        ds=sorted(planes[centre]);rs=[i for i in range(120)if planes[centre]<=adj[i]]
        need(ports_by[centre]==[d for d in sorted(selected)if planes[centre]<=charts[d]],'actual selected physical ports')
        need(rank(words[centre])==(9 if centre==263 else 8),'actual provider ranks9/8')
        fibres[str(centre)]={};joined=[]
        for i in rs:
            K=[]
            for j in ds:
                off=[a for a in visible[j,i]if a!=centre];X=np.vstack([maps[j][a]for a in off]);T=null(X)
                need(X.shape==(45,48)and T.shape==(48,3),'whole off-H inverse fibre')
                K.append(T)
            need(all(rank(np.hstack([K[0],T]))==3 for T in K[1:]),'three full uncertainty fibres coincide')
            indices=[p for p,d in enumerate(ports_by[centre])if charts[d]<=adj[i]]
            need(len(indices)==3,'three actual visible ports')
            reads=[mm(words[centre][np.ix_(indices,range(3*z,3*z+3))],mm(maps[j][centre],K[0]))for z,j in enumerate(ds)]
            need(rank(reads[0])==3 and all(np.array_equal(reads[0],R)for R in reads[1:]),'full common physical readout')
            if centre==642:
                need(rank(np.hstack([K[0],Bfibres[i]]))==3,'second-centre fibres are unchanged geometric fibres')
            else:
                vv=parameters[61,i];oldK=kron(u_polynomial(vv,0)[:,None],I)
                want=Aformula.get(i,oldK)
                need(rank(want)==3 and rank(np.hstack([K[0],want]))==3,'explicit rank-one formula equals entire new fibre')
                changed=rank(np.hstack([K[0],oldK]))>3
                need(changed==(i in Aformula),'exactly the20 prescribed fibres move')
                if changed:
                    moved.append(i)
                    old_off=np.vstack([ev(nodes[0][a])if a==116 else maps[0][a]for a in visible[0,i]if a!=263])
                    restored=null(old_off);need(rank(np.hstack([restored,K[0]]))==4,'omitted reflected edit destroys the common fibre')
                    omitted.append(i)
            fibres[str(centre)][str(i)]={'kernel':K[0].tolist(),'readout':reads[0].tolist(),'ports':[ports_by[centre][p]for p in indices]}
            joined.append(K[0])
        core_rank=rank(np.hstack(joined));need(core_rank==(22 if centre==263 else 18),'exact two-centre core ranks22/18')
        Hreceipts.append({'H':centre,'donors':ds,'ports':ports_by[centre],'geometric_receivers':len(rs),
                          'native_receivers':len(set(rs)&set(range(111))),'provider_rank':rank(words[centre]),'core_rank':core_rank})
    S0=np.column_stack([u_polynomial(1<<s,0)for s in range(6)]);Sb=np.column_stack([u_polynomial(1<<s,60)for s in range(6)])
    envelope=np.hstack([kron(S0,I),kron(Sb,rho)])
    need(rank(envelope)==22 and len(moved)==20,'rank-one22-dimensional envelope attained')
    complement=np.zeros((1,9),dtype=np.uint8);complement[0,0]=1
    kernel=np.zeros((9,1),dtype=np.uint8);kernel[[0,3,6]]=1
    need(not np.any(mm(P,kernel))and mm(complement,kernel)[0,0]==1 and rank(np.vstack([P,complement]))==9,'one paid coordinate repairs specialised provider')
    quota=Counter();actual_exits={263:set(),642:set()}
    for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,owner,_,plane,d,_,source,_=json.loads(line)
        if phase=='X'and plane is not None:
            need(owner==source,'original early owner');quota[owner,plane]+=1
            if plane in actual_exits:actual_exits[plane].add(d)
    need(Counter(quota.values())=={15:2675,30:422,45:11}and all(set(ports_by[h])<=actual_exits[h]for h in ports_by),'actual early quota census and exits')
    early=[];early_matrices={}
    for j in sorted(maps):
        source_chart=263 if j in [0,61,62]else 642;rows=[]
        need(max(quota[j,a]for a in stars[j])==30,'ordinary source donor')
        for plane in stars[j]:
            F=maps[j][plane];count=quota[j,plane]//15;need(count in [1,2],'one/two-lane quota')
            if count==2:rows.append(kron(np.eye(2,dtype=np.uint8),F))
            elif plane in [263,642]:rows.append(np.hstack([F,np.zeros_like(F)]))
            else:
                tag=f'early/{source_chart}/3/{j}/{plane}/0';frame=np.frombuffer(hashlib.shake_256(tag.encode('ascii')).digest(18),dtype=np.uint8).reshape(3,6)&63
                need(rank(frame)==3,'full local early frame');rows.append(np.hstack([mm(frame[:,:3],F),mm(frame[:,3:],F)]))
        M=np.vstack(rows);_,ps,det=echelon(M)
        need(M.shape==(96,96)and len(ps)==96,'full actual early source basis')
        early.append({'donor':j,'seed':0,'rank':96,'determinant':det,'source_chart':source_chart});early_matrices[str(j)]=M.tolist()
    def divided(degree,a):
        return np.array([power(a,degree-m)if m<=degree else 0 for m in range(16)],dtype=np.uint8)
    cores={a:np.column_stack([u_polynomial(1<<s,a)for s in range(6)])for a in qnodes}
    for x,S in cores.items():
        D=[divided(d,x)for d in [0,1,3,7,13,4,15]]
        basis=np.column_stack([D[0],D[1],D[2],D[3],D[4]^D[5],D[6]])
        need(rank(S)==rank(basis)==rank(np.hstack([S,basis]))==6,'exact six-dimensional core formula')
        high=np.zeros(16,dtype=np.uint8);high[15]=1;high[14]=x
        need(np.array_equal(D[6]^MUL[power(x,2),D[4]],high),'universal high-degree core identity')
        for y,T in cores.items():
            if x!=y:need(rank(np.hstack([S,T]))==10,'two-core envelope dimension10')
    first=min(adj[0]&set(range(111)));full=np.vstack([maps[0][a]for a in visible[0,first]])
    need(rank(full)==48 and rank(full[:-3])==45,'deleted source quotient loses three dimensions')
    prior_fibres,_=read_json(base/'bit-shared-h-s031-construction/moving-fibres/output/FIBRES.json.gz')
    prior_core=rank(np.hstack([np.array(row['kernel'],dtype=np.uint8)for row in prior_fibres['263'].values()]))
    need(prior_core==30,'prior moving-fibre core comparison')
    args.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_INDEPENDENT_RANK_ONE_OVERLAP_TWO_H','source_cuts':len(cuts),'native_source_cuts':sum(x['native']for x in cuts),
            'H':Hreceipts,'overlap_action_rank':1,'moved_receivers':moved,'omitted_copy_failures':omitted,
            'propagation_old_spaces':[15,15,30],'second_core_first_propagation_union':30,'rank_one_envelope':22,'prior_first_core_rank':prior_core,
            'actual_early_bases':early,'one_edit_bound':27,'two_edit_bound':36,'saturation_threshold':45,
            'paid_complement_dimension':1,'provider_rank_certificate':certificate(P),'source_payload_sha256':hashlib.sha256(raw).hexdigest(),
            'author_executable_imports':False,'all45ports':False,'complementary_width12':False,'complete_global_word':False,
            'complete_invoice':False,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps(cuts,indent=2,sort_keys=True)+'\n')
    payload={'whole_fibres':fibres,'pencil_checks':pencil_records,'early_matrices':early_matrices,'complement':complement.tolist()}
    (args.out/'MATRICES.json.gz').write_bytes(gzip.compress((json.dumps(payload,sort_keys=True,separators=(',',':'))+'\n').encode(),mtime=0))
    print(result['status'],315,291,72,22,18,1,flush=True)

if __name__=='__main__':main()
