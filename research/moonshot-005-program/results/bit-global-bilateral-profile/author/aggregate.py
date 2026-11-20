"""Form one full physical weighted source profile following the matched rows/columns word."""
import numpy as np


BLOCKS=[(-1,-1),(0,0)]+[(0,e) for e in range(1,8)]+[(e,0) for e in range(1,8)]
INDEX={label:t for t,label in enumerate(BLOCKS)}


def prepare(previous,first,field,state,parameters,weights,late,output):
    output.mkdir(parents=True,exist_ok=True)
    totals={i:np.zeros((len(BLOCKS),480,480),dtype=np.uint8) for i in range(111)}
    for i,js in enumerate(state['adj']):
        for t in (0,1):totals[i][t]=field.product[weights[i],np.eye(480,dtype=np.uint8)]
        early=np.bitwise_xor.reduce(field.product[state['E'][i],weights[js,None,None]],axis=0)
        for pair,(dest,part) in state['updates'].get(i,{}).items():
            totals[i][INDEX[pair],dest]^=field.mm(part,early)
    minor=np.eye(12*480,dtype=np.uint8)
    for j,js in enumerate(state['adj']):
        _,(rim,central,cross)=previous.donor.verify_donor(j,field,first.coefficients,state,parameters,late,minor)
        releases=np.load(late/f'L{j}.npy',mmap_mode='r',allow_pickle=False)
        for i,native_L in zip(js,releases):
            L=field.product[weights[j],native_L]
            totals[i][0]^=field.mm(L,rim);totals[i][1]^=field.mm(L,central)
            for pair,(basis,source) in cross.items():
                totals[i][INDEX[pair]]^=field.mm(field.mm(L,basis),source)
    for i,M in totals.items():np.save(output/f'W{i:03}.npy',M)
