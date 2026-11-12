#!/usr/bin/env python3
"""Independent exact eight-packet review; no author imports."""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse,collections,gzip,hashlib,json
PIN='2b94953dc14a122e3ef089633f05b58ec689ec5156feb7c784ed3e137dc01883'
def need(b,s):
    if not b:raise ValueError(s)
def span(frame):
    out={0}
    for x in frame:out|={y^x for y in out}
    return out
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def odd(x):return x.bit_count()%2
def roots(v):
    S=[k for k in range(9) if(v>>k)&1]
    if len(S)==3:return [Q(int(k in S))-Q(1,3) for k in range(9)]
    need(len(S)==7,'weight3 or7');i,j=[k for k in range(9) if k not in S]
    return [Q(int(k==i)-int(k==j)) for k in range(9)]
def from_roots(v):
    r=roots(v);need(sum(r)==0 and dot(r,r)==2,'hyperplane root')
    a=[2*r[k]+r[8] for k in range(8)];need(all(x.denominator==1 for x in a),'integer rotated code')
    return [int(x) for x in a]
def piecewise(v):
    S={k for k in range(9) if(v>>k)&1}
    if len(S)==3:return [2*int(k in S) if 8 in S else 2*int(k in S)-1 for k in range(8)]
    need(len(S)==7,'piecewise weight');i,j=sorted(set(range(9))-S)
    return [2*int(k==i)-1 if j==8 else 2*(int(k==i)-int(k==j)) for k in range(8)]
def eliminate(rows):
    B={};ind=[];rels=[]
    for i,row in enumerate(rows):
        z=list(map(Q,row));co={i:Q(1)}
        for p,(b,bc) in sorted(B.items()):
            if z[p]:
                c=z[p];z=[x-c*y for x,y in zip(z,b)]
                for j,y in bc.items():
                    co[j]=co.get(j,Q(0))-c*y
                    if not co[j]:del co[j]
        p=next((j for j,x in enumerate(z) if x),None)
        if p is None:rels.append(co)
        else:
            c=z[p];B[p]=([x/c for x in z],{j:x/c for j,x in co.items()});ind.append(i)
    return len(B),ind,rels
def det(a):
    r=[list(map(Q,row)) for row in a];out=Q(1)
    for k in range(len(r)):
        p=next((i for i in range(k,len(r)) if r[i][k]),None)
        if p is None:return Q(0)
        if p!=k:r[k],r[p]=r[p],r[k];out=-out
        c=r[k][k];out*=c
        for i in range(k+1,len(r)):
            d=r[i][k]/c
            for j in range(k,len(r)):r[i][j]-=d*r[k][j]
    return out
def validate_gram(V,A):
    for i,v in enumerate(V):
        need(dot(A[i],A[i])==8,'Gram diagonal')
        for j in range(i):
            g=dot(A[i],A[j]);need(g==0 if odd(v&V[j]) else abs(g)==4,'Gram parity pattern')
def main(a):
    raw=a.source.read_bytes();need(hashlib.sha256(raw).hexdigest()==PIN,'native source pin');w=json.loads(gzip.decompress(raw))
    V=w['ports'];Xs=w['live'];need(len(V)==len(Xs)==104 and len(set(V))==104,'104 paired ports')
    Fs=[span(f) for f in w['frames']];full=set(range(512));routechecks=0
    for v,x in zip(V,Xs):
        need(Fs[w['initial'][x]]=={0,v},'port/source-role correspondence');need(Fs[w['final'][x]]==full,'donor full hub')
        H={z for z in full if not odd(v&z)};need(Fs[w['final'][x+112]]==H,'receiver final hyperplane');need(Fs[w['initial'][x+112]]<=H,'receiver initial hyperplane')
        for e in w['program']:
            if e[0]=='MOVE' and e[1]==x:need(v in Fs[e[2]] and v in Fs[e[3]],'donor route contains line');routechecks+=1
            if e[0]=='MOVE' and e[1]==x+112:need(Fs[e[2]]<=H and Fs[e[3]]<=H,'receiver route inside hyperplane');routechecks+=1
    allV=[sum(1<<k for k in S) for d in [3,7] for S in combinations(range(9),d)];allA=[from_roots(v) for v in allV]
    need(all(row==piecewise(v) for row,v in zip(allA,allV)),'independent9D derivation');validate_gram(allV,allA)
    A=[from_roots(v) for v in V];validate_gram(V,A);rank,idx,rels=eliminate(A);need(rank==8,'source rank8');minor=det([A[i] for i in idx]);need(minor,'nonzero source minor')
    G=[[dot(x,y) for y in A] for x in A];side=[]
    for i,v in enumerate(V):
        terms=[]
        for j,z in enumerate(V):
            known=i!=j and not odd(v&z)
            if known:terms.append([Xs[j],str(Q(G[i][j],8))])
            need(Q(G[i][j],8)-(Q(G[i][j],8) if known else 0)==int(i==j),'complete decoder matrix')
        side.append({'receiver_role':Xs[i]+112,'source_role':Xs[i],'port':v,'correction_terms':terms})
    first=rels[0];need(all(sum(c*A[i][k] for i,c in first.items())==0 for k in range(8)),'empty-side-information kernel')
    mutant=[r[:] for r in A];mutant[0][0]+=1
    try:validate_gram(V,mutant)
    except ValueError as e:bad=str(e)
    else:raise ValueError('coefficient mutant accepted')
    removed=next(k for k in range(8) if A[0][k]);need(sum(x*x for k,x in enumerate(A[0]) if k!=removed)!=8,'omitted packet changes diagonal')
    i,j=next((i,j) for i in range(104) for j in range(i) if not odd(V[i]&V[j]));need(G[i][j]!=0,'opposite zero pattern rejected')
    omitted=sorted(set(allV)-set(V));manifest={'source_sha256':PIN,'roles':Xs,'ports':V,'rows':A,'corrections':side}
    a.output.parent.mkdir(parents=True,exist_ok=True);(a.output.parent/'CERTIFICATE.json').write_text(json.dumps(manifest,indent=2)+'\n')
    result={'status':'PASS_INDEPENDENT_DYADIC_EIGHT_PACKET_CODE','source_sha256':PIN,'universal_ports':len(allV),'universal_pair_checks':7140,'active_ports':104,'active_weight_counts':dict(collections.Counter(v.bit_count() for v in V)),'excluded_from_weight3_or7':omitted,'excluded_weight_counts':dict(collections.Counter(v.bit_count() for v in omitted)),'source_rank':rank,'source_minor_roles':[Xs[i] for i in idx],'source_minor_ports':[V[i] for i in idx],'source_minor_determinant':str(minor),'source_route_incidences_checked':routechecks,'ordered_orthogonal_corrections':sum(len(s['correction_terms']) for s in side),'encoder_nonzeros':sum(bool(x) for row in A for x in row),'correction_degree_counts':dict(collections.Counter(len(s['correction_terms']) for s in side)),'empty_side_information_kernel':[[Xs[i],str(c)] for i,c in sorted(first.items())],'coefficient_mutant_rejected':bad,'omitted_packet_coordinate':removed+1,'opposite_pattern_failure':{'roles':[Xs[i],Xs[j]],'ports':[V[i],V[j]],'binary_dot':0,'gram':G[i][j]},'new_complete_kappa':None,'scope':'Conditional on actual side-information delivery, scheduling, all endpoint restoration and a complete invoice.'}
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);main(p.parse_args())
