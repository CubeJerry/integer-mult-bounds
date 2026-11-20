"""Native inverse fibres and saturated target equations for actual middle cuts."""
import numpy as np
from body import inverse

class Slices:
    def __init__(self,a,source,word,assign):
        self.a=a;self.src=source;self.dmat={};self.assign=assign
        self.override={word['d']:np.array(word['D'],dtype=np.uint8)}
    def members(self,d):
        if d not in self.dmat:
            M,ids=self.a.middle_matrix(d);M=self.override.get(d,M)
            u=self.a
            cols={j:[n for n,t in enumerate(ids)if u.route[t][3]in u.ks[j]]for j in sorted(u.D[d]&set(range(111)))}
            rows={i:[n for n,t in enumerate(ids)if u.route[t][5]in u.ks[i]]for i in sorted(u.D[u.dual[d]]&set(range(111)))}
            self.dmat[d]=(M,cols,rows)
        return self.dmat[d]
    def left(self,i,j,keep):
        a=self.a
        ds=[d for d in range(len(a.D))if j in a.D[d] and i in a.D[a.dual[d]]]
        assert len(ds)==60;rows=self.src.left(j);slices={}
        for n,marked in [(96,True),(384,False)]:
            dd=[d for d in ds if (d in a.marked)==marked]
            if not set(dd)&keep:continue
            start=0 if marked else 96;rr=[]
            for d in dd:
                ids=a.middle[d,'X']+a.middle[d,'Y'];take=[u for u in ids if u in rows]
                assert len(take)==8
                rr.extend(rows[u][start:start+n]for u in take)
            inv=inverse(np.stack(rr))
            for k,d in enumerate(dd):
                if d in keep:slices[d]=inv[:,8*k:8*k+8].T.copy()
        return slices
    def receiver(self,i,keep):
        a=self.a;sp=set(self.src.donors);assert 0 in a.orth[i] and i!=80
        all_d={d for d in range(len(a.D))if i in a.D[a.dual[d]]and 0 in a.D[d]}
        assert set(keep)<={d for d in all_d if (a.D[d]&sp)=={0}or (i,d)==(5,120)}
        keep=set(keep)
        anch=self.left(i,0,keep);js=sorted(set.union(*(a.D[d]&set(range(111))for d in keep)))
        raw={}
        for j in js:
            shared={d for d in keep if j in a.D[d]}
            w=self.left(i,j,shared) if j else anch
            for d in shared:
                M,cols,rows=self.members(d);C0=M[np.ix_(rows[i],cols[0])];C=M[np.ix_(rows[i],cols[j])]
                target=a.ops.matmul(a.ops.matmul(w[d].T,inverse(C)),C0).T
                if j in sp:
                    assert np.array_equal(target,anch[d]),(i,d,j)
                    continue
                raw[d,j]=(anch[d],target)
        return keep,raw

def body_index(s,h):
    return h*48+s if s<48 else 96+h*192+s-48

def matched(assign,i,j,d,domain,image):
    if j!=10:return (j,domain.shape[1]),domain,image
    edge=next((v for v in assign['column_transfers']if v[:2]==[i,10]),None)
    if edge is None:raise ValueError(('target internal, skip',i))
    bank=edge[2];start=0 if domain.shape[1]==96 else 96
    U=np.zeros((8,480),dtype=np.uint8);Q=U.copy();U[:,start:start+domain.shape[1]]=domain;Q[:,start:start+domain.shape[1]]=image
    for h in range(2):
        for s in range(4):U[:,body_index(bank*4+s,h)]^=U[:,body_index(s,h)]
    return (j,480),U,Q


def row_reduce(A):
    from transfer import TABLE,INV
    mat=A.copy()
    k=0
    pivots=[]
    for c in range(mat.shape[1]):
        ind=np.flatnonzero(mat[k:,c])
        if not len(ind):continue
        p=k+int(ind[0]);mat[[p,k]]=mat[[k,p]]
        mat[k]=TABLE[INV[mat[k,c]],mat[k]]
        cc=mat[:,c].copy();cc[k]=0;mat^=TABLE[cc[:,None],mat[k,None,:]]
        pivots.append(c);k+=1
        if k==len(mat):break
    return mat[:k],pivots

def extend_rows(A):
    _,pi=row_reduce(A)
    assert len(pi)==len(A)
    extra=sorted(set(range(A.shape[1]))-set(pi))
    return np.vstack([A,np.eye(A.shape[1],dtype=np.uint8)[extra]]).T

def common_gauge(atlas,U,Q):
    U=np.vstack(U);Q=np.vstack(Q)
    _,use=row_reduce(U.T)
    A=extend_rows(U[use]);B=extend_rows(Q[use]);G=atlas.ops.matmul(B,inverse(A))
    assert np.array_equal(atlas.ops.matmul(U,G.T),Q)
    return G,len(use)
