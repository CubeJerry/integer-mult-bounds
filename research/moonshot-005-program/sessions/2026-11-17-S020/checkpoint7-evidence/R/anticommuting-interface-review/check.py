"""Independent exact changed-interface algebra and literal primitive review."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import argparse,hashlib,importlib.util,json
SOURCE_SHA='ed688f0178639153bec60b2e5a9864d005996df32621d7257b1353da56bb102a'
WORDS_SHA='ee9f47268e3a1265e506079abd1bf81b22cecab5dd3f184d26f71de50bb6c224'
PROOF_SHA='b3bca6ded41e227dafd8d22fe845c1892ad0302848a649f428aefa02c9515583'
NORMALIZER_SHA='910edc04d35cb414202ba275cbc25d1ca21755a7186c9820f88f5f2eecebfe42'

def build(m,s,width):
    c=s.case(m,width);I,Z=c['I'],c['Z'];mul,bm=c['mul'],c['bm'];half=c['half'];P,N,T,R=c['P'],c['N'],c['T'],c['X'];S,J,a=c['S'],c['J'],c['a']
    S2=c['tensor'](c['zs'],c['tp'](c['sab']));As=half(m.add(I,S));Bs=m.add(I,m.scale(As,-1));A2=half(m.add(I,S2));B2=m.add(I,m.scale(A2,-1))
    U=half(m.add(I,R));V=m.add(I,m.scale(U,-1));assert mul(T,R)==m.scale(mul(R,T),-1)
    assert mul(m.power(a,-2),S,m.power(a,2))==S2
    def rot(i,j,h):
        p=half(m.add(I,h));n=m.add(I,m.scale(p,-1));q=c['identity']();q[i][i]=q[j][j]=p;q[i][j]=m.scale(n,-1);q[j][i]=n;return q
    C=bm(bm(bm(c['diag'](I,J,I),rot(0,2,T)),rot(1,2,R)),rot(0,1,S))
    c00=m.add(mul(P,As),m.scale(mul(N,V,Bs),-1));c10=mul(J,U,Bs)
    c20=m.add(mul(N,As),mul(P,V,Bs));c21=m.add(m.scale(mul(N,Bs),-1),mul(P,V,As));c22=mul(P,U);c02=m.scale(mul(N,U),-1)
    assert C[0][0]==c00 and C[1][0]==c10 and C[2]==[c20,c21,c22] and C[0][2]==c02
    gram=m.add(mul(m.star(c00),c00),mul(m.star(c10),c10));kernel=mul(As,N)
    want=m.add(mul(As,P),mul(Bs,U),half(mul(Bs,V)));assert gram==want
    inverse_on_support=m.add(mul(As,P),mul(Bs,U),m.scale(mul(Bs,V),2));support=m.add(I,m.scale(kernel,-1))
    assert mul(gram,inverse_on_support)==mul(inverse_on_support,gram)==support
    assert mul(c00,kernel)==mul(c10,kernel)==Z and m.col_rank(kernel)==c['n']//4
    ordinary_gram=m.add(mul(m.star(c02),c02),mul(m.star(c22),c22));assert ordinary_gram==U
    right0=m.add(mul(As,N),m.scale(mul(Bs,V,P),2));right1=m.add(m.scale(mul(Bs,N),-1),m.scale(mul(As,V,P),2))
    assert m.add(mul(c20,right0),mul(c21,right1))==I
    assert m.col_rank(c20+c21)==c['n']
    H=m.scale(m.add(T,R),(F(1,2),F(1,2)));assert mul(H,m.star(H))==I and mul(H,U,m.star(H))==P
    p=mul(U,B2);z=mul(R,H,U,A2);w=V
    projectors=[mul(U,B2),mul(U,A2),V]
    assert [mul(m.star(q),q) for q in[p,z,w]]==projectors
    assert m.add(*projectors)==I and [m.col_rank(q) for q in projectors]==[c['n']//4,c['n']//4,c['n']//2]
    assert mul(N,A2,z)==z and mul(V,w)==w
    Q=bm(bm(bm(c['diag'](m.star(H),R,m.star(H)),c['route'](1,2,mul(P,A2))),c['route'](0,2,mul(P,B2))),c['diag'](I,I,H))
    assert [Q[i][2] for i in range(3)]==[p,z,w]
    ordinary=[[Z],[mul(c02,w)],[mul(c22,w)]]
    cubic=[[m.scale(mul(a,c00,a,a,z),-1)],[m.scale(mul(a,c10,a,a,z),-1)],[Z]]
    assert ordinary==cubic==[[Z],[Z],[Z]]
    linear=[[mul(a,C[0][2],w)],[m.add(mul(C[0][0],a,p),mul(C[0][1],a,z),mul(a,C[1][2],w))],[m.add(mul(C[2][0],a,p),mul(C[2][1],a,z))]]
    quadratic=[[m.add(mul(a,C[0][0],a,p),mul(a,C[0][1],a,z))],[m.add(mul(a,C[1][0],a,p),m.scale(mul(C[0][0],a,a,z),-1),mul(a,C[1][1],a,z))],[m.scale(mul(C[2][0],a,a,z),-1)]]
    full=bm(bm(bm(c['L'],C),c['U']),[[p],[z],[w]])
    assert full==[[m.add(linear[i][0],quadratic[i][0])] for i in range(3)]
    assert any(row[0]!=Z for row in linear) and any(row[0]!=Z for row in quadratic)
    Dt=c['tensor'](m.mono([[i,(i>>1)&1] for i in range(4)]),m.eye(16**width))
    mon={'I':I,'S':S,'T':T,'R':R,'J':J,'HPminus':m.add(N,mul(P,S2)),'HPplus':m.add(N,m.scale(mul(P,S2),-1)),'NX':R,'NZ':T,'NZX':mul(T,R),'ND':Dt}
    for q in mon.values():m.table(q);assert mul(q,m.star(q))==I
    c.update({'mon':mon,'units':{'Cprime':C,'Q0':Q},'new':locals()});return c

def expand(macros,normalizer):
    result=[];bound=[F(1)]*3;peak=F(1)
    for op in macros:
        if op['op']=='PREFIX_H':
            dest,helper,inverse=op['target'],op['helper'],op['inverse'];assert dest!=helper
            peak=max(peak,3*max(bound[dest],bound[helper]));bound[dest]*=2
            base=normalizer['inverse'][:-1] if inverse else normalizer['forward'][1:]
            phase={'op':'MONO','name':'ND','bank':dest,'inverse':inverse};result.append(phase)
            for original in base:
                q=original.copy()
                if q['op']=='MONO':q['name']={'X':'NX','Z':'NZ','ZX':'NZX','D':'ND'}[q['name']]
                for key in['bank','target','source']:
                    if key in q:q[key]={0:dest,1:helper}[q[key]]
                q['inherited_prefix']=True;result.append(q)
            result.append(phase)
        else:
            result.append(op)
            if op['op']=='ADD':bound[op['target']]+=bound[op['source']]
            elif op['op']=='SCALE':
                re,im=map(F,op['coefficient']);bound[op['bank']]*=abs(re)+abs(im)
        peak=max(peak,*bound)
    return result,peak

def walsh_rank(m,M,r):
    n=len(M);k=1<<r;assert m.mm(m.star(M),M)==m.eye(n)
    rows=[{} for _ in range(n)]
    for j,col in enumerate(M):
        for i,v in col.items():rows[i][j]=v
    alpha=(F(1),F(0))
    for _ in range(r):alpha=m.times(alpha,(F(1,2),F(1,2)))
    groups={}
    for row in rows:
        assert len(row)==k and all(m.div(v,alpha) in m.ROOTS for v in row.values())
        groups.setdefault(tuple(sorted(row)),[]).append(row)
    assert len(groups)==n//k
    for columns,block in groups.items():
        assert len(block)==k;first=block[0];anchor=columns[0];signs=[]
        for row in block:
            mask=0
            for pos,j in enumerate(columns):
                ratio=m.div(m.times(row[j],first[anchor]),m.times(row[anchor],first[j]))
                assert ratio in[(F(1),F(0)),(F(-1),F(0))]
                if ratio[0]==-1:mask|=1<<pos
            signs.append(mask)
        assert len(set(signs))==k and 0 in signs
        assert all(x^y in signs for x in signs for y in signs)
    return r

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--source-review',type=Path,required=True);ap.add_argument('--normalizer',type=Path,required=True);ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    assert hashlib.sha256(a.source_review.read_bytes()).hexdigest()==SOURCE_SHA
    assert hashlib.sha256((a.author/'WORDS.json').read_bytes()).hexdigest()==WORDS_SHA
    assert hashlib.sha256((a.author/'PROOF.md').read_bytes()).hexdigest()==PROOF_SHA
    assert hashlib.sha256((a.normalizer/'WORDS.json').read_bytes()).hexdigest()==NORMALIZER_SHA
    spec=importlib.util.spec_from_file_location('root_independent_prefix_source',a.source_review);s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s);m=s.arithmetic(a.repo)
    words=json.loads((a.author/'WORDS.json').read_text());nw=json.loads((a.normalizer/'WORDS.json').read_text());author=json.loads((a.author/'RESULT.json').read_text())
    counts={'Cprime':{'ADD':12,'SCALE':12,'MONO':7},'Q0':{'ADD':80,'SCALE':152,'MONO':120}};reports=[];omitted=0
    for width in[0,1]:
        c=build(m,s,width);receipt={}
        for name,ws in words.items():
            outputs={};bounds={}
            for direction in['forward','inverse']:
                literal,bound=expand(ws[direction+'_macros'],nw);assert literal==ws[direction]
                assert dict(Counter(op['op'] for op in literal))==counts[name]
                assert str(bound)==author['receipts'][name]['uniform_prefix_'+direction]
                actual,exact=s.primitive_replay(m,c,literal,measure=True);assert exact<=bound
                outputs[direction]=actual;bounds[direction]={'uniform':str(bound),'reduced_exact':str(exact)}
                if width==1:
                    for index,op in enumerate(literal):
                        if op['op']=='ADD':assert s.primitive_replay(m,c,literal,omit=index)[0]!=actual;omitted+=1
            assert outputs['forward']==c['units'][name]
            assert c['bm'](outputs['forward'],outputs['inverse'])==c['bm'](outputs['inverse'],outputs['forward'])==c['identity']()
            receipt[name]={'counts_both_directions':counts[name],'prefix_bounds':bounds}
            print('reviewed anticommuting tail width',width,name,flush=True)
        n=c['new'];mul=c['mul'];Z=c['Z'];P=c['P']
        assert mul(n['c00'],c['a'],c['a'])!=Z
        assert mul(n['c02'],n['U'])!=Z or mul(n['c22'],n['U'])!=Z
        assert c['bm']([[Z,Z,P]],c['bm'](c['bm'](c['L'],n['C']),c['U']))!=[[Z,Z,P]]
        reports.append({'tail_width':width,'all_unit_input_columns':3*c['n'],'last_column_input_columns':c['n'],'active_kernel_rank':c['n']//4,'ordinary_kernel_rank':c['n']//2,'column_initial_ranks':[c['n']//4,c['n']//4,c['n']//2],'third_row_right_inverse':True,'whole_column_only_linear_and_quadratic':True,'bad_cubic_column_rejected':True,'bad_ordinary_column_rejected':True,'old_low_class_selector_rejected':True,'units':receipt})
    assert omitted==184
    A,J,S,K,S1,S2=c['A'],c['j'],c['s'],c['k'],c['s1'],c['sab'];mul=c['mul']
    assert mul(A,J,A)==mul(K,m.power(A,2),S1)
    assert mul(A,J,S,A)==mul(K,m.power(A,2))
    assert mul(A,J,A,A)==mul(K,m.power(A,3),S2)
    assert mul(A,J,S,A,A)==mul(K,m.power(A,3))
    ranks={'A2':walsh_rank(m,m.power(A,2),2),'A3':walsh_rank(m,m.power(A,3),3)}
    result={'status':'PASS_INDEPENDENT_ANTICOMMUTING_PREFIX_INTERFACE','source_review_sha256':SOURCE_SHA,'author_words_sha256':WORDS_SHA,'author_proof_sha256':PROOF_SHA,'normalizer_words_sha256':NORMALIZER_SHA,'cases':reports,'all_primitive_ADD_omissions_rejected':omitted,'exact_base_Walsh_ranks':ranks,'monomial_source_head_transports':{'AJA':2,'AJSA':2,'AJA2':3,'AJSA2':3},'all_width_basis':'Fixed-prefix Pauli/projector algebra, exact tensor source transports, positive Gram support inverse, explicit third-row right inverse, and literal paid arbitrary-borrower unit words.','scope':'Positive Cprime/Q0 units and exact ordinary/cubic last-column cancellation. No whole-bank Gaussian endpoint factorization or complete supplier. Kernel necessity retains faithful fixed-catalogue class separation.','new_complete_kappa':False}
    a.out.mkdir(parents=True,exist_ok=True);(a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'],omitted,'literal omission controls',flush=True)
if __name__=='__main__':main()
