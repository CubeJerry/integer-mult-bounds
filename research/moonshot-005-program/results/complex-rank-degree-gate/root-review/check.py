"""Independent exact monomial transport, clock and determinant checks."""
from pathlib import Path
import argparse, hashlib, importlib.util, itertools, json

def main():
    p=argparse.ArgumentParser();p.add_argument('--engine',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    spec=importlib.util.spec_from_file_location('root_gaussian',a.engine);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    mm=g.mm;mono=g.mono;I=mono(list(range(8)));Z=(0,0)
    def adj(M):return [[(M[j][i][0],-M[j][i][1]) for j in range(8)] for i in range(8)]
    def div(M,d):
        assert all(z[0]%d==z[1]%d==0 for row in M for z in row)
        return [[(z[0]//d,z[1]//d) for z in row] for row in M]
    def ismono(M):return all(sum(z!=Z for z in row)==1 for row in M) and all(sum(M[y][x]!=Z for y in range(8))==1 for x in range(8)) and all(z==Z or z in g.UNIT for row in M for z in row)
    def key(M):return tuple(z for row in M for z in row)
    def group(gens):
        seen={key(I):I};todo=[I]
        while todo:
            m=todo.pop()
            for q in gens:
                x=mm(m,q);k=key(x)
                if k not in seen:seen[k]=x;todo.append(x)
            assert len(seen)<=1024
        return list(seen.values())
    reports={};single_count=adjacent_count=0
    for f in [128,64,112,176]:
        A,perm,phase=g.native(f,3);S=mono(perm,phase);Sinv=adj(S);AA=mm(A,A);AAA=mm(AA,A)
        Hs=[mono(list(range(8)),[2 if x==j else 0 for x in range(8)]) for j in range(8)]
        for H in Hs:
            k=div(mm(mm(adj(A),H),A),4);J=div(mm(mm(A,H),adj(A)),4)
            assert ismono(k) and ismono(J)
            for e1,e2,e3,u,v in itertools.product(range(2),repeat=5):
                M=I
                for q in [A if e1 else I,H if u else I,A if e2 else I,k if v else I,A if e3 else I]:M=mm(M,q)
                r=e1+e2+e3
                assert all(sum(M[y][x]!=Z for y in range(8))==2**r for x in range(8))
                if r==3:assert M==mm(mm(A,H if u^v else I),AA)
                single_count+=1
        H7,H6=Hs[7],Hs[6];pair=mm(H7,H6)
        k7=div(mm(mm(adj(A),H7),A),4);k6=div(mm(mm(adj(A),H6),A),4)
        z=div(mm(mm(adj(AA),pair),AA),16);assert ismono(z)
        G=group([k7,k6,z]);H0=[I,H7,H6,pair]
        for q in G:
            assert ismono(q)
            assert ismono(div(mm(mm(A,q),adj(A)),4))
            assert ismono(div(mm(mm(AA,q),adj(AA)),16))
        for H,q,e in itertools.product(H0,G,itertools.product(range(2),repeat=3)):
            M=I
            for F in [A if e[0] else I,H,A if e[1] else I,q,A if e[2] else I]:M=mm(M,F)
            r=sum(e);assert all(sum(M[y][x]!=Z for y in range(8))==2**r for x in range(8))
            if r==3:
                kh=div(mm(mm(adj(A),H),A),4)
                ordinary=div(mm(mm(AA,mm(kh,q)),adj(AA)),16)
                assert ismono(ordinary) and M==mm(ordinary,AAA)
            adjacent_count+=1
        Db=mono(list(range(8)),[(x>>1)&1 for x in range(8)])
        h=mm(Sinv,Db);R=mm(mm(Sinv,Db),S)
        # Left has two unnormalized A factors; right has one.
        lhs=mm(mm(A,h),A);rhs=mm(mm(Db,A),R)
        assert lhs==[[(2*z[0],2*z[1]) for z in row] for row in rhs]
        wrong=mono(list(range(8)),[2*((x>>1)&1) for x in range(8)])
        wrongproduct=div(mm(mm(A,mm(Sinv,wrong)),A),4)
        assert ismono(wrongproduct)
        for H in [H7,H6]:
            reflection=mm(mm(adj(AA),H),AA)
            assert sorted(sum(reflection[y][x]!=Z for y in range(8)) for x in range(8))==[1]*4+[4]*4
        reports[str(f)]={'adjacent_group_order':len(G),'clock_identity':True,'wrong_sign_collapses_to_monomial':True}
    assert single_count==1024 and adjacent_count==2048
    out={'status':'PASS_INDEPENDENT_RANK_DEGREE_SOURCE_REVIEW','engine_sha256':hashlib.sha256(a.engine.read_bytes()).hexdigest(),
         'single_sector_paths':single_count,'adjacent_sector_paths':adjacent_count,'sources':reports,
         'normal_form_scope':'Explicit monomial reductions plus separately proved source square/cube forms; support counts alone are not the classification proof',
         'new_complete_kappa':False}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])

if __name__=='__main__':main()
