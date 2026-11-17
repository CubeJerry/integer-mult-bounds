"""Independent sparse exact replay of the distinguished-column plus unit."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,hashlib,importlib.util,json
PIN='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    helper=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint2-evidence/C/klein-interface-review/check.py';assert hashlib.sha256(helper.read_bytes()).hexdigest()==PIN
    spec=importlib.util.spec_from_file_location('independent_Qi',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);I=m.eye()
    def mul(*terms):
        out=m.eye(len(terms[0]))
        for term in terms:out=m.mm(out,term)
        return out
    R=m.mono([[((x>>1)&1)+2*((x>>2)&1)+4*((x>>3)&1)+8*(x&1),2*((x&1)*((x>>1)&1)*((x>>3)&1))]for x in range(16)])
    Xb=m.mono([[x^2,0]for x in range(16)]);A=mul(m.add(m.scale(I,(F(1,2),F(1,2))),m.scale(Xb,(F(1,2),F(-1,2)))),R)
    t=m.mono([[x^12,0]for x in range(16)]);h=mul(A,t,m.star(A));j=m.mono([[x,2*((x>>1)&1)]for x in range(16)]);ht=m.table(h);jt=m.table(j)
    assert mul(h,h)==mul(j,j)==I and mul(j,h)==m.scale(mul(h,j),-1)
    assert all(((dest^src)>>1)&1 for src,(dest,phase)in enumerate(ht))
    words=json.loads((a.author/'WORDS.json').read_text());assert all(Counter(x['op']for x in ws)=={'ADD':6,'SCALE':12,'MONO':8}for ws in words.values())
    def collective(tab,width):
        out=[]
        for x in range(16**width):
            dest=0;phase=0
            for k in reversed(range(width)):
                digit=(x//16**k)%16;d,z=tab[digit];dest+=d*16**k;phase+=z
            out.append([dest,phase%4])
        return m.mono(out)
    reports=[];failures=0
    for width in[1,2]:
        n=16**width;Iv=m.eye(n);Z=[{}for _ in range(n)];H=collective(ht,width);J=m.mono([[x,2*((x//16**(width-1)>>1)&1)]for x in range(n)])
        P=m.scale(m.add(Iv,H),F(1,2));M=m.scale(m.add(Iv,m.scale(H,-1)),F(1,2));identity=[[Iv,Z],[Z,Iv]]
        assert mul(J,H)==m.scale(mul(H,J),-1)and mul(P,J)==mul(J,M)
        assert mul(P,P)==P and mul(P,J,M)==mul(J,M)and m.add(mul(P,P),mul(M,J,J,M))==Iv
        expected={'forward':[[P,M],[mul(J,M),mul(J,P)]],'inverse':[[P,mul(M,J)],[M,mul(P,J)]]}
        def bankmul(B,C):return[[m.add(*(mul(B[i][k],C[k][j])for k in range(2)))for j in range(2)]for i in range(2)]
        assert bankmul(expected['forward'],expected['inverse'])==bankmul(expected['inverse'],expected['forward'])==identity
        def replay(ops):
            B=[[Iv,Z],[Z,Iv]]
            for op in ops:
                if op['op']=='ADD':
                    d,s=op['target'],op['source'];B[d]=[m.add(x,y)for x,y in zip(B[d],B[s])]
                elif op['op']=='SCALE':
                    b=op['bank'];B[b]=[m.scale(x,F(op['coefficient']))for x in B[b]]
                else:
                    assert op['op']=='MONO';b=op['bank'];g={'H':H,'J':J}[op['name']];B[b]=[mul(g,x)for x in B[b]]
            return B
        for name,ops in words.items():
            assert replay(ops)==expected[name]
            for i,op in enumerate(ops):
                if op['op']=='ADD':assert replay(ops[:i]+ops[i+1:])!=expected[name];failures+=1
        if width==2:
            wrong=collective(jt,width);assert mul(wrong,H)==mul(H,wrong)and mul(P,wrong,M)!=mul(wrong,M)
        reports.append({'width':width,'dimension_per_bank':n,'all_input_columns':2*n,'unit_inverse_and_plus_split':True,'omitted_ADD_controls':12})
    assert failures==24
    result={'status':'PASS_INDEPENDENT_DISTINGUISHED_COLUMN_PLUS_UNIT','arithmetic_sha256':PIN,'author_word_sha256':hashlib.sha256((a.author/'WORDS.json').read_bytes()).hexdigest(),'author_proof_sha256':hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'actual_h_table':ht,'actual_j_table':jt,'width_controls':reports,'primitive_counts_each_direction':{'ADD':6,'SCALE':12,'MONO':8},'uniform_prefix_bound':5,'incorrect_collective_J_rejected_at_width2':True,'all_width_proof':'One-column anticommutation tensor I on all remaining columns, projector algebra and three actual coefficient shears.','scope':'Explicit fixed distinguished-column template; mathematical/local invoice admission only. Full ordinary compiler and complete caller remain separate. Earlier fixed-collective gates unchanged.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],failures,'controls')
if __name__=='__main__':main()
