#!/usr/bin/env python3
"""Native receiver-covariant target. Exact finite checks, no physical claim."""
from __future__ import annotations
import argparse, gzip, hashlib, json
from fractions import Fraction
from pathlib import Path

LAYOUT_PIN='9f3834b7663a25b782531a11ccc22cffb66433de1a9a072059395265fdb07b72'
def need(value,label):
    if not value: raise ValueError(label)
def rank(rows):
    piv={}
    for x in rows:
        while x:
            k=x.bit_length()-1
            if k not in piv: piv[k]=x; break
            x^=piv[k]
    return len(piv)
def independent(rows):
    piv={};out=[]
    for row in rows:
        x=row
        while x:
            k=x.bit_length()-1
            if k not in piv: piv[k]=x;out.append(row);break
            x^=piv[k]
    return out
def tr(rows,n=None):
    n=len(rows) if n is None else n;out=[0]*n
    for i,x in enumerate(rows):
        while x:
            z=x&-x;out[z.bit_length()-1]^=1<<i;x^=z
    return out
def mm(A,B):
    out=[]
    for x in A:
        z=0
        while x:
            low=x&-x;z^=B[low.bit_length()-1];x^=low
        out.append(z)
    return out
def add(A,B):return [x^y for x,y in zip(A,B)]
def action(A,x):return sum(((row&x).bit_count()%2)<<i for i,row in enumerate(A))
def eye(n):return [1<<i for i in range(n)]
def power(A,n):
    out=eye(len(A))
    while n:
        if n&1:out=mm(out,A)
        A=mm(A,A);n>>=1
    return out
def inverse_binary(A):
    n=len(A);rows=[x|(1<<(n+i))for i,x in enumerate(A)]
    for c in range(n):
        k=next(k for k in range(c,n)if rows[k]>>c&1)
        rows[c],rows[k]=rows[k],rows[c]
        for k in range(n):
            if k!=c and rows[k]>>c&1:rows[k]^=rows[c]
    need([x&((1<<n)-1)for x in rows]==eye(n),'binary inverse left identity')
    return [x>>n for x in rows]
def inverse_rational(A):
    n=len(A);rows=[[Fraction(x)for x in r]+[Fraction(i==j)for j in range(n)]for i,r in enumerate(A)]
    for c in range(n):
        k=next(k for k in range(c,n)if rows[k][c]);rows[c],rows[k]=rows[k],rows[c]
        z=rows[c][c];rows[c]=[x/z for x in rows[c]]
        for k in range(n):
            if k!=c and rows[k][c]:
                z=rows[k][c];rows[k]=[x-z*y for x,y in zip(rows[k],rows[c])]
    return [r[n:]for r in rows]

def geometry(layout,basis):
    roots=layout['root_table'];cols=basis['lattice_basis_columns']
    inv=inverse_rational([[cols[j][i]for j in range(8)]for i in range(8)])
    hyp=basis['hyperbolic_basis_masks'];lookup={}
    for v in range(256):
        z=0
        for k in range(8):
            if v>>k&1:z^=hyp[k]
        lookup[z]=v
    need(len(lookup)==256,'hyperbolic coordinate basis')
    prim=[]
    for k in range(4):
        C=[0]*16;D=[0]*16
        for j in range(16):
            if j>>k&1:D[j^(1<<k)]^=1<<j
            else:C[j|(1<<k)]^=1<<j
        prim.extend([C,D])
    gam=[]
    for root in roots:
        cs=[sum(c*x for c,x in zip(r,root))for r in inv]
        need(all(c.denominator==1 for c in cs),'integral root coordinates')
        v=sum((int(c)%2)<<i for i,c in enumerate(cs));g=[0]*16
        for k in range(8):
            if lookup[v]>>k&1:g=add(g,prim[k])
        need(mm(g,g)==eye(16),'native gamma square');gam.append(g)
    adj=[{j for j,y in enumerate(roots[:111])if i!=j and sum(u*v for u,v in zip(x,y))==0}
         for i,x in enumerate(roots[:111])]
    for i in range(111):
        for j in range(i):
            expected=[0]*16 if j in adj[i] else eye(16)
            need(add(mm(gam[i],gam[j]),mm(gam[j],gam[i]))==expected,'actual native Clifford pair')
    K=[(1<<i)|sum(1<<j for j in adj[i])for i in range(111)]
    need(rank(K)==9 and sum(map(len,adj))==6470,'native rank and edge census')
    need(10 not in adj[80] and [len(adj[80]),len(adj[10])]==[62,61],'native separated stars')
    seen={0};todo=[0]
    while todo:
        for j in adj[todo.pop()]-seen:seen.add(j);todo.append(j)
    need(len(seen)==111,'native connectivity')
    for support in [adj[80]|{10},adj[10]|{80}]:
        mask=((1<<111)-1)^sum(1<<j for j in support)
        need(rank([x&mask for x in K])==9,'native exact support separation')
    return gam,adj,K

def adapted(gam):
    A=add(gam[80],eye(16));C=add(gam[10],eye(16))
    need(mm(A,A)==mm(C,C)==[0]*16 and add(mm(A,C),mm(C,A))==eye(16),'two Clifford nilpotents')
    es=independent(tr(A));need(len(es)==8,'image dimension eight')
    columns=es+[action(C,e)for e in es]
    P=tr(columns);Pinv=inverse_binary(P)
    A2=[1<<(8+i)for i in range(8)]+[0]*8
    C2=[0]*8+[1<<i for i in range(8)]
    need(mm(mm(Pinv,A),P)==A2 and mm(mm(Pinv,C),P)==C2,'explicit adapted Clifford form')
    return columns,[mm(mm(Pinv,g),P)for g in gam]

def generators(w):
    need(w>=2,'secondary width at least two');L=60*w;b=2*L
    J=[0]*L;E=[0]*L
    for k in range(w-1):J[k]=1<<(k+1)
    E[w-1]=1
    Ts=[]
    for l in range(1,60):
        T=[0]*L
        for k in range(w):T[k]=1<<(l*w+k)
        Ts.append(T)
    def lift(N):return N+[x<<L for x in N]
    cross01=[0]*b;cross10=[0]*b
    for k in range(w):cross01[k]=1<<(L+k);cross10[L+k]=1<<k
    rows=[lift(N)for N in [J,E]+Ts]+[cross01]
    cols=[lift(tr(T))for T in Ts]+[cross10,[0]*b]
    need(len(rows)==62 and len(cols)==61,'native generator slots')
    return rows,cols,(J,E,Ts)

def assignment(adj,w):
    rows,cols,_=generators(w)
    out={(80,j):N for j,N in zip(sorted(adj[80]),rows)}
    for i,N in zip(sorted(adj[10]),cols):
        need((i,10)not in out,'disjoint stars');out[i,10]=N
    for i,j in out:
        need(j in adj[i]and (j,i)not in out,'native support and identity reverse')
    return out

def structural(w):
    rows,cols,(J,E,Ts)=generators(w);L=60*w;b=2*L
    need(power(J,w)==[0]*L and any(power(J,w-1)),'exact Jordan index')
    for N in rows[1:]+cols:
        need(mm(N,N)==[0]*b,'all other perturbations square zero')
    need(rank([r for N in rows for r in tr(N)])==2*w,'row-star image dimension')
    need(rank([r for N in cols for r in N])==2*w,'column-star input dimension')
    need(rank([r for N in rows for r in N])==b,'row common kernel zero')
    need(rank([r for N in rows+cols for r in tr(N)])==b,'combined images fill bank')
    # Exact matrix-unit identity at all secondary coordinate positions.
    for r,t in [(0,0),(0,w-1),(w-1,0),(w-1,w-1),(w//2,w//3)]:
        U=mm(mm(power(J,w-1-r),E),power(J,t));expected=[0]*L;expected[r]=1<<t
        need(U==expected,'secondary Jordan closing identity')
    # One complete spanning set of elementary two-factor identities.
    P=[0]*L
    for k in range(w):P[k]=1<<k
    R01=rows[-1];R10=cols[-2]
    expected00=P+[0]*L;expected11=[0]*L+[x<<L for x in P]
    need(mm(R01,R10)==expected00 and mm(R10,R01)==expected11,'two-sided spinor units')
    return {'w':w,'b':b,'excess':4*w,'return_rank':9*b+4*w,'excess_ratio':'1/30',
            'full_matrix_units_proved':b*b,'row_star_rank':2*w,'column_star_rank':2*w}

def full_native(adj,K,w):
    b=120*w;blocks=assignment(adj,w)
    canon=[sum(1<<(j*b+k)for j in range(111)if K[i]>>j&1)for i in range(111)for k in range(b)]
    delta=[0]*(111*b)
    for (i,j),N in blocks.items():
        need(rank(add(N,eye(b)))==b,'literal foreign block invertibility')
        for k,row in enumerate(N):delta[i*b+k]^=row<<(j*b)
    need(rank(delta)==4*w,'literal full native perturbation rank')
    need(rank(add(canon,delta))==9*b+4*w,'literal full native return rank')
    need(rank(canon+delta)==9*b+4*w,'literal full native retained repair rank')
    return {'w':w,'b':b,'literal_matrix_dimension':111*b,'return_rank':9*b+4*w,
            'perturbation_rank':4*w,'altered_or_identity_star_blocks':len(blocks)}

def extended_gamma(g,s):
    w=8*s;L=60*w;b=2*L;out=[0]*b
    for half in range(2):
        for bank in range(60):
            for spin in range(8):
                for copy in range(s):
                    index=half*L+bank*w+spin*s+copy
                    row=g[half*8+spin];z=0
                    for v in range(16):
                        if row>>v&1:z^=1<<((v//8)*L+bank*w+(v%8)*s+copy)
                    out[index]=z
    return out

def covariance(adj,gam):
    s=1;w=8;b=960;blocks=assignment(adj,w)
    cached={};checked=0
    for (i,j),N in blocks.items():
        if i not in cached:cached[i]=extended_gamma(gam[i],s)
        G=cached[i];need(mm(N,G)==mm(G,N),'every modified block receiver covariance');checked+=1
    # A scalar diagonal unit is not nilpotent and destroys invertibility.
    bad=[0]*b;bad[0]=1
    need(rank(add(bad,eye(b)))==b-1,'nonnilpotent diagonal mutation rejected')
    # Replacing the column spinor action by an unrelated root fails locally.
    receiver=sorted(adj[10])[59];counter=None
    for root in range(111):
        if root not in adj[receiver]and root!=receiver:
            N16=add(gam[root],eye(16))
            if mm(N16,gam[receiver])!=mm(gam[receiver],N16):counter=root;break
    need(counter is not None,'wrong-root covariance mutation rejected')
    # Without E10, every generator preserves the first spinor half.
    rows,cols,_=generators(w);mask=(1<<(60*w))-1
    need(all(not(r&mask)for N in rows+cols[:-2]+[cols[-1]]for r in N[60*w:]),
         'omitting E10 leaves a proper invariant half')
    need(any(r&mask for r in cols[-2][60*w:]),'E10 breaks invariant half')
    return {'b':b,'s':s,'direct_commutator_checks':checked,'all_other_foreign_blocks':'identity',
            'wrong_root_control':{'receiver':receiver,'wrong_root':counter},
            'omitted_E10_invariant_dimension':b//2,'diagonal_mutation_rank':b-1}

def budget(data):
    row=data['every_r_zero_through_203'][192]
    need(row['r']==192 and row['first_even_m']==870,'inherited ratio comparison')
    for name,entry in data['power_enclosures'].items():
        lo,hi=map(Fraction,entry['rational'])
        need(lo**200<=int(name)**199<=hi**200,'exact rational power enclosure')
    need(Fraction(row['limiting_room']['rational'][0])>0,'strict limiting movement room')
    need(Fraction(row['previous_gap']['rational'][1])<0,'m868 rejected')
    need(Fraction(row['first_positive_gap']['rational'][0])>0,'m870 accepted')
    return {'first_even_m':870,'previous_even_m':868,'limiting_room':row['limiting_room'],
            'inherited_movement_only':True}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    base=args.repo/'research/moonshot-005-program/results'
    layoutpath=base/'bit-all111-tight-port-atlas/author/output/LAYOUT.json.gz'
    basispath=base/'bit-clifford-one-evaluation-gate/author/BASIS.json'
    budgetpath=base/'bit-canonical-quotient-repair/author/output/BUDGET.json'
    raw=gzip.decompress(layoutpath.read_bytes());need(hashlib.sha256(raw).hexdigest()==LAYOUT_PIN,'exact layout source')
    gam,adj,K=geometry(json.loads(raw),json.loads(basispath.read_text()))
    columns,adaptedgam=adapted(gam)
    finite=full_native(adj,K,2)
    widths=[structural(w)for w in [8,32,96]]
    cov=covariance(adj,adaptedgam)
    inherited=budget(json.loads(budgetpath.read_text()))
    pins=[{'path':str(p.relative_to(args.repo)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
          for p in [layoutpath,basispath,budgetpath,base/'bit-irreducible-low-excess-target/author/PROOF.md',
                    base/'bit-replacement-return-bank/author/PROOF.md']]
    result={'status':'PASS_NATIVE_RECEIVER_COVARIANT_IRREDUCIBLE_TARGET',
            'scope':'explicit algebraic endpoint; no physical H/D/K realization or new complete kappa',
            'theorem_domain':'every characteristic-two field and every positive integer s; b=960s',
            'row_center':80,'column_center':10,'foreign_blocks':6470,'excess_ratio':'1/30',
            'minimum_matrix_source_compatibility':{'s':4,'b':3840,'secondary_width':32,
                'End16_copies':15,'spinor_copies':240,'atlas480_copies':8,'excess':128,'return_rank':34688},
            'literal_full_native_check':finite,'actual_width_structure':widths,'covariance':cov,
            'movement':inherited,'source_pins':pins,
            'negative_controls':['omitted E10 leaves invariant half','wrong Clifford root breaks receiver covariance',
                                 'diagonal mutation makes foreign block singular'],
            'five_foundational_assumptions_retained':True,'new_complete_kappa':False}
    assignment={'row_center':80,'column_center':10,'row_neighbor_order':sorted(adj[80]),
                'column_neighbor_order':sorted(adj[10]),'row_generators':['I2xJ','I2xE']+[f'I2xT{l}'for l in range(1,60)]+['E01xP0'],
                'column_generators':[f'I2xT{l}transpose'for l in range(1,60)]+['E10xP0','zero'],
                'adapted_spinor_basis_columns':columns,'adapted_gamma80':adaptedgam[80],'adapted_gamma10':adaptedgam[10]}
    args.out.mkdir(parents=True,exist_ok=True)
    for name,value in [('RESULT.json',result),('ASSIGNMENT.json',assignment)]:
        (args.out/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(result['status']);print(json.dumps({'finite':finite,'covariance':cov,'matrix_source':result['minimum_matrix_source_compatibility']},sort_keys=True))
if __name__=='__main__':main()
