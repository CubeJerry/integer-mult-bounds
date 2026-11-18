"""Independent exact extension and scope controls; imports no author code."""
from argparse import ArgumentParser
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

def require(ok,label):
    if not ok:raise AssertionError(label)

# F4 = F2[w]/(w^2+w+1), represented in the ordered basis (1,w).
def mul(a,b):
    z=0
    for _ in range(2):
        if b&1:z^=a
        b>>=1;a<<=1
        if a&4:a^=7
    return z
def addm(a,b):return tuple(tuple(x^y for x,y in zip(r,s)) for r,s in zip(a,b))
def mm(a,b):
    out=[]
    for r in a:
        row=[]
        for c in zip(*b):
            z=0
            for x,y in zip(r,c):z^=mul(x,y)
            row.append(z)
        out.append(tuple(row))
    return tuple(out)
def mv(a,v):return tuple(row[0] for row in mm(a,tuple((x,) for x in v)))
def av(a,b):return tuple(x^y for x,y in zip(a,b))
def det2(a):return mul(a[0][0],a[1][1])^mul(a[0][1],a[1][0])
def inv2(a):
    d=det2(a);require(d!=0,'inverse exists');di=mul(d,d)
    return tuple(tuple(mul(di,x) for x in row) for row in ((a[1][1],a[0][1]),(a[1][0],a[0][0])))
def diagonal(a):return all(not a[i][j] for i in range(len(a)) for j in range(len(a)) if i!=j)
def direct(a,b):
    return tuple(tuple(row)+(0,)*len(b) for row in a)+tuple((0,)*len(a)+tuple(row) for row in b)

def main():
    ap=ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--author-proof',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();here=Path(__file__).resolve().parent
    pins=json.loads((here/'SOURCE-PINS.json').read_text())
    require(sha256(args.author_proof.read_bytes()).hexdigest()==pins['author_proof_sha256'],'reviewed author proof pin')
    for p,h in pins['dependencies'].items():require(sha256((args.repo/p).read_bytes()).hexdigest()==h,p)
    Z=((0,0),(0,0));I=((1,0),(0,1));M=((0,1),(1,1));M2=mm(M,M)
    require(addm(addm(M2,M),I)==Z,'irreducible separable multiplication polynomial')
    field=[Z,I,M,addm(I,M)]
    for a,b in product(range(4),repeat=2):
        require(mm(field[a],field[b])==field[mul(a,b)],'multiplication representation')
        require(mm(field[a],field[b])==mm(field[b],field[a]),'common commuting algebra')
    for a,x in product(range(4),repeat=2):
        y=mv(field[a],(x&1,x>>1));require(y[0]+2*y[1]==mul(a,x),'literal base-field multiplication map')
    S=((1,1),(2,3));Si=inv2(S)
    require(mm(Si,S)==mm(S,Si)==I,'extension common basis inverse')
    require(mm(mm(Si,M),S)==((2,0),(0,3)),'explicit extension eigenvalues')
    diagonals=[mm(mm(Si,c),S) for c in field]
    require(all(diagonal(c) for c in diagonals),'simultaneous extension diagonalization')
    gl4=[];gl2=[]
    for entries in product(range(4),repeat=4):
        a=(entries[:2],entries[2:])
        if det2(a):
            gl4.append(a)
            if all(x<2 for x in entries):gl2.append(a)
    require(len(gl4)==180 and len(gl2)==6,'exhaustive small general linear groups')
    common=lambda family,group:sum(all(diagonal(mm(mm(inv2(s),c),s)) for c in family) for s in group)
    require(common(field,gl2)==0,'a common base-field eigenbasis does not exist')
    require(common(field,gl4)==18,'all common extension eigenbases counted')
    blockS=direct(S,S);blockSi=direct(Si,Si)
    blocks=[direct(a,b) for a,b in product(field,repeat=2)]
    require(all(diagonal(mm(mm(blockSi,c),blockS)) for c in blocks),'direct sums retain the common basis')
    require(all(mm(c,d)==mm(d,c) for c,d in product(blocks,repeat=2)),'direct sum algebra commutativity')
    vectors=list(product(range(4),repeat=2));quotients=0
    for i,j in product(range(4),repeat=2):
        for xt,yt in product(vectors,repeat=2):
            z=av(mv(field[i],mv(S,xt)),mv(field[j],mv(S,yt)))
            zt=av(mv(diagonals[i],xt),mv(diagonals[j],yt))
            require(mv(Si,z)==zt,'common conjugation preserves every source quotient');quotients+=1
    native=0;kernel=0
    for x,y,z in product(vectors,repeat=3):
        lhs=(mv(S,av(x,y)),mv(S,av(y,z)))
        rhs=(av(mv(S,x),mv(S,y)),av(mv(S,y),mv(S,z)))
        require(lhs==rhs,'binary canonical map intertwines the same common basis');native+=1
        if av(x,y)==(0,0) and av(y,z)==(0,0):
            require(rhs==((0,0),(0,0)),'canonical zero slice preserved');kernel+=1
    require(kernel==16,'two-dimensional canonical kernel over F4')
    # The componentwise lift of binary Toffoli is a bijection on K^3.
    # It differs from substituting K multiplication into its old formula.
    lift=lambda x,y,z:(x,y,z^(x&y))
    outputs=set();different=0
    for x,y,z in product(range(4),repeat=3):
        image=lift(x,y,z);outputs.add(image)
        require(lift(*image)==(x,y,z),'componentwise nonlinear lift has the same inverse')
        different+=image!=(x,y,z^mul(x,y))
    require(len(outputs)==64 and different>0,'lift preserves the full alphabet without polynomial scalar extension')
    require(lift(2,2,0)==(2,2,2) and mul(2,2)==3,'explicit wrong polynomial-extension control')
    D=((1,0),(0,0));T=((1,1),(0,1));Dp=mm(mm(T,D),inv2(T))
    require(mm(D,D)==D and mm(Dp,Dp)==Dp,'both separate-donor families are semisimple')
    require(mm(D,Dp)!=mm(Dp,D),'separate donor bases need not share a commuting algebra')
    require(common([D,Dp],gl4)==0,'different donor bases have no common extension eigenbasis')
    require(mm(M,D)!=mm(D,M) and common([M,D],gl4)==0,'noncommuting semisimple negative control')
    J=((0,1),(0,0));require(J!=Z and mm(J,J)==Z,'genuine nonzero nilpotent')
    require(common([J],gl4)==0,'Jordan block remains nondiagonalizable over the extension')
    require(mm(addm(I,J),addm(I,J))==I,'nontrivial Jordan unit control')
    v=(0,1)
    require(mv(T,v)!=v,'different source bases do not preserve one native sum')
    # Both inputs have transformed sum v, but original sums differ.
    require(av(mv(T,v),(0,0))!=av((0,0),v),'donor-specific sum ambiguity')
    covered=360*(204+2*23+630+2*249+3*2);uncovered=24*1436;single=11*540
    bound=covered+uncovered+single;need=(111-9)*5760
    require((covered,uncovered,single,bound,need,need-bound)==(498240,34464,5940,538644,587520,48876),'inherited cut invoice')
    result={'status':'PASS_INDEPENDENT_SEMISIMPLE_SOURCE_CONTROLS','F4_GL2_count':len(gl4),
      'F2_GL2_count':len(gl2),'common_F2_bases':0,'common_F4_bases':18,
      'source_quotient_conjugation_controls':quotients,'binary_native_conjugation_controls':native,
      'nonlinear_lift_inputs':64,'lift_differs_from_formal_K_polynomial_inputs':different,
      'direct_sum_family_size':len(blocks),'noncommuting_semisimple_control':True,
      'different_donor_basis_control':True,'nonzero_Jordan_control':True,
      'plane_bound':bound,'required_native_information':need,'deficit':need-bound,
      'author_proof_sha256':pins['author_proof_sha256'],'scope':'Corollary accepted under the inherited varying-stripe source and route hypotheses; controls are not a fresh native atlas replay.',
      'new_complete_kappa':False}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(result['status'])

if __name__=='__main__':main()
