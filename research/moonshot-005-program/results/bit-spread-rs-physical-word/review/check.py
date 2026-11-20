"""Independent actual-owner, phase and RS-rank audit for H, source and terminal words."""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

PINS={'layout':('bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz','9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'),
      'routes':('bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz','6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'),
      'spread':('bit-orthogonal-spread-port-allocation/author/output/WITNESS.json.gz','7fff55e31738681191562949439537ea240557370895488934187455cd29d8ab')}
HPIN='bda9d599f8c17fd04993a96994fca0d6c8e20ea9951fd55c21e6431b82f3cd84'
KPIN={'SPREAD':'513cdf43f2d7e15d6c753e48fd592b95c56e178b7b1819b646ab7acd6f405af0',
      'MIXED':'8b2428093a2c432ebcc2770679574213c1ae45c57baa57900fd92d7eaf2b9f4a'}


def need(x,k):
    if not x:raise ValueError(k)


def read(p,d):
    b=gzip.decompress(p.read_bytes())
    need(hashlib.sha256(b).hexdigest()==d,p)
    return b


def mult(a,b):
    value=0
    for t in range(6):
        if (b>>t)&1:
            value ^= a<<t
    # Binary polynomial division by z^6+z+1.
    while value.bit_length()>6:
        value ^= 67<<(value.bit_length()-7)
    return value


G=np.array([[mult(a,b) for b in range(64)] for a in range(64)],dtype=np.uint8)
INV=[0]+[next(b for b in range(1,64) if G[a,b]==1) for a in range(1,64)]
BINCOST=np.array([sum(int(G[a,1<<b]).bit_count() for b in range(6)) for a in range(64)])
POW=np.ones((64,46),dtype=np.uint8)
for deg in range(1,46):
    POW[:,deg]=G[np.arange(64),POW[:,deg-1]]


def _rank(a):
    z=np.array(a,dtype=np.uint8,copy=True);r=0
    for c in range(z.shape[1]):
        if r==len(z):break
        nz=np.flatnonzero(z[r:,c])
        if len(nz)==0:continue
        k=r+nz[0]
        z[[r,k]]=z[[k,r]]
        w=G[INV[z[r,c]],z[r]]
        z[r+1:] ^= G[z[r+1:,c,None],w[None,:]]
        r+=1
    return r


def binary(a):
    rows=[]
    for fieldrow in a:
        bits=[0]*6
        for s,z in enumerate(fieldrow):
            for b in range(6):
                v=int(G[z,1<<b])
                for t in range(6):
                    if (v>>t)&1:
                        bits[t]|=1<<(s*6+b)
        rows.extend(bits)
    return rows


@lru_cache(None)
def rsword(desc, transpose):
    rows=np.array([coef(*d) for d in desc])
    if transpose:rows=rows.T
    need(_rank(rows)==16,'early/terminal pure rank')
    original=binary(rows);a=original[:];inverse=[]
    for c in range(len(a)):
        if not ((a[c]>>c)&1):
            r=next(y for y in range(c+1,len(a)) if (a[y]>>c)&1)
            a[c],a[r]=a[r],a[c]
            inverse.extend(((c,r),(r,c),(c,r)))
        for i in range(len(a)):
            if i!=c and (a[i]>>c)&1:
                a[i]^=a[c];inverse.append((i,c))
    eye=[1<<t for t in range(len(a))]
    need(a==eye,'RS basis elimination')
    for i,j in reversed(inverse):a[i]^=a[j]
    need(a==original,'RS pure forward')
    for i,j in inverse:a[i]^=a[j]
    need(a==eye,'RS pure inverse')
    return len(inverse)


@lru_cache(None)
def coef(node,deriv,scale):
    return tuple(int(G[scale,POW[node,t-1]]) if t%2 else 0 for t in range(16)) if deriv else tuple(POW[node,:16])


def permcost(source_at_out):
    vals=list(range(len(source_at_out)));where=vals.copy();swaps=0
    need(sorted(source_at_out)==vals,'actual-owner bijection')
    for d,s in enumerate(source_at_out):
        if vals[d]!=s:
            other=where[s];old=vals[d]
            vals[d],vals[other]=vals[other],vals[d]
            where[s],where[old]=d,other
            swaps+=1
    need(vals==source_at_out,'actual shuffled labels')
    return 18*swaps


def zero_polynomial_ratio(nodes,x):
    poly=np.array([1],dtype=np.uint8)
    for y in nodes:
        z=np.zeros(len(poly)+1,dtype=np.uint8)
        z[:-1]^=G[y,poly]
        z[1:]^=poly
        poly=z
    value=0;deriv=0
    for d,q in enumerate(poly):
        value^=int(G[q,POW[x,d]])
        if d%2:deriv^=int(G[q,POW[x,d-1]])
    need(value!=0 and len(poly)==16,'fifteen-node residual')
    return int(G[deriv,INV[value]])


def audit_template(hword):
    cost={}
    for n in (9,36):
        k=n//3;entry=hword[str(n)]
        v=POW[1:n+1,:n]
        nbits=6*n;binary_matrix=[1<<d for d in range(nbits)]
        for p,q in entry['V_binary_ADD']:
            need(p in range(nbits) and q in range(nbits) and p!=q,'H legal ADD')
            binary_matrix[p]^=binary_matrix[q]
        need(binary_matrix==binary(v),'H complete physical template')
        for p,q in reversed(entry['V_binary_ADD']):binary_matrix[p]^=binary_matrix[q]
        need(binary_matrix==[1<<d for d in range(nbits)],'H template inverse')
        for tag,m in [('two',2*k),('singleton',n)]:
            grad=np.zeros((n,n),dtype=np.uint8)
            for t in range(1,m,2):grad[:,t]=POW[1:n+1,t-1]
            need(np.array_equal(grad,entry[tag]['cross_coefficients']),'actual derivative coefficients')
            used=np.flatnonzero(grad.any(axis=0))
            need(list(used)==entry[tag]['cache_field_columns'],'H independent snapshot coordinates')
            cost[n,tag]=(len(used)*6,int(BINCOST[grad].sum()))
        cost[n,'v']=len(entry['V_binary_ADD'])
    return cost


def read_data(repo):
    base=repo/'research/moonshot-005-program/results'
    raw={key:read(base/path,sha) for key,(path,sha) in PINS.items()}
    geo=json.loads(raw['layout']);sel=set(json.loads(raw['spread'])['selected_D'])
    by_h=defaultdict(list);by_k=defaultdict(dict);seen=set()
    for row in raw['routes'].splitlines():
        phase,j,col,h,d,k,line,i=json.loads(row)
        fid=53280*(phase=='Y')+480*j+col
        need(phase in ('X','Y') and j in range(111) and col in range(480) and fid not in seen,'owner labels')
        seen.add(fid)
        if h is not None:by_h[h].append((fid,phase,d,line))
        if k is not None:by_k[k][fid]=(phase,d,j if phase=='Y' else i)
    planes=geo['A2']; d4=[set(d) for d in geo['D4']]
    r=np.array(geo['root_table'],dtype=np.int64)
    ortho=r@r.T==0
    node={j:{h:n+1 for n,h in enumerate(i for i,hs in enumerate(planes) if j in hs)} for j in range(111)}
    half_by=defaultdict(list);quota={}
    for h,v in by_h.items():
        c=Counter(line for f,p,d,line in v if p=='X')
        for j,m in c.items():
            quota[h,j]=m
            if m==15:half_by[j].append(h)
    first={j:set(sorted(half_by[j])[:12]) for j in range(111)}
    return planes,d4,ortho,sel,by_h,by_k,node,first,quota


def rank_batch(xx):
    a=np.array(xx,dtype=np.uint8,copy=True)
    b,n,w=a.shape; idx=np.arange(b); valid=np.ones(b,dtype=bool)
    for c in range(w):
        nz=a[:,c:,c]!=0
        valid &= nz.any(axis=1)
        p=c+nz.argmax(axis=1)
        a[idx,c],a[idx,p]=a[idx,p].copy(),a[idx,c].copy()
        inv=np.asarray(INV,dtype=np.uint8)[a[:,c,c]]
        unit=G[inv[:,None],a[:,c,c:]]
        a[:,c+1:,c:] ^= G[a[:,c+1:,c,None],unit[:,None,:]]
    return valid


def h_and_source(data,hcost,scales):
    planes,d4,ortho,marks,by_h,by_k,node,first,quota=data
    hprice=Counter();sprice=Counter();sizes=Counter();patterns=defaultdict(set)
    bindings=defaultdict(list);seen_source=set();early_bank=Counter();ports={};viewtotal=0
    for h,plane in enumerate(planes):
        ns=sorted(j for j in plane if j<111);r=len(ns);groups=defaultdict(list);outputs=defaultdict(list)
        for f,phase,d,line in by_h[h]:
            require_line=(line in ns) if phase=='X' else (line is None or line in ns)
            need(require_line,'authentic H inlet')
            span=list(range(8*f,8*f+8))
            groups[phase,line]+=span;outputs[phase,d]+=span
        groups={key:sorted(v) for key,v in groups.items()}
        outputs={key:sorted(v) for key,v in outputs.items()}
        ds=sorted({d for p,d in outputs});ports[h]={n:[d for d in ds if (d in marks)==(n==9)] for n in (9,36)}
        for i in np.flatnonzero(ortho[:,plane].all(axis=1)):
            viewtotal+=1
            for n,part in ports[h].items():
                visible=tuple(t for t,d in enumerate(part) if all(ortho[i,j] for j in d4[d]))
                need(len(visible)==n//3 and len(part)==n,'balanced H receiver view')
                patterns[n].add(visible)
        if not r:continue
        for phase in ('X','Y'):
            if not any(key[0]==phase for key in outputs):continue
            pos=Counter();from_owner={}
            for n,part in ports[h].items():
                k=n//3;nlane=len(outputs[phase,part[0]])
                need(nlane in (8,16) and all(len(outputs[phase,d])==nlane for d in part),'uniform component lane quotas')
                if r==3:
                    col=[j for j in ns for _ in range(k)]
                elif r==2:
                    big=max(ns,key=lambda j:quota[h,j]);small=next(j for j in ns if j!=big)
                    col=[big]*(2*k)+[small]*k if phase=='X' else [small]*k+[None]*(2*k)
                else:col=[ns[0] if phase=='X' else None]*n
                for deg,(j,d) in enumerate(zip(col,part)):
                    for lane,output in enumerate(outputs[phase,d]):
                        inp=groups[phase,j][pos[j]];pos[j]+=1
                        from_owner[output]=inp
                        if j is None:continue
                        need(inp not in seen_source,'unique source tap')
                        seen_source.add(inp);sizes[phase]+=1
                        if r==3 and nlane==16:
                            c=deg%k+(lane//8)*k; stripe=lane%8;der=0;scale=1
                        elif r==2 and j==big:
                            c=deg;stripe=lane;der=0;scale=1
                        elif r==1:
                            c=deg if deg<2*k else deg-2*k;stripe=lane;der=int(deg>=2*k)
                            scale=scales[j][int(n==36)] if der else 1
                        else:
                            use_a=(h in first[j])==(phase=='X')
                            c=deg%k+(not use_a)*k;stripe=lane;der=0;scale=1
                        need(c in range(2*k) and stripe<8,'physical RS channel')
                        if phase=='X':
                            early_bank[j,n]+=1
                            bindings[j,n,stripe,c].append((h,der,scale,inp))
                        else:
                            sprice['late_evaluation_ADD']+=int(BINCOST[np.asarray(coef(node[j][h],der,scale))].sum())
                hprice['template_ADD']+=nlane*hcost[n,'v']
                if phase=='Y' and r<3:
                    cached,cross=hcost[n,'two' if r==2 else 'singleton']
                    hprice['cache_bits']+=nlane*cached;hprice['derivative_ADD']+=nlane*cross
            ids=sorted(from_owner); index={f:q for q,f in enumerate(ids)}
            hprice['permutation_ADD']+=permcost([index[from_owner[w]] for w in ids])
            need(all(pos[j]==len(v) for (p,j),v in groups.items() if p==phase),'all input owners consumed')
    for j in range(111):
        out_to_src=[-1]*3840;src=0
        need((early_bank[j,9],early_bank[j,36])==(768,3072),'component allocation')
        for n in (9,36):
            for s in range(8):
                for c in range(2*(n//3)):
                    rows=sorted(bindings[j,n,s,c])
                    desc=tuple((node[j][h],der,m) for h,der,m,f in rows)
                    need(len(rows)==16,'exact pure source rows')
                    sprice['early_basis_ADD']+=rsword(desc,False)
                    for h,der,m,f in rows:
                        dst=f-j*3840;need(dst in range(3840) and out_to_src[dst]<0,'source owner span')
                        out_to_src[dst]=src;src+=1
        sprice['permutation_ADD']+=permcost(out_to_src)
    need(sizes=={'X':426240,'Y':321000} and viewtotal==40320,'complete original access')
    sprice['cache_bits']=111*3840*6
    for n,pat in patterns.items():
        k=n//3;a=np.array(sorted(pat),dtype=int)
        values=POW[1:n+1,:2*k];deriv=np.zeros_like(values);deriv[:,1::2]=values[:,:2*k-1:2]
        for z in range(0,len(a),256):
            sub=a[z:z+256]
            need(rank_batch(np.concatenate((values[sub],deriv[sub]),axis=1)).all(),'direct H Hermite rank')
            for c in range(3):
                need(rank_batch(POW[sub+1,c*k:(c+1)*k]).all(),'direct block projection')
    hprice['total_ADD_including_pure_inverse']=2*(hprice['template_ADD']+hprice['permutation_ADD'])+hprice['cache_bits']+hprice['derivative_ADD']
    sprice['total_ADD_including_pure_inverse']=2*(sprice['early_basis_ADD']+sprice['permutation_ADD'])+sprice['cache_bits']+sprice['late_evaluation_ADD']
    return hprice,sprice,ports,{n:len(v) for n,v in patterns.items()}


def residual_matrix(nodes,k,ratio,scale,side):
    z=G[ratio,scale]
    powers=POW[np.array(nodes),:3*k]
    dv=np.zeros_like(powers)
    for t in range(1,3*k,2):dv[:,t]=powers[:,t-1]
    # Form unconstrained jet operator first, then apply the actual restriction
    # from the fifteen ordinary nodes to the singleton coefficients.
    J=np.concatenate((powers,dv if side=='source' else np.concatenate((dv[:,:2*k],np.zeros((k,k),dtype=np.uint8)),axis=1)))
    return J[:,:2*k] ^ np.concatenate((G[z,J[:,2*k:]],np.zeros((2*k,k),dtype=np.uint8)),axis=1)


def rs_foreign(data,parts,scales,source):
    planes,d4,ortho,marks,by_h,by_k,node,first,quota=data
    ordinary=special=minors=0;unscaled=None;dctrl=None
    for i in range(111):
        h0=next((h for h in node[i] if sum(u<111 for u in planes[h])==1),None)
        for j in np.flatnonzero(ortho[i,:111]):
            local=[h for h in node[i] if ortho[j,planes[h]].all()]
            need(len(local)==16 and len({node[i][h] for h in local})==16,'true polynomial evaluation nodes')
            if h0 not in local:
                ordinary+=1;continue
            special+=1;x=node[i][h0];resid=zero_polynomial_ratio([node[i][h] for h in local if h!=h0],x)
            for n,ds in parts[h0].items():
                k=n//3
                if source:
                    pts=[u+1 for u,d in enumerate(ds) if all(ortho[j,v] for v in d4[d])]
                else:
                    pts=[u+1 for u,d in enumerate(ds) if j in d4[d]]
                need(len(pts)==k,'true incoming/outgoing singleton labels')
                scale=scales[i][{9:0,36:1,45:2}[n]]
                side='source' if source else 'terminal'
                full=_rank(residual_matrix(pts,k,resid,scale,side))
                need(full==2*k,'rank of singleton kernel under complete actual jet')
                if scale!=1 and unscaled is None:
                    wrong=_rank(residual_matrix(pts,k,resid,1,side))
                    if wrong<2*k:unscaled=[int(i),int(j),h0,n,wrong,full]
                if dctrl is None:
                    EV=POW[np.array([node[i][a] for a in local]),:16]
                    bad=EV.copy();bad[-1]=bad[0]
                    need(_rank(EV)==16 and _rank(bad)==15,'duplicate RS node mutation')
                    dctrl=True
                minors+=1
    need((ordinary,special)==(6110,360) and unscaled is not None,'complete foreign coverage')
    return {'ordinary':ordinary,'singleton':special,'singleton_component_tests':minors,
            'bad_unscaled':unscaled,'duplicate_node_control':dctrl}


def terminals(data,kwords,scales):
    planes,d4,ortho,marks,by_h,by_k,node,first,quota=data
    parts={};bindings=defaultdict(list);money=Counter(); visits=Counter();uniq=set()
    for key,chart in kwords.items():
        h=int(key); entries=by_k[h];ns=[j for j in planes[h] if j<111];r=len(ns);parts[h]={}
        ordinals=Counter();early_positions={};expected=set()
        for phase,ins,outs in chart['stripes']:
            n=len(ins);k=n//3;band=ordinals[phase,n];ordinals[phase,n]+=1
            ports=[entries[f][1] for f in ins]
            need(ports==sorted(set(ports)) and parts[h].setdefault(n,ports)==ports,'native ordered K ports')
            if phase=='X':early_positions[n]=outs
            if phase=='Y' and r<3:
                expected.update((early_positions[n][t-1],outs[t]) for t in range(1,2*k,2))
            for t,f in enumerate(outs):
                p,d,i=entries[f];need(p==phase, 'K output phase')
                if r==3:
                    actual=ns[t//k]
                elif r==2:
                    small=next(v for v in ns if quota[h,v]==15)
                    large=next(v for v in ns if v!=small)
                    actual=small if t>=2*k else large if phase=='Y' else None
                else:actual=ns[0] if phase=='Y' else None
                need(i==actual,'K row owner and native receiver')
                if i is None:continue
                need(f not in uniq,'duplicated F owner');uniq.add(f);visits[phase]+=8
                der=0;scale=1
                if r==3 and quota[h,i]==30:c=t%k+band*k
                elif r==2 and quota[h,i]==30:c=t
                elif r==1:
                    der=int(t>=2*k);c=t-2*k if der else t;scale=scales[i][{9:0,36:1,45:2}[n]] if der else 1
                else:c=t%k+int((phase=='Y')!=(h in first[i]))*k
                for copy in range(8):
                    if phase=='Y':
                        bindings[i,n,copy,c].append((h,der,scale,8*f+copy))
                    else:
                        need(not der and scale==1,'early F capture is a plain evaluation')
                        money['early_to_late_ADD']+=int(BINCOST[POW[node[i][h],:16]].sum())
        need(expected==set(map(tuple,chart['early_cache_to_late'])),'actual truncated K derivative')
    groups=sorted(parts[next(iter(parts))])
    for i in range(111):
        ids=[]
        for n in groups:
            for cp in range(8):
                for c in range(2*(n//3)):
                    rows=sorted(bindings[i,n,cp,c]);need(len(rows)==16,'16 actual F basis rows')
                    sig=tuple((node[i][h],der,scale) for h,der,scale,f in rows)
                    money['late_basis_ADD']+=rsword(sig,True)
                    ids.extend(f-(53280+480*i)*8 for h,der,scale,f in rows)
        money['permutation_ADD']+=permcost(ids)
    need(visits=={'X':321000,'Y':426240},'actual F visit counts')
    money['cache_bits']=6*visits['X']
    money['total_ADD_including_pure_inverse']=2*(money['late_basis_ADD']+money['permutation_ADD'])+money['cache_bits']+money['early_to_late_ADD']
    return money,rs_foreign(data,parts,scales,False)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--author',type=Path,required=True)
    parser.add_argument('--k-certs',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    expected_h=json.loads((args.author/'output/RESULT.json').read_text())['finite_word_accounting']
    expected_s=json.loads((args.author/'source-output/RESULT.json').read_text())
    expected_t=json.loads((args.author/'terminal-output/RESULT.json').read_text())
    ss={int(k):v for k,v in expected_s['chosen_singleton_scales'].items()}
    data=read_data(args.repo)
    hword=json.loads(read(args.author/'output/WORDS.json.gz',HPIN))
    hcost=audit_template(hword)
    hp,sp,parts,patterns=h_and_source(data,hcost,ss)
    s_checked=rs_foreign(data,parts,ss,True)
    need(hp['total_ADD_including_pure_inverse']==789156832 and sp['total_ADD_including_pure_inverse']==336206520,'H and source paid totals')
    need(hp['permutation_ADD']==expected_h['permutation_ADD'] and sp['permutation_ADD']==expected_s['finite_source_costs']['source_owner_permutation_ADD'],'independent shuffles matched')
    result={'status':'PASS_NATIVE_RS_SOURCE_H_AND_BOTH_PAID_TERMINALS','H':dict(hp),'RS_source':dict(sp),'left_rank':s_checked,
            'distinct_H_node_subsets':patterns,'audited_parent_H_views':40320,'actual_native_H_donor_views':103520,
            'field':67,'source_pins':{p:s for p,s in PINS.values()},'H_payload':HPIN,'K_payloads':KPIN,'new_complete_kappa':False}
    for mode in ('SPREAD','MIXED'):
        ext=expected_t[mode.lower()]
        ts={int(k):v for k,v in ext['chosen_singleton_scales_by_9_36_45'].items()}
        kwords=json.loads(read(args.k_certs/(mode+'-OWNERS.json.gz'),KPIN[mode]))
        tp,tr=terminals(data,kwords,ts)
        need(tp['total_ADD_including_pure_inverse']==ext['costs']['forward_plus_pure_inverse_ADD'] and
             tp['permutation_ADD']==ext['costs']['actual_Y_permutation_ADD'], 'independent terminal paid bill')
        result[mode]={'terminal':dict(tp),'right_rank':tr}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
