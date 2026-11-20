"""Measure a disjoint-role minor surviving arbitrary invertible local facet postmaps."""
import hashlib
import numpy as np


def check(previous, first, field, state, parameters, cache):
    actual=np.zeros((16*480,16*480),dtype=np.uint8)
    unused=np.zeros((0,0),dtype=np.uint8)
    for j in range(95,111):
        _,(rim,_,_)=previous.donor.verify_donor(j,field,first.coefficients,state,parameters,cache,unused)
        transfers=np.load(cache/f'L{j}.npy',mmap_mode='r',allow_pickle=False)
        for i,L in zip(state['adj'][j],transfers):
            if i>=16:continue
            index=state['adj'][i].index(j);V,S=state['VS'][i]
            start=state['B'][i][index]^field.mm(S,state['E'][i][index]);B=field.mm(V,start)^field.mm(L,rim)
            actual[i*480:(i+1)*480,(j-95)*480:(j-94)*480]=B
    rank=field.rank(actual);digest=hashlib.sha256(actual).hexdigest()
    if (rank,digest)!=(6670,'f9bd50e4b62983d22827d713641445a8cd60d1c5720ab14d926d0f50fc811859'):
        raise ValueError('actual disjoint native role minor')
    return {'receivers':list(range(16)),'donors':list(range(95,111)),'rim_minor_sha256':digest,'one_rim_copy_rank':rank,'full_return_lower_bound':7*rank}
