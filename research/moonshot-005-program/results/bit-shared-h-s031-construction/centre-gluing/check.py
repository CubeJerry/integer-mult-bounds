#!/usr/bin/env python3
"""Exact geometric core and quadratic-pencil preservation certificate."""
from argparse import ArgumentParser
from pathlib import Path
import hashlib, importlib.util, json
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def require(condition, message):
    if not condition:
        raise ValueError(message)


def execute(repo, out):
    out.mkdir(parents=True, exist_ok=True)
    base = repo / 'research/moonshot-005-program/results'
    pins_path = Path(__file__).with_name('SOURCE-PINS.json')
    if pins_path.exists():
        for path, digest in json.loads(pins_path.read_text()).items():
            require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest, 'source pin '+path)
    geom = module(base/'bit-coupled-native-geometric-h-source/component/construction.py', 'glue_geometry')
    families, atlas, previous = geom.context(repo)
    parameters = json.loads((base/'bit-coupled-native-geometric-h-source/component/output/PARAMETERS.json').read_text())
    local = geom.build(families, atlas, previous, parameters)
    product, inverse = atlas.product, atlas.inverse
    eye = np.eye(3, dtype=np.uint8)
    power = lambda x,n: geom.power(int(x), n, atlas)
    quad = lambda x: geom.quadratic(int(x), atlas)
    polar = lambda x,y: quad(x^y)^quad(x)^quad(y)
    nodes = [x for x in range(64) if not quad(x)]
    require(len(nodes) == 28, 'the literal quadric')

    def fibre(v, centre):
        numerator = np.zeros(17, dtype=np.uint8)
        for degree, exponent in [(8,1),(16,2),(14,4),(5,4),(1,8),(2,16),(4,32)]:
            numerator[degree] ^= power(v,exponent)
        numerator[0] ^= geom.xor(product[numerator[d],power(centre,d)] for d in range(17))
        quotient = np.zeros(16, dtype=np.uint8)
        quotient[15] = numerator[16]
        for d in range(14,-1,-1):
            quotient[d] = numerator[d+1]^product[centre,quotient[d+1]]
        require(numerator[0] == product[centre,quotient[0]], 'literal division')
        return quotient

    cores = {a:np.array([fibre(1<<s,a) for s in range(6)], dtype=np.uint8).T for a in nodes}
    require(all(atlas.rank(S)==6 for S in cores.values()), 'all geometric cores')
    incidence=[]
    for a in nodes:
        for b in nodes:
            if a==b:
                continue
            parameters_ab = [v for v in range(1,64) if polar(v,a)==1^quad(v) and polar(v,b)==1^quad(v)]
            P = np.array([fibre(v,b) for v in parameters_ab], dtype=np.uint8).T
            require(len(parameters_ab)==20 and atlas.rank(P)==5, 'all two-node geometric views')
            _, pivots = geom.rref(P,atlas)
            P = P[:,pivots]
            joined = np.hstack((cores[a],P))
            relations = previous.null_basis(joined,atlas)
            intersection = atlas.mm(cores[a],relations[:6])
            linear = np.zeros((16,1),dtype=np.uint8)
            linear[0,0]=a;linear[1,0]=1
            require(intersection.shape==(16,1) and atlas.rank(np.hstack((intersection,linear)))==1,
                    'the forced line is z+a')
            require(atlas.rank(np.hstack((cores[a],cores[b])))==10, 'the full core intersection is span(1,z)')
            incidence.append({'a':a,'b':b,'receiver_count':20,'propagation_rank':5,'core_union_rank':10,'overlap_rank':1})

    E,E2=local['E1'],local['E2']
    N=previous.null_basis(E2.T,atlas).T
    schur=np.vstack([product[N[p],E[:,q]] for p in range(3) for q in range(3)])
    require(atlas.rank(E)==3 and atlas.rank(E2)==6 and atlas.rank(schur)==6,
            'actual9-port Schur annihilator ranks')
    require(not np.any(atlas.mm(schur,E)), 'the full Schur kernel is col(E)')
    omega=int(parameters['omega'])
    require(power(omega,2)^omega==1, 'F4 generator')

    # An explicit proportional-weight fault makes T singular and every D pencil zero.
    beta=np.asarray(parameters['weights'][1],dtype=np.uint8)
    alpha=product[omega,beta]
    W=[previous.null_basis(product[c[:,None],E2].T,atlas).T for c in (alpha^beta,beta,alpha)]
    badT=np.vstack(W)
    require(atlas.rank(badT)==3, 'proportional-weight negative control')
    require(all(not np.any(atlas.mm(W[1],product[alpha[:,None],product[atlas.mm(E,np.eye(3,dtype=np.uint8)[:,r:r+1])[:,0,None],E]])) for r in range(3)),
            'singular T admits the zero pencil')

    # The native global-node parameters bind the centre a and its Hermitian coordinates.
    shared=json.loads((base/'bit-global-desarguesian-port-allocation/author/output/GLOBAL-NODES.json').read_text())
    h=parameters['H'];a=shared['H_nodes'][h]
    basis=parameters['F4_basis']
    coordinates={geom.xor(basis[s] for s in range(6) if mask>>s&1):
                 tuple(((mask>>(2*p))&1)^int(product[omega,(mask>>(2*p+1))&1]) for p in range(3))
                 for mask in range(64)}
    moore=np.array([[power(1<<r,1<<s) for s in range(6)] for r in range(6)],dtype=np.uint8)
    moore_inverse=geom.inverse(moore,atlas)
    native=[]
    for donor in local['chart'].donors:
        mapping={int(i):int(v) for i,v in shared['receiver_parameters'][str(donor)].items()}
        xrows=[];yrows=[]
        for receiver in local['chart'].views:
            v=mapping[receiver]
            bits=np.array([(v>>s)&1 for s in range(6)],dtype=np.uint8)
            if atlas.rank(np.array(xrows+[bits.tolist()],dtype=np.uint8))>len(xrows):
                xrows.append(bits.tolist())
                yrows.append(coordinates[local['nodes'][atlas.masks[receiver]]])
        R=atlas.mm(geom.inverse(np.array(xrows,dtype=np.uint8),atlas),np.array(yrows,dtype=np.uint8))
        full={v:atlas.mm(np.array([[(v>>s)&1 for s in range(6)]],dtype=np.uint8),R)[0] for v in range(64)}
        require(all(geom.xor(power(t,3) for t in full[v])==quad(v)^polar(v,a) for v in range(64)),
                'actual global parameter Hermitian norm identity')
        coeff=atlas.mm(moore_inverse,np.array([full[1<<r] for r in range(6)],dtype=np.uint8))
        require(all(np.array_equal(atlas.mm(np.array([[power(v,1<<s) for s in range(6)]],dtype=np.uint8),coeff)[0],full[v]) for v in range(64)),
                'the complete linearized polynomial')
        require(a!=0 and np.any(coeff[4]), 'nonzero centre forces a nonzero v16 coefficient')
        native.append({'donor':donor,'centre':h,'node':a,'R_coefficients':coeff.tolist(),'r4':coeff[4].tolist()})

    # General norm identity check: no nonzero a is invariant under multiplication by omega.
    failed_invariance={a:next(v for v in range(64) if (quad(v)^polar(v,a))!=(quad(int(product[omega,v]))^polar(int(product[omega,v]),a))) for a in nodes if a}
    require(len(failed_invariance)==27,'all nonzero centres have an exact invariance counterexample')
    require(all(quad(int(product[omega,v]))==quad(v) for v in range(64)), 'the original q is F4 invariant')
    result={'status':'PASS_GEOMETRIC_CORE_AND_QUADRATIC_PENCIL_GATE',
            'ordered_node_pairs':len(incidence),'full_core_intersection':2,'propagation_core_intersection':1,
            'native_H':h,'native_node':a,'native_ports':local['chart'].ports,
            'schur_matrix_rank':6,'proportional_weight_T_rank':3,
            'nonzero_node_invariance_counterexamples':failed_invariance,
            'native_parameter_bindings':native,'new_complete_kappa':False,
            'scope':'Preserved old geometric fibres and the quadratic-annihilator central readout; moving fibres/general H providers remain open.'}
    (out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'NODE-OVERLAPS.json').write_text(json.dumps(incidence,indent=2)+'\n')
    print(result['status'],flush=True)


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    execute(args.repo.resolve(),args.out.resolve())
