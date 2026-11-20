"""Construct both complete S028 perturbation stars on actual native owners."""
import argparse
from collections import Counter, defaultdict
import gzip,hashlib,json
from pathlib import Path

import numpy as np


PINS={'layout':('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'),
      'routes':('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036')}
BODY=8
NATIVE=111
BANK=3840
BASE=480
T8=[167,116,215,112,229,79,125,156]
W8=[219,191,130,199,25,119,93,183]
U8=[4,72,17,35,4,88,85,171]


def need(ok,why):
    if not ok:raise ValueError(why)


def residue(a,b):
    result=0
    for n in range(6):
        if b>>n&1:result^=a<<n
    while result>=64:
        result^=67<<(result.bit_length()-7)
    return result


G=np.array([[residue(i,j) for j in range(64)] for i in range(64)],dtype=np.uint8)
INV=[0]+[next(int(j) for j in range(1,64) if G[i,j]==1) for i in range(1,64)]
MUL_PRICE=[sum(int(G[i,1<<b]).bit_count() for b in range(6)) for i in range(64)]


def scale_price(z):
    rows=[sum(((int(G[z,1<<b])>>t)&1)<<b for b in range(6)) for t in range(6)]
    cost=0
    for b in range(6):
        if not rows[b]>>b&1:
            k=next(k for k in range(b+1,6) if rows[k]>>b&1)
            rows[b],rows[k]=rows[k],rows[b];cost+=3
        for k in range(6):
            if k!=b and rows[k]>>b&1:rows[k]^=rows[b];cost+=1
    need(rows==[1<<i for i in range(6)],'in-place basis multiplier')
    return cost


SCALE_PRICE=[0]+[scale_price(i) for i in range(1,64)]


def covector(d):
    node=1+d%63
    v=[1]
    for i in range(7):v.append(int(G[v[-1],node]))
    return v


def matrix32(tag):
    if tag=='I':return np.eye(32,dtype=np.uint8)
    base={'T':T8,'W':W8,'U':U8}[tag]
    a=np.array([[(r>>b)&1 for b in range(8)]for r in base],dtype=np.uint8)
    b=np.kron(a,np.eye(4,dtype=np.uint8))
    extra=np.zeros((4,4),dtype=np.uint8)
    if tag=='T':
        for i in range(3):extra[i,i+1]=1
    if tag=='W':extra[3,0]=1
    return b ^ np.kron(np.eye(8,dtype=np.uint8),extra)


def target_internal(side,tag):
    # In both the column map and the *dual* row map the populated half is the bottom half.
    b=matrix32(tag)
    if side=='row':b=b.T
    z=np.zeros((64,64),dtype=np.uint8);z[32:,:32]=b
    return z


def load(repo):
    base=repo/'research/moonshot-005-program/results';p={}
    for key,(path,sha) in PINS.items():
        b=gzip.decompress((base/path).read_bytes())
        need(hashlib.sha256(b).hexdigest()==sha,'source pin '+key);p[key]=b
    return json.loads(p['layout']),[json.loads(x) for x in p['routes'].splitlines()]


def reduce_rows(a,ids):
    """Record invertible field row operations carrying a gradient matrix to canonical rows."""
    a=np.array(a,dtype=np.uint8,copy=True);rank=0;ops=[]
    for c in range(a.shape[1]):
        nz=np.flatnonzero(a[rank:,c])
        if len(nz)==0:continue
        pivot=rank+int(nz[0])
        if pivot!=rank:
            a[[pivot,rank]]=a[[rank,pivot]]
            ops.append(['w',ids[pivot],ids[rank]])
        scale=INV[int(a[rank,c])]
        if scale!=1:
            a[rank]=G[scale,a[rank]];ops.append(['s',ids[rank],scale])
        for i in np.flatnonzero(a[:,c]):
            if i==rank:continue
            k=int(a[i,c]);a[i]^=G[k,a[rank]]
            ops.append(['a',ids[int(i)],ids[rank],k])
        rank+=1
        if rank==len(ids):break
    return a[:rank],ops


def inverse_ops(ops):
    return [['s',r[1],INV[r[2]]] if r[0]=='s' else r for r in reversed(ops)]


def permute(arcs):
    need(len(arcs)==len(set(arcs.values())),'partial distinct destinations')
    p=arcs.copy()
    for start in sorted(set(p)-set(p.values())):
        end=start
        while end in p:end=p[end]
        p[end]=start
    inverse={b:a for a,b in p.items()};values={a:a for a in p};where=values.copy();ops=[]
    for dest,src in sorted(inverse.items()):
        if values[dest]==src:continue
        peer=where[src];old=values[dest]
        values[peer],values[dest]=values[dest],values[peer]
        where[old],where[src]=peer,dest
        ops.append(['w',peer,dest])
    need(values==inverse,'actual endpoint permutation')
    return ops


def code_side(geo,routes,side):
    sr=80 if side=='row' else 10
    p='X' if side=='row' else 'Y';early=side=='row'
    roots=np.array(geo['root_table'],dtype=np.int64);adj=(roots@roots.T)==0
    targets=list(map(int,np.flatnonzero(adj[sr,:NATIVE])))
    full=targets[:59];tags=['I','T','W'] if early else ['I','U']
    specials=dict(zip(targets[59:],tags))
    need(set(specials)==(set([106,107,109]) if early else set([109,110])),'the five predecessor internal edges')
    lines=defaultdict(list);sites=defaultdict(dict);D=defaultdict(dict)
    tap=defaultdict(list);bridge=defaultdict(list)
    phase_offset=0 if early else 53280
    for ph,j,c,h,d,k,nline,terminal in routes:
        if ph!=p:continue
        fid=phase_offset+480*j+c
        u=h if early else k
        fielddest=j
        # For a Y route the true terminal is j. For X in reverse it is its original source j.
        if d is not None:
            D[d][fid]=u
            if (terminal if early else nline)==sr:tap[d].append(fid)
        if u is not None:
            sites[u][fid]=fielddest if (early or j in geo['A2'][u]) else None
            if d is not None:bridge[d,u].append(fid)
        lines[fielddest].append(fid)
    plane_full={u:sorted(set(geo['A2'][u])&set(full)) for u in sites}
    # Reverse row H outlets must be real Xs actually originating at a member of H.
    # Forward Y at K always has terminal in K unless specially released (the atlas has none).
    for u,v in sites.items():
        for j in v.values():need(j is None or j in geo['A2'][u],'true plane owner')
    ds_usable=sorted(d for d in tap if any(plane_full.get(u) for u in set(D[d].values()) if u is not None))
    arm={};emissions=[];middle={};chart_values=defaultdict(dict);copy_counts=Counter()
    for d in ds_usable:
        src=min(tap[d]);ends=[]
        for u in sorted({u for u in D[d].values() if u is not None and plane_full.get(u)}):
            dest=min(bridge[d,u]);ends.append(dest)
            chart_values[u][dest]=covector(d)
        if not ends:continue
        pivot=ends[0];ops=[]
        if src!=pivot:ops.append(['w',src,pivot])
        ops.extend(['a',dest,pivot,1] for dest in ends[1:])
        emissions.append([d,src,covector(d)])
        if ops:middle[str(d)]=ops
        copy_counts['D_to_plane']+=len(ends)
    # Pick an anchor with all eight directions for each partial internal generator.
    for j in specials:
        valid=[]
        for u,v in chart_values.items():
            if j in geo['A2'][u] and len({vector[1] for vector in v.values()})>=8:
                valid.append(u)
        need(valid,'full-rank partial target anchor')
        arm[j]=min(valid)
    plane_ops={};terminal_input=defaultdict(dict);special_owners={};basis_sizes=Counter()
    for u,active in sorted(chart_values.items()):
        ids=sorted(sites[u]);pos={f:t for t,f in enumerate(ids)};m=len(ids)
        incoming=np.zeros((m,8),dtype=np.uint8);outgoing=np.zeros_like(incoming)
        for f,vec in active.items():incoming[pos[f]]=vec
        basis,left=reduce_rows(incoming,ids);r=len(basis);basis_sizes[r]+=1
        need(r>0,'live destination chart')
        regular=plane_full[u];pivot_owners=None
        for i in regular:
            orig=sorted(f for f,j in sites[u].items() if j==i)
            need(len(orig)>=r,'full target actual outlets')
            take=orig[:r]
            for f,v in zip(take,basis):
                outgoing[pos[f]]=v;terminal_input[i][f]=v.tolist()
            if i==regular[0]:pivot_owners=take
        basis2,right=reduce_rows(outgoing,ids)
        need(np.array_equal(basis,basis2),'same proper row space for invertible crossing')
        ops=left+inverse_ops(right)
        for j,anchor in sorted(arm.items()):
            if anchor!=u:continue
            need(np.array_equal(basis,np.eye(8,dtype=np.uint8)),'eight true pivot forms at special anchor')
            dst=sorted(f for f,who in sites[u].items() if who==j)[:8]
            need(len(dst)==8,'complete partial-target outlet')
            target=target_internal(side,specials[j]);special_owners[j]=dst
            for dest,source in zip(*np.nonzero(target)):
                out=8*dst[int(dest)//8]+int(dest)%8
                inp=8*pivot_owners[int(source)//8]+int(source)%8
                ops.append(['c',out,inp])
        if ops:plane_ops[str(u)]=ops
    endpoint={}
    for ell,j in enumerate(full,1):
        owners=sorted(lines[j]);need(len(owners)==480,'genuine original role')
        grads=np.array([terminal_input[j].get(f,[0]*8) for f in owners],dtype=np.uint8)
        basis,ops=reduce_rows(grads,owners)
        need(np.array_equal(basis,np.eye(8,dtype=np.uint8)), f'full-rank target role {j}')
        target=owners[8*ell:8*ell+8]
        ops+=permute(dict(zip(owners[:8],target)))
        endpoint[str(j)]=ops
    for j,dst in special_owners.items():
        owners=sorted(lines[j])
        endpoint[str(j)]=permute(dict(zip(dst,owners[:8])))
    raw={'side':side,'phase':p,'center':sr,'D_emissions':emissions,'D':middle,'plane':plane_ops,'endpoint':endpoint,
         'regular':full,'internal':specials,'internal_anchor':arm}
    return raw,dict(basis_sizes),dict(copy_counts)


def operation_cost(op):
    if op[0]=='a':return BODY*MUL_PRICE[op[3]]
    if op[0]=='s':return BODY*SCALE_PRICE[op[2]]
    if op[0]=='w':return BODY*18
    need(op[0]=='c','individual cross-copy field addition')
    return 6


def invoice(word,bases,copies):
    by_stage={stage:sum(operation_cost(x) for moves in word[stage].values() for x in moves) for stage in ('endpoint','plane','D')}
    counts={stage:dict(Counter(op[0] for moves in word[stage].values() for op in moves)) for stage in by_stage}
    fan=sum(BODY*sum(MUL_PRICE[a] for a in vec) for d,tap,vec in word['D_emissions'])
    return {'phase':word['phase'],'emissions':len(word['D_emissions']),'D_to_plane':copies['D_to_plane'],
            'plane_span_histogram':bases,'internal_anchor':word['internal_anchor'],'OPCODE_counts_including_bundles':counts,
            'pure_by_stage_binary_ADD':by_stage,'pure_forward_ADD':sum(by_stage.values()),
            'pure_reverse_ADD':sum(by_stage.values()),'coded_capture_or_injection_ADD':fan,
            'snapshot_copy_or_delivery_ADD':384,'stationary_binary_fields':384,
            'total_ADD':2*sum(by_stage.values())+fan+384}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    geo,routes=load(args.repo);out=args.out;out.mkdir(parents=True,exist_ok=True)
    costs={};digest={}
    for tag in ('row','column'):
        word,hist,counts=code_side(geo,routes,tag)
        raw=json.dumps(word,separators=(',',':'),sort_keys=True).encode()
        digest[tag]=hashlib.sha256(raw).hexdigest();(out/(tag+'-word.json.gz')).write_bytes(gzip.compress(raw,mtime=0))
        costs[tag]=invoice(word,hist,counts)
    result={'route_pin_SHA256':PINS['routes'][1],'layout_pin_SHA256':PINS['layout'][1],'word_SHA256':digest,
            'arithmetic':'GF(64) polynomial x6+x+1','original_bank':BANK,'original_roles':NATIVE,
            'actual_X_fields':NATIVE*BANK,'actual_Y_fields':NATIVE*BANK,'regular_edges':118,'internal_edges':5,
            'nonzero_target_edges':123,'global_proper_rank':128,'standalone_rank_I_plus_delta':NATIVE*BANK,
            'word_costs':costs,'total_binary_ADD':sum(d['total_ADD'] for d in costs.values()),
            'INIT':768,'dirty_CLEAR':768,'extra_MOVE':0,
            'target':'Entire S028 difference Delta = B-S028 canonical foreign O tensor I. Entire B still needs canonical contribution.'}
    (out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
