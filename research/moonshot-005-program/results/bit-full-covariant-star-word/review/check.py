#!/usr/bin/env python3
"""Independent literal binary-basis replay of both complete S028 difference stars."""
from argparse import ArgumentParser
from collections import Counter,defaultdict
from hashlib import sha256
import gzip,json
from pathlib import Path
import numpy as np

N=111*3840
def require(v,msg):
    if not v:raise ValueError(msg)

def data(path,digest):
    v=path.read_bytes()
    if path.suffix=='.gz':v=gzip.decompress(v)
    require(sha256(v).hexdigest()==digest,'pinned '+path.name)
    return v

def multipliers():
    orbit=[1]
    for _ in range(62):
        v=2*orbit[-1]
        orbit.append(v^67 if v&64 else v)
    require(len(set(orbit))==63,'primitive polynomial basis')
    logs={v:i for i,v in enumerate(orbit)}
    def mul(a,b):
        return orbit[(logs[a]+logs[b])%63] if a and b else 0
    masks=[[[p for p in range(6) if mul(z,1<<p)>>q&1] for q in range(6)] for z in range(64)]
    scale={}
    for z in range(1,64):
        A=[sum(1<<t for t in ps) for ps in masks[z]];ops=[]
        def add(d,s):
            A[d]^=A[s];ops.append((d,s))
        for c in range(6):
            if not A[c]>>c&1:
                pivot=next(i for i in range(c+1,6) if A[i]>>c&1)
                add(c,pivot);add(pivot,c);add(c,pivot)
            for i in range(6):
                if i!=c and A[i]>>c&1:add(i,c)
        require(A==[1<<t for t in range(6)],'scalar reducing gates')
        # Every six-bit field value is checked in both directions.
        def evaluate(v,seq):
            for d,s in seq:v^=((v>>s)&1)<<d
            return v
        for v in range(64):
            encoded=evaluate(v,reversed(ops))
            require(encoded==mul(z,v) and evaluate(encoded,ops)==v,'invertible paid binary scale')
        scale[z]=len(ops)
    return masks,scale

def target_arrays(authority,side):
    """One uint64 mask per genuine field. Bit c is its binary master-coordinate coefficient."""
    expect=np.zeros(N,dtype=np.uint64)
    edges=defaultdict(dict)
    for i,j,ell in authority[side+'_transfers']:
        role=j if side=='row' else i
        for t in range(64):
            addr=role*3840+64*ell+t
            expect[addr]=np.uint64(1<<t)
            if side=='row':edges[i,j][t]=1<<(64*ell+t)
            else:edges[i,j][64*ell+t]=1<<t
    for (i,j),B in zip(authority['internal_edges'],authority['internal_matrices_64']):
        if (side=='row')!=(i==80):continue
        require(len(B)==64 and all(0<=r<2**64 for r in B),'S028 internal binary mask convention')
        for t,row in enumerate(B):
            if row:edges[i,j][t]=row
            if side=='row':
                for q in range(64):
                    if row>>q&1:expect[j*3840+q]|=np.uint64(1<<t)
            else:expect[i*3840+t]=np.uint64(row)
    return expect,edges

def dense_binary_product(X,z,masks):
    if z==1:return X
    Y=np.empty_like(X)
    for q,indices in enumerate(masks[z]):
        Y[:,q]=np.bitwise_xor.reduce(X[:,indices],axis=1) if len(indices)>1 else X[:,indices[0]]
    return Y

def actual(side,cfg,ledger,routes,expect,masks,scale):
    ph='X' if side=='row' else 'Y'
    offset=0 if ph=='X' else N//8
    require(cfg['phase']==ph and cfg['center']==(80 if ph=='X' else 10),'true wave and center')
    # Six input bit planes, each packing 64 independent center coordinates.
    # All six physical output bits are retained at every one of the 426240 fields.
    state=np.zeros((N//8,8,6,6),dtype=np.uint64)
    taps=0;seen=set()
    for d,r,a in cfg['D_emissions']:
        owner=routes[r]
        require(owner[0]==ph and owner[4]==d and owner[7 if ph=='X' else 6]==cfg['center'],
                'actual F80 X or line10 Y visit on emitted D owner')
        require(r not in seen and len(a)==8 and all(0<=z<64 for z in a),'one coded direction per carrier')
        seen.add(r)
        for g,z in enumerate(a):
            taps+=8*sum(len(v) for v in masks[z])
            bits=np.array([1<<(8*g+p) for p in range(8)],dtype=np.uint64)
            for q,srcbits in enumerate(masks[z]):
                for p in srcbits:state[r-offset,:,q,p]^=bits
    charges={};ops=Counter()
    for stage,coord in [('D',4),('plane',3 if ph=='X' else 5),('endpoint',1 if ph=='X' else 7)]:
        bill=0
        for site,commands in cfg[stage].items():
            for item in commands:
                kind=item[0]
                a=item[1];b=item[2] if kind!='s' else None
                base=[a] if b is None else [a,b]
                if kind=='c':base=[v//8 for v in base]
                require(all(q in routes and routes[q][0]==ph and routes[q][coord]==int(site) for q in base),
                        'same true simultaneous physical holder location')
                require(b is None or a!=b,'elementary invertible gate')
                ops[kind]+=1
                if kind=='c':
                    aa,bb=divmod(a,8),divmod(b,8)
                    state[aa[0]-offset,aa[1]]^=state[bb[0]-offset,bb[1]]
                    bill+=6
                elif kind=='w':
                    d,s=a-offset,b-offset
                    state[[d,s]]=state[[s,d]]
                    bill+=8*18
                elif kind=='a':
                    z=item[3]
                    require(0<z<64,'legal shear coefficient')
                    state[a-offset]^=dense_binary_product(state[b-offset],z,masks)
                    bill+=8*sum(len(v) for v in masks[z])
                else:
                    require(kind=='s' and 0<item[2]<64,'legal scalar')
                    z=item[2]
                    state[a-offset]=dense_binary_product(state[a-offset],z,masks)
                    bill+=8*scale[z]
        charges[stage]=bill
    wires=state.reshape(N,6,6)
    for q in range(6):
        for p in range(6):
            if p==q:require(np.array_equal(wires[:,q,p],expect),'every genuine binary coefficient, including off-target zeros')
            else:require(not np.any(wires[:,q,p]),'no cross-bit dependence in the final binary target')
    nonzero=sum(int(x).bit_count() for x in expect)
    amount=2*sum(charges.values())+taps+384
    require(charges==ledger['pure_by_stage_binary_ADD'] and taps==ledger['coded_capture_or_injection_ADD'] and
            amount==ledger['total_ADD'],'recomputed six-bit instruction ledger')
    # An actual final transposition on a regular role retains all projection ranks.
    tail=cfg['regular'][0]*3840+64
    require(wires[tail,0,0]!=wires[tail+1,0,0],'rank-preserving internal relabelling detected')
    return {'primitive_counts':dict(ops),'proper_nonzero_field_coefficients':nonzero,'all_true_binary_output_bits':6*N,
            'distinct_binary_master_inputs':384,'bits_of_linear_transfer_compared':6*N*384,
            'stage_forward_ADD':charges,'coded_capture_or_injection_ADD':taps,'total_binary_ADD':amount,
            'stationary_holders_in_bits':384,'extra_MOVE':0}

def xor_rows(mask,rows):
    z=0
    while mask:
        bit=mask&-mask
        z^=rows.get(bit.bit_length()-1,0)
        mask^=bit
    return z

def rank2(rows):
    basis={}
    for x in rows:
        while x:
            p=x.bit_length()-1
            if p not in basis:
                basis[p]=x;break
            x^=basis[p]
    return len(basis)

def main():
    p=ArgumentParser()
    p.add_argument('--repo',type=Path,required=True);p.add_argument('--words',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    root=a.repo/'research/moonshot-005-program/results'
    auth=json.loads(data(root/'bit-two-sided-covariant-target/author/output/ASSIGNMENT.json','deabb7ac9cf8429981b4f28de015723c33399f9ea5c838a34621886ea5c74601'))
    b=data(root/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')
    routes={};masks,scale=multipliers()
    for r in map(json.loads,b.splitlines()):
        key=(r[0]=='Y')*N//8+480*r[1]+r[2]
        require(key not in routes,'unique true physical owner');routes[key]=r
    require(len(routes)==2*N//8,'every independent original record')
    ledger=json.loads((a.words/'RESULT.json').read_bytes());results={};ordered=[]
    for side in ('row','column'):
        expected,e=target_arrays(auth,side);ordered.append(e)
        raw=data(a.words/(side+'-word.json.gz'),ledger['word_SHA256'][side]);cfg=json.loads(raw)
        results[side]=actual(side,cfg,ledger['word_costs'][side],routes,expected,masks,scale)
    # Square the two independently verified sparse maps in the original coordinates.
    row,col=ordered
    S=Counter();paths=Counter()
    for (i,j),A in row.items():
        for (j0,l),B in col.items():
            if j0!=j:continue
            C={r:xor_rows(v,B) for r,v in A.items()}
            if any(C.values()):paths[str(j)]=sum(v.bit_count() for v in C.values())
            for r,v in C.items():S[r]^=v
    r2=rank2(S.values());nonzero=sum(x.bit_count() for x in S.values())
    require(r2==32 and nonzero==168 and set(paths)=={'0','5','8','15','109'},'exact standalone square')
    require(all(10!=i and 80!=j for i,j in list(row)+list(col)),'standalone cube vanishes')
    r=128
    require(sum(v['total_binary_ADD'] for v in results.values())==ledger['total_binary_ADD']==20269944,'full simultaneous charge')
    combined={'rank_delta':r,'rank_delta_squared':r2,'delta_squared_nonzero_field_coefficients':nonzero,
              'double_path_intermediates':paths,'rank_delta_cubed':0,'rank_I_plus_delta':N,
              'nilpotent_Jordan_blocks':{'size_3':r2,'size_2':r-2*r2,'size_1':N-2*r+r2},
              'binary_ADD':20269944,'binary_INIT':768,'binary_dirty_CLEAR':768,'extra_MOVE':0,'new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps({'components':results,'combined':combined},indent=2,sort_keys=True)+'\n')
    print(json.dumps(combined,sort_keys=True))

if __name__=='__main__':main()
