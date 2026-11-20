"""Route the two target star channels on the pinned genuine owner atlas."""
import argparse
from collections import Counter, defaultdict, deque
import gzip
import hashlib
import json
from pathlib import Path

L='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
R='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
MARKED_TAILS=48


def require(ok,label):
    if not ok:raise ValueError(label)


def read(path,digest):
    raw=gzip.decompress(path.read_bytes())
    require(hashlib.sha256(raw).hexdigest()==digest,str(path))
    return raw


class Flow:
    """Integral shortest augmenting paths. Unit cost prices a changed K assignment."""
    def __init__(self):
        self.edges=defaultdict(list)

    def add(self,x,y,capacity,cost):
        f=[y,capacity,cost,None,capacity]
        r=[x,0,-cost,f,0]
        f[3]=r
        self.edges[x].append(f);self.edges[y].append(r)
        return f

    def run(self,source,sink):
        total=price=0
        while True:
            dist={source:0};undo={};q=deque([source]);waiting={source}
            while q:
                x=q.popleft();waiting.remove(x)
                for a in self.edges[x]:
                    y,cap,cost,_,_=a
                    if cap and dist[x]+cost<dist.get(y,10**9):
                        dist[y]=dist[x]+cost;undo[y]=(x,a)
                        if y not in waiting:q.append(y);waiting.add(y)
            if sink not in undo:return total,price
            chain=[];x=sink
            while x!=source:
                x,e=undo[x];chain.append(e)
            f=min(e[1] for e in chain)
            for e in chain:e[1]-=f;e[3][1]+=f
            total+=f;price+=f*dist[sink]


def route_choices(entries,roles,side,chunks):
    # entries gives input labels per (K,donor) and output labels per (K,terminal).
    left,right=entries
    ks=sorted({k for k,g in left}&{k for k,g in right})
    f=Flow();refs={}
    if side=='X':
        for j in roles:f.add('a',('role',j),chunks,0)
        for k in ks:f.add(('K',k),'z',len(right[k,80]),0)
    else:
        for k in ks:f.add('a',('K',k),len(left[k,10]),0)
        for i in roles:f.add(('role',i),'z',chunks,0)
    for k in ks:
        for u in roles:
            starts=left.get((k,u if side=='X' else 10),[])
            ends=right.get((k,80 if side=='X' else u),[])
            if not starts or not ends:continue
            cap=min(len(starts),len(ends));same=len(set(starts)&set(ends))
            a,b=(('role',u),('K',k)) if side=='X' else (('K',k),('role',u))
            refs[k,u]=[f.add(a,b,same,0),f.add(a,b,cap-same,1)]
    flow,price=f.run('a','z')
    if flow!=chunks*len(roles):return None,flow
    demand={(k,u):sum(e[4]-e[1] for e in rr) for (k,u),rr in refs.items()}
    for k in ks:
        for u in roles:demand.setdefault((k,u),0)
    used_in=set();used_out=set();assign=defaultdict(list)
    for direct in (True,False):
        for k in ks:
            for u in roles:
                count=demand[k,u]
                if not count:continue
                im=sorted(set(left[k,u if side=='X' else 10])-used_in)
                om=sorted(set(right[k,80 if side=='X' else u])-used_out)
                if direct:
                    selfset=sorted(set(im)&set(om))[:count]
                    pairings=zip(selfset,selfset)
                else:
                    require(min(len(im),len(om))>=count,'physical K residual packing')
                    pairings=zip(im[:count],om[:count])
                for x,y in pairings:
                    assign[u].append((k,x,y));used_in.add(x);used_out.add(y);demand[k,u]-=1
    require(not any(demand.values()) and set(assign)==set(roles),'complete roles')
    require(sum(x!=y for v in assign.values() for k,x,y in v)==price,'direct-retention optimum')
    return {u:sorted(v) for u,v in assign.items()},flow


def perm_swaps(arcs):
    """Complete a partial wire injection by closing its paths and replay actual swaps."""
    require(len(arcs)==len(set(arcs.values())),'distinct output destinations')
    p=arcs.copy(); starts=set(p)-set(p.values())
    for start in starts:
        x=start
        while x in p:x=p[x]
        p[x]=start
    needset=set(p)
    require(needset==set(p.values()),'completed square chart')
    active=sorted(needset);inv={v:k for k,v in p.items()}
    vals={u:u for u in active};where=vals.copy();word=[]
    for dst in active:
        incoming=inv[dst]
        if vals[dst]==incoming:continue
        loc=where[incoming];old=vals[dst];word.append([dst,loc])
        vals[loc],vals[dst]=vals[dst],vals[loc]
        where[incoming],where[old]=dst,loc
    require(vals==inv,'forward permutation labels')
    for dst,loc in reversed(word):vals[loc],vals[dst]=vals[dst],vals[loc]
    require(all(k==v for k,v in vals.items()),'inverse permutation labels')
    return word


def choose(rside,cside,rows,cols,right_axes):
    nfield=16*len(right_axes);chunks=nfield//8
    row,rflow=route_choices(rside,rows,'X',chunks)
    col,cflow=route_choices(cside,cols,'Y',chunks)
    if row is None or col is None:return None,{'row':rflow,'column':cflow}
    x_perm=defaultdict(dict);kx=defaultdict(dict);ky=defaultdict(dict);yf=defaultdict(dict)
    rowtap=[];coltap=[]
    # One bundle uses all eight genuine owner copies. The spinor index varies before
    # advancing the right-coordinate axis, so consecutive bundles cover all 16 spins.
    for ell,(j,i) in enumerate(zip(rows,cols),1):
        for bundle,(k,inp,out) in enumerate(row[j]):
            for copy in range(8):
                ordinal=8*bundle+copy
                s=ordinal%16;t=right_axes[ordinal//16]
                original=j*3840+64*ell+4*s+t
                src=8*inp+copy;dst=8*out+copy
                x_perm[j][original]=src;kx[k][src]=dst
                rowtap.append([dst,4*s+t])
        for bundle,(k,inp,out) in enumerate(col[i]):
            for copy in range(8):
                ordinal=8*bundle+copy
                s=ordinal%16;t=right_axes[ordinal//16]
                src=8*inp+copy;dst=8*out+copy
                final=(53280+480*i)*8+64*ell+4*s+t
                ky[k][src]=dst;yf[i][dst]=final
                coltap.append([4*s+t,src])
    pure={kind:{str(id):perm_swaps(p) for id,p in maps.items()} for kind,maps in
          [('source_X',x_perm),('K_X',kx),('K_Y',ky),('F_Y',yf)]}
    swaps={k:sum(len(v) for v in charts.values()) for k,charts in pure.items()}
    pure_add=18*sum(swaps.values())
    nt=16*len(right_axes)
    row_copy=6*(len(rowtap)+nt)
    col_copy=6*(len(coltap)+nt)
    result={'right_axes':list(right_axes),'star_edges_each':len(rows),'proper_field_rank_both_stars':2*nt,
            'original_X_routes':rflow,'line10_Y_routes':cflow,
            'row_changed_base_K_destinations':sum(u!=v for picks in row.values() for k,u,v in picks),
            'column_changed_base_K_destinations':sum(u!=v for picks in col.values() for k,u,v in picks),
            'field_swaps':swaps,'pure_forward_ADD':pure_add,'pure_inverse_ADD':pure_add,
            'row_capture_delivery_ADD':row_copy,'column_capture_delivery_ADD':col_copy,
            'total_ADD':2*pure_add+row_copy+col_copy,'INIT':12*nt,'dirty_CLEAR':12*nt,'extra_MOVE':0,
            'standalone_rank_I_plus_B':111*3840,'base_atlas_movement_retained':True,
            'no_claim_of_simultaneous_separated_full_base':True}
    word={'row_target':80,'column_source':10,'rank_one_bundle_order':'right coordinate, spinor, eight original route copies',
          'row_base_paths':dict(row),'column_base_paths':dict(col),'field_swap_words':pure,
          'F80_capture_owner_to_central_position':rowtap,'line10_central_position_to_Y_owner':coltap}
    return word,result


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();p=args.repo/'research/moonshot-005-program/results'
    layout=json.loads(read(p/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz',L))
    raw=read(p/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz',R)
    roots=layout['root_table'];adj=lambda i,j:sum(x*y for x,y in zip(roots[i],roots[j]))==0
    rows=[j for j in range(111) if adj(j,80)][:MARKED_TAILS]
    cols=[i for i in range(111) if adj(i,10)][:MARKED_TAILS]
    x_in=defaultdict(list);x_out=defaultdict(list);y_in=defaultdict(list);y_out=defaultdict(list)
    for line in raw.splitlines():
        ph,j,c,h,d,k,s,i=json.loads(line);owner=480*j+c+53280*(ph=='Y')
        if k is None:continue
        if ph=='X':
            if j in rows:x_in[k,j].append(owner)
            if i==80:x_out[k,80].append(owner)
        else:
            if s==10:y_in[k,10].append(owner)
            if j in cols:y_out[k,j].append(owner)
    xside=(x_in,x_out);yside=(y_in,y_out)
    reports={};args.out.mkdir(parents=True,exist_ok=True)
    for label,axes in [('cross',[0]),('half',[0,1]),('three_quarters',[0,1,2]),('full',[0,1,2,3])]:
        word,result=choose(xside,yside,rows,cols,axes)
        if word is not None:
            data=json.dumps(word,sort_keys=True,separators=(',',':')).encode()
            (args.out/(label+'-word.json.gz')).write_bytes(gzip.compress(data,mtime=0))
            result['word_payload']=hashlib.sha256(data).hexdigest()
        reports[label]=result
    require('word_payload' in reports['cross'],'both simultaneous channels')
    report={'layout_payload':L,'routes_payload':R,'field_degree':6,'physical_bank_per_role':3840,
            'selected_tail_labels':list(range(1,49)),'left_native_donors':rows,'right_native_receivers':cols,
            'atlas_rank_and_movement_invoice':'full bank-480 atlas repeated on all eight six-bit owner copies. No extra MOVE.',
            'results':reports,'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps(reports,sort_keys=True))


if __name__=='__main__':
    main()
