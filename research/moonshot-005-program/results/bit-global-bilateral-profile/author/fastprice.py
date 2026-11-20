"""Price the same physical facet bijection by arrowhead elimination and a thin in-place update."""
import hashlib
import numpy as np


def need(ok,label):
    if not ok:raise ValueError(label)


def regularize(field,matrix):
    rows=field.pivots(matrix.T);cols=field.pivots(matrix)
    spare_rows=sorted(set(range(len(matrix)))-set(rows));spare_cols=sorted(set(range(len(matrix)))-set(cols))
    out=matrix.copy();out[spare_rows,spare_cols]^=1
    inverse,_=field.invert_and_price(out)
    return out,inverse,spare_rows,spare_cols


def compute(field,blocks,weight,Z,W,V,N):
    mm=field.mm;mul=field.product;R,C,X,Y=blocks;w=W.shape[1];v=V.shape[1]
    U0,inv_r,rp,cp=regularize(field,R);up=[mm(A,inv_r) for A in X];dn=[mm(inv_r,A) for A in Y]
    center=C.copy()
    for a,b in zip(up,Y):center^=mm(a,b)
    T0,inv_s,rc,cc=regularize(field,center)
    fee_basis=field.invert_and_price(mul[field.inv[weight],T0])[1]+7*field.invert_and_price(mul[field.inv[weight],U0])[1]
    fee_shears=sum(int(field.weights[A].sum()) for A in up+dn)
    all_rows=rc+[480*e+i for e in range(1,8)for i in rp];all_cols=cc+[480*e+i for e in range(1,8)for i in cp]
    small=np.hstack([V,N]);s=small.shape[1];extra=len(all_rows)
    Xinput=np.zeros((3840,s+extra),dtype=np.uint8);Xinput[:,:s]=small
    if extra:Xinput[all_rows,s+np.arange(extra)]=1
    split=Xinput.reshape(8,480,-1);b=split[0].copy()
    for e in range(7):b^=mm(up[e],split[e+1])
    y0=mm(inv_s,b);raw=[y0]+[mm(inv_r,split[e+1])^mm(dn[e],y0)for e in range(7)];columns=mul[weight,np.vstack(raw)]
    columns[:,:s]^=small
    K=np.zeros((s+extra,3840),dtype=np.uint8);K[np.arange(v),np.arange(v)]=1
    K[v+np.arange(s-v),v+w+np.arange(s-v)]=1
    if extra:K[s:,v:v+w]=W[all_cols]
    basis=columns[:,field.pivots(columns)];inds=field.pivots(basis.T);ib,_=field.invert_and_price(basis[inds]);coordinate=mm(ib,columns[inds]);need(np.array_equal(mm(basis,coordinate),columns),'thin correction basis')
    L=mm(coordinate,K);tr=mm(field.invert_and_price(mm(Z,small))[0],Z);zcols=field.pivots(Z);free=sorted(set(range(3840))-set(zcols))
    # D=[V, aW, N] has \ker Z as its large middle part, in canonical free-coordinate order.
    need(np.array_equal(W[free],np.eye(w,dtype=np.uint8)),'canonical kernel free coordinates')
    functional=np.zeros((len(L),3840),dtype=np.uint8);first=mul[field.inv[weight],L[:,v:v+w]];functional[:,free]=first
    functional^=mm(np.hstack([L[:,:v],L[:,v+w:]])^mm(first,small[free]),tr)
    need(np.array_equal(mm(functional,small),np.hstack([L[:,:v],L[:,v+w:]])) and np.array_equal(mul[weight,mm(functional,W)],L[:,v:v+w]),'full thin physical identity on both subspaces')
    # Conjugating the update I+basis*functional by one shear moves its full image into actual pivot coordinates.
    other=sorted(set(range(3840))-set(inds));normal=mm(basis,ib);fac=mm(basis[inds],functional);rest=normal[other];upper=fac[:,other]
    pivot=np.eye(len(inds),dtype=np.uint8)^fac[:,inds]^mm(upper,rest)
    _,fc=field.invert_and_price(pivot);thin=2*int(field.weights[rest].sum())+int(field.weights[upper].sum())+fc
    # This proves a native forward and equally priced inverse for H = (I + basis*functional)^(-1) * a(C+)^(-1).
    return {'native_rim_patch_rank':len(rp),'native_center_patch_rank':len(rc),'native_thin_rank':len(inds),
            'native_arrowhead_diagonal_ADD':fee_basis,'native_arrowhead_shear_ADD':fee_shears,'native_thin_update_ADD':thin,
            'native_forward_ADD':fee_basis+fee_shears+thin,'thin_basis_sha256':hashlib.sha256(basis.copy()).hexdigest(),'thin_rows_sha256':hashlib.sha256(functional).hexdigest()}
