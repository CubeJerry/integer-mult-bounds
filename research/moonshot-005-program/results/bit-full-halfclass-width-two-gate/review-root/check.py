#!/usr/bin/env python3
"""Independent full-halfclass source review; exact native algebra and quadrics.
Rank3 method follows the root's credited sharp14 census, independently of
Worker C's double-perpendicular author census. Apache-2.0.
"""
import argparse,gzip,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)
def bits(mask):
    while mask:
        b=mask&-mask;yield b.bit_length()-1;mask-=b
def mod_basis(matrix,p=523):
    basis={};chosen=[]
    for i,row in enumerate(matrix):
        row=[int(x)%p for x in row]
        for j,b in sorted(basis.items()):
            c=row[j]
            if c:row=[(x-c*y)%p for x,y in zip(row,b)]
        j=next((j for j,x in enumerate(row) if x),None)
        if j is not None:
            inv=pow(row[j],-1,p);basis[j]=[x*inv%p for x in row];chosen.append(i)
    return chosen
def mod_det(matrix,p=523):
    a=[[int(x)%p for x in r] for r in matrix];value=1
    for j in range(len(a)):
        pivot=next((i for i in range(j,len(a)) if a[i][j]),None)
        if pivot is None:return 0
        if pivot!=j:a[j],a[pivot]=a[pivot],a[j];value=-value
        q=a[j][j];value=value*q%p;inv=pow(q,-1,p)
        for i in range(j+1,len(a)):
            z=a[i][j]*inv%p;a[i]=[(x-z*y)%p for x,y in zip(a[i],a[j])]
    return value%p
def norm(v):
    v=list(map(F,v));scale=2 if sum(x*x for x in v)==1 else 1
    v=[x*scale for x in v];need(all(x.denominator==1 for x in v),'integer roots')
    v=list(map(int,v));need(sum(x*x for x in v)==4,'norm4 roots')
    if next(x for x in v if x)<0:v=[-x for x in v]
    return tuple(v)

def binary_basis(rows):
    piv={}
    for x in rows:
        while x:
            j=x.bit_length()-1
            if j in piv:x^=piv[j]
            else:piv[j]=x;break
    return list(piv.values())
def bspan(rows):
    out={0}
    for r in rows:out|={x^r for x in tuple(out)}
    return out
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def support(r):return tuple(i for i,x in enumerate(r) if x)
def symmetric(q):
    out=[[0]*7 for _ in range(7)]
    for v,(i,j) in zip(q,itertools.combinations_with_replacement(range(7),2)):
        out[i][j]=2*v if i==j else v
        if i!=j:out[j][i]=v
    return out
def split_norm(root,positive):
    removed=next(i for i,x in enumerate(root) if x);free=[i for i in range(8) if i!=removed];sign=[1 if i in positive else -1 for i in range(8)]
    q=[]
    for a,b in itertools.combinations_with_replacement(free,2):
        x=F(sign[a]*int(a==b))+F(sign[removed]*root[a]*root[b],root[removed]**2)
        if a!=b:x*=2
        need(x.denominator==1,'integer split-norm coefficients');q.append(int(x))
    return q
def padd(a,b):
    out=[0]*max(len(a),len(b))
    for i,v in enumerate(a):out[i]+=v
    for i,v in enumerate(b):out[i]+=v
    while len(out)>1 and out[-1]==0:out.pop()
    return out
def pmul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    while len(out)>1 and out[-1]==0:out.pop()
    return out
def pencil_minor(A,B,rows,cols):
    out=[0]
    for perm in itertools.permutations(range(3)):
        term=[(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))]
        for i,j in enumerate(perm):term=pmul(term,[A[rows[i]][cols[j]],B[rows[i]][cols[j]]])
        out=padd(out,term)
    return out

def main():
    p=argparse.ArgumentParser()
    for name in ['native','package','output']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();raw=a.native.read_bytes();need(hashlib.sha256(raw).hexdigest()=='51203e7fc75ba10bd3ac3f8e675759f47e13d262bea66b6600d1e515095cad78','native pin')
    need(hashlib.sha256((a.package/'PROOF.md').read_bytes()).hexdigest()=='90d856cc8bc55b9bb501a89b7a11f72e134cd952f0ff03a24854eee06923a398','frozen proof pin')
    n=json.loads(gzip.decompress(raw));e=json.loads(gzip.decompress((a.package/'output/EVIDENCE.json.gz').read_bytes()))
    R=[norm(n['frames'][str(n['start'][i])]['B'][0]) for i in range(111)]
    need(R[:8]==[tuple(2*int(i==j) for j in range(8)) for i in range(8)],'actual coordinate root ordering')
    K=[sum(int(i==j or dot(r,s)==0)<<j for j,s in enumerate(R)) for i,r in enumerate(R)]
    C=binary_basis(K);code=bspan(C);need(len(C)==9 and len(code)==512 and min(x.bit_count() for x in code if x)==48,'canonical code and distance')
    distances=[min(x.bit_count() for x in {c&~k for c in code} if x) for k in K]
    need(Counter(distances)=={18:7,19:24,20:52,21:16,22:11,23:1},'all restricted distances')
    grouped={}
    for i,r in enumerate(R):grouped.setdefault((support(r),sum(x<0 for x in r)%2),[]).append(i)
    groups=sorted(grouped.values(),key=lambda z:tuple(z));need({tuple(g) for g in groups}=={tuple(g) for g in e['groups']},'independently reconstructed partition')
    h=[sum(1<<j for j in g) for g in groups];B=binary_basis(C+h);RC={c for c in code if all((c&g).bit_count() in (0,len(G)) for g,G in zip(h,groups))}
    need(len(groups)==36 and len(B)==39 and len(RC)==64 and len(binary_basis(RC))==6,'reservoir and true quotient dimensions')
    localgroups=[{g for g,v in enumerate(h) if not v&~k} for k in K]
    local=[sum(h[g] for g in S) for S in localgroups]
    for i,k in enumerate(K):
        L=[h[g] for g in localgroups[i]];dim=39-len(binary_basis([b&~k for b in B]))
        need(dim==len(L)+int(i>=8)==len(binary_basis(L+[k])),'complete local scalar code equality')
        need((k in RC)==(i<8),'coordinate versus noncoordinate canonical part')
    patterns=sorted({support(r) for r in R[8:]});families=[(P,tuple(i for i in range(8) if i not in P)) for P in patterns if P<tuple(i for i in range(8) if i not in P)]
    need(len(families)==7 and len(patterns)==14,'seven complementary support families')
    family={i:next(f for f,pair in enumerate(families) if support(R[i]) in pair) for i in range(8,111)}
    wg={g for g,G in enumerate(groups) if len(G)<=2};X=sum(h[g] for g in wg)
    need(list(bits(X))==[0,1,2,3,4,5,6,7,9,11,46,50],'actual common twelve-port support')
    cross=0;maxunion=0
    for i,j in itertools.combinations(range(8,111),2):
        maxunion=max(maxunion,(local[i]|local[j]).bit_count())
        if family[i]!=family[j]:cross+=1;need(localgroups[i]&localgroups[j]<=wg,'all cross-family local intersections literal in W')
    need(maxunion==34 and cross==4543 and max(x.bit_count() for x in local[8:])==20,'all exact local size constraints')
    enlarged=[];sixcases=[];subcodes=0
    for f,pair in enumerate(families):
        fg={g for g,G in enumerate(groups) if support(R[G[0]]) in pair};need(len(fg)==4,'four halfclasses per family')
        XF=sum(h[g] for g in wg|fg);enlarged.append(XF)
        points=[i for i in range(8,111) if family[i]==f]
        need(XF.bit_count()<48 and all(localgroups[i]<=wg|fg for i in points),'family local lift fits strict distance bound')
        cur=[((),sum(1<<i for i in points))]
        for depth in range(6):cur=[(S+(i,),common&K[i]&~((1<<(i+1))-1)) for S,common in cur for i in bits(common)]
        for S,unused in cur:
            common=set.intersection(*(localgroups[i] for i in S));need(len(common)==2,'six-row literal intersection has two indicators')
            gs=[groups[g] for g in common];need(set(S)<=set(gs[0])|set(gs[1]) and all(set(S)&set(G) for G in gs),'all six receivers in and across both groups')
            need({support(R[G[0]]) for G in gs}==set(pair),'common groups on complementary coordinates')
            sixcases.append((f,S,tuple(sorted(tuple(G) for G in gs))))
        for j in range(8):
            need({c for c in RC if not(c&~K[j]&~XF)}=={0,K[j]},'coordinate canonical family kernel exactly one-dimensional')
            subcodes+=1
    need(len(sixcases)==501 and [x.bit_count() for x in enlarged]==[26,27,28,27,28,23,24],'complete family and six-root domains')
    expected_six={(x['family'],tuple(x['receivers']),tuple(sorted(tuple(e['groups'][g]) for g in x['common_groups']))) for x in e['common_six']}
    need(set(sixcases)==expected_six and subcodes==56,'independent six-domain and all coordinate family subcodes')
    print('independent quotient and local-space premises complete',flush=True)
    mon=list(itertools.combinations_with_replacement(range(7),2));cases=[]
    for i in range(8,111):cases.append(('noncoordinate_local',i,None,[j for j in bits(K[i]&~local[i]) if j!=i],27,support(R[i])))
    for i in range(111):cases.append(('outside_W',i,None,[j for j in bits(K[i]&~X) if j!=i],28,None))
    for f,pair in enumerate(families):
        for i in range(8):cases.append(('coordinate_family',i,f,[j for j in bits(K[i]&~enlarged[f]) if j!=i],26 if f==0 and i in (0,3) else 27,pair[0]))
    author_cases={(c['kind'],c['receiver'],c.get('family')):c for c in e['quadratic_minors']}
    need(len(cases)==len(author_cases)==270,'complete geometric case domain')
    certs=[];pencil_results=[]
    for kind,i,f,points,expected,positive in cases:
        old=author_cases[kind,i,f];need(set(points)==set(old['points']) and expected==old['rank'],'independent forced root set and target rank')
        removed=next(j for j,x in enumerate(R[i]) if x);free=[j for j in range(8) if j!=removed]
        points=list(reversed(points));rows=[[R[j][free[b]]*R[j][free[c]] for b,c in mon] for j in points]
        selected=mod_basis(rows);need(len(selected)==expected,'fresh prime523 rank lower certificate')
        chosen=[rows[j] for j in selected];cols=mod_basis(list(map(list,zip(*chosen))));need(len(cols)==expected,'fresh square minor columns')
        matrix=[[r[j] for j in cols] for r in chosen];det=mod_det(matrix);need(det!=0 and mod_det([matrix[0]]+matrix[:-1])==0,'new exact nonzero minor and duplicate-row control')
        item=dict(kind=kind,receiver=i,family=f,rank=expected,prime=523,minor_roots=[points[j] for j in selected],minor_columns=cols,residue=det)
        if expected==27:
            q=split_norm(R[i],positive);need(any(q) and all(dot(r,q)==0 for r in rows),'independently derived unique split-norm kernel')
            need(mod_det(symmetric(q))!=0,'rank7 quadratic cannot be a hyperplane product')
            item['quadratic_kernel']=q
        elif expected==26:
            pc=e['nonfactorable_pencils'][old['pencil_index']];q0,q1=pc['quadratic_basis'];need(len(mod_basis([q0,q1]))==2,'independent two-kernel basis')
            need(all(dot(r,q0)==dot(r,q1)==0 for r in rows),'exact full quadratic pencil')
            A0,A1=symmetric(q0),symmetric(q1);need(mod_det(A1)!=0,'infinity member rank7')
            p0=pencil_minor(A0,A1,pc['minor_p']['rows'],pc['minor_p']['columns']);p1=pencil_minor(A0,A1,pc['minor_q']['rows'],pc['minor_q']['columns'])
            need(p0==[1,0,-4] and p1==[0,0,0,8] and padd(pmul([1,0,4],p0),pmul([0,2],p1))==[1],'universal exact polynomial Bezout identity')
            pencil_results.append(dict(receiver=i,first_minor=p0,second_minor=p1,bezout=[1],infinity_rank=7))
        certs.append(item)
    need(len(pencil_results)==2,'both exceptional pencils proved nonfactorable')
    S1=[54,56,57,59,61,63,64];S2=[52,53,55,58,60,62,65];directions=[sum(1<<j for j in S) for S in (S1,S2)]
    need(not set(S1)&set(S2),'disjoint sharp-boundary supports')
    for word,S in zip(directions,(S1,S2)):
        need(all((word&g).bit_count() in (0,len(G)) for g,G in zip(h,groups)),'sharp boundary belongs to full reservoir')
        need(all(K[i]>>j&1 for i,j in itertools.combinations(S,2)),'sharp boundary orthogonal cliques')
        need(all(len(mod_basis([R[j] for j in S if j!=i]))==6 for i in S),'each changed foreign row has proper six-dimensional span')
    def lift(word,t):return sum(((word>>j)&1)<<(2*j+t) for j in range(111))
    canonical=[lift(c,t) for c in C for t in range(2)];fitting=[]
    for i,k in enumerate(K):
        word=directions[0] if i in S1 else directions[1] if i in S2 else k
        need(word>>i&1 and not word&~k,'sharp boundary diagonal and fitting zeros')
        fitting.extend(lift(word,t) for t in range(2))
    quotient=len(binary_basis(fitting+canonical))-len(binary_basis(canonical));need(quotient==4,'exact attained quotient threshold')
    out=dict(status='PASS_INDEPENDENT_FULL_HALFCLASS_WIDTH2_GATE',dimensions=dict(canonical=9,indicator=36,union=39,intersection=6,quotient=30),canonical_distance=48,restriction_distances=dict(Counter(distances)),local_identities=111,local_support_maximum=20,pair_union_maximum=maxunion,pair_checks=5253,cross_family_pairs=cross,family_support_sizes=[x.bit_count() for x in enlarged],common_six_cases=len(sixcases),coordinate_family_subcodes=subcodes,independent_geometric_minors=len(certs),prime=523,nonfactorable_pencils=pencil_results,boundary_quotient=quotient,boundary_chi=194,scope='Independent complete new source premises and separate universal proof review. All fields of characteristic2; width2; full halfclass scalar reservoir; quotient dimension at most3. No arbitrary-rank or physical packet inference; no new kappa.')
    a.output.mkdir(parents=True,exist_ok=True);(a.output/'RESULT.json').write_text(json.dumps(out,indent=2)+'\n')
    (a.output/'INDEPENDENT-MINORS.json.gz').write_bytes(gzip.compress(json.dumps(certs,sort_keys=True).encode(),mtime=0))
    print(out['status'])
if __name__=='__main__':main()

