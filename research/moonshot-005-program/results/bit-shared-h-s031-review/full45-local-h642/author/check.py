#!/usr/bin/env python3
"""Full45-port local H642 with a protected rank-eight block and width12 complement.

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

def generic_module(module,ports,radicals,points,views,exteriors,adj,charts):
    word=np.array([[power(q+1,d)for d in range(9)]for q in range(9)],dtype=np.uint8)
    need(rank(word)==9,'generic physical provider invertible')
    controls=[np.eye(48,dtype=np.uint8)[3*j:3*j+3]for j in range(3)]
    found_core=None
    for core_seed in range(128):
        core={}
        for q,d in enumerate(ports):
            difference=np.zeros((2,18),dtype=np.uint8)
            difference[:,:3]=word[q,:3];difference[0,3:6]=word[q,3:6];difference[1,6:9]=word[q,6:9]
            for attempt in range(128):
                change=coefficients(f'full45-H642/{module}/core/{core_seed}/{d}/{attempt}',(2,2))
                if rank(change)==2:break
            else:raise AssertionError('local core basis search')
            rows=np.vstack([np.zeros((1,18),dtype=np.uint8),mm(change,difference)]);rows[:,9+q]=1
            for point,row in zip(radicals[d],rows):
                need(point not in core,'spread has no repeated point');core[point]=row
        need(set(core)==set(points),'spread covers all27 source points')
        if not all(rank(np.array([core[x]for x in S],dtype=np.uint8))==16 for S in exteriors):continue
        for i in views:
            inside=[x for x in points if not polar(x,ROOT_MASKS[i])]
            C=np.array([core[x]for x in inside],dtype=np.uint8)
            need(len(inside)==15 and rank(C)==15,'all H-visible core cuts')
            need(all(rank(np.vstack([C,F[:,:18]]))==18 for F in controls),'every central control completes the core')
        found_core=core;break
    need(found_core is not None,'found a core for every exterior cut')
    tail={x:hermite(q+1)for q,x in enumerate(points)}
    table=None
    for fill_seed in range(128):
        trial={x:np.vstack([np.r_[core[x],np.zeros(30,dtype=np.uint8)],
                           np.hstack([coefficients(f'full45-H642/{module}/fill/{fill_seed}/{x}',(2,18)),tail[x]])])for x in points}
        if all(rank(np.vstack([trial[x]for x in S]))==48 for S in exteriors):table=trial;break
    need(table is not None,'found full literal exterior source views')
    return {'word':word,'controls':controls,'table':table,'core_seed':core_seed,'fill_seed':fill_seed}

def main():
    global ROOT_MASKS
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();repo=args.repo.resolve();here=Path(__file__).resolve().parent
    for name,digest in json.loads((here/'SOURCE-PINS.json').read_text())['files'].items():
        need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'pin '+name)
    base=repo/'research/moonshot-005-program/results'
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json')
    roots=root_coordinates(layout,basis);ROOT_MASKS=roots
    planes,charts=[set(x)for x in layout['A2']],[set(x)for x in layout['D4']]
    adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    h=642;donors=sorted(planes[h]);views=[i for i in range(120)if planes[h]<=adj[i]]
    need(donors==[45,61,100]and len(views)==36 and 80 not in views,'actual ordinary identity-target H642')
    all_ports=[d for d,D in enumerate(charts)if planes[h]<=D];need(len(all_ports)==45,'all45 actual H exits')
    first,second=(roots[j]for j in donors[:2]);project=lambda x:x^(first if polar(x,second)else 0)^(second if polar(x,first)else 0)
    stars={j:[a for a,P in enumerate(planes)if j in P]for j in donors};point={}
    for j in donors:
        point[j]={}
        for a in stars[j]:
            if a==h:continue
            labels={project(roots[t])for t in planes[a]-{j}};need(len(labels)==1,'unique projected source point');point[j][a]=labels.pop()
    points=sorted(point[donors[0]].values())
    need(len(points)==len(set(points))==27 and all(x and not quadratic(x)for x in points),'actual27 singular source points')
    need(all(set(p.values())==set(points)for p in point.values()),'three identical point-labelled source stars')
    radicals={}
    for d in all_ports:
        span=binary_span(roots[j]for j in charts[d]);R=sorted(x for x in span if x and all(not polar(x,y)for y in span))
        need(len(R)==3 and set(R)<=set(points),'actual D radical line');radicals[d]=R
    partition=json.loads((here/'PARTITION.json').read_text())['spreads']
    need(len(partition)==5 and sorted(d for S in partition for d in S)==all_ports,'partition of all45 physical ports')
    for S in partition:
        need(len(S)==9 and sorted(x for d in S for x in radicals[d])==points,'each module is a genuine nine-line spread')
        need(all(sum(charts[d]<=adj[i]for d in S)==3 for i in views),'each receiver sees three ports per module')
    exteriors=sorted({tuple(x for x in points if polar(x,t))for t in points})
    need(len(exteriors)==27 and all(len(S)==16 for S in exteriors),'all27 geometric exterior cuts')
    visible={(j,i):[a for a in stars[j]if planes[a]<=adj[i]]for j in donors for i in adj[j]}
    for j in donors:
        exterior_actual={tuple(sorted(point[j][a]for a in visible[j,i]))for i in adj[j]if h not in visible[j,i]}
        need(exterior_actual==set(exteriors),'all actual off-centre source views equal the exterior family')
    protected,_=read_json(base/'bit-shared-h-s031-construction/rank-eight-provider/output/COEFFICIENTS.json.gz')
    need(protected['ports']==partition[0]and protected['H']==h,'protected module occupies the first spread')
    modules=[{'word':np.array(protected['Hword'],dtype=np.uint8),'maps':{int(j):{int(a):np.array(M,dtype=np.uint8)for a,M in row.items()}for j,row in protected['source_maps'].items()},'core_seed':None,'fill_seed':None}]
    for z in range(1,5):
        module=generic_module(z,partition[z],radicals,points,views,exteriors,adj,charts)
        module['maps']={j:{**{a:module['table'][x]for a,x in point[j].items()},h:module['controls'][s]}for s,j in enumerate(donors)}
        modules.append(module)
        print('BUILT_NONCLASSICAL_MODULE',z,module['core_seed'],module['fill_seed'],flush=True)
    module_cuts=[];module_receipts=[];module_fibres=[]
    for z,module in enumerate(modules):
        m_maps=module['maps'];determinants={}
        for j in donors:
            need(set(m_maps[j])==set(stars[j]),'complete module source star')
            for i in sorted(adj[j]):
                hs=visible[j,i];need(len(hs)==16,'actual16-plane source cut')
                M=np.vstack([m_maps[j][a]for a in hs]);_,ps,det=echelon(M)
                need(M.shape==(48,48)and len(ps)==48 and det!=0,'all module source views invertible')
                determinants[j,i]=det;module_cuts.append({'module':z,'donor':j,'receiver':i,'determinant':det})
        fibres={}
        for i in views:
            off=[a for a in visible[donors[0],i]if a!=h];K=null(np.vstack([m_maps[donors[0]][a]for a in off]))
            need(K.shape==(48,3),'whole module fibre dimension3')
            positions=[p for p,d in enumerate(partition[z])if charts[d]<=adj[i]];reads=[]
            for s,j in enumerate(donors):
                X=np.vstack([m_maps[j][a]for a in visible[j,i]if a!=h]);need(not np.any(mm(X,K)),'whole module fibre common to donors')
                D=mm(m_maps[j][h],K);need(rank(D)==3,'full central module pencil')
                reads.append(mm(module['word'][np.ix_(positions,range(3*s,3*s+3))],D))
            need(rank(reads[0])==3 and all(np.array_equal(reads[0],R)for R in reads[1:]),'common actual module readout')
            fibres[i]=K
        module_fibres.append(fibres);module['determinants']=determinants
        module_receipts.append({'module':z,'ports':partition[z],'provider_rank':rank(module['word']),
            'core_seed':module['core_seed'],'fill_seed':module['fill_seed'],'H_core_rank':rank(np.hstack(list(fibres.values()))),
            'source_cuts':189,'native_source_cuts':176,'geometric_receivers':36,'native_receivers':34})
    full_maps={j:{a:block_diag([module['maps'][j][a]for module in modules])for a in stars[j]}for j in donors}
    full_word=np.zeros((45,45),dtype=np.uint8)
    for z,module in enumerate(modules):
        for p,d in enumerate(partition[z]):
            for s in range(3):full_word[all_ports.index(d),15*s+3*z:15*s+3*z+3]=module['word'][p,3*s:3*s+3]
    need(rank(full_word)==44,'full45-port provider rank44')
    full_cuts=[]
    for j in donors:
        for i in sorted(adj[j]):
            hs=visible[j,i];M=np.vstack([full_maps[j][a]for a in hs])
            order=[15*p+3*z+r for z in range(5)for p in range(16)for r in range(3)]
            expected=block_diag([np.vstack([module['maps'][j][a]for a in hs])for module in modules])
            need(M.shape==(240,240)and np.array_equal(M[order],expected),'literal full view is permuted block diagonal')
            det=1
            for module in modules:det=int(MUL[det,module['determinants'][j,i]])
            need(det!=0,'full source determinant product')
            full_cuts.append({'donor':j,'receiver':i,'native':i<111,'determinant':det})
    full_fibres={}
    for i in views:
        K=block_diag([fibres[i]for fibres in module_fibres]);need(K.shape==(240,15)and rank(K)==15,'whole full-width fibre')
        positions=[p for p,d in enumerate(all_ports)if charts[d]<=adj[i]];need(len(positions)==15,'actual fifteen visible ports')
        reads=[]
        for s,j in enumerate(donors):
            off=np.vstack([full_maps[j][a]for a in visible[j,i]if a!=h]);need(not np.any(mm(off,K)),'whole full-width off-H fibre')
            reads.append(mm(full_word[np.ix_(positions,range(15*s,15*s+15))],mm(full_maps[j][h],K)))
        need(rank(reads[0])==15 and all(np.array_equal(reads[0],R)for R in reads[1:]),'full15-dimensional common physical readout')
        full_fibres[str(i)]={'kernel':K.tolist(),'readout':reads[0].tolist(),'ports':[all_ports[p]for p in positions],
                            'readout_determinant':echelon(reads[0])[2]}
    need(all(rank(F)==15 for row in full_maps.values()for F in row.values()),'all complete quotients rank15')
    propagation=27+4*45;need(propagation==207<240-15,'protected full-width nonsaturation')
    quota=Counter();owners={j:{}for j in donors};Howners=[]
    for line in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines():
        phase,owner,coordinate,plane,d,_,source,_=json.loads(line)
        if phase=='X'and plane is not None:
            need(owner==source,'actual original early owner');quota[owner,plane]+=1
            if owner in owners:owners[owner].setdefault(plane,[]).append(int(coordinate))
            if plane==h:Howners.append([owner,int(coordinate),d])
    need(Counter(quota.values())=={15:2675,30:422,45:11},'raw early quota census')
    need(len(Howners)==90 and set(x[2]for x in Howners)==set(all_ports),'actual90 base owners on all45 exits')
    for j in donors:
        need(sorted(x for row in owners[j].values()for x in row)==list(range(480)),'all480 donor coordinates owned once')
        need(all(len(owners[j][a])==quota[j,a]for a in stars[j]),'exact owner count at every source plane')
    early_matrices={};early_records=[];early_component_data={}
    for j in donors:
        plane_rows={};dets=[];seeds=[]
        for z,module in enumerate(modules):
            good=None
            for seed in range(128):
                rows={};valid=True
                for plane in stars[j]:
                    F=module['maps'][j][plane];count=quota[j,plane]//15;need(count in [1,2],'ordinary source quota')
                    if count==2:rows[plane]=kron(np.eye(2,dtype=np.uint8),F)
                    elif plane==h:rows[plane]=np.hstack([F,np.zeros_like(F)])
                    else:
                        tag=f'early/642/3/{j}/{plane}/{seed}'if z==0 else f'full45-H642/{z}/early/{j}/{plane}/{seed}'
                        A=coefficients(tag,(3,6))
                        if rank(A)!=3:valid=False;break
                        rows[plane]=np.hstack([mm(A[:,:3],F),mm(A[:,3:],F)])
                if not valid:continue
                M=np.vstack([rows[a]for a in stars[j]]);_,ps,det=echelon(M)
                if M.shape==(96,96)and len(ps)==96:good=rows;break
            need(good is not None,'actual component early basis found')
            plane_rows[z]=good;dets.append(det);seeds.append(seed)
            early_component_data[f'{j}/{z}']={'seed':seed,'determinant':det,'matrix':M.tolist()}
        full_rows=[];row_owner_labels=[]
        for plane in stars[j]:
            count=quota[j,plane]//15;R=np.zeros((15*count,480),dtype=np.uint8)
            for z in range(5):
                M=plane_rows[z][plane]
                for lane in range(count):
                    rr=slice(15*lane+3*z,15*lane+3*z+3)
                    R[rr,48*z:48*z+48]=M[3*lane:3*lane+3,:48]
                    R[rr,240+48*z:240+48*z+48]=M[3*lane:3*lane+3,48:]
            full_rows.append(R);row_owner_labels.extend([[plane,x]for x in sorted(owners[j][plane])])
        M=np.vstack(full_rows);_,ps,det=echelon(M)
        need(M.shape==(480,480)and len(ps)==480 and len(row_owner_labels)==480,'complete actual480-dimensional early basis')
        product_det=1
        for d in dets:product_det=int(MUL[product_det,d])
        need(det==product_det,'full early determinant equals component product')
        early_matrices[str(j)]={'matrix':M.tolist(),'row_owners':row_owner_labels}
        early_records.append({'donor':j,'rank':480,'determinant':det,'component_seeds':seeds,'component_determinants':dets,
                              'eight_copy_physical_bank_fields':3840})
    complement=np.zeros((1,45),dtype=np.uint8);complement[0,0]=1
    kernel=np.zeros((45,1),dtype=np.uint8);kernel[[0,15,30]]=1
    augmented=np.vstack([full_word,complement])
    need(not np.any(mm(full_word,kernel))and mm(complement,kernel)[0,0]==1 and rank(augmented)==45,'one missing full-width direction')
    extension=None
    for col in np.eye(46,dtype=np.uint8).T:
        candidate=np.column_stack([augmented,col])
        if rank(candidate)==46:extension=candidate;break
    need(extension is not None,'invertible46-field paid extension');extension_inverse=inverse(extension)
    need(np.array_equal(mm(extension_inverse,augmented),np.vstack([np.eye(45,dtype=np.uint8),np.zeros((1,45),dtype=np.uint8)])), 'full-width original restoration and owned zero')
    Hinputs=[(j,x)for j in donors for x in sorted(owners[j][h])]
    need(len(Hinputs)==90 and all(len(owners[j][h])==30 for j in donors),'thirty real H inputs per donor')
    owner_index={owner:q for q,owner in enumerate(Hinputs)}
    Hphysical=np.zeros((90,90),dtype=np.uint8);Houtput_labels=[]
    for d in all_ports:
        pair=sorted((j,x)for j,x,p in Howners if p==d)
        need(len(pair)==2,'two original owners per D')
        for copy,owner in enumerate(pair):
            row=owner_index[owner];Houtput_labels.append({'owner':list(owner),'D':d,'copy':copy})
            for j in range(3):Hphysical[row,30*j+15*copy:30*j+15*copy+15]=full_word[all_ports.index(d),15*j:15*j+15]
    paid=np.zeros((2,90),dtype=np.uint8);paid[0,0]=1;paid[1,15]=1
    real_augmented=np.vstack([Hphysical,paid])
    need(rank(Hphysical)==88 and rank(real_augmented)==90,'owner-bound provider and two complements')
    _,piv,_=echelon(np.hstack([real_augmented,np.eye(92,dtype=np.uint8)]));extra=[x-90 for x in piv if x>=90]
    need(len(extra)==2,'two square-extension columns')
    real_extension=np.column_stack([real_augmented,np.eye(92,dtype=np.uint8)[:,extra]]);real_inverse=inverse(real_extension)
    need(np.array_equal(mm(real_inverse,real_augmented),np.vstack([np.eye(90,dtype=np.uint8),np.zeros((2,90),dtype=np.uint8)])), 'all90 originals and two zeros restored')
    binary=np.array([[int(MUL[real_extension[r//6,s//6],1<<(s%6)])>>(r%6)&1 for s in range(552)]for r in range(552)],dtype=np.uint8)
    reduced=binary.copy();operations=[]
    def add(target,source):
        need(target!=source,'distinct ADD owners');reduced[target]^=reduced[source];operations.append([target,source])
    for col in range(552):
        pivot=col+int(np.flatnonzero(reduced[col:,col])[0])
        if pivot!=col:add(col,pivot);add(pivot,col);add(col,pivot)
        for row in range(552):
            if row!=col and reduced[row,col]:add(row,col)
    need(np.array_equal(reduced,np.eye(552,dtype=np.uint8)),'literal physical binary compiler')
    symbolic=[1<<i for i in range(540)]+[0]*12
    for target,source in reversed(operations):symbolic[target]^=symbolic[source]
    need(symbolic==[sum(int(binary[r,c])<<c for c in range(540))for r in range(552)],'actual physical forward outputs')
    for target,source in operations:symbolic[target]^=symbolic[source]
    need(symbolic==[1<<i for i in range(540)]+[0]*12,'original owners and paid zeros restored')
    corrupted=full_word.copy();corrupted[all_ports.index(partition[1][0]),15]^=1
    bad_count=0
    for i in views:
        K=np.array(full_fibres[str(i)]['kernel'],dtype=np.uint8);positions=[p for p,d in enumerate(all_ports)if charts[d]<=adj[i]]
        reads=[mm(corrupted[np.ix_(positions,range(15*s,15*s+15))],mm(full_maps[j][h],K))for s,j in enumerate(donors)]
        bad_count+=not all(np.array_equal(reads[0],R)for R in reads[1:])
    need(bad_count>0,'corrupted physical port coefficient rejected')
    need(rank(real_augmented[:-1])==89,'deleting one paid field loses information')
    args.out.mkdir(parents=True,exist_ok=True)
    result={'status':'PASS_FULL45_LOCAL_H642_PROTECTED_COMPLEMENT','H':h,'donors':donors,'physical_ports':all_ports,
            'module_receipts':module_receipts,'source_width':15,'source_bank_dimension':240,'H_input_dimension':45,
            'H_provider_rank':44,'source_geometric_cuts':189,'source_native_cuts':176,'component_source_cuts':len(module_cuts),
            'geometric_receivers':36,'native_receivers':34,'common_readout_dimension':15,'uniform_propagation_upper':207,
            'saturation_threshold':225,'actual_early_bases':early_records,'physical_bank_fields':3840,
            'physical_H_inputs':720,'physical_H_rank':704,'paid_field_exports':16,'paid_MOVE_gap':6,
            'physical_propagation_upper':3312,'physical_saturation_threshold':3600,
            'actual_two_copy_H_owners':90,'actual_two_copy_H_rank':88,'physical_binary_ADD_per_direction':len(operations),
            'eight_lane_forward_inverse_ADDs':16*len(operations),'binary_INIT_MOVE_CLEAR_each':96,
            'corrupted_port_readout_failures':bad_count,'full45_local_H':True,'joint_two_H_sources':False,
            'all111_sources':False,'complete_D_K_facet_word':False,'complete_return':False,'complete_invoice':False,'new_complete_kappa':False}
    coefficient={'H':h,'field_modulus':67,'donors':donors,'ports':all_ports,'partition':partition,
                 'source_maps':{str(j):{str(a):M.tolist()for a,M in row.items()}for j,row in full_maps.items()},
                 'module_words':[module['word'].tolist()for module in modules],'word':full_word.tolist(),'complement':complement.tolist(),
                 'logical_extension':extension.tolist(),'logical_extension_inverse':extension_inverse.tolist(),
                 'physical_owner_inputs':[list(x)for x in Hinputs],'physical_owner_outputs':Houtput_labels,
                 'physical_word':Hphysical.tolist(),'physical_complements':paid.tolist(),
                 'physical_extension':real_extension.tolist(),'physical_extension_inverse':real_inverse.tolist()}
    def save(name,value):
        payload=(json.dumps(value,sort_keys=True,separators=(',',':'))+'\n').encode()
        (args.out/name).write_bytes(gzip.compress(payload,mtime=0));return hashlib.sha256(payload).hexdigest()
    result['coefficient_payload_sha256']=save('COEFFICIENTS.json.gz',coefficient)
    result['fibre_payload_sha256']=save('FIBRES.json.gz',full_fibres)
    result['early_payload_sha256']=save('EARLY.json.gz',{'full':early_matrices,'components':early_component_data})
    result['compiler_payload_sha256']=save('COMPILER.json.gz',{'binary_elimination_ADDs':operations,'dimension':552})
    (args.out/'SOURCE-CUT-DETERMINANTS.json').write_text(json.dumps({'full':full_cuts,'components':module_cuts},sort_keys=True,indent=2)+'\n')
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],189,176,36,34,44,207,16,len(operations),flush=True)

if __name__=='__main__':main()
