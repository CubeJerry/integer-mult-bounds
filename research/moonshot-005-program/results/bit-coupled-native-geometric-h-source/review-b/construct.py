"""Independent reconstruction from literal data and earlier review geometry.

No component/full author constructor, checker, or compiler is imported.
"""
from collections import Counter, defaultdict
import gzip
from hashlib import sha256, shake_256
import importlib.util
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace
import numpy as np

def need(ok, message):
    if not ok:
        raise ValueError(message)

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec); spec.loader.exec_module(value)
    return value

def pseudo(tag, rows, columns):
    return np.frombuffer(shake_256(tag.encode('ascii')).digest(rows*columns), dtype=np.uint8).reshape(rows, columns) & 63

def powers(F, xs, width):
    out = np.ones((len(xs), width), dtype=np.uint8)
    for c in range(1, width):
        out[:, c] = F.product[out[:, c-1], xs]
    return out

def quadratic_frame(space, q):
    """Lexicographic orthogonal planes, with exhaustive pair checks."""
    remaining = set(space); frame = []
    while len(remaining)>1:
        polar = lambda x,y:q(x^y)^q(x)^q(y)
        singular = sorted(x for x in remaining if x and q(x)==0)
        pairs = [(x,y) for x in singular for y in singular if polar(x,y)]
        if pairs:
            x,y = min(pairs)
        else:
            x,y = sorted(remaining-{0})[:2]
        need(polar(x,y)==1, 'nonsingular orthogonal frame plane')
        frame += [x,y]
        remaining = {z for z in remaining if polar(z,x)==polar(z,y)==0}
    need(len(frame)==6, 'six-dimensional quadratic frame')
    return frame

def build_geometric(ctx):
    F,f = ctx.field,ctx.arith; prm=ctx.component_parameters; c=ctx.charts[263,3]
    roots=ctx.binary.roots; U,V=(roots[j] for j in c.donors[:2])
    space={w for w in range(256) if f.b8(w,U)==f.b8(w,V)==0}
    left=quadratic_frame(space,f.q8); right=quadratic_frame(range(64),f.q6)
    nodes={f.xor(left[p] for p in range(6) if mask>>p&1):f.xor(right[p] for p in range(6) if mask>>p&1) for mask in range(64)}
    need(set(nodes)==space and set(nodes.values())==set(range(64)) and all(f.q8(x)==f.q6(y) for x,y in nodes.items()), 'all64 exact quadratic-isometry values')
    for j in c.donors:
        for h,x in c.point[j].items():
            projected={roots[t]^(U if f.b8(roots[t],V) else 0)^(V if f.b8(roots[t],U) else 0) for t in ctx.H[h]-{j}}
            need(projected=={x}, 'D-radical point equals direct orthogonal projection')
    omega=prm['omega']; basis=prm['F4_basis']
    need(f.MUL[omega][omega]^omega==1, 'literal order-three subfield scalar')
    coords={f.xor(basis[p] for p in range(6) if mask>>p&1):tuple(((mask>>(2*p))&1)^(omega if mask>>(2*p+1)&1 else 0) for p in range(3)) for mask in range(64)}
    need(len(coords)==64 and all(f.q6(x)==f.xor(f.power(t,3) for t in v) for x,v in coords.items()), 'all64 Hermitian quadratic identities')
    undo={v:x for x,v in coords.items()}
    rotate={x:undo[tuple(f.MUL[omega][t] for t in v)] for x,v in coords.items()}
    selected=[d for d in c.all_ports if {rotate[nodes[x]] for x in ctx.native.rad[d]}=={nodes[x] for x in ctx.native.rad[d]}]
    need(selected==prm['ports'] and len(selected)==9, 'actual nine Hermitian spread ports')
    need(Counter(x for d in selected for x in ctx.native.rad[d])=={x:1 for x in c.xs}, 'nine radicals partition all27 singular points')
    c.ports=selected
    E1=np.array([[f.power(t,2) for t in coords[nodes[min(ctx.native.rad[d])]]] for d in selected],dtype=np.uint8)
    E2=np.array([[f.MUL[x][x],f.MUL[y][y],f.MUL[z][z],f.MUL[x][y],f.MUL[x][z],f.MUL[y][z]] for x,y,z in E1],dtype=np.uint8)
    need(F.rank(E1)==3 and F.rank(E2)==6, 'linear and quadratic evaluation dimensions')
    aa,bb=np.array(prm['weights'],dtype=np.uint8)
    need(np.all(aa) and np.all(bb) and np.all(aa^bb), 'three nonzero weight families')
    W=[F.null(F.product[z[:,None],E2].T).T for z in (aa^bb,bb,aa)]
    need(all(z.shape==(3,9) for z in W), 'three annihilator dimensions')
    T=np.vstack(W); word=F.solve(T,np.eye(9,dtype=np.uint8))
    points={x:np.kron(powers(F,[nodes[x]],16),np.eye(3,dtype=np.uint8)) for x in c.xs}
    fibres={}; pencils={}; zero=np.zeros((3,3),dtype=np.uint8)
    for i in c.receivers:
        r=np.array(coords[nodes[roots[i]]],dtype=np.uint8)[:,None]
        values=F.mm(E1,r)[:,0]
        visible=[p for p,d in enumerate(selected) if ctx.D[d]<=ctx.perp[i]]
        need(set(visible)==set(np.flatnonzero(values==0)) and len(visible)==3, 'actual exits equal Hermitian zero evaluations')
        A0=F.product[values[:,None],F.product[aa[:,None],E1]]
        A1=F.product[values[:,None],F.product[bb[:,None],E1]]
        A=np.hstack([A0,A1]); D=[F.mm(W[0],A0),F.mm(W[1],A0),F.mm(W[2],A1)]
        need(F.rank(A)==6 and all(F.rank(z)==3 for z in D), 'six-dimensional invisible output and invertible donor pencils')
        need(np.array_equal(F.mm(T,A),np.block([[D[0],D[0]],[D[1],zero],[zero,D[2]]])), 'exact annihilator block identity')
        outputs=[F.mm(word[np.ix_(visible,range(3*j,3*j+3))],D[j]) for j in range(3)]
        need(F.rank(outputs[0])==3 and all(np.array_equal(outputs[0],z) for z in outputs[1:]), 'common invertible readout on every geometric receiver')
        off=[x for x in c.xs if f.b8(x,roots[i])==0]
        K=F.null(np.vstack([points[x] for x in off]))
        need(len(off)==15 and K.shape==(48,3), 'entire ordinary inverse fibre')
        fibres[i]=F.product[f.power(nodes[roots[i]],2),K]; pencils[i]=D
    joined=np.hstack(list(fibres.values())); rank,_,pivots=F.reduce(joined)
    need(rank==18, 'geometric scalar fibre core repeated three times')
    S=joined[:,pivots]; _,_,rows=F.reduce(S.T)
    inverse=F.solve(S[rows],np.eye(18,dtype=np.uint8)); annihilator=F.null(S.T).T
    controls=[]
    for p,j in enumerate(c.donors):
        target=np.hstack([pencils[i][p] for i in c.receivers])[:,pivots]
        C=np.zeros((3,48),dtype=np.uint8); C[:,rows]=F.mm(target,inverse)
        C^=F.mm(pseudo(f'geo-quadratic-tail/263/{prm["weight_seed"]}/{prm["tail_seed"]}/{p}',3,30),annihilator)
        need(all(np.array_equal(F.mm(C,K),pencils[i][p]) for i,K in fibres.items()), 'central map extends every fibre pencil exactly')
        controls.append(C); ctx.maps[j,3]={h:points[x] for h,x in c.point[j].items()}; ctx.maps[j,3][263]=C
    data={'word':word,'points':points,'nodes':nodes,'controls':controls,'fibres':fibres,'pencils':pencils,'E1':E1,'E2':E2,'T':T,'core':S}
    expected=json.loads(ctx.payload['component_result'])
    for key in ('E1','E2','T','core','Hword'):
        matrix=word if key=='Hword' else data[key]
        need(sha256(matrix.tobytes()).hexdigest()==expected['matrix_sha256'][key], 'independent component matrix '+key)
    ctx.components[3]=data

def context(repo, out):
    base = repo/'research/moonshot-005-program/results'
    pins = json.loads(Path(__file__).with_name('SOURCE-PINS.json').read_text())
    payload = {}
    for key, item in pins.items():
        name, digest = item['path'], item['sha256']; raw = (base/name).read_bytes()
        need(sha256(raw).hexdigest() == digest, 'frozen source pin '+key)
        payload[key] = gzip.decompress(raw) if name.endswith('.gz') else raw
    def old(key):
        return module(base/pins[key]['path'], 'geometric_H_review_'+key)
    out.mkdir(parents=True, exist_ok=True)
    library = out/'linear64.so'
    subprocess.run(['c++','-O3','-std=c++17','-shared','-fPIC',str(base/pins['engine_cpp']['path']),'-o',str(library)], check=True)
    field = old('engine').Field(library); oldfield = old('old_field'); geom = old('old_geometry')
    need(np.array_equal(field.product, oldfield.MUL), 'two independent field implementations')
    native = geom.Native(repo, oldfield)
    arith = old('geometric_arithmetic'); binary = old('geometric_geometry')
    layout = json.loads(payload['layout'])
    binary_ctx = binary.reconstruct(layout, json.loads(payload['binary_basis']), arith)
    need(native.H == list(map(set,binary_ctx.planes)) and native.adj == binary_ctx.perp, 'native binary and real geometry agree')
    H = list(map(frozenset,layout['A2'])); D = list(map(frozenset,layout['D4']))
    stars = native.hlist; perp = binary_ctx.perp; views = native.views
    wires = defaultdict(list); xcount = Counter(); owner_keys = set()
    for line in payload['routes'].splitlines():
        phase, role, coordinate, h, d, k, source, terminal = json.loads(line)
        need((phase,role,coordinate) not in owner_keys, 'one actual route per original field')
        owner_keys.add((phase,role,coordinate))
        if phase == 'X':
            need(role == source, 'true early donor ownership'); xcount[h] += 1
        if h is not None and source is not None:
            wires[source,h,phase].extend((((phase=='Y')*111+role)*480+coordinate)*8+c for c in range(8))
    need(len(owner_keys) == 106560, 'complete X/Y route inventory')
    for values in wires.values():
        values.sort(); need(len(values)==len(set(values)), 'distinct physical source owners')
    prm = json.loads(payload['parameters']); cp = json.loads(payload['component_parameters'])
    need(prm['H']==cp['H']==263 and sorted(H[263])==[0,61,62], 'actual three-donor centre')
    charts = {(263,k):geom.Chart(native,263,k) for k in (3,12)}
    ctx = SimpleNamespace(repo=repo,base=base,pins=pins,payload=payload,field=field,native=native,
        arith=arith,binary=binary_ctx,H=H,D=D,stars=stars,perp=perp,views=views,wires=wires,xcount=xcount,
        parameters=prm,component_parameters=cp,centres=[263],donors=[0,61,62],charts=charts,maps={},components={})
    build_geometric(ctx)
    c = charts[263,12]; c.ports = [d for d in c.all_ports if d not in charts[263,3].ports]
    need(c.ports == prm['complementary_ports'] and len(c.ports)==36, 'literal complementary exits')
    need(all(sum(x in native.rad[d] for d in c.ports)==4 for x in c.xs), 'four complementary incidences per point')
    maps = c.single({'core':prm['core_seed'],'fill':prm['fill_seed']})
    ctx.components[12] = {'word':c.V, 'points':{x:maps[c.donors[0]][h] for h,x in c.point[c.donors[0]].items()}}
    for j in ctx.donors:
        ctx.maps[j,12] = maps[j]
    author = json.loads(payload['author_result'])
    for k in (3,12):
        data = ctx.components[k]
        need(sha256(data['word'].tobytes()).hexdigest()==author['components'][str(k)]['H_word_sha256'], 'complete H word coefficient bytes')
        for j in ctx.donors:
            digest = sha256(b''.join(ctx.maps[j,k][h].tobytes() for h in sorted(ctx.maps[j,k]))).hexdigest()
            need(digest==author['components'][str(k)]['source_coefficient_sha256'][str(j)], 'complete source coefficient bytes')
    return ctx
