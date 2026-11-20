"""Two native H charts on shared geometric sources with protected moving fibres."""
from pathlib import Path
import importlib.util, json
import numpy as np


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(repo):
    base = repo/'research/moonshot-005-program/results'
    geometric = module(base/'bit-coupled-native-geometric-h-source/component/construction.py', 'moving_geometry')
    families, atlas, previous = geometric.context(repo)
    parameters = json.loads((base/'bit-coupled-native-geometric-h-source/component/output/PARAMETERS.json').read_text())
    cycle = json.loads((base/'bit-coupled-native-geometric-cycle-source/component/output/PARAMETERS.json').read_text())
    return geometric, families, atlas, previous, parameters, cycle


def fibre(geometric, atlas, v, centre):
    """The normalized scalar coefficient vector U_c(v), with degree at most15."""
    numerator = np.zeros(17,dtype=np.uint8)
    power = lambda x,n:geometric.power(int(x),n,atlas)
    for degree,exponent in [(8,1),(16,2),(14,4),(5,4),(1,8),(2,16),(4,32)]:
        numerator[degree] ^= power(v,exponent)
    numerator[0] ^= geometric.xor(atlas.product[numerator[d],power(centre,d)] for d in range(17))
    answer = np.zeros(16,dtype=np.uint8)
    answer[15] = numerator[16]
    for d in range(14,-1,-1):
        answer[d] = numerator[d+1]^atlas.product[centre,answer[d+1]]
    require(numerator[0] == atlas.product[centre,answer[0]], 'literal U polynomial division')
    return answer


def extend(geometric, atlas, previous, family, X, Y, tag):
    """Extend a compatible prescribed map on columns X, with a declared free tail."""
    require(atlas.rank(np.vstack((X,Y))) == atlas.rank(X), 'consistent prescribed linear map')
    _,columns = geometric.rref(X,atlas)
    basis = X[:,columns]
    target = Y[:,columns]
    _,rows = geometric.rref(basis.T,atlas)
    result = np.zeros((Y.shape[0],X.shape[0]),dtype=np.uint8)
    result[:,rows] = atlas.mm(target,geometric.inverse(basis[rows],atlas))
    annihilator = previous.null_basis(basis.T,atlas).T
    result ^= atlas.mm(family.coefficients(tag,(Y.shape[0],len(annihilator))),annihilator)
    require(np.array_equal(atlas.mm(result,X),Y), 'all prescribed columns retained')
    return result


def build(repo):
    geometric,family,atlas,previous,parameters,cycle = load(repo)
    first,second,shared = 263,642,61
    eye = np.eye(3,dtype=np.uint8)
    original_geometry = geometric.geometry
    old = geometric.build(family,atlas,previous,parameters)
    chart0,old_nodes,old_receiver,old_E,old_E2 = original_geometry(family,atlas,parameters)
    omega = int(parameters['omega'])
    power = lambda x,n:geometric.power(int(x),n,atlas)
    quadratic = lambda x:geometric.quadratic(int(x),atlas)
    polar = lambda x,y:quadratic(x^y)^quadratic(x)^quadratic(y)

    # A Hermitian orthonormal field basis makes the source-node chart respect F4.
    def hermitian(x,y):
        return int(atlas.product[x,power(y,8)]^atlas.product[power(x,4),power(y,32)]^atlas.product[power(x,16),power(y,2)])
    unit=[]
    for _ in range(3):
        unit.append(next(x for x in range(1,64) if quadratic(x) and all(not hermitian(y,x) for y in unit)))
    require(unit == [1,6,11] and all(hermitian(x,y)==int(i==j) for i,x in enumerate(unit) for j,y in enumerate(unit)),
            'literal Hermitian orthonormal field basis')
    field_basis=parameters['F4_basis']
    coordinates={geometric.xor(field_basis[s] for s in range(6) if mask>>s&1):
                 tuple(((mask>>(2*p))&1)^int(atlas.product[omega,(mask>>(2*p+1))&1]) for p in range(3))
                 for mask in range(64)}
    new_nodes={x:geometric.xor(atlas.product[r,y] for r,y in zip(coordinates[t],unit)) for x,t in old_nodes.items()}
    require(len(set(new_nodes.values()))==64 and all(quadratic(t)==atlas.algebra.quadratic(x) for x,t in new_nodes.items()),
            'new source-node quadratic isometry')

    def changed_geometry(f,a,prm):
        return (chart0,new_nodes,{i:tuple(int(a.product[t,t]) for t in r) for i,r in old_receiver.items()},
                a.product[old_E,old_E],a.product[old_E2,old_E2])
    squared_parameters=json.loads(json.dumps(parameters))
    squared_parameters['weights']=[[int(atlas.product[t,t]) for t in row] for row in parameters['weights']]
    geometric.geometry=changed_geometry
    try:
        adapted=geometric.build(family,atlas,previous,squared_parameters)
    finally:
        geometric.geometry=original_geometry
    require(all(not np.any(C[:,3:6]) and atlas.rank(C[:,:3])==3 for C in adapted['controls']),
            'the adapted central controls kill z and retain the constant core')
    chart=adapted['chart']
    maps={j:dict(rows) for j,rows in adapted['maps'].items()}
    base_nodes={j:{h:0 if h==first else new_nodes[chart.point[j][h]] for h in atlas.by_donor[j]} for j in chart.donors}
    point=chart.point[shared][second]
    node=int(new_nodes[point])
    companions={j:next(h for h,x in chart.point[j].items() if x==point) for j in chart.donors}
    require(companions=={0:116,61:642,62:643} and node==60, 'the three reflected actual companion planes')
    visible=[v for v in range(1,64) if quadratic(v)==1 and not polar(v,node)]
    P0=np.array([fibre(geometric,atlas,v,node) for v in visible],dtype=np.uint8).T
    _,pivots=geometric.rref(P0,atlas)
    P=np.kron(P0[:,pivots],eye)
    require(len(visible)==20 and P.shape==(48,15), 'the actual companion propagation core')
    for p,j in enumerate(chart.donors):
        S=adapted['core'];C=adapted['controls'][p]
        X=np.hstack((S,P));Y=np.hstack((atlas.mm(C,S),np.zeros((3,15),dtype=np.uint8)))
        require(atlas.rank(X)==30, 'geometric18+15 cores intersect in3')
        maps[j][first]=extend(geometric,atlas,previous,family,X,Y,f'two-h-A-tail/{j}/{node}/0')

    # The second actual H provider uses the same geometric bank as the shared donor.
    reference=geometric.build(family,atlas,previous,cycle['local'][str(second)])
    chart2=reference['chart']
    point_nodes={chart2.point[shared][h]:base_nodes[shared][h] for h in atlas.by_donor[shared] if h!=second}
    Q=[x for x in range(64) if not quadratic(x)]
    require(len(point_nodes)==27 and set(point_nodes.values())==set(Q)-{node}, 'one complete second-centre node chart')
    blocks={frozenset(x for x in Q if polar(v,x)==1^quadratic(v)):v for v in range(1,64)}
    second_fibres={};receiver_parameters={}
    for i in chart2.views:
        observed=frozenset(base_nodes[shared][h] for h in atlas.by_donor[shared] if atlas.planes[h]<=atlas.adj[i])
        v=blocks[observed]
        receiver_parameters[i]=v
        second_fibres[i]=np.kron(fibre(geometric,atlas,v,node)[:,None],eye)
    X=np.hstack(list(second_fibres.values()))
    require(atlas.rank(X)==18,'second-centre normalized geometric core')
    second_controls={}
    for p,j in enumerate(chart2.donors):
        Y=np.hstack([reference['pencils'][i][p] for i in chart2.views])
        second_controls[j]=extend(geometric,atlas,previous,family,X,Y,f'two-h-B-tail/{j}/{node}/0')
    for j in chart.donors:
        maps[j][companions[j]]=second_controls[shared]
    for j in chart2.donors:
        if j==shared:
            continue
        base_nodes[j]={h:node if h==second else point_nodes[chart2.point[j][h]] for h in atlas.by_donor[j]}
        maps[j]={h:second_controls[j] if h==second else np.kron(atlas.vandermonde([base_nodes[j][h]],16),eye)
                 for h in atlas.by_donor[j]}
    return {'geometric':geometric,'family':family,'atlas':atlas,'previous':previous,
            'first':first,'second':second,'shared':shared,'charts':{first:chart,second:chart2},
            'Hwords':{first:adapted['Hword'],second:reference['Hword']},'maps':maps,'base_nodes':base_nodes,
            'companions':companions,'field_unit_basis':unit,'first_old_points':adapted['points'],
            'second_old_fibres':second_fibres,'second_receiver_parameters':receiver_parameters,
            'actual_early_seeds':{j:0 for j in maps}}
