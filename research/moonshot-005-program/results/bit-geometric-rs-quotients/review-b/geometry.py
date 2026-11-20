"""Verify literal node assignments without the author's Witt-basis algorithm."""
from types import SimpleNamespace

def reconstruct(layout,basis,f):
    columns=basis['lattice_basis_columns'];masks=basis['hyperbolic_basis_masks']
    f.need(f.binary_rank(masks)==8,'eight independent hyperbolic lattice masks')
    change={f.xor(masks[k] for k in range(8) if t>>k&1):t for t in range(256)}
    roots=[]
    # The supplied lattice columns admit these direct integer coordinates.
    # Recomposition checks every root, independently of rational inversion.
    for x in layout['root_table']:
        c=[0]*8;c[7]=x[7];c[6]=x[6];c[5]=x[5];c[3]=x[3]
        numerators={0:x[0]-x[3]-x[5]-x[6],1:x[1]-x[3]-x[5]-x[7],
                    2:x[2]-x[3]-x[6]-x[7],4:x[4]-x[5]-x[6]-x[7]}
        f.need(all(v%2==0 for v in numerators.values()),'integral native lattice coordinates')
        for i,v in numerators.items():c[i]=v//2
        f.need([sum(c[j]*columns[j][i] for j in range(8)) for i in range(8)]==x,'literal real-root recomposition')
        roots.append(change[sum((v&1)<<i for i,v in enumerate(c))])
    f.need(len(set(roots))==120 and set(roots)=={v for v in range(256) if f.q8(v)},'all nonsingular binary roots')
    real=layout['root_table'];perp=[]
    for i,x in enumerate(real):
        f.need(sum(a*a for a in x)==4,'native real root norm')
        adjacent={j for j,y in enumerate(real) if sum(a*b for a,b in zip(x,y))==0}
        f.need(adjacent=={j for j,y in enumerate(roots) if j!=i and not f.b8(roots[i],y)},'real foreign orthogonality equals binary polarity')
        perp.append(adjacent)
    planes=list(map(frozenset,layout['A2']))
    f.need(len(planes)==1120 and all(len(H)==3 and f.xor(roots[j] for j in H)==0 for H in planes),'all actual anisotropic H planes')
    stars={j:[h for h,H in enumerate(planes) if j in H] for j in range(120)}
    f.need(all(len(hs)==28 for hs in stars.values()),'twenty-eight geometric planes through every donor')
    return SimpleNamespace(roots=roots,planes=planes,stars=stars,perp=perp)

def assignment(ctx,record,f,Q):
    j=record['anchor'];h0=record['base_H'];nodes={int(h):a for h,a in record['nodes'].items()}
    f.need(h0==ctx.stars[j][0] and set(nodes)==set(ctx.stars[j]) and set(nodes.values())==set(Q),
           'all literal source-plane labels bind the 28 geometric nodes')
    J=ctx.roots[j];U0=ctx.roots[min(ctx.planes[h0]-{j})]
    complement={w for w in range(256) if not f.b8(w,J) and not f.b8(w,U0)}
    f.need(len(complement)==64 and sum(not f.q8(w) for w in complement)==28,'six-dimensional minus complement')
    by_plane={}
    for h in ctx.stars[j]:
        choices=[]
        for u in ctx.planes[h]-{j}:
            U=ctx.roots[u]
            w=U^U0^(J if f.b8(U0,U) else 0)
            f.need(w in complement and not f.q8(w),'actual singular complement point')
            choices.append(w)
        f.need(len(set(choices))==1,'plane coordinate independent of its nonanchor root representative')
        by_plane[h]=choices[0]
    f.need(len(set(by_plane.values()))==28 and nodes[h0]==0,'one node per singular complement point')
    selected=[];images=[]
    for h in ctx.stars[j]:
        w=by_plane[h]
        if f.binary_rank(selected+[w])>len(selected):
            selected.append(w);images.append(nodes[h])
    f.need(len(selected)==6 and f.binary_rank(images)==6,'literal singular-node labels determine a binary isomorphism')
    isometry={f.xor(selected[k] for k in range(6) if m>>k&1):f.xor(images[k] for k in range(6) if m>>k&1) for m in range(64)}
    f.need(set(isometry)==complement and set(isometry.values())==set(range(64)),'complete extension of the literal node map')
    f.need(all(f.q8(w)==f.q6(a) for w,a in isometry.items()),'quadratic isometry on all sixty-four complement vectors')
    f.need(all(isometry[by_plane[h]]==nodes[h] for h in nodes),'all node labels agree with the independently extended isometry')
    receivers={};views={}
    for r in sorted(ctx.perp[j]):
        R=ctx.roots[r];w=R^(J if f.b8(U0,R) else 0)
        f.need(w in complement,'receiver projection is in the same complement')
        v=isometry[w];f.need(v!=0,'foreign receiver has nonzero field parameter')
        hs=[h for h in ctx.stars[j] if ctx.planes[h]<=ctx.perp[r]]
        block={a for a in Q if f.b6(v,a)==(f.q6(v)^1)}
        f.need(len(hs)==len(block)==16 and {nodes[h] for h in hs}==block,'actual geometric receiver view is the exact field block')
        receivers[r]=v;views[r]=hs
    f.need(len(receivers)==63 and set(receivers.values())==set(range(1,64)),'all sixty-three geometric receiver blocks')
    return SimpleNamespace(nodes=nodes,isometry=isometry,receivers=receivers,views=views,base_H=h0)
