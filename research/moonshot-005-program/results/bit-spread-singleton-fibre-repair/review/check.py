#!/usr/bin/env python3
"""Independent physical source-to-H replays of all literal singleton repairs."""
from argparse import ArgumentParser
from collections import Counter
from hashlib import sha256
import gzip
import importlib.util
import json
from pathlib import Path
import numpy as np

def load_module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def require(x,msg):
    if not x:
        raise ValueError(msg)

def double(A):
    return np.kron(np.eye(2,dtype=np.uint8),A)

def complete_half(f,E):
    """Select a coordinate basis of the quotient via greedy rank increments."""
    r=len(E)
    rows=[E]
    singles=[]
    for v in np.eye(2*r,dtype=np.uint8)[::-1]:
        if f.eliminate(np.vstack(rows+[v]))[0] > r+len(singles):
            rows.append(v)
            singles.append(v)
            if len(singles)==r:
                break
    # Descending greedy completion picks exactly the nonpivots of a
    # left-to-right echelon form of E. The wire order uses ascending labels.
    return np.vstack(singles[::-1])

class Transfer:
    def __init__(self,review,c,maps,seed,donor,singleton,S):
        self.j,self.p,self.k=donor,singleton,c.k
        self.n,self.f=c.native,c.native.f
        self.coeff={}
        self.early=[]
        self.frame_type={}
        self.maps=maps
        self.ordered_ports={}
        for h,F in sorted(maps.items()):
            quota=self.n.early[donor,h]//15
            native=sorted(self.n.H[h]&set(range(111)))
            ports=[d for d,D in enumerate(self.n.D) if self.n.H[h]<=D and (d in self.n.marked)==(c.k==3)]
            require(len(ports)==3*c.k,'native component port fan')
            self.ordered_ports[h]=ports
            self.frame_type[h]=(native,quota)
            original=double(F)
            if h==singleton:
                require(quota==3 and native==[donor],'all 3k singleton X slots belong to this native donor')
                self.coeff[h]=S
                self.early.append(S)
            elif quota==2:
                self.coeff[h]=original
                self.early.append(original)
            else:
                require(quota==1,'ordinary mixed donor phase')
                E=(np.eye(2*c.k,dtype=np.uint8)[:c.k] if h==c.h else
                   review.pseudo(f'early/{c.h}/{c.k}/{donor}/{h}/{seed}',c.k,2*c.k))
                late=complete_half(self.f,E)
                self.coeff[h]=self.f.matmul(np.vstack([E,late]),original)
                self.early.append(self.coeff[h][:c.k])
        B=np.vstack(self.early)
        require(B.shape==(32*c.k,32*c.k) and self.f.eliminate(B)[0]==32*c.k,
                'all original-X early basis columns including all 3k singleton inputs')

    def local(self,h,i):
        k,f=self.k,self.f
        xs=[z for z,d in enumerate(self.ordered_ports[h],1) if self.n.D[d]<=self.n.adj[i]]
        require(len(xs)==k,'actual visible output nodes')
        v=f.power_matrix(xs,3*k)
        der=np.zeros_like(v)
        der[:,1::2]=v[:,:-1:2]
        owners,quota=self.frame_type[h]
        if len(owners)==1:
            block=np.vstack([v,der])
        elif len(owners)==3:
            d=owners.index(self.j)
            block=double(v[:,d*k:(d+1)*k])
        elif quota==2:
            block=np.vstack([v[:,:2*k],der[:,:2*k]])
        else:
            zero=np.zeros((k,k),dtype=np.uint8)
            block=np.block([[v[:,2*k:],zero],[zero,v[:,:k]]])
        return f.matmul(block,self.coeff[h]),block

def check_case(review,n,pr,entry,maps=None,anchor=None):
    j,k,h,p=(entry[q] for q in ('donor','k','h','singleton'))
    S=np.asarray(entry['S'],dtype=np.uint8)
    require(S.shape==(3*k,32*k) and S.max()<64,'declared finite field literal singleton matrix')
    c=review.Chart(n,h,k)
    if maps is None:
        maps=c.single(pr)
    tran=Transfer(review,c,maps[j],pr['early'][str(j)],j,p,S)
    f=n.f
    if anchor is None:
        anchor=next(d for d in c.donors if d!=j)
    native=range(111)
    central=np.zeros((16*k,k),dtype=np.uint8)
    central[:k]=np.eye(k,dtype=np.uint8)
    physical_right=np.zeros((32*k,2*k),dtype=np.uint8)
    physical_right[:2*k]=np.eye(2*k,dtype=np.uint8)
    cut_ids=[]
    view_ids=[]
    fibre_span=[]
    hashed=sha256()
    mutant=None
    for i in sorted(n.adj[j]&set(native)):
        geometric=n.views[j,i]
        if p not in geometric:
            continue
        order=sorted(geometric,key=lambda a:(a!=h,a))
        phys={}
        raw={}
        for a in order:
            phys[a],block=tran.local(a,i)
            raw[a]=S[:2*k] if a==p else double(maps[j][a])
            if a==p:
                jet=block
        full=np.vstack([phys[a] for a in order])
        ordinary=np.vstack([raw[a] for a in order])
        require(f.eliminate(full)[0]==32*k,'entire exact 16-plane physical evaluation including true singleton derivative')
        require(f.eliminate(ordinary)[0]==32*k,'entire new ordinary source quotient')
        cut_ids.append(i)
        if h not in order:
            continue
        require(order[0]==h and i in c.receivers,'true receiver at both designated and singleton planes')
        pos=[t for t,d in enumerate(c.ports) if n.D[d]<=n.adj[i]]
        donor_index=c.ix[anchor]
        M=c.V[pos,donor_index*k:(donor_index+1)*k]
        rest=sorted(set(n.views[anchor,i])-{h})
        anchor_view=np.vstack([f.matmul(M,maps[anchor][h])]+[maps[anchor][a] for a in rest])
        rr,L=f.eliminate(anchor_view,central)
        require(rr==16*k,'unique input lift determined by unmodified donor')
        lifts=double(L)
        require(np.array_equal(f.matmul(full,lifts),physical_right),'common anchor lift solves the actual full H system')
        raw_single=f.matmul(S,lifts)
        require(not np.any(f.matmul(jet,raw_single)),'zero in physical singleton observations')
        if mutant is None:
            for t in range(2*k,3*k):
                if np.any(raw_single[t]):
                    distorted=S.copy()
                    distorted[t]=f.MUL[2,distorted[t]]
                    require(np.array_equal(distorted[:2*k],S[:2*k]),'negative test keeps all ordinary outputs')
                    require(np.any(f.matmul(jet,f.matmul(distorted,lifts))),'rank-preserving extra-row rescaling destroys common physical fibre')
                    mutant={'receiver':i,'scaled_extra_degree':t}
                    break
        fibre_span.append(L)
        hashed.update(lifts.tobytes())
        view_ids.append(i)
    require(mutant is not None,'observable genuine singleton degree at a designated fibre')
    rank=f.eliminate(np.hstack(fibre_span))[0]
    require(rank==15*k,'old designated fibres span the entire old off-singleton kernel')
    require(not f.matmul(maps[j][p],np.hstack(fibre_span)).any(),'old ordinary row annihilates old target fibres')
    return {'h':h,'j':j,'p':p,'k':k,'true_early_rank':32*k,'physical_cut_ids':cut_ids,
            'ordinary_cut_count':len(cut_ids),'replayed_designated_physical_receivers':view_ids,
            'old_fibre_span':rank,'exact_common_lift_sha256':hashed.hexdigest(),'extra_mutation':mutant}

def main():
    a=ArgumentParser()
    a.add_argument('--repo',type=Path,required=True)
    a.add_argument('--packing-review',type=Path)
    a.add_argument('--field-review',type=Path)
    a.add_argument('--overlap-parameters',type=Path)
    a.add_argument('--disjoint-parameters',type=Path)
    a.add_argument('--coefficients',type=Path)
    a.add_argument('--out',type=Path,required=True)
    a=a.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    review=load_module(a.packing_review or base/'bit-spread-overlap-source/review/check.py','packed_review')
    field=load_module(a.field_review or base/'bit-spread-h263-source/review/check.py','field_review')
    op=(a.overlap_parameters or base/'bit-spread-overlap-source/author/output/PARAMETERS.json').read_bytes()
    dp=(a.disjoint_parameters or base/'bit-spread-disjoint-h-sources/author/output/PARAMETERS.json').read_bytes()
    compressed=(a.coefficients or base/'bit-spread-singleton-fibre-repair/author/output/SINGLETON-COEFFICIENTS.json.gz').read_bytes()
    require(sha256(compressed).hexdigest()=='976d9558f33122618cc0001a8f92623893497f2e1d548000b2c8f801c2b32413',
            'archived literal matrix digest')
    ov,di=json.loads(op),json.loads(dp)
    all_params=di+ov['one_centre']
    params={(v['H'],v['k']):v for v in all_params}
    n=review.Native(a.repo,field)
    results=[]
    for entry in json.loads(gzip.decompress(compressed)):
        results.append(check_case(review,n,params[entry['h'],entry['k']],entry))
    rkeys={(v['h'],v['j'],v['p'],v['k']) for v in results}
    require(len(results)==len(rkeys)==16,'16 distinct component witnesses')
    families={}
    for name,cs in [('shared_24',ov['extended_ordinary_packing']),('disjoint_23',sorted({263}|{v['H'] for v in di}))]:
        expected={(h,j,p,k) for h in cs for j in n.H[h] for p in n.hlist[j] if n.early[j,p]==45 for k in (3,12)}
        require(expected<=rkeys,'every true singleton of every selected star repaired')
        count=sum(sum(n.H[h]<=n.adj[i] for i in range(111)) for h in cs)
        families[name]={'centres':len(cs),'native_chart_receivers':count,'affected_six_bit_component_placements':len(expected)}
    a.out.mkdir(parents=True,exist_ok=True)
    data={'compressed_coefficient_sha256':sha256(compressed).hexdigest(),'overlap_parameters_sha256':sha256(op).hexdigest(),
          'disjoint_parameters_sha256':sha256(dp).hexdigest(),'families':families,'physical_replays':results,
          'new_complete_kappa':False}
    (a.out/'RESULT.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps(families,sort_keys=True))

if __name__=='__main__':
    main()
