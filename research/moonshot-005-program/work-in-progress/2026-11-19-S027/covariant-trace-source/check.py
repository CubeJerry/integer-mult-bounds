#!/usr/bin/env python3
"""Exact author verification of the finite covariant-source certificates."""
from __future__ import annotations
from collections import Counter,deque
from hashlib import sha256
from pathlib import Path
import argparse,gzip,json
import numpy as np
import algebra as a

ROUTES_PIN='6d55093625ffd123daf3ae0914bcaeba1308756cec24fd2de083f6887ad0b036'
def mul(x,y):
    z=0
    while y:
        if y&1:z^=x
        x<<=1
        if x&16:x^=19
        y>>=1
    return z
TABLE=np.array([[mul(x,y)for y in range(16)]for x in range(16)],dtype=np.uint8)
BITBLOCK=[[sum(((mul(x,1<<j)>>k)&1)<<j for j in range(4))for k in range(4)]for x in range(16)]
def field_binary_rank(M):
    rows=[]
    for row in M.tolist():
        for bit in range(4):
            rows.append(sum(BITBLOCK[value][bit]<<(4*j)for j,value in enumerate(row)))
    return a.rank(rows)
def array(A,n):return np.array([[(row>>j)&1 for j in range(n)]for row in A],dtype=np.uint8)
def bvec(A,v):
    return np.array([np.bitwise_xor.reduce(np.array([v[j]for j in range(16)if row>>j&1],dtype=np.uint8),initial=0)for row in A],dtype=np.uint8)
def expand_trace_as_left_source(j,k,vectors):
    # Separate reconstruction from the search's direct four-term tensor map.
    base=[a.eye(16),j,k,a.mm(j,k)];lookup={}
    for mask in range(16):
        mat=[0]*16
        for t in range(4):
            if mask>>t&1:mat=a.add(mat,base[t])
        lookup[tuple(mat)]=mask
    a.need(len(lookup)==16,'full local Clifford coefficient basis')
    u=np.zeros((4,16),dtype=np.uint8)
    for C,vector in zip(base,vectors):
        v=np.array(vector,dtype=np.uint8)
        factors=[(a.mm(a.mm(j,k),C),v),(a.mm(j,C),bvec(k,v)),
                 (a.mm(k,C),bvec(j,v)),(C,bvec(a.mm(k,j),v))]
        for L,right in factors:
            mask=lookup[tuple(L)]
            for t in range(4):
                if mask>>t&1:u[t]^=right
    out=np.zeros((16,16,16),dtype=np.uint8)
    for A,v in zip(base,u):out^=array(A,16)[:,:,None]*v[None,None,:]
    return out.reshape(16,256)
def fmat(gam,planes,donor,h,vectors):
    a.need(len(vectors)==4 and all(len(v)==16 for v in vectors),'four actual coefficient vectors')
    a.need(all(0<=x<16 for v in vectors for x in v),'GF16 witness alphabet')
    k=next(k for k in sorted(planes[h])if k!=donor)
    return expand_trace_as_left_source(gam[donor],gam[k],vectors)
def combine(L,F):
    out=np.zeros((len(L),256),dtype=np.uint8);L=np.array(L,dtype=np.uint8)
    for t in range(16):out^=TABLE[L[:,t,None],F[t,None,:]]
    return out
def pmod(x,p):
    while x.bit_length()>=p.bit_length():x^=p<<(x.bit_length()-p.bit_length())
    return x
def pgcd(x,y):
    while y:x,y=y,pmod(x,y)
    return x
def field512():
    p=(1<<9)|(1<<4)|1
    def square(x):return pmod(sum(((x>>k)&1)<<(2*k)for k in range(x.bit_length())),p)
    x=2
    for _ in range(9):x=square(x)
    y=2
    for _ in range(3):y=square(y)
    a.need(x==2 and pgcd(y^2,p)==1,'exact GF512 irreducibility')
    return {'polynomial_binary':p,'polynomial':'z^9+z^4+1','x_to_512_mod_p':x,'proper_factor_gcd':1}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--witnesses',type=Path);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    here=Path(__file__).resolve().parent;wdir=args.witnesses or here/'output';base=args.repo/'research/moonshot-005-program/results'
    layoutpath=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    basispath=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    routespath=base/'bit-asymmetric-balanced-atlas/author/output/ROUTES.jsonl.gz'
    layoutraw=gzip.decompress(layoutpath.read_bytes());routesraw=gzip.decompress(routespath.read_bytes())
    a.need(sha256(layoutraw).hexdigest()==a.LAYOUT_PIN,'authenticated native layout')
    a.need(sha256(routesraw).hexdigest()==ROUTES_PIN,'authenticated literal source routes')
    layout=json.loads(layoutraw);gam,adj,K=a.geometry(layout,json.loads(basispath.read_text()))
    roots=layout['root_table'];planes=list(map(set,layout['A2']));planemap={frozenset(H):h for h,H in enumerate(planes)}
    gammaids={tuple(g):i for i,g in enumerate(gam)};a.need(len(gammaids)==120,'unique gamma native roots')
    alladj=[{j for j,y in enumerate(roots)if i!=j and sum(u*v for u,v in zip(x,y))==0}for i,x in enumerate(roots)]
    complete=set()
    for i in range(120):
        for j in range(i):
            if j not in alladj[i]:
                k=gammaids[tuple(a.add(gam[i],gam[j]))];complete.add(frozenset([i,j,k]))
    a.need(set(planemap)==complete and len(complete)==1120,'complete native A2 list')
    perms=[]
    for u in range(120):
        p=[gammaids[tuple(a.mm(a.mm(gam[u],g),gam[u]))]for g in gam]
        a.need(len(set(p))==120 and all(p[p[v]]==v for v in range(120)),'actual Clifford transvection')
        perms.append(p)
    orbitpath=wdir/'ORBIT.json.gz';orbit=json.loads(gzip.decompress(orbitpath.read_bytes()))
    origin=tuple(orbit['origin']);a.need(origin==(5,77),'fixed origin')
    children={};nodes={origin}
    for i,j,pi,pj,u in orbit['edges']:
        a.need((i,j)not in nodes,'unique orbit tree node');nodes.add((i,j))
        a.need(0<=u<120 and [perms[u][pi],perms[u][pj]]==[i,j],'actual orbit edge')
        children.setdefault((pi,pj),[]).append((i,j))
    reached={origin};todo=[origin]
    while todo:
        for child in children.get(todo.pop(),[]):
            a.need(child not in reached,'acyclic rooted orbit tree');reached.add(child);todo.append(child)
    expected={(i,j)for i in range(120)for j in alladj[i]}
    a.need(reached==nodes==expected and len(nodes)==7560,'complete orthogonal pair orbit')
    a.need(all((i,j)in reached for i in range(111)for j in adj[i]),'all 6470 native pairs covered')
    # Rank-eight coefficient basis checked at every actual A2 plane.
    localchecks=0
    for H in planes:
        j,k=sorted(H)[:2];N=a.add(gam[j],a.eye(16));M=a.add(gam[k],a.eye(16))
        C=[a.mm(N,M),N,M,a.mm(M,N)]
        a.need(a.add(C[0],C[3])==a.eye(16),'local diagonal units sum to identity')
        for x in range(2):
            for y in range(2):
                for z in range(2):
                    for t in range(2):
                        a.need(a.mm(C[2*x+y],C[2*z+t])==(C[2*x+t]if y==z else [0]*16),'full local matrix unit multiplication')
        a.need(all(a.rank(A)==8 for A in C),'all four coefficient maps have rank eight');localchecks+=4
    pairpath=wdir/'PAIR-WITNESS.json';pair=json.loads(pairpath.read_text());i,j=pair['pair']
    hs=[h for h,H in enumerate(planes)if j in H and H<=alladj[i]]
    a.need([i,j]==[5,77]and pair['planes']==hs and len(hs)==16,'actual witness foreign view')
    parts=[fmat(gam,planes,j,h,v)for h,v in zip(hs,pair['vectors'])]
    F=np.concatenate(parts);a.need(F.shape==(256,256),'complete foreign matrix')
    pairrank=field_binary_rank(F);a.need(pairrank==1024,'exact binary expansion of foreign witness')
    bad=F.copy();bad[:16]=0;a.need(field_binary_rank(bad)==960,'missing source quotient negative control')
    routes=[json.loads(line)for line in routesraw.splitlines()];counts=Counter()
    for row in routes:
        if row[0]=='X':counts[row[1],row[3]]+=1
    a.need(sum(counts.values())==53280,'actual source owner census')
    a.need(Counter(counts.values())=={15:2675,30:422,45:11},'actual source quota types')
    quotas={(j,h):n*8//15 for(j,h),n in counts.items()}
    a.need(all(n%15==0 for n in counts.values()),'exact quota normalization')
    for donor in range(111):a.need(sum(n for(j,h),n in quotas.items()if j==donor)==256,'complete donor early dimension')
    earlypath=wdir/'EARLY-WITNESSES.json.gz';early=json.loads(gzip.decompress(earlypath.read_bytes()))
    a.need([x['donor']for x in early]==list(range(111)),'all native donor certificates')
    earlyranks=[];negative=None;extra_count=0;early_rows_count=0
    for cert in early:
        donor=cert['donor'];a.need([f['plane']for f in cert['flags']]==sorted(h for(j,h)in quotas if j==donor),'complete actual early flags')
        rows=[]
        for flag in cert['flags']:
            h=flag['plane'];n=quotas[donor,h];L=flag['early_output_rows'];extra=flag['extra_rows']
            a.need(len(L)==min(n,16)and all(len(row)==16 for row in L),'actual early quotient row counts')
            a.need(len(extra)==max(n-16,0)and all(len(row)==256 for row in extra),'actual extra owner rows')
            a.need(all(0<=x<16 for row in L+extra for x in row),'early coefficient alphabet')
            F=fmat(gam,planes,donor,h,flag['vectors']);rows.append(combine(L,F))
            if extra:rows.append(np.array(extra,dtype=np.uint8))
            extra_count+=len(extra);early_rows_count+=len(L)+len(extra)
        M=np.concatenate(rows);a.need(M.shape==(256,256),'complete literal early matrix')
        r=field_binary_rank(M);a.need(r==1024,'all 111 exact early binary ranks');earlyranks.append(r)
        if donor==0:
            count=quotas[donor,cert['flags'][0]['plane']];bad=M.copy();bad[:count]=0
            rankbad=field_binary_rank(bad);a.need(rankbad==4*(256-count),'omitted early owner group control')
            negative={'donor':0,'omitted_rows':count,'binary_rank':rankbad}
    a.need(extra_count==88 and early_rows_count==111*256,'all genuine extra early owners retained')
    H=planes[263];a.need(0 in H,'fixed noncommuting incidence');j,k=sorted(H)[:2]
    N=a.add(gam[j],a.eye(16));M=a.add(gam[k],a.eye(16))
    a.need(a.add(a.mm(N,M),a.mm(M,N))==a.eye(16),'nonzero local coefficient commutator')
    fanout=max(sum(H<=alladj[i]for i in range(111))for H in planes);a.need(fanout==36,'actual maximum native source fanout')
    degree=8*(fanout+1)+2;a.need(degree==298 and degree<512,'simultaneous field bound')
    field=field512();r=15;Mbits=2304*r;late=192600*r;ADD=222*(Mbits*Mbits+3*Mbits)+Mbits*late+late
    paths=[layoutpath,basispath,routespath,base/'bit-balanced-quotient-source-compiler/author/PROOF.md',
           base/'bit-clifford-two-evaluation-source/author/PROOF.md']
    pins=[{'path':str(p.relative_to(args.repo)),'sha256':sha256(p.read_bytes()).hexdigest()}for p in paths]
    pins += [{'path':'author/output/'+p.name,'sha256':sha256(p.read_bytes()).hexdigest(),
              **({'decompressed_sha256':sha256(gzip.decompress(p.read_bytes())).hexdigest()}if p.suffix=='.gz'else{})}
             for p in [pairpath,orbitpath,earlypath]]
    pins += [{'path':'author/'+p.name,'sha256':sha256(p.read_bytes()).hexdigest()}for p in [here/'algebra.py',here/'search.py']]
    result={'status':'PASS_NATIVE_FULL_COVARIANT_SOURCE_CERTIFICATES','scope':'source existence and paid source module only; H/D/K and full supplier open',
            'complete_root_count':120,'A2_plane_count':1120,'full_orthogonal_pair_orbit':7560,'native_foreign_pairs':6470,
            'origin_foreign_binary_rank':pairrank,'foreign_views_proved_nonzero_by_transport':6470,
            'early_donors':111,'early_binary_rank_histogram':dict(Counter(earlyranks)),
            'early_quota_histogram':dict(Counter(quotas.values())),'extra_early_field_rows_per_matrix_copy':extra_count,
            'rank_eight_coefficient_basis_checks':localchecks,'parameter_dimension_per_incidence':64,
            'maximum_native_fanout':fanout,'individual_degree_bound_with_noncommuting_constraint':degree,
            'fixed_field':field,'chosen_global_GF512_coefficients_emitted':False,
            'minimum_actual_bank_invoice':{'matrix_copies':15,'field_bank':3840,'field_bits':9,'binary_bank':Mbits,
                'late_binary_caches':late,'ADD_upper_bound':ADD,'INIT':late,'charged_dirty_CLEAR':late,'additional_MOVE':0},
            'negative_controls':{'missing_foreign_quotient_binary_rank':960,'omitted_early_owner_group':negative,
                                 'noncommuting_coefficient_commutator':'I16'},
            'source_pins':pins,'new_complete_kappa':False,'five_foundational_assumptions_retained':True}
    args.out.mkdir(parents=True,exist_ok=True);(args.out/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (args.out/'QUOTAS.json').write_text(json.dumps([[j,h,n]for(j,h),n in sorted(quotas.items())],separators=(',',':'))+'\n')
    print(result['status']);print(json.dumps({k:result[k]for k in ['full_orthogonal_pair_orbit','early_binary_rank_histogram','early_quota_histogram','individual_degree_bound_with_noncommuting_constraint','minimum_actual_bank_invoice']},sort_keys=True))
if __name__=='__main__':main()
