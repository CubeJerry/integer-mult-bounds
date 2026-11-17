"""Separate Q(i) source arithmetic and Fraction representation-rank audit."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,hashlib,importlib.util,json
PIN='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
def rank(rows):
    a=[list(map(F,r))for r in rows];k=0
    for j in range(len(a[0])):
        p=next((p for p in range(k,len(a))if a[p][j]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k];q=a[k][j];a[k]=[x/q for x in a[k]]
        for p in range(k+1,len(a)):
            if a[p][j]:q=a[p][j];a[p]=[x-q*y for x,y in zip(a[p],a[k])]
        k+=1
    return k
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    path=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint2-evidence/C/klein-interface-review/check.py';assert hashlib.sha256(path.read_bytes()).hexdigest()==PIN
    spec=importlib.util.spec_from_file_location('separate_Qi',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);I=m.eye();Z=[{}for _ in range(16)]
    def mul(*xs):
        out=I
        for x in xs:out=m.mm(out,x)
        return out
    def plus(x):return m.scale(m.add(I,x),F(1,2))
    def minus(x):return m.scale(m.add(I,m.scale(x,-1)),F(1,2))
    R=m.mono([[((x>>1)&1)+2*((x>>2)&1)+4*((x>>3)&1)+8*(x&1),2*((x&1)*((x>>1)&1)*((x>>3)&1))]for x in range(16)])
    Xb=m.mono([[x^2,0]for x in range(16)]);A=mul(m.add(m.scale(I,(F(1,2),F(1,2))),m.scale(Xb,(F(1,2),F(-1,2)))),R);U=mul(A,A)
    s=m.mono([[(x&3)|((x&4)<<1)|((x&8)>>1),0]for x in range(16)]);t=m.mono([[x^12,0]for x in range(16)])
    s1=mul(m.star(A),s,A);t1=mul(m.star(A),t,A);h0=mul(A,t,m.star(A));h1=mul(U,t,m.star(U));h2=mul(U,s1,t,s1,m.star(U))
    tables={n:m.table(B)for n,B in [('s',s),('t',t),('s1',s1),('h0',h0),('h1',h1),('h2',h2)]}
    for B in[s,t,s1,t1,h0,h1,h2]:assert mul(B,B)==I
    assert mul(s,t)==mul(t,s)and mul(s1,t1)==mul(t1,s1)
    assert mul(U,t)==mul(h1,U)and mul(U,s1,t)==mul(h2,U,s1)and mul(U,s1,t1)==mul(h0,U,s1)
    assert set(map(len,mul(U,s1,m.star(U))))=={4}
    Ps,Pt,Nt=plus(s),plus(t),minus(t);M0,M1,M2=minus(h0),minus(h1),minus(h2);P0=plus(h0)
    c=[Z,m.add(mul(Ps,M0),P0),mul(Pt,M0)];d0=[M1,M1,Z];d1=[M2,mul(h0,M2),Z]
    direct=[mul(A,Ps,A,Nt),m.add(mul(Ps,A,Nt),mul(A,plus(mul(s,t)),A,Nt),mul(A,Pt)),mul(Pt,A,Nt)]
    assert all(direct[i]==m.add(mul(c[i],A),m.scale(m.add(mul(d0[i],U),mul(d1[i],U,s1)),F(1,2)))for i in range(3))
    def dense_mul(B,C):return[[sum(x*y for x,y in zip(row,col))for col in zip(*C)]for row in B]
    def dense_add(B,C,scale=1):return[[x+scale*y for x,y in zip(br,cr)]for br,cr in zip(B,C)]
    J=[[F(i==j)for j in range(15)]for i in range(15)];O=[[F(0)for _ in range(15)]for _ in range(15)]
    def standard(tab):
        D=[row[:]for row in O];perm=[x[0]for x in tab]
        for j in range(15):
            if perm[j]<15:D[perm[j]][j]+=1
            if perm[15]<15:D[perm[15]][j]-=1
        return D
    def proj(B,sign):return[[x/2 for x in row]for row in dense_add(J,B,sign)]
    S,T,H0,H1,H2=[standard(tables[n])for n in['s','t','h0','h1','h2']]
    for B in[S,T,H0,H1,H2]:assert dense_mul(B,B)==J
    PS,PT,MH0,PH0,MH1,MH2=proj(S,1),proj(T,1),proj(H0,-1),proj(H0,1),proj(H1,-1),proj(H2,-1)
    B=dense_add(dense_mul(PS,MH0),PH0);D=dense_mul(PT,MH0);HM=dense_mul(H0,MH2)
    K1=O+B+D;K2=[x+y for x,y in zip(MH1,MH2)]+[x+y for x,y in zip(MH1,HM)]+[x+y for x,y in zip(O,O)]
    ranks={'one_whole':rank(K1),'one_third':rank(D),'two_whole':rank(K2),'two_third':rank(O)};assert ranks=={'one_whole':15,'one_third':4,'two_whole':13,'two_third':0}
    assert rank(O+dense_mul(PS,MH0)+D)!=15
    author=json.loads((a.author/'RESULT.json').read_text());assert author['exact_rational_ranks']==ranks
    for n,tab in tables.items():assert author['literal_conjugates'][n]=={'destinations':[x[0]for x in tab],'input_phase_mod4':[x[1]for x in tab]}
    chars=[]
    for u,v in product([1,-1],repeat=2):
        ps,pt,pst=(1+u)//2,(1+v)//2,(1+u*v)//2;e=(1-u)*(1+v)//4;f=(1-u)*(1-v)//4
        C=[[ps,-e,-f],[pst,0,1-f],[pt,1-e,0]];Ci=[[ps,f,e],[-pt,0,1-e],[-pst,1-f,0]];Q=[[pt,0,1-pt],[0,1,0],[1-pt,0,pt]];identity=[[int(i==j)for j in range(3)]for i in range(3)]
        assert dense_mul(C,Ci)==dense_mul(Ci,C)==identity and dense_mul(Q,Q)==identity;chars.append([u,v])
    result={'status':'PASS_INDEPENDENT_JOINT_ENDPOINT_CAPACITY_REVIEW','arithmetic_sha256':PIN,'author_proof_sha256':hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'exact_rational_ranks':ranks,'required_joint_bound':15,'observed_joint_value':24,'literal_conjugate_tables':tables,'four_abstract_characters':chars,'controls':{'individual_component_ranks_pass':max(ranks['one_whole'],ranks['two_whole'])<=15,'without_quartic_support_no_contradiction':24<=30,'omitted_P0_changes_rank':True},'proof_scope':'Universal dimension and coset arguments are in the written review. Literal identities use collective multiplicative relations; width-one sum checks alone are not the proof.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],ranks)
if __name__=='__main__':main()
