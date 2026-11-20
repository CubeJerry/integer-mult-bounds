#!/usr/bin/env python3
"""Independent full true left H factor, D120 readout and D3 obstruction."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
import gzip,importlib.util,json
from pathlib import Path
import numpy as np

def mod(path,name):
    s=importlib.util.spec_from_file_location(name,path);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);return v

def require(ok,msg):
    if not ok:raise ValueError(msg)

class NativeLeft:
    def __init__(self,root,review,field,base0,patched,payload):
        self.f=field;self.n=review.Native(root,field);self.c=review.Chart(self.n,263,3)
        self.flags=defaultdict(list);self.mid=defaultdict(list);self.routes={}
        routes=field.read_source(root/'research/moonshot-005-program/results','bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
        for a in map(json.loads,routes.splitlines()):
            ph,j,c,h,d,_,_,_=a;r=(ph=='Y')*53280+480*j+c
            self.routes[r]=a;self.mid[d].append(r)
            if h is not None:self.flags[h,d,ph].append(r)
        for bag in (self.mid,self.flags):
            for rows in bag.values():rows.sort()
        self.ports={h:[d for d in sorted(self.n.marked) if self.n.H[h]<=self.n.D[d]] for h in range(1120)}
        self.base=base0['components']['3']
        self.patched={(z['donor'],z['H']):np.asarray(z['matrix'],dtype=np.uint8) for z in patched['frames']}
        self.gauges={z['donor']:np.asarray(z['matrix'],dtype=np.uint8) for z in patched['gauges']}
        self.cache={};self.early_rank={}
        self.RSscale={int(j):m for j,m in payload.items()}
        self.V=field.power_matrix(range(1,10),9);self.der=np.zeros_like(self.V);self.der[:,1::2]=self.V[:,:-1:2]

    def frame(self,j,h,t,q,half):
        f=self.f
        if j in self.c.donors:
            F=(np.eye(48,dtype=np.uint8)[3*self.c.ix[j]:3*(self.c.ix[j]+1)] if h==263 else
               np.asarray(self.base['off_H'][str(self.c.point[j][h])],dtype=np.uint8))
            pair=np.kron(np.eye(2,dtype=np.uint8),F)
            if (j,h) in self.patched:
                T=self.patched[j,h]
            elif q==1:
                T=np.vstack([self.base['early'][str(j)][str(h)],
                             np.eye(6,dtype=np.uint8)[self.base['complementary_late_coordinate_rows'][str(j)][str(h)]]])
            else:T=np.eye(6,dtype=np.uint8)
            require(f.eliminate(T)[0]==6,'whole physical donor frame')
            return f.matmul(T,pair)
        waves=f.power_matrix([t],16)[0]
        B=np.kron(np.eye(6,dtype=np.uint8),waves.reshape(1,16))
        if q==3:
            derivative=np.zeros(16,dtype=np.uint8);derivative[1::2]=waves[:-1:2]
            extra=np.kron(np.eye(3,dtype=np.uint8),f.MUL[self.RSscale[j],derivative].reshape(1,16))
            B=np.vstack([B,np.hstack([extra,np.zeros((3,48),dtype=np.uint8)])])
        elif q==1 and h not in half:
            B=B[[3,4,5,0,1,2]]
        if j in self.gauges:B=f.matmul(B,self.gauges[j])
        return B

    def rows(self,j):
        if j in self.cache:return self.cache[j]
        n=self.n; out={};early=[]
        hs=n.hlist[j]
        half=set([h for h in hs if n.early[j,h]==15][:12])
        for t,h in enumerate(hs,1):
            who=sorted(n.H[h]&set(range(111)));c=len(who);q=n.early[j,h]//15
            s=sum(n.early[u,h] for u in who)//45
            B=self.frame(j,h,t,q,half)
            early.append(B[:3*q])
            if c==3:gX=gY=[u for u in who for _ in range(3)]
            elif c==2:
                big=max(who,key=lambda u:n.early[u,h]);small=next(u for u in who if u!=big)
                gX=[big]*6+[small]*3;gY=[small]*3+[None]*6
            else:gX=[j]*9;gY=[None]*9
            early_input=[]
            for ph,groups,count in [('X',gX,s),('Y',gY,2-s)]:
                for stripe in range(count):
                    feed=np.zeros((9,96),dtype=np.uint8)
                    selected=[u for u,g in enumerate(groups) if g==j]
                    if ph=='Y':offset=3
                    elif s==2:offset=3*stripe
                    else:offset=0
                    for idx,u in enumerate(selected):feed[u]=B[offset+idx]
                    val=self.f.matmul(self.V,feed)
                    if ph=='X':early_input.append(feed)
                    elif c in (1,2):
                        dr=self.der.copy()
                        if c==2:dr[:,6:]=0
                        val^=self.f.matmul(dr,early_input[stripe])
                    for p,d in enumerate(self.ports[h]):
                        rid=self.flags[h,d,ph][stripe]
                        require(rid not in out,'one physical H port value per genuine carrier')
                        out[rid]=val[p]
        E=np.vstack(early);r=self.f.eliminate(E)[0]
        require(E.shape==(96,96) and r==96,'full actual early source basis')
        self.cache[j]=out;self.early_rank[j]=r;return out

    def marked(self,i,j):
        ds=[d for d in sorted(self.n.marked) if j in self.n.D[d] and self.n.D[d]<=self.n.adj[i]]
        require(len(ds)==12,'actual 12 marked D ports of a proper edge')
        rows=self.rows(j);blocks={}
        for d in ds:
            keep=[r for r in self.mid[d] if r in rows]
            require(len(keep)==8,'eight complete H crossings into a marked D')
            blocks[d]=np.stack([rows[r] for r in keep])
        all_rows=np.vstack(list(blocks.values()))
        require(self.f.eliminate(all_rows)[0]==96,'actual full marked proper source edge')
        return ds,all_rows,blocks

def main():
    p=ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--words',type=Path,required=True)
    for t in ('packing-review','field-review','authority','source-compiler','source-receipt'):p.add_argument('--'+t,type=Path)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    base=a.repo/'research/moonshot-005-program/results'
    q=mod(a.packing_review or base/'bit-spread-overlap-source/review/check.py','review')
    f=mod(a.field_review or base/'bit-spread-h263-source/review/check.py','field')
    compiler=mod(a.source_compiler or base/'bit-spread-source-owner-compiler/author/compile_source.py','owner_compiler')
    raw=gzip.decompress(a.words.read_bytes());require(sha256(raw).hexdigest()=='f185c1d220f258b88159f50bcafe47c1b0fde53439320eb5d9313d06e74bc970','literal D120/source pin')
    word=json.loads(raw)
    raw_base=gzip.decompress((a.authority or base/'bit-spread-h263-source/author/output/COEFFICIENTS.json.gz').read_bytes())
    require(sha256(raw_base).hexdigest()=='66fe6820e16e2a1a221cc59656b6356087f92b685ff121ef174a67c7c4890a0e','prior special source')
    n=NativeLeft(a.repo,q,f,json.loads(raw_base),word,{82:3})
    V=np.asarray(word['V'],dtype=np.uint8);omega=np.asarray(word['omega'],dtype=np.uint8);M=np.asarray(word['D'],dtype=np.uint8)
    require(V.shape==(8,96) and f.eliminate(V)[0]==8 and omega.shape==(8,8) and f.eliminate(omega)[0]==8,'complete fixed common input/output labels')
    for G in n.gauges.values():require(G.shape==(96,96) and f.eliminate(G)[0]==96,'genuine full raw-coordinate preconditioner')
    d,i=word['d'],word['i']
    ids=n.mid[d];donors=sorted(n.n.D[d]&set(range(111)))
    recipients=[i for i in range(111) if n.n.D[d]<=n.n.adj[i]]
    new_rows={j:[u for u,r in enumerate(ids) if r in n.rows(j)] for j in donors}
    out_rows={i:[u for u,r in enumerate(ids) if n.routes[r][5] in n.n.hlist[i]] for i in recipients}
    m=sum(n.routes[r][0]=='X' for r in ids)
    require(M.shape==(36,36) and m==19 and np.all(M[:m,m:]==0) and f.eliminate(M[:m,:m])[0]==19 and
            f.eliminate(M[m:,m:])[0]==17,'legal two-wave pure D word')
    minor_counts=Counter()
    for l in recipients:
        for j in donors:
            sub=M[np.ix_(out_rows[l],new_rows[j])]
            require(sub.shape==(8,8) and f.eliminate(sub)[0]==8,'all actual native 8-by-8 D minors')
            minor_counts[l]+=1
    require(len(donors)==12 and len(recipients)==11 and sum(minor_counts.values())==132,'D120 native dimensions')
    for j in donors:
        ds,H,b=n.marked(i,j)
        for z in ds:
            Y=f.matmul(b[z],V.T)
            if z==d:
                D=M[np.ix_(out_rows[i],new_rows[j])]
                require(np.array_equal(f.matmul(D,Y),omega),'same exact captured D output on every donor\'s original input')
            else:require(not Y.any(),'every other marked D annihilates this true isolated original input')
    # Independently solve native H263 graphs after each complete retuning.
    native_h=0
    for i0 in n.c.receivers:
        if i0>=111:continue
        goal=np.zeros((96,6),dtype=np.uint8);goal[:6]=np.eye(6,dtype=np.uint8);L=None
        for j in n.c.donors:
            T=n.rows(j)
            chosen=[r for r in T if n.n.H[n.routes[r][3]]<=n.n.adj[i0] and n.n.D[n.routes[r][4]]<=n.n.adj[i0]]
            chosen.sort(key=lambda r:(n.routes[r][3]!=263,r))
            require(len(chosen)==96 and sum(n.routes[r][3]==263 for r in chosen)==6,'actual native H chart partition')
            A=np.stack([T[r] for r in chosen])
            if L is None:
                rank,L=f.eliminate(A,goal);require(rank==96,'full retuned H263 receiver source')
            require(np.array_equal(f.matmul(A,L),goal),'same original-coordinate H263 transfer after retuning')
        native_h+=1
    wrong={}
    d0=3
    rec0=[i for i in range(111) if n.n.D[d0]<=n.n.adj[i]]
    for j in (26,29):
        U=[]
        for i0 in rec0:
            ds,A,b=n.marked(i0,j)
            t=ds.index(d0);target=np.zeros((96,8),dtype=np.uint8);target[8*t:8*t+8]=np.eye(8,dtype=np.uint8)
            r,X=f.eliminate(A,target)
            require(r==96 and np.array_equal(f.matmul(A,X),target),'direct full D3 isolated source lift')
            U.append(X)
        wrong[j]=f.eliminate(np.hstack(U))[0]
    require(wrong=={26:94,29:96} and len(rec0)==12,'physical two-donor isolated-fibre obstruction')
    # Direct implementation with one six-bit cached late parity per true Y.
    _,early=compiler.compile_invertible(M[:m,:m]);_,late=compiler.compile_invertible(M[m:,m:])
    cross=8*int(compiler.WEIGHT[M[m:,:m]].sum());buffers=8*6*(36-m)
    invoice={'early_pure_ADD':8*early,'late_pure_ADD':8*late,'cached_cross_accumulation_ADD':cross,
             'late_injection_ADD':buffers,'INIT':buffers,'dirty_CLEAR':buffers,
             'forward_ADD':8*(early+late)+cross+buffers,'extra_MOVE':0}
    invoice['forward_and_pure_inverses_ADD']=invoice['forward_ADD']+invoice['early_pure_ADD']+invoice['late_pure_ADD']
    source_old=json.loads((a.source_receipt or base/'bit-spread-source-owner-compiler/author/output/RESULT.json').read_bytes())
    fwd_adjust=inverse_adjust=0
    for j in n.c.donors:
        early_rows=[];late_rows=[]
        for t,h in enumerate(n.n.hlist[j],1):
            quota=n.n.early[j,h]//15;B=n.frame(j,h,t,quota,set())
            early_rows.append(B[:3*quota])
            if quota==1:late_rows.append(B[3:])
        _,cost=compiler.compile_invertible(np.vstack(early_rows))
        writes=8*int(compiler.WEIGHT[np.vstack(late_rows)].sum())
        old=source_old['by_donor'][str(j)]['components']['3']
        difference=8*cost-old['all_eight_pairs_pure_ADD']
        inverse_adjust+=difference
        fwd_adjust+=difference+writes-old['cache_write_ADD']
    perm={u:u for u in range(3840)}
    for stripe in range(8):
        for idx in range(96):
            lane,scalar=divmod(idx,48)
            perm[96*stripe+idx]=16*scalar+8*lane+stripe
    swaps=len(compiler.permutation_swaps(perm))
    ordinary={j:8*compiler.compile_invertible(G)[1]+18*swaps for j,G in n.gauges.items()}
    source=source_old['combined_physical_source']
    fwd=source['source_forward_ADD']+fwd_adjust+sum(ordinary.values())
    inv=source['source_pure_inverse_ADD']+inverse_adjust+sum(ordinary.values())
    source_bill={'special_forward_change':fwd_adjust,'special_inverse_change':inverse_adjust,
                 'ordinary_gauge_ADDs_each_direction':ordinary,'true_label_swaps_per_gauge':swaps,
                 'forward_ADD':fwd,'pure_inverse_ADD':inv,'forward_and_pure_inverse_ADD':fwd+inv,
                 'INIT':source['source_INIT'],'dirty_CLEAR':source['source_dirty_CLEAR']}
    result={'word_sha256':sha256(raw).hexdigest(),'D120':{'native_donors':donors,'native_receivers':recipients,
            'target_receiver':i,'all_true_minors':sum(minor_counts.values()),'marked_cube_per_body':(12,8,96),
            'common_domain_dimension_per_body':8,'native_H263_graphs_retained':native_h,
            'replayed_early_basis_ranks':n.early_rank,'explicit_direct_D_invoice':invoice,'source_invoice':source_bill},
            'D3':{'receivers':rec0,'per_body_span_ranks':wrong,'eight_copy_span_ranks':{j:8*r for j,r in wrong.items()}},
            'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
