#!/usr/bin/env python3
"""Independent review of the all-native D1509 single-cut extension.

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
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--package',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();repo=args.repo.resolve();base=repo/'research/moonshot-005-program/results';p=args.package;oldp=base/'bit-shared-h-s031-construction/native-d1509-cut'
    for name,digest in json.loads((Path(__file__).resolve().parent/'SOURCE-PINS.json').read_text())['files'].items():need(hashlib.sha256((repo/name).read_bytes()).hexdigest()==digest,'frozen input pin '+name)
    source,_=read_json(p/'output/SOURCES.json.gz');early,_=read_json(p/'output/EARLY.json.gz');physical,_=read_json(p/'output/H-PHYSICAL.json.gz');dw,_=read_json(p/'output/D-WORD.json.gz');gauges,_=read_json(p/'output/GAUGES.json.gz');oldsource,_=read_json(oldp/'output/SOURCES.json.gz');oldearly,_=read_json(oldp/'output/EARLY.json.gz');oldphysical,_=read_json(oldp/'output/H-PHYSICAL.json.gz');olddw,_=read_json(oldp/'output/D-WORD.json.gz')
    layout,_=read_json(base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz');basis,_=read_json(base/'bit-clifford-one-evaluation-gate/author/BASIS.json');roots=root_coordinates(layout,basis);planes=[set(x)for x in layout['A2']];charts=[set(x)for x in layout['D4']];adj=[{i for i,y in enumerate(roots)if i!=j and not polar(x,y)}for j,x in enumerate(roots)]
    nodes,_=read_json(base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json');nodes=nodes['H_nodes'];allocation,_=read_json(base/'bit-global-desarguesian-port-allocation/author/WITNESS.json.gz');marked=set(allocation['selected_D']);routes=[json.loads(r)for r in gzip.decompress((base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz').read_bytes()).splitlines()];key=lambda r:(r[1],r[2]);HX={};HY={};Xj={};Yj={}
    for r in routes:
        if r[3]is None:continue
        (HX if r[0]=='X'else HY).setdefault(r[3],[]).append(r)
        if r[0]=='X':Xj.setdefault((r[1],r[3]),[]).append(r)
        elif r[6]is not None:Yj.setdefault((r[6],r[3]),[]).append(r)
    for table in [HX,HY,Xj,Yj]:
        for k in table:table[k].sort(key=key)
    paired={int(j):{int(h):np.array(M,dtype=np.uint8)for h,M in row.items()}for j,row in source['paired_maps'].items()};frames={tuple(map(int,s.split('/'))):np.array(M,dtype=np.uint8)for s,M in source['frames'].items()};donors=sorted(paired);newdonors=[32,35,38,68,69,90];old_donors=[0,45,61,62,100];need(donors==sorted(j for j in charts[1509]if j<111)and len(donors)==11 and set(map(int,gauges))==set(newdonors),'all eleven actual native D sources')
    LF=np.array(source['selected_original_space'],dtype=np.uint8);need(np.array_equal(LF,oldsource['selected_original_space'])and rank(LF)==8,'same full paired target space');prot=list(range(48))+list(range(240,288));LL=LF[prot]
    for name,value in olddw.items():
        if name!='ingress':need(dw[name]==value,'unchanged D owner matrix and full cache compiler '+name)
    for h,value in oldphysical.items():need(physical[h]==value,'every previous H physical word unchanged')
    for j in old_donors:
        need(early[str(j)]==oldearly[str(j)]and source['late_parities'][str(j)]==oldsource['late_parities'][str(j)],'old source early/late data unchanged')
        for h,F in oldsource['maps'][str(j)].items():
            F=np.array(F,dtype=np.uint8);need(np.array_equal(paired[j][int(h)],block_diag([F,F]))and source['frames'][f'{j}/{h}']==oldsource['frames'][f'{j}/{h}'],'old paired source tuple and frame unchanged')
    owners=sorted([r for r in routes if r[4]==1509 and r[0]=='X'],key=key)+sorted([r for r in routes if r[4]==1509 and r[0]=='Y'],key=key);need(owners==dw['owners'],'same35 actual D owners');T=np.array(dw['matrix'],dtype=np.uint8);outputs=dw['selected_output_indices'];di={(r[0],r[1],r[2]):q for q,r in enumerate(owners)}
    actual_hs=set(h for row in paired.values()for h in row);need(set(map(int,physical))==actual_hs and len(actual_hs)==280,'exact280 actual H source planes');sections=[];transfers={};nonzero_cross=[]
    for h in sorted(actual_hs):
        data=physical[str(h)];xs=HX[h];ys=HY.get(h,[]);ne,nl=len(xs),len(ys);need(data['X_owners']==xs and data['Y_owners']==ys and data['ports']==[d for d,Q in enumerate(charts)if planes[h]<=Q],'native physical H phase owners and ports');E=np.array(data['early'],dtype=np.uint8).reshape(ne,ne);B=np.array(data['late'],dtype=np.uint8).reshape(nl,nl);G=np.array(data['cross'],dtype=np.uint8).reshape(nl,ne);need((ne,nl)in [(90,0),(45,45)]and rank(E)==ne-(2 if h==642 else 0)and rank(B)==nl,'full H phase ranks')
        if np.any(G):nonzero_cross.append(h)
        xi={(r[1],r[2]):q for q,r in enumerate(xs)};yi={(r[1],r[2]):q for q,r in enumerate(ys)}
        for j in sorted(planes[h]):
            if j not in donors:continue
            Q=frames[j,h];need(Q.shape==(30,30)and rank(Q)==30,'complete paired source frame');XE=np.zeros((ne,30),dtype=np.uint8);YL=np.zeros((nl,30),dtype=np.uint8);q=len(Xj[j,h]);need(q in [15,30]and len(Yj.get((j,h),[]))==30-q,'ordinary source early and late visits')
            for t,r in enumerate(Xj[j,h]):XE[xi[r[1],r[2]]]=Q[t]
            for t,r in enumerate(Yj.get((j,h),[])):YL[yi[r[1],r[2]]]=Q[q+t]
            RX=mm(E,XE);RY=mm(G,XE)^mm(B,YL);transfers[j,h]=(RX,RY)
            for ii in range(120):
                if not planes[h]<=adj[ii]:continue
                xx=[q for q,r in enumerate(xs)if charts[r[4]]<=adj[ii]];yy=[q for q,r in enumerate(ys)if charts[r[4]]<=adj[ii]];A=np.vstack([RX[xx],RY[yy]]);_,ps,det=echelon(A);need(A.shape==(30,30)and len(ps)==30,'all exact native donor/H sections');sections.append({'donor':j,'H':h,'receiver':ii,'determinant':det})
    need(len(sections)==11088,'all eleven donor stars tested');print('ALL_H_SECTIONS',280,len(sections),flush=True)
    cuts=[];early_records=[];gauge_records=[];propagation=[]
    inherited,_=read_json(oldp/'review-c/output/FULL-SOURCE-DETERMINANTS.json');need(len(inherited)==315 and all(r['determinant']for r in inherited),'pinned old full source determinant certificate')
    cuts.extend({'donor':r['donor'],'receiver':r['receiver'],'native':r['native'],'paired_determinant':power(r['determinant'],2),'mode':'inherited exact paired tuple'}for r in inherited)
    for j in newdonors:
        hs=[h for h,P in enumerate(planes)if j in P];need(set(paired[j])==set(hs)and len(hs)==28,'complete new source star');need(len(set(nodes[h]for h in hs))==28,'distinct actual global nodes');record=gauges[str(j)];J=np.array(record['protected96'],dtype=np.uint8);_,gp,gdet=echelon(J);need(J.shape==(96,96)and len(gp)==96,'invertible96-coordinate input change');need(record['base_H_nodes']=={str(h):nodes[h]for h in hs},'exact global source-node assignment')
        half=[h for h in hs if len(Xj[j,h])==15];full=[h for h in hs if len(Xj[j,h])==30];need(len(half)==24 and len(full)==4 and record['source_frame_first_early_half']==half[:12],'ordinary split of actual early flags');base_maps={};rows=[];labels=[];Ephysical=np.zeros((480,480),dtype=np.uint8)
        for h in hs:
            scalar=np.array([[power(nodes[h],d)for d in range(16)]],dtype=np.uint8);F=block_diag([kron(scalar,np.eye(3,dtype=np.uint8)),kron(scalar,np.eye(12,dtype=np.uint8))]);M=block_diag([F,F]);base_maps[h]=M;expected=M.copy();expected[:,prot]=mm(M[:,prot],J);need(paired[j][h].shape==(30,480)and np.array_equal(paired[j][h],expected),'input change explicitly folded into every paired quotient')
            Q=np.eye(30,dtype=np.uint8)
            if h in half[12:]:Q=np.block([[np.zeros((15,15),dtype=np.uint8),np.eye(15,dtype=np.uint8)],[np.eye(15,dtype=np.uint8),np.zeros((15,15),dtype=np.uint8)]])
            need(np.array_equal(frames[j,h],Q),'literal actual early half-copy assignment');R=mm(Q,paired[j][h]);q=len(Xj[j,h])
            for t,r in enumerate(Xj[j,h]):Ephysical[r[2]]=R[t];labels.append([h,r[2]])
            rows.extend(R[:q]);late=np.array(source['late_parities'][str(j)][str(h)],dtype=np.uint8).reshape(30-q,480);need(np.array_equal(late,R[q:]),'same folded input change in every late parity')
        E=np.array(rows,dtype=np.uint8);need(np.array_equal(E,early[str(j)]['matrix'])and np.array_equal(Ephysical,early[str(j)]['physical_matrix'])and labels==early[str(j)]['row_owners']and sorted(r[1]for r in labels)==list(range(480)),'every actual original early owner bound once');_,ps,det=echelon(Ephysical);need(len(ps)==480,'new physical early480 basis');early_records.append({'donor':j,'determinant':det})
        scalar_inverses={};views={}
        for ii in sorted(adj[j]):
            vv=[h for h in hs if planes[h]<=adj[ii]];need(len(vv)==16,'complete geometric source view');V=np.array([[power(nodes[h],d)for d in range(16)]for h in vv],dtype=np.uint8);_,vp,vdet=echelon(V);need(len(vp)==16,'exact scalar Vandermonde source cut');scalar_inverses[ii]=inverse(V);views[ii]=vv;cuts.append({'donor':j,'receiver':ii,'native':ii<111,'paired_determinant':int(MUL[gdet,power(vdet,30)]),'mode':'literal tensor factorization times folded gauge'})
        pairranks=[]
        for h in hs:
            for r in hs:
                if h==r:continue
                P=np.hstack([scalar_inverses[ii][:,views[ii].index(h):views[ii].index(h)+1]for ii in sorted(adj[j])if h in views[ii]and r in views[ii]]);rk=rank(P);need(rk==5 and not np.any(mm(np.array([[power(nodes[r],d)for d in range(16)]],dtype=np.uint8),P)),'all scalar pair propagation ranks exactly5');pairranks.append([h,r,rk])
        propagation.append({'donor':j,'scalar_maximum':5,'paired_bound':150,'ordered_pairs':pairranks})
        Arows=[];alabels=[]
        for h in hs:
            if not planes[h]<=adj[6]:continue
            RX,RY=transfers[j,h]
            for phase,ownersH,R in [('X',HX[h],RX),('Y',HY.get(h,[]),RY)]:
                values=mm(R,base_maps[h][:,prot])
                for q,r in enumerate(ownersH):
                    if r[4]in marked and charts[r[4]]<=adj[6]:Arows.append(values[q]);alabels.append([phase,r[1],r[2]])
        A=np.array(Arows,dtype=np.uint8);need(A.shape==(96,96)and rank(A)==96 and np.array_equal(A,record['base_proper_left'])and alabels==record['base_proper_left_owner_labels'],'independent actual96-dimensional protected proper-left map');inn=[q for q,r in enumerate(owners)if r[3]is not None and j in planes[r[3]]];need(len(inn)==8,'eight actual D input flags');C=T[np.ix_(outputs,inn)];need(np.array_equal(C,record['D_section'])and rank(C)==8,'same actual D section');Ci=inverse(C);target=np.zeros((96,8),dtype=np.uint8)
        for q,index in enumerate(inn):
            r=owners[index];label=[r[0],r[1],r[2]];need(alabels.count(label)==1,'unique physical proper-left binding');target[alabels.index(label)]=Ci[q]
        U=mm(inverse(A),target);need(np.array_equal(U,record['base_D_inverse_fibre'])and rank(U)==8 and np.array_equal(mm(J,LL),U),'exact gauge interpolation on the entire eight-space');gauge_records.append({'donor':j,'gauge_determinant':gdet,'base_left_determinant':echelon(A)[2],'D_section_determinant':echelon(C)[2],'target_rank':8});print('NEW_DONOR',j,63,det,150,flush=True)
    need(len(cuts)==693 and sum(r['native']for r in cuts)==639,'all geometric and native source cuts');need(dw['supplied_donors']==donors,'literal all-native donor order');ingress=np.zeros((35,8*len(donors)),dtype=np.uint8)
    for t,j in enumerate(donors):
        for h in paired[j]:
            if not planes[h]<=adj[6]:continue
            RX,RY=transfers[j,h];state=mm(paired[j][h],LF)
            for phase,ownersH,R in [('X',HX[h],RX),('Y',HY.get(h,[]),RY)]:
                values=mm(R,state)
                for q,r in enumerate(ownersH):
                    if r[4]==1509:ingress[di[phase,r[1],r[2]],8*t:8*t+8]=values[q]
                    elif charts[r[4]]<=adj[6]:need(not np.any(values[q]),'all other proper D packets vanish for every native donor')
    need(np.array_equal(ingress,dw['ingress'])and np.array_equal(mm(T[outputs],ingress),np.tile(np.eye(8,dtype=np.uint8),(1,11))),'one exact common identity readout for all eleven native donors');need(all(rank(ingress[:,8*t:8*t+8])==8 for t in range(11)),'entire isolated fibre has full8-dimensional D readout')
    args.out.mkdir(parents=True,exist_ok=True);result={'status':'PASS_INDEPENDENT_ALL_NATIVE_D1509_EXTENSION','geometric_source_cuts':693,'native_source_cuts':639,'source_cuts_inherited_by_exact_equality':315,'new_scalar_gauge_factorized_cuts':378,'new_early_bases':early_records,'gauge_certificates':gauge_records,'source_bank_dimension':480,'source_quotient_dimension':30,'paired_bounds':{str(j):150 if j in newdonors else 444 for j in donors},'saturation_threshold':450,'H_modules':len(physical),'H_donor_sections':len(sections),'old_H_modules_exactly_unchanged':136,'nonzero_H_cross_modules':len(nonzero_cross),'all_native_D_donors':donors,'common_entire_fibre_dimension':8,'D_matrix_owners_and_compiler_exactly_unchanged':True,'retained_common_H_readouts_inherited':72,'other_D_receivers':False,'new_whole_H_common_readouts':False,'complete_global_return':False,'complete_invoice':False,'author_executable_imports':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');(args.out/'SOURCE-DETERMINANTS.json').write_text(json.dumps(cuts,sort_keys=True,indent=2)+'\n');(args.out/'H-SECTION-DETERMINANTS.json').write_text(json.dumps(sections,sort_keys=True,indent=2)+'\n');payload=(json.dumps(propagation,sort_keys=True,separators=(',',':'))+'\n').encode();(args.out/'SCALAR-PROPAGATION.json.gz').write_bytes(gzip.compress(payload,mtime=0));print(result['status'],693,639,280,11088,11,8,flush=True)
if __name__=='__main__':main()
