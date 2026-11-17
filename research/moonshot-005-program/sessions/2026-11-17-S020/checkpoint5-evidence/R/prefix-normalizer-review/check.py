"""Independent exact primitive replay and fixed-prefix native normalization."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,hashlib,importlib.util,json
PIN='410c8426e31bc60e76d88095b2ef568c766b46f6dd5a66ff9e8ae9a980a542e2'
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    helper=a.repo/'research/moonshot-005-program/sessions/2026-11-17-S020/checkpoint2-evidence/C/klein-interface-review/check.py';assert hashlib.sha256(helper.read_bytes()).hexdigest()==PIN
    spec=importlib.util.spec_from_file_location('independent_Qi',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);I=m.eye();Z=[{}for _ in range(16)]
    def mul(*xs):
        out=m.eye(len(xs[0]))
        for x in xs:out=m.mm(out,x)
        return out
    def bm(B,C):return [[m.add(*(mul(B[i][k],C[k][j])for k in range(len(C))))for j in range(len(C[0]))]for i in range(len(B))]
    def tensor(B,C):return [{i*len(C)+j:m.times(x,y)for i,x in bc.items()for j,y in cc.items()}for bc in B for cc in C]
    R=m.mono([[((x>>1)&1)+2*((x>>2)&1)+4*((x>>3)&1)+8*(x&1),2*((x&1)*((x>>1)&1)*((x>>3)&1))]for x in range(16)])
    X=m.mono([[x^2,0]for x in range(16)]);Zb=m.mono([[x,2*((x>>1)&1)]for x in range(16)]);D=m.mono([[x,(x>>1)&1]for x in range(16)])
    A=mul(m.add(m.scale(I,(F(1,2),F(1,2))),m.scale(X,(F(1,2),F(-1,2)))),R)
    mon={'I':I,'X':X,'Z':Zb,'ZX':mul(Zb,X),'R':R,'Ri':m.star(R),'D':D,'Di':m.star(D)}
    words=json.loads((a.author/'WORDS.json').read_text());assert set(words)=={'forward','inverse'}
    expected={'forward':[[A,Z],[Z,I]],'inverse':[[m.star(A),Z],[Z,I]]}
    def replay(ops,omit=None,bound=False):
        B=[[I,Z],[Z,I]];maximum=F(1)
        for k,op in enumerate(ops):
            if k==omit:continue
            if op['op']=='ADD':
                target,source=op['target'],op['source'];assert target!=source;B[target]=[m.add(x,y)for x,y in zip(B[target],B[source])]
            elif op['op']=='SCALE':
                c=tuple(map(F,op['coefficient']));assert c!=(0,0)and all(x.denominator&(x.denominator-1)==0 for x in c);b=op['bank'];B[b]=[m.scale(x,c)for x in B[b]]
            else:
                assert op['op']=='MONO';g=mon[op['name']];g=m.star(g)if op['inverse']else g;b=op['bank'];B[b]=[mul(g,x)for x in B[b]]
            if bound:
                for row in B:
                    sums=[F(0)]*16
                    for block in row:
                        for column in block:
                            for i,(re,im)in column.items():sums[i]+=abs(re)+abs(im)
                    maximum=max(maximum,*sums)
        return B,maximum
    counts={};bounds={};failures=0
    for name,ops in words.items():
        counts[name]=dict(Counter(x['op']for x in ops));assert counts[name]=={'ADD':24,'SCALE':48,'MONO':38}
        actual,bound=replay(ops,bound=True);assert actual==expected[name]and bound==3;bounds[name]=str(bound)
        for i,op in enumerate(ops):
            if op['op']=='ADD':assert replay(ops,omit=i)[0]!=expected[name];failures+=1
    identity=[[I,Z],[Z,I]];assert bm(expected['forward'],expected['inverse'])==bm(expected['inverse'],expected['forward'])==identity and failures==48
    for u,v in[(0,1),(1,0)]:
        for lam in[(F(-1),F(0)),(F(1,2),F(-1,2)),(F(0),F(-1))]:
            P=m.scale(m.add(X,m.scale(mon['ZX'],(-1)**u)),m.times(lam,(F(1,2),F(0))));Q=m.scale(m.add(I,m.scale(Zb,(-1)**v)),F(1,2))
            assert mul(P,Q)==P and mul(Q,P)==Z and mul(P,P)==Z
            E01=lambda c:[[I,c],[Z,I]];E10=lambda c:[[I,Z],[c,I]]
            comm=bm(bm(bm(E01(P),E10(Q)),E01(m.scale(P,-1))),E10(m.scale(Q,-1)))
            assert comm==[[m.add(I,P),Z],[Z,I]]
    controls=[]
    for width in[1,2]:
        tail=m.eye(1)if width==1 else A;identity_tail=m.eye(16**(width-1));prefix=tensor(A,identity_tail);body=tensor(I,tail);source=mul(prefix,body);n=16**width;Iv=m.eye(n);Zv=[{}for _ in range(n)]
        assert mul(body,prefix)==source and source==(A if width==1 else tensor(A,A))
        left=[[m.star(prefix),Zv],[Zv,Iv]];right=[[Iv,Zv],[Zv,m.star(prefix)]]
        lower=[[source,Zv],[Iv,source]];upper=[[source,m.scale(mul(source,source),-1)],[Zv,source]]
        want_lower=[[body,Zv],[Iv,body]];want_upper=[[body,m.scale(mul(body,body),-1)],[Zv,body]]
        assert bm(bm(left,lower),right)==want_lower and bm(bm(left,upper),right)==want_upper
        assert bm(left,lower)!=want_lower and bm(upper,right)!=want_upper
        controls.append({'width':width,'all_native_input_columns':2*n,'both_native_types':True,'missing_control_rejected':True})
    result={'status':'PASS_INDEPENDENT_PAID_PREFIX_NATIVE_NORMALIZER','arithmetic_sha256':PIN,'author_words_sha256':hashlib.sha256((a.author/'WORDS.json').read_bytes()).hexdigest(),'author_proof_sha256':hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest(),'counts':counts,'uniform_prefix_bounds':bounds,'omitted_ADD_controls':failures,'all_width_basis':'Exact finite-prefix operator identities tensor the identity; native gauges use a=p*b=b*p. Borrowed bank is restored as an arbitrary input column.','native_controls':controls,'three_native_additional':{'ADD':144,'SCALE':288,'MONO':228},'scope':'Local primitive compiler only; full model compiler, whole caller invoice and target-prefix restoration remain explicit.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],failures,'omission controls')
if __name__=='__main__':main()
