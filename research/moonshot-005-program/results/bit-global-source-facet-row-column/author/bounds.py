"""Rank the true target on the physically fixed columns and rows."""
import hashlib
import numpy as np


def target_kernel(field,state,columns,degrees,transpose):
    raw=state['raw'];terms=state['terms'];adj=state['adj'];w=columns.shape[1]
    source=np.zeros((8,3840,w),dtype=np.uint8)
    for k in range(8):source[k,raw[k]]=columns
    originals=[np.hstack([source[e,:,:degrees[j]] for e in range(8)]) for j in range(111)]
    full=np.hstack(list(source));offset=np.r_[0,np.cumsum([x.shape[1] for x in originals])];parts=[]
    for i in range(111):
        changed={}
        for j in adj[i]:
            key=(j,i) if transpose else (i,j)
            if key not in terms:continue
            dest,src,op=terms[key]
            if transpose:dest,src,op=src,dest,op.T
            add=np.zeros_like(originals[j]);add[dest*64:(dest+1)*64]=field.mm(op,originals[j][src*64:(src+1)*64]);changed[j]=add
        # Coordinate projection is injective on this whole facet image.
        keep=field.pivots(np.hstack([full]+list(changed.values())).T)
        rows=np.zeros((len(keep),offset[-1]),dtype=np.uint8)
        for j in [i]+adj[i]:
            rows[:,offset[j]:offset[j+1]]=originals[j][keep]
            if j in changed:rows[:,offset[j]:offset[j+1]]^=changed[j][keep]
        parts.append(rows)
    reduced=np.vstack(parts);rank=field.rank(reduced)
    return {'input_columns':int(offset[-1]),'compressed_output_rows':len(reduced),'target_fitting_rank':rank,
            'forced_kernel':int(offset[-1])-rank,'compressed_matrix_sha256':hashlib.sha256(reduced).hexdigest()}
