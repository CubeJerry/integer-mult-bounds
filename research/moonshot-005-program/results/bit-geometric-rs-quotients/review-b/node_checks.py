"""Check all literal geometric node assignments and native propagation spans."""
from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json

def verify(ctx,assignments,certificate,f,geometry,Q,polynomials):
    native=set(range(111))
    singleton={next(iter(H & native)) for H in ctx.planes if len(H & native)==1}
    eligible=native-singleton-{10}
    f.need(len(assignments)==99 and {r['anchor'] for r in assignments}==eligible,'exact ninety-nine eligible geometric source assignments')
    witnesses={r['anchor']:r for r in certificate}
    root_index={x:j for j,x in enumerate(ctx.roots)}
    summaries=[];selected_hist=Counter();full_hist=Counter();family_sizes=Counter();native_centre_ranks=Counter()
    total_native_views=0;distinct_fibres=0;native_pair_ranks=Counter();native_pair_sizes=Counter()
    for literal in assignments:
        j=literal['anchor'];source=geometry.assignment(ctx,literal,f,Q);record=witnesses[j]
        total_native_views+=sum(r<111 for r in source.views)
        by_h={h:{r for r in source.views if r<111 and r!=80 and h in source.views[r]} for h in ctx.stars[j]}
        for h,rr in by_h.items():
            native_centre_ranks[f.binary_rank(source.receivers[r] for r in rr)]+=1
        for h,k in combinations(ctx.stars[j],2):
            rr=by_h[h]&by_h[k];rank=f.binary_rank(source.receivers[r] for r in rr)
            f.need(rank==5,'every native common-two-node family has exact Moore rank five')
            native_pair_ranks[rank]+=1;native_pair_sizes[len(rr)]+=1
        @lru_cache(None)
        def fibre(h,r):
            hs=source.views[r]
            f.need(h in hs,'actual anchor centre seen by receiver')
            p=f.polynomial(source.nodes[q] for q in hs if q!=h)
            f.need(p==f.divide(polynomials[source.receivers[r]],source.nodes[h]),'actual source fibre equals field-block division')
            f.need(len(p)==16 and p[-1]==1 and all((f.evaluate(p,source.nodes[q])==0)==(q!=h) for q in hs),
                   'complete original inverse fibre at the native view')
            return p
        left,right=record['leaf_donors'];h1,h2,h3=record['centres'];i=record['final_receiver']
        f.need(left in eligible and right in eligible and len({j,left,right})==3,'three ordinary nonexceptional source roles')
        f.need({j,left}<=ctx.planes[h1] and {j,right}<=ctx.planes[h2] and {left,right}<=ctx.planes[h3],'actual native triangle')
        f.need(i<111 and i!=80 and ctx.planes[h3]<=ctx.perp[i] and j not in ctx.perp[i],'unmodified final receiver outside anchor star')
        rows=[];mapped=[];old_control=None
        for branch,leaf,h in zip(record['propagations'],[left,right],[h1,h2]):
            f.need(branch['leaf']==leaf and branch['centre']==h,'literal quotient propagation edge')
            expected={q for q in ctx.stars[leaf] if q!=h3 and ctx.planes[q]<=ctx.perp[i]}
            f.need(len(expected)==15 and h not in expected and len(branch['quotient_propagations'])==15,'complete final off-centre quotient set')
            third=next(iter(ctx.planes[h]-{j,leaf}));C=ctx.roots[third]
            reflect=lambda u:root_index[ctx.roots[u]^(C if f.b8(C,ctx.roots[u]) else 0)]
            f.need(reflect(j)==leaf and reflect(leaf)==j,'binary transvection exchanges the two actual donors')
            used=set();found=[]
            for entry in branch['quotient_propagations']:
                q=entry['leaf_plane'];R=entry['anchor_plane'];selected=entry['receivers']
                f.need(q in expected and q not in used and R in ctx.stars[j] and R!=h,'off-centre quotient roles')
                f.need({reflect(u) for u in ctx.planes[q]}==ctx.planes[R],'actual reflected leaf-plane correspondence')
                required=ctx.planes[h]|ctx.planes[q]|ctx.planes[R]
                full=[r for r in range(111) if r!=80 and required<=ctx.perp[r]]
                pair=[r for r in range(111) if r!=80 and ctx.planes[h]|ctx.planes[R]<=ctx.perp[r]]
                f.need(full==pair and len(selected)==len(set(selected))==15 and set(selected)<=set(full),
                       'complete valid native family and the literal selected fifteen')
                ranks=[]
                for receivers in (selected,full):
                    vectors=[fibre(h,r) for r in receivers]
                    rank=f.rank(vectors);binary=f.binary_rank(source.receivers[r] for r in receivers)
                    f.need(rank==binary==5,'both native propagation families have exact rank five')
                    f.need(all(not f.evaluate(p,source.nodes[R]) for p in vectors),'all actual fibres vanish at the transported second node')
                    ranks.append(rank)
                selected_hist[ranks[0]]+=1;full_hist[ranks[1]]+=1;family_sizes[len(full)]+=1
                if old_control is None:
                    old_nodes={q:n+1 for n,q in enumerate(ctx.stars[j])}
                    old=[f.polynomial(old_nodes[q] for q in source.views[r] if q!=h) for r in selected]
                    f.need(f.rank(old)==15,'same literal observations had rank fifteen under predecessor node labels')
                    old_control={'centre':h,'leaf_plane':q,'anchor_plane':R,'old_rank':15,'new_rank':5}
                rows.append({'centre':h,'leaf':leaf,'leaf_plane':q,'anchor_plane':R,'selected_receivers':selected,
                             'all_native_receivers':full,'selected_rank':ranks[0],'all_native_rank':ranks[1]})
                used.add(q);found.append(R)
            f.need(used==expected and len(set(found))==15,'all propagated leaf quotients covered exactly once')
            mapped.append(found)
        f.need(mapped==record['distinct_anchor_plane_sets'] and len(rows)==30,'same frozen thirty-record triangle')
        f.need(literal['selected_rank_histogram']=={'5':30} and literal['full_rank_histogram']=={'5':30} and not literal['obstructed'],
               'published geometric-node rank receipts match')
        distinct_fibres+=fibre.cache_info().currsize
        summaries.append({'anchor':j,'base_H':source.base_H,'node_labels':source.nodes,
                          'source_node_sha256':sha256(json.dumps(source.nodes,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
                          'geometric_views':63,'native_views':sum(r<111 for r in source.views),'propagations':rows,
                          'changed_information_control':old_control})
    f.need(selected_hist==full_hist=={5:2970},'complete scalar escape census')
    f.need(native_centre_ranks=={6:2772} and native_pair_ranks=={5:37422},'all native centre and pair families')
    fault=json.loads(json.dumps(assignments[0]));labels=sorted(map(int,fault['nodes']))
    a,b=map(str,labels[1:3]);fault['nodes'][a],fault['nodes'][b]=fault['nodes'][b],fault['nodes'][a]
    try:
        geometry.assignment(ctx,fault,f,Q)
    except ValueError:
        pass
    else:
        raise ValueError('nongeometric node permutation was not rejected')
    return {'status':'PASS_INDEPENDENT_NINETY_NINE_GEOMETRIC_RS_NODE_SYSTEMS','anchors':99,
            'geometric_source_views':99*63,'native_source_views':total_native_views,
            'selected_propagation_rank_histogram':dict(selected_hist),'all_native_propagation_rank_histogram':dict(full_hist),
            'native_receiver_family_size_histogram':dict(family_sizes),'native_fixed_centre_span_rank_histogram':dict(native_centre_ranks),
            'native_all_common_node_pair_span_rank_histogram':dict(native_pair_ranks),
            'native_all_common_node_pair_receiver_count_histogram':dict(native_pair_sizes),'nongeometric_node_permutation_rejected':True,
            'distinct_actual_inverse_fibres':distinct_fibres,'witnesses':summaries}
