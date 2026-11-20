#!/usr/bin/env python3
"""Independent owner and S028 target check of the three partial star words."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
import gzip,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

N=111*3840
def require(v,msg):
    if not v:
        raise ValueError(msg)

def pinned(path,s):
    b=path.read_bytes()
    if path.suffix=='.gz':
        b=gzip.decompress(b)
    require(sha256(b).hexdigest()==s,'authenticated '+path.name)
    return b

def native(repo):
    b=repo/'research/moonshot-005-program/results'
    g=json.loads(pinned(b/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'))
    rr=pinned(b/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
    target=json.loads(pinned(b/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json','deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601'))
    roots=np.array(g['root_table'],dtype=int)
    ortho=(roots@roots.T)==0
    H=[set(p) for p in g['A2']];D=[set(q) for q in g['D4']]
    ordered={};movement=Counter()
    for row in map(json.loads,rr.splitlines()):
        ph,j,c,h,d,k,l,i=row
        key=(ph=='Y')*53280+480*j+c
        require(key not in ordered and 0<=c<480,'unique physical base owner')
        ordered[key]=row
        if h is not None:
            require(H[h]<=D[d] and (l is None or l in H[h]),'real left plane path')
        if k is not None:
            require(all(ortho[a,x] for a in H[k] for x in D[d]) and (i is None or i in H[k]),
                    'real right plane path')
        require((ph=='X' and l==j) or (ph=='Y' and i==j),'correct genuine endpoint')
        heights=[t for t,v in [(1,l),(2,h),(4,d),(6,k),(7,i)] if v is not None]
        heights=heights+[8] if ph=='X' else [0]+heights
        for a,z in zip(heights,heights[1:]):movement[z-a]+=1
        require(heights[-1]-heights[0]==7,'path rank rise')
    require(set(ordered)==set(range(106560)),'every 8-copy route owner')
    require(movement=={1:267060,2:216390,4:11520},'all base movement events')
    for f,j,ell in target['row_transfers']:
        require(f==80 and ortho[f,j] and 1<=ell<=59,'true S028 row transfers')
    for i,j,ell in target['column_transfers']:
        require(j==10 and ortho[i,j] and 1<=ell<=59,'true S028 column transfers')
    return ordered,target,dict(movement)

def trace(swaps,n):
    """Both orientations of a permutation on every real binary-field holder."""
    by_dest=np.arange(n,dtype=np.int64)
    for p,q in swaps:by_dest[p],by_dest[q]=by_dest[q],by_dest[p]
    by_origin=np.argsort(by_dest)
    require(np.array_equal(by_dest[by_origin],np.arange(n)),'pure normalization on every genuine baseline')
    return by_dest,by_origin

def assignment_dual(routes,roles,stripes,side):
    """Construct and verify an exact integral dual bound for changed K assignments."""
    inputs=Counter();out=Counter();same=Counter();cap=Counter()
    for ph,j,_,_,_,k,l,i in routes.values():
        if k is None:continue
        if side=='row' and ph=='X':
            if j in roles:inputs[j,k]+=1
            if i==80:cap[k]+=1
            if j in roles and i==80:same[j,k]+=1
        if side=='column' and ph=='Y':
            if l==10:cap[k]+=1
            if j in roles:inputs[j,k]+=1
            if j in roles and l==10:same[j,k]+=1
    klabels=sorted(cap);ridx={j:t for t,j in enumerate(roles)};kidx={k:t for t,k in enumerate(klabels)}
    cols=[]
    for (j,k),v in sorted(inputs.items()):
        m=min(v,cap[k]);free=same[j,k]
        if free:cols.append((ridx[j],kidx[k],0,free))
        if m>free:cols.append((ridx[j],kidx[k],1,m-free))
    m=len(cols); ones=np.ones(m)
    row=coo_matrix((ones,([v[0] for v in cols],np.arange(m))),shape=(len(roles),m))
    krow=coo_matrix((ones,([v[1] for v in cols],np.arange(m))),shape=(len(klabels),m))
    caps=[cap[k] for k in klabels]
    lp=linprog([v[2] for v in cols],A_eq=row,b_eq=[stripes]*len(roles),A_ub=krow,b_ub=caps,
               bounds=[(0,v[3]) for v in cols],method='highs')
    require(lp.success,'true assignment feasible')
    y=np.rint(lp.eqlin.marginals).astype(int);z=np.rint(lp.ineqlin.marginals).astype(int)
    require((z<=0).all(),'valid capacity dual signs')
    # This integer inequality is valid for every assignment by weak duality.
    bound=stripes*sum(map(int,y))+sum(c*int(t) for c,t in zip(caps,z))
    bound+=sum(u*min(0,c-int(y[r])-int(z[k])) for r,k,c,u in cols)
    return bound

def check_one(name,axes,path,meta,routes,target):
    payload=gzip.decompress(path.read_bytes())
    require(sha256(payload).hexdigest()==meta['word_payload'],'word digest')
    w=json.loads(payload);ordtags=['source_X','K_X','K_Y','F_Y']
    words={};cost={}
    for tag in ordtags:
        runs=[]
        for pos,pairs in w['field_swap_words'][tag].items():
            for a,b in pairs:
                p,q=routes[a//8],routes[b//8]
                expected='X' if tag.endswith('X') else 'Y'
                require(p[0]==q[0]==expected and a!=b,'two distinct carriers at the proper wave')
                loc=1 if tag in ('source_X','F_Y') else 5
                require(p[loc]==q[loc]==int(pos),'two carriers meet at the specified phase location')
                if tag=='F_Y':require(p[7]==q[7]==int(pos),'real terminal facet')
                delta=N if expected=='Y' else 0
                runs.append((a-delta,b-delta))
        words[tag]=runs;cost[tag]=len(runs)
    x_at,_=trace(words['source_X']+words['K_X'],N)
    _,y_to=trace(words['K_Y']+words['F_Y'],N)
    actual=set();capture_positions=Counter();tap_positions=Counter()
    def toggle(output,source):
        item=output,source
        if item in actual:actual.remove(item)
        else:actual.add(item)
    for x,c in w['F80_capture_owner_to_central_position']:
        require(routes[x//8][0]=='X' and routes[x//8][7]==80,'physical row capture at F80')
        toggle(80*3840+c,int(x_at[x]));capture_positions[c]+=1
    for c,y in w['line10_central_position_to_Y_owner']:
        require(routes[y//8][0]=='Y' and routes[y//8][6]==10,'physical Y passes the true line-10 cache')
        require(routes[(10*3840+c)//8][6]==10,'unchanged centre X captured at its true source line')
        toggle(int(y_to[y-N]),10*3840+c);tap_positions[c]+=1
    chosen=[4*s+t for s in range(16) for t in axes];d=len(chosen)
    require(capture_positions==tap_positions==Counter({c:48 for c in chosen}),'all true simultaneous stars')
    row={ell:j for f,j,ell in target['row_transfers'] if ell<=48}
    column={ell:i for i,j,ell in target['column_transfers'] if ell<=48}
    expect={(80*3840+c,j*3840+64*ell+c) for ell,j in row.items() for c in chosen}
    expect|={(i*3840+64*ell+c,10*3840+c) for ell,i in column.items() for c in chosen}
    require(actual==expect,'every proper coefficient equals the authenticated target projection')
    # Recompute the sparse square without using the support argument.
    by_src=defaultdict(list)
    for dst,src in actual:by_src[src].append(dst)
    square=Counter((dst2,src) for dst,src in actual for dst2 in by_src.get(dst,()))
    require(square and all(v==4 for v in square.values()),'proper square cancels four equal paths in characteristic two')
    require(len(square)==d,'one double-star endpoint per selected central field')
    incidence={}
    for side,roster in [('row',row),('column',column)]:
        changed=0;used_in=set();used_out=set()
        paths=w[side+'_base_paths']
        require(set(map(int,paths))==set(roster.values()),'exact target roles')
        for role,items in paths.items():
            require(len(items)==d//8,'all eight true copies in each selected route bundle')
            for k,a,b in items:
                p,q=routes[a],routes[b]
                require(a not in used_in and b not in used_out and p[5]==q[5]==k,'injective true K assignment')
                used_in.add(a);used_out.add(b)
                if side=='row':require(p[0]==q[0]=='X' and p[1]==int(role) and q[7]==80,'actual early assignment')
                else:require(p[0]==q[0]=='Y' and p[6]==10 and q[1]==int(role),'actual late assignment')
                changed+=a!=b
        lower=assignment_dual(routes,list(roster.values()),d//8,side)
        require(lower==changed,'exact integer dual matches actual changed-destination count')
        incidence[side]=changed
    total=36*sum(cost.values())+6*(2*48*d+2*d)
    require(total==meta['total_ADD'] and 12*d==meta['INIT']==meta['dirty_CLEAR'],'full paid field word and all caches')
    require(cost==meta['field_swaps'],'exact stagewise swap count')
    # Swapping two F80 accumulation targets keeps both ranks and permutation words.
    c0,c1=chosen[:2]
    changed={(80*3840+c1 if dst==80*3840+c0 else 80*3840+c0 if dst==80*3840+c1 else dst,src)
             for dst,src in actual}
    require(changed!=expect,'rank-preserving receiver-labelling control changes actual S028 target')
    return {'binary_ADD':total,'binary_INIT':12*d,'binary_dirty_CLEAR':12*d,'late_and_early_field_swaps':cost,
            'minimum_changed_K_assignments':incidence,'independent_X_baselines':N,'independent_Y_baselines':N,
            'proper_nonzero_field_coefficients':len(actual),'proper_rank':2*d,'proper_square_zero':True,
            'aligned_tail_roles':[row[e] for e in row if row[e]==column[e]],'rank_I_plus_proper':N,
            'negative_control':'F80 output label transposition changes proper target','extra_MOVE':0}

def main():
    p=ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--words',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    routes,target,movement=native(a.repo);meta=json.loads((a.words/'RESULT.json').read_bytes())
    reports={}
    for name,axes in [('cross',[0]),('half',[0,1]),('three_quarters',[0,1,2])]:
        reports[name]=check_one(name,axes,a.words/(name+'-word.json.gz'),meta['results'][name],routes,target)
    row=sum(r[0]=='X' and r[7]==80 for r in routes.values())
    col=sum(r[0]=='Y' and r[6]==10 for r in routes.values())
    require(row==col==360 and 48*8>360,'four-axis direct bundle total capacity')
    result={'paid_crossings':reports,'unchanged_MOVEs_per_single_route_copy_by_height':movement,
            'direct_four_axis_required_bundles':384,'actual_early_and_late_capacities':(row,col),'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print([(p,r['binary_ADD']) for p,r in reports.items()])

if __name__=='__main__':
    main()
