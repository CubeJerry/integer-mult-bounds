#!/usr/bin/env python3
"""Independent all111 source/cut/singleton/owner and complete source-price audit.

Only the separately authored predecessor review's coefficient constructors
are reused. No new author checker/compiler or predecessor author compiler is
imported. New field operations, cut checks, inverse equations, holder mapping,
literal reduction stream and binary prices are reconstructed here.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import ctypes
import gzip
from hashlib import sha256, shake_256
import importlib.util
import json
from pathlib import Path
import subprocess
import numpy as np

PINS = {
 "geometry": ("bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz", "9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72"),
 "routes": ("bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz", "6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036"),
 "spread": ("bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz", "7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab"),
 "parameters": ("bit-coupled-native-forty-h-source/all-donors/output/PARAMETERS.json", "5a18a552cf8f67801311e80fdacce4ac8ddf6bc9819cf75b024ce314d2b4ee65"),
 "singletons": ("bit-coupled-native-forty-h-source/all-donors/output/SINGLETONS.json.gz", "317cdf804b53a2f56c4c0b32005250a9cc9043dbe67e0066e30181e84e893fbb"),
 "non_rs": ("bit-coupled-native-forty-h-source/all-donors/output/NON-RS-WITNESSES.json", "dd145caaee578d1a00dcf0e3ffd4091a1e5a3d57498ebd56da713eeb0ec2814c"),
 "cost": ("bit-coupled-native-forty-h-source/all-donors/output/COST.json", "e8086e9cd7ec05decc5509dcf035a69a7a3348d4a41092b489a2e67c23954450"),
 "coefficient_review": ("bit-spread-overlap-source/review/check.py", "ba369d2f9d27726607b62287707b29f9719971810a7e9893592d1035093e7e4f"),
 "field_review": ("bit-spread-h263-source/review/check.py", "db16cd8dcedfca40f6b9f29155de33d1211d8b77b0eff06c3072f6ffd50a3129"),
}

def need(ok, message):
    if not ok: raise ValueError(message)

def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

def polynomial_multiply(a, b):
    product = 0
    for power in range(6):
        if (a >> power) & 1: product ^= b << power
    for power in range(10, 5, -1):
        if (product >> power) & 1: product ^= 0x43 << (power-6)
    return product

def pseudo(tag, rows, columns):
    return np.frombuffer(shake_256(tag.encode("ascii")).digest(rows*columns), dtype=np.uint8).reshape(rows,columns) & 63

class Field:
    def __init__(self, library):
        self.lib = ctypes.CDLL(str(library.resolve()))
        self.lib.gf_product.argtypes = [ctypes.c_int,ctypes.c_int]
        self.lib.gf_product.restype = ctypes.c_int
        self.lib.reduce64.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int,ctypes.c_void_p,ctypes.c_int]
        self.lib.reduce64.restype = ctypes.c_int
        self.lib.matmul64.argtypes = [ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_int,ctypes.c_int,ctypes.c_int]
        self.lib.compile64.argtypes = [ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_void_p]
        self.lib.compile64.restype = ctypes.c_int
        self.product = np.array([[polynomial_multiply(a,b) for b in range(64)] for a in range(64)],dtype=np.uint8)
        need(all(self.lib.gf_product(a,b)==self.product[a,b] for a in range(64) for b in range(64)), "independent Python/C field agreement")
        self.inverse = np.zeros(64,dtype=np.uint8)
        self.weights = np.zeros(64,dtype=np.uint64)
        self.scales = np.zeros(64,dtype=np.uint64)
        for z in range(64):
            bits = [sum(((int(self.product[z,1<<b])>>t)&1)<<b for b in range(6)) for t in range(6)]
            self.weights[z] = sum(v.bit_count() for v in bits)
            if not z: continue
            inverses = [a for a in range(1,64) if self.product[z,a]==1]
            need(len(inverses)==1, "every nonzero scalar has exactly one inverse")
            self.inverse[z]=inverses[0]
            target=bits[:]; ops=[]
            def add(d,s): bits[d]^=bits[s]; ops.append((d,s))
            for c in range(6):
                p=next(i for i in range(c,6) if bits[i]>>c&1)
                if p!=c: add(p,c);add(c,p);add(p,c)
                for i in range(6):
                    if i!=c and bits[i]>>c&1: add(i,c)
            need(bits==[1<<i for i in range(6)], "binary scalar reduction")
            for d,s in reversed(ops): bits[d]^=bits[s]
            need(bits==target, "scalar word and inverse on all six basis columns")
            self.scales[z]=len(ops)

    def mm(self, left, right):
        a=np.ascontiguousarray(left,dtype=np.uint8);b=np.ascontiguousarray(right,dtype=np.uint8)
        need(a.shape[1]==b.shape[0], "field product dimensions")
        out=np.zeros((a.shape[0],b.shape[1]),dtype=np.uint8)
        self.lib.matmul64(a.ctypes.data,b.ctypes.data,out.ctypes.data,a.shape[0],a.shape[1],b.shape[1])
        return out

    def reduce(self, matrix, columns=None, full=False):
        a=np.ascontiguousarray(matrix,dtype=np.uint8).copy()
        columns=a.shape[1] if columns is None else columns
        pivots=np.zeros(min(a.shape[0],columns),dtype=np.int32)
        r=self.lib.reduce64(a.ctypes.data,a.shape[0],columns,a.shape[1],pivots.ctypes.data,int(full))
        return r,a,list(map(int,pivots[:r]))

    def rank(self, matrix): return self.reduce(matrix)[0]

    def null(self, matrix):
        r,a,pivots=self.reduce(matrix,full=True)
        free=[c for c in range(a.shape[1]) if c not in pivots]
        out=np.zeros((a.shape[1],len(free)),dtype=np.uint8)
        out[free]=np.eye(len(free),dtype=np.uint8)
        out[pivots]=a[:r,free]
        need(not np.any(self.mm(matrix,out)), "independent nullspace equations")
        return out

    def solve(self, matrix, right):
        n=matrix.shape[1]
        rank,a,pivots=self.reduce(np.hstack([matrix,right]),n,True)
        need(matrix.shape[0]==n and rank==n and pivots==list(range(n)), "square unique solution")
        answer=a[:,n:]
        need(np.array_equal(self.mm(matrix,answer),right), "independent solve residual")
        return answer

    def compile(self, matrix):
        a=np.ascontiguousarray(matrix,dtype=np.uint8).copy();n=len(a)
        out=np.empty(6*(n*n+2*n),dtype=np.uint8);price=ctypes.c_uint64()
        length=self.lib.compile64(a.ctypes.data,n,out.ctypes.data,len(out),self.weights.ctypes.data,self.scales.ctypes.data,ctypes.byref(price))
        need(length>=0 and np.array_equal(a,np.eye(n,dtype=np.uint8)), "literal early reduction reaches identity")
        return bytes(out[:length]),int(price.value)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    base=args.repo/'research/moonshot-005-program/results'
    payload={}
    for key,(path,pin) in PINS.items():
        raw=(base/path).read_bytes();raw=gzip.decompress(raw) if path.endswith('.gz') else raw
        need(sha256(raw).hexdigest()==pin, 'source pin '+key);payload[key]=raw
    cpp=Path(__file__).with_name('linear64.cpp');library=args.out/'linear64.so'
    subprocess.run(['c++','-O3','-std=c++17','-shared','-fPIC',str(cpp),'-o',str(library)],check=True)
    field=Field(library)
    oldfield=module(base/PINS['field_review'][0],'predecessor_field_review')
    oldreview=module(base/PINS['coefficient_review'][0],'predecessor_coefficient_review')
    need(np.array_equal(field.product,oldfield.MUL), 'coefficient constructor field table')
    native=oldreview.Native(args.repo,oldfield)
    geometry=json.loads(payload['geometry']);roots=geometry['root_table']
    H=list(map(frozenset,geometry['A2']));D=list(map(frozenset,geometry['D4']))
    perpendicular=[{j for j,y in enumerate(roots) if sum(a*b for a,b in zip(x,y))==0} for x in roots]
    need(all(set(native.adj[i])==perpendicular[i] for i in range(120)), 'reconstructed real orthogonality')
    originals=set(range(111));stars={j:[h for h,P in enumerate(H) if j in P] for j in originals}
    views={(j,i):[h for h in stars[j] if H[h]<=perpendicular[i]] for j in originals for i in perpendicular[j]&originals}
    need(len(views)==6470 and all(len(v)==16 for v in views.values()), 'all native sixteen-plane source cuts')
    spread=set(json.loads(payload['spread'])['selected_D'])
    wires=defaultdict(list);xcount=Counter();owners=set()
    for line in payload['routes'].splitlines():
        phase,role,coord,h,d,k,source,terminal=json.loads(line)
        if phase=='X':
            need(role==source and (role,coord) not in owners, 'unique genuine X route')
            owners.add((role,coord));xcount[h]+=1
        if h is not None and source is not None:
            wires[source,h,phase].extend((((phase=='Y')*111+role)*480+coord)*8+copy for copy in range(8))
    need(len(owners)==111*480, 'all actual original source owners')
    for values in wires.values():
        values.sort();need(len(values)==len(set(values)), 'holder multiplicity')
    singleton={j:next((h for h in stars[j] if len(wires[j,h,'X'])==360),None) for j in originals}
    need(sum(h is not None for h in singleton.values())==11, 'eleven genuine singleton sources')
    parameters=json.loads(payload['parameters']);repairs={}
    for row in json.loads(payload['singletons']):
        key=row['h'],row['donor'],row['k']
        need(key not in repairs, 'unique singleton certificate key')
        S=np.asarray(row['S'],dtype=np.uint8)
        need(S.shape==(3*row['k'],32*row['k']) and np.max(S)<64 and singleton[row['donor']]==row['singleton'], 'literal physical singleton dimensions')
        repairs[key]=S
    need(len(repairs)==22, 'all twenty-two singleton matrices')
    author=json.loads((base/'bit-coupled-native-forty-h-source/all-donors/output/RESULT.json').read_bytes())
    expected_cost=json.loads(payload['cost'])
    templates={};charts={};used=set();centres=[]
    for record in parameters['pairs']:
        h,q=record['centres'];block=set(H[h]|H[q])
        need(H[h]&H[q]=={record['shared_donor']} and len(block)==5 and not used&block, 'one shared donor in a disjoint actual pair component')
        need(singleton[record['shared_donor']] is None, 'shared donor has no singleton')
        used|=block;centres.extend((h,q))
        for k in (3,12):
            contexts=[oldreview.Chart(native,p,k) for p in (h,q)]
            maps=oldreview.paired(contexts,record[str(k)])
            for c in contexts: charts[c.h,k]=c
            for j,rows in maps.items():
                need((j,k) not in templates, 'source not privately duplicated')
                context=next(c for c in contexts if j in c.donors)
                templates[j,k]=(context,rows,record[str(k)]['early'][str(j)],{h,q})
    for text,options in parameters['singles'].items():
        h=int(text);need(not used&H[h] and H[h]<=originals, 'disjoint three-donor centre')
        used|=H[h];centres.append(h)
        for k in (3,12):
            context=oldreview.Chart(native,h,k);charts[h,k]=context
            for j,rows in context.single(options[str(k)]).items():
                need((j,k) not in templates, 'single source not duplicated')
                templates[j,k]=(context,rows,options[str(k)]['early'][str(j)],{h})
    need(len(parameters['pairs'])==21 and len(parameters['singles'])==2 and len(set(centres))==44 and used==originals and len(templates)==222, 'complete forty-four-centre allocation')
    for (j,k),(context,rows,seed,cs) in templates.items():
        need(set(rows)==set(stars[j]) and all(v.shape==(k,16*k) and np.max(v)<64 for v in rows.values()), 'all twenty-eight source quotients')
        digest=sha256(b''.join(rows[h].tobytes() for h in sorted(rows))).hexdigest()
        need(digest==author['source_coefficient_sha256'][f'{j}/{k}'], 'independent coefficient reconstruction equals the frozen new source')
    print('PASS_RECONSTRUCTED_ALL_222_COMPONENTS',flush=True)
    audit(args,base,field,native,H,D,perpendicular,views,spread,wires,xcount,singleton,templates,charts,centres,repairs,author,expected_cost,payload,cpp)

def audit(args,base,field,native,H,D,perpendicular,views,spread,wires,xcount,singleton,templates,charts,centres,repairs,author,expected_cost,payload,cpp):
    eye=lambda n:np.eye(n,dtype=np.uint8)
    def doubled(M): return np.kron(eye(2),M)
    def powers(nodes,width):
        out=np.ones((len(nodes),width),dtype=np.uint8)
        for c in range(1,width): out[:,c]=field.product[out[:,c-1],nodes]
        return out
    def selected_ports(h,k,i):
        ports=[d for d,Q in enumerate(D) if H[h]<=Q and ((d in spread)==(k==3))]
        need(len(ports)==3*k, 'actual split-component port count')
        nodes=[ordinal+1 for ordinal,d in enumerate(ports) if D[d]<=perpendicular[i]]
        need(len(nodes)==k, 'actual receiver sees one third of component ports')
        return nodes
    jets={}
    def jet(h,k,i):
        key=h,k,i
        if key not in jets:
            value=powers(selected_ports(h,k,i),3*k)
            deriv=np.zeros_like(value)
            for c in range(1,3*k,2): deriv[:,c]=value[:,c-1]
            jets[key]=np.vstack([value,deriv])
        return jets[key]

    early_matrices={};component_placements={};component_jobs={};all_y=set();true_frames=0
    zero_singleton_control=None
    for (j,k),(context,rows,seed,designated) in sorted(templates.items()):
        prefix=0 if k==3 else 3;offset=0 if k==3 else 768;n=16*k
        early=[];positions=[];jobs=[]
        for h,F in sorted(rows.items()):
            xs=wires[j,h,'X'];ys=wires[j,h,'Y'];quota=len(xs)//120
            need(len(xs)==120*quota and quota in (1,2,3) and len(ys)==120*max(2-quota,0), 'true source phase quota')
            if quota==3:
                need(h==singleton[j] and (context.h,j,k) in repairs, 'the actual singleton certificate is used')
                early.append(repairs[context.h,j,k])
                positions.extend((h,24*prefix+8*d) for d in range(3*k))
            elif quota==2:
                early.append(doubled(F))
                if xcount[h]==90:
                    positions.extend((h,16*prefix+16*d+8*b) for b in range(2) for d in range(k))
                else:
                    need(xcount[h]==45, 'genuine large early donor at two-donor H')
                    positions.extend((h,16*prefix+8*d) for d in range(2*k))
            else:
                E=eye(2*k)[:k] if h in designated else pseudo(f'early/{context.h}/{k}/{j}/{h}/{seed}',k,2*k)
                rank,reduced,pivots=field.reduce(E,full=True)
                need(rank==k, 'full row rank of physical early half frame')
                complement=[c for c in range(2*k) if c not in pivots]
                need(len(complement)==k and field.rank(np.vstack([E,eye(2*k)[complement]]))==2*k, 'complementary late frame is invertible')
                if h in designated: need(complement==list(range(k,2*k)), 'canonical central early/late halves')
                early.append(field.mm(E,doubled(F)))
                positions.extend((h,8*prefix+8*d) for d in range(k));true_frames+=1
                for d,c in enumerate(complement):
                    half,power=divmod(c,k)
                    jobs.append({'h':h,'coefficients':F[power].tolist(),
                                 'dest_and_first_X':[(ys[8*(prefix+d)+lane],j*3840+offset+8*half+lane) for lane in range(8)]})
        A=np.vstack(early)
        need(A.shape==(2*n,2*n) and len(positions)==2*n and field.rank(A)==2*n, 'all original early fields have an invertible actual map')
        if singleton[j] is not None and zero_singleton_control is None:
            p=singleton[j];start=sum(len(block) for h,block in zip(sorted(rows),early) if h<p)
            damaged=A.copy();damaged[start:start+3*k]=0
            need(field.rank(damaged)==2*n-3*k, 'zero singleton matrix loses exactly its genuine early directions')
            zero_singleton_control={'donor':j,'k':k,'before':2*n,'after':2*n-3*k}
        mapping={};placements=[]
        for lane in range(8):
            group=[j*3840+offset+16*c+8*b+lane for b in range(2) for c in range(n)]
            placements.append(group)
            for index,(h,pos) in enumerate(positions):
                destination=wires[j,h,'X'][pos+lane]
                need(destination not in mapping, 'one early scalar per genuine holder')
                mapping[destination]=group[index]
        destinations=[dest for job in jobs for dest,first in job['dest_and_first_X']]
        need(len(destinations)==len(set(destinations)) and not all_y.intersection(destinations), 'every genuine late line visit used once')
        all_y.update(destinations)
        early_matrices[j,k]=A;component_placements[j,k]=(mapping,placements)
        component_jobs[j,k]=jobs
    need(len(all_y)==321000 and true_frames==2*2675, 'all actual late source slots and half-frames')
    print('PASS_ALL_EARLY_BASES_AND_PHYSICAL_HOLDERS',flush=True)

    # Every receiver cut is checked directly from this same source. At the
    # singleton use its actual value/derivative projection, not a free 3k view.
    ordinary_counts=Counter();physical_singletons=Counter();canonical_singletons=Counter();rank_cache={}
    non_rs={r['donor']:r for r in json.loads(payload['non_rs'])};non_rs_counts=Counter()
    need(set(non_rs)==set(range(111)), 'one inequivalence witness per actual donor')
    for (j,k),(context,rows,seed,designated) in sorted(templates.items()):
        n=16*k;p=singleton[j]
        if k==3:
            w=non_rs[j];hs=w['planes']
            need(len(hs)==len(set(hs))==16 and set(hs)<=set(rows) and p not in hs, 'sixteen distinct ordinary source observations')
            rank=field.rank(np.vstack([rows[h] for h in hs]))
            need(rank==w['marked_scalar_rank'] and rank in (44,45,46,47), 'independent non-RS deficiency')
            non_rs_counts[rank]+=1
        for (donor,i),hs in views.items():
            if donor!=j: continue
            if p not in hs:
                stack=np.vstack([rows[h] for h in hs]);key=sha256(stack.tobytes()).digest()
                if key not in rank_cache: rank_cache[key]=field.rank(stack)
                need(rank_cache[key]==n, 'complete ordinary original-coordinate receiver cut')
                ordinary_counts[k]+=1
            else:
                off=np.vstack([rows[h] for h in hs if h!=p]);K=field.null(off)
                need(K.shape==(n,k), 'other fifteen ordinary source quotients have the exact residual width')
                S=repairs[context.h,j,k];reduced=np.hstack([field.mm(S[:,:n],K),field.mm(S[:,n:],K)])
                actual=field.mm(jet(p,k,i),reduced)
                need(field.rank(actual)==2*k, 'true singleton value-and-derivative receiver cut is injective')
                need(field.rank(reduced[:2*k])==2*k, 'canonical ordinary readout remains injective too')
                physical_singletons[k]+=1;canonical_singletons[k]+=1
    need(ordinary_counts=={3:6110,12:6110} and physical_singletons=={3:360,12:360}, 'all 6470 cuts in both components')
    print('PASS_ALL_6470_PHYSICAL_SOURCE_CUTS',dict(non_rs_counts),flush=True)

    inverse_counts=Counter();affected_singletons=Counter();fibre_hashes={};gauge_control=None
    for h in sorted(centres):
        audience=[i for i in range(111) if H[h]<=perpendicular[i]]
        for k in (3,12):
            n=16*k;donors=sorted(H[h]);context=charts[h,k];digest=sha256()
            for i in audience:
                V=powers(selected_ports(h,k,i),3*k)
                j0=donors[0];rows0=templates[j0,k][1]
                off0=[p for p in views[j0,i] if p!=h]
                stack=np.vstack([field.mm(V[:,:k],rows0[h])]+[rows0[p] for p in off0])
                rhs=np.zeros((n,k),dtype=np.uint8);rhs[:k]=eye(k)
                lift=field.solve(stack,rhs);digest.update(lift.tobytes())
                for ordinal,j in enumerate(donors):
                    ctx,rows,seed,ds=templates[j,k]
                    middle=field.mm(V[:,ordinal*k:(ordinal+1)*k],rows[h])
                    need(np.array_equal(field.mm(middle,lift),eye(k)), 'same canonical H readout on every donor lift')
                    for p in views[j,i]:
                        if p==h: continue
                        if p==singleton[j]:
                            S=repairs[ctx.h,j,k]
                            residual=np.hstack([field.mm(S[:,:n],lift),field.mm(S[:,n:],lift)])
                            need(not np.any(field.mm(jet(p,k,i),residual)), 'actual repaired singleton vanishes on the prescribed doubled fibre')
                            affected_singletons[j,k]+=1
                        else:
                            need(not np.any(field.mm(rows[p],lift)), 'every physical ordinary off-centre quotient vanishes')
                    if gauge_control is None and ordinal==1:
                        damaged=field.product[2,middle]
                        need(not np.array_equal(field.mm(damaged,lift),eye(k)) and field.rank(damaged)==k, 'invertible but unequal central relabel breaks the fixed common inverse')
                        gauge_control={'H':h,'receiver':i,'donor':j,'k':k}
                inverse_counts[k]+=1
            fibre_hashes[f'{h}/{k}']=digest.hexdigest()
    need(inverse_counts=={3:1474,12:1474}, 'all 1474 native designated inverse graphs in both components')
    need(len(affected_singletons)==22 and all(affected_singletons[r['donor'],r['k']]==sum(r['affected_designated_native_views'].values()) for r in author['singleton_replacements']), 'all actual affected singleton fibres')
    print('PASS_ALL_1474_COMMON_PHYSICAL_H_FIBRES',flush=True)

    # Reproduce every field primitive stream and independently assign all
    # physical holders. No author source compiler is invoked.
    all_costs=Counter();per_donor={};word_hashes={};late_control=None
    for j in range(111):
        costs=Counter();mapping={};records={};hashes={}
        for k in (3,12):
            A=early_matrices[j,k];stream,price=field.compile(A)
            hashes[str(k)]=sha256(stream).hexdigest()
            need(hashes[str(k)]==expected_cost['all_word_hashes'][str(j)][str(k)], 'exact independent field reduction stream hash')
            assignment,placements=component_placements[j,k]
            need(not set(mapping)&set(assignment), 'components use disjoint real early owners')
            mapping.update(assignment);jobs=component_jobs[j,k]
            late=[dest for job in jobs for dest,first in job['dest_and_first_X']]
            for job in jobs:
                need(any(job['coefficients']), 'every stored late parity is genuinely input-dependent')
                if late_control is None:
                    c=next(q for q,v in enumerate(job['coefficients']) if v)
                    late_control={'donor':j,'k':k,'H':job['h'],'original_power':c,'nonzero_coefficient':job['coefficients'][c]}
            costs['basis_ADD']+=8*price
            costs['write_ADD']+=8*sum(int(field.weights[job['coefficients']].sum()) for job in jobs)
            costs['read_ADD']+=6*len(late);costs['INIT']+=6*len(late);costs['dirty_CLEAR']+=6*len(late)
            records[f'{j}-{k}']={'reduce_file':f'REDUCE-{j}-{k}.bin.gz','original_field_placements':placements,'before_departure_late_parities':jobs}
        original=set(range(3840*j,3840*(j+1)))
        need(set(mapping)==set(mapping.values())==original, 'all 3840 original X fields form one physical permutation')
        seen=set();swaps=[]
        for first in sorted(mapping):
            if first in seen: continue
            cycle=[];at=first
            while at not in seen:
                seen.add(at);cycle.append(at);at=mapping[at]
            need(at==first, 'physical holder map consists of cycles')
            swaps.extend(zip(cycle,cycle[1:]))
        moved={u:u for u in original}
        for a,b in swaps: moved[a],moved[b]=moved[b],moved[a]
        need(moved==mapping, 'actual XOR-swap owner permutation')
        records[f'{j}-swaps']=swaps
        hashes['holder']=sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        need(hashes['holder']==expected_cost['all_word_hashes'][str(j)]['holder'], 'complete independently reconstructed holder dictionary')
        costs['permutation_ADD']=18*len(swaps)
        costs['inverse_ADD']=costs['basis_ADD']+costs['permutation_ADD']
        costs['forward_ADD']=costs['inverse_ADD']+costs['write_ADD']+costs['read_ADD']
        costs['total_ADD']=costs['forward_ADD']+costs['inverse_ADD']
        need(dict(costs)==expected_cost['special_donor_costs'][str(j)], 'every donor source cost including reserved inverse')
        per_donor[str(j)]=dict(costs);all_costs.update(costs);word_hashes[str(j)]=hashes
    need(dict(all_costs)==expected_cost['special'] and all_costs['INIT']==6*len(all_y)==1926000, 'complete all111 source bill')
    need(all_costs['forward_ADD']==2490116744 and all_costs['inverse_ADD']==2125715376 and all_costs['total_ADD']==4615832120, 'published complete source arithmetic totals')
    result={'status':'PASS_INDEPENDENT_ALL_111_CHANGED_SOURCES_AND_44_CENTRES',
        'new_author_python_imported':False,'source_pins_decompressed':{v[0]:v[1] for v in PINS.values()},
        'review_linear_cpp_sha256':sha256(cpp.read_bytes()).hexdigest(),
        'actual_native_source_banks':111,'early_component_bases':222,'native_source_H_cuts_each_component':6470,
        'ordinary_cut_counts':dict(ordinary_counts),'actual_singleton_cut_counts':dict(physical_singletons),
        'literal_singleton_matrices':22,'common_H_inverse_graphs_each_component':1474,
        'native_centres':sorted(centres),'donor_H_inverse_graphs':4422,
        'non_RS_marked_rank_counts':dict(non_rs_counts),'source_stars_inequivalent_under_bijective_gauges':111,
        'actual_X_field_owners':111*3840,'actual_Y_late_taps':len(all_y),
        'independently_matched_reduction_stream_hashes':222,'independently_matched_holder_dictionary_hashes':111,
        'complete_source_costs':dict(all_costs),'per_donor_costs':per_donor,'word_hashes':word_hashes,
        'common_fibre_hashes':fibre_hashes,
        'controls':{'zero_singleton_loses_early_rank':zero_singleton_control,'rank_preserving_donor_relabel_breaks_common_lift':gauge_control,'omitted_late_parity_changes_declared_source':late_control},
        'scope':'Canonical identity inverse graphs on the listed H interfaces, all physical source cuts and complete source price; no common D/K/F continuation or S028 perturbed target.',
        'new_complete_kappa':False}
    (args.out/'RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(result['status'],dict(all_costs),flush=True)

if __name__=='__main__': main()

