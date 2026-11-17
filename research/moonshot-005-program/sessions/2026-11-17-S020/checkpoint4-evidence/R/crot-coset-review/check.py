"""Independent exact sparse arithmetic for the Crot source-coset proof."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,importlib.util,json
PIN='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    path=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint2-evidence/C/klein-interface-review/check.py';assert hashlib.sha256(path.read_bytes()).hexdigest()==PIN
    spec=importlib.util.spec_from_file_location('separate_Qi',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);I=m.eye();Z=[{}for _ in range(16)]
    def mul(*xs):
        out=I
        for x in xs:out=m.mm(out,x)
        return out
    def neg(x):return m.scale(x,-1)
    def bm(B,C):return [[m.add(*(mul(B[i][k],C[k][j])for k in range(len(C))))for j in range(len(C[0]))]for i in range(len(B))]
    R=m.mono([[((x>>1)&1)+2*((x>>2)&1)+4*((x>>3)&1)+8*(x&1),2*((x&1)*((x>>1)&1)*((x>>3)&1))]for x in range(16)])
    X=m.mono([[x^2,0]for x in range(16)]);A=mul(m.add(m.scale(I,(F(1,2),F(1,2))),m.scale(X,(F(1,2),F(-1,2)))),R)
    s=m.mono([[(x&3)|((x&4)<<1)|((x&8)>>1),0]for x in range(16)]);A2=mul(A,A);A3=mul(A2,A)
    # All-column supports and moduli distinguish the retained Gaussian ranks.
    rank_controls=[]
    for k in range(1,5):
        B=m.power(A,k);assert all(len(col)==2**k for col in B)
        assert all(z[0]**2+z[1]**2==F(1,2**k)for col in B for z in col.values());rank_controls.append(k)
    reports=[]
    for sign in [1,-1]:
        T=m.scale(m.add(I,m.scale(s,sign)),F(1,2));N=m.add(I,neg(T));T1=mul(m.star(A),T,A);T2=mul(m.star(A2),T,A2)
        assert mul(T,T)==T and mul(N,N)==N and mul(T,N)==mul(N,T)==Z
        assert mul(A,T,A)==mul(A2,T1)and mul(A,T,A2)==mul(A3,T2)
        C=[[T,Z,neg(N)],[Z,I,Z],[N,Z,T]];Ci=[[T,Z,N],[Z,I,Z],[neg(N),Z,T]]
        L=[[A,Z,Z],[I,A,Z],[Z,Z,I]];U=[[A,neg(A2),Z],[Z,A,Z],[Z,Z,I]]
        B=[[mul(A,T,A),neg(mul(A,T,A2)),neg(mul(A,N))],[mul(T,A),mul(N,A2),neg(N)],[mul(N,A),neg(mul(N,A2)),T]]
        identity=[[I if i==j else Z for j in range(3)]for i in range(3)]
        assert bm(bm(L,C),U)==B and bm(C,Ci)==bm(Ci,C)==identity
        q=R;qi=m.star(R);H=m.add(s,m.mono([[x^4,0]for x in range(16)]));K1=m.add(neg(mul(N,q)),mul(T,H));K2=m.add(mul(T,q),mul(N,H))
        assert mul(q,T)!=mul(T,q)and mul(H,T)!=mul(T,H)
        assert m.add(neg(mul(qi,N,K1)),mul(qi,T,K2))==I
        assert mul(N,K1)==neg(mul(N,q))and mul(T,K2)==mul(T,q)
        assert m.add(neg(mul(N,K1)),mul(T,K2))==q
        assert m.add(mul(qi,N,K1),mul(qi,T,K2))!=I
        assert m.add(neg(mul(N,K1)),mul(T,K2))!=I
        reports.append({'sign':sign,'source_block_identity':True,'unit_inverse':True,'noncommuting_q_and_H':True,'frame_retraction':True,'transversality':True,'wrong_sign_and_missing_inverse_rejected':True})
    g=mul(m.star(R),X);clock=mul(m.star(R),m.mono([[x,(x>>1)&1]for x in range(16)]))
    assert mul(A,g,A)==R
    assert all(len(col)==2 for col in mul(A2,g,A))and all(len(col)==4 for col in mul(A2,g))
    assert all(len(col)==2 for col in mul(A,clock,A))and all(len(col)==2 for col in mul(A,clock))
    result={'status':'PASS_INDEPENDENT_CROT_SOURCE_COSET_REVIEW','arithmetic_sha256':PIN,'author_proof_sha256':hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'source_rank_controls':rank_controls,'projector_controls':reports,'return_controls_preserve_left_coset_distinction':True,'scope':'Written proof establishes the universal fixed finite tail-catalogue theorem with arbitrary finite matrix prefix. These exact controls are not a search-based impossibility proof.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])
if __name__=='__main__':main()
