"""Replay a complete, price-optimal terminal repair on exact rational words."""
import argparse
from collections import Counter,defaultdict
from fractions import Fraction as Q
from functools import cache
import gzip
from hashlib import sha256
import json
from math import ceil,lcm
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from graph import Graph,ROOT,require,rational
from price import moment,add_profiles,pretty

PINS={'rail-base.json.gz':'d8f772b3b2c157da6756f29dd93170feda941a10f57af6e7043c3443ee9c6022',
      'rail-repaired.json.gz':'90440c9115da1b98242113832c296faf314caf0ab7e0743119275dbfc372c9d2',
      'LAYOUT.json.gz':'b0f3ebc5710e469f3e8fc5ce159cbba048b563944182b50993431ef94f4fedbf',
      'base-correction.json.gz':'2b1c8c9ab761aac65f7097b71893fef55f8c0fe090de8f9ea722346940c3e2f5',
      'repaired-correction.json.gz':'27a31dd792e482e48ef8b89e7fe2c76fea68031e76b5428c4640830cae7271d2'}

def read(name):
    b=(ROOT/'sources'/name).read_bytes()
    require(sha256(b).hexdigest()==PINS[name],name+' pin')
    return json.loads(gzip.decompress(b))

def transfer(g):
    n=len(g.initial)
    den={~i:1 for i in range(n)}
    size={~i:Q(1) for i in range(n)}
    for e in g.schedule:
        form=g.forms[e]
        den[e]=lcm(*(q.denominator*den[f] for f,q in form.items()))
        size[e]=sum(abs(q)*size[f] for f,q in form.items())
    grid=lcm(*den.values())
    bits=(2*grid*ceil(max(size.values()))+1).bit_length()
    bits=((bits+7)//8)*8
    values={~j:grid<<(j*bits) for j in range(n)}
    for e in g.schedule:
        form=g.forms[e]
        d=lcm(*(q.denominator for q in form.values()))
        z,rem=divmod(sum(q.numerator*(d//q.denominator)*values[f] for f,q in form.items()),d)
        require(rem==0,'exact public transfer grid')
        values[e]=z
    half=1<<(bits-1)
    mask=(1<<bits)-1
    center=half*((1<<(n*bits))-1)//mask
    rows=[]
    for i in range(n):
        z=values[g.first_output+i]+center
        row={}
        for j in range(n):
            x=(z&mask)-half
            if x:row[j]=Q(x,grid)
            z>>=bits
        require(z==0,'balanced digit range')
        rows.append(row)
    mains={j for row in rows if len(row)>1 for j in row}
    require(len(mains)==400 and all(rows[h]=={h:1} for h in set(range(n))-mains),'main and helper partition')
    return rows,mains,{'independent_source_columns':n,'decoded_terminal_rows':len(rows),'clearing_denominator':str(grid),'lane_bits':bits}

@cache
def span(basis):
    values={0}
    for x in basis:values|={j^x for j in values}
    require(len(values)==1<<len(basis),'independent frame')
    return frozenset(values)

def axpy(acc,scale,row):
    for j,y in row.items():
        x=acc.get(j,0)+scale*y
        if x:acc[j]=x
        else:acc.pop(j,None)

def rank(rows):
    pivots={}
    for row0 in rows:
        row=row0.copy()
        while row:
            k=min(row)
            if k not in pivots:
                z=Q(1,row[k]);pivots[k]={j:z*t for j,t in row.items()};break
            axpy(row,-row[k],pivots[k])
    return len(pivots)

def reduce_rows(matrix,rows,cols):
    return [{j:x for j,x in matrix[i].items()if j in cols}for i in rows]

def replay(word):
    n=word['public'];frames=word['frames'];owned=word['owned_fields']
    require(n==400 and len(word['initial'])==n,'rail domain')
    values=[{j:Q(1)}for j in range(n)]+[None]*owned
    sites=word['initial'].copy()+[None]*owned
    counts=Counter();paid=Counter();pairs=set();live=peak=0
    for op in word['program']:
        k,a=op[:2];counts[k]+=1
        if k=='INIT':
            require(a>=n and sites[a] is None,'reused live packet')
            sites[a]=op[2];values[a]={};live+=1;peak=max(live,peak)
        elif k=='CLEAR':
            require(a>=n and sites[a]==op[2],'retirement ownership')
            sites[a]=None;values[a]=None;live-=1
        elif k=='MOVE':
            _,a,u,v,charged=op
            require(sites[a]==u and type(charged) is bool and charged==(a>=n),'MOVE ownership and source')
            U,V=span(tuple(frames[u])),span(tuple(frames[v]))
            require(U<V or (charged and V<U),'strict nested rail move and downward ownership')
            paid[abs(len(frames[u])-len(frames[v]))]+=1
            pairs.add((u,v));sites[a]=v
        elif k=='ADD':
            _,a,b,x,site=op
            require(a!=b and sites[a]==sites[b]==site,'local ADD')
            axpy(values[a],rational(x),values[b].copy() if a==b else values[b])
        elif k=='SCALE':
            _,a,x,site=op
            require(sites[a]==site and rational(x)!=0,'local SCALE')
            values[a]={j:rational(x)*v for j,v in values[a].items()}
        else:raise ValueError(k)
    require(live==0 and all(x is None for x in sites[n:]),'all owned fields retired')
    return values[:n],sites[:n],paid,pairs,{'instructions':sum(counts.values()),'counts':dict(counts),'allocated_owned_labels':owned,'max_live_owned':peak}

def index_by(labels):
    out=defaultdict(set)
    for i,j in enumerate(labels):out[j].add(i)
    return out

def remap(g,public,mains,layout,word,sites):
    inv={k:j for j,k in enumerate(layout['source_labels'])}
    local={int(v):inv[int(k)] for k,v in word['source_role_map'].items()}
    require(set(local)==set(range(400)) and set(local.values())==mains,'absolute source labels')
    old={k:i for i,k in local.items()};E=[]
    for i in range(400):
        j=local[i]
        require(word['frames'][word['initial'][i]]==g.frames[g.initial[j]],'literal initial chart frame')
        require(word['frames'][sites[i]]==g.frames[g.final[j]],'literal final chart frame')
        E.append({old[k]:x for k,x in public[j].items()})
    require(rank(E)==400,'target invertibility')
    return E

def product(C,L):
    rows=[]
    for form in C:
        acc={}
        for j,x in form.items():axpy(acc,x,L[j])
        rows.append(acc)
    return rows

def block_repair(C,sites):
    groups=index_by(sites);matrix=[];packets=[];n=len(sites)
    for i,row in enumerate(C):
        require({j:q for j,q in row.items() if sites[i]==sites[j]}=={i:Q(1)},'identity within every terminal chart')
    for a,send in sorted(groups.items()):
        for b,recv in sorted(groups.items()):
            if a==b:continue
            block={i:{j:z for j,z in C[i].items() if j in send} for i in recv}
            active=sorted(i for i in recv if block[i]);
            if not active:continue
            u=block[active[0]];pivot=min(u);v={i:block[i].get(pivot,0)/u[pivot] for i in active}
            require(all(block[i]=={j:q*v[i] for j,q in u.items()} for i in active),'rank-one block factorization')
            packets.append((a,b,u,v));matrix.append([a,b,len(u),len(v)])
    require(len(packets)==192 and len({(a,b) for a,b,u,v in packets})==192,'terminal packets')
    return packets,matrix

def append_packets(word,packets):
    n=word['public'];ops=[];reg=n
    # All spoke-to-hub updates precede the reverse sweep.
    for a,b,u,v in sorted(packets,key=lambda item:item[0]==127):
        ops.append(['INIT',reg,a])
        ops.extend(['ADD',reg,j,str(x),a] for j,x in sorted(u.items()))
        ops.append(['MOVE',reg,a,b,True])
        ops.extend(['ADD',j,reg,str(x),b] for j,x in sorted(v.items()))
        ops.append(['CLEAR',reg,b])
    out=dict(word);out['program']=word['program']+ops
    return out,ops

def nilpotent(C,sites):
    off=[{j:q for j,q in row.items()if j!=i}for i,row in enumerate(C)]
    outward=[row if sites[i]!=127 else {} for i,row in enumerate(off)]
    inward=[row if sites[i]==127 else {} for i,row in enumerate(off)]
    require(not any(product(outward,inward)) and not any(product(inward,outward)),'opposite star sweeps annihilate')

def post_cuts(C,sites):
    groups=index_by(sites);all_ids=set(range(len(sites)))
    outgoing={a:rank(reduce_rows(C,all_ids-src,src)) for a,src in groups.items()}
    incoming={a:rank(reduce_rows(C,src,all_ids-src))for a,src in groups.items()}
    require(sum(outgoing.values())==192 and sum(incoming.values())==178,'terminal rank cuts')
    return {'outgoing_ranks':dict(sorted(Counter(outgoing.values()).items())),'incoming_ranks':dict(sorted(Counter(incoming.values()).items())), 'sum_outgoing':sum(outgoing.values()),'sum_incoming':sum(incoming.values())}

def birth_cuts(E,L,birth,sites):
    ends=index_by(sites);starts=index_by(birth);core=next(k for k,z in ends.items()if len(z)==200);zero=next(k for k,z in starts.items()if len(z)==200)
    floor=0;facet=[]
    for b,ix in ends.items():
        if b==core:continue
        forbidden=set().union(*(j for a,j in starts.items() if all(not(set(E[i])&j)for i in ix)))
        r=rank(reduce_rows(L,ix,forbidden));floor+=r;facet.append(r)
    le=rank(reduce_rows(E,ends[core],starts[zero]));ll=rank(reduce_rows(L,ends[core],starts[zero]));floor+=max(0,le-ll)
    require(floor==170 and le==104 and ll==30,'cocharted input mixing floor')
    return {'facet_forbidden_ranks':dict(sorted(Counter(facet).items())),'zero_to_hub_target_rank':le,'zero_to_hub_rail_rank':ll,'summed_required_received_packets':floor}

def analyze(name,g,full,mains,layout):
    word=read('rail-'+name+'.json.gz');L,sites,paid,prior,b0=replay(word);E=remap(g,full,mains,layout,word,sites)
    C=[{int(j):rational(x)for j,x in row.items()}for row in read(name+'-correction.json.gz')]
    require(len(C)==400 and product(C,L)==E,'exact all-column correction')
    packets,structure=block_repair(C,sites);nilpotent(C,sites);changed,ops=append_packets(word,packets)
    actual,loc,bill,charged,b1=replay(changed)
    require(actual==E and loc==sites and bill==paid+Counter({1:192}), 'explicit repaired program')
    p=packets[0];u=dict(p[2]);j=next(iter(u));u[j]=-u[j]
    mutant,_=append_packets(word,[(p[0],p[1],u,p[3]),*packets[1:]])
    require(replay(mutant)[0]!=E,'signed packet mutant')
    no_one,_=append_packets(word,packets[1:]);require(replay(no_one)[0]!=E,'missing packet mutant')
    cut=post_cuts(C,sites);birth=birth_cuts(E,L,word['initial'],sites)
    t=Q(199,200);tariff=moment(bill,t);budget=moment(add_profiles((1,g.fixed_root),(-1,g.fixed_paid)),t);lim=(budget[0]/g.calls,budget[1]/g.calls)
    native=moment(add_profiles((1,g.native),(-1,g.helpers)),t);deficit=(native[0]-lim[1],native[1]-lim[0]);unfixed=moment(paid,t)
    err=rank([{j:rr for j in e.keys()|q.keys()if(rr:=e.get(j,0)-q.get(j,0))}for e,q in zip(E,L)])
    needpairs={(a,b)for a,b,u,v in packets};before={'initial':word['initial'],'frames':word['frames'],'public':400,'owned_fields':changed['owned_fields'],'program':changed['program'],'source_role_map':word['source_role_map']}
    receipt={'source':b0,'complete':b1,'native_paid':dict(sorted(bill.items())),'correction_operations':dict(Counter(o[0]for o in ops)), 'opposite_star_products_have_rank_zero':True,'added_peak_owned':1,'rank_target_minus_rail':err,'correction_nonzero_entries':sum(map(len,C)),'packets':len(packets),'packet_grades':{'1':192},'previously_used_distinct_directed_pairs':len(needpairs&prior),'new_distinct_directed_pairs':len(needpairs-prior),'cut':cut,'free_birth_mixing':birth,'whole_caller':{'native_calls':g.calls,'old_per_call_deficit':pretty(deficit),'per_extra_copy_affordable_paid_moment_limit':pretty(lim),'repair_allowance_for_this_rail':pretty((lim[0]-unfixed[1],lim[1]-unfixed[0])),'new_paid_moment':pretty(tariff),'new_per_extra_copy_shortfall':pretty((tariff[0]-lim[1],tariff[1]-lim[0]))},'controls':['wrong signed coefficient changes the full endpoint','omitting one rank-one packet changes the full endpoint']}
    return receipt,before,needpairs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);group=ap.add_mutually_exclusive_group();group.add_argument('--rebuild-charts',action='store_true');args=ap.parse_args()
    args.out.mkdir(exist_ok=True,parents=True);g=Graph();layout=read('LAYOUT.json.gz');require(sha256(gzip.decompress((ROOT/'sources'/'LAYOUT.json.gz').read_bytes())).hexdigest()==g.receipt['layout_sha256'],'layout binds the application')
    full,mains,receipt=transfer(g);out={'status':'PASS_COMPLETE_EXACT_TIGHT_TERMINAL_STAR','source_transfer':receipt,'complete_kappa_claimed':False};previous=None
    for name in ('base','repaired'):
        record,word,pairs=analyze(name,g,full,mains,layout);out[name]=record
        if name=='base':
            raw=json.dumps(word,sort_keys=True,separators=(',',':')).encode();(args.out/'COMPLETE-WORD.json.gz').write_bytes(gzip.compress(raw,mtime=0));out['word_sha256_uncompressed']=sha256(raw).hexdigest();previous=pairs;frames=word['frames']
        else:require(pairs==previous,'shared terminal repair pair set')
    if args.rebuild_charts:
        from bind import bind
        receipts=bind(frames,previous)
    else:
        receipts=json.loads(gzip.decompress((ROOT/'output'/'SIGNED-RECIPES.json.gz').read_bytes()))
    needpairs={(a['from'],a['to'])for a in receipts};require(needpairs==previous and len(receipts)==192 and all(r['recipe']['rank']==1 for r in receipts),'all advertised signed recipes')
    canonical=json.dumps(receipts,separators=(',',':'),sort_keys=True).encode();out['signed_chart_recipes_sha256_uncompressed']=sha256(canonical).hexdigest()
    path=args.out/'RESULT.json';path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(out['status'],out['base']['whole_caller'])

if __name__=='__main__':main()
