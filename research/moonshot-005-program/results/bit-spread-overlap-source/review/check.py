#!/usr/bin/env python3
"""Independent native reconstruction, source/phase and packed chart review."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256, shake_256
import importlib.util
import json
from pathlib import Path
import numpy as np

def require(ok,msg):
    if not ok:
        raise ValueError(msg)

def import_review(path):
    spec = importlib.util.spec_from_file_location('independent_gf',path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def pseudo(tag,m,n):
    return np.frombuffer(shake_256(tag.encode('ascii')).digest(m*n),dtype=np.uint8).reshape(m,n)&63

class Native:
    def __init__(self,repo,field):
        self.f = field
        base = repo/'research/moonshot-005-program/results'
        def load(stem,digest):
            return json.loads(field.read_source(base,stem,digest))
        l = load('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72')
        spread = load('bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz','7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab')
        docs = field.read_source(base,'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
        self.H = [set(r) for r in l['A2']]
        self.D = [set(r) for r in l['D4']]
        R = np.array(l['root_table'],dtype=int)
        self.adj = [set(map(int,np.flatnonzero(r))) for r in R@R.T==0]
        self.rad = [set(r)-{0} for r in spread['D_radicals']]
        self.marked = set(spread['selected_D'])
        self.hlist = {j:[h for h,P in enumerate(self.H) if j in P] for j in range(111)}
        self.views = {(j,i):[h for h in self.hlist[j] if self.H[h]<=self.adj[i]] for j in range(111) for i in self.adj[j]}
        self.early = Counter()
        for line in docs.splitlines():
            phase,j,coord,h,_,_,source,_ = json.loads(line)
            if phase=='X':
                require(j==source,'early donor original')
                self.early[j,h]+=1

class Chart:
    def __init__(self,n,h,k):
        self.native=n
        self.k,self.h=k,h
        self.donors=sorted(n.H[h])
        self.receivers=[i for i in range(120) if n.H[h]<=n.adj[i]]
        self.all_ports=[d for d,Q in enumerate(n.D) if n.H[h]<=Q]
        self.ports=[d for d in self.all_ports if (d in n.marked)==(k==3)]
        self.point={}
        for j in self.donors:
            dd={}
            for p in n.hlist[j]:
                if p==h: continue
                contains=[n.rad[d] for d in self.all_ports if n.H[p]<=n.D[d]]
                require(len(contains)==5,'native five ports of off-plane')
                common=set.intersection(*contains)
                require(len(common)==1,'native point ID from D radicals')
                dd[p]=common.pop()
            require(len(set(dd.values()))==27,'off-plane bijection')
            self.point[j]=dd
        self.xs=sorted(set(self.point[self.donors[0]].values()))
        self.V=n.f.power_matrix(range(1,3*k+1),3*k)
        self.ix={j:q for q,j in enumerate(self.donors)}

    def core(self,seed):
        k=self.k
        rows={p:[] for p in self.xs}
        for q,d in enumerate(self.ports):
            diff=np.zeros((2,6*k),dtype=np.uint8)
            diff[0,:2*k]=self.V[q,:2*k]
            diff[1,:k]=self.V[q,:k]
            diff[1,2*k:3*k]=self.V[q,2*k:]
            for attempt in range(100):
                g=pseudo(f'core/{self.h}/{k}/{seed}/{d}/{attempt}',2,2)
                det = self.native.f.MUL[g[0,0],g[1,1]] ^ self.native.f.MUL[g[0,1],g[1,0]]
                if det: break
            require(det,'2x2 share relabel')
            w=np.vstack([np.zeros(6*k,dtype=np.uint8),self.native.f.matmul(g,diff)])
            w[:,3*k+q]=1
            for x,val in zip(sorted(self.native.rad[d]),w):
                rows[x].append(val)
        return {x:np.array(v,dtype=np.uint8) for x,v in rows.items()}

    def hermite(self,x,m,width):
        p=self.native.f.power_matrix([x],width)[0]
        return np.array([[p[c-r] if r<=c and (r&c)==r else 0 for c in range(width)] for r in range(m)],dtype=np.uint8)

    def single(self,params):
        k=self.k
        rows=self.core(params['core'])
        tab={}
        for t,p in enumerate(self.xs,1):
            B=np.zeros((k,16*k),dtype=np.uint8)
            B[:k//3,:6*k]=rows[p]
            B[k//3:,:6*k]=pseudo(f'fill/{self.h}/{k}/{params["fill"]}/{p}',2*k//3,6*k)
            B[k//3:,6*k:]=self.hermite(t,2*k//3,10*k)
            tab[p]=B
        mult={}
        eye=np.eye(16*k,dtype=np.uint8)
        for j in self.donors:
            j0=self.ix[j]
            mult[j]={p:tab[x] for p,x in self.point[j].items()}
            mult[j][self.h]=eye[k*j0:k*(j0+1)]
        return mult

def nullspace(M,f):
    A=M.copy()
    piv=[]
    for i in range(A.shape[1]):
        rs=np.flatnonzero(A[len(piv):,i])
        if not len(rs): continue
        k=len(piv)
        u=int(rs[-1])+k
        A[[k,u]]=A[[u,k]]
        A[k]=f.MUL[f.INVERSE[A[k,i]],A[k]]
        r=np.flatnonzero(A[:,i])
        r=r[r!=k]
        A[r]^=f.MUL[A[r,i,None],A[k][None,:]]
        piv.append(i)
        if len(piv)==len(A): break
    free=np.array([t for t in range(A.shape[1]) if t not in piv])
    B=np.zeros((A.shape[1],len(free)),dtype=np.uint8)
    B[free]=np.eye(len(free),dtype=np.uint8)
    B[piv]=A[:len(piv),free]
    require(not f.matmul(M,B).any(),'parameterization lies in exact common kernel')
    return B

def paired(charts,params):
    c0,c1=charts
    k=c0.k
    seven=c0.native
    f=seven.f
    shared,=set(c0.donors)&set(c1.donors)
    read,extra={},{}
    centres=[c0.h,c1.h]
    for ii,c in enumerate(charts):
        rows=c.core(params['core'])
        e={}
        for h,x in c.point[shared].items():
            m=np.zeros((k//3,12*k),dtype=np.uint8)
            m[:,6*k*ii:6*k*(ii+1)]=rows[x]
            e[h]=m
        extra[c.h]=e
        for j in c.donors:
            s=6*k*ii+k*c.ix[j]
            m=np.zeros((k,12*k),dtype=np.uint8)
            m[:,s:s+k]=np.eye(k,dtype=np.uint8)
            read[c.h,j]=m
    constraints=np.vstack([read[c.h,shared][:k//3]^extra[d.h][c.h] for c,d in ((c0,c1),(c1,c0))])
    Z=nullspace(constraints,f)
    b=Z.shape[1]
    require(b==12*k-2*k//3,'independent cross constraints')
    out={}
    for idx,h in enumerate(seven.hlist[shared],1):
        if h in centres:
            base_rows=read[h,shared]
        else:
            base_rows=np.vstack([extra[c.h][h] for c in charts])
        A=np.zeros((k,16*k),dtype=np.uint8)
        u=len(base_rows)
        A[:u,:b]=f.matmul(base_rows,Z)
        if h not in centres:
            A[u:,:b]=pseudo(f'pairfill/{centres}/{k}/{params["fill"]}/{h}',k//3,b)
            A[u:,b:]=c0.hermite(idx,k//3,16*k-b)
        out[h]=A
    all_maps={}
    for c in charts:
        table={x:out[p] for p,x in c.point[shared].items()}
        for j in c.donors:
            m={p:table[x] for p,x in c.point[j].items()}
            m[c.h]=np.hstack([f.matmul(read[c.h,j],Z),np.zeros((k,16*k-b),dtype=np.uint8)])
            if j in all_maps:
                require(all(np.array_equal(m[h],all_maps[j][h]) for h in m),'literal single 28-plane shared donor')
            all_maps[j]=m
    return all_maps

def schedule(n,c,j,maps,seed,centres):
    k=c.k
    rows=[]
    for h,F in sorted(maps.items()):
        q=n.early[j,h]//15
        Z=np.zeros_like(F)
        if q>=2:
            rows.extend((np.hstack([F,Z]),np.hstack([Z,F])))
            if q==3:
                rows.append(pseudo(f'extra/{c.h}/{k}/{j}/{h}/{seed}',k,32*k))
        elif h in centres:
            rows.append(np.hstack([F,Z]))
        else:
            E=pseudo(f'early/{c.h}/{k}/{j}/{h}/{seed}',k,2*k)
            require(n.f.eliminate(E)[0]==k,'early frame admits k independent late complements')
            rows.append(np.hstack([n.f.matmul(E[:,:k],F),n.f.matmul(E[:,k:],F)]))
    E=np.vstack(rows)
    require(E.shape==(32*k,32*k) and n.f.eliminate(E)[0]==32*k, 'true early basis on fixed bank')

def test_chart(c,maps):
    n,f,k=c.native,c.native.f,c.k
    count=0
    digest=sha256()
    changed_basis_rejected=False
    for i in c.receivers:
        pos=[t for t,d in enumerate(c.ports) if n.D[d]<=n.adj[i]]
        require(len(pos)==k,'actual receiver spread cardinality')
        V=c.V[pos]
        j0=c.donors[0]
        off=sorted(set(n.views[j0,i])-{c.h})
        first=f.matmul(V[:,:k],maps[j0][c.h])
        stacked=np.vstack([first]+[maps[j0][h] for h in off])
        right=np.zeros((16*k,k),dtype=np.uint8)
        right[:k]=np.eye(k,dtype=np.uint8)
        r,L=f.eliminate(stacked,right)
        require(r==16*k,'first exact original-coordinate H inverse')
        for j in c.donors:
            q=c.ix[j]
            M=V[:,q*k:(q+1)*k]
            require(f.eliminate(M)[0]==k, 'true H node minor')
            remainder = sorted(set(n.views[j,i])-{c.h})
            S=np.vstack([f.matmul(M,maps[j][c.h])]+[maps[j][a] for a in remainder])
            require(np.array_equal(f.matmul(S,L),right),'same original-coordinate transmission at every donor')
            if not changed_basis_rejected and i<111 and j!=j0:
                mutated=M.copy()
                mutated[0]=f.MUL[2,mutated[0]]
                require(f.eliminate(mutated)[0]==k,'mutation preserves central rank')
                require(not np.array_equal(f.matmul(f.matmul(mutated,maps[j][c.h]),L),right[:k]),
                        'one physically rescaled donor breaks the prescribed common input')
                changed_basis_rejected=True
            # The 15 off-centre planes at this receiver give the same matrices
            # (possibly permuted) on each of the three donor stars. Full rank on
            # the first stack and this explicit common right inverse prove it for all.
            require(sorted(sha256(maps[j][a].tobytes()).digest() for a in remainder)==
                    sorted(sha256(maps[j0][a].tobytes()).digest() for a in off),'equal off-plane row blocks')
        digest.update(L.tobytes())
        if i<111:
            count+=1
    require(changed_basis_rejected,'rank-preserving negative control tested')
    return count,digest.hexdigest()

def check_packing(n,params,charts,ranking):
    pair=params['pair']
    pair_ids=pair['centres']
    shared=pair['shared_donor']
    require(len(pair_ids)==2 and set(pair_ids)<=set(charts),'shared charts included')
    used=Counter(j for h in charts for j in n.H[h])
    require(used[shared]==2 and max(used[j] for j in used if j!=shared)==1, 'intended overlap only')
    allowed={j for j in used if all(n.early[j,h]<=30 for h in n.hlist[j])}
    if ranking: require(allowed==set(used),'no hidden singleton at any patched donor')
    require(all(10 not in n.H[h] and not n.H[h]<=n.adj[80] for h in charts),'unchanged target support')
    selectors={(r['H'],r['k']):r for r in params['one_centre']}
    reports={}
    base_view_count=0
    for k in (3,12):
        cache={}
        passed=set()
        cp=[Chart(n,h,k) for h in pair_ids]
        pair_maps=paired(cp,pair[str(k)])
        for j,maps in pair_maps.items():
            c=next(c for c in cp if j in c.donors)
            schedule(n,c,j,maps,pair[str(k)]['early'][str(j)],set(pair_ids))
        hresults={}
        census=0
        exterior_checks=0
        for h in charts:
            if h in pair_ids:
                c=cp[pair_ids.index(h)]
                maps=pair_maps
            else:
                c=Chart(n,h,k)
                p=selectors[h,k]
                maps=c.single(p)
                for j in c.donors:
                    schedule(n,c,j,maps[j],p['early'][str(j)],{h})
            nv,sh=test_chart(c,maps)
            hresults[h]=(nv,sh)
            census+=nv
            for j in c.donors:
                for i in n.adj[j]:
                    key=(j,i)
                    if key in passed: continue
                    vis=n.views[key]
                    if (h in vis or (j==shared and any(hh in vis for hh in pair_ids))):
                        # Checked through the exact inverse result at that specific chart.
                        passed.add(key)
                        continue
                    array=[maps[j][hh] for hh in vis]
                    idkey=tuple(sorted(sha256(F.tobytes()).digest() for F in array))
                    if idkey not in cache:
                        cache[idkey]=n.f.eliminate(np.vstack(array))[0]
                    require(cache[idkey]==16*k,'all external source full ranks')
                    passed.add(key)
                    exterior_checks+=1
        native=sum(i<111 for j,i in passed)
        require(native==sum(len(n.adj[j]&set(range(111))) for j in used),'all covered native cuts')
        base_view_count = native
        reports[k]={'chart_lift_hashes':hresults,'native_chart_receivers':census,
                    'charts_passing_rank_preserving_mutation_control':len(hresults),
                    'literal_shared_donor':shared,'all_parent_donor_cuts':len(passed),
                    'distinct_external_rank_checks':len(cache),'full_rank_native_special_pairs':native}
    expected_bg = 6470-base_view_count
    require(expected_bg==sum(len(n.adj[j]&set(range(111))) for j in range(111) if j not in used),
            'compatible background donor count')
    return {'native_donors_patched':len(used),'remaining_background_donors':111-len(used),
            'background_source_pairs':expected_bg,'singleton_donors_in_special_set':sorted(set(used)-allowed),
            'components':reports}

def main():
    p=ArgumentParser()
    p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--parameters',type=Path,required=True)
    p.add_argument('--field-review',type=Path)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--extended',action='store_true')
    args=p.parse_args()
    path=args.field_review or args.repo/'research/moonshot-005-program/results/bit-spread-h263-source/review/check.py'
    n=Native(args.repo,import_review(path))
    raw=args.parameters.read_bytes()
    params=json.loads(raw)
    data=check_packing(n,params,params['native_all_views_packing'],True)
    out={'parameter_sha256':sha256(raw).hexdigest(),'new_complete_kappa':False,
         'physical_local_23':data,'all_source_and_actual_H_rank_counts':6470,
         'all_source_and_actual_H_rank_scope':'Physical source-to-H ranks on the 23-chart special sector, combined with separately verified compatible singleton-aware background at the complement; full endpoint remains open.'}
    if args.extended:
        out['ordinary_local_24']=check_packing(n,params,params['extended_ordinary_packing'],False)
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print('PASS',data['native_donors_patched'],data['components'][3]['native_chart_receivers'])

if __name__=='__main__':
    main()
